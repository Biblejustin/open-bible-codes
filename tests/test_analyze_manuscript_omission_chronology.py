"""Tests for the manuscript omission chronology analysis."""

from __future__ import annotations

from scripts.analyze_manuscript_omission_chronology import century_bucket, pearson


def test_century_bucket_boundaries() -> None:
    assert century_bucket(200).startswith("II-III")
    assert century_bucket(250).startswith("II-III")
    assert century_bucket(300).startswith("III-IV")
    assert century_bucket(350).startswith("III-IV")
    assert century_bucket(400).startswith("V")
    assert century_bucket(450).startswith("V")


def test_pearson_perfect_and_degenerate() -> None:
    assert pearson([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]) == 1.0
    assert pearson([1.0, 2.0, 3.0], [6.0, 4.0, 2.0]) == -1.0
    assert pearson([1.0, 2.0], [1.0, 2.0]) is None  # n < 3
    assert pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) is None  # zero variance


def test_pearson_negative_trend_for_older_more_omission() -> None:
    # older (smaller year) -> higher omission rate should give negative r
    r = pearson([200, 350, 450], [0.59, 0.43, 0.27])
    assert r is not None and r < 0
