import pytest

from els.corpus import Corpus, VerseSpan
from els.search import find_els
from els.transforms import TRANSFORM_HEBREW_ATBASH, atbash_hebrew, transform_corpus


def test_atbash_hebrew_maps_babel_and_sheshach() -> None:
    assert atbash_hebrew("בבל") == "ששכ"
    assert atbash_hebrew("ששך") == "בבל"


def test_transform_corpus_preserves_offsets_and_surface_words() -> None:
    corpus = Corpus(
        name="tiny",
        language="hebrew",
        keep_hebrew_final_forms=False,
        text="ששכ",
        verses=(VerseSpan("test", "Jer 25:26", "Jer", "25", "26", "ששך", 0, 3, 3),),
        position_to_verse=[0, 0, 0],
    )

    transformed = transform_corpus(corpus, TRANSFORM_HEBREW_ATBASH)

    assert transformed.name == "tiny:hebrew_atbash"
    assert transformed.text == "בבל"
    assert transformed.ref_at(0) == "Jer 25:26"
    assert list(transformed.position_to_verse) == [0, 0, 0]


def test_atbash_transformed_corpus_can_be_searched_for_decoded_term() -> None:
    corpus = Corpus(
        name="tiny",
        language="hebrew",
        keep_hebrew_final_forms=False,
        text="ששכ",
        verses=(VerseSpan("test", "Jer 25:26", "Jer", "25", "26", "ששך", 0, 3, 3),),
        position_to_verse=[0, 0, 0],
    )
    transformed = transform_corpus(corpus, TRANSFORM_HEBREW_ATBASH)

    hits = list(find_els(transformed, "בבל", min_skip=1, max_skip=1, direction="forward"))

    assert len(hits) == 1
    assert hits[0].start_ref == "Jer 25:26"


def test_hebrew_atbash_rejects_non_hebrew_corpus() -> None:
    corpus = Corpus(
        name="tiny",
        language="english",
        keep_hebrew_final_forms=False,
        text="abc",
        verses=(VerseSpan("test", "Gen 1:1", "Gen", "1", "1", "abc", 0, 3, 3),),
        position_to_verse=[0, 0, 0],
    )

    with pytest.raises(ValueError, match="requires a Hebrew corpus"):
        transform_corpus(corpus, TRANSFORM_HEBREW_ATBASH)
