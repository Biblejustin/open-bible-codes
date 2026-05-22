#!/usr/bin/env python3
"""Validate hypothesis-testing source audit doc keeps source limits explicit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/HYPOTHESIS_TESTING_SOURCE_AUDIT.md")

REQUIRED_PHRASES = (
    "# Hypothesis-Testing Source Audit",
    "Status: source-status audit only.",
    "not an ELS result",
    "| source files scanned | 4 |",
    "| expected labels present | 0 |",
    "| spam-marker pages | 4 |",
    "| root-canonical pages | 4 |",
    "| usable method pages | 0 |",
    "| unusable current downloads | 4 |",
    "Current live downloads do not supply usable hypothesis-testing source pages.",
    "Fisher weights",
    "result-bearing protocol",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_hypothesis_testing_source_audit_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"hypothesis-testing source audit doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"hypothesis-testing source audit doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_hypothesis_testing_source_audit_doc(doc: Path) -> list[str]:
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
