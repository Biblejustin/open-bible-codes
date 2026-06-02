#!/usr/bin/env python3
"""Validate WRR D(w) formula sensitivity doc stays diagnostic."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import analyze_wrr_dw_formula_sensitivity as analyzer

DEFAULT_DOC = analyzer.DEFAULT_MD
DEFAULT_SENSITIVITY = analyzer.DEFAULT_OUT
DEFAULT_CHANGED_PAIRS = analyzer.DEFAULT_CHANGED_OUT
DEFAULT_MANIFEST = analyzer.DEFAULT_MANIFEST

SUMMARY_FIELDNAMES = analyzer.SUMMARY_FIELDNAMES
CHANGED_PAIR_FIELDNAMES = analyzer.CHANGED_FIELDNAMES

EXPECTED_SCOPE_ROWS = {
    "skip_cap_profile": {
        "row_count": "120",
        "printed_formula": "printed",
        "program_formula": "program",
        "program_cap_lt_printed": "13",
        "program_cap_eq_printed": "107",
        "program_cap_gt_printed": "0",
        "target_unreached_rows": "55",
        "program_target_unreached_rows": "55",
    },
    "smoke_length_5_8_cap250": {
        "row_count": "86",
        "printed_formula": "printed",
        "program_formula": "program",
        "printed_defined_corrected_distances": "28",
        "program_defined_corrected_distances": "28",
        "fixed_250_defined_corrected_distances": "28",
        "printed_ordinary_not_valid_pairs": "56",
        "program_ordinary_not_valid_pairs": "56",
        "printed_under_minimum_valid_pairs": "2",
        "program_under_minimum_valid_pairs": "2",
    },
    "all_lanes_cap1000": {
        "row_count": "182",
        "printed_formula": "printed",
        "program_formula": "program",
        "printed_defined_corrected_distances": "72",
        "program_defined_corrected_distances": "72",
        "printed_ordinary_not_valid_pairs": "110",
        "program_ordinary_not_valid_pairs": "110",
        "printed_under_minimum_valid_pairs": "0",
        "program_under_minimum_valid_pairs": "0",
        "changed_pairs": "0",
    },
}
REQUIRED_PHRASES = (
    "# WRR D(w) Formula Sensitivity",
    "Status: sensitivity packet for the selected printed `D(w)` main rule.",
    "printed WRR skip-cap formula",
    "reported WRR-program",
    "| skip_cap_profile | 120 |",
    "| smoke_length_5_8_cap250 | 86 | 28 | 28 |",
    "| all_lanes_cap1000 | 182 | 72 | 72 | 0 |",
    "| Program cap below printed | 13 |",
    "| Program cap equal printed | 107 |",
    "No pair rows changed between all-lane cap-1000 printed and program formula outputs.",
    "Printed `D(w)` is the selected main rule for current WRR diagnostics.",
    "Reported-program `D(w)` remains required sensitivity output.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_dw_formula_sensitivity_doc(
        args.doc,
        args.sensitivity,
        args.changed_pairs,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR D(w) formula sensitivity doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR D(w) formula sensitivity doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--sensitivity", type=Path, default=DEFAULT_SENSITIVITY)
    parser.add_argument("--changed-pairs", type=Path, default=DEFAULT_CHANGED_PAIRS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_dw_formula_sensitivity_doc(
    doc: Path,
    sensitivity: Path | None = DEFAULT_SENSITIVITY,
    changed_pairs: Path | None = DEFAULT_CHANGED_PAIRS,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text and normalize_space(phrase) not in normalized_text
    ]
    if sensitivity is not None:
        failures.extend(validate_sensitivity_csv(sensitivity))
    if changed_pairs is not None:
        failures.extend(validate_changed_pairs_csv(changed_pairs))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_sensitivity_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    by_scope = {row.get("scope", ""): row for row in rows}
    if set(by_scope) != set(EXPECTED_SCOPE_ROWS):
        failures.append(f"{path} scope set drifted")
    for scope, expected in EXPECTED_SCOPE_ROWS.items():
        row = by_scope.get(scope)
        if row is None:
            continue
        for key, value in expected.items():
            if row.get(key) != value:
                failures.append(f"{path} {scope} {key} drifted")
        if "printed D(w)" not in row.get("diagnostic_read", ""):
            failures.append(f"{path} {scope} diagnostic read drifted")
    return failures


def validate_changed_pairs_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != CHANGED_PAIR_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows:
        failures.append(f"{path} has {len(rows)} rows; expected 0 changed pairs")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "analyze_wrr_dw_formula_sensitivity.py",
        "summary_rows": len(EXPECTED_SCOPE_ROWS),
        "changed_pairs": 0,
        "inputs": {
            "skip_summary": str(analyzer.DEFAULT_SKIP_SUMMARY),
            "variants": str(analyzer.DEFAULT_VARIANTS),
            "direct_printed_summary": str(analyzer.DEFAULT_DIRECT_PRINTED_SUMMARY),
            "direct_program_summary": str(analyzer.DEFAULT_DIRECT_PROGRAM_SUMMARY),
            "direct_printed": str(analyzer.DEFAULT_DIRECT_PRINTED),
            "direct_program": str(analyzer.DEFAULT_DIRECT_PROGRAM),
        },
        "outputs": {
            "out": str(DEFAULT_SENSITIVITY),
            "changed_out": str(DEFAULT_CHANGED_PAIRS),
            "markdown_out": str(DEFAULT_DOC),
            "manifest_out": str(DEFAULT_MANIFEST),
        },
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


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
