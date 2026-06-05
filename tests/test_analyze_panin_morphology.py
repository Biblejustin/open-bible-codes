"""Tests for the morphology-based Panin helpers."""

from __future__ import annotations

from scripts.analyze_panin_morphology import NON_ANCESTOR_PROPER, vocab_features


def test_vocab_features_basic_counts() -> None:
    # (lemma, pos, normalized_word); the article appears in two forms, one lemma
    entries = [
        ("ὁ", "article", "ο"), ("ὁ", "article", "τον"),     # 1 lemma, 2 forms, recurs
        ("Ἀβραάμ", "noun", "αβρααμ"),                          # proper noun, once, one form
        ("βίβλος", "noun", "βιβλοσ"),                          # common noun, once, one form
        ("δέ", "particle", "δε"),                              # non-noun
    ]
    f = vocab_features(entries)
    assert f["vocabulary"] == 4                 # ὁ, Ἀβραάμ, βίβλος, δέ
    assert f["nouns"] == 2                       # Ἀβραάμ, βίβλος
    assert f["not_nouns"] == 2                   # ὁ, δέ
    assert f["proper"] == 1                      # Ἀβραάμ (capitalized lemma)
    assert f["common"] == 1                      # βίβλος
    assert f["more_than_once"] == 1              # only ὁ
    assert f["once"] == 3
    assert f["more_than_one_form"] == 1          # only ὁ (ο, τον)
    assert f["one_form"] == 3


def test_vocab_features_letters_and_initials() -> None:
    # two short lemmas; letters and gematria computed on the normalized lemma
    f = vocab_features([("ἐκ", "preposition", "εκ"), ("γῆ", "noun", "γη")])
    assert f["letters"] == 4                     # εκ (2) + γη (2)
    assert f["vowels"] == 2                       # ε, η
    assert f["consonants"] == 2                   # κ, γ
    assert f["vowel_initial"] == 1               # εκ starts with ε
    assert f["consonant_initial"] == 1           # γη starts with γ


def test_male_ancestors_excludes_documented_non_ancestors() -> None:
    # proper names minus the documented non-ancestors; women and subjects drop out
    entries = [
        ("Ἀβραάμ", "noun", "αβρααμ"), ("Ἰσαάκ", "noun", "ισαακ"),
        ("Θαμάρ", "noun", "θαμαρ"), ("Ἰησοῦς", "noun", "ιησου"),
    ]
    f = vocab_features(entries)
    assert f["proper"] == 4
    assert f["male_ancestors"] == 2              # Abraham, Isaac; Tamar and Jesus excluded
    assert "Θαμάρ" in NON_ANCESTOR_PROPER and "Ζάρα" in NON_ANCESTOR_PROPER
