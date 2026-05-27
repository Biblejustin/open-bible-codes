#!/usr/bin/env python3
"""Validate the general-reader findings overview keeps its cautious summary."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/PROJECT_FINDINGS_OVERVIEW.md")

REQUIRED_HEADINGS = (
    "## Short Answer",
    "## What Was Being Looked For",
    "## What We Can Say With Confidence",
    "## Best Occurrence Examples",
    "## Stronger Areas To Keep Studying",
    "## Weaker Areas",
    "## Bible Text Differences",
    "## WRR Famous-Rabbis Study",
    "## What This Means",
    "## Best Current Summary",
    "## Where To Read More",
)

REQUIRED_PHRASES = (
    "Status: findings summary for general readers.",
    "no result should be presented as a settled public finding",
    "hidden-letter patterns are real, but real does not always mean rare, meaningful, or strong",
    "short words create many hits",
    "does not treat a hit count by itself as strong evidence",
    "These are not final conclusions",
    "source comparison, not for making a stronger meaning claim",
    "exact published reproduction remains unfinished",
    "no current row should be treated as settled public evidence",
)

REQUIRED_REFERENCES = (
    "docs/FINAL_REPORT.md",
    "docs/FINAL_REPORT_HIGHLIGHTS.md",
    "docs/CLAIM_CATALOG.md",
    "docs/CONSOLIDATED_FINDINGS.md",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_project_findings_overview(args.doc)
    if failures:
        for failure in failures:
            print(f"project-findings overview failure: {failure}", file=sys.stderr)
        return 1
    print(f"project-findings overview ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_project_findings_overview(doc: Path = DEFAULT_DOC) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    failures: list[str] = []
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            failures.append(f"{doc} missing heading: {heading}")
    for phrase in REQUIRED_PHRASES:
        if normalize_space(phrase) not in normalized:
            failures.append(f"{doc} missing phrase: {phrase}")
    for reference in REQUIRED_REFERENCES:
        if f"`{reference}`" not in text:
            failures.append(f"{doc} missing reference: {reference}")
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
