"""Tests for the nomina sacra reverence analysis helpers."""

from __future__ import annotations

from scripts.analyze_nomina_sacra_reverence import (
    bare,
    full_name,
    is_nomen_sacrum,
    nomen_sacrum_name,
    raw_tokens,
    verse_nomina_sacra,
)


def test_bare_strips_mes_markup() -> None:
    assert bare("+=θν") == "θν"
    assert bare("~=θυ") == "θυ"
    assert bare("x{ραβδοσ}") == "ραβδοσ"


def test_is_nomen_sacrum_detects_marker() -> None:
    assert is_nomen_sacrum("=θσ") is True
    assert is_nomen_sacrum("+=θν") is True
    assert is_nomen_sacrum("θεοσ") is False


def test_nomen_sacrum_name_classifies_core_divine_names() -> None:
    assert nomen_sacrum_name("θσ") == "THEOS"
    assert nomen_sacrum_name("κσ") == "KYRIOS"
    assert nomen_sacrum_name("ιυ") == "IESOUS"
    assert nomen_sacrum_name("χσ") == "CHRISTOS"
    assert nomen_sacrum_name("υν") == "HUIOS"
    assert nomen_sacrum_name("πρσ") is None  # Father not in the core set


def test_full_name_classifies_spelled_out_forms() -> None:
    assert full_name("θεοσ") == "THEOS"
    assert full_name("κυριου") == "KYRIOS"
    assert full_name("ιησουν") == "IESOUS"
    assert full_name("χριστου") == "CHRISTOS"
    assert full_name("υιοσ") == "HUIOS"
    assert full_name("λογοσ") is None


def test_verse_nomina_sacra_finds_lord_and_god_at_john_20_28() -> None:
    # Thomas's confession as Sinaiticus writes it: both titles contracted
    text = "απεκριθη ο θωμασ και ειπεν αυτω ο =κσ μου και ο =θσ μου"
    assert verse_nomina_sacra(text) == {"KYRIOS", "THEOS"}


def test_raw_tokens_splits_on_break_markers() -> None:
    assert raw_tokens("εν αρχη/ην ο λογοσ") == ["εν", "αρχη", "ην", "ο", "λογοσ"]
