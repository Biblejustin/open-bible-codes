import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.analyze_broad_search import (
    focus_counts,
    read_count_rows,
    read_label,
    ratio_cell,
    write_markdown,
)


class BroadSearchTests(unittest.TestCase):
    def test_ratio_cell_handles_zero_baseline(self) -> None:
        self.assertEqual(ratio_cell(10, 0), "")
        self.assertEqual(ratio_cell(15, 10), "1.5")

    def test_read_label_flags_absent_and_short_forms(self) -> None:
        self.assertEqual(
            read_label({"hit_count": "0", "normalized_length": "6"}),
            "absent at this range",
        )
        self.assertEqual(
            read_label({"hit_count": "25", "normalized_length": "3"}),
            "high-noise short form",
        )

    def test_read_count_rows_ignores_generated_top_counts(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_count_csv(root / "modern_names_dates_counts.csv", "trump_h")
            (root / "modern_names_dates_counts.manifest.json").write_text("{}", encoding="utf-8")
            write_count_csv(root / "wide_focus_top_counts.csv", "noise")

            rows = read_count_rows(root)

        self.assertEqual([row["term_id"] for row in rows], ["trump_h"])

    def test_focus_rows_include_target_control_columns(self) -> None:
        rows = focus_counts(
            [
                {
                    "term_set": "modern_names_dates",
                    "corpus": "MT_WLC",
                    "term_id": "trump_h",
                    "concept": "Trump",
                    "category": "modern_names",
                    "term_language": "hebrew",
                    "term": "טראמפ",
                    "normalized_term": "טראמפ",
                    "normalized_length": "5",
                    "hit_count": "1",
                    "status": "counted",
                }
            ]
        )

        self.assertEqual(rows[0]["term_language"], "hebrew")
        self.assertEqual(rows[0]["term"], "טראמפ")

    def test_write_markdown_displays_original_language_terms(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            counts_dir = root / "counts"
            counts_dir.mkdir()
            (counts_dir / "broad_search.manifest.json").write_text(
                '{"min_skip":2,"max_skip":100,"direction":"both","term_sets":["set"]}',
                encoding="utf-8",
            )
            out = root / "broad.md"

            write_markdown(
                out,
                [
                    {
                        "term_set": "set",
                        "corpus": "LXX",
                        "counted_rows": 1,
                        "zero_rows": 0,
                        "total_hits": 7,
                        "max_term_id": "isaac_g",
                        "max_concept": "Isaac",
                        "max_normalized_term": "ισαακ",
                        "max_hit_count": 7,
                    }
                ],
                [
                    {
                        "rank": 1,
                        "term_set": "set",
                        "corpus": "LXX",
                        "term_id": "isaac_g",
                        "concept": "Isaac",
                        "normalized_term": "ισαακ",
                        "normalized_length": 5,
                        "hit_count": 7,
                        "read": "screen only",
                    }
                ],
                [],
                [],
                type(
                    "Args",
                    (),
                    {
                        "counts_dir": counts_dir,
                        "min_top_length": 4,
                    },
                )(),
            )

            self.assertIn("`ισαακ` (Isaak; English: Isaac)", out.read_text(encoding="utf-8"))


def write_count_csv(path: Path, term_id: str) -> None:
    path.write_text(
        "corpus,term_id,concept,category,term_language,normalized_term,normalized_length,hit_count,status\n"
        f"MT_WLC,{term_id},Trump,modern,hebrew,טראמפ,5,1,counted\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
