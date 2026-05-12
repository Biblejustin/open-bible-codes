#!/usr/bin/env python3
"""Run opt-in ELS search over a deterministic transformed corpus."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from els.corpus import Corpus, load_corpus
from els.search import ELSHit, find_els
from els.transforms import TRANSFORM_HEBREW_ATBASH, transform_corpus


FIELDNAMES = [
    "transform",
    "corpus_label",
    "base_corpus",
    "transformed_corpus",
    "term_id",
    "concept",
    "category",
    "input_term",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "start_offset",
    "end_offset",
    "span_letters",
    "sequence",
    "start_ref",
    "end_ref",
    "start_source",
    "end_source",
    "center_offset",
    "center_ref",
    "center_source",
    "center_word_index",
    "center_word",
    "center_normalized_word",
]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    corpus = load_corpus(args.config)
    transformed = transform_corpus(corpus, args.transform)
    term_rows = read_term_rows(args.term, args.terms)
    rows = transformed_search_rows(
        corpus,
        transformed,
        term_rows,
        transform=args.transform,
        corpus_label=args.corpus_label,
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        max_hits_per_term=args.max_hits_per_term,
    )
    write_rows(args.out, rows)
    print(args.out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Corpus config TOML.")
    parser.add_argument("--corpus-label", default="")
    parser.add_argument("--transform", default=TRANSFORM_HEBREW_ATBASH)
    parser.add_argument("--term", action="append", default=[])
    parser.add_argument("--terms", action="append", type=Path, default=[])
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=100)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--max-hits-per-term", type=int, default=200)
    parser.add_argument("--out", type=Path, default=Path("reports/transformed_els/hits.csv"))
    return parser


def read_term_rows(raw_terms: list[str], term_files: list[Path]) -> list[dict[str, str]]:
    rows = [
        {
            "term_id": f"inline_{index}",
            "concept": term,
            "category": "inline",
            "term": term,
        }
        for index, term in enumerate(raw_terms, start=1)
    ]
    for path in term_files:
        with path.open(newline="", encoding="utf-8") as handle:
            rows.extend(dict(row) for row in csv.DictReader(handle))
    return rows


def transformed_search_rows(
    base_corpus: Corpus,
    transformed: Corpus,
    term_rows: list[dict[str, str]],
    *,
    transform: str,
    corpus_label: str = "",
    min_skip: int,
    max_skip: int,
    direction: str,
    max_hits_per_term: int,
) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for term_row in term_rows:
        term = term_row.get("term", "")
        if not term:
            continue
        try:
            hits = find_els(
                transformed,
                term,
                min_skip=min_skip,
                max_skip=max_skip,
                direction=direction,
                max_hits=max_hits_per_term,
            )
            for hit in hits:
                rows.append(
                    transformed_hit_row(
                        base_corpus,
                        transformed,
                        term_row,
                        hit,
                        transform=transform,
                        corpus_label=corpus_label,
                    )
                )
        except ValueError:
            continue
    return rows


def transformed_hit_row(
    base_corpus: Corpus,
    transformed: Corpus,
    term_row: dict[str, str],
    hit: ELSHit,
    *,
    transform: str,
    corpus_label: str = "",
) -> dict[str, str | int]:
    row = {
        "transform": transform,
        "corpus_label": corpus_label,
        "base_corpus": base_corpus.name,
        "transformed_corpus": transformed.name,
        "term_id": term_row.get("term_id", ""),
        "concept": term_row.get("concept", ""),
        "category": term_row.get("category", ""),
        "input_term": term_row.get("term", ""),
    }
    row.update(hit.as_row())
    return row


def write_rows(path: Path, rows: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
