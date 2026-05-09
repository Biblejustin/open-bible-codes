"""Deterministic indexes for repository docs and protocol definitions."""

from __future__ import annotations

import tomllib
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DOC_INDEX_NAME = "INDEX.md"


@dataclass(frozen=True)
class MarkdownDocEntry:
    path: str
    title: str
    category: str


@dataclass(frozen=True)
class ProtocolEntry:
    path: str
    name: str
    description: str
    phase: str
    step_count: int
    term_paths: tuple[str, ...]
    output_roots: tuple[str, ...]
    error: str = ""


def scan_markdown_docs(root: str | Path) -> list[MarkdownDocEntry]:
    root_path = Path(root)
    entries: list[MarkdownDocEntry] = []
    for path in sorted(root_path.glob("*.md")):
        if path.name == DOC_INDEX_NAME:
            continue
        title = markdown_title(path)
        entries.append(
            MarkdownDocEntry(
                path=str(path.relative_to(root_path)),
                title=title or path.stem.replace("_", " ").title(),
                category=doc_category(path.name),
            )
        )
    return entries


def write_docs_index(
    entries: list[MarkdownDocEntry],
    out_path: str | Path,
    *,
    docs_root: str | Path,
) -> None:
    out = Path(out_path)
    grouped: dict[str, list[MarkdownDocEntry]] = defaultdict(list)
    for entry in entries:
        grouped[entry.category].append(entry)

    lines = [
        "# Documentation Index",
        "",
        f"Docs root: `{Path(docs_root)}`",
        f"Documents indexed: {len(entries)}",
        "",
    ]
    for category in sorted(grouped):
        lines.extend(
            [
                f"## {category}",
                "",
                "| Title | Path |",
                "| --- | --- |",
            ]
        )
        for entry in grouped[category]:
            lines.append(f"| {_cell(entry.title)} | `{entry.path}` |")
        lines.append("")
    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def scan_protocols(root: str | Path) -> list[ProtocolEntry]:
    root_path = Path(root)
    entries: list[ProtocolEntry] = []
    for path in sorted(root_path.rglob("*.toml")):
        entries.append(_summarize_protocol(root_path, path))
    return entries


def write_protocol_index(
    entries: list[ProtocolEntry],
    out_path: str | Path,
    *,
    protocols_root: str | Path,
) -> None:
    out = Path(out_path)
    grouped: dict[str, list[ProtocolEntry]] = defaultdict(list)
    for entry in entries:
        grouped[entry.phase].append(entry)

    lines = [
        "# Protocol Index",
        "",
        f"Protocols root: `{Path(protocols_root)}`",
        f"Protocols indexed: {len(entries)}",
        "",
    ]
    for phase in sorted(grouped):
        lines.extend(
            [
                f"## {phase}",
                "",
                "| Name | Description | Steps | Terms | Output Roots | Path |",
                "| --- | --- | ---: | --- | --- | --- |",
            ]
        )
        for entry in grouped[phase]:
            terms = ", ".join(entry.term_paths[:4])
            if len(entry.term_paths) > 4:
                terms += f", +{len(entry.term_paths) - 4}"
            roots = ", ".join(entry.output_roots[:3])
            if len(entry.output_roots) > 3:
                roots += f", +{len(entry.output_roots) - 3}"
            if entry.error:
                description = f"ERROR: {entry.error}"
            else:
                description = entry.description
            lines.append(
                "| "
                + " | ".join(
                    [
                        _cell(entry.name),
                        _cell(description),
                        str(entry.step_count),
                        _cell(terms),
                        _cell(roots),
                        f"`{entry.path}`",
                    ]
                )
                + " |"
            )
        lines.append("")
    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def markdown_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def doc_category(filename: str) -> str:
    stem = filename.removesuffix(".md")
    if stem.endswith("_PREREGISTRATION"):
        return "Preregistrations"
    if stem.endswith("_REPORT"):
        return "Reports"
    if "FINDINGS" in stem:
        return "Findings"
    if "CONTROL" in stem:
        return "Controls"
    if "VERSION" in stem:
        return "Version Studies"
    if "WRR" in stem or "METHODOLOGY" in stem or "HYPOTHESIS" in stem:
        return "Methodology"
    if stem in {"PERFORMANCE", "SOURCES_AND_LICENSES", "IMPLEMENTATION_PLAN"}:
        return "Project"
    return "Studies"


def protocol_phase(path: Path, data: dict[str, Any]) -> str:
    text = " ".join(
        [
            str(data.get("name", "")),
            str(data.get("description", "")),
            path.stem,
        ]
    ).lower()
    if "wrr" in text:
        return "Replication"
    if "dynamic_skip" in text or "partition" in text:
        return "Partitions"
    if "preregistration" in text or "prospective" in text:
        return "Prospective"
    if "control" in text:
        return "Controls"
    if "screening" in text:
        return "Screening"
    if "followup" in text or "follow-up" in text:
        return "Follow-Up"
    if "baseline" in text:
        return "Baseline"
    if "audit" in text:
        return "Audit"
    return "Analysis"


def _summarize_protocol(root: Path, path: Path) -> ProtocolEntry:
    relative = str(path.relative_to(root))
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
        steps = data.get("steps", [])
        term_paths = sorted(_protocol_term_paths(data))
        output_roots = sorted(_protocol_output_roots(data))
        return ProtocolEntry(
            path=relative,
            name=str(data.get("name") or path.stem),
            description=str(data.get("description") or ""),
            phase=protocol_phase(path, data),
            step_count=len(steps) if isinstance(steps, list) else 0,
            term_paths=tuple(term_paths),
            output_roots=tuple(output_roots),
        )
    except Exception as exc:  # pragma: no cover - defensive index should continue.
        return ProtocolEntry(
            path=relative,
            name=path.stem,
            description="",
            phase="Invalid",
            step_count=0,
            term_paths=(),
            output_roots=(),
            error=str(exc),
        )


def _protocol_term_paths(data: dict[str, Any]) -> set[str]:
    found: set[str] = set()
    for value in _walk_strings(data):
        if value.startswith("terms/") and value.endswith(".csv"):
            found.add(value)
        if "=" in value:
            maybe_path = value.split("=", 1)[1]
            if maybe_path.startswith("terms/") and maybe_path.endswith(".csv"):
                found.add(maybe_path)
    return found


def _protocol_output_roots(data: dict[str, Any]) -> set[str]:
    roots: set[str] = set()
    steps = data.get("steps", [])
    if not isinstance(steps, list):
        return roots
    for step in steps:
        if not isinstance(step, dict):
            continue
        for output in step.get("outputs", []):
            if not isinstance(output, str) or not output.startswith("reports/"):
                continue
            parts = output.split("/")
            if len(parts) >= 3 and parts[1] == "protocols":
                roots.add("/".join(parts[:3]))
            elif len(parts) >= 2:
                if len(parts) == 2 and Path(output).suffix:
                    roots.add(parts[0])
                else:
                    roots.add("/".join(parts[:2]))
            else:
                roots.add(output)
    return roots


def _walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        strings: list[str] = []
        for item in value:
            strings.extend(_walk_strings(item))
        return strings
    if isinstance(value, dict):
        strings = []
        for item in value.values():
            strings.extend(_walk_strings(item))
        return strings
    return []


def _cell(value: object, *, limit: int = 90) -> str:
    text = str(value).replace("\n", " ").replace("|", "\\|")
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text
