#!/usr/bin/env python3
"""Validate Cities source-page line-crop triage HTML stays local-only."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_line_crop_triage as triage_builder
from scripts import build_cities_source_page_line_crop_triage_html as builder
from scripts.check_cities_source_page_line_crop_review_html_doc import (
    contains_hebrew_or_greek,
    normalize_space,
)


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_HTML = builder.DEFAULT_HTML
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_TRIAGE = builder.DEFAULT_TRIAGE

REQUIRED_PHRASES = (
    "# Cities Source Page Line Crop Triage HTML",
    "Status: local ignored HTML triage aid for Cities source-page line crops.",
    "displays line-crop images in priority order",
    "embeds no OCR text or source-script text",
    "HTML triage aid: `reports/cities_pdf_recovery_probe/source_page_line_crops/line_crop_triage.html`.",
    "HTML rows: 203.",
    "HTML embeds source text: `false`.",
    "HTML line-crop image rows: 203.",
    "HTML priority sections: 4.",
    "Line-crop triage rows: 203.",
    "Unique table pages: 4.",
    "Crop images available: 203.",
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
    "The ignored HTML file displays crop images in priority order only.",
    "The priority order is not transcription",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_line_crop_triage_html_doc(
        args.doc,
        html_path=args.html,
        summary=args.summary,
        manifest=args.manifest,
        triage=args.triage,
    )
    if failures:
        for failure in failures:
            print(f"Cities source-page line-crop triage HTML failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities source-page line-crop triage HTML ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--triage", type=Path, default=DEFAULT_TRIAGE)
    return parser


def validate_cities_source_page_line_crop_triage_html_doc(
    doc: Path,
    html_path: Path | None = DEFAULT_HTML,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
    triage: Path | None = DEFAULT_TRIAGE,
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
    triage_data: tuple[list[str], list[dict[str, str]]] | None = None
    if triage is not None:
        triage_data = read_csv(triage)
        failures.extend(validate_triage_shape(triage, triage_data))
    if html_path is not None:
        failures.extend(validate_local_html(html_path))
    if summary is not None and triage_data is not None:
        failures.extend(validate_summary_csv(summary, triage_data))
    if manifest is not None and triage_data is not None:
        failures.extend(validate_manifest(manifest, triage_data))
    return failures


def validate_local_html(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: text})
    if "Cities Source Page Line Crop Triage" not in text:
        failures.append(f"{path} missing triage title")
    if text.count('<article class="line-crop">') != 203:
        failures.append(f"{path} line-crop article count drifted")
    if text.count('<section class="priority">') != 4:
        failures.append(f"{path} priority section count drifted")
    return failures


def validate_summary_csv(
    path: Path,
    triage_data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    raw_text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: raw_text})
    fieldnames, rows = read_csv(path)
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    expected = expected_summary_rows(triage_data)
    if rows != expected:
        failures.append(f"{path} summary data drifted")
    return failures


def validate_manifest(
    path: Path,
    triage_data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    raw_text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: raw_text})
    data = json.loads(raw_text)
    expected_summary = {row["metric"]: row["value"] for row in expected_summary_rows(triage_data)}
    expected: dict[str, Any] = {
        "tool": "build_cities_source_page_line_crop_triage_html.py",
        "inputs": {"triage": str(DEFAULT_TRIAGE)},
        "outputs": {
            "html": str(DEFAULT_HTML),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": 203,
        "summary": expected_summary,
        "claim_boundary": triage_builder.CLAIM_BOUNDARY,
        "local_html_boundary": builder.LOCAL_HTML_BOUNDARY,
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


def validate_triage_shape(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != triage_builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 203:
        failures.append(f"{path} has {len(rows)} rows, expected 203")
    ranks = [row.get("triage_rank", "") for row in rows]
    if ranks != [str(index) for index in range(1, 204)]:
        failures.append(f"{path} triage ranks must be 1..203")
    for row in rows:
        rank = row.get("triage_rank", "")
        if row.get("crop_exists") != "true":
            failures.append(f"{path} triage {rank} crop missing")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"{path} triage {rank} {field} must be 0")
    return failures


def expected_summary_rows(
    triage_data: tuple[list[str], list[dict[str, str]]],
) -> list[dict[str, str]]:
    fieldnames, rows = triage_data
    html_summary = {
        "html_exists": DEFAULT_HTML.exists(),
        "html_path": str(DEFAULT_HTML),
        "html_rows": len(rows),
        "html_line_crop_image_rows": sum(
            1 for row in rows if Path(row.get("crop_path", "")).exists()
        ),
        "html_priority_sections": 4,
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
