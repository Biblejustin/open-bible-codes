#!/usr/bin/env python3
"""Validate WRR cross-pair grid doc stays aligned with locked local evidence."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_DOC = Path("docs/WRR_CROSS_PAIR_GRID.md")
DEFAULT_GRID_SUMMARY = Path("reports/wrr_1994/wrr2_cross_pair_grid_summary.csv")
DEFAULT_CAP250_SUMMARY = Path(
    "reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_corrected_distance_250_summary.csv"
)
DEFAULT_CAP250_AGGREGATE = Path(
    "reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_corrected_distance_250_aggregate.csv"
)
DEFAULT_CAP250_PERMUTATION = Path(
    "reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_permutations_1000_summary.csv"
)
DEFAULT_CAP250_NO_WNP_999999 = Path(
    "reports/wrr_1994/cross_pair_grid/"
    "wrr2_cross_pair_permutations_no_wnp_999999_summary.csv"
)
DEFAULT_CAP1000_SUMMARY = Path(
    "reports/wrr_1994/cross_pair_grid/highcap_1000/"
    "wrr2_cross_pair_corrected_distance_1000_summary.csv"
)
DEFAULT_CAP1000_AGGREGATE = Path(
    "reports/wrr_1994/cross_pair_grid/highcap_1000/"
    "wrr2_cross_pair_corrected_distance_1000_aggregate.csv"
)
DEFAULT_CAP1000_PERMUTATION = Path(
    "reports/wrr_1994/cross_pair_grid/highcap_1000/"
    "wrr2_cross_pair_permutations_1000_summary.csv"
)
DEFAULT_CAP1000_999999 = Path(
    "reports/wrr_1994/cross_pair_grid/highcap_1000/"
    "wrr2_cross_pair_permutations_999999_summary.csv"
)
DEFAULT_GRID_MANIFEST = Path("reports/wrr_1994/wrr2_cross_pair_grid.manifest.json")
DEFAULT_CAP250_SUMMARY_MANIFEST = Path(
    "reports/wrr_1994/cross_pair_grid/"
    "wrr2_cross_pair_corrected_distance_250.manifest.json"
)
DEFAULT_CAP250_AGGREGATE_MANIFEST = Path(
    "reports/wrr_1994/cross_pair_grid/"
    "wrr2_cross_pair_corrected_distance_250_aggregate.manifest.json"
)
DEFAULT_CAP250_PERMUTATION_MANIFEST = Path(
    "reports/wrr_1994/cross_pair_grid/"
    "wrr2_cross_pair_permutations_1000.manifest.json"
)
DEFAULT_CAP250_NO_WNP_999999_MANIFEST = Path(
    "reports/wrr_1994/cross_pair_grid/"
    "wrr2_cross_pair_permutations_no_wnp_999999.manifest.json"
)
DEFAULT_CAP1000_SUMMARY_MANIFEST = Path(
    "reports/wrr_1994/cross_pair_grid/highcap_1000/"
    "wrr2_cross_pair_corrected_distance_1000.manifest.json"
)
DEFAULT_CAP1000_AGGREGATE_MANIFEST = Path(
    "reports/wrr_1994/cross_pair_grid/highcap_1000/"
    "wrr2_cross_pair_corrected_distance_1000_aggregate.manifest.json"
)
DEFAULT_CAP1000_PERMUTATION_MANIFEST = Path(
    "reports/wrr_1994/cross_pair_grid/highcap_1000/"
    "wrr2_cross_pair_permutations_1000.manifest.json"
)
DEFAULT_CAP1000_999999_MANIFEST = Path(
    "reports/wrr_1994/cross_pair_grid/highcap_1000/"
    "wrr2_cross_pair_permutations_999999.manifest.json"
)

EXPECTED_GRID_SUMMARY = {
    "pairs": "5208",
    "same_record_pairs": "182",
    "cross_record_pairs": "5026",
    "appellations": "168",
    "dates": "31",
    "appellation_concepts": "30",
    "date_concepts": "30",
    "appellation_min_length_pairs": "4743",
    "length_filtered_pairs": "2231",
    "wnp_disputed_zacut_pairs": "124",
    "rabbi_title_pairs": "992",
    "non_rabbi_title_pairs": "4216",
    "length_filtered_non_rabbi_title_pairs": "1633",
    "zero_hit_pairs": "3696",
    "pairs_with_skip_cap_target_unreached": "2233",
    "status": "diagnostic_cross_pair_grid_not_claim_grade",
}
EXPECTED_CAP250_SUMMARY = {
    "selected_pairs": "5208",
    "pairs": "5208",
    "search_max_skip": "250",
    "skip_cap_formula": "printed",
    "defined_corrected_distances": "1423",
    "ordinary_not_valid_pairs": "3720",
    "under_minimum_valid_pairs": "65",
    "min_corrected_distance": "0.008",
    "max_pair_valid_perturbations": "125",
    "status": "diagnostic_only_not_wrr_reproduction",
}
EXPECTED_CAP1000_SUMMARY = {
    "selected_pairs": "5208",
    "pairs": "5208",
    "search_max_skip": "1000",
    "skip_cap_formula": "printed",
    "defined_corrected_distances": "2013",
    "ordinary_not_valid_pairs": "3183",
    "under_minimum_valid_pairs": "12",
    "min_corrected_distance": "0.008",
    "max_pair_valid_perturbations": "125",
    "status": "diagnostic_only_not_wrr_reproduction",
}
EXPECTED_CAP250_AGGREGATE = {
    "rows": "5208",
    "defined_corrected_distances": "1423",
    "undefined_rows": "3785",
    "p1": "0.321861824814",
    "p2": "0.202650210076",
    "p3": "0.174975735761",
    "p4": "0.137608477166",
    "status": "diagnostic_only_not_wrr_reproduction",
}
EXPECTED_CAP1000_AGGREGATE = {
    "rows": "5208",
    "defined_corrected_distances": "2013",
    "undefined_rows": "3195",
    "p1": "6.65545084562e-07",
    "p2": "7.6208422043e-09",
    "p3": "0.00137172653677",
    "p4": "0.00474912112167",
    "status": "diagnostic_only_not_wrr_reproduction",
}
EXPECTED_CAP250_PERMUTATION = {
    "permutations": "1000",
    "seed": "1994",
    "sample_rows_written": "1001",
    "concepts": "30",
    "observed_rows": "182",
    "observed_defined_corrected_distances": "50",
    "rho_p1": "0.000999000999001",
    "rho_p2": "0.000999000999001",
    "rho_p3": "0.0044955044955",
    "rho_p4": "0.000999000999001",
    "rho0_bonferroni": "0.003996003996",
    "identity_permutations": "0",
    "status": "diagnostic_only_not_wrr_reproduction",
}
EXPECTED_CAP250_NO_WNP_999999 = {
    "permutations": "999999",
    "seed": "1994",
    "sample_rows_written": "1",
    "concepts": "30",
    "observed_rows": "174",
    "observed_defined_corrected_distances": "48",
    "rho_p1": "0.0011565",
    "rho_p2": "0.000215",
    "rho_p3": "0.0069545",
    "rho_p4": "0.000926",
    "rho0_bonferroni": "0.00086",
    "identity_permutations": "0",
    "status": "diagnostic_only_not_wrr_reproduction",
}
EXPECTED_CAP1000_PERMUTATION = {
    "permutations": "1000",
    "seed": "1994",
    "sample_rows_written": "1",
    "concepts": "30",
    "observed_rows": "182",
    "observed_defined_corrected_distances": "72",
    "rho_p1": "0.013986013986",
    "rho_p2": "0.000999000999001",
    "rho_p3": "0.0474525474525",
    "rho_p4": "0.000999000999001",
    "rho0_bonferroni": "0.003996003996",
    "identity_permutations": "0",
    "status": "diagnostic_only_not_wrr_reproduction",
}
EXPECTED_CAP1000_999999 = {
    "permutations": "999999",
    "seed": "1994",
    "sample_rows_written": "1",
    "concepts": "30",
    "observed_rows": "182",
    "observed_defined_corrected_distances": "72",
    "rho_p1": "0.019722",
    "rho_p2": "0.000101",
    "rho_p3": "0.0506065",
    "rho_p4": "0.000535",
    "rho0_bonferroni": "0.000404",
    "identity_permutations": "0",
    "status": "diagnostic_only_not_wrr_reproduction",
}

REQUIRED_PHRASES = (
    "# WRR Cross-Pair Grid",
    "Status: locked local permutation evidence; exact published WRR reproduction remains caveated.",
    "| pairs | 5208 |",
    "| same-record source pairs | 182 |",
    "| cross-record permutation pairs | 5026 |",
    "| defined `c(w,w')` rows | 1423 |",
    "| P1 | 0.321861824814 |",
    "legacy repo-defined diagnostics over the cap-250 corrected-distance field, not exact WRR reproductions.",
    "| permutations | 1000 |",
    "| observed defined `c(w,w')` values | 50 |",
    "| Bonferroni rho0 | 0.003996003996 |",
    "Legacy repo-defined 999,999-permutation run:",
    "| permutations | 999999 |",
    "| observed defined `c(w,w')` values | 48 |",
    "| Bonferroni rho0 | 0.00086 |",
    "## Cap-1000 Corrected-Distance Matrix",
    "| defined `c(w,w')` rows | 2013 |",
    "| P1 | 6.65545084562e-07 |",
    "| P2 | 7.6208422043e-09 |",
    "## Locked Cap-1000 Date-Permutation Run",
    "claim-grade for the repo-defined local lock policy",
    "| pair universe | selected full WRR2 source universe |",
    "| corrected-distance input | cap-1000 `corrected_distance` field |",
    "| observed source rows | 182 |",
    "| observed defined `c(w,w')` values | 72 |",
    "| rho P1 | 0.019722 |",
    "| rho P2 | 0.000101 |",
    "| Bonferroni rho0 | 0.000404 |",
    "Visual-review notes do not change pair inclusion until an explicit source policy is selected.",
    "Cap-1000 corrected-distance and date-permutation output from this grid is the locked local evidence path",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cross_pair_grid_doc(
        args.doc,
        args.grid_summary,
        args.cap250_summary,
        args.cap250_aggregate,
        args.cap250_permutation,
        args.cap250_no_wnp_999999,
        args.cap1000_summary,
        args.cap1000_aggregate,
        args.cap1000_permutation,
        args.cap1000_999999,
        args.grid_manifest,
        args.cap250_summary_manifest,
        args.cap250_aggregate_manifest,
        args.cap250_permutation_manifest,
        args.cap250_no_wnp_999999_manifest,
        args.cap1000_summary_manifest,
        args.cap1000_aggregate_manifest,
        args.cap1000_permutation_manifest,
        args.cap1000_999999_manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR cross-pair grid doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR cross-pair grid doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--grid-summary", type=Path, default=DEFAULT_GRID_SUMMARY)
    parser.add_argument("--cap250-summary", type=Path, default=DEFAULT_CAP250_SUMMARY)
    parser.add_argument("--cap250-aggregate", type=Path, default=DEFAULT_CAP250_AGGREGATE)
    parser.add_argument("--cap250-permutation", type=Path, default=DEFAULT_CAP250_PERMUTATION)
    parser.add_argument(
        "--cap250-no-wnp-999999",
        type=Path,
        default=DEFAULT_CAP250_NO_WNP_999999,
    )
    parser.add_argument("--cap1000-summary", type=Path, default=DEFAULT_CAP1000_SUMMARY)
    parser.add_argument(
        "--cap1000-aggregate",
        type=Path,
        default=DEFAULT_CAP1000_AGGREGATE,
    )
    parser.add_argument(
        "--cap1000-permutation",
        type=Path,
        default=DEFAULT_CAP1000_PERMUTATION,
    )
    parser.add_argument("--cap1000-999999", type=Path, default=DEFAULT_CAP1000_999999)
    parser.add_argument("--grid-manifest", type=Path, default=DEFAULT_GRID_MANIFEST)
    parser.add_argument(
        "--cap250-summary-manifest",
        type=Path,
        default=DEFAULT_CAP250_SUMMARY_MANIFEST,
    )
    parser.add_argument(
        "--cap250-aggregate-manifest",
        type=Path,
        default=DEFAULT_CAP250_AGGREGATE_MANIFEST,
    )
    parser.add_argument(
        "--cap250-permutation-manifest",
        type=Path,
        default=DEFAULT_CAP250_PERMUTATION_MANIFEST,
    )
    parser.add_argument(
        "--cap250-no-wnp-999999-manifest",
        type=Path,
        default=DEFAULT_CAP250_NO_WNP_999999_MANIFEST,
    )
    parser.add_argument(
        "--cap1000-summary-manifest",
        type=Path,
        default=DEFAULT_CAP1000_SUMMARY_MANIFEST,
    )
    parser.add_argument(
        "--cap1000-aggregate-manifest",
        type=Path,
        default=DEFAULT_CAP1000_AGGREGATE_MANIFEST,
    )
    parser.add_argument(
        "--cap1000-permutation-manifest",
        type=Path,
        default=DEFAULT_CAP1000_PERMUTATION_MANIFEST,
    )
    parser.add_argument(
        "--cap1000-999999-manifest",
        type=Path,
        default=DEFAULT_CAP1000_999999_MANIFEST,
    )
    return parser


def validate_cross_pair_grid_doc(
    doc: Path,
    grid_summary: Path | None = DEFAULT_GRID_SUMMARY,
    cap250_summary: Path | None = DEFAULT_CAP250_SUMMARY,
    cap250_aggregate: Path | None = DEFAULT_CAP250_AGGREGATE,
    cap250_permutation: Path | None = DEFAULT_CAP250_PERMUTATION,
    cap250_no_wnp_999999: Path | None = DEFAULT_CAP250_NO_WNP_999999,
    cap1000_summary: Path | None = DEFAULT_CAP1000_SUMMARY,
    cap1000_aggregate: Path | None = DEFAULT_CAP1000_AGGREGATE,
    cap1000_permutation: Path | None = DEFAULT_CAP1000_PERMUTATION,
    cap1000_999999: Path | None = DEFAULT_CAP1000_999999,
    grid_manifest: Path | None = DEFAULT_GRID_MANIFEST,
    cap250_summary_manifest: Path | None = DEFAULT_CAP250_SUMMARY_MANIFEST,
    cap250_aggregate_manifest: Path | None = DEFAULT_CAP250_AGGREGATE_MANIFEST,
    cap250_permutation_manifest: Path | None = DEFAULT_CAP250_PERMUTATION_MANIFEST,
    cap250_no_wnp_999999_manifest: Path | None = DEFAULT_CAP250_NO_WNP_999999_MANIFEST,
    cap1000_summary_manifest: Path | None = DEFAULT_CAP1000_SUMMARY_MANIFEST,
    cap1000_aggregate_manifest: Path | None = DEFAULT_CAP1000_AGGREGATE_MANIFEST,
    cap1000_permutation_manifest: Path | None = DEFAULT_CAP1000_PERMUTATION_MANIFEST,
    cap1000_999999_manifest: Path | None = DEFAULT_CAP1000_999999_MANIFEST,
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
        (grid_summary, EXPECTED_GRID_SUMMARY, "grid summary"),
        (cap250_summary, EXPECTED_CAP250_SUMMARY, "cap-250 corrected-distance summary"),
        (cap250_aggregate, EXPECTED_CAP250_AGGREGATE, "cap-250 aggregate"),
        (cap250_permutation, EXPECTED_CAP250_PERMUTATION, "cap-250 permutation"),
        (
            cap250_no_wnp_999999,
            EXPECTED_CAP250_NO_WNP_999999,
            "cap-250 no-WNP 999999 permutation",
        ),
        (cap1000_summary, EXPECTED_CAP1000_SUMMARY, "cap-1000 corrected-distance summary"),
        (cap1000_aggregate, EXPECTED_CAP1000_AGGREGATE, "cap-1000 aggregate"),
        (cap1000_permutation, EXPECTED_CAP1000_PERMUTATION, "cap-1000 permutation"),
        (cap1000_999999, EXPECTED_CAP1000_999999, "cap-1000 999999 permutation"),
    ]
    for path, expected, label in checks:
        if path is not None:
            failures.extend(validate_single_row_csv(path, expected, label))
    manifest_checks = [
        (
            grid_manifest,
            "grid manifest",
            "build_wrr_cross_pair_grid.py",
            EXPECTED_GRID_SUMMARY,
            {
                "rows": EXPECTED_GRID_SUMMARY["pairs"],
                "inputs": {
                    "terms": "reports/wrr_1994/wrr2_terms.csv",
                    "counts": "reports/wrr_1994/wrr2_genesis_counts.csv",
                    "skip_caps": "reports/wrr_1994/wrr2_skip_caps.csv",
                },
                "parameters": {
                    "appellation_min_term_length": 5,
                    "min_term_length": 5,
                    "max_term_length": 8,
                },
                "outputs": {
                    "csv": "reports/wrr_1994/wrr2_cross_pair_grid.csv",
                    "summary": str(DEFAULT_GRID_SUMMARY),
                    "markdown": "reports/wrr_1994/wrr2_cross_pair_grid.md",
                    "manifest": str(DEFAULT_GRID_MANIFEST),
                },
            },
        ),
        (
            cap250_summary_manifest,
            "cap-250 corrected-distance manifest",
            "analyze_wrr_corrected_distance.py",
            EXPECTED_CAP250_SUMMARY,
            corrected_distance_manifest_expected(
                search_max_skip=250,
                csv="reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_corrected_distance_250.csv",
                summary=str(DEFAULT_CAP250_SUMMARY),
                markdown="reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_corrected_distance_250.md",
                manifest=str(DEFAULT_CAP250_SUMMARY_MANIFEST),
            ),
        ),
        (
            cap250_aggregate_manifest,
            "cap-250 aggregate manifest",
            "analyze_wrr_corrected_distance_aggregate.py",
            EXPECTED_CAP250_AGGREGATE,
            aggregate_manifest_expected(
                input_path="reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_corrected_distance_250.csv",
                csv=str(DEFAULT_CAP250_AGGREGATE),
                markdown="reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_corrected_distance_250_aggregate.md",
                manifest=str(DEFAULT_CAP250_AGGREGATE_MANIFEST),
            ),
        ),
        (
            cap250_permutation_manifest,
            "cap-250 permutation manifest",
            "analyze_wrr_cross_pair_permutations.py",
            EXPECTED_CAP250_PERMUTATION,
            permutation_manifest_expected(
                input_path="reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_corrected_distance_250.csv",
                permutations=1000,
                sample_output_limit=-1,
                csv="reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_permutations_1000.csv",
                summary=str(DEFAULT_CAP250_PERMUTATION),
                markdown="reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_permutations_1000.md",
                manifest=str(DEFAULT_CAP250_PERMUTATION_MANIFEST),
            ),
        ),
        (
            cap250_no_wnp_999999_manifest,
            "cap-250 no-WNP 999999 manifest",
            "analyze_wrr_cross_pair_permutations.py",
            EXPECTED_CAP250_NO_WNP_999999,
            permutation_manifest_expected(
                input_path="reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_corrected_distance_250.csv",
                permutations=999999,
                sample_output_limit=0,
                csv="reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_permutations_no_wnp_999999_observed_only.csv",
                summary=str(DEFAULT_CAP250_NO_WNP_999999),
                markdown="reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_permutations_no_wnp_999999.md",
                manifest=str(DEFAULT_CAP250_NO_WNP_999999_MANIFEST),
                exclude_pair_review_status=["diagnostic_exclusion_candidate_not_locked"],
            ),
        ),
        (
            cap1000_summary_manifest,
            "cap-1000 corrected-distance manifest",
            "analyze_wrr_corrected_distance.py",
            EXPECTED_CAP1000_SUMMARY,
            corrected_distance_manifest_expected(
                search_max_skip=1000,
                csv="reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_corrected_distance_1000.csv",
                summary=str(DEFAULT_CAP1000_SUMMARY),
                markdown="reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_corrected_distance_1000.md",
                manifest=str(DEFAULT_CAP1000_SUMMARY_MANIFEST),
            ),
        ),
        (
            cap1000_aggregate_manifest,
            "cap-1000 aggregate manifest",
            "analyze_wrr_corrected_distance_aggregate.py",
            EXPECTED_CAP1000_AGGREGATE,
            aggregate_manifest_expected(
                input_path="reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_corrected_distance_1000.csv",
                csv=str(DEFAULT_CAP1000_AGGREGATE),
                markdown="reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_corrected_distance_1000_aggregate.md",
                manifest=str(DEFAULT_CAP1000_AGGREGATE_MANIFEST),
            ),
        ),
        (
            cap1000_permutation_manifest,
            "cap-1000 permutation manifest",
            "analyze_wrr_cross_pair_permutations.py",
            EXPECTED_CAP1000_PERMUTATION,
            permutation_manifest_expected(
                input_path="reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_corrected_distance_1000.csv",
                permutations=1000,
                sample_output_limit=0,
                csv="reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_1000_observed_only.csv",
                summary=str(DEFAULT_CAP1000_PERMUTATION),
                markdown="reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_1000.md",
                manifest=str(DEFAULT_CAP1000_PERMUTATION_MANIFEST),
            ),
        ),
        (
            cap1000_999999_manifest,
            "cap-1000 999999 manifest",
            "analyze_wrr_cross_pair_permutations.py",
            EXPECTED_CAP1000_999999,
            permutation_manifest_expected(
                input_path="reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_corrected_distance_1000.csv",
                permutations=999999,
                sample_output_limit=0,
                csv="reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_999999_observed_only.csv",
                summary=str(DEFAULT_CAP1000_999999),
                markdown="reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_999999.md",
                manifest=str(DEFAULT_CAP1000_999999_MANIFEST),
            ),
        ),
    ]
    for path, label, tool, expected_summary, expected_sections in manifest_checks:
        if path is not None:
            failures.extend(
                validate_manifest(path, label, tool, expected_summary, expected_sections)
            )
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


def validate_manifest(
    path: Path,
    label: str,
    tool: str,
    expected_summary: dict[str, str],
    expected_sections: dict[str, Any],
) -> list[str]:
    data = _read_json(path)
    if isinstance(data, str):
        return [data]
    failures: list[str] = []
    if data.get("tool") != tool:
        failures.append(f"{path} {label} tool drifted")
    failures.extend(
        compare_section(data.get("summary", {}), expected_summary, path, label, "summary")
    )
    for section, expected in expected_sections.items():
        if isinstance(expected, dict):
            failures.extend(
                compare_section(data.get(section, {}), expected, path, label, section)
            )
        elif stringify(data.get(section)) != stringify(expected):
            failures.append(f"{path} {label} {section} drifted")
    return failures


def compare_section(
    actual: object,
    expected: dict[str, Any],
    path: Path,
    label: str,
    section: str,
) -> list[str]:
    if not isinstance(actual, dict):
        return [f"{path} {label} {section} missing"]
    failures: list[str] = []
    for key, value in expected.items():
        if stringify(actual.get(key)) != stringify(value):
            failures.append(f"{path} {label} {section}.{key} drifted")
    return failures


def corrected_distance_manifest_expected(
    *,
    search_max_skip: int,
    csv: str,
    summary: str,
    markdown: str,
    manifest: str,
) -> dict[str, Any]:
    return {
        "rows": "5208",
        "pair_table": "reports/wrr_1994/wrr2_cross_pair_grid.csv",
        "config": "configs/example_koren_genesis.toml",
        "parameters": {
            "candidate_lane": "all",
            "min_skip": 2,
            "search_max_skip": search_max_skip,
            "direction": "both",
            "minimum_valid": 10,
            "skip_cap_mode": "term",
            "skip_cap_formula": "printed",
        },
        "outputs": {
            "csv": csv,
            "summary": summary,
            "markdown": markdown,
            "manifest": manifest,
        },
    }


def aggregate_manifest_expected(
    *,
    input_path: str,
    csv: str,
    markdown: str,
    manifest: str,
) -> dict[str, Any]:
    return {
        "input": input_path,
        "parameters": {"p1_threshold": 0.2},
        "outputs": {
            "csv": csv,
            "markdown": markdown,
            "manifest": manifest,
        },
    }


def permutation_manifest_expected(
    *,
    input_path: str,
    permutations: int,
    sample_output_limit: int,
    csv: str,
    summary: str,
    markdown: str,
    manifest: str,
    exclude_pair_review_status: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "input": input_path,
        "parameters": {
            "permutations": permutations,
            "seed": 1994,
            "p1_threshold": 0.2,
            "candidate_lane": [],
            "pair_review_status": [],
            "exclude_pair_review_status": exclude_pair_review_status or [],
            "sample_output_limit": sample_output_limit,
        },
        "outputs": {
            "csv": csv,
            "summary": summary,
            "markdown": markdown,
            "manifest": manifest,
        },
    }


def stringify(value: object) -> str:
    return str(value)


def _read_csv(path: Path) -> list[dict[str, str]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
