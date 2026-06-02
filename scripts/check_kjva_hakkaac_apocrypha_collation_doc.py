#!/usr/bin/env python3
"""Validate Hakkaac KJVA Apocrypha ignored-local collation audit."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import analyze_kjva_hakkaac_apocrypha_collation as audit


DEFAULT_DOC = audit.DEFAULT_MD
DEFAULT_VERSE_ROWS = audit.DEFAULT_VERSE_ROWS
DEFAULT_BOOK_ROWS = audit.DEFAULT_BOOK_ROWS
DEFAULT_BLOCKER_ROWS = audit.DEFAULT_BLOCKER_ROWS
DEFAULT_SUMMARY = audit.DEFAULT_SUMMARY
DEFAULT_MANIFEST = audit.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# KJVA Hakkaac Apocrypha Collation Audit",
    "Status: ignored local collation audit only.",
    "Source-use decision: Hakkaac was approved for ignored local import and collation only.",
    "not an ELS result",
    "not a corpus import",
    "not a source lock",
    "not a result-bearing replication",
    "Raw Hakkaac verse text is written only under ignored `data/private/` output.",
    "Tracked outputs record hashes, counts, lengths, refs, and status only; they do not write Bible text.",
    "Pages fetched: 14.",
    "Local verses: 5720.",
    "Hakkaac verses: 5720.",
    "Comparable refs: 5720.",
    "Exact normalized verse matches: 5719.",
    "Length-match hash-drift verses: 0.",
    "Length-drift verses: 1.",
    "Missing Hakkaac refs: 0.",
    "Missing local refs: 0.",
    "Exact book stream matches: 13/14.",
    "Book stream drift books: 1.",
    "Local normalized letters: 593090.",
    "Hakkaac normalized letters: 593091.",
    "Normalized length delta: 1.",
    "Apocrypha stream hash match: 0.",
    "Source-lock ready: 0.",
    "Result-ready sources: 0.",
    "Claim status: `ignored_local_collation_audit_only_not_result_bearing`.",
    "`SIR 19:1`",
    "`length_drift`",
    "Exact blocker rows: 16/16.",
    "`SIR 44:23` status: `exact_normalized_match`.",
    "`MAN 1:1..15` status: `exact_normalized_match`.",
    "No Bible text is written to tracked outputs.",
    "does not change KJVA bridge result status",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:source-lock ready|result-bearing replication is ready|claim report|"
    r"claim-level|proved|proves|proof|conclusive evidence|significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "Source-lock ready: 0.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_hakkaac_apocrypha_collation_doc(
        args.doc,
        verse_rows=args.verse_rows,
        book_rows=args.book_rows,
        blocker_rows=args.blocker_rows,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA Hakkaac collation failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA Hakkaac collation ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--verse-rows", type=Path, default=DEFAULT_VERSE_ROWS)
    parser.add_argument("--book-rows", type=Path, default=DEFAULT_BOOK_ROWS)
    parser.add_argument("--blocker-rows", type=Path, default=DEFAULT_BLOCKER_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_hakkaac_apocrypha_collation_doc(
    doc: Path = DEFAULT_DOC,
    *,
    verse_rows: Path | None = DEFAULT_VERSE_ROWS,
    book_rows: Path | None = DEFAULT_BOOK_ROWS,
    blocker_rows: Path | None = DEFAULT_BLOCKER_ROWS,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    failures: list[str] = []
    for phrase in REQUIRED_PHRASES:
        if normalize_space(phrase) not in normalized:
            failures.append(f"{doc} missing phrase: {phrase}")
    failures.extend(validate_no_overclaim(doc, text))
    if verse_rows is not None:
        failures.extend(validate_verse_rows(verse_rows))
    if book_rows is not None:
        failures.extend(validate_book_rows(book_rows))
    if blocker_rows is not None:
        failures.extend(validate_blocker_rows(blocker_rows))
    if summary is not None:
        failures.extend(validate_summary(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_verse_rows(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != audit.VERSE_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 5720:
        failures.append(f"{path} expected 5720 verse rows, found {len(rows)}")
        return failures
    drift_rows = [row for row in rows if row["status"] != "exact_normalized_match"]
    if len(drift_rows) != 1:
        failures.append(f"{path} expected 1 drift row, found {len(drift_rows)}")
    elif drift_rows[0]["ref"] != "SIR 19:1":
        failures.append(f"{path} drift ref changed: {drift_rows[0]['ref']!r}")
    return failures


def validate_book_rows(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != audit.BOOK_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 14:
        failures.append(f"{path} expected 14 book rows, found {len(rows)}")
        return failures
    by_book = {row["book"]: row for row in rows}
    sirach = by_book.get("SIR")
    if sirach is None:
        failures.append(f"{path} missing SIR row")
    elif sirach["status"] != "stream_drift" or sirach["norm_len_delta"] != "1":
        failures.append(f"{path} SIR drift summary changed")
    exact_books = [row for row in rows if row["status"] == "exact_normalized_stream_match"]
    if len(exact_books) != 13:
        failures.append(f"{path} expected 13 exact book streams, found {len(exact_books)}")
    return failures


def validate_blocker_rows(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != audit.BLOCKER_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 16:
        failures.append(f"{path} expected 16 blocker rows, found {len(rows)}")
        return failures
    if any(row["status"] != "exact_normalized_match" for row in rows):
        failures.append(f"{path} expected all blocker rows exact_normalized_match")
    refs = {row["ref"] for row in rows}
    if "SIR 44:23" not in refs or "MAN 1:15" not in refs:
        failures.append(f"{path} blocker refs changed")
    return failures


def validate_summary(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != audit.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    expected = {
        "source_use_decision": "approved_ignored_local_collation_only",
        "private_text_path": "data/private/hakkaac_kjva_apocrypha/verses.csv",
        "pages_fetched": "14",
        "local_verses": "5720",
        "hakkaac_verses": "5720",
        "comparable_refs": "5720",
        "exact_normalized_verse_matches": "5719",
        "length_match_hash_drift_verses": "0",
        "length_drift_verses": "1",
        "missing_hakkaac_refs": "0",
        "missing_local_refs": "0",
        "exact_book_stream_matches": "13",
        "book_stream_drift_books": "1",
        "local_norm_letters": "593090",
        "hakkaac_norm_letters": "593091",
        "norm_len_delta": "1",
        "apocrypha_stream_hash_match": "False",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "ignored_local_collation_audit_only_not_result_bearing",
    }
    row = rows[0]
    for key, value in expected.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted: {row.get(key)!r}")
    return failures


def validate_manifest(path: Path, *, doc: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path} is invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return [f"{path} JSON root must be an object"]
    failures: list[str] = []
    if payload.get("claim_boundary") != "ignored local collation audit only; no ELS result":
        failures.append(f"{path} claim_boundary drifted")
    if payload.get("text_retention") != "raw Hakkaac text only in ignored data/private output":
        failures.append(f"{path} text_retention drifted")
    if payload.get("source_use_decision") != "approved ignored local import for collation only":
        failures.append(f"{path} source_use_decision drifted")
    outputs = payload.get("outputs", {})
    markdown = outputs.get("markdown") if isinstance(outputs, dict) else None
    allowed_markdown_paths = {str(doc)}
    try:
        allowed_markdown_paths.add(str(doc.relative_to(Path.cwd())))
    except ValueError:
        pass
    if markdown not in allowed_markdown_paths:
        failures.append(f"{path} markdown output drifted")
    return failures


def validate_no_overclaim(path: Path, text: str) -> list[str]:
    failures: list[str] = []
    for match in FORBIDDEN_OVERCLAIM_RE.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        line_text = text.splitlines()[line - 1].strip()
        if any(context in line_text for context in ALLOWED_FORBIDDEN_CONTEXTS):
            continue
        failures.append(f"{path}:{line} overclaim phrase: {match.group(0)!r}")
    return failures


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
