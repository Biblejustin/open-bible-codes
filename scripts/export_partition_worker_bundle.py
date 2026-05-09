#!/usr/bin/env python3
"""Package completed worker partition artifacts into a portable zip."""

from __future__ import annotations

import argparse
import json
import time
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from scripts.export_dynamic_span_hits import ROOT
from scripts.plan_dynamic_span_partitions import DEFAULT_OUT as DEFAULT_PLAN
from scripts.run_dynamic_span_partitions import read_rows


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    assignment_rows = read_rows(args.assignment)
    plan_rows = read_rows(args.plan)
    plan_by_id = {row["partition_id"]: row for row in plan_rows}
    selected = [plan_by_id[row["partition_id"]] for row in assignment_rows]
    manifest, files = collect_artifacts(selected, require_compressed=not args.allow_raw)
    if manifest["missing"] and not args.allow_missing:
        write_bundle_manifest(args.manifest_out, args, manifest, started)
        print(args.manifest_out)
        return 1
    write_bundle(args.out, args.assignment, manifest, files, started)
    write_bundle_manifest(args.manifest_out, args, manifest, started)
    print(args.out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assignment", type=Path, required=True)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, default=ROOT / "reports/dynamic_skip_focus/worker_bundle.manifest.json")
    parser.add_argument("--allow-raw", action="store_true")
    parser.add_argument("--allow-missing", action="store_true")
    return parser


def collect_artifacts(
    rows: list[dict[str, str]],
    *,
    require_compressed: bool,
) -> tuple[dict[str, Any], list[Path]]:
    files: list[Path] = []
    completed: list[str] = []
    missing: list[dict[str, str]] = []
    for row in rows:
        artifacts = artifacts_for_row(row, require_compressed=require_compressed)
        required = [path for _label, path, is_required in artifacts if is_required]
        missing_required = [path for path in required if not path.exists()]
        if missing_required:
            missing.append(
                {
                    "partition_id": row["partition_id"],
                    "missing": ", ".join(display_path(path) for path in missing_required),
                }
            )
            continue
        completed.append(row["partition_id"])
        for _label, path, _is_required in artifacts:
            if path.exists() and path not in files:
                files.append(path)
    manifest = {
        "assigned_partitions": len(rows),
        "completed_partitions": len(completed),
        "missing_partitions": len(missing),
        "completed": completed,
        "missing": missing,
        "files": [display_path(path) for path in files],
    }
    return manifest, files


def artifacts_for_row(row: dict[str, str], *, require_compressed: bool) -> list[tuple[str, Path, bool]]:
    raw_out = absolute_path(row["out"])
    compressed_out = raw_out.with_suffix(raw_out.suffix + ".gz")
    selected_out = compressed_out if compressed_out.exists() or require_compressed else raw_out
    return [
        ("hits", selected_out, True),
        ("manifest", absolute_path(row["manifest_out"]), True),
        ("summary", absolute_path(row["summary_out"]), False),
    ]


def write_bundle(
    out: Path,
    assignment: Path,
    manifest: dict[str, Any],
    files: list[Path],
    started: float,
) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "script": "scripts/export_partition_worker_bundle.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "assignment": display_path(assignment),
        **manifest,
    }
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_STORED) as archive:
        archive.writestr(
            "worker_bundle_manifest.json",
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        )
        archive.write(assignment, "assignment.csv")
        archive.writestr("partition_ids.txt", "\n".join(manifest["completed"]) + "\n")
        for path in files:
            archive.write(path, display_path(path))


def write_bundle_manifest(
    path: Path,
    args: argparse.Namespace,
    manifest: dict[str, Any],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "script": "scripts/export_partition_worker_bundle.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "assignment": display_path(args.assignment),
        "out": display_path(args.out),
        **manifest,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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
