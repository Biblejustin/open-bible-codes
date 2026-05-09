import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import select_all_codes_followup as select
from scripts.triage_surface_all_codes import QUEUE_FIELDNAMES


class SelectAllCodesFollowupTests(unittest.TestCase):
    def test_select_rows_applies_bucket_term_and_dedupe_caps(self) -> None:
        rows = [
            queue_row("q1", "center_word_exact", "alpha_h", "1"),
            queue_row("q1", "center_word_exact", "alpha_h", "2"),
            queue_row("q1", "center_word_exact", "alpha_h", "3"),
            queue_row("q1", "center_verse_exact", "beta_h", "4"),
            queue_row("q2", "center_word_exact", "alpha_h", "1"),
            queue_row("q2", "hidden_path_only", "gamma_h", "5"),
        ]

        selected = select.select_rows(
            rows,
            max_rows_per_queue=3,
            max_rows_per_bucket=2,
            max_rows_per_term=2,
        )

        self.assertEqual(
            [(row["source_queue"], row["bucket"], row["term_id"], row["center_ref"]) for row in selected],
            [
                ("q1", "center_word_exact", "alpha_h", "Test 1:1"),
                ("q1", "center_word_exact", "alpha_h", "Test 1:2"),
                ("q1", "center_verse_exact", "beta_h", "Test 1:4"),
                ("q2", "hidden_path_only", "gamma_h", "Test 1:5"),
            ],
        )
        self.assertEqual([row["selection_rank"] for row in selected], ["1", "2", "3", "4"])

    def test_main_writes_selected_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            queue = root / "queue.csv"
            selected = root / "selected.csv"
            markdown = root / "selection.md"
            manifest = root / "manifest.json"
            write_queue(queue, [queue_row("", "center_word_exact", "alpha_h", "1")])

            exit_code = select.main(
                [
                    "--queue",
                    f"sample={queue}",
                    "--selected-out",
                    str(selected),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(exit_code, 0)
            rows = read_rows(selected)
            self.assertEqual(rows[0]["source_queue"], "sample")
            self.assertEqual(rows[0]["bucket"], "center_word_exact")
            self.assertIn("hidden-path-only rows remain eligible", markdown.read_text(encoding="utf-8"))
            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(data["selected_rows"], 1)
            self.assertEqual(data["selected_by_queue"], {"sample": 1})


def queue_row(source_queue: str, bucket: str, term_id: str, center_suffix: str) -> dict[str, str]:
    row = {field: "" for field in QUEUE_FIELDNAMES}
    row.update(
        {
            "source_queue": source_queue,
            "bucket": bucket,
            "bucket_rank": center_suffix,
            "overall_rank": center_suffix,
            "presence_scope": "all_source",
            "present_corpora": "A,B",
            "corpus_count": "2",
            "corpus_row_count": "2",
            "term_id": term_id,
            "concept": term_id,
            "category": "test",
            "term": term_id,
            "normalized_term": term_id.replace("_h", ""),
            "normalized_length": "5",
            "skip": "2",
            "direction": "forward",
            "span_letters": "9",
            "offsets_by_corpus": "A:1/3/5;B:1/3/5",
            "start_ref": f"Test 1:{center_suffix}",
            "center_ref": f"Test 1:{center_suffix}",
            "end_ref": f"Test 1:{center_suffix}",
            "center_word": term_id,
            "center_normalized_word": term_id,
            "center_words_by_corpus": f"A:{term_id};B:{term_id}",
        }
    )
    return row


def write_queue(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=QUEUE_FIELDNAMES)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in QUEUE_FIELDNAMES} for row in rows])


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
