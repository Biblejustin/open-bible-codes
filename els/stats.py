"""Simple null-model helpers for ELS counts."""

from __future__ import annotations

import random
import statistics
from dataclasses import dataclass
from typing import Sequence

from .corpus import Corpus
from .normalization import normalize_text
from .search import count_els_terms_by_lanes
from .statistics import tail_p_value_ge


@dataclass(frozen=True)
class ShuffleResult:
    observed: int
    shuffled_counts: tuple[int, ...]
    p_greater_equal: float


@dataclass(frozen=True)
class NullSummary:
    samples: int
    mean: float | None
    stdev: float | None
    z_score: float | None
    p_greater_equal: float | None
    percentile: float | None
    min_count: int | None
    max_count: int | None


def shuffled_letter_control(
    corpus: Corpus,
    term: str,
    *,
    min_skip: int,
    max_skip: int,
    direction: str,
    shuffles: int,
    seed: int,
    jobs: int = 1,
) -> ShuffleResult:
    return shuffled_letter_controls(
        corpus,
        [term],
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
        shuffles=shuffles,
        seed=seed,
        jobs=jobs,
    )[0][1]


def shuffled_letter_controls(
    corpus: Corpus,
    terms: list[str],
    *,
    min_skip: int,
    max_skip: int,
    direction: str,
    shuffles: int,
    seed: int,
    jobs: int = 1,
) -> list[tuple[str, ShuffleResult]]:
    prepared = [(term, normalize_term(corpus, term)) for term in terms]
    queries = sorted({query for _term, query in prepared if query})
    observed_counts = count_els_terms_by_lanes(
        corpus.text,
        queries,
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
        jobs=jobs,
    )

    null_counts = {query: [] for query in queries}
    rng = random.Random(seed)
    letters = list(corpus.text)
    for _ in range(shuffles):
        rng.shuffle(letters)
        counts = count_els_terms_by_lanes(
            "".join(letters),
            queries,
            min_skip=min_skip,
            max_skip=max_skip,
            direction=direction,
            jobs=jobs,
        )
        for query in queries:
            null_counts[query].append(counts.get(query, 0))

    results: list[tuple[str, ShuffleResult]] = []
    for term, query in prepared:
        if not query:
            observed = 0
            query_null_counts = tuple(0 for _ in range(shuffles))
        else:
            observed = observed_counts.get(query, 0)
            query_null_counts = tuple(null_counts.get(query, ()))
        greater_equal = sum(1 for count in query_null_counts if count >= observed)
        p_value = (greater_equal + 1) / (shuffles + 1)
        results.append(
            (
                term,
                ShuffleResult(
                    observed=observed,
                    shuffled_counts=query_null_counts,
                    p_greater_equal=p_value,
                ),
            )
        )
    return results


def summarize_null_counts(observed: int, null_counts: Sequence[int]) -> NullSummary:
    samples = len(null_counts)
    if samples == 0:
        return NullSummary(
            samples=0,
            mean=None,
            stdev=None,
            z_score=None,
            p_greater_equal=None,
            percentile=None,
            min_count=None,
            max_count=None,
        )
    mean = statistics.fmean(null_counts)
    stdev = statistics.pstdev(null_counts)
    z_score = None if stdev == 0 else (observed - mean) / stdev
    less_equal = sum(1 for count in null_counts if count <= observed)
    return NullSummary(
        samples=samples,
        mean=mean,
        stdev=stdev,
        z_score=z_score,
        p_greater_equal=tail_p_value_ge(observed, null_counts),
        percentile=100.0 * less_equal / samples,
        min_count=min(null_counts),
        max_count=max(null_counts),
    )


def shuffled_term_samples(query: str, *, shuffles: int, rng: random.Random) -> tuple[str, ...]:
    if shuffles < 1:
        return ()
    letters = list(query)
    samples: list[str] = []
    for _index in range(shuffles):
        shuffled = letters[:]
        rng.shuffle(shuffled)
        samples.append("".join(shuffled))
    return tuple(samples)


def normalize_term(corpus: Corpus, term: str) -> str:
    return normalize_text(
        term,
        corpus.language,
        keep_hebrew_final_forms=corpus.keep_hebrew_final_forms,
    )
