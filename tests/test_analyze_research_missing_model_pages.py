import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_research_missing_model_pages as audit


OVERVIEW = """<html><body>
<a href="../research/research_3a.html">Geometric Model Level 2</a>
<a href="../research/research_3b.html">Geometric Model Level 3</a>
<a href="../research/research_3d.html">ELS Model Level 2</a>
<a href="../research/research_3e.html">ELS Model Level 3</a>
</body></html>"""

ROOT_SPAM = """<html><head>
<title>Daftar Bet Kecil 100</title>
<link href="https://www.torah-code.org/" rel="canonical" />
</head><body>slot bet deposit pulsa rtp slot</body></html>"""


class ResearchMissingModelPagesTests(unittest.TestCase):
    def test_main_writes_missing_model_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            overview = root / "overview.html"
            overview.write_text(OVERVIEW, encoding="utf-8")
            paths = []
            for name in audit.EXPECTED:
                path = root / name
                path.write_text(ROOT_SPAM, encoding="utf-8")
                paths.append(path)
            args = []
            for path in paths:
                args.extend(["--source", str(path)])

            rc = audit.main(
                [
                    "--overview",
                    str(overview),
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
            summary_rows = list(csv.DictReader((root / "summary.csv").open(encoding="utf-8")))
            self.assertEqual(summary_rows[0]["overview_expected_level23_links"], "4")
            self.assertEqual(summary_rows[0]["expected_label_present_files"], "0")
            self.assertEqual(summary_rows[0]["usable_model_pages"], "0")
            markdown = (root / "audit.md").read_text(encoding="utf-8")
            self.assertIn("source-status audit only", markdown)
            self.assertIn("Found anchors: 6 of 6", markdown)
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["sources"]), 4)


if __name__ == "__main__":
    unittest.main()
