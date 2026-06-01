CRD_REVIEWER ?= gpt-5-assisted-draft
CRD_LOCKED_BY ?= gpt-5-assisted-draft
CRD_DRAFTED_WITH ?= gpt-5
REPORT_DB ?= reports/db/open_bible_codes.duckdb
CRD_SELF_CLASSIFIED_TABLE := crd_self_surface_classified_hits
CRD_CONCEPT_CLASSIFIED_TABLE := crd_concept_surface_classified_hits
DYNAMIC_FULL_SPAN_HITS_TABLE := dynamic_skip_focus_full_span_exported_hits
CRD_SELF_COMPARISON_DB_ARGS := $(shell test -f "$(REPORT_DB)" && echo "--db $(REPORT_DB) --classified-table $(CRD_SELF_CLASSIFIED_TABLE)")
CRD_SELF_TABLE_DB_ARGS := $(shell test -f "$(REPORT_DB)" && echo "--db $(REPORT_DB) --table $(CRD_SELF_CLASSIFIED_TABLE)")
CRD_CONCEPT_COMPARISON_DB_ARGS := $(shell test -f "$(REPORT_DB)" && echo "--db $(REPORT_DB) --classified-table $(CRD_CONCEPT_CLASSIFIED_TABLE)")
CRD_CONCEPT_TABLE_DB_ARGS := $(shell test -f "$(REPORT_DB)" && echo "--db $(REPORT_DB) --table $(CRD_CONCEPT_CLASSIFIED_TABLE)")
DYNAMIC_FULL_SPAN_HITS_DB_ARGS := $(shell test -f "$(REPORT_DB)" && echo "--db $(REPORT_DB) --hits-table $(DYNAMIC_FULL_SPAN_HITS_TABLE)")
CIPHER_LAYERED_PLAIN_HITS ?= reports/cipher_layered_pairs/plain_mt_wlc_hits.csv
CIPHER_LAYERED_PLAIN_CONFIG ?= configs/example_oshb_wlc.toml
CIPHER_LAYERED_PLAIN_CORPUS ?= MT_WLC
CIPHER_LAYERED_TERMS ?= terms/hebrew_atbash_audit_terms.csv
CIPHER_LAYERED_CIPHER_HITS ?= reports/hebrew_atbash_audit/MT_WLC_hits.csv
COHORT_CLUSTER_OCCURRENCES ?= reports/centered_occurrence_index/centered_occurrences.csv
COHORT_CLUSTER_TERMS ?= terms/biblical_tribes.csv
COHORT_CLUSTER_WINDOW_WORDS ?= 50
COHORT_CLUSTER_MIN_DISTINCT ?= 2
COHORT_CLUSTER_CORPUS_CONFIGS ?= --corpus-config MT_WLC=configs/example_oshb_wlc.toml --corpus-config UXLC=configs/example_uxlc.toml --corpus-config EBIBLE_WLC=configs/example_ebible_hebwlc.toml --corpus-config MAM=configs/example_mam.toml --corpus-config UHB=configs/example_uhb.toml --corpus-config LXX=configs/example_ebible_grclxx.toml --corpus-config KJV=configs/example_ebible_engkjv.toml --corpus-config KJVA=configs/example_ebible_engkjv_apocrypha.toml --corpus-config TR_NT=configs/example_ebible_grctr.toml --corpus-config SBLGNT=configs/example_sblgnt.toml --corpus-config BYZ_NT=configs/example_ebible_grcmt.toml --corpus-config TCG_NT=configs/example_ebible_grctcgnt.toml --corpus-config HEB_PBY_AHAD_HAAM=configs/nonbible_hebrew_pby_ahad_haam.toml --corpus-config HEB_PBY_BIALIK=configs/nonbible_hebrew_pby_bialik.toml --corpus-config HEB_PBY_BRENNER=configs/nonbible_hebrew_pby_brenner.toml --corpus-config ENG_PG_SHAKESPEARE=configs/nonbible_english_pg_shakespeare.toml

.PHONY: demo indexes test lint fast-validate release-ready public-release-check local-data-doc-check protocol-files corpus-configs term-files script-tests check-script-tests check-script-wiring study-mapping-schemas public-reader-package-check expanded-strata-tooling-check expanded-strata-postprocess real-report public-reader-package report-db dynamic-full-span-hit-findings notable-passage-gaps thematic-chapter-absence match-strata-index boundary-alignment chapter-position-bias direction-asymmetry canonical-first-summary cross-skip-summary review-flag-summary hebrew-atbash-audit hebrew-albam-audit word-edge-pattern-audit word-skip-term-audit matrix-cluster-candidates matrix-cluster-control-summary cipher-layered-plain-hits cipher-layered-pairs cohort-cluster-density crd-review-scaffold crd-review-scaffold-self crd-review-apply crd-review-check crd-check crd-deterministic crd-llm crd-parallel crd-broad-screening-findings crd-center-word-findings crd-self-surface-prepare crd-self-surface-run crd-self-surface-report crd-self-surface-queue crd-self-surface-center-word crd-self-surface-center-word-density crd-self-surface-center-word-queue crd-self-surface-center-word-packet crd-self-surface-center-word-presence crd-concept-surface-prepare crd-concept-surface-run crd-concept-surface-report crd-concept-surface-queue crd-concept-surface-center-word crd-concept-surface-center-word-density crd-concept-surface-center-word-queue crd-concept-surface-center-word-packet crd-concept-surface-center-word-presence

demo:
	python3 -m els.demo

indexes:
	python3 -m scripts.build_docs_index
	python3 -m scripts.build_protocol_index

test:
	python3 -m pytest -q

lint:
	python3 -m compileall -q els scripts tests

fast-validate: test indexes
	git diff --check
	python3 -m scripts.check_public_release_hygiene --allow-dirty
	python3 -m scripts.check_expanded_strata_tooling
	python3 -m scripts.check_clean_lock_results_summary_doc
	python3 -m scripts.check_project_findings_overview_doc
	python3 -m scripts.check_real_report_run_doc
	python3 -m scripts.check_consolidated_findings_doc
	python3 -m scripts.check_claim_catalog_doc
	python3 -m scripts.check_final_report_assembly_docs
	python3 -m scripts.check_final_report_highlights_doc
	python3 -m scripts.check_strongest_candidate_deep_dive_doc
	python3 -m scripts.check_prospective_lane_status_doc
	python3 -m scripts.check_study_lock_manifests_doc
	python3 -m scripts.check_prospective_study_readiness_doc
	python3 -m scripts.check_prospective_study_next_lock_doc
	python3 -m scripts.check_wrr_public_handoff_docs
	python3 -m scripts.check_cities_public_handoff_docs
	python3 -m scripts.check_kjva_public_handoff_docs
	python3 -m scripts.check_wrr_no_input_handoff_status_doc
	python3 -m scripts.check_cities_no_input_handoff_status_doc
	python3 -m scripts.check_kjva_no_input_handoff_status_doc
	python3 -m scripts.check_public_claim_language
	$(MAKE) protocol-files
	$(MAKE) corpus-configs
	$(MAKE) term-files
	$(MAKE) script-tests
	$(MAKE) check-script-tests
	$(MAKE) check-script-wiring
	$(MAKE) study-mapping-schemas
	$(MAKE) public-reader-package-check
	$(MAKE) local-data-doc-check

release-ready: fast-validate public-release-check

public-release-check:
	python3 -m scripts.check_public_release_hygiene
	python3 -m scripts.check_expanded_strata_tooling
	python3 -m scripts.check_doc_command_references
	python3 -m scripts.check_clean_lock_results_summary_doc
	python3 -m scripts.check_project_findings_overview_doc
	python3 -m scripts.check_real_report_run_doc
	python3 -m scripts.check_consolidated_findings_doc
	python3 -m scripts.check_claim_catalog_doc
	python3 -m scripts.check_final_report_assembly_docs
	python3 -m scripts.check_final_report_highlights_doc
	python3 -m scripts.check_strongest_candidate_deep_dive_doc
	python3 -m scripts.check_prospective_lane_status_doc
	python3 -m scripts.check_study_lock_manifests_doc
	python3 -m scripts.check_prospective_study_readiness_doc
	python3 -m scripts.check_prospective_study_next_lock_doc
	python3 -m scripts.check_wrr_public_handoff_docs
	python3 -m scripts.check_cities_public_handoff_docs
	python3 -m scripts.check_kjva_public_handoff_docs
	python3 -m scripts.check_wrr_no_input_handoff_status_doc
	python3 -m scripts.check_cities_no_input_handoff_status_doc
	python3 -m scripts.check_kjva_no_input_handoff_status_doc
	python3 -m scripts.check_public_claim_language
	$(MAKE) protocol-files
	$(MAKE) corpus-configs
	$(MAKE) term-files
	$(MAKE) script-tests
	$(MAKE) check-script-tests
	$(MAKE) check-script-wiring
	$(MAKE) study-mapping-schemas
	$(MAKE) public-reader-package-check

local-data-doc-check:
	python3 -m scripts.check_doc_command_references --check-local-data

protocol-files:
	python3 -m scripts.check_protocol_files

corpus-configs:
	python3 -m scripts.check_corpus_configs

term-files:
	python3 -m scripts.check_term_files

script-tests:
	python3 -m scripts.check_script_tests

check-script-tests:
	python3 -m scripts.check_check_script_tests

check-script-wiring:
	python3 -m scripts.check_check_script_wiring

study-mapping-schemas:
	python3 -m scripts.validate_study_mapping_schemas
	python3 -m scripts.check_study_mapping_term_ids
	python3 -m scripts.check_wrr_manual_decision_records
	python3 -m scripts.check_cities_ocr_page_review_decisions
	python3 -m scripts.check_cities_source_row_lock_decision_records
	python3 -m scripts.check_cities_source_transcription_decision_records

public-reader-package-check:
	python3 -m scripts.build_public_reader_package --out-dir /tmp/edls_public_reader_package_check
	python3 -m scripts.check_public_reader_package --package-dir /tmp/edls_public_reader_package_check

expanded-strata-tooling-check:
	python3 -m scripts.check_expanded_strata_tooling

expanded-strata-postprocess: match-strata-index boundary-alignment chapter-position-bias direction-asymmetry canonical-first-summary cross-skip-summary review-flag-summary cohort-cluster-density

real-report:
	python3 -m scripts.run_protocol protocols/real_report_run.toml --resume

public-reader-package:
	python3 -m scripts.build_public_reader_package

report-db:
	python3 -m scripts.build_report_db --skip-missing

dynamic-full-span-hit-findings:
	python3 -m scripts.summarize_dynamic_span_hits $(DYNAMIC_FULL_SPAN_HITS_DB_ARGS)

notable-passage-gaps:
	python3 -m scripts.run_protocol protocols/notable_passage_gaps.toml --resume

thematic-chapter-absence:
	python3 -m scripts.run_protocol protocols/thematic_chapter_absence.toml --resume

match-strata-index:
	python3 -m scripts.run_protocol protocols/match_strata_index.toml --resume

boundary-alignment:
	python3 -m scripts.run_protocol protocols/boundary_alignment.toml --resume

chapter-position-bias:
	python3 -m scripts.run_protocol protocols/chapter_position_bias.toml --resume

direction-asymmetry:
	python3 -m scripts.run_protocol protocols/direction_asymmetry.toml --resume

canonical-first-summary:
	python3 -m scripts.run_protocol protocols/canonical_first_summary.toml --resume

cross-skip-summary:
	python3 -m scripts.run_protocol protocols/cross_skip_summary.toml --resume

review-flag-summary:
	python3 -m scripts.run_protocol protocols/review_flag_summary.toml --resume

hebrew-atbash-audit:
	python3 -m scripts.run_protocol protocols/hebrew_atbash_audit.toml --resume

hebrew-albam-audit:
	python3 -m scripts.run_protocol protocols/hebrew_albam_audit.toml --resume

word-edge-pattern-audit:
	python3 -m scripts.run_protocol protocols/word_edge_pattern_audit.toml --resume

word-skip-term-audit:
	python3 -m scripts.run_protocol protocols/word_skip_term_audit.toml --resume

matrix-cluster-candidates:
	python3 -m scripts.run_protocol protocols/matrix_cluster_candidates.toml --resume

matrix-cluster-control-summary:
	python3 -m scripts.run_protocol protocols/matrix_cluster_control_summary.toml --resume

cipher-layered-plain-hits:
	python3 -m scripts.search_transformed_els --config "$(CIPHER_LAYERED_PLAIN_CONFIG)" --corpus-label "$(CIPHER_LAYERED_PLAIN_CORPUS)" --transform plain --terms "$(CIPHER_LAYERED_TERMS)" --min-skip 2 --max-skip 100 --direction both --max-hits-per-term 200 --out "$(CIPHER_LAYERED_PLAIN_HITS)"

cipher-layered-pairs: cipher-layered-plain-hits
	python3 -m scripts.build_cipher_layered_pairs --plain-hits "$(CIPHER_LAYERED_PLAIN_HITS)" --cipher-hits "$(CIPHER_LAYERED_CIPHER_HITS)" --out reports/cipher_layered_pairs/pairs.csv --summary-out reports/cipher_layered_pairs/summary.csv --manifest-out reports/cipher_layered_pairs/manifest.json

cohort-cluster-density:
	python3 -m scripts.build_cohort_cluster_density --occurrences "$(COHORT_CLUSTER_OCCURRENCES)" --cohort "$(COHORT_CLUSTER_TERMS)" --window-words "$(COHORT_CLUSTER_WINDOW_WORDS)" --min-distinct-terms "$(COHORT_CLUSTER_MIN_DISTINCT)" $(COHORT_CLUSTER_CORPUS_CONFIGS) --out reports/cohort_cluster_density/windows.csv --summary-out reports/cohort_cluster_density/summary.csv --markdown-out docs/COHORT_CLUSTER_DENSITY_AUDIT.md --manifest-out reports/cohort_cluster_density/manifest.json

crd-review-scaffold:
	python3 -m scripts.scaffold_crd_relevance_dictionary --term-file terms/gog_magog_pair_prospective_terms.csv --out reports/crd/relevance_dictionary_draft.toml --queue-out reports/crd/relevance_review_queue.csv --locked-by "$(CRD_LOCKED_BY)" --reviewer "$(CRD_REVIEWER)" --drafted-with "$(CRD_DRAFTED_WITH)"

crd-review-scaffold-self:
	python3 -m scripts.scaffold_crd_relevance_dictionary --term-file terms/gog_magog_pair_prospective_terms.csv --out reports/crd/relevance_dictionary_draft.toml --queue-out reports/crd/relevance_review_queue.csv --locked-by "$(CRD_LOCKED_BY)" --reviewer "$(CRD_REVIEWER)" --drafted-with "$(CRD_DRAFTED_WITH)" --seed-surface-term

crd-review-apply:
	python3 -m scripts.apply_crd_relevance_review --queue reports/crd/relevance_review_queue.csv --out reports/crd/relevance_dictionary_reviewed.toml --locked-by "$(CRD_LOCKED_BY)" --reviewer "$(CRD_REVIEWER)" --drafted-with "$(CRD_DRAFTED_WITH)"

crd-review-check:
	python3 -m scripts.check_crd_relevance_dictionary --dictionary reports/crd/relevance_dictionary_reviewed.toml --term-file terms/gog_magog_pair_prospective_terms.csv --require-reviewed

crd-check:
	python3 -m scripts.check_crd_relevance_dictionary --dictionary terms/relevance_dictionary.toml --term-file terms/gog_magog_pair_prospective_terms.csv --expected-sha256 "a6406048b9953ca50715d99100994b9065394d9db31b35867666d365a3bd0f99" --require-reviewed

crd-deterministic:
	python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --classifier-mode deterministic --resume
	python3 -m scripts.build_crd_comparison

crd-llm:
	python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --classifier-mode llm --resume
	python3 -m scripts.build_crd_comparison

crd-parallel:
	python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --classifier-mode parallel --resume
	python3 -m scripts.build_crd_comparison

crd-center-word-findings:
	python3 -m scripts.build_crd_center_word_findings

crd-broad-screening-findings:
	python3 -m scripts.build_crd_broad_screening_findings

crd-self-surface-prepare:
	python3 -m scripts.prepare_crd_self_surface_run

crd-self-surface-run:
	python3 -m scripts.run_crd_density reports/crd_self_surface/protocol.toml --classifier-mode deterministic --resume

crd-self-surface-report:
	python3 -m scripts.build_crd_comparison --density-matrix reports/crd_self_surface/density_matrix.csv --classified-hits reports/crd_self_surface/classified_hits.csv --manifest reports/crd_self_surface/manifest.json --out-dir reports/crd_self_surface --markdown-out reports/crd_self_surface/CRD_SELF_SURFACE_REPORT.md $(CRD_SELF_COMPARISON_DB_ARGS)

crd-self-surface-queue:
	python3 -m scripts.build_crd_review_queue --summary reports/crd_self_surface/bible_vs_control_summary.csv --classified-hits reports/crd_self_surface/classified_hits.csv --output reports/crd_self_surface/review_queue.csv $(CRD_SELF_TABLE_DB_ARGS)

crd-self-surface-center-word:
	python3 -m scripts.filter_crd_classified_hits --classified-hits reports/crd_self_surface/classified_hits.csv --output reports/crd_self_surface/center_word_hits.csv --corpus-class bible --is-relevant true --surface-match-scope center_word $(CRD_SELF_TABLE_DB_ARGS)

crd-self-surface-center-word-density:
	python3 -m scripts.build_crd_scope_density --base-density-matrix reports/crd_self_surface/density_matrix.csv --classified-hits reports/crd_self_surface/classified_hits.csv --surface-match-scope center_word --matrix-out reports/crd_self_surface/center_word_density_matrix.csv --summary-out reports/crd_self_surface/center_word_bible_vs_control_summary.csv $(CRD_SELF_TABLE_DB_ARGS)

crd-self-surface-center-word-queue:
	python3 -m scripts.build_crd_review_queue --summary reports/crd_self_surface/center_word_bible_vs_control_summary.csv --classified-hits reports/crd_self_surface/center_word_hits.csv --output reports/crd_self_surface/center_word_review_queue.csv

crd-self-surface-center-word-packet:
	python3 -m scripts.build_crd_review_packet --queue reports/crd_self_surface/center_word_review_queue.csv --output reports/crd_self_surface/center_word_review_packet.md --title "CRD Self-Surface Exact Center-Word Review Packet"

crd-self-surface-center-word-presence:
	python3 -m scripts.build_crd_center_word_presence --center-word-hits reports/crd_self_surface/center_word_hits.csv --summary reports/crd_self_surface/center_word_bible_vs_control_summary.csv --output reports/crd_self_surface/center_word_presence.csv --markdown-out reports/crd_self_surface/center_word_presence.md

crd-concept-surface-prepare:
	python3 -m scripts.prepare_crd_self_surface_run --seed-mode concept --out-dir reports/crd_concept_surface

crd-concept-surface-run:
	python3 -m scripts.run_crd_density reports/crd_concept_surface/protocol.toml --classifier-mode deterministic --resume

crd-concept-surface-report:
	python3 -m scripts.build_crd_comparison --density-matrix reports/crd_concept_surface/density_matrix.csv --classified-hits reports/crd_concept_surface/classified_hits.csv --manifest reports/crd_concept_surface/manifest.json --out-dir reports/crd_concept_surface --markdown-out reports/crd_concept_surface/CRD_CONCEPT_SURFACE_REPORT.md $(CRD_CONCEPT_COMPARISON_DB_ARGS)

crd-concept-surface-queue:
	python3 -m scripts.build_crd_review_queue --summary reports/crd_concept_surface/bible_vs_control_summary.csv --classified-hits reports/crd_concept_surface/classified_hits.csv --output reports/crd_concept_surface/review_queue.csv $(CRD_CONCEPT_TABLE_DB_ARGS)

crd-concept-surface-center-word:
	python3 -m scripts.filter_crd_classified_hits --classified-hits reports/crd_concept_surface/classified_hits.csv --output reports/crd_concept_surface/center_word_hits.csv --corpus-class bible --is-relevant true --surface-match-scope center_word $(CRD_CONCEPT_TABLE_DB_ARGS)

crd-concept-surface-center-word-density:
	python3 -m scripts.build_crd_scope_density --base-density-matrix reports/crd_concept_surface/density_matrix.csv --classified-hits reports/crd_concept_surface/classified_hits.csv --surface-match-scope center_word --matrix-out reports/crd_concept_surface/center_word_density_matrix.csv --summary-out reports/crd_concept_surface/center_word_bible_vs_control_summary.csv $(CRD_CONCEPT_TABLE_DB_ARGS)

crd-concept-surface-center-word-queue:
	python3 -m scripts.build_crd_review_queue --summary reports/crd_concept_surface/center_word_bible_vs_control_summary.csv --classified-hits reports/crd_concept_surface/center_word_hits.csv --output reports/crd_concept_surface/center_word_review_queue.csv

crd-concept-surface-center-word-packet:
	python3 -m scripts.build_crd_review_packet --queue reports/crd_concept_surface/center_word_review_queue.csv --output reports/crd_concept_surface/center_word_review_packet.md --title "CRD Concept-Surface Exact Center-Word Review Packet"

crd-concept-surface-center-word-presence:
	python3 -m scripts.build_crd_center_word_presence --center-word-hits reports/crd_concept_surface/center_word_hits.csv --summary reports/crd_concept_surface/center_word_bible_vs_control_summary.csv --output reports/crd_concept_surface/center_word_presence.csv --markdown-out reports/crd_concept_surface/center_word_presence.md
