import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_under_construction_experiments_source as audit


PAGE_TEMPLATE = """<html><head><title>{title}</title></head><body>
<p><b>{heading}</b></p>
Under Construction
<a href="../experiments.html">Experiments</a>
</body></html>"""


class UnderConstructionExperimentSourceTests(unittest.TestCase):
    def test_extract_heading(self) -> None:
        self.assertEqual(
            audit.extract_heading("<p><b>Twin Towers</b></p>"),
            "Twin Towers",
        )

    def test_main_writes_status_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = []
            pages = {
                "torah_code_experiment_chumash.html": ("Torah Codes -- Chumash", "Chumash"),
                "torah_code_experiment_twin_towers.html": (
                    "Torah Codes -- Twin Towers",
                    "Twin Towers",
                ),
                "torah_code_experiment_tsunami.html": ("Torah Codes -- Tsunami", "Tsunami"),
                "torah_code_experiment_katrina.html": ("Torah Codes -- Tsunami", "Tsunami"),
                "torah_code_experiment_great_rabbis.html": (
                    "Torah Codes -- Great Rabbis",
                    "Great Rabbis",
                ),
                "torah_code_experiment_son_rabbis.html": (
                    "Torah Codes -- Son Rabbis",
                    "Son Rabbis",
                ),
            }
            for name, (title, heading) in pages.items():
                path = root / name
                path.write_text(
                    PAGE_TEMPLATE.format(title=title, heading=heading),
                    encoding="utf-8",
                )
                paths.append(path)
            args = []
            for path in paths:
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
            summary_rows = list(csv.DictReader((root / "summary.csv").open(encoding="utf-8")))
            self.assertEqual(summary_rows[0]["source_files"], "6")
            self.assertEqual(summary_rows[0]["under_construction_pages"], "6")
            self.assertEqual(summary_rows[0]["katrina_mislabeled_tsunami"], "True")
            markdown = (root / "audit.md").read_text(encoding="utf-8")
            self.assertIn("source-status audit only", markdown)
            self.assertIn("Found anchors: 9 of 9", markdown)
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["sources"]), 6)


if __name__ == "__main__":
    unittest.main()
