#!/usr/bin/env python3
"""Fail if preregistration drafts still contain bracketed placeholders."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"\[[A-Za-z0-9_ .|/;:'-]+\]")
TASK_LIST_MARKERS = {"[ ]", "[x]", "[X]"}
STALE_TEMPLATE_PHRASES = (
    "Status: template",
    "copy before use",
    "pending current preregistration commit",
    "State the exact question",
    "Example shape:",
    "State whether the sources",
)


@dataclass(frozen=True)
class PlaceholderHit:
    path: Path
    line_number: int
    column_number: int
    placeholder: str


@dataclass(frozen=True)
class StaleTemplatePhraseHit:
    path: Path
    line_number: int
    column_number: int
    phrase: str


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    hits = []
    stale_hits = []
    for path in args.path:
        hits.extend(find_placeholders(path, allowed=set(args.allow)))
        stale_hits.extend(find_stale_template_phrases(path))
    if hits or stale_hits:
        for hit in hits:
            print(
                f"unresolved preregistration placeholder: "
                f"{hit.path}:{hit.line_number}:{hit.column_number}: {hit.placeholder}"
            )
        for hit in stale_hits:
            print(
                f"stale preregistration template phrase: "
                f"{hit.path}:{hit.line_number}:{hit.column_number}: {hit.phrase}"
            )
        return 1
    print("preregistration placeholders ok")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, nargs="+")
    parser.add_argument(
        "--allow",
        action="append",
        default=[],
        metavar="[placeholder]",
        help="Allow a specific bracketed placeholder token.",
    )
    return parser


def find_placeholders(path: Path, *, allowed: set[str]) -> list[PlaceholderHit]:
    hits: list[PlaceholderHit] = []
    for line_index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for match in PLACEHOLDER_RE.finditer(line):
            placeholder = match.group(0)
            if placeholder in allowed or placeholder in TASK_LIST_MARKERS:
                continue
            hits.append(
                PlaceholderHit(
                    path=path,
                    line_number=line_index,
                    column_number=match.start() + 1,
                    placeholder=placeholder,
                )
            )
    return hits


def find_stale_template_phrases(path: Path) -> list[StaleTemplatePhraseHit]:
    hits: list[StaleTemplatePhraseHit] = []
    for line_index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for phrase in STALE_TEMPLATE_PHRASES:
            column = line.find(phrase)
            if column == -1:
                continue
            hits.append(
                StaleTemplatePhraseHit(
                    path=path,
                    line_number=line_index,
                    column_number=column + 1,
                    phrase=phrase,
                )
            )
    return hits


if __name__ == "__main__":
    raise SystemExit(main())
