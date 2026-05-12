from els.protocol_runner import load_protocol


def test_lxx_apocrypha_bridge_display_steps_track_term_display_helper() -> None:
    protocol = load_protocol("protocols/apocrypha_bridge_study.toml")
    steps_by_id = {step["id"]: step for step in protocol["steps"]}

    for step_id in [
        "bridge_candidates",
        "bridge_context",
        "bridge_controls",
        "apocrypha_only_counts",
        "bridge_completion_review",
    ]:
        assert "els/term_display.py" in steps_by_id[step_id]["inputs"], step_id
