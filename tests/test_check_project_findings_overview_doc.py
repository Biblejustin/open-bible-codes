from pathlib import Path

from scripts import check_project_findings_overview_doc as check


def test_current_project_findings_overview_passes() -> None:
    assert check.validate_project_findings_overview() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    doc = tmp_path / "missing.md"

    assert check.validate_project_findings_overview(doc) == [f"{doc} is missing"]


def test_missing_required_heading_fails(tmp_path: Path) -> None:
    doc = tmp_path / "overview.md"
    doc.write_text(current_doc_text().replace("## Short Answer", "## Summary"), encoding="utf-8")

    failures = check.validate_project_findings_overview(doc)

    assert failures == [f"{doc} missing heading: ## Short Answer"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "overview.md"
    doc.write_text(
        current_doc_text().replace(
            "no result should be presented as a settled public finding",
            "results should be promoted",
        ),
        encoding="utf-8",
    )

    failures = check.validate_project_findings_overview(doc)

    assert failures == [
        f"{doc} missing phrase: "
        "no result should be presented as a settled public finding"
    ]


def test_missing_reference_fails(tmp_path: Path) -> None:
    doc = tmp_path / "overview.md"
    doc.write_text(
        current_doc_text().replace("`docs/CLAIM_CATALOG.md`", "`docs/MISSING.md`"),
        encoding="utf-8",
    )

    failures = check.validate_project_findings_overview(doc)

    assert failures == [f"{doc} missing reference: docs/CLAIM_CATALOG.md"]


def test_missing_readme_reader_path_fails(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    start_here = tmp_path / "START_HERE.md"
    readme.write_text("reader path missing\n", encoding="utf-8")
    start_here.write_text(valid_start_here_text(), encoding="utf-8")

    failures = check.validate_project_findings_overview(
        check.DEFAULT_DOC,
        readme,
        start_here,
    )

    assert failures == [
        f"{readme} missing phrase: "
        "whole-project findings overview: `docs/PROJECT_FINDINGS_OVERVIEW.md`"
    ]


def test_missing_start_here_reader_path_fails(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    start_here = tmp_path / "START_HERE.md"
    readme.write_text(valid_readme_text(), encoding="utf-8")
    start_here.write_text("reader path missing\n", encoding="utf-8")

    failures = check.validate_project_findings_overview(
        check.DEFAULT_DOC,
        readme,
        start_here,
    )

    assert failures == [
        f"{start_here} missing phrase: "
        "1. `docs/PROJECT_FINDINGS_OVERVIEW.md` for the whole-project findings summary.",
        f"{start_here} missing phrase: no current row should be presented as a public claim",
    ]


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--doc", str(tmp_path / "missing.md")])

    assert code == 1
    assert "project-findings overview failure" in capsys.readouterr().err


def test_main_uses_reader_path_arguments(tmp_path: Path, capsys) -> None:
    readme = tmp_path / "README.md"
    start_here = tmp_path / "START_HERE.md"
    readme.write_text(valid_readme_text(), encoding="utf-8")
    start_here.write_text("reader path missing\n", encoding="utf-8")

    code = check.main(
        [
            "--doc",
            str(check.DEFAULT_DOC),
            "--readme",
            str(readme),
            "--start-here",
            str(start_here),
        ]
    )

    assert code == 1
    assert f"{start_here} missing phrase" in capsys.readouterr().err


def current_doc_text() -> str:
    return check.DEFAULT_DOC.read_text(encoding="utf-8")


def valid_readme_text() -> str:
    return "\n".join(check.READER_PATH_REQUIREMENTS[check.DEFAULT_README])


def valid_start_here_text() -> str:
    return "\n".join(check.READER_PATH_REQUIREMENTS[check.DEFAULT_START_HERE])
