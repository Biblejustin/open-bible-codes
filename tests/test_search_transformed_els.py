from els.corpus import Corpus, VerseSpan
from els.transforms import TRANSFORM_HEBREW_ATBASH, TRANSFORM_PLAIN, transform_corpus
from scripts.search_transformed_els import read_term_rows, transformed_search_rows


def tiny_atbash_corpus() -> Corpus:
    return Corpus(
        name="tiny",
        language="hebrew",
        keep_hebrew_final_forms=False,
        text="ששכ",
        verses=(VerseSpan("test", "Jer 25:26", "Jer", "25", "26", "ששך", 0, 3, 3),),
        position_to_verse=[0, 0, 0],
    )


def test_transformed_search_rows_find_decoded_term() -> None:
    corpus = tiny_atbash_corpus()
    transformed = transform_corpus(corpus, TRANSFORM_HEBREW_ATBASH)

    rows = transformed_search_rows(
        corpus,
        transformed,
        [{"term_id": "babylon", "concept": "Babylon", "category": "test", "term": "בבל"}],
        transform=TRANSFORM_HEBREW_ATBASH,
        corpus_label="TINY",
        min_skip=1,
        max_skip=1,
        direction="forward",
        max_hits_per_term=10,
    )

    assert len(rows) == 1
    assert rows[0]["base_corpus"] == "tiny"
    assert rows[0]["corpus_label"] == "TINY"
    assert rows[0]["transform"] == TRANSFORM_HEBREW_ATBASH
    assert rows[0]["term_id"] == "babylon"
    assert rows[0]["center_ref"] == "Jer 25:26"


def test_transformed_search_rows_support_plain_layer() -> None:
    corpus = tiny_atbash_corpus()
    transformed = transform_corpus(corpus, TRANSFORM_PLAIN)

    rows = transformed_search_rows(
        corpus,
        transformed,
        [{"term_id": "sheshach", "concept": "Sheshach", "category": "test", "term": "ששך"}],
        transform=TRANSFORM_PLAIN,
        corpus_label="TINY",
        min_skip=1,
        max_skip=1,
        direction="forward",
        max_hits_per_term=10,
    )

    assert len(rows) == 1
    assert rows[0]["transform"] == TRANSFORM_PLAIN
    assert rows[0]["term_id"] == "sheshach"
    assert rows[0]["sequence"] == "ששכ"


def test_read_term_rows_combines_inline_and_csv(tmp_path) -> None:
    path = tmp_path / "terms.csv"
    path.write_text(
        "term_id,concept,category,language,term,notes\n"
        "babel,Babel,test,hebrew,בבל,\n",
        encoding="utf-8",
    )

    rows = read_term_rows(["ששך"], [path])

    assert [row["term_id"] for row in rows] == ["inline_1", "babel"]
