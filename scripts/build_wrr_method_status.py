#!/usr/bin/env python3
"""Build a WRR method-status matrix from current audit outputs."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_TEXT_SOURCE = Path("reports/wrr_1994/koren_genesis_text_source.csv")
DEFAULT_PAIR_SUMMARY = Path("reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv")
DEFAULT_DEFINED_PAIR_SUMMARY = Path("reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv")
DEFAULT_DEFINED_GAP_REASONS = Path("reports/wrr_1994/wrr_defined_gap_reasons.csv")
DEFAULT_ZERO_HIT_VARIANT_SUMMARY = Path("reports/wrr_1994/wrr_zero_hit_variant_probe_summary.csv")
DEFAULT_VARIANT_GAP_SUMMARY = Path("reports/wrr_1994/wrr_variant_gap_impact_summary.csv")
DEFAULT_VARIANT_RESIDUAL_SUMMARY = Path(
    "reports/wrr_1994/wrr_variant_residual_review_summary.csv"
)
DEFAULT_TABLE2_BRIDGE_SUMMARY = Path("reports/wrr_1994/wrr_table2_source_bridge_summary.csv")
DEFAULT_TABLE2_OCR_SUMMARY = Path("reports/wrr_1994/wrr_primary_table2_ocr_probe_summary.csv")
DEFAULT_TABLE2_ROW_OCR_SUMMARY = Path("reports/wrr_1994/wrr_primary_table2_row_ocr_probe_summary.csv")
DEFAULT_SKIP_SUMMARY = Path("reports/wrr_1994/wrr2_skip_caps_summary.csv")
DEFAULT_VARIANTS = Path("reports/wrr_1994/wrr2_corrected_distance_variant_comparison.csv")
DEFAULT_SOURCE_POLICY_SCENARIOS = Path("reports/wrr_1994/wrr_source_policy_scenarios.csv")
DEFAULT_SOURCE_POLICY_TERM_IMPACTS = Path(
    "reports/wrr_1994/wrr_source_policy_term_impacts.csv"
)
DEFAULT_DW_FORMULA_SENSITIVITY = Path("reports/wrr_1994/wrr_dw_formula_sensitivity.csv")
DEFAULT_AGGREGATE = Path(
    "reports/wrr_1994/direct_all/highcap_1000/"
    "wrr2_corrected_distance_all_lanes_aggregate.csv"
)
DEFAULT_CROSS_PAIR_PERMUTATION_SUMMARY = Path(
    "reports/wrr_1994/cross_pair_grid/highcap_1000/"
    "wrr2_cross_pair_permutations_1000_summary.csv"
)
DEFAULT_CROSS_PAIR_RECOMMENDED_PERMUTATION_SUMMARY = Path(
    "reports/wrr_1994/cross_pair_grid/highcap_1000/"
    "wrr2_cross_pair_permutations_999999_summary.csv"
)
DEFAULT_HIGHCAP_CORRECTED_DISTANCE_SUMMARY = Path(
    "reports/wrr_1994/direct_all/highcap_1000/"
    "wrr2_corrected_distance_all_lanes_merged_summary.csv"
)
DEFAULT_HIGHCAP_PERTURBATION_SUMMARY = Path(
    "reports/wrr_1994/highcap_1000/wrr2_perturbation_diagnostics_summary.csv"
)
DEFAULT_HIGHCAP_PAIR_READINESS_SUMMARY = Path(
    "reports/wrr_1994/highcap_1000/wrr2_perturbation_pair_readiness_summary.csv"
)
DEFAULT_PRIMARY_RESULT_TABLE = Path("reports/wrr_1994/wrr_primary_result_table.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_method_status.csv")
DEFAULT_MD = Path("docs/WRR_METHOD_STATUS.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_method_status.manifest.json")

FIELDNAMES = [
    "decision_area",
    "status",
    "current_read",
    "evidence",
    "next_action",
]

SOURCE_ANCHORS = [
    {
        "topic": "WRR printed D(w) formula",
        "source": "WRR 1994 Appendix A.4",
        "read": "Uses a term-specific skip bound chosen so the expected ELS count is 10; printed window count uses (D - 1)(2L - (k - 1)(D + 2)).",
    },
    {
        "topic": "WRR second-list filtered sample",
        "source": "WRR 1994 Appendix A.3",
        "read": "Restricts words to length 5..8 for the corrected-distance calculation and reports 298 word pairs before later defined-distance filtering.",
    },
    {
        "topic": "WRR permutation count",
        "source": "WRR 1994 main text and Appendix A.6",
        "read": "Uses 999,999 random permutations of the 32 personalities for significance calculations.",
    },
    {
        "topic": "Program formula mismatch",
        "source": "MBBK 1999 Appendix A",
        "read": "Reports that WRR programs used (D - 1)(2L - (k - 1)D), not the printed WRR 1994 formula.",
    },
    {
        "topic": "Corrected-distance definedness",
        "source": "MBBK 1999 Appendix A and Gans communities method section",
        "read": (
            "Treats c(w,w') as defined only when the ordinary perturbation is defined and at least 10 "
            "perturbation values are defined; MBBK uses greater-than-or-equal ranking while extracted "
            "WRR 1994 text has strict greater-than wording in one passage."
        ),
    },
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    text_row = read_one_row(args.text_source)
    pair_row = read_one_row(args.pair_summary)
    defined_pair_rows = read_rows(args.defined_pair_summary) if args.defined_pair_summary.exists() else []
    defined_gap_reason_rows = read_rows(args.defined_gap_reasons) if args.defined_gap_reasons.exists() else []
    zero_hit_variant_rows = read_rows(args.zero_hit_variant_summary) if args.zero_hit_variant_summary.exists() else []
    variant_gap_rows = read_rows(args.variant_gap_summary) if args.variant_gap_summary.exists() else []
    variant_residual_rows = read_optional_rows(args.variant_residual_summary)
    table2_bridge_row = read_one_row(args.table2_bridge_summary)
    table2_ocr_row = read_one_row(args.table2_ocr_summary)
    table2_row_ocr_row = read_one_row(args.table2_row_ocr_summary) if args.table2_row_ocr_summary.exists() else None
    skip_row = read_one_row(args.skip_summary)
    variant_rows = read_rows(args.corrected_distance_variants)
    source_policy_rows = read_optional_rows(args.source_policy_scenarios)
    source_policy_term_impact_rows = read_optional_rows(args.source_policy_term_impacts)
    dw_formula_rows = read_optional_rows(args.dw_formula_sensitivity)
    aggregate_row = read_one_row(args.corrected_distance_aggregate) if args.corrected_distance_aggregate.exists() else None
    cross_pair_permutation_row = read_optional_one_row(
        args.cross_pair_permutation_summary
    )
    cross_pair_recommended_permutation_row = read_optional_one_row(
        args.cross_pair_recommended_permutation_summary
    )
    highcap_corrected_distance_row = read_optional_one_row(
        args.highcap_corrected_distance_summary
    )
    highcap_perturbation_row = read_optional_one_row(args.highcap_perturbation_summary)
    highcap_pair_readiness_row = read_optional_one_row(args.highcap_pair_readiness_summary)
    primary_result_rows = read_rows(args.primary_result_table)
    rows = build_status_rows(
        text_row,
        pair_row,
        defined_pair_rows,
        defined_gap_reason_rows,
        zero_hit_variant_rows,
        variant_gap_rows,
        variant_residual_rows,
        skip_row,
        variant_rows,
        source_policy_rows,
        source_policy_term_impact_rows,
        dw_formula_rows,
        primary_result_rows,
        table2_bridge_row,
        table2_ocr_row,
        table2_row_ocr_row,
        aggregate_row,
        cross_pair_permutation_row,
        cross_pair_recommended_permutation_row,
        highcap_corrected_distance_row,
        highcap_perturbation_row,
        highcap_pair_readiness_row,
    )
    write_csv(args.out, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text-source", type=Path, default=DEFAULT_TEXT_SOURCE)
    parser.add_argument("--pair-summary", type=Path, default=DEFAULT_PAIR_SUMMARY)
    parser.add_argument("--defined-pair-summary", type=Path, default=DEFAULT_DEFINED_PAIR_SUMMARY)
    parser.add_argument("--defined-gap-reasons", type=Path, default=DEFAULT_DEFINED_GAP_REASONS)
    parser.add_argument("--zero-hit-variant-summary", type=Path, default=DEFAULT_ZERO_HIT_VARIANT_SUMMARY)
    parser.add_argument("--variant-gap-summary", type=Path, default=DEFAULT_VARIANT_GAP_SUMMARY)
    parser.add_argument("--variant-residual-summary", type=Path, default=DEFAULT_VARIANT_RESIDUAL_SUMMARY)
    parser.add_argument("--table2-bridge-summary", type=Path, default=DEFAULT_TABLE2_BRIDGE_SUMMARY)
    parser.add_argument("--table2-ocr-summary", type=Path, default=DEFAULT_TABLE2_OCR_SUMMARY)
    parser.add_argument("--table2-row-ocr-summary", type=Path, default=DEFAULT_TABLE2_ROW_OCR_SUMMARY)
    parser.add_argument("--skip-summary", type=Path, default=DEFAULT_SKIP_SUMMARY)
    parser.add_argument("--corrected-distance-variants", type=Path, default=DEFAULT_VARIANTS)
    parser.add_argument("--source-policy-scenarios", type=Path, default=DEFAULT_SOURCE_POLICY_SCENARIOS)
    parser.add_argument(
        "--source-policy-term-impacts",
        type=Path,
        default=DEFAULT_SOURCE_POLICY_TERM_IMPACTS,
    )
    parser.add_argument("--dw-formula-sensitivity", type=Path, default=DEFAULT_DW_FORMULA_SENSITIVITY)
    parser.add_argument("--corrected-distance-aggregate", type=Path, default=DEFAULT_AGGREGATE)
    parser.add_argument(
        "--cross-pair-permutation-summary",
        type=Path,
        default=DEFAULT_CROSS_PAIR_PERMUTATION_SUMMARY,
    )
    parser.add_argument(
        "--cross-pair-recommended-permutation-summary",
        type=Path,
        default=DEFAULT_CROSS_PAIR_RECOMMENDED_PERMUTATION_SUMMARY,
    )
    parser.add_argument(
        "--highcap-corrected-distance-summary",
        type=Path,
        default=DEFAULT_HIGHCAP_CORRECTED_DISTANCE_SUMMARY,
    )
    parser.add_argument(
        "--highcap-perturbation-summary",
        type=Path,
        default=DEFAULT_HIGHCAP_PERTURBATION_SUMMARY,
    )
    parser.add_argument(
        "--highcap-pair-readiness-summary",
        type=Path,
        default=DEFAULT_HIGHCAP_PAIR_READINESS_SUMMARY,
    )
    parser.add_argument("--primary-result-table", type=Path, default=DEFAULT_PRIMARY_RESULT_TABLE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise ValueError(f"expected exactly one row in {path}")
    return rows[0]


def read_optional_one_row(path: Path) -> dict[str, str] | None:
    if not path.exists():
        return None
    return read_one_row(path)


def read_optional_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_rows(path)


def build_status_rows(
    text_row: dict[str, str],
    pair_row: dict[str, str],
    defined_pair_rows: list[dict[str, str]] | None,
    defined_gap_reason_rows: list[dict[str, str]] | None,
    zero_hit_variant_rows: list[dict[str, str]] | None,
    variant_gap_rows: list[dict[str, str]] | None,
    variant_residual_rows: list[dict[str, str]] | None,
    skip_row: dict[str, str],
    variant_rows: list[dict[str, str]],
    source_policy_rows: list[dict[str, str]] | None = None,
    source_policy_term_impact_rows: list[dict[str, str]] | None = None,
    dw_formula_rows: list[dict[str, str]] | None = None,
    primary_result_rows: list[dict[str, str]] | None = None,
    table2_bridge_row: dict[str, str] | None = None,
    table2_ocr_row: dict[str, str] | None = None,
    table2_row_ocr_row: dict[str, str] | None = None,
    corrected_distance_aggregate_row: dict[str, str] | None = None,
    cross_pair_permutation_row: dict[str, str] | None = None,
    cross_pair_recommended_permutation_row: dict[str, str] | None = None,
    highcap_corrected_distance_row: dict[str, str] | None = None,
    highcap_perturbation_row: dict[str, str] | None = None,
    highcap_pair_readiness_row: dict[str, str] | None = None,
) -> list[dict[str, str]]:
    return [
        {
            "decision_area": "Genesis text stream",
            "status": "locally_locked",
            "current_read": "Koren Genesis stream has stable local fingerprint for smoke work.",
            "evidence": (
                f"{text_row.get('normalized_letters', '')} normalized letters; "
                f"{text_row.get('verse_count', '')} verses; normalized SHA-256 "
                f"{text_row.get('normalized_text_sha256', '')}"
            ),
            "next_action": "Cross-check against primary WRR text-source statement before claiming reproduction.",
        },
        {
            "decision_area": "WRR2 term source",
            "status": "working_source_locked",
            "current_read": "User authorized ANU/McKay WRR2 plain text as the working machine-readable source; it remains secondary-source, not primary-paper ground truth.",
            "evidence": (
                table2_bridge_evidence(table2_bridge_row)
                + "; "
                + table2_ocr_evidence(table2_ocr_row)
                + "; "
                + table2_row_ocr_evidence(table2_row_ocr_row)
                + optional_evidence(zero_hit_variant_evidence(zero_hit_variant_rows or []))
                + "; "
                f"{pair_row.get('source_records', '')} source records; "
                f"{pair_row.get('source_appellations', '')} appellations; "
                f"{pair_row.get('source_dates', '')} date rows; "
                f"{pair_row.get('source_undated_records', '')} undated records skipped"
            ),
            "next_action": "Use this source for working corrected-distance runs while keeping primary/OCR bridge evidence as provenance caveat.",
        },
        {
            "decision_area": "Pair universe",
            "status": "source_locked",
            "current_read": (
                "User selected keep_all_working_source: all imported WRR2 same-record "
                "pairs remain the working candidate universe; visual/source-review "
                "flags do not exclude pairs automatically, and 163 remains a "
                "defined-distance output target rather than a raw pair count."
            ),
            "evidence": pair_universe_evidence(
                pair_row,
                defined_pair_rows or [],
                defined_gap_reason_rows or [],
                source_policy_rows or [],
                source_policy_term_impact_rows or [],
                variant_gap_rows or [],
                variant_residual_rows or [],
            ),
            "next_action": (
                "Use the source-locked keep_all_working_source universe for local "
                "locked-method reporting, while keeping the 163-distance gap and "
                "manual no-source-change locks visible for exact published reproduction."
            ),
        },
        {
            "decision_area": "D(w) skip-cap formula",
            "status": "source_locked",
            "current_read": (
                "User selected the printed WRR formula as the main skip-cap rule; "
                "the reported WRR-program formula remains required sensitivity output."
            ),
            "evidence": (
                f"{skip_row.get('rows', '')} length-filtered rows; "
                f"{skip_row.get('program_cap_lt_printed', '')} program caps below printed; "
                f"{skip_row.get('program_cap_eq_printed', '')} equal caps; "
                f"{skip_row.get('target_unreached_rows', '')} rows do not reach target expected hits"
                + optional_evidence(dw_formula_sensitivity_evidence(dw_formula_rows or []))
            ),
            "next_action": (
                "Use printed-paper D(w) for main corrected-distance runs and keep "
                "reported-program D(w) side-by-side as sensitivity evidence."
            ),
        },
        corrected_distance_status(
            variant_rows,
            highcap_corrected_distance_row,
            highcap_perturbation_row,
            highcap_pair_readiness_row,
        ),
        aggregate_status(
            primary_result_rows or [],
            corrected_distance_aggregate_row,
            cross_pair_permutation_row,
            cross_pair_recommended_permutation_row,
        ),
    ]


def pair_universe_evidence(
    pair_row: dict[str, str],
    defined_pair_rows: list[dict[str, str]],
    defined_gap_reason_rows: list[dict[str, str]],
    source_policy_rows: list[dict[str, str]],
    source_policy_term_impact_rows: list[dict[str, str]],
    variant_gap_rows: list[dict[str, str]],
    variant_residual_rows: list[dict[str, str]],
) -> str:
    parts = [
        f"{pair_row.get('source_same_record_pairs', '')} raw same-record pairs",
        (
            f"{pair_row.get('appellation_min_length_same_record_pairs', '')} after appellation length >= "
            f"{pair_row.get('appellation_min_length', '')}"
        ),
        (
            f"{pair_row.get('length_filtered_same_record_pairs', '')} in current length "
            f"{pair_row.get('length_filter_min', '')}..{pair_row.get('length_filter_max', '')} smoke lane"
        ),
        f"{pair_row.get('expected_published_pairs', '')} cited second-list distances",
        "298 paper-stated candidate word pairs",
    ]
    best = best_defined_pair_summary(defined_pair_rows)
    if best:
        parts.append(
            f"defined pair-set audit best run {best.get('run_label', '')}: "
            f"{best.get('defined', '')} defined of {best.get('source_cited_defined_distances', '')}, "
            f"gap {best.get('defined_gap_to_source_cited', '')}, "
            f"{best.get('ordinary_not_valid', '')} ordinary-not-valid"
        )
    gap_read = best_gap_reason_evidence(defined_gap_reason_rows)
    if gap_read:
        parts.append(gap_read)
    source_policy_read = source_policy_evidence(source_policy_rows)
    if source_policy_read:
        parts.append(source_policy_read)
    term_impact_read = source_policy_term_impact_evidence(source_policy_term_impact_rows)
    if term_impact_read:
        parts.append(term_impact_read)
    variant_gap_read = variant_gap_evidence(variant_gap_rows)
    if variant_gap_read:
        parts.append(variant_gap_read)
    variant_residual_read = variant_residual_evidence(variant_residual_rows)
    if variant_residual_read:
        parts.append(variant_residual_read)
    return "; ".join(parts)


def best_defined_pair_summary(rows: list[dict[str, str]]) -> dict[str, str] | None:
    return max(rows, key=lambda row: int_value(row.get("defined", "")), default=None)


def best_gap_reason_evidence(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    best_label = ""
    best_defined = -1
    for row in rows:
        defined = int_value(row.get("run_defined", ""))
        if defined > best_defined:
            best_defined = defined
            best_label = row.get("run_label", "")
    best_rows = {row.get("reason", ""): row for row in rows if row.get("run_label", "") == best_label}
    if not best_rows:
        return ""
    return (
        f"gap-reason audit best run {best_label}: "
        f"{pairs_for_reason(best_rows, 'ordinary_missing_appellation_hits')} no-appellation ordinary hits, "
        f"{pairs_for_reason(best_rows, 'ordinary_missing_date_hits')} no-date ordinary hits, "
        f"{pairs_for_reason(best_rows, 'ordinary_missing_both_terms')} neither-term ordinary hits, "
        f"{pairs_for_reason(best_rows, 'under_minimum_valid_perturbations')} under-minimum"
    )


def pairs_for_reason(rows_by_reason: dict[str, dict[str, str]], reason: str) -> int:
    return int_value(rows_by_reason.get(reason, {}).get("pairs", ""))


def optional_evidence(value: str) -> str:
    return f"; {value}" if value else ""


def source_policy_evidence(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    scenarios = [
        scenario_evidence(rows, "keep_all_working_source", "baseline"),
        scenario_evidence(rows, "exclude_wnp_zacut_only", "exclude WNP Zacut"),
        scenario_evidence(rows, "exclude_all_source_review_flags", "exclude all flags"),
    ]
    scenario_parts = [part for part in scenarios if part]
    if not scenario_parts:
        return ""
    return (
        "source-policy scenarios: "
        + "; ".join(scenario_parts)
        + (
            "; source policy selected: keep_all_working_source; Visual triage "
            "notes do not exclude pairs automatically"
        )
    )


def scenario_evidence(rows: list[dict[str, str]], scenario: str, label: str) -> str:
    row = next((item for item in rows if item.get("scenario") == scenario), None)
    if not row:
        return ""
    return (
        f"{label} >=5 {row.get('remaining_appellation_min_length_pairs', '')} "
        f"(gap {row.get('gap_to_source_cited_163_after_appellation_min_length', '')})"
    )


def source_policy_term_impact_evidence(rows: list[dict[str, str]]) -> str:
    closing_rows = [
        row
        for row in rows
        if row.get("closes_appellation_min_length_gap_to_163", "").lower() == "true"
    ]
    if not closing_rows:
        return ""
    first = closing_rows[0]
    terms = ", ".join(row.get("term", "") for row in closing_rows[:4] if row.get("term"))
    example_text = f"; examples {terms}" if terms else ""
    return (
        "single-term source-policy impacts: "
        f"{len(closing_rows)} term(s) individually leave >=5 "
        f"{first.get('remaining_appellation_min_length_pairs_if_excluded', '')} "
        f"(gap {first.get('gap_to_source_cited_163_after_appellation_min_length_if_excluded', '')})"
        f"{example_text}; diagnostic only"
    )


def variant_gap_evidence(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    run_label = preferred_variant_gap_run_label(rows)
    by_status = {
        row.get("impact_status", ""): row
        for row in rows
        if row.get("run_label", "") == run_label
    }
    if not by_status:
        return ""
    all_hits = by_status.get("all_blocking_terms_have_variant_hit", {}).get("pairs", "")
    some_hits = by_status.get("some_blocking_terms_have_variant_hit", {}).get("pairs", "")
    no_hits = by_status.get("no_blocking_term_variant_hit", {}).get("pairs", "")
    return (
        f"variant-gap impact best run {run_label}: "
        f"{all_hits} blocked pairs have all blocking terms with variant leads, "
        f"{some_hits} have partial variant leads, {no_hits} have no simple variant lead; "
        "diagnostic only"
    )


def variant_residual_evidence(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    pool = next((row for row in rows if row.get("group") == "residual_pool"), None)
    frontier = next((row for row in rows if row.get("group") == "review_frontier"), None)
    if not pool:
        return ""
    return (
        f"variant residual review best run {pool.get('run_label', '')}: "
        f"{pool.get('candidate_pool_pairs', '')} residual candidate pairs, "
        f"{pool.get('residual_needed', '')} needed after the simple-variant upper bound, "
        f"{pool.get('residual_slack_pairs', '')} slack pairs"
        + (
            f"; priority frontier {frontier.get('pairs', '')} rows"
            if frontier
            else ""
        )
        + "; diagnostic only"
    )


def preferred_variant_gap_run_label(rows: list[dict[str, str]]) -> str:
    labels = {row.get("run_label", "") for row in rows}
    for label in ("all_lanes_cap1000", "all_lanes_cap1000_program", "all_lanes_cap250"):
        if label in labels:
            return label
    totals: dict[str, int] = {}
    for row in rows:
        label = row.get("run_label", "")
        totals[label] = totals.get(label, 0) + int_value(row.get("pairs", ""))
    return max(totals, key=totals.get, default="")


def dw_formula_sensitivity_evidence(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    all_lanes = next((row for row in rows if row.get("scope") == "all_lanes_cap1000"), None)
    smoke = next((row for row in rows if row.get("scope") == "smoke_length_5_8_cap250"), None)
    parts: list[str] = []
    if all_lanes:
        parts.append(
            "all-lane cap1000 printed/program defined "
            f"{all_lanes.get('printed_defined_corrected_distances', '')}/"
            f"{all_lanes.get('program_defined_corrected_distances', '')}; "
            f"{all_lanes.get('changed_pairs', '')} changed pairs"
        )
    if smoke:
        parts.append(
            "smoke cap250 printed/program/fixed250 defined "
            f"{smoke.get('printed_defined_corrected_distances', '')}/"
            f"{smoke.get('program_defined_corrected_distances', '')}/"
            f"{smoke.get('fixed_250_defined_corrected_distances', '')}"
        )
    if not parts:
        return ""
    return (
        "D(w) sensitivity: "
        + "; ".join(parts)
        + "; printed formula selected as main; program formula retained as sensitivity"
    )


def zero_hit_variant_evidence(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    zero_terms = sum(int_value(row.get("zero_terms", "")) for row in rows)
    with_hit = sum(int_value(row.get("terms_with_variant_hit", "")) for row in rows)
    variant_hits = sum(int_value(row.get("best_variant_total_hits", "")) for row in rows)
    details = ", ".join(
        (
            f"{row.get('category', '')} "
            f"{row.get('terms_with_variant_hit', '')}/{row.get('zero_terms', '')}"
        )
        for row in rows
    )
    return (
        "zero-hit variant probe found simple one-edit raw ELS variants for "
        f"{with_hit}/{zero_terms} zero-hit terms ({details}), total variant hits "
        f"{variant_hits}; diagnostic_only_not_source_correction"
    )


def corrected_distance_status(
    variant_rows: list[dict[str, str]],
    highcap_corrected_distance_row: dict[str, str] | None = None,
    highcap_perturbation_row: dict[str, str] | None = None,
    highcap_pair_readiness_row: dict[str, str] | None = None,
) -> dict[str, str]:
    if not variant_rows:
        return {
            "decision_area": "Corrected distance c(w,w')",
            "status": "missing",
            "current_read": "No corrected-distance variant rows supplied.",
            "evidence": "",
            "next_action": "Run corrected-distance smoke before method review.",
        }
    defined_counts = [int_value(row.get("defined_corrected_distances", "")) for row in variant_rows]
    max_valid = max(int_value(row.get("max_pair_valid_perturbations", "")) for row in variant_rows)
    variants = ", ".join(
        f"{row.get('variant', '')}: {row.get('defined_corrected_distances', '')} defined"
        for row in variant_rows
    )
    total_defined = sum(defined_counts)
    evidence_parts = [
        f"{variants}; maximum valid perturbation count {max_valid}; total defined {total_defined}"
    ]
    highcap = highcap_evidence(
        highcap_corrected_distance_row,
        highcap_perturbation_row,
        highcap_pair_readiness_row,
    )
    full_run = is_full_corrected_distance_run(highcap_corrected_distance_row)
    if highcap:
        evidence_parts.append(highcap)
    return {
        "decision_area": "Corrected distance c(w,w')",
        "status": "defined_full_run" if full_run else "smoke_only",
        "current_read": corrected_distance_current_read(total_defined, full_run),
        "evidence": "; ".join(evidence_parts),
        "next_action": corrected_distance_next_action(full_run),
    }


def is_full_corrected_distance_run(row: dict[str, str] | None) -> bool:
    if not row:
        return False
    pairs = int_value(row.get("pairs", ""))
    return (
        row.get("candidate_lane") == "all"
        and pairs > 0
        and pairs == int_value(row.get("selected_pairs", ""))
        and row.get("skip_cap_formula") == "printed"
    )


def corrected_distance_current_read(total_defined: int, full_run: bool) -> str:
    if full_run:
        return (
            "Full selected keep_all_working_source corrected-distance output exists "
            "for all imported same-record pairs using printed D(w); undefined rows "
            "remain ordinary-not-valid rather than missing work."
        )
    if total_defined:
        return (
            "Direct perturbed-letter smoke driver now produces defined corrected distances in the "
            "current candidate lane, but this remains diagnostic until the full selected "
            "keep_all_working_source universe has defined corrected-distance output."
        )
    return "Smoke driver exists, but current candidate lane produces no defined corrected distances."


def corrected_distance_next_action(full_run: bool) -> str:
    if full_run:
        return (
            "Use the full selected-universe corrected-distance output for aggregate/permutation "
            "locking while keeping exact-WRR reproduction caveats visible."
        )
    return (
        "Extend direct perturbed search over the selected keep_all_working_source "
        "universe using printed D(w) as main and program D(w) as sensitivity."
    )


def highcap_evidence(
    corrected_distance_row: dict[str, str] | None,
    perturbation_row: dict[str, str] | None,
    pair_readiness_row: dict[str, str] | None,
) -> str:
    parts: list[str] = []
    if corrected_distance_row:
        if is_full_corrected_distance_run(corrected_distance_row):
            parts.append(
                "full all-lane cap "
                f"{corrected_distance_row.get('search_max_skip', '')} run: "
                f"{corrected_distance_row.get('defined_corrected_distances', '')} defined over "
                f"{corrected_distance_row.get('pairs', '')} selected pairs, "
                f"{corrected_distance_row.get('ordinary_not_valid_pairs', '')} ordinary-not-valid, "
                f"{corrected_distance_row.get('under_minimum_valid_pairs', '')} under-minimum, "
                f"max valid {corrected_distance_row.get('max_pair_valid_perturbations', '')}; "
                f"status {corrected_distance_row.get('status', '')}"
            )
        else:
            parts.append(
                "high-cap "
                f"{corrected_distance_row.get('search_max_skip', '')} split: "
                f"{corrected_distance_row.get('defined_corrected_distances', '')} defined over "
                f"{corrected_distance_row.get('pairs', '')} pairs, max valid "
                f"{corrected_distance_row.get('max_pair_valid_perturbations', '')}"
            )
    if perturbation_row:
        parts.append(
            "legacy ordinary-hit perturbation diagnostic: "
            f"{perturbation_row.get('rows_with_hits', '')}/{perturbation_row.get('rows', '')} rows with hits, "
            f"max row-min exact {perturbation_row.get('max_exact_perturbation_matches', '')}, "
            f"{perturbation_row.get('rows_with_checked_under_10_exact_matches', '')} rows under 10 exact"
        )
    if pair_readiness_row:
        parts.append(
            "legacy ordinary-hit pair readiness: "
            f"{pair_readiness_row.get('pairs_ready', '')} ready, "
            f"{pair_readiness_row.get('pairs_missing_checked_hits', '')} missing hits, "
            f"{pair_readiness_row.get('pairs_under_10_exact_matches', '')} under exact"
        )
    return "; ".join(part for part in parts if part)


def aggregate_status(
    primary_result_rows: list[dict[str, str]],
    corrected_distance_aggregate_row: dict[str, str] | None = None,
    cross_pair_permutation_row: dict[str, str] | None = None,
    cross_pair_recommended_permutation_row: dict[str, str] | None = None,
) -> dict[str, str]:
    local_evidence = aggregate_evidence(corrected_distance_aggregate_row)
    permutation_locked = is_full_universe_permutation_lock(
        corrected_distance_aggregate_row,
        cross_pair_recommended_permutation_row,
    )
    permutation_evidence = cross_pair_permutation_evidence(
        cross_pair_permutation_row,
        "cap1000 1000-sample date-label diagnostic",
    )
    recommended_permutation_evidence = cross_pair_permutation_evidence(
        cross_pair_recommended_permutation_row,
        "locked keep-all cap1000 999999 date-label permutation",
    )
    has_permutation = bool(
        cross_pair_permutation_row or cross_pair_recommended_permutation_row
    )
    if permutation_locked:
        status = "permutation_locked"
    elif has_permutation:
        status = "diagnostic_not_claim_grade"
    else:
        status = "source_locked_not_built"
    current_read = (
        "Full selected-universe cap1000 aggregate/permutation is locked under "
        "the repo policy: keep_all_working_source, printed D(w), and 999,999 "
        "date-label shuffles. This supports locked-method local evidence, not "
        "an exact published WRR reproduction claim."
        if permutation_locked
        else "Published Table 3 ranks are source-audited; local diagnostic P1..P4 "
        "and date-permutation runs exist, including a repo-defined 999,999 "
        "run, but this is not an exact WRR reproduction."
        if has_permutation
        else "Published Table 3 ranks are source-audited; local P1..P4 aggregate diagnostics exist, but the date-permutation runner is not built."
    )
    next_action = (
        "Use the locked-method result with caveats: the local selected-policy run is complete, while exact published-WRR reproduction remains unsupported by the current source-defined 163-distance gap."
        if permutation_locked
        else "Use the full selected-universe corrected-distance output and repo-defined 999,999 diagnostic for local evidence; lock aggregate/permutation before exact WRR reproduction language."
        if has_permutation
        else "Implement only after final pair universe and corrected-distance values are locked."
    )
    genesis = next(
        (row for row in primary_result_rows if row.get("label") == "G" and row.get("status") == "found"),
        None,
    )
    if genesis is None:
        return {
            "decision_area": "Aggregate statistic and permutation",
            "status": status if cross_pair_permutation_row else "not_built",
            "current_read": current_read,
            "evidence": "; ".join(
                part
                for part in [
                    "No primary Table 3 source-result row was supplied",
                    local_evidence,
                    permutation_evidence,
                    recommended_permutation_evidence,
                ]
                if part
            ),
            "next_action": next_action,
        }
    control_summary = ", ".join(
        f"{row.get('label', '')} p0={row.get('bonferroni_p0', '')}"
        for row in primary_result_rows
        if row.get("label") != "G" and row.get("status") == "found"
    )
    return {
        "decision_area": "Aggregate statistic and permutation",
        "status": status,
        "current_read": current_read,
        "evidence": "; ".join(
            part
            for part in [
                (
                    f"Source Table 3: G min {genesis.get('min_statistic', '')} rank "
                    f"{genesis.get('min_rank', '')}, p0={genesis.get('bonferroni_p0', '')}"
                ),
                f"controls: {control_summary}",
                local_evidence,
                permutation_evidence,
                recommended_permutation_evidence,
            ]
            if part
        ),
        "next_action": next_action,
    }


def cross_pair_permutation_evidence(row: dict[str, str] | None, label: str) -> str:
    if not row:
        return ""
    return (
        f"{label}: "
        f"{row.get('permutations', '')} permutations, seed {row.get('seed', '')}, "
        f"{row.get('observed_defined_corrected_distances', '')} observed defined c-values "
        f"over {row.get('observed_rows', '')} rows; "
        f"rho P1={row.get('rho_p1', '')}, P2={row.get('rho_p2', '')}, "
        f"P3={row.get('rho_p3', '')}, P4={row.get('rho_p4', '')}, "
        f"rho0={row.get('rho0_bonferroni', '')}"
    )


def is_full_universe_permutation_lock(
    aggregate_row: dict[str, str] | None,
    permutation_row: dict[str, str] | None,
) -> bool:
    if not aggregate_row or not permutation_row:
        return False
    return (
        int_value(permutation_row.get("permutations", "")) == 999999
        and int_value(permutation_row.get("observed_rows", ""))
        == int_value(aggregate_row.get("rows", ""))
        and int_value(permutation_row.get("observed_defined_corrected_distances", ""))
        == int_value(aggregate_row.get("defined_corrected_distances", ""))
        and "highcap_1000" in permutation_row.get("source", "")
    )


def aggregate_evidence(row: dict[str, str] | None) -> str:
    if not row:
        return "no current protocol step computes aggregate scores from defined c-values"
    defined = row.get("defined_corrected_distances", "")
    if defined == "0":
        return (
            f"local P1..P4 aggregate diagnostic has {defined} defined c-values "
            f"from {row.get('rows', '')} rows, so P1..P4 remain blank"
        )
    return (
        f"local P1={row.get('p1', '')}, P2={row.get('p2', '')}, "
        f"P3={row.get('p3', '')}, P4={row.get('p4', '')} from "
        f"{defined} defined c-values from {row.get('rows', '')} rows; "
        "P3/P4 smaller sample has "
        f"{row.get('p3_p4_sample_defined_corrected_distances', '')} defined c-values"
    )


def int_value(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    lines = [
        "# WRR Method Status",
        "",
        "Status: current audit matrix; not an exact published WRR reproduction.",
        "",
        "This file summarizes what the current local WRR work has locked and what",
        "still has a 163-distance gap; current manual records do not authorize source edits.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_method_status "
            f"--text-source {args.text_source} "
            f"--pair-summary {args.pair_summary} "
            f"--defined-pair-summary {args.defined_pair_summary} "
            f"--defined-gap-reasons {args.defined_gap_reasons} "
            f"--zero-hit-variant-summary {args.zero_hit_variant_summary} "
            f"--variant-gap-summary {args.variant_gap_summary} "
            f"--variant-residual-summary {args.variant_residual_summary} "
            f"--table2-bridge-summary {args.table2_bridge_summary} "
            f"--table2-ocr-summary {args.table2_ocr_summary} "
            f"--table2-row-ocr-summary {getattr(args, 'table2_row_ocr_summary', '')} "
            f"--skip-summary {args.skip_summary} "
            f"--corrected-distance-variants {args.corrected_distance_variants} "
            f"--source-policy-scenarios {args.source_policy_scenarios} "
            f"--source-policy-term-impacts {args.source_policy_term_impacts} "
            f"--dw-formula-sensitivity {args.dw_formula_sensitivity} "
            f"--corrected-distance-aggregate {args.corrected_distance_aggregate} "
            f"--cross-pair-permutation-summary {args.cross_pair_permutation_summary} "
            f"--cross-pair-recommended-permutation-summary {args.cross_pair_recommended_permutation_summary} "
            f"--highcap-corrected-distance-summary {args.highcap_corrected_distance_summary} "
            f"--highcap-perturbation-summary {args.highcap_perturbation_summary} "
            f"--highcap-pair-readiness-summary {args.highcap_pair_readiness_summary} "
            f"--primary-result-table {args.primary_result_table} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Matrix",
        "",
        "| Area | Status | Current read | Evidence | Next action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["decision_area"]),
                    f"`{markdown_cell(row['status'])}`",
                    markdown_cell(row["current_read"]),
                    markdown_cell(row["evidence"]),
                    markdown_cell(row["next_action"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Source Anchors",
            "",
            "| Topic | Source | Current read |",
            "| --- | --- | --- |",
        ]
    )
    for row in SOURCE_ANCHORS:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["topic"]),
                    markdown_cell(row["source"]),
                    markdown_cell(row["read"]),
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def table2_bridge_evidence(row: dict[str, str] | None) -> str:
    if not row:
        return "primary Table 2 bridge not supplied"
    return (
        f"{row.get('primary_rows_found', '')}/{row.get('primary_rows', '')} primary Table 2 "
        f"English row labels found; {row.get('secondary_records', '')} secondary records; "
        f"{row.get('primary_hebrew_cells_verified', '')} primary Hebrew cells verified"
    )


def table2_ocr_evidence(row: dict[str, str] | None) -> str:
    if not row:
        return "primary Table 2 OCR probe not supplied"
    return (
        f"OCR probe matched {row.get('matched_terms', '')}/{row.get('total_terms', '')} "
        f"secondary Hebrew terms "
        f"({row.get('matched_appellation_terms', '')}/{row.get('appellation_terms', '')} appellations, "
        f"{row.get('matched_date_terms', '')}/{row.get('date_terms', '')} dates); "
        f"{row.get('status', '')}"
    )


def table2_row_ocr_evidence(row: dict[str, str] | None) -> str:
    if not row:
        return "primary Table 2 row OCR probe not supplied"
    return (
        f"row OCR probe matched {row.get('matched_terms', '')}/{row.get('total_terms', '')} "
        f"row-specific secondary Hebrew terms "
        f"({row.get('matched_appellation_terms', '')}/{row.get('appellation_terms', '')} appellations, "
        f"{row.get('matched_date_terms', '')}/{row.get('date_terms', '')} dates); "
        f"{count_phrase(row, 'detected_row_markers', 'detected row marker')}; "
        f"{count_phrase(row, 'inferred_row_markers', 'inferred row marker')}; "
        f"{row.get('status', '')}"
    )


def count_phrase(row: dict[str, str], key: str, singular_label: str) -> str:
    count = row.get(key, "")
    label = singular_label if count == "1" else f"{singular_label}s"
    return f"{count} {label}"


def write_manifest(args: argparse.Namespace, rows: list[dict[str, str]], started: float) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "text_source": str(args.text_source),
            "pair_summary": str(args.pair_summary),
            "defined_pair_summary": str(args.defined_pair_summary),
            "defined_gap_reasons": str(args.defined_gap_reasons),
            "zero_hit_variant_summary": str(args.zero_hit_variant_summary),
            "variant_gap_summary": str(args.variant_gap_summary),
            "variant_residual_summary": str(args.variant_residual_summary),
            "table2_bridge_summary": str(args.table2_bridge_summary),
            "table2_ocr_summary": str(args.table2_ocr_summary),
            "table2_row_ocr_summary": str(args.table2_row_ocr_summary),
            "skip_summary": str(args.skip_summary),
            "corrected_distance_variants": str(args.corrected_distance_variants),
            "source_policy_scenarios": str(args.source_policy_scenarios),
            "source_policy_term_impacts": str(args.source_policy_term_impacts),
            "dw_formula_sensitivity": str(args.dw_formula_sensitivity),
            "corrected_distance_aggregate": str(args.corrected_distance_aggregate),
            "cross_pair_permutation_summary": str(args.cross_pair_permutation_summary),
            "cross_pair_recommended_permutation_summary": str(
                args.cross_pair_recommended_permutation_summary
            ),
            "highcap_corrected_distance_summary": str(
                args.highcap_corrected_distance_summary
            ),
            "highcap_perturbation_summary": str(args.highcap_perturbation_summary),
            "highcap_pair_readiness_summary": str(args.highcap_pair_readiness_summary),
            "primary_result_table": str(args.primary_result_table),
        },
        "outputs": {
            "csv": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
