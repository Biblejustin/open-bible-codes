#!/usr/bin/env python3
"""Split remaining dynamic full-span partitions into non-overlapping worker files."""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from scripts.export_dynamic_span_hits import ROOT
from scripts.plan_dynamic_span_partitions import DEFAULT_OUT as DEFAULT_PLAN
from scripts.plan_dynamic_span_partitions import export_command
from scripts.run_dynamic_span_partitions import is_control_corpus, read_rows
from scripts.summarize_dynamic_span_partition_outputs import completed_plan_rows


DEFAULT_OUT_DIR = ROOT / "reports/dynamic_skip_focus/worker_batches"
COUNT_FIELDNAMES = [
    "corpus",
    "corpus_language",
    "corpus_letters",
    "term_id",
    "concept",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "normalized_length",
    "mode",
    "min_skip",
    "effective_max_skip",
    "search_space_positions",
    "expected_hits",
    "expected_hits_per_million_positions",
    "direction",
    "forward_count",
    "backward_count",
    "hit_count",
    "hits_per_million_positions",
    "counter_elapsed_seconds",
    "status",
]


@dataclass
class WorkerBucket:
    label: str
    rows: list[dict[str, str]] = field(default_factory=list)
    estimated_hits: int = 0

    @property
    def partition_count(self) -> int:
        return len(self.rows)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    plan_rows = read_rows(args.plan)
    selected = select_remaining_rows(plan_rows, args)
    buckets = assign_rows(selected, args.workers, args.worker_prefix)
    write_worker_files(args.out_dir, buckets, args, plan_rows)
    write_manifest(args.out_dir / "manifest.json", args, plan_rows, selected, buckets, started)
    print(args.out_dir)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--worker-prefix", default="worker")
    parser.add_argument("--partition-count", action="append", type=int, default=[])
    parser.add_argument("--min-partition-count", type=int)
    parser.add_argument("--max-partition-count", type=int)
    parser.add_argument("--max-estimated-hits", type=int, default=1_000_000)
    parser.add_argument("--bible-only", action="store_true")
    parser.add_argument("--controls-only", action="store_true")
    parser.add_argument("--limit", type=int)
    return parser


def select_remaining_rows(rows: list[dict[str, str]], args: argparse.Namespace) -> list[dict[str, str]]:
    if args.workers < 1:
        raise ValueError("--workers must be at least 1")
    if args.bible_only and args.controls_only:
        raise ValueError("--bible-only and --controls-only cannot both be set")
    completed_ids = {row["partition_id"] for row in completed_plan_rows(rows)}
    partition_counts = set(args.partition_count)
    selected: list[dict[str, str]] = []
    for row in rows:
        if row["partition_id"] in completed_ids:
            continue
        partition_count = int(row["partition_count"])
        if partition_counts and partition_count not in partition_counts:
            continue
        if args.min_partition_count is not None and partition_count < args.min_partition_count:
            continue
        if args.max_partition_count is not None and partition_count > args.max_partition_count:
            continue
        if args.max_estimated_hits is not None and int(row["estimated_partition_hits"]) > args.max_estimated_hits:
            continue
        if args.bible_only and is_control_corpus(row["corpus"]):
            continue
        if args.controls_only and not is_control_corpus(row["corpus"]):
            continue
        selected.append(row)
    selected.sort(key=row_sort_key)
    if args.limit is not None:
        selected = selected[: args.limit]
    return selected


def assign_rows(rows: list[dict[str, str]], workers: int, worker_prefix: str) -> list[WorkerBucket]:
    buckets = [WorkerBucket(f"{worker_prefix}_{index:02d}") for index in range(1, workers + 1)]
    for row in sorted(rows, key=lambda item: (-int(item["estimated_partition_hits"]), row_sort_key(item))):
        bucket = min(buckets, key=lambda item: (item.estimated_hits, item.partition_count, item.label))
        bucket.rows.append(row)
        bucket.estimated_hits += int(row["estimated_partition_hits"])
    for bucket in buckets:
        bucket.rows.sort(key=row_sort_key)
    return buckets


def write_worker_files(
    out_dir: Path,
    buckets: list[WorkerBucket],
    args: argparse.Namespace,
    plan_rows: list[dict[str, str]],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    all_rows: list[dict[str, str]] = []
    count_rows_by_key = count_rows_for_plan_rows([row for bucket in buckets for row in bucket.rows])
    fieldnames = ["worker", *plan_rows[0].keys()]
    for bucket in buckets:
        csv_path = out_dir / f"{bucket.label}_partitions.csv"
        count_path = out_dir / f"{bucket.label}_counts.csv"
        count_rows = unique_count_rows(bucket.rows, count_rows_by_key)
        write_csv(count_path, COUNT_FIELDNAMES, count_rows)
        rows = [
            {"worker": bucket.label, **worker_plan_row(row, count_path)}
            for row in bucket.rows
        ]
        write_csv(csv_path, fieldnames, rows)
        write_worker_readme(out_dir / f"{bucket.label}_README.md", bucket, csv_path, count_path)
        all_rows.extend(rows)
    write_csv(out_dir / "partition_worker_assignments.csv", fieldnames, all_rows)


def write_worker_readme(path: Path, bucket: WorkerBucket, csv_path: Path, count_path: Path) -> None:
    rel_csv = display_path(csv_path)
    rel_counts = display_path(count_path)
    bundle_path = f"reports/dynamic_skip_focus/worker_batches/{bucket.label}_results.zip"
    lines = [
        f"# {bucket.label} Partition Worker",
        "",
        f"- assigned partitions: {bucket.partition_count}",
        f"- estimated hits: {bucket.estimated_hits:,}",
        f"- worker plan CSV: `{rel_csv}`",
        f"- worker counts CSV: `{rel_counts}`",
        "",
        "## Worker Commands",
        "",
        "```bash",
        f"python3 -m scripts.run_dynamic_span_partitions --plan {rel_csv} --partition-id-file {rel_csv} --max-estimated-hits 1000000",
        f"python3 -m scripts.summarize_dynamic_span_partition_outputs --plan {rel_csv}",
        f"python3 -m scripts.compress_dynamic_span_partition_outputs --plan {rel_csv}",
        f"python3 -m scripts.export_partition_worker_bundle --plan {rel_csv} --assignment {rel_csv} --out {bundle_path}",
        "```",
        "",
        "Send the result zip back to the coordinator. The coordinator imports it,",
        "then regenerates summaries and commits docs.",
        "",
        "On Windows, use `python` instead of `python3` if needed. The runner",
        "uses the active interpreter for child export processes.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    plan_rows: list[dict[str, str]],
    selected_rows: list[dict[str, str]],
    buckets: list[WorkerBucket],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/plan_partition_worker_batches.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "plan": display_path(args.plan),
        "plan_rows": len(plan_rows),
        "selected_rows": len(selected_rows),
        "workers": len(buckets),
        "total_estimated_hits": sum(bucket.estimated_hits for bucket in buckets),
        "buckets": [
            {
                "worker": bucket.label,
                "partitions": bucket.partition_count,
                "estimated_hits": bucket.estimated_hits,
                "assignment": display_path(path.parent / f"{bucket.label}_partitions.csv"),
                "counts": display_path(path.parent / f"{bucket.label}_counts.csv"),
            }
            for bucket in buckets
        ],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def row_sort_key(row: dict[str, str]) -> tuple[str, str, int]:
    return (row["corpus"], row["term_id"], int(row["partition_index"]))


def count_rows_for_plan_rows(rows: list[dict[str, str]]) -> dict[tuple[str, str, str, str, str], dict[str, str]]:
    source_paths = sorted(
        {absolute_path(row["count_source_file"]) for row in rows if row.get("count_source_file")}
    )
    count_rows: dict[tuple[str, str, str, str, str], dict[str, str]] = {}
    for path in source_paths:
        if not path.exists():
            continue
        for row in read_rows(path):
            normalized = {field: row.get(field, "") for field in COUNT_FIELDNAMES}
            count_rows[count_key(normalized)] = normalized
    return count_rows


def unique_count_rows(
    plan_rows: list[dict[str, str]],
    count_rows_by_key: dict[tuple[str, str, str, str, str], dict[str, str]],
) -> list[dict[str, str]]:
    rows: dict[tuple[str, str, str, str, str], dict[str, str]] = {}
    for row in plan_rows:
        key = count_key_for_plan_row(row)
        rows[key] = count_rows_by_key.get(key, fallback_count_row(row))
    return [rows[key] for key in sorted(rows)]


def fallback_count_row(row: dict[str, str]) -> dict[str, str]:
    return {
        "corpus": row["corpus"],
        "corpus_language": row.get("corpus_language", ""),
        "corpus_letters": "",
        "term_id": row["term_id"],
        "concept": row.get("concept", ""),
        "category": row.get("category", ""),
        "term_language": row.get("term_language", ""),
        "term": row.get("term", ""),
        "normalized_term": row.get("normalized_term", ""),
        "normalized_length": row.get("normalized_length", ""),
        "mode": row.get("mode", ""),
        "min_skip": row.get("min_abs_skip", ""),
        "effective_max_skip": row.get("max_abs_skip", ""),
        "search_space_positions": "",
        "expected_hits": "",
        "expected_hits_per_million_positions": "",
        "direction": row.get("direction", "both"),
        "forward_count": "",
        "backward_count": "",
        "hit_count": row.get("total_hit_count", row.get("estimated_partition_hits", "")),
        "hits_per_million_positions": "",
        "counter_elapsed_seconds": "",
        "status": "worker_plan_fallback",
    }


def worker_plan_row(row: dict[str, str], count_path: Path) -> dict[str, str]:
    rewritten = dict(row)
    rewritten["count_source_file"] = display_path(count_path)
    rewritten["export_command"] = export_command(
        rewritten,
        int(rewritten["min_abs_skip"]),
        int(rewritten["max_abs_skip"]),
        ROOT / rewritten["out"],
        ROOT / rewritten["summary_out"],
        ROOT / rewritten["manifest_out"],
    )
    return rewritten


def count_key(row: dict[str, str]) -> tuple[str, str, str, str, str]:
    return (
        row.get("corpus", ""),
        row.get("term_id", ""),
        row.get("mode", ""),
        row.get("direction", "both") or "both",
        row.get("hit_count", ""),
    )


def count_key_for_plan_row(row: dict[str, str]) -> tuple[str, str, str, str, str]:
    return (
        row.get("corpus", ""),
        row.get("term_id", ""),
        row.get("mode", ""),
        row.get("direction", "both") or "both",
        row.get("total_hit_count", ""),
    )


def absolute_path(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
