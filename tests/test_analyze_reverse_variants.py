"""Tests for the reverse-variant analysis helpers."""

from __future__ import annotations

from scripts.analyze_reverse_variants import (
    covers,
    fmt_ref,
    has_token_stem,
    is_present,
)


def test_covers_vs_is_present() -> None:
    w = {"42022044": "ιδρωσ", "42024040": "-"}
    assert covers(w, "42022044") and is_present(w, "42022044")
    assert covers(w, "42024040") and not is_present(w, "42024040")  # covered but absent
    assert not covers(w, "99999999")  # lacuna


def test_has_token_stem_finds_spear() -> None:
    text = "αλλοσ δε λαβων λογχην ενυξεν αυτου την πλευραν"
    assert has_token_stem(text, "λογχη") is True
    assert has_token_stem("οι δε λοιποι ελεγον αφεσ", "λογχη") is False


def test_fmt_ref() -> None:
    assert fmt_ref("42022044") == "Luke 22:44"
    assert fmt_ref("40027049") == "Matt 27:49"
