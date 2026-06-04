"""Load configured Bible text into a normalized letter stream."""

from __future__ import annotations

import csv
import gzip
import hashlib
import html.parser
import json
import os
import pickle
import tomllib
import xml.etree.ElementTree as ET
from array import array
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .normalization import normalize_text
from .books import NT_BOOK_ORDER, OT_BOOK_ORDER


CORPUS_CACHE_VERSION = 3
DEFAULT_CORPUS_CACHE_DIR = Path(__file__).resolve().parents[1] / "data" / "cache" / "corpora"


@dataclass(frozen=True)
class VerseSpan:
    source: str
    ref: str
    book: str
    chapter: str
    verse: str
    raw_text: str
    norm_start: int
    norm_end: int
    norm_length: int


@dataclass(frozen=True)
class WordSpan:
    source: str
    ref: str
    book: str
    chapter: str
    verse: str
    word_index: int
    raw_word: str
    normalized_word: str
    norm_start: int
    norm_end: int
    norm_length: int


@dataclass(frozen=True)
class Corpus:
    name: str
    language: str
    keep_hebrew_final_forms: bool
    text: str
    verses: tuple[VerseSpan, ...]
    position_to_verse: Sequence[int]
    words: tuple[WordSpan, ...] = ()
    position_to_word: Sequence[int] = ()

    def ref_at(self, position: int) -> str:
        return self.verses[self.position_to_verse[position]].ref

    def source_at(self, position: int) -> str:
        return self.verses[self.position_to_verse[position]].source

    def word_at(self, position: int) -> WordSpan | None:
        if not self.position_to_word:
            return None
        return self.words[self.position_to_word[position]]

    def summary(self) -> dict[str, Any]:
        verse_counts = Counter(verse.source for verse in self.verses)
        letter_counts: Counter[str] = Counter()
        for verse in self.verses:
            letter_counts[verse.source] += verse.norm_length
        return {
            "name": self.name,
            "language": self.language,
            "keep_hebrew_final_forms": self.keep_hebrew_final_forms,
            "letters": len(self.text),
            "verses": len(self.verses),
            "sources": [
                {
                    "name": source,
                    "verses": verse_counts[source],
                    "letters": letter_counts[source],
                }
                for source in sorted(verse_counts)
            ],
        }

    def summary_json(self) -> str:
        return json.dumps(self.summary(), ensure_ascii=False, indent=2)


def load_corpus(config_path: str | Path, *, use_cache: bool | None = None) -> Corpus:
    config_file = Path(config_path).expanduser().resolve()
    with config_file.open("rb") as handle:
        config = tomllib.load(handle)

    if use_cache is None:
        use_cache = os.environ.get("EDLS_NO_CORPUS_CACHE") not in {"1", "true", "yes"}
    if use_cache:
        cache_path = corpus_cache_path(config_file, config)
        cached = read_cached_corpus(cache_path)
        if cached is not None:
            return cached
        corpus = build_corpus(config_file, config)
        write_cached_corpus(cache_path, corpus)
        return corpus

    return build_corpus(config_file, config)


def splice_verses_into_corpus(
    base: Corpus,
    donor: Corpus,
    donor_refs: list[str],
) -> Corpus:
    """Return a corpus with donor verses inserted in donor canonical order."""

    donor_ref_set = set(donor_refs)
    base_by_key = {
        (_canonical_nt_book(verse.book), verse.chapter, verse.verse): verse
        for verse in base.verses
    }
    letters: list[str] = []
    verses: list[VerseSpan] = []
    position_to_verse: list[int] = []
    for donor_verse in donor.verses:
        verse = donor_verse if donor_verse.ref in donor_ref_set else base_by_key.get(
            (_canonical_nt_book(donor_verse.book), donor_verse.chapter, donor_verse.verse)
        )
        if verse is None:
            continue
        start = len(letters)
        normalized = normalize_text(
            verse.raw_text,
            base.language,
            keep_hebrew_final_forms=base.keep_hebrew_final_forms,
        )
        verse_index = len(verses)
        letters.extend(normalized)
        position_to_verse.extend([verse_index] * len(normalized))
        verses.append(
            VerseSpan(
                source=verse.source,
                ref=verse.ref,
                book=verse.book,
                chapter=verse.chapter,
                verse=verse.verse,
                raw_text=verse.raw_text,
                norm_start=start,
                norm_end=len(letters) - 1,
                norm_length=len(normalized),
            )
        )
    return Corpus(
        name=f"{base.name}+spliced",
        language=base.language,
        keep_hebrew_final_forms=base.keep_hebrew_final_forms,
        text="".join(letters),
        verses=tuple(verses),
        position_to_verse=array("i", position_to_verse),
    )


def _canonical_nt_book(book: str) -> str:
    return {
        "Matt": "MAT",
        "Mark": "MRK",
        "Luke": "LUK",
        "John": "JHN",
        "Acts": "ACT",
        "Rom": "ROM",
        "1Cor": "1CO",
        "2Cor": "2CO",
        "Gal": "GAL",
        "Eph": "EPH",
        "Phil": "PHP",
        "Col": "COL",
        "1Thess": "1TH",
        "2Thess": "2TH",
        "1Tim": "1TI",
        "2Tim": "2TI",
        "Titus": "TIT",
        "Phlm": "PHM",
        "Heb": "HEB",
        "Jas": "JAS",
        "1Pet": "1PE",
        "2Pet": "2PE",
        "1John": "1JN",
        "2John": "2JN",
        "3John": "3JN",
        "Jude": "JUD",
        "Rev": "REV",
    }.get(book, book)


def build_corpus(config_file: Path, config: dict[str, Any]) -> Corpus:
    language = config["language"]
    keep_hebrew_final_forms = bool(config.get("keep_hebrew_final_forms", False))
    name = config.get("name", config_file.stem)

    verses: list[VerseSpan] = []
    words: list[WordSpan] = []
    letters: list[str] = []
    position_to_verse: list[int] = []
    position_to_word: list[int] = []

    for source_config in config.get("sources", []):
        for row in _read_source(config_file.parent, source_config):
            raw_text = row["text"]
            start = len(letters)
            verse_index = len(verses)
            normalized_words = _normalized_word_spans(
                raw_text,
                language,
                keep_hebrew_final_forms=keep_hebrew_final_forms,
            )
            normalized = "".join(word for _raw_word, word in normalized_words)
            direct_normalized = normalize_text(
                raw_text,
                language,
                keep_hebrew_final_forms=keep_hebrew_final_forms,
            )
            if normalized != direct_normalized:
                normalized_words = [(raw_text, direct_normalized)]
                normalized = direct_normalized
            for word_index_in_verse, (raw_word, normalized_word) in enumerate(
                normalized_words,
                start=1,
            ):
                word_start = len(letters)
                letters.extend(normalized_word)
                word_index = len(words)
                position_to_verse.extend([verse_index] * len(normalized_word))
                position_to_word.extend([word_index] * len(normalized_word))
                word_end = len(letters) - 1
                words.append(
                    WordSpan(
                        source=row["source"],
                        ref=row["ref"],
                        book=row.get("book", ""),
                        chapter=row.get("chapter", ""),
                        verse=row.get("verse", ""),
                        word_index=word_index_in_verse,
                        raw_word=raw_word,
                        normalized_word=normalized_word,
                        norm_start=word_start,
                        norm_end=word_end,
                        norm_length=len(normalized_word),
                    )
                )
            end = len(letters) - 1
            verses.append(
                VerseSpan(
                    source=row["source"],
                    ref=row["ref"],
                    book=row.get("book", ""),
                    chapter=row.get("chapter", ""),
                    verse=row.get("verse", ""),
                    raw_text=raw_text,
                    norm_start=start,
                    norm_end=end,
                    norm_length=len(normalized),
                )
            )

    return Corpus(
        name=name,
        language=language,
        keep_hebrew_final_forms=keep_hebrew_final_forms,
        text="".join(letters),
        verses=tuple(verses),
        position_to_verse=array("i", position_to_verse),
        words=tuple(words),
        position_to_word=array("i", position_to_word),
    )


def corpus_cache_path(config_file: Path, config: dict[str, Any]) -> Path:
    cache_dir = Path(
        os.environ.get("EDLS_CORPUS_CACHE_DIR", str(DEFAULT_CORPUS_CACHE_DIR))
    ).expanduser()
    digest = corpus_cache_key(config_file, config)
    return cache_dir / f"{digest}.pickle"


def corpus_cache_key(config_file: Path, config: dict[str, Any]) -> str:
    payload = {
        "version": CORPUS_CACHE_VERSION,
        # Absolute paths deliberately keep this local cache simple.
        "config_path": str(config_file),
        "config_sha256": hashlib.sha256(config_file.read_bytes()).hexdigest(),
        "sources": [
            source_cache_metadata(config_file.parent, source_config)
            for source_config in config.get("sources", [])
        ],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def source_cache_metadata(
    base_dir: Path,
    source_config: dict[str, Any],
) -> dict[str, object]:
    source_format = source_config.get("format", "csv")
    path = _resolve_path(base_dir, source_config["path"])
    return {
        "format": source_format,
        "path": str(path),
        "files": [file_cache_metadata(file) for file in source_files_for_cache(path, source_format)],
    }


def source_files_for_cache(path: Path, source_format: str) -> list[Path]:
    if source_format == "sblgnt_text_dir":
        return sorted(file for file in path.glob("*.txt") if file.is_file())
    if source_format == "oshb_wlc_dir":
        return sorted(file for file in path.glob("*.xml") if file.is_file())
    if source_format == "uxlc_dir":
        return sorted(
            file
            for file in path.glob("*.xml")
            if file.is_file() and file.stem in UXLC_BOOK_ORDER
        )
    if source_format == "mam_html_dir":
        return sorted(
            file
            for file in path.glob("*.html")
            if file.is_file() and file.stem in MAM_BOOK_ORDER
        )
    return [path]


def file_cache_metadata(path: Path) -> dict[str, object]:
    stat = path.stat()
    return {
        "path": str(path),
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
    }


def read_cached_corpus(cache_path: Path) -> Corpus | None:
    if not cache_path.exists():
        return None
    try:
        with cache_path.open("rb") as handle:
            cached = pickle.load(handle)
    except (OSError, pickle.PickleError, EOFError):
        return None
    if isinstance(cached, Corpus):
        return cached
    return None


def write_cached_corpus(cache_path: Path, corpus: Corpus) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = cache_path.with_suffix(f".{os.getpid()}.tmp")
    with temp_path.open("wb") as handle:
        pickle.dump(corpus, handle, protocol=pickle.HIGHEST_PROTOCOL)
    temp_path.replace(cache_path)


def _normalized_word_spans(
    raw_text: str,
    language: str,
    *,
    keep_hebrew_final_forms: bool,
) -> list[tuple[str, str]]:
    normalized_words: list[tuple[str, str]] = []
    for raw_word in raw_text.split():
        normalized_word = normalize_text(
            raw_word,
            language,
            keep_hebrew_final_forms=keep_hebrew_final_forms,
        )
        if normalized_word:
            normalized_words.append((raw_word, normalized_word))
    return normalized_words


def _read_source(base_dir: Path, source_config: dict[str, Any]) -> Iterable[dict[str, str]]:
    source_format = source_config.get("format", "csv")
    path = _resolve_path(base_dir, source_config["path"])
    source_name = source_config.get("name", path.stem)

    if source_format == "csv":
        yield from _read_csv(path, source_name, source_config)
        return
    if source_format == "michigan_claremont":
        yield from _read_michigan_claremont(path, source_name, source_config)
        return
    if source_format == "text":
        yield {
            "source": source_name,
            "ref": source_config.get("ref", source_name),
            "book": source_config.get("book", source_name),
            "chapter": "",
            "verse": "",
            "text": _read_text(path, source_config.get("encoding", "utf-8")),
        }
        return
    if source_format == "sblgnt_text_dir":
        yield from _read_sblgnt_text_dir(path, source_name, source_config)
        return
    if source_format == "oshb_wlc_dir":
        yield from _read_oshb_wlc_dir(path, source_name, source_config)
        return
    if source_format == "uxlc_dir":
        yield from _read_uxlc_dir(path, source_name, source_config)
        return
    if source_format == "mam_html_dir":
        yield from _read_mam_html_dir(path, source_name, source_config)
        return
    raise ValueError(f"unsupported source format: {source_format}")


def _read_csv(
    path: Path,
    source_name: str,
    source_config: dict[str, Any],
) -> Iterable[dict[str, str]]:
    text_column = source_config.get("text_column", "text")
    ref_column = source_config.get("ref_column", "ref")
    book_column = source_config.get("book_column", "book")
    chapter_column = source_config.get("chapter_column", "chapter")
    verse_column = source_config.get("verse_column", "verse")
    encoding = source_config.get("encoding", "utf-8")

    with path.open("r", encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle)
        for line_number, row in enumerate(reader, start=2):
            raw_text = row.get(text_column, "")
            if raw_text is None:
                raw_text = ""
            ref = row.get(ref_column) or _compose_ref(
                row.get(book_column, ""),
                row.get(chapter_column, ""),
                row.get(verse_column, ""),
                line_number,
            )
            yield {
                "source": source_name,
                "ref": ref,
                "book": row.get(book_column, ""),
                "chapter": row.get(chapter_column, ""),
                "verse": row.get(verse_column, ""),
                "text": raw_text,
            }


def _read_michigan_claremont(
    path: Path,
    source_name: str,
    source_config: dict[str, Any],
) -> Iterable[dict[str, str]]:
    encoding = source_config.get("encoding", "utf-8")
    book_name = source_config.get("book", source_name)
    book_number = str(source_config.get("book_number", ""))
    for line_number, line in enumerate(_read_text(path, encoding).splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.strip().split(maxsplit=3)
        if len(parts) < 4:
            raise ValueError(f"{path}:{line_number}: expected book chapter verse text")
        raw_book, chapter, verse, text = parts
        chapter = _normalize_ref_number(chapter)
        verse = _normalize_ref_number(verse)
        ref_book = book_name
        if book_number and raw_book != book_number:
            raise ValueError(
                f"{path}:{line_number}: expected book {book_number}, got {raw_book}"
            )
        yield {
            "source": source_name,
            "ref": f"{ref_book} {chapter}:{verse}",
            "book": ref_book,
            "chapter": chapter,
            "verse": verse,
            "text": text,
        }


def _compose_ref(book: str, chapter: str, verse: str, line_number: int) -> str:
    if book and chapter and verse:
        return f"{book} {chapter}:{verse}"
    if book:
        return book
    return f"line {line_number}"


def _read_sblgnt_text_dir(
    path: Path,
    source_name: str,
    source_config: dict[str, Any],
) -> Iterable[dict[str, str]]:
    encoding = source_config.get("encoding", "utf-8")
    files = [file for file in path.glob("*.txt") if file.is_file()]
    for file in sorted(files, key=lambda file: _nt_book_sort_key(file.stem)):
        for line_number, line in enumerate(_read_text(file, encoding).splitlines(), start=1):
            if "\t" not in line:
                continue
            ref, text = line.split("\t", 1)
            ref = ref.strip()
            if not ref:
                continue
            book, chapter, verse = _split_bible_ref(ref)
            yield {
                "source": source_name,
                "ref": ref,
                "book": book,
                "chapter": chapter,
                "verse": verse,
                "text": text.strip(),
            }


def _read_oshb_wlc_dir(
    path: Path,
    source_name: str,
    source_config: dict[str, Any],
) -> Iterable[dict[str, str]]:
    files = [file for file in path.glob("*.xml") if file.is_file()]
    for file in sorted(files, key=lambda file: _ot_book_sort_key(file.stem)):
        tree = ET.parse(file)
        root = tree.getroot()
        for verse in root.iter("{http://www.bibletechnologies.net/2003/OSIS/namespace}verse"):
            osis_id = verse.attrib.get("osisID", "")
            if not osis_id:
                continue
            book, chapter, verse_num = _split_osis_ref(osis_id)
            yield {
                "source": source_name,
                "ref": f"{book} {chapter}:{verse_num}",
                "book": book,
                "chapter": chapter,
                "verse": verse_num,
                "text": " ".join(_osis_direct_word_texts(verse)),
            }


def _osis_direct_word_texts(verse: ET.Element) -> Iterable[str]:
    for child in verse:
        if child.tag == "{http://www.bibletechnologies.net/2003/OSIS/namespace}w":
            text = "".join(child.itertext()).strip()
            if text:
                yield text


def _read_uxlc_dir(
    path: Path,
    source_name: str,
    source_config: dict[str, Any],
) -> Iterable[dict[str, str]]:
    qere_mode = source_config.get("qere_mode", "ketiv")
    if qere_mode not in {"ketiv", "qere", "both"}:
        raise ValueError("uxlc qere_mode must be one of: ketiv, qere, both")
    files = [file for file in path.glob("*.xml") if _is_uxlc_book_file(file)]
    for file in sorted(files, key=lambda file: UXLC_BOOK_ORDER.get(file.stem, 999)):
        tree = ET.parse(file)
        root = tree.getroot()
        names = root.find("./tanach/book/names")
        book = _required_element_text(names, "name", file)
        abbrev = _required_element_text(names, "abbrev", file)
        for chapter in root.findall("./tanach/book/c"):
            chapter_num = chapter.attrib.get("n", "")
            for verse in chapter.findall("./v"):
                verse_num = verse.attrib.get("n", "")
                yield {
                    "source": source_name,
                    "ref": f"{abbrev} {chapter_num}:{verse_num}",
                    "book": book,
                    "chapter": chapter_num,
                    "verse": verse_num,
                    "text": " ".join(_uxlc_word_texts(verse, qere_mode)),
                }


def _is_uxlc_book_file(file: Path) -> bool:
    return (
        file.is_file()
        and file.suffix == ".xml"
        and not file.name.endswith(".DH.xml")
        and file.stem in UXLC_BOOK_ORDER
    )


def _required_element_text(element: ET.Element | None, child: str, file: Path) -> str:
    if element is None:
        raise ValueError(f"{file}: missing names block")
    value = element.findtext(child, default="").strip()
    if not value:
        raise ValueError(f"{file}: missing {child}")
    return value


def _uxlc_word_texts(verse: ET.Element, qere_mode: str) -> Iterable[str]:
    for child in verse:
        text = "".join(child.itertext()).strip()
        if not text:
            continue
        if child.tag == "w":
            yield text
        elif child.tag == "k" and qere_mode in {"ketiv", "both"}:
            yield text
        elif child.tag == "q" and qere_mode in {"qere", "both"}:
            yield text


def _read_mam_html_dir(
    path: Path,
    source_name: str,
    source_config: dict[str, Any],
) -> Iterable[dict[str, str]]:
    encoding = source_config.get("encoding", "utf-8")
    files = [file for file in path.glob("*.html") if file.stem in MAM_BOOK_ORDER]
    for file in sorted(files, key=lambda file: MAM_BOOK_ORDER.get(file.stem, 999)):
        parser = MAMBookParser(file)
        parser.feed(_read_text(file, encoding))
        parser.close()
        for verse in parser.verses:
            yield {
                "source": source_name,
                "ref": f"{parser.book_ref} {verse['chapter']}:{verse['verse']}",
                "book": parser.book_name,
                "chapter": verse["chapter"],
                "verse": verse["verse"],
                "text": verse["text"],
            }


class MAMBookParser(html.parser.HTMLParser):
    def __init__(self, file: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.file = file
        self.book_name = MAM_BOOK_NAMES.get(file.stem, file.stem)
        self.book_ref = MAM_BOOK_REFS.get(file.stem, self.book_name)
        self.verses: list[dict[str, str]] = []
        self.in_title = False
        self.in_tr = False
        self.in_td = False
        self.current_td_attrs: dict[str, str] = {}
        self.current_td_text: list[str] = []
        self.current_row: list[tuple[dict[str, str], str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self.in_title = True
        elif tag == "tr":
            self.in_tr = True
            self.current_row = []
        elif tag == "td" and self.in_tr:
            self.in_td = True
            self.current_td_attrs = {key: value or "" for key, value in attrs}
            self.current_td_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        elif tag == "td" and self.in_td:
            self.current_row.append(
                (self.current_td_attrs, normalize_html_text("".join(self.current_td_text)))
            )
            self.in_td = False
            self.current_td_attrs = {}
            self.current_td_text = []
        elif tag == "tr" and self.in_tr:
            self._finish_row()
            self.in_tr = False
            self.current_row = []

    def handle_data(self, data: str) -> None:
        if self.in_title:
            prefix = "MAM with doc: "
            title = data.strip()
            if title.startswith(prefix):
                title_book = title.removeprefix(prefix)
                self.book_ref = MAM_TITLE_REFS.get(title_book, self.book_ref)
        if self.in_td:
            self.current_td_text.append(data)

    def _finish_row(self) -> None:
        if len(self.current_row) < 2:
            return
        attrs, _label = self.current_row[0]
        verse_id = attrs.get("id", "")
        if not verse_id.startswith("c") or "v" not in verse_id:
            return
        chapter, verse = split_mam_verse_id(verse_id)
        if not chapter or not verse:
            return
        self.verses.append(
            {
                "chapter": chapter,
                "verse": verse,
                "text": self.current_row[1][1],
            }
        )


def split_mam_verse_id(value: str) -> tuple[str, str]:
    chapter, verse = value.removeprefix("c").split("v", 1)
    return chapter, verse


def normalize_html_text(value: str) -> str:
    return " ".join(value.replace("\xa0", " ").split())


UXLC_BOOK_ORDER = {
    "Genesis": 1,
    "Exodus": 2,
    "Leviticus": 3,
    "Numbers": 4,
    "Deuteronomy": 5,
    "Joshua": 6,
    "Judges": 7,
    "Samuel_1": 8,
    "Samuel_2": 9,
    "Kings_1": 10,
    "Kings_2": 11,
    "Isaiah": 12,
    "Jeremiah": 13,
    "Ezekiel": 14,
    "Hosea": 15,
    "Joel": 16,
    "Amos": 17,
    "Obadiah": 18,
    "Jonah": 19,
    "Micah": 20,
    "Nahum": 21,
    "Habakkuk": 22,
    "Zephaniah": 23,
    "Haggai": 24,
    "Zechariah": 25,
    "Malachi": 26,
    "Psalms": 27,
    "Proverbs": 28,
    "Job": 29,
    "Song_of_Songs": 30,
    "Ruth": 31,
    "Lamentations": 32,
    "Ecclesiastes": 33,
    "Esther": 34,
    "Daniel": 35,
    "Ezra": 36,
    "Nehemiah": 37,
    "Chronicles_1": 38,
    "Chronicles_2": 39,
}

MAM_BOOK_ORDER = {
    "A1-Genesis": 1,
    "A2-Exodus": 2,
    "A3-Levit": 3,
    "A4-Numbers": 4,
    "A5-Deuter": 5,
    "B1-Joshua": 6,
    "B2-Judges": 7,
    "BA-1Samuel": 8,
    "BB-2Samuel": 9,
    "BC-1Kings": 10,
    "BD-2Kings": 11,
    "C1-Isaiah": 12,
    "C2-Jeremiah": 13,
    "C3-Ezekiel": 14,
    "CA-Hosea": 15,
    "CB-Joel": 16,
    "CC-Amos": 17,
    "CD-Obadiah": 18,
    "CE-Jonah": 19,
    "CF-Micah": 20,
    "CG-Nahum": 21,
    "CH-Habakkuk": 22,
    "CI-Tsefaniah": 23,
    "CJ-Haggai": 24,
    "CK-Zechariah": 25,
    "CL-Malachi": 26,
    "D1-Psalms": 27,
    "D2-Proverbs": 28,
    "D3-Job": 29,
    "E1-Song of Songs": 30,
    "E2-Ruth": 31,
    "E3-Lamentations": 32,
    "E4-Ecclesiastes": 33,
    "E5-Esther": 34,
    "F1-Daniel": 35,
    "FA-Ezra": 36,
    "FB-Nehemiah": 37,
    "FC-1Chronicles": 38,
    "FD-2Chronicles": 39,
}

MAM_BOOK_NAMES = {
    "A1-Genesis": "Genesis",
    "A2-Exodus": "Exodus",
    "A3-Levit": "Leviticus",
    "A4-Numbers": "Numbers",
    "A5-Deuter": "Deuteronomy",
    "B1-Joshua": "Joshua",
    "B2-Judges": "Judges",
    "BA-1Samuel": "1Samuel",
    "BB-2Samuel": "2Samuel",
    "BC-1Kings": "1Kings",
    "BD-2Kings": "2Kings",
    "C1-Isaiah": "Isaiah",
    "C2-Jeremiah": "Jeremiah",
    "C3-Ezekiel": "Ezekiel",
    "CA-Hosea": "Hosea",
    "CB-Joel": "Joel",
    "CC-Amos": "Amos",
    "CD-Obadiah": "Obadiah",
    "CE-Jonah": "Jonah",
    "CF-Micah": "Micah",
    "CG-Nahum": "Nahum",
    "CH-Habakkuk": "Habakkuk",
    "CI-Tsefaniah": "Zephaniah",
    "CJ-Haggai": "Haggai",
    "CK-Zechariah": "Zechariah",
    "CL-Malachi": "Malachi",
    "D1-Psalms": "Psalms",
    "D2-Proverbs": "Proverbs",
    "D3-Job": "Job",
    "E1-Song of Songs": "Song of Songs",
    "E2-Ruth": "Ruth",
    "E3-Lamentations": "Lamentations",
    "E4-Ecclesiastes": "Ecclesiastes",
    "E5-Esther": "Esther",
    "F1-Daniel": "Daniel",
    "FA-Ezra": "Ezra",
    "FB-Nehemiah": "Nehemiah",
    "FC-1Chronicles": "1Chronicles",
    "FD-2Chronicles": "2Chronicles",
}

MAM_BOOK_REFS = {
    "A1-Genesis": "Gen",
    "A2-Exodus": "Ex",
    "A3-Levit": "Lev",
    "A4-Numbers": "Num",
    "A5-Deuter": "Deut",
    "B1-Joshua": "Josh",
    "B2-Judges": "Judg",
    "BA-1Samuel": "1 Sam",
    "BB-2Samuel": "2 Sam",
    "BC-1Kings": "1 Kgs",
    "BD-2Kings": "2 Kgs",
    "C1-Isaiah": "Isa",
    "C2-Jeremiah": "Jer",
    "C3-Ezekiel": "Ezek",
    "CA-Hosea": "Hos",
    "CB-Joel": "Joel",
    "CC-Amos": "Amos",
    "CD-Obadiah": "Obad",
    "CE-Jonah": "Jonah",
    "CF-Micah": "Mic",
    "CG-Nahum": "Nah",
    "CH-Habakkuk": "Hab",
    "CI-Tsefaniah": "Zeph",
    "CJ-Haggai": "Hag",
    "CK-Zechariah": "Zech",
    "CL-Malachi": "Mal",
    "D1-Psalms": "Ps",
    "D2-Proverbs": "Prov",
    "D3-Job": "Job",
    "E1-Song of Songs": "Song",
    "E2-Ruth": "Ruth",
    "E3-Lamentations": "Lam",
    "E4-Ecclesiastes": "Eccl",
    "E5-Esther": "Esth",
    "F1-Daniel": "Dan",
    "FA-Ezra": "Ezra",
    "FB-Nehemiah": "Neh",
    "FC-1Chronicles": "1 Chr",
    "FD-2Chronicles": "2 Chr",
}

MAM_TITLE_REFS = {
    name: MAM_BOOK_REFS[key]
    for key, name in MAM_BOOK_NAMES.items()
    if key in MAM_BOOK_REFS
}


def _nt_book_sort_key(book: str) -> tuple[int, str]:
    return (NT_BOOK_ORDER.get(book, 999), book)


def _ot_book_sort_key(book: str) -> tuple[int, str]:
    return (OT_BOOK_ORDER.get(book, 999), book)


def _split_bible_ref(ref: str) -> tuple[str, str, str]:
    book_and_rest = ref.rsplit(" ", 1)
    if len(book_and_rest) != 2 or ":" not in book_and_rest[1]:
        return ref, "", ""
    book, rest = book_and_rest
    chapter, verse = rest.split(":", 1)
    return book, chapter, verse


def _split_osis_ref(ref: str) -> tuple[str, str, str]:
    parts = ref.split(".")
    if len(parts) != 3:
        return ref, "", ""
    return parts[0], parts[1], parts[2]


def _resolve_path(base_dir: Path, configured_path: str) -> Path:
    path = Path(configured_path).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()


def _read_text(path: Path, encoding: str) -> str:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding=encoding) as handle:
            return handle.read()
    return path.read_text(encoding=encoding)


def _normalize_ref_number(value: str) -> str:
    # Michigan-Claremont stores chapter/verse digits right-to-left.
    if value.isdigit() and len(value) > 1:
        return value[::-1].lstrip("0") or "0"
    return value
