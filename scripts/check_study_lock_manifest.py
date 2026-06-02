#!/usr/bin/env python3
"""Validate a prospective study lock manifest before running a study."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from els.protocol_runner import path_fingerprint


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        manifest = read_manifest(args.manifest)
    except (OSError, ValueError) as exc:
        print(f"lock manifest failure: {exc}")
        return 1
    failures = validate_manifest(
        manifest,
        required_settings=args.required_setting,
        allow_dirty=args.allow_dirty,
        verify_paths=not args.no_verify_paths,
    )
    if failures:
        for failure in failures:
            print(f"lock manifest failure: {failure}")
        return 1
    print(f"lock manifest ok: {args.manifest}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--required-setting", action="append", default=[])
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--no-verify-paths",
        action="store_true",
        help="Only validate manifest structure and settings; do not re-fingerprint locked paths.",
    )
    return parser


def read_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path} JSON root must be an object")
    return payload


def validate_manifest(
    manifest: dict[str, Any],
    *,
    required_settings: list[str],
    allow_dirty: bool,
    verify_paths: bool = True,
) -> list[str]:
    failures: list[str] = []
    if manifest.get("status") != "locked":
        failures.append("status is not locked")
    git = manifest.get("git", {})
    if git.get("dirty") and not allow_dirty:
        failures.append("git dirty-state is true")
    locked_paths = manifest.get("locked_paths", [])
    if not isinstance(locked_paths, list) or not locked_paths:
        failures.append("locked_paths is empty")
    elif verify_paths:
        failures.extend(validate_locked_paths(locked_paths))
    missing_paths = manifest.get("missing_paths", [])
    if missing_paths:
        failures.append("manifest has missing paths: " + ", ".join(str(path) for path in missing_paths))
    settings = manifest.get("settings", {})
    if not isinstance(settings, dict):
        failures.append("settings is not an object")
        settings = {}
    for key in required_settings:
        if key not in settings or not str(settings[key]).strip():
            failures.append(f"missing required setting: {key}")
    return failures


def validate_locked_paths(locked_paths: list[Any]) -> list[str]:
    failures: list[str] = []
    for locked in locked_paths:
        if not isinstance(locked, dict):
            failures.append("locked path entry is not an object")
            continue
        raw_path = locked.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            failures.append("locked path entry missing path")
            continue
        try:
            current = path_fingerprint(raw_path)
        except OSError as exc:
            failures.append(f"locked path unavailable: {raw_path}: {exc.strerror or exc}")
            continue
        if not locked_path_matches(locked, current):
            failures.append(f"locked path changed: {raw_path}")
    return failures


def locked_path_matches(locked: dict[str, Any], current: dict[str, Any]) -> bool:
    """Compare stable fingerprint fields and ignore filesystem timestamp churn."""

    if locked.get("path") != current.get("path"):
        return False
    locked_type = locked.get("type")
    if locked_type != current.get("type"):
        return False
    if locked_type == "file":
        return (
            locked.get("size") == current.get("size")
            and locked.get("sha256") == current.get("sha256")
        )
    if locked_type == "directory":
        if locked.get("entries") != current.get("entries"):
            return False
        if "legacy_tree_sha256" in locked:
            return locked.get("tree_sha256") == current.get("tree_sha256")
        return locked.get("tree_sha256") in {
            current.get("tree_sha256"),
            current.get("legacy_tree_sha256"),
        }
    return True


if __name__ == "__main__":
    raise SystemExit(main())
