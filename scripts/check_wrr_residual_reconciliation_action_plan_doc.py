#!/usr/bin/env python3
"""Validate WRR residual reconciliation action plan keeps limits explicit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md")

REQUIRED_PHRASES = (
    "# WRR Residual Reconciliation Action Plan",
    "Status: diagnostic action plan from the residual unique-term queue.",
    "does not select source corrections, exclude pairs, or reproduce WRR",
    "- Action terms: 58.",
    "- Residual pair links: 59.",
    "- Minimum-frontier pair links: 40.",
    "| `source_policy_or_pair_rule_review` | 1 | 1 | 1 |",
    "| `source_transcription_or_row_alignment` | 43 | 44 | 35 |",
    "| 1 | `source_policy_or_pair_rule_review` | `wrr2_32_app_05` | `$LMHMX@LMA` |",
    "keep term in working source; no automatic correction or exclusion without citable rule",
    "method or pair-universe review before source edits",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_residual_reconciliation_action_plan_doc(args.doc)
    if failures:
        for failure in failures:
            print(
                f"WRR residual reconciliation action-plan failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"WRR residual reconciliation action plan ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_residual_reconciliation_action_plan_doc(doc: Path) -> list[str]:
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
