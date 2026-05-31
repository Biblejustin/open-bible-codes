from pathlib import Path

from scripts import check_check_script_tests as check


def test_current_check_scripts_have_matching_tests() -> None:
    assert check.validate_check_script_tests() == []


def test_missing_test_fails(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    tests = tmp_path / "tests"
    scripts.mkdir()
    tests.mkdir()
    (scripts / "check_example.py").write_text("print('x')\n", encoding="utf-8")

    failures = check.validate_check_script_tests(scripts, tests)

    assert failures == [
        f"{scripts / 'check_example.py'} missing matching test "
        f"{tests / 'test_check_example.py'}"
    ]


def test_orphan_test_fails(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    tests = tmp_path / "tests"
    scripts.mkdir()
    tests.mkdir()
    (tests / "test_check_missing.py").write_text("def test_x(): pass\n", encoding="utf-8")

    failures = check.validate_check_script_tests(scripts, tests)

    assert f"{scripts} has no check_*.py scripts" in failures
    assert (
        f"{tests / 'test_check_missing.py'} has no matching script "
        f"{scripts / 'check_missing.py'}"
    ) in failures


def test_expected_test_path_uses_full_script_name() -> None:
    assert check.expected_test_path(Path("scripts/check_alpha.py")) == Path(
        "tests/test_check_alpha.py"
    )
