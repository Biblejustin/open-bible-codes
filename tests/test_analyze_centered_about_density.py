"""Tests for the centered-AND-about density test."""

from __future__ import annotations

from pathlib import Path

from els.corpus import load_corpus
from scripts.analyze_centered_about_density import about


def _toy_corpus(text: str, tmp_path: Path):
    (tmp_path / "toy.txt").write_text(text, encoding="utf-8")
    (tmp_path / "toy.toml").write_text(
        'name = "toy"\nlanguage = "greek"\n\n[[sources]]\n'
        'name = "toy"\nformat = "text"\npath = "toy.txt"\nref = "T 1:1"\nbook = "T"\n',
        encoding="utf-8",
    )
    return load_corpus(tmp_path / "toy.toml")


def test_about_true_when_term_recurs_in_window(tmp_path: Path) -> None:
    corpus = _toy_corpus("δοξα αβγδ δοξα", tmp_path)
    # center offset 0 sits on the first 'δοξα'; it recurs within the window
    assert about(corpus, 0, "δοξα") is True


def test_about_false_when_term_isolated(tmp_path: Path) -> None:
    corpus = _toy_corpus("δοξα αβγδ εζηθ", tmp_path)
    assert about(corpus, 0, "δοξα") is False
