from pathlib import Path

from scripts import check_wrr_support_docs_local_lock as check


def test_current_wrr_support_docs_pass() -> None:
    assert check.validate_support_docs() == []


def test_missing_support_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_support_docs(tmp_path)

    assert any("docs/WRR_REPLICATION_PLAN.md is missing" in failure for failure in failures)


def test_missing_locked_local_boundary_phrase_fails(tmp_path: Path) -> None:
    for relative_path, phrases in check.REQUIRED_PHRASES_BY_DOC.items():
        doc = tmp_path / relative_path
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text("\n".join(phrases) + "\n", encoding="utf-8")

    target = tmp_path / "docs/WRR_METHODOLOGY_GAPS.md"
    text = target.read_text(encoding="utf-8")
    target.write_text(
        text.replace("72 defined, 110 ordinary-not-valid, 0 under-minimum", ""),
        encoding="utf-8",
    )

    failures = check.validate_support_docs(tmp_path)

    assert any("72 defined, 110 ordinary-not-valid" in failure for failure in failures)


def test_stale_phrase_fails(tmp_path: Path) -> None:
    for relative_path, phrases in check.REQUIRED_PHRASES_BY_DOC.items():
        doc = tmp_path / relative_path
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text("\n".join(phrases) + "\n", encoding="utf-8")

    target = tmp_path / "docs/WRR_CORRECTED_DISTANCE_NOTES.md"
    target.write_text(
        target.read_text(encoding="utf-8") + "\nchoose one before final `D(w)` runs\n",
        encoding="utf-8",
    )

    failures = check.validate_support_docs(tmp_path)

    assert any("stale phrase" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--root", str(tmp_path)])

    assert code == 1
    assert "WRR support-doc local-lock failure" in capsys.readouterr().err
