#!/usr/bin/env python3
"""Validate Cities unreadable-PDF OCR review checklist doc stays no-input."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_CHECKLIST.md")
DEFAULT_ROWS = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_checklist.csv"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_checklist_summary.csv"
)

REQUIRED_PHRASES = (
    "# Cities Unreadable PDF OCR Review Checklist",
    "Status: no-input OCR review checklist.",
    "creates contact sheets",
    "does not track OCR text",
    "repair text",
    "import source rows",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "Checklist rows: 7.",
    "PDF rows: 7.",
    "Pages total: 41.",
    "Pages with OCR text: 39.",
    "Pages without OCR text: 2.",
    "Label contact sheets: 7.",
    "Contact sheets are visual review aids only",
    "OCR sidecars remain ignored local files",
    "separate citable decision records",
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
    failures = validate_cities_unreadable_pdf_ocr_review_checklist_doc(
        args.doc,
        args.rows,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities unreadable-PDF OCR review checklist doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities unreadable-PDF OCR review checklist doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_cities_unreadable_pdf_ocr_review_checklist_doc(
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
    priorities = {row.get("review_priority", "") for row in rows}
    failures: list[str] = []
    for label in EXPECTED_LABELS:
        if label not in labels:
            failures.append(f"rows CSV missing label: {label}")
        if label not in normalized_doc:
            failures.append(f"{doc} missing label: {label}")
    if "1_empty_or_low_ocr_pages" not in priorities:
        failures.append("rows CSV missing priority: 1_empty_or_low_ocr_pages")
    if "1_empty_or_low_ocr_pages" not in normalized_doc:
        failures.append(f"{doc} missing priority: 1_empty_or_low_ocr_pages")
    return failures


def validate_summary(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
    summary: dict[str, str],
) -> list[str]:
    expected = {
        "Checklist rows": summary.get("checklist_rows", ""),
        "PDF rows": summary.get("pdf_rows", ""),
        "Pages total": summary.get("pages_total", ""),
        "Pages with OCR text": summary.get("pages_with_ocr_text", ""),
        "Pages without OCR text": summary.get("pages_without_ocr_text", ""),
        "OCR text signal chars": summary.get("ocr_text_signal_chars", ""),
        "OCR words": summary.get("ocr_words", ""),
        "OCR lines": summary.get("ocr_lines", ""),
        "Label contact sheets": summary.get("label_contact_sheets", ""),
    }
    failures: list[str] = []
    if summary.get("checklist_rows") != str(len(rows)):
        failures.append(
            f"summary CSV checklist_rows={summary.get('checklist_rows')} "
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
