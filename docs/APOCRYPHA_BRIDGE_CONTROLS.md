# LXX Apocrypha Bridge Controls

Status: non-Bible boundary controls for the initial LXX apocrypha bridge scan.
This is not a claim report.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_controls --canonical-label LXX --canonical-config configs/example_ebible_grclxx.toml --control ILIAD=configs/nonbible_greek_perseus_iliad.toml --control ODYSSEY=configs/nonbible_greek_perseus_odyssey.toml --control HERODOTUS=configs/nonbible_greek_perseus_herodotus.toml --terms terms/theological_terms.csv --terms terms/prophetic_terms.csv --terms terms/greek_nt_claim_terms.csv --observed reports/apocrypha_bridge_candidates/bridge_candidates.csv --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/apocrypha_bridge_controls/control_summary.csv --term-out reports/apocrypha_bridge_controls/term_summary.csv --markdown-out docs/APOCRYPHA_BRIDGE_CONTROLS.md --manifest-out reports/apocrypha_bridge_controls/manifest.json
```

## Observed Bridge Baseline

- observed bridge rows: 62
- observed terms with bridge rows: 21
- observed apocrypha_to_canonical: 27
- observed canonical_to_apocrypha: 35
- non-Bible controls >= observed total: 0 of 3

## Control Summary

| Control | Bridge rows | Terms | C→A | A→C | Multi |
| --- | ---: | ---: | ---: | ---: | ---: |
| `ILIAD` | 59 | 24 | 28 | 31 | 0 |
| `ODYSSEY` | 39 | 15 | 18 | 21 | 0 |
| `HERODOTUS` | 61 | 27 | 27 | 34 | 0 |

## Top Control Terms

| Control | Term | Bridge rows | C→A | A→C | Multi |
| --- | --- | ---: | ---: | ---: | ---: |
| `ODYSSEY` | `ναοσ` | 13 | 5 | 8 | 0 |
| `ILIAD` | `αιμα` | 12 | 4 | 8 | 0 |
| `HERODOTUS` | `αιμα` | 11 | 4 | 7 | 0 |
| `ILIAD` | `ναοσ` | 9 | 6 | 3 | 0 |
| `HERODOTUS` | `ναοσ` | 8 | 4 | 4 | 0 |
| `HERODOTUS` | `αμην` | 6 | 3 | 3 | 0 |
| `ILIAD` | `αμην` | 5 | 2 | 3 | 0 |
| `ILIAD` | `υιοσ` | 4 | 2 | 2 | 0 |
| `ODYSSEY` | `αιμα` | 4 | 2 | 2 | 0 |
| `ODYSSEY` | `υιοσ` | 4 | 4 | 0 | 0 |
| `HERODOTUS` | `αδησ` | 3 | 3 | 0 | 0 |
| `HERODOTUS` | `θεοσ` | 3 | 2 | 1 | 0 |
| `HERODOTUS` | `λεων` | 3 | 0 | 3 | 0 |
| `ILIAD` | `αδαμ` | 3 | 3 | 0 | 0 |
| `ILIAD` | `αδησ` | 3 | 2 | 1 | 0 |
| `ILIAD` | `ρωμη` | 3 | 1 | 2 | 0 |
| `ILIAD` | `σιων` | 3 | 2 | 1 | 0 |
| `ODYSSEY` | `ελαμ` | 3 | 1 | 2 | 0 |
| `HERODOTUS` | `δοξα` | 2 | 0 | 2 | 0 |
| `HERODOTUS` | `ελαμ` | 2 | 0 | 2 | 0 |
| `HERODOTUS` | `ισαακ` | 2 | 1 | 1 | 0 |
| `HERODOTUS` | `οργη` | 2 | 1 | 1 | 0 |
| `HERODOTUS` | `σαρρα` | 2 | 1 | 1 | 0 |
| `HERODOTUS` | `τυροσ` | 2 | 1 | 1 | 0 |
| `ILIAD` | `χαραν` | 2 | 1 | 1 | 0 |
| `ODYSSEY` | `αδαμ` | 2 | 0 | 2 | 0 |
| `ODYSSEY` | `αμην` | 2 | 1 | 1 | 0 |
| `ODYSSEY` | `αμνοσ` | 2 | 1 | 1 | 0 |
| `ODYSSEY` | `θεοσ` | 2 | 1 | 1 | 0 |
| `HERODOTUS` | `αδαμ` | 1 | 1 | 0 | 0 |
| `HERODOTUS` | `βασαν` | 1 | 1 | 0 | 0 |
| `HERODOTUS` | `δαυιδ` | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `ελκη` | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `ηλιασ` | 1 | 1 | 0 | 0 |
| `HERODOTUS` | `καροσ` | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `κερασ` | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `μαρια` | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `νικαω` | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `νομοσ` | 1 | 1 | 0 | 0 |
| `HERODOTUS` | `ρωμη` | 1 | 0 | 1 | 0 |

## Read

- These controls preserve the LXX canonical prefix
  length and replace the apocrypha block with same-length non-Bible
  control text.
- A control match means the tested canonical/block boundary can generate
  comparable cross-boundary ELS rows.
- This does not answer manuscript-specific insertion order; it only tests
  whether the first boundary scan is unusual against comparable
  boundary opportunities.
