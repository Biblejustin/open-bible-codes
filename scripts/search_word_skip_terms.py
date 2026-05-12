#!/usr/bin/env python3
"""Search full word-token skip patterns."""

from __future__ import annotations

import argparse
import csv
import re
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
    "language",
    "input_term",
    "normalized_term",
    "normalized_tokens",
    "direction",
    "sequence",
    "word_count",
    "word_skip",
    "word_span",
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
    rows = search_word_skip_terms(
        corpus,
        term_rows,
        corpus_label=args.corpus_label,
        direction=args.direction,
        min_word_skip=args.min_word_skip,
        max_word_skip=args.max_word_skip,
        max_hits_per_term=args.max_hits_per_term,
    )
    write_rows(args.out, rows)
    print(args.out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Corpus config TOML.")
    parser.add_argument("--corpus-label", default="")
    parser.add_argument("--term", action="append", default=[])
    parser.add_argument("--terms", action="append", type=Path, default=[])
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--min-word-skip", type=int, default=1)
    parser.add_argument("--max-word-skip", type=int, default=3)
    parser.add_argument("--max-hits-per-term", type=int, default=200)
    parser.add_argument("--out", type=Path, default=Path("reports/word_skip_terms/hits.csv"))
    return parser


def read_term_rows(raw_terms: list[str], term_files: list[Path]) -> list[dict[str, str]]:
    rows = [
        {
            "term_id": f"inline_{index}",
            "concept": term,
            "category": "inline",
            "language": "",
            "term": term,
        }
        for index, term in enumerate(raw_terms, start=1)
    ]
    for path in term_files:
        with path.open(newline="", encoding="utf-8") as handle:
            rows.extend(dict(row) for row in csv.DictReader(handle))
    return rows


def search_word_skip_terms(
    corpus: Corpus,
    term_rows: list[dict[str, str]],
    *,
    corpus_label: str = "",
    direction: str = "both",
    min_word_skip: int = 1,
    max_word_skip: int = 3,
    max_hits_per_term: int = 200,
) -> list[dict[str, str | int]]:
    validate_word_skip_range(min_word_skip, max_word_skip)
    rows: list[dict[str, str | int]] = []
    directions = ("forward", "backward") if direction == "both" else (direction,)
    normalized_words = tuple(word.normalized_word for word in corpus.words)
    token_positions = token_positions_by_word(normalized_words)
    for term_row in term_rows:
        if not term_language_matches_corpus(term_row, corpus):
            continue
        query_tokens = normalize_term_tokens(
            term_row.get("term", ""),
            corpus.language,
            keep_hebrew_final_forms=corpus.keep_hebrew_final_forms,
        )
        if not query_tokens:
            continue
        hits = 0
        for direction_value in directions:
            target = query_tokens if direction_value == "forward" else tuple(reversed(query_tokens))
            for word_skip in range(min_word_skip, max_word_skip + 1):
                for start_index in matching_word_starts(
                    corpus.words,
                    target,
                    word_skip=word_skip,
                    token_positions=token_positions,
                ):
                    rows.append(
                        word_skip_hit_row(
                            corpus,
                            term_row,
                            normalized_tokens=query_tokens,
                            direction=direction_value,
                            sequence=target,
                            word_skip=word_skip,
                            start_index=start_index,
                            corpus_label=corpus_label,
                        )
                    )
                    hits += 1
                    if hits >= max_hits_per_term:
                        break
                if hits >= max_hits_per_term:
                    break
            if hits >= max_hits_per_term:
                break
    return rows


def normalize_term_tokens(
    value: str,
    language: str,
    *,
    keep_hebrew_final_forms: bool = False,
) -> tuple[str, ...]:
    tokens = []
    for raw_token in re.split(r"\s+", value.strip()):
        normalized = normalize_text(
            raw_token,
            language,
            keep_hebrew_final_forms=keep_hebrew_final_forms,
        )
        if normalized:
            tokens.append(normalized)
    return tuple(tokens)


def term_language_matches_corpus(term_row: dict[str, str], corpus: Corpus) -> bool:
    language = term_row.get("language", "").strip()
    return not language or language == corpus.language


def validate_word_skip_range(min_word_skip: int, max_word_skip: int) -> None:
    if min_word_skip < 1:
        raise ValueError("min_word_skip must be >= 1")
    if max_word_skip < min_word_skip:
        raise ValueError("max_word_skip must be >= min_word_skip")


def token_positions_by_word(words: tuple[str, ...]) -> dict[str, list[int]]:
    positions: dict[str, list[int]] = {}
    for index, word in enumerate(words):
        if not word:
            continue
        positions.setdefault(word, []).append(index)
    return positions


def matching_word_starts(
    words: tuple[WordSpan, ...],
    query_tokens: tuple[str, ...],
    *,
    word_skip: int = 1,
    token_positions: dict[str, list[int]] | None = None,
) -> list[int]:
    if not query_tokens:
        return []
    if token_positions is None:
        token_positions = token_positions_by_word(tuple(word.normalized_word for word in words))
    starts = []
    last_index = len(words) - 1
    for start_index in token_positions.get(query_tokens[0], []):
        end_index = start_index + (len(query_tokens) - 1) * word_skip
        if end_index > last_index:
            continue
        if all(
            words[start_index + token_index * word_skip].normalized_word == token
            for token_index, token in enumerate(query_tokens[1:], start=1)
        ):
            starts.append(start_index)
    return starts


def word_skip_hit_row(
    corpus: Corpus,
    term_row: dict[str, str],
    *,
    normalized_tokens: tuple[str, ...],
    direction: str,
    sequence: tuple[str, ...],
    word_skip: int,
    start_index: int,
    corpus_label: str,
) -> dict[str, str | int]:
    end_index = start_index + (len(sequence) - 1) * word_skip
    center_index = start_index + ((len(sequence) - 1) // 2) * word_skip
    start_word = corpus.words[start_index]
    end_word = corpus.words[end_index]
    center_word = corpus.words[center_index]
    normalized_term = " ".join(normalized_tokens)
    return {
        "pattern_type": "word_skip_ELS",
        "corpus_label": corpus_label,
        "corpus": corpus.name,
        "term_id": term_row.get("term_id", ""),
        "concept": term_row.get("concept", ""),
        "category": term_row.get("category", ""),
        "language": term_row.get("language", ""),
        "input_term": term_row.get("term", ""),
        "normalized_term": normalized_term,
        "normalized_tokens": normalized_term,
        "direction": direction,
        "sequence": " ".join(sequence),
        "word_count": len(sequence),
        "word_skip": word_skip,
        "word_span": end_index - start_index + 1,
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
