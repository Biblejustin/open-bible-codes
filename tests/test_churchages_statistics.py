import csv
import tempfile
import unittest
from pathlib import Path

from scripts.analyze_churchages_statistics import (
    audit_claim,
    churchages_triangle_positions,
    main,
)


class ChurchAgesStatisticsTests(unittest.TestCase):
    def test_triangle_positions_use_article_axis_formula(self) -> None:
        self.assertEqual(churchages_triangle_positions(100, 5, "forward"), 1000)
        self.assertEqual(churchages_triangle_positions(100, 5, "both"), 2000)

    def test_audit_claim_emits_expected_comparison_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            config = root / "source.toml"
            source.write_text("abababab", encoding="utf-8")
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "english"',
                        "",
                        "[[sources]]",
                        'name = "sample"',
                        'format = "text"',
                        'path = "source.txt"',
                        'ref = "Sample 1:1"',
                    ]
                ),
                encoding="utf-8",
            )

            row = audit_claim(
                {
                    "term_id": "sample_ab",
                    "term": "ab",
                    "corpus": "SAMPLE",
                    "config": str(config),
                    "direction": "forward",
                    "observed_hits": "3",
                    "min_skip": "2",
                    "max_skip_mode": "fixed",
                    "max_skip": "3",
                    "claimed_corpus_letters": "8",
                    "source_url": "",
                    "notes": "",
                },
                {},
            )

        self.assertEqual(row["normalized_term"], "ab")
        self.assertEqual(row["effective_max_skip"], "3")
        self.assertEqual(row["exact_search_space_positions"], "11")
        self.assertEqual(row["observed_hits"], "3")
        self.assertNotEqual(row["churchages_expected_hits"], "")
        self.assertNotEqual(row["exact_expected_hits"], "")

    def test_main_writes_csv_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            config = root / "source.toml"
            claims = root / "claims.csv"
            out = root / "audit.csv"
            markdown = root / "audit.md"
            manifest = root / "audit.json"
            source.write_text("abababab", encoding="utf-8")
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "english"',
                        "",
                        "[[sources]]",
                        'name = "sample"',
                        'format = "text"',
                        'path = "source.txt"',
                        'ref = "Sample 1:1"',
                    ]
                ),
                encoding="utf-8",
            )
            with claims.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "term_id",
                        "term",
                        "corpus",
                        "config",
                        "direction",
                        "observed_hits",
                        "min_skip",
                        "max_skip_mode",
                        "max_skip",
                        "claimed_corpus_letters",
                        "source_url",
                        "notes",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "term_id": "sample_ab",
                        "term": "ab",
                        "corpus": "SAMPLE",
                        "config": str(config),
                        "direction": "forward",
                        "observed_hits": "3",
                        "min_skip": "2",
                        "max_skip_mode": "fixed",
                        "max_skip": "3",
                        "claimed_corpus_letters": "8",
                        "source_url": "",
                        "notes": "",
                    }
                )

            code = main(
                [
                    "--claims",
                    str(claims),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )
            markdown_text = markdown.read_text(encoding="utf-8")
            output_rows = list(csv.DictReader(out.open(newline="")))

            self.assertEqual(code, 0)
            self.assertIn("ChurchAges Statistics Audit", markdown_text)
            self.assertEqual(len(output_rows), 1)


if __name__ == "__main__":
    unittest.main()
