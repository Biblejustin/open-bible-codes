#!/usr/bin/env python3
"""Build a WRR residual reconciliation action plan from unique term targets."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_QUEUE = Path("reports/wrr_1994/wrr_residual_term_reconciliation_queue.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_residual_reconciliation_action_plan.csv")
DEFAULT_SUMMARY_OUT = Path(
    "reports/wrr_1994/wrr_residual_reconciliation_action_summary.csv"
)
DEFAULT_MD = Path("docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_residual_reconciliation_action_plan.manifest.json"
)

ACTION_FIELDNAMES = [
    "run_label",
    "action_rank",
    "action_lane",
    "term_id",
    "term",
    "term_side",
    "residual_pairs",
    "frontier_pairs",
    "term_priority_rank",
    "review_buckets",
    "term_ocr_statuses",
    "source_flags",
    "source_queue_rank",
    "source_queue_ocr_status",
    "source_queue_best_variant_hits",
    "source_queue_best_variant_rule",
    "source_review_action",
    "visual_review_action",
    "pair_ids",
    "evidence_required",
    "no_input_boundary",
    "read",
]

SUMMARY_FIELDNAMES = [
    "run_label",
    "action_lane",
    "terms",
    "residual_pairs",
    "frontier_pairs",
    "evidence_required",
    "no_input_boundary",
    "read",
]

LANE_ORDER = {
    "source_policy_or_pair_rule_review": 0,
    "source_transcription_or_row_alignment": 1,
    "page_image_near_match_review": 2,
    "method_or_pair_universe_review": 3,
    "source_queue_join_review": 4,
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    term_rows = read_rows(args.residual_term_queue)
    action_rows = build_action_rows(term_rows)
    summary_rows = build_summary_rows(action_rows)
    write_csv(args.out, ACTION_FIELDNAMES, action_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, action_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, action_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--residual-term-queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_action_rows(term_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in term_rows:
        lane = row.get("reconciliation_need", "") or "source_queue_join_review"
        rows.append(
            {
                "run_label": row.get("run_label", ""),
                "action_rank": 0,
                "action_lane": lane,
                "term_id": row.get("term_id", ""),
                "term": row.get("term", ""),
                "term_side": row.get("term_side", ""),
                "residual_pairs": int_or_zero(row.get("residual_pairs", "")),
                "frontier_pairs": int_or_zero(row.get("frontier_pairs", "")),
                "term_priority_rank": row.get("priority_rank", ""),
                "review_buckets": row.get("review_buckets", ""),
                "term_ocr_statuses": row.get("term_ocr_statuses", ""),
                "source_flags": row.get("source_flags", ""),
                "source_queue_rank": row.get("source_queue_rank", ""),
                "source_queue_ocr_status": row.get("source_queue_ocr_status", ""),
                "source_queue_best_variant_hits": row.get(
                    "source_queue_best_variant_hits", ""
                ),
                "source_queue_best_variant_rule": row.get(
                    "source_queue_best_variant_rule", ""
                ),
                "source_review_action": row.get("source_review_action", ""),
                "visual_review_action": row.get("visual_review_action", ""),
                "pair_ids": row.get("pair_ids", ""),
                "evidence_required": evidence_required(lane),
                "no_input_boundary": no_input_boundary(lane),
                "read": read_for_lane(lane),
            }
        )
    rows.sort(key=action_sort_key)
    for index, row in enumerate(rows, start=1):
        row["action_rank"] = index
    return rows


def build_summary_rows(action_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    if not action_rows:
        return []
    by_lane: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in action_rows:
        by_lane[str(row["action_lane"])].append(row)
    run_label = str(action_rows[0]["run_label"])
    out: list[dict[str, object]] = []
    for lane, rows in sorted(by_lane.items(), key=lambda item: lane_sort_key(item[0])):
        out.append(
            {
                "run_label": run_label,
                "action_lane": lane,
                "terms": len(rows),
                "residual_pairs": sum_int(rows, "residual_pairs"),
                "frontier_pairs": sum_int(rows, "frontier_pairs"),
                "evidence_required": evidence_required(lane),
                "no_input_boundary": no_input_boundary(lane),
                "read": read_for_lane(lane),
            }
        )
    return out


def evidence_required(lane: str) -> str:
    return {
        "source_policy_or_pair_rule_review": (
            "citable source-policy or pair-rule evidence for whether the flagged appellation belongs in the selected pair universe"
        ),
        "source_transcription_or_row_alignment": (
            "primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead"
        ),
        "page_image_near_match_review": (
            "page-image inspection against near-match OCR before treating the term as source text or method blocker"
        ),
        "method_or_pair_universe_review": (
            "method and pair-universe review because OCR already matched but ordinary hits remain absent"
        ),
        "source_queue_join_review": (
            "source-queue join repair before source or method interpretation"
        ),
    }.get(lane, "manual review of unmapped reconciliation lane")


def no_input_boundary(lane: str) -> str:
    return {
        "source_policy_or_pair_rule_review": (
            "keep term in working source; no automatic correction or exclusion without citable rule"
        ),
        "source_transcription_or_row_alignment": (
            "keep imported term; do not correct transcription until primary row evidence is locked"
        ),
        "page_image_near_match_review": (
            "keep imported term; do not treat near OCR as correction without page-image review"
        ),
        "method_or_pair_universe_review": (
            "keep source row; investigate ordinary-hit method or pair universe before source edits"
        ),
        "source_queue_join_review": (
            "do not interpret row until queue join is repaired"
        ),
    }.get(lane, "manual boundary needed before changing source or method state")


def read_for_lane(lane: str) -> str:
    return {
        "source_policy_or_pair_rule_review": (
            "one flagged frontier term can affect source policy, but it cannot be used as an exclusion without a locked rule"
        ),
        "source_transcription_or_row_alignment": (
            "largest residual mass; these are transcription/alignment evidence tasks, not current corrections"
        ),
        "page_image_near_match_review": (
            "small near-match lane should be checked against page images before method work"
        ),
        "method_or_pair_universe_review": (
            "OCR-matched terms probably require method or pair-universe explanation, not source transcription fixes"
        ),
        "source_queue_join_review": (
            "join failure blocks interpretation"
        ),
    }.get(lane, "unmapped lane; review manually")


def write_markdown(
    path: Path,
    action_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    total_terms = len(action_rows)
    total_pairs = sum_int(action_rows, "residual_pairs")
    total_frontier = sum_int(action_rows, "frontier_pairs")
    lines = [
        "# WRR Residual Reconciliation Action Plan",
        "",
        "Status: diagnostic action plan from the residual unique-term queue.",
        "It does not select source corrections, exclude pairs, or reproduce WRR.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_residual_reconciliation_action_plan "
            f"--residual-term-queue {args.residual_term_queue} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Action terms: {total_terms}.",
        f"- Residual pair links: {total_pairs}.",
        f"- Minimum-frontier pair links: {total_frontier}.",
        "",
        "## Action Lanes",
        "",
        "| Action lane | Terms | Residual pairs | Frontier pairs | Evidence required | Boundary |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| `{action_lane}` | {terms} | {residual_pairs} | {frontier_pairs} | "
            "{evidence_required} | {no_input_boundary} |".format(
                **markdown_row(row)
            )
        )
    lines.extend(
        [
            "",
            "## Priority Actions",
            "",
            "| Rank | Lane | Term id | Term | Pairs | Frontier | Source flags | Evidence required |",
            "| ---: | --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in action_rows[:30]:
        lines.append(
            "| {action_rank} | `{action_lane}` | `{term_id}` | `{term}` | "
            "{residual_pairs} | {frontier_pairs} | {flags} | {evidence_required} |".format(
                flags=markdown_code_or_blank(row.get("source_flags", "")),
                **markdown_row(row),
            )
        )
    lines.extend(
        [
            "",
            "## No-Input Boundary",
            "",
            "- This plan is a review work order, not a source correction set.",
            "- Keep all residual terms in the working source until citable row, policy, or method evidence is locked.",
            "- Source-policy flags need citable pair-rule evidence before any source-lock change.",
            "- OCR-matched/no-variant terms should move to method or pair-universe review before source edits.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    action_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_residual_reconciliation_action_plan",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "action_rows": len(action_rows),
        "summary_rows": len(summary_rows),
        "inputs": {
            "residual_term_queue": str(args.residual_term_queue),
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


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def action_sort_key(row: dict[str, object]) -> tuple[int, int, int, str]:
    return (
        lane_sort_key(str(row["action_lane"])),
        -int(row["frontier_pairs"]),
        int_or_zero(str(row["term_priority_rank"])),
        str(row["term_id"]),
    )


def lane_sort_key(lane: str) -> int:
    return LANE_ORDER.get(lane, 99)


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
