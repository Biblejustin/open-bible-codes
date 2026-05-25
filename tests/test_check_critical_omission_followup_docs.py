from pathlib import Path

from scripts import check_critical_omission_followup_docs as check


def test_current_critical_omission_docs_pass() -> None:
    assert check.validate_critical_omission_docs() == []


def test_missing_docs_fail(tmp_path: Path) -> None:
    failures = check.validate_critical_omission_docs(tmp_path)

    assert failures == [f"{rule.path} is missing" for rule in check.DOC_RULES]


def test_missing_required_section_fails(tmp_path: Path) -> None:
    for rule in check.DOC_RULES:
        doc = tmp_path / rule.path
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text(
            "\n".join(
                phrase
                for phrase in (*check.REQUIRED_SECTIONS, *rule.required_phrases)
                if phrase != "## Cautions"
            ),
            encoding="utf-8",
        )

    failures = check.validate_critical_omission_docs(tmp_path)

    assert failures == [
        f"{rule.path} missing section: ## Cautions" for rule in check.DOC_RULES
    ]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    for rule in check.DOC_RULES:
        doc = tmp_path / rule.path
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text(
            "\n".join((*check.REQUIRED_SECTIONS, *rule.required_phrases)),
            encoding="utf-8",
        )
    first = check.DOC_RULES[0]
    first_doc = tmp_path / first.path
    first_doc.write_text(
        first_doc.read_text(encoding="utf-8").replace(
            "Broken total: 558.",
            "Broken total: unknown.",
        ),
        encoding="utf-8",
    )

    failures = check.validate_critical_omission_docs(tmp_path)

    assert failures == [
        f"{first.path} missing phrase: Broken total: 558.",
    ]


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--root", str(tmp_path)])

    assert code == 1
    assert "critical-omission doc failure" in capsys.readouterr().err
