#!/usr/bin/env python3
"""Validate Cities OCR page-review decision records stay non-source."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

from scripts import build_cities_unreadable_pdf_ocr_page_review as builder


DEFAULT_DECISIONS = builder.DEFAULT_DECISIONS
DEFAULT_PACKET = builder.DEFAULT_PACKET
EXPECTED_FIELDNAMES = (
    "decision_id",
    "label",
    "page_number",
    "visual_review_status",
    "visual_page_role",
    "visual_text_signal",
    "ocr_read_status",
    "source_row_use",
    "decision",
    "reviewed_by",
    "reviewed_at",
    "notes",
)
REQUIRED_FIELDS = (
    "decision_id",
    "label",
    "page_number",
    "visual_review_status",
    "visual_page_role",
    "visual_text_signal",
    "ocr_read_status",
    "source_row_use",
    "decision",
    "reviewed_by",
    "reviewed_at",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_decisions(args.decisions, args.packet)
    if failures:
        for failure in failures:
            print(f"Cities OCR page-review decision failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities OCR page-review decisions ok: {args.decisions}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decisions", type=Path, default=DEFAULT_DECISIONS)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    return parser


def validate_decisions(
    decisions: Path = DEFAULT_DECISIONS,
    packet: Path = DEFAULT_PACKET,
) -> list[str]:
    if not decisions.exists():
        return [f"{decisions} is missing"]
    if not packet.exists():
        return [f"{packet} is missing"]

    failures: list[str] = []
    fieldnames, rows = read_rows(decisions)
    packet_keys = {
        (row.get("label", ""), row.get("page_number", ""))
        for row in builder.read_csv(packet)
    }
    if tuple(fieldnames) != EXPECTED_FIELDNAMES:
        failures.append(f"{decisions} fieldnames drifted")
    if len(rows) != 41:
        failures.append(f"{decisions} has {len(rows)} rows, expected 41")
    if contains_source_script(decisions.read_text(encoding="utf-8")):
        failures.append(f"{decisions} appears to contain OCR/source-script body text")

    seen_ids: set[str] = set()
    for row_number, row in enumerate(rows, start=2):
        failures.extend(validate_row(decisions, row_number, row, packet_keys, seen_ids))
    return failures


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def validate_row(
    decisions: Path,
    row_number: int,
    row: dict[str, str],
    packet_keys: set[tuple[str, str]],
    seen_ids: set[str],
) -> list[str]:
    failures: list[str] = []
    decision_id = row.get("decision_id", "").strip()
    expected_id = f"cities_ocr_page_review_{row_number - 1:03d}"
    if decision_id != expected_id:
        failures.append(f"{decisions}:{row_number} decision_id must be {expected_id}")
    if decision_id in seen_ids:
        failures.append(f"{decisions}:{row_number} duplicate decision_id: {decision_id}")
    seen_ids.add(decision_id)

    for field in REQUIRED_FIELDS:
        if not row.get(field, "").strip():
            failures.append(f"{decisions}:{row_number} missing {field}")
    if (row.get("label", ""), row.get("page_number", "")) not in packet_keys:
        failures.append(f"{decisions}:{row_number} label/page not in OCR packet")
    if row.get("visual_review_status", "") != "reviewed":
        failures.append(f"{decisions}:{row_number} visual_review_status must be reviewed")
    if row.get("source_row_use", "") != "no_source_row_use":
        failures.append(f"{decisions}:{row_number} source_row_use must be no_source_row_use")
    if row.get("decision", "") != "no_source_row_import":
        failures.append(f"{decisions}:{row_number} decision must be no_source_row_import")
    try:
        date.fromisoformat(row.get("reviewed_at", ""))
    except ValueError:
        failures.append(f"{decisions}:{row_number} reviewed_at must be ISO date")
    return failures


def contains_source_script(text: str) -> bool:
    for char in text:
        code = ord(char)
        if 0x0590 <= code <= 0x05FF or 0x0370 <= code <= 0x03FF:
            return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())
