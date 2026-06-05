"""Tests for the TR-vs-critical anatomy helpers."""

from __future__ import annotations

from scripts.analyze_tr_critical_anatomy import (
    book_of,
    classify_pair,
    token_delta,
    wording_type,
)


def test_wording_type() -> None:
    assert wording_type(["a", "b", "c"], ["a", "c"]) == "alex_shorter"       # WH drops b
    assert wording_type(["a", "c"], ["a", "b", "c"]) == "alex_longer"        # WH adds b
    assert wording_type(["a", "b", "c"], ["a", "x", "c"]) == "substitution"  # swap
    assert wording_type(["a", "b", "c", "d"], ["a", "x", "d", "e"]) == "mixed"


def test_classify_pair() -> None:
    assert classify_pair(True, False, ["x"], []) == "alex_omits_verse"
    assert classify_pair(False, True, [], ["x"]) == "tr_omits_verse"
    assert classify_pair(False, False, [], []) == "both_absent"
    assert classify_pair(True, True, ["a", "b"], ["a", "b"]) == "identical"
    assert classify_pair(True, True, ["a", "b"], ["a"]) == "alex_shorter"


def test_token_delta() -> None:
    # WH drops one token, adds none
    assert token_delta(["a", "b", "c"], ["a", "c"]) == (1, 0)
    # substitution: one dropped, one added
    assert token_delta(["a", "b", "c"], ["a", "x", "c"]) == (1, 1)


def test_book_of() -> None:
    assert book_of("41016009") == "Mark"
    assert book_of("54003016") == "1Tim"
