import pytest

from scripts import build_doxa_four_source_claim_followup_report as report


def test_followup_status_passes_only_when_all_criteria_pass() -> None:
    criteria = [("one", "pass", ""), ("two", "pass", "")]
    assert report.followup_status(criteria) == "claim_followup_review_candidate"

    criteria = [("one", "pass", ""), ("two", "fail", "")]
    assert report.followup_status(criteria) == "review_hold"


def test_q_pass_gate_uses_claim_followup_threshold() -> None:
    assert report.q_passes("0.01")
    assert not report.q_passes("0.0101")
    assert not report.q_passes("")


def test_criteria_requires_expected_four_corpora() -> None:
    paired_rows = [
        {"corpus": "BYZ_NT", "combined_min_q": "0.0002", "flags": "short_base_term"},
        {"corpus": "SBLGNT", "combined_min_q": "0.0002", "flags": "short_base_term"},
        {"corpus": "TCG_NT", "combined_min_q": "0.0002", "flags": "short_base_term"},
        {"corpus": "TR_NT", "combined_min_q": "0.0002", "flags": "short_base_term"},
    ]
    context_rows = [
        {"corpus": "BYZ_NT", "center_exact": "True"},
        {"corpus": "SBLGNT", "center_exact": "True"},
        {"corpus": "TCG_NT", "center_exact": "True"},
        {"corpus": "TR_NT", "center_exact": "True"},
    ]

    criteria = report.criteria_results(paired_rows, context_rows)

    assert report.followup_status(criteria) == "claim_followup_review_candidate"


def test_report_uses_build_commit_label_for_cached_subreports() -> None:
    text = report.build_report(
        paired_rows=[
            {
                "corpus": "BYZ_NT",
                "combined_min_q": "0.0002",
                "combined_min_p": "0.0002",
                "term_any_p_ge": "0.1",
                "random_any_p_ge": "0.1",
                "observed_score": "1",
                "matched_refs": "JHN 1:14",
                "flags": "short_base_term",
            },
            {
                "corpus": "SBLGNT",
                "combined_min_q": "0.0002",
                "combined_min_p": "0.0002",
                "term_any_p_ge": "0.1",
                "random_any_p_ge": "0.1",
                "observed_score": "1",
                "matched_refs": "JHN 1:14",
                "flags": "short_base_term",
            },
            {
                "corpus": "TCG_NT",
                "combined_min_q": "0.0002",
                "combined_min_p": "0.0002",
                "term_any_p_ge": "0.1",
                "random_any_p_ge": "0.1",
                "observed_score": "1",
                "matched_refs": "JHN 1:14",
                "flags": "short_base_term",
            },
            {
                "corpus": "TR_NT",
                "combined_min_q": "0.0002",
                "combined_min_p": "0.0002",
                "term_any_p_ge": "0.1",
                "random_any_p_ge": "0.1",
                "observed_score": "1",
                "matched_refs": "JHN 1:14",
                "flags": "short_base_term",
            },
        ],
        context_rows=[
            context_row("BYZ_NT"),
            context_row("SBLGNT"),
            context_row("TCG_NT"),
            context_row("TR_NT"),
        ],
        protocol_manifest={"steps": []},
        run_commit="abc123",
        prereg_commit="def456",
    )

    assert "Local report build commit" in text
    assert "Run commit" not in text
    assert "recorded in local manifests only" in text
    assert "`δοξα` (doxa; English: glory)" in text
    assert "`δοξανωσ` (doxanos; English: hidden extension form from doxa)" in text
    assert "`δόξαν ὡς` (doxan hos; English: glory as)" in text
    assert "`δοξαζηται` (doxazetai)" in text


def test_report_can_point_to_confirmatory_output_dir() -> None:
    text = report.build_report(
        paired_rows=[
            paired_row("BYZ_NT"),
            paired_row("SBLGNT"),
            paired_row("TCG_NT"),
            paired_row("TR_NT"),
        ],
        context_rows=[
            context_row("BYZ_NT"),
            context_row("SBLGNT"),
            context_row("TCG_NT"),
            context_row("TR_NT"),
        ],
        protocol_manifest={"steps": []},
        run_commit="abc123",
        prereg_commit="def456",
        report_title="Doxa Four-Source Confirmatory Follow-Up Report",
        preregistration_doc="docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_PREREGISTRATION.md",
        protocol_path="protocols/doxa_four_source_confirmatory_followup.toml",
        term_control_samples=20000,
        random_control_samples=20000,
        report_out=report.Path("docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md"),
    )

    assert "Doxa Four-Source Confirmatory Follow-Up Report" in text
    assert "20000 shuffled-term controls" in text
    assert "reports/doxa_four_source_confirmatory_followup/paired_controls_summary.csv" in text
    assert "reports/doxa_four_source_confirmatory_followup/letter_paths.md" in text


def test_cli_requires_explicit_preregistration_commit(tmp_path) -> None:
    paired = tmp_path / "paired.csv"
    context = tmp_path / "context.csv"
    manifest = tmp_path / "protocol.json"
    paired.write_text("corpus\n", encoding="utf-8")
    context.write_text("corpus\n", encoding="utf-8")
    manifest.write_text("{}", encoding="utf-8")

    with pytest.raises(SystemExit, match="preregistration-commit"):
        report.main(
            [
                "--paired-summary",
                str(paired),
                "--context-summary",
                str(context),
                "--protocol-manifest",
                str(manifest),
                "--report-out",
                str(tmp_path / "report.md"),
                "--manifest-out",
                str(tmp_path / "manifest.json"),
                "--run-commit",
                "abc123",
            ]
        )


def test_report_omits_volatile_step_timings(tmp_path) -> None:
    (tmp_path / "paired_controls.manifest.json").write_text(
        '{"created_utc": "2026-05-06T00:12:54+00:00", "seconds": 89.125}',
        encoding="utf-8",
    )
    (tmp_path / "context_review.manifest.json").write_text(
        '{"created_utc": "2026-05-06T00:12:55+00:00", "seconds": 0.759}',
        encoding="utf-8",
    )
    text = report.build_report(
        paired_rows=[
            paired_row("BYZ_NT"),
            paired_row("SBLGNT"),
            paired_row("TCG_NT"),
            paired_row("TR_NT"),
        ],
        context_rows=[
            context_row("BYZ_NT"),
            context_row("SBLGNT"),
            context_row("TCG_NT"),
            context_row("TR_NT"),
        ],
        protocol_manifest={
            "status": "success",
            "started_utc": "volatile-start",
            "ended_utc": "volatile-end",
            "duration_seconds": 0.016,
            "steps": [
                {"id": "paired_controls", "duration_seconds": 0.009},
                {"id": "context_review", "duration_seconds": 0.008},
            ],
        },
        run_commit="abc123",
        prereg_commit="def456",
        report_out=tmp_path / "report.md",
    )

    assert "Paired controls completed UTC | recorded in local manifests only" in text
    assert "Context review completed UTC | recorded in local manifests only" in text
    assert "Analysis runtime | recorded in local manifests only" in text
    assert "2026-05-06T00:12:54+00:00" not in text
    assert "89.884s" not in text
    assert "volatile-start" not in text
    assert "0.016s" not in text


def paired_row(corpus: str) -> dict[str, str]:
    return {
        "corpus": corpus,
        "combined_min_q": "0.0002",
        "combined_min_p": "0.0002",
        "term_any_p_ge": "0.1",
        "random_any_p_ge": "0.1",
        "observed_score": "1",
        "matched_refs": "JHN 1:14",
        "flags": "short_base_term",
    }


def context_row(corpus: str) -> dict[str, str]:
    return {
        "corpus": corpus,
        "center_exact": "True",
        "center_ref": "2Thess 3:1",
        "center_word": "δοξαζηται",
        "hit_refs": "2Thess 3:1",
        "context_read": "exact-center context",
    }
