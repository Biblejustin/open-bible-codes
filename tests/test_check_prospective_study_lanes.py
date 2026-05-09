import json

from scripts import check_prospective_study_lanes as check


def valid_profile(source_path: str) -> dict:
    return {
        "id": "demo_lane",
        "title": "Demo Lane",
        "status": "ready",
        "language": "hebrew",
        "term_file": "terms/demo.csv",
        "protocol": "protocols/demo.toml",
        "report_doc": "docs/DEMO_REPORT.md",
        "sources": [{"label": "MT_WLC", "path": source_path}],
        "skip_range": "2..100",
        "direction": "both",
        "min_normalized_length": "4",
        "candidate_type": "exact rows",
        "context_rule": "none",
        "controls": "controls",
        "correction": "bh",
        "source_term_files": "terms/demo.csv",
        "dedupe_rule": "normalized term",
        "excluded_prior": "none",
        "candidate_rule": "rule",
        "primary_row_outcome": "row outcome",
        "primary_study_outcome": "study outcome",
    }


def test_validate_current_profiles_pass() -> None:
    assert check.validate_profiles(check.DEFAULT_PROFILE_FILE) == []


def test_validate_profiles_rejects_duplicate_ids(tmp_path) -> None:
    source = tmp_path / "config.toml"
    source.write_text('name = "demo"\n', encoding="utf-8")
    payload = {"profiles": [valid_profile(str(source)), valid_profile(str(source))]}
    path = tmp_path / "profiles.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    failures = check.validate_profiles(path)

    assert "demo_lane: duplicate id" in failures


def test_validate_profiles_checks_source_paths(tmp_path) -> None:
    missing = tmp_path / "missing.toml"
    payload = {"profiles": [valid_profile(str(missing))]}
    path = tmp_path / "profiles.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    failures = check.validate_profiles(path)

    assert failures == [f"demo_lane: source path missing: {missing}"]


def test_main_returns_failure_for_bad_profiles(tmp_path) -> None:
    path = tmp_path / "profiles.json"
    path.write_text(json.dumps({"profiles": []}), encoding="utf-8")

    assert check.main([str(path)]) == 1
