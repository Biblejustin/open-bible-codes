#!/usr/bin/env python3
"""Validate Cities source-row lock worksheet stays pre-import."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CITIES_SOURCE_ROW_LOCK_WORKSHEET.md")
DEFAULT_ROWS = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_worksheet.csv"
)

REQUIRED_PHRASES = (
    "# Cities Source Row Lock Worksheet",
    "Status: worksheet plus current Cities source-row lock decision-record status.",
    "does not update either file",
    "No OCR body text or source-script body text appears",
    "Worksheet rows: 14.",
    "Table-bearing candidate pages: 4.",
    "Source-list candidate pages: 5.",
    "Exception-note candidate pages: 5.",
    "Recorded decision rows: 0.",
    "Locked decision rows: 0.",
    "Unrecorded decision rows: 14.",
    "Source-row imports: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "Recorded selected actions: none.",
    "source_row_lock_ready",
    "`cities_source_row_lock_001`",
    "`cities_source_row_lock_014`",
    "never imports or transcribes source rows",
    "CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md",
    "recovered PDF metadata and page-image paths",
)

EXPECTED_IDS = tuple(f"cities_source_row_lock_{index:03d}" for index in range(1, 15))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_row_lock_worksheet_doc(args.doc, args.rows)
    if failures:
        for failure in failures:
            print(
                f"Cities source-row lock worksheet doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-row lock worksheet doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    return parser


def validate_cities_source_row_lock_worksheet_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
) -> list[str]:
    missing = [str(path) for path in (doc, rows_csv) if not path.exists()]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    rows_text = rows_csv.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    rows = read_csv(rows_csv)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(validate_no_source_text(doc, text, rows_csv, rows_text))
    failures.extend(validate_rows(doc, normalized, rows))
    return failures


def validate_no_source_text(
    doc: Path,
    doc_text: str,
    rows_csv: Path,
    rows_text: str,
) -> list[str]:
    failures: list[str] = []
    if contains_hebrew_or_greek(doc_text):
        failures.append(f"{doc} appears to contain source-script body text")
    if contains_hebrew_or_greek(rows_text):
        failures.append(f"{rows_csv} appears to contain source-script body text")
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    ids = [row.get("decision_id", "") for row in rows]
    if tuple(ids) != EXPECTED_IDS:
        failures.append("rows CSV decision ids do not match expected 1..14 sequence")
    for row in rows:
        decision_id = row.get("decision_id", "")
        if row.get("source_row_use") != "no_source_row_use":
            failures.append(f"rows CSV {decision_id} allows source-row use")
        if row.get("current_decision") != "no_source_row_import":
            failures.append(f"rows CSV {decision_id} imports source row")
        if row.get("record_decision_status") != "unrecorded":
            failures.append(f"rows CSV {decision_id} unexpectedly has a lock record")
        if row.get("record_selected_action"):
            failures.append(f"rows CSV {decision_id} unexpectedly has selected action")
        if decision_id and decision_id not in normalized_doc:
            failures.append(f"{doc} missing decision id: {decision_id}")
    return failures


def contains_hebrew_or_greek(text: str) -> bool:
    for char in text:
        code = ord(char)
        if 0x0590 <= code <= 0x05FF or 0x0370 <= code <= 0x03FF:
            return True
    return False


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
