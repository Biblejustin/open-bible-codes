from pathlib import Path

from scripts.run_biblegateway_english_versions import render_config, resolve_config_path, toml_string


def test_render_config_uses_csv_path_and_escaped_strings() -> None:
    row = {"label": "Demo", "resolved_config_path": "", "resolved_local_csv": "demo.csv"}

    text = render_config(row, "demo.csv")

    assert 'name = "Local Private English Demo"' in text
    assert 'path = "demo.csv"' in text
    assert toml_string('a"b') == '"a\\"b"'
    assert resolve_config_path(Path("/tmp/base"), "configs/demo.toml") == Path(
        "/tmp/base/configs/demo.toml"
    ).resolve()
