from pathlib import Path

from scripts import check_script_tests as check


def test_current_scripts_have_matching_tests() -> None:
    assert check.validate_script_tests() == []


def test_missing_test_fails(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    tests = tmp_path / "tests"
    scripts.mkdir()
    tests.mkdir()
    (scripts / "example.py").write_text("print('x')\n", encoding="utf-8")

    failures = check.validate_script_tests(scripts, tests)

    assert failures == [
        f"{scripts / 'example.py'} missing matching test {tests / 'test_example.py'}"
    ]


def test_dunder_init_is_ignored(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    tests = tmp_path / "tests"
    scripts.mkdir()
    tests.mkdir()
    (scripts / "__init__.py").write_text("", encoding="utf-8")

    assert check.validate_script_tests(scripts, tests) == [
        f"{scripts} has no script modules"
    ]


def test_expected_test_path_uses_full_script_name() -> None:
    assert check.expected_test_path(Path("scripts/alpha.py")) == Path(
        "tests/test_alpha.py"
    )
