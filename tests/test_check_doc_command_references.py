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


def test_reports_missing_config(tmp_path: Path) -> None:
    write_minimal_repo(tmp_path)
    (tmp_path / "README.md").write_text(
        "Stats: `python3 -m els stats --config configs/missing.toml`.\n",
        encoding="utf-8",
    )

    assert validate_doc_command_references(tmp_path) == [
        "README.md:1: missing config configs/missing.toml"
    ]


def test_reports_missing_term_file(tmp_path: Path) -> None:
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "TERMS.md").write_text(
        "Terms: `terms/missing_terms.csv`.\n",
        encoding="utf-8",
    )

    assert validate_doc_command_references(tmp_path) == [
        "docs/TERMS.md:1: missing term file terms/missing_terms.csv"
    ]


def test_reports_missing_claim_file(tmp_path: Path) -> None:
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "CLAIMS.md").write_text(
        "Claim catalog: `claims/missing_claims.csv`.\n",
        encoding="utf-8",
    )

    assert validate_doc_command_references(tmp_path) == [
        "docs/CLAIMS.md:1: missing claim file claims/missing_claims.csv"
    ]


def test_reports_missing_mapping_file(tmp_path: Path) -> None:
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "MAPPING.md").write_text(
        "Mapping: `data/study/mappings/missing_mapping.csv`.\n",
        encoding="utf-8",
    )

    assert validate_doc_command_references(tmp_path) == [
        "docs/MAPPING.md:1: missing mapping file data/study/mappings/missing_mapping.csv"
    ]


def test_reports_missing_treat_as_deleted_file(tmp_path: Path) -> None:
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "OVERRIDE.md").write_text(
        "Override: `protocols/treat_as_deleted/missing_override.csv`.\n",
        encoding="utf-8",
    )

    assert validate_doc_command_references(tmp_path) == [
        (
            "docs/OVERRIDE.md:1: missing treat-as-deleted file "
            "protocols/treat_as_deleted/missing_override.csv"
        )
    ]


def test_ignores_protocol_placeholders(tmp_path: Path) -> None:
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "TEMPLATE.md").write_text(
        "Protocol: `protocols/[protocol].toml`\n"
        "Config: `configs/[config].toml`\n"
        "Terms: `terms/[term_file].csv`\n",
        encoding="utf-8",
    )

    assert validate_doc_command_references(tmp_path) == []


def test_does_not_match_embedded_terms_path_fragment(tmp_path: Path) -> None:
    write_minimal_repo(tmp_path)
    (tmp_path / "docs" / "REPORT.md").write_text(
        "Report: `reports/greek_surface_new_terms/term_summary.csv`.\n",
        encoding="utf-8",
    )

    assert validate_doc_command_references(tmp_path) == []


def write_minimal_repo(root: Path) -> None:
    (root / "scripts").mkdir()
    (root / "scripts" / "run_protocol.py").write_text("", encoding="utf-8")
    (root / "protocols").mkdir()
    (root / "docs").mkdir()
    (root / "README.md").write_text("", encoding="utf-8")
