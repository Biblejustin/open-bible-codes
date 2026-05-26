import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import build_israeli_prime_ministers_detail_recovery_probe as probe
from scripts.download_wrr_sources import FetchResult


GOOD_HTML = """<html><head>
<title>Benjamin Netanyahu</title>
<link rel="canonical" href="https://www.torah-code.org/experiments/israeli_prime_ministers_9.html">
</head><body>Benjamin Netanyahu</body></html>"""

ROOT_HTML = """<html><head>
<title>Torah Codes</title>
<link rel="canonical" href="https://www.torah-code.org/">
</head><body>slot bet deposit pulsa</body></html>"""


class IsraeliPrimeMinisterDetailRecoveryProbeTests(unittest.TestCase):
    def test_analyze_snapshot_classifies_usable_and_root_redirect_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = root / "good.html"
            bad = root / "bad.html"
            good.write_text(GOOD_HTML, encoding="utf-8")
            bad.write_text(ROOT_HTML, encoding="utf-8")

            good_row = probe.analyze_snapshot(
                probe.DetailPage(9, "Benjamin Netanyahu"),
                FetchResult(
                    data=GOOD_HTML.encode("utf-8"),
                    final_url="https://www.torah-code.org/experiments/israeli_prime_ministers_9.html",
                    http_status=200,
                ),
                good,
            )
            bad_row = probe.analyze_snapshot(
                probe.DetailPage(10, "Ehud Barak"),
                FetchResult(
                    data=ROOT_HTML.encode("utf-8"),
                    final_url="https://www.torah-code.org/",
                    http_status=200,
                ),
                bad,
            )

        self.assertEqual(good_row["usable_status"], "usable_detail_page")
        self.assertTrue(good_row["expected_title_present"])
        self.assertEqual(bad_row["usable_status"], "unrecovered_detail_page")
        self.assertTrue(bad_row["redirected"])
        self.assertTrue(bad_row["final_url_is_root"])
        self.assertTrue(bad_row["canonical_is_root"])
        self.assertTrue(bad_row["spam_marker_present"])

    def test_main_writes_summary_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            html_by_url = {
                probe.DetailPage(index, title).url: ROOT_HTML.encode("utf-8")
                for index, title in probe.EXPECTED_PAGES
            }

            def fake_fetch(url: str) -> FetchResult:
                return FetchResult(
                    data=html_by_url[url],
                    final_url="https://www.torah-code.org/",
                    http_status=200,
                )

            with patch(
                "scripts.build_israeli_prime_ministers_detail_recovery_probe.fetch_url",
                side_effect=fake_fetch,
            ):
                rc = probe.main(
                    [
                        "--out-dir",
                        str(root / "snapshots"),
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
            self.assertEqual(summary["pages_probed"], "4")
            self.assertEqual(summary["usable_detail_pages"], "0")
            self.assertEqual(summary["unrecovered_detail_pages"], "4")
            text = (root / "probe.md").read_text(encoding="utf-8")
            self.assertIn("Israeli Prime Ministers Detail Recovery Probe", text)
            self.assertIn("Do not run a result-bearing protocol", text)
            manifest = json.loads((root / "probe.manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["summary"]["recovery_status"], "no_detail_pages_recovered")


if __name__ == "__main__":
    unittest.main()
