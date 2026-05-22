#!/usr/bin/env python3
"""Validate WRR blocker packet keeps no-input claim blockers visible."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_CLAIM_BLOCKER_PACKET.md")

REQUIRED_PHRASES = (
    "# WRR Claim Blocker Packet",
    "Status: working locks selected; corrected-distance/permutation still not claim-grade.",
    "| Corrected distance c(w,w') | `smoke_only` |",
    "| Aggregate statistic and permutation | `diagnostic_not_claim_grade` |",
    "run full corrected-distance over keep_all_working_source with printed D(w)",
    "requires full corrected-distance output before claim-grade lock",
    "source/title-prefix rule review; visual notes show title text without visible B@L prefix",
    "source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass",
    "## Visual Triage Highlights",
    "primary page row visibly contains Yaakov Ha-Levi wording; row OCR missed it",
    "treat as visual OCR miss until a locked transcription says otherwise",
    "This is a decision packet, not a reproduction result.",
    "Pair universe lock: keep_all_working_source",
    "D(w) lock: printed WRR formula main",
    "No visual-review note excludes a pair automatically; pair exclusion would require an explicit source-policy change.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_blocker_packet_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR claim-blocker packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR claim-blocker packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_blocker_packet_doc(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    return [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]


if __name__ == "__main__":
    raise SystemExit(main())
