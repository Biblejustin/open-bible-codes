"""Helpers for skipping tests that need local corpus/report data.

Many tests load real Bible corpora from ``data/`` or read generated outputs
from ``reports/``. Both trees are gitignored, so a fresh clone (or CI without a
download step) cannot run them. Rather than hand-tag every such test, the
conftest converts the specific "missing local generated artifact" failure into
a skip. Everything else (assertions, real bugs, ``FileNotFoundError`` pointing
at tracked source files) still fails loudly.

This module holds the pure predicate so it can be unit-tested without invoking
the pytest hook machinery.
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

# Gitignored trees that only exist after downloading corpora or running
# protocols. A FileNotFoundError pointing inside one of these is "no local
# data", not a code bug.
GENERATED_TREES: tuple[Path, ...] = (
    REPO_ROOT / "data",
    REPO_ROOT / "reports",
)


def _candidate_path(exc: BaseException) -> str | None:
    """Best-effort path string the exception is complaining about."""
    filename = getattr(exc, "filename", None)
    if filename:
        return str(filename)
    filename2 = getattr(exc, "filename2", None)
    if filename2:
        return str(filename2)
    message = str(exc)
    return message or None


def is_missing_generated_artifact(exc: BaseException | None) -> bool:
    """True if ``exc`` is a missing-file error for a path under a gitignored
    generated tree (``data/`` or ``reports/``).

    Only ``FileNotFoundError`` / ``NotADirectoryError`` qualify; an
    ``AssertionError`` or a ``FileNotFoundError`` for a tracked source file is
    a real failure and returns False.
    """
    if not isinstance(exc, (FileNotFoundError, NotADirectoryError)):
        return False
    candidate = _candidate_path(exc)
    if not candidate:
        return False
    try:
        resolved = Path(candidate).resolve()
    except (OSError, ValueError, RuntimeError):
        resolved = None
    for tree in GENERATED_TREES:
        if resolved is not None and (resolved == tree or tree in resolved.parents):
            return True
        # Fall back to a string check for non-absolute / synthetic messages.
        if str(tree) in candidate:
            return True
    return False
