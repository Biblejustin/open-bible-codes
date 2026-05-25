#!/usr/bin/env python3
"""Validate generated prospective lane status doc freshness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts import build_prospective_lane_status as lane_status
from scripts import scaffold_prospective_study as scaffold


DEFAULT_DOC = lane_status.DEFAULT_OUT
DEFAULT_PROFILES = lane_status.DEFAULT_PROFILES


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_lane_status_doc(args.doc, args.profiles)
    if failures:
        for failure in failures:
            print(f"prospective lane-status doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"prospective lane-status doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    return parser


def validate_lane_status_doc(doc: Path, profiles_path: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    try:
        profiles = scaffold.load_profiles(profiles_path)
    except (OSError, ValueError) as exc:
        return [f"could not read profile file {profiles_path}: {exc}"]

    expected = lane_status.render_markdown(profiles, Path(display_path(profiles_path)))
    actual = doc.read_text(encoding="utf-8")
    if actual != expected:
        return [
            f"{doc} is stale; rerun python3 -m scripts.build_prospective_lane_status"
        ]
    return []


def display_path(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
