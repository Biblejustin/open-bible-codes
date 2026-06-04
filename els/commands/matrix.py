"""`matrix` subcommand: lay ELS hits onto skip-width letter grids."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import load_corpus
from els.io import open_dict_reader, open_dict_writer, write_dict_rows, write_run_manifest
from els.matrix import matrix_letters, matrix_summary
from els.rows import (
    MATRIX_LETTER_FIELDNAMES,
    MATRIX_SUMMARY_FIELDNAMES,
    hit_from_row,
    hit_with_corpus_center,
    matrix_letter_row,
    matrix_summary_row,
)


def cmd_matrix(args: argparse.Namespace) -> int:
    corpus = load_corpus(args.config)
    corpus_label = args.corpus_label or corpus.name
    input_hit_count = 0
    skipped_hit_count = 0
    hit_count = 0
    letter_count = 0
    summary_rows: list[dict[str, object]] = []

    with open_dict_reader(args.hits) as rows, open_dict_writer(
        args.out,
        MATRIX_LETTER_FIELDNAMES,
    ) as writer:
        for row in rows:
            input_hit_count += 1
            row_corpus = row.get("corpus", "")
            if row_corpus:
                if not args.corpus_label:
                    raise SystemExit(
                        "hits file has corpus labels; pass --corpus-label to select one"
                    )
                if row_corpus != args.corpus_label:
                    skipped_hit_count += 1
                    continue
            hit = hit_with_corpus_center(corpus, hit_from_row(row))
            hit_count += 1
            hit_index = hit_count
            letters = matrix_letters(
                corpus,
                hit,
                hit_index=hit_index,
                row_width=args.row_width,
            )
            width = args.row_width or abs(hit.skip)
            for letter in letters:
                writer.writerow(matrix_letter_row(corpus_label, hit, letter, width))
            letter_count += len(letters)
            summary_rows.append(
                matrix_summary_row(
                    corpus_label,
                    hit,
                    matrix_summary(hit, letters, row_width=args.row_width),
                )
            )

    if args.summary_out:
        write_dict_rows(summary_rows, args.summary_out, MATRIX_SUMMARY_FIELDNAMES)
    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "created_utc": datetime.now(UTC).isoformat(),
                "config": str(Path(args.config).expanduser().resolve()),
                "hits": str(Path(args.hits).expanduser().resolve()),
                "corpus": corpus.summary(),
                "corpus_label": corpus_label,
                "row_width": args.row_width,
                "input_hit_count": input_hit_count,
                "skipped_hit_count": skipped_hit_count,
                "hit_count": hit_count,
                "letter_count": letter_count,
            },
            args.manifest_out,
        )
    return 0
