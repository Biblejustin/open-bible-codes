"""Toy-corpus tests for the cross-tradition proximity + shared-omission logic.

These certify the mechanics of the Stage-1 fix (recovering preserved codes the
strict equivalent-offset test rejects after word-length deltas) and the
shared-omission classification (an endpoint verse the comparison tradition
omits). No real corpora needed.
"""

from __future__ import annotations

from array import array

from els.corpus import Corpus, VerseSpan
from els.critical import ref_absence_kind, verse_span_preserved
from scripts.analyze_critical_omission_breaks_cross_tradition import (
    classify_cross_proximity,
    equivalent_status,
    proximity_status,
)


def _corpus(verses: list[tuple[str, str]]) -> Corpus:
    """Build a toy corpus from a list of (ref, text). A ref of the form
    'Book C:V' is parsed into book/chapter/verse; otherwise book='X'."""
    text_parts: list[str] = []
    spans: list[VerseSpan] = []
    p2v: list[int] = []
    offset = 0
    for index, (ref, vtext) in enumerate(verses):
        book, chapter, verse = _parse_ref(ref, index)
        spans.append(VerseSpan("S", ref, book, chapter, verse, vtext, offset, offset + len(vtext) - 1, len(vtext)))
        p2v.extend([index] * len(vtext))
        text_parts.append(vtext)
        offset += len(vtext)
    return Corpus(
        name="toy",
        language="greek",
        keep_hebrew_final_forms=False,
        text="".join(text_parts),
        verses=tuple(spans),
        position_to_verse=array("i", p2v),
    )


def _parse_ref(ref: str, index: int) -> tuple[str, str, str]:
    if " " in ref and ":" in ref.rsplit(" ", 1)[1]:
        head, tail = ref.rsplit(" ", 1)
        chapter, verse = tail.split(":", 1)
        return head, chapter, verse
    return "X", "1", str(index + 1)


def _index(corpus: Corpus) -> dict[str, int]:
    return {v.ref: i for i, v in enumerate(corpus.verses)}


def _bc(corpus: Corpus) -> set[tuple[str, str]]:
    return {(v.book, v.chapter) for v in corpus.verses}


def _spanmap(corpus: Corpus) -> dict[str, VerseSpan]:
    return {v.ref: v for v in corpus.verses}


def _row(query: str, *, skip: int, start: int, end: int, start_ref="v1", end_ref="v1") -> dict[str, str]:
    return {
        "start_ref": start_ref,
        "end_ref": end_ref,
        "start_offset": str(start),
        "end_offset": str(end),
        "skip": str(skip),
        "normalized_term": query,
    }


# --- verse_span_preserved (Stage 1 mechanic) ---------------------------------


def test_movable_nu_recovered_by_proximity_but_missed_by_strict() -> None:
    tr = _corpus([("v1", "aXcYe")])
    other = _corpus([("v1", "ZaXcYe")])  # leading insert shifts the ELS to offsets 1,3,5
    row = _row("ace", skip=2, start=0, end=4)

    assert equivalent_status(row, tr, _spanmap(tr), other, _spanmap(other)) == "not_preserved_equivalent_offsets"
    assert verse_span_preserved(other, _index(other), "v1", "v1", "ace", 2, window_verses=2) is True
    status, omitted = proximity_status(row, _spanmap(tr), other, _index(other), _bc(other), 2)
    assert status == "preserved_within_verse_span"
    assert omitted == ""


def test_strict_preserved_implies_proximity_preserved() -> None:
    other = _corpus([("v1", "abcde")])
    assert verse_span_preserved(other, _index(other), "v1", "v1", "ace", 2, window_verses=0) is True


def test_distant_match_outside_window_not_preserved() -> None:
    other = _corpus([("v1", "zzz"), ("v2", "qqq"), ("v3", "qqq"), ("v4", "qqq"), ("v5", "ace")])
    assert verse_span_preserved(other, _index(other), "v1", "v1", "ace", 1, window_verses=2) is False


def test_zero_skip_and_empty_query_not_preserved() -> None:
    other = _corpus([("v1", "abcde")])
    assert verse_span_preserved(other, _index(other), "v1", "v1", "ace", 0, window_verses=2) is False
    assert verse_span_preserved(other, _index(other), "v1", "v1", "", 2, window_verses=2) is False


# --- ref_absence_kind (shared-omission classifier) ---------------------------


def test_ref_absence_kind_distinguishes_omission_from_chapter_absence() -> None:
    present_refs = {"ACT 8:36", "ACT 8:38"}
    bc = {("ACT", "8")}
    assert ref_absence_kind("ACT 8:36", present_refs, bc) == "present"
    assert ref_absence_kind("ACT 8:37", present_refs, bc) == "omitted_verse"  # chapter present, verse skipped
    assert ref_absence_kind("ROM 16:25", present_refs, bc) == "chapter_absent"
    assert ref_absence_kind("garbage", present_refs, bc) == "unparseable"


# --- proximity_status shared-omission path -----------------------------------


def test_proximity_status_flags_shared_omission() -> None:
    # other omits ACT 8:37 (has 36 and 38, skips 37). A hit ending in 8:37 is a
    # shared omission, not a lookup miss.
    tr = _corpus([("ACT 8:36", "aa"), ("ACT 8:37", "bb"), ("ACT 8:38", "cc")])
    other = _corpus([("ACT 8:36", "aa"), ("ACT 8:38", "cc")])
    row = _row("ab", skip=1, start=0, end=2, start_ref="ACT 8:36", end_ref="ACT 8:37")

    status, omitted = proximity_status(row, _spanmap(tr), other, _index(other), _bc(other), 2)
    assert status == "omitted_in_comparison_tradition"
    assert omitted == "ACT 8:37"


def test_proximity_status_ref_missing_when_chapter_absent() -> None:
    tr = _corpus([("ROM 16:25", "aa"), ("ROM 16:26", "bb")])
    other = _corpus([("ACT 8:36", "aa")])  # no Romans at all
    row = _row("ab", skip=1, start=0, end=2, start_ref="ROM 16:25", end_ref="ROM 16:25")

    status, omitted = proximity_status(row, _spanmap(tr), other, _index(other), _bc(other), 2)
    assert status == "ref_missing"
    assert omitted == ""


def test_proximity_status_tr_ref_missing() -> None:
    tr = _corpus([("v1", "abcde")])
    other = _corpus([("v1", "abcde")])
    row = _row("ace", skip=2, start=0, end=4, start_ref="vX")
    status, _ = proximity_status(row, _spanmap(tr), other, _index(other), _bc(other), 2)
    assert status == "tr_ref_missing"


# --- classify_cross_proximity ------------------------------------------------


def test_classify_cross_proximity_combines_sources() -> None:
    P = "preserved_within_verse_span"
    N = "not_preserved_within_window"
    O = "omitted_in_comparison_tradition"
    assert classify_cross_proximity(P, P) == "preserved_by_byz_and_tcg"
    assert classify_cross_proximity(P, N) == "preserved_by_byz"
    assert classify_cross_proximity(N, P) == "preserved_by_tcg"
    assert classify_cross_proximity(O, O) == "omitted_in_byz_and_tcg"
    assert classify_cross_proximity(O, N) == "omitted_in_one_tradition"
    assert classify_cross_proximity(N, N) == "tr_specific_within_window"
