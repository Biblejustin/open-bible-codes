#!/usr/bin/env python3
"""Validate every check_* script is referenced by a release or protocol path."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(".")
SCRIPTS_DIR = Path("scripts")
PROTOCOLS_DIR = Path("protocols")
MAKEFILE = Path("Makefile")
PREFLIGHT = Path("scripts/preflight_real_report_run.py")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_check_script_wiring(args.root)
    if failures:
        for failure in failures:
            print(f"check-script wiring failure: {failure}", file=sys.stderr)
        return 1
    print(f"check-script wiring ok: {args.root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    return parser


def validate_check_script_wiring(root: Path = ROOT) -> list[str]:
    scripts_dir = root / SCRIPTS_DIR
    if not scripts_dir.exists():
        return [f"{scripts_dir} is missing"]

    check_scripts = sorted(scripts_dir.glob("check_*.py"))
    if not check_scripts:
        return [f"{scripts_dir} has no check_*.py scripts"]

    wiring_text = "\n".join(read_wiring_files(root))
    failures: list[str] = []
    for script in check_scripts:
        relative = script.relative_to(root).as_posix()
        module = relative[:-3].replace("/", ".")
        if relative not in wiring_text and module not in wiring_text:
            failures.append(
                f"{relative} is not referenced by Makefile, preflight, or protocols"
            )
    return failures


def read_wiring_files(root: Path) -> list[str]:
    texts: list[str] = []
    for path in [root / MAKEFILE, root / PREFLIGHT]:
        if path.exists():
            texts.append(path.read_text(encoding="utf-8"))

    protocols_dir = root / PROTOCOLS_DIR
    if protocols_dir.exists():
        for path in sorted(protocols_dir.glob("*.toml")):
            texts.append(path.read_text(encoding="utf-8"))
    return texts


if __name__ == "__main__":
    raise SystemExit(main())
