#!/usr/bin/env python3
"""Validate Cities priority line-crop review worksheet stays no-input."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_line_crop_priority_contact_sheet as contact_builder
from scripts import build_cities_source_page_line_crop_priority_review_worksheet as builder
from scripts import build_cities_source_page_line_crop_triage as triage_builder
from scripts.check_cities_source_page_line_crop_contact_sheet_doc import (
    contains_hebrew_or_greek,
    normalize_space,
)


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_TRIAGE = builder.DEFAULT_TRIAGE
DEFAULT_PRIORITY_CONTACT = builder.DEFAULT_PRIORITY_CONTACT

EXPECTED_PRIORITY_COUNTS = {
    "priority_1_dense_text": 120,
    "priority_2_medium_text": 71,
    "priority_3_short_text": 12,
    "priority_4_no_text": 0,
}

REQUIRED_PHRASES = (
    "# Cities Source Page Line Crop Priority Review Worksheet",
    "Status: priority-ordered worksheet for future Cities source-page line-crop review.",
    "joins triage rank, crop image paths, and priority contact sheet paths",
    "without transcribing Hebrew or importing source rows",
    "No OCR body text or source-script body text appears",
    "Priority review rows: 203.",
    "Unique table pages: 4.",
    "Priority contact sheets: 4.",
    "Priority contact sheets available: 4.",
    "Crop images available: 203.",
    "OCR words represented by line boxes: 1511.",
    "OCR Hebrew letters represented by line boxes: 4934.",
    "Review state: `pending_priority_line_crop_review`.",
    "Dense-text priority rows: 120.",
    "Medium-text priority rows: 71.",
    "Short-text priority rows: 12.",
    "No-text priority rows: 0.",
    "Source-row imports: 0.",
    "City-name normalization: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "p-levels: 0.",
    "Priority order is not transcription",
    "readable source evidence before import",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_line_crop_priority_review_worksheet_doc(
        args.doc,
        rows_csv=args.rows,
        summary_csv=args.summary,
        manifest_json=args.manifest,
        triage_csv=args.triage,
        priority_contact_csv=args.priority_contact,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities source-page line-crop priority worksheet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-page line-crop priority worksheet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--triage", type=Path, default=DEFAULT_TRIAGE)
    parser.add_argument("--priority-contact", type=Path, default=DEFAULT_PRIORITY_CONTACT)
    return parser


def validate_cities_source_page_line_crop_priority_review_worksheet_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
    triage_csv: Path = DEFAULT_TRIAGE,
    priority_contact_csv: Path = DEFAULT_PRIORITY_CONTACT,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, summary_csv, manifest_json, triage_csv, priority_contact_csv)
        if not path.exists()
    ]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    rows_text = rows_csv.read_text(encoding="utf-8")
    summary_text = summary_csv.read_text(encoding="utf-8")
    manifest_text = manifest_json.read_text(encoding="utf-8")
    normalized = normalize_space(text)

    rows_data = read_csv(rows_csv)
    summary_data = read_csv(summary_csv)
    triage_data = read_csv(triage_csv)
    contact_data = read_csv(priority_contact_csv)
    if isinstance(rows_data, str):
        return [rows_data]
    if isinstance(summary_data, str):
        return [summary_data]
    if isinstance(triage_data, str):
        return [triage_data]
    if isinstance(contact_data, str):
        return [contact_data]

    triage_fieldnames, triage_rows = triage_data
    contact_fieldnames, contact_rows = contact_data
    expected_rows = builder.build_priority_review_rows(triage_rows, contact_rows)
    expected_summary = builder.build_summary_rows(
        triage_fieldnames, contact_fieldnames, expected_rows, contact_rows
    )
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
    failures.extend(validate_triage_shape(triage_csv, triage_data))
    failures.extend(validate_contact_shape(priority_contact_csv, contact_data))
    failures.extend(validate_rows_csv(rows_csv, rows_data, expected_rows))
    failures.extend(validate_summary_csv(summary_csv, summary_data, expected_summary))
    failures.extend(validate_rows(doc, normalized, rows_data[1]))
    failures.extend(validate_manifest(manifest_json, manifest, expected_rows, expected_summary))
    return failures


def validate_triage_shape(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != triage_builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 203:
        failures.append(f"{path} has {len(rows)} rows, expected 203")
    return failures


def validate_contact_shape(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != contact_builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 4:
        failures.append(f"{path} has {len(rows)} rows, expected 4")
    return failures


def validate_rows_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
    expected_rows: list[dict[str, str]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows != expected_rows:
        failures.append(f"{path} row data drifted")
    return failures


def validate_summary_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
    expected_summary: list[dict[str, str]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows != expected_summary:
        failures.append(f"{path} summary data drifted")
    summary = {row["metric"]: row["value"] for row in rows}
    for priority, expected_count in EXPECTED_PRIORITY_COUNTS.items():
        if summary.get(priority) != str(expected_count):
            failures.append(f"{path} {priority}={summary.get(priority)!r}")
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    if len(rows) != 203:
        failures.append(f"rows CSV has {len(rows)} rows, expected 203")
    ids = [row.get("line_review_id", "") for row in rows]
    expected_ids = [
        f"cities_source_priority_line_crop_{index:03d}" for index in range(1, 204)
    ]
    if ids != expected_ids:
        failures.append("rows CSV line review ids do not match expected 1..203 sequence")
    priority_counts: dict[str, int] = {}
    for row in rows:
        line_review_id = row.get("line_review_id", "")
        priority = row.get("review_priority", "")
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
        if row.get("review_state") != builder.REVIEW_STATE:
            failures.append(f"rows CSV {line_review_id} review state drifted")
        if row.get("crop_exists") != "true":
            failures.append(f"rows CSV {line_review_id} crop missing")
        if not row.get("priority_contact_sheet_path"):
            failures.append(f"rows CSV {line_review_id} missing priority contact sheet")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"rows CSV {line_review_id} {field} must be 0")
        if priority and priority not in normalized_doc:
            failures.append(f"{doc} missing priority: {priority}")
    normalized_priority_counts = {
        priority: priority_counts.get(priority, 0)
        for priority in EXPECTED_PRIORITY_COUNTS
    }
    if normalized_priority_counts != EXPECTED_PRIORITY_COUNTS:
        failures.append(f"rows CSV priority counts drifted: {priority_counts}")
    return failures


def validate_manifest(
    path: Path,
    data: dict[str, Any] | str,
    expected_rows: list[dict[str, str]],
    expected_summary: list[dict[str, str]],
) -> list[str]:
    if isinstance(data, str):
        return [data]
    expected: dict[str, Any] = {
        "tool": "build_cities_source_page_line_crop_priority_review_worksheet.py",
        "inputs": {
            "triage": str(DEFAULT_TRIAGE),
            "priority_contact": str(DEFAULT_PRIORITY_CONTACT),
        },
        "outputs": {
            "csv": str(DEFAULT_ROWS),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": len(expected_rows),
        "summary": {row["metric"]: row["value"] for row in expected_summary},
        "triage_fieldnames_match": True,
        "priority_contact_fieldnames_match": True,
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
        "review_state": builder.REVIEW_STATE,
        "claim_boundary": builder.CLAIM_BOUNDARY,
        "source_triage_boundary": triage_builder.CLAIM_BOUNDARY,
        "source_priority_contact_boundary": contact_builder.NO_INPUT_BOUNDARY,
    }
    failures: list[str] = []
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_no_source_text(texts_by_path: dict[Path, str]) -> list[str]:
    failures: list[str] = []
    for path, text in texts_by_path.items():
        if contains_hebrew_or_greek(text):
            failures.append(f"{path} appears to contain source-script body text")
    return failures


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            return reader.fieldnames or [], list(reader)
    except OSError as exc:
        return f"{path} could not be read: {exc}"


def read_json(path: Path) -> dict[str, Any] | str:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return f"{path} could not be read as JSON: {exc}"


if __name__ == "__main__":
    raise SystemExit(main())
