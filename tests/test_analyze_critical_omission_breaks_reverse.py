import csv
from pathlib import Path

from scripts.analyze_critical_omission_breaks_reverse import write_rows


def test_write_rows_creates_parent_directory(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "rows.csv"

    write_rows(out, [{"ref": "John 1:1", "broken_total_hits": 1}])

    with out.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == [{"ref": "John 1:1", "broken_total_hits": "1"}]

