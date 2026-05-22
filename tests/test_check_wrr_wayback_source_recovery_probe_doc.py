from scripts import check_wrr_wayback_source_recovery_probe_doc as check


def test_current_wrr_wayback_source_recovery_probe_doc_passes() -> None:
    assert check.validate_wayback_source_recovery_probe_doc(check.DEFAULT_DOC) == []


def test_missing_wrr_wayback_source_recovery_probe_doc_fails(tmp_path) -> None:
    failures = check.validate_wayback_source_recovery_probe_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_incomplete_wrr_wayback_source_recovery_probe_doc_fails(tmp_path) -> None:
    doc = tmp_path / "WRR_WAYBACK_SOURCE_RECOVERY_PROBE.md"
    doc.write_text("# WRR Wayback Source Recovery Probe\n", encoding="utf-8")

    failures = check.validate_wayback_source_recovery_probe_doc(doc)

    assert failures
    assert any("Status: archived-source recovery probe only." in failure for failure in failures)
