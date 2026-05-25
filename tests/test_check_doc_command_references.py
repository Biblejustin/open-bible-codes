from pathlib import Path

from scripts.check_doc_command_references import validate_doc_command_references


def test_current_doc_command_references_pass() -> None:
    assert validate_doc_command_references() == []


def test_reports_missing_script_module(tmp_path: Path) -> None:
    write_minimal_repo(tmp_path)
    (tmp_path / "README.md").write_text(
        "```bash\npython3 -m scripts.missing_tool\n```\n",
        encoding="utf-8",
    )

    assert validate_doc_command_references(tmp_path) == [
        "README.md:2: missing script module scripts.missing_tool"
    ]


def test_reports_missing_protocol(tmp_path: Path) -> None:
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "RUN.md").write_text(
        "Run `python3 -m scripts.run_protocol protocols/missing.toml --resume`.\n",
        encoding="utf-8",
    )

    assert validate_doc_command_references(tmp_path) == [
        "docs/RUN.md:1: missing protocol protocols/missing.toml"
    ]


def test_ignores_protocol_placeholders(tmp_path: Path) -> None:
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "TEMPLATE.md").write_text(
        "Protocol: `protocols/[protocol].toml`\n",
        encoding="utf-8",
    )

    assert validate_doc_command_references(tmp_path) == []


def write_minimal_repo(root: Path) -> None:
    (root / "scripts").mkdir()
    (root / "scripts" / "run_protocol.py").write_text("", encoding="utf-8")
    (root / "protocols").mkdir()
    (root / "docs").mkdir()
    (root / "README.md").write_text("", encoding="utf-8")
