#!/usr/bin/env python3
"""Validate Israeli prime-minister detail recovery doc keeps limits explicit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/ISRAELI_PRIME_MINISTERS_DETAIL_RECOVERY_PROBE.md")
EXPECTED_PAGES = {"9", "10", "11", "12"}
REQUIRED_PHRASES = (
    "# Israeli Prime Ministers Detail Recovery Probe",
    "Status: live-source recovery probe only.",
    "does not infer missing",
    "| missing detail pages probed | 4 |",
    "| rows where expected title appeared | 0 |",
    "| redirected rows | 4 |",
    "| final URL is Torah-code root | 4 |",
    "| canonical URL is Torah-code root | 4 |",
    "| unrelated slot/gambling markers | 4 |",
    "| usable detail pages | 0 |",
    "Current recovery status: `no_detail_pages_recovered`.",
    "Do not run a result-bearing protocol",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_detail_recovery_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"Israeli PM detail recovery doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Israeli PM detail recovery doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_detail_recovery_doc(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    present_pages = probe_pages(text)
    missing_pages = sorted(EXPECTED_PAGES - present_pages)
    if missing_pages:
        failures.append(f"{doc} missing probe pages: " + ", ".join(missing_pages))
    return failures


def probe_pages(text: str) -> set[str]:
    pages: set[str] = set()
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 10 and cells[0] in EXPECTED_PAGES:
            pages.add(cells[0])
    return pages


if __name__ == "__main__":
    raise SystemExit(main())
