#!/usr/bin/env python3
"""Validate critical-omission follow-up docs keep required report shape."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_SECTIONS = ("## Setup", "## Method", "## Results", "## Cautions")


@dataclass(frozen=True)
class DocRule:
    path: Path
    required_phrases: tuple[str, ...]


DOC_RULES = (
    DocRule(
        Path("docs/CRITICAL_OMISSION_BREAKS.md"),
        (
            "# Critical Omission Breaks",
            "`reports/critical_omission_breaks_summary.csv`",
            "Broken total: 558.",
            "Deleted blocks used: 18.",
            "Raw break counts are not significance tests.",
        ),
    ),
    DocRule(
        Path("docs/CRITICAL_OMISSION_BREAKS_REVERSE.md"),
        (
            "# Critical Omission Breaks Reverse",
            "`reports/critical_omission_breaks_reverse_summary.csv`",
            "Spliced blocks: 18.",
            "Broken example rows: 237.",
            "Raw break counts are not significance tests.",
        ),
    ),
    DocRule(
        Path("docs/CRITICAL_OMISSION_BREAKS_CROSS_TRADITION.md"),
        (
            "# Critical Omission Breaks Cross Tradition",
            "`reports/critical_omission_breaks_cross_tradition.csv`",
            "Current output rows: 558",
            "`preserved_by_byz_and_tcg`: 163.",
            "This is a robustness screen, not a textual-critical stemma.",
        ),
    ),
    DocRule(
        Path("docs/CRITICAL_OMISSION_BREAKS_NULL.md"),
        (
            "# Critical Omission Breaks Null",
            "`reports/critical_omission_breaks_null/summary.csv`",
            "Observed breaks: 558.",
            "Greater-or-equal tail: 0.9910.",
            "Raw break counts are not significance tests.",
        ),
    ),
    DocRule(
        Path("docs/CRITICAL_OMISSION_BREAKS_LENGTH_STRATIFIED.md"),
        (
            "# Critical Omission Breaks Length Stratified",
            "`reports/critical_omission_breaks_length_stratified.csv`",
            "Current output rows: 458.",
            "`naive_expected_break_rate = L * D / N`",
            "Raw break counts are not significance tests.",
        ),
    ),
    DocRule(
        Path("docs/CRITICAL_OMISSION_BREAKS_PERICOPE_OVERRIDE.md"),
        (
            "# Critical Omission Breaks Pericope Override",
            "`reports/critical_omission_breaks_pericope_override_summary.csv`",
            "Broken example rows: 1,185.",
            "## Other Disputed Passages",
            "Raw break counts are not significance tests.",
        ),
    ),
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_critical_omission_docs(args.root)
    if failures:
        for failure in failures:
            print(f"critical-omission doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"critical-omission docs ok: {args.root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    return parser


def validate_critical_omission_docs(root: Path = Path(".")) -> list[str]:
    failures: list[str] = []
    for rule in DOC_RULES:
        doc = root / rule.path
        if not doc.exists():
            failures.append(f"{rule.path} is missing")
            continue
        normalized_text = normalize_space(doc.read_text(encoding="utf-8"))
        for section in REQUIRED_SECTIONS:
            if normalize_space(section) not in normalized_text:
                failures.append(f"{rule.path} missing section: {section}")
        for phrase in rule.required_phrases:
            if normalize_space(phrase) not in normalized_text:
                failures.append(f"{rule.path} missing phrase: {phrase}")
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
