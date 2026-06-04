"""Schema-agnostic CSV/JSON output helpers.

Pure I/O utilities extracted from els.cli so analysis scripts and command
modules can share them without importing the whole CLI. cli.py re-imports these
for its own use; schema-specific writers (hit rows, batch rows) stay in cli.py.
"""

from __future__ import annotations

import csv
import json
import sys
from contextlib import contextmanager
from pathlib import Path


def write_dict_rows(
    rows: list[dict[str, object]],
    output_path: str,
    fieldnames: list[str] | None = None,
) -> None:
    path = Path(output_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

@contextmanager
def open_dict_reader(input_path: str | Path):
    path = Path(input_path).expanduser()
    with path.open("r", encoding="utf-8", newline="") as handle:
        yield csv.DictReader(handle)

@contextmanager
def open_dict_writer(output_path: str | Path, fieldnames: list[str]):
    path = Path(output_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        yield writer

def write_control_stats(rows: list[dict[str, object]], output_path: str | None) -> None:
    payload = json.dumps(rows, ensure_ascii=False, indent=2)
    if output_path:
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload + "\n", encoding="utf-8")
        return
    print(payload, file=sys.stderr)

def write_run_manifest(payload: dict[str, object], output_path: str) -> None:
    path = Path(output_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
