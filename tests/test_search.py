import random
import unittest

from els.corpus import Corpus, VerseSpan, WordSpan
from els.search import (
    AhoAutomaton,
    count_els_text_at_positions,
    count_els_terms_by_lanes,
    count_els_text,
    count_els_text_by_lanes,
    find_els,
    find_els_terms,
    iter_els_query_matches_by_lanes,
    iter_matches_at_positions,
    iter_skips,
    positions_of,
    select_process_start_method,
)


def sample_corpus() -> Corpus:
    verse = VerseSpan(
        source="test",
        ref="Test 1:1",
        book="Test",
        chapter="1",
        verse="1",
        raw_text="αβγδεζηθ",
        norm_start=0,
        norm_end=7,
        norm_length=8,
    )
    words = (
        WordSpan("test", "Test 1:1", "Test", "1", "1", 1, "αβ", "αβ", 0, 1, 2),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 2, "γδ", "γδ", 2, 3, 2),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 3, "εζ", "εζ", 4, 5, 2),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 4, "ηθ", "ηθ", 6, 7, 2),
    )
    return Corpus(
        name="test",
        language="greek",
        keep_hebrew_final_forms=False,
        text="αβγδεζηθ",
        verses=(verse,),
        position_to_verse=tuple(0 for _ in range(8)),
        words=words,
        position_to_word=(0, 0, 1, 1, 2, 2, 3, 3),
    )


class SearchTests(unittest.TestCase):
    def test_skip_iteration(self) -> None:
        self.assertEqual(list(iter_skips(2, 3, "both")), [2, -2, 3, -3])

    def test_find_forward_els(self) -> None:
        hits = list(find_els(sample_corpus(), "αγε", min_skip=2, max_skip=2))
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].sequence, "αγε")
        self.assertEqual(hits[0].skip, 2)
        self.assertEqual(hits[0].direction, "forward")
        self.assertEqual(hits[0].center_ref, "Test 1:1")
        self.assertEqual(hits[0].center_word_index, 2)
        self.assertEqual(hits[0].center_word, "γδ")

    def test_find_backward_els_has_center_word(self) -> None:
        hits = list(
            find_els(
                sample_corpus(),
                "εγα",
                min_skip=2,
                max_skip=2,
                direction="backward",
            )
        )
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].direction, "backward")
        self.assertEqual(hits[0].center_word_index, 2)
        self.assertEqual(hits[0].center_word, "γδ")

    def test_find_els_preserves_start_order_with_max_hits(self) -> None:
        corpus = Corpus(
            name="ordered",
            language="greek",
            keep_hebrew_final_forms=False,
            text="δαγαβδβ",
            verses=(
                VerseSpan("test", "Test 1:1", "Test", "1", "1", "", 0, 6, 7),
            ),
            position_to_verse=tuple(0 for _ in range(7)),
        )

        forward = list(
            find_els(
                corpus,
                "αβ",
                min_skip=3,
                max_skip=3,
                direction="forward",
                max_hits=1,
            )
        )
        backward = list(
            find_els(
                corpus,
                "βα",
                min_skip=3,
                max_skip=3,
                direction="backward",
                max_hits=1,
            )
        )

        self.assertEqual(
            (forward[0].start_offset, forward[0].end_offset),
            (1, 4),
        )
        self.assertEqual(
            (backward[0].start_offset, backward[0].end_offset),
            (4, 1),
        )

    def test_count_backward_els(self) -> None:
        self.assertEqual(
            count_els_text(
                "αβγδε",
                "εγα",
                min_skip=2,
                max_skip=2,
                direction="backward",
            ),
            1,
        )

    def test_lane_count_matches_position_count(self) -> None:
        text = "abcxabcyabc"
        for query in ["abc", "ac", "cba", "b"]:
            self.assertEqual(
                count_els_text_by_lanes(text, query, min_skip=1, max_skip=4),
                count_els_text_at_positions(
                    text,
                    query,
                    positions_of(text, query[0]),
                    min_skip=1,
                    max_skip=4,
                    direction="both",
                ),
            )

    def test_multi_term_lane_count_matches_single_term_count(self) -> None:
        text = "abcxabcyabc"
        queries = ["abc", "ac", "cba", "b"]

        counts = count_els_terms_by_lanes(text, queries, min_skip=1, max_skip=4)

        self.assertEqual(
            counts,
            {
                query: count_els_text(text, query, min_skip=1, max_skip=4)
                for query in queries
            },
        )

    def test_parallel_multi_term_count_matches_serial_count(self) -> None:
        text = "abcxabcyabcabcxyzcba"
        queries = ["abc", "ac", "cba", "b"]

        serial = count_els_terms_by_lanes(text, queries, min_skip=1, max_skip=6)
        parallel = count_els_terms_by_lanes(
            text,
            queries,
            min_skip=1,
            max_skip=6,
            jobs=2,
        )

        self.assertEqual(parallel, serial)

    def test_skip_chunks_are_round_robin_balanced(self) -> None:
        from els.search import chunk_skip_values

        self.assertEqual(
            chunk_skip_values(2, 9, 3),
            [(2, 5, 8), (3, 6, 9), (4, 7)],
        )

    def test_start_method_prefers_fork_on_linux(self) -> None:
        self.assertEqual(
            select_process_start_method(("spawn", "forkserver", "fork"), "linux"),
            "fork",
        )

    def test_start_method_prefers_forkserver_on_macos(self) -> None:
        self.assertEqual(
            select_process_start_method(("spawn", "forkserver", "fork"), "darwin"),
            "forkserver",
        )

    def test_start_method_uses_spawn_on_macos_without_forkserver(self) -> None:
        self.assertEqual(
            select_process_start_method(("spawn", "fork"), "darwin"),
            "spawn",
        )

    def test_start_method_prefers_spawn_on_other_platforms(self) -> None:
        self.assertEqual(
            select_process_start_method(("fork", "spawn"), "win32"),
            "spawn",
        )

    def test_start_method_returns_none_without_known_methods(self) -> None:
        self.assertIsNone(select_process_start_method(("custom",), "unknown"))

    def test_aho_find_outputs(self) -> None:
        automaton = AhoAutomaton()
        automaton.add("abc", "abc")
        automaton.add("bc", "bc")
        automaton.add("zzz", "zzz")
        automaton.build()

        self.assertEqual(automaton.find_outputs("xxabcx"), {"abc", "bc"})

    def test_aho_scan_counts_overlaps_and_rebuild_is_stable(self) -> None:
        automaton = AhoAutomaton()
        automaton.add("aa", "aa")
        automaton.add("aaa", "aaa")
        automaton.build()
        automaton.build()
        counts = {"aa": 0, "aaa": 0}

        automaton.scan("xaaa", counts)

        self.assertEqual(counts, {"aa": 2, "aaa": 1})

    def test_aho_encoded_stride_matches_string_scan(self) -> None:
        automaton = AhoAutomaton()
        automaton.add("ab", "ab")
        automaton.add("ba", "ba")
        automaton.build()
        string_counts = {"ab": 0, "ba": 0}
        encoded_counts = {"ab": 0, "ba": 0}

        automaton.scan("xababa", string_counts)
        automaton.scan_encoded_stride(automaton.encode_text("xababa"), encoded_counts)

        self.assertEqual(encoded_counts, string_counts)

    def test_fast_count_matches_position_reference_on_larger_text(self) -> None:
        rng = random.Random(20260503)
        alphabet = "αβγδεζηθ"
        text = "".join(rng.choice(alphabet) for _ in range(5000))

        for query in ("αβγ", "δε", "ηθα", "α"):
            expected = count_els_text_at_positions(
                text,
                query,
                positions_of(text, query[0]),
                min_skip=1,
                max_skip=12,
                direction="both",
            )
            self.assertEqual(
                count_els_text_by_lanes(text, query, min_skip=1, max_skip=12),
                expected,
            )
            self.assertEqual(
                count_els_text(text, query, min_skip=1, max_skip=12),
                expected,
            )

    def test_find_els_matches_position_reference(self) -> None:
        rng = random.Random(20260503)
        alphabet = "αβγδε"
        text = "".join(rng.choice(alphabet) for _ in range(500))
        corpus = Corpus(
            name="random",
            language="greek",
            keep_hebrew_final_forms=False,
            text=text,
            verses=(
                VerseSpan(
                    "test",
                    "Test 1:1",
                    "Test",
                    "1",
                    "1",
                    text,
                    0,
                    len(text) - 1,
                    len(text),
                ),
            ),
            position_to_verse=tuple(0 for _ in text),
        )

        for query in ("αβγ", "δε", "εδ", "α"):
            expected = sorted(
                (skip, start, end)
                for skip in iter_skips(1, 8, "both")
                for start, end in _reference_matches(
                    text,
                    query,
                    skip,
                )
            )
            actual = sorted(
                (hit.skip, hit.start_offset, hit.end_offset)
                for hit in find_els(corpus, query, min_skip=1, max_skip=8)
            )
            self.assertEqual(actual, expected)

    def test_bulk_find_els_matches_per_term_find(self) -> None:
        rng = random.Random(20260504)
        alphabet = "αβγδε"
        text = "".join(rng.choice(alphabet) for _ in range(500))
        corpus = Corpus(
            name="random",
            language="greek",
            keep_hebrew_final_forms=False,
            text=text,
            verses=(
                VerseSpan(
                    "test",
                    "Test 1:1",
                    "Test",
                    "1",
                    "1",
                    text,
                    0,
                    len(text) - 1,
                    len(text),
                ),
            ),
            position_to_verse=tuple(0 for _ in text),
        )
        terms = ("αβγ", "δε", "εδ", "α")

        expected = sorted(
            (term, hit.skip, hit.start_offset, hit.end_offset)
            for term in terms
            for hit in find_els(corpus, term, min_skip=1, max_skip=8)
        )
        actual = sorted(
            (hit.term, hit.skip, hit.start_offset, hit.end_offset)
            for hit in find_els_terms(corpus, terms, min_skip=1, max_skip=8)
        )

        self.assertEqual(actual, expected)

    def test_parallel_bulk_match_metadata_matches_serial(self) -> None:
        text = "αβγδαβγδδαβγ"
        queries = ("αβ", "βγδ", "δα")

        serial = sorted(
            iter_els_query_matches_by_lanes(
                text,
                queries,
                min_skip=1,
                max_skip=4,
                direction="both",
                jobs=1,
            )
        )
        parallel = sorted(
            iter_els_query_matches_by_lanes(
                text,
                queries,
                min_skip=1,
                max_skip=4,
                direction="both",
                jobs=2,
            )
        )

        self.assertEqual(parallel, serial)

    def test_bulk_match_metadata_caps_each_query(self) -> None:
        matches = list(
            iter_els_query_matches_by_lanes(
                "αβαβαβαβ",
                ("αβ", "βα"),
                min_skip=1,
                max_skip=4,
                direction="both",
                max_hits_per_query=2,
            )
        )

        counts = {"αβ": 0, "βα": 0}
        for query, _skip, _start, _end in matches:
            counts[query] += 1
        self.assertEqual(counts, {"αβ": 2, "βα": 2})

    def test_bulk_count_respects_per_query_max_skip_caps(self) -> None:
        serial = count_els_terms_by_lanes(
            "αxxβ",
            ("αβ",),
            min_skip=1,
            max_skip=3,
            direction="forward",
            max_skip_by_query={"αβ": 2},
        )
        parallel = count_els_terms_by_lanes(
            "αxxβ",
            ("αβ",),
            min_skip=1,
            max_skip=3,
            direction="forward",
            jobs=2,
            max_skip_by_query={"αβ": 2},
        )

        self.assertEqual(serial["αβ"], 0)
        self.assertEqual(parallel, serial)

    def test_bulk_match_metadata_respects_per_query_max_skip_caps(self) -> None:
        serial = list(
            iter_els_query_matches_by_lanes(
                "αxxβ",
                ("αβ",),
                min_skip=1,
                max_skip=3,
                direction="forward",
                max_skip_by_query={"αβ": 2},
            )
        )
        parallel = list(
            iter_els_query_matches_by_lanes(
                "αxxβ",
                ("αβ",),
                min_skip=1,
                max_skip=3,
                direction="forward",
                jobs=2,
                max_skip_by_query={"αβ": 2},
            )
        )

        self.assertEqual(serial, [])
        self.assertEqual(parallel, serial)


def _reference_matches(
    text: str,
    query: str,
    skip: int,
) -> list[tuple[int, int]]:
    return list(
        iter_matches_at_positions(text, query, skip, positions_of(text, query[0]))
    )


if __name__ == "__main__":
    unittest.main()
