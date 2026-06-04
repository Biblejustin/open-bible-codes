"""Subcommand implementations for the Open Bible Codes CLI.

Each module exposes one cmd_<name>(args) -> int entry point wired into the
parser by els.cli.build_parser. Command modules import only from els leaf
modules (never from els.cli) to keep the dependency graph one-directional.
"""
