"""Pair-distance and compactness helpers for ELS hits."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from .search import ELSHit


@dataclass(frozen=True)
class PairMetrics:
    center_distance: float
    span_gap: int
    overlap: bool
    span_union_letters: int
    same_center_ref: bool
    same_center_chapter: bool
    same_signed_skip: bool
    same_abs_skip: bool
    skip_abs_delta: int
    compactness_score: float


def hit_center(hit: ELSHit) -> float:
    return (hit.start_offset + hit.end_offset) / 2


def hit_offsets(hit: ELSHit) -> tuple[int, ...]:
    return tuple(
        hit.start_offset + index * hit.skip
        for index in range(len(hit.sequence))
    )


def hit_bounds(hit: ELSHit) -> tuple[int, int]:
    low, high = sorted((hit.start_offset, hit.end_offset))
    return low, high


def span_gap(left: ELSHit, right: ELSHit) -> int:
    left_low, left_high = hit_bounds(left)
    right_low, right_high = hit_bounds(right)
    if left_low <= right_high and right_low <= left_high:
        return 0
    if left_high < right_low:
        return right_low - left_high
    return left_low - right_high


def center_chapter(ref: str) -> str:
    if not ref:
        return ""
    book, _, chapter_verse = ref.rpartition(" ")
    chapter, _, _verse = chapter_verse.partition(":")
    if not book or not chapter:
        return ""
    return f"{book} {chapter}"


def cylindrical_coordinates(offset: int, row_width: int) -> tuple[int, int]:
    validate_row_width(row_width)
    return offset // row_width, offset % row_width


def cylindrical_point_distance(left_offset: int, right_offset: int, row_width: int) -> float:
    left_row, left_col = cylindrical_coordinates(left_offset, row_width)
    right_row, right_col = cylindrical_coordinates(right_offset, row_width)
    raw_col_delta = abs(left_col - right_col)
    col_delta = min(raw_col_delta, row_width - raw_col_delta)
    row_delta = abs(left_row - right_row)
    return sqrt(col_delta * col_delta + row_delta * row_delta)


def cylindrical_hit_distance(left: ELSHit, right: ELSHit, row_width: int) -> float:
    validate_row_width(row_width)
    return min(
        cylindrical_point_distance(left_offset, right_offset, row_width)
        for left_offset in hit_offsets(left)
        for right_offset in hit_offsets(right)
    )


def validate_row_width(row_width: int) -> None:
    if row_width <= 0:
        raise ValueError("row_width must be > 0")


def pair_metrics(left: ELSHit, right: ELSHit) -> PairMetrics:
    left_low, left_high = hit_bounds(left)
    right_low, right_high = hit_bounds(right)
    gap = span_gap(left, right)
    center_distance = abs(hit_center(left) - hit_center(right))
    compactness_score = gap + center_distance
    left_chapter = center_chapter(left.center_ref)
    right_chapter = center_chapter(right.center_ref)
    return PairMetrics(
        center_distance=center_distance,
        span_gap=gap,
        overlap=gap == 0,
        span_union_letters=max(left_high, right_high) - min(left_low, right_low) + 1,
        same_center_ref=bool(left.center_ref and left.center_ref == right.center_ref),
        same_center_chapter=bool(left_chapter and left_chapter == right_chapter),
        same_signed_skip=left.skip == right.skip,
        same_abs_skip=abs(left.skip) == abs(right.skip),
        skip_abs_delta=abs(abs(left.skip) - abs(right.skip)),
        compactness_score=compactness_score,
    )
