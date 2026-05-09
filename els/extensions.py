"""Same-skip extension checks for ELS hits."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .corpus import Corpus, WordSpan
from .search import ELSHit


EXTENSION_TYPE_PRIORITY = {
    "before_plus_term_plus_after": 3,
    "before_plus_term": 2,
    "term_plus_after": 2,
    "before_match": 1,
    "after_match": 1,
}
ALL_CODES_EXTENSION_TYPE_PRIORITY = {
    "before_plus_term_plus_after": 4,
    "before_plus_term": 3,
    "term_plus_after": 3,
    "before_match": 1,
    "after_match": 1,
}


def extension_score(
    extension_type: str,
    extension_length: int,
    match_kind: str,
    match_count: int,
    *,
    high_priority_scale: bool = False,
) -> int:
    priorities = (
        ALL_CODES_EXTENSION_TYPE_PRIORITY if high_priority_scale else EXTENSION_TYPE_PRIORITY
    )
    priority = priorities.get(extension_type, 0)
    phrase_bonus = 1 if match_kind.startswith("phrase_") else 0
    if high_priority_scale:
        return (
            priority * 100000
            + extension_length * 1000
            + phrase_bonus * 10
            + min(match_count, 9)
        )
    return (
        extension_length * 1000
        + priority * 100
        + phrase_bonus * 10
        + min(match_count, 9)
    )


@dataclass(frozen=True)
class LexiconEntry:
    normalized: str
    match_kind: str
    count: int
    raw_examples: tuple[str, ...]
    refs: tuple[str, ...]


@dataclass(frozen=True)
class ExtensionLexicon:
    entries: dict[str, LexiconEntry]

    def get(self, normalized: str) -> LexiconEntry | None:
        return self.entries.get(normalized)


@dataclass(frozen=True)
class ExtensionMatch:
    extension_type: str
    extension_side: str
    extension_length: int
    before_letters: str
    after_letters: str
    extended_sequence: str
    matched_normalized: str
    match_kind: str
    match_count: int
    matched_examples: str
    matched_refs: str
    extension_start_offset: int
    extension_end_offset: int
    extension_start_ref: str
    extension_end_ref: str


@dataclass
class MutableLexiconEntry:
    kinds: set[str]
    count: int = 0
    raw_examples: list[str] | None = None
    refs: list[str] | None = None

    def add(self, kind: str, raw: str, ref: str) -> None:
        self.kinds.add(kind)
        self.count += 1
        if self.raw_examples is None:
            self.raw_examples = []
        if self.refs is None:
            self.refs = []
        if raw not in self.raw_examples and len(self.raw_examples) < 5:
            self.raw_examples.append(raw)
        if ref not in self.refs and len(self.refs) < 5:
            self.refs.append(ref)


def build_extension_lexicon(
    corpus: Corpus,
    *,
    max_phrase_words: int = 4,
) -> ExtensionLexicon:
    """Build a normalized word/phrase lexicon from corpus surface words."""

    mutable: dict[str, MutableLexiconEntry] = {}

    def add(normalized: str, kind: str, raw: str, ref: str) -> None:
        if not normalized:
            return
        entry = mutable.setdefault(normalized, MutableLexiconEntry(set()))
        entry.add(kind, raw, ref)

    words_by_ref: dict[str, list[WordSpan]] = defaultdict(list)
    for word in corpus.words:
        add(word.normalized_word, "word", word.raw_word, word.ref)
        words_by_ref[word.ref].append(word)

    if max_phrase_words >= 2:
        for words in words_by_ref.values():
            for start_index in range(len(words)):
                normalized_parts: list[str] = []
                raw_parts: list[str] = []
                for end_index in range(
                    start_index,
                    min(len(words), start_index + max_phrase_words),
                ):
                    word = words[end_index]
                    normalized_parts.append(word.normalized_word)
                    raw_parts.append(word.raw_word)
                    phrase_length = end_index - start_index + 1
                    if phrase_length < 2:
                        continue
                    add(
                        "".join(normalized_parts),
                        f"phrase_{phrase_length}",
                        " ".join(raw_parts),
                        word.ref,
                    )

    return ExtensionLexicon(
        entries={
            normalized: LexiconEntry(
                normalized=normalized,
                match_kind="+".join(sorted(entry.kinds)),
                count=entry.count,
                raw_examples=tuple(entry.raw_examples or ()),
                refs=tuple(entry.refs or ()),
            )
            for normalized, entry in mutable.items()
        }
    )


def extensions_for_hit(
    corpus: Corpus,
    hit: ELSHit,
    lexicon: ExtensionLexicon,
    *,
    max_before: int = 12,
    max_after: int = 12,
    include_both_sided: bool = False,
    max_extensions: int | None = None,
) -> list[ExtensionMatch]:
    """Return lexicon matches adjacent to a hit along the same signed skip lane."""

    matches: list[ExtensionMatch] = []
    before_sequences = extension_sequences_before(corpus, hit, max_before)
    after_sequences = extension_sequences_after(corpus, hit, max_after)

    def append_match(
        extension_type: str,
        extension_side: str,
        before_letters: str,
        after_letters: str,
        extended_sequence: str,
        start_offset: int,
        end_offset: int,
    ) -> bool:
        entry = lexicon.get(extended_sequence)
        if entry is None:
            return False
        matches.append(
            ExtensionMatch(
                extension_type=extension_type,
                extension_side=extension_side,
                extension_length=len(before_letters) + len(after_letters),
                before_letters=before_letters,
                after_letters=after_letters,
                extended_sequence=extended_sequence,
                matched_normalized=entry.normalized,
                match_kind=entry.match_kind,
                match_count=entry.count,
                matched_examples="; ".join(entry.raw_examples),
                matched_refs="; ".join(entry.refs),
                extension_start_offset=start_offset,
                extension_end_offset=end_offset,
                extension_start_ref=corpus.ref_at(start_offset),
                extension_end_ref=corpus.ref_at(end_offset),
            )
        )
        return max_extensions is not None and len(matches) >= max_extensions

    for letters, offsets in before_sequences:
        if append_match(
            "before_match",
            "before",
            letters,
            "",
            letters,
            offsets[0],
            offsets[-1],
        ):
            return matches
        if append_match(
            "before_plus_term",
            "before",
            letters,
            "",
            letters + hit.normalized_term,
            offsets[0],
            hit.end_offset,
        ):
            return matches

    for letters, offsets in after_sequences:
        if append_match(
            "after_match",
            "after",
            "",
            letters,
            letters,
            offsets[0],
            offsets[-1],
        ):
            return matches
        if append_match(
            "term_plus_after",
            "after",
            "",
            letters,
            hit.normalized_term + letters,
            hit.start_offset,
            offsets[-1],
        ):
            return matches

    if include_both_sided:
        for before_letters, before_offsets in before_sequences:
            for after_letters, after_offsets in after_sequences:
                if append_match(
                    "before_plus_term_plus_after",
                    "both",
                    before_letters,
                    after_letters,
                    before_letters + hit.normalized_term + after_letters,
                    before_offsets[0],
                    after_offsets[-1],
                ):
                    return matches

    return matches


def extension_sequences_before(
    corpus: Corpus,
    hit: ELSHit,
    max_before: int,
) -> list[tuple[str, tuple[int, ...]]]:
    sequences: list[tuple[str, tuple[int, ...]]] = []
    for length in range(1, max_before + 1):
        offsets = tuple(
            hit.start_offset - hit.skip * index
            for index in range(length, 0, -1)
        )
        if not offsets_in_bounds(corpus, offsets):
            break
        sequences.append(("".join(corpus.text[offset] for offset in offsets), offsets))
    return sequences


def extension_sequences_after(
    corpus: Corpus,
    hit: ELSHit,
    max_after: int,
) -> list[tuple[str, tuple[int, ...]]]:
    sequences: list[tuple[str, tuple[int, ...]]] = []
    for length in range(1, max_after + 1):
        offsets = tuple(
            hit.end_offset + hit.skip * index
            for index in range(1, length + 1)
        )
        if not offsets_in_bounds(corpus, offsets):
            break
        sequences.append(("".join(corpus.text[offset] for offset in offsets), offsets))
    return sequences


def offsets_in_bounds(corpus: Corpus, offsets: tuple[int, ...]) -> bool:
    return all(0 <= offset < len(corpus.text) for offset in offsets)
