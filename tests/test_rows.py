"""Tests for the CSV schema and row-producing helpers extracted from cli."""

from __future__ import annotations

from types import SimpleNamespace

from els.rows import (
    EXTENSION_FIELDNAMES,
    EXTENSION_TOP_FIELDNAMES,
    FIELDNAMES,
    SURFACE_CONTEXT_FIELDNAMES,
    extension_rank_key,
    extension_score,
    hit_from_row,
    int_or_empty,
    int_or_zero,
    skip_plan_row,
)


def test_int_or_empty() -> None:
    assert int_or_empty("") == ""
    assert int_or_empty("7") == 7
    assert int_or_empty(7) == 7


def test_int_or_zero() -> None:
    assert int_or_zero("") == 0
    assert int_or_zero(None) == 0
    assert int_or_zero("4") == 4
    assert int_or_zero(4) == 4


def _base_row() -> dict[str, str]:
    return {
        "term": "abc",
        "normalized_term": "abc",
        "skip": "5",
        "start_offset": "2",
        "end_offset": "12",
        "span_letters": "11",
        "sequence": "abc",
        "start_ref": "Test 1:1",
        "end_ref": "Test 1:1",
        "start_source": "test",
        "end_source": "test",
        "center_offset": "",
        "center_ref": "",
        "center_source": "",
        "center_word_index": "",
        "center_word": "",
        "center_normalized_word": "",
    }


def test_hit_from_row_fills_center_offset_midpoint_when_blank() -> None:
    hit = hit_from_row(_base_row())
    assert hit.center_offset == 7  # (2 + 12) // 2
    assert hit.skip == 5
    assert hit.center_word_index == ""  # int_or_empty("") -> ""


def test_hit_from_row_uses_explicit_center_offset_and_word_index() -> None:
    row = {**_base_row(), "center_offset": "9", "center_word_index": "3"}
    hit = hit_from_row(row)
    assert hit.center_offset == 9
    assert hit.center_word_index == 3


def test_schema_composition_invariants() -> None:
    # surface and extension schemas embed the base hit schema verbatim
    for field in FIELDNAMES:
        assert field in SURFACE_CONTEXT_FIELDNAMES
        assert field in EXTENSION_FIELDNAMES
    # the "top" extension schema is the extension schema plus a score column
    assert EXTENSION_TOP_FIELDNAMES == [*EXTENSION_FIELDNAMES, "extension_score"]


def test_extension_score_returns_int() -> None:
    score = extension_score(
        {"extension_type": "term_plus_after", "match_kind": "exact", "match_count": "3"},
        4,
    )
    assert isinstance(score, int)


def test_extension_rank_key_orders_by_score_first() -> None:
    high = extension_rank_key({"extension_score": "10", "extension_length": "1"})
    low = extension_rank_key({"extension_score": "1", "extension_length": "9"})
    assert high > low  # score dominates the rank key


def test_skip_plan_row_rounds_floats() -> None:
    plan = SimpleNamespace(
        term="x",
        normalized_term="x",
        normalized_length=1,
        min_skip=1,
        max_skip_limit=10,
        selected_max_skip=5,
        direction="both",
        target_expected_hits=1 / 3,
        expected_hits=2 / 3,
        expected_at_min_skip=0.123456789,
        status="ok",
    )
    row = skip_plan_row(plan)
    assert row["target_expected_hits"] == round(1 / 3, 6)
    assert row["expected_at_min_skip"] == round(0.123456789, 6)
    assert row["status"] == "ok"
