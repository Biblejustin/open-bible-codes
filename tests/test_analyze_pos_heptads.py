"""Tests for the part-of-speech heptad helpers."""

from __future__ import annotations

from scripts.analyze_pos_heptads import mean_count, pos_heptad_rate, unit_pos_counts

ROWS = [
    ("Matt", "1", "1", "noun"), ("Matt", "1", "1", "verb"),
    ("Matt", "1", "2", "noun"), ("Matt", "1", "2", "noun"),
    ("Matt", "2", "1", "verb"),
]


def test_unit_pos_counts_groups_by_level() -> None:
    verses = unit_pos_counts(ROWS, "verse")
    assert verses[("Matt", "1", "1")]["noun"] == 1
    assert verses[("Matt", "1", "2")]["noun"] == 2
    chapters = unit_pos_counts(ROWS, "chapter")
    assert chapters[("Matt", "1")]["noun"] == 3      # both verses of ch1
    assert chapters[("Matt", "1")]["verb"] == 1
    books = unit_pos_counts(ROWS, "book")
    assert books[("Matt",)]["noun"] == 3 and books[("Matt",)]["verb"] == 2


def test_pos_heptad_rate_counts_nonzero_multiples_of_seven() -> None:
    # two units, one with 7 nouns (heptad), one with 3 (not)
    units = {("a",): {"noun": 7}, ("b",): {"noun": 3}}
    assert pos_heptad_rate(units, "noun") == 0.5
    # zero never counts as a heptad
    assert pos_heptad_rate({("a",): {"noun": 0}}, "noun") == 0.0
    assert pos_heptad_rate({}, "noun") == 0.0


def test_mean_count() -> None:
    units = {("a",): {"verb": 4}, ("b",): {"verb": 2}}
    assert mean_count(units, "verb") == 3.0
    assert mean_count(units, "noun") == 0.0      # absent POS counts as zero
