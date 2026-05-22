import csv
import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts import analyze_wrr_zero_hit_variant_probe as probe


class WrrZeroHitVariantProbeTests(unittest.TestCase):
    def test_generate_variants_includes_deletion_and_aleph_ayin_swap(self) -> None:
        variants = dict(probe.generate_variants(")WY("))

        self.assertEqual(variants["original"], ")WY(")
        self.assertEqual(variants["delete_mater@2"], ")Y(")
        self.assertEqual(variants["delete_mater@3"], ")W(")
        self.assertEqual(variants["swap_aleph_ayin@1"], "(WY(")
        self.assertEqual(variants["swap_ayin_aleph@4"], ")WY)")

    def test_main_writes_variant_summary_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            config = root / "config.toml"
            counts = root / "counts.csv"
            row_ocr = root / "row_ocr.csv"
            out = root / "out.csv"
            summary = root / "summary.csv"
            markdown = root / "out.md"
            manifest = root / "manifest.json"

            source.write_text("ABC\n", encoding="utf-8")
            config.write_text(
                textwrap.dedent(
                    f"""
                    name = "tiny"
                    language = "michigan"

                    [[sources]]
                    name = "tiny"
                    format = "text"
                    path = "{source}"
                    book = "Genesis"
                    book_number = 1
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
            write_csv(
                counts,
                [
                    {
                        "term_id": "t1",
                        "concept": "WRR2 01",
                        "category": "wrr_appellation",
                        "term": "ABXC",
                        "normalized_term": ")BXC",
                        "hit_count": "0",
                        "status": "counted",
                    }
                ],
            )
            write_csv(
                row_ocr,
                [
                    {
                        "term_id": "t1",
                        "row_ocr_status": "matched",
                    }
                ],
            )

            rc = probe.main(
                [
                    "--config",
                    str(config),
                    "--counts",
                    str(counts),
                    "--row-ocr",
                    str(row_ocr),
                    "--min-skip",
                    "1",
                    "--max-skip",
                    "1",
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            detail_rows = list(csv.DictReader(out.open(encoding="utf-8")))
            self.assertEqual(detail_rows[0]["variant_rule"], "delete_one@3")
            self.assertEqual(detail_rows[0]["variant_normalized"], ")BC")
            self.assertEqual(detail_rows[0]["variant_hit_count"], "1")
            summary_rows = list(csv.DictReader(summary.open(encoding="utf-8")))
            self.assertEqual(summary_rows[0]["terms_with_variant_hit"], "1")
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("WRR Zero-Hit Variant Probe", text)
            self.assertTrue(manifest.exists())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
