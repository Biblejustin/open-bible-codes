.PHONY: demo indexes test lint crd-deterministic crd-llm crd-parallel

demo:
	python3 -m els.demo

indexes:
	python3 -m scripts.build_docs_index
	python3 -m scripts.build_protocol_index

test:
	python3 -m pytest -q

lint:
	python3 -m compileall -q els scripts tests

crd-deterministic:
	python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --classifier-mode deterministic --resume
	python3 -m scripts.build_crd_comparison

crd-llm:
	python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --classifier-mode llm --resume
	python3 -m scripts.build_crd_comparison

crd-parallel:
	python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --classifier-mode parallel --resume
	python3 -m scripts.build_crd_comparison
