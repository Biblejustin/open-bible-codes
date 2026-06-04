"""`search` subcommand: write ELS hits for terms, with optional shuffle controls."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import load_corpus
from els.io import write_control_stats, write_run_manifest
from els.maxskip import effective_max_skip_for_query
from els.rows import open_hits_writer
from els.search import find_els, normalize_for_corpus
from els.stats import shuffled_letter_controls
from els.term_io import collect_terms


def cmd_search(args: argparse.Namespace) -> int:
    terms = collect_terms(args.term, args.terms_file)
    if not terms:
        raise SystemExit("provide --term or --terms-file")

    corpus = load_corpus(args.config)
    hit_count = 0
    control_rows: list[dict[str, object]] = []
    effective_max_skips: dict[str, int | str] = {}
    if args.shuffles and args.max_skip_mode != "fixed":
        raise SystemExit("--shuffles currently requires --max-skip-mode fixed")

    with open_hits_writer(args.out) as writer:
        for term in terms:
            normalized = normalize_for_corpus(corpus, term)
            effective_max_skip = effective_max_skip_for_query(corpus, normalized, args)
            effective_max_skips[term] = effective_max_skip or ""
            if effective_max_skip is None:
                continue
            for hit in find_els(
                corpus,
                term,
                min_skip=args.min_skip,
                max_skip=effective_max_skip,
                direction=args.direction,
                max_hits=args.max_hits,
            ):
                writer.writerow(hit.as_row())
                hit_count += 1

    if args.shuffles:
        controls = shuffled_letter_controls(
            corpus,
            terms,
            min_skip=args.min_skip,
            max_skip=args.max_skip,
            direction=args.direction,
            shuffles=args.shuffles,
            seed=args.seed,
        )
        for term, control in controls:
            control_rows.append(
                {
                    "term": term,
                    "observed": control.observed,
                    "shuffled_counts": list(control.shuffled_counts),
                    "p_greater_equal": control.p_greater_equal,
                }
            )

    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "created_utc": datetime.now(UTC).isoformat(),
                "config": str(Path(args.config).expanduser().resolve()),
                "corpus": corpus.summary(),
                "terms": terms,
                "min_skip": args.min_skip,
                "max_skip": args.max_skip,
                "max_skip_mode": args.max_skip_mode,
                "max_skip_limit": args.max_skip_limit,
                "effective_max_skips": effective_max_skips,
                "direction": args.direction,
                "max_hits": args.max_hits,
                "hit_count": hit_count,
                "shuffles": args.shuffles,
                "seed": args.seed,
            },
            args.manifest_out,
        )
    if args.shuffles:
        write_control_stats(control_rows, args.stats_out)
    return 0
