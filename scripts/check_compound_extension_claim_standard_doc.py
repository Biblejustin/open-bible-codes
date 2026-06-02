#!/usr/bin/env python3
"""Validate the compound-extension prospective claim standard."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/COMPOUND_EXTENSION_PROSPECTIVE_CLAIM_STANDARD.md")

REQUIRED_HEADINGS = (
    "# Compound Extension Prospective Claim Standard",
    "## Boundary",
    "## Required Lock Before Search",
    "## Default Source Set",
    "## Default Extension Rule",
    "## Control Standard",
    "## Required Audit Outputs",
    "## Allowed Status Labels",
    "## Current Project Implication",
)

REQUIRED_LINKS = (
    "docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md",
    "docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md",
    "docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md",
    "configs/example_oshb_wlc.toml",
    "configs/example_uxlc.toml",
    "configs/example_ebible_hebwlc.toml",
    "configs/example_mam.toml",
    "configs/example_uhb.toml",
)

REQUIRED_PHRASES = (
    "Status: preregistration scaffold; no result-producing run yet.",
    "not as new prospective discoveries under this standard",
    "Before a future result-producing compound-extension run starts",
    "at least 5000 shuffled-base-term and 5000 random controls",
    "The next result-producing step should not widen raw all-codes searches",
)

DISALLOWED_PHRASES = (
    "This confirms",
    "proves the row",
    "is claim-grade",
    "is a claim",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_compound_extension_claim_standard_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"compound-extension claim-standard doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"compound-extension claim-standard doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_compound_extension_claim_standard_doc(doc: Path = DEFAULT_DOC) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]

    text = doc.read_text(encoding="utf-8")
    normalized = normalize_whitespace(text)
    failures: list[str] = []

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            failures.append(f"{doc} missing heading: {heading}")

    for link in REQUIRED_LINKS:
        if f"`{link}`" not in text:
            failures.append(f"{doc} missing link: {link}")

    for phrase in REQUIRED_PHRASES:
        if normalize_whitespace(phrase) not in normalized:
            failures.append(f"{doc} missing guard phrase: {phrase}")

    for phrase in DISALLOWED_PHRASES:
        if phrase.casefold() in text.casefold():
            failures.append(f"{doc} has disallowed claim phrase: {phrase}")

    return failures


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
