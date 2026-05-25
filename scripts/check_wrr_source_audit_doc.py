#!/usr/bin/env python3
"""Validate WRR source-audit doc keeps current local-lock boundary."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_AUDIT.md")

REQUIRED_PHRASES = (
    "# WRR Source Audit",
    "Status: source audit trail for WRR; local locked-method evidence exists",
    "exact published WRR reproduction remains caveated",
    "Visual triage",
    "do not exclude pairs automatically",
    "The repo now has a locked local reporting path: keep_all_working_source",
    "printed `D(w)` as the main rule",
    "reported-program `D(w)` as sensitivity output",
    "full selected-universe cap-1000 corrected-distance output",
    "keep-all cap-1000 999,999 date-label permutation",
    "source-cited 163 defined distances still do not match the current 72 defined",
    "current manual decision records keep the working source unchanged",
    "locking method-lane rows",
    "Do not describe that local run as exact published WRR reproduction.",
)

FORBIDDEN_PHRASES = (
    "corrected-distance smoke driver built",
    "future corrected-distance implementation",
    "missing corrected-distance layer",
    "the WRR distance metric is implemented and tested against toy fixtures",
    "the permutation procedure is implemented with saved seeds and manifests",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_audit_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR source-audit doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-audit doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_audit_doc(doc: Path = DEFAULT_DOC) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized_text
    ]
    for phrase in FORBIDDEN_PHRASES:
        if normalize_space(phrase) in normalized_text:
            failures.append(f"{doc} contains stale phrase: {phrase}")
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
