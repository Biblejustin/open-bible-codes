from collections import Counter

from scripts import analyze_greek_surface_control_pool as pool


def freq(
    term_id: str,
    term: str,
    *,
    length: str,
    vector: tuple[int, int, int, int],
    selected: str = "False",
    concept: str = "Concept",
) -> dict[str, str]:
    return {
        "term_id": term_id,
        "concept": concept,
        "category": "category",
        "term": term,
        "normalized_term": term,
        "normalized_length": length,
        "selected_target": selected,
        "surface_verses_tr_nt": str(vector[0]),
        "surface_verses_byz_nt": str(vector[1]),
        "surface_verses_tcg_nt": str(vector[2]),
        "surface_verses_sblgnt": str(vector[3]),
        "surface_verse_sum": str(sum(vector)),
        "surface_verse_min": str(min(vector)),
        "surface_verse_max": str(max(vector)),
        "all_source_surface_present": str(all(value > 0 for value in vector)),
    }


def test_frequency_row_marks_all_source_surface_presence() -> None:
    row = pool.frequency_row(
        {
            "term_id": "t1",
            "concept": "Concept",
            "category": "category",
            "term": "λόγος",
        },
        Counter({"TR_NT": 2, "BYZ_NT": 2, "TCG_NT": 1, "SBLGNT": 2}),
        {"t1"},
    )

    assert row["normalized_term"] == "λογοσ"
    assert row["surface_verse_sum"] == "7"
    assert row["all_source_surface_present"] == "True"
    assert row["selected_target"] == "True"


def test_matched_candidates_require_same_length_and_all_source_presence() -> None:
    target = freq("target", "ανομια", length="6", vector=(12, 12, 12, 13), selected="True")
    close = freq("close", "σκοτος", length="6", vector=(13, 13, 13, 13))
    wrong_length = freq("wrong", "νομος", length="5", vector=(45, 45, 45, 45))
    missing_source = freq("missing", "θλιψις", length="6", vector=(7, 0, 7, 7))
    selected_peer = freq("selected_peer", "μυστηρ", length="6", vector=(12, 12, 12, 12), selected="True")

    candidates = pool.matched_candidates(
        target,
        [target, wrong_length, missing_source, selected_peer, close],
    )

    assert [row["term_id"] for row in candidates] == ["close"]


def test_matched_row_reports_vector_deltas() -> None:
    target = freq("target", "ισαακ", length="5", vector=(18, 18, 18, 18))
    control = freq("control", "ηλιας", length="5", vector=(17, 17, 17, 16))

    row = pool.matched_row(target, control)

    assert row["target_surface_vector"] == "18/18/18/18"
    assert row["control_surface_vector"] == "17/17/17/16"
    assert row["surface_sum_delta"] == "5"
    assert row["surface_vector_l1_delta"] == "5"


def test_markdown_uses_configured_title(tmp_path) -> None:
    path = tmp_path / "pool.md"

    pool.write_markdown(
        path,
        [
            freq(
                "target",
                "ισαακ",
                length="5",
                vector=(18, 18, 18, 18),
                selected="True",
            )
        ],
        [],
        type("Args", (), {"title": "Custom Pool", "terms": "terms.csv", "selected": "selected.csv", "top_controls": 999})(),
    )

    assert path.read_text(encoding="utf-8").startswith("# Custom Pool")
