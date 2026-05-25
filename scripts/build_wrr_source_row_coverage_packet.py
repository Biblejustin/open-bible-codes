#!/usr/bin/env python3
"""Build WRR source-row visual-triage coverage packet."""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_ROW_CHECKLIST = Path(
    "reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv"
)
DEFAULT_SOURCE_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_source_row_coverage_packet.csv")
DEFAULT_SUMMARY_OUT = Path(
    "reports/wrr_1994/wrr_source_row_coverage_packet_summary.csv"
)
DEFAULT_MD = Path("docs/WRR_SOURCE_ROW_COVERAGE_PACKET.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_source_row_coverage_packet.manifest.json")

TERM_ID_RE = re.compile(r"wrr2_\d+_[a-z]+_\d+")
NO_INPUT_BOUNDARY = (
    "No row transcription, source correction, pair exclusion, or method change "
    "is selected by this coverage packet."
)

FIELDNAMES = [
    "run_label",
    "row_rank",
    "row_number",
    "concept",
    "action_terms",
    "residual_pairs",
    "frontier_pairs",
    "action_term_ids",
    "direct_visual_terms",
    "related_visual_terms",
    "visual_note_count",
    "coverage_state",
    "next_manual_action",
    "no_input_boundary",
]

SUMMARY_FIELDNAMES = ["metric", "value", "read"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    row_checklist = read_rows(args.row_checklist)
    source_queue = read_rows(args.source_queue)
    packet_rows = build_packet_rows(row_checklist, source_queue)
    summary_rows = build_summary_rows(packet_rows, row_checklist, source_queue)
    write_csv(args.out, packet_rows, FIELDNAMES)
    write_csv(args.summary_out, summary_rows, SUMMARY_FIELDNAMES)
    write_markdown(args.markdown_out, packet_rows, summary_rows, source_queue, args)
    write_manifest(args.manifest_out, args, packet_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--row-checklist", type=Path, default=DEFAULT_ROW_CHECKLIST)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_packet_rows(
    row_checklist: list[dict[str, str]], source_queue: list[dict[str, str]]
) -> list[dict[str, object]]:
    visual_by_row = visual_rows_by_row(source_queue)
    rows: list[dict[str, object]] = []
    for row in row_checklist:
        row_number = row.get("row_number", "")
        action_ids = term_ids_from_text(row.get("terms_to_verify", ""))
        visual_rows = visual_by_row.get(row_number, [])
        direct_terms = [
            item.get("term_id", "")
            for item in visual_rows
            if item.get("term_id", "") in action_ids
        ]
        related_terms = [
            item.get("term_id", "")
            for item in visual_rows
            if item.get("term_id", "") and item.get("term_id", "") not in action_ids
        ]
        state = coverage_state(action_ids, direct_terms, related_terms)
        rows.append(
            {
                "run_label": row.get("run_label", ""),
                "row_rank": int_or_zero(row.get("row_rank", "")),
                "row_number": row_number,
                "concept": row.get("concept", ""),
                "action_terms": int_or_zero(row.get("action_terms", "")),
                "residual_pairs": int_or_zero(row.get("residual_pairs", "")),
                "frontier_pairs": int_or_zero(row.get("frontier_pairs", "")),
                "action_term_ids": ";".join(action_ids),
                "direct_visual_terms": ";".join(direct_terms),
                "related_visual_terms": ";".join(related_terms),
                "visual_note_count": len(visual_rows),
                "coverage_state": state,
                "next_manual_action": next_manual_action(
                    state, int_or_zero(row.get("frontier_pairs", ""))
                ),
                "no_input_boundary": NO_INPUT_BOUNDARY,
            }
        )
    rows.sort(key=lambda item: (int(item["row_rank"]), str(item["row_number"])))
    return rows


def build_summary_rows(
    packet_rows: list[dict[str, object]],
    row_checklist: list[dict[str, str]],
    source_queue: list[dict[str, str]],
) -> list[dict[str, object]]:
    row_numbers = {row.get("row_number", "") for row in row_checklist}
    outside_rows = sorted(
        {
            row_number
            for item in visual_rows(source_queue)
            for row_number in split_values(item.get("row_numbers", ""))
            if row_number not in row_numbers
        }
    )
    direct_terms = sum(
        len(split_values(str(row.get("direct_visual_terms", "")))) for row in packet_rows
    )
    rows_with_direct = sum(
        1 for row in packet_rows if split_values(str(row.get("direct_visual_terms", "")))
    )
    related_only = sum(
        1 for row in packet_rows if row.get("coverage_state") == "related_row_visual_triage_only"
    )
    no_related = sum(
        1 for row in packet_rows if row.get("coverage_state") == "no_related_visual_triage"
    )
    return [
        metric("source_rows", len(packet_rows), "source-transcription row clusters"),
        metric("action_terms", sum_int(packet_rows, "action_terms"), "terms requiring row-level review"),
        metric("frontier_pairs", sum_int(packet_rows, "frontier_pairs"), "minimum-frontier pair links"),
        metric(
            "direct_visual_action_terms",
            direct_terms,
            "action terms already covered by visual-triage notes",
        ),
        metric(
            "rows_with_direct_visual_action_term_coverage",
            rows_with_direct,
            "rows with at least one action term covered directly",
        ),
        metric(
            "rows_with_related_visual_triage_only",
            related_only,
            "same row has visual notes, but not for current action terms",
        ),
        metric(
            "rows_with_no_related_visual_triage",
            no_related,
            "no current source-queue visual note for that row",
        ),
        metric(
            "visual_triage_rows_outside_source_transcription_checklist",
            len(outside_rows),
            ";".join(outside_rows),
        ),
    ]


def visual_rows_by_row(
    source_queue: list[dict[str, str]]
) -> dict[str, list[dict[str, str]]]:
    by_row: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in visual_rows(source_queue):
        for row_number in split_values(row.get("row_numbers", "")):
            by_row[row_number].append(row)
    return by_row


def visual_rows(source_queue: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in source_queue if row.get("visual_review_note", "").strip()]


def term_ids_from_text(text: str) -> list[str]:
    return sorted(set(TERM_ID_RE.findall(text)))


def coverage_state(
    action_ids: list[str], direct_terms: list[str], related_terms: list[str]
) -> str:
    if action_ids and len(set(direct_terms)) == len(set(action_ids)):
        return "direct_visual_triage_for_all_action_terms"
    if direct_terms:
        return "partial_direct_visual_triage"
    if related_terms:
        return "related_row_visual_triage_only"
    return "no_related_visual_triage"


def next_manual_action(state: str, frontier_pairs: int) -> str:
    if state == "direct_visual_triage_for_all_action_terms":
        return "review notes against primary row image before locking any source decision"
    if state == "partial_direct_visual_triage":
        return "review remaining action terms directly on the primary row image"
    if state == "related_row_visual_triage_only":
        return "do not transfer related visual notes to action terms; review row image directly"
    if frontier_pairs > 0:
        return "retrieve or review primary row image before any frontier source decision"
    return "review after frontier rows unless policy scope changes"


def write_markdown(
    path: Path,
    packet_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    source_queue: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {str(row["metric"]): row for row in summary_rows}
    direct_terms = summary["direct_visual_action_terms"]["value"]
    related_only = summary["rows_with_related_visual_triage_only"]["value"]
    no_related = summary["rows_with_no_related_visual_triage"]["value"]
    lines = [
        "# WRR Source Row Coverage Packet",
        "",
        "Status: no-input visual-triage coverage packet for WRR source-row review.",
        "It does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_source_row_coverage_packet "
            f"--row-checklist {args.row_checklist} "
            f"--source-queue {args.source_queue} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Source rows: {summary['source_rows']['value']}.",
        f"- Action terms: {summary['action_terms']['value']}.",
        f"- Frontier pairs: {summary['frontier_pairs']['value']}.",
        f"- Direct action-term visual coverage: {direct_terms} terms.",
        f"- Related row visual triage only: {related_only} rows.",
        f"- No related visual triage: {no_related} rows.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Row Coverage",
        "",
        "| Rank | Row | Terms | Frontier | Direct visual terms | Related visual terms | Coverage | Next action |",
        "| ---: | --- | ---: | ---: | --- | --- | --- | --- |",
    ]
    for row in packet_rows:
        lines.append(
            "| {row_rank} | `{row_number}` | {action_terms} | {frontier_pairs} | "
            "{direct} | {related} | `{coverage_state}` | {next_manual_action} |".format(
                direct=markdown_code_or_blank(row.get("direct_visual_terms", "")),
                related=markdown_code_or_blank(row.get("related_visual_terms", "")),
                **markdown_row(row),
            )
        )
    outside = str(
        summary["visual_triage_rows_outside_source_transcription_checklist"]["read"]
    )
    lines.extend(
        [
            "",
            "## Visual-Triage Rows Outside This Checklist",
            "",
            f"- Rows with visual notes outside this source-transcription checklist: `{outside}`.",
            "- These rows can remain useful for page-image, title-prefix, or source-policy review, but they do not cover the current source-transcription action terms directly.",
            "",
            "## Visual Note Boundary",
            "",
            "- Do not transfer related visual notes to action terms.",
            "- Visual notes can identify rows worth reviewing, but they are not locked primary transcriptions.",
            "- No row here changes the working WRR source or excludes a pair automatically.",
            "- Preserve the working source unless a separate decision record selects a source or method change.",
            "",
        ]
    )
    if visual_rows(source_queue):
        lines.extend(
            [
                "## Source-Queue Visual Notes Used",
                "",
                "| Row | Term id | Visual note | Visual action |",
                "| --- | --- | --- | --- |",
            ]
        )
        for row in visual_rows(source_queue):
            lines.append(
                "| {rows} | `{term}` | {note} | {action} |".format(
                    rows=markdown_cell(row.get("row_numbers", "")),
                    term=markdown_cell(row.get("term_id", "")),
                    note=markdown_cell(row.get("visual_review_note", "")),
                    action=markdown_cell(row.get("visual_review_action", "")),
                )
            )
        lines.append("")
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
        "tool": "build_wrr_source_row_coverage_packet",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "rows": len(packet_rows),
        "action_terms": sum_int(packet_rows, "action_terms"),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "inputs": {
            "row_checklist": str(args.row_checklist),
            "source_queue": str(args.source_queue),
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


def metric(name: str, value: object, read: str) -> dict[str, object]:
    return {"metric": name, "value": value, "read": read}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


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
