#!/usr/bin/env python3
"""Build WRR source-transcription row review checklist from evidence packets."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_ROW_SUMMARY = Path(
    "reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv"
)
DEFAULT_OUT = Path(
    "reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv"
)
DEFAULT_MD = Path("docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_source_transcription_row_review_checklist.manifest.json"
)

REVIEW_STATE = "pending_manual_source_lock"
NO_INPUT_BOUNDARY = (
    "No row transcription, source correction, pair exclusion, or method change "
    "is selected by this checklist."
)

FIELDNAMES = [
    "run_label",
    "row_rank",
    "row_number",
    "concept",
    "review_state",
    "action_terms",
    "residual_pairs",
    "frontier_pairs",
    "terms_to_verify",
    "matched_row_terms",
    "row_ocr_name_texts",
    "row_ocr_date_texts",
    "table2_bridge_read",
    "required_source_evidence",
    "required_alignment_evidence",
    "required_decision_record",
    "no_input_boundary",
    "allowed_without_input",
    "next_manual_action",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    row_summary_rows = read_rows(args.row_summary)
    checklist_rows = build_checklist_rows(row_summary_rows)
    write_csv(args.out, checklist_rows)
    write_markdown(args.markdown_out, checklist_rows, args)
    write_manifest(args.manifest_out, args, checklist_rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--row-summary", type=Path, default=DEFAULT_ROW_SUMMARY)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_checklist_rows(
    row_summary_rows: list[dict[str, str]]
) -> list[dict[str, object]]:
    rows = []
    for row in row_summary_rows:
        rows.append(
            {
                "run_label": row.get("run_label", ""),
                "row_rank": int_or_zero(row.get("row_rank", "")),
                "row_number": row.get("row_number", ""),
                "concept": row.get("concept", ""),
                "review_state": REVIEW_STATE,
                "action_terms": int_or_zero(row.get("action_terms", "")),
                "residual_pairs": int_or_zero(row.get("residual_pairs", "")),
                "frontier_pairs": int_or_zero(row.get("frontier_pairs", "")),
                "terms_to_verify": row.get("action_terms_display", ""),
                "matched_row_terms": row.get("row_matched_terms", ""),
                "row_ocr_name_texts": row.get("row_ocr_name_texts", ""),
                "row_ocr_date_texts": row.get("row_ocr_date_texts", ""),
                "table2_bridge_read": row.get("table2_bridge_read", ""),
                "required_source_evidence": (
                    "citable primary Table 2 row image or source-list row "
                    "transcription for this row"
                ),
                "required_alignment_evidence": (
                    "row-number and column alignment evidence tying the cited "
                    "transcription to the imported WRR2 terms"
                ),
                "required_decision_record": (
                    "explicit keep, correct, exclude, or method/pair-universe "
                    "decision recorded outside this checklist"
                ),
                "no_input_boundary": NO_INPUT_BOUNDARY,
                "allowed_without_input": "organize evidence only",
                "next_manual_action": next_manual_action(row),
            }
        )
    rows.sort(
        key=lambda row: (
            int(row["row_rank"]),
            str(row["row_number"]),
        )
    )
    return rows


def next_manual_action(row: dict[str, str]) -> str:
    terms = int_or_zero(row.get("action_terms", ""))
    frontier = int_or_zero(row.get("frontier_pairs", ""))
    if terms > 1 and frontier > 0:
        return "review row image once before individual term decisions"
    if frontier > 0:
        return "review row image before any frontier pair decision"
    return "review after frontier rows unless policy scope changes"


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    total_terms = sum_int(rows, "action_terms")
    total_pairs = sum_int(rows, "residual_pairs")
    total_frontier = sum_int(rows, "frontier_pairs")
    lines = [
        "# WRR Source-Transcription Row Review Checklist",
        "",
        "Status: no-input checklist for row-level source-transcription review.",
        "It does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_source_transcription_row_review_checklist "
            f"--row-summary {args.row_summary} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Row review clusters: {len(rows)}.",
        f"- Source-transcription action terms: {total_terms}.",
        f"- Residual pair links: {total_pairs}.",
        f"- Minimum-frontier pair links: {total_frontier}.",
        f"- Review state: `{REVIEW_STATE}`.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Row Checklist",
        "",
        "| Rank | Row | Concept | State | Terms | Pairs | Frontier | Terms to verify | Next manual action |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {row_rank} | `{row_number}` | `{concept}` | `{review_state}` | "
            "{action_terms} | {residual_pairs} | {frontier_pairs} | {terms} | "
            "{next_manual_action} |".format(
                terms=markdown_code_or_blank(row.get("terms_to_verify", "")),
                **markdown_row(row),
            )
        )
    lines.extend(
        [
            "",
            "## Required Decision Record",
            "",
            "- Cite the primary row image or source-list row transcription used.",
            "- State row and column alignment evidence.",
            "- Record keep, correct, exclude, or method/pair-universe decision outside this checklist.",
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
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_source_transcription_row_review_checklist",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "rows": len(rows),
        "action_terms": sum_int(rows, "action_terms"),
        "residual_pairs": sum_int(rows, "residual_pairs"),
        "frontier_pairs": sum_int(rows, "frontier_pairs"),
        "inputs": {"row_summary": str(args.row_summary)},
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
