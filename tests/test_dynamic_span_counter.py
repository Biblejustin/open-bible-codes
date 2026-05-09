import os
import shutil
import unittest

from els.search import count_els_text
from scripts.run_dynamic_span_counter import DEFAULT_BINARY, build_binary, run_counter


class DynamicSpanCounterTests(unittest.TestCase):
    def test_compiled_counter_matches_reference_for_dynamic_modes(self) -> None:
        compiler = os.environ.get("CXX", "clang++")
        if shutil.which(compiler) is None:
            self.skipTest(f"{compiler} not available")

        text = "αβγαβγαβγ"
        query = "αβγ"
        terms = [{"term_id": "sample", "normalized_term": query}]
        binary = build_binary(DEFAULT_BINARY)

        letters_rows = run_counter(
            binary,
            text,
            terms,
            min_skip=1,
            mode="letters-per-term",
            direction="both",
        )
        full_rows = run_counter(
            binary,
            text,
            terms,
            min_skip=1,
            mode="full-span",
            direction="both",
        )

        letters_max = len(text) // len(query)
        full_max = (len(text) - 1) // (len(query) - 1)

        self.assertEqual(
            int(letters_rows[0]["hit_count"]),
            count_els_text(text, query, min_skip=1, max_skip=letters_max, direction="both"),
        )
        self.assertEqual(
            int(full_rows[0]["hit_count"]),
            count_els_text(text, query, min_skip=1, max_skip=full_max, direction="both"),
        )
        self.assertGreaterEqual(int(full_rows[0]["hit_count"]), int(letters_rows[0]["hit_count"]))


if __name__ == "__main__":
    unittest.main()
