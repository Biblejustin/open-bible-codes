#!/usr/bin/env python3
"""Guard public-facing docs against unsupported claim language."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_PATHS = (Path("README.md"), Path("docs"), Path("claims"), Path("protocols"))
SCAN_SUFFIXES = {".md", ".csv", ".toml"}
OVERCLAIM_RE = re.compile(
    r"\bprov(?:e|es|ed)\b|\bproof\b|statistically[ -]impossible|"
    r"prophecy[ -]confirmed|validation of inspiration|claim[- ]level",
    re.IGNORECASE,
)
WRR_EXACT_OVERCLAIM_RE = re.compile(
    r"\bexact[- ]published WRR (?:has been |was |is )?reproduced\b|"
    r"\bexact[- ]published WRR reproduction (?:is|was|has been) "
    r"(?:closed|complete|finished|ready|reproduced)\b|"
    r"\bexact WRR reproduction (?:is|was|has been) "
    r"(?:closed|complete|finished|ready|reproduced)\b",
    re.IGNORECASE,
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_public_claim_language(args.path)
    if failures:
        for failure in failures:
            print(f"public claim-language failure: {failure}", file=sys.stderr)
        return 1
    print("public claim language ok")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="*",
        type=Path,
        default=list(DEFAULT_PATHS),
        help="Files or directories to scan. Defaults to README.md, docs/, claims/, and protocols/.",
    )
    return parser


def validate_public_claim_language(paths: list[Path] | None = None) -> list[str]:
    failures: list[str] = []
    for path in iter_scan_paths(paths or list(DEFAULT_PATHS)):
        lines = path.read_text(encoding="utf-8").splitlines()
        fenced = fenced_code_lines(lines) if path.suffix == ".md" else set()
        heading = ""
        for line_no, line in enumerate(lines, start=1):
            if path.suffix == ".md" and line.lstrip().startswith("#"):
                heading = line.strip("# ").lower()
            if line_no in fenced:
                continue
            if "forbidden" in heading:
                continue
            for match in OVERCLAIM_RE.finditer(line):
                failures.append(f"{path}:{line_no}: unsupported claim language `{match.group(0)}`")
            if "do not" in line.lower():
                continue
            for match in WRR_EXACT_OVERCLAIM_RE.finditer(line):
                failures.append(
                    f"{path}:{line_no}: unsupported WRR exact-published language `{match.group(0)}`"
                )
    return failures


def iter_scan_paths(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_dir():
            out.extend(
                sorted(
                    candidate
                    for candidate in path.rglob("*")
                    if candidate.is_file() and candidate.suffix in SCAN_SUFFIXES
                )
            )
        elif path.suffix in SCAN_SUFFIXES:
            out.append(path)
    return out


def fenced_code_lines(lines: list[str]) -> set[int]:
    inside = False
    fenced: set[int] = set()
    for index, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            inside = not inside
            fenced.add(index)
            continue
        if inside:
            fenced.add(index)
    return fenced


if __name__ == "__main__":
    raise SystemExit(main())
