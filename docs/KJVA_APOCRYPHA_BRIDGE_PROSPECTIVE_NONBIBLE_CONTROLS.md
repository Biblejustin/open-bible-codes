# KJVA Prospective Apocrypha Bridge Controls

Status: non-Bible boundary controls for the initial KJVA Prospective apocrypha bridge scan.
This is not a claim report.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_controls --canonical-label KJVA Prospective --canonical-config configs/example_ebible_engkjv_apocrypha.toml --control SHAKESPEARE=configs/nonbible_english_pg_shakespeare.toml --control WAR_PEACE=configs/nonbible_english_pg_war_and_peace.toml --control MOBY_DICK=configs/nonbible_english_pg_moby_dick.toml --terms terms/kjv_apocrypha_bridge_prospective_terms.csv --observed reports/kjv_apocrypha_bridge_prospective/bridge_candidates.csv --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/kjv_apocrypha_bridge_prospective_nonbible_controls/control_summary.csv --term-out reports/kjv_apocrypha_bridge_prospective_nonbible_controls/term_summary.csv --markdown-out docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md --manifest-out reports/kjv_apocrypha_bridge_prospective_nonbible_controls/manifest.json
```

## Observed Bridge Baseline

- observed bridge rows: 1
- observed terms with bridge rows: 1
- observed canonical_to_apocrypha: 1
- non-Bible controls >= observed total: 1 of 3

## Control Summary

| Control | Bridge rows | Terms | C→A | A→C | Multi |
| --- | ---: | ---: | ---: | ---: | ---: |
| `SHAKESPEARE` | 0 | 0 | 0 | 0 | 0 |
| `WAR_PEACE` | 0 | 0 | 0 | 0 | 0 |
| `MOBY_DICK` | 1 | 1 | 1 | 0 | 0 |

## Top Control Terms

| Control | Term | Bridge rows | C→A | A→C | Multi |
| --- | --- | ---: | ---: | ---: | ---: |
| `MOBY_DICK` | `tobit` | 1 | 1 | 0 | 0 |

## Read

- These controls preserve the KJVA Prospective canonical prefix
  length and replace the apocrypha block with same-length non-Bible
  control text.
- A control match means the tested canonical/block boundary can generate
  comparable cross-boundary ELS rows.
- This does not answer manuscript-specific insertion order; it only tests
  whether the first boundary scan is unusual against comparable
  boundary opportunities.
