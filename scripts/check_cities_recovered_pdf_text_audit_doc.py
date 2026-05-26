#!/usr/bin/env python3
"""Validate Cities recovered-PDF text audit doc matches generated CSVs."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CITIES_RECOVERED_PDF_TEXT_AUDIT.md")
DEFAULT_ROWS = Path("reports/cities_pdf_recovery_probe/cities_recovered_pdf_text_audit.csv")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_recovered_pdf_text_audit_summary.csv"
)
DEFAULT_ANCHORS = Path("reports/cities_pdf_recovery_probe/cities_recovered_pdf_text_anchors.csv")

REQUIRED_PHRASES = (
    "# Cities Recovered PDF Text Audit",
    "Status: source-shape audit only.",
    "does not run OCR",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "Rows with extractable text are now separated from image-only or garbled",
    "does not decide which texts are admissible for a result-bearing protocol",
)

EXPECTED_ROW_LABELS = (
    "cities_pdf_wrr",
    "cities_pdf_dp365a_p1_4",
    "cities_pdf_communities_data",
    "cities_pdf_gans",
)

EXPECTED_STATUSES = (
    "zero_extractable_text",
    "extractable_but_garbled_or_nonlatin",
    "extractable_text",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_recovered_pdf_text_audit_doc(
        args.doc,
        args.rows,
        args.summary,
        args.anchors,
    )
    if failures:
        for failure in failures:
            print(f"Cities recovered-PDF text audit doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities recovered-PDF text audit doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHORS)
    return parser


def validate_cities_recovered_pdf_text_audit_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    anchors_csv: Path = DEFAULT_ANCHORS,
) -> list[str]:
    missing_files = [str(path) for path in (doc, rows_csv, summary_csv, anchors_csv) if not path.exists()]
    if missing_files:
        return ["missing required files: " + ", ".join(missing_files)]

    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    rows = read_csv(rows_csv)
    summary_rows = read_csv(summary_csv)
    anchors = read_csv(anchors_csv)
    if len(summary_rows) != 1:
        return [f"{summary_csv} must have exactly one summary row"]
    summary = summary_rows[0]

    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(validate_summary_counts(doc, normalized, summary, anchors))
    failures.extend(validate_rows(doc, normalized, rows))
    return failures


def validate_summary_counts(
    doc: Path,
    normalized_doc: str,
    summary: dict[str, str],
    anchors: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    count_expectations = {
        "recovered PDF rows audited": summary["recovered_pdf_rows"],
        "extractable text rows": summary["extractable_text_rows"],
        "zero-text rows": summary["zero_text_rows"],
        "garbled/non-Latin extract rows": summary["garbled_or_nonlatin_rows"],
        "Gans/community family rows": summary["gans_family_rows"],
        "Aumann committee family rows": summary["aumann_family_rows"],
        "other family rows": summary["other_family_rows"],
    }
    for label, value in count_expectations.items():
        expected = normalize_space(f"| {label} | {value} |")
        if expected not in normalized_doc:
            failures.append(f"{doc} missing summary count: {label}={value}")

    anchor_total = str(len(anchors))
    anchor_found = str(sum(1 for row in anchors if row.get("status") == "found"))
    found_phrase = normalize_space(f"Found anchors: {anchor_found} of {anchor_total}.")
    if found_phrase not in normalized_doc:
        failures.append(
            f"{doc} missing anchor count: found={anchor_found} total={anchor_total}"
        )
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    labels = {row.get("label", "") for row in rows}
    statuses = {row.get("text_status", "") for row in rows}
    failures: list[str] = []
    for label in EXPECTED_ROW_LABELS:
        if label not in labels:
            failures.append(f"rows CSV missing expected label: {label}")
        if label not in normalized_doc:
            failures.append(f"{doc} missing row label: {label}")
    for status in EXPECTED_STATUSES:
        if status not in statuses:
            failures.append(f"rows CSV missing expected text status: {status}")
        if status not in normalized_doc:
            failures.append(f"{doc} missing text status: {status}")
    return failures


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
