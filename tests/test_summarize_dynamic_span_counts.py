from scripts.summarize_dynamic_span_counts import table_row


def test_table_row_rounds_elapsed_seconds() -> None:
    row = {
        "corpus": "TR_NT",
        "mode": "full-span",
        "term_id": "alpha",
        "hit_count": "10",
        "hits_per_million_positions": "1.2",
        "forward_count": "6",
        "backward_count": "4",
        "effective_max_skip": "50",
        "counter_elapsed_seconds": "1.23456",
    }

    assert table_row(row).endswith("| 50 | 1.235 |")

