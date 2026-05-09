import json

from scripts import build_greek_surface_followup_report as report


def selected(term_id: str = "target") -> dict[str, str]:
    return {
        "term_id": term_id,
        "normalized_term": "ανομια",
        "concept": "Lawlessness",
        "center_ref": "Matt 7:23",
        "skip": "20",
        "direction": "forward",
    }


def path(term_id: str, corpus: str, matches: str = "True") -> dict[str, str]:
    return {
        "term_id": term_id,
        "normalized_term": "ανομια",
        "corpus": corpus,
        "sequence": "ανομια",
        "matches_term": matches,
        "center_word": "Οὐδέποτε",
        "path_refs": "Matt 7:22; Matt 7:23",
    }


def control(term_id: str = "target", q: str = "0.032258") -> dict[str, str]:
    return {
        "target_term_id": term_id,
        "all_source_q_value": q,
        "controls_ge_observed_all_source": "0",
        "all_source_p_ge": "0.032258",
        "matched_controls": "30",
    }


def four_path_rows(term_id: str = "target") -> list[dict[str, str]]:
    return [
        path(term_id, "BYZ_NT"),
        path(term_id, "SBLGNT"),
        path(term_id, "TCG_NT"),
        path(term_id, "TR_NT"),
    ]


def test_followup_status_passes_only_when_all_criteria_pass() -> None:
    criteria = report.criteria_results([selected()], four_path_rows(), [control()])

    assert report.followup_status(criteria) == "post_screen_surface_followup_review_candidate"

    failed = report.criteria_results([selected()], [path("target", "TR_NT")], [control()])
    assert report.followup_status(failed) == "review_hold"


def test_criteria_requires_paths_to_match_terms() -> None:
    rows = four_path_rows()
    rows[0]["matches_term"] = "False"

    criteria = report.criteria_results([selected()], rows, [control()])

    assert ("All reconstructed paths spell the normalized term", "fail", "4 path rows") in criteria


def test_q_range_read_formats_values() -> None:
    assert report.q_range_read([control(q="0.032258")]) == "min 0.032258; max 0.032258"


def test_build_report_states_post_screen_boundary() -> None:
    text = report.build_report(
        selected_rows=[selected()],
        path_rows=four_path_rows(),
        control_rows=[control()],
        letter_manifest={"status": "success"},
        control_manifest={"status": "success"},
        run_commit="abc123",
    )

    assert "post_screen_surface_followup_review_candidate" in text
    assert "not a claim" in text
    assert "not prospective discovery" in text


def test_write_manifest_includes_followup_status(tmp_path) -> None:
    path = tmp_path / "manifest.json"

    report.write_manifest(
        path,
        run_commit="abc123",
        selected_rows=[selected()],
        path_rows=four_path_rows(),
        control_rows=[control()],
        status="post_screen_surface_followup_review_candidate",
        report_out=tmp_path / "report.md",
    )

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["status"] == "post_screen_surface_followup_review_candidate"
    assert payload["selected_rows"] == 1
