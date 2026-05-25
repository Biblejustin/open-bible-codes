import json
from pathlib import Path

from scripts import check_prospective_study_next_lock_doc as check


def test_current_next_lock_doc_passes() -> None:
    assert check.validate_next_lock_doc(check.DEFAULT_DOC, check.DEFAULT_PROFILES) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_next_lock_doc(tmp_path / "missing.md", check.DEFAULT_PROFILES)

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_no_ready_doc_fails_when_profile_is_ready(tmp_path: Path) -> None:
    profiles = tmp_path / "profiles.json"
    profiles.write_text(
        json.dumps({"profiles": [{"id": "ready_lane", "status": "ready_for_preflight"}]}),
        encoding="utf-8",
    )
    doc = tmp_path / "next_lock.md"
    doc.write_text(
        "\n".join(
            (
                f"`{profiles.as_posix()}`",
                "`docs/PROSPECTIVE_LANE_STATUS.md`",
                check.NO_READY_PHRASE,
                check.FRESH_TARGET_PHRASE,
                *check.NO_PROMOTION_PHRASES,
            )
        ),
        encoding="utf-8",
    )

    failures = check.validate_next_lock_doc(doc, profiles)

    assert any("says no ready lanes but profiles show: `ready_lane`" in f for f in failures)
    assert any("missing ready lane id: `ready_lane`" in f for f in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "prospective next-lock doc failure" in capsys.readouterr().err
