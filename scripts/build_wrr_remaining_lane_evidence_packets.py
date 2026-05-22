#!/usr/bin/env python3
"""Build evidence packet for remaining WRR residual action lanes."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_ACTION_PLAN = Path("reports/wrr_1994/wrr_residual_reconciliation_action_plan.csv")
DEFAULT_SOURCE_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_ROW_OCR = Path("reports/wrr_1994/wrr_primary_table2_row_ocr_probe.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_remaining_lane_evidence_packet.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv")
DEFAULT_MD = Path("docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_remaining_lane_evidence_packets.manifest.json"
)

TARGET_LANES = {
    "page_image_near_match_review",
    "method_or_pair_universe_review",
}
LANE_ORDER = {
    "page_image_near_match_review": 0,
    "method_or_pair_universe_review": 1,
}
DIAGNOSTIC_BOUNDARY = (
    "No automatic source correction or method change; page-image, method, or "
    "pair-universe evidence must be locked first."
)

PACKET_FIELDNAMES = [
    "run_label",
    "evidence_rank",
    "action_rank",
    "action_lane",
    "term_id",
    "term",
    "concept",
    "row_number",
    "residual_pairs",
    "frontier_pairs",
    "review_buckets",
    "row_ocr_status",
    "row_ocr_near_match_distance",
    "row_ocr_near_match_text",
    "row_ocr_text_normalized",
    "best_variant_hit_count",
    "best_variant_rule",
    "evidence_required",
    "no_input_boundary",
    "evidence_read",
]

SUMMARY_FIELDNAMES = [
    "run_label",
    "action_lane",
    "action_terms",
    "residual_pairs",
    "frontier_pairs",
    "concepts",
    "evidence_required",
    "no_input_boundary",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    action_rows = read_rows(args.action_plan)
    source_rows = read_rows(args.source_queue)
    row_ocr_rows = read_rows(args.row_ocr)
    packet_rows = build_packet_rows(action_rows, source_rows, row_ocr_rows)
    summary_rows = build_summary_rows(packet_rows)
    write_csv(args.out, PACKET_FIELDNAMES, packet_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, packet_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, packet_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--action-plan", type=Path, default=DEFAULT_ACTION_PLAN)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument("--row-ocr", type=Path, default=DEFAULT_ROW_OCR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_packet_rows(
    action_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    row_ocr_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    source_by_term = {row.get("term_id", ""): row for row in source_rows}
    row_ocr_by_term = {row.get("term_id", ""): row for row in row_ocr_rows}
    rows = []
    for action_row in action_rows:
        lane = action_row.get("action_lane", "")
        if lane not in TARGET_LANES:
            continue
        term_id = action_row.get("term_id", "")
        source_row = source_by_term.get(term_id, {})
        ocr_row = row_ocr_by_term.get(term_id, {})
        concept = (
            source_row.get("concepts", "")
            or ocr_row.get("concept", "")
            or concept_from_term_id(term_id)
        )
        rows.append(
            {
                "run_label": action_row.get("run_label", ""),
                "evidence_rank": 0,
                "action_rank": int_or_zero(action_row.get("action_rank", "")),
                "action_lane": lane,
                "term_id": term_id,
                "term": action_row.get("term", ""),
                "concept": concept,
                "row_number": (
                    ocr_row.get("row_number", "")
                    or source_row.get("row_numbers", "")
                    or concept.split()[-1]
                ),
                "residual_pairs": int_or_zero(action_row.get("residual_pairs", "")),
                "frontier_pairs": int_or_zero(action_row.get("frontier_pairs", "")),
                "review_buckets": action_row.get("review_buckets", ""),
                "row_ocr_status": source_row.get(
                    "row_ocr_status", ocr_row.get("row_ocr_status", "")
                ),
                "row_ocr_near_match_distance": source_row.get(
                    "row_ocr_near_match_distance", ""
                ),
                "row_ocr_near_match_text": source_row.get(
                    "row_ocr_near_match_text", ""
                ),
                "row_ocr_text_normalized": ocr_row.get(
                    "row_ocr_text_normalized",
                    source_row.get("row_ocr_text_normalized", ""),
                ),
                "best_variant_hit_count": source_row.get(
                    "best_variant_hit_count",
                    action_row.get("source_queue_best_variant_hits", ""),
                ),
                "best_variant_rule": source_row.get(
                    "best_variant_rule",
                    action_row.get("source_queue_best_variant_rule", ""),
                ),
                "evidence_required": evidence_required(lane),
                "no_input_boundary": DIAGNOSTIC_BOUNDARY,
                "evidence_read": evidence_read(lane),
            }
        )
    rows.sort(
        key=lambda row: (
            LANE_ORDER.get(str(row["action_lane"]), 99),
            -int(row["frontier_pairs"]),
            int(row["action_rank"]),
            str(row["term_id"]),
        )
    )
    for index, row in enumerate(rows, start=1):
        row["evidence_rank"] = index
    return rows


def build_summary_rows(packet_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    if not packet_rows:
        return []
    by_lane: dict[str, list[dict[str, object]]] = {}
    for row in packet_rows:
        by_lane.setdefault(str(row["action_lane"]), []).append(row)
    run_label = str(packet_rows[0].get("run_label", ""))
    rows = []
    for lane, lane_rows in sorted(by_lane.items(), key=lambda item: LANE_ORDER[item[0]]):
        rows.append(
            {
                "run_label": run_label,
                "action_lane": lane,
                "action_terms": len(lane_rows),
                "residual_pairs": sum_int(lane_rows, "residual_pairs"),
                "frontier_pairs": sum_int(lane_rows, "frontier_pairs"),
                "concepts": len({str(row.get("concept", "")) for row in lane_rows}),
                "evidence_required": evidence_required(lane),
                "no_input_boundary": DIAGNOSTIC_BOUNDARY,
                "read": evidence_read(lane),
            }
        )
    return rows


def write_markdown(
    path: Path,
    packet_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    total_terms = len(packet_rows)
    total_pairs = sum_int(packet_rows, "residual_pairs")
    total_frontier = sum_int(packet_rows, "frontier_pairs")
    lines = [
        "# WRR Remaining-Lane Evidence Packets",
        "",
        "Status: diagnostic evidence packet for page-image and method residual lanes.",
        "It does not choose source corrections, method changes, or pair exclusions.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_remaining_lane_evidence_packets "
            f"--action-plan {args.action_plan} "
            f"--source-queue {args.source_queue} "
            f"--row-ocr {args.row_ocr} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Remaining-lane action terms: {total_terms}.",
        f"- Residual pair links: {total_pairs}.",
        f"- Minimum-frontier pair links: {total_frontier}.",
        f"- Boundary: {DIAGNOSTIC_BOUNDARY}",
        "",
        "## Lane Summary",
        "",
        "| Lane | Terms | Pairs | Frontier | Concepts | Evidence required |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| `{action_lane}` | {action_terms} | {residual_pairs} | {frontier_pairs} | "
            "{concepts} | {evidence_required} |".format(**markdown_row(row))
        )
    lines.extend(
        [
            "",
            "## Action Terms",
            "",
            "| Rank | Lane | Term id | Term | Row | Pairs | Frontier | OCR status | Near match | Evidence read |",
            "| ---: | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |",
        ]
    )
    for row in packet_rows:
        near = near_match_display(row)
        lines.append(
            "| {evidence_rank} | `{action_lane}` | `{term_id}` | `{term}` | `{row_number}` | "
            "{residual_pairs} | {frontier_pairs} | {row_ocr_status} | {near} | {evidence_read} |".format(
                near=near,
                **markdown_row(row),
            )
        )
    lines.extend(
        [
            "",
            "## No-Input Boundary",
            "",
            "- Page-image near-match rows need page-image review before source edits.",
            "- OCR-matched method rows need method or pair-universe explanation before source edits.",
            "- No remaining-lane term changes the working source automatically.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    packet_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_remaining_lane_evidence_packets",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "packet_rows": len(packet_rows),
        "summary_rows": len(summary_rows),
        "inputs": {
            "action_plan": str(args.action_plan),
            "source_queue": str(args.source_queue),
            "row_ocr": str(args.row_ocr),
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


def evidence_required(lane: str) -> str:
    if lane == "page_image_near_match_review":
        return "page-image inspection against near-match OCR"
    if lane == "method_or_pair_universe_review":
        return "method or pair-universe review for OCR-matched missing ordinary hits"
    return "manual evidence review"


def evidence_read(lane: str) -> str:
    if lane == "page_image_near_match_review":
        return "near OCR exists, but page image must decide whether it is source evidence"
    if lane == "method_or_pair_universe_review":
        return "OCR matched the imported term; investigate method or pair universe before source edits"
    return "manual review needed"


def near_match_display(row: dict[str, object]) -> str:
    distance = str(row.get("row_ocr_near_match_distance", ""))
    text = str(row.get("row_ocr_near_match_text", ""))
    if not distance and not text:
        return ""
    return f"`d={markdown_cell(distance)} {markdown_cell(text)}`"


def concept_from_term_id(term_id: str) -> str:
    parts = term_id.split("_")
    return f"WRR2 {parts[1]}" if len(parts) > 1 else ""


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
