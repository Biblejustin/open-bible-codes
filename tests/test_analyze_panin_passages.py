"""Tests for the Panin-passages helpers (removal / load-bearing test)."""

from __future__ import annotations

from scripts.analyze_panin_passages import (
    forms_count,
    mark,
    tally,
    verse_codes,
)


def test_verse_codes_builds_cntr_codes() -> None:
    assert verse_codes(41, 16, [9, 10, 11]) == ["41016009", "41016010", "41016011"]
    assert verse_codes(40, 1, range(1, 3)) == ["40001001", "40001002"]


def test_tally_counts_tokens_and_letters() -> None:
    edition = {"41016009": "Καὶ τότε", "41016010": "ὁ"}
    tokens, letters = tally(edition, ["41016009", "41016010"])
    assert tokens == 3                 # και, τοτε, ο
    assert letters == 3 + 4 + 1        # normalized lengths
    # a code with no text contributes nothing
    assert tally(edition, ["99999999"]) == (0, 0)


def test_forms_count_is_distinct_tokens() -> None:
    edition = {"a": "ο ο θεοσ", "b": "ο"}
    assert forms_count(edition, ["a", "b"]) == 2    # {ο, θεοσ}


def test_mark_flags_nonzero_multiples_of_seven() -> None:
    assert mark(133) == "yes"     # 19 x 7
    assert mark(299) == "no"
    assert mark(0) == "no"
