"""Tests for the NT-LXX quotation overlap helpers."""

from __future__ import annotations

from scripts.analyze_nt_lxx_quotation_overlap import (
    greek_tokens,
    longest_common_run,
    lookup,
    ordered_recall,
)


def test_longest_common_run_finds_verbatim_phrase() -> None:
    # a 4-token verbatim LXX phrase embedded in a much longer NT verse
    lxx = "προσκυνησατωσαν αυτω παντες αγγελοι θεου και"
    nt = "οταν δε παλιν εισαγαγη προσκυνησατωσαν αυτω παντες αγγελοι θεου"
    assert longest_common_run(nt, lxx) >= 4
    # disjoint texts -> no run
    assert longest_common_run("ἐκάλεσα τὸν υἱόν", "ορθρου απερριφησαν") == 0


def test_greek_tokens_normalizes() -> None:
    assert greek_tokens("ἡ παρθένος") == ["η", "παρθενοσ"]


def test_ordered_recall_full_when_lxx_embedded_in_nt_framing() -> None:
    # the whole LXX verse appears inside the NT verse with framing words around it
    lxx = "ἰδοὺ ἡ παρθένος ἐν γαστρὶ ἕξει"
    nt = "λέγοντος ἰδοὺ ἡ παρθένος ἐν γαστρὶ ἕξει καὶ τέξεται"
    assert ordered_recall(nt, lxx) == 1.0


def test_ordered_recall_low_when_disjoint() -> None:
    assert ordered_recall("ἐκάλεσα τὸν υἱόν μου", "ορθρου απερριφησαν βασιλευς") == 0.0


def test_ordered_recall_empty_lxx() -> None:
    assert ordered_recall("any text", "") == 0.0


def test_lookup_uppercases_book() -> None:
    vmap = {("PSA", "109", "1"): "ειπεν ο κυριος"}
    assert lookup(vmap, ("PSA", "109", "1")) == "ειπεν ο κυριος"
    assert lookup(vmap, ("Psa", "109", "1")) == "ειπεν ο κυριος"
    assert lookup(vmap, ("PSA", "110", "1")) == ""
