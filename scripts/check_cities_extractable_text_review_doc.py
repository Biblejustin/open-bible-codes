#!/usr/bin/env python3
"""Validate Cities extractable-text review doc stays role-review only."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CITIES_EXTRACTABLE_TEXT_REVIEW.md")
DEFAULT_ROWS = Path("reports/cities_pdf_recovery_probe/cities_extractable_text_review.csv")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_extractable_text_review_summary.csv"
)

REQUIRED_PHRASES = (
    "# Cities Extractable Text Review",
    "Status: source-role review only.",
    "does not import source rows",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "Extractable rows reviewed: 5.",
    "Data-bearing candidates: 1.",
    "Data candidates with existing source-shape audit: 1.",
    "Gans source-shape records: 66.",
    "Gans community rows: 210.",
    "Method-context candidates: 1.",
    "Commentary/critique rows: 3.",
    "docs/GANS_COMMUNITIES_SOURCE_AUDIT.md",
    "source_shape_covered_not_result_bearing",
    "does not create city-name rows",
    "does not make a result-bearing claim",
    "not a result protocol",
)

EXPECTED_LABELS = (
    "cities_pdf_communities_data",
    "cities_pdf_gans",
    "cities_pdf_dp_365_1",
    "cities_pdf_dp_365_2",
    "cities_pdf_dp_365_4",
)

EXPECTED_STATUSES = (
    "data_bearing_candidate",
    "method_context_candidate",
    "commentary_or_perspective",
    "critique_or_response",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_extractable_text_review_doc(
        args.doc,
        args.rows,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(f"Cities extractable-text review doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities extractable-text review doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_cities_extractable_text_review_doc(
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
    failures.extend(validate_summary(doc, normalized, summary))
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    labels = {row.get("label", "") for row in rows}
    statuses = {row.get("data_bearing_status", "") for row in rows}
    failures: list[str] = []
    for label in EXPECTED_LABELS:
        if label not in labels:
            failures.append(f"rows CSV missing label: {label}")
        if label not in normalized_doc:
            failures.append(f"{doc} missing label: {label}")
    for status in EXPECTED_STATUSES:
        if status not in statuses:
            failures.append(f"rows CSV missing status: {status}")
        if status not in normalized_doc:
            failures.append(f"{doc} missing status: {status}")
    return failures


def validate_summary(
    doc: Path,
    normalized_doc: str,
    summary: dict[str, str],
) -> list[str]:
    expected = {
        "Extractable rows reviewed": summary.get("extractable_rows_reviewed", ""),
        "Anchors found": summary.get("anchors_found", ""),
        "Data-bearing candidates": summary.get("status_data_bearing_candidate", ""),
        "Data candidates with existing source-shape audit": summary.get(
            "data_candidates_with_existing_source_shape_audit",
            "",
        ),
        "Gans source-shape records": summary.get("gans_source_records", ""),
        "Gans community rows": summary.get("gans_source_community_rows", ""),
        "Method-context candidates": summary.get("status_method_context_candidate", ""),
    }
    failures: list[str] = []
    for label, value in expected.items():
        if not value:
            failures.append(f"summary CSV missing metric for {label}")
            continue
        if label == "Anchors found":
            needle = normalize_space(
                f"- {label}: {value} of {summary.get('extractable_rows_reviewed', '')}."
            )
        else:
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
