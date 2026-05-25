from pathlib import Path

from scripts import check_wrr_adjacent_source_audit_docs as check


def test_current_adjacent_source_audit_docs_pass() -> None:
    assert check.validate_adjacent_source_audit_docs() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_adjacent_source_audit_docs(tmp_path)

    assert failures
    assert failures[0].endswith("is missing")


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    for rule in check.DOC_RULES:
        doc = tmp_path / rule.path
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text("\n".join(rule.required_phrases) + "\n", encoding="utf-8")
    first = check.DOC_RULES[0]
    (tmp_path / first.path).write_text(
        "\n".join(first.required_phrases[1:]) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_adjacent_source_audit_docs(tmp_path)

    assert failures == [f"{first.path} missing phrase: {first.required_phrases[0]}"]


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--root", str(tmp_path)])

    assert code == 1
    assert "WRR adjacent source audit doc failure" in capsys.readouterr().err
