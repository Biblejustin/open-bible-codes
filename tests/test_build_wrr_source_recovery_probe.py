import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_source_recovery_probe as probe


GOOD_HTML = """<html><head>
<title>Torah Codes -- Research Program</title>
<link rel="canonical" href="https://www.torah-code.org/research/research_1.html">
</head><body>Research Program</body></html>"""

ROOT_HTML = """<html><head>
<title>Torah Codes</title>
<link rel="canonical" href="https://www.torah-code.org/">
</head><body>slot bet deposit pulsa</body></html>"""


class WrrSourceRecoveryProbeTests(unittest.TestCase):
    def test_analyze_download_classifies_usable_and_root_redirect_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = root / "good.html"
            bad = root / "bad.html"
            good.write_text(GOOD_HTML, encoding="utf-8")
            bad.write_text(ROOT_HTML, encoding="utf-8")

            good_row = probe.analyze_download(
                {
                    "label": "torah_code_research_program_1",
                    "url": "https://www.torah-code.org/research/research_1.html",
                    "final_url": "https://www.torah-code.org/research/research_1.html",
                    "redirected": False,
                    "http_status": 200,
                    "path": str(good),
                    "status": "downloaded",
                }
            )
            bad_row = probe.analyze_download(
                {
                    "label": "torah_code_research_geometric_model_level_2",
                    "url": "https://www.torah-code.org/research/research_3a.html",
                    "final_url": "https://www.torah-code.org/",
                    "redirected": True,
                    "http_status": 200,
                    "path": str(bad),
                    "status": "downloaded",
                }
            )

        self.assertEqual(good_row["usable_status"], "usable_current_source")
        self.assertTrue(good_row["expected_label_present"])
        self.assertEqual(bad_row["usable_status"], "unusable_current_download")
        self.assertTrue(bad_row["redirected"])
        self.assertTrue(bad_row["final_url_is_root"])
        self.assertTrue(bad_row["canonical_is_root"])
        self.assertTrue(bad_row["spam_marker_present"])

    def test_main_writes_probe_summary_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = root / "good.html"
            bad = root / "bad.html"
            good.write_text(GOOD_HTML, encoding="utf-8")
            bad.write_text(ROOT_HTML, encoding="utf-8")
            source_manifest = root / "sources.manifest.json"
            source_manifest.write_text(
                json.dumps(
                    {
                        "downloads": [
                            {
                                "label": "torah_code_research_program_1",
                                "url": "https://www.torah-code.org/research/research_1.html",
                                "final_url": "https://www.torah-code.org/research/research_1.html",
                                "redirected": False,
                                "http_status": 200,
                                "path": str(good),
                                "status": "downloaded",
                            },
                            {
                                "label": "torah_code_research_geometric_model_level_2",
                                "url": "https://www.torah-code.org/research/research_3a.html",
                                "final_url": "https://www.torah-code.org/",
                                "redirected": True,
                                "http_status": 200,
                                "path": str(bad),
                                "status": "downloaded",
                            },
                        ]
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            rc = probe.main(
                [
                    "--manifest",
                    str(source_manifest),
                    "--out",
                    str(root / "probe.csv"),
                    "--summary-out",
                    str(root / "summary.csv"),
                    "--markdown-out",
                    str(root / "probe.md"),
                    "--manifest-out",
                    str(root / "probe.manifest.json"),
                ]
            )

            self.assertEqual(rc, 0)
            summary = list(csv.DictReader((root / "summary.csv").open(encoding="utf-8")))[0]
            self.assertEqual(summary["downloads"], "2")
            self.assertEqual(summary["expected_label_present_rows"], "1")
            self.assertEqual(summary["redirected_rows"], "1")
            self.assertEqual(summary["root_final_url_rows"], "1")
            self.assertEqual(summary["spam_marker_rows"], "1")
            self.assertEqual(summary["usable_current_source_rows"], "1")
            rows = list(csv.DictReader((root / "probe.csv").open(encoding="utf-8")))
            self.assertEqual(rows[0]["usable_status"], "usable_current_source")
            self.assertEqual(rows[1]["usable_status"], "unusable_current_download")
            markdown = (root / "probe.md").read_text(encoding="utf-8")
            self.assertIn("WRR Source Recovery Probe", markdown)
            self.assertIn("does not update the cached `reports/wrr_1994/` bundle", markdown)
            manifest = json.loads((root / "probe.manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["summary"]["current_recovery_status"], "some_live_sources_recovered")


if __name__ == "__main__":
    unittest.main()
