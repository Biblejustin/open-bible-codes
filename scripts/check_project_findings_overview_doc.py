#!/usr/bin/env python3
"""Validate the general-reader findings overview keeps its cautious summary."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/PROJECT_FINDINGS_OVERVIEW.md")
DEFAULT_README = Path("README.md")
DEFAULT_START_HERE = Path("docs/START_HERE.md")

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

READER_PATH_REQUIREMENTS = {
    DEFAULT_README: (
        "whole-project findings overview: `docs/PROJECT_FINDINGS_OVERVIEW.md`",
    ),
    DEFAULT_START_HERE: (
        "1. `docs/PROJECT_FINDINGS_OVERVIEW.md` for the whole-project findings summary.",
        "no current row should be presented as a public claim",
    ),
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_project_findings_overview(
        args.doc,
        args.readme,
        args.start_here,
    )
    if failures:
        for failure in failures:
            print(f"project-findings overview failure: {failure}", file=sys.stderr)
        return 1
    print(f"project-findings overview ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--readme", type=Path, default=DEFAULT_README)
    parser.add_argument("--start-here", type=Path, default=DEFAULT_START_HERE)
    return parser


def validate_project_findings_overview(
    doc: Path = DEFAULT_DOC,
    readme: Path = DEFAULT_README,
    start_here: Path = DEFAULT_START_HERE,
) -> list[str]:
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
    failures.extend(validate_reader_paths({DEFAULT_README: readme, DEFAULT_START_HERE: start_here}))
    return failures


def validate_reader_paths(path_by_default: dict[Path, Path]) -> list[str]:
    failures: list[str] = []
    for default_path, actual_path in path_by_default.items():
        required_phrases = READER_PATH_REQUIREMENTS[default_path]
        if not actual_path.exists():
            failures.append(f"{actual_path} is missing")
            continue
        normalized = normalize_space(actual_path.read_text(encoding="utf-8"))
        for phrase in required_phrases:
            if normalize_space(phrase) not in normalized:
                failures.append(f"{actual_path} missing phrase: {phrase}")
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
