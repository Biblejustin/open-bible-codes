from scripts.build_greek_surface_prospective_report import build_report


def test_build_report_marks_empty_selection_as_negative() -> None:
    text = build_report(
        terms=[],
        queue=[],
        patterns=[{"presence_scope": "source_only"}],
        selected=[],
        cohort=[{"selected": "False", "read": "not_selected"}],
        controls=[],
        lock={"git": {"commit": "abc123", "dirty": False}, "settings": {}},
        preflight={"status": "ok", "output_path": "reports/preflight.json"},
        protocol={"status": "ok"},
        title="Greek Surface Demo",
        description="Demo run.",
    )

    assert "Status: negative_primary_filter_result; no claim." in text
    assert "| Source-only patterns | 1 |" in text
    assert "valid negative result" in text

