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
| `ODYSSEY` | `ναοσ` (naos) | 13 | 5 | 8 | 0 |
| `ILIAD` | `αιμα` (aima) | 12 | 4 | 8 | 0 |
| `HERODOTUS` | `αιμα` (aima) | 11 | 4 | 7 | 0 |
| `ILIAD` | `ναοσ` (naos) | 9 | 6 | 3 | 0 |
| `HERODOTUS` | `ναοσ` (naos) | 8 | 4 | 4 | 0 |
| `HERODOTUS` | `αμην` (amen) | 6 | 3 | 3 | 0 |
| `ILIAD` | `αμην` (amen) | 5 | 2 | 3 | 0 |
| `ILIAD` | `υιοσ` (uios) | 4 | 2 | 2 | 0 |
| `ODYSSEY` | `αιμα` (aima) | 4 | 2 | 2 | 0 |
| `ODYSSEY` | `υιοσ` (uios) | 4 | 4 | 0 | 0 |
| `HERODOTUS` | `αδησ` (ades) | 3 | 3 | 0 | 0 |
| `HERODOTUS` | `θεοσ` (theos) | 3 | 2 | 1 | 0 |
| `HERODOTUS` | `λεων` (leon) | 3 | 0 | 3 | 0 |
| `ILIAD` | `αδαμ` (adam) | 3 | 3 | 0 | 0 |
| `ILIAD` | `αδησ` (ades) | 3 | 2 | 1 | 0 |
| `ILIAD` | `ρωμη` (rome) | 3 | 1 | 2 | 0 |
| `ILIAD` | `σιων` (sion) | 3 | 2 | 1 | 0 |
| `ODYSSEY` | `ελαμ` (elam) | 3 | 1 | 2 | 0 |
| `HERODOTUS` | `δοξα` (doxa; English: glory) | 2 | 0 | 2 | 0 |
| `HERODOTUS` | `ελαμ` (elam) | 2 | 0 | 2 | 0 |
| `HERODOTUS` | `ισαακ` (Isaak; English: Isaac) | 2 | 1 | 1 | 0 |
| `HERODOTUS` | `οργη` (orge) | 2 | 1 | 1 | 0 |
| `HERODOTUS` | `σαρρα` (sarra) | 2 | 1 | 1 | 0 |
| `HERODOTUS` | `τυροσ` (turos) | 2 | 1 | 1 | 0 |
| `ILIAD` | `χαραν` (charan) | 2 | 1 | 1 | 0 |
| `ODYSSEY` | `αδαμ` (adam) | 2 | 0 | 2 | 0 |
| `ODYSSEY` | `αμην` (amen) | 2 | 1 | 1 | 0 |
| `ODYSSEY` | `αμνοσ` (amnos) | 2 | 1 | 1 | 0 |
| `ODYSSEY` | `θεοσ` (theos) | 2 | 1 | 1 | 0 |
| `HERODOTUS` | `αδαμ` (adam) | 1 | 1 | 0 | 0 |
| `HERODOTUS` | `βασαν` (basan) | 1 | 1 | 0 | 0 |
| `HERODOTUS` | `δαυιδ` (dauid) | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `ελκη` (elke) | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `ηλιασ` (elias) | 1 | 1 | 0 | 0 |
| `HERODOTUS` | `καροσ` (karos) | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `κερασ` (keras) | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `μαρια` (maria) | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `νικαω` (nikao) | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `νομοσ` (nomos) | 1 | 1 | 0 | 0 |
| `HERODOTUS` | `ρωμη` (rome) | 1 | 0 | 1 | 0 |

## Read

- These controls preserve the LXX canonical prefix
  length and replace the apocrypha block with same-length non-Bible
  control text.
- A control match means the tested canonical/block boundary can generate
  comparable cross-boundary ELS rows.
- This does not answer manuscript-specific insertion order; it only tests
  whether the first boundary scan is unusual against comparable
  boundary opportunities.
