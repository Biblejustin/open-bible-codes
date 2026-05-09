#!/usr/bin/env python3
"""Run selected dynamic full-span partition exports from a plan CSV."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from scripts.export_dynamic_span_hits import ROOT
from scripts.plan_dynamic_span_partitions import DEFAULT_OUT as DEFAULT_PLAN


DEFAULT_STATUS = ROOT / "reports/dynamic_skip_focus/partition_run_status.csv"
DEFAULT_MANIFEST = ROOT / "reports/dynamic_skip_focus/partition_run_status.manifest.json"
CONTROL_PREFIXES = ("HEB_PBY_", "GRC_PERSEUS_", "ENG_PG_")

STATUS_FIELDNAMES = [
    "partition_id",
    "corpus",
    "term_id",
    "partition_index",
    "partition_count",
    "min_abs_skip",
    "max_abs_skip",
    "estimated_partition_hits",
    "status",
    "returncode",
    "elapsed_seconds",
    "out",
    "manifest_out",
    "message",
    "command",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    plan_rows = read_rows(args.plan)
    selected = select_partition_rows(plan_rows, args)
    status_rows = run_partitions(selected, args)
    write_csv(args.status_out, STATUS_FIELDNAMES, status_rows)
    write_manifest(args.manifest_out, args, plan_rows, selected, status_rows, started)
    print(args.status_out)
    print(args.manifest_out)
    return 1 if any(row["status"] == "failed" for row in status_rows) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--partition-id", action="append", default=[])
    parser.add_argument("--partition-id-file", action="append", type=Path, default=[])
    parser.add_argument("--term-id", action="append", default=[])
    parser.add_argument("--corpus-label", action="append", default=[])
    parser.add_argument("--min-partition-index", type=int)
    parser.add_argument("--max-partition-index", type=int)
    parser.add_argument("--partition-count", type=int)
    parser.add_argument("--max-estimated-hits", type=int)
    parser.add_argument("--bible-only", action="store_true")
    parser.add_argument("--controls-only", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--rerun", action="store_true")
    parser.add_argument("--status-out", type=Path, default=DEFAULT_STATUS)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def select_partition_rows(rows: list[dict[str, str]], args: argparse.Namespace) -> list[dict[str, str]]:
    if args.bible_only and args.controls_only:
        raise ValueError("--bible-only and --controls-only cannot both be set")
    partition_ids = selected_partition_ids(args)
    term_ids = set(args.term_id)
    corpus_labels = set(args.corpus_label)
    selected = []
    for row in rows:
        if partition_ids and row["partition_id"] not in partition_ids:
            continue
        if term_ids and row["term_id"] not in term_ids:
            continue
        if corpus_labels and row["corpus"] not in corpus_labels:
            continue
        if args.bible_only and is_control_corpus(row["corpus"]):
            continue
        if args.controls_only and not is_control_corpus(row["corpus"]):
            continue
        partition_index = int(row["partition_index"])
        if args.min_partition_index is not None and partition_index < args.min_partition_index:
            continue
        if args.max_partition_index is not None and partition_index > args.max_partition_index:
            continue
        if args.partition_count is not None and int(row["partition_count"]) != args.partition_count:
            continue
        if args.max_estimated_hits is not None and int(row["estimated_partition_hits"]) > args.max_estimated_hits:
            continue
        selected.append(row)
    selected.sort(key=lambda item: (item["corpus"], item["term_id"], int(item["partition_index"])))
    if args.limit is not None:
        selected = selected[: args.limit]
    return selected


def run_partitions(rows: list[dict[str, str]], args: argparse.Namespace) -> list[dict[str, str]]:
    statuses = []
    for row in rows:
        command = command_for_partition(row)
        out = existing_partition_completion_path(row)
        manifest = ROOT / row["manifest_out"]
        if args.dry_run:
            statuses.append(status_row(row, "dry_run", 0, 0.0, "", command))
            continue
        if not args.rerun and out.exists() and manifest.exists():
            statuses.append(status_row(row, "skipped_existing", 0, 0.0, "", command))
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        manifest.parent.mkdir(parents=True, exist_ok=True)
        started = time.perf_counter()
        completed = subprocess.run(command, text=True, capture_output=True)
        elapsed = round(time.perf_counter() - started, 3)
        message = completed.stderr.strip() or completed.stdout.strip()
        status = "executed" if completed.returncode == 0 else "failed"
        statuses.append(status_row(row, status, completed.returncode, elapsed, message, command))
    return statuses


def existing_partition_completion_path(row: dict[str, str]) -> Path:
    out = ROOT / row["out"]
    if out.exists():
        return out
    gz_out = out.with_suffix(out.suffix + ".gz")
    if gz_out.exists():
        return gz_out
    archived_marker = archive_marker_path(row)
    return archived_marker if archived_marker.exists() else out


def archive_marker_path(row: dict[str, str]) -> Path:
    out = ROOT / row["out"]
    gz_out = out.with_suffix(out.suffix + ".gz")
    return gz_out.with_suffix(gz_out.suffix + ".archived.json")


def command_for_partition(row: dict[str, str]) -> list[str]:
    command = [
        sys.executable,
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
        row["min_abs_skip"],
        "--max-abs-skip",
        row["max_abs_skip"],
        "--out",
        row["out"],
        "--summary-out",
        row["summary_out"],
        "--manifest-out",
        row["manifest_out"],
    ]
    if row.get("count_source_file"):
        command.extend(["--counts", row["count_source_file"]])
    return command


def status_row(
    row: dict[str, str],
    status: str,
    returncode: int,
    elapsed: float,
    message: str,
    command: list[str],
) -> dict[str, str]:
    return {
        "partition_id": row["partition_id"],
        "corpus": row["corpus"],
        "term_id": row["term_id"],
        "partition_index": row["partition_index"],
        "partition_count": row["partition_count"],
        "min_abs_skip": row["min_abs_skip"],
        "max_abs_skip": row["max_abs_skip"],
        "estimated_partition_hits": row["estimated_partition_hits"],
        "status": status,
        "returncode": str(returncode),
        "elapsed_seconds": str(elapsed),
        "out": row["out"],
        "manifest_out": row["manifest_out"],
        "message": message,
        "command": " ".join(shell_token(part) for part in command),
    }


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def selected_partition_ids(args: argparse.Namespace) -> set[str]:
    partition_ids = set(args.partition_id)
    for path in getattr(args, "partition_id_file", []):
        partition_ids.update(read_partition_id_file(path))
    return partition_ids


def read_partition_id_file(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return set()
    if "," in lines[0]:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or "partition_id" not in reader.fieldnames:
                raise ValueError(f"{path} must contain a partition_id column")
            return {row["partition_id"].strip() for row in reader if row.get("partition_id", "").strip()}
    return {line for line in lines if not line.startswith("#")}


def is_control_corpus(corpus: str) -> bool:
    return corpus.startswith(CONTROL_PREFIXES)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    plan_rows: list[dict[str, str]],
    selected_rows: list[dict[str, str]],
    status_rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    status_counts = {}
    for row in status_rows:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    payload: dict[str, Any] = {
        "script": "scripts/run_dynamic_span_partitions.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "plan": display_path(args.plan),
        "plan_rows": len(plan_rows),
        "selected_rows": len(selected_rows),
        "status_counts": status_counts,
        "dry_run": args.dry_run,
        "rerun": args.rerun,
        "status_out": display_path(args.status_out),
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def shell_token(value: str) -> str:
    if value and all(char.isalnum() or char in "/._=-" for char in value):
        return value
    return "'" + value.replace("'", "'\"'\"'") + "'"


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
