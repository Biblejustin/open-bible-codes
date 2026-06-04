"""`gematria-year` subcommand: print Hebrew-year encodings of a year."""

from __future__ import annotations

import argparse
import json

from els.gematria import hebrew_year_additive, hebrew_year_compact, hebrew_year_remainder


def cmd_gematria_year(args: argparse.Namespace) -> int:
    print(
        json.dumps(
            {
                "year": args.year,
                "compact_thousands": hebrew_year_compact(args.year),
                "additive_full_value": hebrew_year_additive(args.year),
                "year_remainder": hebrew_year_remainder(args.year),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0
