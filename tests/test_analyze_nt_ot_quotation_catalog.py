"""Tests for the full-catalog NT-OT quotation sweep helpers."""

from __future__ import annotations

from scripts.analyze_nt_ot_quotation_catalog import (
    candidate_lxx_refs,
    longest_common_run,
    lxx_psalm_chapter,
    ordered_recall,
    parse_catalog,
)


def test_lxx_psalm_chapter_offset() -> None:
    assert lxx_psalm_chapter(110) == 109   # MT 110 -> LXX 109
    assert lxx_psalm_chapter(22) == 21
    assert lxx_psalm_chapter(8) == 8        # <= 8 unchanged
    assert lxx_psalm_chapter(150) == 150    # >= 148 unchanged


def test_candidate_lxx_refs_psalm_window() -> None:
    refs = candidate_lxx_refs("PSA", 110, 1)
    # tries LXX 109 across a +/-1 verse window
    assert ("PSA", "109", "1") in refs
    assert ("PSA", "109", "2") in refs
    # non-Psalm book: same chapter, verse window
    refs2 = candidate_lxx_refs("ISA", 7, 14)
    assert ("ISA", "7", "14") in refs2 and ("ISA", "7", "13") in refs2


def test_parse_catalog() -> None:
    rows = parse_catalog("Matt 1:23 | Isa 7:14\n1 Cor 15:54 | Isa 25:8\n")
    assert rows[0] == ("Matt", "1", "23", "Isa", "7", "14")
    assert rows[1] == ("1 Cor", "15", "54", "Isa", "25", "8")


def test_overlap_helpers() -> None:
    assert ordered_recall("α β γ δ", "β γ") == 1.0
    assert ordered_recall("α β", "") == 0.0
    assert longest_common_run("α β γ δ", "x β γ y") == 2
