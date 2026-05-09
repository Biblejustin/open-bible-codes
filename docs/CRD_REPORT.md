# CRD Report

Status: generated from the Centered-Relevance Density matrix.

## Reproduce

```bash
python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --resume
python3 -m scripts.build_crd_comparison
```

## Summary

- density rows: 80
- term/control comparison rows: 10
- edition summary rows: 8
- classifier agreement rows: 0
- manifest status: completed

## Bible vs Secular Controls

| Classifier | Term | Bible max | Secular max | Ratio | Exceeds secular max |
| --- | --- | ---: | ---: | ---: | --- |
| deterministic | `beast_h` | 13.3662812 | 0 |  | true |
| deterministic | `cyrus_h` | 3.3415703 | 0 |  | true |
| deterministic | `darius_h` | 9.98356871 | 0 |  | true |
| deterministic | `dragon_h` | 70.1729764 | 0 |  | true |
| deterministic | `gog_h` | 7.51853318 | 0 |  | true |
| deterministic | `horn_h` | 11.6954961 | 0 |  | true |
| deterministic | `magog_h` | 16.6392812 | 0 |  | true |
| deterministic | `prophet_h` | 40.9342362 | 0 |  | true |
| deterministic | `seal_h` | 22.5555996 | 0 |  | true |
| deterministic | `vision_h` | 31.7449179 | 0 |  | true |

## Read

- CRD is a density screen, not a claim promotion engine.
- Deterministic mode only reports locked exact dictionary matches.
- LLM and parallel modes require audit-log review before interpretation.
- Interpret results only against the dictionary and preregistration hashes recorded in the manifest.
