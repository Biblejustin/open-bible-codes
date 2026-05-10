from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.build_report_db import main


def test_build_report_db_skips_current_table(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    pytest.importorskip("duckdb")
    csv_path = tmp_path / "hits.csv"
    db = tmp_path / "reports" / "db.duckdb"
    write_rows(csv_path, [{"hit_id": "1", "term_id": "term"}])

    assert main(["--db", str(db), "--no-defaults", "--table", f"{csv_path}:hits"]) == 0
    first = capsys.readouterr().out
    assert "imported=1" in first
    assert main(["--db", str(db), "--no-defaults", "--table", f"{csv_path}:hits"]) == 0
    second = capsys.readouterr().out
    assert "current hits" in second
    assert "imported=0" in second
    assert "current=1" in second


def test_build_report_db_reimports_stale_table(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    pytest.importorskip("duckdb")
    csv_path = tmp_path / "hits.csv"
    db = tmp_path / "reports" / "db.duckdb"
    write_rows(csv_path, [{"hit_id": "1", "term_id": "term"}])
    assert main(["--db", str(db), "--no-defaults", "--table", f"{csv_path}:hits"]) == 0
    capsys.readouterr()
    write_rows(csv_path, [{"hit_id": "1", "term_id": "term"}, {"hit_id": "2", "term_id": "term"}])

    assert main(["--db", str(db), "--no-defaults", "--table", f"{csv_path}:hits"]) == 0
    output = capsys.readouterr().out
    assert "rows=2" in output
    assert "imported=1" in output


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
