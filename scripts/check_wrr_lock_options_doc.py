#!/usr/bin/env python3
"""Validate WRR lock-options doc keeps selected working locks explicit."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_wrr_lock_options as builder

DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_OPTIONS = builder.DEFAULT_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

FIELDNAMES = builder.FIELDNAMES

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
    failures = validate_lock_options_doc(args.doc, args.options, args.manifest)
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
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_lock_options_doc(
    doc: Path,
    options: Path | None = DEFAULT_OPTIONS,
    manifest: Path | None = DEFAULT_MANIFEST,
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
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_options_csv(options: Path) -> list[str]:
    data = _read_csv(options)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != FIELDNAMES:
        failures.append(f"{options} fieldnames drifted")
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


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "build_wrr_lock_options",
        "inputs": {
            "pair_summary": str(builder.DEFAULT_PAIR_SUMMARY),
            "skip_summary": str(builder.DEFAULT_SKIP_SUMMARY),
            "variants": str(builder.DEFAULT_VARIANTS),
            "recommended_permutation": str(builder.DEFAULT_RECOMMENDED_PERMUTATION),
            "source_review_summary": str(builder.DEFAULT_SOURCE_REVIEW_SUMMARY),
            "source_policy_scenarios": str(builder.DEFAULT_SOURCE_POLICY_SCENARIOS),
            "source_policy_term_impacts": str(
                builder.DEFAULT_SOURCE_POLICY_TERM_IMPACTS
            ),
            "direct_all_lanes_250_summary": str(
                builder.DEFAULT_DIRECT_ALL_LANES_250_SUMMARY
            ),
            "direct_all_lanes_1000_summary": str(
                builder.DEFAULT_DIRECT_ALL_LANES_1000_SUMMARY
            ),
            "direct_all_lanes_1000_program_summary": str(
                builder.DEFAULT_DIRECT_ALL_LANES_1000_PROGRAM_SUMMARY
            ),
            "direct_all_lanes_1000": str(builder.DEFAULT_DIRECT_ALL_LANES_1000),
            "direct_all_lanes_1000_program": str(
                builder.DEFAULT_DIRECT_ALL_LANES_1000_PROGRAM
            ),
        },
        "outputs": {
            "out": str(DEFAULT_OPTIONS),
            "markdown_out": str(DEFAULT_DOC),
        },
        "rows": len(EXPECTED_OPTIONS),
    }
    failures: list[str] = []
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{manifest} {key} drifted")
    return failures


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return f"{path} is invalid JSON: {exc}"
    if not isinstance(data, dict):
        return f"{path} JSON root must be an object"
    return data


if __name__ == "__main__":
    raise SystemExit(main())
