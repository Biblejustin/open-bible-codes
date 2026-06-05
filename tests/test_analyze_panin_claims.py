"""Tests for the broad Panin-claims helpers."""

from __future__ import annotations

from scripts.analyze_panin_claims import (
    GRK_ISOPSEPHY,
    HEB_GEMATRIA,
    PANIN_MATTHEW,
    gematria,
    greek_genealogy_panel,
    hebrew_words,
    heptad_hits,
    lemma_count,
    panel_features,
)


def test_gematria_known_values() -> None:
    # famous anchors; final mem in Elohim must map to 40
    assert gematria("אלהים", HEB_GEMATRIA) == 86
    assert gematria("יהוה", HEB_GEMATRIA) == 26
    # Greek isopsephy of Iesous (normalized, final sigma already folded) is 888
    assert gematria("ιησουσ", GRK_ISOPSEPHY) == 888
    # unmapped characters contribute nothing
    assert gematria("x?", HEB_GEMATRIA) == 0


def test_hebrew_words_strips_to_consonants() -> None:
    # the morpheme slash, points, and cantillation drop; tokens with no letters vanish
    assert hebrew_words("בְּ/רֵאשִׁ֖ית בָּרָ֣א") == ["בראשית", "ברא"]


def test_greek_genealogy_panel_counts_vocabulary() -> None:
    # vocabulary is distinct words; frequencies split once vs more-than-once
    panel = greek_genealogy_panel(["ο", "ο", "θεοσ", "ην"])
    assert panel["vocabulary"] == 3
    assert panel["occurs_more_than_once"] == 1   # only "ο"
    assert panel["occurs_once"] == 2             # "θεοσ", "ην"
    assert panel["letters"] == 1 + 4 + 2         # over distinct words
    assert panel["vowel_initial"] == 2           # "ο", "ην"
    assert panel["consonant_initial"] == 1       # "θεοσ"


def test_panin_targets_are_all_heptads() -> None:
    # every published Panin count is an exact multiple of seven, by construction
    assert all(v % 7 == 0 for v in PANIN_MATTHEW.values())


def test_panel_features_shape_and_values() -> None:
    feats = panel_features(["αβ", "αβ", "γ"], GRK_ISOPSEPHY)
    assert feats["words"] == 3
    assert feats["letters"] == 5
    assert feats["vocabulary"] == 2
    assert feats["words_occurring_once"] == 1     # only "γ"
    assert feats["longest_word_letters"] == 2
    assert feats["first_word_letters"] == 2
    assert feats["last_word_letters"] == 1
    # gematria_total = (1+2) + (1+2) + 3 = 9
    assert feats["gematria_total"] == 9


def test_panel_features_empty() -> None:
    assert panel_features([], HEB_GEMATRIA) == {}
    assert panel_features(["", ""], HEB_GEMATRIA) == {}


def test_heptad_hits_counts_nonzero_multiples_of_seven() -> None:
    assert heptad_hits({"a": 7, "b": 3, "c": 14, "d": 0, "e": 49}) == 3
    assert heptad_hits({}) == 0


def test_lemma_count_collapses_article_and_name_cases() -> None:
    # article forms count as one word; a name in two cases counts as one word
    forms = {"ο", "τον", "του",        # article -> 1 lemma
             "ιουδασ", "ιουδαν",        # Judah nom/acc -> 1 lemma
             "δε", "εγεννησεν"}         # two more, distinct
    assert lemma_count(forms) == 4
    # the Solomon case the symmetric stem rule must catch: solomon / solomona
    assert lemma_count({"σολομων", "σολομωνα"}) == 1
    # no article present, two unrelated words stay two
    assert lemma_count({"δε", "και"}) == 2
