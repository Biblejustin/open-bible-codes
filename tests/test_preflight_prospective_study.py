import json
from pathlib import Path

from scripts import preflight_prospective_study as preflight


def test_required_settings_uses_defaults_and_dedupes() -> None:
    parser = preflight.build_parser()
    args = parser.parse_args(
        [
            "--preregistration",
            "docs/demo.md",
            "--manifest",
            "reports/demo.json",
            "--required-setting",
            "skip_range",
            "--required-setting",
            "source_set",
        ]
    )

    settings = preflight.required_settings_for(args)

    assert settings.count("skip_range") == 1
    assert "direction" in settings
    assert settings[-1] == "source_set"


def test_default_out_path_uses_manifest_stem() -> None:
    assert preflight.default_out_path(
        Path("reports/study_locks/greek_surface.manifest.json")
    ) == Path("reports/study_locks/greek_surface.preflight.json")
    assert preflight.default_out_path(
        Path("reports/study_locks/demo.json")
    ) == Path("reports/study_locks/demo.preflight.json")


def test_placeholder_failures_reports_missing_file(tmp_path) -> None:
    hits = preflight.placeholder_failures(tmp_path / "missing.md")

    assert hits == [
        {
            "path": str(tmp_path / "missing.md"),
            "line": 0,
            "column": 0,
            "placeholder": "missing file",
        }
    ]


def test_placeholder_failures_reports_unresolved_token(tmp_path) -> None:
    prereg = tmp_path / "study.md"
    prereg.write_text("Study `[name]`\n", encoding="utf-8")

    hits = preflight.placeholder_failures(prereg)

    assert hits[0]["line"] == 1
    assert hits[0]["placeholder"] == "[name]"


def test_main_fails_for_unresolved_preregistration_placeholder(tmp_path) -> None:
    prereg = tmp_path / "study.md"
    manifest = tmp_path / "manifest.json"
    out = tmp_path / "preflight.json"
    prereg.write_text("Study `[name]`\n", encoding="utf-8")
    manifest.write_text(
        json.dumps(
            {
                "status": "locked",
                "git": {"dirty": False},
                "locked_paths": [{"path": str(prereg), "type": "file", "sha256": "bad"}],
                "missing_paths": [],
                "settings": {
                    "skip_range": "2..50",
                    "direction": "both",
                    "min_normalized_length": "5",
                    "controls": "100",
                    "correction": "bh",
                },
            }
        ),
        encoding="utf-8",
    )

    code = preflight.main(
        [
            "--preregistration",
            str(prereg),
            "--manifest",
            str(manifest),
            "--no-verify-paths",
            "--allow-dirty",
            "--out",
            str(out),
        ]
    )

    assert code == 1
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["status"] == "failed"
    assert payload["placeholder_hits"][0]["placeholder"] == "[name]"


def test_main_passes_with_clean_preregistration_and_manifest(tmp_path) -> None:
    prereg = tmp_path / "study.md"
    manifest = tmp_path / "manifest.json"
    out = tmp_path / "preflight.json"
    prereg.write_text("Study `fixed`\n", encoding="utf-8")
    manifest.write_text(
        json.dumps(
            {
                "status": "locked",
                "git": {"dirty": False},
                "locked_paths": [{"path": str(prereg), "type": "file", "sha256": "bad"}],
                "missing_paths": [],
                "settings": {
                    "skip_range": "2..50",
                    "direction": "both",
                    "min_normalized_length": "5",
                    "controls": "100",
                    "correction": "bh",
                },
            }
        ),
        encoding="utf-8",
    )

    code = preflight.main(
        [
            "--preregistration",
            str(prereg),
            "--manifest",
            str(manifest),
            "--no-verify-paths",
            "--allow-dirty",
            "--out",
            str(out),
        ]
    )

    assert code == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["status"] == "passed"
    assert payload["output_path"] == str(out)
    assert "remote_failures" in payload
    assert "risky_tracked_paths" in payload
    assert "secret_pattern_hits" in payload


def test_main_uses_manifest_based_default_out_path(tmp_path) -> None:
    prereg = tmp_path / "study.md"
    manifest = tmp_path / "study.manifest.json"
    out = tmp_path / "study.preflight.json"
    prereg.write_text("Study `fixed`\n", encoding="utf-8")
    manifest.write_text(
        json.dumps(
            {
                "status": "locked",
                "git": {"dirty": False},
                "locked_paths": [{"path": str(prereg), "type": "file", "sha256": "bad"}],
                "missing_paths": [],
                "settings": {
                    "skip_range": "2..50",
                    "direction": "both",
                    "min_normalized_length": "5",
                    "controls": "100",
                    "correction": "bh",
                },
            }
        ),
        encoding="utf-8",
    )

    code = preflight.main(
        [
            "--preregistration",
            str(prereg),
            "--manifest",
            str(manifest),
            "--no-verify-paths",
            "--allow-dirty",
        ]
    )

    assert code == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["status"] == "passed"
    assert payload["output_path"] == str(out)


def test_clean_term_audit_failures_require_passed_status(tmp_path) -> None:
    missing = tmp_path / "missing.json"
    matched = tmp_path / "matched.json"
    passed = tmp_path / "passed.json"
    matched.write_text(
        json.dumps({"status": "matched", "match_rows": 2}),
        encoding="utf-8",
    )
    passed.write_text(
        json.dumps({"status": "passed", "match_rows": 0}),
        encoding="utf-8",
    )

    failures = preflight.clean_term_audit_failures([missing, matched, passed])

    assert failures == [
        f"missing audit summary: {missing}",
        f"{matched} status=matched match_rows=2",
    ]
