#!/usr/bin/env python3
"""Run a fixed protocol TOML file."""

from __future__ import annotations

import argparse

from els.protocol_runner import run_protocol


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("protocol")
    parser.add_argument("--only", action="append", help="run one step id; repeatable")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--manifest-out")
    args = parser.parse_args()
    return run_protocol(
        args.protocol,
        only=set(args.only or []),
        dry_run=args.dry_run,
        manifest_out=args.manifest_out,
        resume=args.resume,
    )


if __name__ == "__main__":
    raise SystemExit(main())
