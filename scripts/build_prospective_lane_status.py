#!/usr/bin/env python3
"""Build a Markdown status table for prospective study lanes."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from scripts import scaffold_prospective_study as scaffold


DEFAULT_PROFILES = Path("configs/prospective_study_lanes.json")
DEFAULT_OUT = Path("docs/PROSPECTIVE_LANE_STATUS.md")

STATUS_READS = {
    "blocked_until_new_term_source": "blocked; needs new external term source",
    "needs_predeclared_term_list": "blocked; needs predeclared term list",
    "completed_negative_controlled_result": "completed negative controlled result",
    "completed_negative_weak_controlled_result": "completed weak or negative controlled result",
    "completed_negative_curiosity_appendix": "completed negative curiosity appendix",
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    profiles = scaffold.load_profiles(args.profiles)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_markdown(profiles, args.profiles), encoding="utf-8")
    print(args.out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser


def render_markdown(profiles: list[dict[str, Any]], profile_path: Path) -> str:
    lines = [
        "# Prospective Lane Status",
        "",
        "Status: planning index, not a result report.",
        "",
        "This page is generated from `configs/prospective_study_lanes.json`.",
        "It lists which lanes are completed, blocked, or waiting on a new lock.",
        "",
        "## Lanes",
        "",
        "| Lane | Status | Read | Term file | Protocol | Report |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for profile in profiles:
        status = str(profile["status"])
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{profile['id']}`",
                    f"`{status}`",
                    STATUS_READS.get(status, status.replace("_", " ")),
                    f"`{profile['term_file']}`",
                    f"`{profile['protocol']}`",
                    f"`{profile['report_doc']}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Blocked Lanes",
            "",
            "| Lane | Needed input | Boundary |",
            "| --- | --- | --- |",
        ]
    )
    for profile in blocked_profiles(profiles):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{profile['id']}`",
                    str(profile["source_term_files"]),
                    str(profile["excluded_prior"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Safe Commands",
            "",
            "```bash",
            "python3 -m scripts.check_prospective_study_lanes",
            "python3 -m scripts.scaffold_prospective_study --list-profiles",
            "python3 -m scripts.build_prospective_lane_status",
            "```",
            "",
            "## Interpretation Rules",
            "",
            "- A lane marked blocked must not produce result-bearing outputs yet.",
            "- Completed negative lanes can be rerun for reproducibility, not promoted.",
            "- Post-discovery lanes stay review-only unless a fresh prospective lock is created first.",
            "- This document summarizes planning state from "
            f"`{profile_path.as_posix()}`; it does not change study status.",
            "",
        ]
    )
    return "\n".join(lines)


def blocked_profiles(profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        profile
        for profile in profiles
        if str(profile.get("status", "")).startswith("blocked")
        or str(profile.get("status", "")).startswith("needs_")
    ]


if __name__ == "__main__":
    raise SystemExit(main())
