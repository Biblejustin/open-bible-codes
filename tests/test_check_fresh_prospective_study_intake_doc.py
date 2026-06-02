from pathlib import Path

from scripts import check_fresh_prospective_study_intake_doc as check


def test_current_doc_passes() -> None:
    assert check.validate_fresh_prospective_study_intake_doc() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    assert check.validate_fresh_prospective_study_intake_doc(missing) == [
        f"{missing} is missing"
    ]


def test_missing_gate_fails(tmp_path: Path) -> None:
    doc = tmp_path / "intake.md"
    text = "\n".join(
        [
            *check.REQUIRED_HEADINGS,
            *[f"`{link}`" for link in check.REQUIRED_LINKS],
            *check.REQUIRED_PHRASES,
            *[f"| {gate} | evidence | pass |" for gate in check.REQUIRED_GATES[1:]],
        ]
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_fresh_prospective_study_intake_doc(doc)

    assert any("missing checklist gate: Source lawfulness" in failure for failure in failures)


def test_disallowed_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "intake.md"
    text = "\n".join(
        [
            *check.REQUIRED_HEADINGS,
            *[f"`{link}`" for link in check.REQUIRED_LINKS],
            *check.REQUIRED_PHRASES,
            *[f"| {gate} | evidence | pass |" for gate in check.REQUIRED_GATES],
            "result-producing run is allowed",
        ]
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_fresh_prospective_study_intake_doc(doc)

    assert any(
        "disallowed phrase: result-producing run is allowed" in failure
        for failure in failures
    )


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "fresh prospective-study intake doc failure" in capsys.readouterr().err
