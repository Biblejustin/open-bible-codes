import pytest

from scripts.download_door43_english_controls import select_rows


def test_select_rows_filters_by_label_or_source_id() -> None:
    rows = [{"label": "ULT", "source_id": "ult"}, {"label": "UST", "source_id": "ust"}]

    assert select_rows(rows, ["ult"]) == [rows[0]]
    assert select_rows(rows, ["UST"]) == [rows[1]]
    with pytest.raises(SystemExit, match="unknown source filters"):
        select_rows(rows, ["missing"])

