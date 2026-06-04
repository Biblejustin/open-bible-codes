"""Tests for the term/corpus-argument helpers extracted from cli."""

from __future__ import annotations

import pytest

from els.term_io import accepted_term_languages, collect_terms, is_safe_report_label, parse_corpus_args


def test_accepted_term_languages() -> None:
    assert accepted_term_languages("greek") == {"greek"}
    assert accepted_term_languages("english") == {"english"}
    assert accepted_term_languages("hebrew") == {"hebrew", "michigan"}
    assert accepted_term_languages("michigan_claremont") == {"hebrew", "michigan"}
    assert accepted_term_languages("latin") == {"latin"}


def test_parse_corpus_args_label_config() -> None:
    assert parse_corpus_args(["TR=configs/tr.toml", "SBL=configs/sbl.toml"]) == [
        ("TR", "configs/tr.toml"),
        ("SBL", "configs/sbl.toml"),
    ]


def test_parse_corpus_args_rejects_malformed() -> None:
    with pytest.raises(SystemExit):
        parse_corpus_args(["no-equals-sign"])


def test_is_safe_report_label() -> None:
    assert is_safe_report_label("public_baseline-1") is True
    assert is_safe_report_label("bad/label") is False


def test_collect_terms_inline_and_file(tmp_path) -> None:
    f = tmp_path / "terms.txt"
    f.write_text("# comment\nθεος\n\nιησους\n", encoding="utf-8")
    assert collect_terms(["  αβ  ", ""], str(f)) == ["αβ", "θεος", "ιησους"]
