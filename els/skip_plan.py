"""Expected-hit skip cap planning."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class SkipPlan:
    term: str
    normalized_term: str
    normalized_length: int
    min_skip: int
    max_skip_limit: int
    selected_max_skip: int
    direction: str
    target_expected_hits: float
    expected_hits: float
    expected_at_min_skip: float
    status: str


def query_probability(text: str, query: str) -> float:
    if not text or not query:
        return 0.0
    counts = Counter(text)
    total = len(text)
    probability = 1.0
    for char in query:
        probability *= counts.get(char, 0) / total
    return probability


def directional_factor(direction: str) -> int:
    if direction == "both":
        return 2
    if direction in {"forward", "backward"}:
        return 1
    raise ValueError(f"unsupported direction: {direction}")


def expected_hits_for_skip(
    text_length: int,
    query_length: int,
    probability: float,
    skip: int,
    direction: str,
) -> float:
    span = (query_length - 1) * skip
    if text_length <= 0 or query_length <= 0 or span >= text_length:
        return 0.0
    placements = text_length - span
    return placements * probability * directional_factor(direction)


def expected_hits_through_skip(
    text_length: int,
    query_length: int,
    probability: float,
    *,
    min_skip: int,
    max_skip: int,
    direction: str,
) -> float:
    return sum(
        expected_hits_for_skip(text_length, query_length, probability, skip, direction)
        for skip in range(min_skip, max_skip + 1)
    )


def max_possible_skip(text_length: int, query_length: int) -> int:
    if query_length <= 1:
        return max(1, text_length - 1)
    return max(1, (text_length - 1) // (query_length - 1))


def letters_per_term_skip(text_length: int, query_length: int) -> int:
    if query_length <= 0:
        return 0
    return max(1, text_length // query_length)


def max_skip_for_mode(text_length: int, query_length: int, mode: str) -> int:
    if mode == "full-span":
        return max_possible_skip(text_length, query_length)
    if mode == "letters-per-term":
        return letters_per_term_skip(text_length, query_length)
    if mode == "fixed":
        raise ValueError("fixed mode does not compute a dynamic max skip")
    raise ValueError(f"unsupported max skip mode: {mode}")


def plan_skip_cap(
    text: str,
    term: str,
    normalized_term: str,
    *,
    min_skip: int,
    max_skip_limit: int,
    direction: str,
    target_expected_hits: float,
) -> SkipPlan:
    if min_skip < 1:
        raise ValueError("min_skip must be >= 1")
    if max_skip_limit < min_skip:
        raise ValueError("max_skip_limit must be >= min_skip")
    if target_expected_hits < 0:
        raise ValueError("target_expected_hits must be >= 0")

    query_length = len(normalized_term)
    probability = query_probability(text, normalized_term)
    hard_max_skip = min(max_skip_limit, max_possible_skip(len(text), query_length))
    selected_max_skip = min_skip
    cumulative = 0.0
    expected_at_min_skip = expected_hits_for_skip(
        len(text),
        query_length,
        probability,
        min_skip,
        direction,
    )
    status = "planned"

    if not normalized_term:
        return SkipPlan(
            term=term,
            normalized_term=normalized_term,
            normalized_length=0,
            min_skip=min_skip,
            max_skip_limit=max_skip_limit,
            selected_max_skip=min_skip,
            direction=direction,
            target_expected_hits=target_expected_hits,
            expected_hits=0.0,
            expected_at_min_skip=0.0,
            status="skipped_empty_term",
        )

    for skip in range(min_skip, hard_max_skip + 1):
        next_expected = expected_hits_for_skip(
            len(text),
            query_length,
            probability,
            skip,
            direction,
        )
        if cumulative + next_expected > target_expected_hits and skip > min_skip:
            status = "capped_by_target"
            break
        cumulative += next_expected
        selected_max_skip = skip
    else:
        status = "reached_limit"

    if expected_at_min_skip > target_expected_hits:
        status = "target_below_min_skip_expectation"

    return SkipPlan(
        term=term,
        normalized_term=normalized_term,
        normalized_length=query_length,
        min_skip=min_skip,
        max_skip_limit=max_skip_limit,
        selected_max_skip=selected_max_skip,
        direction=direction,
        target_expected_hits=target_expected_hits,
        expected_hits=cumulative,
        expected_at_min_skip=expected_at_min_skip,
        status=status,
    )
