import unittest

from scripts.build_broad_bible_control_findings import (
    compare_rows,
    corpus_class,
    distinct_terms,
    read_label,
)


class BroadBibleControlFindingsTests(unittest.TestCase):
    def test_corpus_class_uses_non_bible_marker(self) -> None:
        self.assertEqual(corpus_class({"name": "Non-Bible Greek Control: Herodotus"}), "control")
        self.assertEqual(corpus_class({"name": "SBL Greek New Testament"}), "bible")

    def test_compare_rows_normalizes_by_search_space(self) -> None:
        rows = [
            count_row("BIBLE", "8"),
            count_row("CONTROL", "4"),
        ]
        corpus_meta = {
            "BIBLE": {"name": "Tiny Bible", "letters": 20},
            "CONTROL": {"name": "Non-Bible Tiny Control", "letters": 20},
        }
        manifest = {"min_skip": 1, "max_skip": 2, "direction": "both", "corpora": []}

        output = compare_rows(rows, corpus_meta, manifest)

        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["bible_max_corpus"], "BIBLE")
        self.assertEqual(output[0]["control_max_corpus"], "CONTROL")
        self.assertEqual(output[0]["bible_over_control_max_rate_ratio"], "2.0")

    def test_read_label_marks_low_count_queue_rows(self) -> None:
        bible = {"hit_count": 1, "search_space": 100}
        control = {"hit_count": 0, "search_space": 100}

        self.assertEqual(
            read_label(bible, control, 0.0),
            "Bible-over-control low-count queue row",
        )

    def test_distinct_terms_deduplicates_same_normalized_concept(self) -> None:
        rows = [
            {"term_language": "english", "normalized_term": "john", "concept": "John", "term_id": "john_1"},
            {"term_language": "english", "normalized_term": "john", "concept": "John", "term_id": "john_2"},
            {"term_language": "english", "normalized_term": "john", "concept": "John Apostle", "term_id": "john_3"},
        ]

        deduped = distinct_terms(rows)

        self.assertEqual([row["term_id"] for row in deduped], ["john_1", "john_3"])


def count_row(corpus: str, hits: str) -> dict[str, str]:
    return {
        "corpus": corpus,
        "corpus_language": "greek",
        "term_set": "set",
        "term_id": "term_g",
        "concept": "Term",
        "category": "category",
        "term_language": "greek",
        "term": "λογος",
        "normalized_term": "λογοσ",
        "normalized_length": "5",
        "min_skip": "1",
        "max_skip": "2",
        "direction": "both",
        "hit_count": hits,
        "status": "counted",
    }


if __name__ == "__main__":
    unittest.main()
