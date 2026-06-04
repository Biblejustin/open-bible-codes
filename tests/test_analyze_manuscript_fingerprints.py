"""Tests for the manuscript-fingerprint analysis helpers."""

from __future__ import annotations

from scripts.analyze_manuscript_fingerprints import (
    classify_agreement,
    is_present,
    norm_tokens,
    similarity,
)


def test_norm_tokens_normalizes_greek() -> None:
    assert norm_tokens("Θεὸς ἦν ὁ λόγος") == ["θεοσ", "ην", "ο", "λογοσ"]


def test_similarity_bounds() -> None:
    assert similarity(["a", "b", "c"], ["a", "b", "c"]) == 1.0
    assert similarity(["a", "b"], ["x", "y"]) == 0.0


def test_classify_agreement_picks_closer_edition() -> None:
    ms = ["a", "b", "c", "d"]
    rp = ["a", "b", "c", "d"]   # identical to ms
    wh = ["a", "x", "y", "z"]   # far from ms
    assert classify_agreement(ms, rp, wh) == "byzantine"
    assert classify_agreement(ms, wh, rp) == "alexandrian"
    assert classify_agreement(ms, ms, ms) == "tie"


def test_is_present() -> None:
    w = {"40017021": "text", "40018011": "-"}
    assert is_present(w, "40017021") is True
    assert is_present(w, "40018011") is False
    assert is_present(w, "99999999") is False
