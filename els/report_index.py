"""Build a compact index for generated report files."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


EXCLUDED_PATH_PARTS = {".step-stamps", "benchmarks"}
EXCLUDED_INDEX_FILES = {"INDEX.md", "index.json"}


@dataclass(frozen=True)
class ReportEntry:
    path: str
    kind: str
    bytes: int
    rows: int | None = None
    columns: tuple[str, ...] = ()
    sample_rows: tuple[dict[str, str], ...] = ()
    json_keys: tuple[str, ...] = ()
    label: str = ""
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


def scan_reports(root: str | Path, *, sample_limit: int = 3) -> list[ReportEntry]:
    root_path = Path(root).expanduser().resolve()
    entries: list[ReportEntry] = []
    for path in sorted(root_path.rglob("*")):
        if should_skip_report_path(root_path, path):
            continue
        if path.suffix == ".csv":
            entries.append(_summarize_csv(root_path, path, sample_limit=sample_limit))
        elif path.suffix == ".json":
            entries.append(_summarize_json(root_path, path))
    return entries


def should_skip_report_path(root: Path, path: Path) -> bool:
    if not path.is_file() or path.name == ".gitkeep":
        return True
    if path.name in EXCLUDED_INDEX_FILES:
        return True
    relative = path.relative_to(root)
    if any(part.startswith(".") for part in relative.parts):
        return True
    return any(part in EXCLUDED_PATH_PARTS for part in relative.parts)


def write_markdown_index(
    entries: list[ReportEntry],
    out_path: str | Path,
    *,
    reports_root: str | Path,
) -> None:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    csv_entries = [entry for entry in entries if entry.kind == "csv"]
    json_entries = [entry for entry in entries if entry.kind == "json"]
    lines = [
        "# Report Index",
        "",
        f"Generated UTC: {datetime.now(UTC).isoformat()}",
        f"Reports root: `{Path(reports_root)}`",
        "",
        "## CSV Reports",
        "",
        "| Path | Rows | Columns | Bytes |",
        "| --- | ---: | ---: | ---: |",
    ]
    for entry in csv_entries:
        lines.append(
            f"| `{entry.path}` | {entry.rows or 0} | {len(entry.columns)} | {entry.bytes} |"
        )
    lines.extend(
        [
            "",
            "## JSON Reports",
            "",
            "| Path | Label | Keys | Bytes |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for entry in json_entries:
        keys = ", ".join(entry.json_keys[:8])
        lines.append(
            f"| `{entry.path}` | {_cell(entry.label)} | {_cell(keys)} | {entry.bytes} |"
        )

    lines.extend(["", "## Samples", ""])
    for entry in csv_entries:
        if not entry.sample_rows:
            continue
        lines.extend(_sample_table(entry))
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json_index(entries: list[ReportEntry], out_path: str | Path) -> None:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_utc": datetime.now(UTC).isoformat(),
        "reports": [
            {
                "path": entry.path,
                "kind": entry.kind,
                "bytes": entry.bytes,
                "rows": entry.rows,
                "columns": list(entry.columns),
                "json_keys": list(entry.json_keys),
                "label": entry.label,
                "error": entry.error,
                "metadata": entry.metadata,
            }
            for entry in entries
        ],
    }
    out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _summarize_csv(root: Path, path: Path, *, sample_limit: int) -> ReportEntry:
    sample: list[dict[str, str]] = []
    row_count = 0
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = tuple(reader.fieldnames or ())
            for row in reader:
                row_count += 1
                if len(sample) < sample_limit:
                    sample.append({key: row.get(key, "") for key in columns})
        return ReportEntry(
            path=str(path.relative_to(root)),
            kind="csv",
            bytes=path.stat().st_size,
            rows=row_count,
            columns=columns,
            sample_rows=tuple(sample),
        )
    except Exception as exc:  # pragma: no cover - defensive index should keep going.
        return ReportEntry(
            path=str(path.relative_to(root)),
            kind="csv",
            bytes=path.stat().st_size,
            error=str(exc),
        )


def _summarize_json(root: Path, path: Path) -> ReportEntry:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            keys = tuple(sorted(data.keys()))
            label = _json_label(data)
            metadata = _json_metadata(data)
        else:
            keys = ()
            label = type(data).__name__
            metadata = {}
        return ReportEntry(
            path=str(path.relative_to(root)),
            kind="json",
            bytes=path.stat().st_size,
            json_keys=keys,
            label=label,
            metadata=metadata,
        )
    except Exception as exc:  # pragma: no cover - defensive index should keep going.
        return ReportEntry(
            path=str(path.relative_to(root)),
            kind="json",
            bytes=path.stat().st_size,
            error=str(exc),
        )


def _json_label(data: dict[str, Any]) -> str:
    for key in ["tool", "source_id", "name"]:
        value = data.get(key)
        if value:
            return str(value)
    return ""


def _json_metadata(data: dict[str, Any]) -> dict[str, Any]:
    wanted = [
        "created_utc",
        "downloaded_at",
        "hit_count",
        "rows",
        "summary_rows",
        "verse_count",
        "book_count",
        "status",
    ]
    return {key: data[key] for key in wanted if key in data}


def _sample_table(entry: ReportEntry) -> list[str]:
    columns = entry.columns[:8]
    lines = [
        f"### `{entry.path}`",
        "",
        "| " + " | ".join(_cell(column) for column in columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in entry.sample_rows:
        lines.append("| " + " | ".join(_cell(row.get(column, "")) for column in columns) + " |")
    lines.append("")
    return lines


def _cell(value: Any, *, limit: int = 80) -> str:
    text = str(value).replace("\n", " ").replace("|", "\\|")
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text
