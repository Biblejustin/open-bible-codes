# CRD Self-Surface Broad Screening Findings

Status: local deterministic broad screening run completed on 2026-05-09. Raw artifacts are intentionally kept under ignored `reports/crd_self_surface/` because `classified_hits.csv` is 5.3 GB.

## Scope

This run asks a narrow, non-interpretive question: when a hidden ELS term is centered, does the visible surface context contain that same term spelling? It does not test broader related-term relevance. It uses the same Bible and secular-control corpus list as the locked CRD Gog/Magog protocol, with `skip_range = 2..100`, `direction = both`, `min_term_length = 3`, and `max_hits_per_term = 200`.

The input term set combines all committed term CSVs except `terms/crd_placeholder_terms.csv`, deduped by first-seen `term_id`. The local self-surface dictionary was generated with `--seed-surface-term`, so each deterministic entry uses only the term's own visible spelling as `surface_keywords`.

## Outputs

- protocol: `reports/crd_self_surface/protocol.toml`
- preregistration: `reports/crd_self_surface/CRD_SELF_SURFACE_PREREGISTRATION.md`
- dictionary: `reports/crd_self_surface/relevance_dictionary_self_surface.toml`
- density matrix: `reports/crd_self_surface/density_matrix.csv`
- classified hits: `reports/crd_self_surface/classified_hits.csv`
- comparison report: `reports/crd_self_surface/CRD_SELF_SURFACE_REPORT.md`
- compact review queue: `reports/crd_self_surface/review_queue.csv`
- Bible exact center-word hits: `reports/crd_self_surface/center_word_hits.csv`
- exact center-word density summary: `reports/crd_self_surface/center_word_bible_vs_control_summary.csv`
- exact center-word review queue: `reports/crd_self_surface/center_word_review_queue.csv`
- exact center-word review packet: `reports/crd_self_surface/center_word_review_packet.md`
- exact center-word version presence: `reports/crd_self_surface/center_word_presence.md`

## Reproduce

```bash
make crd-self-surface-prepare
make crd-self-surface-run
make crd-self-surface-report
make crd-self-surface-queue
make crd-self-surface-center-word
make crd-self-surface-center-word-density
make crd-self-surface-center-word-queue
make crd-self-surface-center-word-packet
make crd-self-surface-center-word-presence
```

## Run Size

- density rows: 18,444
- term/control comparison rows: 2,731
- classified hit rows: 1,404,450
- corpora with output: 20
- nonzero `(term, corpus)` density rows: 5,323
- compact review queue rows: 309
- compact review queue selected terms: 50
- exact center-word review queue rows: 202
- exact center-word review queue selected terms: 50
- runtime: 7,539.274 seconds

## Headline Counts

- `exceeds_secular_max = true`: 221 / 2,731 terms
- rows with secular max density = 0: 1,680 / 2,731 terms
- Hebrew exceeds: 80 / 1,018
- Greek exceeds: 98 / 862
- English exceeds: 43 / 851

Large numbers of secular-zero rows mean many terms have no self-surface match in the available control corpora. These rows are useful for triage, but they should not be interpreted as strong evidence without matched vocabulary controls or shuffled controls.

## Surface Match Scope

The rerun writes deterministic match scope for every relevant classified hit:

- all relevant rows: `center_verse = 117,464`, `span = 4,084`, `center_word = 1,245`
- Bible relevant rows: `center_verse = 14,647`, `span = 4,084`, `center_word = 1,044`
- secular-control relevant rows: `center_verse = 102,817`, `center_word = 201`
- compact review queue rows: `center_verse = 151`, `span = 138`, `center_word = 20`

The exact `center_word` scope is the strictest form of self-surface coincidence: the hidden term is centered on the same visible word, not merely somewhere in the same verse or span.

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
| `plague_h` | hebrew | 3.34553338 | UHB | 0.524842639 | HEB_PBY_BIALIK | 6.37435515 |
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
| `eng_zion` and duplicate rows | english | 3.10248276 | KJV |
| `elishah_g` and duplicate | greek | 2.90734016 | TCG_NT |
| `jacob_g` and duplicate | greek | 2.90734016 | TCG_NT |
| `gpx_lawlessness_g` | greek | 2.89633859 | BYZ_NT |

## Exact Center-Word Subset

The exact center-word extraction contains:

- Bible center-word rows: 1,044
- distinct term IDs with Bible center-word rows: 131
- rows whose term exceeds the secular maximum in the center-word-only summary: 1,023
- rows whose term does not exceed the secular maximum in the center-word-only summary: 21

The center-word-only density summary contains 2,731 term rows:

- `exceeds_secular_max = true`: 120
- Bible-positive / secular-zero terms: 94
- Hebrew exceeds: 70
- Greek exceeds: 35
- English exceeds: 15

The version-presence summary keeps source-specific results visible:

- exact center-word term rows: 131
- exact center-word hit rows: 1,044
- language distribution: Hebrew 71, Greek 37, English 23
- corpus-count distribution: 57 terms in 5 corpus labels, 1 term in 4, 5 terms in 3, 24 terms in 2, and 44 terms in 1

Top finite center-word-only ratios:

| Term | Language | Bible max | Bible corpus | Secular max | Secular corpus | Ratio |
| --- | --- | ---: | --- | ---: | --- | ---: |
| `desolation_h` | hebrew | 1.67276669 | UHB | 0.174947546 | HEB_PBY_BIALIK | 9.5615 |
| `cc_wine_h`, `mt_wine_h`, `twn_wine_h` | hebrew | 1.67276669 | UHB | 0.179491289 | HEB_PBY_BRENNER | 9.3195 |
| `cc_israel_h`, `htp_israel_h`, `israel_h`, `twn_israel_h` | hebrew | 5.84774803 | MT_WLC | 0.725114523 | HEB_PBY_AHAD_HAAM | 8.0646 |
| `bcd_spoils_h` | hebrew | 2.50915003 | UHB | 0.349895093 | HEB_PBY_BIALIK | 7.1711 |
| `solomon_h` | hebrew | 2.50915003 | UHB | 0.362557261 | HEB_PBY_AHAD_HAAM | 6.9207 |
| `sephar_h` | hebrew | 2.50617773 | MT_WLC | 0.362557261 | HEB_PBY_AHAD_HAAM | 6.9125 |

Top Bible-positive / secular-zero center-word terms:

| Term | Language | Bible max | Bible corpus |
| --- | --- | ---: | --- |
| `yhwh_h` and duplicates | hebrew | 10.0247109 | MT_WLC |
| `babel_h`, `babylon_h`, and duplicates | hebrew | 6.68314061 | MT_WLC |
| `dyn_gog_g`, `gog_g`, `noah_g` | greek | 2.94169992 | SBLGNT |
| `wisdom_g`, `wisdom_gxc` | greek | 2.89633859 | BYZ_NT |
| `cc_elohim_h`, `god_h`, `lord_h` | hebrew | 2.50915003 | UHB |
| `eng_david`, `eng_david_2` | english | 1.86148966 | KJV |

## Interpretation Notes

- This run is about self-surface coincidence only: hidden `X` centered near visible `X`.
- The `center_word` subset is the clearest review surface for hidden `X` centered directly on visible `X`; verse-level and span-level rows remain useful but should be reported separately.
- It does not answer whether hidden `X` is centered on a broader related concept unless a separate relevance dictionary locks that relationship.
- Duplicate term IDs from different claim lists were deduped by first-seen ID for this local run, but duplicate concepts with different IDs remain visible in the results.
- The large 5.3 GB classified-hit file exposed a real scaling issue. `scripts/build_crd_comparison.py` now streams representative examples and agreement inputs instead of loading the whole file.
- `scripts/run_crd_density.py` now streams classified-hit rows during generation so future broad runs do not buffer millions of hit rows in memory.
- The next production improvement should be resumable per-corpus or per-term checkpointing for interrupted broad CRD runs.
