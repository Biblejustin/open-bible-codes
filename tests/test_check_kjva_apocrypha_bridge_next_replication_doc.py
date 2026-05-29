from pathlib import Path

from scripts import check_kjva_apocrypha_bridge_next_replication_doc as check


def test_current_kjva_next_replication_doc_passes() -> None:
    assert check.validate_next_replication_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_next_replication_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "No significance wording from raw bridge counts alone.",
        "Raw counts are enough.",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_next_replication_doc(doc)

    assert any("missing phrase" in failure for failure in failures)


def test_missing_evidence_link_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "`reports/kjv_apocrypha_bridge_prospective/term_summary.csv`",
        "`reports/kjv_apocrypha_bridge_prospective/moved.csv`",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_next_replication_doc(doc)

    assert any("missing evidence link" in failure for failure in failures)


def test_overclaim_wording_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = (
        check.DEFAULT_DOC.read_text(encoding="utf-8")
        + "\nThis is a significant finding.\n"
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_next_replication_doc(doc)

    assert any("possible overclaim wording" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "KJVA apocrypha bridge next-replication doc failure" in capsys.readouterr().err
