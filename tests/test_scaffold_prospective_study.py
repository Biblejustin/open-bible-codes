from scripts import scaffold_prospective_study as scaffold


def test_scaffold_values_defaults_paths_from_name() -> None:
    parser = scaffold.build_parser()
    args = parser.parse_args(["--name", "Greek-Surface-Next"])

    values = scaffold.scaffold_values(args)

    assert values["name"] == "greek_surface_next"
    assert values["NAME"] == "GREEK_SURFACE_NEXT"
    assert values["term_file"] == "greek_surface_next_terms.csv"
    assert values["protocol"] == "greek_surface_next"


def test_render_template_replaces_core_placeholders() -> None:
    parser = scaffold.build_parser()
    args = parser.parse_args(
        [
            "--name",
            "greek_surface_next",
            "--language",
            "greek",
            "--source",
            "TR_NT=configs/example_ebible_grctr.toml",
            "--skip-range",
            "2..50",
            "--direction",
            "both",
            "--min-normalized-length",
            "5",
            "--controls",
            "5000_each",
            "--correction",
            "benjamini_hochberg",
        ]
    )
    values = scaffold.scaffold_values(args)
    text = scaffold.render_template(
        "Study [name] [NAME]\n"
        "- `[LABEL]` from `[config path]`;\n"
        "- `[LABEL]` from `[config path]`.\n"
        "terms/[term_file].csv protocols/[protocol].toml docs/[NAME]_REPORT.md\n"
        "  --path [config path] \\\n"
        "[min..max] [forward|backward|both] [n] [control budget] [method]",
        values,
    )

    assert "greek_surface_next" in text
    assert "GREEK_SURFACE_NEXT" in text
    assert "- `TR_NT` from `configs/example_ebible_grctr.toml`." in text
    assert "terms/greek_surface_next_terms.csv" in text
    assert "protocols/greek_surface_next.toml" in text
    assert "docs/GREEK_SURFACE_NEXT_REPORT.md" in text
    assert "--path configs/example_ebible_grctr.toml" in text
    assert "2..50 both 5 5000_each benjamini_hochberg" in text


def test_render_template_separates_source_files_dedupe_and_exclusions() -> None:
    parser = scaffold.build_parser()
    args = parser.parse_args(
        [
            "--name",
            "demo",
            "--source-term-files",
            "terms/a.csv, terms/b.csv",
            "--dedupe-rule",
            "normalized form",
            "--excluded-prior",
            "known rows",
            "--candidate-rule",
            "all-source exact-center",
        ]
    )
    values = scaffold.scaffold_values(args)
    text = scaffold.render_template(
        "- source term files: `[list]`;\n"
        "- dedupe rule: `[rule]`;\n"
        "- excluded prior rows/forms: `[list]`.\n"
        "| Candidate selection rule | `[rule]` |",
        values,
    )

    assert "- source term files: `terms/a.csv, terms/b.csv`;" in text
    assert "- dedupe rule: `normalized form`;" in text
    assert "- excluded prior rows/forms: `known rows`." in text
    assert "| Candidate selection rule | `all-source exact-center` |" in text


def test_main_refuses_to_overwrite_without_force(tmp_path) -> None:
    output = tmp_path / "study.md"
    output.write_text("keep me", encoding="utf-8")

    code = scaffold.main(["--name", "demo", "--out", str(output)])

    assert code == 1
    assert output.read_text(encoding="utf-8") == "keep me"


def test_main_requires_name_or_profile(tmp_path) -> None:
    output = tmp_path / "study.md"

    code = scaffold.main(["--out", str(output)])

    assert code == 1
    assert not output.exists()


def test_main_writes_scaffold_with_force(tmp_path) -> None:
    output = tmp_path / "study.md"

    code = scaffold.main(["--name", "demo", "--out", str(output), "--force"])

    assert code == 0
    assert "Study name | `demo`" in output.read_text(encoding="utf-8")


def test_profile_values_populate_lane_defaults() -> None:
    parser = scaffold.build_parser()
    args = parser.parse_args(["--profile", "compound_extension_prospective"])

    values = scaffold.scaffold_values(args)

    assert values["name"] == "compound_extension_prospective"
    assert values["language"] == "hebrew"
    assert values["skip_range"] == "2..100"
    assert values["min_normalized_length"] == "5"
    assert "configs/example_oshb_wlc.toml" in values["config_path_lines"]
    assert "predeclared compound-extension target list" in values["source_term_files"]


def test_profile_values_can_be_overridden() -> None:
    parser = scaffold.build_parser()
    args = parser.parse_args(
        [
            "--profile",
            "gog_magog_pair_controls",
            "--name",
            "gog_magog_custom",
            "--skip-range",
            "2..250",
        ]
    )

    values = scaffold.scaffold_values(args)

    assert values["name"] == "gog_magog_custom"
    assert values["skip_range"] == "2..250"
    assert values["direction"] == "both"


def test_profile_listing_includes_current_lanes() -> None:
    listing = scaffold.profile_listing(scaffold.load_profiles())

    assert "greek_surface_new_terms" in listing
    assert "hebrew_modern_geopolitical_presence" in listing
    assert "compound_extension_prospective" in listing


def test_scaffold_command_uses_profile_id() -> None:
    parser = scaffold.build_parser()
    args = parser.parse_args(["--profile", "local_terms_negative_appendix"])
    values = scaffold.scaffold_values(args)

    command = scaffold.scaffold_command(values, profile_id=args.profile)

    assert "--profile local_terms_negative_appendix" in command
    assert "docs/LOCAL_TERMS_NEGATIVE_APPENDIX_PREREGISTRATION.md" in command


def test_profile_scaffold_quotes_settings_with_spaces() -> None:
    parser = scaffold.build_parser()
    args = parser.parse_args(["--profile", "compound_extension_prospective"])
    values = scaffold.scaffold_values(args)

    text = scaffold.render_template(
        "--setting controls=[control budget] \\\n"
        "--setting correction=[method] \\",
        values,
    )

    assert "--setting 'controls=5000 shuffled-term and 5000 random controls per registered target'" in text
    assert "--setting correction=benjamini_hochberg_across_all_registered_compound_targets" in text
