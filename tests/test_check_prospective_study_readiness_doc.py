import json
from pathlib import Path

from scripts import check_prospective_study_readiness_doc as check


def test_current_prospective_readiness_doc_passes() -> None:
    assert check.validate_readiness_doc(check.DEFAULT_DOC, check.DEFAULT_PROFILES) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_readiness_doc(tmp_path / "missing.md", check.DEFAULT_PROFILES)

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_no_ready_doc_fails_when_profile_is_ready(tmp_path: Path) -> None:
    profiles = tmp_path / "profiles.json"
    profiles.write_text(
        json.dumps({"profiles": [{"id": "ready_lane", "status": "ready_for_preflight"}]}),
        encoding="utf-8",
    )
    doc = tmp_path / "readiness.md"
    doc.write_text(
        "\n".join(
            (
                "`configs/prospective_study_lanes.json`",
                "`docs/PROSPECTIVE_LANE_STATUS.md`",
                check.NO_CLAIM_RERUN_PHRASE,
                check.NO_READY_PHRASE,
                check.FRESH_TARGET_PHRASE,
                check.NO_BLOCKED_PHRASE,
            )
        ),
        encoding="utf-8",
    )

    failures = check.validate_readiness_doc(doc, profiles)

    assert any("says no ready lanes but profiles show: `ready_lane`" in f for f in failures)
    assert any("missing ready lane id: `ready_lane`" in f for f in failures)


def test_blocked_profile_requires_lane_id(tmp_path: Path) -> None:
    profiles = tmp_path / "profiles.json"
    profiles.write_text(
        json.dumps(
            {"profiles": [{"id": "blocked_lane", "status": "needs_predeclared_term_list"}]}
        ),
        encoding="utf-8",
    )
    doc = tmp_path / "readiness.md"
    doc.write_text(
        "\n".join(
            (
                f"`{profiles.as_posix()}`",
                "`docs/PROSPECTIVE_LANE_STATUS.md`",
                check.NO_CLAIM_RERUN_PHRASE,
                check.NO_READY_PHRASE,
                check.FRESH_TARGET_PHRASE,
            )
        ),
        encoding="utf-8",
    )

    failures = check.validate_readiness_doc(doc, profiles)

    assert any("missing blocked lane id: `blocked_lane`" in f for f in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "prospective readiness doc failure" in capsys.readouterr().err
