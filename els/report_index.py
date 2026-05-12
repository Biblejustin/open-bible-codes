"""Build a compact index for generated report files."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from els.report_db import (
    DuckDBUnavailable,
    connect,
    report_table_name_for_path,
)


EXCLUDED_PATH_PARTS = {".step-stamps", "benchmarks", "db", "partitions", "worker_batches", "worker_imports"}
EXCLUDED_INDEX_FILES = {"INDEX.md", "index.json", "protocol_run.manifest.json"}


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


def scan_reports(
    root: str | Path,
    *,
    sample_limit: int = 3,
    db_path: str | Path | None = None,
    cache_path: str | Path | None = None,
) -> list[ReportEntry]:
    root_path = Path(root).expanduser().resolve()
    report_db = Path(db_path) if db_path is not None else root_path / "db" / "open_bible_codes.duckdb"
    row_count_cache_path = Path(cache_path) if cache_path is not None else root_path / ".report_index_cache.json"
    row_count_cache = _read_row_count_cache(row_count_cache_path)
    db_row_counts = _db_row_counts(report_db)
    entries: list[ReportEntry] = []
    for path in sorted(root_path.rglob("*")):
        if should_skip_report_path(root_path, path):
            continue
        if path.suffix == ".csv":
            entries.append(
                _summarize_csv(
                    root_path,
                    path,
                    sample_limit=sample_limit,
                    db_row_counts=db_row_counts,
                    row_count_cache=row_count_cache,
                )
            )
        elif path.suffix == ".json":
            entries.append(_summarize_json(root_path, path))
    _write_row_count_cache(row_count_cache_path, row_count_cache)
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
    write_text_if_changed(out, "\n".join(lines) + "\n")


def write_json_index(entries: list[ReportEntry], out_path: str | Path) -> None:
    out = Path(out_path)
    payload = {
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
    write_text_if_changed(out, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _summarize_csv(
    root: Path,
    path: Path,
    *,
    sample_limit: int,
    db_row_counts: dict[str, tuple[int, int, int]],
    row_count_cache: dict[str, dict[str, int]],
) -> ReportEntry:
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
                if len(sample) >= sample_limit:
                    break
        db_row_count = _db_csv_row_count(db_row_counts, path)
        if db_row_count is not None:
            row_count = db_row_count
            _cache_row_count(root, path, row_count_cache, row_count)
        else:
            row_count = _cached_or_count_csv_rows(root, path, row_count_cache)
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


def _count_csv_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        try:
            next(reader)
        except StopIteration:
            return 0
        return sum(1 for _row in reader)


def _cached_or_count_csv_rows(root: Path, path: Path, cache: dict[str, dict[str, int]]) -> int:
    key = str(path.relative_to(root))
    stat = path.stat()
    cached = cache.get(key)
    if (
        cached
        and cached.get("size") == stat.st_size
        and cached.get("mtime_ns") == stat.st_mtime_ns
        and "rows" in cached
    ):
        return int(cached["rows"])
    row_count = _count_csv_rows(path)
    _cache_row_count(root, path, cache, row_count)
    return row_count


def _cache_row_count(root: Path, path: Path, cache: dict[str, dict[str, int]], row_count: int) -> None:
    stat = path.stat()
    cache[str(path.relative_to(root))] = {
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "rows": row_count,
    }


def _read_row_count_cache(path: Path) -> dict[str, dict[str, int]]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    return {
        str(key): {
            "size": int(value.get("size", 0)),
            "mtime_ns": int(value.get("mtime_ns", 0)),
            "rows": int(value.get("rows", 0)),
        }
        for key, value in data.items()
        if isinstance(value, dict)
    }


def _write_row_count_cache(path: Path, cache: dict[str, dict[str, int]]) -> None:
    write_text_if_changed(path, json.dumps(cache, ensure_ascii=False, sort_keys=True) + "\n")


def write_text_if_changed(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = text.encode("utf-8")
    if path.exists() and path.read_bytes() == content:
        return
    path.write_bytes(content)


def _db_row_counts(db_path: Path | None) -> dict[str, tuple[int, int, int]]:
    if db_path is None or not db_path.exists():
        return {}
    try:
        with connect(db_path, read_only=True) as con:
            metadata_table = con.execute(
                "SELECT count(*) FROM information_schema.tables WHERE table_name = 'report_table_imports'"
            ).fetchone()
            if not metadata_table or not metadata_table[0]:
                return {}
            rows = con.execute(
                """
                SELECT table_name, source_size_bytes, source_mtime_ns, row_count
                FROM report_table_imports
                """
            ).fetchall()
    except DuckDBUnavailable:
        return {}
    return {
        str(table_name): (int(source_size), int(source_mtime), int(row_count))
        for table_name, source_size, source_mtime, row_count in rows
    }


def _db_csv_row_count(
    db_row_counts: dict[str, tuple[int, int, int]],
    source_path: Path,
) -> int | None:
    if not db_row_counts:
        return None
    table_name = report_table_name_for_path(source_path)
    row = db_row_counts.get(table_name)
    if row is None:
        return None
    source_size, source_mtime_ns, row_count = row
    stat = source_path.stat()
    if source_size != stat.st_size or source_mtime_ns != stat.st_mtime_ns:
        return None
    return row_count


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
