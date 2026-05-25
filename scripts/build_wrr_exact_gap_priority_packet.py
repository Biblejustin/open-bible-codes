#!/usr/bin/env python3
"""Build a WRR exact-gap priority packet without selecting source changes."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_DASHBOARD = Path("reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.csv")
DEFAULT_ACTION_SUMMARY = Path(
    "reports/wrr_1994/wrr_residual_reconciliation_action_summary.csv"
)
DEFAULT_ROW_SUMMARY = Path(
    "reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv"
)
DEFAULT_REMAINING_SUMMARY = Path(
    "reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv"
)
DEFAULT_METHOD_SUMMARY = Path(
    "reports/wrr_1994/wrr_method_pair_universe_evidence_summary.csv"
)
DEFAULT_GAP_REASONS = Path("reports/wrr_1994/wrr_defined_gap_reasons.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_exact_gap_priority_packet.csv")
DEFAULT_SUMMARY_OUT = Path(
    "reports/wrr_1994/wrr_exact_gap_priority_packet_summary.csv"
)
DEFAULT_MD = Path("docs/WRR_EXACT_GAP_PRIORITY_PACKET.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_exact_gap_priority_packet.manifest.json"
)

FIELDNAMES = [
    "section",
    "priority",
    "item",
    "value",
    "status",
    "evidence_required",
    "no_input_boundary",
    "source",
    "read",
]

SUMMARY_FIELDNAMES = ["metric", "value", "source"]

LANE_ORDER = {
    "source_policy_or_pair_rule_review": 1,
    "source_transcription_or_row_alignment": 2,
    "page_image_near_match_review": 3,
    "method_or_pair_universe_review": 4,
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    inputs = LoadedInputs(
        dashboard=read_rows(args.dashboard),
        action_summary=read_rows(args.action_summary),
        row_summary=read_rows(args.row_summary),
        remaining_summary=read_rows(args.remaining_summary),
        method_summary=read_rows(args.method_summary),
        gap_reasons=read_rows(args.gap_reasons),
    )
    rows = build_priority_rows(inputs, args)
    summary = build_summary_rows(inputs, rows, args)
    write_csv(args.out, FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary)
    write_markdown(args.markdown_out, rows, summary, inputs, args)
    write_manifest(args.manifest_out, args, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


class LoadedInputs:
    def __init__(
        self,
        *,
        dashboard: list[dict[str, str]],
        action_summary: list[dict[str, str]],
        row_summary: list[dict[str, str]],
        remaining_summary: list[dict[str, str]],
        method_summary: list[dict[str, str]],
        gap_reasons: list[dict[str, str]],
    ) -> None:
        self.dashboard = dashboard
        self.action_summary = action_summary
        self.row_summary = row_summary
        self.remaining_summary = remaining_summary
        self.method_summary = method_summary
        self.gap_reasons = gap_reasons


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dashboard", type=Path, default=DEFAULT_DASHBOARD)
    parser.add_argument("--action-summary", type=Path, default=DEFAULT_ACTION_SUMMARY)
    parser.add_argument("--row-summary", type=Path, default=DEFAULT_ROW_SUMMARY)
    parser.add_argument("--remaining-summary", type=Path, default=DEFAULT_REMAINING_SUMMARY)
    parser.add_argument("--method-summary", type=Path, default=DEFAULT_METHOD_SUMMARY)
    parser.add_argument("--gap-reasons", type=Path, default=DEFAULT_GAP_REASONS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_priority_rows(
    inputs: LoadedInputs, args: argparse.Namespace
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    rows.extend(gap_rows(inputs.dashboard, args))
    rows.extend(lane_rows(inputs.action_summary, args))
    rows.extend(source_row_cluster_rows(inputs.row_summary, args))
    rows.extend(remaining_lane_rows(inputs.remaining_summary, args))
    rows.extend(method_pair_rows(inputs.method_summary, args))
    rows.extend(gap_reason_rows(inputs.gap_reasons, args))
    return rows


def gap_rows(
    dashboard: list[dict[str, str]], args: argparse.Namespace
) -> list[dict[str, object]]:
    by_item = {row.get("item", ""): row for row in dashboard}
    return [
        packet_row(
            "gap",
            1,
            "remaining_163_distance_gap",
            (
                f"{dashboard_value(by_item, 'current_defined_distances')} current "
                f"defined distances vs "
                f"{dashboard_value(by_item, 'source_cited_defined_distances')} "
                f"source-cited; gap "
                f"{dashboard_value(by_item, 'remaining_gap')}"
            ),
            "exact_published_reproduction_open",
            "explain source-cited 163 defined distances before stronger reproduction language",
            "keep local locked-method result separate from exact published WRR reproduction",
            args.dashboard,
            "Remaining 163-distance gap is still the hard boundary.",
        )
    ]


def lane_rows(
    action_summary: list[dict[str, str]], args: argparse.Namespace
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in sorted(
        action_summary, key=lambda item: LANE_ORDER.get(item.get("action_lane", ""), 99)
    ):
        lane = row.get("action_lane", "")
        out.append(
            packet_row(
                "review_lane",
                LANE_ORDER.get(lane, 99),
                lane,
                (
                    f"{row.get('terms', '')} terms; "
                    f"{row.get('residual_pairs', '')} residual pairs; "
                    f"{row.get('frontier_pairs', '')} frontier pairs"
                ),
                "evidence_needed_no_source_change_selected",
                row.get("evidence_required", ""),
                row.get("no_input_boundary", ""),
                args.action_summary,
                row.get("read", ""),
            )
        )
    return out


def source_row_cluster_rows(
    row_summary: list[dict[str, str]], args: argparse.Namespace
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in sorted(row_summary, key=source_row_sort_key):
        out.append(
            packet_row(
                "source_row_cluster",
                int_or_zero(row.get("row_rank", "")),
                f"row {row.get('row_number', '')} {row.get('concept', '')}".strip(),
                (
                    f"{row.get('action_terms', '')} action terms; "
                    f"{row.get('residual_pairs', '')} residual pairs; "
                    f"{row.get('frontier_pairs', '')} frontier pairs"
                ),
                "needs_primary_row_evidence",
                row.get("evidence_required", ""),
                row.get("no_input_boundary", ""),
                args.row_summary,
                row.get("read", ""),
            )
        )
    return out


def remaining_lane_rows(
    remaining_summary: list[dict[str, str]], args: argparse.Namespace
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in sorted(
        remaining_summary,
        key=lambda item: LANE_ORDER.get(item.get("action_lane", ""), 99),
    ):
        lane = row.get("action_lane", "")
        out.append(
            packet_row(
                "remaining_lane",
                LANE_ORDER.get(lane, 99),
                lane,
                (
                    f"{row.get('action_terms', '')} terms; "
                    f"{row.get('residual_pairs', '')} residual pairs; "
                    f"{row.get('frontier_pairs', '')} frontier pairs"
                ),
                "review_before_method_or_source_change",
                row.get("evidence_required", ""),
                row.get("no_input_boundary", ""),
                args.remaining_summary,
                row.get("read", ""),
            )
        )
    return out


def method_pair_rows(
    method_summary: list[dict[str, str]], args: argparse.Namespace
) -> list[dict[str, object]]:
    if not method_summary:
        return []
    row = method_summary[0]
    return [
        packet_row(
            "method_pair_universe",
            1,
            "ocr_matched_zero_ordinary_hits",
            (
                f"{row.get('ocr_matched_terms', '')} OCR-matched terms; "
                f"{row.get('zero_highcap_appellation_terms', '')} zero high-cap "
                f"appellation-hit terms; "
                f"{row.get('both_sides_zero_highcap_pairs', '')} both-side-zero pairs"
            ),
            "method_or_pair_universe_review",
            "method or pair-universe explanation for OCR-matched missing ordinary hits",
            "do not treat OCR-matched missing ordinary hits as source corrections",
            args.method_summary,
            row.get("read", ""),
        )
    ]


def gap_reason_rows(
    gap_reasons: list[dict[str, str]], args: argparse.Namespace
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for index, row in enumerate(
        [
            r
            for r in gap_reasons
            if r.get("run_label") == "all_lanes_cap1000"
            and r.get("reason") != "defined"
        ],
        start=1,
    ):
        out.append(
            packet_row(
                "gap_reason",
                index,
                row.get("reason", ""),
                row.get("pairs", ""),
                "diagnostic_not_decision",
                "use reason counts to focus evidence review",
                "reason counts do not select source or method changes",
                args.gap_reasons,
                row.get("read", ""),
            )
        )
    return out


def build_summary_rows(
    inputs: LoadedInputs, rows: list[dict[str, object]], args: argparse.Namespace
) -> list[dict[str, object]]:
    dashboard = {row.get("item", ""): row for row in inputs.dashboard}
    source_rows = [row for row in rows if row["section"] == "source_row_cluster"]
    return [
        {
            "metric": "source_cited_defined_distances",
            "value": dashboard_value(dashboard, "source_cited_defined_distances"),
            "source": str(args.dashboard),
        },
        {
            "metric": "current_defined_distances",
            "value": dashboard_value(dashboard, "current_defined_distances"),
            "source": str(args.dashboard),
        },
        {
            "metric": "remaining_163_distance_gap",
            "value": dashboard_value(dashboard, "remaining_gap"),
            "source": str(args.dashboard),
        },
        {
            "metric": "review_lanes",
            "value": str(len([row for row in rows if row["section"] == "review_lane"])),
            "source": str(args.action_summary),
        },
        {
            "metric": "source_row_clusters",
            "value": str(len(source_rows)),
            "source": str(args.row_summary),
        },
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    inputs: LoadedInputs,
    args: argparse.Namespace,
) -> None:
    summary_by_metric = {str(row["metric"]): str(row["value"]) for row in summary}
    review_lanes = [row for row in rows if row["section"] == "review_lane"]
    row_clusters = [row for row in rows if row["section"] == "source_row_cluster"]
    remaining_lanes = [row for row in rows if row["section"] == "remaining_lane"]
    method_rows = [row for row in rows if row["section"] == "method_pair_universe"]
    gap_reasons = [row for row in rows if row["section"] == "gap_reason"]
    lines = [
        "# WRR Exact Gap Priority Packet",
        "",
        "Status: no-input priority packet for the exact-published WRR reproduction gap.",
        "",
        "This packet ranks current evidence tasks. It does not select source corrections, pair exclusions, replacement spellings, or method changes.",
        "",
        "## Setup",
        "",
        "```bash",
        "python3 -m scripts.build_wrr_exact_gap_priority_packet",
        "```",
        "",
        "## Current Boundary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Source-cited defined distances | {summary_by_metric.get('source_cited_defined_distances', '')} |",
        f"| Current defined distances | {summary_by_metric.get('current_defined_distances', '')} |",
        f"| Remaining 163-distance gap | {summary_by_metric.get('remaining_163_distance_gap', '')} |",
        f"| Review lanes | {summary_by_metric.get('review_lanes', '')} |",
        f"| Source-row clusters | {summary_by_metric.get('source_row_clusters', '')} |",
        "",
        "## Priority Lanes",
        "",
        "| Priority | Lane | Value | Evidence required | Boundary |",
        "| ---: | --- | --- | --- | --- |",
    ]
    for row in review_lanes:
        lines.append(
            "| {priority} | `{item}` | {value} | {evidence_required} | {no_input_boundary} |".format(
                **markdown_row(row)
            )
        )
    lines.extend(
        [
            "",
            "## Source-Row Clusters",
            "",
            f"Full CSV includes {len(row_clusters)} row clusters. Top clusters by action terms:",
            "",
            "| Rank | Row | Value | Read |",
            "| ---: | --- | --- | --- |",
        ]
    )
    for row in row_clusters[:10]:
        lines.append(
            "| {priority} | {item} | {value} | {read} |".format(**markdown_row(row))
        )
    lines.extend(
        [
            "",
            "## Remaining And Method Lanes",
            "",
            "| Section | Item | Value | Boundary | Read |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in [*remaining_lanes, *method_rows]:
        lines.append(
            "| {section} | `{item}` | {value} | {no_input_boundary} | {read} |".format(
                **markdown_row(row)
            )
        )
    lines.extend(
        [
            "",
            "## Gap Reasons",
            "",
            "| Reason | Pairs | Read |",
            "| --- | ---: | --- |",
        ]
    )
    for row in gap_reasons:
        lines.append("| `{item}` | {value} | {read} |".format(**markdown_row(row)))
    lines.extend(
        [
            "",
            "## Cautions",
            "",
            "- This is an evidence-priority packet, not an exact published WRR reproduction result.",
            "- Do not describe the local locked-method result as exact published reproduction.",
            "- Do not promote OCR near matches, WNP/context flags, or zero-hit method diagnostics into source edits without citable source evidence.",
            "- Raw lane counts are review workload counts, not statistical significance tests.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_exact_gap_priority_packet",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "dashboard": str(args.dashboard),
            "action_summary": str(args.action_summary),
            "row_summary": str(args.row_summary),
            "remaining_summary": str(args.remaining_summary),
            "method_summary": str(args.method_summary),
            "gap_reasons": str(args.gap_reasons),
        },
        "outputs": {
            "csv": str(args.out),
            "summary_csv": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
        "rows": len(rows),
        "summary_rows": len(summary),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def packet_row(
    section: str,
    priority: int,
    item: str,
    value: str,
    status: str,
    evidence_required: str,
    no_input_boundary: str,
    source: Path,
    read: str,
) -> dict[str, object]:
    return {
        "section": section,
        "priority": priority,
        "item": item,
        "value": value,
        "status": status,
        "evidence_required": evidence_required,
        "no_input_boundary": no_input_boundary,
        "source": str(source),
        "read": read,
    }


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def dashboard_value(by_item: dict[str, dict[str, str]], item: str) -> str:
    return by_item.get(item, {}).get("value", "")


def source_row_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    return (
        -int_or_zero(row.get("action_terms", "")),
        -int_or_zero(row.get("residual_pairs", "")),
        int_or_zero(row.get("row_rank", "")),
    )


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def markdown_row(row: dict[str, object]) -> dict[str, str]:
    return {key: markdown_cell(str(value)) for key, value in row.items()}


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
