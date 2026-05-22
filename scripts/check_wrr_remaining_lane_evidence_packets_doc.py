#!/usr/bin/env python3
"""Validate WRR remaining-lane evidence packet stays diagnostic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md")

REQUIRED_PHRASES = (
    "# WRR Remaining-Lane Evidence Packets",
    "Status: diagnostic evidence packet for page-image and method residual lanes.",
    "It does not choose source corrections, method changes, or pair exclusions.",
    "- Remaining-lane action terms: 14.",
    "- Residual pair links: 14.",
    "- Minimum-frontier pair links: 4.",
    "| `page_image_near_match_review` | 3 | 3 | 2 |",
    "| `method_or_pair_universe_review` | 11 | 11 | 2 |",
    "`wrr2_19_app_11`",
    "`YWSP+RANY`",
    "`wrr2_02_app_03`",
    "`ZR@ABRHM`",
    "primary page row visibly contains Maharit/Trani forms",
    "primary page row visibly contains Rabbi Shalom Sharabi forms",
    "Page-image near-match rows need page-image review before source edits.",
    "OCR-matched method rows need method or pair-universe explanation before source edits.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_remaining_lane_evidence_packets_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR remaining-lane evidence packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR remaining-lane evidence packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_remaining_lane_evidence_packets_doc(doc: Path) -> list[str]:
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
