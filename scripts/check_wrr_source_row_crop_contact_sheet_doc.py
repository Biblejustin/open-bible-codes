#!/usr/bin/env python3
"""Validate WRR source row crop contact sheet stays scoped to review aids."""

from __future__ import annotations

import argparse
import csv
import json
import struct
import sys
from pathlib import Path
from typing import Any

from scripts.build_wrr_source_row_crop_packet import (
    FIELDNAMES,
    NO_INPUT_BOUNDARY,
    SUMMARY_FIELDNAMES,
)


DEFAULT_DOC = Path("docs/WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md")
DEFAULT_IMAGE = Path("reports/wrr_1994/wrr_source_row_crop_contact_sheet.png")
DEFAULT_ROWS = Path("reports/wrr_1994/wrr_source_row_crop_packet.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_source_row_crop_packet_summary.csv")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_source_row_crop_packet.manifest.json")
EXPECTED_DIMENSIONS = (1930, 1742)
EXPECTED_ROW_ORDER = (
    ("1", "06", "4", "4"),
    ("2", "14", "3", "3"),
    ("3", "24", "3", "3"),
    ("4", "01", "2", "2"),
    ("5", "03", "2", "2"),
    ("6", "09", "2", "2"),
    ("7", "10", "2", "2"),
    ("8", "11", "2", "2"),
    ("9", "15", "2", "2"),
    ("10", "22", "2", "2"),
    ("11", "23", "2", "2"),
    ("12", "25", "2", "2"),
    ("13", "26", "2", "1"),
    ("14", "27", "1", "1"),
    ("15", "02", "1", "1"),
    ("16", "05", "1", "1"),
    ("17", "07", "1", "1"),
    ("18", "16", "1", "1"),
    ("19", "20", "1", "1"),
    ("20", "30", "4", "0"),
    ("21", "32", "2", "0"),
    ("22", "29", "1", "0"),
)
EXPECTED_MANUAL_CROP_COUNTS = {"23": "1", "27": "1", "30": "1", "32": "1"}
EXPECTED_SUMMARY = {
    "source_rows": ("22", "source-transcription rows with crop entries"),
    "auto_crops_available": ("22", "reports/wrr_1994/source_review_crops_auto"),
    "contact_sheet_available": (
        "true",
        "reports/wrr_1994/wrr_source_row_crop_contact_sheet.png",
    ),
    "contact_sheet_rows": ("22", "rows rendered into local contact sheet"),
    "existing_manual_crop_rows_in_checklist": (
        "4",
        "reports/wrr_1994/source_review_crops",
    ),
    "action_terms": ("43", "terms requiring row-level review"),
    "frontier_pairs": ("35", "minimum-frontier pair links"),
    "detected_row_markers": ("31", "OCR row markers detected from TSV"),
    "crop_boundary": (NO_INPUT_BOUNDARY, "no source or method decision selected"),
}

REQUIRED_PHRASES = (
    "# WRR Source Row Crop Contact Sheet",
    "Status: local visual contact sheet for WRR source-row review.",
    "It is a review aid only; it is not transcription verification",
    "Contact sheet image: `reports/wrr_1994/wrr_source_row_crop_contact_sheet.png`.",
    "Contact sheet dimensions: 1930 x 1742.",
    "Crop availability is not transcription verification.",
    "Manual visual notes remain triage notes unless a separate decision record cites source evidence.",
    "No row here changes the working WRR source or excludes a pair automatically.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_row_crop_contact_sheet_doc(
        args.doc,
        image=args.image,
        rows=args.rows,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR source row crop contact sheet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source row crop contact sheet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_source_row_crop_contact_sheet_doc(
    doc: Path,
    image: Path | None = DEFAULT_IMAGE,
    rows: Path | None = DEFAULT_ROWS,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text and normalize_space(phrase) not in normalized_text
    ]
    failures.extend(validate_doc_row_order(doc, text))
    if image is not None:
        failures.extend(validate_contact_sheet_image(image))
    if rows is not None:
        failures.extend(validate_rows_csv(rows))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_doc_row_order(doc: Path, text: str) -> list[str]:
    failures: list[str] = []
    rows = contact_sheet_doc_rows(text)
    if set(rows) != {rank for rank, _row, _terms, _frontier in EXPECTED_ROW_ORDER}:
        failures.append(f"{doc} contact-sheet rank set drifted")
    for rank, row_number, action_terms, frontier_pairs in EXPECTED_ROW_ORDER:
        row = rows.get(rank)
        if row is None:
            failures.append(f"{doc} missing contact-sheet rank {rank}")
            continue
        expected_path = crop_path(row_number)
        checks = {
            "row_number": row_number,
            "action_terms": action_terms,
            "frontier_pairs": frontier_pairs,
            "crop_path": expected_path,
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{doc} rank {rank} {key} drifted")
    return failures


def contact_sheet_doc_rows(text: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[0].isdigit():
            continue
        rows[cells[0]] = {
            "row_number": cells[1].strip("`"),
            "action_terms": cells[2],
            "frontier_pairs": cells[3],
            "crop_path": cells[4].strip("`"),
        }
    return rows


def validate_contact_sheet_image(image: Path) -> list[str]:
    if not image.exists():
        return [f"{image} is missing"]
    try:
        with image.open("rb") as handle:
            signature = handle.read(8)
            chunk_length, chunk_type = struct.unpack(">I4s", handle.read(8))
            chunk_data = handle.read(chunk_length)
    except (OSError, struct.error) as exc:
        return [f"{image} could not be read as PNG: {exc}"]
    if signature != b"\x89PNG\r\n\x1a\n" or chunk_type != b"IHDR":
        return [f"{image} is not a PNG with an IHDR header"]
    width, height = struct.unpack(">II", chunk_data[:8])
    if (width, height) != EXPECTED_DIMENSIONS:
        return [
            f"{image} dimensions {(width, height)}; expected {EXPECTED_DIMENSIONS}"
        ]
    return []


def validate_rows_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != len(EXPECTED_ROW_ORDER):
        failures.append(f"{path} has {len(rows)} rows; expected {len(EXPECTED_ROW_ORDER)}")
    for index, (rank, row_number, action_terms, frontier_pairs) in enumerate(
        EXPECTED_ROW_ORDER
    ):
        if index >= len(rows):
            break
        row = rows[index]
        expected_manual = EXPECTED_MANUAL_CROP_COUNTS.get(row_number, "0")
        expected_next = (
            "keep crop as later review aid unless policy scope changes"
            if frontier_pairs == "0"
            else "inspect generated crop against source row before any frontier source decision"
        )
        checks = {
            "run_label": "all_lanes_cap1000",
            "row_rank": rank,
            "row_number": row_number,
            "concept": f"WRR2 {row_number}",
            "action_terms": action_terms,
            "frontier_pairs": frontier_pairs,
            "crop_left": "500",
            "crop_right": "2050",
            "crop_width": "1550",
            "crop_path": crop_path(row_number),
            "crop_exists": "true",
            "crop_status": "written_review_aid_only",
            "manual_crop_count": expected_manual,
            "no_input_boundary": NO_INPUT_BOUNDARY,
            "next_manual_action": expected_next,
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{path} rank {rank} {key} drifted")
        if expected_manual == "0" and row.get("manual_crop_paths"):
            failures.append(f"{path} rank {rank} manual_crop_paths drifted")
        if expected_manual != "0" and row_number not in row.get("manual_crop_paths", ""):
            failures.append(f"{path} rank {rank} manual_crop_paths drifted")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    by_metric = {row.get("metric", ""): row for row in rows}
    if set(by_metric) != set(EXPECTED_SUMMARY):
        failures.append(f"{path} metric set drifted")
    for metric, (value, read) in EXPECTED_SUMMARY.items():
        row = by_metric.get(metric)
        if row is None:
            continue
        if row.get("value") != value:
            failures.append(f"{path} {metric} value drifted")
        if row.get("read") != read:
            failures.append(f"{path} {metric} read drifted")
    return failures


def validate_manifest(path: Path) -> list[str]:
    data = _read_json(path)
    if isinstance(data, str):
        return [data]
    failures: list[str] = []
    if data.get("rows") != len(EXPECTED_ROW_ORDER):
        failures.append(f"{path} rows drifted")
    summary = data.get("summary")
    if not isinstance(summary, dict):
        failures.append(f"{path} summary missing or not an object")
    else:
        for metric, (value, _read) in EXPECTED_SUMMARY.items():
            if str(summary.get(metric, "")) != value:
                failures.append(f"{path} summary {metric} drifted")
    contact_sheet = data.get("contact_sheet")
    if not isinstance(contact_sheet, dict):
        failures.append(f"{path} contact_sheet missing or not an object")
    else:
        checks: dict[str, object] = {
            "contact_sheet_exists": True,
            "contact_sheet_path": str(DEFAULT_IMAGE),
            "contact_sheet_rows": len(EXPECTED_ROW_ORDER),
            "contact_sheet_width": EXPECTED_DIMENSIONS[0],
            "contact_sheet_height": EXPECTED_DIMENSIONS[1],
        }
        for key, value in checks.items():
            if contact_sheet.get(key) != value:
                failures.append(f"{path} contact_sheet {key} drifted")
    return failures


def crop_path(row_number: str) -> str:
    return (
        "reports/wrr_1994/source_review_crops_auto/"
        f"wrr_table2_row{row_number}_auto.png"
    )


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
