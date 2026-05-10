import unittest
from argparse import Namespace
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.analyze_apocrypha_bridge_candidates import (
    classify_bridge,
    hit_positions,
    letter_path_positions,
    rank_bridge_rows,
    write_markdown,
)


class ApocryphaBridgeCandidateTests(unittest.TestCase):
    def test_hit_positions_follow_signed_skip(self) -> None:
        self.assertEqual(hit_positions(10, 3, 4), [10, 13, 16, 19])
        self.assertEqual(hit_positions(10, -3, 4), [10, 7, 4, 1])

    def test_classify_bridge(self) -> None:
        self.assertEqual(
            classify_bridge(["canonical", "canonical", "apocrypha"]),
            "canonical_to_apocrypha",
        )
        self.assertEqual(
            classify_bridge(["apocrypha", "canonical"]),
            "apocrypha_to_canonical",
        )
        self.assertEqual(
            classify_bridge(["canonical", "apocrypha", "canonical"]),
            "multi_segment_bridge",
        )

    def test_rank_bridge_rows_uses_skip_order_after_parallel_collection(self) -> None:
        rows = [
            {
                "rank": 0,
                "skip": -10,
                "start_ref": "TOB 1:1",
                "end_ref": "MAL 4:6",
                "normalized_term": "bbb",
                "class_path": "AAC",
            },
            {
                "rank": 0,
                "skip": 5,
                "start_ref": "MAL 4:6",
                "end_ref": "TOB 1:1",
                "normalized_term": "aaa",
                "class_path": "CCA",
            },
        ]

        ranked = rank_bridge_rows(rows)

        self.assertEqual([row["skip"] for row in ranked], [5, -10])
        self.assertEqual([row["rank"] for row in ranked], [1, 2])

    def test_letter_path_positions_extracts_offsets(self) -> None:
        self.assertEqual(
            letter_path_positions("1:a@MAL 4:6:canonical:10;2:b@TOB 1:1:apocrypha:15"),
            [10, 15],
        )

    def test_write_markdown_displays_original_language_terms(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "candidates.md"
            args = Namespace(
                corpus_label="LXX",
                config=Path("configs/example.toml"),
                terms=[Path("terms/example.csv")],
                min_skip=2,
                max_skip=250,
                direction="both",
                min_term_length=4,
                jobs=1,
                out=root / "rows.csv",
                summary_out=root / "summary.csv",
                markdown_out=out,
                manifest_out=root / "manifest.json",
            )

            write_markdown(
                out,
                [
                    {
                        "rank": 1,
                        "bridge_type": "canonical_to_apocrypha",
                        "normalized_term": "μαρια",
                        "skip": 29,
                        "start_ref": "MAL 4:6",
                        "center_ref": "MAL 4:6",
                        "end_ref": "TOB 1:1",
                        "apocrypha_books": "TOB",
                        "class_path": "CCCAA",
                    }
                ],
                [{"metric": "bridge_rows", "value": 1}],
                args,
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("`μαρια` (Maria; English: Mary)", text)
