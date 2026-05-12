from els.corpus import Corpus, VerseSpan
from els.match_strata import (
    BoundaryIndex,
    DirectionCounts,
    boundary_strata_for_offsets,
    build_boundary_index,
    canonical_first_keys,
    canonical_ref_sort_key,
    center_position_strata_for_ref,
    direction_counts_by_key,
    direction_counts_from_row,
    direction_strata_by_key,
    direction_stratum,
    row_identity,
)


def test_direction_counts_parse_direction_and_signed_skips() -> None:
    assert direction_counts_from_row({"direction": "forward", "skip": "7"}).forward >= 1
    assert direction_counts_from_row({"direction": "backward", "skip": "-7"}).backward >= 1
    assert direction_stratum(DirectionCounts(forward=2, backward=0)) == "forward_only"
    assert direction_stratum(DirectionCounts(forward=0, backward=2)) == "backward_only"
    assert direction_stratum(DirectionCounts(forward=1, backward=1)) == "bidirectional_present"


def test_direction_strata_group_rows_by_term_and_corpus() -> None:
    rows = [
        {"source_family": "f", "corpus": "MT", "term_id": "a", "normalized_term": "אב", "direction": "forward"},
        {"source_family": "f", "corpus": "MT", "term_id": "a", "normalized_term": "אב", "direction": "backward"},
        {"source_family": "f", "corpus": "MT", "term_id": "b", "normalized_term": "גד", "direction": "forward"},
    ]
    strata = direction_strata_by_key(rows, key_fields=("source_family", "corpus", "term_id", "normalized_term"))
    counts = direction_counts_by_key(rows, key_fields=("source_family", "corpus", "term_id", "normalized_term"))
    assert strata[("f", "MT", "a", "אב")] == "bidirectional_present"
    assert strata[("f", "MT", "b", "גד")] == "forward_only"
    assert counts[("f", "MT", "a", "אב")] == DirectionCounts(forward=1, backward=1)


def test_canonical_ref_sort_key_handles_ot_and_nt_refs() -> None:
    assert canonical_ref_sort_key("Gen 1:1") < canonical_ref_sort_key("Rev 22:21")
    assert canonical_ref_sort_key("2Kgs 10:19") < canonical_ref_sort_key("Matt 1:1")


def test_canonical_first_keys_marks_first_row_in_group() -> None:
    rows = [
        {
            "source_family": "f",
            "term_id": "x",
            "normalized_term": "x",
            "center_ref": "Rev 1:1",
            "source_record": "late",
        },
        {
            "source_family": "f",
            "term_id": "x",
            "normalized_term": "x",
            "center_ref": "Gen 1:1",
            "source_record": "early",
        },
    ]
    first = canonical_first_keys(rows, group_fields=("source_family", "term_id", "normalized_term"))
    assert row_identity(rows[1]) in first
    assert row_identity(rows[0]) not in first


def test_boundary_strata_detect_verse_chapter_book_edges() -> None:
    corpus = tiny_corpus()
    index = build_boundary_index(corpus)

    first = boundary_strata_for_offsets(start_offset=0, end_offset=2, boundary_index=index)
    assert "boundary_start_verse" in first
    assert "boundary_start_chapter" in first
    assert "boundary_start_book" in first
    assert "boundary_end_verse" in first
    assert "boundary_both_endpoints" in first

    last = boundary_strata_for_offsets(start_offset=6, end_offset=8, boundary_index=index)
    assert "boundary_end_chapter" in last
    assert "boundary_end_book" in last


def test_center_position_strata_detect_first_and_last_verses() -> None:
    index = build_boundary_index(tiny_corpus())

    first = center_position_strata_for_ref("Gen 1:1", boundary_index=index)
    assert "center_verse_first_in_chapter" in first
    assert "center_verse_first_in_book" in first

    last = center_position_strata_for_ref("Exod 1:1", boundary_index=index)
    assert "center_verse_last_in_chapter" in last
    assert "center_verse_last_in_book" in last


def tiny_corpus() -> Corpus:
    verses = (
        VerseSpan("test", "Gen 1:1", "Gen", "1", "1", "abc", 0, 3, 3),
        VerseSpan("test", "Gen 1:2", "Gen", "1", "2", "def", 3, 6, 3),
        VerseSpan("test", "Exod 1:1", "Exod", "1", "1", "ghi", 6, 9, 3),
    )
    return Corpus(
        name="tiny",
        language="english",
        keep_hebrew_final_forms=False,
        text="abcdefghi",
        verses=verses,
        position_to_verse=[0, 0, 0, 1, 1, 1, 2, 2, 2],
    )


def test_boundary_strata_tolerates_explicit_index_type() -> None:
    index = BoundaryIndex(
        verse_by_position=[0],
        verses=(VerseSpan("test", "Gen 1:1", "Gen", "1", "1", "a", 0, 1, 1),),
        first_chapter_verse_indexes=frozenset({0}),
        last_chapter_verse_indexes=frozenset({0}),
        first_book_verse_indexes=frozenset({0}),
        last_book_verse_indexes=frozenset({0}),
    )
    assert "boundary_both_endpoints" in boundary_strata_for_offsets(
        start_offset=0,
        end_offset=0,
        boundary_index=index,
    )
