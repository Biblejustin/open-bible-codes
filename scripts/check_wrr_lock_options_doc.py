#!/usr/bin/env python3
"""Validate WRR lock-options doc keeps method choices explicitly unlocked."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_LOCK_OPTIONS.md")

REQUIRED_PHRASES = (
    "# WRR Lock Options",
    "Status: decision aid, not a WRR reproduction.",
    "This report does not lock disputed WRR method choices.",
    "Pair universe",
    "D(w) skip-cap formula",
    "Permutation",
    "not claim-ready",
    "diagnostic only",
    "Current No-Input Path",
    "Recommended no-input working posture:",
    "Broad same-record WRR2 rows remain working diagnostic input only.",
    "No source-review flag or visual-review note excludes a pair automatically.",
    "Printed `D(w)` remains the source-facing default; reported-program `D(w)` remains sensitivity output.",
    "Date-label permutation output remains diagnostic until the pair universe, `D(w)`, corrected distances, and aggregate rule are source-locked.",
    "Claim-grade language still requires a source-locked pair universe",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_lock_options_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR lock-options doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR lock-options doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_lock_options_doc(doc: Path) -> list[str]:
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
