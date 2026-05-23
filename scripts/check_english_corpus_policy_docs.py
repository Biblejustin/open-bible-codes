#!/usr/bin/env python3
"""Validate English corpus docs keep missing BibleGateway rows deferred."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_PHRASES_BY_DOC = {
    Path("README.md"): (
        "accepted working set unless a lawful source package with clear",
        "do not treat the missing BibleGateway rows as an active blocker",
        "or scrape BibleGateway text to fill them",
    ),
    Path("docs/PRIVATE_ENGLISH_VERSIONS.md"): (
        "private-only CSV hooks and are not active blockers",
        "lawful source package with clear permission",
        "do not scrape BibleGateway text to fill missing rows",
    ),
    Path("docs/REMAINING_WORK_REGISTER.md"): (
        "## Deferred Inputs",
        "### BibleGateway English Corpora Without Lawful Local Text",
        "what we have is the working set",
        "do not scrape BibleGateway text to fill these rows",
    ),
    Path("docs/SOURCE_BASIS_AUDIT_QUEUE.md"): (
        "metadata-only unless a lawful",
        "local text or source package with clear permission is available",
    ),
}

FORBIDDEN_PHRASES_BY_DOC = {
    Path("docs/REMAINING_WORK_REGISTER.md"): (
        "### Remaining BibleGateway English Corpora",
        "This file tracks work that remains outside the missing copyrighted/private English CSVs.",
    ),
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_policy_docs(args.root)
    if failures:
        for failure in failures:
            print(f"English corpus policy failure: {failure}", file=sys.stderr)
        return 1
    print(f"English corpus policy docs ok: {args.root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    return parser


def validate_policy_docs(root: Path = Path(".")) -> list[str]:
    failures: list[str] = []
    for relative_path, phrases in REQUIRED_PHRASES_BY_DOC.items():
        path = root / relative_path
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            failures.append(f"{relative_path}: could not read: {exc}")
            continue
        normalized = normalize_space(text)
        for phrase in phrases:
            if phrase not in text and normalize_space(phrase) not in normalized:
                failures.append(f"{relative_path}: missing phrase: {phrase}")
        for phrase in FORBIDDEN_PHRASES_BY_DOC.get(relative_path, ()):
            if phrase in text or normalize_space(phrase) in normalized:
                failures.append(f"{relative_path}: forbidden stale phrase: {phrase}")
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
