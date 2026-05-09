"""Content-word counting and multiple checks."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable

from .corpus import Corpus, WordSpan
from .normalization import normalize_text


DEFAULT_MULTIPLES = (3, 7, 12, 40, 70)

GREEK_STOPWORDS = {
    "ο",
    "η",
    "το",
    "του",
    "τη",
    "τησ",
    "τω",
    "τον",
    "την",
    "οι",
    "αι",
    "τα",
    "τασ",
    "των",
    "τοισ",
    "ταισ",
    "τουσ",
    "και",
    "δε",
    "γαρ",
    "ουν",
    "τε",
    "η",
    "ει",
    "μη",
    "ου",
    "ουκ",
    "ουχ",
    "εν",
    "εισ",
    "εκ",
    "εξ",
    "απο",
    "προσ",
    "δια",
    "κατα",
    "μετα",
    "περι",
    "υπο",
    "υπερ",
    "επι",
    "επ",
    "παρα",
    "αντι",
    "προ",
    "συν",
    "ως",
    "ωσ",
    "εωσ",
    "οτι",
    "ινα",
    "αλλα",
    "αλλ",
    "εαν",
    "αν",
    "μεν",
    "να",
    "εγω",
    "συ",
    "αυτοσ",
    "αυτον",
    "αυτου",
    "αυτη",
    "αυτην",
    "αυτησ",
    "αυτω",
    "αυτων",
    "αυτοι",
    "αυτοισ",
    "αυτουσ",
    "μου",
    "σου",
    "ημων",
    "υμων",
    "με",
    "σε",
    "ημασ",
    "ημιν",
    "υμασ",
    "υμιν",
    "μοι",
    "σοι",
    "εστιν",
    "εστι",
    "εισιν",
    "ην",
    "εσται",
    "ειμι",
    "ει",
    "τι",
    "τισ",
    "τινα",
    "τινεσ",
    "παν",
    "πασ",
    "πασα",
    "παντα",
    "παντεσ",
    "τουτο",
    "ταυτα",
    "υμεισ",
    "υμεις",
    "οσ",
    "ος",
    "οστισ",
    "οστις",
    "ουτοσ",
    "ουτος",
    "αυται",
    "αυταισ",
    "ιδου",
}

HEBREW_STOPWORDS = {
    "את",
    "אשר",
    "כי",
    "לא",
    "אל",
    "על",
    "כל",
    "מנ",
    "מן",
    "עם",
    "או",
    "אם",
    "אז",
    "אך",
    "גם",
    "כן",
    "זה",
    "זאת",
    "הוא",
    "היא",
    "הם",
    "אתה",
    "אני",
    "אנכי",
    "אנחנו",
    "אתמ",
    "אלה",
    "אשר",
    "שם",
    "המ",
    "כמ",
    "נו",
    "ני",
    "כ",
    "ו",
}

MICHIGAN_STOPWORDS = {
    ")T",
    ")$R",
    "KY",
    "L)",
    ")L",
    "(L",
    "KL",
    "MN",
    "(M",
    ")W",
    ")M",
    "GM",
    "KN",
    "ZH",
    "HW)",
    "HY)",
    "HM",
    "$M",
}

STOPWORDS_BY_LANGUAGE = {
    "greek": GREEK_STOPWORDS,
    "hebrew": HEBREW_STOPWORDS,
    "michigan": MICHIGAN_STOPWORDS,
    "michigan_claremont": MICHIGAN_STOPWORDS,
}


@dataclass(frozen=True)
class WordCountBundle:
    by_word: Counter[str]
    by_book: Counter[tuple[str, str]]
    by_chapter: Counter[tuple[str, str, str]]
    by_verse: Counter[tuple[str, str, str]]
    raw_examples: dict[str, Counter[str]]
    verse_refs: dict[str, set[str]]
    chapter_refs: dict[str, set[str]]
    book_refs: dict[str, set[str]]


def content_words(
    corpus: Corpus,
    *,
    min_word_length: int = 2,
    exclude_refs: set[str] | None = None,
) -> Iterable[WordSpan]:
    stopwords = STOPWORDS_BY_LANGUAGE.get(corpus.language, set())
    excluded = exclude_refs or set()
    for word in corpus.words:
        normalized = content_key_for_word(corpus, word)
        if word.ref in excluded:
            continue
        if len(normalized) < min_word_length:
            continue
        if normalized in stopwords:
            continue
        yield word


def count_content_words(
    corpus: Corpus,
    *,
    min_word_length: int = 2,
    exclude_refs: set[str] | None = None,
) -> WordCountBundle:
    by_word: Counter[str] = Counter()
    by_book: Counter[tuple[str, str]] = Counter()
    by_chapter: Counter[tuple[str, str, str]] = Counter()
    by_verse: Counter[tuple[str, str, str]] = Counter()
    raw_examples: dict[str, Counter[str]] = defaultdict(Counter)
    verse_refs: dict[str, set[str]] = defaultdict(set)
    chapter_refs: dict[str, set[str]] = defaultdict(set)
    book_refs: dict[str, set[str]] = defaultdict(set)

    stopwords = STOPWORDS_BY_LANGUAGE.get(corpus.language, set())
    excluded = exclude_refs or set()
    use_lexical_segment = corpus.language in {"hebrew", "michigan", "michigan_claremont"}
    for word in corpus.words:
        if word.ref in excluded:
            continue
        if use_lexical_segment and "/" in word.raw_word:
            normalized = normalize_text(
                word.raw_word.rsplit("/", 1)[-1],
                corpus.language,
                keep_hebrew_final_forms=corpus.keep_hebrew_final_forms,
            )
        else:
            normalized = word.normalized_word
        if len(normalized) < min_word_length:
            continue
        if normalized in stopwords:
            continue
        chapter_ref = f"{word.book} {word.chapter}" if word.book and word.chapter else ""
        by_word[normalized] += 1
        by_book[(word.book, normalized)] += 1
        by_chapter[(word.book, word.chapter, normalized)] += 1
        by_verse[(word.ref, normalized, word.raw_word)] += 1
        raw_examples[normalized][word.raw_word] += 1
        verse_refs[normalized].add(word.ref)
        if chapter_ref:
            chapter_refs[normalized].add(chapter_ref)
        if word.book:
            book_refs[normalized].add(word.book)

    return WordCountBundle(
        by_word=by_word,
        by_book=by_book,
        by_chapter=by_chapter,
        by_verse=by_verse,
        raw_examples=dict(raw_examples),
        verse_refs=dict(verse_refs),
        chapter_refs=dict(chapter_refs),
        book_refs=dict(book_refs),
    )


def content_key_for_word(corpus: Corpus, word: WordSpan) -> str:
    if corpus.language in {"hebrew", "michigan", "michigan_claremont"} and "/" in word.raw_word:
        raw_word = word.raw_word.rsplit("/", 1)[-1]
        return normalize_text(
            raw_word,
            corpus.language,
            keep_hebrew_final_forms=corpus.keep_hebrew_final_forms,
        )
    return word.normalized_word


@lru_cache(maxsize=None)
def multiples_for_count(count: int, multiples: tuple[int, ...] = DEFAULT_MULTIPLES) -> tuple[int, ...]:
    if count == 0:
        return ()
    return tuple(value for value in multiples if count % value == 0)


def multiple_flags(count: int, multiples: tuple[int, ...] = DEFAULT_MULTIPLES) -> dict[str, bool]:
    return {f"multiple_{value}": value in multiples_for_count(count, multiples) for value in multiples}


def preferred_raw(raw_examples: dict[str, Counter[str]], normalized: str) -> str:
    examples = raw_examples.get(normalized)
    if not examples:
        return ""
    return examples.most_common(1)[0][0]
