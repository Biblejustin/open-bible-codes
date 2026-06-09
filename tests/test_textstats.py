"""Tests for the shared text-statistics helpers in els.textstats."""

from __future__ import annotations

from els.textstats import (
    GRK_ISOPSEPHY,
    HEB_GEMATRIA,
    HEBREW_SEVEN_STRONGS,
    gematria,
    greek_letter_counts,
    greek_tokens,
    hebrew_letters,
    is_heptad,
    verse_map,
)


class _Verse:
    def __init__(self, book, chapter, verse, raw_text):
        self.book, self.chapter, self.verse, self.raw_text = book, chapter, verse, raw_text


class _Corpus:
    def __init__(self, verses):
        self.verses = verses


def test_verse_map_uppercases_book_and_keys_by_ref() -> None:
    corpus = _Corpus([_Verse("Gen", 1, 1, "text a"), _Verse("ISA", "7", "14", "text b")])
    out = verse_map(corpus)
    assert out[("GEN", "1", "1")] == "text a"
    assert out[("ISA", "7", "14")] == "text b"


def test_hebrew_letters_strips_points_and_markers() -> None:
    assert hebrew_letters("בְּ/רֵאשִׁ֖ית") == "בראשית"
    assert len(hebrew_letters("בָּרָ֣א")) == 3


def test_greek_tokens_normalizes() -> None:
    assert greek_tokens("Βίβλος γενέσεως") == ["βιβλοσ", "γενεσεωσ"]


def test_greek_letter_counts_splits_vowels_and_consonants() -> None:
    letters, vowels, consonants = greek_letter_counts(["αβγ", "εδ"])
    assert (letters, vowels, consonants) == (5, 2, 3)


def test_is_heptad() -> None:
    assert is_heptad(28) is True
    assert is_heptad(172) is False
    assert is_heptad(0) is False


def test_gematria_known_anchors() -> None:
    assert gematria("אלהים", HEB_GEMATRIA) == 86       # final mem takes 40
    assert gematria("יהוה", HEB_GEMATRIA) == 26
    assert gematria("ιησουσ", GRK_ISOPSEPHY) == 888
    assert gematria("x?", HEB_GEMATRIA) == 0            # unmapped contributes nothing


def test_hebrew_seven_strongs_is_the_number_family() -> None:
    # seven, seventh, seventy, week, sevenfold; excludes swear/satisfied/oath homographs
    assert HEBREW_SEVEN_STRONGS == {"7651", "7637", "7657", "7620", "7659", "7658"}
    assert "7650" not in HEBREW_SEVEN_STRONGS    # swear
    assert "7646" not in HEBREW_SEVEN_STRONGS    # satisfied
