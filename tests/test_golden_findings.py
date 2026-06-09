"""Golden-findings integration suite for the textual-witness analysis family.

These tests run each analysis script end to end against the real local corpora
and assert the headline numbers in the manifests it writes. The findings are
the product of these scripts; until now they were verified by hand whenever
something changed. This locks them: a refactor, a corpus swap, or an edit that
silently flips Genesis 1:1 off 7/7 or moves Panin's 49 fails the suite.

Marked integration + requires_corpus, so a fresh clone without data/ skips
them; the full local `make cert` runs them. Each test regenerates its own
reports/<tool>/ directory, which is what the scripts do anyway.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import pytest

from scripts import (
    analyze_dss_witness_cases,
    analyze_heptadic_claims_catalog,
    analyze_heptadic_counts,
    analyze_heptadic_structure,
    analyze_panin_claims,
    analyze_panin_morphology,
    analyze_panin_passages,
    analyze_pos_heptads,
)

pytestmark = [pytest.mark.integration, pytest.mark.requires_corpus]


@lru_cache(maxsize=None)
def run_tool(module_name: str) -> dict:
    """Run a script's main() once per process and return its manifest."""
    module = {
        "heptadic_counts": analyze_heptadic_counts,
        "panin_claims": analyze_panin_claims,
        "panin_passages": analyze_panin_passages,
        "panin_morphology": analyze_panin_morphology,
        "dss_witness_cases": analyze_dss_witness_cases,
        "heptadic_structure": analyze_heptadic_structure,
        "heptadic_claims_catalog": analyze_heptadic_claims_catalog,
        "pos_heptads": analyze_pos_heptads,
    }[module_name]
    assert module.main() == 0
    return json.loads(
        Path(f"reports/{module_name}/manifest.json").read_text(encoding="utf-8")
    )


def test_genesis_and_base_rates_hold() -> None:
    m = run_tool("heptadic_counts")
    # Genesis 1:1's sevenfold structure confirms in full; Matthew 1's running
    # text stays non-sevenfold across the five editions.
    assert m["genesis_1_1_claims_confirmed"] == "7/7"
    assert m["matthew_1_counts_sevenfold"] == "3/50"
    # whole-corpus divisibility-by-seven sits at the one-in-seven chance rate
    assert m["base_rate_hebrew"] == {
        "verses": 23213, "words_pct": 0.1654, "letters_pct": 0.145, "both_pct": 0.026,
    }
    assert m["base_rate_greek"] == {
        "verses": 7939, "words_pct": 0.1396, "letters_pct": 0.1372, "both_pct": 0.0198,
    }


def test_panin_lemma_reconciliation_and_neutral_panel_hold() -> None:
    m = run_tool("panin_claims")
    editions = m["matthew_editions"]
    # Panin's 49 is the exact lemma count of the critical-text family; the
    # TR/Byzantine genealogy gives 50, so the count is real but text-bound.
    for name in ("WH", "SR", "SBLGNT"):
        assert editions[name]["lemmas"] == 49 and editions[name]["lemmas_match_panin_49"]
    for name in ("TR", "Byzantine"):
        assert editions[name]["lemmas"] == 50 and not editions[name]["lemmas_match_panin_49"]
    panel = m["neutral_panel"]
    assert panel["hebrew_mean_hits"] == 1.748
    assert panel["greek_mean_hits"] == 1.675
    assert panel["genesis_1_1_hits"] == 4
    assert panel["hebrew_verses_tying_or_beating_genesis_1_1"] == 2936
    assert m["gematria_checkpoints"] == {
        "elohim_86": 86, "yhwh_26": 26, "iesous_888": 888, "genesis_1_1_total_2701": 2701,
    }


def test_removal_does_not_break_the_sevens() -> None:
    m = run_tool("panin_passages")
    # the load-bearing claim inverts: removing disputed passages gains sevens
    assert m["removal_div7_gained_by_removal"] == 3
    assert m["removal_div7_lost_by_removal"] == 0
    # Panin's running-word count for the birth narrative is exact on WH
    birth_tokens = [r for r in m["part_a_further_counts"]
                    if r["passage"] == "Matthew 1:18-25 birth" and r["metric"] == "tokens"]
    assert birth_tokens and birth_tokens[0]["computed"] == 161 and birth_tokens[0]["matches"]


def test_panin_morphology_ledger_holds() -> None:
    m = run_tool("panin_morphology")
    assert m["matthew_1_1_11_features_exact"] == "13/15"
    vocab = {r["passage"]: r["delta"] for r in m["passage_vocabularies"]}
    assert vocab["Matthew 1:18-25 birth"] == 0      # 77 exactly
    assert vocab["Matthew 2 childhood"] == 0        # 161 exactly
    gem = m["genealogy_vocabulary_gematria"]
    # the famous gematria flourish is text-bound: a heptad on WH, not on SBLGNT
    assert gem["panin_wh_divisible_by_7"] is True
    assert gem["sblgnt_morphgnt"] == 42452 and gem["sblgnt_divisible_by_7"] is False


def test_dss_witness_holds() -> None:
    m = run_tool("dss_witness_cases")
    assert m["cases"] == 7
    assert m["scroll_confirmed"] == 7
    assert m["dss_sides_with"] == {"MT": 1, "LXX": 6}


def test_heptadic_structure_concentration_holds() -> None:
    m = run_tool("heptadic_structure")
    # the seven word-family concentrates where the theology of seven lives
    assert m["greek_seven_total"] == 108
    assert m["greek_lead_book"] == {"book": "Rev", "count": 60, "per_1000": 6.1}
    assert m["hebrew_seven_total"] == 610
    assert m["revelation_series_total"] == 51
    assert m["revelation_series_distinct"] == 18


def test_structural_claims_catalog_holds() -> None:
    m = run_tool("heptadic_claims_catalog")
    # Genesis tov 7, Elohim 35, Jericho 14, seven woes, seven beatitudes
    assert m["counted_confirmed"] == "5/5"


def test_pos_rates_straddle_chance_and_lists_are_plural() -> None:
    m = run_tool("pos_heptads")
    low, high = m["chapter_rate_range"]
    assert low < 1 / 7 < high            # chapter-level POS heptads sit at chance
    assert m["enumerated_list_counts"] == [5, 6, 7, 9, 10, 12]
