import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_hypothesis_testing_source as audit


OVERVIEW_HTML = """<html><head>
<title>Torah Codes -- Hypothesis Testing</title>
</head><body>
<p><b>Hypothesis Testing</b></p>
Null hypothesis. Alternative hypothesis. Test statistic.
Critical region. Acceptance region.
<a href="hypothesis_2.html">Types of Errors</a>
<a href="hypotheses.html">Types of Hypotheses</a>
<a href="simulated_experiments.html">Understanding Through Simulated Experiments</a>
</body></html>"""

ROOT_HTML = """<html><head>
<title>Daftar Bet Kecil</title>
<link rel="canonical" href="https://www.torah-code.org/">
</head><body>slot bet deposit pulsa</body></html>"""


class HypothesisTestingSourceAuditTests(unittest.TestCase):
    def test_analyze_file_marks_overview_usable_and_spam_unusable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            overview = root / "torah_code_hypothesis_testing_overview.html"
            errors = root / "torah_code_hypothesis_testing_errors.html"
            overview.write_text(OVERVIEW_HTML, encoding="utf-8")
            errors.write_text(ROOT_HTML, encoding="utf-8")

            good_row = audit.analyze_file(overview)
            bad_row = audit.analyze_file(errors)

        self.assertEqual(good_row["usable_status"], "usable_method_source")
        self.assertTrue(good_row["expected_label_present"])
        self.assertEqual(good_row["method_anchor_count"], 5)
        self.assertEqual(good_row["link_count"], 3)
        self.assertEqual(bad_row["usable_status"], "unusable_current_download")
        self.assertTrue(bad_row["spam_marker_present"])
        self.assertTrue(bad_row["canonical_is_root"])

    def test_main_writes_status_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pages = {
                "torah_code_hypothesis_testing_overview.html": OVERVIEW_HTML,
                "torah_code_hypothesis_testing_errors.html": ROOT_HTML,
                "torah_code_hypothesis_testing_hypotheses.html": ROOT_HTML,
                "torah_code_hypothesis_testing_simulated_experiments.html": ROOT_HTML,
            }
            args = []
            for name, html in pages.items():
                path = root / name
                path.write_text(html, encoding="utf-8")
                args.extend(["--source", str(path)])

            rc = audit.main(
                [
                    *args,
                    "--out",
                    str(root / "pages.csv"),
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

            self.assertEqual(rc, 0)
            summary = list(csv.DictReader((root / "summary.csv").open(encoding="utf-8")))[0]
            self.assertEqual(summary["source_files"], "4")
            self.assertEqual(summary["usable_method_pages"], "1")
            self.assertEqual(summary["spam_marker_pages"], "3")
            markdown = (root / "audit.md").read_text(encoding="utf-8")
            self.assertIn("source-status audit only", markdown)
            self.assertIn("Found anchors: 7 of 7", markdown)
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["summary"]["claim_status"], "source_status_only_not_result_bearing")


if __name__ == "__main__":
    unittest.main()
