"""Toy-corpus tests for the cross-tradition proximity preservation test.

These certify the mechanics of the Stage-1 fix that recovers preserved codes
the strict equivalent-offset test rejects after upstream word-length deltas.
No real corpora needed.
"""

from __future__ import annotations

from array import array

from els.corpus import Corpus, VerseSpan
from els.critical import verse_span_preserved
from scripts.analyze_critical_omission_breaks_cross_tradition import (
    classify_cross_proximity,
    equivalent_status,
    proximity_status,
)


def _corpus(verses: list[tuple[str, str]]) -> Corpus:
    """Build a toy corpus from a list of (ref, text)."""
    text_parts: list[str] = []
    spans: list[VerseSpan] = []
    p2v: list[int] = []
    offset = 0
    for index, (ref, vtext) in enumerate(verses):
        spans.append(
            VerseSpan("S", ref, "X", "1", str(index + 1), vtext, offset, offset + len(vtext) - 1, len(vtext))
        )
        p2v.extend([index] * len(vtext))
        text_parts.append(vtext)
        offset += len(vtext)
    text = "".join(text_parts)
    return Corpus(
        name="toy",
        language="greek",
        keep_hebrew_final_forms=False,
        text=text,
        verses=tuple(spans),
        position_to_verse=array("i", p2v),
    )


def _index(corpus: Corpus) -> dict[str, int]:
    return {v.ref: i for i, v in enumerate(corpus.verses)}


def _row(query: str, *, skip: int, start: int, end: int, start_ref="v1", end_ref="v1") -> dict[str, str]:
    return {
        "start_ref": start_ref,
        "end_ref": end_ref,
        "start_offset": str(start),
        "end_offset": str(end),
        "skip": str(skip),
        "normalized_term": query,
    }


def test_movable_nu_recovered_by_proximity_but_missed_by_strict() -> None:
    # TR verse "aXcYe": query "ace" at skip 2 spells over offsets 0,2,4.
    tr = _corpus([("v1", "aXcYe")])
    # other gained a leading letter ("ZaXcYe"); the same ELS is still present at
    # skip 2 but shifted to offsets 1,3,5. Strict anchors at the verse start and
    # reads Z,X,Y -> miss. Proximity scans the window and finds it.
    other = _corpus([("v1", "ZaXcYe")])
    row = _row("ace", skip=2, start=0, end=4)

    strict = equivalent_status(row, tr, _index_spanmap(tr), other, _index_spanmap(other))
    assert strict == "not_preserved_equivalent_offsets"

    assert verse_span_preserved(other, _index(other), "v1", "v1", "ace", 2, window_verses=2) is True
    assert proximity_status(row, _index_spanmap(tr), other, _index(other), 2) == "preserved_within_verse_span"


def test_strict_preserved_implies_proximity_preserved() -> None:
    # Identical corpora: strict preserves, so proximity must too (subset).
    tr = _corpus([("v1", "abcde")])
    other = _corpus([("v1", "abcde")])
    row = _row("ace", skip=2, start=0, end=4)

    assert equivalent_status(row, tr, _index_spanmap(tr), other, _index_spanmap(other)) == "preserved_equivalent_offsets"
    assert verse_span_preserved(other, _index(other), "v1", "v1", "ace", 2, window_verses=0) is True


def test_distant_match_outside_window_not_preserved() -> None:
    # The query exists only far outside the hit's verse window -> not preserved.
    other = _corpus([("v1", "ace"), ("v2", "qqq"), ("v3", "qqq"), ("v4", "qqq"), ("v5", "ace")])
    # Hit anchored at v1; the second "ace" sits at v5, beyond window_verses=2.
    assert verse_span_preserved(other, _index(other), "v1", "v1", "ace", 1, window_verses=2) is True  # local copy
    # Remove the local copy: only the distant one remains.
    other2 = _corpus([("v1", "zzz"), ("v2", "qqq"), ("v3", "qqq"), ("v4", "qqq"), ("v5", "ace")])
    assert verse_span_preserved(other2, _index(other2), "v1", "v1", "ace", 1, window_verses=2) is False


def test_missing_ref_reports_ref_missing() -> None:
    tr = _corpus([("v1", "abcde")])
    other = _corpus([("v1", "abcde")])
    row = _row("ace", skip=2, start=0, end=4, start_ref="vX")
    assert proximity_status(row, _index_spanmap(tr), other, _index(other), 2) == "tr_ref_missing"

    row2 = _row("ace", skip=2, start=0, end=4)  # present in tr, absent in other
    other_missing = _corpus([("vZ", "abcde")])
    assert proximity_status(row2, _index_spanmap(tr), other_missing, _index(other_missing), 2) == "ref_missing"


def test_zero_skip_and_empty_query_are_not_preserved() -> None:
    other = _corpus([("v1", "abcde")])
    assert verse_span_preserved(other, _index(other), "v1", "v1", "ace", 0, window_verses=2) is False
    assert verse_span_preserved(other, _index(other), "v1", "v1", "", 2, window_verses=2) is False


def test_classify_cross_proximity_combines_sources() -> None:
    P = "preserved_within_verse_span"
    N = "not_preserved_within_window"
    assert classify_cross_proximity(P, P) == "preserved_by_byz_and_tcg"
    assert classify_cross_proximity(P, N) == "preserved_by_byz"
    assert classify_cross_proximity(N, P) == "preserved_by_tcg"
    assert classify_cross_proximity(N, N) == "tr_specific_within_window"


def _index_spanmap(corpus: Corpus) -> dict[str, VerseSpan]:
    return {v.ref: v for v in corpus.verses}
