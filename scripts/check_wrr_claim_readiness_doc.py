#!/usr/bin/env python3
"""Validate tracked WRR claim-readiness docs keep blocker language visible."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_CLAIM_READINESS.md")

REQUIRED_PHRASES = (
    "Status: blocked for claim-grade WRR reproduction language.",
    "Pair universe",
    "D(w) skip-cap formula",
    "Corrected distance c(w,w')",
    "Aggregate statistic and permutation",
    "variant-gap impact best run",
    "not claim-ready",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_readiness_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR claim-readiness doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR claim-readiness doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_readiness_doc(doc: Path) -> list[str]:
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
