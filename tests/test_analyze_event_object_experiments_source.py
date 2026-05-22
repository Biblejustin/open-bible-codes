import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_event_object_experiments_source as audit


SONS_MAIN = """<html><head><title>Sons of Haman</title></head><body>
The results were not statistically significant.
</body></html>"""

SONS_DATA = """<html><body>
Key Word List
\u05d9\u05d2\u05d1 \u05d0\u05d3\u05e8 \u05e4\u05d5\u05e8\u05d9\u05dd
\u05e4\u05e8\u05e9\u05e0\u05d3\u05ea\u05d0
Experimental Protocol
Text The Five Books of Moses; the Chumash
Skip Specification Expected Number of ELS = 10
Compactness Measure Maximum distance between the letters of an ELS pair
Number of Trials 10,000
The p-value of the experiment was 16.5/10,000.
</body></html>"""

PUMBEDITA_HTML = """<html><body>
Experimental Protocol
Expected Number of ELS = 10
Compactness Measure Maximum distance between the letters of an ELS pair
The experiment failed to produce any statistically significant results.
</body></html>"""

AUSCHWITZ_HTML = """<html><body>
Witztum stated that the probability due to chance was 1/1,000,000.
Experimental Protocol
Expected Number of ELS = 10
Compactness Measure Maximum distance between the letters of an ELS pair
The test of hypothesis failed to produce statistically significant results.
</body></html>"""

ARK_HTML = """<html><body>
<img src="../widgets/underconstruction1.gif">
<a href="../experiments/ark_code_1.pdf">tutorial</a>
</body></html>"""

PUMBEDITA_PDF_TEXT = "\n".join(f"{i} Name{i} hebrew" for i in range(1, 21))
AUSCHWITZ_PDF_TEXT = "\n".join(f"{i} Camp{i} hebrew" for i in range(1, 33))
ARK_PDF_TEXT = "Ark Code tutorial"


class EventObjectExperimentSourceTests(unittest.TestCase):
    def test_count_numbered_pdf_rows(self) -> None:
        texts = [
            audit.SourceText(
                path=Path("torah_code_experiment_pumbedita_data.pdf"),
                experiment="pumbedita",
                raw_text=PUMBEDITA_PDF_TEXT,
                plain_text=PUMBEDITA_PDF_TEXT,
            )
        ]

        self.assertEqual(audit.count_numbered_pdf_rows(texts, "pumbedita"), 20)

    def test_event_object_data_rows_extract_keywords_and_pdf_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rows, texts = self.build_sample_sources(Path(tmp))
            del rows
            data_rows = audit.event_object_data_rows(texts)

        self.assertEqual(len(data_rows), 54)
        self.assertEqual(data_rows[0]["experiment"], "sons_of_haman")
        self.assertEqual(data_rows[0]["source_table"], "sons_of_haman_keyword_list")
        self.assertEqual(data_rows[2]["source_table"], "pumbedita_amoraim")
        self.assertEqual(data_rows[-1]["source_table"], "auschwitz_subcamp_keywords")

    def test_protocol_anchors_find_expected_declared_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rows, texts = self.build_sample_sources(root)
            status_rows = audit.build_status_rows(rows, texts)
            summary = audit.build_summary(rows, status_rows)
            anchors = audit.protocol_anchors(texts, status_rows, summary)

            self.assertEqual({row["status"] for row in anchors}, {"found"})

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_paths = self.write_sample_files(root)
            original_pdfinfo = audit.pdfinfo_pages
            original_pdftotext = audit.pdftotext
            try:
                audit.pdfinfo_pages = self.fake_pdfinfo_pages  # type: ignore[assignment]
                audit.pdftotext = self.fake_pdftotext  # type: ignore[assignment]
                args = []
                for source in source_paths:
                    args.extend(["--source", str(source)])
                rc = audit.main(
                    [
                        *args,
                        "--out",
                        str(root / "files.csv"),
                        "--status-out",
                        str(root / "status.csv"),
                        "--data-rows-out",
                        str(root / "data_rows.csv"),
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
                audit.pdfinfo_pages = original_pdfinfo  # type: ignore[assignment]
                audit.pdftotext = original_pdftotext  # type: ignore[assignment]

            self.assertEqual(rc, 0)
            summary_rows = list(csv.DictReader((root / "summary.csv").open(encoding="utf-8")))
            self.assertEqual(summary_rows[0]["source_files"], "8")
            self.assertEqual(summary_rows[0]["sons_of_haman_keyword_rows"], "2")
            self.assertEqual(summary_rows[0]["pumbedita_rows"], "20")
            self.assertEqual(summary_rows[0]["auschwitz_rows"], "32")
            self.assertEqual(summary_rows[0]["machine_data_rows"], "54")
            markdown = (root / "audit.md").read_text(encoding="utf-8")
            self.assertIn("source-shape audit only", markdown)
            self.assertIn("machine data rows extracted | 54", markdown)
            self.assertIn("Found anchors: 10 of 10", markdown)
            self.assertTrue((root / "data_rows.csv").exists())
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["sources"]), 8)

    def build_sample_sources(
        self,
        root: Path,
    ) -> tuple[list[dict[str, object]], list[audit.SourceText]]:
        source_paths = self.write_sample_files(root)
        original_pdfinfo = audit.pdfinfo_pages
        original_pdftotext = audit.pdftotext
        try:
            audit.pdfinfo_pages = self.fake_pdfinfo_pages  # type: ignore[assignment]
            audit.pdftotext = self.fake_pdftotext  # type: ignore[assignment]
            return audit.analyze_sources(source_paths)
        finally:
            audit.pdfinfo_pages = original_pdfinfo  # type: ignore[assignment]
            audit.pdftotext = original_pdftotext  # type: ignore[assignment]

    def write_sample_files(self, root: Path) -> list[Path]:
        files = {
            "torah_code_experiment_sons_of_haman.html": SONS_MAIN,
            "torah_code_experiment_sons_of_haman_data.html": SONS_DATA,
            "torah_code_experiment_pumbedita.html": PUMBEDITA_HTML,
            "torah_code_experiment_auschwitz.html": AUSCHWITZ_HTML,
            "torah_code_experiment_ark.html": ARK_HTML,
        }
        paths = []
        for name, text in files.items():
            path = root / name
            path.write_text(text, encoding="utf-8")
            paths.append(path)
        for name in [
            "torah_code_experiment_pumbedita_data.pdf",
            "torah_code_experiment_auschwitz_data.pdf",
            "torah_code_experiment_ark_code.pdf",
        ]:
            path = root / name
            path.write_bytes(b"%PDF-1.4\n")
            paths.append(path)
        return paths

    def fake_pdfinfo_pages(self, path: Path) -> str:
        if "ark_code" in path.name:
            return "57"
        return "1"

    def fake_pdftotext(self, path: Path) -> str:
        if "pumbedita" in path.name:
            return PUMBEDITA_PDF_TEXT
        if "auschwitz" in path.name:
            return AUSCHWITZ_PDF_TEXT
        return ARK_PDF_TEXT


if __name__ == "__main__":
    unittest.main()
