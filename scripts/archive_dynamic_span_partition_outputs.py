#!/usr/bin/env python3
"""Move completed compressed dynamic-span partition outputs to an archive root."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from scripts.export_dynamic_span_hits import ROOT
from scripts.plan_dynamic_span_partitions import DEFAULT_OUT as DEFAULT_PLAN
from scripts.run_dynamic_span_partitions import archive_marker_path
from scripts.summarize_dynamic_span_partition_outputs import compressed_partition_output_path, partition_manifest_path


DEFAULT_MANIFEST = ROOT / "reports/dynamic_skip_focus/partition_archive.manifest.json"
DEFAULT_MIN_FREE_GIB = 160.0

FIELDNAMES = [
    "partition_id",
    "corpus",
    "term_id",
    "status",
    "source",
    "archive_path",
    "marker",
    "source_size",
    "archive_size",
    "sha256",
    "message",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_rows(args.plan)
    selected = archive_candidates(rows)
    if args.limit is not None:
        selected = selected[: args.limit]
    before_free = shutil.disk_usage(ROOT).free
    results = archive_rows(selected, archive_root=args.archive_root, dry_run=args.dry_run, min_free_gib=args.min_free_gib)
    after_free = shutil.disk_usage(ROOT).free
    write_manifest(args.manifest, args, results, before_free, after_free, started)
    print(args.manifest)
    return 1 if any(row["status"] == "failed" for row in results) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--min-free-gib", type=float, default=DEFAULT_MIN_FREE_GIB)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def archive_candidates(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    candidates = []
    for row in rows:
        source = compressed_partition_output_path(row)
        manifest = partition_manifest_path(row)
        marker = archive_marker_path(row)
        if source.exists() and manifest.exists() and not marker.exists():
            candidates.append(row)
    candidates.sort(key=lambda item: (item["corpus"], item["term_id"], int(item["partition_index"])))
    return candidates


def archive_rows(
    rows: list[dict[str, str]],
    *,
    archive_root: Path,
    dry_run: bool,
    min_free_gib: float,
) -> list[dict[str, Any]]:
    archive_root = archive_root.resolve()
    results = []
    for row in rows:
        free_gib = shutil.disk_usage(ROOT).free / 1024**3
        if free_gib >= min_free_gib and results:
            break
        source = compressed_partition_output_path(row)
        marker = archive_marker_path(row)
        archive_path = archive_root / archive_relative_path(source)
        try:
            results.append(archive_row(row, source, archive_path, marker, dry_run=dry_run))
        except Exception as exc:  # pragma: no cover - defensive path for long unattended runs.
            results.append(result_row(row, "failed", source, archive_path, marker, 0, 0, "", str(exc)))
            break
    return results


def archive_row(row: dict[str, str], source: Path, archive_path: Path, marker: Path, *, dry_run: bool) -> dict[str, Any]:
    source_size = source.stat().st_size
    digest = sha256_file(source)
    if dry_run:
        return result_row(row, "dry_run", source, archive_path, marker, source_size, 0, digest, "")
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = archive_path.with_suffix(archive_path.suffix + ".tmp")
    shutil.copy2(source, tmp)
    archive_size = tmp.stat().st_size
    archive_digest = sha256_file(tmp)
    if archive_size != source_size or archive_digest != digest:
        tmp.unlink(missing_ok=True)
        raise ValueError("archive verification failed")
    tmp.replace(archive_path)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker_payload = {
        "archive_version": 1,
        "archived_at": datetime.now(UTC).isoformat(),
        "partition_id": row["partition_id"],
        "source": display_path(source),
        "archive_path": str(archive_path),
        "size": source_size,
        "sha256": digest,
    }
    tmp_marker = marker.with_suffix(marker.suffix + ".tmp")
    tmp_marker.write_text(json.dumps(marker_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp_marker.replace(marker)
    source.unlink()
    return result_row(row, "archived", source, archive_path, marker, source_size, archive_size, digest, "")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def result_row(
    row: dict[str, str],
    status: str,
    source: Path,
    archive_path: Path,
    marker: Path,
    source_size: int,
    archive_size: int,
    digest: str,
    message: str,
) -> dict[str, Any]:
    return {
        "partition_id": row["partition_id"],
        "corpus": row["corpus"],
        "term_id": row["term_id"],
        "status": status,
        "source": display_path(source),
        "archive_path": str(archive_path),
        "marker": display_path(marker),
        "source_size": source_size,
        "archive_size": archive_size,
        "sha256": digest,
        "message": message,
    }


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    results: list[dict[str, Any]],
    before_free: int,
    after_free: int,
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "script": "scripts/archive_dynamic_span_partition_outputs.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "archive_root": str(args.archive_root),
        "dry_run": args.dry_run,
        "min_free_gib": args.min_free_gib,
        "before_free_bytes": before_free,
        "after_free_bytes": after_free,
        "bytes_freed": max(after_free - before_free, 0),
        "result_counts": result_counts(results),
        "results": results,
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def result_counts(results: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in results:
        status = str(row["status"])
        counts[status] = counts.get(status, 0) + 1
    return counts


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def archive_relative_path(path: Path) -> Path:
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return Path(path.name)


if __name__ == "__main__":
    raise SystemExit(main())
