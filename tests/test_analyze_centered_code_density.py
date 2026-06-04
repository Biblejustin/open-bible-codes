"""Tests for the centered-code-density premise test."""

from __future__ import annotations

from pathlib import Path

from els.corpus import load_corpus
from scripts.analyze_centered_code_density import top_terms


def _toy_corpus(text: str, tmp_path: Path):
    (tmp_path / "toy.txt").write_text(text, encoding="utf-8")
    (tmp_path / "toy.toml").write_text(
        'name = "toy"\nlanguage = "greek"\n\n[[sources]]\n'
        'name = "toy"\nformat = "text"\npath = "toy.txt"\nref = "T 1:1"\nbook = "T"\n',
        encoding="utf-8",
    )
    return load_corpus(tmp_path / "toy.toml")


def test_top_terms_ranks_by_frequency_and_filters_short(tmp_path: Path) -> None:
    # 'δοξα' avoids the final-sigma fold; words are normalized (accents stripped,
    # ς->σ) before counting.
    corpus = _toy_corpus("δοξα δοξα δοξα αββα αββα ευα", tmp_path)
    terms = top_terms(corpus, "greek")
    assert terms[0] == ("δοξα", 3)
    assert ("αββα", 2) in terms
    # 'ευα' is length 3, below MIN_LEN, so excluded
    assert all(term != "ευα" for term, _ in terms)
