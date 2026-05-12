"""Helpers for post-search ELS match strata.

These helpers annotate already-discovered hits. They do not widen a search by
themselves; callers are responsible for declaring the term/corpus/control family
before using the resulting strata in a study.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .corpus import NT_BOOK_ORDER, OT_BOOK_ORDER, Corpus, VerseSpan


DIRECTION_FORWARD_ONLY = "forward_only"
DIRECTION_BACKWARD_ONLY = "backward_only"
DIRECTION_BIDIRECTIONAL = "bidirectional_present"
DIRECTION_UNKNOWN = "direction_unknown"


BOOK_ALIASES = {
    "gen": "Gen",
    "genesis": "Gen",
    "ex": "Exod",
    "exo": "Exod",
    "exod": "Exod",
    "exodus": "Exod",
    "lev": "Lev",
    "leviticus": "Lev",
    "num": "Num",
    "numbers": "Num",
    "deut": "Deut",
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
    "hos": "Hos",
    "hosea": "Hos",
    "obad": "Obad",
    "obadiah": "Obad",
    "jon": "Jonah",
    "jonah": "Jonah",
    "mic": "Mic",
    "micah": "Mic",
    "nah": "Nah",
    "nahum": "Nah",
    "hab": "Hab",
    "habakkuk": "Hab",
    "zeph": "Zeph",
    "zephaniah": "Zeph",
    "hag": "Hag",
    "haggai": "Hag",
    "zech": "Zech",
    "zechariah": "Zech",
    "mal": "Mal",
    "malachi": "Mal",
    "ps": "Ps",
    "psa": "Ps",
    "psalm": "Ps",
    "psalms": "Ps",
    "prov": "Prov",
    "proverbs": "Prov",
    "job": "Job",
    "song": "Song",
    "songofsongs": "Song",
    "song of songs": "Song",
    "ruth": "Ruth",
    "lam": "Lam",
    "lamentations": "Lam",
    "eccl": "Eccl",
    "ecclesiastes": "Eccl",
    "esth": "Esth",
    "esther": "Esth",
    "dan": "Dan",
    "daniel": "Dan",
    "ezra": "Ezra",
    "neh": "Neh",
    "nehemiah": "Neh",
    "1chr": "1Chr",
    "1chronicles": "1Chr",
    "1 chr": "1Chr",
    "1 chronicles": "1Chr",
    "2chr": "2Chr",
    "2chronicles": "2Chr",
    "2 chr": "2Chr",
    "2 chronicles": "2Chr",
    "matt": "Matt",
    "mat": "Matt",
    "matthew": "Matt",
    "mark": "Mark",
    "mrk": "Mark",
    "luke": "Luke",
    "luk": "Luke",
    "john": "John",
    "jhn": "John",
    "acts": "Acts",
    "act": "Acts",
    "rom": "Rom",
    "romans": "Rom",
    "1cor": "1Cor",
    "1corinthians": "1Cor",
    "1 cor": "1Cor",
    "1 corinthians": "1Cor",
    "2cor": "2Cor",
    "2corinthians": "2Cor",
    "2 cor": "2Cor",
    "2 corinthians": "2Cor",
    "gal": "Gal",
    "galatians": "Gal",
    "eph": "Eph",
    "ephesians": "Eph",
    "phil": "Phil",
    "philippians": "Phil",
    "col": "Col",
    "colossians": "Col",
    "1thess": "1Thess",
    "1thessalonians": "1Thess",
    "1 thess": "1Thess",
    "1 thessalonians": "1Thess",
    "2thess": "2Thess",
    "2thessalonians": "2Thess",
    "2 thess": "2Thess",
    "2 thessalonians": "2Thess",
    "1tim": "1Tim",
    "1timothy": "1Tim",
    "1 tim": "1Tim",
    "1 timothy": "1Tim",
    "2tim": "2Tim",
    "2timothy": "2Tim",
    "2 tim": "2Tim",
    "2 timothy": "2Tim",
    "titus": "Titus",
    "phlm": "Phlm",
    "philemon": "Phlm",
    "heb": "Heb",
    "hebrews": "Heb",
    "jas": "Jas",
    "james": "Jas",
    "1pet": "1Pet",
    "1peter": "1Pet",
    "1 pet": "1Pet",
    "1 peter": "1Pet",
    "2pet": "2Pet",
    "2peter": "2Pet",
    "2 pet": "2Pet",
    "2 peter": "2Pet",
    "1john": "1John",
    "1 john": "1John",
    "2john": "2John",
    "2 john": "2John",
    "3john": "3John",
    "3 john": "3John",
    "jude": "Jude",
    "rev": "Rev",
    "revelation": "Rev",
    "revelations": "Rev",
}

BOOK_ORDER = {
    **OT_BOOK_ORDER,
    **{book: 1000 + order for book, order in NT_BOOK_ORDER.items()},
}

REF_RE = re.compile(r"^(?P<book>.+?)\s+(?P<chapter>\d+):(?P<verse>\d+)")


@dataclass(frozen=True)
class ParsedRef:
    book: str
    chapter: int
    verse: int


@dataclass(frozen=True)
class DirectionCounts:
    forward: int = 0
    backward: int = 0


@dataclass(frozen=True)
class BoundaryIndex:
    verse_by_position: Sequence[int]
    verses: Sequence[VerseSpan]
    first_chapter_verse_indexes: frozenset[int]
    last_chapter_verse_indexes: frozenset[int]
    first_book_verse_indexes: frozenset[int]
    last_book_verse_indexes: frozenset[int]


def direction_counts_from_row(row: Mapping[str, Any]) -> DirectionCounts:
    direction = str(row.get("direction", "")).strip().lower()
    skips = parse_skip_values(row.get("skip", ""))
    forward = 0
    backward = 0
    if direction == "both":
        forward += 1
        backward += 1
    elif direction == "forward":
        forward += 1
    elif direction == "backward":
        backward += 1

    for skip in skips:
        if skip > 0:
            forward += 1
        elif skip < 0:
            backward += 1

    if not direction and not skips:
        return DirectionCounts()
    return DirectionCounts(forward=forward, backward=backward)


def direction_stratum(counts: DirectionCounts) -> str:
    if counts.forward and counts.backward:
        return DIRECTION_BIDIRECTIONAL
    if counts.forward:
        return DIRECTION_FORWARD_ONLY
    if counts.backward:
        return DIRECTION_BACKWARD_ONLY
    return DIRECTION_UNKNOWN


def direction_strata_by_key(
    rows: Iterable[Mapping[str, Any]],
    *,
    key_fields: Sequence[str],
) -> dict[tuple[str, ...], str]:
    totals: dict[tuple[str, ...], Counter[str]] = defaultdict(Counter)
    for row in rows:
        key = tuple(str(row.get(field, "")) for field in key_fields)
        counts = direction_counts_from_row(row)
        totals[key]["forward"] += counts.forward
        totals[key]["backward"] += counts.backward
    return {
        key: direction_stratum(DirectionCounts(counts["forward"], counts["backward"]))
        for key, counts in totals.items()
    }


def parse_skip_values(value: Any) -> tuple[int, ...]:
    text = str(value or "")
    if not text:
        return ()
    values = []
    for part in re.split(r"[;,| ]+", text):
        if not part:
            continue
        try:
            values.append(int(part))
        except ValueError:
            continue
    return tuple(values)


def parse_ref(value: Any) -> ParsedRef | None:
    text = str(value or "").split("=", 1)[0].strip()
    match = REF_RE.match(text)
    if not match:
        return None
    book = normalize_book(match.group("book"))
    if not book:
        return None
    return ParsedRef(book=book, chapter=int(match.group("chapter")), verse=int(match.group("verse")))


def canonical_ref_sort_key(value: Any) -> tuple[int, int, int, str]:
    parsed = parse_ref(value)
    if parsed is None:
        return (999999, 999999, 999999, str(value or ""))
    return (BOOK_ORDER.get(parsed.book, 999999), parsed.chapter, parsed.verse, parsed.book)


def normalize_book(value: str) -> str:
    cleaned = " ".join(value.strip().replace("_", " ").split()).lower()
    collapsed = cleaned.replace(" ", "")
    return BOOK_ALIASES.get(cleaned) or BOOK_ALIASES.get(collapsed) or value.strip()


def canonical_first_keys(
    rows: Iterable[Mapping[str, Any]],
    *,
    group_fields: Sequence[str],
    ref_field: str = "center_ref",
) -> set[tuple[str, ...]]:
    grouped: dict[tuple[str, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(str(row.get(field, "")) for field in group_fields)].append(row)
    first_keys = set()
    for group_rows in grouped.values():
        first = min(
            group_rows,
            key=lambda row: (
                canonical_ref_sort_key(row.get(ref_field, "")),
                str(row.get("occurrence_rank", "")),
                str(row.get("source_record", "")),
            ),
        )
        first_keys.add(row_identity(first))
    return first_keys


def row_identity(row: Mapping[str, Any]) -> tuple[str, ...]:
    return (
        str(row.get("source_family", "")),
        str(row.get("source_queue", "")),
        str(row.get("corpus", "")),
        str(row.get("present_corpora", "")),
        str(row.get("term_id", "")),
        str(row.get("normalized_term", "")),
        str(row.get("center_ref", "")),
        str(row.get("center_word", "")),
        str(row.get("source_record", "")),
    )


def build_boundary_index(corpus: Corpus) -> BoundaryIndex:
    first_chapter: set[int] = set()
    last_chapter: set[int] = set()
    first_book: set[int] = set()
    last_book: set[int] = set()
    previous_chapter_key: tuple[str, str] | None = None
    previous_book: str | None = None

    for index, verse in enumerate(corpus.verses):
        chapter_key = (verse.book, verse.chapter)
        if chapter_key != previous_chapter_key:
            first_chapter.add(index)
            if index > 0:
                last_chapter.add(index - 1)
            previous_chapter_key = chapter_key
        if verse.book != previous_book:
            first_book.add(index)
            if index > 0:
                last_book.add(index - 1)
            previous_book = verse.book
    if corpus.verses:
        last_chapter.add(len(corpus.verses) - 1)
        last_book.add(len(corpus.verses) - 1)

    return BoundaryIndex(
        verse_by_position=corpus.position_to_verse,
        verses=corpus.verses,
        first_chapter_verse_indexes=frozenset(first_chapter),
        last_chapter_verse_indexes=frozenset(last_chapter),
        first_book_verse_indexes=frozenset(first_book),
        last_book_verse_indexes=frozenset(last_book),
    )


def boundary_strata_for_offsets(
    *,
    start_offset: int,
    end_offset: int,
    boundary_index: BoundaryIndex,
    tolerance: int = 1,
) -> tuple[str, ...]:
    if start_offset < 0 or end_offset < 0:
        return ()
    if start_offset >= len(boundary_index.verse_by_position) or end_offset >= len(boundary_index.verse_by_position):
        return ()

    start_verse_index = boundary_index.verse_by_position[start_offset]
    end_verse_index = boundary_index.verse_by_position[end_offset]
    start_verse = boundary_index.verses[start_verse_index]
    end_verse = boundary_index.verses[end_verse_index]
    start_delta = start_offset - start_verse.norm_start
    end_delta = (end_verse.norm_end - 1) - end_offset

    strata: list[str] = []
    start_on_verse = 0 <= start_delta <= tolerance
    end_on_verse = 0 <= end_delta <= tolerance
    if start_on_verse:
        strata.append("boundary_start_verse")
    if end_on_verse:
        strata.append("boundary_end_verse")
    if start_on_verse and start_verse_index in boundary_index.first_chapter_verse_indexes:
        strata.append("boundary_start_chapter")
    if end_on_verse and end_verse_index in boundary_index.last_chapter_verse_indexes:
        strata.append("boundary_end_chapter")
    if start_on_verse and start_verse_index in boundary_index.first_book_verse_indexes:
        strata.append("boundary_start_book")
    if end_on_verse and end_verse_index in boundary_index.last_book_verse_indexes:
        strata.append("boundary_end_book")
    if any(value.startswith("boundary_start_") for value in strata) and any(
        value.startswith("boundary_end_") for value in strata
    ):
        strata.append("boundary_both_endpoints")
    return tuple(strata)
