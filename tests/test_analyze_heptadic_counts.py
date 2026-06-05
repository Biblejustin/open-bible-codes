"""Tests for the heptadic-counts helpers."""

from __future__ import annotations

from scripts.analyze_heptadic_counts import (
    greek_letter_counts,
    greek_tokens,
    hebrew_letters,
    heptad_rate,
    is_heptad,
)


def test_hebrew_letters_strips_points_and_markers() -> None:
    # vowel points, cantillation, the morpheme slash, and spaces all drop out
    assert hebrew_letters("בְּ/רֵאשִׁ֖ית") == "בראשית"
    assert len(hebrew_letters("בָּרָ֣א")) == 3


def test_greek_tokens_normalizes() -> None:
    assert greek_tokens("Βίβλος γενέσεως") == ["βιβλοσ", "γενεσεωσ"]


def test_greek_letter_counts_splits_vowels_and_consonants() -> None:
    letters, vowels, consonants = greek_letter_counts(["αβγ", "εδ"])
    assert letters == 5
    assert vowels == 2  # alpha, epsilon
    assert consonants == 3


def test_is_heptad() -> None:
    assert is_heptad(28) is True
    assert is_heptad(14) is True
    assert is_heptad(172) is False
    assert is_heptad(0) is False


def test_heptad_rate_empty() -> None:
    r = heptad_rate([])
    assert r == {"verses": 0, "words_pct": 0.0, "letters_pct": 0.0, "both_pct": 0.0}


def test_heptad_rate_counts_each_dimension() -> None:
    # two of three verses are heptadic in both words and letters; one in neither
    r = heptad_rate([(7, 28), (7, 28), (3, 5)])
    assert r["verses"] == 3
    assert r["words_pct"] == round(2 / 3, 4)
    assert r["letters_pct"] == round(2 / 3, 4)
    assert r["both_pct"] == round(2 / 3, 4)


def test_heptad_rate_dimensions_are_independent() -> None:
    # words divisible by 7 but letters not, and vice versa: both_pct stays 0
    r = heptad_rate([(7, 5), (3, 14)])
    assert r["words_pct"] == 0.5
    assert r["letters_pct"] == 0.5
    assert r["both_pct"] == 0.0
