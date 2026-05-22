#!/usr/bin/env python3
"""Build source-transcription evidence packet for WRR residual action targets."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_ACTION_PLAN = Path("reports/wrr_1994/wrr_residual_reconciliation_action_plan.csv")
DEFAULT_SOURCE_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_ROW_OCR = Path("reports/wrr_1994/wrr_primary_table2_row_ocr_probe.csv")
DEFAULT_TABLE2_BRIDGE = Path("reports/wrr_1994/wrr_table2_source_bridge.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_source_transcription_evidence_packet.csv")
DEFAULT_ROW_SUMMARY_OUT = Path(
    "reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv"
)
DEFAULT_MD = Path("docs/WRR_SOURCE_TRANSCRIPTION_EVIDENCE_PACKET.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_source_transcription_evidence_packet.manifest.json"
)

TARGET_LANE = "source_transcription_or_row_alignment"
DIAGNOSTIC_BOUNDARY = (
    "No automatic source correction; primary row transcription or row-alignment "
    "evidence must be locked before changing imported terms."
)

PACKET_FIELDNAMES = [
    "run_label",
    "evidence_rank",
    "action_rank",
    "term_id",
    "term",
    "concept",
    "row_number",
    "residual_pairs",
    "frontier_pairs",
    "review_buckets",
    "row_ocr_status",
    "row_ocr_text_normalized",
    "best_variant_hit_count",
    "best_variant_rule",
    "row_matched_terms",
    "row_action_not_matched_terms",
    "table2_bridge_read",
    "evidence_required",
    "no_input_boundary",
    "evidence_read",
]

ROW_SUMMARY_FIELDNAMES = [
    "run_label",
    "row_rank",
    "row_number",
    "concept",
    "action_terms",
    "residual_pairs",
    "frontier_pairs",
    "action_term_ids",
    "action_terms_display",
    "row_matched_terms",
    "row_action_not_matched_terms",
    "row_ocr_name_texts",
    "row_ocr_date_texts",
    "table2_bridge_read",
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
    table2_bridge_rows = read_rows(args.table2_bridge)
    packet_rows = build_packet_rows(
        action_rows, source_rows, row_ocr_rows, table2_bridge_rows
    )
    row_summary_rows = build_row_summary_rows(packet_rows, row_ocr_rows)
    write_csv(args.out, PACKET_FIELDNAMES, packet_rows)
    write_csv(args.row_summary_out, ROW_SUMMARY_FIELDNAMES, row_summary_rows)
    write_markdown(args.markdown_out, packet_rows, row_summary_rows, args)
    write_manifest(args.manifest_out, args, packet_rows, row_summary_rows, started)
    print(args.out)
    print(args.row_summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--action-plan", type=Path, default=DEFAULT_ACTION_PLAN)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument("--row-ocr", type=Path, default=DEFAULT_ROW_OCR)
    parser.add_argument("--table2-bridge", type=Path, default=DEFAULT_TABLE2_BRIDGE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--row-summary-out", type=Path, default=DEFAULT_ROW_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_packet_rows(
    action_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    row_ocr_rows: list[dict[str, str]],
    table2_bridge_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    source_by_term = {row.get("term_id", ""): row for row in source_rows}
    row_ocr_by_term = {row.get("term_id", ""): row for row in row_ocr_rows}
    row_ocr_by_concept = group_by(row_ocr_rows, "concept")
    rows = []
    for action_row in action_rows:
        if action_row.get("action_lane") != TARGET_LANE:
            continue
        term_id = action_row.get("term_id", "")
        source_row = source_by_term.get(term_id, {})
        ocr_row = row_ocr_by_term.get(term_id, {})
        concept = (
            source_row.get("concepts", "")
            or ocr_row.get("concept", "")
            or concept_from_term_id(term_id)
        )
        concept_ocr_rows = row_ocr_by_concept.get(concept, [])
        row_number = (
            ocr_row.get("row_number", "")
            or source_row.get("row_numbers", "")
            or concept.split()[-1]
        )
        rows.append(
            {
                "run_label": action_row.get("run_label", ""),
                "evidence_rank": 0,
                "action_rank": int_or_zero(action_row.get("action_rank", "")),
                "term_id": term_id,
                "term": action_row.get("term", ""),
                "concept": concept,
                "row_number": row_number,
                "residual_pairs": int_or_zero(action_row.get("residual_pairs", "")),
                "frontier_pairs": int_or_zero(action_row.get("frontier_pairs", "")),
                "review_buckets": action_row.get("review_buckets", ""),
                "row_ocr_status": source_row.get(
                    "row_ocr_status", ocr_row.get("row_ocr_status", "")
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
                "row_matched_terms": row_terms(concept_ocr_rows, "matched"),
                "row_action_not_matched_terms": "",
                "table2_bridge_read": table2_bridge_read(table2_bridge_rows, concept),
                "evidence_required": (
                    "primary Table 2 row transcription or row-alignment evidence"
                ),
                "no_input_boundary": DIAGNOSTIC_BOUNDARY,
                "evidence_read": evidence_read(action_row, source_row),
            }
        )
    action_ids_by_concept = defaultdict(set)
    for row in rows:
        action_ids_by_concept[str(row["concept"])].add(str(row["term_id"]))
    for row in rows:
        concept_rows = row_ocr_by_concept.get(str(row["concept"]), [])
        row["row_action_not_matched_terms"] = row_terms(
            [
                ocr_row
                for ocr_row in concept_rows
                if ocr_row.get("term_id", "") in action_ids_by_concept[str(row["concept"])]
            ],
            "not_matched",
        )
    rows.sort(
        key=lambda row: (
            -int(row["frontier_pairs"]),
            int(row["action_rank"]),
            str(row["term_id"]),
        )
    )
    for index, row in enumerate(rows, start=1):
        row["evidence_rank"] = index
    return rows


def build_row_summary_rows(
    packet_rows: list[dict[str, object]],
    row_ocr_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    ocr_by_concept = group_by(row_ocr_rows, "concept")
    by_concept: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in packet_rows:
        by_concept[str(row["concept"])].append(row)
    out = []
    for concept, rows in by_concept.items():
        first = rows[0]
        ocr_rows = ocr_by_concept.get(concept, [])
        out.append(
            {
                "run_label": str(first.get("run_label", "")),
                "row_rank": 0,
                "row_number": str(first.get("row_number", "")),
                "concept": concept,
                "action_terms": len(rows),
                "residual_pairs": sum_int(rows, "residual_pairs"),
                "frontier_pairs": sum_int(rows, "frontier_pairs"),
                "action_term_ids": join_nonempty(row.get("term_id", "") for row in rows),
                "action_terms_display": join_nonempty(
                    f"{row.get('term_id', '')} {row.get('term', '')}" for row in rows
                ),
                "row_matched_terms": row_terms(ocr_rows, "matched"),
                "row_action_not_matched_terms": str(
                    rows[0].get("row_action_not_matched_terms", "")
                ),
                "row_ocr_name_texts": unique_column_reads(ocr_rows, "name"),
                "row_ocr_date_texts": unique_column_reads(ocr_rows, "date"),
                "table2_bridge_read": str(first.get("table2_bridge_read", "")),
                "evidence_required": (
                    "primary Table 2 row transcription or row-alignment evidence"
                ),
                "no_input_boundary": DIAGNOSTIC_BOUNDARY,
                "read": row_read(rows),
            }
        )
    out.sort(
        key=lambda row: (
            -int(row["frontier_pairs"]),
            -int(row["residual_pairs"]),
            str(row["row_number"]),
        )
    )
    for index, row in enumerate(out, start=1):
        row["row_rank"] = index
    return out


def write_markdown(
    path: Path,
    packet_rows: list[dict[str, object]],
    row_summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    total_terms = len(packet_rows)
    total_pairs = sum_int(packet_rows, "residual_pairs")
    total_frontier = sum_int(packet_rows, "frontier_pairs")
    lines = [
        "# WRR Source-Transcription Evidence Packet",
        "",
        "Status: diagnostic evidence packet for source-transcription residual terms.",
        "It does not choose source corrections, row edits, or pair exclusions.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_source_transcription_evidence_packet "
            f"--action-plan {args.action_plan} "
            f"--source-queue {args.source_queue} "
            f"--row-ocr {args.row_ocr} "
            f"--table2-bridge {args.table2_bridge} "
            f"--out {args.out} "
            f"--row-summary-out {args.row_summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Source-transcription action terms: {total_terms}.",
        f"- Residual pair links: {total_pairs}.",
        f"- Minimum-frontier pair links: {total_frontier}.",
        f"- Row clusters: {len(row_summary_rows)}.",
        "- Evidence target: primary Table 2 row transcription or row-alignment evidence.",
        f"- Boundary: {DIAGNOSTIC_BOUNDARY}",
        "",
        "## Priority Row Clusters",
        "",
        "| Rank | Row | Concept | Terms | Pairs | Frontier | Matched row terms | Action terms not matched |",
        "| ---: | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in row_summary_rows:
        lines.append(
            "| {row_rank} | `{row_number}` | `{concept}` | {action_terms} | "
            "{residual_pairs} | {frontier_pairs} | {matched} | {not_matched} |".format(
                matched=markdown_code_or_blank(row.get("row_matched_terms", "")),
                not_matched=markdown_code_or_blank(
                    row.get("row_action_not_matched_terms", "")
                ),
                **markdown_row(row),
            )
        )
    lines.extend(
        [
            "",
            "## Priority Terms",
            "",
            "| Rank | Action rank | Term id | Term | Row | Pairs | Frontier | OCR status | Variant hits | Evidence read |",
            "| ---: | ---: | --- | --- | --- | ---: | ---: | --- | ---: | --- |",
        ]
    )
    for row in packet_rows:
        lines.append(
            "| {evidence_rank} | {action_rank} | `{term_id}` | `{term}` | `{row_number}` | "
            "{residual_pairs} | {frontier_pairs} | {row_ocr_status} | "
            "{best_variant_hit_count} | {evidence_read} |".format(**markdown_row(row))
        )
    lines.extend(
        [
            "",
            "## No-Input Boundary",
            "",
            "- This packet is a row-transcription work order, not a correction set.",
            "- Keep imported terms until citable primary row or row-alignment evidence is locked.",
            "- No simple variant lead means do not infer a replacement from ordinary Genesis hits.",
            "- Rows with multiple unresolved terms should be reviewed once by row, not term-by-term in isolation.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    packet_rows: list[dict[str, object]],
    row_summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_source_transcription_evidence_packet",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "packet_rows": len(packet_rows),
        "row_summary_rows": len(row_summary_rows),
        "inputs": {
            "action_plan": str(args.action_plan),
            "source_queue": str(args.source_queue),
            "row_ocr": str(args.row_ocr),
            "table2_bridge": str(args.table2_bridge),
        },
        "outputs": {
            "out": str(args.out),
            "row_summary_out": str(args.row_summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def row_terms(rows: list[dict[str, str]], status: str) -> str:
    return join_nonempty(
        f"{row.get('term_id', '')} {row.get('michigan_term', '')}"
        for row in rows
        if row.get("row_ocr_status", "") == status
    )


def unique_column_reads(rows: list[dict[str, str]], column: str) -> str:
    values = []
    for row in rows:
        if row.get("column", "") != column:
            continue
        value = row.get("row_ocr_text_normalized", "")
        if value and value not in values:
            values.append(value)
    return ";".join(values)


def table2_bridge_read(rows: list[dict[str, str]], concept: str) -> str:
    row_number = concept.split()[-1].lstrip("0")
    for row in rows:
        if row.get("row_number", "").lstrip("0") == row_number:
            return row.get("current_read", "")
    return ""


def evidence_read(action_row: dict[str, str], source_row: dict[str, str]) -> str:
    hits = source_row.get(
        "best_variant_hit_count", action_row.get("source_queue_best_variant_hits", "")
    )
    if hits == "0":
        return (
            "no simple variant lead; needs primary row transcription or "
            "row-alignment evidence before any source edit"
        )
    return "source queue needs primary row evidence before any source edit"


def row_read(rows: list[dict[str, object]]) -> str:
    if len(rows) > 1:
        return "multi-term row cluster; review row image/alignment once before term edits"
    return "single-term row cluster; still needs primary row transcription evidence"


def concept_from_term_id(term_id: str) -> str:
    parts = term_id.split("_")
    return f"WRR2 {parts[1]}" if len(parts) > 1 else ""


def group_by(rows: list[dict[str, str]], field: str) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        out[row.get(field, "")].append(row)
    return out


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


def join_nonempty(values) -> str:
    return ";".join(str(value) for value in values if value)


def markdown_row(row: dict[str, object]) -> dict[str, str]:
    return {key: markdown_cell(value) for key, value in row.items()}


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def markdown_code_or_blank(value: object) -> str:
    text = markdown_cell(value)
    return f"`{text}`" if text else ""


if __name__ == "__main__":
    raise SystemExit(main())
