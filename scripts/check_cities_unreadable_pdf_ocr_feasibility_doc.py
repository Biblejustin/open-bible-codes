#!/usr/bin/env python3
"""Validate Cities unreadable-PDF OCR feasibility doc stays non-result-bearing."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CITIES_UNREADABLE_PDF_OCR_FEASIBILITY.md")
DEFAULT_ROWS = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_feasibility.csv"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_feasibility_summary.csv"
)

REQUIRED_PHRASES = (
    "# Cities Unreadable PDF OCR Feasibility",
    "Status: OCR feasibility only.",
    "records only counts/status",
    "does not store OCR text in tracked files",
    "repair text",
    "import source rows",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "Rows reviewed: 7.",
    "Rows with OCR text: 7.",
    "Pages attempted: 41.",
    "Pages with OCR text: 39.",
    "OCR text signal chars: 54324.",
    "OCR text detected rows: 7.",
    "Low OCR text rows: 0.",
    "OCR empty rows: 0.",
    "OCR error rows: 0.",
    "does not publish OCR text",
    "make a result-bearing claim",
)

EXPECTED_LABELS = (
    "cities_pdf_dp365a_appendix_6",
    "cities_pdf_dp365a_appendix_7",
    "cities_pdf_dp365a_part_2_p105_111",
    "cities_pdf_wrr",
    "cities_pdf_dp365a_p12_17",
    "cities_pdf_dp365a_p1_4",
    "cities_pdf_dp365a_p5_11",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_unreadable_pdf_ocr_feasibility_doc(
        args.doc,
        args.rows,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities unreadable-PDF OCR feasibility doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities unreadable-PDF OCR feasibility doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_cities_unreadable_pdf_ocr_feasibility_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
) -> list[str]:
    missing = [str(path) for path in (doc, rows_csv, summary_csv) if not path.exists()]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    rows = read_csv(rows_csv)
    summary = {row["metric"]: row["value"] for row in read_csv(summary_csv)}
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(validate_rows(doc, normalized, rows))
    failures.extend(validate_summary(doc, normalized, rows, summary))
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    labels = {row.get("label", "") for row in rows}
    statuses = {row.get("ocr_status", "") for row in rows}
    failures: list[str] = []
    for label in EXPECTED_LABELS:
        if label not in labels:
            failures.append(f"rows CSV missing label: {label}")
        if label not in normalized_doc:
            failures.append(f"{doc} missing label: {label}")
    if "ocr_text_detected" not in statuses:
        failures.append("rows CSV missing status: ocr_text_detected")
    if "ocr_text_detected" not in normalized_doc:
        failures.append(f"{doc} missing status: ocr_text_detected")
    return failures


def validate_summary(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
    summary: dict[str, str],
) -> list[str]:
    expected = {
        "Rows reviewed": summary.get("rows_reviewed", ""),
        "Rows with OCR text": summary.get("rows_with_ocr_text", ""),
        "Pages attempted": summary.get("pages_attempted", ""),
        "Pages with OCR text": summary.get("pages_with_ocr_text", ""),
        "OCR text signal chars": summary.get("ocr_text_signal_chars", ""),
        "OCR text detected rows": summary.get("status_ocr_text_detected", "0"),
        "Low OCR text rows": summary.get("status_low_ocr_text", "0"),
        "OCR empty rows": summary.get("status_ocr_empty", "0"),
        "OCR error rows": summary.get("status_ocr_error", "0"),
    }
    failures: list[str] = []
    if summary.get("rows_reviewed") != str(len(rows)):
        failures.append(
            f"summary CSV rows_reviewed={summary.get('rows_reviewed')} "
            f"does not match rows={len(rows)}"
        )
    for label, value in expected.items():
        if not value:
            failures.append(f"summary CSV missing metric for {label}")
            continue
        needle = normalize_space(f"- {label}: {value}.")
        if needle not in normalized_doc:
            failures.append(f"{doc} missing summary value: {label}={value}")
    return failures


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
