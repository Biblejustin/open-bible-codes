"""ELS search routines."""

from __future__ import annotations

import multiprocessing
import os
import sys
from array import array
from collections import deque
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Iterable, Mapping, Sequence

from .corpus import Corpus
from .normalization import normalize_text


@dataclass(frozen=True)
class ELSHit:
    term: str
    normalized_term: str
    skip: int
    start_offset: int
    end_offset: int
    span_letters: int
    sequence: str
    start_ref: str
    end_ref: str
    start_source: str
    end_source: str
    center_offset: int
    center_ref: str
    center_source: str
    center_word_index: int | str
    center_word: str
    center_normalized_word: str

    @property
    def direction(self) -> str:
        return "forward" if self.skip > 0 else "backward"

    def as_row(self) -> dict[str, str | int]:
        return {
            "term": self.term,
            "normalized_term": self.normalized_term,
            "skip": self.skip,
            "direction": self.direction,
            "start_offset": self.start_offset,
            "end_offset": self.end_offset,
            "span_letters": self.span_letters,
            "sequence": self.sequence,
            "start_ref": self.start_ref,
            "end_ref": self.end_ref,
            "start_source": self.start_source,
            "end_source": self.end_source,
            "center_offset": self.center_offset,
            "center_ref": self.center_ref,
            "center_source": self.center_source,
            "center_word_index": self.center_word_index,
            "center_word": self.center_word,
            "center_normalized_word": self.center_normalized_word,
        }


def find_els(
    corpus: Corpus,
    term: str,
    *,
    min_skip: int = 2,
    max_skip: int = 100,
    direction: str = "both",
    max_hits: int | None = None,
) -> Iterable[ELSHit]:
    query = normalize_for_corpus(corpus, term)
    if not query:
        raise ValueError(f"term has no {corpus.language} letters after normalization")

    hits = 0
    _validate_skip_args(min_skip, max_skip, direction)
    text_length = len(corpus.text)
    for skip in range(min_skip, max_skip + 1):
        lanes = make_lanes(corpus.text, skip)
        if direction in {"forward", "both"}:
            for start, end in iter_forward_matches_in_lanes(
                lanes,
                query,
                skip,
                text_length=text_length,
            ):
                yield build_hit(corpus, term, query, skip, start, end)
                hits += 1
                if max_hits is not None and hits >= max_hits:
                    return
        if direction in {"backward", "both"}:
            for low, high in iter_forward_matches_in_lanes(
                lanes,
                query[::-1],
                skip,
                text_length=text_length,
            ):
                yield build_hit(corpus, term, query, -skip, high, low)
                hits += 1
                if max_hits is not None and hits >= max_hits:
                    return


def find_els_terms(
    corpus: Corpus,
    terms: Iterable[str],
    *,
    min_skip: int = 2,
    max_skip: int = 100,
    direction: str = "both",
    max_hits: int | None = None,
) -> Iterable[ELSHit]:
    """Find ELS hits for many terms with one automaton pass per skip lane."""

    terms_by_query: dict[str, list[str]] = {}
    for term in terms:
        query = normalize_for_corpus(corpus, term)
        if query:
            terms_by_query.setdefault(query, []).append(term)

    hits = 0
    for query, skip, start, end in iter_els_query_matches_by_lanes(
        corpus.text,
        terms_by_query,
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
    ):
        for term in terms_by_query[query]:
            yield build_hit(corpus, term, query, skip, start, end)
            hits += 1
            if max_hits is not None and hits >= max_hits:
                return


def iter_els_query_matches_by_lanes(
    text: str,
    queries: Iterable[str],
    *,
    min_skip: int = 2,
    max_skip: int = 100,
    direction: str = "both",
    jobs: int = 1,
    max_hits_per_query: int | None = None,
    max_skip_by_query: Mapping[str, int] | None = None,
) -> Iterable[tuple[str, int, int, int]]:
    """Yield normalized query, skip, start, and end for many ELS queries."""

    unique_queries = sorted({query for query in queries if query})
    _validate_skip_args(min_skip, max_skip, direction)
    _validate_jobs(jobs)
    query_skip_caps = normalized_query_skip_caps(
        unique_queries,
        max_skip_by_query,
        min_skip=min_skip,
        max_skip=max_skip,
    )
    unique_queries = [
        query
        for query in unique_queries
        if query_skip_caps.get(query, max_skip) >= min_skip
    ]
    if max_hits_per_query is not None and max_hits_per_query <= 0:
        return
    if not unique_queries:
        return
    effective_jobs = 1 if max_hits_per_query is not None else resolve_count_jobs(
        jobs,
        max_skip - min_skip + 1,
    )
    if effective_jobs > 1:
        try:
            yield from iter_els_query_matches_by_lanes_parallel(
                text,
                tuple(unique_queries),
                min_skip=min_skip,
                max_skip=max_skip,
                direction=direction,
                jobs=effective_jobs,
                max_skip_by_query=query_skip_caps,
            )
            return
        except PermissionError:
            pass

    forward_automaton = None
    forward_encoded_text = None
    if direction in {"forward", "both"}:
        forward_automaton = build_query_match_automaton(unique_queries, reverse=False)
        forward_encoded_text = forward_automaton.encode_text(text)

    backward_automaton = None
    backward_encoded_text = None
    if direction in {"backward", "both"}:
        backward_automaton = build_query_match_automaton(unique_queries, reverse=True)
        backward_encoded_text = backward_automaton.encode_text(text)

    hit_counts = {query: 0 for query in unique_queries}
    active_queries = set(unique_queries) if max_hits_per_query is not None else None
    for skip in range(min_skip, max_skip + 1):
        skip_active_queries = active_queries_for_skip(
            unique_queries,
            skip,
            query_skip_caps,
            active_queries,
        )
        if skip_active_queries == set():
            if no_future_active_queries(unique_queries, skip, query_skip_caps, active_queries):
                return
            continue
        if forward_automaton is not None and forward_encoded_text is not None:
            for query, start, end in iter_automaton_query_matches_at_skip(
                forward_encoded_text,
                forward_automaton,
                skip,
                active_queries=skip_active_queries,
            ):
                yield query, skip, start, end
                if active_queries is not None:
                    hit_counts[query] += 1
                    if hit_counts[query] >= max_hits_per_query:
                        active_queries.discard(query)
                        if not active_queries:
                            return
        if backward_automaton is not None and backward_encoded_text is not None:
            for query, low, high in iter_automaton_query_matches_at_skip(
                backward_encoded_text,
                backward_automaton,
                skip,
                active_queries=skip_active_queries,
            ):
                yield query, -skip, high, low
                if active_queries is not None:
                    hit_counts[query] += 1
                    if hit_counts[query] >= max_hits_per_query:
                        active_queries.discard(query)
                        if not active_queries:
                            return


def iter_els_query_matches_by_lanes_parallel(
    text: str,
    unique_queries: tuple[str, ...],
    *,
    min_skip: int,
    max_skip: int,
    direction: str,
    jobs: int,
    max_skip_by_query: Mapping[str, int] | None = None,
) -> Iterable[tuple[str, int, int, int]]:
    chunks = chunk_skip_values(min_skip, max_skip, jobs)
    with ProcessPoolExecutor(
        max_workers=jobs,
        mp_context=process_context(),
        initializer=initialize_match_worker,
        initargs=(text, unique_queries, direction, dict(max_skip_by_query or {})),
    ) as executor:
        for partial_matches in executor.map(match_skip_chunk_worker, chunks):
            yield from partial_matches


def build_query_match_automaton(queries: Iterable[str], *, reverse: bool) -> AhoAutomaton:
    automaton = AhoAutomaton()
    for query in queries:
        automaton.add(query[::-1] if reverse else query, query)
    automaton.build()
    return automaton


def iter_automaton_query_matches_at_skip(
    encoded_text: Sequence[int],
    automaton: AhoAutomaton,
    skip: int,
    *,
    active_queries: set[str] | None = None,
) -> Iterable[tuple[str, int, int]]:
    for offset in range(skip):
        for end, query in automaton.iter_outputs_encoded_stride(
            encoded_text,
            offset=offset,
            step=skip,
        ):
            if active_queries is not None and query not in active_queries:
                continue
            start = end - (len(query) - 1) * skip
            yield query, start, end


def build_hit(
    corpus: Corpus,
    term: str,
    query: str,
    skip: int,
    start: int,
    end: int,
) -> ELSHit:
    low = min(start, end)
    high = max(start, end)
    center_offset = (low + high) // 2
    center_word = corpus.word_at(center_offset)
    return ELSHit(
        term=term,
        normalized_term=query,
        skip=skip,
        start_offset=start,
        end_offset=end,
        span_letters=high - low + 1,
        sequence=query,
        start_ref=corpus.ref_at(start),
        end_ref=corpus.ref_at(end),
        start_source=corpus.source_at(start),
        end_source=corpus.source_at(end),
        center_offset=center_offset,
        center_ref=corpus.ref_at(center_offset),
        center_source=corpus.source_at(center_offset),
        center_word_index=center_word.word_index if center_word else "",
        center_word=center_word.raw_word if center_word else "",
        center_normalized_word=center_word.normalized_word if center_word else "",
    )


def count_els_text(
    text: str,
    query: str,
    *,
    min_skip: int = 2,
    max_skip: int = 100,
    direction: str = "both",
) -> int:
    return count_els_text_by_lanes(
        text,
        query,
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
    )


def count_els_text_by_lanes(
    text: str,
    query: str,
    *,
    min_skip: int = 2,
    max_skip: int = 100,
    direction: str = "both",
) -> int:
    """Count ELS hits using C-level substring searches along skip lanes."""

    if not query:
        return 0
    _validate_skip_args(min_skip, max_skip, direction)
    total = 0
    for skip in range(min_skip, max_skip + 1):
        if direction in {"forward", "both"}:
            total += count_query_at_skip(text, query, skip)
        if direction in {"backward", "both"}:
            total += count_query_at_skip(text, query[::-1], skip)
    return total


def count_els_terms_by_lanes(
    text: str,
    queries: Iterable[str],
    *,
    min_skip: int = 2,
    max_skip: int = 100,
    direction: str = "both",
    jobs: int = 1,
    max_skip_by_query: Mapping[str, int] | None = None,
) -> dict[str, int]:
    """Count many normalized terms with one automaton pass per skip lane."""

    unique_queries = sorted({query for query in queries if query})
    _validate_skip_args(min_skip, max_skip, direction)
    _validate_jobs(jobs)
    query_skip_caps = normalized_query_skip_caps(
        unique_queries,
        max_skip_by_query,
        min_skip=min_skip,
        max_skip=max_skip,
    )
    unique_queries = [
        query
        for query in unique_queries
        if query_skip_caps.get(query, max_skip) >= min_skip
    ]
    counts = {query: 0 for query in unique_queries}
    if not unique_queries:
        return counts

    effective_jobs = resolve_count_jobs(jobs, max_skip - min_skip + 1)
    if effective_jobs > 1:
        try:
            return count_els_terms_by_lanes_parallel(
                text,
                tuple(unique_queries),
                min_skip=min_skip,
                max_skip=max_skip,
                direction=direction,
                jobs=effective_jobs,
                max_skip_by_query=query_skip_caps,
            )
        except PermissionError:
            pass

    automaton = build_count_automaton(unique_queries, direction)

    encoded_text = automaton.encode_text(text)
    for skip in range(min_skip, max_skip + 1):
        skip_active_queries = active_queries_for_skip(
            unique_queries,
            skip,
            query_skip_caps,
            None,
        )
        if skip_active_queries == set():
            if no_future_active_queries(unique_queries, skip, query_skip_caps, None):
                break
            continue
        count_automaton_encoded_at_skip(
            encoded_text,
            automaton,
            skip,
            counts,
            active_queries=skip_active_queries,
        )
    return counts


def count_els_terms_by_lanes_parallel(
    text: str,
    unique_queries: tuple[str, ...],
    *,
    min_skip: int,
    max_skip: int,
    direction: str,
    jobs: int,
    max_skip_by_query: Mapping[str, int] | None = None,
) -> dict[str, int]:
    counts = {query: 0 for query in unique_queries}
    chunks = chunk_skip_values(min_skip, max_skip, jobs)
    context = process_context()
    with ProcessPoolExecutor(
        max_workers=jobs,
        mp_context=context,
        initializer=initialize_count_worker,
        initargs=(text, unique_queries, direction, dict(max_skip_by_query or {})),
    ) as executor:
        for partial_counts in executor.map(count_skip_chunk_worker, chunks):
            merge_counts(counts, partial_counts)
    return counts


def build_count_automaton(queries: Iterable[str], direction: str) -> AhoAutomaton:
    automaton = AhoAutomaton()
    for query in queries:
        if direction in {"forward", "both"}:
            automaton.add(query, query)
        if direction in {"backward", "both"}:
            automaton.add(query[::-1], query)
    automaton.build()
    return automaton


def resolve_count_jobs(jobs: int, skip_count: int) -> int:
    if jobs == 0:
        jobs = os.cpu_count() or 1
    return max(1, min(jobs, max(1, skip_count)))


def chunk_skip_values(min_skip: int, max_skip: int, jobs: int) -> list[tuple[int, ...]]:
    skip_values = list(range(min_skip, max_skip + 1))
    return [
        chunk
        for index in range(jobs)
        if (chunk := tuple(skip_values[index::jobs]))
    ]


def merge_counts(counts: dict[str, int], partial_counts: dict[str, int]) -> None:
    for query, count in partial_counts.items():
        counts[query] += count


def process_context() -> multiprocessing.context.BaseContext:
    requested = os.environ.get("EDLS_MULTIPROCESSING_START_METHOD")
    if requested:
        return multiprocessing.get_context(requested)
    method = select_process_start_method(
        multiprocessing.get_all_start_methods(),
        sys.platform,
    )
    if method:
        return multiprocessing.get_context(method)
    return multiprocessing.get_context()


def select_process_start_method(
    available: Sequence[str],
    platform: str,
) -> str | None:
    available_methods = set(available)
    if platform.startswith("linux"):
        preferred = ("fork", "forkserver", "spawn")
    elif platform == "darwin":
        preferred = ("forkserver", "spawn", "fork")
    else:
        preferred = ("spawn", "forkserver", "fork")
    for method in preferred:
        if method in available_methods:
            return method
    return None


_COUNT_WORKER_AUTOMATON: AhoAutomaton | None = None
_COUNT_WORKER_ENCODED_TEXT: array[int] | None = None
_COUNT_WORKER_QUERIES: tuple[str, ...] = ()
_COUNT_WORKER_MAX_SKIP_BY_QUERY: dict[str, int] = {}
_MATCH_WORKER_FORWARD_AUTOMATON: AhoAutomaton | None = None
_MATCH_WORKER_FORWARD_ENCODED_TEXT: array[int] | None = None
_MATCH_WORKER_BACKWARD_AUTOMATON: AhoAutomaton | None = None
_MATCH_WORKER_BACKWARD_ENCODED_TEXT: array[int] | None = None
_MATCH_WORKER_QUERIES: tuple[str, ...] = ()
_MATCH_WORKER_MAX_SKIP_BY_QUERY: dict[str, int] = {}


def initialize_count_worker(
    text: str,
    queries: tuple[str, ...],
    direction: str,
    max_skip_by_query: dict[str, int] | None = None,
) -> None:
    global _COUNT_WORKER_AUTOMATON
    global _COUNT_WORKER_ENCODED_TEXT
    global _COUNT_WORKER_QUERIES
    global _COUNT_WORKER_MAX_SKIP_BY_QUERY

    automaton = build_count_automaton(queries, direction)
    _COUNT_WORKER_AUTOMATON = automaton
    _COUNT_WORKER_ENCODED_TEXT = automaton.encode_text(text)
    _COUNT_WORKER_QUERIES = queries
    _COUNT_WORKER_MAX_SKIP_BY_QUERY = max_skip_by_query or {}


def count_skip_chunk_worker(skip_values: tuple[int, ...]) -> dict[str, int]:
    if _COUNT_WORKER_AUTOMATON is None or _COUNT_WORKER_ENCODED_TEXT is None:
        raise RuntimeError("count worker is not initialized")
    counts = {query: 0 for query in _COUNT_WORKER_QUERIES}
    for skip in skip_values:
        skip_active_queries = active_queries_for_skip(
            _COUNT_WORKER_QUERIES,
            skip,
            _COUNT_WORKER_MAX_SKIP_BY_QUERY,
            None,
        )
        if skip_active_queries == set():
            continue
        count_automaton_encoded_at_skip(
            _COUNT_WORKER_ENCODED_TEXT,
            _COUNT_WORKER_AUTOMATON,
            skip,
            counts,
            active_queries=skip_active_queries,
        )
    return counts


def initialize_match_worker(
    text: str,
    queries: tuple[str, ...],
    direction: str,
    max_skip_by_query: dict[str, int] | None = None,
) -> None:
    global _MATCH_WORKER_FORWARD_AUTOMATON
    global _MATCH_WORKER_FORWARD_ENCODED_TEXT
    global _MATCH_WORKER_BACKWARD_AUTOMATON
    global _MATCH_WORKER_BACKWARD_ENCODED_TEXT
    global _MATCH_WORKER_QUERIES
    global _MATCH_WORKER_MAX_SKIP_BY_QUERY

    _MATCH_WORKER_FORWARD_AUTOMATON = None
    _MATCH_WORKER_FORWARD_ENCODED_TEXT = None
    _MATCH_WORKER_BACKWARD_AUTOMATON = None
    _MATCH_WORKER_BACKWARD_ENCODED_TEXT = None
    _MATCH_WORKER_QUERIES = queries
    _MATCH_WORKER_MAX_SKIP_BY_QUERY = max_skip_by_query or {}
    if direction in {"forward", "both"}:
        automaton = build_query_match_automaton(queries, reverse=False)
        _MATCH_WORKER_FORWARD_AUTOMATON = automaton
        _MATCH_WORKER_FORWARD_ENCODED_TEXT = automaton.encode_text(text)
    if direction in {"backward", "both"}:
        automaton = build_query_match_automaton(queries, reverse=True)
        _MATCH_WORKER_BACKWARD_AUTOMATON = automaton
        _MATCH_WORKER_BACKWARD_ENCODED_TEXT = automaton.encode_text(text)


def match_skip_chunk_worker(skip_values: tuple[int, ...]) -> list[tuple[str, int, int, int]]:
    matches: list[tuple[str, int, int, int]] = []
    for skip in skip_values:
        skip_active_queries = active_queries_for_skip(
            _MATCH_WORKER_QUERIES,
            skip,
            _MATCH_WORKER_MAX_SKIP_BY_QUERY,
            None,
        )
        if skip_active_queries == set():
            continue
        if (
            _MATCH_WORKER_FORWARD_AUTOMATON is not None
            and _MATCH_WORKER_FORWARD_ENCODED_TEXT is not None
        ):
            matches.extend(
                (query, skip, start, end)
                for query, start, end in iter_automaton_query_matches_at_skip(
                    _MATCH_WORKER_FORWARD_ENCODED_TEXT,
                    _MATCH_WORKER_FORWARD_AUTOMATON,
                    skip,
                    active_queries=skip_active_queries,
                )
            )
        if (
            _MATCH_WORKER_BACKWARD_AUTOMATON is not None
            and _MATCH_WORKER_BACKWARD_ENCODED_TEXT is not None
        ):
            matches.extend(
                (query, -skip, high, low)
                for query, low, high in iter_automaton_query_matches_at_skip(
                    _MATCH_WORKER_BACKWARD_ENCODED_TEXT,
                    _MATCH_WORKER_BACKWARD_AUTOMATON,
                    skip,
                    active_queries=skip_active_queries,
                )
            )
    return matches


def count_query_at_skip(text: str, query: str, skip: int) -> int:
    if skip < 1:
        raise ValueError("skip must be >= 1")
    if len(query) == 1:
        return text.count(query)
    if (len(query) - 1) * skip >= len(text):
        return 0
    total = 0
    for offset in range(skip):
        lane = text[offset::skip]
        total += count_overlapping(lane, query)
    return total


def count_overlapping(text: str, query: str) -> int:
    total = 0
    start = text.find(query)
    while start != -1:
        total += 1
        start = text.find(query, start + 1)
    return total


class AhoNode:
    __slots__ = ("children", "fail", "outputs", "terminal_outputs")

    def __init__(self) -> None:
        self.children: dict[str, int] = {}
        self.fail = 0
        self.terminal_outputs: list[str] = []
        self.outputs: list[str] = []


class AhoAutomaton:
    def __init__(self) -> None:
        self.nodes = [AhoNode()]
        self.alphabet: dict[str, int] = {}
        self.goto: array[int] = array("i")
        self.outputs_by_state: tuple[tuple[str, ...], ...] = ()
        self.width = 0
        self.built = False

    def add(self, pattern: str, output: str) -> None:
        node_index = 0
        self.built = False
        for char in pattern:
            node = self.nodes[node_index]
            next_index = node.children.get(char)
            if next_index is None:
                next_index = len(self.nodes)
                node.children[char] = next_index
                self.nodes.append(AhoNode())
            node_index = next_index
        self.nodes[node_index].terminal_outputs.append(output)

    def build(self) -> None:
        for node in self.nodes:
            node.fail = 0
            node.outputs = list(node.terminal_outputs)

        queue: deque[int] = deque()
        for child_index in self.nodes[0].children.values():
            self.nodes[child_index].fail = 0
            queue.append(child_index)

        while queue:
            current_index = queue.popleft()
            current = self.nodes[current_index]
            for char, child_index in current.children.items():
                fail_index = current.fail
                while fail_index and char not in self.nodes[fail_index].children:
                    fail_index = self.nodes[fail_index].fail
                self.nodes[child_index].fail = self.nodes[fail_index].children.get(char, 0)
                self.nodes[child_index].outputs.extend(
                    self.nodes[self.nodes[child_index].fail].outputs
                )
                queue.append(child_index)

        self.alphabet = {
            char: index
            for index, char in enumerate(
                sorted({char for node in self.nodes for char in node.children})
            )
        }
        self.width = len(self.alphabet)
        self.goto = self.build_goto_table()
        self.outputs_by_state = tuple(tuple(node.outputs) for node in self.nodes)
        self.built = True

    def build_goto_table(self) -> array[int]:
        if not self.alphabet:
            return array("i")
        goto = array("i", [0]) * (len(self.nodes) * self.width)
        for node_index in range(len(self.nodes)):
            row_start = node_index * self.width
            for char, char_index in self.alphabet.items():
                goto[row_start + char_index] = self.next_state(node_index, char)
        return goto

    def next_state(self, node_index: int, char: str) -> int:
        while node_index and char not in self.nodes[node_index].children:
            node_index = self.nodes[node_index].fail
        return self.nodes[node_index].children.get(char, 0)

    def scan(self, text: str, counts: dict[str, int]) -> None:
        if not self.built:
            self.build()
        if not self.width:
            return
        alphabet = self.alphabet
        goto = self.goto
        width = self.width
        outputs_by_state = self.outputs_by_state
        node_index = 0
        for char in text:
            char_index = alphabet.get(char)
            if char_index is None:
                node_index = 0
                continue
            node_index = goto[node_index * width + char_index]
            for output in outputs_by_state[node_index]:
                counts[output] += 1

    def encode_text(self, text: str) -> array[int]:
        if not self.built:
            self.build()
        alphabet = self.alphabet
        return array("i", (alphabet.get(char, -1) for char in text))

    def scan_encoded_stride(
        self,
        encoded_text: Sequence[int],
        counts: dict[str, int],
        *,
        offset: int = 0,
        step: int = 1,
        active_outputs: set[str] | None = None,
    ) -> None:
        if not self.built:
            self.build()
        if not self.width:
            return
        goto = self.goto
        width = self.width
        outputs_by_state = self.outputs_by_state
        node_index = 0
        for position in range(offset, len(encoded_text), step):
            char_index = encoded_text[position]
            if char_index < 0:
                node_index = 0
                continue
            node_index = goto[node_index * width + char_index]
            for output in outputs_by_state[node_index]:
                if active_outputs is None or output in active_outputs:
                    counts[output] += 1

    def iter_outputs_encoded_stride(
        self,
        encoded_text: Sequence[int],
        *,
        offset: int = 0,
        step: int = 1,
    ) -> Iterable[tuple[int, str]]:
        if not self.built:
            self.build()
        if not self.width:
            return
        goto = self.goto
        width = self.width
        outputs_by_state = self.outputs_by_state
        node_index = 0
        for position in range(offset, len(encoded_text), step):
            char_index = encoded_text[position]
            if char_index < 0:
                node_index = 0
                continue
            node_index = goto[node_index * width + char_index]
            for output in outputs_by_state[node_index]:
                yield position, output

    def find_outputs(self, text: str) -> set[str]:
        if not self.built:
            self.build()
        if not self.width:
            return set()
        alphabet = self.alphabet
        goto = self.goto
        width = self.width
        outputs_by_state = self.outputs_by_state
        outputs: set[str] = set()
        node_index = 0
        for char in text:
            char_index = alphabet.get(char)
            if char_index is None:
                node_index = 0
                continue
            node_index = goto[node_index * width + char_index]
            outputs.update(outputs_by_state[node_index])
        return outputs


def count_automaton_at_skip(
    text: str,
    automaton: AhoAutomaton,
    skip: int,
    counts: dict[str, int],
) -> None:
    for offset in range(skip):
        automaton.scan(text[offset::skip], counts)


def count_automaton_encoded_at_skip(
    encoded_text: Sequence[int],
    automaton: AhoAutomaton,
    skip: int,
    counts: dict[str, int],
    *,
    active_queries: set[str] | None = None,
) -> None:
    for offset in range(skip):
        automaton.scan_encoded_stride(
            encoded_text,
            counts,
            offset=offset,
            step=skip,
            active_outputs=active_queries,
        )


def normalized_query_skip_caps(
    queries: Sequence[str],
    max_skip_by_query: Mapping[str, int] | None,
    *,
    min_skip: int,
    max_skip: int,
) -> dict[str, int]:
    if not max_skip_by_query:
        return {}
    return {
        query: min(int(max_skip_by_query.get(query, max_skip)), max_skip)
        for query in queries
        if int(max_skip_by_query.get(query, max_skip)) >= min_skip
    }


def active_queries_for_skip(
    queries: Sequence[str],
    skip: int,
    max_skip_by_query: Mapping[str, int],
    active_queries: set[str] | None,
) -> set[str] | None:
    if not max_skip_by_query:
        return active_queries
    base_queries = active_queries if active_queries is not None else set(queries)
    return {query for query in base_queries if skip <= max_skip_by_query.get(query, skip)}


def no_future_active_queries(
    queries: Sequence[str],
    skip: int,
    max_skip_by_query: Mapping[str, int],
    active_queries: set[str] | None,
) -> bool:
    if not max_skip_by_query:
        return False
    base_queries = active_queries if active_queries is not None else queries
    return all(max_skip_by_query.get(query, skip) <= skip for query in base_queries)


def _validate_skip_args(min_skip: int, max_skip: int, direction: str) -> None:
    if min_skip < 1:
        raise ValueError("min_skip must be >= 1")
    if max_skip < min_skip:
        raise ValueError("max_skip must be >= min_skip")
    if direction not in {"forward", "backward", "both"}:
        raise ValueError("direction must be forward, backward, or both")


def _validate_jobs(jobs: int) -> None:
    if jobs < 0:
        raise ValueError("jobs must be >= 0")


def count_els_text_at_positions(
    text: str,
    query: str,
    candidate_starts: tuple[int, ...],
    *,
    min_skip: int = 2,
    max_skip: int = 100,
    direction: str = "both",
) -> int:
    if not query:
        return 0
    return sum(
        1
        for skip in iter_skips(min_skip, max_skip, direction)
        for _start, _end in iter_matches_at_positions(
            text,
            query,
            skip,
            candidate_starts,
        )
    )


def iter_matches(text: str, query: str, skip: int) -> Iterable[tuple[int, int]]:
    if not query:
        return

    if skip > 0:
        yield from iter_forward_matches_by_lanes(text, query, skip)
        return
    if skip < 0:
        for low, high in iter_forward_matches_by_lanes(text, query[::-1], -skip):
            yield high, low
        return
    raise ValueError("skip must not be 0")


def iter_forward_matches_by_lanes(
    text: str,
    query: str,
    skip: int,
) -> Iterable[tuple[int, int]]:
    if skip < 1:
        raise ValueError("skip must be >= 1")
    yield from iter_forward_matches_in_lanes(
        make_lanes(text, skip),
        query,
        skip,
        text_length=len(text),
    )


def make_lanes(text: str, skip: int) -> list[str]:
    if skip < 1:
        raise ValueError("skip must be >= 1")
    return [text[offset::skip] for offset in range(skip)]


def iter_forward_matches_in_lanes(
    lanes: list[str],
    query: str,
    skip: int,
    *,
    text_length: int | None = None,
) -> Iterable[tuple[int, int]]:
    if not query:
        return
    query_length = len(query)
    span = (query_length - 1) * skip
    if text_length is None:
        text_length = total_lane_text_length(lanes)
    if not lanes or span >= text_length:
        return
    heap: list[tuple[int, int, int]] = []
    for offset, lane in enumerate(lanes):
        lane_index = lane.find(query)
        if lane_index != -1:
            start = offset + lane_index * skip
            heappush(heap, (start, offset, lane_index))

    while heap:
        _start_key, offset, lane_index = heappop(heap)
        lane = lanes[offset]
        start = offset + lane_index * skip
        end = start + span
        yield start, end
        next_lane_index = lane.find(query, lane_index + 1)
        if next_lane_index != -1:
            next_start = offset + next_lane_index * skip
            heappush(heap, (next_start, offset, next_lane_index))


def total_lane_text_length(lanes: list[str]) -> int:
    return sum(len(lane) for lane in lanes)


def iter_matches_at_positions(
    text: str,
    query: str,
    skip: int,
    candidate_starts: tuple[int, ...],
) -> Iterable[tuple[int, int]]:
    text_length = len(text)
    query_length = len(query)
    span = (query_length - 1) * skip

    for start in candidate_starts:
        end = start + span
        if end < 0 or end >= text_length:
            continue
        for index in range(1, query_length):
            if text[start + index * skip] != query[index]:
                break
        else:
            yield start, end


def positions_of(text: str, char: str) -> tuple[int, ...]:
    if not char:
        return ()
    positions: list[int] = []
    index = text.find(char)
    while index != -1:
        positions.append(index)
        index = text.find(char, index + 1)
    return tuple(positions)


def normalize_for_corpus(corpus: Corpus, term: str) -> str:
    return normalize_text(
        term,
        corpus.language,
        keep_hebrew_final_forms=corpus.keep_hebrew_final_forms,
    )


def iter_skips(min_skip: int, max_skip: int, direction: str) -> Iterable[int]:
    _validate_skip_args(min_skip, max_skip, direction)

    for skip in range(min_skip, max_skip + 1):
        if direction in {"forward", "both"}:
            yield skip
        if direction in {"backward", "both"}:
            yield -skip
