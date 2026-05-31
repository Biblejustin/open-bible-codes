import unittest

from scripts.analyze_wrr_primary_result_table import (
    EXPECTED_SOURCES,
    build_result_rows,
    markdown_cell,
    parse_rank,
    parse_table3_rows,
    summarize_ranks,
)


TABLE_TEXT = """
TABLE 3
Rank order of Pi among one million P,
P1 P2 P3 P4
G 453 5 570 4
R 619,140 681,451 364,859 573,861
V 211,777 519,115 410,746 591,503
"""


class WrrPrimaryResultTableTests(unittest.TestCase):
    def test_parse_table3_rows_extracts_rank_values_and_page(self) -> None:
        rows = parse_table3_rows(["other", TABLE_TEXT])

        self.assertEqual(rows["G"]["page"], 2)
        self.assertEqual(rows["G"]["ranks"], (453, 5, 570, 4))
        self.assertEqual(rows["R"]["ranks"], (619140, 681451, 364859, 573861))

    def test_build_result_rows_marks_missing_expected_sources(self) -> None:
        rows = build_result_rows([TABLE_TEXT])
        by_label = {row["label"]: row for row in rows}

        self.assertEqual(len(rows), len(EXPECTED_SOURCES))
        self.assertEqual(by_label["G"]["status"], "found")
        self.assertEqual(by_label["T"]["status"], "missing")

    def test_summarize_ranks_derives_paper_bonferroni_value(self) -> None:
        summary = summarize_ranks((453, 5, 570, 4))

        self.assertEqual(summary["min_rank"], "4")
        self.assertEqual(summary["min_statistic"], "P4")
        self.assertEqual(summary["min_rank_proportion"], "0.000004")
        self.assertEqual(summary["bonferroni_p0"], "0.000016")
        self.assertEqual(summary["bonferroni_p0_capped"], "0.000016")

    def test_summarize_ranks_caps_control_pvalue_for_display(self) -> None:
        summary = summarize_ranks((619140, 681451, 364859, 573861))

        self.assertEqual(summary["bonferroni_p0"], "1.459436")
        self.assertEqual(summary["bonferroni_p0_capped"], "1.000000")

    def test_parse_rank_removes_commas(self) -> None:
        self.assertEqual(parse_rank("619,140"), 619140)

    def test_markdown_cell_escapes_pipes(self) -> None:
        self.assertEqual(markdown_cell("a|b\nc"), "a\\|b c")


if __name__ == "__main__":
    unittest.main()
