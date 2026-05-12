#!/usr/bin/env python3
"""Check that expanded-strata operator docs reference live tools."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


DEFAULT_DOC = Path("docs/EXPANDED_STRATA_TOOLING.md")
DEFAULT_MAKEFILE = Path("Makefile")
DEFAULT_REPORT = Path("reports/expanded_strata_tooling_check.json")


@dataclass(frozen=True)
class ToolingEntry:
    name: str
    path: Path
    make_target: str


ENTRIES = (
    ToolingEntry("match strata index", Path("protocols/match_strata_index.toml"), "match-strata-index"),
    ToolingEntry("boundary alignment", Path("protocols/boundary_alignment.toml"), "boundary-alignment"),
    ToolingEntry("chapter position bias", Path("protocols/chapter_position_bias.toml"), "chapter-position-bias"),
    ToolingEntry("direction asymmetry", Path("protocols/direction_asymmetry.toml"), "direction-asymmetry"),
    ToolingEntry("canonical first summary", Path("protocols/canonical_first_summary.toml"), "canonical-first-summary"),
    ToolingEntry("cross-skip summary", Path("protocols/cross_skip_summary.toml"), "cross-skip-summary"),
    ToolingEntry("review flag summary", Path("protocols/review_flag_summary.toml"), "review-flag-summary"),
    ToolingEntry("thematic chapter absence", Path("protocols/thematic_chapter_absence.toml"), "thematic-chapter-absence"),
    ToolingEntry("Hebrew Atbash audit", Path("protocols/hebrew_atbash_audit.toml"), "hebrew-atbash-audit"),
    ToolingEntry("Hebrew ALBAM audit", Path("protocols/hebrew_albam_audit.toml"), "hebrew-albam-audit"),
    ToolingEntry("word-edge pattern audit", Path("protocols/word_edge_pattern_audit.toml"), "word-edge-pattern-audit"),
    ToolingEntry("word-skip term audit", Path("protocols/word_skip_term_audit.toml"), "word-skip-term-audit"),
    ToolingEntry("matrix cluster candidates", Path("scripts/build_matrix_cluster_candidates.py"), "matrix-cluster-candidates"),
    ToolingEntry("cipher layered pairs", Path("scripts/build_cipher_layered_pairs.py"), "cipher-layered-pairs"),
    ToolingEntry("cohort cluster density", Path("scripts/build_cohort_cluster_density.py"), "cohort-cluster-density"),
)

REQUIRED_SNIPPETS = (
    ("matrix doc row width flag", "doc", "--row-width 50"),
    ("matrix Makefile row width flag", "makefile", "--row-width \"$(MATRIX_CLUSTER_WIDTH)\""),
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = check_tooling(args.doc, args.makefile)
    write_report(args.report, result)
    print(args.report)
    return 0 if result["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--makefile", type=Path, default=DEFAULT_MAKEFILE)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser


def check_tooling(doc: Path, makefile: Path) -> dict[str, object]:
    missing: list[str] = []
    doc_text = read_text_if_exists(doc)
    make_text = read_text_if_exists(makefile)
    if not doc.exists():
        missing.append(str(doc))
    if not makefile.exists():
        missing.append(str(makefile))

    checked = []
    for entry in ENTRIES:
        path_text = str(entry.path)
        target_text = f"make {entry.make_target}"
        target_def = f"{entry.make_target}:"
        path_exists = entry.path.exists()
        doc_mentions_path = path_text in doc_text
        doc_mentions_target = target_text in doc_text
        make_mentions_target = target_def in make_text
        checked.append(
            {
                "name": entry.name,
                "path": path_text,
                "make_target": entry.make_target,
                "path_exists": path_exists,
                "doc_mentions_path": doc_mentions_path,
                "doc_mentions_target": doc_mentions_target,
                "make_mentions_target": make_mentions_target,
            }
        )
        if not path_exists:
            missing.append(path_text)
        if not doc_mentions_path:
            missing.append(f"{doc}:{path_text}")
        if not doc_mentions_target:
            missing.append(f"{doc}:{target_text}")
        if not make_mentions_target:
            missing.append(f"{makefile}:{target_def}")

    for name, source, snippet in REQUIRED_SNIPPETS:
        path = doc if source == "doc" else makefile
        haystack = doc_text if source == "doc" else make_text
        checked.append({"name": name, "path": str(path), "required_snippet": snippet, "snippet_present": snippet in haystack})
        if snippet not in haystack:
            missing.append(f"{path}:{snippet}")

    return {"ok": not missing, "missing": missing, "checked": checked}


def read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def write_report(path: Path, result: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
