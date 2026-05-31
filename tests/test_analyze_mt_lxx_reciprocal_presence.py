from __future__ import annotations

from scripts.analyze_hebrew_hit_version_presence import TermRow
from scripts.analyze_mt_lxx_reciprocal_presence import (
    CorpusRefs,
    HitView,
    counterpart_status,
    reciprocal_summary_rows,
)


def hit(side: str, concept: str, ref: str, term_id: str | None = None) -> HitView:
    return HitView(
        side=side,
        concept=concept,
        term_id=term_id or f"{concept.lower()}_{side.lower()}",
        category="test",
        term=concept,
        normalized_term=concept.lower(),
        corpus=side,
        skip=7,
        direction="forward",
        start_ref=ref,
        center_ref=ref,
        end_ref=ref,
    )


def term(term_id: str, concept: str) -> TermRow:
    return TermRow(term_id=term_id, concept=concept, category="test", term=concept)


def refs(*values: str) -> CorpusRefs:
    chapters = frozenset(value.rsplit(":", 1)[0] for value in values)
    return CorpusRefs(verse_refs=frozenset(values), chapter_refs=chapters)


def test_reciprocal_summary_marks_common_verse() -> None:
    mt_refs = refs("Gen 1:1", "Gen 1:2")
    lxx_refs = refs("Gen 1:1", "Gen 1:2")
    rows = reciprocal_summary_rows(
        [term("light_h", "Light")],
        [term("light_g", "Light")],
        [hit("MT", "Light", "Gen 1:1")],
        [hit("LXX", "Light", "Gen 1:1")],
        mt_refs,
        lxx_refs,
    )

    assert rows[0]["presence_class"] == "mt_lxx_common_verse"
    assert rows[0]["common_center_refs"] == 1


def test_reciprocal_summary_marks_common_chapter_when_verse_differs() -> None:
    mt_refs = refs("Gen 1:1", "Gen 1:2")
    lxx_refs = refs("Gen 1:1", "Gen 1:2")
    rows = reciprocal_summary_rows(
        [term("light_h", "Light")],
        [term("light_g", "Light")],
        [hit("MT", "Light", "Gen 1:1")],
        [hit("LXX", "Light", "Gen 1:2")],
        mt_refs,
        lxx_refs,
    )

    assert rows[0]["presence_class"] == "mt_lxx_common_chapter"
    assert rows[0]["common_chapters"] == 1


def test_reciprocal_summary_marks_mt_only() -> None:
    mt_refs = refs("Gen 1:1")
    lxx_refs = refs("Gen 1:1")
    rows = reciprocal_summary_rows(
        [term("light_h", "Light")],
        [term("light_g", "Light")],
        [hit("MT", "Light", "Gen 1:1")],
        [],
        mt_refs,
        lxx_refs,
    )

    assert rows[0]["presence_class"] == "mt_only_lxx_absent"
    assert rows[0]["mt_only_aligned_refs"] == 1


def test_counterpart_status_marks_unaligned_verse_when_chapter_exists() -> None:
    status, scope = counterpart_status(
        hit("MT", "Light", "Gen 1:3"),
        [],
        refs("Gen 1:1", "Gen 1:2"),
    )

    assert status == "alignment_broken_verse"
    assert scope == "chapter_exists"


def test_counterpart_status_marks_aligned_absence() -> None:
    status, scope = counterpart_status(
        hit("LXX", "Light", "Gen 1:1"),
        [],
        refs("Gen 1:1"),
    )

    assert status == "lxx_only_mt_absent"
    assert scope == "aligned_ref"
