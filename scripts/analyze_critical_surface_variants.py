#!/usr/bin/env python3
"""Compare TR and SBLGNT surface content-word counts, including variants."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els.corpus import Corpus, load_corpus
from els.critical import BOOK_TO_SBL, classify_missing_verses
from els.word_counts import content_key_for_word, content_words, multiple_flags, multiples_for_count


TR_CONFIG = Path("configs/example_ebible_grctr.toml")
SBL_CONFIG = Path("configs/example_sblgnt.toml")

OUT_COUNTS = Path("reports/critical_surface_tr_vs_sbl_counts.csv")
OUT_VERSES = Path("reports/critical_surface_variant_verses.csv")
OUT_MANIFEST = Path("reports/critical_surface_variants.manifest.json")


def main() -> int:
    tr = load_corpus(TR_CONFIG)
    sbl = load_corpus(SBL_CONFIG)
    tr_by_key = {canonical_key_tr(verse.book, verse.chapter, verse.verse): verse for verse in tr.verses}
    sbl_by_key = {canonical_key_sbl(verse.book, verse.chapter, verse.verse): verse for verse in sbl.verses}
    common_keys = sorted(set(tr_by_key) & set(sbl_by_key), key=ref_sort_key)
    missing_blocks = classify_missing_verses(tr, sbl)

    tr_counts = Counter(content_key_for_word(tr, word) for word in content_words(tr))
    sbl_counts = Counter(content_key_for_word(sbl, word) for word in content_words(sbl))
    write_rows(OUT_COUNTS, count_delta_rows(tr_counts, sbl_counts))

    tr_words_by_ref = words_by_ref(tr)
    sbl_words_by_ref = words_by_ref(sbl)
    verse_rows = []
    for key in common_keys:
        tr_ref = tr_by_key[key].ref
        sbl_ref = sbl_by_key[key].ref
        tr_counter = tr_words_by_ref.get(tr_ref, Counter())
        sbl_counter = sbl_words_by_ref.get(sbl_ref, Counter())
        if tr_counter == sbl_counter:
            continue
        tr_only = tr_counter - sbl_counter
        sbl_only = sbl_counter - tr_counter
        verse_rows.append(
            {
                "canonical_ref": format_key(key),
                "tr_ref": tr_ref,
                "sbl_ref": sbl_ref,
                "tr_content_word_count": sum(tr_counter.values()),
                "sbl_content_word_count": sum(sbl_counter.values()),
                "net_delta_sbl_minus_tr": sum(sbl_counter.values()) - sum(tr_counter.values()),
                "tr_only_count": sum(tr_only.values()),
                "sbl_only_count": sum(sbl_only.values()),
                "tr_only_words": format_counter(tr_only),
                "sbl_only_words": format_counter(sbl_only),
            }
        )
    write_rows(OUT_VERSES, verse_rows)
    write_manifest(tr, sbl, missing_blocks, common_keys, verse_rows)

    for path in [OUT_COUNTS, OUT_VERSES, OUT_MANIFEST]:
        print(path)
    return 0


def words_by_ref(corpus: Corpus) -> dict[str, Counter[str]]:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for word in content_words(corpus):
        grouped[word.ref][content_key_for_word(corpus, word)] += 1
    return dict(grouped)


def count_delta_rows(tr_counts: Counter[str], sbl_counts: Counter[str]) -> list[dict[str, object]]:
    rows = []
    for word in sorted(set(tr_counts) | set(sbl_counts)):
        tr_count = tr_counts.get(word, 0)
        sbl_count = sbl_counts.get(word, 0)
        if tr_count == sbl_count:
            continue
        tr_multiples = set(multiples_for_count(tr_count))
        sbl_multiples = set(multiples_for_count(sbl_count))
        broken = sorted(tr_multiples - sbl_multiples)
        created = sorted(sbl_multiples - tr_multiples)
        row = {
            "normalized_word": word,
            "tr_count": tr_count,
            "sblgnt_count": sbl_count,
            "delta_sbl_minus_tr": sbl_count - tr_count,
            "tr_multiples": format_multiples(tr_multiples),
            "sblgnt_multiples": format_multiples(sbl_multiples),
            "broken_multiples": format_multiples(broken),
            "created_multiples": format_multiples(created),
        }
        row.update({f"tr_{key}": value for key, value in multiple_flags(tr_count).items()})
        row.update({f"sbl_{key}": value for key, value in multiple_flags(sbl_count).items()})
        rows.append(row)
    rows.sort(
        key=lambda row: (
            0 if row["broken_multiples"] or row["created_multiples"] else 1,
            -abs(int(row["delta_sbl_minus_tr"])),
            row["normalized_word"],
        )
    )
    return rows


def canonical_key_tr(book: str, chapter: str, verse: str) -> tuple[str, str, str]:
    return BOOK_TO_SBL.get(book, book), chapter, verse


def canonical_key_sbl(book: str, chapter: str, verse: str) -> tuple[str, str, str]:
    return book, chapter, verse


def format_key(key: tuple[str, str, str]) -> str:
    return f"{key[0]} {key[1]}:{key[2]}"


def ref_sort_key(key: tuple[str, str, str]) -> tuple[str, int, int, str, str]:
    chapter = int(key[1]) if key[1].isdigit() else 9999
    verse = int(key[2]) if key[2].isdigit() else 9999
    return key[0], chapter, verse, key[1], key[2]


def format_counter(counter: Counter[str]) -> str:
    return ";".join(f"{word}:{count}" for word, count in counter.most_common(20))


def format_multiples(values) -> str:
    return ";".join(str(value) for value in sorted(values))


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(tr, sbl, missing_blocks, common_keys, verse_rows) -> None:
    OUT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    OUT_MANIFEST.write_text(
        json.dumps(
            {
                "tool": "critical_surface_variants",
                "created_utc": datetime.now(UTC).isoformat(),
                "tr_config": str(TR_CONFIG.resolve()),
                "sbl_config": str(SBL_CONFIG.resolve()),
                "tr_corpus": tr.summary(),
                "sbl_corpus": sbl.summary(),
                "common_refs": len(common_keys),
                "variant_common_refs": len(verse_rows),
                "ref_missing_verses": len(missing_blocks),
                "deleted_refs_used": sum(block.used_as_deletion for block in missing_blocks),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
