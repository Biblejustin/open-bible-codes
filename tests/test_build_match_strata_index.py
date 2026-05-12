from scripts.build_match_strata_index import build_strata_rows, build_summary_rows


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
