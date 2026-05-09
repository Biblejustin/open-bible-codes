.PHONY: demo indexes test

demo:
	python3 -m els.demo

indexes:
	python3 -m scripts.build_docs_index
	python3 -m scripts.build_protocol_index

test:
	python3 -m pytest -q
