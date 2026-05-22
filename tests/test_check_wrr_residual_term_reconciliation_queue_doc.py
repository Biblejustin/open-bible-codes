from scripts import check_wrr_residual_term_reconciliation_queue_doc as check


def test_current_wrr_residual_term_reconciliation_queue_doc_passes() -> None:
    assert check.validate_residual_term_reconciliation_queue_doc(check.DEFAULT_DOC) == []


def test_missing_wrr_residual_term_reconciliation_queue_doc_fails(tmp_path) -> None:
    failures = check.validate_residual_term_reconciliation_queue_doc(
        tmp_path / "missing.md"
    )

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_incomplete_wrr_residual_term_reconciliation_queue_doc_fails(tmp_path) -> None:
    doc = tmp_path / "WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md"
    doc.write_text("# WRR Residual Term Reconciliation Queue\n", encoding="utf-8")

    failures = check.validate_residual_term_reconciliation_queue_doc(doc)

    assert failures
    assert any("Unique unresolved terms" in failure for failure in failures)
