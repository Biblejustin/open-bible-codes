#!/usr/bin/env python3
"""Compress completed dynamic full-span partition CSVs in place."""

from __future__ import annotations

import argparse
import gzip
import json
import shutil
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from scripts.export_dynamic_span_hits import ROOT
from scripts.plan_dynamic_span_partitions import DEFAULT_OUT as DEFAULT_PLAN
from scripts.summarize_dynamic_span_partition_outputs import (
    DEFAULT_SUMMARY_CACHE,
    compressed_partition_output_path,
    load_summary_cache,
    partition_fingerprint,
    partition_manifest_path,
    read_rows,
    write_summary_cache,
)


DEFAULT_MANIFEST = ROOT / "reports/dynamic_skip_focus/partition_compression.manifest.json"
DEFAULT_EXAMPLES_PER_PARTITION = 3


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    plan_rows = read_rows(args.plan)
    cache = load_summary_cache(args.summary_cache) if not args.no_cache else {}
    selected = completed_uncompressed_rows(plan_rows)
    if args.limit is not None:
        selected = selected[: args.limit]
    before_free = free_bytes(ROOT)
    results = compress_rows(
        selected,
        cache=cache,
        examples_per_partition=args.examples_per_partition,
        dry_run=args.dry_run,
    )
    if not args.dry_run and not args.no_cache:
        write_summary_cache(args.summary_cache, cache)
    after_free = free_bytes(ROOT)
    write_manifest(args.manifest, args, results, before_free, after_free, started)
    print(args.manifest)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--summary-cache", type=Path, default=DEFAULT_SUMMARY_CACHE)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--examples-per-partition", type=int, default=DEFAULT_EXAMPLES_PER_PARTITION)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-cache", action="store_true")
    return parser


def completed_uncompressed_rows(plan_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for row in plan_rows:
        out = raw_partition_output_path(row)
        manifest = partition_manifest_path(row)
        if out.exists() and manifest.exists():
            rows.append(row)
    rows.sort(key=lambda item: (item["corpus"], item["term_id"], int(item["partition_index"])))
    return rows


def compress_rows(
    rows: list[dict[str, str]],
    *,
    cache: dict[str, dict[str, Any]],
    examples_per_partition: int,
    dry_run: bool,
) -> list[dict[str, Any]]:
    results = []
    for row in rows:
        source = raw_partition_output_path(row)
        target = compressed_partition_output_path(row)
        source_size = source.stat().st_size
        if dry_run:
            results.append(result_row(row, "dry_run", source, target, source_size, 0))
            continue
        if target.exists():
            results.append(result_row(row, "skipped_existing_gzip", source, target, source_size, target.stat().st_size))
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(target.suffix + ".tmp")
        with source.open("rb") as src, gzip.open(tmp, "wb", compresslevel=6) as dst:
            shutil.copyfileobj(src, dst, length=1024 * 1024)
        tmp.replace(target)
        target_size = target.stat().st_size
        source.unlink()
        cached = cache.get(row["partition_id"])
        if cached:
            cached["fingerprint"] = partition_fingerprint(row, examples_per_partition)
        results.append(result_row(row, "compressed", source, target, source_size, target_size))
    return results


def result_row(
    row: dict[str, str],
    status: str,
    source: Path,
    target: Path,
    source_size: int,
    target_size: int,
) -> dict[str, Any]:
    return {
        "partition_id": row["partition_id"],
        "corpus": row["corpus"],
        "term_id": row["term_id"],
        "status": status,
        "source": display_path(source),
        "target": display_path(target),
        "source_size": source_size,
        "target_size": target_size,
        "bytes_saved": max(source_size - target_size, 0),
    }


def raw_partition_output_path(row: dict[str, str]) -> Path:
    out = Path(row["out"])
    return out if out.is_absolute() else ROOT / out


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    results: list[dict[str, Any]],
    before_free: int,
    after_free: int,
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    status_counts: dict[str, int] = {}
    for row in results:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    payload: dict[str, Any] = {
        "script": "scripts/compress_dynamic_span_partition_outputs.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "dry_run": args.dry_run,
        "plan": display_path(args.plan),
        "summary_cache": display_path(args.summary_cache),
        "selected_rows": len(results),
        "status_counts": status_counts,
        "source_bytes": sum(int(row["source_size"]) for row in results),
        "target_bytes": sum(int(row["target_size"]) for row in results),
        "bytes_saved": sum(int(row["bytes_saved"]) for row in results),
        "free_bytes_before": before_free,
        "free_bytes_after": after_free,
        "rows": results[:25],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def free_bytes(path: Path) -> int:
    return shutil.disk_usage(path).free


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
