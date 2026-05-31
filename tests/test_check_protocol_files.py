from pathlib import Path

from scripts import check_protocol_files as check


def test_current_protocol_files_pass() -> None:
    assert check.validate_protocol_files() == []


def test_invalid_protocol_fails(tmp_path: Path) -> None:
    protocols = tmp_path / "protocols"
    protocols.mkdir()
    (protocols / "bad.toml").write_text(
        """
name = "bad"

[[steps]]
id = "one"
argv = "not-a-list"
""".lstrip(),
        encoding="utf-8",
    )

    failures = check.validate_protocol_files(protocols)

    assert len(failures) == 1
    assert "step one needs argv string list" in failures[0]


def test_duplicate_protocol_name_fails(tmp_path: Path) -> None:
    protocols = tmp_path / "protocols"
    protocols.mkdir()
    write_protocol(protocols / "a.toml", "same")
    write_protocol(protocols / "b.toml", "same")

    failures = check.validate_protocol_files(protocols)

    assert len(failures) == 1
    assert "duplicate protocol name same" in failures[0]


def write_protocol(path: Path, name: str) -> None:
    path.write_text(
        f"""
name = "{name}"

[[steps]]
id = "one"
argv = ["-c", "print(1)"]
""".lstrip(),
        encoding="utf-8",
    )
