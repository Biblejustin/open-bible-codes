#!/usr/bin/env python3
"""Validate Cities source-page review bundle stays no-input."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_review_bundle as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_WORKSHEET = builder.DEFAULT_WORKSHEET

REQUIRED_PHRASES = (
    "# Cities Source Page Review Bundle",
    "Status: no-input page-image review bundle for locked Cities source pages.",
    "verifies page-image paths and dimensions",
    "No OCR body text or source-script body text appears",
    "does not import source rows",
    "Bundle rows: 14.",
    "Page images found: 14.",
    "Page images missing: 0.",
    "Table-bearing candidate pages: 4.",
    "Source-list candidate pages: 5.",
    "Exception-note candidate pages: 5.",
    "Source-row imports: 0.",
    "City-name normalization: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "p-levels: 0.",
    "`cities_source_transcription_001`",
    "`cities_source_transcription_014`",
    "Page-image existence is not transcription verification.",
    "Future source-row use still requires readable transcription",
)

EXPECTED_IDS = tuple(
    f"cities_source_transcription_{index:03d}" for index in range(1, 15)
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_review_bundle_doc(
        args.doc,
        args.rows,
        args.summary,
        args.manifest,
        args.worksheet,
    )
    if failures:
        for failure in failures:
            print(f"Cities source-page review bundle failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities source-page review bundle ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--worksheet", type=Path, default=DEFAULT_WORKSHEET)
    return parser


def validate_cities_source_page_review_bundle_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
    worksheet_csv: Path = DEFAULT_WORKSHEET,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, summary_csv, manifest_json, worksheet_csv)
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
    worksheet_data = read_csv(worksheet_csv)
    for data in (rows_data, summary_data, worksheet_data):
        if isinstance(data, str):
            return [data]

    _, rows = rows_data
    _, summary_rows = summary_data
    _, worksheet_rows = worksheet_data
    expected_rows = builder.build_bundle_rows(worksheet_rows)
    expected_summary = builder.build_summary_rows(expected_rows)
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
    failures.extend(validate_rows_csv(rows_csv, rows_data, expected_rows))
    failures.extend(validate_summary_csv(summary_csv, summary_data, expected_summary))
    failures.extend(validate_rows(doc, normalized, rows))
    failures.extend(validate_artifact_paths(rows_csv, rows))
    failures.extend(validate_manifest(manifest_json, manifest, expected_rows, expected_summary, worksheet_csv))
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
    expected_rows: list[dict[str, str]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.SUMMARY_FIELDNAMES:
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
    if len(rows) != 14:
        failures.append(f"rows CSV has {len(rows)} rows, expected 14")
    ids = [row.get("transcription_decision_id", "") for row in rows]
    if tuple(ids) != EXPECTED_IDS:
        failures.append("rows CSV transcription ids do not match expected 1..14 sequence")
    for row in rows:
        decision_id = row.get("transcription_decision_id", "")
        if row.get("page_image_exists") != "true":
            failures.append(f"rows CSV {decision_id} page image missing")
        if row.get("page_image_width") == "0" or row.get("page_image_height") == "0":
            failures.append(f"rows CSV {decision_id} page image dimensions missing")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"rows CSV {decision_id} {field} must be 0")
        if decision_id and decision_id not in normalized_doc:
            failures.append(f"{doc} missing transcription decision id: {decision_id}")
    return failures


def validate_artifact_paths(
    rows_csv: Path,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    for row in rows:
        decision_id = row.get("transcription_decision_id", "")
        for field in ("selected_path", "page_image_path"):
            value = row.get(field, "").strip()
            if not value:
                failures.append(f"{rows_csv} {decision_id} missing {field}")
                continue
            if not Path(value).exists():
                failures.append(f"{rows_csv} {decision_id} {field} not found: {value}")
    return failures


def validate_manifest(
    path: Path,
    data: dict[str, Any] | str,
    expected_rows: list[dict[str, str]],
    expected_summary: list[dict[str, str]],
    worksheet_csv: Path,
) -> list[str]:
    if isinstance(data, str):
        return [data]
    expected: dict[str, Any] = {
        "tool": "build_cities_source_page_review_bundle.py",
        "inputs": {"worksheet": str(worksheet_csv)},
        "outputs": {
            "csv": str(DEFAULT_ROWS),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": len(expected_rows),
        "summary": {row["metric"]: row["value"] for row in expected_summary},
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
    if not path.exists():
        return f"{path} is missing"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
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
