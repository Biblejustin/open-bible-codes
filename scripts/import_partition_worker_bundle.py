#!/usr/bin/env python3
"""Import completed worker partition artifacts into the coordinator checkout."""

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


DEFAULT_IMPORT_DIR = ROOT / "reports/dynamic_skip_focus/worker_imports"
ALLOWED_SUFFIXES = (".csv", ".csv.gz", ".manifest.json", ".md")
PARTITION_PREFIX = "reports/dynamic_skip_focus/partitions/"


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    all_results: list[dict[str, Any]] = []
    failed = False
    for bundle in args.bundle:
        try:
            results = import_bundle(bundle, dry_run=args.dry_run, overwrite=args.overwrite)
            all_results.extend(results)
        except Exception as exc:
            failed = True
            all_results.append({"bundle": str(bundle), "status": "failed", "message": str(exc)})
    write_manifest(args.manifest_out, args, all_results, started)
    print(args.manifest_out)
    return 1 if failed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path, nargs="+")
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_IMPORT_DIR / "latest_import.manifest.json")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser


def import_bundle(bundle: Path, *, dry_run: bool, overwrite: bool) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with zipfile.ZipFile(bundle) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            if not is_partition_artifact(info.filename):
                results.append(
                    {
                        "bundle": str(bundle),
                        "member": info.filename,
                        "status": "skipped_metadata",
                    }
                )
                continue
            target = safe_target(info.filename)
            if target.exists() and not overwrite:
                if target.stat().st_size == info.file_size:
                    status = "skipped_existing"
                else:
                    raise FileExistsError(f"{target} exists with different size")
            else:
                status = "dry_run" if dry_run else "imported"
                if not dry_run:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(info) as source, target.open("wb") as dest:
                        dest.write(source.read())
            results.append(
                {
                    "bundle": str(bundle),
                    "member": info.filename,
                    "target": display_path(target),
                    "status": status,
                    "bytes": info.file_size,
                }
            )
    return results


def is_partition_artifact(member: str) -> bool:
    if member.startswith("/") or "\\" in member:
        return False
    path = Path(member)
    if ".." in path.parts:
        return False
    if not member.startswith(PARTITION_PREFIX):
        return False
    return any(member.endswith(suffix) for suffix in ALLOWED_SUFFIXES)


def safe_target(member: str) -> Path:
    path = Path(member)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe zip path: {member}")
    target = (ROOT / path).resolve()
    root = ROOT.resolve()
    if root not in target.parents and target != root:
        raise ValueError(f"zip path escapes repository: {member}")
    return target


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    results: list[dict[str, Any]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    status_counts: dict[str, int] = {}
    for row in results:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    payload = {
        "script": "scripts/import_partition_worker_bundle.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "dry_run": args.dry_run,
        "overwrite": args.overwrite,
        "bundles": [str(path) for path in args.bundle],
        "status_counts": status_counts,
        "rows": results,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
