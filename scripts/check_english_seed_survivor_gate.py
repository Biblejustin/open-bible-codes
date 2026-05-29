#!/usr/bin/env python3
"""Validate the English seed survivor gate remains closed when no rows survive."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_FOLLOWUP_SUMMARY = Path("reports/english_seed_shuffle_followup_100/summary.csv")
DEFAULT_SURVIVORS = Path("terms/english_seed_followup_survivors.csv")
DEFAULT_FOLLOWUP_DOC = Path("docs/ENGLISH_SEED_SHUFFLE_FOLLOWUP_REPORT.md")
DEFAULT_TERM_SHUFFLE_SUMMARY = Path("reports/english_seed_term_shuffle_1000/summary.csv")
DEFAULT_SURVIVOR_AUDIT_SUMMARY = Path("reports/english_seed_survivor_audit/summary.csv")
DEFAULT_SURVIVOR_AUDIT_LETTER_PATHS = Path(
    "reports/english_seed_survivor_audit/letter_paths.csv"
)
DEFAULT_SURVIVOR_AUDIT_DOC = Path("docs/ENGLISH_SEED_SURVIVOR_AUDIT.md")
DEFAULT_TARGET_SUMMARY = Path("reports/english_seed_survivor_targets/target_summary.csv")
DEFAULT_PAIRED_SUMMARY = Path("reports/english_seed_paired_controls_1000/summary.csv")
DEFAULT_PAIRED_EXAMPLES = Path("reports/english_seed_paired_controls_1000/examples.csv")
DEFAULT_PAIRED_DOC = Path("docs/ENGLISH_SEED_PAIRED_CONTROLS_1000.md")

SURVIVOR_FIELDNAMES = ["term_id", "concept", "category", "language", "term", "notes"]

FOLLOWUP_REQUIRED_PHRASES = (
    "No English seed row survived the 100-sample corpus-letter shuffle at p_ge <= 0.05",
    "The survivor list is therefore intentionally empty",
    "Downstream same-letter term shuffle, survivor audit, and paired-control survivor reports should not be treated as current",
)
SURVIVOR_AUDIT_REQUIRED_PHRASES = (
    "Status: no current survivor rows.",
    "survivor hit rows: 0",
    "downstream paired-control survivor reports idle",
)
PAIRED_REQUIRED_PHRASES = (
    "Status: no target rows.",
    "survivor gate has no rows",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_english_seed_survivor_gate(
        followup_summary=args.followup_summary,
        survivors=args.survivors,
        followup_doc=args.followup_doc,
        term_shuffle_summary=args.term_shuffle_summary,
        survivor_audit_summary=args.survivor_audit_summary,
        survivor_audit_letter_paths=args.survivor_audit_letter_paths,
        survivor_audit_doc=args.survivor_audit_doc,
        target_summary=args.target_summary,
        paired_summary=args.paired_summary,
        paired_examples=args.paired_examples,
        paired_doc=args.paired_doc,
        threshold=args.threshold,
    )
    if failures:
        for failure in failures:
            print(f"English seed survivor gate failure: {failure}", file=sys.stderr)
        return 1
    print("English seed survivor gate ok")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--followup-summary", type=Path, default=DEFAULT_FOLLOWUP_SUMMARY)
    parser.add_argument("--survivors", type=Path, default=DEFAULT_SURVIVORS)
    parser.add_argument("--followup-doc", type=Path, default=DEFAULT_FOLLOWUP_DOC)
    parser.add_argument(
        "--term-shuffle-summary", type=Path, default=DEFAULT_TERM_SHUFFLE_SUMMARY
    )
    parser.add_argument(
        "--survivor-audit-summary", type=Path, default=DEFAULT_SURVIVOR_AUDIT_SUMMARY
    )
    parser.add_argument(
        "--survivor-audit-letter-paths",
        type=Path,
        default=DEFAULT_SURVIVOR_AUDIT_LETTER_PATHS,
    )
    parser.add_argument("--survivor-audit-doc", type=Path, default=DEFAULT_SURVIVOR_AUDIT_DOC)
    parser.add_argument("--target-summary", type=Path, default=DEFAULT_TARGET_SUMMARY)
    parser.add_argument("--paired-summary", type=Path, default=DEFAULT_PAIRED_SUMMARY)
    parser.add_argument("--paired-examples", type=Path, default=DEFAULT_PAIRED_EXAMPLES)
    parser.add_argument("--paired-doc", type=Path, default=DEFAULT_PAIRED_DOC)
    parser.add_argument("--threshold", type=float, default=0.05)
    return parser


def validate_english_seed_survivor_gate(
    *,
    followup_summary: Path = DEFAULT_FOLLOWUP_SUMMARY,
    survivors: Path = DEFAULT_SURVIVORS,
    followup_doc: Path = DEFAULT_FOLLOWUP_DOC,
    term_shuffle_summary: Path = DEFAULT_TERM_SHUFFLE_SUMMARY,
    survivor_audit_summary: Path = DEFAULT_SURVIVOR_AUDIT_SUMMARY,
    survivor_audit_letter_paths: Path = DEFAULT_SURVIVOR_AUDIT_LETTER_PATHS,
    survivor_audit_doc: Path = DEFAULT_SURVIVOR_AUDIT_DOC,
    target_summary: Path = DEFAULT_TARGET_SUMMARY,
    paired_summary: Path = DEFAULT_PAIRED_SUMMARY,
    paired_examples: Path = DEFAULT_PAIRED_EXAMPLES,
    paired_doc: Path = DEFAULT_PAIRED_DOC,
    threshold: float = 0.05,
) -> list[str]:
    failures: list[str] = []
    failures.extend(validate_followup_summary(followup_summary, threshold=threshold))
    failures.extend(validate_survivor_terms(survivors))
    for path, label in (
        (term_shuffle_summary, "term-shuffle summary"),
        (survivor_audit_summary, "survivor-audit summary"),
        (survivor_audit_letter_paths, "survivor-audit letter paths"),
        (target_summary, "survivor target summary"),
        (paired_summary, "paired-control summary"),
        (paired_examples, "paired-control examples"),
    ):
        failures.extend(validate_empty_data_rows(path, label))
    failures.extend(validate_doc(followup_doc, FOLLOWUP_REQUIRED_PHRASES))
    failures.extend(validate_doc(survivor_audit_doc, SURVIVOR_AUDIT_REQUIRED_PHRASES))
    failures.extend(validate_doc(paired_doc, PAIRED_REQUIRED_PHRASES))
    return failures


def validate_followup_summary(path: Path, *, threshold: float) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if "p_greater_equal" not in fieldnames:
        failures.append(f"{path} missing p_greater_equal column")
        return failures
    if not rows:
        failures.append(f"{path} has no follow-up rows")
    for row in rows:
        label = f"{row.get('corpus', '')}:{row.get('term_id', '')}"
        try:
            p_value = float(row.get("p_greater_equal", "nan"))
        except ValueError:
            failures.append(f"{path} {label} has nonnumeric p_greater_equal")
            continue
        if p_value <= threshold:
            failures.append(
                f"{path} {label} crosses survivor threshold: p_greater_equal={p_value}"
            )
    return failures


def validate_survivor_terms(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != SURVIVOR_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows:
        failures.append(f"{path} has {len(rows)} survivor row(s); downstream is no longer idle")
    return failures


def validate_empty_data_rows(path: Path, label: str) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    _, rows = data
    if rows:
        return [f"{path} {label} has {len(rows)} row(s); expected 0"]
    return []


def validate_doc(path: Path, required_phrases: tuple[str, ...]) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    normalized = normalize_space(path.read_text(encoding="utf-8"))
    return [
        f"{path} missing phrase: {phrase}"
        for phrase in required_phrases
        if normalize_space(phrase) not in normalized
    ]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
