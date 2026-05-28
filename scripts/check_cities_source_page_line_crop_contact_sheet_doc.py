#!/usr/bin/env python3
"""Validate Cities source-page line-crop contact sheets stay review-only."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_line_crop_contact_sheet as builder
from scripts import build_cities_source_page_line_crop_packet as packet_builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_PACKET = builder.DEFAULT_PACKET

EXPECTED_PAGE_COUNTS = {
    "cities_source_transcription_001": 44,
    "cities_source_transcription_002": 55,
    "cities_source_transcription_003": 54,
    "cities_source_transcription_004": 50,
}

REQUIRED_PHRASES = (
    "# Cities Source Page Line Crop Contact Sheet",
    "Status: local visual contact sheets for Cities source-page line-crop review.",
    "without transcribing Hebrew or importing source rows",
    "Tracked files contain no OCR body text or source-script body text.",
    "Table pages: 4.",
    "Line crop rows: 203.",
    "Line crop images found: 203.",
    "Contact sheets: 4.",
    "Contact sheets available: 4.",
    "OCR words represented by line boxes: 1511.",
    "OCR Hebrew letters represented by line boxes: 4934.",
    "Source-row imports: 0.",
    "City-name normalization: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "p-levels: 0.",
    "`cities_source_transcription_001`",
    "`cities_source_transcription_004`",
    "Contact sheets are not transcription verification.",
    "it does not read or import Hebrew source rows",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_line_crop_contact_sheet_doc(
        args.doc,
        args.rows,
        args.summary,
        args.manifest,
        args.packet,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities source-page line-crop contact sheet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-page line-crop contact sheet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    return parser


def validate_cities_source_page_line_crop_contact_sheet_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
    packet_csv: Path = DEFAULT_PACKET,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, summary_csv, manifest_json, packet_csv)
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
    if isinstance(rows_data, str):
        return [rows_data]
    if isinstance(summary_data, str):
        return [summary_data]
    if isinstance(packet_data, str):
        return [packet_data]
    _, rows = rows_data
    _, packet_rows = packet_data
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
    failures.extend(validate_rows_csv(rows_csv, rows_data))
    failures.extend(validate_summary_csv(summary_csv, summary_data))
    failures.extend(validate_rows(doc, normalized, rows))
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
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    summary = {row["metric"]: row["value"] for row in rows}
    expected = {
        "table_pages": "4",
        "line_crop_rows": "203",
        "line_crop_images_found": "203",
        "contact_sheets": "4",
        "contact_sheets_available": "4",
        "ocr_words": "1511",
        "ocr_hebrew_letters": "4934",
        "source_row_imports": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "no_input_boundary": builder.NO_INPUT_BOUNDARY,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            failures.append(f"{path} {key}={summary.get(key)!r}; expected {value!r}")
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    page_counts = {
        row.get("transcription_decision_id", ""): int(row.get("line_crop_rows", "0"))
        for row in rows
    }
    if page_counts != EXPECTED_PAGE_COUNTS:
        failures.append(f"rows CSV page counts drifted: {page_counts}")
    for row in rows:
        transcription_id = row.get("transcription_decision_id", "")
        if row.get("contact_sheet_exists") != "true":
            failures.append(f"rows CSV {transcription_id} contact sheet missing")
        image_path = Path(row.get("contact_sheet_path", ""))
        if not image_path.exists():
            failures.append(f"{image_path} is missing")
        else:
            actual_width, actual_height = builder.png_dimensions(image_path)
            if row.get("contact_sheet_width") != str(actual_width):
                failures.append(f"rows CSV {transcription_id} width drifted")
            if row.get("contact_sheet_height") != str(actual_height):
                failures.append(f"rows CSV {transcription_id} height drifted")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"rows CSV {transcription_id} {field} must be 0")
        if transcription_id and transcription_id not in normalized_doc:
            failures.append(f"{doc} missing transcription id: {transcription_id}")
    return failures


def validate_manifest(path: Path, data: dict[str, Any] | str) -> list[str]:
    if isinstance(data, str):
        return [data]
    expected: dict[str, Any] = {
        "tool": "build_cities_source_page_line_crop_contact_sheet.py",
        "inputs": {"packet": str(DEFAULT_PACKET)},
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
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return f"{path} could not be read as JSON: {exc}"


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
