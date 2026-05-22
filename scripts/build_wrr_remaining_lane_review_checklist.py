#!/usr/bin/env python3
"""Build WRR remaining-lane review checklist from page/method evidence packet."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_PACKET = Path("reports/wrr_1994/wrr_remaining_lane_evidence_packet.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_remaining_lane_review_checklist.csv")
DEFAULT_MD = Path("docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_remaining_lane_review_checklist.manifest.json"
)

NO_INPUT_BOUNDARY = (
    "No source correction, method change, or pair exclusion is selected by "
    "this checklist."
)

FIELDNAMES = [
    "run_label",
    "checklist_rank",
    "action_lane",
    "review_state",
    "term_id",
    "term",
    "concept",
    "row_number",
    "residual_pairs",
    "frontier_pairs",
    "row_ocr_status",
    "near_match",
    "visual_review_note",
    "evidence_required",
    "required_decision_record",
    "no_input_boundary",
    "allowed_without_input",
    "next_manual_action",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    packet_rows = read_rows(args.packet)
    summary_rows = read_rows(args.summary)
    checklist_rows = build_checklist_rows(packet_rows)
    write_csv(args.out, checklist_rows)
    write_markdown(args.markdown_out, checklist_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, checklist_rows, summary_rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_checklist_rows(packet_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for row in packet_rows:
        lane = row.get("action_lane", "")
        rows.append(
            {
                "run_label": row.get("run_label", ""),
                "checklist_rank": int_or_zero(row.get("evidence_rank", "")),
                "action_lane": lane,
                "review_state": review_state(lane),
                "term_id": row.get("term_id", ""),
                "term": row.get("term", ""),
                "concept": row.get("concept", ""),
                "row_number": row.get("row_number", ""),
                "residual_pairs": int_or_zero(row.get("residual_pairs", "")),
                "frontier_pairs": int_or_zero(row.get("frontier_pairs", "")),
                "row_ocr_status": row.get("row_ocr_status", ""),
                "near_match": near_match(row),
                "visual_review_note": row.get("visual_review_note", ""),
                "evidence_required": row.get("evidence_required", ""),
                "required_decision_record": required_decision_record(lane),
                "no_input_boundary": NO_INPUT_BOUNDARY,
                "allowed_without_input": "organize evidence only",
                "next_manual_action": next_manual_action(row),
            }
        )
    rows.sort(
        key=lambda row: (
            lane_order(str(row["action_lane"])),
            -int(row["frontier_pairs"]),
            int(row["checklist_rank"]),
            str(row["term_id"]),
        )
    )
    for index, row in enumerate(rows, start=1):
        row["checklist_rank"] = index
    return rows


def review_state(lane: str) -> str:
    if lane == "page_image_near_match_review":
        return "pending_page_image_lock"
    if lane == "method_or_pair_universe_review":
        return "pending_method_pair_universe_lock"
    return "pending_manual_lock"


def required_decision_record(lane: str) -> str:
    if lane == "page_image_near_match_review":
        return "explicit page-image transcription decision with cited image evidence"
    if lane == "method_or_pair_universe_review":
        return "explicit method or pair-universe decision explaining zero ordinary hits"
    return "explicit manual decision record"


def next_manual_action(row: dict[str, str]) -> str:
    lane = row.get("action_lane", "")
    if lane == "page_image_near_match_review":
        return "inspect page image before any source correction"
    if lane == "method_or_pair_universe_review":
        if int_or_zero(row.get("frontier_pairs", "")) > 0:
            return "resolve method or pair universe before frontier pair decision"
        return "review after frontier method rows unless scope changes"
    return "manual review required"


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    total_terms = len(rows)
    total_pairs = sum_int(rows, "residual_pairs")
    total_frontier = sum_int(rows, "frontier_pairs")
    lines = [
        "# WRR Remaining-Lane Review Checklist",
        "",
        "Status: no-input checklist for page-image and method/pair-universe review.",
        "It does not choose source corrections, method changes, or pair exclusions.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_remaining_lane_review_checklist "
            f"--packet {args.packet} "
            f"--summary {args.summary} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Remaining-lane checklist terms: {total_terms}.",
        f"- Residual pair links: {total_pairs}.",
        f"- Minimum-frontier pair links: {total_frontier}.",
        "- Page-image terms: 3.",
        "- Method/pair-universe terms: 11.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Lane Summary",
        "",
        "| Lane | Terms | Pairs | Frontier | Evidence required |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| `{action_lane}` | {action_terms} | {residual_pairs} | "
            "{frontier_pairs} | {evidence_required} |".format(**markdown_row(row))
        )
    lines.extend(
        [
            "",
            "## Checklist",
            "",
            "| Rank | Lane | State | Term id | Term | Row | Pairs | Frontier | Near match | Next manual action |",
            "| ---: | --- | --- | --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| {checklist_rank} | `{action_lane}` | `{review_state}` | `{term_id}` | "
            "`{term}` | `{row_number}` | {residual_pairs} | {frontier_pairs} | "
            "{near} | {next_manual_action} |".format(
                near=markdown_code_or_blank(row.get("near_match", "")),
                **markdown_row(row),
            )
        )
    lines.extend(
        [
            "",
            "## Required Decision Record",
            "",
            "- Page-image near-match rows need cited page-image transcription evidence.",
            "- Method rows need an explicit method or pair-universe explanation for zero ordinary hits.",
            "- Preserve the working source until that decision record exists.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_remaining_lane_review_checklist",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "rows": len(rows),
        "summary_rows": len(summary_rows),
        "residual_pairs": sum_int(rows, "residual_pairs"),
        "frontier_pairs": sum_int(rows, "frontier_pairs"),
        "inputs": {
            "packet": str(args.packet),
            "summary": str(args.summary),
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


def near_match(row: dict[str, str]) -> str:
    distance = row.get("row_ocr_near_match_distance", "")
    text = row.get("row_ocr_near_match_text", "")
    if distance == "" and text == "":
        return ""
    return f"d={distance} {text}".strip()


def lane_order(lane: str) -> int:
    if lane == "page_image_near_match_review":
        return 0
    if lane == "method_or_pair_universe_review":
        return 1
    return 99


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
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


def markdown_code_or_blank(value: object) -> str:
    text = markdown_cell(value)
    return f"`{text}`" if text else ""


if __name__ == "__main__":
    raise SystemExit(main())
