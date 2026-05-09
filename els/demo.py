"""Small end-to-end demo that does not require downloaded corpora."""

from __future__ import annotations

from array import array

from .corpus import Corpus, VerseSpan, WordSpan
from .search import count_els_terms_by_lanes, find_els, normalize_for_corpus


def demo_corpus() -> Corpus:
    verses = (
        VerseSpan("demo", "Demo 1:1", "Demo", "1", "1", "alpha beta gamma", 0, 13, 14),
        VerseSpan("demo", "Demo 1:2", "Demo", "1", "2", "delta eta theta", 14, 26, 13),
    )
    words = (
        WordSpan("demo", "Demo 1:1", "Demo", "1", "1", 1, "alpha", "alpha", 0, 4, 5),
        WordSpan("demo", "Demo 1:1", "Demo", "1", "1", 2, "beta", "beta", 5, 8, 4),
        WordSpan("demo", "Demo 1:1", "Demo", "1", "1", 3, "gamma", "gamma", 9, 13, 5),
        WordSpan("demo", "Demo 1:2", "Demo", "1", "2", 1, "delta", "delta", 14, 18, 5),
        WordSpan("demo", "Demo 1:2", "Demo", "1", "2", 2, "eta", "eta", 19, 21, 3),
        WordSpan("demo", "Demo 1:2", "Demo", "1", "2", 3, "theta", "theta", 22, 26, 5),
    )
    position_to_word = [
        word_index
        for word_index, word in enumerate(words)
        for _ in range(word.norm_length)
    ]
    position_to_verse = [0] * 14 + [1] * 13
    return Corpus(
        name="demo",
        language="english",
        keep_hebrew_final_forms=False,
        text="alphabetagammadeltaetatheta",
        verses=verses,
        position_to_verse=array("i", position_to_verse),
        words=words,
        position_to_word=array("i", position_to_word),
    )


def main() -> int:
    corpus = demo_corpus()
    terms = ["alpha", "theta", "aaa"]
    queries = [normalize_for_corpus(corpus, term) for term in terms]
    counts = count_els_terms_by_lanes(corpus.text, queries, min_skip=1, max_skip=5)

    print("Open Bible Codes demo")
    print(f"corpus={corpus.name} language={corpus.language} letters={len(corpus.text)}")
    print("term,normalized,hits")
    for term, query in zip(terms, queries, strict=True):
        print(f"{term},{query},{counts[query]}")

    print("")
    print("sample hits for theta")
    for hit in find_els(corpus, "theta", min_skip=1, max_skip=5, max_hits=3):
        print(
            ",".join(
                [
                    hit.term,
                    str(hit.skip),
                    hit.direction,
                    hit.start_ref,
                    hit.end_ref,
                    hit.center_word or "",
                ]
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
