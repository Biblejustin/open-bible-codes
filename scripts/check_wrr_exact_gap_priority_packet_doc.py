#!/usr/bin/env python3
"""Validate the WRR exact-gap priority packet keeps boundaries visible."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_EXACT_GAP_PRIORITY_PACKET.md")

REQUIRED_PHRASES = (
    "# WRR Exact Gap Priority Packet",
    "Status: no-input priority packet for the exact-published WRR reproduction gap.",
    "It does not select source corrections, pair exclusions, replacement spellings, or method changes.",
    "Source-cited defined distances | 163",
    "Current defined distances | 72",
    "Remaining 163-distance gap | 91",
    "| 2 | `source_transcription_or_row_alignment` | 43 terms; 44 residual pairs; 35 frontier pairs |",
    "Full CSV includes 22 row clusters.",
    "| remaining_lane | `method_or_pair_universe_review` | 11 terms; 11 residual pairs; 2 frontier pairs |",
    "| method_pair_universe | `ocr_matched_zero_ordinary_hits` | 11 OCR-matched terms;",
    "This is an evidence-priority packet, not an exact published WRR reproduction result.",
    "Do not describe the local locked-method result as exact published reproduction.",
)

FORBIDDEN_PHRASES = (
    "source correction selected",
    "pair exclusion selected",
    "replacement spelling selected",
    "exact published WRR reproduced",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_priority_packet_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR exact-gap priority packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR exact-gap priority packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_priority_packet_doc(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    for phrase in FORBIDDEN_PHRASES:
        if phrase in text and f"- {phrase}" not in text:
            failures.append(f"{doc} forbidden phrase outside caution list: {phrase}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
