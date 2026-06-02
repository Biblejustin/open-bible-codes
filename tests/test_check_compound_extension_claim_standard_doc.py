from pathlib import Path

from scripts import check_compound_extension_claim_standard_doc as check


def test_current_doc_passes() -> None:
    assert check.validate_compound_extension_claim_standard_doc() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    assert check.validate_compound_extension_claim_standard_doc(missing) == [
        f"{missing} is missing"
    ]


def test_missing_heading_fails(tmp_path: Path) -> None:
    doc = tmp_path / "standard.md"
    text = "\n".join(
        [
            check.REQUIRED_HEADINGS[0],
            *check.REQUIRED_HEADINGS[2:],
            *[f"`{link}`" for link in check.REQUIRED_LINKS],
            *check.REQUIRED_PHRASES,
        ]
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_compound_extension_claim_standard_doc(doc)

    assert any("missing heading: ## Boundary" in failure for failure in failures)


def test_disallowed_claim_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "standard.md"
    text = "\n".join(
        [
            *check.REQUIRED_HEADINGS,
            *[f"`{link}`" for link in check.REQUIRED_LINKS],
            *check.REQUIRED_PHRASES,
            "This confirms the row.",
        ]
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_compound_extension_claim_standard_doc(doc)

    assert any("disallowed claim phrase: This confirms" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "compound-extension claim-standard doc failure" in capsys.readouterr().err
