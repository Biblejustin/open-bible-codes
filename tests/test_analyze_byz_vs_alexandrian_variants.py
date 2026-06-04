"""Tests for the Byzantine-vs-Alexandrian whole-verse presence table."""

from __future__ import annotations

from pathlib import Path

from scripts.analyze_byz_vs_alexandrian_variants import fmt_ref, load_witness


def test_fmt_ref_decodes_book_chapter_verse() -> None:
    ref, book, chapter, verse = fmt_ref("41016009")
    assert (ref, book, chapter, verse) == ("Mark 16:9", "Mark", "16", "9")
    assert fmt_ref("54003016")[0] == "1Tim 3:16"


def test_load_witness_marks_absent_vs_present(tmp_path: Path) -> None:
    f = tmp_path / "WX.txt"
    f.write_text("41016008 και εξελθουσαι\n41016009 -\n", encoding="utf-8")
    siglum, status = load_witness(f)
    assert siglum == "WX"
    assert status["41016009"] == "absent"
    assert status["41016008"] != "absent"
