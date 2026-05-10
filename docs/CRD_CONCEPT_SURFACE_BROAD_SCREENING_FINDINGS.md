# CRD Concept-Surface Broad Screening Findings

Status: local deterministic broad screening run completed on 2026-05-09. Raw artifacts are intentionally kept under ignored `reports/crd_concept_surface/` because `classified_hits.csv` is 5.3 GB.

## Scope

This run asks a broader deterministic question than the self-surface run: when a hidden ELS term is centered, does the visible surface context contain any locked surface spelling from a committed term row with the same language and same concept?

This still does not use fuzzy matching, embeddings, or live interpretation. It uses exact normalized dictionary matching only. The run uses the same Bible and secular-control corpus list as the CRD protocol, with `skip_range = 2..100`, `direction = both`, `min_term_length = 3`, and `max_hits_per_term = 200`.

The input term set combines all committed term CSVs except `terms/crd_placeholder_terms.csv`, deduped by first-seen `term_id`. The local concept-surface dictionary was generated with `--seed-mode concept`, so each deterministic entry uses committed surface spellings that share the same `(language, concept)`.

## Outputs

- protocol: `reports/crd_concept_surface/protocol.toml`
- preregistration: `reports/crd_concept_surface/CRD_CONCEPT_SURFACE_PREREGISTRATION.md`
- dictionary: `reports/crd_concept_surface/relevance_dictionary_concept_surface.toml`
- density matrix: `reports/crd_concept_surface/density_matrix.csv`
- classified hits: `reports/crd_concept_surface/classified_hits.csv`
- comparison report: `reports/crd_concept_surface/CRD_CONCEPT_SURFACE_REPORT.md`

## Reproduce

```bash
make crd-concept-surface-prepare
make crd-concept-surface-run
make crd-concept-surface-report
```

## Run Size

- density rows: 18,444
- term/control comparison rows: 2,731
- classified hit rows: 1,404,450
- corpora with output: 20
- nonzero `(term, corpus)` density rows: 5,370
- runtime: 7,096.908 seconds
- API calls: 0
- estimated API cost: 0.0 USD

## Headline Counts

- `exceeds_secular_max = true`: 223 / 2,731 terms
- rows with secular max density = 0: 1,677 / 2,731 terms
- rows with Bible max > 0 and secular max = 0: 99 / 2,731 terms
- Hebrew exceeds: 82 / 1,018
- Greek exceeds: 98 / 862
- English exceeds: 43 / 851

Compared with the self-surface run, the concept-surface run is only slightly broader at the headline level: `exceeds_secular_max` moved from 221 to 223, and nonzero density rows moved from 5,323 to 5,370. That means many current concepts still have only one effective surface spelling, or their same-concept variants do not materially change the centered-hit density screen.

## Strongest Finite Bible-Vs-Control Ratios

| Term | Language | Bible max | Bible corpus | Secular max | Secular corpus | Ratio |
| --- | --- | ---: | --- | ---: | --- | ---: |
| `gilead_h` | hebrew | 5.01830007 | UHB | 0.174947546 | HEB_PBY_BIALIK | 28.6845982 |
| `lord_h` | hebrew | 26.764267 | UHB | 1.22463282 | HEB_PBY_BIALIK | 21.854932 |
| `darius_h` | hebrew | 4.1598203 | MAM | 0.362557261 | HEB_PBY_AHAD_HAAM | 11.473554 |
| `ephraim_h` | hebrew | 7.5274501 | UHB | 0.874737732 | HEB_PBY_BIALIK | 8.60537945 |
| `jebusite_h` | hebrew | 2.50617773 | MT_WLC | 0.349895093 | HEB_PBY_BIALIK | 7.16265469 |
| `yhwh_h` and duplicates | hebrew | 63.5651342 | UHB | 9.4471675 | HEB_PBY_BIALIK | 6.72848599 |
| `bns_chaldea_h` | hebrew | 3.34553338 | UHB | 0.524842639 | HEB_PBY_BIALIK | 6.37435515 |
| `plague_h` and concept duplicates | hebrew | 3.34553338 | UHB | 0.524842639 | HEB_PBY_BIALIK | 6.37435515 |
| `isaac_g` and duplicates | greek | 5.88339984 | SBLGNT | 1.03924717 | GRC_PERSEUS_HERODOTUS | 5.66121324 |
| `bns_jesus_g` and duplicates | greek | 5.79012812 | TR_NT | 1.03924717 | GRC_PERSEUS_HERODOTUS | 5.57146393 |

## Strongest Bible Hits With Secular Max Zero

| Term | Language | Bible max | Bible corpus |
| --- | --- | ---: | --- |
| `david_g` and duplicate | greek | 6.80550128 | LXX |
| `spirit_g`, `spirit_gxc`, `spirit_pneuma_g` | greek | 5.88339984 | SBLGNT |
| `eng_david` and duplicates | english | 4.65372414 | KJV |
| `wisdom_g`, `wisdom_gxc` | greek | 4.41254988 | SBLGNT |
| `kyrios_gnt`, `lord_g`, `lord_gxc` | greek | 3.2236585 | LXX |
| `eng_zion` and duplicates | english | 3.10248276 | KJV |
| `elishah_g` and duplicate | greek | 2.90734016 | TCG_NT |
| `jacob_g` and duplicate | greek | 2.90734016 | TCG_NT |
| `gpx_lawlessness_g` | greek | 2.89633859 | BYZ_NT |

## Interpretation Notes

- This run is deterministic concept-surface screening: hidden `X` centered near a visible spelling from the same committed concept.
- It is broader than self-surface coincidence, but still narrower than a human or LLM related-concept judgment.
- A concept match here means the dictionary locked an exact surface spelling from a same-concept term row before the density comparison was interpreted.
- The strongest rows remain broadly similar to the self-surface run, which suggests the current concept grouping does not radically inflate the top-line signal.
- Secular-control zeroes can reflect missing surface vocabulary in the control corpora, not only signal strength. Treat those as review-priority flags, not proof.
- Follow-up work should inspect representative centered hits for high-ratio terms and compare them against matched controls and null-control terms.
