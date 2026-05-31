#!/usr/bin/env python3
"""Validate Cities source-transcription decision records stay locked empty."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from scripts import build_cities_source_transcription_review_worksheet as builder


DEFAULT_RECORDS = builder.DEFAULT_RECORDS


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_decision_records(args.records)
    if failures:
        for failure in failures:
            print(
                f"Cities source-transcription decision records failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-transcription decision records ok: {args.records}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS)
    return parser


def validate_decision_records(records: Path = DEFAULT_RECORDS) -> list[str]:
    failures: list[str] = []
    if not records.exists():
        return [f"{records} is missing"]

    with records.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    if fieldnames != builder.RECORD_FIELDS:
        failures.append(f"{records} fieldnames drifted")
    if rows:
        failures.append(
            f"{records} has {len(rows)} populated transcription decision rows; "
            "readable transcription decisions are not locked yet"
        )
    if contains_source_script(records.read_text(encoding="utf-8")):
        failures.append(f"{records} appears to contain source-script body text")
    return failures


def contains_source_script(text: str) -> bool:
    for char in text:
        code = ord(char)
        if 0x0590 <= code <= 0x05FF or 0x0370 <= code <= 0x03FF:
            return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())
