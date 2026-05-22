from pathlib import Path

from scripts import check_wrr_source_policy_scenarios_doc as check


def test_current_wrr_source_policy_scenarios_doc_passes() -> None:
    assert check.validate_source_policy_scenarios_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_policy_scenarios_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_exclusion_counts_fail(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_POLICY_SCENARIOS.md"
    phrases = [
        phrase
        for phrase in check.REQUIRED_PHRASES
        if "exclude_all_source_review_flags" not in phrase
    ]
    doc.write_text("\n".join(phrases) + "\n", encoding="utf-8")

    failures = check.validate_source_policy_scenarios_doc(doc)

    assert any("exclude_all_source_review_flags" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR source-policy scenarios doc failure" in capsys.readouterr().err
