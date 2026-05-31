from scripts import build_real_report_run_summary as summary


def test_report_summary_cells_escape_markdown_and_ranges() -> None:
    assert summary.md_cell("a|b\nc") == "a\\|b c"
    assert summary.range_text(None, 10) == "none"
    assert summary.range_text(7, 7) == "7"
    assert summary.range_text(7, 12) == "7..12"

