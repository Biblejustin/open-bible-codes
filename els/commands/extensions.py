"""`extensions` subcommand: grow ELS hits into surrounding-letter matches."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import load_corpus
from els.extensions import build_extension_lexicon, extensions_for_hit
from els.io import open_dict_reader, open_dict_writer, write_run_manifest
from els.rows import EXTENSION_FIELDNAMES, extension_row, hit_from_row, hit_with_corpus_center


def cmd_extensions(args: argparse.Namespace) -> int:
    corpus = load_corpus(args.config)
    lexicon = build_extension_lexicon(corpus, max_phrase_words=args.phrase_words)
    corpus_label = args.corpus_label or corpus.name
    input_hit_count = 0
    hit_count = 0
    skipped_hit_count = 0
    extension_count = 0

    with open_dict_reader(args.hits) as rows, open_dict_writer(
        args.out,
        EXTENSION_FIELDNAMES,
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
            hit = hit_from_row(row)
            hit = hit_with_corpus_center(corpus, hit)
            hit_count += 1
            for extension in extensions_for_hit(
                corpus,
                hit,
                lexicon,
                max_before=args.max_before,
                max_after=args.max_after,
                include_both_sided=args.include_both_sided,
                max_extensions=args.max_extensions_per_hit,
            ):
                writer.writerow(extension_row(corpus_label, hit, extension))
                extension_count += 1

    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "created_utc": datetime.now(UTC).isoformat(),
                "config": str(Path(args.config).expanduser().resolve()),
                "hits": str(Path(args.hits).expanduser().resolve()),
                "corpus": corpus.summary(),
                "max_before": args.max_before,
                "max_after": args.max_after,
                "phrase_words": args.phrase_words,
                "include_both_sided": args.include_both_sided,
                "max_extensions_per_hit": args.max_extensions_per_hit,
                "lexicon_entries": len(lexicon.entries),
                "input_hit_count": input_hit_count,
                "skipped_hit_count": skipped_hit_count,
                "hit_count": hit_count,
                "extension_count": extension_count,
            },
            args.manifest_out,
        )
    return 0
