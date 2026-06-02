#!/usr/bin/env python3
"""Validate Cities line-crop band review worksheet stays no-input."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_line_crop_band_map as band_builder
from scripts import build_cities_source_page_line_crop_band_review_worksheet as builder
from scripts.check_cities_source_page_line_crop_contact_sheet_doc import (
    contains_hebrew_or_greek,
    normalize_space,
)


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_BAND_MAP = builder.DEFAULT_BAND_MAP

EXPECTED_BANDS_BY_PAGE = {
    "cities_source_transcription_001": 7,
    "cities_source_transcription_002": 2,
    "cities_source_transcription_003": 2,
    "cities_source_transcription_004": 5,
}

REQUIRED_PHRASES = (
    "# Cities Source Page Line Crop Band Review Worksheet",
    "Status: no-input worksheet for future Cities source-page line-crop band review.",
    "reduces the 203 line crops into coordinate bands",
    "No OCR body text or source-script body text appears",
    "Band review rows: 16.",
    "Source line rows represented: 203.",
    "Unique table pages: 4.",
    "Crop images available: 203.",
    "OCR words represented by line boxes: 1511.",
    "OCR Hebrew letters represented by line boxes: 4934.",
    "Review state: `pending_band_visual_review`.",
    "Source-row imports: 0.",
    "City-name normalization: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "p-levels: 0.",
    "coordinate-band review only",
    "not a verified source row",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_line_crop_band_review_worksheet_doc(
        args.doc,
        rows_csv=args.rows,
        summary_csv=args.summary,
        manifest_json=args.manifest,
        band_map_csv=args.band_map,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities source-page line-crop band worksheet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-page line-crop band worksheet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--band-map", type=Path, default=DEFAULT_BAND_MAP)
    return parser


def validate_cities_source_page_line_crop_band_review_worksheet_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
    band_map_csv: Path = DEFAULT_BAND_MAP,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, summary_csv, manifest_json, band_map_csv)
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
    band_data = read_csv(band_map_csv)
    if isinstance(rows_data, str):
        return [rows_data]
    if isinstance(summary_data, str):
        return [summary_data]
    if isinstance(band_data, str):
        return [band_data]

    band_fieldnames, band_rows = band_data
    expected_rows = builder.build_review_rows(band_rows)
    expected_summary = builder.build_summary_rows(band_fieldnames, band_rows, expected_rows)
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
    failures.extend(validate_band_map_shape(band_map_csv, band_data))
    failures.extend(validate_rows_csv(rows_csv, rows_data, expected_rows))
    failures.extend(validate_summary_csv(summary_csv, summary_data, expected_summary))
    failures.extend(validate_rows(doc, normalized, rows_data[1]))
    failures.extend(validate_manifest(manifest_json, manifest, expected_rows, expected_summary))
    return failures


def validate_band_map_shape(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != band_builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 16:
        failures.append(f"{path} has {len(rows)} rows, expected 16")
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
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    if len(rows) != 16:
        failures.append(f"rows CSV has {len(rows)} rows, expected 16")
    ids = [row.get("band_review_id", "") for row in rows]
    expected_ids = [f"cities_source_band_review_{index:03d}" for index in range(1, 17)]
    if ids != expected_ids:
        failures.append("rows CSV band review ids do not match expected 1..16 sequence")
    page_counts: dict[str, int] = {}
    for row in rows:
        band_review_id = row.get("band_review_id", "")
        transcription_id = row.get("transcription_decision_id", "")
        page_counts[transcription_id] = page_counts.get(transcription_id, 0) + 1
        if row.get("review_state") != builder.REVIEW_STATE:
            failures.append(f"rows CSV {band_review_id} review state drifted")
        if row.get("crop_images_available") == "0":
            failures.append(f"rows CSV {band_review_id} has no crop images")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"rows CSV {band_review_id} {field} must be 0")
        if transcription_id and transcription_id not in normalized_doc:
            failures.append(f"{doc} missing transcription id: {transcription_id}")
    if page_counts != EXPECTED_BANDS_BY_PAGE:
        failures.append(f"rows CSV page counts drifted: {page_counts}")
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
        "tool": "build_cities_source_page_line_crop_band_review_worksheet.py",
        "inputs": {"band_map": str(DEFAULT_BAND_MAP)},
        "outputs": {
            "csv": str(DEFAULT_ROWS),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": len(expected_rows),
        "summary": {row["metric"]: row["value"] for row in expected_summary},
        "band_map_fieldnames_match": True,
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
        "review_state": builder.REVIEW_STATE,
        "claim_boundary": builder.CLAIM_BOUNDARY,
        "source_band_boundary": band_builder.CLAIM_BOUNDARY,
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
