#!/usr/bin/env python3
"""Audit prospective term files for reuse of prior evidence terms."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.normalization import GREEK_LETTERS, HEBREW_LETTERS, normalize_text


OUT = Path("reports/study_locks/prospective_term_audit.csv")
LANGUAGE_FIELDS = (
    "language",
    "term_language",
    "target_language",
    "candidate_language",
    "corpus_language",
)
ID_FIELDS = ("term_id", "target_term_id", "candidate_term_id", "left_term_id", "right_term_id")
CONCEPT_FIELDS = ("concept", "target_concept", "candidate_concept")
CATEGORY_FIELDS = ("category", "target_category", "candidate_category")
NORMALIZED_VALUE_FIELDS = (
    "normalized_term",
    "normalized_query",
    "target_normalized",
    "candidate_normalized",
    "control_normalized",
    "matched_normalized",
    "extended_sequence",
    "extension_sequence",
    "sequence",
    "query",
)
RAW_VALUE_FIELDS = (
    "term",
    "target_term",
    "candidate_term",
    "control_term",
    "matched_phrase",
    "extended_phrase",
)
FIELDNAMES = [
    "severity",
    "relationship",
    "language",
    "normalized",
    "matched_length",
    "candidate_file",
    "candidate_row",
    "candidate_term_id",
    "candidate_concept",
    "candidate_category",
    "candidate_term",
    "candidate_normalized",
    "evidence_file",
    "evidence_row",
    "evidence_term_id",
    "evidence_concept",
    "evidence_category",
    "evidence_value_field",
    "evidence_value",
    "evidence_normalized",
]


@dataclass(frozen=True)
class CandidateTerm:
    path: Path
    row_number: int
    term_id: str
    concept: str
    category: str
    language: str
    term: str
    normalized: str


@dataclass(frozen=True)
class EvidenceValue:
    path: Path
    row_number: int
    term_id: str
    concept: str
    category: str
    language: str
    value_field: str
    value: str
    normalized: str


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    candidate_paths = expand_csv_paths(args.candidate)
    evidence_paths = expand_csv_paths(args.evidence)
    candidates, skipped_candidates = read_candidates(
        candidate_paths,
        min_normalized_length=args.min_normalized_length,
    )
    evidence, skipped_evidence = read_evidence_values(
        evidence_paths,
        min_normalized_length=1,
    )
    rows = audit_matches(
        candidates,
        evidence,
        include_substrings=not args.exact_only,
        min_substring_length=args.min_substring_length,
        include_self=args.include_self,
    )
    write_rows(args.out, rows)
    summary_path = args.summary_out or default_summary_out(args.out)
    write_summary(
        summary_path,
        {
            "tool": "audit_prospective_terms",
            "edls_version": __version__,
            "generated_at": datetime.now(UTC).isoformat(),
            "duration_seconds": round(time.perf_counter() - started, 6),
            "status": "matched" if rows else "passed",
            "candidate_files": [str(path) for path in candidate_paths],
            "evidence_files": [str(path) for path in evidence_paths],
            "candidate_rows": len(candidates),
            "evidence_values": len(evidence),
            "skipped_candidate_rows": skipped_candidates,
            "skipped_evidence_values": skipped_evidence,
            "match_rows": len(rows),
            "severity_counts": dict(Counter(row["severity"] for row in rows)),
            "relationship_counts": dict(Counter(row["relationship"] for row in rows)),
            "out": str(args.out),
        },
    )
    print(args.out)
    print(summary_path)
    if rows and args.fail_on_match:
        print(f"prospective term audit found {len(rows)} prior-evidence overlap rows")
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, action="append", required=True)
    parser.add_argument("--evidence", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--summary-out", type=Path)
    parser.add_argument("--min-normalized-length", type=int, default=1)
    parser.add_argument("--min-substring-length", type=int, default=4)
    parser.add_argument("--exact-only", action="store_true")
    parser.add_argument("--include-self", action="store_true")
    parser.add_argument("--fail-on-match", action="store_true")
    return parser


def expand_csv_paths(paths: list[Path]) -> list[Path]:
    expanded: list[Path] = []
    for path in paths:
        if path.is_dir():
            expanded.extend(sorted(path.rglob("*.csv")))
        else:
            expanded.append(path)
    return expanded


def read_candidates(
    paths: list[Path],
    *,
    min_normalized_length: int,
) -> tuple[list[CandidateTerm], int]:
    candidates: list[CandidateTerm] = []
    skipped = 0
    for path in paths:
        for row_number, row in read_csv_rows(path):
            language = row.get("language", "").strip()
            if not language:
                raise ValueError(f"{path}:{row_number}: candidate row missing language")
            term = row.get("term", "").strip()
            normalized = normalize_text(term, language)
            if len(normalized) < min_normalized_length:
                skipped += 1
                continue
            candidates.append(
                CandidateTerm(
                    path=path,
                    row_number=row_number,
                    term_id=row.get("term_id", "").strip(),
                    concept=row.get("concept", "").strip(),
                    category=row.get("category", "").strip(),
                    language=language,
                    term=term,
                    normalized=normalized,
                )
            )
    return candidates, skipped


def read_evidence_values(
    paths: list[Path],
    *,
    min_normalized_length: int,
) -> tuple[list[EvidenceValue], int]:
    evidence: list[EvidenceValue] = []
    skipped = 0
    for path in paths:
        for row_number, row in read_csv_rows(path):
            seen_values: set[tuple[str, str]] = set()
            for field, value in row_evidence_values(row):
                language = language_for_row(row, value)
                if not language:
                    skipped += 1
                    continue
                normalized = normalize_text(value, language)
                if len(normalized) < min_normalized_length:
                    skipped += 1
                    continue
                key = (language, normalized)
                if key in seen_values:
                    continue
                seen_values.add(key)
                evidence.append(
                    EvidenceValue(
                        path=path,
                        row_number=row_number,
                        term_id=first_present(row, ID_FIELDS),
                        concept=first_present(row, CONCEPT_FIELDS),
                        category=first_present(row, CATEGORY_FIELDS),
                        language=language,
                        value_field=field,
                        value=value,
                        normalized=normalized,
                    )
                )
    return evidence, skipped


def read_csv_rows(path: Path) -> list[tuple[int, dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [
            (row_number, {key: value or "" for key, value in row.items() if key is not None})
            for row_number, row in enumerate(reader, start=2)
        ]


def row_evidence_values(row: dict[str, str]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    for field in NORMALIZED_VALUE_FIELDS:
        value = row.get(field, "").strip()
        if value:
            values.append((field, value))
    for field in RAW_VALUE_FIELDS:
        value = row.get(field, "").strip()
        if value:
            values.append((field, value))
    return values


def language_for_row(row: dict[str, str], value: str) -> str:
    language = first_present(row, LANGUAGE_FIELDS)
    if language:
        return language
    return infer_language(value)


def first_present(row: dict[str, str], fields: tuple[str, ...]) -> str:
    for field in fields:
        value = row.get(field, "").strip()
        if value:
            return value
    return ""


def infer_language(value: str) -> str:
    if any(is_hebrew_char(char) for char in value):
        return "hebrew"
    if any(is_greek_char(char) for char in value):
        return "greek"
    return ""


def is_hebrew_char(char: str) -> bool:
    return char in HEBREW_LETTERS or 0x0590 <= ord(char) <= 0x05FF


def is_greek_char(char: str) -> bool:
    char = char.lower()
    return (
        char in GREEK_LETTERS
        or 0x0370 <= ord(char) <= 0x03FF
        or 0x1F00 <= ord(char) <= 0x1FFF
    )


def audit_matches(
    candidates: list[CandidateTerm],
    evidence_values: list[EvidenceValue],
    *,
    include_substrings: bool,
    min_substring_length: int,
    include_self: bool,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for candidate in candidates:
        for evidence in evidence_values:
            if candidate.language != evidence.language:
                continue
            if not include_self and is_same_row(candidate, evidence):
                continue
            relationship = match_relationship(
                candidate.normalized,
                evidence.normalized,
                include_substrings=include_substrings,
                min_substring_length=min_substring_length,
            )
            if not relationship:
                continue
            matched = matched_normalized(candidate.normalized, evidence.normalized, relationship)
            rows.append(match_row(candidate, evidence, relationship, matched))
    return sorted(
        rows,
        key=lambda row: (
            row["severity"],
            row["candidate_file"],
            row["candidate_term_id"],
            row["evidence_file"],
            row["evidence_row"],
            row["evidence_value_field"],
        ),
    )


def is_same_row(candidate: CandidateTerm, evidence: EvidenceValue) -> bool:
    return (
        candidate.path.resolve() == evidence.path.resolve()
        and candidate.row_number == evidence.row_number
        and candidate.term_id == evidence.term_id
    )


def match_relationship(
    candidate: str,
    evidence: str,
    *,
    include_substrings: bool,
    min_substring_length: int,
) -> str:
    if candidate == evidence:
        return "exact"
    if not include_substrings:
        return ""
    if len(candidate) < min_substring_length or len(evidence) < min_substring_length:
        return ""
    if evidence in candidate:
        return "candidate_contains_evidence"
    if candidate in evidence:
        return "evidence_contains_candidate"
    return ""


def matched_normalized(candidate: str, evidence: str, relationship: str) -> str:
    if relationship in {"exact", "candidate_contains_evidence"}:
        return evidence
    if relationship == "evidence_contains_candidate":
        return candidate
    return ""


def match_row(
    candidate: CandidateTerm,
    evidence: EvidenceValue,
    relationship: str,
    normalized: str,
) -> dict[str, str]:
    return {
        "severity": severity_for(relationship),
        "relationship": relationship,
        "language": candidate.language,
        "normalized": normalized,
        "matched_length": str(len(normalized)),
        "candidate_file": str(candidate.path),
        "candidate_row": str(candidate.row_number),
        "candidate_term_id": candidate.term_id,
        "candidate_concept": candidate.concept,
        "candidate_category": candidate.category,
        "candidate_term": candidate.term,
        "candidate_normalized": candidate.normalized,
        "evidence_file": str(evidence.path),
        "evidence_row": str(evidence.row_number),
        "evidence_term_id": evidence.term_id,
        "evidence_concept": evidence.concept,
        "evidence_category": evidence.category,
        "evidence_value_field": evidence.value_field,
        "evidence_value": evidence.value,
        "evidence_normalized": evidence.normalized,
    }


def severity_for(relationship: str) -> str:
    if relationship == "exact":
        return "block"
    return "review"


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def default_summary_out(out: Path) -> Path:
    return out.with_suffix(out.suffix + ".summary.json")


def write_summary(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
