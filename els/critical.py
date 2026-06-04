"""Critical-text omission helpers."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable

from .corpus import Corpus, VerseSpan
from .normalization import normalize_text
from .search import ELSHit, build_hit, iter_els_query_matches_by_lanes, normalize_for_corpus
from .books import BOOK_TO_SBL


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
    deleted_blocks_override: list[OmittedBlock | BlockPlacement] | None = None,
) -> list[OmittedBlock | BlockPlacement]:
    """Return blocks to treat as deletions for omission-break analysis."""
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
        if not explicit_deletion:
            merge_status = adjacent_merge_status(normalized, verse, critical_book, critical_verses)
            if merge_status is not None:
                status = merge_status
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
    matches: Iterable[tuple[str, int, int, int]] | None = None,
    update_stats: bool = True,
    collect_broken_hits: bool = True,
) -> tuple[int, list[int], list[BrokenHit]]:
    """Count hits broken by deleting verse-aligned blocks from a corpus."""
    deleted_blocks = [block for block in blocks if block.used_as_deletion]
    per_block_breaks = [0 for _block in deleted_blocks]
    block_index = {block.ref: index for index, block in enumerate(deleted_blocks)}
    total_breaks = 0
    broken_hits: list[BrokenHit] = []

    match_iter = matches
    if match_iter is None:
        match_iter = iter_els_query_matches_by_lanes(
            corpus.text,
            stats_by_query,
            min_skip=min_skip,
            max_skip=max_skip,
            direction=direction,
        )

    for normalized, skip, start, end in match_iter:
        stats_for_query = stats_by_query[normalized]
        if update_stats:
            for stats in stats_for_query:
                stats.total_hits += 1
        span_blocks = blocks_in_offsets(start, end, deleted_blocks)
        if not span_blocks:
            continue

        sequence_positions = [start + index * skip for index in range(len(normalized))]
        removed_blocks = blocks_with_sequence_letters(sequence_positions, span_blocks)
        if removed_blocks:
            for stats in stats_for_query:
                if update_stats:
                    stats.span_intersect_hits += 1
                    stats.broken_removed_letter_hits += 1
                total_breaks += 1
                for block in removed_blocks:
                    per_block_breaks[block_index[block.ref]] += 1
                if collect_broken_hits:
                    hit = build_hit(corpus, stats.term_row["term"], normalized, skip, start, end)
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
        if keeps_same_skip(mapped_positions, skip):
            if update_stats:
                for stats in stats_for_query:
                    stats.span_intersect_hits += 1
                    stats.preserved_across_omission_hits += 1
            continue

        for stats in stats_for_query:
            if update_stats:
                stats.span_intersect_hits += 1
                stats.broken_spacing_hits += 1
            total_breaks += 1
            for block in span_blocks:
                per_block_breaks[block_index[block.ref]] += 1
            if collect_broken_hits:
                hit = build_hit(corpus, stats.term_row["term"], normalized, skip, start, end)
                broken_hits.append(
                    BrokenHit(
                        term_row=stats.term_row,
                        hit=hit,
                        break_type="broken_spacing",
                        span_blocks=tuple(span_blocks),
                        removed_blocks=(),
                    )
                )

    return total_breaks, per_block_breaks, broken_hits


def count_insertion_breaks_for_blocks(
    base: Corpus,
    augmented: Corpus,
    stats_by_query: dict[str, list[TermBreakStats]],
    blocks: list[OmittedBlock | BlockPlacement],
    *,
    min_skip: int,
    max_skip: int,
    direction: str = "both",
) -> tuple[int, list[int], list[BrokenHit]]:
    """Count base-corpus hits whose spacing breaks when blocks are inserted."""
    inserted_blocks = [block for block in blocks if block.used_as_deletion]
    per_block_breaks = [0 for _block in inserted_blocks]
    block_index = {block.ref: index for index, block in enumerate(inserted_blocks)}
    augmented_by_ref = {verse.ref: verse for verse in augmented.verses}
    total_breaks = 0
    broken_hits: list[BrokenHit] = []

    def augmented_position(position: int) -> int | None:
        verse = base.verses[base.position_to_verse[position]]
        augmented_verse = augmented_by_ref.get(verse.ref)
        if augmented_verse is None:
            return None
        return augmented_verse.norm_start + (position - verse.norm_start)

    for normalized, skip, start, end in iter_els_query_matches_by_lanes(
        base.text,
        stats_by_query,
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
    ):
        stats_for_query = stats_by_query[normalized]
        for stats in stats_for_query:
            stats.total_hits += 1

        base_positions = [start + index * skip for index in range(len(normalized))]
        mapped_positions = [augmented_position(position) for position in base_positions]
        if any(position is None for position in mapped_positions):
            continue
        augmented_positions = [int(position) for position in mapped_positions]
        span_blocks = blocks_in_offsets(min(augmented_positions), max(augmented_positions), inserted_blocks)
        if not span_blocks:
            continue

        if keeps_same_skip(augmented_positions, skip):
            for stats in stats_for_query:
                stats.span_intersect_hits += 1
                stats.preserved_across_omission_hits += 1
            continue

        for stats in stats_for_query:
            stats.span_intersect_hits += 1
            stats.broken_spacing_hits += 1
            total_breaks += 1
            for block in span_blocks:
                per_block_breaks[block_index[block.ref]] += 1
            hit = build_hit(base, stats.term_row["term"], normalized, skip, start, end)
            broken_hits.append(
                BrokenHit(
                    term_row=stats.term_row,
                    hit=hit,
                    break_type="broken_spacing",
                    span_blocks=tuple(span_blocks),
                    removed_blocks=(),
                )
            )

    return total_breaks, per_block_breaks, broken_hits


def shuffled_block_placement(
    corpus: Corpus,
    actual_blocks: list[OmittedBlock],
    *,
    exclude_refs: set[str] | None = None,
    seed: int,
) -> list[BlockPlacement]:
    rng = random.Random(seed)
    excluded = set({block.ref for block in actual_blocks} if exclude_refs is None else exclude_refs)
    eligible = [index for index, verse in enumerate(corpus.verses) if verse.ref not in excluded]
    if not eligible and actual_blocks:
        raise RuntimeError("could not place shuffle blocks: no eligible verses")
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
    return adjacent_merge_status(normalized, verse, critical_book, critical_verses) is not None


def adjacent_merge_status(
    normalized: str,
    verse: VerseSpan,
    critical_book: str,
    critical_verses: list[VerseSpan],
) -> str | None:
    if not normalized:
        return None
    try:
        tr_verse_num = int(verse.verse)
    except ValueError:
        return None
    variants = adjacent_merge_variants(normalized)
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
        for candidate, status in variants:
            if adjacent_text_matches(candidate, critical_normalized):
                return status
    return None


def adjacent_merge_variants(normalized: str) -> list[tuple[str, str]]:
    variants = [(normalized, "adjacent_merge")]
    if normalized.endswith("αμην"):
        variants.append((normalized[:-4], "renumbered_minus_amen"))
    without_subscription = strip_trailing_greek_subscription(normalized)
    if without_subscription != normalized:
        variants.append((without_subscription, "renumbered_minus_amen_subscription"))
        if without_subscription.endswith("αμην"):
            variants.append((without_subscription[:-4], "renumbered_minus_amen_subscription"))
    return [(candidate, status) for candidate, status in variants if candidate]


def strip_trailing_greek_subscription(normalized: str) -> str:
    marker = "αμηνπροσ"
    index = normalized.find(marker, len(normalized) // 2)
    if index == -1:
        return normalized
    return normalized[:index]


def adjacent_text_matches(needle: str, haystack: str) -> bool:
    if needle in haystack:
        return True
    if len(needle) < 20:
        return False
    return near_substring_one_edit(needle, haystack)


def near_substring_one_edit(needle: str, haystack: str) -> bool:
    for size in range(max(1, len(needle) - 1), len(needle) + 2):
        if size > len(haystack):
            continue
        for start in range(0, len(haystack) - size + 1):
            candidate = haystack[start : start + size]
            if within_one_edit(needle, candidate) and (
                common_prefix_len(needle, candidate) >= 8 or common_suffix_len(needle, candidate) >= 8
            ):
                return True
    return False


def within_one_edit(left: str, right: str) -> bool:
    if abs(len(left) - len(right)) > 1:
        return False
    if len(left) == len(right):
        return sum(1 for a, b in zip(left, right) if a != b) <= 1
    if len(left) > len(right):
        left, right = right, left
    i = j = edits = 0
    while i < len(left) and j < len(right):
        if left[i] == right[j]:
            i += 1
            j += 1
            continue
        edits += 1
        if edits > 1:
            return False
        j += 1
    return True


def common_prefix_len(left: str, right: str) -> int:
    count = 0
    for a, b in zip(left, right):
        if a != b:
            break
        count += 1
    return count


def common_suffix_len(left: str, right: str) -> int:
    count = 0
    for a, b in zip(reversed(left), reversed(right)):
        if a != b:
            break
        count += 1
    return count


def verse_span_preserved(
    other: Corpus,
    other_ref_to_index: dict[str, int],
    start_ref: str,
    end_ref: str,
    query: str,
    skip: int,
    *,
    window_verses: int = 2,
) -> bool:
    """True if ``query`` occurs at ``skip`` within +/-``window_verses`` of the
    ``[start_ref, end_ref]`` verse span in ``other``.

    The strict equivalent-offset test (see the cross-tradition analysis) maps a
    TR hit's letter offsets verse-locally into ``other`` and requires an exact
    match. That fails whenever upstream word-length deltas (movable nu, article
    presence, verb-ending variants) shift every offset, even when the same ELS
    is physically present. This proximity test decouples preservation from
    exact per-letter offset equivalence by scanning a small verse window.

    Both refs must resolve in ``other``; the versification case (a ref present
    under a shifted number) is a separate Stage-2 concern. Returns False on a
    missing ref, empty query, or zero skip.

    Invariant: any hit the strict test classes ``preserved_equivalent_offsets``
    is also preserved here -- the strict match position lies inside the span,
    hence inside the window. The window only ever adds matches.
    """
    if not query or skip == 0:
        return False
    if start_ref not in other_ref_to_index or end_ref not in other_ref_to_index:
        return False
    i_start = other_ref_to_index[start_ref]
    i_end = other_ref_to_index[end_ref]
    last = len(other.verses) - 1
    lo_idx = max(0, min(i_start, i_end) - window_verses)
    hi_idx = min(last, max(i_start, i_end) + window_verses)
    lo = other.verses[lo_idx].norm_start
    hi = other.verses[hi_idx].norm_end
    text = other.text
    text_len = len(text)
    length = len(query)
    for anchor in range(lo, hi + 1):
        positions = [anchor + index * skip for index in range(length)]
        if any(pos < lo or pos > hi or pos < 0 or pos >= text_len for pos in positions):
            continue
        if all(text[pos] == query[index] for index, pos in enumerate(positions)):
            return True
    return False


def ref_absence_kind(
    ref: str,
    present_refs,
    present_book_chapters: set[tuple[str, str]],
) -> str:
    """Classify why ``ref`` is absent from a comparison corpus.

    Returns one of:

    - ``present`` -- the ref is in the corpus.
    - ``omitted_verse`` -- the ref's book+chapter exist in the corpus but the
      verse number does not. The tradition skips this verse number (e.g. Acts 8
      running ...36, 38, ...), which is a *shared omission*, not a versification
      renumbering. A TR ELS hit whose endpoint is such a verse genuinely cannot
      be reconstructed in the corpus; the omitted letters are not there.
    - ``chapter_absent`` -- the book+chapter is not in the corpus at all.
    - ``unparseable`` -- the ref is not of the form ``Book C:V``.

    ``present_book_chapters`` is a set of ``(book, chapter)`` pairs the corpus
    contains, where ``book`` matches the leading token(s) of the ref.
    """
    if ref in present_refs:
        return "present"
    if " " not in ref:
        return "unparseable"
    head, tail = ref.rsplit(" ", 1)
    if ":" not in tail:
        return "unparseable"
    chapter, verse = tail.split(":", 1)
    if not chapter.isdigit() or not verse.isdigit():
        return "unparseable"
    if (head, chapter) in present_book_chapters:
        return "omitted_verse"
    return "chapter_absent"
