"""Tests for the CNTR MES manuscript importer (data-free, synthetic lines)."""

from __future__ import annotations

from pathlib import Path

from els.corpus import _read_cntr_mes, _resolve_mes_corrections
from els.normalization import normalize_greek


def test_correction_resolves_to_first_hand_by_default() -> None:
    assert _resolve_mes_corrections("τον x{ισακ} {ισαακ} δε", "first") == "τον ισακ δε"
    assert _resolve_mes_corrections("τον x{ισακ} {ισαακ} δε", "edited") == "τον ισαακ δε"


def test_correction_original_omission_keeps_nothing_first_hand() -> None:
    # x{} {ουν} = original scribe wrote nothing, corrector added ουν.
    assert _resolve_mes_corrections("ινα x{} {ουν} οσα", "first") == "ινα  οσα"
    assert _resolve_mes_corrections("ινα x{} {ουν} οσα", "edited") == "ινα ουν οσα"


def test_correction_drops_corrector_layers_first_hand() -> None:
    # {base} a{corrector}: first-hand keeps base, drops the a-correction.
    assert _resolve_mes_corrections("{και} a{ϗ ελθον} ευρισκει", "first") == "και ευρισκει"


def test_no_correction_passthrough() -> None:
    assert _resolve_mes_corrections("βιβλοσ γενεσεωσ", "first") == "βιβλοσ γενεσεωσ"


def _rows(lines: list[str], tmp_path: Path, **opts) -> list[dict]:
    f = tmp_path / "ms.txt"
    f.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return list(_read_cntr_mes(f, "MS", opts))


def test_absent_verse_is_skipped(tmp_path: Path) -> None:
    rows = _rows(["41016008 και εξελθουσαι", "41016009 -", "41016020 -"], tmp_path)
    refs = [r["ref"] for r in rows]
    assert refs == ["MRK 16:8"]  # 16:9 and 16:20 dropped


def test_ref_book_chapter_verse_mapping(tmp_path: Path) -> None:
    rows = _rows(["40001001 βιβλοσ", "44008037 και"], tmp_path)
    assert rows[0]["ref"] == "MAT 1:1" and rows[0]["book"] == "MAT"
    assert rows[1]["ref"] == "ACT 8:37"


def test_markup_strips_to_clean_greek(tmp_path: Path) -> None:
    # nomina sacra (=), line break (/), damaged (%): all non-Greek, normalized away,
    # leaving the abbreviated written letters.
    rows = _rows(["40001001 βιβλοσ /=ιυ =χυ σα%λωμων"], tmp_path)
    words = [normalize_greek(tok) for tok in rows[0]["text"].split()]
    words = [w for w in words if w]
    assert words == ["βιβλοσ", "ιυ", "χυ", "σαλωμων"]


def test_extant_only_drops_missing_letters(tmp_path: Path) -> None:
    # default keeps the reconstructed reading (υμι^ν -> υμιν); extant_only drops it.
    default = _rows(["43017012 υμι^ν"], tmp_path)
    extant = _rows(["43017012 υμι^ν"], tmp_path, extant_only=True)
    assert normalize_greek(default[0]["text"]) == "υμιν"
    assert normalize_greek(extant[0]["text"]) == "υμν"
