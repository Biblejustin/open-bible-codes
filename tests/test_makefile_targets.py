"""Guard the developer-workflow Makefile targets.

The cert / cert-fast / docs-gate / coverage targets are the validation loop
this repo's conventions depend on (background-safe exit codes, the fast
docs-only gate, parallel runs, repeatable coverage). A Makefile edit that
drops or renames one should fail a test, the same way the doc-check targets
are guarded elsewhere.
"""

from __future__ import annotations

from pathlib import Path

MAKEFILE = Path("Makefile").read_text(encoding="utf-8")


def recipe_of(target: str) -> str:
    """Return the recipe block of a Makefile target."""
    lines = MAKEFILE.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.startswith(f"{target}:"))
    except StopIteration:
        return ""
    body = []
    for line in lines[start + 1:]:
        if line.startswith(("\t", "    ")):
            body.append(line)
        elif line.strip() == "" or line.lstrip().startswith("#"):
            continue
        else:
            break
    return "\n".join(body)


def test_phony_declares_workflow_targets() -> None:
    phony = next(line for line in MAKEFILE.splitlines() if line.startswith(".PHONY:"))
    for target in ("test", "cert", "cert-fast", "docs-gate", "coverage", "lint"):
        assert f" {target}" in phony or phony.endswith(target)


def test_cert_runs_full_suite_with_propagating_exit() -> None:
    recipe = recipe_of("cert")
    assert "python3 -m pytest" in recipe
    assert "-p no:cacheprovider" in recipe


def test_cert_fast_is_the_parallel_run() -> None:
    recipe = recipe_of("cert-fast")
    assert "python3 -m pytest" in recipe
    assert "-n auto" in recipe


def test_docs_gate_covers_claim_language_doc_guards_and_indexes() -> None:
    recipe = recipe_of("docs-gate")
    assert "check_public_claim_language" in recipe
    assert "reader-doc-checks" in recipe
    assert "build_docs_index" in recipe
    assert "build_protocol_index" in recipe


def test_coverage_target_measures_els_and_scripts() -> None:
    recipe = recipe_of("coverage")
    assert "--cov=els" in recipe
    assert "--cov=scripts" in recipe
