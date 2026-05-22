#!/usr/bin/env python3
"""Collapse WRR residual pair blockers into unique unresolved term targets."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_RESIDUAL_PACKET = Path("reports/wrr_1994/wrr_variant_residual_review_packet.csv")
DEFAULT_SOURCE_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_residual_term_reconciliation_queue.csv")
DEFAULT_SUMMARY_OUT = Path(
    "reports/wrr_1994/wrr_residual_term_reconciliation_summary.csv"
)
DEFAULT_MD = Path("docs/WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_residual_term_reconciliation_queue.manifest.json"
)

TERM_FIELDNAMES = [
    "run_label",
    "priority_rank",
    "term_id",
    "term",
    "term_side",
    "residual_pairs",
    "frontier_pairs",
    "concepts",
    "impact_statuses",
    "row_ocr_pair_statuses",
    "review_buckets",
    "term_ocr_statuses",
    "source_flags",
    "source_review_action",
    "visual_review_action",
    "source_queue_rank",
    "source_queue_bucket",
    "source_queue_ocr_status",
    "source_queue_row_ocr_basis",
    "source_queue_best_variant_hits",
    "source_queue_best_variant_rule",
    "source_queue_best_variant_normalized",
    "source_queue_pair_ids",
    "pair_ids",
    "reconciliation_need",
    "read",
]

SUMMARY_FIELDNAMES = [
    "run_label",
    "group",
    "value",
    "terms",
    "residual_pairs",
    "frontier_pairs",
    "read",
]

BUCKET_ORDER = {
    "ocr_not_matched_no_variant_lead": 0,
    "ocr_near_match_no_variant_lead": 1,
    "ocr_matched_no_variant_lead": 2,
    "missing_source_queue_row": 3,
}

NEED_ORDER = {
    "source_policy_or_pair_rule_review": 0,
    "source_transcription_or_row_alignment": 1,
    "page_image_near_match_review": 2,
    "method_or_pair_universe_review": 3,
    "source_queue_join_review": 4,
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    residual_rows = read_rows(args.residual_packet)
    source_rows = keyed_rows(read_rows(args.source_queue), "term_id")
    term_rows = build_term_rows(residual_rows, source_rows)
    summary_rows = build_summary_rows(term_rows)
    write_csv(args.out, TERM_FIELDNAMES, term_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, term_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, term_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--residual-packet", type=Path, default=DEFAULT_RESIDUAL_PACKET)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_term_rows(
    residual_rows: list[dict[str, str]],
    source_rows: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, object]] = {}
    for row in residual_rows:
        term_ids = split_values(row.get("unresolved_term_ids", ""))
        terms = split_values(row.get("unresolved_terms", ""))
        sides = split_values(row.get("unresolved_term_sides", ""))
        buckets = split_values(row.get("unresolved_term_buckets", ""))
        ocr_statuses = split_values(row.get("unresolved_term_ocr_statuses", ""))
        flags = split_values(row.get("unresolved_source_flags", ""))
        visual_actions = split_values(row.get("unresolved_visual_actions", ""))
        for index, term_id in enumerate(term_ids):
            item = grouped.setdefault(
                term_id,
                {
                    "run_label": row.get("run_label", ""),
                    "term_id": term_id,
                    "term": value_at(terms, index),
                    "term_side": value_at(sides, index) or term_side(term_id),
                    "pair_ids": set(),
                    "frontier_pair_ids": set(),
                    "concepts": set(),
                    "impact_statuses": Counter(),
                    "row_ocr_pair_statuses": Counter(),
                    "review_buckets": set(),
                    "term_ocr_statuses": set(),
                    "source_flags": set(),
                    "visual_actions": set(),
                },
            )
            pair_id = row.get("pair_id", "")
            if pair_id:
                cast_set(item["pair_ids"]).add(pair_id)
            if truthy(row.get("within_minimum_residual_frontier", "")) and pair_id:
                cast_set(item["frontier_pair_ids"]).add(pair_id)
            cast_set(item["concepts"]).add(row.get("concept", ""))
            cast_counter(item["impact_statuses"])[row.get("impact_status", "")] += 1
            cast_counter(item["row_ocr_pair_statuses"])[row.get("row_ocr_pair_status", "")] += 1
            cast_set(item["review_buckets"]).update(buckets)
            cast_set(item["term_ocr_statuses"]).update(ocr_statuses)
            cast_set(item["source_flags"]).update(flags)
            cast_set(item["visual_actions"]).update(visual_actions)

    rows: list[dict[str, object]] = []
    for term_id, item in grouped.items():
        source = source_rows.get(term_id, {})
        buckets = sorted(cast_set(item["review_buckets"])) or ["missing_source_queue_row"]
        source_flags = sorted(cast_set(item["source_flags"]))
        need = reconciliation_need(buckets, source_flags, bool(source))
        pair_ids = sorted(cast_set(item["pair_ids"]))
        frontier_pair_ids = sorted(cast_set(item["frontier_pair_ids"]))
        rows.append(
            {
                "run_label": item["run_label"],
                "priority_rank": 0,
                "term_id": term_id,
                "term": item["term"],
                "term_side": item["term_side"],
                "residual_pairs": len(pair_ids),
                "frontier_pairs": len(frontier_pair_ids),
                "concepts": join_sorted(cast_set(item["concepts"])),
                "impact_statuses": format_counter(cast_counter(item["impact_statuses"])),
                "row_ocr_pair_statuses": format_counter(
                    cast_counter(item["row_ocr_pair_statuses"])
                ),
                "review_buckets": ";".join(buckets),
                "term_ocr_statuses": join_sorted(cast_set(item["term_ocr_statuses"])),
                "source_flags": ";".join(source_flags),
                "source_review_action": source.get("source_review_action", ""),
                "visual_review_action": join_sorted(cast_set(item["visual_actions"])),
                "source_queue_rank": source.get("priority_rank", ""),
                "source_queue_bucket": source.get("review_bucket", ""),
                "source_queue_ocr_status": source.get("row_ocr_status", ""),
                "source_queue_row_ocr_basis": source.get("row_ocr_match_basis", ""),
                "source_queue_best_variant_hits": source.get("best_variant_hit_count", ""),
                "source_queue_best_variant_rule": source.get("best_variant_rule", ""),
                "source_queue_best_variant_normalized": source.get(
                    "best_variant_normalized", ""
                ),
                "source_queue_pair_ids": source.get("pair_ids", ""),
                "pair_ids": ";".join(pair_ids),
                "reconciliation_need": need,
                "read": read_for_need(need),
            }
        )
    rows.sort(key=term_sort_key)
    for index, row in enumerate(rows, start=1):
        row["priority_rank"] = index
    return rows


def build_summary_rows(term_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    if not term_rows:
        return []
    run_label = str(term_rows[0]["run_label"])
    out: list[dict[str, object]] = [
        {
            "run_label": run_label,
            "group": "residual_terms",
            "value": "unique_unresolved_terms",
            "terms": len(term_rows),
            "residual_pairs": sum_int(term_rows, "residual_pairs"),
            "frontier_pairs": sum_int(term_rows, "frontier_pairs"),
            "read": "unique unresolved term targets collapsed from residual pair rows",
        },
    ]
    out.extend(counter_summary(term_rows, "term_side", "term_side"))
    out.extend(multi_value_summary(term_rows, "review_buckets", "review_bucket"))
    out.extend(multi_value_summary(term_rows, "term_ocr_statuses", "term_ocr_status"))
    out.extend(multi_value_summary(term_rows, "source_flags", "source_flag"))
    out.extend(counter_summary(term_rows, "reconciliation_need", "reconciliation_need"))
    return out


def counter_summary(
    term_rows: list[dict[str, object]],
    field: str,
    group: str,
) -> list[dict[str, object]]:
    counter: Counter[str] = Counter(str(row.get(field, "")) for row in term_rows)
    by_value: dict[str, list[dict[str, object]]] = {
        value: [row for row in term_rows if str(row.get(field, "")) == value]
        for value in counter
        if value
    }
    return [
        {
            "run_label": str(term_rows[0]["run_label"]),
            "group": group,
            "value": value,
            "terms": len(rows),
            "residual_pairs": sum_int(rows, "residual_pairs"),
            "frontier_pairs": sum_int(rows, "frontier_pairs"),
            "read": "residual term queue breakdown; diagnostic only",
        }
        for value, rows in sorted(by_value.items())
    ]


def multi_value_summary(
    term_rows: list[dict[str, object]],
    field: str,
    group: str,
) -> list[dict[str, object]]:
    by_value: dict[str, list[dict[str, object]]] = {}
    for row in term_rows:
        for value in split_values(str(row.get(field, ""))):
            by_value.setdefault(value, []).append(row)
    return [
        {
            "run_label": str(term_rows[0]["run_label"]),
            "group": group,
            "value": value,
            "terms": len(rows),
            "residual_pairs": sum_int(rows, "residual_pairs"),
            "frontier_pairs": sum_int(rows, "frontier_pairs"),
            "read": "residual term queue breakdown; diagnostic only",
        }
        for value, rows in sorted(by_value.items())
        if value
    ]


def reconciliation_need(
    buckets: list[str],
    source_flags: list[str],
    has_source_row: bool,
) -> str:
    if not has_source_row:
        return "source_queue_join_review"
    if source_flags:
        return "source_policy_or_pair_rule_review"
    if any(bucket == "ocr_not_matched_no_variant_lead" for bucket in buckets):
        return "source_transcription_or_row_alignment"
    if any(bucket == "ocr_near_match_no_variant_lead" for bucket in buckets):
        return "page_image_near_match_review"
    if any(bucket == "ocr_matched_no_variant_lead" for bucket in buckets):
        return "method_or_pair_universe_review"
    return "source_queue_join_review"


def read_for_need(need: str) -> str:
    return {
        "source_transcription_or_row_alignment": (
            "term has no simple variant lead and did not match row OCR; check primary row transcription/alignment"
        ),
        "page_image_near_match_review": (
            "term has no simple variant lead but OCR has a near match; inspect page image before method changes"
        ),
        "method_or_pair_universe_review": (
            "term matched OCR but still lacks ordinary hits; source text alone probably does not close it"
        ),
        "source_policy_or_pair_rule_review": (
            "term carries source-policy context; need citable rule before inclusion/exclusion changes"
        ),
        "source_queue_join_review": (
            "term lacks enough source-queue context; inspect upstream queue inputs"
        ),
    }[need]


def term_sort_key(row: dict[str, object]) -> tuple[int, int, int, int, str]:
    buckets = split_values(str(row.get("review_buckets", "")))
    first_bucket_order = min((BUCKET_ORDER.get(bucket, 99) for bucket in buckets), default=99)
    return (
        NEED_ORDER.get(str(row["reconciliation_need"]), 99),
        first_bucket_order,
        -int(row["frontier_pairs"]),
        -int(row["residual_pairs"]),
        str(row["term_id"]),
    )


def write_markdown(
    path: Path,
    term_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# WRR Residual Term Reconciliation Queue",
        "",
        "Status: diagnostic-only unique-term queue from the residual pair packet.",
        "It does not select source corrections, exclude pairs, or reproduce WRR.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_residual_term_reconciliation_queue "
            f"--residual-packet {args.residual_packet} "
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
        f"- Unique unresolved terms: {len(term_rows)}.",
        f"- Residual pair links represented: {sum_int(term_rows, 'residual_pairs')}.",
        f"- Minimum-frontier pair links represented: {sum_int(term_rows, 'frontier_pairs')}.",
        "",
        "## Summary",
        "",
        "| Group | Value | Terms | Residual pairs | Frontier pairs | Read |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| `{group}` | `{value}` | {terms} | {residual_pairs} | "
            "{frontier_pairs} | {read} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Priority Terms",
            "",
            "| Rank | Term id | Term | Need | Pairs | Frontier | Buckets | Source flags | Read |",
            "| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |",
        ]
    )
    for row in term_rows[:30]:
        lines.append(
            "| {priority_rank} | `{term_id}` | `{term}` | `{reconciliation_need}` | "
            "{residual_pairs} | {frontier_pairs} | `{review_buckets}` | {flags} | "
            "{read} |".format(flags=markdown_code_or_blank(str(row["source_flags"])), **row)
        )
    flagged = [row for row in term_rows if row.get("source_flags")]
    if flagged:
        lines.extend(
            [
                "",
                "## Source-Policy Context",
                "",
                "| Rank | Term id | Term | Flags | Action |",
                "| ---: | --- | --- | --- | --- |",
            ]
        )
        for row in flagged:
            lines.append(
                "| {priority_rank} | `{term_id}` | `{term}` | `{source_flags}` | "
                "{source_review_action} |".format(**row)
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This queue compresses repeated residual pair blockers into unique unresolved terms.",
            "- Term priority is a review order, not a correction set.",
            "- Source-policy flags require citable pair-rule evidence before any source-lock change.",
            "- OCR-matched/no-variant terms are likely method or pair-universe blockers, not quick transcription fixes.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    term_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": "build_wrr_residual_term_reconciliation_queue",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "residual_packet": str(args.residual_packet),
            "source_queue": str(args.source_queue),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
        "term_rows": len(term_rows),
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


def split_values(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def value_at(values: list[str], index: int) -> str:
    return values[index] if index < len(values) else ""


def term_side(term_id: str) -> str:
    if "_app_" in term_id:
        return "appellation"
    if "_date_" in term_id:
        return "date"
    return ""


def truthy(value: str) -> bool:
    return value.lower() in {"true", "1", "yes"}


def cast_set(value: object) -> set[str]:
    if not isinstance(value, set):
        raise TypeError("expected set")
    return value


def cast_counter(value: object) -> Counter[str]:
    if not isinstance(value, Counter):
        raise TypeError("expected Counter")
    return value


def join_sorted(values: set[str]) -> str:
    return ";".join(sorted(value for value in values if value))


def format_counter(counter: Counter[str]) -> str:
    return ", ".join(f"{counter[key]} {key}" for key in sorted(counter) if key)


def sum_int(rows: list[dict[str, object]], field: str) -> int:
    return sum(int(row.get(field, 0)) for row in rows)


def markdown_code_or_blank(value: str) -> str:
    return f"`{value}`" if value else ""


if __name__ == "__main__":
    raise SystemExit(main())
