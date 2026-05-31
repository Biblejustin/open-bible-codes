from scripts import analyze_greek_expanded_surface_triage as triage


def term(term_id: str, value: str, concept: str = "Concept") -> dict[str, str]:
    return {
        "term_id": term_id,
        "concept": concept,
        "category": "category",
        "language": "greek",
        "term": value,
        "notes": "",
    }


def summary(
    term_id: str,
    *,
    hits: str = "1",
    unique: str = "1",
    all_source: str = "0",
    multi: str = "0",
    source_only: str = "0",
) -> dict[str, str]:
    return {
        "term_id": term_id,
        "concept": "Concept",
        "category": "category",
        "term": "",
        "normalized_term": "",
        "total_exact_center_hits": hits,
        "unique_patterns": unique,
        "all_source_patterns": all_source,
        "multi_source_patterns": multi,
        "source_specific_patterns": source_only,
        "read": "",
    }


def pattern(term_id: str, normalized: str, scope: str = "all_sources") -> dict[str, str]:
    return {
        "term_id": term_id,
        "concept": "Concept",
        "category": "category",
        "term": normalized,
        "normalized_term": normalized,
        "skip": "5",
        "direction": "forward",
        "start_ref": "John 1:1",
        "center_ref": "John 1:1",
        "end_ref": "John 1:1",
        "present_corpora": "TR_NT,BYZ_NT,TCG_NT,SBLGNT",
        "absent_corpora": "",
        "presence_scope": scope,
        "hit_count": "4",
        "center_words_by_corpus": "TR_NT:λογος",
        "offsets_by_corpus": "TR_NT:1/2/3",
        "read": "",
    }


def test_build_cohort_selects_all_source_length_threshold() -> None:
    rows = triage.build_cohort_rows(
        [term("short", "αμην"), term("long", "ισαακ"), term("zero", "μαρια")],
        [
            summary("short", all_source="3"),
            summary("long", all_source="1"),
        ],
        min_length=5,
    )

    by_id = {row["term_id"]: row for row in rows}
    assert by_id["short"]["selected"] == "False"
    assert by_id["short"]["read"] == "all-source but below length threshold"
    assert by_id["long"]["selected"] == "True"
    assert by_id["zero"]["read"] == "no exact-center surface pattern"


def test_selected_pattern_rows_keep_only_all_source_long_terms() -> None:
    cohort = triage.build_cohort_rows(
        [term("short", "αμην"), term("long", "ισαακ"), term("multi", "τερασ")],
        [
            summary("short", all_source="1"),
            summary("long", all_source="1"),
            summary("multi", multi="1"),
        ],
        min_length=5,
    )

    selected = triage.selected_pattern_rows(
        [
            pattern("short", "αμην"),
            pattern("long", "ισαακ"),
            pattern("multi", "τερασ", scope="multi_source"),
        ],
        cohort,
        min_length=5,
    )

    assert [row["term_id"] for row in selected] == ["long"]
    assert selected[0]["read"] == "tight review row; needs matched surface-frequency controls"


def test_length_filter_note_distinguishes_prospective_gate_from_length4_followup() -> None:
    assert "excludes the dense length-4" in " ".join(triage.length_filter_note(5))
    assert "`αμην` (amen; English: Amen)" in " ".join(triage.length_filter_note(5))
    assert "post-discovery review material" in " ".join(triage.length_filter_note(4))


def test_ranked_cohort_counts_terms_by_length() -> None:
    rows = triage.build_cohort_rows(
        [term("a", "ισαακ"), term("b", "τερας"), term("c", "ανομια")],
        [summary("a", all_source="1", multi="3"), summary("b", all_source="1", multi="2")],
        min_length=5,
    )

    by_id = {row["term_id"]: row for row in rows}
    assert by_id["a"]["length_cohort_terms"] == "2"
    assert by_id["a"]["length_cohort_all_source_rank"] == "1"
    assert by_id["b"]["length_cohort_all_source_rank"] == "2"
    assert by_id["c"]["length_cohort_terms"] == "1"


def test_display_triage_term_adds_transliteration_and_english() -> None:
    assert (
        triage.display_triage_term({"normalized_term": "ανομια", "concept": "Lawlessness"})
        == "`ανομια` (anomia; English: Lawlessness)"
    )


def test_display_center_words_by_corpus_adds_transliteration() -> None:
    value = triage.display_center_words_by_corpus("TR_NT:οὖν; BYZ_NT:ουν")

    assert "TR_NT:`οὖν` (oun; English: therefore)" in value
    assert "BYZ_NT:`ουν` (oun; English: therefore)" in value
