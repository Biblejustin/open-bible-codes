#!/usr/bin/env python3
"""Count content words and test count multiples."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from functools import cache
from pathlib import Path

from els.corpus import Corpus, load_corpus
from els.critical import classify_missing_verses
from els.word_counts import (
    DEFAULT_MULTIPLES,
    WordCountBundle,
    count_content_words,
    multiples_for_count,
    preferred_raw,
)


CORPORA = [
    ("MT_WLC", Path("configs/example_oshb_wlc.toml")),
    ("LXX", Path("configs/example_ebible_grclxx.toml")),
    ("TR_NT", Path("configs/example_ebible_grctr.toml")),
    ("SBLGNT", Path("configs/example_sblgnt.toml")),
]

CRITICAL_BASE = ("TR_NT", Path("configs/example_ebible_grctr.toml"))
CRITICAL_COMPARE = ("SBLGNT", Path("configs/example_sblgnt.toml"))

MIN_WORD_LENGTH = 2
OUT_BY_WORD = Path("reports/word_counts_by_word.csv")
OUT_BY_BOOK = Path("reports/word_counts_by_book.csv")
OUT_BY_CHAPTER = Path("reports/word_counts_by_chapter.csv")
OUT_BY_VERSE = Path("reports/word_counts_by_verse.csv")
OUT_MULTIPLES = Path("reports/word_count_multiples.csv")
OUT_CRITICAL = Path("reports/critical_word_multiples_breaks.csv")
OUT_MANIFEST = Path("reports/word_counts.manifest.json")


def main() -> int:
    by_word_rows: list[dict[str, object]] = []
    by_book_rows: list[dict[str, object]] = []
    by_chapter_rows: list[dict[str, object]] = []
    by_verse_rows: list[dict[str, object]] = []
    multiples_rows: list[dict[str, object]] = []
    manifests = []
    bundles: dict[str, WordCountBundle] = {}
    corpora: dict[str, Corpus] = {}

    for label, config_path in CORPORA:
        corpus = load_corpus(config_path)
        corpora[label] = corpus
        bundle = count_content_words(corpus, min_word_length=MIN_WORD_LENGTH)
        bundles[label] = bundle
        manifests.append({"label": label, "config": str(config_path.resolve()), "summary": corpus.summary()})

        display_words = preferred_raw_by_word(bundle)
        by_word_rows.extend(word_rows(label, bundle, display_words))
        by_book_rows.extend(book_rows(label, bundle, display_words))
        by_chapter_rows.extend(chapter_rows(label, bundle, display_words))
        by_verse_rows.extend(verse_rows(label, bundle))
        multiples_rows.extend(multiple_rows(label, bundle, display_words))

    write_rows(OUT_BY_WORD, by_word_rows)
    write_rows(OUT_BY_BOOK, by_book_rows)
    write_rows(OUT_BY_CHAPTER, by_chapter_rows)
    write_rows(OUT_BY_VERSE, by_verse_rows)
    write_rows(OUT_MULTIPLES, multiples_rows)

    tr = corpora.get(CRITICAL_BASE[0]) or load_corpus(CRITICAL_BASE[1])
    critical = corpora.get(CRITICAL_COMPARE[0]) or load_corpus(CRITICAL_COMPARE[1])
    omitted_blocks = classify_missing_verses(tr, critical)
    deleted_refs = {block.ref for block in omitted_blocks if block.used_as_deletion}
    tr_full = bundles.get(CRITICAL_BASE[0]) or count_content_words(tr, min_word_length=MIN_WORD_LENGTH)
    tr_minus_deleted = count_content_words(
        tr,
        min_word_length=MIN_WORD_LENGTH,
        exclude_refs=deleted_refs,
    )
    write_rows(
        OUT_CRITICAL,
        critical_break_rows(tr_full, tr_minus_deleted, deleted_refs),
    )
    write_manifest(manifests, omitted_blocks, deleted_refs)

    for path in [
        OUT_BY_WORD,
        OUT_BY_BOOK,
        OUT_BY_CHAPTER,
        OUT_BY_VERSE,
        OUT_MULTIPLES,
        OUT_CRITICAL,
        OUT_MANIFEST,
    ]:
        print(path)
    return 0


def word_rows(
    label: str,
    bundle: WordCountBundle,
    display_words: dict[str, str],
) -> list[dict[str, object]]:
    rows = []
    for normalized, count in sorted(bundle.by_word.items(), key=lambda item: (-item[1], item[0])):
        row = {
            "corpus": label,
            "normalized_word": normalized,
            "display_word": display_words.get(normalized, ""),
            "total_count": count,
            "book_count": len(bundle.book_refs.get(normalized, set())),
            "chapter_count": len(bundle.chapter_refs.get(normalized, set())),
            "verse_count": len(bundle.verse_refs.get(normalized, set())),
        }
        row.update(count_fields(count))
        rows.append(row)
    return rows


def book_rows(
    label: str,
    bundle: WordCountBundle,
    display_words: dict[str, str],
) -> list[dict[str, object]]:
    return [
        {
            "corpus": label,
            "book": book,
            "normalized_word": normalized,
            "display_word": display_words.get(normalized, ""),
            "count": count,
            **count_fields(count),
        }
        for (book, normalized), count in sorted(
            bundle.by_book.items(),
            key=lambda item: (item[0][0], -item[1], item[0][1]),
        )
    ]


def chapter_rows(
    label: str,
    bundle: WordCountBundle,
    display_words: dict[str, str],
) -> list[dict[str, object]]:
    return [
        {
            "corpus": label,
            "book": book,
            "chapter": chapter,
            "normalized_word": normalized,
            "display_word": display_words.get(normalized, ""),
            "count": count,
            **count_fields(count),
        }
        for (book, chapter, normalized), count in sorted(
            bundle.by_chapter.items(),
            key=lambda item: (item[0][0], chapter_sort_key(item[0][1]), -item[1], item[0][2]),
        )
    ]


def verse_rows(label: str, bundle: WordCountBundle) -> list[dict[str, object]]:
    return [
        {
            "corpus": label,
            "ref": ref,
            "normalized_word": normalized,
            "raw_word": raw_word,
            "count": count,
            **count_fields(count),
        }
        for (ref, normalized, raw_word), count in sorted(
            bundle.by_verse.items(),
            key=lambda item: (item[0][0], -item[1], item[0][1], item[0][2]),
        )
    ]


def multiple_rows(
    label: str,
    bundle: WordCountBundle,
    display_words: dict[str, str],
) -> list[dict[str, object]]:
    rows = []
    for normalized, count in sorted(bundle.by_word.items(), key=lambda item: (-item[1], item[0])):
        fields = count_fields(count)
        if not fields["multiples"]:
            continue
        rows.append(
            {
                "corpus": label,
                "normalized_word": normalized,
                "display_word": display_words.get(normalized, ""),
                "total_count": count,
                "multiples": fields["multiples"],
                "book_count": len(bundle.book_refs.get(normalized, set())),
                "chapter_count": len(bundle.chapter_refs.get(normalized, set())),
                "verse_count": len(bundle.verse_refs.get(normalized, set())),
                **multiple_flag_fields(fields),
            }
        )
    return rows


def critical_break_rows(
    full: WordCountBundle,
    minus_deleted: WordCountBundle,
    deleted_refs: set[str],
) -> list[dict[str, object]]:
    rows = []
    words = set(full.by_word) | set(minus_deleted.by_word)
    for normalized in sorted(words):
        full_count = full.by_word.get(normalized, 0)
        minus_count = minus_deleted.by_word.get(normalized, 0)
        deleted_count = full_count - minus_count
        if deleted_count == 0:
            continue
        full_multiples = set(multiples_for_count(full_count))
        minus_multiples = set(multiples_for_count(minus_count))
        broken = sorted(full_multiples - minus_multiples)
        created = sorted(minus_multiples - full_multiples)
        if not broken and not created:
            continue
        deleted_word_refs = sorted(full.verse_refs.get(normalized, set()) & deleted_refs)
        rows.append(
            {
                "normalized_word": normalized,
                "display_word": preferred_raw(full.raw_examples, normalized),
                "full_count": full_count,
                "minus_deleted_count": minus_count,
                "deleted_count": deleted_count,
                "full_multiples": ";".join(str(value) for value in sorted(full_multiples)),
                "minus_deleted_multiples": ";".join(str(value) for value in sorted(minus_multiples)),
                "broken_multiples": ";".join(str(value) for value in broken),
                "created_multiples": ";".join(str(value) for value in created),
                "deleted_refs": ";".join(deleted_word_refs),
            }
        )
    rows.sort(
        key=lambda row: (
            0 if row["broken_multiples"] else 1,
            -int(row["deleted_count"]),
            row["normalized_word"],
        )
    )
    return rows


@cache
def chapter_sort_key(value: str) -> tuple[int, str]:
    return (int(value), "") if value.isdigit() else (9999, value)


@cache
def count_fields(count: int) -> dict[str, object]:
    multiples = multiples_for_count(count)
    matched = set(multiples)
    return {
        "multiples": ";".join(str(value) for value in multiples),
        **{f"multiple_{value}": value in matched for value in DEFAULT_MULTIPLES},
    }


def multiple_flag_fields(fields: dict[str, object]) -> dict[str, object]:
    return {
        f"multiple_{value}": fields[f"multiple_{value}"]
        for value in DEFAULT_MULTIPLES
    }


def preferred_raw_by_word(bundle: WordCountBundle) -> dict[str, str]:
    return {
        normalized: preferred_raw(bundle.raw_examples, normalized)
        for normalized in bundle.raw_examples
    }


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(fieldnames)
        writer.writerows(
            [row.get(fieldname, "") for fieldname in fieldnames]
            for row in rows
        )


def write_manifest(manifests: list[dict[str, object]], omitted_blocks, deleted_refs: set[str]) -> None:
    OUT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    OUT_MANIFEST.write_text(
        json.dumps(
            {
                "tool": "word_counts",
                "created_utc": datetime.now(UTC).isoformat(),
                "min_word_length": MIN_WORD_LENGTH,
                "stopword_mode": "surface_normalized_language_stoplist",
                "multiples": list(DEFAULT_MULTIPLES),
                "corpora": manifests,
                "critical_base": CRITICAL_BASE[0],
                "critical_compare": CRITICAL_COMPARE[0],
                "ref_missing_verses": len(omitted_blocks),
                "deleted_refs_used": len(deleted_refs),
                "deleted_refs": sorted(deleted_refs),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
