from els.match_strata import build_boundary_index
from els.letter_stats import BigramProfile, LetterFrequencyProfile
from scripts.build_match_strata_index import (
    build_strata_rows,
    build_summary_rows,
    parse_offset_triplets,
    read_meaningful_constants,
)
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


def test_build_strata_rows_adds_center_position_flags() -> None:
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
                "direction": "forward",
                "occurrence_type": "centered_self_exact_word",
            }
        ],
        boundary_indexes={"TINY": build_boundary_index(tiny_corpus())},
    )

    assert "center_verse_first_in_chapter" in rows[0]["center_position_strata"]
    assert "center_verse_first_in_book" in rows[0]["extended_strata"]


def test_build_strata_rows_adds_cross_skip_pair_at_word() -> None:
    rows = build_strata_rows(
        [
            {
                "source_family": "test",
                "source_queue": "q",
                "corpus": "MT",
                "present_corpora": "MT",
                "term_id": "left",
                "normalized_term": "left",
                "center_ref": "Gen 1:1",
                "center_word": "center",
                "center_normalized_word": "center",
                "skip": "5",
                "direction": "forward",
                "occurrence_type": "hidden_path_only",
            },
            {
                "source_family": "test",
                "source_queue": "q",
                "corpus": "MT",
                "present_corpora": "MT",
                "term_id": "right",
                "normalized_term": "right",
                "center_ref": "Gen 1:1",
                "center_word": "center",
                "center_normalized_word": "center",
                "skip": "-7",
                "direction": "backward",
                "occurrence_type": "hidden_path_only",
            },
        ]
    )

    assert {row["cross_skip_pair_at_word"] for row in rows} == {"yes"}
    assert rows[0]["cross_skip_pair_terms"] == "right"
    assert rows[1]["cross_skip_pair_terms"] == "left"
    assert "cross_skip_pair_at_word" in rows[0]["extended_strata"]


def test_build_strata_rows_adds_meaningful_skip_and_gematria_flags() -> None:
    rows = build_strata_rows(
        [
            {
                "source_family": "test",
                "source_queue": "q",
                "corpus": "MT",
                "present_corpora": "MT",
                "term_id": "yhwh",
                "concept": "YHWH",
                "normalized_term": "יהוה",
                "center_ref": "Gen 1:1",
                "center_word": "center",
                "center_normalized_word": "center",
                "skip": "7;26",
                "direction": "forward",
                "occurrence_type": "hidden_path_only",
            }
        ],
        meaningful_constants={7: "Sabbath", 26: "YHWH standard Hebrew gematria"},
    )

    row = rows[0]
    assert row["skip_equals_meaningful_constant"] == "yes"
    assert row["meaningful_constant_skips"] == "7;26"
    assert row["term_gematria_value"] == "26"
    assert row["skip_equals_term_gematria"] == "yes"
    assert "skip_equals_meaningful_constant" in row["extended_strata"]
    assert "skip_equals_term_gematria" in row["extended_strata"]


def test_build_strata_rows_adds_bigram_surprise_flags() -> None:
    rows = build_strata_rows(
        [
            {
                "source_family": "test",
                "source_queue": "q",
                "corpus": "MT",
                "present_corpora": "MT",
                "term_id": "rare",
                "normalized_term": "cd",
                "center_ref": "Gen 1:1",
                "center_word": "center",
                "center_normalized_word": "center",
                "skip": "5",
                "direction": "forward",
                "occurrence_type": "hidden_path_only",
            }
        ],
        bigram_profiles={"MT": BigramProfile.from_text("ababababababababcd")},
    )

    row = rows[0]
    assert row["bigram_surprise_stratum"] == "high_bigram_surprise"
    assert row["bigram_surprise_evidence"] == "cd:1"
    assert "high_bigram_surprise" in row["extended_strata"]


def test_build_strata_rows_adds_letter_frequency_flags() -> None:
    rows = build_strata_rows(
        [
            {
                "source_family": "test",
                "source_queue": "q",
                "corpus": "MT",
                "present_corpora": "MT",
                "term_id": "rare",
                "normalized_term": "af",
                "center_ref": "Gen 1:1",
                "center_word": "center",
                "center_normalized_word": "center",
                "skip": "5",
                "direction": "forward",
                "occurrence_type": "hidden_path_only",
            }
        ],
        letter_frequency_profiles={"MT": LetterFrequencyProfile.from_text("aaaaaaaaaabcdef")},
    )

    row = rows[0]
    assert row["letter_frequency_stratum"] == "letter_frequency_anomaly"
    assert row["letter_frequency_evidence"] == "f:1"
    assert "letter_frequency_anomaly" in row["extended_strata"]


def test_read_meaningful_constants_ignores_bad_values(tmp_path) -> None:
    path = tmp_path / "constants.csv"
    path.write_text(
        "constant_id,value,label,category,notes\n"
        "seven,7,Sabbath,biblical,\n"
        "bad,not-a-number,Bad,biblical,\n",
        encoding="utf-8",
    )

    assert read_meaningful_constants(path) == {7: "Sabbath"}


def test_parse_offset_triplets_ignores_malformed_offsets() -> None:
    assert parse_offset_triplets("MT:1/2/3;bad;KJV:x/y/z") == [("MT", 1, 3)]
