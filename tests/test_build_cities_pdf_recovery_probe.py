import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import build_cities_pdf_recovery_probe as probe


HTML_ONE = """<html><body>
<a href="../experiments/dp364_short.pdf">Aumann report</a>
<a href="../experiments/dp364_appendix_4.pdf">City names</a>
</body></html>"""

HTML_TWO = """<html><body>
<a href="https://www.torah-code.org/experiments/dp364_appendix_4.pdf">dupe</a>
</body></html>"""


def sample_row(label: str, status: str) -> dict[str, object]:
    selected = "live" if status == "usable_live_pdf" else ""
    return {
        "label": label,
        "source_pages": "cities",
        "url": f"https://example.test/{label}.pdf",
        "live_final_url": f"https://example.test/{label}.pdf",
        "live_http_status": 200,
        "live_status": "pdf" if selected else "html",
        "live_kind": "pdf" if selected else "html",
        "live_bytes": 10 if selected else 20,
        "live_sha256": "a" * 64 if selected else "b" * 64,
        "archive_probe_url": "",
        "archive_status": "not_checked" if selected else "no_archived_snapshot",
        "archive_snapshot_source": "",
        "archive_timestamp": "",
        "archive_cdx_checked": False,
        "archive_cdx_candidate_count": 0,
        "archive_raw_url": "",
        "archive_kind": "",
        "archive_bytes": 0,
        "archive_sha256": "",
        "selected_source": selected,
        "selected_path": f"/tmp/{label}.pdf" if selected else "",
        "pdf_pages": "1" if selected else "",
        "pdf_text_chars": "0" if selected else "",
        "usable_status": status,
    }


class CitiesPdfRecoveryProbeTests(unittest.TestCase):
    def test_discover_pdf_sources_resolves_and_dedupes_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = root / "torah_code_experiment_cities_aumann.html"
            b = root / "torah_code_experiment_cities_simon_mckay.html"
            a.write_text(HTML_ONE, encoding="utf-8")
            b.write_text(HTML_TWO, encoding="utf-8")

            rows = probe.discover_pdf_sources([a, b])

        self.assertEqual([row.label for row in rows], [
            "cities_pdf_dp364_appendix_4",
            "cities_pdf_dp364_short",
        ])
        by_label = {row.label: row for row in rows}
        self.assertEqual(
            by_label["cities_pdf_dp364_appendix_4"].url,
            "https://www.torah-code.org/experiments/dp364_appendix_4.pdf",
        )
        self.assertEqual(
            by_label["cities_pdf_dp364_appendix_4"].source_pages,
            (
                "torah_code_experiment_cities_aumann",
                "torah_code_experiment_cities_simon_mckay",
            ),
        )

    def test_archive_candidate_urls_adds_http_variant_for_https(self) -> None:
        self.assertEqual(
            probe.archive_candidate_urls("https://www.torah-code.org/papers/gans.pdf"),
            [
                "https://www.torah-code.org/papers/gans.pdf",
                "http://www.torah-code.org/papers/gans.pdf",
            ],
        )

    def test_build_summary_counts_live_and_missing_rows(self) -> None:
        summary = probe.build_summary(
            [
                sample_row("live", "usable_live_pdf"),
                sample_row("missing", "no_pdf_recovered"),
            ]
        )

        self.assertEqual(summary["pdf_urls_probed"], 2)
        self.assertEqual(summary["live_pdf_rows"], 1)
        self.assertEqual(summary["usable_pdf_rows"], 1)
        self.assertEqual(summary["unrecovered_pdf_rows"], 1)
        self.assertEqual(
            summary["current_pdf_recovery_status"],
            "partial_pdf_sources_recovered",
        )

    def test_main_writes_probe_outputs_with_patched_probe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "inputs"
            input_dir.mkdir()
            html = input_dir / "torah_code_experiment_cities_aumann.html"
            html.write_text(HTML_ONE, encoding="utf-8")

            def fake_probe(source, snapshot_dir, *, refresh):
                return sample_row(source.label, "usable_live_pdf")

            with patch.object(probe, "probe_pdf_source", side_effect=fake_probe):
                rc = probe.main(
                    [
                        "--source-glob",
                        str(input_dir / "*.html"),
                        "--snapshot-dir",
                        str(root / "snapshots"),
                        "--out",
                        str(root / "probe.csv"),
                        "--summary-out",
                        str(root / "summary.csv"),
                        "--markdown-out",
                        str(root / "probe.md"),
                        "--manifest-out",
                        str(root / "manifest.json"),
                    ]
                )

            self.assertEqual(rc, 0)
            rows = list(csv.DictReader((root / "probe.csv").open(encoding="utf-8")))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["usable_status"], "usable_live_pdf")
            markdown = (root / "probe.md").read_text(encoding="utf-8")
            self.assertIn("Cities PDF Recovery Probe", markdown)
            self.assertIn("Recovered PDF bytes are source-shape inputs only", markdown)
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["rows"], 2)

    def test_cdx_snapshots_rejects_non_list_api_root(self) -> None:
        with patch.object(
            probe,
            "fetch_json_with_timeout",
            return_value={"message": "rate limited"},
        ):
            with self.assertRaisesRegex(
                ValueError, "Cities Wayback CDX API JSON root must be a list"
            ):
                probe.cdx_snapshots_with_timeout("https://example.test/source.pdf")


if __name__ == "__main__":
    unittest.main()
