.PHONY: demo indexes test lint crd-review-scaffold crd-review-apply crd-review-check crd-check crd-deterministic crd-llm crd-parallel

demo:
	python3 -m els.demo

indexes:
	python3 -m scripts.build_docs_index
	python3 -m scripts.build_protocol_index

test:
	python3 -m pytest -q

lint:
	python3 -m compileall -q els scripts tests

crd-review-scaffold:
	python3 -m scripts.scaffold_crd_relevance_dictionary --term-file terms/gog_magog_pair_prospective_terms.csv --out reports/crd/relevance_dictionary_draft.toml --queue-out reports/crd/relevance_review_queue.csv

crd-review-apply:
	python3 -m scripts.apply_crd_relevance_review --queue reports/crd/relevance_review_queue.csv --out reports/crd/relevance_dictionary_reviewed.toml

crd-review-check:
	python3 -m scripts.check_crd_relevance_dictionary --dictionary reports/crd/relevance_dictionary_reviewed.toml --term-file terms/gog_magog_pair_prospective_terms.csv --require-reviewed

crd-check:
	python3 -m scripts.check_crd_relevance_dictionary --dictionary terms/relevance_dictionary.toml --term-file terms/crd_placeholder_terms.csv

crd-deterministic:
	python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --classifier-mode deterministic --resume
	python3 -m scripts.build_crd_comparison

crd-llm:
	python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --classifier-mode llm --resume
	python3 -m scripts.build_crd_comparison

crd-parallel:
	python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --classifier-mode parallel --resume
	python3 -m scripts.build_crd_comparison
