from scripts import analyze_greek_expanded_surface_queue as queue


def row(corpus: str, term_id: str = "t1", center_ref: str = "JHN 1:1") -> dict[str, str]:
    return {
        "corpus": corpus,
        "term_id": term_id,
        "concept": "Concept",
        "category": "category",
        "term": "λογος",
        "normalized_term": "λογοσ",
        "skip": "5",
        "direction": "forward",
        "start_ref": "JHN 1:1",
        "center_ref": center_ref,
        "end_ref": "JHN 1:1",
        "center_word": "λόγος",
        "start_offset": "1",
        "center_offset": "2",
        "end_offset": "3",
    }


def test_surface_pattern_rows_groups_canonical_refs_across_sources() -> None:
    rows = [row("TR_NT", center_ref="JHN 1:1"), row("SBLGNT", center_ref="John 1:1")]

    patterns = queue.surface_pattern_rows(rows, ("TR_NT", "SBLGNT"))

    assert len(patterns) == 1
    assert patterns[0]["presence_scope"] == "all_sources"
    assert patterns[0]["present_corpora"] == "TR_NT,SBLGNT"


def test_term_summary_counts_surface_patterns() -> None:
    rows = [row("TR_NT"), row("SBLGNT"), row("TR_NT", term_id="t2")]
    patterns = queue.surface_pattern_rows(rows, ("TR_NT", "SBLGNT"))

    summary = queue.term_summary_rows(patterns, rows)

    by_term = {item["term_id"]: item for item in summary}
    assert by_term["t1"]["all_source_patterns"] == "1"
    assert by_term["t2"]["source_specific_patterns"] == "1"


def test_read_label_marks_related_byzantine_pair() -> None:
    assert (
        queue.read_label(["BYZ_NT", "TCG_NT"], ("TR_NT", "BYZ_NT", "TCG_NT", "SBLGNT"))
        == "surface exact-center pattern in related Byzantine-source pair"
    )
