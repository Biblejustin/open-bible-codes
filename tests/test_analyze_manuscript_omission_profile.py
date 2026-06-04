"""Tests for the per-manuscript omission profile."""

from __future__ import annotations

from pathlib import Path

from scripts.analyze_manuscript_omission_profile import fmt_ref, load_statuses


def test_fmt_ref_uses_usfm_codes() -> None:
    assert fmt_ref("41016009") == "MRK 16:9"
    assert fmt_ref("44008037") == "ACT 8:37"


def test_load_statuses_present_vs_omitted(tmp_path: Path) -> None:
    f = tmp_path / "01.txt"
    f.write_text("41016008 και εξελθουσαι\n41016009 -\n", encoding="utf-8")
    status = load_statuses(f)
    assert status["41016008"] == "present"
    assert status["41016009"] == "omitted"
    # a verse with no line is simply absent from the mapping (not_covered)
    assert "41016010" not in status
