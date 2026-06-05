"""Tests for the heptadic-claims-catalog helpers."""

from __future__ import annotations

from scripts.analyze_heptadic_claims_catalog import count_in_spans, ego_eimi_total


def test_count_in_spans_limits_to_passage_and_lemmas() -> None:
    rows = [
        ("Gen", "1", "4", "2896"), ("Gen", "1", "10", "2896"),
        ("Gen", "1", "4", "430"),                 # different lemma, not counted
        ("Gen", "2", "9", "2896"),                # outside the span, not counted
        ("Exod", "1", "4", "2896"),               # different book
    ]
    # count lemma 2896 in Genesis 1
    assert count_in_spans(rows, "Gen", [(1, range(1, 32))], {"2896"}) == 2
    # multi-span and lemma-set
    assert count_in_spans(rows, "Gen", [(1, range(1, 32)), (2, range(1, 10))], {"2896"}) == 3
    # empty when nothing matches
    assert count_in_spans(rows, "Gen", [(1, range(1, 32))], {"9999"}) == 0


def test_ego_eimi_total_counts_adjacent_pairs_in_john() -> None:
    rows = [
        ("John", "6", "35", "ἐγώ"), ("John", "6", "35", "εἰμί"),       # one I-am
        ("John", "8", "12", "ἐγώ"), ("John", "8", "12", "εἰμί"),       # another
        ("John", "1", "1", "ἐγώ"), ("John", "1", "1", "λόγος"),        # ἐγώ not followed by εἰμί
        ("Matt", "1", "1", "ἐγώ"), ("Matt", "1", "1", "εἰμί"),         # not John
    ]
    assert ego_eimi_total(rows) == 2
