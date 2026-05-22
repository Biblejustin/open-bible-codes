#!/usr/bin/env python3
"""Validate WRR residual term reconciliation queue doc keeps limits explicit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md")

REQUIRED_PHRASES = (
    "# WRR Residual Term Reconciliation Queue",
    "Status: diagnostic-only unique-term queue from the residual pair packet.",
    "does not select source corrections, exclude pairs, or reproduce WRR",
    "- Unique unresolved terms: 58.",
    "- Residual pair links represented: 59.",
    "- Minimum-frontier pair links represented: 40.",
    "| `term_side` | `appellation` | 58 | 59 | 40 |",
    "| `source_flag` | `wnp_chelm_spelling_context` | 1 | 1 | 1 |",
    "| `reconciliation_need` | `source_transcription_or_row_alignment` | 43 | 44 | 35 |",
    "| 1 | `wrr2_32_app_05` | `$LMHMX@LMA` | `source_policy_or_pair_rule_review` |",
    "Source-Policy Context",
    "pair-rule evidence before any source-lock change",
    "method or pair-universe blockers",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_residual_term_reconciliation_queue_doc(args.doc)
    if failures:
        for failure in failures:
            print(
                f"WRR residual term reconciliation doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"WRR residual term reconciliation doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_residual_term_reconciliation_queue_doc(doc: Path) -> list[str]:
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
