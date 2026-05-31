from pathlib import Path

from scripts.compress_dynamic_span_partition_outputs import result_row


def test_result_row_reports_bytes_saved_without_negative_values() -> None:
    row = {"partition_id": "p1", "corpus": "TR_NT", "term_id": "demo"}

    compressed = result_row(row, "compressed", Path("out.csv"), Path("out.csv.gz"), 100, 40)
    expanded = result_row(row, "compressed", Path("out.csv"), Path("out.csv.gz"), 40, 100)

    assert compressed["bytes_saved"] == 60
    assert expanded["bytes_saved"] == 0

