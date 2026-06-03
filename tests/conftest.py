"""Pytest configuration for the EDLS test suite.

Goal: a fresh clone (or CI without a corpus-download step) can run the data-free
unit suite green, while the full suite still runs everything when ``data/`` and
``reports/`` are present.

Two mechanisms:

1. The ``integration`` and ``requires_corpus`` markers let tests opt in to being
   deselected with ``pytest -m "not integration"``.
2. A failure hook converts the specific "missing local corpus/report artifact"
   error into a *skip*. This auto-covers the many tests that call
   ``load_corpus`` against a real config or read a generated ``reports/`` file
   without needing every one tagged by hand. Any other failure -- assertions,
   real bugs, or a ``FileNotFoundError`` for a tracked source file -- still
   fails loudly.

Run the data-free unit suite:        pytest -m "not integration"
Run everything (needs data/+reports): pytest

Limitation: the hook covers the setup and call phases. A module that loads a
corpus at import time would still error during collection; corpora should be
loaded inside tests or fixtures, not at module scope.
"""

from __future__ import annotations

import pytest

from tests._skip_helpers import is_missing_generated_artifact


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when not in ("setup", "call") or not report.failed:
        return
    exc = call.excinfo.value if call.excinfo is not None else None
    if is_missing_generated_artifact(exc):
        report.outcome = "skipped"
        lineno = item.location[1] or 0
        report.longrepr = (
            str(item.fspath),
            lineno,
            "Skipped: requires local corpus/report data "
            "(data/ or reports/ not present in this checkout).",
        )
