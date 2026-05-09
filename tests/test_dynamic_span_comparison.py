import unittest

from scripts.compare_dynamic_span_bible_controls import compare


class DynamicSpanComparisonTests(unittest.TestCase):
    def test_compare_uses_normalized_rates_not_raw_counts(self) -> None:
        rows = [
            row(
                corpus="KJV",
                term_id="sample_e",
                mode="full-span",
                term_language="english",
                hit_count="10",
                rate="10.0",
            ),
            row(
                corpus="ENG_PG_SHAKESPEARE",
                term_id="sample_e",
                mode="full-span",
                term_language="english",
                hit_count="100",
                rate="5.0",
            ),
        ]

        compared = compare(rows)

        self.assertEqual(len(compared), 1)
        self.assertEqual(compared[0]["bible_max_rate_per_million"], "10.0")
        self.assertEqual(compared[0]["control_max_rate_per_million"], "5.0")
        self.assertEqual(compared[0]["bible_over_control_max_rate_ratio"], "2.0")
        self.assertEqual(
            compared[0]["read"],
            "bible max rate exceeds all observed controls",
        )


def row(
    *,
    corpus: str,
    term_id: str,
    mode: str,
    term_language: str,
    hit_count: str,
    rate: str,
) -> dict[str, str]:
    return {
        "corpus": corpus,
        "corpus_language": term_language,
        "corpus_letters": "100",
        "term_id": term_id,
        "concept": "Sample",
        "category": "test",
        "term_language": term_language,
        "term": "sample",
        "normalized_term": "sample",
        "normalized_length": "6",
        "mode": mode,
        "min_skip": "2",
        "effective_max_skip": "10",
        "search_space_positions": "1000000",
        "expected_hits": "",
        "expected_hits_per_million_positions": "",
        "direction": "both",
        "forward_count": "",
        "backward_count": "",
        "hit_count": hit_count,
        "hits_per_million_positions": rate,
        "counter_elapsed_seconds": "0.001",
        "status": "counted",
    }


if __name__ == "__main__":
    unittest.main()
