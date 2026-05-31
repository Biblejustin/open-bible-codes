from argparse import Namespace

from scripts import preflight_real_report_run as preflight


def test_required_paths_appends_cli_paths_without_dropping_defaults() -> None:
    paths = preflight.required_paths(Namespace(required_path=["docs/EXTRA.md"]))

    assert "scripts/preflight_real_report_run.py" in paths
    assert "docs/EXTRA.md" in paths

