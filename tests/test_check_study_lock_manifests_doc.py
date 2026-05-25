import json
from pathlib import Path

from scripts import check_study_lock_manifests_doc as check


def test_current_study_lock_manifests_doc_passes() -> None:
    assert check.validate_study_lock_doc(check.DEFAULT_DOC, check.DEFAULT_PROFILES) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_study_lock_doc(tmp_path / "missing.md", check.DEFAULT_PROFILES)

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_ready_profile_rejects_historical_only_boundary(tmp_path: Path) -> None:
    profiles = tmp_path / "profiles.json"
    profiles.write_text(
        json.dumps({"profiles": [{"id": "ready_lane", "status": "ready_for_preflight"}]}),
        encoding="utf-8",
    )
    doc = tmp_path / "study_lock.md"
    doc.write_text(
        "\n".join(
            (
                f"`{profiles.as_posix()}`",
                "`docs/PROSPECTIVE_STUDY_READINESS.md`",
                "`docs/PROSPECTIVE_STUDY_PREREGISTRATION_TEMPLATE.md`",
                check.HISTORICAL_STATUS_PHRASE,
                check.FRESH_TARGET_PHRASE,
                check.NO_COMPLETED_PROFILE_AS_CLAIM_PHRASE,
                check.LOCK_NOT_RESULT_PHRASE,
                *check.REQUIRED_COMMANDS,
            )
        ),
        encoding="utf-8",
    )

    failures = check.validate_study_lock_doc(doc, profiles)

    assert any(
        "says profiles are historical/status records but ready profiles show: `ready_lane`"
        in failure
        for failure in failures
    )
    assert any("missing ready lane id: `ready_lane`" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "study-lock manifests doc failure" in capsys.readouterr().err
