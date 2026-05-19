# CRD Self-Surface Broad Screening Findings

Status: local deterministic broad screening run completed at `2026-05-12T15:45:32.189534+00:00`. Raw artifacts stay under ignored `reports/crd_self_surface/`; `classified_hits.csv` is 7.07 GB.

## Scope

This run asks a deterministic centered-relevance question: when a hidden ELS term is centered, does the visible surface context contain that same term spelling? It uses exact normalized dictionary matching only; no fuzzy matching, embeddings, or live interpretation are used.

The run uses the same Bible and secular-control corpus list as the CRD protocol, with `skip_range = 2..100`, `direction = both`, `min_term_length = 3`, and `max_hits_per_term = 200`.

The input term set combines all committed term CSVs except `terms/crd_placeholder_terms.csv`, deduped by first-seen `term_id`. Self-surface means hidden `X` is centered near visible `X`.

## Outputs

- protocol: `reports/crd_self_surface/protocol.toml`
- preregistration: `reports/crd_self_surface/CRD_SELF_SURFACE_PREREGISTRATION.md`
- dictionary: `reports/crd_self_surface/relevance_dictionary_self_surface.toml`
- density matrix: `reports/crd_self_surface/density_matrix.csv`
- classified hits: `reports/crd_self_surface/classified_hits.csv`
- comparison report: `reports/crd_self_surface/CRD_SELF_SURFACE_REPORT.md`
- compact review queue: `reports/crd_self_surface/review_queue.csv`
- Bible exact center-word hits: `reports/crd_self_surface/center_word_hits.csv`
- exact center-word version presence: `reports/crd_self_surface/center_word_presence.md`

## Reproduce

```bash
make crd-self-surface-prepare
python3 -m scripts.run_crd_density reports/crd_self_surface/protocol.toml --classifier-mode deterministic --resume --force-reset
make report-db
make crd-self-surface-report
make crd-self-surface-queue
make crd-self-surface-center-word
make crd-self-surface-center-word-density
make crd-self-surface-center-word-queue
make crd-self-surface-center-word-packet
make crd-self-surface-center-word-presence
make crd-broad-screening-findings
make crd-center-word-findings
```

## Run Size

- density rows: 23,012
- term/control comparison rows: 3,612
- classified hit rows: 1,734,450
- corpora with output: 20
- nonzero `(term, corpus)` density rows: 13,795
- compact review queue rows: 433
- compact review queue selected terms: 50
- exact center-word review queue rows: 231
- exact center-word review queue selected terms: 50
- runtime: 8700.714 seconds
- API calls: 0
- estimated API cost: 0.0 USD

## Headline Counts

- `exceeds_secular_max = true`: 622 / 3,612 terms
- rows with secular max density = 0: 3,480 / 3,612 terms
- rows with Bible max > 0 and secular max = 0: 523 / 3,612 terms
- English exceeds: 202 / 1,471
- Greek exceeds: 160 / 962
- Hebrew exceeds: 260 / 1,179

Large numbers of secular-zero rows are review-priority flags, not automatic claim promotions. They can reflect dictionary vocabulary and control-corpus coverage.

## Surface Match Scope

Relevant classified-hit rows by scope:

- `bible.center_word`: 1,379
- `bible.center_verse`: 6,371
- `bible.span`: 2,814
- `secular_control.center_word`: 242
- `secular_control.center_verse`: 0
- `secular_control.span`: 0

Compact review queue scope:

- `center_verse`: 263
- `center_word`: 71
- `span`: 99

The exact `center_word` scope is the strictest form: the hidden term is centered directly on the visible matching or same-concept word. `center_verse` and `span` remain broader contextual flags and should be reviewed separately.

## Strongest Finite Bible-Vs-Control Ratios

| Term | Language | Bible max | Bible corpus | Secular max | Secular corpus | Ratio |
| --- | --- | ---: | --- | ---: | --- | ---: |
| `ישראל` (Yisrael; English: Israel)<br>`cc_israel_h` | hebrew | 52.6297323 | MT_WLC | 0.725114523 | HEB_PBY_AHAD_HAAM | 72.5812691 |
| `ישראל` (Yisrael; English: Israel)<br>`htp_israel_h` | hebrew | 52.6297323 | MT_WLC | 0.725114523 | HEB_PBY_AHAD_HAAM | 72.5812691 |
| `ישראל` (Yisrael; English: Israel)<br>`israel_h` | hebrew | 52.6297323 | MT_WLC | 0.725114523 | HEB_PBY_AHAD_HAAM | 72.5812691 |
| `ישראל` (Yisrael; English: Israel)<br>`npg_israel_h` | hebrew | 52.6297323 | MT_WLC | 0.725114523 | HEB_PBY_AHAD_HAAM | 72.5812691 |
| `ישראל` (Yisrael; English: Israel)<br>`twn_israel_h` | hebrew | 52.6297323 | MT_WLC | 0.725114523 | HEB_PBY_AHAD_HAAM | 72.5812691 |
| `יוסף` (ywsp; English: Joseph)<br>`cc_joseph_h` | hebrew | 11.6954961 | MT_WLC | 0.174947546 | HEB_PBY_BIALIK | 66.8514441 |
| `יוסף` (ywsp; English: Joseph)<br>`joseph_h` | hebrew | 11.6954961 | MT_WLC | 0.174947546 | HEB_PBY_BIALIK | 66.8514441 |
| `יוסף` (ywsp; English: Joseph Tribe)<br>`joseph_tribe_h` | hebrew | 11.6954961 | MT_WLC | 0.174947546 | HEB_PBY_BIALIK | 66.8514441 |
| `יוסף` (ywsp; English: Joseph)<br>`mt_joseph_h` | hebrew | 11.6954961 | MT_WLC | 0.174947546 | HEB_PBY_BIALIK | 66.8514441 |
| `Lord`<br>`eng_lord` | english | 19.2353931 | KJV | 0.739422378 | ENG_PG_SHAKESPEARE | 26.0140803 |

## Strongest Bible Hits With Secular Max Zero

| Term | Language | Bible max | Bible corpus |
| --- | --- | ---: | --- |
| `יהוה` (YHWH; English: YHWH Esther Acrostic)<br>`bns_esther_yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`cc_yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`htp_yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`npg_yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`twn_yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`word_edge_yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`yhwh_h` | hebrew | 50.9589471 | MT_WLC |
| `אשר` (shr; English: Asher)<br>`asher_h` | hebrew | 34.2510956 | MT_WLC |
| `יהודה` (Yehudah; English: Judah)<br>`judah_h` | hebrew | 20.8848144 | MT_WLC |

## Exact Center-Word Subset

- Bible center-word rows: 1,379
- distinct term IDs with Bible center-word rows: 169
- exact center-word presence rows: 169
- distinct visible spellings in presence output: 92
- center-word-only summary rows: 3,612; `exceeds_secular_max = true`: 155
- Bible-positive / secular-zero center-word terms: 124
- English center-word exceeds: 27 / 1,471
- Greek center-word exceeds: 39 / 962
- Hebrew center-word exceeds: 89 / 1,179
- corpus-count distribution: 69 terms in 5 corpus labels, 1 term in 4 corpus labels, 6 terms in 3 corpus labels, 30 terms in 2 corpus labels, 63 terms in 1 corpus label

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
| `יהוה` (YHWH; English: YHWH)<br>`npg_yhwh_h` | hebrew | 10.0247109 | MT_WLC |
| `יהוה` (YHWH; English: YHWH)<br>`twn_yhwh_h` | hebrew | 10.0247109 | MT_WLC |

## Interpretation Notes

- This run is about self-surface coincidence; all broader interpretation remains downstream review.
- The `center_word` subset is the clearest review surface and is reported separately from verse/span relevance.
- Duplicate term IDs from different claim lists were deduped by first-seen ID for this local run, but duplicate concepts with different IDs remain visible.
- The large classified-hit file is intentionally ignored; the DuckDB mirror is used for fast summaries.
- LLM and parallel modes require audit-log review before interpretation.
- Interpret results only against the dictionary and preregistration hashes recorded in the manifest.
