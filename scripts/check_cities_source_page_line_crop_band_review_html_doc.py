#!/usr/bin/env python3
"""Validate Cities source-page line-crop band HTML stays local-only."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_line_crop_band_contact_sheet as contact_builder
from scripts import build_cities_source_page_line_crop_band_review_html as builder
from scripts.check_cities_source_page_line_crop_review_html_doc import (
    contains_hebrew_or_greek,
    normalize_space,
)
from scripts.json_utils import read_json_object


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_HTML = builder.DEFAULT_HTML
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_BAND_CONTACT = builder.DEFAULT_BAND_CONTACT

EXPECTED_BANDS_BY_PAGE = {
    "cities_source_transcription_001": 7,
    "cities_source_transcription_002": 2,
    "cities_source_transcription_003": 2,
    "cities_source_transcription_004": 5,
}

REQUIRED_PHRASES = (
    "# Cities Source Page Line Crop Band Review HTML",
    "Status: local ignored HTML review aid for Cities source-page line-crop coordinate bands.",
    "displays band contact-sheet images only",
    "embeds no OCR text or source-script text",
    "HTML band review aid: `reports/cities_pdf_recovery_probe/source_page_line_crops/band_review.html`.",
    "HTML rows: 16.",
    "HTML embeds source text: `false`.",
    "HTML band image rows: 16.",
    "Band contact-sheet rows: 16.",
    "Band contact sheets available: 16.",
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
    "The ignored HTML file displays band contact-sheet images only.",
    "The band view is not transcription",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_line_crop_band_review_html_doc(
        args.doc,
        html_path=args.html,
        summary=args.summary,
        manifest=args.manifest,
        band_contact=args.band_contact,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities source-page line-crop band HTML failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-page line-crop band HTML ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--band-contact", type=Path, default=DEFAULT_BAND_CONTACT)
    return parser


def validate_cities_source_page_line_crop_band_review_html_doc(
    doc: Path,
    html_path: Path | None = DEFAULT_HTML,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
    band_contact: Path | None = DEFAULT_BAND_CONTACT,
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
    contact_data: tuple[list[str], list[dict[str, str]]] | None = None
    if band_contact is not None:
        contact_data = read_csv(band_contact)
        failures.extend(validate_contact_shape(band_contact, contact_data))
    if html_path is not None:
        failures.extend(validate_local_html(html_path))
    if summary is not None and contact_data is not None:
        failures.extend(validate_summary_csv(summary, contact_data))
    if manifest is not None and contact_data is not None:
        failures.extend(validate_manifest(manifest, contact_data))
    return failures


def validate_local_html(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: text})
    if "Cities Source Page Line Crop Band Review" not in text:
        failures.append(f"{path} missing band review title")
    if text.count('<article class="band">') != 16:
        failures.append(f"{path} band article count drifted")
    return failures


def validate_summary_csv(
    path: Path,
    contact_data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    raw_text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: raw_text})
    fieldnames, rows = read_csv(path)
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    expected = expected_summary_rows(contact_data)
    if rows != expected:
        failures.append(f"{path} summary data drifted")
    summary = {row["metric"]: row["value"] for row in rows}
    for transcription_id, expected_count in EXPECTED_BANDS_BY_PAGE.items():
        metric = f"bands_{transcription_id}"
        if summary.get(metric) != str(expected_count):
            failures.append(f"{path} {metric}={summary.get(metric)!r}")
    return failures


def validate_manifest(
    path: Path,
    contact_data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    raw_text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: raw_text})
    try:
        data = read_json_object(path)
    except ValueError as exc:
        failures.append(str(exc))
        return failures
    expected_summary = {row["metric"]: row["value"] for row in expected_summary_rows(contact_data)}
    expected: dict[str, Any] = {
        "tool": "build_cities_source_page_line_crop_band_review_html.py",
        "inputs": {"band_contact": str(DEFAULT_BAND_CONTACT)},
        "outputs": {
            "html": str(DEFAULT_HTML),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": 16,
        "summary": expected_summary,
        "local_html_boundary": builder.LOCAL_HTML_BOUNDARY,
        "contact_sheet_boundary": contact_builder.NO_INPUT_BOUNDARY,
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_contact_shape(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != contact_builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 16:
        failures.append(f"{path} has {len(rows)} rows, expected 16")
    ids = [row.get("band_review_id", "") for row in rows]
    expected_ids = [f"cities_source_band_review_{index:03d}" for index in range(1, 17)]
    if ids != expected_ids:
        failures.append(f"{path} band review ids drifted")
    page_counts: dict[str, int] = {}
    for row in rows:
        band_id = row.get("band_review_id", "")
        page_counts[row.get("transcription_decision_id", "")] = (
            page_counts.get(row.get("transcription_decision_id", ""), 0) + 1
        )
        if row.get("contact_sheet_exists") != "true":
            failures.append(f"{path} {band_id} contact sheet missing")
        if not Path(row.get("contact_sheet_path", "")).exists():
            failures.append(f"{path} {band_id} contact sheet path missing")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"{path} {band_id} {field} must be 0")
    if page_counts != EXPECTED_BANDS_BY_PAGE:
        failures.append(f"{path} page counts drifted: {page_counts}")
    return failures


def expected_summary_rows(
    contact_data: tuple[list[str], list[dict[str, str]]],
) -> list[dict[str, str]]:
    fieldnames, rows = contact_data
    html_summary = {
        "html_exists": DEFAULT_HTML.exists(),
        "html_path": str(DEFAULT_HTML),
        "html_rows": len(rows),
        "html_band_image_rows": sum(
            1 for row in rows if Path(row.get("contact_sheet_path", "")).exists()
        ),
    }
    return builder.build_summary_rows(fieldnames, rows, html_summary)


def validate_no_source_text(texts_by_path: dict[Path, str]) -> list[str]:
    failures: list[str] = []
    for path, text in texts_by_path.items():
        if contains_hebrew_or_greek(text):
            failures.append(f"{path} appears to contain source-script body text")
    return failures


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


if __name__ == "__main__":
    raise SystemExit(main())
