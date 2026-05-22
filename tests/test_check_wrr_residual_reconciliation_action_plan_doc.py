from pathlib import Path

from scripts import check_wrr_residual_reconciliation_action_plan_doc as check


def test_current_wrr_residual_reconciliation_action_plan_doc_passes() -> None:
    assert check.validate_residual_reconciliation_action_plan_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_residual_reconciliation_action_plan_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_boundary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md"
    text = "\n".join(
        phrase
        for phrase in check.REQUIRED_PHRASES
        if phrase
        != "keep term in working source; no automatic correction or exclusion without citable rule"
    )
    doc.write_text(text + "\n", encoding="utf-8")

    failures = check.validate_residual_reconciliation_action_plan_doc(doc)

    assert any("automatic correction" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR residual reconciliation action-plan failure" in capsys.readouterr().err
