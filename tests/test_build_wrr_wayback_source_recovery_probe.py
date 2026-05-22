import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import build_wrr_wayback_source_recovery_probe as probe


GOOD_HTML = """<html><head>
<title>Torah Codes -- The Model</title>
</head><body>The Model</body></html>"""

SPAM_HTML = """<html><head>
<title>Spam Root</title>
</head><body>slot bet deposit pulsa</body></html>"""


class WrrWaybackSourceRecoveryProbeTests(unittest.TestCase):
    def test_wayback_raw_snapshot_url_uses_id_replay(self) -> None:
        raw = probe.wayback_raw_snapshot_url(
            "http://web.archive.org/web/20160615070555/"
            "http://www.torah-code.org:80/research/research_2a.shtml"
        )

        self.assertEqual(
            raw,
            "https://web.archive.org/web/20160615070555id_/"
            "http://www.torah-code.org:80/research/research_2a.shtml",
        )

    def test_analyze_snapshot_classifies_usable_and_missing_rows(self) -> None:
        source = probe.SOURCE_BY_LABEL["torah_code_research_model_overview_shtml"]
        usable = probe.analyze_snapshot(
            source=source,
            availability_status="availability_checked",
            closest={
                "available": True,
                "status": "200",
                "timestamp": "20160615070555",
                "url": "http://web.archive.org/web/20160615070555/"
                "http://www.torah-code.org:80/research/research_2a.shtml",
            },
            archive_raw_url="https://web.archive.org/web/20160615070555id_/source",
            archive_fetch_status="downloaded",
            path=Path("snapshot.html"),
            raw=GOOD_HTML.encode("utf-8"),
        )
        missing = probe.analyze_snapshot(
            source=source,
            availability_status="availability_checked",
            closest={},
            archive_raw_url="",
            archive_fetch_status="not_available",
            path=None,
            raw=b"",
        )
        spam = probe.analyze_snapshot(
            source=source,
            availability_status="availability_checked",
            closest={"available": True, "status": "200"},
            archive_raw_url="https://web.archive.org/web/20160615070555id_/source",
            archive_fetch_status="downloaded",
            path=Path("snapshot.html"),
            raw=SPAM_HTML.encode("utf-8"),
        )

        self.assertEqual(usable["usable_status"], "usable_archived_source")
        self.assertTrue(usable["expected_label_present"])
        self.assertEqual(usable["title"], "Torah Codes -- The Model")
        self.assertEqual(missing["usable_status"], "no_archived_snapshot")
        self.assertEqual(spam["usable_status"], "unusable_archived_snapshot")
        self.assertTrue(spam["spam_marker_present"])

    def test_main_writes_wayback_probe_outputs(self) -> None:
        available_payload = {
            "archived_snapshots": {
                "closest": {
                    "available": True,
                    "status": "200",
                    "timestamp": "20160615070555",
                    "url": "http://web.archive.org/web/20160615070555/"
                    "http://www.torah-code.org:80/research/research_2a.shtml",
                }
            }
        }
        missing_payload = {"archived_snapshots": {}}

        def fake_fetch_json(url: str) -> dict:
            if "research_2a" in url:
                return available_payload
            return missing_payload

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(
                probe,
                "fetch_json",
                side_effect=fake_fetch_json,
            ), patch.object(
                probe,
                "fetch_bytes",
                return_value=GOOD_HTML.encode("utf-8"),
            ):
                rc = probe.main(
                    [
                        "--out",
                        str(root / "probe.csv"),
                        "--summary-out",
                        str(root / "summary.csv"),
                        "--markdown-out",
                        str(root / "probe.md"),
                        "--manifest-out",
                        str(root / "manifest.json"),
                        "--snapshot-dir",
                        str(root / "snapshots"),
                        "--refresh",
                        "--label",
                        "torah_code_research_model_overview_shtml",
                        "--label",
                        "torah_code_research_geometric_model_level_2_shtml",
                    ]
                )

            self.assertEqual(rc, 0)
            rows = list(csv.DictReader((root / "probe.csv").open(encoding="utf-8")))
            self.assertEqual(rows[0]["usable_status"], "usable_archived_source")
            self.assertEqual(rows[1]["usable_status"], "no_archived_snapshot")
            summary = list(csv.DictReader((root / "summary.csv").open(encoding="utf-8")))[0]
            self.assertEqual(summary["probe_rows"], "2")
            self.assertEqual(summary["usable_archived_source_rows"], "1")
            self.assertEqual(summary["missing_archived_concepts"], "1")
            markdown = (root / "probe.md").read_text(encoding="utf-8")
            self.assertIn("WRR Wayback Source Recovery Probe", markdown)
            self.assertIn("does not update the cached `reports/wrr_1994/` bundle", markdown)
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["summary"]["current_archive_recovery_status"],
                "partial_archived_sources_recovered",
            )


if __name__ == "__main__":
    unittest.main()
