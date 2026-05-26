#!/usr/bin/env python3
"""Validate Cities unreadable-PDF OCR page-review doc stays non-source."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_unreadable_pdf_ocr_page_review as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_PACKET = builder.DEFAULT_PACKET
DEFAULT_DECISIONS = builder.DEFAULT_DECISIONS

REQUIRED_PHRASES = (
    "# Cities Unreadable PDF OCR Page Review",
    "Status: manual page-image review record.",
    "does not track OCR body text",
    "No OCR body text appears",
    "Review rows: 41.",
    "Reviewed pages: 41.",
    "OCR-empty pages reviewed: 2.",
    "Low-signal pages reviewed: 3.",
    "Source-row imports: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "appendix_toc_or_index_page",
    "blank_or_separator_page",
    "method_intro_prose_page",
    "source_exception_notes_page",
    "criteria_and_source_exception_page",
    "title_page",
    "method_prose_with_index_page",
    "prose_with_source_table_page",
    "source_table_page",
    "source_table_and_notes_page",
    "method_notes_page",
    "method_toc_and_prose_page",
    "appendix_prose_page",
    "source_list_page",
    "context_paper_title_page",
    "context_paper_figure_page",
    "context_paper_prose_page",
    "context_paper_table_page",
    "context_paper_formula_page",
    "context_paper_chart_page",
    "context_paper_reference_page",
    "Source-row decisions require separate citable decision records.",
)

EXPECTED_PAGES = (
    ("cities_pdf_dp365a_p1_4", "3", "appendix_toc_or_index_page"),
    ("cities_pdf_dp365a_p1_4", "4", "blank_or_separator_page"),
    ("cities_pdf_dp365a_p1_4", "1", "method_toc_and_prose_page"),
    ("cities_pdf_dp365a_p1_4", "2", "method_toc_and_prose_page"),
    ("cities_pdf_dp365a_p12_17", "1", "method_intro_prose_page"),
    ("cities_pdf_dp365a_p12_17", "2", "source_exception_notes_page"),
    ("cities_pdf_dp365a_p12_17", "3", "source_exception_notes_page"),
    ("cities_pdf_dp365a_p12_17", "4", "source_exception_notes_page"),
    ("cities_pdf_dp365a_p12_17", "5", "source_exception_notes_page"),
    ("cities_pdf_dp365a_p12_17", "6", "criteria_and_source_exception_page"),
    ("cities_pdf_dp365a_p5_11", "1", "title_page"),
    ("cities_pdf_dp365a_p5_11", "2", "method_prose_with_index_page"),
    ("cities_pdf_dp365a_p5_11", "3", "prose_with_source_table_page"),
    ("cities_pdf_dp365a_p5_11", "4", "source_table_page"),
    ("cities_pdf_dp365a_p5_11", "5", "source_table_page"),
    ("cities_pdf_dp365a_p5_11", "6", "source_table_and_notes_page"),
    ("cities_pdf_dp365a_p5_11", "7", "method_notes_page"),
    ("cities_pdf_dp365a_appendix_6", "1", "appendix_prose_page"),
    ("cities_pdf_dp365a_appendix_6", "2", "appendix_prose_page"),
    ("cities_pdf_dp365a_appendix_7", "1", "source_list_page"),
    ("cities_pdf_dp365a_appendix_7", "2", "source_list_page"),
    ("cities_pdf_dp365a_appendix_7", "3", "source_list_page"),
    ("cities_pdf_dp365a_appendix_7", "4", "source_list_page"),
    ("cities_pdf_dp365a_appendix_7", "5", "source_list_page"),
    ("cities_pdf_dp365a_part_2_p105_111", "1", "appendix_prose_page"),
    ("cities_pdf_dp365a_part_2_p105_111", "2", "appendix_prose_page"),
    ("cities_pdf_dp365a_part_2_p105_111", "3", "appendix_prose_page"),
    ("cities_pdf_dp365a_part_2_p105_111", "4", "appendix_prose_page"),
    ("cities_pdf_dp365a_part_2_p105_111", "5", "appendix_prose_page"),
    ("cities_pdf_dp365a_part_2_p105_111", "6", "appendix_prose_page"),
    ("cities_pdf_dp365a_part_2_p105_111", "7", "appendix_prose_page"),
    ("cities_pdf_wrr", "1", "context_paper_title_page"),
    ("cities_pdf_wrr", "2", "context_paper_figure_page"),
    ("cities_pdf_wrr", "3", "context_paper_prose_page"),
    ("cities_pdf_wrr", "4", "context_paper_table_page"),
    ("cities_pdf_wrr", "5", "context_paper_table_page"),
    ("cities_pdf_wrr", "6", "context_paper_prose_page"),
    ("cities_pdf_wrr", "7", "context_paper_formula_page"),
    ("cities_pdf_wrr", "8", "context_paper_formula_page"),
    ("cities_pdf_wrr", "9", "context_paper_chart_page"),
    ("cities_pdf_wrr", "10", "context_paper_reference_page"),
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_unreadable_pdf_ocr_page_review_doc(
        args.doc,
        args.rows,
        args.summary,
        args.manifest,
        args.packet,
        args.decisions,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities unreadable-PDF OCR page-review doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities unreadable-PDF OCR page-review doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--decisions", type=Path, default=DEFAULT_DECISIONS)
    return parser


def validate_cities_unreadable_pdf_ocr_page_review_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
    packet_csv: Path = DEFAULT_PACKET,
    decisions_csv: Path = DEFAULT_DECISIONS,
) -> list[str]:
    missing = [
        str(path)
        for path in (
            doc,
            rows_csv,
            summary_csv,
            manifest_json,
            packet_csv,
            decisions_csv,
        )
        if not path.exists()
    ]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    rows_text = rows_csv.read_text(encoding="utf-8")
    summary_text = summary_csv.read_text(encoding="utf-8")
    manifest_text = manifest_json.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    rows_fieldnames, rows = read_csv(rows_csv)
    summary_fieldnames, summary_rows = read_csv(summary_csv)
    packet_rows = builder.read_csv(packet_csv)
    decision_rows = builder.read_csv(decisions_csv)
    expected_rows = builder.build_page_review_rows(packet_rows, decision_rows)
    expected_summary_rows = builder.build_summary_rows(expected_rows)
    summary = {row["metric"]: row["value"] for row in summary_rows}
    manifest = read_json(manifest_json)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(
        validate_no_source_text(
            {
                doc: text,
                rows_csv: rows_text,
                summary_csv: summary_text,
                manifest_json: manifest_text,
            }
        )
    )
    failures.extend(validate_rows_csv(rows_fieldnames, rows, expected_rows))
    failures.extend(validate_rows(doc, normalized, rows))
    failures.extend(
        validate_summary_csv(
            summary_fieldnames,
            summary_rows,
            expected_summary_rows,
        )
    )
    failures.extend(validate_summary(doc, normalized, rows, summary))
    failures.extend(
        validate_manifest(
            manifest_json,
            manifest,
            expected_rows,
            expected_summary_rows,
            packet_csv,
            decisions_csv,
        )
    )
    return failures


def validate_no_source_text(texts_by_path: dict[Path, str]) -> list[str]:
    failures: list[str] = []
    for path, text in texts_by_path.items():
        if contains_hebrew_or_greek(text):
            failures.append(f"{path} appears to contain OCR/source-script body text")
    return failures


def validate_rows_csv(
    fieldnames: list[str],
    rows: list[dict[str, str]],
    expected_rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    if fieldnames != builder.FIELDNAMES:
        failures.append(
            f"rows CSV fieldnames drifted: {fieldnames} expected {builder.FIELDNAMES}"
        )
    if rows != expected_rows:
        failures.append("rows CSV row data drifted from builder output")
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    by_key = {(row.get("label", ""), row.get("page_number", "")): row for row in rows}
    for label, page, role in EXPECTED_PAGES:
        row = by_key.get((label, page))
        if row is None:
            failures.append(f"rows CSV missing reviewed page: {label} p{page}")
            continue
        if row.get("visual_page_role") != role:
            failures.append(
                f"rows CSV {label} p{page} role={row.get('visual_page_role')} expected {role}"
            )
        if row.get("source_row_use") != "no_source_row_use":
            failures.append(f"rows CSV {label} p{page} allows source-row use")
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
        "Review rows": summary.get("review_rows", ""),
        "Reviewed pages": summary.get("reviewed_pages", ""),
        "OCR-empty pages reviewed": summary.get("ocr_empty_pages_reviewed", ""),
        "Low-signal pages reviewed": summary.get("low_signal_pages_reviewed", ""),
        "Visual-text-present pages": summary.get("visual_text_present_pages", ""),
        "Source-row imports": summary.get("source_row_imports", ""),
        "ELS runs": summary.get("els_runs", ""),
        "Compactness runs": summary.get("compactness_runs", ""),
    }
    failures: list[str] = []
    if summary.get("review_rows") != str(len(rows)):
        failures.append(
            f"summary CSV review_rows={summary.get('review_rows')} does not match rows={len(rows)}"
        )
    for label, value in expected.items():
        if not value:
            failures.append(f"summary CSV missing metric for {label}")
            continue
        needle = normalize_space(f"- {label}: {value}.")
        if needle not in normalized_doc:
            failures.append(f"{doc} missing summary value: {label}={value}")
    return failures


def validate_summary_csv(
    fieldnames: list[str],
    rows: list[dict[str, str]],
    expected_rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(
            f"summary CSV fieldnames drifted: {fieldnames} expected {builder.SUMMARY_FIELDNAMES}"
        )
    if rows != expected_rows:
        failures.append("summary CSV summary rows drifted from builder output")
    return failures


def validate_manifest(
    manifest_json: Path,
    manifest: dict[str, Any],
    expected_rows: list[dict[str, str]],
    expected_summary_rows: list[dict[str, str]],
    packet_csv: Path,
    decisions_csv: Path,
) -> list[str]:
    expected = {
        "tool": "build_cities_unreadable_pdf_ocr_page_review.py",
        "inputs": {
            "packet": str(packet_csv),
            "decisions": str(decisions_csv),
        },
        "rows": len(expected_rows),
        "summary": {
            row["metric"]: row["value"] for row in expected_summary_rows
        },
        "outputs": {
            "csv": str(DEFAULT_ROWS),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "claim_boundary": builder.CLAIM_BOUNDARY,
    }
    failures: list[str] = []
    for key, expected_value in expected.items():
        if manifest.get(key) != expected_value:
            failures.append(
                f"{manifest_json} {key} drifted: {manifest.get(key)!r} expected {expected_value!r}"
            )
    return failures


def contains_hebrew_or_greek(text: str) -> bool:
    for char in text:
        code = ord(char)
        if 0x0590 <= code <= 0x05FF or 0x0370 <= code <= 0x03FF:
            return True
    return False


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {}
    return payload


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
