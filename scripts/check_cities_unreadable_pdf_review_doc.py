#!/usr/bin/env python3
"""Validate Cities unreadable-PDF review doc stays OCR-planning only."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CITIES_UNREADABLE_PDF_REVIEW.md")
DEFAULT_ROWS = Path("reports/cities_pdf_recovery_probe/cities_unreadable_pdf_review.csv")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_review_summary.csv"
)

REQUIRED_PHRASES = (
    "# Cities Unreadable PDF Review",
    "Status: OCR/encoding planning only.",
    "does not run OCR",
    "repair text",
    "import source rows",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "Unreadable rows reviewed: 7.",
    "OCR/image-only rows: 4.",
    "Encoding-or-OCR candidate rows: 3.",
    "Aumann committee rows: 6.",
    "Other-family rows: 1.",
    "Pages needing review: 41.",
    "Garbled text chars: 5364.",
    "does not repair the PDFs",
    "does not repair the PDFs, create OCR text, decide source admissibility",
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

EXPECTED_LANES = (
    "ocr_image_only_pdf",
    "encoding_or_ocr_candidate",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_unreadable_pdf_review_doc(
        args.doc,
        args.rows,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(f"Cities unreadable-PDF review doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities unreadable-PDF review doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_cities_unreadable_pdf_review_doc(
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
    lanes = {row.get("lane", "") for row in rows}
    failures: list[str] = []
    for label in EXPECTED_LABELS:
        if label not in labels:
            failures.append(f"rows CSV missing label: {label}")
        if label not in normalized_doc:
            failures.append(f"{doc} missing label: {label}")
    for lane in EXPECTED_LANES:
        if lane not in lanes:
            failures.append(f"rows CSV missing lane: {lane}")
        if lane not in normalized_doc:
            failures.append(f"{doc} missing lane: {lane}")
    return failures


def validate_summary(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
    summary: dict[str, str],
) -> list[str]:
    expected = {
        "Unreadable rows reviewed": summary.get("unreadable_rows_reviewed", ""),
        "OCR/image-only rows": summary.get("ocr_image_only_rows", ""),
        "Encoding-or-OCR candidate rows": summary.get("encoding_or_ocr_candidate_rows", ""),
        "Aumann committee rows": summary.get("aumann_committee_rows", ""),
        "Other-family rows": summary.get("other_family_rows", ""),
        "Pages needing review": summary.get("total_pages_needing_review", ""),
        "Garbled text chars": summary.get("garbled_text_chars", ""),
    }
    failures: list[str] = []
    if summary.get("unreadable_rows_reviewed") != str(len(rows)):
        failures.append(
            f"summary CSV unreadable_rows_reviewed={summary.get('unreadable_rows_reviewed')} "
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
