#!/usr/bin/env python3
"""Build a WRR exact-published reproduction gap dashboard."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_LOCKED_REPORT = Path("reports/wrr_1994/wrr_locked_method_report.csv")
DEFAULT_DEFINED_PAIR_SUMMARY = Path(
    "reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv"
)
DEFAULT_GAP_REASONS = Path("reports/wrr_1994/wrr_defined_gap_reasons.csv")
DEFAULT_VARIANT_UPPER_BOUND = Path("reports/wrr_1994/wrr_variant_gap_upper_bound.csv")
DEFAULT_ACTION_SUMMARY = Path(
    "reports/wrr_1994/wrr_residual_reconciliation_action_summary.csv"
)
DEFAULT_MANUAL_REGISTER_SUMMARY = Path(
    "reports/wrr_1994/wrr_manual_decision_register_summary.csv"
)
DEFAULT_MANUAL_DECISION_RECORDS = Path(
    "data/study/mappings/wrr_manual_decision_records.csv"
)
DEFAULT_SOURCE_POLICY_CHECKLIST = Path(
    "reports/wrr_1994/wrr_source_policy_review_checklist.csv"
)
DEFAULT_ROW_CHECKLIST = Path(
    "reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv"
)
DEFAULT_REMAINING_CHECKLIST = Path(
    "reports/wrr_1994/wrr_remaining_lane_review_checklist.csv"
)
DEFAULT_OUT = Path("reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.csv")
DEFAULT_MD = Path("docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.manifest.json"
)

FIELDNAMES = ["section", "item", "value", "status", "evidence", "source"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    inputs = LoadedInputs(
        locked_report=read_rows(args.locked_report),
        defined_pair_summary=read_rows(args.defined_pair_summary),
        gap_reasons=read_rows(args.gap_reasons),
        variant_upper_bound=read_rows(args.variant_upper_bound),
        action_summary=read_rows(args.action_summary),
        manual_register_summary=read_rows(args.manual_register_summary),
        manual_decision_records=read_rows(args.manual_decision_records),
        source_policy_checklist=read_rows(args.source_policy_checklist),
        row_checklist=read_rows(args.row_checklist),
        remaining_checklist=read_rows(args.remaining_checklist),
    )
    rows = build_dashboard_rows(inputs, args)
    write_csv(args.out, rows)
    write_markdown(args.markdown_out, rows, inputs, args)
    write_manifest(args.manifest_out, rows, inputs, args, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


class LoadedInputs:
    def __init__(
        self,
        *,
        locked_report: list[dict[str, str]],
        defined_pair_summary: list[dict[str, str]],
        gap_reasons: list[dict[str, str]],
        variant_upper_bound: list[dict[str, str]],
        action_summary: list[dict[str, str]],
        manual_register_summary: list[dict[str, str]],
        manual_decision_records: list[dict[str, str]],
        source_policy_checklist: list[dict[str, str]],
        row_checklist: list[dict[str, str]],
        remaining_checklist: list[dict[str, str]],
    ) -> None:
        self.locked_report = locked_report
        self.defined_pair_summary = defined_pair_summary
        self.gap_reasons = gap_reasons
        self.variant_upper_bound = variant_upper_bound
        self.action_summary = action_summary
        self.manual_register_summary = manual_register_summary
        self.manual_decision_records = manual_decision_records
        self.source_policy_checklist = source_policy_checklist
        self.row_checklist = row_checklist
        self.remaining_checklist = remaining_checklist


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locked-report", type=Path, default=DEFAULT_LOCKED_REPORT)
    parser.add_argument(
        "--defined-pair-summary", type=Path, default=DEFAULT_DEFINED_PAIR_SUMMARY
    )
    parser.add_argument("--gap-reasons", type=Path, default=DEFAULT_GAP_REASONS)
    parser.add_argument(
        "--variant-upper-bound", type=Path, default=DEFAULT_VARIANT_UPPER_BOUND
    )
    parser.add_argument("--action-summary", type=Path, default=DEFAULT_ACTION_SUMMARY)
    parser.add_argument(
        "--manual-register-summary", type=Path, default=DEFAULT_MANUAL_REGISTER_SUMMARY
    )
    parser.add_argument(
        "--manual-decision-records", type=Path, default=DEFAULT_MANUAL_DECISION_RECORDS
    )
    parser.add_argument(
        "--source-policy-checklist", type=Path, default=DEFAULT_SOURCE_POLICY_CHECKLIST
    )
    parser.add_argument("--row-checklist", type=Path, default=DEFAULT_ROW_CHECKLIST)
    parser.add_argument(
        "--remaining-checklist", type=Path, default=DEFAULT_REMAINING_CHECKLIST
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_dashboard_rows(
    inputs: LoadedInputs, args: argparse.Namespace
) -> list[dict[str, str]]:
    defined = all_lanes_cap1000(inputs.defined_pair_summary)
    upper_bound = all_lanes_cap1000(inputs.variant_upper_bound)
    manual_totals = manual_summary(inputs.manual_register_summary)
    manual_record_totals = manual_record_summary(inputs.manual_decision_records)
    locked_status = lookup_locked_value(inputs.locked_report, "status", "report_status")
    rows = [
        row(
            "status",
            "exact_published_reproduction",
            "not_reproduced",
            "open",
            "Local locked-method report exists, but exact published WRR reproduction remains caveated.",
            str(args.locked_report),
        ),
        row(
            "status",
            "local_locked_report",
            locked_status,
            "locked_local",
            "Selected local policy remains the reporting boundary.",
            str(args.locked_report),
        ),
        row(
            "gap",
            "source_cited_defined_distances",
            defined.get("source_cited_defined_distances", ""),
            defined.get("status", ""),
            "Published/secondary source cited count treated as a corrected-distance output target.",
            str(args.defined_pair_summary),
        ),
        row(
            "gap",
            "current_defined_distances",
            defined.get("defined", ""),
            defined.get("status", ""),
            "Current selected all-lane cap1000 defined corrected-distance count.",
            str(args.defined_pair_summary),
        ),
        row(
            "gap",
            "remaining_gap",
            defined.get("defined_gap_to_source_cited", ""),
            defined.get("status", ""),
            "This is the exact-published reproduction gap to explain before stronger language.",
            str(args.defined_pair_summary),
        ),
        row(
            "variant_upper_bound",
            "residual_after_simple_variants",
            upper_bound.get("residual_gap_after_simple_variant_upper_bound", ""),
            upper_bound.get("status", ""),
            upper_bound.get("read", ""),
            str(args.variant_upper_bound),
        ),
        row(
            "manual_locks",
            "manual_decision_inventory",
            (
                f"{manual_totals['decision_rows']} rows; "
                f"{manual_totals['action_terms']} action terms; "
                f"{manual_totals['frontier_pairs']} frontier pair links"
            ),
            "locked_no_source_change_or_method_lock",
            "Manual locks organize review state; they do not select corrections, replacements, or exclusions.",
            str(args.manual_register_summary),
        ),
        row(
            "manual_locks",
            "manual_decision_records",
            (
                f"{manual_record_totals['locked']} locked; "
                f"{manual_record_totals['unlocked']} unlocked; "
                f"{format_counts(manual_record_totals['selected_actions'])}"
            ),
            "all_current_manual_reviews_locked"
            if manual_record_totals["unlocked"] == 0
            else "manual_reviews_unlocked",
            "Decision records set current lock status; source corrections require selected_action to name a source change.",
            str(args.manual_decision_records),
        ),
    ]
    source_lock = source_policy_lock(inputs.manual_decision_records)
    if source_lock:
        rows.append(
            row(
                "manual_locks",
                "source_policy_pair_rule_lock",
                (
                    f"{source_lock.get('decision_id', '')} "
                    f"{source_lock.get('selected_action', '')}"
                ).strip(),
                source_lock.get("decision_status", ""),
                source_lock.get("evidence_summary", ""),
                str(args.manual_decision_records),
            )
        )
    for reason_row in selected_gap_reasons(inputs.gap_reasons):
        rows.append(
            row(
                "gap_reason",
                reason_row.get("reason", ""),
                reason_row.get("pairs", ""),
                "diagnostic",
                reason_row.get("read", ""),
                str(args.gap_reasons),
            )
        )
    for action_row in inputs.action_summary:
        rows.append(
            row(
                "review_lane",
                action_row.get("action_lane", ""),
                (
                    f"{action_row.get('terms', '')} terms; "
                    f"{action_row.get('residual_pairs', '')} residual pairs; "
                    f"{action_row.get('frontier_pairs', '')} frontier pairs"
                ),
                "pending_review",
                action_row.get("evidence_required", ""),
                str(args.action_summary),
            )
        )
    for item, evidence in recommended_next_items(inputs):
        rows.append(
            row(
                "recommended_next",
                item,
                "organize_evidence_only",
                "no_source_change",
                evidence,
                "derived from current review checklists",
            )
        )
    return rows


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    inputs: LoadedInputs,
    args: argparse.Namespace,
) -> None:
    defined = all_lanes_cap1000(inputs.defined_pair_summary)
    upper_bound = all_lanes_cap1000(inputs.variant_upper_bound)
    manual_totals = manual_summary(inputs.manual_register_summary)
    manual_record_totals = manual_record_summary(inputs.manual_decision_records)
    action_rows = inputs.action_summary
    gap_reasons = selected_gap_reasons(inputs.gap_reasons)
    recommended = recommended_next_items(inputs)
    lines = [
        "# WRR Exact Reproduction Gap Dashboard",
        "",
        "Status: exact published WRR reproduction is not closed.",
        "",
        "This dashboard starts from the locked local WRR method report and shows",
        "what still blocks exact published reproduction language.",
        "It does not select source corrections, pair exclusions, replacement spellings, or method changes.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_exact_reproduction_gap_dashboard "
            f"--locked-report {args.locked_report} "
            f"--defined-pair-summary {args.defined_pair_summary} "
            f"--gap-reasons {args.gap_reasons} "
            f"--variant-upper-bound {args.variant_upper_bound} "
            f"--action-summary {args.action_summary} "
            f"--manual-register-summary {args.manual_register_summary} "
            f"--manual-decision-records {args.manual_decision_records} "
            f"--source-policy-checklist {args.source_policy_checklist} "
            f"--row-checklist {args.row_checklist} "
            f"--remaining-checklist {args.remaining_checklist} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Gap Summary",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| Source-cited defined distances | {cell(defined.get('source_cited_defined_distances', ''))} |",
        f"| Current defined distances | {cell(defined.get('defined', ''))} |",
        f"| Remaining 163-distance gap | {cell(defined.get('defined_gap_to_source_cited', ''))} |",
        f"| Residual gap after simple-variant upper bound | {cell(upper_bound.get('residual_gap_after_simple_variant_upper_bound', ''))} |",
        f"| Manual decision rows | {manual_totals['decision_rows']} |",
        f"| Manual action terms | {manual_totals['action_terms']} |",
        f"| Manual frontier pair links | {manual_totals['frontier_pairs']} |",
        f"| Locked manual decision records | {manual_record_totals['locked']} |",
        f"| Unlocked manual decision records | {manual_record_totals['unlocked']} |",
        f"| Recorded selected actions | {cell(format_counts(manual_record_totals['selected_actions']))} |",
        "",
        "## Gap Reasons",
        "",
        "| Reason | Pairs | Read |",
        "| --- | ---: | --- |",
    ]
    for gap_row in gap_reasons:
        lines.append(
            "| {reason} | {pairs} | {read} |".format(
                reason=cell(gap_row.get("reason", "")),
                pairs=cell(gap_row.get("pairs", "")),
                read=cell(gap_row.get("read", "")),
            )
        )
    lines.extend(
        [
            "",
            "## Review Lanes",
            "",
            "| Lane | Terms | Residual pairs | Frontier pairs | Evidence required |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )
    for action_row in action_rows:
        lines.append(
            "| `{lane}` | {terms} | {residual} | {frontier} | {evidence} |".format(
                lane=cell(action_row.get("action_lane", "")),
                terms=cell(action_row.get("terms", "")),
                residual=cell(action_row.get("residual_pairs", "")),
                frontier=cell(action_row.get("frontier_pairs", "")),
                evidence=cell(action_row.get("evidence_required", "")),
            )
        )
    lines.extend(
        [
            "",
            "## Manual Lock Status",
            "",
            "| Lock | Status | Action | Evidence read |",
            "| --- | --- | --- | --- |",
        ]
    )
    for lock_row in manual_lock_rows(inputs.manual_decision_records):
        lines.append(
            "| {target} | {status} | {action} | {evidence} |".format(
                target=cell(lock_row.get("decision_target", "")),
                status=cell(lock_row.get("decision_status", "")),
                action=cell(lock_row.get("selected_action", "")),
                evidence=cell(lock_row.get("evidence_summary", "")),
            )
        )
    lines.extend(
        [
            "",
            "## Recommended Next Items",
            "",
            "| Rank | Item | Action |",
            "| ---: | --- | --- |",
        ]
    )
    for index, (item, evidence) in enumerate(recommended, start=1):
        lines.append(f"| {index} | {cell(item)} | {cell(evidence)} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Keep the locked local WRR report unchanged unless a separate decision record changes source or method policy.",
            "- Do not describe the local result as exact published WRR reproduction.",
            "- Do not promote WNP/context flags, OCR near matches, or simple variant leads into corrections without citable source evidence.",
            "- This dashboard is a review map, not a reproduction result.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def recommended_next_items(inputs: LoadedInputs) -> list[tuple[str, str]]:
    source = first(inputs.source_policy_checklist)
    manual_record_totals = manual_record_summary(inputs.manual_decision_records)
    unlocked = int(manual_record_totals["unlocked"])
    row_frontier = sorted(
        [
            row
            for row in inputs.row_checklist
            if int_or_zero(row.get("frontier_pairs", "")) > 0
        ],
        key=lambda row: int_or_zero(row.get("checklist_rank", row.get("row_rank", ""))),
    )
    remaining_frontier = sorted(
        [
            row
            for row in inputs.remaining_checklist
            if int_or_zero(row.get("frontier_pairs", "")) > 0
        ],
        key=lambda row: int_or_zero(row.get("checklist_rank", "")),
    )
    items: list[tuple[str, str]] = []
    if unlocked == 0:
        items.append(
            (
                "post-lock reporting boundary",
                "all current manual review rows are locked; keep source unchanged and describe the residual gap as exact-reproduction work, not pending source edits",
            )
        )
    if source and unlocked > 0:
        items.append(
            (
                f"source-policy/pair-rule: {source.get('term_id', '')} {source.get('term', '')}",
                source.get("next_manual_action", "")
                or "cite source/pair-rule evidence before changing working source",
            )
        )
    if row_frontier and unlocked > 0:
        top_rows = ", ".join(
            f"row {row.get('row_number', '')}" for row in row_frontier[:5]
        )
        frontier_pairs = sum_int(row_frontier, "frontier_pairs")
        items.append(
            (
                f"source-transcription row clusters: {top_rows}",
                f"review row images for {frontier_pairs} frontier pair links before term edits",
            )
        )
    page_rows = [
        row for row in remaining_frontier if row.get("action_lane") == "page_image_near_match_review"
    ]
    if page_rows and unlocked > 0:
        items.append(
            (
                "page-image near-match terms",
                f"inspect {len(page_rows)} frontier near-match terms before source correction",
            )
        )
    method_rows = [
        row for row in remaining_frontier if row.get("action_lane") == "method_or_pair_universe_review"
    ]
    if method_rows and unlocked > 0:
        items.append(
            (
                "method/pair-universe zero ordinary-hit terms",
                f"review {len(method_rows)} frontier OCR-matched terms for method or pair-universe explanation",
            )
        )
    items.append(
        (
            "exact-published gap language",
            "keep exact-published reproduction caveat attached until the 163-distance gap is explained",
        )
    )
    return items


def selected_gap_reasons(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if row.get("run_label") == "all_lanes_cap1000"
        and row.get("reason") != "defined"
    ]


def all_lanes_cap1000(rows: list[dict[str, str]]) -> dict[str, str]:
    return first([row for row in rows if row.get("run_label") == "all_lanes_cap1000"] or rows)


def manual_summary(rows: list[dict[str, str]]) -> dict[str, int]:
    totals = Counter()
    for row in rows:
        totals["decision_rows"] += int_or_zero(row.get("decision_rows", ""))
        totals["action_terms"] += int_or_zero(row.get("action_terms", ""))
        totals["residual_pairs"] += int_or_zero(row.get("residual_pairs", ""))
        totals["frontier_pairs"] += int_or_zero(row.get("frontier_pairs", ""))
    return {
        "decision_rows": totals["decision_rows"],
        "action_terms": totals["action_terms"],
        "residual_pairs": totals["residual_pairs"],
        "frontier_pairs": totals["frontier_pairs"],
    }


def manual_record_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    selected: Counter[str] = Counter()
    locked = 0
    unlocked = 0
    for row in rows:
        if row.get("decision_status") == "locked":
            locked += 1
        else:
            unlocked += 1
        action = row.get("selected_action", "")
        if action:
            selected[action] += 1
    return {
        "locked": locked,
        "unlocked": unlocked,
        "selected_actions": dict(sorted(selected.items())),
    }


def source_policy_lock(rows: list[dict[str, str]]) -> dict[str, str]:
    return first(
        [
            row
            for row in rows
            if row.get("decision_lane") == "source_policy_pair_rule"
        ]
    )


def manual_lock_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    lanes = [
        "source_policy_pair_rule",
        "source_transcription_row_cluster",
        "page_image_near_match",
        "method_pair_universe",
    ]
    selected: list[dict[str, str]] = []
    for lane in lanes:
        for row in rows:
            if row.get("decision_lane") == lane:
                selected.append(row)
                break
    return selected


def format_counts(counts: object) -> str:
    if not isinstance(counts, dict):
        return ""
    return "; ".join(f"{key}={value}" for key, value in sorted(counts.items()))


def lookup_locked_value(
    rows: list[dict[str, str]], section: str, item: str
) -> str:
    for row in rows:
        if row.get("section") == section and row.get("item") == item:
            return row.get("value", "")
    return ""


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    rows: list[dict[str, str]],
    inputs: LoadedInputs,
    args: argparse.Namespace,
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_exact_reproduction_gap_dashboard",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "dashboard_rows": len(rows),
        "gap_reason_rows": len(selected_gap_reasons(inputs.gap_reasons)),
        "review_lane_rows": len(inputs.action_summary),
        "inputs": {
            "locked_report": str(args.locked_report),
            "defined_pair_summary": str(args.defined_pair_summary),
            "gap_reasons": str(args.gap_reasons),
            "variant_upper_bound": str(args.variant_upper_bound),
            "action_summary": str(args.action_summary),
            "manual_register_summary": str(args.manual_register_summary),
            "manual_decision_records": str(args.manual_decision_records),
            "source_policy_checklist": str(args.source_policy_checklist),
            "row_checklist": str(args.row_checklist),
            "remaining_checklist": str(args.remaining_checklist),
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


def row(
    section: str,
    item: str,
    value: str,
    status: str,
    evidence: str,
    source: str,
) -> dict[str, str]:
    return {
        "section": section,
        "item": item,
        "value": value,
        "status": status,
        "evidence": evidence,
        "source": source,
    }


def first(rows: list[dict[str, str]]) -> dict[str, str]:
    return rows[0] if rows else {}


def sum_int(rows: list[dict[str, str]], field: str) -> int:
    return sum(int_or_zero(row.get(field, "")) for row in rows)


def int_or_zero(value: object) -> int:
    try:
        return int(str(value))
    except ValueError:
        return 0


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


if __name__ == "__main__":
    raise SystemExit(main())
