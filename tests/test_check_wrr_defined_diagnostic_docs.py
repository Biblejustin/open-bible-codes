from pathlib import Path

from scripts import check_wrr_defined_diagnostic_docs as check


def test_current_wrr_defined_diagnostic_docs_pass() -> None:
    assert check.validate_defined_diagnostic_docs() == []


def test_missing_pair_set_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_defined_diagnostic_docs(
        pair_set_doc=tmp_path / "missing_pair.md",
        gap_reason_doc=check.DEFAULT_GAP_REASON_DOC,
    )

    assert failures == [f"{tmp_path / 'missing_pair.md'} is missing"]


def test_missing_gap_reason_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_defined_diagnostic_docs(
        pair_set_doc=check.DEFAULT_PAIR_SET_DOC,
        gap_reason_doc=tmp_path / "missing_gap.md",
    )

    assert failures == [f"{tmp_path / 'missing_gap.md'} is missing"]


def test_missing_pair_set_best_run_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_DEFINED_PAIR_SET_AUDIT.md"
    doc.write_text("\n".join(check.PAIR_SET_REQUIRED_PHRASES[:-2]) + "\n", encoding="utf-8")

    failures = check.validate_doc(doc, check.PAIR_SET_REQUIRED_PHRASES)

    assert any("72 of 163" in failure for failure in failures)


def test_missing_gap_reason_ordinary_missing_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_DEFINED_GAP_REASON_AUDIT.md"
    doc.write_text("\n".join(check.GAP_REASON_REQUIRED_PHRASES[:-2]) + "\n", encoding="utf-8")

    failures = check.validate_doc(doc, check.GAP_REASON_REQUIRED_PHRASES)

    assert any("Ordinary-missing rows total 110" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--pair-set-doc", str(missing)])

    assert code == 1
    assert "WRR defined diagnostic doc failure" in capsys.readouterr().err
