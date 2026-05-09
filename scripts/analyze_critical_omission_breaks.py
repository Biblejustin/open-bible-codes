#!/usr/bin/env python3
"""Find TR ELS hits broken by verse blocks absent from a critical text."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els.cli import accepted_term_languages
from els.corpus import Corpus, load_corpus
from els.critical import OmittedBlock, classify_missing_verses
from els.search import (
    ELSHit,
    build_hit,
    iter_els_query_matches_by_lanes,
    normalize_for_corpus,
)


TR_CONFIG = Path("configs/example_ebible_grctr.toml")
CRITICAL_CONFIG = Path("configs/example_sblgnt.toml")
TERM_PATHS = [
    Path("terms/theological_terms.csv"),
    Path("terms/modern_names_dates.csv"),
    Path("terms/table_of_nations.csv"),
    Path("terms/prophetic_terms.csv"),
]
SUMMARY_OUT = Path("reports/critical_omission_breaks_summary.csv")
EXAMPLES_OUT = Path("reports/critical_omission_breaks_examples.csv")
VERSES_OUT = Path("reports/critical_omission_breaks_by_verse.csv")
MISSING_VERSES_OUT = Path("reports/critical_omission_missing_verses.csv")
MANIFEST_OUT = Path("reports/critical_omission_breaks.manifest.json")

MIN_SKIP = 2
MAX_SKIP = 50
MIN_TERM_LENGTH = 3


@dataclass
class TermBreakStats:
    order: int
    term_row: dict[str, str]
    normalized: str
    total_hits: int = 0
    span_intersect_hits: int = 0
    broken_removed_letter_hits: int = 0
    broken_spacing_hits: int = 0
    preserved_across_omission_hits: int = 0
    status: str = "counted"


def main() -> int:
    tr = load_corpus(TR_CONFIG)
    critical = load_corpus(CRITICAL_CONFIG)
    omitted_blocks = classify_missing_verses(tr, critical)
    deleted_blocks = [block for block in omitted_blocks if block.used_as_deletion]
    terms = read_greek_terms(TERM_PATHS, tr)

    write_rows(MISSING_VERSES_OUT, [block.__dict__ for block in omitted_blocks])

    summary_rows: list[dict[str, object]] = []
    example_entries: list[tuple[tuple[int, int, int, int, int], dict[str, object]]] = []
    by_verse = {
        block.ref: {
            "omitted_ref": block.ref,
            "norm_start": block.start,
            "norm_end": block.end,
            "norm_length": block.length,
            "span_intersect_hits": 0,
            "broken_removed_letter_hits": 0,
            "broken_spacing_hits": 0,
            "broken_total_hits": 0,
        }
        for block in deleted_blocks
    }

    term_stats: list[TermBreakStats] = []
    stats_by_query: dict[str, list[TermBreakStats]] = {}
    for term_row in terms:
        term = term_row["term"]
        normalized = normalize_for_corpus(tr, term)
        if len(normalized) < MIN_TERM_LENGTH:
            term_stats.append(
                TermBreakStats(
                    order=len(term_stats),
                    term_row=term_row,
                    normalized=normalized,
                    status="skipped_short_term",
                )
            )
            continue

        stats = TermBreakStats(
            order=len(term_stats),
            term_row=term_row,
            normalized=normalized,
        )
        term_stats.append(stats)
        stats_by_query.setdefault(normalized, []).append(stats)

    for normalized, skip, start, end in iter_els_query_matches_by_lanes(
        tr.text,
        stats_by_query,
        min_skip=MIN_SKIP,
        max_skip=MAX_SKIP,
        direction="both",
    ):
        for stats in stats_by_query[normalized]:
            stats.total_hits += 1
            span_blocks = blocks_in_offsets(start, end, deleted_blocks)
            if not span_blocks:
                continue

            hit = build_hit(tr, stats.term_row["term"], normalized, skip, start, end)
            stats.span_intersect_hits += 1
            for block in span_blocks:
                by_verse[block.ref]["span_intersect_hits"] += 1

            sequence_positions = hit_sequence_positions(hit)
            removed_blocks = blocks_with_sequence_letters(sequence_positions, span_blocks)
            if removed_blocks:
                stats.broken_removed_letter_hits += 1
                for block in removed_blocks:
                    by_verse[block.ref]["broken_removed_letter_hits"] += 1
                    by_verse[block.ref]["broken_total_hits"] += 1
                example_entries.append(
                    (
                        example_sort_key(stats, hit),
                        example_row(
                            stats.term_row,
                            hit,
                            "broken_removed_letter",
                            span_blocks,
                            removed_blocks,
                        ),
                    )
                )
                continue

            mapped_positions = [
                map_old_to_deleted_text(position, deleted_blocks)
                for position in sequence_positions
            ]
            if keeps_same_skip(mapped_positions, hit.skip):
                stats.preserved_across_omission_hits += 1
                continue

            stats.broken_spacing_hits += 1
            for block in span_blocks:
                by_verse[block.ref]["broken_spacing_hits"] += 1
                by_verse[block.ref]["broken_total_hits"] += 1
            example_entries.append(
                (
                    example_sort_key(stats, hit),
                    example_row(stats.term_row, hit, "broken_spacing", span_blocks, []),
                )
            )

    for stats in term_stats:
        summary_rows.append(
            summary_row(
                stats.term_row,
                stats.normalized,
                stats.total_hits,
                stats.span_intersect_hits,
                stats.broken_removed_letter_hits,
                stats.broken_spacing_hits,
                stats.preserved_across_omission_hits,
                stats.status,
            )
        )

    example_rows = [row for _key, row in sorted(example_entries, key=lambda entry: entry[0])]
    write_rows(SUMMARY_OUT, summary_rows)
    write_rows(EXAMPLES_OUT, example_rows)
    write_rows(VERSES_OUT, list(by_verse.values()))
    write_manifest(tr, critical, omitted_blocks, terms, len(example_rows))

    print(SUMMARY_OUT)
    print(EXAMPLES_OUT)
    print(VERSES_OUT)
    print(MISSING_VERSES_OUT)
    print(MANIFEST_OUT)
    return 0


def read_greek_terms(paths: list[Path], corpus: Corpus) -> list[dict[str, str]]:
    languages = accepted_term_languages(corpus.language)
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("language") not in languages:
                    continue
                key = (str(path), row.get("term_id", ""))
                if key in seen:
                    continue
                seen.add(key)
                row = dict(row)
                row["term_source"] = str(path)
                rows.append(row)
    return rows


def hit_sequence_positions(hit: ELSHit) -> list[int]:
    return [hit.start_offset + index * hit.skip for index in range(len(hit.normalized_term))]


def blocks_in_hit_span(hit: ELSHit, blocks: list[OmittedBlock]) -> list[OmittedBlock]:
    return blocks_in_offsets(hit.start_offset, hit.end_offset, blocks)


def blocks_in_offsets(start: int, end: int, blocks: list[OmittedBlock]) -> list[OmittedBlock]:
    low, high = sorted((start, end))
    return [block for block in blocks if block.start <= high and block.end >= low]


def example_sort_key(stats: TermBreakStats, hit: ELSHit) -> tuple[int, int, int, int, int]:
    direction_order = 0 if hit.skip > 0 else 1
    low, high = sorted((hit.start_offset, hit.end_offset))
    return stats.order, abs(hit.skip), direction_order, low, high


def blocks_with_sequence_letters(
    sequence_positions: list[int],
    blocks: list[OmittedBlock],
) -> list[OmittedBlock]:
    found = []
    for block in blocks:
        if any(block.start <= position <= block.end for position in sequence_positions):
            found.append(block)
    return found


def map_old_to_deleted_text(position: int, blocks: list[OmittedBlock]) -> int:
    deleted_before = 0
    for block in blocks:
        if block.end < position:
            deleted_before += block.length
    return position - deleted_before


def keeps_same_skip(mapped_positions: list[int], skip: int) -> bool:
    return all(
        mapped_positions[index] - mapped_positions[index - 1] == skip
        for index in range(1, len(mapped_positions))
    )


def summary_row(
    term_row: dict[str, str],
    normalized: str,
    total_hits: int,
    span_intersect_hits: int,
    broken_removed_letter_hits: int,
    broken_spacing_hits: int,
    preserved_across_omission_hits: int,
    status: str,
) -> dict[str, object]:
    return {
        "term_source": term_row.get("term_source", ""),
        "term_id": term_row.get("term_id", ""),
        "concept": term_row.get("concept", ""),
        "category": term_row.get("category", ""),
        "term": term_row.get("term", ""),
        "normalized_term": normalized,
        "normalized_length": len(normalized),
        "tr_hits": total_hits,
        "span_intersect_hits": span_intersect_hits,
        "broken_removed_letter_hits": broken_removed_letter_hits,
        "broken_spacing_hits": broken_spacing_hits,
        "broken_total_hits": broken_removed_letter_hits + broken_spacing_hits,
        "preserved_across_omission_hits": preserved_across_omission_hits,
        "status": status,
    }


def example_row(
    term_row: dict[str, str],
    hit: ELSHit,
    break_type: str,
    span_blocks: list[OmittedBlock],
    removed_blocks: list[OmittedBlock],
) -> dict[str, object]:
    return {
        "term_source": term_row.get("term_source", ""),
        "term_id": term_row.get("term_id", ""),
        "concept": term_row.get("concept", ""),
        "category": term_row.get("category", ""),
        "term": term_row.get("term", ""),
        "normalized_term": hit.normalized_term,
        "skip": hit.skip,
        "direction": hit.direction,
        "start_offset": hit.start_offset,
        "end_offset": hit.end_offset,
        "span_letters": hit.span_letters,
        "start_ref": hit.start_ref,
        "end_ref": hit.end_ref,
        "center_ref": hit.center_ref,
        "center_word_index": hit.center_word_index,
        "center_word": hit.center_word,
        "center_normalized_word": hit.center_normalized_word,
        "break_type": break_type,
        "omitted_refs_in_span": ";".join(block.ref for block in span_blocks),
        "omitted_refs_with_sequence_letters": ";".join(block.ref for block in removed_blocks),
    }


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    tr: Corpus,
    critical: Corpus,
    blocks: list[OmittedBlock],
    terms: list[dict[str, str]],
    examples: int,
) -> None:
    used_blocks = [block for block in blocks if block.used_as_deletion]
    MANIFEST_OUT.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_OUT.write_text(
        json.dumps(
            {
                "tool": "critical_omission_breaks",
                "created_utc": datetime.now(UTC).isoformat(),
                "tr_config": str(TR_CONFIG.resolve()),
                "critical_config": str(CRITICAL_CONFIG.resolve()),
                "tr_corpus": tr.summary(),
                "critical_corpus": critical.summary(),
                "term_paths": [str(path.resolve()) for path in TERM_PATHS],
                "term_rows": len(terms),
                "min_skip": MIN_SKIP,
                "max_skip": MAX_SKIP,
                "min_term_length": MIN_TERM_LENGTH,
                "ref_missing_verses": len(blocks),
                "deleted_blocks_used": len(used_blocks),
                "deleted_letters_used": sum(block.length for block in used_blocks),
                "broken_example_rows": examples,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
