#!/usr/bin/env python3
"""Validate Cities source-page OCR review packet stays non-importing."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_ocr_review_packet as builder
from scripts.json_utils import read_json_object


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_PACKET = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_BUNDLE = builder.DEFAULT_BUNDLE

EXPECTED_SUMMARY = {
    "source_page_ocr_rows": "14",
    "page_images_found": "14",
    "page_images_missing": "0",
    "ocr_pages_attempted": "14",
    "pages_with_ocr_text": "14",
    "pages_with_low_ocr_text": "0",
    "pages_with_empty_ocr_text": "0",
    "ocr_errors": "0",
    "blocked_missing_ocr_dependency": "0",
    "ocr_text_sidecars": "14",
    "ocr_text_signal_chars": "14872",
    "ocr_hebrew_letters": "14408",
    "ocr_words": "3939",
    "ocr_lines": "596",
    "language": "heb",
    "psm": "4",
    "tessdata_dir": "reports/wrr_1994/tessdata",
    "source_row_imports": "0",
    "city_name_normalization": "0",
    "els_runs": "0",
    "compactness_runs": "0",
    "p_levels": "0",
    "no_input_boundary": builder.NO_INPUT_BOUNDARY,
}

REQUIRED_PHRASES = (
    "# Cities Source Page OCR Review Packet",
    "Status: local Hebrew OCR review packet for locked Cities source pages.",
    "OCR text sidecars are local ignored review aids only.",
    "Tracked files contain no OCR body text or source-script body text.",
    "Source-page OCR rows: 14.",
    "Page images found: 14.",
    "Page images missing: 0.",
    "OCR pages attempted: 14.",
    "Pages with OCR text: 14.",
    "OCR text sidecars: 14.",
    "OCR Hebrew letters: 14408.",
    "OCR words: 3939.",
    "OCR lines: 596.",
    "Source-row imports: 0.",
    "City-name normalization: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "p-levels: 0.",
    "`cities_source_transcription_001`",
    "`cities_source_transcription_014`",
    "OCR sidecar availability is not transcription verification.",
    "the tracked packet does not quote source text",
    "Future source-row import still requires",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_ocr_review_packet_doc(
        args.doc,
        args.packet,
        args.summary,
        args.manifest,
        args.bundle,
    )
    if failures:
        for failure in failures:
            print(f"Cities source-page OCR packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities source-page OCR packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    return parser


def validate_cities_source_page_ocr_review_packet_doc(
    doc: Path,
    packet: Path | None = DEFAULT_PACKET,
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
    if packet is not None:
        failures.extend(validate_packet_csv(packet))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    if bundle is not None:
        failures.extend(validate_bundle_rows(bundle))
    return failures


def validate_packet_csv(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    raw_text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: raw_text})
    fieldnames, rows = read_csv(path)
    if fieldnames != builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 14:
        failures.append(f"{path} has {len(rows)} rows, expected 14")
    for index, row in enumerate(rows, start=1):
        expected_id = f"cities_source_transcription_{index:03d}"
        if row.get("ocr_rank") != str(index):
            failures.append(f"{path} row {index} rank drifted")
        if row.get("transcription_decision_id") != expected_id:
            failures.append(f"{path} row {index} transcription id drifted")
        if row.get("ocr_status") != "source_page_ocr_text_detected":
            failures.append(f"{path} row {index} OCR status drifted")
        if row.get("ocr_text_exists") != "true":
            failures.append(f"{path} row {index} OCR sidecar missing")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"{path} row {index} {field} must be 0")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    raw_text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: raw_text})
    fieldnames, rows = read_csv(path)
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    summary = {row["metric"]: row["value"] for row in rows}
    for key, value in EXPECTED_SUMMARY.items():
        if summary.get(key) != value:
            failures.append(f"{path} {key}={summary.get(key)!r}; expected {value!r}")
    return failures


def validate_manifest(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    raw_text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: raw_text})
    try:
        data = read_json_object(path)
    except ValueError as exc:
        failures.append(str(exc))
        return failures
    expected: dict[str, Any] = {
        "tool": "build_cities_source_page_ocr_review_packet.py",
        "inputs": {
            "bundle": str(DEFAULT_BUNDLE),
            "tessdata_dir": str(builder.DEFAULT_TESSDATA_DIR),
            "language": "heb",
            "psm": "4",
        },
        "outputs": {
            "csv": str(DEFAULT_PACKET),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
            "base_dir": str(builder.DEFAULT_BASE_DIR),
        },
        "rows": 14,
        "summary": EXPECTED_SUMMARY,
        "no_input_boundary": builder.NO_INPUT_BOUNDARY,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_bundle_rows(path: Path) -> list[str]:
    fieldnames, rows = read_csv(path)
    failures: list[str] = []
    if not fieldnames:
        failures.append(f"{path} is missing fieldnames")
    if len(rows) != 14:
        failures.append(f"{path} has {len(rows)} rows, expected 14")
    for index, row in enumerate(rows, start=1):
        expected_id = f"cities_source_transcription_{index:03d}"
        if row.get("transcription_decision_id") != expected_id:
            failures.append(f"{path} row {index} transcription id drifted")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"{path} row {index} {field} must be 0")
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


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
