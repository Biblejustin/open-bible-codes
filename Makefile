CRD_REVIEWER ?= gpt-5-assisted-draft
CRD_LOCKED_BY ?= gpt-5-assisted-draft
CRD_DRAFTED_WITH ?= gpt-5
REPORT_DB ?= reports/db/open_bible_codes.duckdb
CRD_SELF_CLASSIFIED_TABLE := crd_self_surface_classified_hits
CRD_CONCEPT_CLASSIFIED_TABLE := crd_concept_surface_classified_hits
CRD_SELF_COMPARISON_DB_ARGS := $(shell test -f "$(REPORT_DB)" && echo "--db $(REPORT_DB) --classified-table $(CRD_SELF_CLASSIFIED_TABLE)")
CRD_SELF_TABLE_DB_ARGS := $(shell test -f "$(REPORT_DB)" && echo "--db $(REPORT_DB) --table $(CRD_SELF_CLASSIFIED_TABLE)")
CRD_CONCEPT_COMPARISON_DB_ARGS := $(shell test -f "$(REPORT_DB)" && echo "--db $(REPORT_DB) --classified-table $(CRD_CONCEPT_CLASSIFIED_TABLE)")
CRD_CONCEPT_TABLE_DB_ARGS := $(shell test -f "$(REPORT_DB)" && echo "--db $(REPORT_DB) --table $(CRD_CONCEPT_CLASSIFIED_TABLE)")

.PHONY: demo indexes test lint report-db crd-review-scaffold crd-review-scaffold-self crd-review-apply crd-review-check crd-check crd-deterministic crd-llm crd-parallel crd-self-surface-prepare crd-self-surface-run crd-self-surface-report crd-self-surface-queue crd-self-surface-center-word crd-self-surface-center-word-density crd-self-surface-center-word-queue crd-self-surface-center-word-packet crd-self-surface-center-word-presence crd-concept-surface-prepare crd-concept-surface-run crd-concept-surface-report crd-concept-surface-queue crd-concept-surface-center-word crd-concept-surface-center-word-density crd-concept-surface-center-word-queue crd-concept-surface-center-word-packet crd-concept-surface-center-word-presence

demo:
	python3 -m els.demo

indexes:
	python3 -m scripts.build_docs_index
	python3 -m scripts.build_protocol_index

test:
	python3 -m pytest -q

lint:
	python3 -m compileall -q els scripts tests

report-db:
	python3 -m scripts.build_report_db --skip-missing

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
