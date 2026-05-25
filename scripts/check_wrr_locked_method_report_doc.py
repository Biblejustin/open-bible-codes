#!/usr/bin/env python3
"""Validate the WRR locked-method report keeps claim boundaries visible."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_LOCKED_METHOD_REPORT.md")

REQUIRED_PHRASES = (
    "# WRR Locked Method Report",
    "Status: locked local WRR method report; not an exact published WRR reproduction.",
    "Pair universe: keep_all_working_source",
    "D(w): printed WRR formula main",
    "Permutation: 999,999 date-label shuffles",
    "Manual decisions: 37 locked rows",
    "26 no_source_change",
    "11 method_lock",
    "Defined c-values",
    "rho0 | 0.000404",
    "Exact published WRR reproduction remains caveated",
    "source-defined 163-distance gap",
    "primary-source transcription limits",
    "Do not describe this as an exact published WRR reproduction.",
    "source correction selected",
)

FORBIDDEN_PHRASES = (
    "exact published WRR reproduced",
    "proves WRR",
    "conclusive WRR",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_locked_method_report_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR locked-method report failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR locked-method report ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_locked_method_report_doc(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    for phrase in FORBIDDEN_PHRASES:
        if phrase in text and f"- {phrase}" not in text:
            failures.append(f"{doc} forbidden phrase outside forbidden-language list: {phrase}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
