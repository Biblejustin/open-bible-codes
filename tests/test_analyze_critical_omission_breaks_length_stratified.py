import csv
from pathlib import Path

from scripts.analyze_critical_omission_breaks_length_stratified import write_rows


def test_write_rows_uses_input_keys_as_header(tmp_path: Path) -> None:
    out = tmp_path / "rows.csv"

    write_rows(out, [{"term_id": "alpha", "broken_hits": 2}])

    with out.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == [{"term_id": "alpha", "broken_hits": "2"}]

