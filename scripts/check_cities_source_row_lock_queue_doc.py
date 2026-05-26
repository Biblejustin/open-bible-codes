#!/usr/bin/env python3
"""Validate Cities source-row lock queue stays pre-import."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CITIES_SOURCE_ROW_LOCK_QUEUE.md")
DEFAULT_ROWS = Path("reports/cities_pdf_recovery_probe/cities_source_row_lock_queue.csv")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_queue_summary.csv"
)

REQUIRED_PHRASES = (
    "# Cities Source Row Lock Queue",
    "Status: source-row lock planning record",
    "does not import source rows",
    "No OCR body text or source-script body text appears",
    "Queue rows: 14.",
    "Unique labels: 3.",
    "Table-bearing candidate pages: 4.",
    "Source-list candidate pages: 5.",
    "Exception-note candidate pages: 5.",
    "Source-row imports: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "table_candidate_page",
    "source_list_candidate_page",
    "exception_note_candidate_page",
    "needs_citable_source_row_lock",
    "This queue names page locations only.",
    "CITIES_SOURCE_ROW_LOCK_WORKSHEET.md",
    "decision ids and evidence prompts",
)

EXPECTED_PAGES = (
    ("cities_pdf_dp365a_p5_11", "3", "prose_with_source_table_page"),
    ("cities_pdf_dp365a_p5_11", "4", "source_table_page"),
    ("cities_pdf_dp365a_p5_11", "5", "source_table_page"),
    ("cities_pdf_dp365a_p5_11", "6", "source_table_and_notes_page"),
    ("cities_pdf_dp365a_appendix_7", "1", "source_list_page"),
    ("cities_pdf_dp365a_appendix_7", "2", "source_list_page"),
    ("cities_pdf_dp365a_appendix_7", "3", "source_list_page"),
    ("cities_pdf_dp365a_appendix_7", "4", "source_list_page"),
    ("cities_pdf_dp365a_appendix_7", "5", "source_list_page"),
    ("cities_pdf_dp365a_p12_17", "2", "source_exception_notes_page"),
    ("cities_pdf_dp365a_p12_17", "3", "source_exception_notes_page"),
    ("cities_pdf_dp365a_p12_17", "4", "source_exception_notes_page"),
    ("cities_pdf_dp365a_p12_17", "5", "source_exception_notes_page"),
    ("cities_pdf_dp365a_p12_17", "6", "criteria_and_source_exception_page"),
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_row_lock_queue_doc(
        args.doc,
        args.rows,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(f"Cities source-row lock queue doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities source-row lock queue doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_cities_source_row_lock_queue_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
) -> list[str]:
    missing = [str(path) for path in (doc, rows_csv, summary_csv) if not path.exists()]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    rows_text = rows_csv.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    rows = read_csv(rows_csv)
    summary = {row["metric"]: row["value"] for row in read_csv(summary_csv)}
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(validate_no_source_text(doc, text, rows_csv, rows_text))
    failures.extend(validate_rows(doc, normalized, rows))
    failures.extend(validate_summary(doc, normalized, rows, summary))
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
    by_key = {(row.get("label", ""), row.get("page_number", "")): row for row in rows}
    if len(rows) != len(EXPECTED_PAGES):
        failures.append(f"rows CSV has {len(rows)} rows, expected {len(EXPECTED_PAGES)}")
    for label, page, role in EXPECTED_PAGES:
        row = by_key.get((label, page))
        if row is None:
            failures.append(f"rows CSV missing candidate page: {label} p{page}")
            continue
        if row.get("visual_page_role") != role:
            failures.append(
                f"rows CSV {label} p{page} role={row.get('visual_page_role')} expected {role}"
            )
        if row.get("source_row_use") != "no_source_row_use":
            failures.append(f"rows CSV {label} p{page} allows source-row use")
        if row.get("current_decision") != "no_source_row_import":
            failures.append(f"rows CSV {label} p{page} imports source row")
        if row.get("lock_status") != "needs_citable_source_row_lock":
            failures.append(f"rows CSV {label} p{page} missing lock status")
        if label not in normalized_doc:
            failures.append(f"{doc} missing label: {label}")
        if role not in normalized_doc:
            failures.append(f"{doc} missing role: {role}")
    return failures


def validate_summary(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
    summary: dict[str, str],
) -> list[str]:
    expected = {
        "Queue rows": summary.get("queue_rows", ""),
        "Unique labels": summary.get("unique_labels", ""),
        "Table-bearing candidate pages": summary.get("table_candidate_pages", ""),
        "Source-list candidate pages": summary.get("source_list_candidate_pages", ""),
        "Exception-note candidate pages": summary.get(
            "exception_note_candidate_pages", ""
        ),
        "Source-row imports": summary.get("source_row_imports", ""),
        "ELS runs": summary.get("els_runs", ""),
        "Compactness runs": summary.get("compactness_runs", ""),
    }
    failures: list[str] = []
    if summary.get("queue_rows") != str(len(rows)):
        failures.append(
            f"summary CSV queue_rows={summary.get('queue_rows')} does not match rows={len(rows)}"
        )
    for label, value in expected.items():
        if not value:
            failures.append(f"summary CSV missing metric for {label}")
            continue
        needle = normalize_space(f"- {label}: {value}.")
        if needle not in normalized_doc:
            failures.append(f"{doc} missing summary value: {label}={value}")
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
