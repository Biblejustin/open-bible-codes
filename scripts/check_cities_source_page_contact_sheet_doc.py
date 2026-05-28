#!/usr/bin/env python3
"""Validate Cities source-page contact sheet stays a local review aid."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_contact_sheet as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_IMAGE = builder.DEFAULT_CONTACT_SHEET
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_BUNDLE = builder.DEFAULT_BUNDLE
EXPECTED_DIMENSIONS = (808, 4114)

REQUIRED_PHRASES = (
    "# Cities Source Page Contact Sheet",
    "Status: local visual contact sheet for locked Cities source-page review.",
    "It is a review aid only; it is not transcription verification",
    "Tracked files contain no OCR body text or source-script body text.",
    "Contact sheet image: `reports/cities_pdf_recovery_probe/cities_source_page_contact_sheet.png`.",
    "Contact sheet pages: 14.",
    "Contact sheet dimensions: 808 x 4114.",
    "Page images found: 14.",
    "Page images missing: 0.",
    "Source-row imports: 0.",
    "City-name normalization: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "p-levels: 0.",
    "`cities_source_transcription_001`",
    "`cities_source_transcription_014`",
    "Contact-sheet availability is not transcription verification.",
    "before any source-row import",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_contact_sheet_doc(
        args.doc,
        args.image,
        args.summary,
        args.manifest,
        args.bundle,
    )
    if failures:
        for failure in failures:
            print(f"Cities source-page contact sheet failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities source-page contact sheet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    return parser


def validate_cities_source_page_contact_sheet_doc(
    doc: Path,
    image: Path | None = DEFAULT_IMAGE,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
    bundle: Path | None = DEFAULT_BUNDLE,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized_text
    ]
    failures.extend(validate_no_source_text({doc: text}))
    if image is not None:
        failures.extend(validate_contact_sheet_image(image))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    if bundle is not None:
        failures.extend(validate_bundle_rows(doc, normalized_text, bundle))
    return failures


def validate_contact_sheet_image(image: Path) -> list[str]:
    if not image.exists():
        return [f"{image} is missing"]
    actual = builder.png_dimensions(image)
    if actual != EXPECTED_DIMENSIONS:
        return [f"{image} dimensions {actual} expected {EXPECTED_DIMENSIONS}"]
    return []


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        return [f"{path} fieldnames drifted"]
    summary = {row["metric"]: row["value"] for row in rows}
    expected = {
        "contact_sheet_pages": "14",
        "contact_sheet_exists": "true",
        "contact_sheet_path": str(DEFAULT_IMAGE),
        "contact_sheet_width": str(EXPECTED_DIMENSIONS[0]),
        "contact_sheet_height": str(EXPECTED_DIMENSIONS[1]),
        "page_images_found": "14",
        "page_images_missing": "0",
        "source_row_imports": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "no_input_boundary": builder.NO_INPUT_BOUNDARY,
    }
    failures: list[str] = []
    for key, value in expected.items():
        if summary.get(key) != value:
            failures.append(f"{path} {key}={summary.get(key)!r}; expected {value!r}")
    return failures


def validate_manifest(path: Path) -> list[str]:
    data = read_json(path)
    if isinstance(data, str):
        return [data]
    expected: dict[str, Any] = {
        "tool": "build_cities_source_page_contact_sheet.py",
        "inputs": {"bundle": str(DEFAULT_BUNDLE)},
        "outputs": {
            "contact_sheet": str(DEFAULT_IMAGE),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": 14,
        "contact_sheet": {
            "contact_sheet_exists": True,
            "contact_sheet_path": str(DEFAULT_IMAGE),
            "contact_sheet_pages": 14,
            "contact_sheet_width": EXPECTED_DIMENSIONS[0],
            "contact_sheet_height": EXPECTED_DIMENSIONS[1],
        },
        "no_input_boundary": builder.NO_INPUT_BOUNDARY,
    }
    failures: list[str] = []
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_bundle_rows(
    doc: Path,
    normalized_doc: str,
    bundle: Path,
) -> list[str]:
    data = read_csv(bundle)
    if isinstance(data, str):
        return [data]
    _fieldnames, rows = data
    failures: list[str] = []
    if len(rows) != 14:
        failures.append(f"{bundle} has {len(rows)} rows, expected 14")
    for index, row in enumerate(rows, start=1):
        expected_id = f"cities_source_transcription_{index:03d}"
        if row.get("transcription_decision_id") != expected_id:
            failures.append(f"{bundle} rank {index} transcription id drifted")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"{bundle} rank {index} {field} must be 0")
        if expected_id not in normalized_doc:
            failures.append(f"{doc} missing transcription id {expected_id}")
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
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
