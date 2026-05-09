import unittest

from scripts.compare_completed_dense_partitions import compare_completed


class CompletedDensePartitionComparisonTests(unittest.TestCase):
    def test_compare_completed_groups_bible_and_control_rows(self) -> None:
        rows = [
            row("KJV", "dyn_christ_e", "complete", 10, 1),
            row("ENG_PG_SHAKESPEARE", "dyn_christ_e", "complete", 30, 3),
            row("ENG_PG_MOBY_DICK", "dyn_christ_e", "partial", 100, 10),
        ]

        compared = compare_completed(rows)

        self.assertEqual(len(compared), 1)
        self.assertEqual(compared[0]["term_id"], "dyn_christ_e")
        self.assertEqual(compared[0]["bible_completed_corpora"], "KJV")
        self.assertEqual(compared[0]["control_completed_corpora"], "ENG_PG_SHAKESPEARE")
        self.assertEqual(compared[0]["bible_completed_hits"], "10")
        self.assertEqual(compared[0]["control_completed_hits"], "30")
        self.assertEqual(compared[0]["control_over_bible_hits_ratio"], "3.0")
        self.assertEqual(compared[0]["control_over_bible_exact_center_ratio"], "3.0")

    def test_compare_completed_marks_control_only_rows(self) -> None:
        compared = compare_completed([row("GRC_PERSEUS_ILIAD", "dyn_gog_g", "complete", 7, 0)])

        self.assertEqual(compared[0]["completion_read"], "completed control dense export available; bible still deferred or absent")
        self.assertEqual(compared[0]["control_completed_hits"], "7")
        self.assertEqual(compared[0]["bible_completed_hits"], "0")


def row(
    corpus: str,
    term_id: str,
    status: str,
    hits: int,
    exact_hits: int,
) -> dict[str, str]:
    return {
        "corpus": corpus,
        "term_id": term_id,
        "mode": "full-span",
        "total_hit_count": str(hits),
        "planned_partitions": "1",
        "completed_partitions": "1" if status == "complete" else "0",
        "completed_exported_hits": str(hits),
        "exact_center_word_hits": str(exact_hits),
        "coverage_status": status,
        "completed_skip_ranges": "2-9",
    }


if __name__ == "__main__":
    unittest.main()
