from pathlib import Path

from scripts import check_clean_lock_results_summary_doc as check


def test_current_clean_lock_summary_passes() -> None:
    assert check.validate_clean_lock_results_summary_doc() == []


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "summary.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8")
    doc.write_text(text.replace("0 adjusted-support terms", ""), encoding="utf-8")

    failures = check.validate_clean_lock_results_summary_doc(doc)

    assert any("missing phrase: 0 adjusted-support terms" in failure for failure in failures)


def test_missing_reference_fails(tmp_path: Path) -> None:
    doc = tmp_path / "summary.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8")
    doc.write_text(
        text.replace("docs/GREEK_SURFACE_NEW_TERMS_REPORT.md", "docs/OTHER.md"),
        encoding="utf-8",
    )

    failures = check.validate_clean_lock_results_summary_doc(doc)

    assert any(
        "missing reference: docs/GREEK_SURFACE_NEW_TERMS_REPORT.md" in failure
        for failure in failures
    )


def test_forbidden_claim_ready_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "summary.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8")
    doc.write_text(text + "\nThis lane is claim-ready.\n", encoding="utf-8")

    failures = check.validate_clean_lock_results_summary_doc(doc)

    assert any("contains forbidden phrase: claim-ready" in failure for failure in failures)


def test_forbidden_positive_conclusive_claim_fails(tmp_path: Path) -> None:
    doc = tmp_path / "summary.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8")
    doc.write_text(text + "\nThis lane is a conclusive claim.\n", encoding="utf-8")

    failures = check.validate_clean_lock_results_summary_doc(doc)

    assert any("contains forbidden pattern:" in failure for failure in failures)
