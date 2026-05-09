#!/usr/bin/env python3
"""Build an English screening term list from declared term concepts."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

from els.normalization import normalize_text


DEFAULT_TERMS_DIR = Path("terms")
DEFAULT_OUT = DEFAULT_TERMS_DIR / "english_search_terms.csv"
EXCLUDED_DEFAULT_FILES = {
    "english_search_terms.csv",
    "null_controls.csv",
}
FIELDNAMES = ["term_id", "concept", "category", "language", "term", "notes"]


@dataclass
class EnglishTerm:
    concept: str
    category: str
    term: str
    normalized: str
    sources: set[str] = field(default_factory=set)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source_paths = args.source or default_source_paths(args.terms_dir, args.include_controls)
    rows, skipped = build_english_rows(source_paths)
    write_rows(args.out, rows)
    print(args.out)
    print(f"rows={len(rows)} skipped={skipped}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms-dir", type=Path, default=DEFAULT_TERMS_DIR)
    parser.add_argument("--source", type=Path, action="append", default=[])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--include-controls",
        action="store_true",
        help="Include control term files such as null_controls.csv.",
    )
    return parser


def default_source_paths(terms_dir: Path, include_controls: bool) -> list[Path]:
    excluded = set(EXCLUDED_DEFAULT_FILES)
    if include_controls:
        excluded.discard("null_controls.csv")
    return [
        path
        for path in sorted(terms_dir.glob("*.csv"))
        if path.name not in excluded
    ]


def build_english_rows(paths: list[Path]) -> tuple[list[dict[str, str]], int]:
    terms_by_key: dict[tuple[str, str, str], EnglishTerm] = {}
    skipped = 0
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                concept = clean_cell(row.get("concept", ""))
                category = clean_cell(row.get("category", "")) or "uncategorized"
                if not concept or contains_decimal_digit(concept):
                    skipped += 1
                    continue
                normalized = normalize_text(concept, "english")
                if not normalized:
                    skipped += 1
                    continue
                key = (normalized, concept.casefold(), category.casefold())
                term = terms_by_key.setdefault(
                    key,
                    EnglishTerm(
                        concept=concept,
                        category=category,
                        term=concept,
                        normalized=normalized,
                    ),
                )
                term.sources.add(f"{path.name}:{clean_cell(row.get('term_id', ''))}")
    return rows_from_terms(terms_by_key.values()), skipped


def rows_from_terms(terms: Iterable[EnglishTerm]) -> list[dict[str, str]]:
    base_counts: dict[str, int] = defaultdict(int)
    rows = []
    for term in sorted(terms, key=lambda item: (item.category, item.concept, item.normalized)):
        base = f"eng_{slug(term.concept)}"
        base_counts[base] += 1
        term_id = base if base_counts[base] == 1 else f"{base}_{base_counts[base]}"
        rows.append(
            {
                "term_id": term_id,
                "concept": term.concept,
                "category": term.category,
                "language": "english",
                "term": term.term,
                "notes": source_note(term.sources),
            }
        )
    return rows


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def clean_cell(value: str) -> str:
    return " ".join(value.strip().split())


def contains_decimal_digit(value: str) -> bool:
    return any(char.isdecimal() for char in value)


def slug(value: str) -> str:
    normalized = normalize_text(value, "english")
    if normalized:
        return normalized[:80]
    ascii_slug = "_".join(re.findall(r"[a-z0-9]+", value.lower()))
    return ascii_slug[:80] or "term"


def source_note(sources: set[str]) -> str:
    ordered = sorted(sources)
    shown = ordered[:5]
    suffix = "" if len(ordered) <= len(shown) else f"; +{len(ordered) - len(shown)} more"
    return "generated from declared concept labels; sources: " + "; ".join(shown) + suffix


if __name__ == "__main__":
    raise SystemExit(main())
