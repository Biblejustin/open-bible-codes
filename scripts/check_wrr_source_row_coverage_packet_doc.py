#!/usr/bin/env python3
"""Validate WRR source row coverage packet stays scoped to triage."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_ROW_COVERAGE_PACKET.md")

REQUIRED_PHRASES = (
    "# WRR Source Row Coverage Packet",
    "Status: no-input visual-triage coverage packet for WRR source-row review.",
    "It does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
    "Direct action-term visual coverage: 0 terms.",
    "Related row visual triage only: 4 rows.",
    "No related visual triage: 18 rows.",
    "Do not transfer related visual notes to action terms.",
    "Visual notes can identify rows worth reviewing, but they are not locked primary transcriptions.",
    "No row here changes the working WRR source or excludes a pair automatically.",
    "Preserve the working source unless a separate decision record selects a source or method change.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_row_coverage_packet_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR source row coverage packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source row coverage packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_row_coverage_packet_doc(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    return [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text and normalize_space(phrase) not in normalized_text
    ]


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
