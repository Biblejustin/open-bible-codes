from scripts import check_cities_pdf_recovery_probe_doc as check


def test_current_cities_pdf_recovery_probe_doc_passes() -> None:
    assert check.validate_cities_pdf_recovery_probe_doc(check.DEFAULT_DOC) == []


def test_detects_missing_boundary_phrase(tmp_path) -> None:
    doc = tmp_path / "probe.md"
    doc.write_text("# Cities PDF Recovery Probe\n", encoding="utf-8")

    failures = check.validate_cities_pdf_recovery_probe_doc(doc)

    assert any("missing phrase" in failure for failure in failures)
