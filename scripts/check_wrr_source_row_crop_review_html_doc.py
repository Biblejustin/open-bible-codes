#!/usr/bin/env python3
"""Validate WRR source-row crop HTML stays local-only."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_wrr_source_row_crop_packet as crop_packet
from scripts import build_wrr_source_row_crop_review_html as builder
from scripts.check_cities_source_page_line_crop_review_html_doc import (
    contains_hebrew_or_greek,
    normalize_space,
)
from scripts.check_wrr_source_row_crop_contact_sheet_doc import EXPECTED_ROW_ORDER


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_HTML = builder.DEFAULT_HTML
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_CROP_PACKET = builder.DEFAULT_CROP_PACKET

REQUIRED_PHRASES = (
    "# WRR Source Row Crop Review HTML",
    "Status: local ignored HTML review aid for WRR source-row crops.",
    "displays source-row crop images only",
    "embeds no OCR text or source-script text",
    "HTML crop review aid: `reports/wrr_1994/wrr_source_row_crop_review.html`.",
    "HTML rows: 22.",
    "HTML embeds source text: `false`.",
    "HTML crop image rows: 22.",
    "Source-row crop rows: 22.",
    "Auto crops available: 22.",
    "Manual crop rows: 4.",
    "Action terms: 43.",
    "Frontier pairs: 35.",
    "Row transcriptions: 0.",
    "Source corrections: 0.",
    "Pair exclusions: 0.",
    "Method changes: 0.",
    "The ignored HTML file displays generated row-crop images only.",
    "The crop view is not transcription",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_row_crop_review_html_doc(
        args.doc,
        html_path=args.html,
        summary=args.summary,
        manifest=args.manifest,
        crop_packet_path=args.crop_packet,
    )
    if failures:
        for failure in failures:
            print(f"WRR source row crop HTML failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source row crop HTML ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--crop-packet", type=Path, default=DEFAULT_CROP_PACKET)
    return parser


def validate_source_row_crop_review_html_doc(
    doc: Path,
    html_path: Path | None = DEFAULT_HTML,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
    crop_packet_path: Path | None = DEFAULT_CROP_PACKET,
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
    crop_data: tuple[list[str], list[dict[str, str]]] | None = None
    if crop_packet_path is not None:
        crop_data = read_csv(crop_packet_path)
        failures.extend(validate_crop_packet(crop_packet_path, crop_data))
    if html_path is not None:
        failures.extend(validate_local_html(html_path))
    if summary is not None and crop_data is not None:
        failures.extend(validate_summary_csv(summary, crop_data))
    if manifest is not None and crop_data is not None:
        failures.extend(validate_manifest(manifest, crop_data))
    return failures


def validate_local_html(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: text})
    if "WRR Source Row Crop Review" not in text:
        failures.append(f"{path} missing crop review title")
    if text.count('<article class="row">') != 22:
        failures.append(f"{path} source-row article count drifted")
    return failures


def validate_summary_csv(
    path: Path,
    crop_data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    raw_text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: raw_text})
    fieldnames, rows = read_csv(path)
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    expected = expected_summary_rows(crop_data)
    if rows != expected:
        failures.append(f"{path} summary data drifted")
    summary = {row["metric"]: row["value"] for row in rows}
    checks = {
        "html_rows": "22",
        "html_crop_image_rows": "22",
        "source_row_crop_rows": "22",
        "auto_crops_available": "22",
        "manual_crop_rows": "4",
        "action_terms": "43",
        "frontier_pairs": "35",
        "row_transcriptions": "0",
        "source_corrections": "0",
        "pair_exclusions": "0",
        "method_changes": "0",
    }
    for key, value in checks.items():
        if summary.get(key) != value:
            failures.append(f"{path} {key}={summary.get(key)!r}")
    return failures


def validate_manifest(
    path: Path,
    crop_data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    raw_text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: raw_text})
    data = json.loads(raw_text)
    expected_summary = {row["metric"]: row["value"] for row in expected_summary_rows(crop_data)}
    expected: dict[str, Any] = {
        "tool": "build_wrr_source_row_crop_review_html.py",
        "inputs": {"crop_packet": str(DEFAULT_CROP_PACKET)},
        "outputs": {
            "html": str(DEFAULT_HTML),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": 22,
        "summary": expected_summary,
        "local_html_boundary": builder.LOCAL_HTML_BOUNDARY,
        "crop_packet_boundary": crop_packet.NO_INPUT_BOUNDARY,
        "row_transcriptions": 0,
        "source_corrections": 0,
        "pair_exclusions": 0,
        "method_changes": 0,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_crop_packet(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != crop_packet.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != len(EXPECTED_ROW_ORDER):
        failures.append(f"{path} has {len(rows)} rows, expected {len(EXPECTED_ROW_ORDER)}")
    for index, (rank, row_number, action_terms, frontier_pairs) in enumerate(
        EXPECTED_ROW_ORDER
    ):
        if index >= len(rows):
            break
        row = rows[index]
        checks = {
            "row_rank": rank,
            "row_number": row_number,
            "action_terms": action_terms,
            "frontier_pairs": frontier_pairs,
            "crop_exists": "true",
            "crop_status": "written_review_aid_only",
            "no_input_boundary": crop_packet.NO_INPUT_BOUNDARY,
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{path} rank {rank} {key} drifted")
        crop_path = Path(row.get("crop_path", ""))
        if not crop_path.exists():
            failures.append(f"{path} rank {rank} crop path missing")
    return failures


def expected_summary_rows(
    crop_data: tuple[list[str], list[dict[str, str]]],
) -> list[dict[str, str]]:
    fieldnames, rows = crop_data
    html_summary = {
        "html_exists": DEFAULT_HTML.exists(),
        "html_path": str(DEFAULT_HTML),
        "html_rows": len(rows),
        "html_crop_image_rows": sum(1 for row in rows if Path(row.get("crop_path", "")).exists()),
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
