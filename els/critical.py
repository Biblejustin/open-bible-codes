"""Critical-text omission helpers."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable

from .corpus import Corpus, VerseSpan
from .normalization import normalize_text
from .search import ELSHit, build_hit, iter_els_query_matches_by_lanes, normalize_for_corpus


BOOK_TO_SBL = {
    "MAT": "Matt",
    "MRK": "Mark",
    "LUK": "Luke",
    "JHN": "John",
    "ACT": "Acts",
    "ROM": "Rom",
    "1CO": "1Cor",
    "2CO": "2Cor",
    "GAL": "Gal",
    "EPH": "Eph",
    "PHP": "Phil",
    "COL": "Col",
    "1TH": "1Thess",
    "2TH": "2Thess",
    "1TI": "1Tim",
    "2TI": "2Tim",
    "TIT": "Titus",
    "PHM": "Phlm",
    "HEB": "Heb",
    "JAS": "Jas",
    "1PE": "1Pet",
    "2PE": "2Pet",
    "1JN": "1John",
    "2JN": "2John",
    "3JN": "3John",
    "JUD": "Jude",
    "REV": "Rev",
    "Matthew": "Matt",
    "Mark": "Mark",
    "Luke": "Luke",
    "John": "John",
    "Acts": "Acts",
    "Romans": "Rom",
    "1 Corinthians": "1Cor",
    "2 Corinthians": "2Cor",
    "Galatians": "Gal",
    "Ephesians": "Eph",
    "Philippians": "Phil",
    "Colossians": "Col",
    "1 Thessalonians": "1Thess",
    "2 Thessalonians": "2Thess",
    "1 Timothy": "1Tim",
    "2 Timothy": "2Tim",
    "Titus": "Titus",
    "Philemon": "Phlm",
    "Hebrews": "Heb",
    "James": "Jas",
    "1 Peter": "1Pet",
    "2 Peter": "2Pet",
    "1 John": "1John",
    "2 John": "2John",
    "3 John": "3John",
    "Jude": "Jude",
    "Revelation": "Rev",
}


@dataclass(frozen=True)
class OmittedBlock:
    ref: str
    start: int
    end: int
    length: int
    status: str
    used_as_deletion: bool


@dataclass(frozen=True)
class BlockPlacement:
    """A contiguous run of verses treated as a deletion block."""

    ref: str
    start: int
    end: int
    length: int
    verse_count: int
    used_as_deletion: bool = True


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


@dataclass(frozen=True)
class BrokenHit:
    term_row: dict[str, str]
    hit: ELSHit
    break_type: str
    span_blocks: tuple[OmittedBlock | BlockPlacement, ...]
    removed_blocks: tuple[OmittedBlock | BlockPlacement, ...]

    def as_row(self) -> dict[str, object]:
        return {
            "term_source": self.term_row.get("term_source", ""),
            "term_id": self.term_row.get("term_id", ""),
            "concept": self.term_row.get("concept", ""),
            "category": self.term_row.get("category", ""),
            "term": self.term_row.get("term", ""),
            "normalized_term": self.hit.normalized_term,
            "skip": self.hit.skip,
            "direction": self.hit.direction,
            "start_offset": self.hit.start_offset,
            "end_offset": self.hit.end_offset,
            "span_letters": self.hit.span_letters,
            "start_ref": self.hit.start_ref,
            "end_ref": self.hit.end_ref,
            "center_ref": self.hit.center_ref,
            "center_word_index": self.hit.center_word_index,
            "center_word": self.hit.center_word,
            "center_normalized_word": self.hit.center_normalized_word,
            "break_type": self.break_type,
            "omitted_refs_in_span": ";".join(block.ref for block in self.span_blocks),
            "omitted_refs_with_sequence_letters": ";".join(block.ref for block in self.removed_blocks),
        }


def classify_missing_verses(
    tr: Corpus,
    critical: Corpus,
    *,
    extra_deleted_refs: set[str] | None = None,
    deleted_blocks_override: list[OmittedBlock] | None = None,
) -> list[OmittedBlock]:
    if deleted_blocks_override is not None:
        return deleted_blocks_override
    critical_refs = {(verse.book, verse.chapter, verse.verse) for verse in critical.verses}
    critical_verses = list(critical.verses)
    extra_refs = extra_deleted_refs or set()
    blocks: list[OmittedBlock] = []
    for verse in tr.verses:
        critical_book = BOOK_TO_SBL.get(verse.book, verse.book)
        explicit_deletion = verse.ref in extra_refs
        if not explicit_deletion and (critical_book, verse.chapter, verse.verse) in critical_refs:
            continue
        normalized = normalize_for_corpus(tr, verse.raw_text)
        status = "explicit_deleted_ref" if explicit_deletion else "deleted_block"
        used_as_deletion = True
        if not explicit_deletion and is_adjacent_merge(normalized, verse, critical_book, critical_verses):
            status = "adjacent_merge"
            used_as_deletion = False
        elif not explicit_deletion and normalized.endswith("αμην") and is_adjacent_merge(
            normalized[:-4],
            verse,
            critical_book,
            critical_verses,
        ):
            status = "renumbered_minus_amen"
            used_as_deletion = False
        blocks.append(
            OmittedBlock(
                ref=verse.ref,
                start=verse.norm_start,
                end=verse.norm_end,
                length=verse.norm_length,
                status=status,
                used_as_deletion=used_as_deletion,
            )
        )
    return blocks


def count_breaks_for_blocks(
    corpus: Corpus,
    stats_by_query: dict[str, list[TermBreakStats]],
    blocks: list[OmittedBlock | BlockPlacement],
    *,
    min_skip: int,
    max_skip: int,
    direction: str = "both",
) -> tuple[int, list[int], list[BrokenHit]]:
    deleted_blocks = [block for block in blocks if block.used_as_deletion]
    per_block_breaks = [0 for _block in deleted_blocks]
    block_index = {block.ref: index for index, block in enumerate(deleted_blocks)}
    broken_hits: list[BrokenHit] = []

    for normalized, skip, start, end in iter_els_query_matches_by_lanes(
        corpus.text,
        stats_by_query,
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
    ):
        for stats in stats_by_query[normalized]:
            stats.total_hits += 1
            span_blocks = blocks_in_offsets(start, end, deleted_blocks)
            if not span_blocks:
                continue

            hit = build_hit(corpus, stats.term_row["term"], normalized, skip, start, end)
            stats.span_intersect_hits += 1
            sequence_positions = hit_sequence_positions(hit)
            removed_blocks = blocks_with_sequence_letters(sequence_positions, span_blocks)
            if removed_blocks:
                stats.broken_removed_letter_hits += 1
                for block in removed_blocks:
                    per_block_breaks[block_index[block.ref]] += 1
                broken_hits.append(
                    BrokenHit(
                        term_row=stats.term_row,
                        hit=hit,
                        break_type="broken_removed_letter",
                        span_blocks=tuple(span_blocks),
                        removed_blocks=tuple(removed_blocks),
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
                per_block_breaks[block_index[block.ref]] += 1
            broken_hits.append(
                BrokenHit(
                    term_row=stats.term_row,
                    hit=hit,
                    break_type="broken_spacing",
                    span_blocks=tuple(span_blocks),
                    removed_blocks=(),
                )
            )

    return len(broken_hits), per_block_breaks, broken_hits


def shuffled_block_placement(
    corpus: Corpus,
    actual_blocks: list[OmittedBlock],
    *,
    exclude_refs: set[str] | None = None,
    seed: int,
) -> list[BlockPlacement]:
    rng = random.Random(seed)
    excluded = set(exclude_refs or {block.ref for block in actual_blocks})
    eligible = [index for index, verse in enumerate(corpus.verses) if verse.ref not in excluded]
    block_verse_counts = [_actual_block_verse_count(block, corpus) for block in actual_blocks]

    placements: list[BlockPlacement] = []
    used: set[int] = set()
    for index, verse_count in enumerate(block_verse_counts):
        for _attempt in range(1000):
            start = rng.choice(eligible)
            run = range(start, start + verse_count)
            if any(j in used or j >= len(corpus.verses) for j in run):
                continue
            if any(corpus.verses[j].ref in excluded for j in run):
                continue
            used.update(run)
            first = corpus.verses[run[0]]
            last = corpus.verses[run[-1]]
            placements.append(
                BlockPlacement(
                    ref=f"shuffle-block-{index}",
                    start=first.norm_start,
                    end=last.norm_end,
                    length=sum(corpus.verses[j].norm_length for j in run),
                    verse_count=verse_count,
                )
            )
            break
        else:
            raise RuntimeError(f"could not place shuffle block {index} after 1000 attempts")
    return placements


def _actual_block_verse_count(block: OmittedBlock, corpus: Corpus) -> int:
    return sum(1 for verse in corpus.verses if block.start <= verse.norm_start and verse.norm_end <= block.end) or 1


def hit_sequence_positions(hit: ELSHit) -> list[int]:
    return [hit.start_offset + index * hit.skip for index in range(len(hit.normalized_term))]


def blocks_in_offsets(
    start: int,
    end: int,
    blocks: Iterable[OmittedBlock | BlockPlacement],
) -> list[OmittedBlock | BlockPlacement]:
    low, high = sorted((start, end))
    return [block for block in blocks if block.start <= high and block.end >= low]


def blocks_with_sequence_letters(
    sequence_positions: list[int],
    blocks: Iterable[OmittedBlock | BlockPlacement],
) -> list[OmittedBlock | BlockPlacement]:
    return [
        block
        for block in blocks
        if any(block.start <= position <= block.end for position in sequence_positions)
    ]


def map_old_to_deleted_text(position: int, blocks: Iterable[OmittedBlock | BlockPlacement]) -> int:
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


def is_adjacent_merge(
    normalized: str,
    verse: VerseSpan,
    critical_book: str,
    critical_verses: list[VerseSpan],
) -> bool:
    if not normalized:
        return False
    try:
        tr_verse_num = int(verse.verse)
    except ValueError:
        return False
    for critical_verse in critical_verses:
        if critical_verse.book != critical_book or critical_verse.chapter != verse.chapter:
            continue
        try:
            critical_verse_num = int(critical_verse.verse)
        except ValueError:
            continue
        if abs(critical_verse_num - tr_verse_num) > 1:
            continue
        critical_normalized = normalize_text(critical_verse.raw_text, "greek")
        if normalized in critical_normalized:
            return True
    return False
