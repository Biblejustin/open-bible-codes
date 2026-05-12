import csv
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.build_apocrypha_bridge_completion_review import (
    build_completion_rows,
    main,
    parse_input_spec,
    parse_letter_path,
)


class ApocryphaBridgeCompletionReviewTests(unittest.TestCase):
    def test_parse_letter_path_preserves_refs_with_colons(self) -> None:
        steps = parse_letter_path("1:a@MAL 4:6:canonical:10;2:b@TOB 1:1:apocrypha:15")

        self.assertEqual(steps[0].ref, "MAL 4:6")
        self.assertEqual(steps[1].ref, "TOB 1:1")
        self.assertEqual(steps[1].source_class, "apocrypha")

    def test_build_completion_rows_marks_canonical_partial_and_apocrypha_completion(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidates = root / "bridge_candidates.csv"
            write_candidate_csv(candidates)

            rows = build_completion_rows([parse_input_spec(f"LXX={candidates}")])

        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["canonical_only_complete"], "no")
        self.assertEqual(row["expanded_stream_complete"], "yes")
        self.assertEqual(row["canonical_partial_pattern"], "ab.")
        self.assertEqual(row["apocrypha_completion_pattern"], "..c")
        self.assertEqual(row["canonical_letter_indexes"], "1;2")
        self.assertEqual(row["apocrypha_completion_indexes"], "3")

    def test_main_writes_review_outputs(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidates = root / "bridge_candidates.csv"
            out = root / "rows.csv"
            summary = root / "summary.csv"
            markdown = root / "review.md"
            manifest = root / "manifest.json"
            write_candidate_csv(candidates)

            exit_code = main(
                [
                    "--input",
                    f"LXX={candidates}",
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
            manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
            markdown_text = markdown.read_text(encoding="utf-8")

        self.assertEqual(exit_code, 0)
        self.assertEqual(manifest_payload["row_count"], 1)
        self.assertIn("Apocrypha Bridge Completion Review", markdown_text)
        self.assertIn("`ab.`", markdown_text)


def write_candidate_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "rank",
                "term_ids",
                "concepts",
                "categories",
                "normalized_term",
                "term_length",
                "skip",
                "direction",
                "bridge_type",
                "start_ref",
                "center_ref",
                "end_ref",
                "apocrypha_books",
                "class_path",
                "letter_path",
                "center_word",
                "center_normalized_word",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "rank": "1",
                "term_ids": "sample",
                "concepts": "Sample",
                "categories": "test",
                "normalized_term": "abc",
                "term_length": "3",
                "skip": "5",
                "direction": "forward",
                "bridge_type": "canonical_to_apocrypha",
                "start_ref": "MAL 4:6",
                "center_ref": "MAL 4:6",
                "end_ref": "TOB 1:1",
                "apocrypha_books": "TOB",
                "class_path": "CCA",
                "letter_path": "1:a@MAL 4:6:canonical:10;2:b@MAL 4:6:canonical:15;3:c@TOB 1:1:apocrypha:20",
                "center_word": "sample",
                "center_normalized_word": "sample",
            }
        )


if __name__ == "__main__":
    unittest.main()
