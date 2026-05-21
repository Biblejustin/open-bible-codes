from scripts import build_prospective_lane_status as status
from scripts import scaffold_prospective_study as scaffold


def test_render_markdown_lists_blocked_lanes() -> None:
    profiles = [
        {
            "id": "blocked_lane",
            "status": "needs_predeclared_term_list",
            "term_file": "terms/blocked.csv",
            "protocol": "protocols/blocked.toml",
            "report_doc": "docs/BLOCKED.md",
            "source_term_files": "new term source",
            "excluded_prior": "old rows excluded",
        },
        {
            "id": "completed_lane",
            "status": "completed_negative_controlled_result",
            "term_file": "terms/done.csv",
            "protocol": "protocols/done.toml",
            "report_doc": "docs/DONE.md",
            "source_term_files": "fixed",
            "excluded_prior": "none",
        },
    ]

    text = status.render_markdown(profiles, status.DEFAULT_PROFILES)

    assert "`blocked_lane`" in text
    assert "`completed_lane`" in text
    assert "blocked; needs predeclared term list" in text
    assert "| `blocked_lane` | new term source | old rows excluded |" in text
    assert "| `completed_lane` | fixed | none |" not in text


def test_blocked_profiles_accepts_blocked_and_needs_statuses() -> None:
    profiles = [
        {"id": "a", "status": "blocked_until_new_term_source"},
        {"id": "b", "status": "needs_predeclared_term_list"},
        {"id": "c", "status": "completed_negative_controlled_result"},
    ]

    assert [profile["id"] for profile in status.blocked_profiles(profiles)] == ["a", "b"]


def test_tracked_lane_status_doc_matches_profiles() -> None:
    profiles = scaffold.load_profiles(status.DEFAULT_PROFILES)
    expected = status.render_markdown(profiles, status.DEFAULT_PROFILES)

    assert status.DEFAULT_OUT.read_text(encoding="utf-8") == expected
