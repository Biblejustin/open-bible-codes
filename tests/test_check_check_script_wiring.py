from pathlib import Path

from scripts import check_check_script_wiring as check


def test_current_check_scripts_are_wired() -> None:
    assert check.validate_check_script_wiring() == []


def test_missing_wiring_fails(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    protocols = tmp_path / "protocols"
    scripts.mkdir()
    protocols.mkdir()
    (scripts / "check_example.py").write_text("print('x')\n", encoding="utf-8")
    (tmp_path / "Makefile").write_text("", encoding="utf-8")
    (scripts / "preflight_real_report_run.py").write_text("", encoding="utf-8")
    (protocols / "demo.toml").write_text('name = "demo"\n', encoding="utf-8")

    failures = check.validate_check_script_wiring(tmp_path)

    assert failures == [
        "scripts/check_example.py is not referenced by Makefile, preflight, or protocols"
    ]


def test_makefile_module_reference_counts_as_wired(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "check_example.py").write_text("print('x')\n", encoding="utf-8")
    (tmp_path / "Makefile").write_text(
        "check-example:\n\tpython3 -m scripts.check_example\n",
        encoding="utf-8",
    )

    assert check.validate_check_script_wiring(tmp_path) == []


def test_protocol_path_reference_counts_as_wired(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    protocols = tmp_path / "protocols"
    scripts.mkdir()
    protocols.mkdir()
    (scripts / "check_example.py").write_text("print('x')\n", encoding="utf-8")
    (protocols / "demo.toml").write_text(
        'name = "demo"\ninputs = ["scripts/check_example.py"]\n',
        encoding="utf-8",
    )

    assert check.validate_check_script_wiring(tmp_path) == []
