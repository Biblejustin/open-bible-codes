import json
from pathlib import Path

from scripts import check_greek_surface_second_cohort_readiness_doc as check


def test_current_second_cohort_doc_passes() -> None:
    assert check.validate_second_cohort_doc(check.DEFAULT_DOC, check.DEFAULT_PROFILES) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_second_cohort_doc(tmp_path / "missing.md", check.DEFAULT_PROFILES)

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_ready_profile_rejects_no_ready_boundary(tmp_path: Path) -> None:
    profile_rows = [{"id": "ready_lane", "status": "ready_for_preflight"}]
    profiles = tmp_path / "profiles.json"
    profiles.write_text(
        json.dumps({"profiles": profile_rows}),
        encoding="utf-8",
    )
    doc = tmp_path / "second_cohort.md"
    doc.write_text(
        "\n".join(
            (
                "`terms/greek_expanded_prospective_terms.csv`",
                "`docs/PROSPECTIVE_STUDY_READINESS.md`",
                check.NO_READY_PHRASE,
                check.FRESH_TARGET_PHRASE,
                check.BLOCKED_STATUS_PHRASE,
                check.NOT_FROM_EXISTING_POOL_PHRASE,
                check.ZERO_OUTPUT_PHRASE,
                check.NO_EXISTING_POOL_RERUN_PHRASE,
                *check.status_count_phrases(profile_rows),
            )
        ),
        encoding="utf-8",
    )

    failures = check.validate_second_cohort_doc(doc, profiles)

    assert any("says no ready lanes but profiles show: `ready_lane`" in f for f in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "Greek second-cohort readiness doc failure" in capsys.readouterr().err
