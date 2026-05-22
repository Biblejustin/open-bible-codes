#!/usr/bin/env python3
"""Validate WRR source-policy scenario doc stays diagnostic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_POLICY_SCENARIOS.md")

REQUIRED_PHRASES = (
    "# WRR Source Policy Scenario Impact",
    "Status: scenario impact for selected keep_all_working_source policy.",
    "The selected working policy keeps all imported WRR2 same-record pairs; exclusion scenarios are not applied.",
    "Visual-review notes remain triage only and do not exclude pairs automatically.",
    "| keep_all_working_source | `baseline` | 0 | 0 | 165 | 86 | -2 | 77 |",
    "| exclude_wnp_zacut_only | `diagnostic_exclusion` | 8 | 0 | 157 | 78 | 6 | 85 |",
    "| exclude_all_source_review_flags | `diagnostic_exclusion` | 11 | 0 | 154 | 78 | 9 | 85 |",
    "source/title-prefix rule review; visual notes show title text without visible B@L prefix",
    "source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass",
    "## Single-Term Impact",
    "| `wrr2_27_app_02` | `ZKWTA` | `wnp_disputed_zacut_appellation` | 2 | 163 | 0 | single-term exclusion closes >=5 count gap |",
    "`review_chelm_spelling_only` keeps pair counts stable and records review scope.",
    "Locked local WRR evidence now uses keep_all_working_source, printed D(w), full cap1000 corrected distances, and a keep-all 999,999 date-label permutation",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_policy_scenarios_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR source-policy scenarios doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-policy scenarios doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_policy_scenarios_doc(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    return [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text and normalize_space(phrase) not in normalized_text
    ]


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
