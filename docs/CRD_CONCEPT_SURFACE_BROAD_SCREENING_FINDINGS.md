# CRD Concept-Surface Broad Screening Findings

Status: local deterministic broad screening run completed at `2026-05-11T07:02:23.586783+00:00`. Raw artifacts stay under ignored `reports/crd_concept_surface/`; `classified_hits.csv` is 6.56 GB.

## Scope

This run asks a deterministic centered-relevance question: when a hidden ELS term is centered, does the visible surface context contain any locked surface spelling with the same language and same concept? It uses exact normalized dictionary matching only; no fuzzy matching, embeddings, or live interpretation are used.

The run uses the same Bible and secular-control corpus list as the CRD protocol, with `skip_range = 2..100`, `direction = both`, `min_term_length = 3`, and `max_hits_per_term = 200`.

The input term set combines all committed term CSVs except `terms/crd_placeholder_terms.csv`, deduped by first-seen `term_id`. Concept-surface means hidden `X` is centered near a committed same-concept spelling.

## Outputs

- protocol: `reports/crd_concept_surface/protocol.toml`
- preregistration: `reports/crd_concept_surface/CRD_CONCEPT_SURFACE_PREREGISTRATION.md`
- dictionary: `reports/crd_concept_surface/relevance_dictionary_concept_surface.toml`
- density matrix: `reports/crd_concept_surface/density_matrix.csv`
- classified hits: `reports/crd_concept_surface/classified_hits.csv`
- comparison report: `reports/crd_concept_surface/CRD_CONCEPT_SURFACE_REPORT.md`
- compact review queue: `reports/crd_concept_surface/review_queue.csv`
- Bible exact center-word hits: `reports/crd_concept_surface/center_word_hits.csv`
- exact center-word version presence: `reports/crd_concept_surface/center_word_presence.md`

## Reproduce

```bash
make crd-concept-surface-prepare
python3 -m scripts.run_crd_density reports/crd_concept_surface/protocol.toml --classifier-mode deterministic --resume --force-reset
make report-db
make crd-concept-surface-report
make crd-concept-surface-queue
make crd-concept-surface-center-word
make crd-concept-surface-center-word-density
make crd-concept-surface-center-word-queue
make crd-concept-surface-center-word-packet
make crd-concept-surface-center-word-presence
make crd-broad-screening-findings
make crd-center-word-findings
```

## Run Size

- density rows: 22,220
- term/control comparison rows: 3,503
- classified hit rows: 1,621,960
- corpora with output: 20
- nonzero `(term, corpus)` density rows: 13,120
- compact review queue rows: 419
- compact review queue selected terms: 50
- exact center-word review queue rows: 215
- exact center-word review queue selected terms: 50
- runtime: 8523.210 seconds
- API calls: 0
- estimated API cost: 0.0 USD

## Headline Counts

- `exceeds_secular_max = true`: 582 / 3,503 terms
- rows with secular max density = 0: 3,383 / 3,503 terms
- rows with Bible max > 0 and secular max = 0: 493 / 3,503 terms
- English exceeds: 196 / 1,451
- Greek exceeds: 153 / 947
- Hebrew exceeds: 233 / 1,105

Large numbers of secular-zero rows are review-priority flags, not automatic claim promotions. They can reflect dictionary vocabulary and control-corpus coverage.

## Surface Match Scope

Relevant classified-hit rows by scope:

- `bible.center_word`: 1,153
- `bible.center_verse`: 5,458
- `bible.span`: 2,494
- `secular_control.center_word`: 225
- `secular_control.center_verse`: 0
- `secular_control.span`: 0

Compact review queue scope:

- `center_verse`: 265
- `center_word`: 70
- `span`: 84

The exact `center_word` scope is the strictest form: the hidden term is centered directly on the visible matching or same-concept word. `center_verse` and `span` remain broader contextual flags and should be reviewed separately.

## Strongest Finite Bible-Vs-Control Ratios

| Term | Language | Bible max | Bible corpus | Secular max | Secular corpus | Ratio |
| --- | --- | ---: | --- | ---: | --- | ---: |
| `ישראל` (Yisrael; English: Israel)<br>`cc_israel_h` | hebrew | 52.6297323 | MT_WLC | 0.725114523 | HEB_PBY_AHAD_HAAM | 72.5812691 |
| `ישראל` (Yisrael; English: Israel)<br>`htp_israel_h` | hebrew | 52.6297323 | MT_WLC | 0.725114523 | HEB_PBY_AHAD_HAAM | 72.5812691 |
| `ישראל` (Yisrael; English: Israel)<br>`israel_h` | hebrew | 52.6297323 | MT_WLC | 0.725114523 | HEB_PBY_AHAD_HAAM | 72.5812691 |
| `ישראל` (Yisrael; English: Israel)<br>`twn_israel_h` | hebrew | 52.6297323 | MT_WLC | 0.725114523 | HEB_PBY_AHAD_HAAM | 72.5812691 |
| `יוסף` (ywsp; English: Joseph)<br>`cc_joseph_h` | hebrew | 11.6954961 | MT_WLC | 0.174947546 | HEB_PBY_BIALIK | 66.8514441 |
| `יוסף` (ywsp; English: Joseph)<br>`joseph_h` | hebrew | 11.6954961 | MT_WLC | 0.174947546 | HEB_PBY_BIALIK | 66.8514441 |
| `יוסף` (ywsp; English: Joseph Tribe)<br>`joseph_tribe_h` | hebrew | 11.6954961 | MT_WLC | 0.174947546 | HEB_PBY_BIALIK | 66.8514441 |
| `יוסף` (ywsp; English: Joseph)<br>`mt_joseph_h` | hebrew | 11.6954961 | MT_WLC | 0.174947546 | HEB_PBY_BIALIK | 66.8514441 |
| `Lord`<br>`eng_lord` | english | 19.2353931 | KJV | 0.739422378 | ENG_PG_SHAKESPEARE | 26.0140803 |
| `Lord`<br>`eng_lord_2` | english | 19.2353931 | KJV | 0.739422378 | ENG_PG_SHAKESPEARE | 26.0140803 |

## Strongest Bible Hits With Secular Max Zero

| Term | Language | Bible max | Bible corpus |
| --- | --- | ---: | --- |
| `יהוה` (YHWH; English: YHWH Esther Acrostic)<br>`bns_esther_yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`cc_yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`htp_yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`twn_yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `אשר` (shr; English: Asher)<br>`asher_h` | hebrew | 34.2510956 | MT_WLC |
| `יהודה` (Yehudah; English: Judah)<br>`judah_h` | hebrew | 20.8848144 | MT_WLC |
| `יהודה` (Yehudah; English: Judas Absence)<br>`mt_judas_absence_h` | hebrew | 20.8848144 | MT_WLC |
| `אדני` (Adonai; English: Lord)<br>`lord_h` | hebrew | 18.3786367 | MT_WLC |

## Exact Center-Word Subset

- Bible center-word rows: 1,153
- distinct term IDs with Bible center-word rows: 154
- exact center-word presence rows: 154
- distinct visible spellings in presence output: 90
- center-word-only summary rows: 3,503; `exceeds_secular_max = true`: 141
- Bible-positive / secular-zero center-word terms: 114
- English center-word exceeds: 27 / 1,451
- Greek center-word exceeds: 37 / 947
- Hebrew center-word exceeds: 77 / 1,105
- corpus-count distribution: 63 terms in 5 corpus labels, 1 term in 4 corpus labels, 5 terms in 3 corpus labels, 25 terms in 2 corpus labels, 60 terms in 1 corpus label

Top finite center-word-only ratios:

| Term | Language | Bible max | Bible corpus | Secular max | Secular corpus | Ratio |
| --- | --- | ---: | --- | ---: | --- | ---: |
| `שממה` (shemamah; English: Desolation)<br>`desolation_h` | hebrew | 1.67276669 | UHB | 0.174947546 | HEB_PBY_BIALIK | 9.56153275 |
| `יין` (yayin; English: Wine)<br>`cc_wine_h` | hebrew | 1.67276669 | UHB | 0.179491289 | HEB_PBY_BRENNER | 9.31948675 |
| `יין` (yayin; English: Wine)<br>`mt_wine_h` | hebrew | 1.67276669 | UHB | 0.179491289 | HEB_PBY_BRENNER | 9.31948675 |
| `יין` (yayin; English: Wine)<br>`twn_wine_h` | hebrew | 1.67276669 | UHB | 0.179491289 | HEB_PBY_BRENNER | 9.31948675 |
| `ישראל` (Yisrael; English: Israel)<br>`cc_israel_h` | hebrew | 5.84774803 | MT_WLC | 0.725114523 | HEB_PBY_AHAD_HAAM | 8.06458545 |
| `ישראל` (Yisrael; English: Israel)<br>`htp_israel_h` | hebrew | 5.84774803 | MT_WLC | 0.725114523 | HEB_PBY_AHAD_HAAM | 8.06458545 |

Top Bible-positive / secular-zero center-word terms:

| Term | Language | Bible max | Bible corpus |
| --- | --- | ---: | --- |
| `יהוה` (YHWH; English: YHWH Esther Acrostic)<br>`bns_esther_yhwh_h` | hebrew | 10.0247109 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`cc_yhwh_h` | hebrew | 10.0247109 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | hebrew | 10.0247109 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`htp_yhwh_h` | hebrew | 10.0247109 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`twn_yhwh_h` | hebrew | 10.0247109 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`yhwh_h` | hebrew | 10.0247109 | MT_WLC |

## Delta Versus Self-Surface Run

The concept-surface dictionary changed 26 `(term, corpus)` density rows compared with self-surface and created 26 newly nonzero rows.

Largest increases by added relevant centered hits:

| Term | Corpus | Concept | Self hits | Concept hits | Added hits |
| --- | --- | --- | ---: | ---: | ---: |
| `עובד` (wbd; English: Obed)<br>`twn_obed_h` | MT_WLC | Obed | 0 | 7 | 7 |
| `עובד` (wbd; English: Obed)<br>`twn_obed_h` | UXLC | Obed | 0 | 7 | 7 |
| `עובד` (wbd; English: Obed)<br>`twn_obed_h` | MAM | Obed | 0 | 4 | 4 |
| `עובד` (wbd; English: Obed)<br>`twn_obed_h` | EBIBLE_WLC | Obed | 0 | 4 | 4 |
| `עובד` (wbd; English: Obed)<br>`twn_obed_h` | UHB | Obed | 0 | 4 | 4 |
| `שטה` (shittah; English: Acacia)<br>`cc_acacia_h` | HEB_PBY_AHAD_HAAM | Acacia | 0 | 4 | 4 |
| `תתתתתא` (ttttt; English: Gregorian 2001)<br>`year_2001_additive_h` | MT_WLC | Gregorian 2001 | 0 | 2 | 2 |
| `צור` (tswr; English: Tyre)<br>`tyre_alt_h` | MT_WLC | Tyre | 0 | 2 | 2 |
| `תתתתתא` (ttttt; English: Gregorian 2001)<br>`year_2001_additive_h` | UXLC | Gregorian 2001 | 0 | 2 | 2 |
| `צור` (tswr; English: Tyre)<br>`tyre_alt_h` | UXLC | Tyre | 0 | 2 | 2 |

Same-concept expansion broadens recall, but it also broadens control hits. Treat concept-surface rows as a review queue, not as stronger evidence by default.

## Interpretation Notes

- This run is about concept-surface coincidence; all broader interpretation remains downstream review.
- The `center_word` subset is the clearest review surface and is reported separately from verse/span relevance.
- Duplicate term IDs from different claim lists were deduped by first-seen ID for this local run, but duplicate concepts with different IDs remain visible.
- The large classified-hit file is intentionally ignored; the DuckDB mirror is used for fast summaries.
- LLM and parallel modes require audit-log review before interpretation.
- Interpret results only against the dictionary and preregistration hashes recorded in the manifest.
