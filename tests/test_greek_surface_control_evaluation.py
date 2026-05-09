from scripts import analyze_greek_surface_control_evaluation as evaluation


def cohort_row(
    term_id: str,
    term: str,
    *,
    all_source: str,
    multi: str = "0",
    unique: str = "0",
    hits: str = "0",
) -> dict[str, str]:
    return {
        "term_id": term_id,
        "concept": "Concept",
        "category": "category",
        "term": term,
        "normalized_term": term,
        "normalized_length": str(len(term)),
        "total_exact_center_hits": hits,
        "unique_patterns": unique,
        "all_source_patterns": all_source,
        "multi_source_patterns": multi,
        "source_specific_patterns": "0",
        "length_cohort_terms": "10",
        "length_cohort_all_source_rank": "1",
        "selected": "False",
        "read": "",
    }


def matched(target: str, control: str) -> dict[str, str]:
    return {
        "target_term_id": target,
        "target_concept": "Target",
        "target_normalized_term": "target",
        "control_term_id": control,
        "control_concept": "Control",
        "control_normalized_term": "control",
        "normalized_length": "5",
        "target_surface_vector": "1/1/1/1",
        "control_surface_vector": "1/1/1/1",
        "target_surface_verse_sum": "4",
        "control_surface_verse_sum": "4",
        "surface_sum_delta": "0",
        "surface_vector_l1_delta": "0",
        "read": "",
    }


def test_evaluate_controls_computes_add_one_tail_probability() -> None:
    cohort = {
        "target": cohort_row("target", "ισαακ", all_source="1", multi="2", unique="4", hits="10"),
        "c1": cohort_row("c1", "ηλιασ", all_source="0"),
        "c2": cohort_row("c2", "χαραν", all_source="1"),
    }

    rows, details = evaluation.evaluate_controls(
        cohort,
        [matched("target", "c1"), matched("target", "c2")],
    )
    evaluation.annotate_q_values(rows)

    assert rows[0]["controls_ge_observed_all_source"] == "1"
    assert rows[0]["all_source_p_ge"] == "0.666667"
    assert rows[0]["all_source_q_value"] == "0.666667"
    assert len(details) == 2


def test_read_cohort_rows_accepts_separate_control_cohort(tmp_path) -> None:
    target_path = tmp_path / "targets.csv"
    control_path = tmp_path / "controls.csv"
    evaluation.write_rows(
        target_path,
        list(cohort_row("target", "αμην", all_source="2")),
        [cohort_row("target", "αμην", all_source="2")],
    )
    evaluation.write_rows(
        control_path,
        list(cohort_row("control", "λογοσ", all_source="0")),
        [cohort_row("control", "λογοσ", all_source="0")],
    )

    rows = evaluation.read_cohort_rows(target_path, [control_path])

    assert set(rows) == {"target", "control"}
    assert rows["target"]["all_source_patterns"] == "2"
    assert rows["control"]["all_source_patterns"] == "0"


def test_read_label_identifies_small_pool_limit() -> None:
    assert (
        evaluation.read_label(1 / 11, controls_ge=0, control_count=10)
        == "target exceeds matched controls, but small control pool is not significant"
    )


def test_markdown_reports_dynamic_control_counts(tmp_path) -> None:
    path = tmp_path / "report.md"

    evaluation.write_markdown(
        path,
        [
            {
                "matched_controls": "30",
                "target_normalized_term": "ανομια",
                "target_concept": "Lawlessness",
                "observed_all_source_patterns": "1",
                "controls_ge_observed_all_source": "0",
                "all_source_p_ge": "0.032258",
                "all_source_q_value": "0.032258",
                "read": "read",
            },
            {
                "matched_controls": "33",
                "target_normalized_term": "ισαακ",
                "target_concept": "Isaac",
                "observed_all_source_patterns": "1",
                "controls_ge_observed_all_source": "0",
                "all_source_p_ge": "0.029412",
                "all_source_q_value": "0.032258",
                "read": "read",
            },
        ],
        "Dynamic Title",
    )

    text = path.read_text(encoding="utf-8")
    assert text.startswith("# Dynamic Title")
    assert "range from 30 to 33" in text
    assert "0.029412" in text
    assert "0.032258" in text


def test_control_read_lines_reports_full_target_overlap() -> None:
    assert "Matched controls overlap every target" in " ".join(
        evaluation.control_read_lines(
            [
                {
                    "controls_ge_observed_all_source": "7",
                    "all_source_q_value": "0.278607",
                }
            ]
        )
    )
