"""Tests for the famous-variants attestation helpers."""

from __future__ import annotations

from scripts.analyze_famous_variants_attestation import (
    classify_1tim_3_16,
    classify_comma,
    classify_presence,
    classify_rev_13_18,
    clean,
    has_greek,
    verse_line,
)


def test_clean_strips_markers_and_resolves_overline_nu() -> None:
    assert clean("/αναστασ δε πρω^ι |πρωτη~") == "αναστασ δε πρωι πρωτη"
    assert clean("αριθμο¯") == "αριθμον"


def test_verse_line_and_has_greek() -> None:
    ms = "41016008 και εξελθουσαι\n41016009 -\n41016010 -~\n"
    assert verse_line(ms, "41016008") == "και εξελθουσαι"
    assert verse_line(ms, "41016009") == "-"
    assert verse_line(ms, "99999999") is None
    assert has_greek("και εξελθουσαι") is True
    assert has_greek("-") is False
    assert has_greek("-~") is False          # absence marker with uncertainty sign


def test_classify_presence_treats_marker_lines_as_absent() -> None:
    assert classify_presence("-~") == "verse absent (marked '-')"
    assert classify_presence("/αναστασ δε πρωι") == "verse present"


def test_classify_rev_13_18_readings() -> None:
    # P47 style numerals; Sinaiticus spelled; P115 numerals; Ephraemi spelled 616
    assert classify_rev_13_18("εστιν δε $χ $ξ $σ").startswith("666 (numeral")
    assert classify_rev_13_18("εξακοσιαι εξηκο¯/τα εξ").startswith("666 (spelled")
    assert classify_rev_13_18("+εστιν η $χ $ι $σ").startswith("616 (numeral")
    assert classify_rev_13_18("εστι¯ /εξακοσιαι δεκα εξ").startswith("616 (spelled")


def test_classify_1tim_3_16_readings() -> None:
    assert classify_1tim_3_16("μυστηριον οσ ε/φανερωθη") == "hos (relative pronoun)"
    assert classify_1tim_3_16("μυστηριον x{οσ} {=θσ} εφανερωθη") == (
        "hos (first hand), corrected to theos")
    assert classify_1tim_3_16("μυστηριον =θσ εφανερωθη") == "theos (nomen sacrum)"


def test_classify_comma() -> None:
    assert classify_comma("οτι τρεισ εισιν οι μαρτυρουντεσ") == "short reading (no Comma)"
    assert classify_comma("εν τω ουρανω ο πατηρ ο λογοσ").startswith("Comma present")
