"""Matrix/table coordinates for ELS hits."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .corpus import Corpus
from .search import ELSHit


@dataclass(frozen=True)
class MatrixLetter:
    hit_index: int
    letter_index: int
    letter: str
    offset: int
    row: int
    col: int
    ref: str
    word_index: int | str
    word: str
    normalized_word: str


@dataclass(frozen=True)
class MatrixSummary:
    hit_index: int
    row_width: int
    min_row: int
    max_row: int
    min_col: int
    max_col: int
    rows_spanned: int
    cols_spanned: int
    letter_count: int
    first_offset: int
    last_offset: int


def hit_offsets(hit: ELSHit) -> tuple[int, ...]:
    """Return letter offsets in ELS reading order."""

    return tuple(
        hit.start_offset + index * hit.skip
        for index in range(len(hit.sequence))
    )


def default_row_width(hit: ELSHit) -> int:
    return abs(hit.skip)


def validate_row_width(row_width: int) -> int:
    if row_width <= 0:
        raise ValueError("row width must be > 0")
    return row_width


def matrix_letters(
    corpus: Corpus,
    hit: ELSHit,
    *,
    hit_index: int,
    row_width: int | None = None,
) -> tuple[MatrixLetter, ...]:
    width = validate_row_width(row_width or default_row_width(hit))
    offsets = hit_offsets(hit)
    letters: list[MatrixLetter] = []
    for letter_index, offset in enumerate(offsets):
        verse = corpus.verses[corpus.position_to_verse[offset]]
        word = corpus.word_at(offset)
        letters.append(
            MatrixLetter(
                hit_index=hit_index,
                letter_index=letter_index,
                letter=hit.sequence[letter_index],
                offset=offset,
                row=offset // width,
                col=offset % width,
                ref=verse.ref,
                word_index=word.word_index if word is not None else "",
                word=word.raw_word if word is not None else "",
                normalized_word=word.normalized_word if word is not None else "",
            )
        )
    return tuple(letters)


def matrix_summary(
    hit: ELSHit,
    letters: Iterable[MatrixLetter],
    *,
    row_width: int | None = None,
) -> MatrixSummary:
    letter_rows = tuple(letters)
    if not letter_rows:
        raise ValueError("matrix summary requires at least one letter")
    width = validate_row_width(row_width or default_row_width(hit))
    rows = [letter.row for letter in letter_rows]
    cols = [letter.col for letter in letter_rows]
    offsets = [letter.offset for letter in letter_rows]
    return MatrixSummary(
        hit_index=letter_rows[0].hit_index,
        row_width=width,
        min_row=min(rows),
        max_row=max(rows),
        min_col=min(cols),
        max_col=max(cols),
        rows_spanned=max(rows) - min(rows) + 1,
        cols_spanned=max(cols) - min(cols) + 1,
        letter_count=len(letter_rows),
        first_offset=offsets[0],
        last_offset=offsets[-1],
    )
