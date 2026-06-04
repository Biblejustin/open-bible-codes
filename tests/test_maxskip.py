"""Tests for effective max-skip resolution (els.maxskip)."""

from __future__ import annotations

import pytest

from els.maxskip import effective_max_skip_for_normalized


def test_fixed_mode_returns_fixed_cap() -> None:
    assert effective_max_skip_for_normalized(1000, 5, 1, 50, "fixed", None) == 50


def test_fixed_mode_rejects_cap_below_min_skip() -> None:
    with pytest.raises(SystemExit):
        effective_max_skip_for_normalized(1000, 5, 2, 1, "fixed", None)


def test_zero_normalized_length_returns_none() -> None:
    assert effective_max_skip_for_normalized(1000, 0, 1, 50, "fixed", None) is None


def test_min_skip_below_one_raises() -> None:
    with pytest.raises(SystemExit):
        effective_max_skip_for_normalized(1000, 5, 0, 50, "fixed", None)


def test_limit_below_min_skip_raises() -> None:
    with pytest.raises(SystemExit):
        effective_max_skip_for_normalized(1000, 5, 10, 50, "fixed", 5)


def test_dynamic_mode_clamped_by_limit() -> None:
    # a large corpus yields a large dynamic cap; a small limit clamps it, and the
    # result stays within [min_skip, limit].
    val = effective_max_skip_for_normalized(100_000, 5, 1, 0, "letters-per-term", 7)
    assert val is not None and 1 <= val <= 7


def test_dynamic_cap_below_min_skip_returns_none() -> None:
    # an enormous min_skip with no fixed limit: the dynamic cap falls below it.
    assert effective_max_skip_for_normalized(100, 5, 10**9, 0, "full-span", None) is None
