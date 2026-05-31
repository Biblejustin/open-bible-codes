import pytest

from scripts.download_ebible_english_controls import select_rows


def test_select_rows_filters_by_label_or_source_id() -> None:
    rows = [{"label": "BSB", "source_id": "engbsb"}, {"label": "WEB", "source_id": "engwebu"}]

    assert select_rows(rows, ["engbsb"]) == [rows[0]]
    assert select_rows(rows, ["WEB"]) == [rows[1]]
    with pytest.raises(SystemExit, match="unknown source filters"):
        select_rows(rows, ["missing"])

