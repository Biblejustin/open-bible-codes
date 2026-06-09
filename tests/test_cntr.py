"""Tests for the CNTR edition loader in els.cntr."""

from __future__ import annotations

from pathlib import Path

from els.cntr import load_edition


def test_load_edition_parses_mes_lines(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "WH.txt").write_text(
        "40001001 Βίβλος γενέσεως\n"
        "40001002 Ἀβραὰμ ἐγέννησεν\n"
        "not-a-verse-line\n",
        encoding="utf-8",
    )
    out = load_edition("WH", root=tmp_path)
    assert out["40001001"] == "Βίβλος γενέσεως"
    assert out["40001002"] == "Ἀβραὰμ ἐγέννησεν"
    assert len(out) == 2                      # the malformed line is skipped


def test_load_edition_missing_siglum_returns_empty(tmp_path: Path) -> None:
    assert load_edition("NOPE", root=tmp_path) == {}
