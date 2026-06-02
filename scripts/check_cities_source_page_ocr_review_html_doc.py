#!/usr/bin/env python3
"""Validate Cities source-page OCR review HTML handoff stays local-only."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_ocr_review_html as builder
from scripts.json_utils import read_json_object


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_HTML = builder.DEFAULT_HTML
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_PACKET = builder.DEFAULT_PACKET

EXPECTED_SUMMARY = {
    "html_rows": "14",
    "html_exists": "true",
    "html_path": str(DEFAULT_HTML),
    "html_embeds_ocr_text": "true",
    "html_embedded_ocr_text_rows": "14",
    "page_images_found": "14",
    "ocr_text_sidecars": "14",
    "pages_with_ocr_text": "14",
    "ocr_hebrew_letters": "14408",
    "ocr_words": "3939",
    "ocr_lines": "596",
    "source_row_imports": "0",
    "city_name_normalization": "0",
    "els_runs": "0",
    "compactness_runs": "0",
    "p_levels": "0",
    "tracked_no_input_boundary": builder.NO_INPUT_BOUNDARY,
    "local_html_boundary": builder.LOCAL_HTML_BOUNDARY,
}

REQUIRED_PHRASES = (
    "# Cities Source Page OCR Review HTML",
    "Status: local ignored HTML review aid for locked Cities source-page OCR.",
    "The HTML file embeds OCR sidecar text",
    "Tracked files contain no OCR body text or source-script body text.",
    "HTML review aid: `reports/cities_pdf_recovery_probe/source_page_ocr_review/source_page_ocr_review.html`.",
    "HTML rows: 14.",
    "HTML embeds OCR text: `true`.",
    "HTML embedded OCR text rows: 14.",
    "Page images found: 14.",
    "OCR text sidecars: 14.",
    "Pages with OCR text: 14.",
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
    "The ignored HTML file may display OCR text; tracked files do not.",
    "OCR text is a review aid, not verified transcription.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_ocr_review_html_doc(
        args.doc,
        args.html,
        args.summary,
        args.manifest,
        args.packet,
    )
    if failures:
        for failure in failures:
            print(f"Cities source-page OCR HTML failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities source-page OCR HTML ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    return parser


def validate_cities_source_page_ocr_review_html_doc(
    doc: Path,
    html_path: Path | None = DEFAULT_HTML,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
    packet: Path | None = DEFAULT_PACKET,
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
    if html_path is not None:
        failures.extend(validate_local_html(html_path))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    if packet is not None:
        failures.extend(validate_packet_shape(packet))
    return failures


def validate_local_html(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    text = path.read_text(encoding="utf-8")
    failures: list[str] = []
    if "Cities Source Page OCR Review" not in text:
        failures.append(f"{path} missing review title")
    if text.count('<section class="page">') != 14:
        failures.append(f"{path} page section count drifted")
    if not contains_hebrew_or_greek(text):
        failures.append(f"{path} should contain local OCR text")
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
        "tool": "build_cities_source_page_ocr_review_html.py",
        "inputs": {"packet": str(DEFAULT_PACKET)},
        "outputs": {
            "html": str(DEFAULT_HTML),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": 14,
        "summary": EXPECTED_SUMMARY,
        "tracked_no_input_boundary": builder.NO_INPUT_BOUNDARY,
        "local_html_boundary": builder.LOCAL_HTML_BOUNDARY,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_packet_shape(path: Path) -> list[str]:
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
