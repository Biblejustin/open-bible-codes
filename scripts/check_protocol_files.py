#!/usr/bin/env python3
"""Validate tracked protocol TOML files without running them."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from els.protocol_runner import load_protocol


PROTOCOLS_DIR = Path("protocols")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_protocol_files(args.protocols_dir)
    if failures:
        for failure in failures:
            print(f"protocol file failure: {failure}", file=sys.stderr)
        return 1
    print(f"protocol files ok: {args.protocols_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocols-dir", type=Path, default=PROTOCOLS_DIR)
    return parser


def validate_protocol_files(protocols_dir: Path = PROTOCOLS_DIR) -> list[str]:
    failures: list[str] = []
    if not protocols_dir.exists():
        return [f"{protocols_dir} is missing"]

    paths = sorted(protocols_dir.glob("*.toml"))
    if not paths:
        return [f"{protocols_dir} has no protocol TOML files"]

    seen_names: dict[str, Path] = {}
    for path in paths:
        try:
            protocol = load_protocol(path)
        except Exception as exc:  # noqa: BLE001 - convert load errors to checker rows.
            failures.append(f"{path}: {exc}")
            continue
        name = str(protocol.get("name", "")).strip()
        previous = seen_names.get(name)
        if previous is not None:
            failures.append(f"{path} duplicate protocol name {name}: also in {previous}")
        seen_names[name] = path
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
