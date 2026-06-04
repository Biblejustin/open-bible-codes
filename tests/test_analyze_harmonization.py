"""Tests for the harmonization analysis helpers."""

from __future__ import annotations

from scripts.analyze_harmonization import classify, has_token_stem, is_present


def test_has_token_stem() -> None:
    assert has_token_stem("γενηθητω το θελημα σου", "θελημ") is True
    assert has_token_stem("αλλα ρυσαι ημασ απο του πονηρου", "ρυσ") is True
    assert has_token_stem("πατερ αγιασθητω το ονομα σου", "δανιη") is False


def test_classify_verdicts() -> None:
    # TR has it, WH lacks it, source has it -> harmonization
    assert classify(True, False, True) == "byzantine_harmonization"
    # both editions have it -> not diagnostic
    assert classify(True, True, True) == "both_have_phrase"
    # neither has it
    assert classify(False, False, True) == "neither_has_phrase"
    # TR has it but source lacks it -> not a parallel harmonization
    assert classify(True, False, False) == "other"


def test_is_present() -> None:
    w = {"42011004": "text", "40017021": "-"}
    assert is_present(w, "42011004") is True
    assert is_present(w, "40017021") is False
    assert is_present(w, "00000000") is False
