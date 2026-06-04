"""Effective max-skip resolution.

Shared by the search, batch, pairs, and surface paths: from corpus and term
lengths plus the user's skip arguments, decide the max skip to search (or None
to skip the term). Pure logic over els.skip_plan.max_skip_for_mode.
"""

from __future__ import annotations

import argparse

from els.skip_plan import max_skip_for_mode


def effective_max_skip_for_query(corpus, normalized: str, args: argparse.Namespace) -> int | None:
    return effective_max_skip_for_normalized(
        len(corpus.text),
        len(normalized),
        args.min_skip,
        args.max_skip,
        args.max_skip_mode,
        args.max_skip_limit,
    )


def effective_max_skip_for_normalized(
    text_length: int,
    normalized_length: int,
    min_skip: int,
    fixed_max_skip: int,
    mode: str,
    max_skip_limit,
) -> int | None:
    if min_skip < 1:
        raise SystemExit("--min-skip must be >= 1")
    if max_skip_limit is not None and int(max_skip_limit) < min_skip:
        raise SystemExit("--max-skip-limit must be >= --min-skip")
    if normalized_length <= 0:
        return None
    if mode == "fixed":
        if fixed_max_skip < min_skip:
            raise SystemExit("--max-skip must be >= --min-skip")
        return fixed_max_skip
    dynamic_max_skip = max_skip_for_mode(text_length, normalized_length, mode)
    if max_skip_limit is not None:
        dynamic_max_skip = min(dynamic_max_skip, int(max_skip_limit))
    if dynamic_max_skip < min_skip:
        return None
    return dynamic_max_skip
