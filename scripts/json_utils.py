from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path} JSON root must be an object")
    return payload
