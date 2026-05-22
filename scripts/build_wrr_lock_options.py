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
DEFAULT_SOURCE_REVIEW_SUMMARY = Path("reports/wrr_1994/wrr_source_review_queue_summary.csv")
DEFAULT_SOURCE_POLICY_SCENARIOS = Path("reports/wrr_1994/wrr_source_policy_scenarios.csv")
DEFAULT_SOURCE_POLICY_TERM_IMPACTS = Path(
    "reports/wrr_1994/wrr_source_policy_term_impacts.csv"
)
DEFAULT_DIRECT_ALL_LANES_250_SUMMARY = Path(
    "reports/wrr_1994/direct_all/wrr2_corrected_distance_all_lanes_250_summary.csv"
)
DEFAULT_DIRECT_ALL_LANES_1000_SUMMARY = Path(
    "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged_summary.csv"
)
DEFAULT_DIRECT_ALL_LANES_1000_PROGRAM_SUMMARY = Path(
    "reports/wrr_1994/direct_all/highcap_1000_program/wrr2_corrected_distance_all_lanes_merged_summary.csv"
)
DEFAULT_DIRECT_ALL_LANES_1000 = Path(
    "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged.csv"
)
DEFAULT_DIRECT_ALL_LANES_1000_PROGRAM = Path(
    "reports/wrr_1994/direct_all/highcap_1000_program/wrr2_corrected_distance_all_lanes_merged.csv"
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
    source_review_summary = read_optional_rows(args.source_review_summary)
    source_policy_scenarios = read_optional_rows(args.source_policy_scenarios)
    source_policy_term_impacts = read_optional_rows(args.source_policy_term_impacts)
    direct_all_lanes_250 = read_optional_one_row(args.direct_all_lanes_250_summary)
    direct_all_lanes_1000 = read_optional_one_row(args.direct_all_lanes_1000_summary)
    direct_all_lanes_1000_program = read_optional_one_row(
        args.direct_all_lanes_1000_program_summary
    )
    direct_all_lanes_program_changed_pairs = compare_corrected_distance_changes(
        args.direct_all_lanes_1000,
        args.direct_all_lanes_1000_program,
    )
    rows = build_option_rows(
        pair_row,
        skip_row,
        variant_rows,
        permutation_row,
        source_review_summary=source_review_summary,
        source_policy_scenarios=source_policy_scenarios,
        source_policy_term_impacts=source_policy_term_impacts,
        direct_all_lanes_250=direct_all_lanes_250,
        direct_all_lanes_1000=direct_all_lanes_1000,
        direct_all_lanes_1000_program=direct_all_lanes_1000_program,
        direct_all_lanes_program_changed_pairs=direct_all_lanes_program_changed_pairs,
    )
    write_csv(args.out, rows)
    write_markdown(
        args.markdown_out,
        rows,
        direct_all_lanes_program_changed_pairs=direct_all_lanes_program_changed_pairs,
    )
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
    parser.add_argument("--source-review-summary", type=Path, default=DEFAULT_SOURCE_REVIEW_SUMMARY)
    parser.add_argument("--source-policy-scenarios", type=Path, default=DEFAULT_SOURCE_POLICY_SCENARIOS)
    parser.add_argument(
        "--source-policy-term-impacts",
        type=Path,
        default=DEFAULT_SOURCE_POLICY_TERM_IMPACTS,
    )
    parser.add_argument(
        "--direct-all-lanes-250-summary",
        type=Path,
        default=DEFAULT_DIRECT_ALL_LANES_250_SUMMARY,
    )
    parser.add_argument(
        "--direct-all-lanes-1000-summary",
        type=Path,
        default=DEFAULT_DIRECT_ALL_LANES_1000_SUMMARY,
    )
    parser.add_argument(
        "--direct-all-lanes-1000-program-summary",
        type=Path,
        default=DEFAULT_DIRECT_ALL_LANES_1000_PROGRAM_SUMMARY,
    )
    parser.add_argument(
        "--direct-all-lanes-1000",
        type=Path,
        default=DEFAULT_DIRECT_ALL_LANES_1000,
    )
    parser.add_argument(
        "--direct-all-lanes-1000-program",
        type=Path,
        default=DEFAULT_DIRECT_ALL_LANES_1000_PROGRAM,
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_option_rows(
    pair_row: dict[str, str],
    skip_row: dict[str, str],
    variant_rows: list[dict[str, str]],
    permutation_row: dict[str, str],
    *,
    source_review_summary: list[dict[str, str]] | None = None,
    source_policy_scenarios: list[dict[str, str]] | None = None,
    source_policy_term_impacts: list[dict[str, str]] | None = None,
    direct_all_lanes_250: dict[str, str] | None = None,
    direct_all_lanes_1000: dict[str, str] | None = None,
    direct_all_lanes_1000_program: dict[str, str] | None = None,
    direct_all_lanes_program_changed_pairs: int | None = None,
) -> list[dict[str, str]]:
    imported_pairs = pair_row.get("imported_same_record_pairs", "")
    appellation_min_pairs = pair_row.get("appellation_min_length_same_record_pairs", "")
    one_zacut_pairs = pair_row.get("appellation_min_length_pairs_after_one_zacut_appellation_excluded", "")
    expected_pairs = pair_row.get("expected_published_pairs", "")
    length_filtered_pairs = pair_row.get("length_filtered_same_record_pairs", "")
    wnp_delta = pair_row.get("wnp_disputed_zacut_appellation_min_length_pair_delta", "")
    source_review_flag_text = source_review_flag_evidence(source_review_summary or [])
    source_policy_scenario_text = source_policy_scenario_evidence(
        source_policy_scenarios or []
    )
    source_policy_term_impact_text = source_policy_term_impact_evidence(
        source_policy_term_impacts or []
    )
    if source_policy_term_impact_text:
        source_policy_scenario_text = (
            f"{source_policy_scenario_text} {source_policy_term_impact_text}"
        )
    printed_defined = variant_value(variant_rows, "term_printed", "defined_corrected_distances")
    program_defined = variant_value(variant_rows, "term_program", "defined_corrected_distances")
    fixed_defined = variant_value(variant_rows, "fixed_250", "defined_corrected_distances")
    all_lane_250_defined = optional_value(direct_all_lanes_250, "defined_corrected_distances")
    all_lane_1000_defined = optional_value(direct_all_lanes_1000, "defined_corrected_distances")
    all_lane_program_defined = optional_value(
        direct_all_lanes_1000_program, "defined_corrected_distances"
    )
    defined_distance_evidence = (
        f"The cited {expected_pairs} is best treated as a corrected-distance output count, "
        "not a raw table count."
    )
    defined_distance_recommendation = (
        "Next no-input path: compute corrected distances over the broad working input "
        "and report the defined set."
    )
    if all_lane_250_defined and all_lane_1000_defined:
        defined_distance_evidence = (
            f"{defined_distance_evidence} Broad all-lane diagnostics now define "
            f"{all_lane_250_defined} distances at cap 250 and {all_lane_1000_defined} at cap 1000."
        )
        defined_distance_recommendation = (
            "Use the defined set as diagnostic pressure only; it still does not reproduce "
            f"the source-cited {expected_pairs} distances."
        )
    program_evidence = (
        f"{skip_row.get('program_cap_lt_printed', '')} program caps below printed; "
        f"{skip_row.get('program_cap_eq_printed', '')} equal; "
        f"defined smoke rows printed/program/fixed250 = {printed_defined}/{program_defined}/{fixed_defined}."
    )
    if all_lane_program_defined and direct_all_lanes_program_changed_pairs is not None:
        program_evidence = (
            f"{program_evidence} All-lane cap-1000 program formula defines "
            f"{all_lane_program_defined} rows and changes {direct_all_lanes_program_changed_pairs} "
            "pair rows versus printed."
        )
    return [
        {
            "area": "Pair universe",
            "option": "all imported WRR2 same-record pairs",
            "status": "selected_working_source_policy",
            "evidence": (
                f"{imported_pairs} imported same-record pairs; source-cited second-list "
                f"defined distances = {expected_pairs}; raw imported count does not equal the cited distance count."
            ),
            "recommendation": (
                "Use as the broad working input under keep_all_working_source; do not apply WNP/context or visual-review exclusions automatically."
            ),
            "claim_boundary": "source policy locked; full local corrected-distance run available",
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
            "option": "WNP/context flagged source-review queue",
            "status": "diagnostic_source_review_context",
            "evidence": source_review_flag_text,
            "recommendation": (
                "Use these flags to prioritize source-lock review; do not change "
                "the pair universe automatically."
            ),
            "claim_boundary": "diagnostic only",
        },
        {
            "area": "Pair universe",
            "option": "source-policy scenario impact",
            "status": "policy_selected_keep_all_working_source",
            "evidence": source_policy_scenario_text,
            "recommendation": (
                "Treat keep_all_working_source as the working source policy; keep exclusion scenarios as diagnostics only."
            ),
            "claim_boundary": "working source policy selected",
        },
        {
            "area": "Pair universe",
            "option": "defined-distance output interpretation",
            "status": "recommended_working_interpretation",
            "evidence": defined_distance_evidence,
            "recommendation": defined_distance_recommendation,
            "claim_boundary": "full local run available; exact WRR reproduction still blocked",
        },
        {
            "area": "D(w) skip-cap formula",
            "option": "printed WRR formula",
            "status": "source_locked_primary_formula",
            "evidence": (
                f"{skip_row.get('rows', '')} skip-cap rows; printed formula currently selected in the audit; "
                f"{skip_row.get('target_unreached_rows', '')} rows do not reach the expected-hit target."
            ),
            "recommendation": "Use as the main source-facing D(w) formula because it is the printed WRR formula.",
            "claim_boundary": "formula locked; full local corrected-distance run available",
        },
        {
            "area": "D(w) skip-cap formula",
            "option": "reported WRR-program formula",
            "status": "required_sensitivity_variant",
            "evidence": program_evidence,
            "recommendation": (
                "Carry as a required sensitivity run because MBBK reports the WRR programs used this formula."
            ),
            "claim_boundary": "sensitivity only",
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


def source_review_flag_evidence(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "No source-review queue summary was available."
    counts: dict[str, int] = {}
    for row in rows:
        for count, flag in parse_flag_counts(row.get("source_review_flags", "")):
            counts[flag] = counts.get(flag, 0) + count
    if not counts:
        return "Source-review queue has no WNP/context flags in the current run."
    total = sum(counts.values())
    parts = ", ".join(f"{counts[flag]} {flag}" for flag in sorted(counts))
    return f"Source-review queue flags {total} WNP/context queued terms: {parts}."


def source_policy_scenario_evidence(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "No source-policy scenario summary was available."
    parts = [
        scenario_evidence(rows, "keep_all_working_source", "baseline"),
        scenario_evidence(rows, "exclude_wnp_zacut_only", "exclude WNP Zacut"),
        scenario_evidence(rows, "exclude_all_source_review_flags", "exclude all flags"),
    ]
    scenario_parts = [part for part in parts if part]
    if not scenario_parts:
        return "Source-policy scenario summary has no recognized scenario rows."
    return "; ".join(scenario_parts) + "; source policy selected: keep_all_working_source."


def source_policy_term_impact_evidence(rows: list[dict[str, str]]) -> str:
    closing_rows = [
        row
        for row in rows
        if row.get("closes_appellation_min_length_gap_to_163", "").lower() == "true"
    ]
    if not closing_rows:
        return ""
    first = closing_rows[0]
    examples = ", ".join(row.get("term", "") for row in closing_rows[:4] if row.get("term"))
    examples_text = f"; examples {examples}" if examples else ""
    return (
        "Single-term impact: "
        f"{len(closing_rows)} term(s) individually leave "
        f"{first.get('remaining_appellation_min_length_pairs_if_excluded', '')} >=5 pairs "
        f"(gap {first.get('gap_to_source_cited_163_after_appellation_min_length_if_excluded', '')})"
        f"{examples_text}; diagnostic only."
    )


def scenario_evidence(rows: list[dict[str, str]], scenario: str, label: str) -> str:
    row = next((item for item in rows if item.get("scenario") == scenario), None)
    if not row:
        return ""
    return (
        f"{label}: {row.get('remaining_appellation_min_length_pairs', '')} >=5 pairs "
        f"(gap {row.get('gap_to_source_cited_163_after_appellation_min_length', '')}), "
        f"{row.get('remaining_length_filtered_pairs', '')} in 5..8 lane"
    )


def parse_flag_counts(value: str) -> list[tuple[int, str]]:
    out = []
    for part in value.split(","):
        chunk = part.strip()
        if not chunk:
            continue
        count_text, _, flag = chunk.partition(" ")
        if not flag:
            continue
        try:
            out.append((int(count_text), flag.strip()))
        except ValueError:
            continue
    return out


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_optional_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_rows(path)


def read_one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise ValueError(f"{path} must contain exactly one data row; found {len(rows)}")
    return rows[0]


def read_optional_one_row(path: Path) -> dict[str, str] | None:
    if not path.exists():
        return None
    return read_one_row(path)


def optional_value(row: dict[str, str] | None, field: str) -> str:
    if not row:
        return ""
    return row.get(field, "")


def compare_corrected_distance_changes(left: Path, right: Path) -> int | None:
    if not left.exists() or not right.exists():
        return None
    left_rows = keyed_corrected_distance_rows(left)
    right_rows = keyed_corrected_distance_rows(right)
    pair_ids = set(left_rows) | set(right_rows)
    return sum(1 for pair_id in pair_ids if left_rows.get(pair_id) != right_rows.get(pair_id))


def keyed_corrected_distance_rows(path: Path) -> dict[str, tuple[str, str, str]]:
    rows = {}
    for row in read_rows(path):
        rows[row.get("pair_id", "")] = (
            row.get("corrected_distance", ""),
            row.get("corrected_distance_status", ""),
            row.get("pair_valid_perturbations", ""),
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    *,
    direct_all_lanes_program_changed_pairs: int | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# WRR Lock Options",
        "",
        "Status: decision aid, not a WRR reproduction.",
        "",
        "This report records the selected working locks and keeps diagnostic",
        "alternatives separate so later runs do not silently promote review flags",
        "or sensitivity variants into source policy.",
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
    lines.extend(["", "## Current No-Input Path", ""])
    lines.extend(
        [
            "Proceeding no-input work has now wired the broad imported same-record",
            "WRR2 pair input as keep_all_working_source, kept the printed formula",
            "as the source-facing main D(w),",
            "carried the reported-program formula as a sensitivity variant, and",
            "treated the WNP-excluded 999,999 date-label permutation as diagnostic",
            "evidence only.",
            "",
        ]
    )
    if direct_all_lanes_program_changed_pairs is not None:
        lines.extend(
            [
                "Current broad-input result: the all-lane cap-1000 program-formula",
                "sensitivity run changes "
                f"{direct_all_lanes_program_changed_pairs} pair rows versus the printed-formula run.",
                "This lowers the current diagnostic risk from the printed-vs-program",
                "formula choice while preserving the program formula as sensitivity output.",
                "",
            ]
        )
    lines.extend(
        [
            "Recommended no-input working posture:",
            "",
            "- Broad same-record WRR2 rows are the selected working source policy.",
            "- No source-review flag or visual-review note excludes a pair automatically.",
            "- Printed `D(w)` is the main source-facing rule; reported-program `D(w)` remains sensitivity output.",
            "- Date-label permutation output remains diagnostic until corrected distances and the aggregate rule are source-locked.",
            "",
            "Claim-grade language still requires a locked aggregate/permutation",
            "procedure over the full selected-universe corrected-distance output.",
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
            "source_review_summary": str(args.source_review_summary),
            "source_policy_scenarios": str(args.source_policy_scenarios),
            "source_policy_term_impacts": str(args.source_policy_term_impacts),
            "direct_all_lanes_250_summary": str(args.direct_all_lanes_250_summary),
            "direct_all_lanes_1000_summary": str(args.direct_all_lanes_1000_summary),
            "direct_all_lanes_1000_program_summary": str(
                args.direct_all_lanes_1000_program_summary
            ),
            "direct_all_lanes_1000": str(args.direct_all_lanes_1000),
            "direct_all_lanes_1000_program": str(args.direct_all_lanes_1000_program),
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
