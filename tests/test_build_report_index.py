import json
import sys
from pathlib import Path

from scripts import build_report_index


def test_build_report_index_writes_markdown_and_json(tmp_path: Path, monkeypatch) -> None:
    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "summary.csv").write_text("term,hits\nalpha,1\n", encoding="utf-8")
    markdown_out = tmp_path / "INDEX.md"
    json_out = tmp_path / "index.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_report_index",
            "--reports-dir",
            str(reports),
            "--out",
            str(markdown_out),
            "--json-out",
            str(json_out),
        ],
    )

    assert build_report_index.main() == 0

    assert "summary.csv" in markdown_out.read_text(encoding="utf-8")
    payload = json.loads(json_out.read_text(encoding="utf-8"))
    assert any(row["path"] == "summary.csv" for row in payload["reports"])

