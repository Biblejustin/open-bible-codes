from pathlib import Path

from scripts.check_expanded_strata_tooling import check_tooling


def test_check_tooling_passes_for_current_repo() -> None:
    result = check_tooling(Path("docs/EXPANDED_STRATA_TOOLING.md"), Path("Makefile"))

    assert result["ok"] is True
    assert result["missing"] == []


def test_check_tooling_flags_missing_doc_reference(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    makefile = tmp_path / "Makefile"
    doc.write_text("make match-strata-index\n", encoding="utf-8")
    makefile.write_text("match-strata-index:\n", encoding="utf-8")

    result = check_tooling(doc, makefile)

    assert result["ok"] is False
    assert any("protocols/match_strata_index.toml" in item for item in result["missing"])


def test_check_tooling_flags_matrix_width_flag_drift(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    makefile = tmp_path / "Makefile"
    repo_doc = Path("docs/EXPANDED_STRATA_TOOLING.md").read_text(encoding="utf-8")
    repo_makefile = Path("Makefile").read_text(encoding="utf-8")
    doc.write_text(repo_doc.replace("--row-width 50", "--width 50"), encoding="utf-8")
    makefile.write_text(
        repo_makefile.replace('--row-width "$(MATRIX_CLUSTER_WIDTH)"', '--width "$(MATRIX_CLUSTER_WIDTH)"'),
        encoding="utf-8",
    )

    result = check_tooling(doc, makefile)

    assert result["ok"] is False
    assert any("--row-width 50" in item for item in result["missing"])
    assert any('--row-width "$(MATRIX_CLUSTER_WIDTH)"' in item for item in result["missing"])
