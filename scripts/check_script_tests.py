#!/usr/bin/env python3
"""Validate every script module has a matching test module."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPTS_DIR = Path("scripts")
TESTS_DIR = Path("tests")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_script_tests(args.scripts_dir, args.tests_dir)
    if failures:
        for failure in failures:
            print(f"script test failure: {failure}", file=sys.stderr)
        return 1
    print(f"script tests ok: {args.scripts_dir} -> {args.tests_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scripts-dir", type=Path, default=SCRIPTS_DIR)
    parser.add_argument("--tests-dir", type=Path, default=TESTS_DIR)
    return parser


def validate_script_tests(
    scripts_dir: Path = SCRIPTS_DIR,
    tests_dir: Path = TESTS_DIR,
) -> list[str]:
    failures: list[str] = []
    if not scripts_dir.exists():
        return [f"{scripts_dir} is missing"]
    if not tests_dir.exists():
        return [f"{tests_dir} is missing"]

    scripts = sorted(
        path
        for path in scripts_dir.glob("*.py")
        if path.name != "__init__.py"
    )
    if not scripts:
        failures.append(f"{scripts_dir} has no script modules")

    for script in scripts:
        expected = expected_test_path(script, tests_dir)
        if not expected.exists():
            failures.append(f"{script} missing matching test {expected}")

    return failures


def expected_test_path(script: Path, tests_dir: Path = TESTS_DIR) -> Path:
    return tests_dir / f"test_{script.name}"


if __name__ == "__main__":
    raise SystemExit(main())
