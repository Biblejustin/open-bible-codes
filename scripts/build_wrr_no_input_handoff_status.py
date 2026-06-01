#!/usr/bin/env python3
"""Build a consolidated WRR no-input handoff status packet."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


DEFAULT_CLAIM_READINESS = Path("reports/wrr_1994/wrr_claim_readiness.csv")
DEFAULT_CLAIM_BLOCKERS = Path("reports/wrr_1994/wrr_claim_blocker_packet.csv")
DEFAULT_EXACT_GAP_SUMMARY = Path(
    "reports/wrr_1994/wrr_exact_gap_priority_packet_summary.csv"
)
DEFAULT_ACTION_SUMMARY = Path(
    "reports/wrr_1994/wrr_residual_reconciliation_action_summary.csv"
)
DEFAULT_ROW_SUMMARY = Path(
    "reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv"
)
DEFAULT_REMAINING_SUMMARY = Path(
    "reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv"
)
DEFAULT_MANUAL_SUMMARY = Path(
    "reports/wrr_1994/wrr_manual_decision_register_summary.csv"
)
DEFAULT_METHOD_SUMMARY = Path(
    "reports/wrr_1994/wrr_method_pair_universe_evidence_summary.csv"
)
DEFAULT_METHOD_WIDE_SKIP_SUMMARY = Path(
    "reports/wrr_1994/wrr_method_lane_wide_skip_probe_summary.csv"
)
DEFAULT_OUT = Path("reports/wrr_1994/wrr_no_input_handoff_status.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/wrr_no_input_handoff_status_summary.csv")
DEFAULT_MD = Path("docs/WRR_NO_INPUT_HANDOFF_STATUS.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_no_input_handoff_status.manifest.json")

STATUS_FIELDNAMES = [
    "status_id",
    "area",
    "current_status",
    "current_value",
    "handoff_ready",
    "manual_input_needed",
    "next_action",
    "boundary",
    "source",
]
SUMMARY_FIELDNAMES = [
    "status_rows",
    "handoff_ready_rows",
    "manual_input_needed_rows",
    "claim_readiness_rows",
    "claim_readiness_ready_rows",
    "claim_blocker_rows",
    "source_cited_defined_distances",
    "current_defined_distances",
    "remaining_gap",
    "review_lanes",
    "residual_action_terms",
    "residual_pairs",
    "frontier_pairs",
    "manual_decision_rows",
    "manual_action_terms",
    "manual_residual_pairs",
    "manual_frontier_pairs",
    "source_transcription_row_clusters",
    "source_transcription_action_terms",
    "page_image_terms",
    "method_pair_universe_terms",
    "wide_skip_max",
    "wide_skip_total_hits",
    "new_result_allowed",
    "exact_reproduction_ready",
    "claim_boundary",
]

CLAIM_BOUNDARY = "local_locked_method_ready_exact_published_open"


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    inputs = LoadedInputs(
        claim_readiness=read_rows(args.claim_readiness),
        claim_blockers=read_rows(args.claim_blockers),
        exact_gap_summary=read_rows(args.exact_gap_summary),
        action_summary=read_rows(args.action_summary),
        row_summary=read_rows(args.row_summary),
        remaining_summary=read_rows(args.remaining_summary),
        manual_summary=read_rows(args.manual_summary),
        method_summary=read_rows(args.method_summary),
        method_wide_skip_summary=read_rows(args.method_wide_skip_summary),
    )
    summary = build_summary(inputs)
    rows = build_status_rows(summary, inputs, args)
    write_csv(args.out, STATUS_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, rows)
    write_manifest(args.manifest_out, args, summary, rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


class LoadedInputs:
    def __init__(
        self,
        *,
        claim_readiness: list[dict[str, str]],
        claim_blockers: list[dict[str, str]],
        exact_gap_summary: list[dict[str, str]],
        action_summary: list[dict[str, str]],
        row_summary: list[dict[str, str]],
        remaining_summary: list[dict[str, str]],
        manual_summary: list[dict[str, str]],
        method_summary: list[dict[str, str]],
        method_wide_skip_summary: list[dict[str, str]],
    ) -> None:
        self.claim_readiness = claim_readiness
        self.claim_blockers = claim_blockers
        self.exact_gap_summary = exact_gap_summary
        self.action_summary = action_summary
        self.row_summary = row_summary
        self.remaining_summary = remaining_summary
        self.manual_summary = manual_summary
        self.method_summary = method_summary
        self.method_wide_skip_summary = method_wide_skip_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claim-readiness", type=Path, default=DEFAULT_CLAIM_READINESS)
    parser.add_argument("--claim-blockers", type=Path, default=DEFAULT_CLAIM_BLOCKERS)
    parser.add_argument("--exact-gap-summary", type=Path, default=DEFAULT_EXACT_GAP_SUMMARY)
    parser.add_argument("--action-summary", type=Path, default=DEFAULT_ACTION_SUMMARY)
    parser.add_argument("--row-summary", type=Path, default=DEFAULT_ROW_SUMMARY)
    parser.add_argument("--remaining-summary", type=Path, default=DEFAULT_REMAINING_SUMMARY)
    parser.add_argument("--manual-summary", type=Path, default=DEFAULT_MANUAL_SUMMARY)
    parser.add_argument("--method-summary", type=Path, default=DEFAULT_METHOD_SUMMARY)
    parser.add_argument(
        "--method-wide-skip-summary",
        type=Path,
        default=DEFAULT_METHOD_WIDE_SKIP_SUMMARY,
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_summary(inputs: LoadedInputs) -> dict[str, Any]:
    metric = metrics_by_name(inputs.exact_gap_summary)
    action_terms = sum_int(inputs.action_summary, "terms")
    action_pairs = sum_int(inputs.action_summary, "residual_pairs")
    action_frontier = sum_int(inputs.action_summary, "frontier_pairs")
    manual_rows = sum_int(inputs.manual_summary, "decision_rows")
    manual_terms = sum_int(inputs.manual_summary, "action_terms")
    manual_pairs = sum_int(inputs.manual_summary, "residual_pairs")
    manual_frontier = sum_int(inputs.manual_summary, "frontier_pairs")
    row_terms = sum_int(inputs.row_summary, "action_terms")
    page_image = lane_row(inputs.remaining_summary, "page_image_near_match_review")
    method_row = first_row(inputs.method_summary)
    wide_skip = first_row(inputs.method_wide_skip_summary)
    claim_ready = sum(
        1 for row in inputs.claim_readiness if row.get("ready", "").lower() == "true"
    )
    summary = {
        "status_rows": 9,
        "handoff_ready_rows": 9,
        "manual_input_needed_rows": 8,
        "claim_readiness_rows": len(inputs.claim_readiness),
        "claim_readiness_ready_rows": claim_ready,
        "claim_blocker_rows": len(inputs.claim_blockers),
        "source_cited_defined_distances": metric.get(
            "source_cited_defined_distances", ""
        ),
        "current_defined_distances": metric.get("current_defined_distances", ""),
        "remaining_gap": metric.get("remaining_163_distance_gap", ""),
        "review_lanes": len(inputs.action_summary),
        "residual_action_terms": action_terms,
        "residual_pairs": action_pairs,
        "frontier_pairs": action_frontier,
        "manual_decision_rows": manual_rows,
        "manual_action_terms": manual_terms,
        "manual_residual_pairs": manual_pairs,
        "manual_frontier_pairs": manual_frontier,
        "source_transcription_row_clusters": len(inputs.row_summary),
        "source_transcription_action_terms": row_terms,
        "page_image_terms": int_or_zero(page_image.get("action_terms", "")),
        "method_pair_universe_terms": int_or_zero(method_row.get("action_terms", "")),
        "wide_skip_max": wide_skip.get("max_skip", ""),
        "wide_skip_total_hits": int_or_zero(wide_skip.get("total_hits_through_max", "")),
        "new_result_allowed": False,
        "exact_reproduction_ready": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return summary


def build_status_rows(
    summary: dict[str, Any], inputs: LoadedInputs, args: argparse.Namespace
) -> list[dict[str, str]]:
    action_by_lane = {
        row.get("action_lane", ""): row for row in inputs.action_summary
    }
    page_image = action_by_lane.get("page_image_near_match_review", {})
    method_action = action_by_lane.get("method_or_pair_universe_review", {})
    source_policy = action_by_lane.get("source_policy_or_pair_rule_review", {})
    transcription = action_by_lane.get("source_transcription_or_row_alignment", {})
    wide_skip = first_row(inputs.method_wide_skip_summary)
    return [
        status_row(
            "local_claim_readiness",
            "local locked-method claim readiness",
            "ready_under_selected_local_policy",
            (
                f"{summary['claim_readiness_ready_rows']}/"
                f"{summary['claim_readiness_rows']} decision areas ready; "
                f"claim blockers {summary['claim_blocker_rows']}"
            ),
            "yes",
            "no",
            "keep exact-published WRR caveat attached to local locked-method reporting",
            "local lock readiness is not exact published WRR reproduction",
            args.claim_readiness,
        ),
        status_row(
            "exact_published_reproduction_gap",
            "exact published WRR reproduction",
            "open",
            (
                f"{summary['current_defined_distances']}/"
                f"{summary['source_cited_defined_distances']} defined distances; "
                f"gap {summary['remaining_gap']}"
            ),
            "yes",
            "yes",
            "continue source/term/pair-rule reconciliation plus method review",
            "do not describe local locked-method evidence as exact published reproduction",
            args.exact_gap_summary,
        ),
        status_row(
            "residual_review_lanes",
            "residual review lanes",
            "pending_manual_evidence",
            (
                f"{summary['review_lanes']} lanes; "
                f"{summary['residual_action_terms']} terms; "
                f"{summary['residual_pairs']} residual pairs; "
                f"{summary['frontier_pairs']} frontier pairs"
            ),
            "yes",
            "yes",
            "work lanes in priority order without automatic source edits",
            "lane counts are review workload counts, not corrections",
            args.action_summary,
        ),
        status_row(
            "source_policy_pair_rule",
            "source policy or pair rule",
            "needs_citable_rule",
            lane_value(source_policy),
            "yes",
            "yes",
            source_policy.get("evidence_required", ""),
            source_policy.get("no_input_boundary", ""),
            args.action_summary,
        ),
        status_row(
            "source_transcription_rows",
            "source transcription row clusters",
            "needs_primary_row_evidence",
            (
                f"{summary['source_transcription_row_clusters']} row clusters; "
                f"{summary['source_transcription_action_terms']} action terms"
            ),
            "yes",
            "yes",
            transcription.get("evidence_required", ""),
            transcription.get("no_input_boundary", ""),
            args.row_summary,
        ),
        status_row(
            "page_image_near_match",
            "page-image near-match terms",
            "needs_page_image_review",
            lane_value(page_image),
            "yes",
            "yes",
            page_image.get("evidence_required", ""),
            page_image.get("no_input_boundary", ""),
            args.remaining_summary,
        ),
        status_row(
            "method_pair_universe",
            "method or pair-universe terms",
            "needs_method_explanation",
            lane_value(method_action),
            "yes",
            "yes",
            method_action.get("evidence_required", ""),
            method_action.get("no_input_boundary", ""),
            args.method_summary,
        ),
        status_row(
            "method_wide_skip_probe",
            "method-lane wide-skip probe",
            "diagnostic_complete_no_hits",
            (
                f"{summary['method_pair_universe_terms']} terms; "
                f"skip {summary['wide_skip_max']}; "
                f"total hits {summary['wide_skip_total_hits']}"
            ),
            "yes",
            "yes",
            wide_skip.get("read", ""),
            "wide-skip zero-hit diagnostic does not select a method change",
            args.method_wide_skip_summary,
        ),
        status_row(
            "manual_decision_records",
            "manual decision records",
            "pending_manual_locks",
            (
                f"{summary['manual_decision_rows']} rows; "
                f"{summary['manual_action_terms']} terms; "
                f"{summary['manual_residual_pairs']} residual pairs; "
                f"{summary['manual_frontier_pairs']} frontier pairs"
            ),
            "yes",
            "yes",
            "fill decision records only from citable source, row, page-image, or method evidence",
            "records do not select corrections until evidence is locked",
            args.manual_summary,
        ),
    ]


def write_markdown(
    path: Path,
    summary: dict[str, Any],
    rows: list[dict[str, str]],
) -> None:
    lines = [
        "# WRR No-Input Handoff Status",
        "",
        "Status: consolidated no-input handoff.",
        "",
        "This is not a new WRR result, not an exact published WRR reproduction, not a source correction, not a pair exclusion, not a replacement spelling lock, and not a method change.",
        "It gathers the current no-input status from the WRR claim-readiness, exact-gap, residual-lane, manual-decision, and method-lane packets.",
        "It exists so the next work item starts from one guarded status file instead of re-reading the whole WRR packet chain.",
        "",
        "## Summary",
        "",
        f"- Status rows: {summary['status_rows']}.",
        f"- Handoff-ready rows: {summary['handoff_ready_rows']}.",
        f"- Manual-input-needed rows: {summary['manual_input_needed_rows']}.",
        f"- Local claim-readiness rows: {summary['claim_readiness_ready_rows']}/{summary['claim_readiness_rows']} ready.",
        f"- Claim-blocker rows: {summary['claim_blocker_rows']}.",
        f"- Source-cited defined distances: {summary['source_cited_defined_distances']}.",
        f"- Current defined distances: {summary['current_defined_distances']}.",
        f"- Remaining gap: {summary['remaining_gap']}.",
        f"- Review lanes: {summary['review_lanes']}.",
        f"- Residual action terms: {summary['residual_action_terms']}.",
        f"- Residual pairs: {summary['residual_pairs']}.",
        f"- Frontier pairs: {summary['frontier_pairs']}.",
        f"- Manual decision rows: {summary['manual_decision_rows']}.",
        f"- Source-transcription row clusters: {summary['source_transcription_row_clusters']}.",
        f"- Page-image near-match terms: {summary['page_image_terms']}.",
        f"- Method/pair-universe terms: {summary['method_pair_universe_terms']}.",
        f"- Wide-skip total hits through skip {summary['wide_skip_max']}: {summary['wide_skip_total_hits']}.",
        f"- New WRR result allowed: {int(bool(summary['new_result_allowed']))}.",
        f"- Exact published reproduction ready: {int(bool(summary['exact_reproduction_ready']))}.",
        f"- Claim boundary: `{summary['claim_boundary']}`.",
        "",
        "## Handoff Rows",
        "",
        "| Status id | Area | Status | Value | Manual input | Boundary |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['status_id']}` | {row['area']} | `{row['current_status']}` | {row['current_value']} | `{row['manual_input_needed']}` | {row['boundary']} |"
        )
    lines.extend(
        [
            "",
            "## Next Work",
            "",
            "The no-input path can still keep reports aligned, rebuild packets, and run guarded diagnostics.",
            "It cannot close source-policy, source-transcription, page-image, or method/pair-universe decisions without citable evidence.",
            "The next result-bearing WRR claim remains blocked until those manual-input rows are resolved.",
            "",
            "## Cautions",
            "",
            "- This handoff is a map of remaining work, not a new statistical result.",
            "- Local locked-method evidence remains separate from exact published WRR reproduction.",
            "- Review-lane counts are workload counts, not significance tests.",
            "- Do not promote OCR near matches, source flags, zero-hit diagnostics, or row clusters into corrections without citable evidence.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, Any],
    rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.build_wrr_no_input_handoff_status",
        "claim_boundary": "WRR no-input handoff only; no new result",
        "text_retention": "no Bible text written to tracked outputs",
        "summary": summary,
        "status_rows": len(rows),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "claim_readiness": str(args.claim_readiness),
            "claim_blockers": str(args.claim_blockers),
            "exact_gap_summary": str(args.exact_gap_summary),
            "action_summary": str(args.action_summary),
            "row_summary": str(args.row_summary),
            "remaining_summary": str(args.remaining_summary),
            "manual_summary": str(args.manual_summary),
            "method_summary": str(args.method_summary),
            "method_wide_skip_summary": str(args.method_wide_skip_summary),
        },
        "outputs": {
            "status": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def status_row(
    status_id: str,
    area: str,
    current_status: str,
    current_value: str,
    handoff_ready: str,
    manual_input_needed: str,
    next_action: str,
    boundary: str,
    source: Path,
) -> dict[str, str]:
    return {
        "status_id": status_id,
        "area": area,
        "current_status": current_status,
        "current_value": current_value,
        "handoff_ready": handoff_ready,
        "manual_input_needed": manual_input_needed,
        "next_action": next_action,
        "boundary": boundary,
        "source": str(source),
    }


def lane_value(row: dict[str, str]) -> str:
    terms = row.get("terms", row.get("action_terms", ""))
    pairs = row.get("residual_pairs", "")
    frontier = row.get("frontier_pairs", "")
    return f"{terms} terms; {pairs} residual pairs; {frontier} frontier pairs"


def lane_row(rows: list[dict[str, str]], lane: str) -> dict[str, str]:
    for row in rows:
        if row.get("action_lane") == lane:
            return row
    return {}


def metrics_by_name(rows: list[dict[str, str]]) -> dict[str, str]:
    return {row.get("metric", ""): row.get("value", "") for row in rows}


def first_row(rows: list[dict[str, str]]) -> dict[str, str]:
    return rows[0] if rows else {}


def sum_int(rows: list[dict[str, str]], key: str) -> int:
    return sum(int_or_zero(row.get(key, "")) for row in rows)


def int_or_zero(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
