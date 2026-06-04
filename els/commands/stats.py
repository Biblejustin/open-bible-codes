"""`stats` subcommand: print corpus summary JSON."""

from __future__ import annotations

import argparse

from els.corpus import load_corpus


def cmd_stats(args: argparse.Namespace) -> int:
    corpus = load_corpus(args.config)
    print(corpus.summary_json())
    return 0
