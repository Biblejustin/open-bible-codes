"""Tests for the messianic MT-vs-LXX analysis helpers."""

from __future__ import annotations

from scripts.analyze_messianic_mt_lxx import (
    greek_overlap,
    greek_tokens,
    has_stem,
    lookup,
)


def test_greek_tokens_normalizes() -> None:
    assert greek_tokens("ἡ παρθένος") == ["η", "παρθενοσ"]


def test_greek_overlap_identical_and_disjoint() -> None:
    assert greek_overlap("ἡ παρθένος τέξεται", "ἡ παρθένος τέξεται") == 1.0
    assert greek_overlap("ἡ παρθένος", "ὁ λόγος θεος") == 0.0


def test_has_stem_finds_virgin() -> None:
    assert has_stem("ἰδοὺ ἡ παρθένος ἐν γαστρὶ", "παρθεν") is True
    assert has_stem("ἰδοὺ ἡ νεᾶνις", "παρθεν") is False


def test_lookup_uses_uppercased_book() -> None:
    vmap = {("ISA", "7", "14"): "ἡ παρθένος"}
    assert lookup(vmap, ("Isa", "7", "14")) == "ἡ παρθένος"
    assert lookup(vmap, ("ISA", "7", "14")) == "ἡ παρθένος"
    assert lookup(vmap, ("Isa", "7", "15")) == ""
