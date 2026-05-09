#!/usr/bin/env python3
"""Write a preregistration lock manifest for prospective studies."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.protocol_runner import expanded_input_paths, path_fingerprints


OUT = Path("reports/study_locks/study_lock.manifest.json")


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    raw_paths = [str(path) for path in args.path]
    lock_paths = resolve_lock_paths(raw_paths, expand_corpus_configs=not args.no_expand_corpus_configs)
    missing = missing_paths(lock_paths)
    if missing and not args.allow_missing:
        for path in missing:
            print(f"missing lock path: {path}")
        return 1
    payload = build_payload(
        name=args.name,
        raw_paths=raw_paths,
        lock_paths=lock_paths,
        notes=args.note,
        settings=parse_settings(args.setting),
        missing=missing,
        expand_corpus_configs=not args.no_expand_corpus_configs,
        started=started,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--path", type=Path, action="append", required=True)
    parser.add_argument("--note", action="append", default=[])
    parser.add_argument(
        "--setting",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Record a locked non-file study setting such as skip_range=2..50.",
    )
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--allow-missing", action="store_true")
    parser.add_argument(
        "--no-expand-corpus-configs",
        action="store_true",
        help="Do not include source files referenced by corpus config TOML inputs.",
    )
    return parser


def resolve_lock_paths(raw_paths: list[str], *, expand_corpus_configs: bool) -> list[str]:
    if not expand_corpus_configs:
        return dedupe(raw_paths)
    return expanded_input_paths({"inputs": raw_paths})


def missing_paths(raw_paths: list[str]) -> list[str]:
    return [path for path in raw_paths if not Path(path).expanduser().exists()]


def build_payload(
    *,
    name: str,
    raw_paths: list[str],
    lock_paths: list[str],
    notes: list[str],
    settings: dict[str, str],
    missing: list[str],
    expand_corpus_configs: bool,
    started: float,
) -> dict[str, Any]:
    fingerprints = [] if missing else path_fingerprints(lock_paths)
    git = git_metadata()
    return {
        "tool": "build_study_lock_manifest",
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "name": name,
        "status": "failed" if missing else "locked",
        "git": git,
        "expand_corpus_configs": expand_corpus_configs,
        "requested_paths": raw_paths,
        "missing_paths": missing,
        "settings": settings,
        "notes": notes,
        "locked_paths": fingerprints,
    }


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        key = str(Path(value).expanduser())
        if key in seen:
            continue
        seen.add(key)
        result.append(value)
    return result


def parse_settings(raw_settings: list[str]) -> dict[str, str]:
    settings: dict[str, str] = {}
    for raw in raw_settings:
        if "=" not in raw:
            raise ValueError(f"setting must be KEY=VALUE: {raw}")
        key, value = raw.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"setting key cannot be empty: {raw}")
        settings[key] = value.strip()
    return settings


def git_metadata() -> dict[str, Any]:
    return {
        "commit": run_git("rev-parse", "--short", "HEAD"),
        "dirty": bool(run_git("status", "--short")),
    }


def run_git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())
