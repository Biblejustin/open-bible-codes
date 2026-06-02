#!/usr/bin/env python3
"""Validate Cities source-page line-crop priority HTML stays local-only."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_line_crop_priority_contact_sheet as contact_builder
from scripts import build_cities_source_page_line_crop_priority_review_html as builder
from scripts.check_cities_source_page_line_crop_review_html_doc import (
    contains_hebrew_or_greek,
    normalize_space,
)
from scripts.json_utils import read_json_object


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_HTML = builder.DEFAULT_HTML
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_PRIORITY_CONTACT = builder.DEFAULT_PRIORITY_CONTACT

EXPECTED_PRIORITY_COUNTS = {
    "priority_1_dense_text": 120,
    "priority_2_medium_text": 71,
    "priority_3_short_text": 12,
    "priority_4_no_text": 0,
}

REQUIRED_PHRASES = (
    "# Cities Source Page Line Crop Priority Review HTML",
    "Status: local ignored HTML review aid for Cities source-page line-crop triage priorities.",
    "displays priority contact-sheet images only",
    "embeds no OCR text or source-script text",
    "HTML priority review aid: `reports/cities_pdf_recovery_probe/source_page_line_crops/priority_review.html`.",
    "HTML rows: 4.",
    "HTML embeds source text: `false`.",
    "HTML priority image rows: 4.",
    "Priority contact-sheet rows: 4.",
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
    "The ignored HTML file displays priority contact-sheet images only.",
    "The priority view is not transcription",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_line_crop_priority_review_html_doc(
        args.doc,
        html_path=args.html,
        summary=args.summary,
        manifest=args.manifest,
        priority_contact=args.priority_contact,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities source-page line-crop priority HTML failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-page line-crop priority HTML ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--priority-contact", type=Path, default=DEFAULT_PRIORITY_CONTACT)
    return parser


def validate_cities_source_page_line_crop_priority_review_html_doc(
    doc: Path,
    html_path: Path | None = DEFAULT_HTML,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
    priority_contact: Path | None = DEFAULT_PRIORITY_CONTACT,
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
    if priority_contact is not None:
        contact_data = read_csv(priority_contact)
        failures.extend(validate_contact_shape(priority_contact, contact_data))
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
    if "Cities Source Page Line Crop Priority Review" not in text:
        failures.append(f"{path} missing priority review title")
    if text.count('<article class="priority">') != 4:
        failures.append(f"{path} priority article count drifted")
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
    for priority, expected_count in EXPECTED_PRIORITY_COUNTS.items():
        if summary.get(priority) != str(expected_count):
            failures.append(f"{path} {priority}={summary.get(priority)!r}")
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
        "tool": "build_cities_source_page_line_crop_priority_review_html.py",
        "inputs": {"priority_contact": str(DEFAULT_PRIORITY_CONTACT)},
        "outputs": {
            "html": str(DEFAULT_HTML),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": 4,
        "summary": expected_summary,
        "local_html_boundary": builder.LOCAL_HTML_BOUNDARY,
        "priority_contact_boundary": contact_builder.NO_INPUT_BOUNDARY,
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
    if len(rows) != 4:
        failures.append(f"{path} has {len(rows)} rows, expected 4")
    priority_counts = {
        row.get("review_priority", ""): int(row.get("line_crop_rows", "0"))
        for row in rows
    }
    if priority_counts != EXPECTED_PRIORITY_COUNTS:
        failures.append(f"{path} priority counts drifted: {priority_counts}")
    priorities = [row.get("review_priority", "") for row in rows]
    if priorities != contact_builder.PRIORITY_ORDER:
        failures.append(f"{path} priority order drifted: {priorities}")
    for row in rows:
        priority = row.get("review_priority", "")
        if row.get("contact_sheet_exists") != "true":
            failures.append(f"{path} {priority} contact sheet missing")
        if not Path(row.get("contact_sheet_path", "")).exists():
            failures.append(f"{path} {priority} contact sheet path missing")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"{path} {priority} {field} must be 0")
    return failures


def expected_summary_rows(
    contact_data: tuple[list[str], list[dict[str, str]]],
) -> list[dict[str, str]]:
    fieldnames, rows = contact_data
    html_summary = {
        "html_exists": DEFAULT_HTML.exists(),
        "html_path": str(DEFAULT_HTML),
        "html_rows": len(rows),
        "html_priority_image_rows": sum(
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
