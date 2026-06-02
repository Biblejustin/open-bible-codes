#!/usr/bin/env python3
"""Validate Cities source-page line-crop review worksheet stays no-input."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_line_crop_review_worksheet as builder
from scripts import build_cities_source_page_line_crop_packet as packet_builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_PACKET = packet_builder.DEFAULT_OUT

EXPECTED_PAGE_COUNTS = {
    "cities_source_transcription_001": 44,
    "cities_source_transcription_002": 55,
    "cities_source_transcription_003": 54,
    "cities_source_transcription_004": 50,
}

REQUIRED_PHRASES = (
    "# Cities Source Page Line Crop Review Worksheet",
    "Status: no-input worksheet for future Cities source-page line-crop review.",
    "does not transcribe rows or import source rows",
    "No OCR body text or source-script body text appears",
    "Line-crop review rows: 203.",
    "Unique table pages: 4.",
    "Table-candidate page rows: 203.",
    "Crop images available: 203.",
    "OCR words represented by line boxes: 1511.",
    "OCR Hebrew letters represented by line boxes: 4934.",
    "Review state: `pending_line_crop_review`.",
    "Source-row imports: 0.",
    "City-name normalization: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "p-levels: 0.",
    "`cities_source_transcription_001`",
    "`cities_source_transcription_004`",
    "This worksheet organizes visual review only.",
    "Line crops are not verified source rows.",
    "before any source row can be imported",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_line_crop_review_worksheet_doc(
        args.doc,
        args.rows,
        args.manifest,
        args.packet,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities source-page line-crop worksheet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-page line-crop worksheet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    return parser


def validate_cities_source_page_line_crop_review_worksheet_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    manifest_json: Path = DEFAULT_MANIFEST,
    packet_csv: Path = DEFAULT_PACKET,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, manifest_json, packet_csv)
        if not path.exists()
    ]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    rows_text = rows_csv.read_text(encoding="utf-8")
    manifest_text = manifest_json.read_text(encoding="utf-8")
    normalized = normalize_space(text)

    rows_data = read_csv(rows_csv)
    packet_data = read_csv(packet_csv)
    if isinstance(rows_data, str):
        return [rows_data]
    if isinstance(packet_data, str):
        return [packet_data]
    _, rows = rows_data
    _, packet_rows = packet_data
    expected_rows = builder.build_worksheet_rows(packet_rows)
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
                manifest_json: manifest_text,
            }
        )
    )
    failures.extend(validate_packet_shape(packet_csv, packet_data))
    failures.extend(validate_rows_csv(rows_csv, rows_data, expected_rows))
    failures.extend(validate_rows(doc, normalized, rows))
    failures.extend(validate_manifest(manifest_json, manifest, expected_rows))
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


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    if len(rows) != 203:
        failures.append(f"rows CSV has {len(rows)} rows, expected 203")
    page_counts: dict[str, int] = {}
    ids = [row.get("line_review_id", "") for row in rows]
    expected_ids = [f"cities_source_line_crop_{index:03d}" for index in range(1, 204)]
    if ids != expected_ids:
        failures.append("rows CSV line review ids do not match expected 1..203 sequence")
    for row in rows:
        line_review_id = row.get("line_review_id", "")
        transcription_id = row.get("transcription_decision_id", "")
        page_counts[transcription_id] = page_counts.get(transcription_id, 0) + 1
        if row.get("review_state") != builder.REVIEW_STATE:
            failures.append(f"rows CSV {line_review_id} review state drifted")
        if row.get("crop_exists") != "true":
            failures.append(f"rows CSV {line_review_id} crop missing")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"rows CSV {line_review_id} {field} must be 0")
        if transcription_id and transcription_id not in normalized_doc:
            failures.append(f"{doc} missing transcription id: {transcription_id}")
    if page_counts != EXPECTED_PAGE_COUNTS:
        failures.append(f"rows CSV page counts drifted: {page_counts}")
    return failures


def validate_manifest(
    path: Path,
    data: dict[str, Any] | str,
    expected_rows: list[dict[str, str]],
) -> list[str]:
    if isinstance(data, str):
        return [data]
    expected: dict[str, Any] = {
        "tool": "build_cities_source_page_line_crop_review_worksheet.py",
        "inputs": {
            "packet": str(DEFAULT_PACKET),
            "html_review_aid": str(builder.DEFAULT_HTML_REVIEW_AID),
        },
        "outputs": {
            "csv": str(DEFAULT_ROWS),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": len(expected_rows),
        "unique_table_pages": 4,
        "crop_images_available": 203,
        "ocr_words": 1511,
        "ocr_hebrew_letters": 4934,
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
        "review_state": builder.REVIEW_STATE,
        "claim_boundary": builder.CLAIM_BOUNDARY,
        "source_packet_boundary": builder.NO_INPUT_BOUNDARY,
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


def contains_hebrew_or_greek(text: str) -> bool:
    for char in text:
        code = ord(char)
        if 0x0590 <= code <= 0x05FF or 0x0370 <= code <= 0x03FF:
            return True
    return False


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


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
