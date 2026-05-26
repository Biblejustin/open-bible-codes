#!/usr/bin/env python3
"""Validate WRR D(w) formula sensitivity doc stays diagnostic."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_DW_FORMULA_SENSITIVITY.md")
DEFAULT_SENSITIVITY = Path("reports/wrr_1994/wrr_dw_formula_sensitivity.csv")
DEFAULT_CHANGED_PAIRS = Path("reports/wrr_1994/wrr_dw_formula_changed_pairs.csv")

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
CHANGED_PAIR_FIELDNAMES = [
    "pair_id",
    "concept",
    "printed_corrected_distance_status",
    "program_corrected_distance_status",
    "printed_corrected_distance",
    "program_corrected_distance",
    "printed_pair_valid_perturbations",
    "program_pair_valid_perturbations",
    "changed_fields",
]

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
    return parser


def validate_dw_formula_sensitivity_doc(
    doc: Path,
    sensitivity: Path | None = DEFAULT_SENSITIVITY,
    changed_pairs: Path | None = DEFAULT_CHANGED_PAIRS,
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
    return failures


def validate_sensitivity_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    _, rows = data
    failures: list[str] = []
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


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
