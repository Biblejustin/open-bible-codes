from scripts import check_israeli_prime_ministers_detail_recovery_probe_doc as check


def test_current_israeli_prime_ministers_detail_recovery_doc_passes() -> None:
    assert check.validate_detail_recovery_doc(check.DEFAULT_DOC) == []


def test_missing_israeli_prime_ministers_detail_recovery_doc_fails(tmp_path) -> None:
    failures = check.validate_detail_recovery_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_incomplete_israeli_prime_ministers_detail_recovery_doc_fails(tmp_path) -> None:
    doc = tmp_path / "probe.md"
    doc.write_text("# Israeli Prime Ministers Detail Recovery Probe\n", encoding="utf-8")

    failures = check.validate_detail_recovery_doc(doc)

    assert any("missing phrase" in failure for failure in failures)
    assert any("missing probe pages" in failure for failure in failures)
