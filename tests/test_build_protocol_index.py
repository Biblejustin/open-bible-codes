import sys
from pathlib import Path

from scripts import build_protocol_index


def test_build_protocol_index_writes_markdown_index(tmp_path: Path, monkeypatch) -> None:
    protocols = tmp_path / "protocols"
    protocols.mkdir()
    (protocols / "demo.toml").write_text(
        'name = "demo"\n'
        'description = "Demo protocol."\n'
        'manifest_out = "reports/demo/manifest.json"\n',
        encoding="utf-8",
    )
    out = tmp_path / "INDEX.md"
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_protocol_index", "--protocols-dir", str(protocols), "--out", str(out)],
    )

    assert build_protocol_index.main() == 0

    text = out.read_text(encoding="utf-8")
    assert "demo.toml" in text
    assert "Demo protocol" in text

