#!/usr/bin/env python3
"""Validate Cities unreadable-PDF OCR review packet doc stays review-only."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_PACKET.md")
DEFAULT_ROWS = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_packet.csv"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_packet_summary.csv"
)

REQUIRED_PHRASES = (
    "# Cities Unreadable PDF OCR Review Packet",
    "Status: OCR review packet only.",
    "records only paths/counts/status in tracked files",
    "does not track OCR text",
    "repair text",
    "import source rows",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "PDF rows: 7.",
    "Page rows: 41.",
    "Pages with OCR text: 39.",
    "Pages without OCR text: 2.",
    "Image sidecars: 41.",
    "OCR text sidecars: 41.",
    "Page OCR text detected rows: 39.",
    "Page OCR empty rows: 2.",
    "OCR text sidecars are ignored local review aids",
    "source-row use",
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
    failures = validate_cities_unreadable_pdf_ocr_review_packet_doc(
        args.doc,
        args.rows,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities unreadable-PDF OCR review packet doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities unreadable-PDF OCR review packet doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_cities_unreadable_pdf_ocr_review_packet_doc(
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
    for status in ("page_ocr_text_detected", "page_ocr_empty"):
        if status not in statuses:
            failures.append(f"rows CSV missing status: {status}")
        if status not in normalized_doc:
            failures.append(f"{doc} missing status: {status}")
    return failures


def validate_summary(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
    summary: dict[str, str],
) -> list[str]:
    expected = {
        "PDF rows": summary.get("pdf_rows", ""),
        "Page rows": summary.get("page_rows", ""),
        "Pages with OCR text": summary.get("pages_with_ocr_text", ""),
        "Pages without OCR text": summary.get("pages_without_ocr_text", ""),
        "OCR text signal chars": summary.get("ocr_text_signal_chars", ""),
        "OCR words": summary.get("ocr_words", ""),
        "OCR lines": summary.get("ocr_lines", ""),
        "Image sidecars": summary.get("image_sidecars", ""),
        "OCR text sidecars": summary.get("ocr_text_sidecars", ""),
        "Page OCR text detected rows": summary.get("status_page_ocr_text_detected", "0"),
        "Page OCR empty rows": summary.get("status_page_ocr_empty", "0"),
        "OCR error rows": summary.get("status_ocr_error", "0"),
    }
    failures: list[str] = []
    if summary.get("page_rows") != str(len(rows)):
        failures.append(
            f"summary CSV page_rows={summary.get('page_rows')} "
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
