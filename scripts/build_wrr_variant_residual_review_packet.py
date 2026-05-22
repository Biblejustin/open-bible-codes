#!/usr/bin/env python3
"""Build a WRR residual review packet after the simple-variant upper bound."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_BLOCKED_PAIRS = Path("reports/wrr_1994/wrr_defined_gap_blocked_pairs.csv")
DEFAULT_VARIANT_IMPACT = Path("reports/wrr_1994/wrr_variant_gap_impact.csv")
DEFAULT_SOURCE_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_UPPER_BOUND = Path("reports/wrr_1994/wrr_variant_gap_upper_bound.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_variant_residual_review_packet.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/wrr_variant_residual_review_summary.csv")
DEFAULT_MD = Path("docs/WRR_VARIANT_RESIDUAL_REVIEW_PACKET.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_variant_residual_review_packet.manifest.json"
)

ALL_VARIANT = "all_blocking_terms_have_variant_hit"
SOME_VARIANT = "some_blocking_terms_have_variant_hit"
NO_VARIANT = "no_blocking_term_variant_hit"

DETAIL_FIELDNAMES = [
    "run_label",
    "review_rank",
    "within_minimum_residual_frontier",
    "impact_status",
    "pair_id",
    "concept",
    "candidate_lane",
    "reason",
    "row_ocr_pair_status",
    "unresolved_term_ids",
    "unresolved_terms",
    "unresolved_term_sides",
    "unresolved_term_buckets",
    "unresolved_term_ocr_statuses",
    "unresolved_source_flags",
    "unresolved_visual_actions",
    "blocking_terms",
    "blocking_term_variant_hits",
    "blocking_term_variant_rules",
    "pair_review_status",
    "appellation_term_id",
    "appellation_term",
    "appellation_ordinary_hits",
    "date_term_id",
    "date_term",
    "date_ordinary_hits",
    "residual_needed",
    "candidate_pool_pairs",
    "residual_slack_pairs",
    "read",
]

SUMMARY_FIELDNAMES = [
    "run_label",
    "group",
    "value",
    "pairs",
    "residual_needed",
    "candidate_pool_pairs",
    "residual_slack_pairs",
    "read",
]

BEST_RUN_ORDER = ("all_lanes_cap1000", "all_lanes_cap1000_program", "all_lanes_cap250")
IMPACT_ORDER = {SOME_VARIANT: 0, NO_VARIANT: 1}
OCR_PAIR_ORDER = {"both_not_matched": 0, "mixed": 1, "both_matched": 2}
LANE_ORDER = {
    "length_5_8_smoke_candidate": 0,
    "appellation_min_length_candidate": 1,
    "excluded_by_appellation_min_length": 2,
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    blocked_rows = keyed_rows(read_rows(args.blocked_pairs), "pair_id")
    variant_rows = read_rows(args.variant_impact)
    source_rows = keyed_rows(read_rows(args.source_queue), "term_id")
    upper_rows = read_rows(args.upper_bound)
    upper = best_upper_bound_row(upper_rows, args.run_label)
    detail_rows = build_detail_rows(
        blocked_rows=blocked_rows,
        variant_rows=variant_rows,
        source_rows=source_rows,
        upper=upper,
    )
    summary_rows = build_summary_rows(detail_rows, upper)
    write_csv(args.out, DETAIL_FIELDNAMES, detail_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, detail_rows, summary_rows, upper, args)
    write_manifest(args.manifest_out, args, detail_rows, summary_rows, upper, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocked-pairs", type=Path, default=DEFAULT_BLOCKED_PAIRS)
    parser.add_argument("--variant-impact", type=Path, default=DEFAULT_VARIANT_IMPACT)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument("--upper-bound", type=Path, default=DEFAULT_UPPER_BOUND)
    parser.add_argument("--run-label", default="")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_detail_rows(
    *,
    blocked_rows: dict[str, dict[str, str]],
    variant_rows: list[dict[str, str]],
    source_rows: dict[str, dict[str, str]],
    upper: dict[str, str],
) -> list[dict[str, object]]:
    run_label = upper["run_label"]
    residual_needed = int_or_zero(
        upper.get("residual_gap_after_simple_variant_upper_bound", "")
    )
    candidates = [
        row
        for row in variant_rows
        if row.get("run_label") == run_label and row.get("impact_status") != ALL_VARIANT
    ]
    candidate_pool = len(candidates)
    residual_slack = max(0, candidate_pool - residual_needed)
    rows: list[dict[str, object]] = []
    for row in candidates:
        pair = blocked_rows.get(row.get("pair_id", ""), {})
        blockers = parse_blockers(row)
        unresolved = [blocker for blocker in blockers if blocker["variant_hits"] <= 0]
        unresolved_sources = [source_rows.get(str(blocker["term_id"]), {}) for blocker in unresolved]
        rows.append(
            {
                "run_label": run_label,
                "review_rank": 0,
                "within_minimum_residual_frontier": "false",
                "impact_status": row.get("impact_status", ""),
                "pair_id": row.get("pair_id", ""),
                "concept": row.get("concept", ""),
                "candidate_lane": pair.get("candidate_lane", ""),
                "reason": row.get("reason", ""),
                "row_ocr_pair_status": row.get("row_ocr_pair_status", ""),
                "unresolved_term_ids": join_unique(
                    str(blocker["term_id"]) for blocker in unresolved
                ),
                "unresolved_terms": join_unique(str(blocker["term"]) for blocker in unresolved),
                "unresolved_term_sides": join_unique(
                    term_side(str(blocker["term_id"])) for blocker in unresolved
                ),
                "unresolved_term_buckets": join_unique(
                    source.get("review_bucket", "") for source in unresolved_sources
                ),
                "unresolved_term_ocr_statuses": join_unique(
                    source.get("row_ocr_status", "") for source in unresolved_sources
                ),
                "unresolved_source_flags": join_unique(
                    flag
                    for source in unresolved_sources
                    for flag in source.get("source_review_flags", "").split(";")
                ),
                "unresolved_visual_actions": join_unique(
                    source.get("visual_review_action", "") for source in unresolved_sources
                ),
                "blocking_terms": row.get("blocking_terms", ""),
                "blocking_term_variant_hits": row.get("blocking_term_variant_hits", ""),
                "blocking_term_variant_rules": row.get("blocking_term_variant_rules", ""),
                "pair_review_status": pair.get("pair_review_status", ""),
                "appellation_term_id": pair.get("appellation_term_id", ""),
                "appellation_term": pair.get("appellation_term", ""),
                "appellation_ordinary_hits": pair.get("appellation_ordinary_hits", ""),
                "date_term_id": pair.get("date_term_id", ""),
                "date_term": pair.get("date_term", ""),
                "date_ordinary_hits": pair.get("date_ordinary_hits", ""),
                "residual_needed": residual_needed,
                "candidate_pool_pairs": candidate_pool,
                "residual_slack_pairs": residual_slack,
                "read": read_for_row(row.get("impact_status", "")),
            }
        )
    rows.sort(key=residual_sort_key)
    for index, row in enumerate(rows, start=1):
        row["review_rank"] = index
        row["within_minimum_residual_frontier"] = (
            "true" if index <= residual_needed else "false"
        )
    return rows


def build_summary_rows(
    detail_rows: list[dict[str, object]],
    upper: dict[str, str],
) -> list[dict[str, object]]:
    run_label = upper["run_label"]
    residual_needed = int_or_zero(
        upper.get("residual_gap_after_simple_variant_upper_bound", "")
    )
    candidate_pool = len(detail_rows)
    residual_slack = max(0, candidate_pool - residual_needed)
    out: list[dict[str, object]] = [
        {
            "run_label": run_label,
            "group": "residual_pool",
            "value": "candidate_pairs_not_closed_by_all-blocker_simple_variants",
            "pairs": candidate_pool,
            "residual_needed": residual_needed,
            "candidate_pool_pairs": candidate_pool,
            "residual_slack_pairs": residual_slack,
            "read": "at least residual_needed rows from this pool need source-rule or method resolution to reach the source-cited count",
        },
        {
            "run_label": run_label,
            "group": "review_frontier",
            "value": "minimum_residual_frontier",
            "pairs": min(residual_needed, candidate_pool),
            "residual_needed": residual_needed,
            "candidate_pool_pairs": candidate_pool,
            "residual_slack_pairs": residual_slack,
            "read": "frontier is a deterministic review priority, not a selected correction set",
        },
    ]
    out.extend(counter_summary(detail_rows, "impact_status", upper))
    out.extend(counter_summary(detail_rows, "row_ocr_pair_status", upper))
    return out


def counter_summary(
    rows: list[dict[str, object]],
    field: str,
    upper: dict[str, str],
) -> list[dict[str, object]]:
    counter = Counter(str(row.get(field, "")) for row in rows)
    residual_needed = int_or_zero(
        upper.get("residual_gap_after_simple_variant_upper_bound", "")
    )
    candidate_pool = len(rows)
    residual_slack = max(0, candidate_pool - residual_needed)
    return [
        {
            "run_label": upper["run_label"],
            "group": field,
            "value": value,
            "pairs": count,
            "residual_needed": residual_needed,
            "candidate_pool_pairs": candidate_pool,
            "residual_slack_pairs": residual_slack,
            "read": "residual-pool breakdown; diagnostic only",
        }
        for value, count in sorted(counter.items())
    ]


def parse_blockers(row: dict[str, str]) -> list[dict[str, object]]:
    ids = row.get("blocking_term_ids", "").split(";")
    terms = row.get("blocking_terms", "").split(";")
    hits = row.get("blocking_term_variant_hits", "").split(";")
    rules = row.get("blocking_term_variant_rules", "").split(";")
    out = []
    for index, term_id in enumerate(ids):
        if not term_id:
            continue
        out.append(
            {
                "term_id": term_id,
                "term": value_at(terms, index),
                "variant_hits": int_or_zero(value_at(hits, index)),
                "variant_rule": value_at(rules, index),
            }
        )
    return out


def best_upper_bound_row(rows: list[dict[str, str]], requested_run_label: str) -> dict[str, str]:
    if requested_run_label:
        for row in rows:
            if row.get("run_label") == requested_run_label:
                return row
        raise ValueError(f"unknown run label: {requested_run_label}")
    if not rows:
        raise ValueError("upper-bound input has no rows")
    return min(
        rows,
        key=lambda row: (
            int_or_zero(row.get("residual_gap_after_simple_variant_upper_bound", "")),
            BEST_RUN_ORDER.index(row["run_label"])
            if row.get("run_label") in BEST_RUN_ORDER
            else 99,
            row.get("run_label", ""),
        ),
    )


def residual_sort_key(row: dict[str, object]) -> tuple[int, int, int, int, str, str]:
    return (
        IMPACT_ORDER.get(str(row["impact_status"]), 99),
        0 if str(row.get("unresolved_source_flags", "")) else 1,
        OCR_PAIR_ORDER.get(str(row["row_ocr_pair_status"]), 99),
        LANE_ORDER.get(str(row["candidate_lane"]), 99),
        str(row["concept"]),
        str(row["pair_id"]),
    )


def read_for_row(impact_status: str) -> str:
    if impact_status == SOME_VARIANT:
        return "partial simple-variant lead; unresolved blockers still need source or method evidence"
    if impact_status == NO_VARIANT:
        return "no simple one-edit variant lead for current blockers; residual source or method review needed"
    return "not part of residual pool"


def write_markdown(
    path: Path,
    detail_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    upper: dict[str, str],
    args: argparse.Namespace,
) -> None:
    residual_needed = int_or_zero(
        upper.get("residual_gap_after_simple_variant_upper_bound", "")
    )
    candidate_pool = len(detail_rows)
    residual_slack = max(0, candidate_pool - residual_needed)
    current_defined = upper.get("current_defined_distances", "")
    source_cited = upper.get("source_cited_defined_distances", "")
    upper_defined = upper.get("upper_bound_defined_distances", "")
    lines = [
        "# WRR Variant Residual Review Packet",
        "",
        "Status: diagnostic-only residual review packet after the simple-variant upper bound.",
        "It does not select source corrections, replace terms, or reproduce WRR.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_variant_residual_review_packet "
            f"--blocked-pairs {args.blocked_pairs} "
            f"--variant-impact {args.variant_impact} "
            f"--source-queue {args.source_queue} "
            f"--upper-bound {args.upper_bound} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Best current run: `{upper['run_label']}`.",
        f"- Current defined distances: {current_defined} of {source_cited}.",
        f"- Generous simple-variant upper bound: {upper_defined} defined distances.",
        f"- Residual needed after that upper bound: {residual_needed}.",
        f"- Residual candidate pool: {candidate_pool} pairs.",
        f"- Residual slack: {residual_slack} pairs.",
        f"- Therefore at least {residual_needed} pairs still need source-rule or method resolution even after the generous simple-variant upper bound.",
        "",
        "## Residual Summary",
        "",
        "| Group | Value | Pairs | Read |",
        "| --- | --- | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| `{group}` | `{value}` | {pairs} | {read} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Priority Frontier",
            "",
            "| Rank | Frontier | Pair | Concept | Impact | Row OCR | Unresolved terms | Buckets | Flags |",
            "| ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in detail_rows[:25]:
        lines.append(
            "| {review_rank} | `{within_minimum_residual_frontier}` | `{pair_id}` | "
            "`{concept}` | `{impact_status}` | `{row_ocr_pair_status}` | "
            "`{unresolved_terms}` | `{unresolved_term_buckets}` | "
            "{flags} |".format(
                flags=markdown_code_or_blank(str(row.get("unresolved_source_flags", ""))),
                **row,
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The frontier is deterministic triage, not a correction set.",
            "- Rows outside the first 40 remain relevant because the 59-row pool has only 19 slack pairs.",
            "- Partial-variant rows are ranked first because one blocker has a simple variant lead and one blocker remains unresolved.",
            "- No-variant rows are the harder residual pool; they need source transcription, pair-rule, or method evidence beyond simple one-edit variant leads.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    detail_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    upper: dict[str, str],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": "build_wrr_variant_residual_review_packet",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "run_label": upper.get("run_label", ""),
        "inputs": {
            "blocked_pairs": str(args.blocked_pairs),
            "variant_impact": str(args.variant_impact),
            "source_queue": str(args.source_queue),
            "upper_bound": str(args.upper_bound),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
        "detail_rows": len(detail_rows),
        "summary_rows": len(summary_rows),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def keyed_rows(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row.get(key, ""): row for row in rows if row.get(key, "")}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def value_at(values: list[str], index: int) -> str:
    return values[index] if index < len(values) else ""


def term_side(term_id: str) -> str:
    if "_app_" in term_id:
        return "appellation"
    if "_date_" in term_id:
        return "date"
    return ""


def join_unique(values: object) -> str:
    return ";".join(sorted({str(value) for value in values if str(value)}))


def markdown_code_or_blank(value: str) -> str:
    return f"`{value}`" if value else ""


def int_or_zero(value: str | object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


if __name__ == "__main__":
    raise SystemExit(main())
