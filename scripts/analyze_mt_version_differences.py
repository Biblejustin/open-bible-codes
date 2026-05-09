#!/usr/bin/env python3
"""Compare normalized verse text across Hebrew MT-family corpora."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, VerseSpan, load_corpus


DEFAULT_CORPORA = [
    "MT_WLC=configs/example_oshb_wlc.toml",
    "UXLC=configs/example_uxlc.toml",
    "MAM=configs/example_mam.toml",
    "EBIBLE_WLC=configs/example_ebible_hebwlc.toml",
    "UHB=configs/example_uhb.toml",
]
OUT_DIR = Path("reports/mt_version_comparison")
SUMMARY_OUT = OUT_DIR / "summary.csv"
DIFFS_OUT = OUT_DIR / "verse_differences.csv"
MD_OUT = OUT_DIR / "mt_version_comparison.md"
MANIFEST_OUT = OUT_DIR / "manifest.json"

SUMMARY_FIELDNAMES = [
    "pair",
    "left",
    "right",
    "left_verses",
    "right_verses",
    "shared_refs",
    "equal_refs",
    "different_refs",
    "left_only_refs",
    "right_only_refs",
    "left_letters",
    "right_letters",
]

DIFF_FIELDNAMES = [
    "pair",
    "ref",
    "status",
    "left",
    "right",
    "left_length",
    "right_length",
    "length_delta",
    "first_diff_index",
    "left_window",
    "right_window",
    "left_text",
    "right_text",
]

BOOK_ALIASES = {
    "gen": "Gen",
    "genesis": "Gen",
    "ex": "Exod",
    "exo": "Exod",
    "exod": "Exod",
    "exodus": "Exod",
    "lev": "Lev",
    "levit": "Lev",
    "leviticus": "Lev",
    "num": "Num",
    "numbers": "Num",
    "deut": "Deut",
    "deu": "Deut",
    "deuter": "Deut",
    "deuteronomy": "Deut",
    "josh": "Josh",
    "jos": "Josh",
    "joshua": "Josh",
    "judg": "Judg",
    "jdg": "Judg",
    "judges": "Judg",
    "1sa": "1Sam",
    "1sam": "1Sam",
    "1samuel": "1Sam",
    "1 sam": "1Sam",
    "1 samuel": "1Sam",
    "2sa": "2Sam",
    "2sam": "2Sam",
    "2samuel": "2Sam",
    "2 sam": "2Sam",
    "2 samuel": "2Sam",
    "1kgs": "1Kgs",
    "1kings": "1Kgs",
    "1 kgs": "1Kgs",
    "1 kings": "1Kgs",
    "1ki": "1Kgs",
    "2kgs": "2Kgs",
    "2kings": "2Kgs",
    "2 kgs": "2Kgs",
    "2 kings": "2Kgs",
    "2ki": "2Kgs",
    "isa": "Isa",
    "isaiah": "Isa",
    "jer": "Jer",
    "jeremiah": "Jer",
    "ezek": "Ezek",
    "ezekiel": "Ezek",
    "ezk": "Ezek",
    "hos": "Hos",
    "hosea": "Hos",
    "joel": "Joel",
    "jol": "Joel",
    "amos": "Amos",
    "amo": "Amos",
    "obad": "Obad",
    "obadiah": "Obad",
    "oba": "Obad",
    "jonah": "Jonah",
    "jon": "Jonah",
    "mic": "Mic",
    "micah": "Mic",
    "nah": "Nah",
    "nahum": "Nah",
    "nam": "Nah",
    "hab": "Hab",
    "habakkuk": "Hab",
    "zeph": "Zeph",
    "zephaniah": "Zeph",
    "tsefaniah": "Zeph",
    "zep": "Zeph",
    "hag": "Hag",
    "haggai": "Hag",
    "zech": "Zech",
    "zechariah": "Zech",
    "zec": "Zech",
    "mal": "Mal",
    "malachi": "Mal",
    "ps": "Ps",
    "psa": "Ps",
    "psalm": "Ps",
    "psalms": "Ps",
    "prov": "Prov",
    "proverbs": "Prov",
    "pro": "Prov",
    "job": "Job",
    "song": "Song",
    "song of songs": "Song",
    "sng": "Song",
    "ruth": "Ruth",
    "rut": "Ruth",
    "lam": "Lam",
    "lamentations": "Lam",
    "eccl": "Eccl",
    "ecclesiastes": "Eccl",
    "ecc": "Eccl",
    "esth": "Esth",
    "esther": "Esth",
    "est": "Esth",
    "dan": "Dan",
    "daniel": "Dan",
    "ezra": "Ezra",
    "ezr": "Ezra",
    "neh": "Neh",
    "nehemiah": "Neh",
    "1chr": "1Chr",
    "1ch": "1Chr",
    "1chronicles": "1Chr",
    "1 chr": "1Chr",
    "1 chronicles": "1Chr",
    "2chr": "2Chr",
    "2ch": "2Chr",
    "2chronicles": "2Chr",
    "2 chr": "2Chr",
    "2 chronicles": "2Chr",
}

BOOK_ORDER = {
    book: index
    for index, book in enumerate(
        [
            "Gen",
            "Exod",
            "Lev",
            "Num",
            "Deut",
            "Josh",
            "Judg",
            "1Sam",
            "2Sam",
            "1Kgs",
            "2Kgs",
            "Isa",
            "Jer",
            "Ezek",
            "Hos",
            "Joel",
            "Amos",
            "Obad",
            "Jonah",
            "Mic",
            "Nah",
            "Hab",
            "Zeph",
            "Hag",
            "Zech",
            "Mal",
            "Ps",
            "Prov",
            "Job",
            "Song",
            "Ruth",
            "Lam",
            "Eccl",
            "Esth",
            "Dan",
            "Ezra",
            "Neh",
            "1Chr",
            "2Chr",
        ],
        start=1,
    )
}


@dataclass(frozen=True)
class VerseRecord:
    label: str
    ref: str
    key: tuple[str, int, int]
    normalized: str


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpora = load_labeled_corpora(args.corpus or DEFAULT_CORPORA)
    verse_maps = {
        label: verses_by_key(label, corpus)
        for label, corpus in corpora.items()
    }
    summary_rows, diff_rows = compare_all(verse_maps, corpora)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.diffs_out, DIFF_FIELDNAMES, diff_rows)
    write_markdown(args.markdown_out, summary_rows, diff_rows, corpora, args)
    write_manifest(args, corpora, len(summary_rows), len(diff_rows), started)
    print(args.summary_out)
    print(args.diffs_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", action="append", default=[])
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--diffs-out", type=Path, default=DIFFS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    parser.add_argument("--examples", type=int, default=30)
    return parser


def load_labeled_corpora(values: list[str]) -> dict[str, Corpus]:
    corpora: dict[str, Corpus] = {}
    for value in values:
        label, config = split_labeled_path(value)
        corpora[label] = load_corpus(config)
    return corpora


def split_labeled_path(value: str) -> tuple[str, Path]:
    if "=" not in value:
        path = Path(value)
        return path.stem, path
    label, path = value.split("=", 1)
    if not label:
        raise ValueError(f"empty corpus label: {value}")
    return label, Path(path)


def verses_by_key(label: str, corpus: Corpus) -> dict[tuple[str, int, int], VerseRecord]:
    records: dict[tuple[str, int, int], VerseRecord] = {}
    for verse in corpus.verses:
        key = verse_key(verse)
        records[key] = VerseRecord(
            label=label,
            ref=format_key(key),
            key=key,
            normalized=normalized_verse_text(corpus, verse),
        )
    return records


def verse_key(verse: VerseSpan) -> tuple[str, int, int]:
    return (
        normalize_book(verse.book),
        int(verse.chapter),
        int(verse.verse),
    )


def normalize_book(book: str) -> str:
    cleaned = " ".join(book.strip().replace("_", " ").split()).lower()
    collapsed = cleaned.replace(" ", "")
    for key in (cleaned, collapsed):
        if key in BOOK_ALIASES:
            return BOOK_ALIASES[key]
    raise ValueError(f"unsupported book label: {book}")


def normalized_verse_text(corpus: Corpus, verse: VerseSpan) -> str:
    if verse.norm_length <= 0:
        return ""
    return corpus.text[verse.norm_start : verse.norm_end + 1]


def compare_all(
    verse_maps: dict[str, dict[tuple[str, int, int], VerseRecord]],
    corpora: dict[str, Corpus],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    labels = list(verse_maps)
    summary_rows: list[dict[str, object]] = []
    diff_rows: list[dict[str, object]] = []
    for left_index, left in enumerate(labels):
        for right in labels[left_index + 1 :]:
            summary, diffs = compare_pair(
                left,
                verse_maps[left],
                right,
                verse_maps[right],
                corpora[left],
                corpora[right],
            )
            summary_rows.append(summary)
            diff_rows.extend(diffs)
    return summary_rows, sorted(diff_rows, key=diff_sort_key)


def compare_pair(
    left: str,
    left_map: dict[tuple[str, int, int], VerseRecord],
    right: str,
    right_map: dict[tuple[str, int, int], VerseRecord],
    left_corpus: Corpus,
    right_corpus: Corpus,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    left_keys = set(left_map)
    right_keys = set(right_map)
    shared_keys = sorted(left_keys & right_keys, key=sort_key)
    left_only = sorted(left_keys - right_keys, key=sort_key)
    right_only = sorted(right_keys - left_keys, key=sort_key)
    pair = f"{left}_vs_{right}"
    diff_rows: list[dict[str, object]] = []
    equal_refs = 0
    different_refs = 0
    for key in shared_keys:
        left_record = left_map[key]
        right_record = right_map[key]
        if left_record.normalized == right_record.normalized:
            equal_refs += 1
            continue
        different_refs += 1
        diff_rows.append(diff_row(pair, left_record, right_record, "different"))
    for key in left_only:
        diff_rows.append(
            diff_row(pair, left_map[key], empty_record(right, key), "left_only")
        )
    for key in right_only:
        diff_rows.append(
            diff_row(pair, empty_record(left, key), right_map[key], "right_only")
        )
    return (
        {
            "pair": pair,
            "left": left,
            "right": right,
            "left_verses": len(left_map),
            "right_verses": len(right_map),
            "shared_refs": len(shared_keys),
            "equal_refs": equal_refs,
            "different_refs": different_refs,
            "left_only_refs": len(left_only),
            "right_only_refs": len(right_only),
            "left_letters": len(left_corpus.text),
            "right_letters": len(right_corpus.text),
        },
        diff_rows,
    )


def diff_row(
    pair: str,
    left_record: VerseRecord,
    right_record: VerseRecord,
    status: str,
) -> dict[str, object]:
    first_diff = first_difference_index(left_record.normalized, right_record.normalized)
    return {
        "pair": pair,
        "ref": left_record.ref or right_record.ref,
        "status": status,
        "left": left_record.label,
        "right": right_record.label,
        "left_length": len(left_record.normalized),
        "right_length": len(right_record.normalized),
        "length_delta": len(left_record.normalized) - len(right_record.normalized),
        "first_diff_index": "" if first_diff is None else first_diff,
        "left_window": diff_window(left_record.normalized, first_diff),
        "right_window": diff_window(right_record.normalized, first_diff),
        "left_text": left_record.normalized,
        "right_text": right_record.normalized,
    }


def empty_record(label: str, key: tuple[str, int, int]) -> VerseRecord:
    return VerseRecord(label=label, ref=format_key(key), key=key, normalized="")


def first_difference_index(left: str, right: str) -> int | None:
    for index, (left_char, right_char) in enumerate(zip(left, right, strict=False)):
        if left_char != right_char:
            return index
    if len(left) != len(right):
        return min(len(left), len(right))
    return None


def diff_window(value: str, index: int | None, *, radius: int = 16) -> str:
    if index is None:
        return ""
    start = max(0, index - radius)
    end = min(len(value), index + radius + 1)
    return value[start:end]


def sort_key(key: tuple[str, int, int]) -> tuple[int, int, int, str]:
    book, chapter, verse = key
    return (BOOK_ORDER.get(book, 999), chapter, verse, book)


def diff_sort_key(row: dict[str, object]) -> tuple[str, int, tuple[int, int, int, str]]:
    status_order = {"different": 0, "left_only": 1, "right_only": 2}
    return (
        str(row["pair"]),
        status_order.get(str(row["status"]), 9),
        parse_formatted_ref(str(row["ref"])),
    )


def parse_formatted_ref(ref: str) -> tuple[int, int, int, str]:
    book, rest = ref.rsplit(" ", 1)
    chapter, verse = rest.split(":", 1)
    return (BOOK_ORDER.get(book, 999), int(chapter), int(verse), book)


def format_key(key: tuple[str, int, int]) -> str:
    book, chapter, verse = key
    return f"{book} {chapter}:{verse}"


def write_rows(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    diff_rows: list[dict[str, object]],
    corpora: dict[str, Corpus],
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    status_counts = Counter(str(row["status"]) for row in diff_rows)
    lines = [
        "# MT Version Comparison",
        "",
        "This report compares normalized consonantal verse text across the configured",
        "Hebrew MT-family corpora. It aligns verses by canonical book/chapter/verse",
        "labels before comparing text.",
        "",
        "## Corpora",
        "",
        "| Corpus | Verses | Letters |",
        "| --- | ---: | ---: |",
    ]
    for label, corpus in corpora.items():
        lines.append(f"| {label} | {len(corpus.verses):,} | {len(corpus.text):,} |")
    lines.extend(
        [
            "",
            "## Pair Summary",
            "",
            "| Pair | Shared refs | Equal refs | Different refs | Left-only | Right-only |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary_rows:
        lines.append(
            f"| {row['pair']} | {int(row['shared_refs']):,} | "
            f"{int(row['equal_refs']):,} | {int(row['different_refs']):,} | "
            f"{int(row['left_only_refs']):,} | {int(row['right_only_refs']):,} |"
        )
    lines.extend(
        [
            "",
            "## Difference Status Counts",
            "",
            "| Status | Rows |",
            "| --- | ---: |",
        ]
    )
    for status, count in sorted(status_counts.items()):
        lines.append(f"| {status} | {count:,} |")
    lines.extend(
        [
            "",
            "## Largest Length Deltas",
            "",
            "| Pair | Ref | Status | Left length | Right length | Delta | First differing window |",
            "| --- | --- | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in largest_length_deltas(diff_rows, args.examples):
        window = f"{row['left_window']} / {row['right_window']}"
        lines.append(
            f"| {row['pair']} | {row['ref']} | {row['status']} | "
            f"{row['left_length']} | {row['right_length']} | {row['length_delta']} | "
            f"`{window}` |"
        )
    lines.extend(
        [
            "",
            "## First Differences",
            "",
            "| Pair | Ref | Status | First index | Left window | Right window |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in [row for row in diff_rows if row["status"] == "different"][: args.examples]:
        lines.append(
            f"| {row['pair']} | {row['ref']} | {row['status']} | "
            f"{row['first_diff_index']} | `{row['left_window']}` | "
            f"`{row['right_window']}` |"
        )
    lines.extend(
        [
            "",
            "## Cautions",
            "",
            "- This is a normalized consonantal comparison, not a full diplomatic collation.",
            "- Vowels, cantillation, punctuation, and final-form distinctions are removed",
            "  under the normal ELS settings.",
            "- MAM has fewer parsed verse rows than the Leningrad-family streams; missing",
            "  aligned refs are reported instead of silently filled.",
            "- Some left-only/right-only refs reflect versification differences. The text",
            "  can still be present under nearby shifted refs in another corpus.",
            "- Different rows are review queues. They are not claims by themselves.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def largest_length_deltas(
    rows: list[dict[str, object]],
    limit: int,
) -> list[dict[str, object]]:
    return sorted(
        rows,
        key=lambda row: (-abs(int(row["length_delta"])), str(row["pair"]), str(row["ref"])),
    )[:limit]


def write_manifest(
    args: argparse.Namespace,
    corpora: dict[str, Corpus],
    summary_count: int,
    diff_count: int,
    started: float,
) -> None:
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "script": Path(__file__).name,
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "corpora": {
            label: {"name": corpus.name, "verses": len(corpus.verses), "letters": len(corpus.text)}
            for label, corpus in corpora.items()
        },
        "summary_rows": summary_count,
        "diff_rows": diff_count,
        "outputs": {
            "summary": str(args.summary_out),
            "diffs": str(args.diffs_out),
            "markdown": str(args.markdown_out),
        },
    }
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
