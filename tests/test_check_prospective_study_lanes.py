import json

from scripts import check_prospective_study_lanes as check


def valid_profile(source_path: str) -> dict:
    return {
        "id": "demo_lane",
        "title": "Demo Lane",
        "status": "ready_for_preflight",
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


def write_profile_assets(tmp_path) -> None:
    for relative, text in [
        ("terms/demo.csv", "term\nDEMO\n"),
        ("protocols/demo.toml", 'name = "demo"\n'),
        ("docs/DEMO_REPORT.md", "# Demo\n"),
    ]:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def test_validate_current_profiles_pass() -> None:
    assert check.validate_profiles(check.DEFAULT_PROFILE_FILE) == []


def test_validate_profiles_rejects_duplicate_ids(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    write_profile_assets(tmp_path)
    source = tmp_path / "config.toml"
    source.write_text('name = "demo"\n', encoding="utf-8")
    payload = {"profiles": [valid_profile(str(source)), valid_profile(str(source))]}
    path = tmp_path / "profiles.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    failures = check.validate_profiles(path)

    assert "demo_lane: duplicate id" in failures


def test_validate_profiles_checks_source_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    write_profile_assets(tmp_path)
    missing = tmp_path / "missing.toml"
    payload = {"profiles": [valid_profile(str(missing))]}
    path = tmp_path / "profiles.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    failures = check.validate_profiles(path)

    assert failures == [f"demo_lane: source path missing: {missing}"]


def test_validate_profiles_checks_profile_artifact_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "config.toml"
    source.write_text('name = "demo"\n', encoding="utf-8")
    payload = {"profiles": [valid_profile(str(source))]}
    path = tmp_path / "profiles.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    failures = check.validate_profiles(path)

    assert failures == [
        "demo_lane: term_file path missing: terms/demo.csv",
        "demo_lane: protocol path missing: protocols/demo.toml",
        "demo_lane: report_doc path missing: docs/DEMO_REPORT.md",
    ]


def test_validate_profiles_rejects_unknown_status(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    write_profile_assets(tmp_path)
    source = tmp_path / "config.toml"
    source.write_text('name = "demo"\n', encoding="utf-8")
    profile = valid_profile(str(source))
    profile["status"] = "ready"
    path = tmp_path / "profiles.json"
    path.write_text(json.dumps({"profiles": [profile]}), encoding="utf-8")

    failures = check.validate_profiles(path)

    assert failures == ["demo_lane: unknown status: ready"]


def test_main_returns_failure_for_bad_profiles(tmp_path) -> None:
    path = tmp_path / "profiles.json"
    path.write_text(json.dumps({"profiles": []}), encoding="utf-8")

    assert check.main([str(path)]) == 1
