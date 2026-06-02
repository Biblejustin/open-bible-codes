#!/usr/bin/env python3
"""Validate Cities priority contact sheets stay review-only."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_line_crop_priority_contact_sheet as builder
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

EXPECTED_PRIORITY_COUNTS = {
    "priority_1_dense_text": 120,
    "priority_2_medium_text": 71,
    "priority_3_short_text": 12,
    "priority_4_no_text": 0,
}

REQUIRED_PHRASES = (
    "# Cities Source Page Line Crop Priority Contact Sheet",
    "Status: local visual contact sheets for Cities source-page line-crop triage priorities.",
    "group crop images by priority without transcribing Hebrew or importing source rows",
    "Tracked files contain no OCR body text or source-script body text.",
    "Priority contact sheets: 4.",
    "Priority contact sheets available: 4.",
    "Line crop rows: 203.",
    "Line crop images found: 203.",
    "OCR words represented by line boxes: 1511.",
    "OCR Hebrew letters represented by line boxes: 4934.",
    "Dense-text priority rows: 120.",
    "Medium-text priority rows: 71.",
    "Short-text priority rows: 12.",
    "No-text priority rows: 0.",
    "Source-row imports: 0.",
    "City-name normalization: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "p-levels: 0.",
    "`priority_1_dense_text`",
    "`priority_4_no_text`",
    "Priority contact sheets are not transcription verification.",
    "Any future import still needs explicit source-row evidence",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_line_crop_priority_contact_sheet_doc(
        args.doc,
        rows_csv=args.rows,
        summary_csv=args.summary,
        manifest_json=args.manifest,
        triage_csv=args.triage,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities source-page line-crop priority contact sheet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-page line-crop priority contact sheet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--triage", type=Path, default=DEFAULT_TRIAGE)
    return parser


def validate_cities_source_page_line_crop_priority_contact_sheet_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
    triage_csv: Path = DEFAULT_TRIAGE,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, summary_csv, manifest_json, triage_csv)
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
    if isinstance(rows_data, str):
        return [rows_data]
    if isinstance(summary_data, str):
        return [summary_data]
    if isinstance(triage_data, str):
        return [triage_data]
    _, rows = rows_data
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
    failures.extend(validate_rows_csv(rows_csv, rows_data))
    failures.extend(validate_summary_csv(summary_csv, summary_data, triage_data, rows))
    failures.extend(validate_rows(doc, normalized, rows))
    failures.extend(validate_manifest(manifest_json, manifest))
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


def validate_rows_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 4:
        failures.append(f"{path} has {len(rows)} rows, expected 4")
    return failures


def validate_summary_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
    triage_data: tuple[list[str], list[dict[str, str]]],
    sheet_rows: list[dict[str, str]],
) -> list[str]:
    fieldnames, rows = data
    triage_fieldnames, triage_rows = triage_data
    failures: list[str] = []
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    expected = builder.build_summary_rows(triage_fieldnames, triage_rows, sheet_rows)
    if rows != expected:
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
    priority_counts = {
        row.get("review_priority", ""): int(row.get("line_crop_rows", "0"))
        for row in rows
    }
    if priority_counts != EXPECTED_PRIORITY_COUNTS:
        failures.append(f"rows CSV priority counts drifted: {priority_counts}")
    for row in rows:
        priority = row.get("review_priority", "")
        if row.get("contact_sheet_exists") != "true":
            failures.append(f"rows CSV {priority} contact sheet missing")
        image_path = Path(row.get("contact_sheet_path", ""))
        if not image_path.exists():
            failures.append(f"{image_path} is missing")
        else:
            actual_width, actual_height = builder.png_dimensions(image_path)
            if row.get("contact_sheet_width") != str(actual_width):
                failures.append(f"rows CSV {priority} width drifted")
            if row.get("contact_sheet_height") != str(actual_height):
                failures.append(f"rows CSV {priority} height drifted")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"rows CSV {priority} {field} must be 0")
        if priority and priority not in normalized_doc:
            failures.append(f"{doc} missing priority: {priority}")
    return failures


def validate_manifest(path: Path, data: dict[str, Any] | str) -> list[str]:
    if isinstance(data, str):
        return [data]
    expected: dict[str, Any] = {
        "tool": "build_cities_source_page_line_crop_priority_contact_sheet.py",
        "inputs": {"triage": str(DEFAULT_TRIAGE)},
        "outputs": {
            "base_dir": str(builder.DEFAULT_BASE_DIR),
            "csv": str(DEFAULT_ROWS),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": 4,
        "line_crop_rows": 203,
        "no_input_boundary": builder.NO_INPUT_BOUNDARY,
        "claim_boundary": builder.CLAIM_BOUNDARY,
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
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return f"{path} could not be read as JSON: {exc}"
    except json.JSONDecodeError as exc:
        return f"{path} is invalid JSON: {exc}"
    if not isinstance(data, dict):
        return f"{path} JSON root must be an object"
    return data


if __name__ == "__main__":
    raise SystemExit(main())
