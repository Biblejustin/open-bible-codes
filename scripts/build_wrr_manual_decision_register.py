#!/usr/bin/env python3
"""Build consolidated WRR manual-decision register from no-input checklists."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_SOURCE_POLICY = Path(
    "reports/wrr_1994/wrr_source_policy_review_checklist.csv"
)
DEFAULT_ROW_CHECKLIST = Path(
    "reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv"
)
DEFAULT_REMAINING = Path("reports/wrr_1994/wrr_remaining_lane_review_checklist.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_manual_decision_register.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/wrr_manual_decision_register_summary.csv")
DEFAULT_MD = Path("docs/WRR_MANUAL_DECISION_REGISTER.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_manual_decision_register.manifest.json"
)

NO_INPUT_BOUNDARY = (
    "No source correction, row transcription, pair exclusion, replacement lock, "
    "or method change is selected by this register."
)

FIELDNAMES = [
    "decision_rank",
    "decision_lane",
    "review_state",
    "decision_target",
    "concept",
    "row_number",
    "term_id",
    "term",
    "action_terms",
    "residual_pairs",
    "frontier_pairs",
    "required_decision_record",
    "source_checklist",
    "no_input_boundary",
    "allowed_without_input",
    "next_manual_action",
]

SUMMARY_FIELDNAMES = [
    "decision_lane",
    "decision_rows",
    "action_terms",
    "residual_pairs",
    "frontier_pairs",
    "review_state",
]

SOURCE_POLICY_DOC = "docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md"
ROW_CHECKLIST_DOC = "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md"
REMAINING_DOC = "docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md"


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    source_rows = read_rows(args.source_policy)
    row_rows = read_rows(args.row_checklist)
    remaining_rows = read_rows(args.remaining)
    register_rows = build_register_rows(source_rows, row_rows, remaining_rows)
    summary_rows = build_summary_rows(register_rows)
    write_csv(args.out, FIELDNAMES, register_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, register_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, register_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-policy", type=Path, default=DEFAULT_SOURCE_POLICY)
    parser.add_argument("--row-checklist", type=Path, default=DEFAULT_ROW_CHECKLIST)
    parser.add_argument("--remaining", type=Path, default=DEFAULT_REMAINING)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_register_rows(
    source_rows: list[dict[str, str]],
    row_rows: list[dict[str, str]],
    remaining_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    rows.extend(source_policy_rows(source_rows))
    rows.extend(row_checklist_rows(row_rows))
    rows.extend(remaining_lane_rows(remaining_rows))
    rows.sort(
        key=lambda row: (
            lane_order(str(row["decision_lane"])),
            -int(row["frontier_pairs"]),
            str(row["row_number"]),
            str(row["term_id"]),
        )
    )
    for index, row in enumerate(rows, start=1):
        row["decision_rank"] = index
    return rows


def source_policy_rows(source_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for row in source_rows:
        rows.append(
            {
                "decision_rank": 0,
                "decision_lane": "source_policy_pair_rule",
                "review_state": row.get("review_state", ""),
                "decision_target": "Chelm source-policy/pair-rule target",
                "concept": row.get("concept", ""),
                "row_number": row_number_from_term_id(row.get("term_id", "")),
                "term_id": row.get("term_id", ""),
                "term": row.get("term", ""),
                "action_terms": 1,
                "residual_pairs": int_or_zero(row.get("residual_pairs", "")),
                "frontier_pairs": int_or_zero(row.get("frontier_pairs", "")),
                "required_decision_record": row.get("required_decision_record", ""),
                "source_checklist": SOURCE_POLICY_DOC,
                "no_input_boundary": NO_INPUT_BOUNDARY,
                "allowed_without_input": "organize evidence only",
                "next_manual_action": row.get("next_manual_action", ""),
            }
        )
    return rows


def row_checklist_rows(row_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for row in row_rows:
        rows.append(
            {
                "decision_rank": 0,
                "decision_lane": "source_transcription_row_cluster",
                "review_state": row.get("review_state", ""),
                "decision_target": f"row {row.get('row_number', '')}",
                "concept": row.get("concept", ""),
                "row_number": row.get("row_number", ""),
                "term_id": "",
                "term": row.get("terms_to_verify", ""),
                "action_terms": int_or_zero(row.get("action_terms", "")),
                "residual_pairs": int_or_zero(row.get("residual_pairs", "")),
                "frontier_pairs": int_or_zero(row.get("frontier_pairs", "")),
                "required_decision_record": row.get("required_decision_record", ""),
                "source_checklist": ROW_CHECKLIST_DOC,
                "no_input_boundary": NO_INPUT_BOUNDARY,
                "allowed_without_input": "organize evidence only",
                "next_manual_action": row.get("next_manual_action", ""),
            }
        )
    return rows


def remaining_lane_rows(remaining_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for row in remaining_rows:
        rows.append(
            {
                "decision_rank": 0,
                "decision_lane": remaining_decision_lane(row.get("action_lane", "")),
                "review_state": row.get("review_state", ""),
                "decision_target": row.get("term_id", ""),
                "concept": row.get("concept", ""),
                "row_number": row.get("row_number", ""),
                "term_id": row.get("term_id", ""),
                "term": row.get("term", ""),
                "action_terms": 1,
                "residual_pairs": int_or_zero(row.get("residual_pairs", "")),
                "frontier_pairs": int_or_zero(row.get("frontier_pairs", "")),
                "required_decision_record": row.get("required_decision_record", ""),
                "source_checklist": REMAINING_DOC,
                "no_input_boundary": NO_INPUT_BOUNDARY,
                "allowed_without_input": "organize evidence only",
                "next_manual_action": row.get("next_manual_action", ""),
            }
        )
    return rows


def build_summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    lanes = sorted({str(row["decision_lane"]) for row in rows}, key=lane_order)
    summary = []
    for lane in lanes:
        lane_rows = [row for row in rows if row["decision_lane"] == lane]
        states = sorted({str(row["review_state"]) for row in lane_rows})
        summary.append(
            {
                "decision_lane": lane,
                "decision_rows": len(lane_rows),
                "action_terms": sum_int(lane_rows, "action_terms"),
                "residual_pairs": sum_int(lane_rows, "residual_pairs"),
                "frontier_pairs": sum_int(lane_rows, "frontier_pairs"),
                "review_state": ";".join(states),
            }
        )
    return summary


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    lane_counts = Counter(str(row["decision_lane"]) for row in rows)
    lines = [
        "# WRR Manual Decision Register",
        "",
        "Status: consolidated no-input register for WRR manual-lock decisions.",
        "It does not choose source corrections, row transcriptions, pair exclusions, replacement locks, or method changes.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_manual_decision_register "
            f"--source-policy {args.source_policy} "
            f"--row-checklist {args.row_checklist} "
            f"--remaining {args.remaining} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Manual decision rows: {len(rows)}.",
        f"- Action terms represented: {sum_int(rows, 'action_terms')}.",
        f"- Residual pair links represented: {sum_int(rows, 'residual_pairs')}.",
        f"- Minimum-frontier pair links represented: {sum_int(rows, 'frontier_pairs')}.",
        f"- Source-policy/pair-rule decision rows: {lane_counts['source_policy_pair_rule']}.",
        f"- Source-transcription row-cluster decision rows: {lane_counts['source_transcription_row_cluster']}.",
        f"- Page-image decision rows: {lane_counts['page_image_near_match']}.",
        f"- Method/pair-universe decision rows: {lane_counts['method_pair_universe']}.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Lane Summary",
        "",
        "| Lane | Decisions | Terms | Pairs | Frontier | State |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| `{decision_lane}` | {decision_rows} | {action_terms} | "
            "{residual_pairs} | {frontier_pairs} | `{review_state}` |".format(
                **markdown_row(row)
            )
        )
    lines.extend(
        [
            "",
            "## Decision Register",
            "",
            "| Rank | Lane | State | Target | Concept | Row | Terms | Pairs | Frontier | Checklist | Next manual action |",
            "| ---: | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| {decision_rank} | `{decision_lane}` | `{review_state}` | "
            "`{decision_target}` | `{concept}` | `{row_number}` | "
            "{action_terms} | {residual_pairs} | {frontier_pairs} | "
            "`{source_checklist}` | {next_manual_action} |".format(
                **markdown_row(row)
            )
        )
    lines.extend(
        [
            "",
            "## Required Decision Records",
            "",
            "- Source-policy/pair-rule rows need citable source and pair-rule evidence.",
            "- Source-transcription row clusters need cited row image or source-list transcription plus row/column alignment evidence.",
            "- Page-image rows need cited page-image transcription evidence.",
            "- Method/pair-universe rows need an explicit explanation for zero ordinary hits.",
            "- Preserve the working source until those decision records exist.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_manual_decision_register",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "rows": len(rows),
        "summary_rows": len(summary_rows),
        "action_terms": sum_int(rows, "action_terms"),
        "residual_pairs": sum_int(rows, "residual_pairs"),
        "frontier_pairs": sum_int(rows, "frontier_pairs"),
        "inputs": {
            "source_policy": str(args.source_policy),
            "row_checklist": str(args.row_checklist),
            "remaining": str(args.remaining),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def remaining_decision_lane(action_lane: str) -> str:
    if action_lane == "page_image_near_match_review":
        return "page_image_near_match"
    if action_lane == "method_or_pair_universe_review":
        return "method_pair_universe"
    return action_lane or "remaining_lane"


def lane_order(lane: str) -> int:
    return {
        "source_policy_pair_rule": 0,
        "source_transcription_row_cluster": 1,
        "page_image_near_match": 2,
        "method_pair_universe": 3,
    }.get(lane, 99)


def row_number_from_term_id(term_id: str) -> str:
    parts = term_id.split("_")
    if len(parts) >= 2:
        return parts[1]
    return ""


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sum_int(rows: list[dict[str, object]], field: str) -> int:
    return sum(int_or_zero(str(row.get(field, ""))) for row in rows)


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def markdown_row(row: dict[str, object]) -> dict[str, str]:
    return {key: markdown_cell(value) for key, value in row.items()}


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


if __name__ == "__main__":
    raise SystemExit(main())
