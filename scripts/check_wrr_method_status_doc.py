#!/usr/bin/env python3
"""Validate WRR method-status doc keeps reproduction blockers explicit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_METHOD_STATUS.md")

REQUIRED_PHRASES = (
    "# WRR Method Status",
    "Status: current audit matrix; not a WRR reproduction.",
    "still needs source or implementation work before any reproduction claim",
    "| Genesis text stream | `locally_locked` |",
    "| WRR2 term source | `working_source_locked` |",
    "| Pair universe | `open` |",
    "| D(w) skip-cap formula | `open` |",
    "| Corrected distance c(w,w') | `smoke_only` |",
    "| Aggregate statistic and permutation | `diagnostic_not_claim_grade` |",
    "variant-gap impact best run",
    "Source Anchors",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_method_status_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR method-status doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR method-status doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_method_status_doc(doc: Path) -> list[str]:
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
