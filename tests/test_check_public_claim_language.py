from pathlib import Path

from scripts.check_public_claim_language import validate_public_claim_language


def test_current_public_claim_language_passes() -> None:
    assert validate_public_claim_language() == []


def test_reports_unsupported_claim_language(tmp_path: Path) -> None:
    doc = tmp_path / "CLAIM.md"
    doc.write_text("This proves the design.\n", encoding="utf-8")

    assert validate_public_claim_language([doc]) == [
        f"{doc}:1: unsupported claim language `proves`"
    ]


def test_reports_claim_level_phrase(tmp_path: Path) -> None:
    doc = tmp_path / "claims.csv"
    doc.write_text("id,notes\nx,claim-level output\n", encoding="utf-8")

    assert validate_public_claim_language([doc]) == [
        f"{doc}:2: unsupported claim language `claim-level`"
    ]


def test_ignores_fenced_markdown_commands(tmp_path: Path) -> None:
    doc = tmp_path / "README.md"
    doc.write_text(
        "```bash\n"
        "rg -n \"proof|claim-level\" docs README.md\n"
        "```\n",
        encoding="utf-8",
    )

    assert validate_public_claim_language([doc]) == []


def test_ignores_forbidden_language_section(tmp_path: Path) -> None:
    doc = tmp_path / "README.md"
    doc.write_text(
        "## Forbidden Language\n"
        "- proves WRR\n",
        encoding="utf-8",
    )

    assert validate_public_claim_language([doc]) == []
