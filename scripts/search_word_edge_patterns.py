#!/usr/bin/env python3
"""Search consecutive-word acrostic and telestic patterns."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from els.corpus import Corpus, WordSpan, load_corpus
from els.normalization import normalize_text


FIELDNAMES = [
    "pattern_type",
    "corpus_label",
    "corpus",
    "term_id",
    "concept",
    "category",
    "input_term",
    "normalized_term",
    "direction",
    "sequence",
    "word_count",
    "start_word_global_index",
    "end_word_global_index",
    "start_ref",
    "end_ref",
    "center_ref",
    "start_word",
    "end_word",
    "center_word",
    "center_normalized_word",
]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    corpus = load_corpus(args.config)
    term_rows = read_term_rows(args.term, args.terms)
    rows = search_word_edge_patterns(
        corpus,
        term_rows,
        corpus_label=args.corpus_label,
        pattern=args.pattern,
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
    parser.add_argument("--term", action="append", default=[])
    parser.add_argument("--terms", action="append", type=Path, default=[])
    parser.add_argument("--pattern", choices=["acrostic", "telestic", "both"], default="both")
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--max-hits-per-term", type=int, default=200)
    parser.add_argument("--out", type=Path, default=Path("reports/word_edge_patterns/hits.csv"))
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


def search_word_edge_patterns(
    corpus: Corpus,
    term_rows: list[dict[str, str]],
    *,
    corpus_label: str = "",
    pattern: str = "both",
    direction: str = "both",
    max_hits_per_term: int = 200,
) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    patterns = ("acrostic", "telestic") if pattern == "both" else (pattern,)
    directions = ("forward", "backward") if direction == "both" else (direction,)
    letters_by_pattern = {pattern_type: word_edge_letters(corpus.words, pattern_type) for pattern_type in patterns}
    for term_row in term_rows:
        query = normalize_text(
            term_row.get("term", ""),
            corpus.language,
            keep_hebrew_final_forms=corpus.keep_hebrew_final_forms,
        )
        if not query:
            continue
        for pattern_type in patterns:
            letters = letters_by_pattern[pattern_type]
            for direction_value in directions:
                target = query if direction_value == "forward" else query[::-1]
                hits = 0
                for start_index in matching_starts(letters, target):
                    rows.append(
                        word_edge_hit_row(
                            corpus,
                            term_row,
                            normalized_term=query,
                            pattern_type=pattern_type,
                            corpus_label=corpus_label,
                            direction=direction_value,
                            sequence=target,
                            start_index=start_index,
                        )
                    )
                    hits += 1
                    if hits >= max_hits_per_term:
                        break
    return rows


def word_edge_letters(words: tuple[WordSpan, ...], pattern_type: str) -> str:
    if pattern_type == "acrostic":
        return "".join(word.normalized_word[0] for word in words if word.normalized_word)
    if pattern_type == "telestic":
        return "".join(word.normalized_word[-1] for word in words if word.normalized_word)
    raise ValueError(f"unknown word-edge pattern type: {pattern_type}")


def matching_starts(text: str, query: str) -> list[int]:
    starts = []
    position = text.find(query)
    while position != -1:
        starts.append(position)
        position = text.find(query, position + 1)
    return starts


def word_edge_hit_row(
    corpus: Corpus,
    term_row: dict[str, str],
    *,
    normalized_term: str,
    pattern_type: str,
    corpus_label: str,
    direction: str,
    sequence: str,
    start_index: int,
) -> dict[str, str | int]:
    end_index = start_index + len(sequence) - 1
    center_index = start_index + (len(sequence) - 1) // 2
    start_word = corpus.words[start_index]
    end_word = corpus.words[end_index]
    center_word = corpus.words[center_index]
    return {
        "pattern_type": pattern_type,
        "corpus_label": corpus_label,
        "corpus": corpus.name,
        "term_id": term_row.get("term_id", ""),
        "concept": term_row.get("concept", ""),
        "category": term_row.get("category", ""),
        "input_term": term_row.get("term", ""),
        "normalized_term": normalized_term,
        "direction": direction,
        "sequence": sequence,
        "word_count": len(sequence),
        "start_word_global_index": start_index,
        "end_word_global_index": end_index,
        "start_ref": start_word.ref,
        "end_ref": end_word.ref,
        "center_ref": center_word.ref,
        "start_word": start_word.raw_word,
        "end_word": end_word.raw_word,
        "center_word": center_word.raw_word,
        "center_normalized_word": center_word.normalized_word,
    }


def write_rows(path: Path, rows: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
