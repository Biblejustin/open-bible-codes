"""`skip-plan` subcommand: pick a max-skip cap per term from corpus letter frequencies."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import load_corpus
from els.io import write_dict_rows, write_run_manifest
from els.rows import SKIP_PLAN_FIELDNAMES, skip_plan_row
from els.search import normalize_for_corpus
from els.skip_plan import plan_skip_cap
from els.term_io import collect_terms


def cmd_skip_plan(args: argparse.Namespace) -> int:
    terms = collect_terms(args.term, args.terms_file)
    if not terms:
        raise SystemExit("provide --term or --terms-file")

    corpus = load_corpus(args.config)
    rows: list[dict[str, object]] = []
    for term in terms:
        normalized = normalize_for_corpus(corpus, term)
        plan = plan_skip_cap(
            corpus.text,
            term,
            normalized,
            min_skip=args.min_skip,
            max_skip_limit=args.max_skip_limit,
            direction=args.direction,
            target_expected_hits=args.target_expected_hits,
        )
        rows.append(skip_plan_row(plan))

    write_dict_rows(rows, args.out, SKIP_PLAN_FIELDNAMES)
    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "mode": "skip-plan",
                "created_utc": datetime.now(UTC).isoformat(),
                "config": str(Path(args.config).expanduser().resolve()),
                "corpus": corpus.summary(),
                "terms": terms,
                "min_skip": args.min_skip,
                "max_skip_limit": args.max_skip_limit,
                "direction": args.direction,
                "target_expected_hits": args.target_expected_hits,
                "rows": len(rows),
                "model": "independent letters from corpus frequency",
            },
            args.manifest_out,
        )
    return 0
