import unittest
from pathlib import Path

from scripts import analyze_colinear_els_source as audit


ATTACHMENTS_HTML = """<html><head>
<link rel="canonical" href="https://www.torah-code.org/papers/attachments.html" />
</head><body>
<a href="../patterns/pls.pdf">http://www.torahcodes.org/patterns/pls.pdf</a>
<a href="../patterns/roots.pdf">http://www.torahcodes.org/patterns/roots.pdf</a>
<a href="../patterns/all_1698.pdf">http://www.torahcodes.org/patterns/all_1698.pdf</a>
<a href="../patterns/res_113.pdf">http://www.torahcodes.org/patterns/res_113.pdf</a>
<a href="../patterns/consul_138.pdf">http://www.torahcodes.org/patterns/consul_138.pdf</a>
<a href="../patterns/intersec_108.pdf">http://www.torahcodes.org/patterns/intersec_108.pdf</a>
<a href="../patterns/comb_143.pdf">http://www.torahcodes.org/patterns/comb_143.pdf</a>
<a href="../patterns/att_heb.pdf">http://www.torahcodes.org/patterns/att_heb.pdf</a>
</body></html>"""


class ColinearElsSourceAuditTests(unittest.TestCase):
    def test_parse_attachments_page_counts_pdf_links(self) -> None:
        with self.subTest("windows-1255 page"):
            import tempfile

            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "attachments.html"
                path.write_bytes(ATTACHMENTS_HTML.encode("windows-1255"))

                parsed = audit.parse_attachments_page(path)

        self.assertEqual(parsed["pdf_links"], 8)
        self.assertEqual(parsed["canonical"], "https://www.torah-code.org/papers/attachments.html")
        self.assertIn("http://www.torahcodes.org/patterns/pls.pdf", parsed["pdf_link_targets"])

    def test_numeric_row_prefix_counts_complete_prefix(self) -> None:
        text = audit.clean_text("x \u202a1\u202c y \u202a2\u202c z \u202a4\u202c ###")

        self.assertEqual(audit.numeric_row_prefix(text, 10), 2)

    def test_parse_pls_pairs_from_text_extracts_raw_pair_rows(self) -> None:
        rows = audit.parse_pls_pairs_from_text(
            "\u202a\u05d5\u05ea\u05d1\u05d0\u05d5\u202c "
            "\u202a\u05ea\u05de\u05d5\u05e0\u05ea\u202c \u202a1\u202c\n"
            "\u05d0\u05e4\u05d3\u05ea\u05d5 \u05de\u05d4\u05db\u05d5\u05ea 2\n"
        )
        summary = audit.summarize_pls_pairs(rows)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["row_index"], 1)
        self.assertEqual(rows[0]["word_b"], "\u05d5\u05ea\u05d1\u05d0\u05d5")
        self.assertEqual(rows[0]["word_a"], "\u05ea\u05de\u05d5\u05e0\u05ea")
        self.assertEqual(summary["missing_row_indexes"], "")
        self.assertEqual(summary["duplicate_row_indexes"], 0)

    def test_parse_roots_rows_from_text_extracts_raw_root_tokens(self) -> None:
        rows = audit.parse_roots_rows_from_text(
            "root4 root3 root2 root1 word\n"
            "\u05d0\u05e8\u05e8          \u05d0\u05d0\u05e8\n"
            "\u05d0\u05d1\u05d3\u05d4      \u05d0\u05d1\u05d3        \u05d0\u05d1\u05d3\u05d4\n"
            "\u05d5\u05d1\u05de\u05e9\u05d0\u05e8\u05d5\u05ea\u05d9\u05db\u05de\u05e9\u05d0\u05e8\u05ea\n"
        )
        summary = audit.summarize_roots_rows(rows)

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["word"], "\u05d0\u05d0\u05e8")
        self.assertEqual(rows[0]["root_tokens"], "\u05d0\u05e8\u05e8")
        self.assertEqual(rows[1]["word"], "\u05d0\u05d1\u05d3\u05d4")
        self.assertEqual(rows[1]["root_tokens"], "\u05d0\u05d1\u05d3\u05d4 \u05d0\u05d1\u05d3")
        self.assertEqual(rows[2]["parse_status"], "single_token_unparsed")
        self.assertEqual(summary["rows"], 3)
        self.assertEqual(summary["parsed_rows"], 2)
        self.assertEqual(summary["single_token_rows"], 1)

    def test_hash_markers_can_complete_all_1698_count(self) -> None:
        pls_summary = {
            "rows": 6060,
            "duplicate_row_indexes": 0,
            "missing_row_indexes": "",
        }
        roots_summary = {
            "rows": 12830,
            "parsed_rows": 12828,
        }
        row = {
            "label": "all_1698",
            "expected_rows": 1698,
            "numeric_row_prefix": 999,
            "hash_marker_rows": 699,
            "observed_source_rows": 1698,
            "bytes": 1,
        }
        anchors = audit.protocol_anchors(
            "co-linear if d = d0 all words in P at least 5 letters long "
            "2 <= d <= 1000 6, 060 PLSs were found "
            "p-level obtained for this experiment is 6 x 10-8",
            {"pdf_links": 8},
            [
                {"label": "pls", "observed_source_rows": 6060, "bytes": 1},
                row,
                {"label": "res_113", "observed_source_rows": 113, "bytes": 1},
                {"label": "consul_138", "observed_source_rows": 138, "bytes": 1},
                {"label": "intersec_108", "observed_source_rows": 108, "bytes": 1},
                {"label": "comb_143", "observed_source_rows": 143, "bytes": 1},
                {"label": "roots", "observed_source_rows": "", "bytes": 1},
                {"label": "att_heb", "observed_source_rows": "", "bytes": 1},
            ],
            pls_summary,
            roots_summary,
        )

        by_anchor = {anchor["anchor"]: anchor["status"] for anchor in anchors}
        self.assertEqual(by_anchor["pls_pairs_6060_machine_rows"], "found")
        self.assertEqual(by_anchor["roots_rows_machine_extracted"], "found")
        self.assertEqual(by_anchor["all_1698_rows_observed"], "found")
        self.assertEqual(by_anchor["review_sets_502_rows_observed"], "found")


if __name__ == "__main__":
    unittest.main()
