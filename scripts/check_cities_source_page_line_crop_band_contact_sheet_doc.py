#!/usr/bin/env python3
"""Validate Cities band contact sheets stay review-only."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_line_crop_band_contact_sheet as builder
from scripts import build_cities_source_page_line_crop_band_review_worksheet as band_review
from scripts import build_cities_source_page_line_crop_packet as packet_builder
from scripts.check_cities_source_page_line_crop_contact_sheet_doc import (
    contains_hebrew_or_greek,
    normalize_space,
)


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_PACKET = builder.DEFAULT_PACKET
DEFAULT_BAND_REVIEW = builder.DEFAULT_BAND_REVIEW

EXPECTED_BANDS_BY_PAGE = {
    "cities_source_transcription_001": 7,
    "cities_source_transcription_002": 2,
    "cities_source_transcription_003": 2,
    "cities_source_transcription_004": 5,
}

REQUIRED_PHRASES = (
    "# Cities Source Page Line Crop Band Contact Sheet",
    "Status: local visual contact sheets for Cities source-page line-crop coordinate bands.",
    "group crop images by coordinate band without transcribing Hebrew or importing source rows",
    "Tracked files contain no OCR body text or source-script body text.",
    "Band contact sheets: 16.",
    "Band contact sheets available: 16.",
    "Band review rows: 16.",
    "Line crop rows: 203.",
    "Line crop images found: 203.",
    "Unique table pages: 4.",
    "OCR words represented by line boxes: 1511.",
    "OCR Hebrew letters represented by line boxes: 4934.",
    "Source-row imports: 0.",
    "City-name normalization: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "p-levels: 0.",
    "`cities_source_band_review_001`",
    "`cities_source_band_review_016`",
    "Band contact sheets are not transcription verification.",
    "Any future import still needs explicit source-row evidence",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_line_crop_band_contact_sheet_doc(
        args.doc,
        rows_csv=args.rows,
        summary_csv=args.summary,
        manifest_json=args.manifest,
        packet_csv=args.packet,
        band_review_csv=args.band_review,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities source-page line-crop band contact sheet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-page line-crop band contact sheet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--band-review", type=Path, default=DEFAULT_BAND_REVIEW)
    return parser


def validate_cities_source_page_line_crop_band_contact_sheet_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
    packet_csv: Path = DEFAULT_PACKET,
    band_review_csv: Path = DEFAULT_BAND_REVIEW,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, summary_csv, manifest_json, packet_csv, band_review_csv)
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
    packet_data = read_csv(packet_csv)
    band_data = read_csv(band_review_csv)
    if isinstance(rows_data, str):
        return [rows_data]
    if isinstance(summary_data, str):
        return [summary_data]
    if isinstance(packet_data, str):
        return [packet_data]
    if isinstance(band_data, str):
        return [band_data]
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
    failures.extend(validate_packet_shape(packet_csv, packet_data))
    failures.extend(validate_band_review_shape(band_review_csv, band_data))
    failures.extend(validate_rows_csv(rows_csv, rows_data))
    failures.extend(validate_summary_csv(summary_csv, summary_data, packet_data, band_data, rows))
    failures.extend(validate_rows(doc, normalized, rows, band_data[1]))
    failures.extend(validate_manifest(manifest_json, manifest))
    return failures


def validate_packet_shape(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != packet_builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 203:
        failures.append(f"{path} has {len(rows)} rows, expected 203")
    return failures


def validate_band_review_shape(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != band_review.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 16:
        failures.append(f"{path} has {len(rows)} rows, expected 16")
    return failures


def validate_rows_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 16:
        failures.append(f"{path} has {len(rows)} rows, expected 16")
    return failures


def validate_summary_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
    packet_data: tuple[list[str], list[dict[str, str]]],
    band_data: tuple[list[str], list[dict[str, str]]],
    sheet_rows: list[dict[str, str]],
) -> list[str]:
    fieldnames, rows = data
    packet_fieldnames, packet_rows = packet_data
    band_fieldnames, band_rows = band_data
    failures: list[str] = []
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    expected = builder.build_summary_rows(
        packet_fieldnames,
        packet_rows,
        band_fieldnames,
        band_rows,
        sheet_rows,
    )
    if rows != expected:
        failures.append(f"{path} summary data drifted")
    summary = {row["metric"]: row["value"] for row in rows}
    for transcription_id, expected_count in EXPECTED_BANDS_BY_PAGE.items():
        metric = f"bands_{transcription_id}"
        if summary.get(metric) != str(expected_count):
            failures.append(f"{path} {metric}={summary.get(metric)!r}")
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
    band_rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    ids = [row.get("band_review_id", "") for row in rows]
    expected_ids = [f"cities_source_band_review_{index:03d}" for index in range(1, 17)]
    if ids != expected_ids:
        failures.append("rows CSV band review ids do not match expected 1..16 sequence")
    band_line_counts = {
        row.get("band_review_id", ""): row.get("line_crop_rows", "") for row in band_rows
    }
    page_counts: dict[str, int] = {}
    total_rows = 0
    total_images = 0
    for row in rows:
        band_review_id = row.get("band_review_id", "")
        transcription_id = row.get("transcription_decision_id", "")
        page_counts[transcription_id] = page_counts.get(transcription_id, 0) + 1
        total_rows += int(row.get("line_crop_rows", "0"))
        total_images += int(row.get("line_crop_images_found", "0"))
        if row.get("line_crop_rows") != band_line_counts.get(band_review_id):
            failures.append(f"rows CSV {band_review_id} line crop count drifted")
        if row.get("contact_sheet_exists") != "true":
            failures.append(f"rows CSV {band_review_id} contact sheet missing")
        image_path = Path(row.get("contact_sheet_path", ""))
        if not image_path.exists():
            failures.append(f"{image_path} is missing")
        else:
            actual_width, actual_height = builder.png_dimensions(image_path)
            if row.get("contact_sheet_width") != str(actual_width):
                failures.append(f"rows CSV {band_review_id} width drifted")
            if row.get("contact_sheet_height") != str(actual_height):
                failures.append(f"rows CSV {band_review_id} height drifted")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"rows CSV {band_review_id} {field} must be 0")
        if band_review_id and band_review_id not in normalized_doc:
            failures.append(f"{doc} missing band review id: {band_review_id}")
    if page_counts != EXPECTED_BANDS_BY_PAGE:
        failures.append(f"rows CSV page counts drifted: {page_counts}")
    if total_rows != 203:
        failures.append(f"rows CSV line crop total is {total_rows}, expected 203")
    if total_images != 203:
        failures.append(f"rows CSV image total is {total_images}, expected 203")
    return failures


def validate_manifest(path: Path, data: dict[str, Any] | str) -> list[str]:
    if isinstance(data, str):
        return [data]
    expected: dict[str, Any] = {
        "tool": "build_cities_source_page_line_crop_band_contact_sheet.py",
        "inputs": {
            "packet": str(DEFAULT_PACKET),
            "band_review": str(DEFAULT_BAND_REVIEW),
        },
        "outputs": {
            "base_dir": str(builder.DEFAULT_BASE_DIR),
            "csv": str(DEFAULT_ROWS),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": 16,
        "line_crop_rows": 203,
        "packet_rows": 203,
        "band_review_rows": 16,
        "no_input_boundary": builder.NO_INPUT_BOUNDARY,
        "claim_boundary": builder.band_review.CLAIM_BOUNDARY,
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
