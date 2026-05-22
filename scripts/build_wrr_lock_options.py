#!/usr/bin/env python3
"""Build a WRR lock-options report from current audit summaries."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_PAIR_SUMMARY = Path("reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv")
DEFAULT_SKIP_SUMMARY = Path("reports/wrr_1994/wrr2_skip_caps_summary.csv")
DEFAULT_VARIANTS = Path("reports/wrr_1994/wrr2_corrected_distance_variant_comparison.csv")
DEFAULT_RECOMMENDED_PERMUTATION = Path(
    "reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_permutations_no_wnp_999999_summary.csv"
)
DEFAULT_OUT = Path("reports/wrr_1994/wrr_lock_options.csv")
DEFAULT_MD = Path("docs/WRR_LOCK_OPTIONS.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_lock_options.manifest.json")

FIELDNAMES = [
    "area",
    "option",
    "status",
    "evidence",
    "recommendation",
    "claim_boundary",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    pair_row = read_one_row(args.pair_summary)
    skip_row = read_one_row(args.skip_summary)
    variant_rows = read_rows(args.variants)
    permutation_row = read_one_row(args.recommended_permutation)
    rows = build_option_rows(pair_row, skip_row, variant_rows, permutation_row)
    write_csv(args.out, rows)
    write_markdown(args.markdown_out, rows)
    write_manifest(args.manifest_out, args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair-summary", type=Path, default=DEFAULT_PAIR_SUMMARY)
    parser.add_argument("--skip-summary", type=Path, default=DEFAULT_SKIP_SUMMARY)
    parser.add_argument("--variants", type=Path, default=DEFAULT_VARIANTS)
    parser.add_argument("--recommended-permutation", type=Path, default=DEFAULT_RECOMMENDED_PERMUTATION)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_option_rows(
    pair_row: dict[str, str],
    skip_row: dict[str, str],
    variant_rows: list[dict[str, str]],
    permutation_row: dict[str, str],
) -> list[dict[str, str]]:
    imported_pairs = pair_row.get("imported_same_record_pairs", "")
    appellation_min_pairs = pair_row.get("appellation_min_length_same_record_pairs", "")
    one_zacut_pairs = pair_row.get("appellation_min_length_pairs_after_one_zacut_appellation_excluded", "")
    expected_pairs = pair_row.get("expected_published_pairs", "")
    length_filtered_pairs = pair_row.get("length_filtered_same_record_pairs", "")
    wnp_delta = pair_row.get("wnp_disputed_zacut_appellation_min_length_pair_delta", "")
    printed_defined = variant_value(variant_rows, "term_printed", "defined_corrected_distances")
    program_defined = variant_value(variant_rows, "term_program", "defined_corrected_distances")
    fixed_defined = variant_value(variant_rows, "fixed_250", "defined_corrected_distances")
    return [
        {
            "area": "Pair universe",
            "option": "all imported WRR2 same-record pairs",
            "status": "candidate_input_only",
            "evidence": (
                f"{imported_pairs} imported same-record pairs; source-cited second-list "
                f"defined distances = {expected_pairs}; raw imported count does not equal the cited distance count."
            ),
            "recommendation": (
                "Use as the broad working input for diagnostics, not as the final claimed WRR pair universe."
            ),
            "claim_boundary": "not claim-ready",
        },
        {
            "area": "Pair universe",
            "option": "appellation length >= 5 rows",
            "status": "near_count_not_lock",
            "evidence": (
                f"{appellation_min_pairs} same-record pairs after appellation length filter; "
                f"{length_filtered_pairs} after both-side 5..8 filter."
            ),
            "recommendation": (
                "Keep as reconciliation evidence only; this still does not source-lock the final 163 distances."
            ),
            "claim_boundary": "not claim-ready",
        },
        {
            "area": "Pair universe",
            "option": "single Zacut appellation exclusion",
            "status": "diagnostic_only",
            "evidence": (
                f"One length-eligible Zacut appellation exclusion gives {one_zacut_pairs}; "
                f"all WNP-disputed Zacut appellations would remove {wnp_delta} pairs."
            ),
            "recommendation": (
                "Do not lock from this alone. The source critique explains a clue, not a WRR exclusion rule."
            ),
            "claim_boundary": "not claim-ready",
        },
        {
            "area": "Pair universe",
            "option": "defined-distance output interpretation",
            "status": "recommended_working_interpretation",
            "evidence": (
                f"The cited {expected_pairs} is best treated as a corrected-distance output count, "
                "not a raw table count."
            ),
            "recommendation": (
                "Next no-input path: compute corrected distances over the broad working input and report the defined set."
            ),
            "claim_boundary": "still blocked until source and formula locks",
        },
        {
            "area": "D(w) skip-cap formula",
            "option": "printed WRR formula",
            "status": "primary_text_default",
            "evidence": (
                f"{skip_row.get('rows', '')} skip-cap rows; printed formula currently selected in the audit; "
                f"{skip_row.get('target_unreached_rows', '')} rows do not reach the expected-hit target."
            ),
            "recommendation": "Keep as the source-facing default because it is the printed WRR formula.",
            "claim_boundary": "not claim-ready without final pair lock",
        },
        {
            "area": "D(w) skip-cap formula",
            "option": "reported WRR-program formula",
            "status": "sensitivity_variant",
            "evidence": (
                f"{skip_row.get('program_cap_lt_printed', '')} program caps below printed; "
                f"{skip_row.get('program_cap_eq_printed', '')} equal; "
                f"defined smoke rows printed/program/fixed250 = {printed_defined}/{program_defined}/{fixed_defined}."
            ),
            "recommendation": (
                "Carry as a required sensitivity run because MBBK reports the WRR programs used this formula."
            ),
            "claim_boundary": "not claim-ready without source decision",
        },
        {
            "area": "Permutation",
            "option": "repo-defined WNP-excluded 999,999 date-label diagnostic",
            "status": "best_current_diagnostic_not_reproduction",
            "evidence": (
                f"{permutation_row.get('permutations', '')} permutations; "
                f"{permutation_row.get('observed_rows', '')} observed rows; "
                f"{permutation_row.get('observed_defined_corrected_distances', '')} defined c-values; "
                f"rho0={permutation_row.get('rho0_bonferroni', '')}."
            ),
            "recommendation": (
                "Use for local diagnostic evidence while keeping exact WRR reproduction blocked."
            ),
            "claim_boundary": "diagnostic only",
        },
    ]


def variant_value(rows: list[dict[str, str]], variant: str, field: str) -> str:
    for row in rows:
        if row.get("variant") == variant:
            return row.get(field, "")
    return ""


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise ValueError(f"{path} must contain exactly one data row; found {len(rows)}")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# WRR Lock Options",
        "",
        "Status: decision aid, not a WRR reproduction.",
        "",
        "This report does not lock disputed WRR method choices. It separates",
        "current source-backed options from diagnostic shortcuts so the next",
        "run can proceed without silently promoting an open decision.",
        "",
        "## Options",
        "",
        "| Area | Option | Status | Evidence | Recommendation | Claim boundary |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                markdown_cell(row[field])
                for field in (
                    "area",
                    "option",
                    "status",
                    "evidence",
                    "recommendation",
                    "claim_boundary",
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Current No-Input Path",
            "",
            "Proceed with the broad imported same-record WRR2 pair input, keep the",
            "printed formula as the source-facing default, carry the reported-program",
            "formula as a sensitivity variant, and treat the WNP-excluded 999,999",
            "date-label permutation as diagnostic evidence only.",
            "",
            "Claim-grade language still requires a source-locked pair universe, a",
            "source-locked `D(w)` formula decision, full corrected distances over that",
            "locked universe, and a locked aggregate/permutation procedure.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_lock_options",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "pair_summary": str(args.pair_summary),
            "skip_summary": str(args.skip_summary),
            "variants": str(args.variants),
            "recommended_permutation": str(args.recommended_permutation),
        },
        "outputs": {
            "out": str(args.out),
            "markdown_out": str(args.markdown_out),
        },
        "rows": len(rows),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
