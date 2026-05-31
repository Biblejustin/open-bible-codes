import sys
from pathlib import Path

from scripts import build_docs_index


def test_build_docs_index_writes_markdown_index(tmp_path: Path, monkeypatch) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "A.md").write_text("# Alpha\n\nBody.\n", encoding="utf-8")
    out = tmp_path / "INDEX.md"
    monkeypatch.setattr(sys, "argv", ["build_docs_index", "--docs-dir", str(docs), "--out", str(out)])

    assert build_docs_index.main() == 0

    text = out.read_text(encoding="utf-8")
    assert "Alpha" in text
    assert "A.md" in text

