#!/usr/bin/env python3
"""Validate WRR source row crop packet stays scoped to review aids."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_wrr_source_row_crop_packet as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_PACKET = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

PACKET_FIELDNAMES = builder.FIELDNAMES
SUMMARY_FIELDNAMES = builder.SUMMARY_FIELDNAMES

EXPECTED_SUMMARY = {
    "source_rows": "22",
    "auto_crops_available": "22",
    "contact_sheet_available": "true",
    "contact_sheet_rows": "22",
    "existing_manual_crop_rows_in_checklist": "4",
    "action_terms": "43",
    "frontier_pairs": "35",
    "detected_row_markers": "31",
    "crop_boundary": (
        "Crops are review aids only; no row transcription, source correction, "
        "pair exclusion, or method change is selected by this packet."
    ),
}

NO_INPUT_BOUNDARY = EXPECTED_SUMMARY["crop_boundary"]
CROP_STATUS = "written_review_aid_only"

REQUIRED_PHRASES = (
    "# WRR Source Row Crop Packet",
    "Status: no-input row-crop packet for WRR source-row review.",
    "It writes local review crops only; it does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
    "Auto row crops available: 22.",
    "Existing manual crop rows in checklist: 4.",
    "Crop availability is not transcription verification.",
    "Manual visual notes remain triage notes unless a separate decision record cites source evidence.",
    "No row here changes the working WRR source or excludes a pair automatically.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_row_crop_packet_doc(
        args.doc,
        args.packet,
        args.summary,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR source row crop packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source row crop packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_source_row_crop_packet_doc(
    doc: Path,
    packet: Path | None = DEFAULT_PACKET,
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
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if packet is not None:
        failures.extend(validate_packet_csv(packet))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_summary_csv(summary: Path) -> list[str]:
    data = _read_csv(summary)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    by_metric = {row.get("metric", ""): row for row in rows}
    failures: list[str] = []
    if fieldnames != SUMMARY_FIELDNAMES:
        failures.append(f"{summary} fieldnames drifted")
    for metric, expected in EXPECTED_SUMMARY.items():
        actual = by_metric.get(metric, {}).get("value")
        if actual != expected:
            failures.append(f"{summary} metric {metric}={actual!r}; expected {expected!r}")
    return failures


def validate_packet_csv(packet: Path) -> list[str]:
    data = _read_csv(packet)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != PACKET_FIELDNAMES:
        failures.append(f"{packet} fieldnames drifted")
    expected_rows = int(EXPECTED_SUMMARY["source_rows"])
    if len(rows) != expected_rows:
        failures.append(f"{packet} has {len(rows)} rows; expected {expected_rows}")
    ranks = [row.get("row_rank", "") for row in rows]
    expected_ranks = [str(index) for index in range(1, expected_rows + 1)]
    if ranks != expected_ranks:
        failures.append(f"{packet} row_rank sequence drifted")

    action_terms = sum(_int(row, "action_terms") for row in rows)
    frontier_pairs = sum(_int(row, "frontier_pairs") for row in rows)
    auto_crops = sum(1 for row in rows if row.get("crop_exists") == "true")
    manual_crop_rows = sum(1 for row in rows if _int(row, "manual_crop_count") > 0)
    if action_terms != int(EXPECTED_SUMMARY["action_terms"]):
        failures.append(f"{packet} action_terms sum={action_terms}")
    if frontier_pairs != int(EXPECTED_SUMMARY["frontier_pairs"]):
        failures.append(f"{packet} frontier_pairs sum={frontier_pairs}")
    if auto_crops != int(EXPECTED_SUMMARY["auto_crops_available"]):
        failures.append(f"{packet} auto crops available={auto_crops}")
    expected_manual_rows = int(
        EXPECTED_SUMMARY["existing_manual_crop_rows_in_checklist"]
    )
    if manual_crop_rows != expected_manual_rows:
        failures.append(f"{packet} manual crop rows={manual_crop_rows}")

    for row in rows:
        row_rank = row.get("row_rank", "")
        if row.get("crop_status") != CROP_STATUS:
            failures.append(f"{packet} rank {row_rank} crop status drifted")
        if row.get("no_input_boundary") != NO_INPUT_BOUNDARY:
            failures.append(f"{packet} rank {row_rank} no-input boundary drifted")
        if not row.get("crop_path", "").startswith(
            "reports/wrr_1994/source_review_crops_auto/"
        ):
            failures.append(f"{packet} rank {row_rank} crop path drifted")
        if _int(row, "crop_width") <= 0 or _int(row, "crop_height") <= 0:
            failures.append(f"{packet} rank {row_rank} crop dimensions invalid")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "build_wrr_source_row_crop_packet",
        "rows": int(EXPECTED_SUMMARY["source_rows"]),
        "summary": {
            key: _manifest_summary_value(value)
            for key, value in EXPECTED_SUMMARY.items()
        },
        "contact_sheet": {
            "contact_sheet_path": str(builder.DEFAULT_CONTACT_SHEET),
            "contact_sheet_exists": True,
            "contact_sheet_width": 1930,
            "contact_sheet_height": 1742,
            "contact_sheet_rows": int(EXPECTED_SUMMARY["contact_sheet_rows"]),
        },
        "inputs": {
            "row_checklist": str(builder.DEFAULT_ROW_CHECKLIST),
            "tsv": str(builder.DEFAULT_TSV),
            "image": str(builder.DEFAULT_IMAGE),
            "manual_crop_dir": str(builder.DEFAULT_MANUAL_CROP_DIR),
        },
        "outputs": {
            "crop_dir": str(builder.DEFAULT_CROP_DIR),
            "out": str(DEFAULT_PACKET),
            "summary_out": str(DEFAULT_SUMMARY),
            "markdown_out": str(DEFAULT_DOC),
            "contact_sheet_out": str(builder.DEFAULT_CONTACT_SHEET),
            "contact_sheet_markdown_out": str(builder.DEFAULT_CONTACT_MD),
            "manifest_out": str(DEFAULT_MANIFEST),
        },
    }
    failures: list[str] = []
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{manifest} {key} drifted")
    return failures


def _manifest_summary_value(value: str) -> int | str:
    try:
        return int(value)
    except ValueError:
        return value


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return f"{path} is invalid JSON: {exc}"
    if not isinstance(data, dict):
        return f"{path} JSON root must be an object"
    return data


def _int(row: dict[str, str], key: str) -> int:
    value = row.get(key, "0")
    try:
        return int(value)
    except ValueError:
        return 0


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
