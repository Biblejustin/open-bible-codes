"""Surface-text context checks for ELS hits."""

from __future__ import annotations

from dataclasses import dataclass

from .corpus import Corpus
from .normalization import normalize_text
from .search import AhoAutomaton, ELSHit


@dataclass(frozen=True)
class SurfaceTerm:
    term_source: str
    term_id: str
    concept: str
    category: str
    term: str
    normalized_term: str


@dataclass(frozen=True)
class SurfaceContext:
    best_context: str
    center_word_exact: bool
    center_word_same_concept: bool
    center_word_same_category: bool
    center_exact: bool
    center_same_concept: bool
    center_same_category: bool
    span_exact: bool
    span_same_concept: bool
    span_same_category: bool
    center_word_same_concept_terms: str
    center_word_same_category_terms: str
    center_same_concept_terms: str
    center_same_category_terms: str
    span_exact_refs: str
    span_same_concept_refs: str
    span_same_category_refs: str

    @property
    def has_context(self) -> bool:
        return self.best_context != ""


@dataclass
class SurfaceContextIndex:
    normalized_verses: tuple[str, ...]
    terms: tuple[SurfaceTerm, ...]
    term_index_by_term: dict[SurfaceTerm, int]
    verse_indexes_by_term: dict[SurfaceTerm, frozenset[int]]
    verse_indexes_by_index: tuple[frozenset[int], ...]
    same_concept_indexes_by_index: tuple[tuple[int, ...], ...]
    same_category_indexes_by_index: tuple[tuple[int, ...], ...]

    def verse_indexes(self, term: SurfaceTerm) -> frozenset[int]:
        return self.verse_indexes_by_term.get(term, frozenset())

    def term_index(self, term: SurfaceTerm) -> int:
        return self.term_index_by_term[term]

    def verse_indexes_at(self, index: int) -> frozenset[int]:
        return self.verse_indexes_by_index[index]

    def same_concept_indexes_at(self, index: int) -> tuple[int, ...]:
        return self.same_concept_indexes_by_index[index]

    def same_category_indexes_at(self, index: int) -> tuple[int, ...]:
        return self.same_category_indexes_by_index[index]


def normalize_verses(corpus: Corpus) -> tuple[str, ...]:
    return tuple(
        normalize_text(
            verse.raw_text,
            corpus.language,
            keep_hebrew_final_forms=corpus.keep_hebrew_final_forms,
        )
        for verse in corpus.verses
    )


def build_surface_context_index(
    corpus: Corpus,
    terms: list[SurfaceTerm],
    normalized_verses: tuple[str, ...] | None = None,
) -> SurfaceContextIndex:
    if normalized_verses is None:
        normalized_verses = normalize_verses(corpus)
    indexed_terms = tuple(terms)
    term_index_by_term = {
        term: index
        for index, term in enumerate(indexed_terms)
    }
    terms_by_pattern: dict[str, list[SurfaceTerm]] = {}
    mutable_indexes: list[set[int]] = [set() for _term in indexed_terms]
    for index, term in enumerate(indexed_terms):
        if term.normalized_term:
            terms_by_pattern.setdefault(term.normalized_term, []).append(term)

    if not terms_by_pattern:
        return make_surface_context_index(
            normalized_verses,
            indexed_terms,
            term_index_by_term,
            tuple(frozenset() for _term in indexed_terms),
        )

    automaton = AhoAutomaton()
    for pattern in terms_by_pattern:
        automaton.add(pattern, pattern)
    automaton.build()

    for index, normalized_verse in enumerate(normalized_verses):
        matched_patterns = automaton.find_outputs(normalized_verse)
        if not matched_patterns:
            continue
        for pattern in matched_patterns:
            for term in terms_by_pattern[pattern]:
                mutable_indexes[term_index_by_term[term]].add(index)

    return make_surface_context_index(
        normalized_verses,
        indexed_terms,
        term_index_by_term,
        tuple(frozenset(indexes) for indexes in mutable_indexes),
    )


def make_surface_context_index(
    normalized_verses: tuple[str, ...],
    terms: tuple[SurfaceTerm, ...],
    term_index_by_term: dict[SurfaceTerm, int],
    verse_indexes_by_index: tuple[frozenset[int], ...],
) -> SurfaceContextIndex:
    same_concept_indexes_by_index = tuple(
        tuple(
            related_index
            for related_index, related in enumerate(terms)
            if related.concept == term.concept
            and related.term_id != term.term_id
            and related.normalized_term
        )
        for term in terms
    )
    same_category_indexes_by_index = tuple(
        tuple(
            related_index
            for related_index, related in enumerate(terms)
            if related.category == term.category
            and related.concept != term.concept
            and related.normalized_term
        )
        for term in terms
    )
    return SurfaceContextIndex(
        normalized_verses=normalized_verses,
        terms=terms,
        term_index_by_term=term_index_by_term,
        verse_indexes_by_term={
            term: verse_indexes_by_index[index]
            for index, term in enumerate(terms)
        },
        verse_indexes_by_index=verse_indexes_by_index,
        same_concept_indexes_by_index=same_concept_indexes_by_index,
        same_category_indexes_by_index=same_category_indexes_by_index,
    )


def surface_context_for_hit(
    corpus: Corpus,
    hit: ELSHit,
    term: SurfaceTerm,
    related_terms: list[SurfaceTerm],
    normalized_verses: tuple[str, ...],
) -> SurfaceContext:
    """Convenience wrapper for one-off calls; reuse an index for repeated hits."""

    return surface_context_for_hit_indexed(
        corpus,
        hit,
        term,
        related_terms,
        build_surface_context_index(corpus, related_terms, normalized_verses),
    )


def surface_context_for_hit_indexed(
    corpus: Corpus,
    hit: ELSHit,
    term: SurfaceTerm,
    related_terms: list[SurfaceTerm],
    context_index: SurfaceContextIndex,
) -> SurfaceContext:
    center_index = corpus.position_to_verse[hit.center_offset]
    center_word = corpus.word_at(hit.center_offset)
    center_normalized_word = center_word.normalized_word if center_word is not None else ""
    span_indexes = verse_indexes_for_hit(corpus, hit)

    span_refs = [(index, corpus.verses[index].ref) for index in span_indexes]
    term_index = context_index.term_index(term)
    term_verse_indexes = context_index.verse_indexes_at(term_index)

    center_exact = center_index in term_verse_indexes
    center_word_exact = contains_surface_term(center_normalized_word, term.normalized_term)
    span_exact_matches = [
        ref for index, ref in span_refs if index in term_verse_indexes
    ]

    same_concept_indexes = context_index.same_concept_indexes_at(term_index)
    same_category_indexes = context_index.same_category_indexes_at(term_index)

    center_same_concept_matches = [
        context_index.terms[index]
        for index in same_concept_indexes
        if center_index in context_index.verse_indexes_at(index)
    ]
    center_word_same_concept_matches = [
        context_index.terms[index]
        for index in same_concept_indexes
        if contains_surface_term(center_normalized_word, context_index.terms[index].normalized_term)
    ]
    center_same_category_matches = [
        context_index.terms[index]
        for index in same_category_indexes
        if center_index in context_index.verse_indexes_at(index)
    ]
    center_word_same_category_matches = [
        context_index.terms[index]
        for index in same_category_indexes
        if contains_surface_term(center_normalized_word, context_index.terms[index].normalized_term)
    ]
    span_same_concept_matches = refs_for_indexed_term_index_matches(
        context_index,
        span_refs,
        same_concept_indexes,
    )
    span_same_category_matches = refs_for_indexed_term_index_matches(
        context_index,
        span_refs,
        same_category_indexes,
    )

    center_word_same_concept = bool(center_word_same_concept_matches)
    center_word_same_category = bool(center_word_same_category_matches)
    center_same_concept = bool(center_same_concept_matches)
    center_same_category = bool(center_same_category_matches)
    span_exact = bool(span_exact_matches)
    span_same_concept = bool(span_same_concept_matches)
    span_same_category = bool(span_same_category_matches)

    best_context = ""
    for name, matched in [
        ("exact_center", center_exact),
        ("same_concept_center", center_same_concept),
        ("same_category_center", center_same_category),
        ("exact_span", span_exact),
        ("same_concept_span", span_same_concept),
        ("same_category_span", span_same_category),
    ]:
        if matched:
            best_context = name
            break

    return SurfaceContext(
        best_context=best_context,
        center_word_exact=center_word_exact,
        center_word_same_concept=center_word_same_concept,
        center_word_same_category=center_word_same_category,
        center_exact=center_exact,
        center_same_concept=center_same_concept,
        center_same_category=center_same_category,
        span_exact=span_exact,
        span_same_concept=span_same_concept,
        span_same_category=span_same_category,
        center_word_same_concept_terms=format_term_ids(center_word_same_concept_matches),
        center_word_same_category_terms=format_term_ids(center_word_same_category_matches),
        center_same_concept_terms=format_term_ids(center_same_concept_matches),
        center_same_category_terms=format_term_ids(center_same_category_matches),
        span_exact_refs=";".join(span_exact_matches),
        span_same_concept_refs=format_term_ref_matches(span_same_concept_matches),
        span_same_category_refs=format_term_ref_matches(span_same_category_matches),
    )


def contains_surface_term(normalized_word: str, normalized_term: str) -> bool:
    return bool(normalized_word and normalized_term and normalized_term in normalized_word)


def verse_indexes_for_hit(corpus: Corpus, hit: ELSHit) -> range:
    low, high = sorted((hit.start_offset, hit.end_offset))
    first = corpus.position_to_verse[low]
    last = corpus.position_to_verse[high]
    return range(first, last + 1)


def refs_for_indexed_term_index_matches(
    context_index: SurfaceContextIndex,
    indexed_refs: list[tuple[int, str]],
    term_indexes: tuple[int, ...],
) -> list[tuple[SurfaceTerm, str]]:
    matches = []
    for term_index in term_indexes:
        matched_indexes = context_index.verse_indexes_at(term_index)
        related = context_index.terms[term_index]
        for index, ref in indexed_refs:
            if index in matched_indexes:
                matches.append((related, ref))
    return matches


def format_term_ids(terms: list[SurfaceTerm]) -> str:
    return ";".join(term.term_id for term in terms)


def format_term_ref_matches(matches: list[tuple[SurfaceTerm, str]]) -> str:
    return ";".join(f"{term.term_id}@{ref}" for term, ref in matches)
