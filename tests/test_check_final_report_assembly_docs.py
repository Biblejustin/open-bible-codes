from pathlib import Path

from scripts import check_final_report_assembly_docs as check


def test_current_final_report_assembly_docs_pass() -> None:
    assert check.validate_final_report_assembly_docs() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_final_report_assembly_docs(tmp_path)

    assert failures == [
        f"{path} is missing" for path in check.REQUIRED_PHRASES_BY_DOC
    ]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    for relative_path, phrases in check.REQUIRED_PHRASES_BY_DOC.items():
        doc = tmp_path / relative_path
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text("\n".join(phrases), encoding="utf-8")
    final_report = tmp_path / "docs" / "FINAL_REPORT.md"
    final_report.write_text(
        final_report.read_text(encoding="utf-8").replace(
            "does not promote any row to a public claim",
            "missing claim boundary",
        ),
        encoding="utf-8",
    )

    failures = check.validate_final_report_assembly_docs(tmp_path)

    assert failures == [
        "docs/FINAL_REPORT.md missing phrase: "
        "does not promote any row to a public claim"
    ]


def test_missing_final_report_handoff_link_fails(tmp_path: Path) -> None:
    for relative_path, phrases in check.REQUIRED_PHRASES_BY_DOC.items():
        doc = tmp_path / relative_path
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text("\n".join(phrases), encoding="utf-8")
    final_report = tmp_path / "docs" / "FINAL_REPORT.md"
    final_report.write_text(
        final_report.read_text(encoding="utf-8").replace(
            "`docs/WRR_NO_INPUT_HANDOFF_STATUS.md`",
            "`docs/MISSING.md`",
        ),
        encoding="utf-8",
    )

    failures = check.validate_final_report_assembly_docs(tmp_path)

    assert failures == [
        "docs/FINAL_REPORT.md missing phrase: "
        "`docs/WRR_NO_INPUT_HANDOFF_STATUS.md`"
    ]


def test_forbidden_final_report_outline_phrase_fails(tmp_path: Path) -> None:
    for relative_path, phrases in check.REQUIRED_PHRASES_BY_DOC.items():
        doc = tmp_path / relative_path
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text("\n".join(phrases), encoding="utf-8")
    outline = tmp_path / "docs" / "FINAL_REPORT_OUTLINE.md"
    outline.write_text(
        outline.read_text(encoding="utf-8")
        + "\nkeeps 8 handoff rows, 61 OCR packet pages\n",
        encoding="utf-8",
    )

    failures = check.validate_final_report_assembly_docs(tmp_path)

    assert failures == [
        "docs/FINAL_REPORT_OUTLINE.md contains forbidden phrase: "
        "keeps 8 handoff rows, 61 OCR packet pages"
    ]


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--root", str(tmp_path)])

    assert code == 1
    assert "final-report assembly doc failure" in capsys.readouterr().err
