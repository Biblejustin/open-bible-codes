"""Reusable statistics helpers for ELS screening analyses."""

from __future__ import annotations

from collections.abc import Sequence


def tail_p_value_ge(observed: float | int | None, samples: Sequence[float | int]) -> float | None:
    """Empirical greater-or-equal tail probability with add-one smoothing."""
    if observed is None or not samples:
        return None
    return (sum(1 for sample in samples if sample >= observed) + 1) / (len(samples) + 1)


def tail_p_value_le(observed: float | int | None, samples: Sequence[float | int]) -> float | None:
    """Empirical less-or-equal tail probability with add-one smoothing."""
    if observed is None or not samples:
        return None
    return (sum(1 for sample in samples if sample <= observed) + 1) / (len(samples) + 1)


def benjamini_hochberg_q_values(
    p_values: Sequence[float | None],
) -> list[float | None]:
    """Return Benjamini-Hochberg adjusted q-values, preserving None slots."""
    indexed = sorted(
        (p_value, index)
        for index, p_value in enumerate(p_values)
        if p_value is not None
    )
    q_values: list[float | None] = [None for _value in p_values]
    total = len(indexed)
    previous = 1.0
    for rank, (p_value, index) in reversed(list(enumerate(indexed, start=1))):
        adjusted = min(1.0, p_value * total / rank)
        previous = min(previous, adjusted)
        q_values[index] = previous
    return q_values


def direction_count(direction: str) -> int:
    """Number of directional scans represented by a direction option."""
    return 2 if direction == "both" else 1


def estimated_search_space(
    text_length: int,
    query_length: int,
    min_skip: int,
    max_skip: int,
    direction: str,
) -> int:
    """Count valid ELS start positions before term-frequency weighting."""
    if text_length < 1 or query_length < 1 or min_skip > max_skip:
        return 0
    forward_positions = 0
    for skip in range(min_skip, max_skip + 1):
        span = (query_length - 1) * skip
        if span < text_length:
            forward_positions += text_length - span
    return forward_positions * direction_count(direction)


def hits_per_million(observed: int, search_space: int) -> float | str:
    if search_space < 1:
        return ""
    return round_float(1_000_000 * observed / search_space)


def round_float(value: float | None) -> float | str:
    if value is None:
        return ""
    return round(value, 6)


def numeric_value(value: object) -> float | None:
    if value == "" or value is None:
        return None
    return float(value)
