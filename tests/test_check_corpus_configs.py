from pathlib import Path

from scripts import check_corpus_configs as check


def test_current_corpus_configs_pass() -> None:
    assert check.validate_corpus_configs() == []


def test_invalid_language_fails(tmp_path: Path) -> None:
    configs = tmp_path / "configs"
    configs.mkdir()
    write_config(
        configs / "demo.toml",
        """
name = "Demo"
language = "latin"

[[sources]]
name = "Demo"
format = "text"
path = "../data/demo.txt"
ref = "DEMO"
""".lstrip(),
    )

    assert check.validate_corpus_configs(configs) == [
        f"{configs / 'demo.toml'} unsupported language: latin"
    ]


def test_csv_missing_text_column_fails(tmp_path: Path) -> None:
    configs = tmp_path / "configs"
    configs.mkdir()
    write_config(
        configs / "demo.toml",
        """
name = "Demo"
language = "english"

[[sources]]
name = "Demo"
format = "csv"
path = "../data/demo.csv"
ref_column = "ref"
book_column = "book"
chapter_column = "chapter"
verse_column = "verse"
""".lstrip(),
    )

    assert check.validate_corpus_configs(configs) == [
        f"{configs / 'demo.toml'}:source 1 missing required fields: text_column"
    ]


def test_empty_non_template_config_fails(tmp_path: Path) -> None:
    configs = tmp_path / "configs"
    configs.mkdir()
    write_config(configs / "demo.toml", "")

    assert check.validate_corpus_configs(configs) == [
        f"{configs / 'demo.toml'} is empty"
    ]


def write_config(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
