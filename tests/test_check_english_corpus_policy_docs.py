from pathlib import Path

from scripts import check_english_corpus_policy_docs as check


def test_current_policy_docs_pass() -> None:
    assert check.validate_policy_docs() == []


def test_policy_docs_report_missing_required_phrase(tmp_path: Path) -> None:
    write_policy_docs(tmp_path)
    (tmp_path / "README.md").write_text("missing policy\n", encoding="utf-8")

    failures = check.validate_policy_docs(tmp_path)

    assert failures
    assert "README.md: missing phrase:" in failures[0]


def test_policy_docs_report_stale_blocker_header(tmp_path: Path) -> None:
    write_policy_docs(tmp_path)
    register = tmp_path / "docs" / "REMAINING_WORK_REGISTER.md"
    register.write_text(
        register.read_text(encoding="utf-8")
        + "\n### Remaining BibleGateway English Corpora\n",
        encoding="utf-8",
    )

    failures = check.validate_policy_docs(tmp_path)

    assert failures == [
        "docs/REMAINING_WORK_REGISTER.md: forbidden stale phrase: "
        "### Remaining BibleGateway English Corpora"
    ]


def write_policy_docs(root: Path) -> None:
    docs = root / "docs"
    docs.mkdir()
    for relative_path, phrases in check.REQUIRED_PHRASES_BY_DOC.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(phrases) + "\n", encoding="utf-8")
