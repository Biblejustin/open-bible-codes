"""Tests for the within-verse Byzantine-vs-Alexandrian wording diff."""

from __future__ import annotations

from scripts.analyze_byz_vs_alexandrian_wording import DIVINE, diff_verse, norm_words


def test_norm_words_strips_accents_punctuation() -> None:
    assert norm_words("θεὸς ἐφανερώθη, ¶μυστήριον·") == ["θεοσ", "εφανερωθη", "μυστηριον"]


def test_diff_verse_classifies_substitution() -> None:
    byz_only, alex_only, dtype = diff_verse(["θεοσ", "εφανερωθη"], ["οσ", "εφανερωθη"])
    assert byz_only == ["θεοσ"] and alex_only == ["οσ"] and dtype == "substitution"


def test_diff_verse_classifies_length() -> None:
    assert diff_verse(["α", "β", "γ"], ["α", "γ"])[2] == "alex_shorter"
    assert diff_verse(["α", "γ"], ["α", "β", "γ"])[2] == "alex_longer"


def test_divine_set_contains_normalized_nominatives() -> None:
    # final-sigma folded forms must be present (the bug the importer test guards)
    assert "θεοσ" in DIVINE and "κυριοσ" in DIVINE and "ιησουσ" in DIVINE
