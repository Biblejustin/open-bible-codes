"""Tests for the genealogy-chronology numeral composers."""

from __future__ import annotations

from scripts.analyze_genealogy_chronology import (
    PATRIARCHS,
    greek_number,
    hebrew_number,
)


def test_hebrew_number_thirty_and_a_hundred() -> None:
    # Genesis 5:3 shape: "thirty and a hundred year" = 130, stop at begat
    tokens = [("7970", "שלשים"), ("3967", "מאת"), ("8141", "שנה"),
              ("3205", "ויולד"), ("702", "ארבע")]
    assert hebrew_number(tokens) == 130


def test_hebrew_number_unit_plus_singular_hundred_adds() -> None:
    # Genesis 5:6 shape: "five years and a hundred year" = 105, not 500
    tokens = [("2568", "חמש"), ("8141", "שנים"), ("3967", "מאת"), ("8141", "שנה")]
    assert hebrew_number(tokens) == 105


def test_hebrew_number_unit_before_plural_hundreds_multiplies() -> None:
    # "nine hundreds year" = 900; "three hundreds" = 300
    assert hebrew_number([("8672", "תשע"), ("3967", "מאות")]) == 900
    assert hebrew_number([("7969", "שלש"), ("3967", "מאות"), ("8141", "שנה")]) == 300


def test_hebrew_number_compound_182() -> None:
    # Genesis 5:28 shape: "two and eighty year and a hundred year" = 182
    tokens = [("8147", "שתים"), ("8084", "ושמנים"), ("8141", "שנה"),
              ("3967", "מאת"), ("8141", "שנה")]
    assert hebrew_number(tokens) == 182


def test_greek_number_stops_at_begat_with_or_without_nu() -> None:
    assert greek_number("εκατον τριακοντα πεντε ετη και εγεννησε τον καιναν") == 135
    assert greek_number("διακοσια τριακοντα ετη και εγεννησεν υιον") == 230


def test_greek_number_after_name_anchors_on_lived_name() -> None:
    # the LXX composite verse: Arpachshad's after-years (430) come first; the
    # count must start at "lived Cainan", not at Cainan's first mention
    verse = ("και εζησεν αρφαξαδ μετα το γεννησαι αυτον τον καιναν ετη "
             "τετρακοσια και εγεννησεν υιους και εζησε καιναν εκατον και "
             "τριακοντα ετη και εγεννησε τον σαλα")
    assert greek_number(verse, after_name="καιναν") == 130
    assert greek_number(verse) == 400          # without the anchor: the first clause


def test_patriarch_table_is_well_formed() -> None:
    names = [p[0] for p in PATRIARCHS]
    assert names[0] == "Adam" and names[-1] == "Terah"
    cainan = next(p for p in PATRIARCHS if p[0].startswith("Cainan"))
    assert cainan[1] is None and cainan[3] == "καιναν"   # LXX-only, anchored
