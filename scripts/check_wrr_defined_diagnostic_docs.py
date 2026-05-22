#!/usr/bin/env python3
"""Validate WRR defined-distance diagnostic docs keep blocker counts visible."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_PAIR_SET_DOC = Path("docs/WRR_DEFINED_PAIR_SET_AUDIT.md")
DEFAULT_GAP_REASON_DOC = Path("docs/WRR_DEFINED_GAP_REASON_AUDIT.md")

PAIR_SET_REQUIRED_PHRASES = (
    "# WRR Defined Pair-Set Audit",
    "Status: diagnostic-only pair-universe pressure audit, not a WRR reproduction.",
    "| all_lanes_cap1000 | 182 | 72 | 91 | 110 | 0 | 0 |",
    "Best current run: `all_lanes_cap1000` defines 72 of 163.",
    "Claim language stays blocked by `docs/WRR_CLAIM_READINESS.md`.",
)

GAP_REASON_REQUIRED_PHRASES = (
    "# WRR Defined Gap Reason Audit",
    "Status: diagnostic-only failure taxonomy for the current WRR all-lane",
    "| all_lanes_cap1000 | `defined` | 72 | 72 | 91 |",
    "| all_lanes_cap1000 | `ordinary_missing_appellation_hits` | 83 | 72 | 91 |",
    "| all_lanes_cap1000 | `ordinary_missing_date_hits` | 12 | 72 | 91 |",
    "| all_lanes_cap1000 | `ordinary_missing_both_terms` | 15 | 72 | 91 |",
    "Ordinary-missing rows total 110; under-minimum rows total 0.",
    "alignment problem before it is a permutation problem",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_defined_diagnostic_docs(
        pair_set_doc=args.pair_set_doc,
        gap_reason_doc=args.gap_reason_doc,
    )
    if failures:
        for failure in failures:
            print(f"WRR defined diagnostic doc failure: {failure}", file=sys.stderr)
        return 1
    print(
        "WRR defined diagnostic docs ok: "
        f"{args.pair_set_doc}, {args.gap_reason_doc}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair-set-doc", type=Path, default=DEFAULT_PAIR_SET_DOC)
    parser.add_argument("--gap-reason-doc", type=Path, default=DEFAULT_GAP_REASON_DOC)
    return parser


def validate_defined_diagnostic_docs(
    *,
    pair_set_doc: Path = DEFAULT_PAIR_SET_DOC,
    gap_reason_doc: Path = DEFAULT_GAP_REASON_DOC,
) -> list[str]:
    return [
        *validate_doc(pair_set_doc, PAIR_SET_REQUIRED_PHRASES),
        *validate_doc(gap_reason_doc, GAP_REASON_REQUIRED_PHRASES),
    ]


def validate_doc(doc: Path, required_phrases: tuple[str, ...]) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    return [
        f"{doc} missing phrase: {phrase}"
        for phrase in required_phrases
        if phrase not in text
    ]


if __name__ == "__main__":
    raise SystemExit(main())
