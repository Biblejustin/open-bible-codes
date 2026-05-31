#!/usr/bin/env python3
"""Validate study-mapping term ids point at tracked term rows."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_MAPPINGS_DIR = Path("data/study/mappings")
DEFAULT_TERMS_DIR = Path("terms")
MAPPING_TERM_COLUMNS = (
    ("thematic_chapters.csv", "term_id"),
    ("author_book_mapping.csv", "author_term_id"),
    ("protagonist_narrative_mapping.csv", "protagonist_term_id"),
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_mapping_term_ids(args.mappings_dir, args.terms_dir)
    if failures:
        for failure in failures:
            print(f"study mapping term-id failure: {failure}", file=sys.stderr)
        return 1
    print(f"study mapping term ids ok: {args.mappings_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mappings-dir", type=Path, default=DEFAULT_MAPPINGS_DIR)
    parser.add_argument("--terms-dir", type=Path, default=DEFAULT_TERMS_DIR)
    return parser


def validate_mapping_term_ids(
    mappings_dir: Path = DEFAULT_MAPPINGS_DIR,
    terms_dir: Path = DEFAULT_TERMS_DIR,
) -> list[str]:
    term_ids, term_failures = load_term_ids(terms_dir)
    failures = list(term_failures)
    if not term_ids:
        failures.append(f"{terms_dir} has no term_id rows")
        return failures

    for filename, column in MAPPING_TERM_COLUMNS:
        path = mappings_dir / filename
        if not path.exists():
            failures.append(f"{path} is missing")
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if column not in (reader.fieldnames or []):
                failures.append(f"{path} missing required term-id column: {column}")
                continue
            for row_number, row in enumerate(reader, start=2):
                term_id = clean(row.get(column))
                if term_id and term_id not in term_ids:
                    failures.append(f"{path}:{row_number} unknown {column}: {term_id}")
    return failures


def load_term_ids(terms_dir: Path) -> tuple[set[str], list[str]]:
    failures: list[str] = []
    term_ids: set[str] = set()
    if not terms_dir.exists():
        return term_ids, [f"{terms_dir} is missing"]
    for path in sorted(terms_dir.rglob("*.csv")):
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if "term_id" not in (reader.fieldnames or []):
                continue
            for row_number, row in enumerate(reader, start=2):
                term_id = clean(row.get("term_id"))
                if not term_id:
                    failures.append(f"{path}:{row_number} missing term_id")
                    continue
                term_ids.add(term_id)
    return term_ids, failures


def clean(value: str | None) -> str:
    return (value or "").strip()


if __name__ == "__main__":
    raise SystemExit(main())
