#!/usr/bin/env python3
"""Plan bounded skip-range exports for dense dynamic full-span rows."""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from els import __version__
from scripts.export_dynamic_span_hits import DEFAULT_COUNTS, ROOT, read_many


DEFAULT_OUT = ROOT / "reports/dynamic_skip_focus/full_span_partition_plan.csv"
DEFAULT_REPORT = ROOT / "docs/DYNAMIC_SKIP_FULL_SPAN_PARTITION_PLAN.md"
DEFAULT_MANIFEST = ROOT / "reports/dynamic_skip_focus/full_span_partition_plan.manifest.json"
DEFAULT_PARTITION_DIR = ROOT / "reports/dynamic_skip_focus/partitions"

FIELDNAMES = [
    "partition_id",
    "corpus",
    "corpus_language",
    "term_id",
    "concept",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "normalized_length",
    "mode",
    "direction",
    "total_hit_count",
    "partition_index",
    "partition_count",
    "min_abs_skip",
    "max_abs_skip",
    "estimated_partition_hits",
    "count_source_file",
    "out",
    "summary_out",
    "manifest_out",
    "export_command",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = select_dense_rows(read_many(args.counts or DEFAULT_COUNTS), args)
    plan_rows = build_partition_plan(rows, args)
    write_csv(args.out, plan_rows)
    write_report(args.report, rows, plan_rows, args)
    write_manifest(args.manifest, args, rows, plan_rows, started)
    print(args.out)
    print(args.report)
    print(args.manifest)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--counts", type=Path, action="append", default=[])
    parser.add_argument("--mode", action="append", default=["full-span"])
    parser.add_argument("--term-id", action="append", default=[])
    parser.add_argument("--corpus-label", action="append", default=[])
    parser.add_argument("--dense-threshold", type=int, default=50_000)
    parser.add_argument("--target-hits-per-partition", type=int, default=1_000_000)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--partition-dir", type=Path, default=DEFAULT_PARTITION_DIR)
    return parser


def select_dense_rows(rows: list[dict[str, str]], args: argparse.Namespace) -> list[dict[str, str]]:
    modes = set(args.mode)
    term_ids = set(args.term_id)
    corpus_labels = set(args.corpus_label)
    selected = []
    for row in rows:
        if row.get("mode") not in modes:
            continue
        if term_ids and row.get("term_id") not in term_ids:
            continue
        if corpus_labels and row.get("corpus") not in corpus_labels:
            continue
        if int(row.get("hit_count") or 0) > args.dense_threshold:
            selected.append(row)
    return sorted(selected, key=lambda item: (-int(item["hit_count"]), item["corpus"], item["term_id"]))


def build_partition_plan(rows: list[dict[str, str]], args: argparse.Namespace) -> list[dict[str, str]]:
    plan_rows = []
    for row in rows:
        hit_count = int(row["hit_count"])
        min_skip = int(row.get("min_skip") or 2)
        max_skip = int(row["effective_max_skip"])
        requested_partition_count = max(1, math.ceil(hit_count / args.target_hits_per_partition))
        ranges = partition_ranges(min_skip, max_skip, requested_partition_count)
        partition_count = len(ranges)
        for index, (start, end) in enumerate(ranges, start=1):
            estimated_hits = estimate_partition_hits(hit_count, min_skip, max_skip, start, end)
            partition_id = make_partition_id(row, index, partition_count, start, end)
            out = args.partition_dir / f"{partition_id}.csv"
            summary_out = args.partition_dir / f"{partition_id}.md"
            manifest_out = args.partition_dir / f"{partition_id}.manifest.json"
            plan_rows.append(
                {
                    "partition_id": partition_id,
                    "corpus": row["corpus"],
                    "corpus_language": row.get("corpus_language", ""),
                    "term_id": row["term_id"],
                    "concept": row.get("concept", ""),
                    "category": row.get("category", ""),
                    "term_language": row.get("term_language", ""),
                    "term": row.get("term", ""),
                    "normalized_term": row.get("normalized_term", ""),
                    "normalized_length": row.get("normalized_length", ""),
                    "mode": row["mode"],
                    "direction": row.get("direction", "both"),
                    "total_hit_count": row["hit_count"],
                    "partition_index": str(index),
                    "partition_count": str(partition_count),
                    "min_abs_skip": str(start),
                    "max_abs_skip": str(end),
                    "estimated_partition_hits": str(estimated_hits),
                    "count_source_file": display_path(Path(row.get("count_source_file", ""))),
                    "out": display_path(out),
                    "summary_out": display_path(summary_out),
                    "manifest_out": display_path(manifest_out),
                    "export_command": export_command(row, start, end, out, summary_out, manifest_out),
                }
            )
    return plan_rows


def partition_ranges(min_skip: int, max_skip: int, partition_count: int) -> list[tuple[int, int]]:
    if max_skip < min_skip:
        return []
    span = max_skip - min_skip + 1
    count = min(partition_count, span)
    ranges = []
    for index in range(count):
        start = min_skip + (span * index) // count
        end = min_skip + (span * (index + 1)) // count - 1
        ranges.append((start, end))
    return ranges


def estimate_partition_hits(
    hit_count: int,
    full_min_skip: int,
    full_max_skip: int,
    partition_min_skip: int,
    partition_max_skip: int,
) -> int:
    full_span = max(1, full_max_skip - full_min_skip + 1)
    partition_span = max(0, partition_max_skip - partition_min_skip + 1)
    return math.ceil(hit_count * partition_span / full_span)


def make_partition_id(
    row: dict[str, str],
    index: int,
    partition_count: int,
    start: int,
    end: int,
) -> str:
    mode = row["mode"].replace("-", "_")
    return (
        f"{row['corpus']}__{row['term_id']}__{mode}__"
        f"p{index:05d}_of_{partition_count:05d}__skip_{start}_{end}"
    )


def export_command(
    row: dict[str, str],
    start: int,
    end: int,
    out: Path,
    summary_out: Path,
    manifest_out: Path,
) -> str:
    source = row.get("count_source_file", "")
    parts = [
        "python3",
        "-m",
        "scripts.export_dynamic_span_hits",
        "--include-dense",
        "--max-export-hits",
        "0",
        "--corpus-label",
        row["corpus"],
        "--term-id",
        row["term_id"],
        "--mode",
        row["mode"],
        "--min-abs-skip",
        str(start),
        "--max-abs-skip",
        str(end),
        "--out",
        display_path(out),
        "--summary-out",
        display_path(summary_out),
        "--manifest-out",
        display_path(manifest_out),
    ]
    if source:
        parts.extend(["--counts", display_path(Path(source))])
    return " ".join(shell_token(part) for part in parts)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    path: Path,
    dense_rows: list[dict[str, str]],
    plan_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_language = Counter(row.get("term_language", "") for row in dense_rows)
    total_dense_hits = sum(int(row["hit_count"]) for row in dense_rows)
    lines = [
        "# Dynamic Full-Span Partition Plan",
        "",
        "This plan splits high-density dynamic full-span rows into bounded",
        "absolute-skip ranges. It does not drop those rows; it creates a",
        "reproducible path to export them in shards.",
        "",
        "## Reproduce",
        "",
        "```bash",
        "python3 -m scripts.plan_dynamic_span_partitions",
        "```",
        "",
        "## Scope",
        "",
        f"- dense threshold: {args.dense_threshold:,} hits",
        f"- target hits per partition: {args.target_hits_per_partition:,}",
        f"- dense count rows planned: {len(dense_rows):,}",
        f"- planned partitions: {len(plan_rows):,}",
        f"- total dense row hits represented: {total_dense_hits:,}",
        f"- plan CSV: `{display_path(args.out)}`",
        "",
        "## Dense Rows By Language",
        "",
        "| Language | Rows |",
        "| --- | ---: |",
    ]
    for language, count in sorted(by_language.items()):
        lines.append(f"| {language} | {count:,} |")
    lines.extend(
        [
            "",
            "## Largest Dense Rows",
            "",
            "| Corpus | Term | Hits | Max skip | Partitions |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in dense_rows[:25]:
        partition_count = planned_partition_count(row, args.target_hits_per_partition)
        lines.append(
            f"| {row['corpus']} | `{row['term_id']}` | {int(row['hit_count']):,} | "
            f"{int(row['effective_max_skip']):,} | {partition_count:,} |"
        )
    lines.extend(
        [
            "",
            "## First Export Commands",
            "",
            "These commands are examples from the plan CSV. They use `--max-export-hits 0`,",
            "which means no cap inside the bounded skip shard.",
            "",
            "```bash",
        ]
    )
    for row in plan_rows[:5]:
        lines.append(row["export_command"])
    lines.extend(
        [
            "```",
            "",
            "## Read",
            "",
            "- Partition estimates are based on proportional skip-range width, not a pre-count of each shard.",
            "- A shard may still be heavier than estimated; rerun that shard with narrower skip bounds if needed.",
            "- The full-span count rows remain the source of truth for version presence.",
            "- The partition CSV is the execution queue for dense all-hit export.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    dense_rows: list[dict[str, str]],
    plan_rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "script": "scripts/plan_dynamic_span_partitions.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "dense_threshold": args.dense_threshold,
        "target_hits_per_partition": args.target_hits_per_partition,
        "dense_rows": len(dense_rows),
        "planned_partitions": len(plan_rows),
        "out": display_path(args.out),
        "report": display_path(args.report),
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def shell_token(value: str) -> str:
    if value and all(char.isalnum() or char in "/._=-" for char in value):
        return value
    return "'" + value.replace("'", "'\"'\"'") + "'"


def planned_partition_count(row: dict[str, str], target_hits_per_partition: int) -> int:
    min_skip = int(row.get("min_skip") or 2)
    max_skip = int(row["effective_max_skip"])
    requested = max(1, math.ceil(int(row["hit_count"]) / target_hits_per_partition))
    return len(partition_ranges(min_skip, max_skip, requested))


def display_path(path: Path) -> str:
    if not str(path):
        return ""
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
