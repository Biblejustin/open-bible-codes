import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_cities_recovered_pdf_text as audit


GOOD_GANS = """Patterns of Equidistant Letter Sequence Pairs in Genesis
Patterns of Equidistant Letters Sequence Pairs in Genesis
The Linguistic Protocol and Data used for the Communities Experiment
"""

GOOD_AUMANN = """A PERSONAL PERSPECTIVE ON THE WORK OF THE "GANS" COMMITTEE
committee text
"""

GARBLED = """. , : 1 .. 6 .I :R : 18 II :R : 21"""


def recovery_row(label: str, path: Path, status: str = "usable_archived_pdf") -> dict[str, str]:
    return {
        "label": label,
        "source_pages": "cities",
        "url": f"https://example.test/{label}.pdf",
        "selected_source": "archive",
        "selected_path": str(path),
        "pdf_pages": "1",
        "usable_status": status,
    }


class CitiesRecoveredPdfTextAuditTests(unittest.TestCase):
    def test_text_status_classifies_zero_garbled_and_extractable(self) -> None:
        self.assertEqual(audit.text_status("", 0), "zero_extractable_text")
        self.assertEqual(
            audit.text_status(GARBLED, audit.latin_letter_ratio(GARBLED)),
            "extractable_but_garbled_or_nonlatin",
        )
        self.assertEqual(
            audit.text_status(GOOD_GANS, audit.latin_letter_ratio(GOOD_GANS)),
            "extractable_text",
        )

    def test_analyze_row_classifies_family_and_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.pdf"
            path.write_text(GOOD_GANS, encoding="utf-8")
            original_extract = audit.extract_pdf_text
            try:
                audit.extract_pdf_text = lambda pdf: GOOD_GANS  # type: ignore[assignment]
                row = audit.analyze_row(recovery_row("cities_pdf_gans", path))
            finally:
                audit.extract_pdf_text = original_extract  # type: ignore[assignment]

        self.assertEqual(row["family"], "gans_communities")
        self.assertEqual(row["text_status"], "extractable_text")
        self.assertIn("Patterns of Equidistant Letter", row["title_guess"])

    def test_protocol_anchors_find_expected_titles(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            gans = root / "gans.pdf"
            dp1 = root / "dp1.pdf"
            gans.write_text(GOOD_GANS, encoding="utf-8")
            dp1.write_text(GOOD_AUMANN, encoding="utf-8")
            rows = [
                {
                    "label": "cities_pdf_communities_data",
                    "selected_path": str(gans),
                    "title_guess": GOOD_GANS,
                },
                {
                    "label": "cities_pdf_dp_365_1",
                    "selected_path": str(dp1),
                    "title_guess": GOOD_AUMANN,
                },
            ]
            original_extract = audit.extract_pdf_text
            try:
                audit.extract_pdf_text = lambda pdf: Path(pdf).read_text(encoding="utf-8")  # type: ignore[assignment]
                anchors = audit.protocol_anchors(rows)
            finally:
                audit.extract_pdf_text = original_extract  # type: ignore[assignment]

        by_anchor = {row["anchor"]: row for row in anchors}
        self.assertEqual(by_anchor["gans_communities_data_title"]["status"], "found")
        self.assertEqual(by_anchor["aumann_personal_perspective"]["status"], "found")
        self.assertEqual(by_anchor["gans_paper_title"]["status"], "missing")

    def test_main_writes_audit_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.pdf"
            source.write_text(GOOD_GANS, encoding="utf-8")
            recovery = root / "recovery.csv"
            with recovery.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "label",
                        "source_pages",
                        "url",
                        "selected_source",
                        "selected_path",
                        "pdf_pages",
                        "usable_status",
                    ],
                )
                writer.writeheader()
                writer.writerow(recovery_row("cities_pdf_gans", source))
                writer.writerow(recovery_row("missing", source, "no_pdf_recovered"))

            original_extract = audit.extract_pdf_text
            try:
                audit.extract_pdf_text = lambda pdf: GOOD_GANS  # type: ignore[assignment]
                rc = audit.main(
                    [
                        "--recovery-csv",
                        str(recovery),
                        "--out",
                        str(root / "rows.csv"),
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
                audit.extract_pdf_text = original_extract  # type: ignore[assignment]

            self.assertEqual(rc, 0)
            rows = list(csv.DictReader((root / "rows.csv").open(encoding="utf-8")))
            self.assertEqual(len(rows), 1)
            summary = list(csv.DictReader((root / "summary.csv").open(encoding="utf-8")))[0]
            self.assertEqual(summary["recovered_pdf_rows"], "1")
            markdown = (root / "audit.md").read_text(encoding="utf-8")
            self.assertIn("source-shape audit only", markdown)
            self.assertIn("does not run OCR", markdown)
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["rows"], 1)


if __name__ == "__main__":
    unittest.main()
