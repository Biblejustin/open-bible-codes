#!/usr/bin/env python3
"""Create a study-specific preregistration draft from the project template."""

from __future__ import annotations

import argparse
import re
import shlex
from pathlib import Path
from typing import Any

from scripts.json_utils import read_json_object


TEMPLATE = Path("docs/PROSPECTIVE_STUDY_PREREGISTRATION_TEMPLATE.md")
PROFILES = Path("configs/prospective_study_lanes.json")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.list_profiles:
        print(profile_listing(load_profiles(args.profile_file)))
        return 0
    try:
        values = scaffold_values(args)
    except ValueError as exc:
        print(str(exc))
        return 1
    if args.print_command:
        print(scaffold_command(values, profile_id=args.profile))
        return 0
    text = render_template(TEMPLATE.read_text(encoding="utf-8"), values)
    output = args.out or Path(f"docs/{values['NAME']}_PREREGISTRATION.md")
    if output.exists() and not args.force:
        print(f"refusing to overwrite existing file: {output}")
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="Stable lowercase study id.")
    parser.add_argument(
        "--profile",
        help="Profile id from configs/prospective_study_lanes.json.",
    )
    parser.add_argument("--profile-file", type=Path, default=PROFILES)
    parser.add_argument("--list-profiles", action="store_true")
    parser.add_argument("--print-command", action="store_true")
    parser.add_argument("--title", help="Human-readable study title.")
    parser.add_argument("--language")
    parser.add_argument("--term-file", type=Path)
    parser.add_argument("--protocol", type=Path)
    parser.add_argument("--report-doc", type=Path)
    parser.add_argument("--source", action="append", default=[], metavar="LABEL=PATH")
    parser.add_argument("--skip-range")
    parser.add_argument("--direction")
    parser.add_argument("--min-normalized-length")
    parser.add_argument("--candidate-type")
    parser.add_argument("--context-rule")
    parser.add_argument("--controls")
    parser.add_argument("--correction")
    parser.add_argument("--source-term-files")
    parser.add_argument("--dedupe-rule")
    parser.add_argument("--excluded-prior")
    parser.add_argument("--candidate-rule")
    parser.add_argument("--primary-row-outcome")
    parser.add_argument("--primary-study-outcome")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def scaffold_values(args: argparse.Namespace) -> dict[str, str]:
    profile = profile_by_id(args.profile, args.profile_file) if args.profile else {}
    raw_name = args.name or str(profile.get("id", ""))
    if not raw_name:
        raise ValueError("--name is required unless --profile is supplied")
    safe_name = normalize_name(raw_name)
    title = args.title or str(profile.get("title") or safe_name.replace("_", " ").title())
    name_upper = safe_name.upper()
    term_file = args.term_file or Path(
        str(profile.get("term_file") or f"terms/{safe_name}_terms.csv")
    )
    protocol = args.protocol or Path(
        str(profile.get("protocol") or f"protocols/{safe_name}.toml")
    )
    report_doc = args.report_doc or Path(
        str(profile.get("report_doc") or f"docs/{name_upper}_REPORT.md")
    )
    sources = parse_sources(args.source) if args.source else profile_sources(profile)
    config_paths = [path for _label, path in sources]
    return {
        "name": safe_name,
        "NAME": name_upper,
        "title": title,
        "language": arg_or_profile(
            args.language,
            profile,
            "language",
            "[hebrew|greek|michigan|english]",
        ),
        "term_file": path_without_terms_prefix(term_file),
        "protocol": path_without_protocols_prefix(protocol),
        "report_doc": str(report_doc),
        "source_lines": source_lines(sources),
        "config_path": first_or_placeholder(config_paths, "[config path]"),
        "config_path_lines": lock_path_lines(config_paths),
        "skip_range": arg_or_profile(
            args.skip_range,
            profile,
            "skip_range",
            "[min..max]",
        ),
        "direction": arg_or_profile(
            args.direction,
            profile,
            "direction",
            "[forward|backward|both]",
        ),
        "min_normalized_length": arg_or_profile(
            args.min_normalized_length,
            profile,
            "min_normalized_length",
            "[n]",
        ),
        "candidate_type": arg_or_profile(
            args.candidate_type,
            profile,
            "candidate_type",
            "[candidate type]",
        ),
        "context_rule": arg_or_profile(
            args.context_rule,
            profile,
            "context_rule",
            "[surface/context]",
        ),
        "controls": arg_or_profile(args.controls, profile, "controls", "[control budget]"),
        "correction": arg_or_profile(args.correction, profile, "correction", "[method]"),
        "source_term_files": arg_or_profile(
            args.source_term_files,
            profile,
            "source_term_files",
            "[list]",
        ),
        "dedupe_rule": arg_or_profile(args.dedupe_rule, profile, "dedupe_rule", "[rule]"),
        "excluded_prior": arg_or_profile(args.excluded_prior, profile, "excluded_prior", "[list]"),
        "candidate_rule": arg_or_profile(args.candidate_rule, profile, "candidate_rule", "[rule]"),
        "primary_row_outcome": arg_or_profile(
            args.primary_row_outcome,
            profile,
            "primary_row_outcome",
            "[metric]",
        ),
        "primary_study_outcome": arg_or_profile(
            args.primary_study_outcome,
            profile,
            "primary_study_outcome",
            "[metric and threshold]",
        ),
    }


def load_profiles(path: Path = PROFILES) -> list[dict[str, Any]]:
    payload = read_json_object(path)
    profiles = payload.get("profiles", [])
    if not isinstance(profiles, list):
        raise ValueError(f"profiles must be a list: {path}")
    return profiles


def profile_by_id(profile_id: str | None, path: Path = PROFILES) -> dict[str, Any]:
    if not profile_id:
        return {}
    for profile in load_profiles(path):
        if profile.get("id") == profile_id:
            return profile
    raise ValueError(f"unknown prospective study profile: {profile_id}")


def profile_sources(profile: dict[str, Any]) -> list[tuple[str, str]]:
    sources = profile.get("sources", [])
    if not sources:
        return []
    parsed = []
    for source in sources:
        if not isinstance(source, dict) or "label" not in source or "path" not in source:
            raise ValueError("profile sources must contain label and path")
        parsed.append((str(source["label"]), str(source["path"])))
    return parsed


def arg_or_profile(
    arg_value: str | None,
    profile: dict[str, Any],
    key: str,
    fallback: str,
) -> str:
    if arg_value is not None:
        return arg_value
    value = profile.get(key)
    if value is None:
        return fallback
    return str(value)


def profile_listing(profiles: list[dict[str, Any]]) -> str:
    lines = ["Profile\tStatus\tTitle"]
    for profile in profiles:
        lines.append(
            "\t".join(
                [
                    str(profile.get("id", "")),
                    str(profile.get("status", "")),
                    str(profile.get("title", "")),
                ]
            )
        )
    return "\n".join(lines)


def scaffold_command(values: dict[str, str], *, profile_id: str | None = None) -> str:
    parts = ["python3", "-m", "scripts.scaffold_prospective_study"]
    if profile_id:
        parts.extend(["--profile", profile_id])
    else:
        parts.extend(["--name", values["name"]])
    parts.extend(["--out", f"docs/{values['NAME']}_PREREGISTRATION.md"])
    return " ".join(shlex.quote(part) for part in parts)


def shell_setting(key: str, value: str) -> str:
    return shlex.quote(f"{key}={value}")


def render_template(template: str, values: dict[str, str]) -> str:
    text = template
    text = text.replace(
        "--setting skip_range=[min..max]",
        f"--setting {shell_setting('skip_range', values['skip_range'])}",
    )
    text = text.replace(
        "--setting direction=[direction]",
        f"--setting {shell_setting('direction', values['direction'])}",
    )
    text = text.replace(
        "--setting min_normalized_length=[n]",
        f"--setting {shell_setting('min_normalized_length', values['min_normalized_length'])}",
    )
    text = text.replace(
        "--setting controls=[control budget]",
        f"--setting {shell_setting('controls', values['controls'])}",
    )
    text = text.replace(
        "--setting correction=[method]",
        f"--setting {shell_setting('correction', values['correction'])}",
    )
    text = text.replace(
        "- source term files: `[list]`;",
        f"- source term files: `{values['source_term_files']}`;",
    )
    text = text.replace(
        "- dedupe rule: `[rule]`;",
        f"- dedupe rule: `{values['dedupe_rule']}`;",
    )
    text = text.replace(
        "- excluded prior rows/forms: `[list]`.",
        f"- excluded prior rows/forms: `{values['excluded_prior']}`.",
    )
    text = text.replace(
        "| Candidate selection rule | `[rule]` |",
        f"| Candidate selection rule | `{values['candidate_rule']}` |",
    )
    text = text.replace(
        "| Context rule | `[rule]` |",
        f"| Context rule | `{values['context_rule']}` |",
    )
    replacements = {
        "[name]": values["name"],
        "[NAME]": values["NAME"],
        "[language/source scope]": values["language"],
        "[candidate type]": values["candidate_type"],
        "[skip range]": values["skip_range"],
        "[direction]": values["direction"],
        "[surface/context]": values["context_rule"],
        "[control]": values["controls"],
        "terms/[term_file].csv": f"terms/{values['term_file']}",
        "protocols/[protocol].toml": f"protocols/{values['protocol']}.toml",
        "docs/[NAME]_REPORT.md": values["report_doc"],
        "[hebrew|greek|michigan|english]": values["language"],
        "[n]": values["min_normalized_length"],
        "[min..max]": values["skip_range"],
        "[forward|backward|both]": values["direction"],
        "[budget]": values["controls"],
        "[method]": values["correction"],
        "[control budget]": values["controls"],
        "[metric and threshold]": values["primary_study_outcome"],
        "[metric]": values["primary_row_outcome"],
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace(
        "- `[LABEL]` from `[config path]`;\n- `[LABEL]` from `[config path]`.",
        values["source_lines"],
    )
    text = text.replace("  --path [config path] \\", values["config_path_lines"])
    return text


def normalize_name(raw: str) -> str:
    name = raw.strip().lower().replace("-", "_")
    if not re.fullmatch(r"[a-z0-9_]+", name):
        raise ValueError("name must contain only letters, numbers, dashes, or underscores")
    return name


def parse_sources(raw_sources: list[str]) -> list[tuple[str, str]]:
    parsed: list[tuple[str, str]] = []
    for raw in raw_sources:
        if "=" not in raw:
            raise ValueError(f"source must be LABEL=PATH: {raw}")
        label, path = raw.split("=", 1)
        parsed.append((label.strip(), path.strip()))
    return parsed


def source_lines(sources: list[tuple[str, str]]) -> str:
    if not sources:
        return "- `[LABEL]` from `[config path]`;\n- `[LABEL]` from `[config path]`."
    lines = []
    for index, (label, path) in enumerate(sources):
        punctuation = "." if index == len(sources) - 1 else ";"
        lines.append(f"- `{label}` from `{path}`{punctuation}")
    return "\n".join(lines)


def lock_path_lines(paths: list[str]) -> str:
    if not paths:
        return "  --path [config path] \\"
    return "\n".join(f"  --path {path} \\" for path in paths)


def first_or_placeholder(values: list[str], placeholder: str) -> str:
    return values[0] if values else placeholder


def path_without_terms_prefix(path: Path) -> str:
    text = str(path)
    return text.removeprefix("terms/")


def path_without_protocols_prefix(path: Path) -> str:
    text = str(path)
    return text.removeprefix("protocols/").removesuffix(".toml")


if __name__ == "__main__":
    raise SystemExit(main())
