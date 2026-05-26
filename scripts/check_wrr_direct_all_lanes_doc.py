#!/usr/bin/env python3
"""Validate WRR direct all-lane diagnostic doc stays diagnostic."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md")
DEFAULT_CAP250_SUMMARY = Path(
    "reports/wrr_1994/direct_all/wrr2_corrected_distance_all_lanes_250_summary.csv"
)
DEFAULT_CAP1000_SUMMARY = Path(
    "reports/wrr_1994/direct_all/highcap_1000/"
    "wrr2_corrected_distance_all_lanes_merged_summary.csv"
)
DEFAULT_CAP1000_AGGREGATE = Path(
    "reports/wrr_1994/direct_all/highcap_1000/"
    "wrr2_corrected_distance_all_lanes_aggregate.csv"
)
DEFAULT_PROGRAM_SUMMARY = Path(
    "reports/wrr_1994/direct_all/highcap_1000_program/"
    "wrr2_corrected_distance_all_lanes_merged_summary.csv"
)
DEFAULT_DW_SENSITIVITY = Path("reports/wrr_1994/wrr_dw_formula_sensitivity.csv")

EXPECTED_CAP250_SUMMARY = {
    "selected_pairs": "182",
    "pairs": "182",
    "search_max_skip": "250",
    "skip_cap_formula": "printed",
    "defined_corrected_distances": "50",
    "ordinary_not_valid_pairs": "130",
    "under_minimum_valid_pairs": "2",
    "min_corrected_distance": "0.008",
    "max_pair_valid_perturbations": "125",
    "status": "diagnostic_only_not_wrr_reproduction",
}
EXPECTED_CAP1000_SUMMARY = {
    "selected_pairs": "182",
    "shard_index": "merged",
    "shard_count": "2",
    "pairs": "182",
    "search_max_skip": "1000",
    "skip_cap_formula": "printed",
    "defined_corrected_distances": "72",
    "ordinary_not_valid_pairs": "110",
    "under_minimum_valid_pairs": "0",
    "min_corrected_distance": "0.008",
    "max_pair_valid_perturbations": "125",
    "status": "diagnostic_only_not_wrr_reproduction",
}
EXPECTED_CAP1000_AGGREGATE = {
    "rows": "182",
    "defined_corrected_distances": "72",
    "undefined_rows": "110",
    "p3_p4_sample_rows": "149",
    "p3_p4_sample_defined_corrected_distances": "59",
    "p1": "0.00252257011468",
    "p2": "1.16472976875e-05",
    "p3": "0.0184584022574",
    "p4": "0.000274264355592",
    "status": "diagnostic_only_not_wrr_reproduction",
}
EXPECTED_PROGRAM_SUMMARY = {
    "selected_pairs": "182",
    "shard_index": "merged",
    "shard_count": "2",
    "pairs": "182",
    "search_max_skip": "1000",
    "skip_cap_formula": "program",
    "defined_corrected_distances": "72",
    "ordinary_not_valid_pairs": "110",
    "under_minimum_valid_pairs": "0",
    "min_corrected_distance": "0.008",
    "max_pair_valid_perturbations": "125",
    "status": "diagnostic_only_not_wrr_reproduction",
}
EXPECTED_DW_SENSITIVITY_ALL_LANES = {
    "scope": "all_lanes_cap1000",
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
}

REQUIRED_PHRASES = (
    "# WRR Direct All-Lane Corrected-Distance Diagnostic",
    "Status: diagnostic-only, not a WRR reproduction.",
    "182 imported same-record WRR2 pairs",
    "| all lanes, cap 250 | 182 | 50 | 130 | 2 | 0.008 | 125 |",
    "| all lanes, cap 1000 split | 182 | 72 | 110 | 0 | 0.008 | 125 |",
    "| `length_5_8_smoke_candidate` | 46 | 40 |",
    "| `excluded_by_appellation_min_length` | 14 | 3 |",
    "| defined `c(w,w')` values | 72 |",
    "| P1 | 0.00252257011468 |",
    "| all lanes, cap 1000, program formula | 0 |",
    "direct all-lane cap 1000 defines 72 values, not 163.",
    "The 14 defined rows in `excluded_by_appellation_min_length` are diagnostic only",
    "Local locked-method language is governed by `docs/WRR_CLAIM_READINESS.md`; exact published reproduction remains caveated.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_direct_all_lanes_doc(
        args.doc,
        args.cap250_summary,
        args.cap1000_summary,
        args.cap1000_aggregate,
        args.program_summary,
        args.dw_sensitivity,
    )
    if failures:
        for failure in failures:
            print(f"WRR direct all-lane doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR direct all-lane doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--cap250-summary", type=Path, default=DEFAULT_CAP250_SUMMARY)
    parser.add_argument("--cap1000-summary", type=Path, default=DEFAULT_CAP1000_SUMMARY)
    parser.add_argument("--cap1000-aggregate", type=Path, default=DEFAULT_CAP1000_AGGREGATE)
    parser.add_argument("--program-summary", type=Path, default=DEFAULT_PROGRAM_SUMMARY)
    parser.add_argument("--dw-sensitivity", type=Path, default=DEFAULT_DW_SENSITIVITY)
    return parser


def validate_direct_all_lanes_doc(
    doc: Path,
    cap250_summary: Path | None = DEFAULT_CAP250_SUMMARY,
    cap1000_summary: Path | None = DEFAULT_CAP1000_SUMMARY,
    cap1000_aggregate: Path | None = DEFAULT_CAP1000_AGGREGATE,
    program_summary: Path | None = DEFAULT_PROGRAM_SUMMARY,
    dw_sensitivity: Path | None = DEFAULT_DW_SENSITIVITY,
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
    checks = [
        (cap250_summary, EXPECTED_CAP250_SUMMARY, "cap-250 summary"),
        (cap1000_summary, EXPECTED_CAP1000_SUMMARY, "cap-1000 summary"),
        (cap1000_aggregate, EXPECTED_CAP1000_AGGREGATE, "cap-1000 aggregate"),
        (program_summary, EXPECTED_PROGRAM_SUMMARY, "program-formula summary"),
    ]
    for path, expected, label in checks:
        if path is not None:
            failures.extend(validate_single_row_csv(path, expected, label))
    if dw_sensitivity is not None:
        failures.extend(validate_dw_sensitivity_csv(dw_sensitivity))
    return failures


def validate_single_row_csv(
    path: Path,
    expected: dict[str, str],
    label: str,
) -> list[str]:
    rows = _read_csv(path)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    if len(rows) != 1:
        failures.append(f"{path} {label} has {len(rows)} rows; expected 1")
    row = rows[0] if rows else {}
    for key, value in expected.items():
        if row.get(key) != value:
            failures.append(f"{path} {label} {key} drifted")
    return failures


def validate_dw_sensitivity_csv(path: Path) -> list[str]:
    rows = _read_csv(path)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    by_scope = {row.get("scope", ""): row for row in rows}
    row = by_scope.get("all_lanes_cap1000")
    if row is None:
        return [f"{path} missing all_lanes_cap1000 row"]
    for key, value in EXPECTED_DW_SENSITIVITY_ALL_LANES.items():
        if row.get(key) != value:
            failures.append(f"{path} all_lanes_cap1000 {key} drifted")
    if "printed D(w) main" not in row.get("diagnostic_read", ""):
        failures.append(f"{path} all_lanes_cap1000 diagnostic read drifted")
    return failures


def _read_csv(path: Path) -> list[dict[str, str]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
