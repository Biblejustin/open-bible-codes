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

    def test_hash_markers_can_complete_all_1698_count(self) -> None:
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
        )

        by_anchor = {anchor["anchor"]: anchor["status"] for anchor in anchors}
        self.assertEqual(by_anchor["all_1698_rows_observed"], "found")
        self.assertEqual(by_anchor["review_sets_502_rows_observed"], "found")


if __name__ == "__main__":
    unittest.main()
