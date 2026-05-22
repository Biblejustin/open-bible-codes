#!/usr/bin/env python3
"""Build a WRR claim-blocker packet from current readiness artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_READINESS = Path("reports/wrr_1994/wrr_claim_readiness.csv")
DEFAULT_LOCK_OPTIONS = Path("reports/wrr_1994/wrr_lock_options.csv")
DEFAULT_SOURCE_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_METHOD_STATUS = Path("reports/wrr_1994/wrr_method_status.csv")
DEFAULT_SOURCE_POLICY_SCENARIOS = Path("reports/wrr_1994/wrr_source_policy_scenarios.csv")
DEFAULT_SOURCE_POLICY_TERM_IMPACTS = Path(
    "reports/wrr_1994/wrr_source_policy_term_impacts.csv"
)
DEFAULT_DW_FORMULA_SENSITIVITY = Path("reports/wrr_1994/wrr_dw_formula_sensitivity.csv")
DEFAULT_VARIANT_RESIDUAL_SUMMARY = Path(
    "reports/wrr_1994/wrr_variant_residual_review_summary.csv"
)
DEFAULT_VARIANT_RESIDUAL_PACKET = Path(
    "reports/wrr_1994/wrr_variant_residual_review_packet.csv"
)
DEFAULT_RESIDUAL_TERM_SUMMARY = Path(
    "reports/wrr_1994/wrr_residual_term_reconciliation_summary.csv"
)
DEFAULT_RESIDUAL_TERM_QUEUE = Path(
    "reports/wrr_1994/wrr_residual_term_reconciliation_queue.csv"
)
DEFAULT_METHOD_PAIR_UNIVERSE_SUMMARY = Path(
    "reports/wrr_1994/wrr_method_pair_universe_evidence_summary.csv"
)
DEFAULT_SOURCE_TRANSCRIPTION_ROW_SUMMARY = Path(
    "reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv"
)
DEFAULT_REMAINING_LANE_SUMMARY = Path(
    "reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv"
)
DEFAULT_REMAINING_LANE_PACKET = Path(
    "reports/wrr_1994/wrr_remaining_lane_evidence_packet.csv"
)
DEFAULT_OUT = Path("reports/wrr_1994/wrr_claim_blocker_packet.csv")
DEFAULT_MD = Path("docs/WRR_CLAIM_BLOCKER_PACKET.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_claim_blocker_packet.manifest.json")

FIELDNAMES = [
    "decision_area",
    "current_status",
    "ready",
    "blocker",
    "current_read",
    "available_options",
    "source_review_flags",
    "no_input_next",
    "input_needed",
]


INPUT_NEEDED = {
    "Pair universe": "source policy selected: keep_all_working_source",
    "D(w) skip-cap formula": "formula selected: printed WRR formula main; program sensitivity",
    "Corrected distance c(w,w')": "run full corrected-distance over keep_all_working_source with printed D(w)",
    "Aggregate statistic and permutation": "lock aggregate/permutation procedure over full corrected-distance output",
}

NO_INPUT_NEXT = {
    "Pair universe": (
        "continue with all imported same-record pairs; source-review and visual "
        "flags remain review notes only"
    ),
    "D(w) skip-cap formula": (
        "use printed D(w) as the main formula and keep reported-program D(w) "
        "visible as sensitivity"
    ),
    "Corrected distance c(w,w')": (
        "run full-lane corrected-distance work under the selected source and D(w) locks"
    ),
    "Aggregate statistic and permutation": (
        "report locked local aggregate/permutation evidence with exact-WRR caveats"
    ),
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    readiness_rows = read_rows(args.readiness)
    lock_rows = read_rows(args.lock_options)
    source_rows = read_rows(args.source_queue)
    method_rows = read_rows(args.method_status)
    source_policy_rows = read_optional_rows(args.source_policy_scenarios)
    source_policy_term_rows = read_optional_rows(args.source_policy_term_impacts)
    dw_formula_rows = read_optional_rows(args.dw_formula_sensitivity)
    variant_residual_rows = read_optional_rows(args.variant_residual_summary)
    variant_residual_packet_rows = read_optional_rows(args.variant_residual_packet)
    residual_term_summary_rows = read_optional_rows(args.residual_term_summary)
    residual_term_queue_rows = read_optional_rows(args.residual_term_queue)
    method_pair_universe_rows = read_optional_rows(args.method_pair_universe_summary)
    source_transcription_rows = read_optional_rows(args.source_transcription_row_summary)
    remaining_lane_summary_rows = read_optional_rows(args.remaining_lane_summary)
    remaining_lane_packet_rows = read_optional_rows(args.remaining_lane_packet)
    packet_rows = build_packet_rows(readiness_rows, lock_rows, source_rows, method_rows)
    write_csv(args.out, packet_rows)
    write_markdown(
        args.markdown_out,
        packet_rows,
        source_rows,
        source_policy_rows,
        source_policy_term_rows,
        dw_formula_rows,
        variant_residual_rows,
        variant_residual_packet_rows,
        residual_term_summary_rows,
        residual_term_queue_rows,
        method_pair_universe_rows,
        source_transcription_rows,
        remaining_lane_summary_rows,
        remaining_lane_packet_rows,
        args,
    )
    write_manifest(
        args.manifest_out,
        args,
        packet_rows,
        source_policy_rows,
        source_policy_term_rows,
        dw_formula_rows,
        variant_residual_rows,
        variant_residual_packet_rows,
        residual_term_summary_rows,
        residual_term_queue_rows,
        method_pair_universe_rows,
        source_transcription_rows,
        remaining_lane_summary_rows,
        remaining_lane_packet_rows,
        started,
    )
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readiness", type=Path, default=DEFAULT_READINESS)
    parser.add_argument("--lock-options", type=Path, default=DEFAULT_LOCK_OPTIONS)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument("--method-status", type=Path, default=DEFAULT_METHOD_STATUS)
    parser.add_argument(
        "--source-policy-scenarios",
        type=Path,
        default=DEFAULT_SOURCE_POLICY_SCENARIOS,
    )
    parser.add_argument(
        "--source-policy-term-impacts",
        type=Path,
        default=DEFAULT_SOURCE_POLICY_TERM_IMPACTS,
    )
    parser.add_argument(
        "--dw-formula-sensitivity",
        type=Path,
        default=DEFAULT_DW_FORMULA_SENSITIVITY,
    )
    parser.add_argument(
        "--variant-residual-summary",
        type=Path,
        default=DEFAULT_VARIANT_RESIDUAL_SUMMARY,
    )
    parser.add_argument(
        "--variant-residual-packet",
        type=Path,
        default=DEFAULT_VARIANT_RESIDUAL_PACKET,
    )
    parser.add_argument(
        "--residual-term-summary",
        type=Path,
        default=DEFAULT_RESIDUAL_TERM_SUMMARY,
    )
    parser.add_argument(
        "--residual-term-queue",
        type=Path,
        default=DEFAULT_RESIDUAL_TERM_QUEUE,
    )
    parser.add_argument(
        "--method-pair-universe-summary",
        type=Path,
        default=DEFAULT_METHOD_PAIR_UNIVERSE_SUMMARY,
    )
    parser.add_argument(
        "--source-transcription-row-summary",
        type=Path,
        default=DEFAULT_SOURCE_TRANSCRIPTION_ROW_SUMMARY,
    )
    parser.add_argument(
        "--remaining-lane-summary",
        type=Path,
        default=DEFAULT_REMAINING_LANE_SUMMARY,
    )
    parser.add_argument(
        "--remaining-lane-packet",
        type=Path,
        default=DEFAULT_REMAINING_LANE_PACKET,
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_packet_rows(
    readiness_rows: list[dict[str, str]],
    lock_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    method_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    options_by_area = group_lock_options(lock_rows)
    method_by_area = {row.get("decision_area", ""): row for row in method_rows}
    source_flags = source_flag_summary(source_rows)
    out = []
    for row in readiness_rows:
        area = row.get("decision_area", "")
        if row.get("ready", "") == "true":
            continue
        out.append(
            {
                "decision_area": area,
                "current_status": row.get("status", ""),
                "ready": row.get("ready", ""),
                "blocker": row.get("blocker", ""),
                "current_read": method_by_area.get(area, {}).get("current_read", ""),
                "available_options": options_by_area.get(area, ""),
                "source_review_flags": source_flags if area == "Pair universe" else "",
                "no_input_next": NO_INPUT_NEXT.get(area, ""),
                "input_needed": INPUT_NEEDED.get(area, ""),
            }
        )
    return out


def group_lock_options(rows: list[dict[str, str]]) -> dict[str, str]:
    grouped: dict[str, list[str]] = {}
    for row in rows:
        area = row.get("area", "")
        if not area:
            continue
        grouped.setdefault(area, []).append(
            f"{row.get('option', '')} [{row.get('status', '')}]"
        )
    return {area: "; ".join(options) for area, options in grouped.items()}


def source_flag_summary(rows: list[dict[str, str]]) -> str:
    counter = Counter(
        flag
        for row in rows
        for flag in row.get("source_review_flags", "").split(";")
        if flag
    )
    if not counter:
        return ""
    total = sum(counter.values())
    parts = ", ".join(f"{counter[flag]} {flag}" for flag in sorted(counter))
    return f"{total} flagged queued terms: {parts}"


def flagged_source_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    flagged = [row for row in rows if row.get("source_review_flags")]
    return sorted(flagged, key=lambda row: int_or_zero(row.get("priority_rank", "")))


def visual_source_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    visual = [row for row in rows if row.get("visual_review_note")]
    return sorted(visual, key=lambda row: int_or_zero(row.get("priority_rank", "")))


def residual_summary_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    wanted = {
        "residual_pool",
        "review_frontier",
        "impact_status",
        "row_ocr_pair_status",
        "frontier_impact_status",
        "frontier_row_ocr_pair_status",
        "unresolved_term_side",
        "unresolved_term_bucket",
        "unresolved_source_flag",
    }
    return [row for row in rows if row.get("group") in wanted]


def residual_frontier_rows(rows: list[dict[str, str]], limit: int = 10) -> list[dict[str, str]]:
    frontier = [
        row
        for row in rows
        if row.get("within_minimum_residual_frontier", "").lower() == "true"
    ]
    return sorted(frontier, key=lambda row: int_or_zero(row.get("review_rank", "")))[:limit]


def residual_term_summary_display_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    wanted = {
        "residual_terms",
        "term_side",
        "review_bucket",
        "term_ocr_status",
        "source_flag",
        "reconciliation_need",
    }
    return [row for row in rows if row.get("group") in wanted]


def top_residual_term_rows(rows: list[dict[str, str]], limit: int = 10) -> list[dict[str, str]]:
    return sorted(rows, key=lambda row: int_or_zero(row.get("priority_rank", "")))[:limit]


def top_source_transcription_rows(
    rows: list[dict[str, str]], limit: int = 5
) -> list[dict[str, str]]:
    return sorted(rows, key=lambda row: int_or_zero(row.get("row_rank", "")))[:limit]


def page_image_near_match_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    filtered = [
        row for row in rows if row.get("action_lane") == "page_image_near_match_review"
    ]
    return sorted(filtered, key=lambda row: int_or_zero(row.get("evidence_rank", "")))


def page_image_summary_row(rows: list[dict[str, str]]) -> dict[str, str]:
    for row in rows:
        if row.get("action_lane") == "page_image_near_match_review":
            return row
    return {}


def write_markdown(
    path: Path,
    packet_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    source_policy_rows: list[dict[str, str]],
    source_policy_term_rows: list[dict[str, str]],
    dw_formula_rows: list[dict[str, str]],
    variant_residual_rows: list[dict[str, str]],
    variant_residual_packet_rows: list[dict[str, str]],
    residual_term_summary_rows: list[dict[str, str]],
    residual_term_queue_rows: list[dict[str, str]],
    method_pair_universe_rows: list[dict[str, str]],
    source_transcription_rows: list[dict[str, str]],
    remaining_lane_summary_rows: list[dict[str, str]],
    remaining_lane_packet_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    status_line = (
        "Status: no current claim-readiness blockers under selected local WRR lock policy."
        if not packet_rows
        else "Status: current claim-readiness blockers remain."
    )
    lines = [
        "# WRR Claim Blocker Packet",
        "",
        status_line,
        "",
        "This packet records the selected WRR working policy and gathers the",
        "remaining claim-readiness blockers, current lock options, WNP/context source",
        "queue flags, and visual triage notes into one handoff artifact.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_claim_blocker_packet "
            f"--readiness {args.readiness} "
            f"--lock-options {args.lock_options} "
            f"--source-queue {args.source_queue} "
            f"--method-status {args.method_status} "
            f"--source-policy-scenarios {args.source_policy_scenarios} "
            f"--source-policy-term-impacts {args.source_policy_term_impacts} "
            f"--dw-formula-sensitivity {args.dw_formula_sensitivity} "
            f"--variant-residual-summary {args.variant_residual_summary} "
            f"--variant-residual-packet {args.variant_residual_packet} "
            f"--residual-term-summary {args.residual_term_summary} "
            f"--residual-term-queue {args.residual_term_queue} "
            f"--method-pair-universe-summary {args.method_pair_universe_summary} "
            f"--source-transcription-row-summary {args.source_transcription_row_summary} "
            f"--remaining-lane-summary {args.remaining_lane_summary} "
            f"--remaining-lane-packet {args.remaining_lane_packet} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Blockers",
        "",
        "| Area | Status | Blocker | Input needed |",
        "| --- | --- | --- | --- |",
    ]
    if packet_rows:
        for row in packet_rows:
            lines.append(
                "| {area} | `{status}` | {blocker} | {input_needed} |".format(
                    area=markdown_cell(row["decision_area"]),
                    status=markdown_cell(row["current_status"]),
                    blocker=markdown_cell(row["blocker"]),
                    input_needed=markdown_cell(row["input_needed"]),
                )
            )
    else:
        lines.append(
            "| None | `ready` | Current method-status rows satisfy the claim-readiness gate. | none |"
        )
    lines.extend(
        [
            "",
            "## No-Input Boundary",
            "",
            "| Area | Current read | Available options | No-input next |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in packet_rows:
        lines.append(
            "| {area} | {current_read} | {options} | {no_input_next} |".format(
                area=markdown_cell(row["decision_area"]),
                current_read=markdown_cell(row["current_read"]),
                options=markdown_cell(row["available_options"]),
                no_input_next=markdown_cell(row["no_input_next"]),
            )
        )
    if not packet_rows:
        lines.append(
            "| None | All required areas are ready under the selected local lock policy. |  | continue reporting exact-WRR caveats explicitly |"
        )
    residual_rows = residual_summary_rows(variant_residual_rows)
    if residual_rows:
        lines.extend(
            [
                "",
                "## Exact-WRR Residual Caveat",
                "",
                "The local lock policy is claim-ready for repo-defined reporting, but exact published WRR reproduction still has a residual source/method gap after the generous simple-variant upper bound.",
                "",
                "| Group | Value | Pairs | Read |",
                "| --- | --- | ---: | --- |",
            ]
        )
        for row in residual_rows:
            lines.append(
                "| `{group}` | `{value}` | {pairs} | {read} |".format(
                    group=markdown_cell(row.get("group", "")),
                    value=markdown_cell(row.get("value", "")),
                    pairs=markdown_cell(row.get("pairs", "")),
                    read=markdown_cell(row.get("read", "")),
                )
            )
    frontier_rows = residual_frontier_rows(variant_residual_packet_rows)
    if frontier_rows:
        lines.extend(
            [
                "",
                "### Residual Frontier Sample",
                "",
                "| Rank | Pair | Concept | Impact | Row OCR | Unresolved terms | Flags |",
                "| ---: | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in frontier_rows:
            lines.append(
                (
                    "| {rank} | `{pair}` | `{concept}` | `{impact}` | `{ocr}` | "
                    "`{terms}` | {flags} |"
                ).format(
                    rank=markdown_cell(row.get("review_rank", "")),
                    pair=markdown_cell(row.get("pair_id", "")),
                    concept=markdown_cell(row.get("concept", "")),
                    impact=markdown_cell(row.get("impact_status", "")),
                    ocr=markdown_cell(row.get("row_ocr_pair_status", "")),
                    terms=markdown_cell(row.get("unresolved_terms", "")),
                    flags=markdown_code_or_blank(row.get("unresolved_source_flags", "")),
                )
            )
    term_summary_rows = residual_term_summary_display_rows(residual_term_summary_rows)
    if term_summary_rows:
        lines.extend(
            [
                "",
                "### Residual Term Queue",
                "",
                "The queue compresses repeated residual pair blockers into unique unresolved terms. It is a diagnostic review order, not a correction set or exclusion policy.",
                "",
                "| Group | Value | Terms | Residual pairs | Frontier pairs | Read |",
                "| --- | --- | ---: | ---: | ---: | --- |",
            ]
        )
        for row in term_summary_rows:
            lines.append(
                "| `{group}` | `{value}` | {terms} | {residual_pairs} | {frontier_pairs} | {read} |".format(
                    group=markdown_cell(row.get("group", "")),
                    value=markdown_cell(row.get("value", "")),
                    terms=markdown_cell(row.get("terms", "")),
                    residual_pairs=markdown_cell(row.get("residual_pairs", "")),
                    frontier_pairs=markdown_cell(row.get("frontier_pairs", "")),
                    read=markdown_cell(row.get("read", "")),
                )
            )
    top_term_rows = top_residual_term_rows(residual_term_queue_rows)
    if top_term_rows:
        lines.extend(
            [
                "",
                "### Top Residual Term Targets",
                "",
                "| Rank | Term id | Term | Need | Pairs | Frontier | Buckets | Source flags |",
                "| ---: | --- | --- | --- | ---: | ---: | --- | --- |",
            ]
        )
        for row in top_term_rows:
            lines.append(
                (
                    "| {rank} | `{term_id}` | `{term}` | `{need}` | {pairs} | "
                    "{frontier} | `{buckets}` | {flags} |"
                ).format(
                    rank=markdown_cell(row.get("priority_rank", "")),
                    term_id=markdown_cell(row.get("term_id", "")),
                    term=markdown_cell(row.get("term", "")),
                    need=markdown_cell(row.get("reconciliation_need", "")),
                    pairs=markdown_cell(row.get("residual_pairs", "")),
                    frontier=markdown_cell(row.get("frontier_pairs", "")),
                    buckets=markdown_cell(row.get("review_buckets", "")),
                    flags=markdown_code_or_blank(row.get("source_flags", "")),
                )
            )
    if source_transcription_rows:
        action_terms = sum_int(
            row.get("action_terms", "") for row in source_transcription_rows
        )
        residual_pairs = sum_int(
            row.get("residual_pairs", "") for row in source_transcription_rows
        )
        frontier_pairs = sum_int(
            row.get("frontier_pairs", "") for row in source_transcription_rows
        )
        top_rows = top_source_transcription_rows(source_transcription_rows)
        top_row = top_rows[0] if top_rows else {}
        lines.extend(
            [
                "",
                "### Source-Transcription Row Evidence Summary",
                "",
                "| Row clusters | Action terms | Residual pairs | Frontier pairs | Top row | Read |",
                "| ---: | ---: | ---: | ---: | --- | --- |",
                (
                    "| {clusters} | {terms} | {pairs} | {frontier} | `{top}` | "
                    "review multi-term rows once by row before term edits |"
                ).format(
                    clusters=markdown_cell(len(source_transcription_rows)),
                    terms=markdown_cell(action_terms),
                    pairs=markdown_cell(residual_pairs),
                    frontier=markdown_cell(frontier_pairs),
                    top=markdown_cell(top_row.get("row_number", "")),
                ),
                "",
                "### Source-Transcription Priority Rows",
                "",
                "| Rank | Row | Concept | Terms | Pairs | Frontier | Action terms not matched |",
                "| ---: | --- | --- | ---: | ---: | ---: | --- |",
            ]
        )
        for row in top_rows:
            lines.append(
                (
                    "| {rank} | `{row_number}` | `{concept}` | {terms} | "
                    "{pairs} | {frontier} | {not_matched} |"
                ).format(
                    rank=markdown_cell(row.get("row_rank", "")),
                    row_number=markdown_cell(row.get("row_number", "")),
                    concept=markdown_cell(row.get("concept", "")),
                    terms=markdown_cell(row.get("action_terms", "")),
                    pairs=markdown_cell(row.get("residual_pairs", "")),
                    frontier=markdown_cell(row.get("frontier_pairs", "")),
                    not_matched=markdown_cell(
                        row.get("row_action_not_matched_terms", "")
                    ),
                )
            )
    near_match_summary = page_image_summary_row(remaining_lane_summary_rows)
    near_match_rows = page_image_near_match_rows(remaining_lane_packet_rows)
    if near_match_summary:
        lines.extend(
            [
                "",
                "### Page-Image Near-Match Evidence Summary",
                "",
                "| Terms | Residual pairs | Frontier pairs | Concepts | Read |",
                "| ---: | ---: | ---: | ---: | --- |",
                "| {terms} | {pairs} | {frontier} | {concepts} | {read} |".format(
                    terms=markdown_cell(near_match_summary.get("action_terms", "")),
                    pairs=markdown_cell(near_match_summary.get("residual_pairs", "")),
                    frontier=markdown_cell(near_match_summary.get("frontier_pairs", "")),
                    concepts=markdown_cell(near_match_summary.get("concepts", "")),
                    read=markdown_cell(near_match_summary.get("read", "")),
                ),
            ]
        )
    if near_match_rows:
        lines.extend(
            [
                "",
                "### Page-Image Near-Match Terms",
                "",
                "| Rank | Term id | Term | Row | Near match | Visual note |",
                "| ---: | --- | --- | --- | --- | --- |",
            ]
        )
        for row in near_match_rows:
            near_match = (
                f"d={row.get('row_ocr_near_match_distance', '')} "
                f"{row.get('row_ocr_near_match_text', '')}"
            )
            lines.append(
                "| {rank} | `{term_id}` | `{term}` | `{row_number}` | `{near}` | {note} |".format(
                    rank=markdown_cell(row.get("evidence_rank", "")),
                    term_id=markdown_cell(row.get("term_id", "")),
                    term=markdown_cell(row.get("term", "")),
                    row_number=markdown_cell(row.get("row_number", "")),
                    near=markdown_cell(near_match),
                    note=markdown_cell(row.get("visual_review_note", "")),
                )
            )
    if method_pair_universe_rows:
        summary = method_pair_universe_rows[0]
        lines.extend(
            [
                "",
                "### Method/Pair-Universe Evidence Summary",
                "",
                "| Terms | Pairs | OCR matched | Zero skip-250 | Zero high-cap | Both sides zero | Read |",
                "| ---: | ---: | ---: | ---: | ---: | ---: | --- |",
                (
                    "| {terms} | {pairs} | {ocr} | {zero_250} | {zero_highcap} | "
                    "{both_zero} | {read} |"
                ).format(
                    terms=markdown_cell(summary.get("action_terms", "")),
                    pairs=markdown_cell(summary.get("residual_pairs", "")),
                    ocr=markdown_cell(summary.get("ocr_matched_terms", "")),
                    zero_250=markdown_cell(summary.get("zero_base_skip_250_terms", "")),
                    zero_highcap=markdown_cell(
                        summary.get("zero_highcap_appellation_terms", "")
                    ),
                    both_zero=markdown_cell(
                        summary.get("both_sides_zero_highcap_pairs", "")
                    ),
                    read=markdown_cell(summary.get("read", "")),
                ),
            ]
        )
    if source_policy_rows:
        lines.extend(
            [
                "",
                "## Source Policy Scenario Impact",
                "",
                "| Scenario | Type | Excluded pairs | Remaining >=5 | Gap >=5 vs 163 | Remaining 5..8 |",
                "| --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in source_policy_rows:
            lines.append(
                (
                    "| {scenario} | `{policy_type}` | {excluded} | "
                    "{remaining_app} | {gap_app} | {remaining_len} |"
                ).format(
                    scenario=markdown_cell(row.get("scenario", "")),
                    policy_type=markdown_cell(row.get("policy_type", "")),
                    excluded=markdown_cell(row.get("excluded_pairs", "")),
                    remaining_app=markdown_cell(
                        row.get("remaining_appellation_min_length_pairs", "")
                    ),
                    gap_app=markdown_cell(
                        row.get("gap_to_source_cited_163_after_appellation_min_length", "")
                    ),
                    remaining_len=markdown_cell(row.get("remaining_length_filtered_pairs", "")),
                )
            )
    closing_term_rows = [
        row
        for row in source_policy_term_rows
        if row.get("closes_appellation_min_length_gap_to_163", "").lower() == "true"
    ]
    if closing_term_rows:
        lines.extend(
            [
                "",
                "## Single-Term Source Policy Impact",
                "",
                "| Term id | Term | Flags | Affected >=5 pairs | Remaining >=5 | Gap >=5 vs 163 | Read |",
                "| --- | --- | --- | ---: | ---: | ---: | --- |",
            ]
        )
        for row in closing_term_rows:
            lines.append(
                (
                    "| {term_id} | {term} | {flags} | {affected_app} | "
                    "{remaining_app} | {gap_app} | {read} |"
                ).format(
                    term_id=markdown_cell(row.get("term_id", "")),
                    term=markdown_cell(row.get("term", "")),
                    flags=markdown_cell(row.get("flags", "")),
                    affected_app=markdown_cell(
                        row.get("affected_appellation_min_length_pairs", "")
                    ),
                    remaining_app=markdown_cell(
                        row.get(
                            "remaining_appellation_min_length_pairs_if_excluded",
                            "",
                        )
                    ),
                    gap_app=markdown_cell(
                        row.get(
                            "gap_to_source_cited_163_after_appellation_min_length_if_excluded",
                            "",
                        )
                    ),
                    read=markdown_cell(row.get("diagnostic_read", "")),
                )
            )
    if dw_formula_rows:
        lines.extend(
            [
                "",
                "## D(w) Formula Sensitivity",
                "",
                "| Scope | Rows | Printed defined | Program defined | Changed pairs | Read |",
                "| --- | ---: | ---: | ---: | ---: | --- |",
            ]
        )
        for row in dw_formula_rows:
            lines.append(
                (
                    "| {scope} | {rows} | {printed} | "
                    "{program} | {changed} | {read} |"
                ).format(
                    scope=markdown_cell(row.get("scope", "")),
                    rows=markdown_cell(row.get("row_count", "")),
                    printed=markdown_cell(row.get("printed_defined_corrected_distances", "")),
                    program=markdown_cell(row.get("program_defined_corrected_distances", "")),
                    changed=markdown_cell(row.get("changed_pairs", "")),
                    read=markdown_cell(row.get("diagnostic_read", "")),
                )
            )
    flagged_rows = flagged_source_rows(source_rows)
    visual_rows = visual_source_rows(source_rows)
    if visual_rows:
        lines.extend(
            [
                "",
                "## Visual Triage Highlights",
                "",
                "| Rank | Term id | Note | Action |",
                "| ---: | --- | --- | --- |",
            ]
        )
        for row in visual_rows:
            lines.append(
                "| {rank} | `{term_id}` | {note} | {action} |".format(
                    rank=markdown_cell(row.get("priority_rank", "")),
                    term_id=markdown_cell(row.get("term_id", "")),
                    note=markdown_cell(row.get("visual_review_note", "")),
                    action=markdown_cell(row.get("visual_review_action", "")),
                )
            )
    if flagged_rows:
        lines.extend(
            [
                "",
                "## Flagged Source-Review Rows",
                "",
                "| Rank | Term id | Term | Bucket | Flags | Action |",
                "| ---: | --- | --- | --- | --- | --- |",
            ]
        )
        for row in flagged_rows:
            lines.append(
                "| {rank} | `{term_id}` | `{term}` | `{bucket}` | `{flags}` | {action} |".format(
                    rank=markdown_cell(row.get("priority_rank", "")),
                    term_id=markdown_cell(row.get("term_id", "")),
                    term=markdown_cell(row.get("term", "")),
                    bucket=markdown_cell(row.get("review_bucket", "")),
                    flags=markdown_cell(row.get("source_review_flags", "")),
                    action=markdown_cell(row.get("source_review_action", "")),
                )
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a decision packet, not a reproduction result.",
            "- Pair universe lock: keep_all_working_source; WNP/context and visual-review flags do not exclude pairs automatically.",
            "- Exact published WRR reproduction remains caveated by the residual source/method gap after the simple-variant upper bound.",
            "- Residual term priority is a review order, not a correction set or pair-exclusion list.",
            "- D(w) lock: printed WRR formula main; reported-program formula remains sensitivity output.",
            "- Aggregate/permutation lock: keep-all cap1000 999,999 date-label permutation over the full selected-universe corrected-distance output.",
            "- No visual-review note excludes a pair automatically; pair exclusion would require an explicit source-policy change.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_optional_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_rows(path)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    source_policy_rows: list[dict[str, str]],
    source_policy_term_rows: list[dict[str, str]],
    dw_formula_rows: list[dict[str, str]],
    variant_residual_rows: list[dict[str, str]],
    variant_residual_packet_rows: list[dict[str, str]],
    residual_term_summary_rows: list[dict[str, str]],
    residual_term_queue_rows: list[dict[str, str]],
    method_pair_universe_rows: list[dict[str, str]],
    source_transcription_rows: list[dict[str, str]],
    remaining_lane_summary_rows: list[dict[str, str]],
    remaining_lane_packet_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_claim_blocker_packet",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "blocker_rows": len(rows),
        "source_policy_scenario_rows": len(source_policy_rows),
        "source_policy_term_impact_rows": len(source_policy_term_rows),
        "dw_formula_sensitivity_rows": len(dw_formula_rows),
        "variant_residual_summary_rows": len(variant_residual_rows),
        "variant_residual_packet_rows": len(variant_residual_packet_rows),
        "residual_term_summary_rows": len(residual_term_summary_rows),
        "residual_term_queue_rows": len(residual_term_queue_rows),
        "method_pair_universe_summary_rows": len(method_pair_universe_rows),
        "source_transcription_row_summary_rows": len(source_transcription_rows),
        "remaining_lane_summary_rows": len(remaining_lane_summary_rows),
        "remaining_lane_packet_rows": len(remaining_lane_packet_rows),
        "inputs": {
            "readiness": str(args.readiness),
            "lock_options": str(args.lock_options),
            "source_queue": str(args.source_queue),
            "method_status": str(args.method_status),
            "source_policy_scenarios": str(args.source_policy_scenarios),
            "source_policy_term_impacts": str(args.source_policy_term_impacts),
            "dw_formula_sensitivity": str(args.dw_formula_sensitivity),
            "variant_residual_summary": str(args.variant_residual_summary),
            "variant_residual_packet": str(args.variant_residual_packet),
            "residual_term_summary": str(args.residual_term_summary),
            "residual_term_queue": str(args.residual_term_queue),
            "method_pair_universe_summary": str(args.method_pair_universe_summary),
            "source_transcription_row_summary": str(args.source_transcription_row_summary),
            "remaining_lane_summary": str(args.remaining_lane_summary),
            "remaining_lane_packet": str(args.remaining_lane_packet),
        },
        "outputs": {
            "out": str(args.out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def markdown_code_or_blank(value: object) -> str:
    text = markdown_cell(value)
    return f"`{text}`" if text else ""


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def sum_int(values: Iterable[object]) -> int:
    return sum(int_or_zero(str(value)) for value in values)


if __name__ == "__main__":
    raise SystemExit(main())
