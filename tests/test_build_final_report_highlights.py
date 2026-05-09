import csv
import tempfile
import unittest
from pathlib import Path

from scripts.build_final_report_highlights import build_highlights, main


class FinalReportHighlightsTests(unittest.TestCase):
    def test_build_highlights_prefers_gog_source_review(self) -> None:
        rows = [
            {
                "summary_rank": "2",
                "occurrence_type": "centered_self_exact_word",
                "source_family": "original_language_findings",
                "corpus_class": "bible",
                "normalized_term": "γωγ",
                "center_ref": "REV 20:8",
                "center_word": "Γὼγ",
                "corpora": "TCG_NT",
                "total_paths": "4",
                "frequency_reads": "promote",
                "control_reads": "",
                "context_excerpt": "Gog context",
            },
            {
                "summary_rank": "1",
                "occurrence_type": "centered_self_exact_word",
                "source_family": "gog_source_review",
                "corpus_class": "bible",
                "normalized_term": "γωγ",
                "center_ref": "REV 20:8",
                "center_word": "Gog",
                "corpora": "BYZ_NT;SBLGNT;TCG_NT;TR_NT",
                "total_paths": "14",
                "frequency_reads": "length-3 matched-control rank desc 25/asc 1; not frequency-promoted",
                "control_reads": "controls above target",
                "context_excerpt": "Rev 20:8 Gog/Magog context",
            },
        ]

        highlights = build_highlights(rows, limit=10)

        self.assertEqual(highlights[0]["source_family"], "gog_source_review")
        self.assertEqual(highlights[0]["status"], "contextual_occurrence_frequency_cautioned")

    def test_main_writes_csv_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            centered = root / "presence.csv"
            claims = root / "claims.csv"
            out = root / "out.csv"
            markdown = root / "out.md"
            manifest = root / "manifest.json"
            with centered.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "summary_rank",
                        "occurrence_type",
                        "source_family",
                        "corpus_class",
                        "normalized_term",
                        "center_ref",
                        "center_word",
                        "corpora",
                        "total_paths",
                        "frequency_reads",
                        "control_reads",
                        "context_excerpt",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "summary_rank": "1",
                        "occurrence_type": "centered_self_exact_word",
                        "source_family": "gog_source_review",
                        "corpus_class": "bible",
                        "normalized_term": "γωγ",
                        "center_ref": "REV 20:8",
                        "center_word": "Gog",
                        "corpora": "TR_NT",
                        "total_paths": "4",
                        "frequency_reads": "not frequency-promoted",
                        "control_reads": "control read",
                        "context_excerpt": "context",
                    }
                )
            with claims.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "claim_id",
                        "status",
                        "current_reproduction",
                        "evidence",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "claim_id": "gog",
                        "status": "controlled_review_candidate",
                        "current_reproduction": "review",
                        "evidence": "docs/CENTERED_OCCURRENCE_INDEX.md",
                    }
                )

            code = main(
                [
                    "--centered-summary",
                    str(centered),
                    "--claim-catalog",
                    str(claims),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(code, 0)
            self.assertIn("γωγ", out.read_text(encoding="utf-8"))
            self.assertIn("Final Report Highlights", markdown.read_text(encoding="utf-8"))
            self.assertIn("build_final_report_highlights", manifest.read_text(encoding="utf-8"))
