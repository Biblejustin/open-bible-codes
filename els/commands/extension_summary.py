"""`extension-summary` subcommand: aggregate extension rows and rank strong ones."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from heapq import nlargest
from pathlib import Path

from els import __version__
from els.io import open_dict_reader, write_dict_rows, write_run_manifest
from els.rows import (
    EXTENSION_SUMMARY_FIELDNAMES,
    EXTENSION_TOP_FIELDNAMES,
    add_extension_summary_group,
    extension_rank_key,
    extension_score,
    extension_summary_rows,
)


STRONG_EXTENSION_TYPES = {
    "before_plus_term",
    "term_plus_after",
    "before_plus_term_plus_after",
}


def cmd_extension_summary(args: argparse.Namespace) -> int:
    input_rows = 0
    kept_rows = 0
    filtered_short_rows = 0
    filtered_term_length_rows = 0
    filtered_match_kind_rows = 0
    filtered_excluded_term_rows = 0
    excluded_terms = set(args.exclude_term)
    groups: dict[tuple[str, ...], dict[str, object]] = {}
    top_candidates: list[dict[str, object]] = []

    with open_dict_reader(args.extensions) as rows:
        for row in rows:
            input_rows += 1
            extension_length = int(row["extension_length"])
            if extension_length < args.min_extension_length:
                filtered_short_rows += 1
                continue
            if len(row.get("normalized_term", "")) < args.min_term_length:
                filtered_term_length_rows += 1
                continue
            if args.match_kind_prefix and not row.get("match_kind", "").startswith(
                args.match_kind_prefix
            ):
                filtered_match_kind_rows += 1
                continue
            if (
                row.get("term", "") in excluded_terms
                or row.get("normalized_term", "") in excluded_terms
            ):
                filtered_excluded_term_rows += 1
                continue
            kept_rows += 1
            add_extension_summary_group(groups, row, extension_length)
            if row.get("extension_type") in STRONG_EXTENSION_TYPES:
                ranked_row = dict(row)
                ranked_row["extension_score"] = extension_score(row, extension_length)
                top_candidates.append(ranked_row)

    summary_rows = extension_summary_rows(groups)
    write_dict_rows(summary_rows, args.out, fieldnames=EXTENSION_SUMMARY_FIELDNAMES)

    top_rows = nlargest(
        args.top,
        top_candidates,
        key=extension_rank_key,
    )
    if args.top_out:
        write_dict_rows(top_rows, args.top_out, fieldnames=EXTENSION_TOP_FIELDNAMES)

    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "created_utc": datetime.now(UTC).isoformat(),
                "extensions": str(Path(args.extensions).expanduser().resolve()),
                "min_extension_length": args.min_extension_length,
                "min_term_length": args.min_term_length,
                "match_kind_prefix": args.match_kind_prefix,
                "exclude_terms": sorted(excluded_terms),
                "top": args.top,
                "input_rows": input_rows,
                "kept_rows": kept_rows,
                "filtered_short_rows": filtered_short_rows,
                "filtered_term_length_rows": filtered_term_length_rows,
                "filtered_match_kind_rows": filtered_match_kind_rows,
                "filtered_excluded_term_rows": filtered_excluded_term_rows,
                "summary_rows": len(summary_rows),
                "top_rows": len(top_rows),
            },
            args.manifest_out,
        )
    return 0
