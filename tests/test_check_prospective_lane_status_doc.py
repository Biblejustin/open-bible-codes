import json
from pathlib import Path

from scripts import build_prospective_lane_status as builder
from scripts import check_prospective_lane_status_doc as check


def test_current_lane_status_doc_passes() -> None:
    assert check.validate_lane_status_doc(check.DEFAULT_DOC, check.DEFAULT_PROFILES) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_lane_status_doc(
        tmp_path / "missing.md",
        check.DEFAULT_PROFILES,
    )

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_stale_doc_fails(tmp_path: Path) -> None:
    profiles = tmp_path / "profiles.json"
    profiles.write_text(
        json.dumps(
            {
                "profiles": [
                    {
                        "id": "ready_lane",
                        "status": "ready_for_preflight",
                        "term_file": "terms/ready.csv",
                        "protocol": "protocols/ready.toml",
                        "report_doc": "docs/READY.md",
                        "source_term_files": "fresh source",
                        "excluded_prior": "prior evidence",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    doc = tmp_path / "status.md"
    doc.write_text("stale", encoding="utf-8")

    failures = check.validate_lane_status_doc(doc, profiles)

    assert failures == [
        f"{doc} is stale; rerun python3 -m scripts.build_prospective_lane_status"
    ]


def test_generated_doc_with_same_profiles_passes(tmp_path: Path) -> None:
    profiles = tmp_path / "profiles.json"
    profile_data = {
        "profiles": [
            {
                "id": "blocked_lane",
                "status": "blocked_until_new_term_source",
                "term_file": "terms/blocked.csv",
                "protocol": "protocols/blocked.toml",
                "report_doc": "docs/BLOCKED.md",
                "source_term_files": "new external list",
                "excluded_prior": "prior rows",
            }
        ]
    }
    profiles.write_text(json.dumps(profile_data), encoding="utf-8")
    rendered = builder.render_markdown(
        profile_data["profiles"],
        Path(check.display_path(profiles)),
    )
    doc = tmp_path / "status.md"
    doc.write_text(rendered, encoding="utf-8")

    assert check.validate_lane_status_doc(doc, profiles) == []


def test_default_profile_lock_rejects_status_drift(tmp_path: Path) -> None:
    profiles = [
        {
            "id": profile_id,
            "status": "changed" if index == 0 else status,
            "term_file": term_file,
            "protocol": protocol,
            "report_doc": report_doc,
        }
        for index, (profile_id, status, term_file, protocol, report_doc) in enumerate(
            check.EXPECTED_PROFILE_ROWS
        )
    ]
    path = tmp_path / "profiles.json"
    path.write_text(json.dumps({"profiles": profiles}), encoding="utf-8")

    failures = check.validate_default_profiles_json(path, profiles)

    assert any("profile rows drifted" in failure for failure in failures)
    assert any("status counts drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "prospective lane-status doc failure" in capsys.readouterr().err
