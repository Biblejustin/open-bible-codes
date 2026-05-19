import csv
import tomllib
import unittest
from pathlib import Path

from els.normalization import normalize_text


TERMS_DIR = Path("terms")
NON_TERM_METADATA_FILES = {"meaningful_constants.csv"}
ALLOW_EMPTY_TERM_FILES = {"english_seed_followup_survivors.csv"}


def term_list_paths() -> list[Path]:
    return [path for path in sorted(TERMS_DIR.glob("*.csv")) if path.name not in NON_TERM_METADATA_FILES]


def term_ids(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["term_id"] for row in csv.DictReader(handle)}


class TermListTests(unittest.TestCase):
    def test_term_lists_have_required_fields_and_unique_ids(self) -> None:
        for path in term_list_paths():
            with self.subTest(path=path):
                with path.open("r", encoding="utf-8", newline="") as handle:
                    reader = csv.DictReader(handle)
                    rows = list(reader)
                if not rows:
                    self.assertIn(path.name, ALLOW_EMPTY_TERM_FILES)
                    self.assertGreaterEqual(
                        set(reader.fieldnames or []),
                        {"term_id", "concept", "category", "language", "term"},
                    )
                    continue
                self.assertGreater(len(rows), 0)
                self.assertGreaterEqual(
                    set(rows[0]),
                    {"term_id", "concept", "category", "language", "term"},
                )
                for row in rows:
                    self.assertNotIn(None, row)
                    self.assertTrue(all(value is not None for value in row.values()))
                term_ids = [row["term_id"] for row in rows]
                self.assertEqual(len(term_ids), len(set(term_ids)))

    def test_terms_normalize_to_letters(self) -> None:
        for path in term_list_paths():
            with path.open("r", encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    with self.subTest(path=path, term_id=row["term_id"]):
                        self.assertIn(
                            row["language"],
                            {"hebrew", "greek", "michigan", "english"},
                        )
                        normalized = normalize_text(row["term"], row["language"])
                        if normalized == "":
                            self.assertIn("digits are removed", row.get("notes", ""))

    def test_meaningful_constants_schema(self) -> None:
        path = TERMS_DIR / "meaningful_constants.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

        self.assertGreaterEqual(
            set(rows[0]),
            {"constant_id", "value", "label", "category", "notes"},
        )
        values = [int(row["value"]) for row in rows]
        self.assertEqual(len(values), len(set(values)))
        self.assertGreaterEqual(set(values), {7, 12, 22, 26, 40, 42, 50, 70, 144, 666})

    def test_gematria_schemes_schema(self) -> None:
        path = TERMS_DIR / "gematria_schemes.toml"
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        schemes = data["schemes"]

        self.assertGreaterEqual(
            {scheme["scheme_id"] for scheme in schemes},
            {"hebrew_standard", "greek_standard"},
        )
        for scheme in schemes:
            with self.subTest(scheme=scheme["scheme_id"]):
                self.assertIn(scheme["language"], {"hebrew", "greek"})
                self.assertTrue(scheme["implementation"].startswith("els.gematria."))
                self.assertEqual(scheme["status"], "implemented")

    def test_prophetic_terms_include_expected_categories(self) -> None:
        path = TERMS_DIR / "prophetic_terms.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            categories = {row["category"] for row in csv.DictReader(handle)}
        self.assertGreaterEqual(
            categories,
            {
                "empires_places",
                "rulers_figures",
                "apocalyptic_symbols",
                "apocalyptic_figures",
                "judgment_terms",
                "revelation_terms",
            },
        )

    def test_greek_nt_claim_terms_include_expected_categories(self) -> None:
        path = TERMS_DIR / "greek_nt_claim_terms.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            categories = {row["category"] for row in csv.DictReader(handle)}
        self.assertGreaterEqual(
            categories,
            {
                "core_names_titles",
                "key_concepts_events",
                "people",
                "search_phrases",
                "revelation_focused",
            },
        )

    def test_user_requested_modern_and_local_terms_remain_declared(self) -> None:
        modern_ids = term_ids(TERMS_DIR / "modern_names_dates.csv")
        prophetic_ids = term_ids(TERMS_DIR / "prophetic_terms.csv")

        self.assertGreaterEqual(
            modern_ids,
            {
                "trump_h",
                "trump_g",
                "vance_h",
                "vance_g",
                "netanyahu_h",
                "netanyahu_g",
                "iran_h",
                "iran_g",
                "russia_h",
                "russia_g",
                "europe_h",
                "europe_g",
                "france_h",
                "france_g",
                "germany_h",
                "germany_g",
                "turkey_h",
                "turkey_alt_h",
                "turkey_g",
                "united_states_h",
                "united_states_g",
                "united_states_america_h",
                "united_states_america_g",
                "usa_abbrev_h",
                "usa_abbrev_g",
                "united_nations_h",
                "united_nations_g",
                "united_nations_acronym_h",
                "united_nations_acronym_g",
                "european_union_h",
                "european_union_g",
                "confederacy_h",
                "confederacy_g",
                "cowboy_h",
                "cowboy_g",
                "catering_h",
                "catering_g",
                "cowboy_catering_h",
                "cowboy_catering_g",
                "simsberry_h",
                "simsberry_g",
                "simscorner_h",
                "simscorner_g",
            },
        )
        self.assertGreaterEqual(
            prophetic_ids,
            {
                "gog_h",
                "gog_g",
                "magog_h",
                "magog_g",
            },
        )

    def test_user_requested_prime_ministers_and_roman_emperors_remain_declared(self) -> None:
        modern_ids = term_ids(TERMS_DIR / "modern_names_dates.csv")
        prophetic_ids = term_ids(TERMS_DIR / "prophetic_terms.csv")
        prime_minister_bases = (
            "david_ben_gurion",
            "moshe_sharett",
            "levi_eshkol",
            "golda_meir",
            "yitzhak_rabin_pm",
            "menachem_begin",
            "yitzhak_shamir",
            "shimon_peres_pm",
            "benjamin_netanyahu_pm",
            "ehud_barak_pm",
            "ariel_sharon_pm",
            "ehud_olmert_pm",
            "naftali_bennett",
            "yair_lapid",
        )
        roman_emperor_bases = (
            "augustus",
            "tiberius",
            "caligula",
            "claudius_emperor",
            "nero_emperor",
            "galba",
            "otho",
            "vitellius",
            "vespasian",
            "titus_emperor",
            "domitian",
            "nerva",
            "trajan",
            "hadrian",
            "antoninus_pius",
            "marcus_aurelius",
            "lucius_verus",
            "commodus",
            "pertinax",
            "didius_julianus",
            "septimius_severus",
            "caracalla",
            "geta",
            "macrinus",
            "elagabalus",
            "severus_alexander",
            "maximinus",
            "gordian_i",
            "gordian_ii",
            "pupienus",
            "balbinus",
            "gordian_iii",
            "philip_arab",
            "decius",
            "hostilian",
            "gallus",
            "aemilian",
            "valerian",
            "gallienus",
            "claudius_gothicus",
            "quintillus",
            "aurelian",
            "tacitus",
            "florian",
            "probus",
            "carus",
            "numerian",
            "carinus",
            "diocletian",
            "maximian",
            "constantius_i",
            "galerius",
            "severus_ii",
            "maxentius",
            "constantine_i",
            "maximinus_daza",
            "licinius",
        )

        self.assertGreaterEqual(
            modern_ids,
            {f"{base}_{language}" for base in prime_minister_bases for language in ("h", "g")},
        )
        self.assertGreaterEqual(
            prophetic_ids,
            {f"{base}_{language}" for base in roman_emperor_bases for language in ("h", "g")},
        )

    def test_bible_code_digest_source_audit_terms_remain_declared(self) -> None:
        bcd_ids = term_ids(TERMS_DIR / "bible_code_digest_claim_terms.csv")

        self.assertGreaterEqual(
            bcd_ids,
            {
                "bcd_yeshua_messiah_h",
                "bcd_messiah_yeshua_h",
                "bcd_who_like_god_h",
                "bcd_david_king_h",
                "bcd_war_h",
                "bcd_barack_obama_h",
                "bcd_shimon_peres_h",
                "bcd_global_economic_crisis_h",
                "bcd_hurricane_katrina_h",
                "bcd_muhammad_h",
            },
        )

    def test_cri_critique_stress_terms_remain_declared(self) -> None:
        cri_ids = term_ids(TERMS_DIR / "cri_els_critique_terms.csv")

        self.assertGreaterEqual(
            cri_ids,
            {
                "cri_rabin_h",
                "cri_robin_h",
                "cri_hitler_h",
                "cri_aids_h",
                "cri_allah_h",
                "cri_muhammad_h",
                "cri_false_messiah_h",
                "cri_cri_yes_e",
            },
        )

    def test_thewordnotes_source_audit_terms_remain_declared(self) -> None:
        twn_ids = term_ids(TERMS_DIR / "thewordnotes_els_claim_terms.csv")

        self.assertGreaterEqual(
            twn_ids,
            {
                "twn_yeshua_shmi_h",
                "twn_yeshua_yakhol_h",
                "twn_sadat_h",
                "twn_hitler_h",
                "twn_french_revolution_h",
                "twn_aaron_h",
                "twn_caiaphas_h",
                "twn_atonement_lamb_h",
                "twn_received_text_g",
            },
        )

    def test_cosmic_codes_source_audit_terms_remain_declared(self) -> None:
        cc_ids = term_ids(TERMS_DIR / "cosmic_codes_claim_terms.csv")

        self.assertGreaterEqual(
            cc_ids,
            {
                "cc_torah_h",
                "cc_israel_h",
                "cc_tamarisk_h",
                "cc_hitler_h",
                "cc_auschwitz_h",
                "cc_eichmann_h",
                "cc_yeshua_shmi_h",
                "cc_yeshua_strong_name_h",
                "cc_caiaphas_h",
                "cc_john_h",
                "cc_hallelujah_h",
                "cc_hallelujah_g",
                "cc_hallelujah_e",
                "cc_rabin_h",
            },
        )

    def test_mark_tabata_isaiah53_source_audit_terms_remain_declared(self) -> None:
        mt_ids = term_ids(TERMS_DIR / "mark_tabata_isaiah53_claim_terms.csv")

        self.assertGreaterEqual(
            mt_ids,
            {
                "mt_yeshua_shmi_h",
                "mt_messiah_h",
                "mt_caiaphas_h",
                "mt_john_h",
                "mt_mary_h",
                "mt_cross_h",
                "mt_pierce_h",
                "mt_atonement_lamb_h",
                "mt_judas_absence_h",
            },
        )

    def test_bible_and_science_source_audit_terms_remain_declared(self) -> None:
        bns_ids = term_ids(TERMS_DIR / "bible_and_science_codes_terms.csv")

        self.assertGreaterEqual(
            bns_ids,
            {
                "bns_koran_e",
                "bns_moby_dick_e",
                "bns_no_god_e",
                "bns_god_dead_e",
                "bns_aleppo_codex_e",
                "bns_leningrad_codex_e",
                "bns_4q_samuel_e",
                "bns_esther_yhwh_h",
                "bns_sheshach_h",
                "bns_leb_kamai_h",
                "bns_nero_caesar_666_h",
                "bns_nero_caesar_616_h",
                "bns_eliezer_h",
                "bns_jesus_g",
            },
        )

    def test_religions_wiki_source_audit_terms_remain_declared(self) -> None:
        rw_ids = term_ids(TERMS_DIR / "religions_wiki_scriptural_codes_terms.csv")

        self.assertGreaterEqual(
            rw_ids,
            {
                "rw_torah_code_e",
                "rw_war_and_peace_e",
                "rw_moby_dick_e",
                "rw_miracle_nineteen_e",
                "rw_rashad_khalifa_e",
                "rw_gematria_e",
                "rw_theomatics_e",
                "rw_chinese_characters_e",
                "rw_multiple_comparisons_e",
                "rw_texas_sharpshooter_e",
                "rw_apophenia_e",
                "rw_brendan_mckay_e",
                "rw_dror_bar_natan_e",
            },
        )

    def test_bible_codes_org_source_audit_terms_remain_declared(self) -> None:
        bco_ids = term_ids(TERMS_DIR / "bible_codes_org_claim_terms.csv")

        self.assertGreaterEqual(
            bco_ids,
            {
                "bco_bible_code_e",
                "bco_matrix_slide_e",
                "bco_picture_bible_code_e",
                "bco_john_3_16_e",
                "bco_gate_e",
                "bco_lane_e",
                "bco_burning_bush_e",
                "bco_i_am_yeshua_e",
                "bco_creation_code_e",
                "bco_mene_tekel_e",
                "bco_cherub_code_e",
                "bco_israel_acrostic_e",
                "bco_names_code_e",
                "bco_kjv_bible_code_e",
                "bco_swine_flu_e",
                "bco_twelve_comets_e",
                "bco_textual_variants_e",
            },
        )

    def test_additional_screening_cohorts_remain_declared(self) -> None:
        narrative_ids = term_ids(TERMS_DIR / "biblical_narrative_names.csv")
        prophet_ids = term_ids(TERMS_DIR / "biblical_prophets_cohort.csv")
        eschatology_ids = term_ids(TERMS_DIR / "eschatology_expanded_terms.csv")
        isaiah53_ids = term_ids(TERMS_DIR / "isaiah53_servant_cohort.csv")
        tabernacle_ids = term_ids(TERMS_DIR / "tabernacle_temple_terms.csv")
        metals_ids = term_ids(TERMS_DIR / "daniel_statue_metals.csv")
        anno_mundi_ids = term_ids(TERMS_DIR / "hebrew_anno_mundi_years.csv")
        disaster_war_ids = term_ids(TERMS_DIR / "modern_disaster_war_terms.csv")
        maccabean_ids = term_ids(TERMS_DIR / "maccabean_apocrypha_names.csv")
        theological_ids = term_ids(TERMS_DIR / "theological_terms.csv")

        self.assertGreaterEqual(
            narrative_ids,
            {
                "narrative_joshua_h",
                "narrative_joshua_g",
                "narrative_esther_h",
                "narrative_samuel_h",
                "narrative_mary_magdalene_g",
                "narrative_caiaphas_g",
            },
        )
        self.assertGreaterEqual(
            prophet_ids,
            {
                "prophet_isaiah_h",
                "prophet_jeremiah_g",
                "prophet_hosea_h",
                "prophet_jonah_g",
                "prophet_malachi_h",
            },
        )
        self.assertGreaterEqual(
            eschatology_ids,
            {
                "esch_antichrist_g",
                "esch_rapture_g",
                "esch_666_h",
                "esch_666_stigma_g",
                "esch_number_of_beast_g",
                "esch_end_h",
            },
        )
        self.assertGreaterEqual(
            isaiah53_ids,
            {
                "isa53_transgression_h",
                "isa53_iniquity_g",
                "isa53_wound_h",
                "isa53_lamb_g",
                "isa53_grave_h",
            },
        )
        self.assertGreaterEqual(
            tabernacle_ids,
            {
                "tabernacle_mishkan_h",
                "tabernacle_ark_g",
                "tabernacle_mercy_seat_h",
                "tabernacle_holy_of_holies_g",
            },
        )
        self.assertGreaterEqual(
            metals_ids,
            {
                "daniel_gold_h",
                "daniel_silver_g",
                "daniel_bronze_h",
                "daniel_iron_g",
                "daniel_clay_h",
            },
        )
        self.assertGreaterEqual(
            anno_mundi_ids,
            {
                "am_5708_compact_h",
                "am_5727_full_h",
                "am_5733_compact_h",
                "am_5790_full_h",
                "am_5793_compact_h",
            },
        )
        self.assertGreaterEqual(
            disaster_war_ids,
            {
                "disaster_earthquake_h",
                "disaster_cancer_g",
                "war_ww1_h",
                "war_six_day_h",
                "war_yom_kippur_g",
            },
        )
        self.assertGreaterEqual(
            maccabean_ids,
            {
                "macc_antiochus_h",
                "macc_mattathias_g",
                "macc_judah_maccabee_h",
                "macc_tobit_g",
                "macc_holofernes_h",
            },
        )
        self.assertGreaterEqual(
            theological_ids,
            {
                "el_shaddai_h",
                "el_elyon_h",
                "yhwh_tzevaot_h",
                "sabaoth_g",
                "ruach_hakodesh_h",
                "holy_spirit_g",
                "trinity_g",
                "father_g",
            },
        )


if __name__ == "__main__":
    unittest.main()
