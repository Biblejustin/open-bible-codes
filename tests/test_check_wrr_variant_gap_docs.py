from pathlib import Path

from scripts import check_wrr_variant_gap_docs as check


def test_current_wrr_variant_gap_docs_pass() -> None:
    assert check.validate_variant_gap_docs() == []


def test_missing_zero_hit_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_variant_gap_docs(
        zero_hit_doc=tmp_path / "missing_zero.md",
        variant_gap_doc=check.DEFAULT_VARIANT_GAP_DOC,
    )

    assert failures == [f"{tmp_path / 'missing_zero.md'} is missing"]


def test_missing_variant_gap_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_variant_gap_docs(
        zero_hit_doc=check.DEFAULT_ZERO_HIT_DOC,
        variant_gap_doc=tmp_path / "missing_gap.md",
    )

    assert failures == [f"{tmp_path / 'missing_gap.md'} is missing"]


def test_missing_zero_hit_summary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_ZERO_HIT_VARIANT_PROBE.md"
    doc.write_text("\n".join(check.ZERO_HIT_REQUIRED_PHRASES[:-2]) + "\n", encoding="utf-8")

    failures = check.validate_doc(doc, check.ZERO_HIT_REQUIRED_PHRASES)

    assert any("wrr_date" in failure for failure in failures)


def test_missing_variant_gap_summary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_VARIANT_GAP_IMPACT.md"
    doc.write_text("\n".join(check.VARIANT_GAP_REQUIRED_PHRASES[:-4]) + "\n", encoding="utf-8")

    failures = check.validate_doc(doc, check.VARIANT_GAP_REQUIRED_PHRASES)

    assert any("all_blocking_terms_have_variant_hit" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--zero-hit-doc", str(missing)])

    assert code == 1
    assert "WRR variant-gap doc failure" in capsys.readouterr().err
