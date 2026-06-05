"""Tests for the heptadic-structure helpers."""

from __future__ import annotations

from scripts.analyze_heptadic_structure import (
    book_counts,
    density_rows,
    seven_collocations,
)


def test_book_counts_tallies_seven_and_words() -> None:
    items = [("Rev", True), ("Rev", False), ("Rev", True), ("Matt", False), ("Matt", True)]
    per, words = book_counts(items)
    assert per["Rev"] == 2 and words["Rev"] == 3
    assert per["Matt"] == 1 and words["Matt"] == 2


def test_density_rows_rate_and_order() -> None:
    per = {"Rev": 60, "Matt": 11}
    words = {"Rev": 10000, "Matt": 18000}
    rows = density_rows(per, words)
    # Revelation's rate is far higher, so it ranks first
    assert rows[0]["book"] == "Rev"
    assert rows[0]["per_1000"] == 6.0
    assert rows[1]["book"] == "Matt"
    assert rows[1]["per_1000"] == round(1000 * 11 / 18000, 2)


def test_seven_collocations_pairs_hepta_with_next_noun() -> None:
    # ἑπτά then the next noun in the same verse is the counted "seven X"
    items = [
        ("Rev 1:4", "ἑπτά", "adjective"), ("Rev 1:4", "πνεῦμα", "noun"),
        ("Rev 1:12", "ἑπτά", "adjective"), ("Rev 1:12", "χρυσοῦς", "adjective"),
        ("Rev 1:12", "λυχνία", "noun"),
        ("Rev 1:16", "ἑπτά", "adjective"), ("Rev 1:16", "ἀστήρ", "noun"),
        ("Rev 1:16", "πνεῦμα", "noun"),   # second noun, not counted for this ἑπτά
    ]
    things = seven_collocations(items)
    assert things["πνεῦμα"] == 1
    assert things["λυχνία"] == 1     # skips the intervening adjective χρυσοῦς
    assert things["ἀστήρ"] == 1
    assert sum(things.values()) == 3


def test_seven_collocations_stops_at_verse_boundary() -> None:
    # an ἑπτά with no following noun before the verse ends counts nothing
    items = [("Rev 5:1", "ἑπτά", "adjective"), ("Rev 5:2", "ἄγγελος", "noun")]
    assert seven_collocations(items) == {}
