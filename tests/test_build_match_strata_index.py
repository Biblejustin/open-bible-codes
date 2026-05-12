from els.match_strata import build_boundary_index
from scripts.build_match_strata_index import build_strata_rows, build_summary_rows, parse_offset_triplets
from tests.test_match_strata import tiny_corpus


def test_build_strata_rows_adds_direction_and_canonical_first_flags() -> None:
    rows = [
        {
            "occurrence_rank": "1",
            "source_family": "test",
            "source_queue": "q",
            "corpus": "MT",
            "present_corpora": "MT",
            "term_id": "term",
            "concept": "Term",
            "category": "cat",
            "normalized_term": "אבג",
            "center_ref": "Rev 1:1",
            "center_word": "late",
            "occurrence_type": "centered_self_exact_word",
            "skip": "5",
            "direction": "forward",
            "source_record": "late",
        },
        {
            "occurrence_rank": "2",
            "source_family": "test",
            "source_queue": "q",
            "corpus": "MT",
            "present_corpora": "MT",
            "term_id": "term",
            "concept": "Term",
            "category": "cat",
            "normalized_term": "אבג",
            "center_ref": "Gen 1:1",
            "center_word": "early",
            "occurrence_type": "centered_self_exact_word",
            "skip": "-7",
            "direction": "backward",
            "source_record": "early",
        },
    ]

    output = build_strata_rows(rows)

    assert {row["direction_stratum"] for row in output} == {"bidirectional_present"}
    assert output[0]["forward_direction_count"] == 1
    assert output[0]["backward_direction_count"] == 1
    assert output[0]["direction_imbalance_score"] == "0.000000"
    assert output[0]["canonical_first_centered_occurrence"] == "no"
    assert output[1]["canonical_first_centered_occurrence"] == "yes"
    assert "canonical_first_occurrence" in str(output[1]["extended_strata"])


def test_build_summary_rows_counts_each_extended_stratum() -> None:
    summary = build_summary_rows(
        [
            {"extended_strata": "centered_self_exact_word;forward_only;canonical_first_occurrence"},
            {"extended_strata": "span_relevant;forward_only"},
        ]
    )
    by_stratum = {row["stratum"]: row["rows"] for row in summary}
    assert by_stratum["forward_only"] == 2
    assert by_stratum["canonical_first_occurrence"] == 1


def test_build_strata_rows_adds_boundary_flags_from_offset_triplets() -> None:
    rows = build_strata_rows(
        [
            {
                "source_family": "test",
                "source_queue": "q",
                "corpus": "TINY",
                "present_corpora": "TINY",
                "term_id": "term",
                "normalized_term": "abc",
                "center_ref": "Gen 1:1",
                "offset_triplets": "TINY:0/1/2",
                "direction": "forward",
                "occurrence_type": "centered_self_exact_word",
            }
        ],
        boundary_indexes={"TINY": build_boundary_index(tiny_corpus())},
    )

    assert "boundary_start_verse" in rows[0]["boundary_strata"]
    assert "boundary_end_verse" in rows[0]["boundary_strata"]
    assert "boundary_both_endpoints" in rows[0]["extended_strata"]


def test_parse_offset_triplets_ignores_malformed_offsets() -> None:
    assert parse_offset_triplets("MT:1/2/3;bad;KJV:x/y/z") == [("MT", 1, 3)]
