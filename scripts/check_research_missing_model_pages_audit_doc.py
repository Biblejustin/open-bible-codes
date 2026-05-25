#!/usr/bin/env python3
"""Validate missing research model page audit doc keeps source limits explicit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/RESEARCH_MISSING_MODEL_PAGES_AUDIT.md")

REQUIRED_PHRASES = (
    "# Research Missing Model Pages Audit",
    "Status: source-status audit only.",
    "not an ELS result",
    "not a claim-ready model reconstruction",
    "| downloaded source files | 4 |",
    "| overview level-2/3 links | 4 |",
    "| files containing expected model labels | 0 |",
    "| files declaring root canonical URL | 4 |",
    "| files with unrelated slot/gambling markers | 4 |",
    "| usable level-2/3 model pages | 0 |",
    "| adjacent level-1 source files | 2 |",
    "| usable adjacent level-1 model pages | 2 |",
    "Treat these four levels as missing source material",
    "until clean Torah-code research pages are recovered and checksummed.",
    "the missing level-2/3 model rules.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_research_missing_model_pages_audit_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"research missing model pages audit doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"research missing model pages audit doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_research_missing_model_pages_audit_doc(doc: Path) -> list[str]:
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
