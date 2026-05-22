import tempfile
import unittest
from pathlib import Path

from scripts import analyze_israeli_prime_ministers_source as ipm


PDF_TEXT = """Israeli Prime Ministers

Head of the Government             dlynnd y`x
Head                                          y`x

       English Name       Hebrew Name Key Words
1      David Ben Gurion              oeixeb oa cec
                                        oeixeb oa c
2      Moshe Sharett                   zxy dyn
                                         zxy n
                                           zxy
"""

MAIN_HTML = """<html><body>
Since the founding of the state of Israel, there have been twelve people who have occupied the position.
<table><tr><td>Skip Specification</td><td>Expected Number of ELS = 10</td></tr>
<tr><td>Number of Trials</td><td>10,000</td></tr></table>
The p-level of the experiment was 6/10,000.
</body></html>"""

DETAIL_HTML = """<html><body><p><b>David Ben Gurion</b></p>
<b>Key Words: Gurion, Head </b><p>
<a href="../experiments/israeli_prime_ministers_2.html"> &lt; Next &gt; </a>
</body></html>"""


class IsraeliPrimeMinistersSourceTests(unittest.TestCase):
    def test_parse_pdf_records_counts_keyword_rows(self) -> None:
        records = ipm.parse_pdf_records(PDF_TEXT)
        keyword_rows = ipm.pdf_keyword_rows_from_source(PDF_TEXT, records)

        self.assertEqual([record.record_index for record in records], [1, 2])
        self.assertEqual(records[0].hebrew_keyword_rows, 2)
        self.assertEqual(records[1].hebrew_keyword_rows, 3)
        self.assertEqual(ipm.pdf_keyword_phrase_rows(PDF_TEXT), 2)
        self.assertEqual(len(keyword_rows), 7)
        self.assertEqual(keyword_rows[0]["source_table"], "prime_minister_phrase_keywords")
        self.assertEqual(keyword_rows[0]["english_label"], "Head of the Government")
        self.assertEqual(keyword_rows[2]["english_label"], "David Ben Gurion")
        self.assertEqual(keyword_rows[-1]["hebrew_keyword"], "zxy")

    def test_protocol_anchors_find_main_pdf_and_detail_pages(self) -> None:
        detail = {"has_key_words": True}
        anchors = ipm.protocol_anchors(MAIN_HTML, PDF_TEXT, [detail])

        self.assertEqual({row["status"] for row in anchors}, {"found"})

    def test_main_writes_source_shape_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            main = root / "main.html"
            pdf = root / "source.pdf"
            page = root / "page_1.html"
            main.write_text(MAIN_HTML, encoding="utf-8")
            pdf.write_bytes(PDF_TEXT.encode("utf-8"))
            page.write_text(DETAIL_HTML, encoding="utf-8")

            original_extract = ipm.extract_pdf_text
            try:
                ipm.extract_pdf_text = lambda path: PDF_TEXT  # type: ignore[assignment]
                rc = ipm.main(
                    [
                        "--main-html",
                        str(main),
                        "--pdf",
                        str(pdf),
                        "--keyword-page-glob",
                        str(root / "page_*.html"),
                        "--out",
                        str(root / "records.csv"),
                        "--pdf-keywords-out",
                        str(root / "pdf_keywords.csv"),
                        "--detail-pages-out",
                        str(root / "detail_pages.csv"),
                        "--summary-out",
                        str(root / "summary.csv"),
                        "--anchors-out",
                        str(root / "anchors.csv"),
                        "--markdown-out",
                        str(root / "audit.md"),
                        "--manifest-out",
                        str(root / "manifest.json"),
                    ]
                )
            finally:
                ipm.extract_pdf_text = original_extract  # type: ignore[assignment]

            self.assertEqual(rc, 0)
            markdown = (root / "audit.md").read_text(encoding="utf-8")
            self.assertIn("source-shape audit only", markdown)
            self.assertIn("PDF prime-minister rows | 2", markdown)
            self.assertIn("machine PDF keyword rows extracted | 7", markdown)
            self.assertIn("machine HTML detail rows extracted | 1", markdown)
            self.assertIn("not a claim-ready replication", markdown)
            self.assertTrue((root / "pdf_keywords.csv").exists())
            self.assertTrue((root / "detail_pages.csv").exists())
            self.assertTrue((root / "manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
