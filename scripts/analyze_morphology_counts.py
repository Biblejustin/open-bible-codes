#!/usr/bin/env python3
"""Count lemma/POS morphology for OSHB and MorphGNT."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from els.morphology import (
    CONTENT_POS,
    MorphCountBundle,
    count_morph_tokens,
    format_multiples,
    preferred_display,
    preferred_word,
    read_morphgnt_tokens,
    read_oshb_tokens,
)
from els.word_counts import DEFAULT_MULTIPLES, multiple_flags


OSHB_DIR = Path("data/raw/oshb/wlc")
MORPHGNT_DIR = Path("data/raw/morphgnt/sblgnt")

OUT_BY_LEMMA = Path("reports/morph_counts_by_lemma.csv")
OUT_BY_BOOK = Path("reports/morph_counts_by_book.csv")
OUT_BY_CHAPTER = Path("reports/morph_counts_by_chapter.csv")
OUT_BY_VERSE = Path("reports/morph_counts_by_verse.csv")
OUT_MULTIPLES = Path("reports/morph_count_multiples.csv")
OUT_MANIFEST = Path("reports/morph_counts.manifest.json")


def main() -> int:
    corpora = []
    if OSHB_DIR.exists():
        corpora.append(("MT_WLC_MORPH", read_oshb_tokens(OSHB_DIR)))
    if MORPHGNT_DIR.exists():
        corpora.append(("SBLGNT_MORPH", read_morphgnt_tokens(MORPHGNT_DIR)))
    if not corpora:
        raise SystemExit("no morphology data found; run download scripts first")

    by_lemma_rows: list[dict[str, object]] = []
    by_book_rows: list[dict[str, object]] = []
    by_chapter_rows: list[dict[str, object]] = []
    by_verse_rows: list[dict[str, object]] = []
    multiple_rows: list[dict[str, object]] = []
    manifest_corpora = []

    for label, tokens in corpora:
        bundle = count_morph_tokens(tokens)
        by_lemma_rows.extend(lemma_rows(label, bundle))
        by_book_rows.extend(book_rows(label, bundle))
        by_chapter_rows.extend(chapter_rows(label, bundle))
        by_verse_rows.extend(verse_rows(label, bundle))
        multiple_rows.extend(multiples_rows(label, bundle))
        manifest_corpora.append(
            {
                "label": label,
                "token_rows": len(tokens),
                "content_token_rows": sum(count for (_pos, _lemma), count in bundle.by_lemma.items()),
                "lemma_rows": len(bundle.by_lemma),
            }
        )

    write_rows(OUT_BY_LEMMA, by_lemma_rows)
    write_rows(OUT_BY_BOOK, by_book_rows)
    write_rows(OUT_BY_CHAPTER, by_chapter_rows)
    write_rows(OUT_BY_VERSE, by_verse_rows)
    write_rows(OUT_MULTIPLES, multiple_rows)
    write_manifest(manifest_corpora)

    for path in [OUT_BY_LEMMA, OUT_BY_BOOK, OUT_BY_CHAPTER, OUT_BY_VERSE, OUT_MULTIPLES, OUT_MANIFEST]:
        print(path)
    return 0


def lemma_rows(label: str, bundle: MorphCountBundle) -> list[dict[str, object]]:
    rows = []
    for (pos, lemma), count in sorted(bundle.by_lemma.items(), key=lambda item: (-item[1], item[0][0], item[0][1])):
        key = (pos, lemma)
        row = {
            "corpus": label,
            "pos": pos,
            "normalized_lemma": lemma,
            "display_lemma": preferred_display(bundle.display_lemmas, lemma),
            "display_word": preferred_word(bundle.display_words, pos, lemma),
            "total_count": count,
            "book_count": len(bundle.book_refs.get(key, set())),
            "chapter_count": len(bundle.chapter_refs.get(key, set())),
            "verse_count": len(bundle.verse_refs.get(key, set())),
            "multiples": format_multiples(count),
        }
        row.update(multiple_flags(count))
        rows.append(row)
    return rows


def book_rows(label: str, bundle: MorphCountBundle) -> list[dict[str, object]]:
    rows = []
    for (book, pos, lemma), count in sorted(
        bundle.by_book.items(),
        key=lambda item: (item[0][0], item[0][1], -item[1], item[0][2]),
    ):
        rows.append(scope_row(label, {"book": book}, pos, lemma, count, bundle))
    return rows


def chapter_rows(label: str, bundle: MorphCountBundle) -> list[dict[str, object]]:
    rows = []
    for (book, chapter, pos, lemma), count in sorted(
        bundle.by_chapter.items(),
        key=lambda item: (item[0][0], chapter_sort_key(item[0][1]), item[0][2], -item[1], item[0][3]),
    ):
        rows.append(scope_row(label, {"book": book, "chapter": chapter}, pos, lemma, count, bundle))
    return rows


def verse_rows(label: str, bundle: MorphCountBundle) -> list[dict[str, object]]:
    rows = []
    for (ref, pos, lemma, raw_word), count in sorted(
        bundle.by_verse.items(),
        key=lambda item: (item[0][0], item[0][1], item[0][2], item[0][3]),
    ):
        row = {
            "corpus": label,
            "ref": ref,
            "pos": pos,
            "normalized_lemma": lemma,
            "display_lemma": preferred_display(bundle.display_lemmas, lemma),
            "display_word": preferred_word(bundle.display_words, pos, lemma),
            "raw_word": raw_word,
            "count": count,
            "multiples": format_multiples(count),
        }
        row.update(multiple_flags(count))
        rows.append(row)
    return rows


def multiples_rows(label: str, bundle: MorphCountBundle) -> list[dict[str, object]]:
    return [row for row in lemma_rows(label, bundle) if row["multiples"]]


def scope_row(
    label: str,
    scope: dict[str, str],
    pos: str,
    lemma: str,
    count: int,
    bundle: MorphCountBundle,
) -> dict[str, object]:
    row = {
        "corpus": label,
        **scope,
        "pos": pos,
        "normalized_lemma": lemma,
        "display_lemma": preferred_display(bundle.display_lemmas, lemma),
        "display_word": preferred_word(bundle.display_words, pos, lemma),
        "count": count,
        "multiples": format_multiples(count),
    }
    row.update(multiple_flags(count))
    return row


def chapter_sort_key(value: str) -> tuple[int, str]:
    return (int(value), "") if value.isdigit() else (9999, value)


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(corpora: list[dict[str, object]]) -> None:
    OUT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    OUT_MANIFEST.write_text(
        json.dumps(
            {
                "tool": "morphology_counts",
                "created_utc": datetime.now(UTC).isoformat(),
                "sources": {
                    "oshb_dir": str(OSHB_DIR.resolve()),
                    "morphgnt_dir": str(MORPHGNT_DIR.resolve()),
                },
                "content_pos": sorted(CONTENT_POS),
                "multiples": list(DEFAULT_MULTIPLES),
                "corpora": corpora,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
