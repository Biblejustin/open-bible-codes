import json
from pathlib import Path

from scripts import check_consolidated_findings_doc as check


def test_current_consolidated_findings_doc_passes() -> None:
    assert (
        check.validate_consolidated_findings_doc(
            check.DEFAULT_DOC,
            check.DEFAULT_PROFILES,
        )
        == []
    )


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_consolidated_findings_doc(
        tmp_path / "missing.md",
        check.DEFAULT_PROFILES,
    )

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_ready_profile_rejects_no_ready_boundary(tmp_path: Path) -> None:
    profiles = tmp_path / "profiles.json"
    profiles.write_text(
        json.dumps({"profiles": [{"id": "ready_lane", "status": "ready_for_preflight"}]}),
        encoding="utf-8",
    )
    doc = tmp_path / "consolidated.md"
    doc.write_text(
        "\n".join(
            (
                "`configs/prospective_study_lanes.json`",
                "`docs/PROSPECTIVE_STUDY_READINESS.md`",
                "`docs/PROSPECTIVE_LANE_STATUS.md`",
                "`docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md`",
                check.CURRENT_STATUS_PHRASE,
                check.NO_READY_PHRASE,
                check.FRESH_TARGET_PHRASE,
                check.NO_RERUN_PHRASE,
                check.NO_RAW_COUNT_PHRASE,
            )
        ),
        encoding="utf-8",
    )

    failures = check.validate_consolidated_findings_doc(doc, profiles)

    assert any("says no ready lanes but profiles show: `ready_lane`" in f for f in failures)


def test_missing_required_links_fail(tmp_path: Path) -> None:
    doc = tmp_path / "consolidated.md"
    doc.write_text(
        "\n".join(
            (
                check.CURRENT_STATUS_PHRASE,
                check.NO_READY_PHRASE,
                check.FRESH_TARGET_PHRASE,
                check.NO_RERUN_PHRASE,
                check.NO_RAW_COUNT_PHRASE,
            )
        ),
        encoding="utf-8",
    )

    failures = check.validate_consolidated_findings_doc(doc, check.DEFAULT_PROFILES)

    assert any("missing link: configs/prospective_study_lanes.json" in f for f in failures)
    assert any("missing link: docs/PROSPECTIVE_LANE_STATUS.md" in f for f in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "consolidated findings doc failure" in capsys.readouterr().err
