from pathlib import Path

from scripts import check_kjva_public_handoff_docs as check


def test_current_kjva_public_handoff_docs_pass() -> None:
    assert check.validate_kjva_public_handoff_docs() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    write_valid_docs(tmp_path, skip=Path("README.md"))

    failures = check.validate_kjva_public_handoff_docs(tmp_path)

    assert failures == ["README.md is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    missing = "new independent KJVA result output blocked"
    write_valid_docs(tmp_path, omit={Path("README.md"): missing})

    failures = check.validate_kjva_public_handoff_docs(tmp_path)

    assert failures == [f"README.md missing phrase: {missing}"]


def test_forbidden_stale_phrase_fails(tmp_path: Path) -> None:
    stale = "new KJVA result is ready"
    write_valid_docs(tmp_path)
    doc = tmp_path / "docs/FINAL_REPORT.md"
    with doc.open("a", encoding="utf-8") as handle:
        handle.write(f"\n{stale}\n")

    failures = check.validate_kjva_public_handoff_docs(tmp_path)

    assert failures == [f"docs/FINAL_REPORT.md contains stale phrase: {stale}"]


def test_generated_summary_stale_result_allowed_fails(tmp_path: Path) -> None:
    stale = "| Result allowed | 1 |"
    write_valid_docs(tmp_path)
    doc = tmp_path / "reports/real_report_run/summary.md"
    with doc.open("a", encoding="utf-8") as handle:
        handle.write(f"\n{stale}\n")

    failures = check.validate_kjva_public_handoff_docs(tmp_path)

    assert failures == [
        f"reports/real_report_run/summary.md contains stale phrase: {stale}"
    ]


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--root", str(tmp_path)])

    assert code == 1
    assert "KJVA public handoff doc failure" in capsys.readouterr().err


def write_valid_docs(
    root: Path,
    *,
    skip: Path | None = None,
    omit: dict[Path, str] | None = None,
) -> None:
    omit = omit or {}
    for relative_path, phrases in check.REQUIRED_PHRASES_BY_DOC.items():
        if relative_path == skip:
            continue
        doc = root / relative_path
        doc.parent.mkdir(parents=True, exist_ok=True)
        text = "\n".join(
            phrase for phrase in phrases if phrase != omit.get(relative_path)
        )
        doc.write_text(text + "\n", encoding="utf-8")
