#!/usr/bin/env python3
"""Analyze related modern-name ELS pairs by overlap, chapter, and proximity."""

from __future__ import annotations

import csv
from bisect import bisect_left
from dataclasses import dataclass
from pathlib import Path

from els.cli import accepted_term_languages
from els.corpus import Corpus, load_corpus
from els.search import (
    ELSHit,
    build_hit,
    iter_forward_matches_in_lanes,
    make_lanes,
    normalize_for_corpus,
)


TERMS_PATH = Path("terms/modern_names_dates.csv")
SUMMARY_OUT = Path("reports/related_name_pairs_summary.csv")
EXAMPLES_OUT = Path("reports/related_name_pairs_examples.csv")

RELATED_PAIRS = [
    ("trump_h", "vance_h"),
    ("trump_h", "vance_alt_h"),
    ("trump_h", "netanyahu_h"),
    ("trump_h", "biden_h"),
    ("biden_h", "harris_h"),
    ("netanyahu_h", "hamas_h"),
    ("netanyahu_h", "israel_h"),
    ("netanyahu_h", "gaza_h"),
    ("netanyahu_h", "iran_h"),
    ("netanyahu_h", "persia_h"),
    ("trump_h", "iran_h"),
    ("trump_h", "persia_h"),
    ("israel_h", "iran_h"),
    ("israel_h", "persia_h"),
    ("hamas_h", "iran_h"),
    ("hamas_h", "persia_h"),
    ("iran_h", "gaza_h"),
    ("persia_h", "gaza_h"),
    ("putin_h", "zelensky_h"),
    ("israel_h", "gaza_h"),
    ("israel_h", "hamas_h"),
    ("hamas_h", "gaza_h"),
    ("trump_g", "vance_g"),
    ("trump_g", "netanyahu_g"),
    ("trump_g", "biden_g"),
    ("biden_g", "harris_g"),
    ("netanyahu_g", "hamas_g"),
    ("netanyahu_g", "israel_g"),
    ("netanyahu_g", "gaza_g"),
    ("netanyahu_g", "iran_g"),
    ("netanyahu_g", "persia_g"),
    ("trump_g", "iran_g"),
    ("trump_g", "persia_g"),
    ("israel_g", "iran_g"),
    ("israel_g", "persia_g"),
    ("hamas_g", "iran_g"),
    ("hamas_g", "persia_g"),
    ("iran_g", "gaza_g"),
    ("persia_g", "gaza_g"),
    ("putin_g", "zelensky_g"),
    ("israel_g", "gaza_g"),
    ("israel_g", "hamas_g"),
    ("hamas_g", "gaza_g"),
]


@dataclass(frozen=True)
class PairExample:
    corpus: str
    left_term_id: str
    left_concept: str
    left_term: str
    left_skip: int
    left_start_ref: str
    left_end_ref: str
    left_center_ref: str
    left_center_word_index: int | str
    left_center_word: str
    left_center_normalized_word: str
    right_term_id: str
    right_concept: str
    right_term: str
    right_skip: int
    right_start_ref: str
    right_end_ref: str
    right_center_ref: str
    right_center_word_index: int | str
    right_center_word: str
    right_center_normalized_word: str
    span_gap: int
    center_distance: float
    shared_chapters: str


def main() -> int:
    corpora = [
        ("MT_WLC", "configs/example_oshb_wlc.toml"),
        ("LXX", "configs/example_ebible_grclxx.toml"),
        ("TR_NT", "configs/example_ebible_grctr.toml"),
        ("SBLGNT", "configs/example_sblgnt.toml"),
    ]
    terms = {row["term_id"]: row for row in read_terms()}
    summary_rows: list[dict[str, object]] = []
    example_rows: list[dict[str, object]] = []

    for corpus_label, config_path in corpora:
        corpus = load_corpus(config_path)
        hits_by_term = collect_needed_hits(corpus, terms)
        for left_id, right_id in RELATED_PAIRS:
            if left_id not in hits_by_term or right_id not in hits_by_term:
                continue
            left_hits = hits_by_term[left_id]
            right_hits = hits_by_term[right_id]
            examples = score_pair(corpus_label, corpus, terms, left_id, right_id, left_hits, right_hits)
            same_chapter = [example for example in examples if example.shared_chapters]
            overlaps = [example for example in examples if example.span_gap == 0]
            close = [example for example in examples if example.span_gap <= 500]
            examples.sort(key=lambda example: (example.span_gap, example.center_distance))

            best = examples[0] if examples else None
            summary_rows.append(
                {
                    "corpus": corpus_label,
                    "left_term_id": left_id,
                    "left_concept": terms[left_id]["concept"],
                    "left_term": terms[left_id]["term"],
                    "left_hits": len(left_hits),
                    "right_term_id": right_id,
                    "right_concept": terms[right_id]["concept"],
                    "right_term": terms[right_id]["term"],
                    "right_hits": len(right_hits),
                    "overlap_pairs": len(overlaps),
                    "same_chapter_pairs": len(same_chapter),
                    "within_500_pairs": len(close),
                    "best_span_gap": best.span_gap if best else "",
                    "best_center_distance": round(best.center_distance, 1) if best else "",
                    "best_shared_chapters": best.shared_chapters if best else "",
                    "best_refs": (
                        f"{best.left_start_ref}->{best.left_end_ref} / "
                        f"{best.right_start_ref}->{best.right_end_ref}"
                        if best
                        else ""
                    ),
                }
            )
            for example in examples[:10]:
                example_rows.append(example.__dict__)

    write_rows(SUMMARY_OUT, summary_rows)
    write_rows(EXAMPLES_OUT, example_rows)
    print(SUMMARY_OUT)
    print(EXAMPLES_OUT)
    return 0


def read_terms() -> list[dict[str, str]]:
    with TERMS_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def collect_needed_hits(corpus: Corpus, terms: dict[str, dict[str, str]]) -> dict[str, list[ELSHit]]:
    needed_ids = {term_id for pair in RELATED_PAIRS for term_id in pair}
    languages = accepted_term_languages(corpus.language)
    hits_by_term: dict[str, list[ELSHit]] = {}
    term_ids_by_query: dict[str, list[str]] = {}
    for term_id in sorted(needed_ids):
        row = terms.get(term_id)
        if row is None or row["language"] not in languages:
            continue
        hits_by_term[term_id] = []
        normalized = normalize_for_corpus(corpus, row["term"])
        if len(normalized) < 3:
            continue
        term_ids_by_query.setdefault(normalized, []).append(term_id)

    text_length = len(corpus.text)
    for skip in range(2, 51):
        lanes = make_lanes(corpus.text, skip)
        for normalized, term_ids in term_ids_by_query.items():
            for start, end in iter_forward_matches_in_lanes(
                lanes,
                normalized,
                skip,
                text_length=text_length,
            ):
                append_query_hits(
                    corpus,
                    terms,
                    hits_by_term,
                    term_ids,
                    normalized,
                    skip,
                    start,
                    end,
                )
            for low, high in iter_forward_matches_in_lanes(
                lanes,
                normalized[::-1],
                skip,
                text_length=text_length,
            ):
                append_query_hits(
                    corpus,
                    terms,
                    hits_by_term,
                    term_ids,
                    normalized,
                    -skip,
                    high,
                    low,
                )

    for hits in hits_by_term.values():
        hits.sort(key=find_els_order_key)
    return hits_by_term


def append_query_hits(
    corpus: Corpus,
    terms: dict[str, dict[str, str]],
    hits_by_term: dict[str, list[ELSHit]],
    term_ids: list[str],
    normalized: str,
    skip: int,
    start: int,
    end: int,
) -> None:
    for term_id in term_ids:
        row = terms[term_id]
        hits_by_term[term_id].append(
            build_hit(corpus, row["term"], normalized, skip, start, end)
        )


def score_pair(
    corpus_label: str,
    corpus: Corpus,
    terms: dict[str, dict[str, str]],
    left_id: str,
    right_id: str,
    left_hits: list[ELSHit],
    right_hits: list[ELSHit],
) -> list[PairExample]:
    examples: list[PairExample] = []
    if not left_hits or not right_hits:
        return examples

    right_sorted = sorted(right_hits, key=hit_center)
    right_centers = [hit_center(hit) for hit in right_sorted]
    for left_hit in left_hits:
        candidates = nearest_hits(left_hit, right_sorted, right_centers, radius=8)
        for right_hit in candidates:
            gap = span_gap(left_hit, right_hit)
            if gap > 500:
                continue
            shared = sorted(hit_chapters(corpus, left_hit) & hit_chapters(corpus, right_hit))
            examples.append(
                PairExample(
                    corpus=corpus_label,
                    left_term_id=left_id,
                    left_concept=terms[left_id]["concept"],
                    left_term=terms[left_id]["term"],
                    left_skip=left_hit.skip,
                    left_start_ref=left_hit.start_ref,
                    left_end_ref=left_hit.end_ref,
                    left_center_ref=left_hit.center_ref,
                    left_center_word_index=left_hit.center_word_index,
                    left_center_word=left_hit.center_word,
                    left_center_normalized_word=left_hit.center_normalized_word,
                    right_term_id=right_id,
                    right_concept=terms[right_id]["concept"],
                    right_term=terms[right_id]["term"],
                    right_skip=right_hit.skip,
                    right_start_ref=right_hit.start_ref,
                    right_end_ref=right_hit.end_ref,
                    right_center_ref=right_hit.center_ref,
                    right_center_word_index=right_hit.center_word_index,
                    right_center_word=right_hit.center_word,
                    right_center_normalized_word=right_hit.center_normalized_word,
                    span_gap=gap,
                    center_distance=abs(hit_center(left_hit) - hit_center(right_hit)),
                    shared_chapters=";".join(shared),
                )
            )
    return dedupe_examples(examples)


def nearest_hits(
    hit: ELSHit,
    sorted_hits: list[ELSHit],
    centers: list[float],
    *,
    radius: int,
) -> list[ELSHit]:
    center = hit_center(hit)
    insertion_index = bisect_left(centers, center)
    if insertion_index == 0:
        best_index = 0
    elif insertion_index == len(centers):
        best_index = len(centers) - 1
    else:
        before = insertion_index - 1
        after = insertion_index
        best_index = (
            before
            if center - centers[before] <= centers[after] - center
            else after
        )
    best_index = bisect_left(centers, centers[best_index])
    start = max(0, best_index - radius)
    end = min(len(sorted_hits), best_index + radius + 1)
    return sorted_hits[start:end]


def find_els_order_key(hit: ELSHit) -> tuple[int, int, int]:
    direction_order = 0 if hit.skip > 0 else 1
    low = min(hit.start_offset, hit.end_offset)
    return abs(hit.skip), direction_order, low


def dedupe_examples(examples: list[PairExample]) -> list[PairExample]:
    seen = set()
    unique = []
    for example in examples:
        key = (
            example.left_term_id,
            example.left_start_ref,
            example.left_end_ref,
            example.left_skip,
            example.right_term_id,
            example.right_start_ref,
            example.right_end_ref,
            example.right_skip,
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(example)
    return unique


def hit_center(hit: ELSHit) -> float:
    return (hit.start_offset + hit.end_offset) / 2


def span_gap(left: ELSHit, right: ELSHit) -> int:
    left_low, left_high = sorted((left.start_offset, left.end_offset))
    right_low, right_high = sorted((right.start_offset, right.end_offset))
    if left_low <= right_high and right_low <= left_high:
        return 0
    if left_high < right_low:
        return right_low - left_high
    return left_low - right_high


def hit_chapters(corpus: Corpus, hit: ELSHit) -> set[str]:
    low, high = sorted((hit.start_offset, hit.end_offset))
    chapter_refs = set()
    previous_verse_index = None
    for position in range(low, high + 1):
        verse_index = corpus.position_to_verse[position]
        if verse_index == previous_verse_index:
            continue
        previous_verse_index = verse_index
        verse = corpus.verses[verse_index]
        if verse.book and verse.chapter:
            chapter_refs.add(f"{verse.book} {verse.chapter}")
    return chapter_refs


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
