#!/usr/bin/env python3
"""Validate WRR blocker packet keeps no-input claim blockers visible."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_CLAIM_BLOCKER_PACKET.md")

REQUIRED_PHRASES = (
    "# WRR Claim Blocker Packet",
    "Status: no current claim-readiness blockers under selected local WRR lock policy.",
    "| None | `ready` | Current method-status rows satisfy the claim-readiness gate. | none |",
    "Aggregate/permutation lock: keep-all cap1000 999,999 date-label permutation over the full selected-universe corrected-distance output.",
    "source/title-prefix rule review; visual notes show title text without visible B@L prefix",
    "source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass",
    "## Exact-WRR Residual Caveat",
    "Residual Frontier Sample",
    "Residual Term Queue",
    "Top Residual Term Targets",
    "Source-Transcription Row Evidence Summary",
    "Source-Transcription Priority Rows",
    "review multi-term rows once by row before term edits",
    "Page-Image Near-Match Evidence Summary",
    "Page-Image Near-Match Terms",
    "near OCR exists, but page image must decide whether it is source evidence",
    "Method/Pair-Universe Evidence Summary",
    "OCR matched all method-lane terms",
    "unique_unresolved_terms",
    "source_policy_or_pair_rule_review",
    "wnp_chelm_spelling_context",
    "Residual term priority is a review order, not a correction set or pair-exclusion list.",
    "residual source/method gap after the simple-variant upper bound",
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
