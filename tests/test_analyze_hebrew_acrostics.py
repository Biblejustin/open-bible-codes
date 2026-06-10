"""Tests for the Hebrew-acrostics helpers."""

from __future__ import annotations

from scripts.analyze_hebrew_acrostics import (
    ALPHABET,
    PE_BEFORE_AYIN,
    group_initials,
    verse_initials,
    walk_alphabet,
)


def test_orders_are_22_letters_and_swap_only_ayin_pe() -> None:
    assert len(ALPHABET) == 22 and len(set(ALPHABET)) == 22
    assert PE_BEFORE_AYIN.index("פ") + 1 == PE_BEFORE_AYIN.index("ע")
    assert sorted(PE_BEFORE_AYIN) == sorted(ALPHABET)


def test_verse_initials_skips_title_words_on_first_verse_only() -> None:
    vmap = {
        ("PS", "25", "1"): "לְדָוִד אֵלֶיךָ יהוה",
        ("PS", "25", "2"): "בְּךָ בָטַחְתִּי",
    }
    out = verse_initials(vmap, "PS", [(25, 1, 2)], skip_title_words=1)
    assert out == [("25:1", "א"), ("25:2", "ב")]   # title word skipped on v1 only


def test_group_initials_collapses_per_letter() -> None:
    initials = [("1", "א"), ("2", "א"), ("3", "ב"), ("4", "ב")]
    groups = group_initials(initials, 2)
    assert groups == [("1,2", "אא"), ("3,4", "בב")]


def test_walk_alphabet_complete() -> None:
    groups = [(str(i), c) for i, c in enumerate(ALPHABET)]
    result = walk_alphabet(groups, ALPHABET)
    assert result["complete"] is True
    assert result["matched_count"] == 22
    assert result["missing"] == ""


def test_walk_alphabet_detects_a_missing_letter() -> None:
    # Psalm 145 shape: all letters except nun
    groups = [(str(i), c) for i, c in enumerate(ALPHABET) if c != "נ"]
    result = walk_alphabet(groups, ALPHABET)
    assert result["missing"] == "נ"
    assert result["matched_count"] == 21
    assert result["complete"] is False


def test_walk_alphabet_ignores_continuation_verses() -> None:
    # variable-span acrostic: filler verses between letters must not steal
    # letters from later in the alphabet (the Psalm 37 shape)
    groups = [("1", "א"), ("2", "כ"), ("3", "ב"), ("4", "ו"), ("5", "ג")]
    result = walk_alphabet(groups, "אבג")
    assert result["matched"] == "אבג"
    assert {u["letter"] for u in result["unmatched"]} == {"כ", "ו"}


def test_walk_alphabet_pe_before_ayin_order() -> None:
    observed = "אבגדהוזחטיכלמנספעצקרשת"     # pe then ayin
    groups = [(str(i), c) for i, c in enumerate(observed)]
    swapped = walk_alphabet(groups, PE_BEFORE_AYIN)
    standard = walk_alphabet(groups, ALPHABET)
    assert swapped["complete"] is True
    assert standard["complete"] is False       # one of the pair falls out of order
