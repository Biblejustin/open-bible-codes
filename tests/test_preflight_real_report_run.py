from argparse import Namespace
from pathlib import Path

from scripts import preflight_real_report_run as preflight


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_required_paths_appends_cli_paths_without_dropping_defaults() -> None:
    paths = preflight.required_paths(Namespace(required_path=["docs/EXTRA.md"]))

    assert "scripts/preflight_real_report_run.py" in paths
    assert "docs/EXTRA.md" in paths


def test_preflight_protocol_inputs_report_invalid_toml(tmp_path) -> None:
    _write(tmp_path / "protocols/real_report_run.toml", "[[steps]\nid = 'preflight'\n")

    failures = preflight.find_preflight_protocol_input_failures(tmp_path)

    assert len(failures) == 1
    assert failures[0].startswith(
        "protocols/real_report_run.toml is invalid TOML:"
    )


def test_preflight_protocol_inputs_require_steps_list(tmp_path) -> None:
    _write(tmp_path / "protocols/real_report_run.toml", 'steps = "bad"\n')

    failures = preflight.find_preflight_protocol_input_failures(tmp_path)

    assert failures == ["protocols/real_report_run.toml steps must be a list"]
