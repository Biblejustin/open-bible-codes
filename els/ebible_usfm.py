"""Small USFM reader for eBible source packages."""

from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class UsfmVerse:
    book: str
    chapter: str
    verse: str
    text: str

    @property
    def ref(self) -> str:
        return f"{self.book} {self.chapter}:{self.verse}"


CHAPTER_RE = re.compile(r"^\\c\s+(\S+)")
ID_RE = re.compile(r"^\\id\s+(\S+)")
VERSE_RE = re.compile(r"(?:^|\s)\\v\s+(\S+)\s*(.*)$")
NOTE_RE = re.compile(r"\\[fx]\b.*?\\[fx]\*", re.DOTALL)
WORD_MARKER_RE = re.compile(r"\\w\s+(.+?)\\w\*", re.DOTALL)
WORD_ATTR_RE = re.compile(r"\|[A-Za-z0-9_:-]+=\"[^\"]*\"")
END_MARKER_RE = re.compile(r"\\\+?[A-Za-z][A-Za-z0-9-]*\*")
MARKER_RE = re.compile(r"\\\+?[A-Za-z][A-Za-z0-9-]*\s*")
HEBREW_PARAGRAPH_MARKER_RE = re.compile(r"(^|[\s׃])[פס](?=\s|$)")


def parse_usfm_zip(path: str | Path) -> list[UsfmVerse]:
    """Read all USFM files from a zip archive in archive order."""

    archive_path = Path(path)
    verses: list[UsfmVerse] = []
    with zipfile.ZipFile(archive_path) as archive:
        names = [
            name
            for name in archive.namelist()
            if name.lower().endswith((".usfm", ".sfm"))
        ]
        for name in sorted(names, key=_archive_sort_key):
            raw = archive.read(name).decode("utf-8-sig")
            verses.extend(parse_usfm(raw, default_book=_book_from_filename(name)))
    return verses


def parse_usfm(text: str, *, default_book: str = "") -> list[UsfmVerse]:
    """Parse verse-level text from simple USFM."""

    book = default_book
    chapter = ""
    current_verse = ""
    current_parts: list[str] = []
    verses: list[UsfmVerse] = []

    def flush_current() -> None:
        nonlocal current_parts, current_verse
        if not current_verse:
            return
        verse_text = _clean_usfm_text(" ".join(current_parts))
        if verse_text:
            verses.append(
                UsfmVerse(
                    book=book,
                    chapter=chapter,
                    verse=current_verse,
                    text=verse_text,
                )
            )
        current_verse = ""
        current_parts = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        id_match = ID_RE.match(line)
        if id_match:
            book = id_match.group(1)
            continue

        chapter_match = CHAPTER_RE.match(line)
        if chapter_match:
            flush_current()
            chapter = chapter_match.group(1)
            continue

        verse_match = VERSE_RE.search(line)
        if verse_match:
            flush_current()
            current_verse = verse_match.group(1)
            current_parts = [verse_match.group(2)]
            continue

        if current_verse:
            continuation = _clean_usfm_text(line)
            if continuation:
                current_parts.append(continuation)

    flush_current()
    return verses


def _clean_usfm_text(text: str) -> str:
    text = NOTE_RE.sub(" ", text)
    text = WORD_MARKER_RE.sub(_clean_word_marker, text)
    text = WORD_ATTR_RE.sub("", text)
    text = END_MARKER_RE.sub(" ", text)
    text = MARKER_RE.sub(" ", text)
    text = HEBREW_PARAGRAPH_MARKER_RE.sub(_strip_hebrew_paragraph_marker, text)
    text = text.replace("\\", " ")
    return " ".join(text.split())


def _clean_word_marker(match: re.Match[str]) -> str:
    payload = match.group(1)
    return payload.split("|", 1)[0].strip()


def _strip_hebrew_paragraph_marker(match: re.Match[str]) -> str:
    return match.group(1)


def _archive_sort_key(name: str) -> tuple[int, str]:
    match = re.match(r"^(\d+)-", Path(name).name)
    if match:
        return (int(match.group(1)), name)
    return (999, name)


def _book_from_filename(name: str) -> str:
    stem = Path(name).stem
    match = re.match(r"^\d+-([1-3]?[A-Z]+)", stem)
    if match:
        return match.group(1)
    return stem
