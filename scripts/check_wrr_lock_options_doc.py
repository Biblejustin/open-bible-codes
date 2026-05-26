#!/usr/bin/env python3
"""Validate WRR lock-options doc keeps selected working locks explicit."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_LOCK_OPTIONS.md")
DEFAULT_OPTIONS = Path("reports/wrr_1994/wrr_lock_options.csv")

EXPECTED_OPTIONS = {
    "all imported WRR2 same-record pairs": (
        "Pair universe",
        "selected_working_source_policy",
        "source policy locked; full local corrected-distance run available",
    ),
    "appellation length >= 5 rows": (
        "Pair universe",
        "near_count_not_lock",
        "not claim-ready",
    ),
    "single Zacut appellation exclusion": (
        "Pair universe",
        "diagnostic_only",
        "not claim-ready",
    ),
    "WNP/context flagged source-review queue": (
        "Pair universe",
        "diagnostic_source_review_context",
        "diagnostic only",
    ),
    "source-policy scenario impact": (
        "Pair universe",
        "policy_selected_keep_all_working_source",
        "working source policy selected",
    ),
    "defined-distance output interpretation": (
        "Pair universe",
        "recommended_working_interpretation",
        "full local run available; exact WRR reproduction still caveated",
    ),
    "printed WRR formula": (
        "D(w) skip-cap formula",
        "source_locked_primary_formula",
        "formula locked; full local corrected-distance run available",
    ),
    "reported WRR-program formula": (
        "D(w) skip-cap formula",
        "required_sensitivity_variant",
        "sensitivity only",
    ),
    "repo-defined keep-all cap1000 999,999 date-label permutation": (
        "Permutation",
        "locked_local_permutation",
        "locked local evidence; exact published reproduction still caveated",
    ),
}

REQUIRED_PHRASES = (
    "# WRR Lock Options",
    "Status: decision aid, not a WRR reproduction.",
    "This report records the selected working locks",
    "Pair universe",
    "D(w) skip-cap formula",
    "Permutation",
    "not claim-ready",
    "diagnostic only",
    "Current No-Input Path",
    "Recommended no-input working posture:",
    "Broad same-record WRR2 rows are the selected working source policy.",
    "No source-review flag or visual-review note excludes a pair automatically.",
    "Printed `D(w)` is the main source-facing rule; reported-program `D(w)` remains sensitivity output.",
    "Date-label permutation output is locked for the repo-defined keep_all_working_source cap1000 run.",
    "Exact published WRR reproduction language remains caveated",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_lock_options_doc(args.doc, args.options)
    if failures:
        for failure in failures:
            print(f"WRR lock-options doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR lock-options doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--options", type=Path, default=DEFAULT_OPTIONS)
    return parser


def validate_lock_options_doc(
    doc: Path,
    options: Path | None = DEFAULT_OPTIONS,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    if options is not None:
        failures.extend(validate_options_csv(options))
    return failures


def validate_options_csv(options: Path) -> list[str]:
    rows = _read_csv(options)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    if len(rows) != len(EXPECTED_OPTIONS):
        failures.append(f"{options} has {len(rows)} rows; expected {len(EXPECTED_OPTIONS)}")
    by_option = {row.get("option", ""): row for row in rows}
    if set(by_option) != set(EXPECTED_OPTIONS):
        failures.append(f"{options} option set drifted")
    for option, (area, status, claim_boundary) in EXPECTED_OPTIONS.items():
        row = by_option.get(option)
        if row is None:
            continue
        if row.get("area") != area:
            failures.append(f"{options} {option} area drifted")
        if row.get("status") != status:
            failures.append(f"{options} {option} status drifted")
        if row.get("claim_boundary") != claim_boundary:
            failures.append(f"{options} {option} claim boundary drifted")
        if not row.get("evidence") or not row.get("recommendation"):
            failures.append(f"{options} {option} missing evidence/recommendation")
    return failures


def _read_csv(path: Path) -> list[dict[str, str]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
