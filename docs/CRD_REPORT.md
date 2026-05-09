# CRD Report

Status: generated from the Centered-Relevance Density matrix.

## Reproduce

```bash
python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --resume
python3 -m scripts.build_crd_comparison
```

## Summary

- density rows: 4
- term/control comparison rows: 1
- edition summary rows: 4
- classifier agreement rows: 0
- manifest status: completed

## Bible vs Secular Controls

| Classifier | Term | Bible max | Secular max | Ratio | Exceeds secular max |
| --- | --- | ---: | ---: | ---: | --- |
| deterministic | `EXAMPLE_TERM` | 0 | 0 |  | false |

## Read

- CRD is a density screen, not a claim promotion engine.
- Deterministic mode only reports locked exact dictionary matches.
- LLM and parallel modes require audit-log review before interpretation.
- A populated production dictionary should be locked in a new preregistration before substantive runs.
