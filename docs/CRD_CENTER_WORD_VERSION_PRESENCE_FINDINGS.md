# CRD Center-Word Version Presence Findings

Status: local summary completed on 2026-05-10 from ignored CRD exact center-word outputs.

## Scope

This report summarizes which Bible edition labels contain exact center-word CRD hits. It uses the self-surface exact center-word subset because the concept-surface run has the same Bible exact center-word row keys.

This answers a source-distribution question: a centered pattern may be source-specific, multi-version, or broadly stable. The report does not require every pattern to appear in every edition.

## Outputs

- self-surface presence CSV: `reports/crd_self_surface/center_word_presence.csv`
- self-surface presence Markdown: `reports/crd_self_surface/center_word_presence.md`
- concept-surface presence CSV: `reports/crd_concept_surface/center_word_presence.csv`
- concept-surface presence Markdown: `reports/crd_concept_surface/center_word_presence.md`

## Reproduce

```bash
make crd-self-surface-center-word-presence
make crd-concept-surface-center-word-presence
```

## Summary

- exact center-word term rows: 131
- exact center-word hit rows: 1,044
- terms exceeding secular max in the center-word-only summary: 120
- language distribution: Hebrew 71, Greek 37, English 23
- corpus-count distribution: 57 terms in 5 corpus labels, 1 term in 4, 5 terms in 3, 24 terms in 2, and 44 terms in 1

## Strongest Multi-Version Rows

| Term | Language | Rows | Corpus count | Corpora | Exceeds secular max | Bible max | Secular max |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: |
| `bns_esther_yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `cc_yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `dyn_yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `htp_yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `twn_yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `cc_israel_h` | hebrew | 33 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 5.84774803 | 0.725114523 |
| `htp_israel_h` | hebrew | 33 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 5.84774803 | 0.725114523 |
| `israel_h` | hebrew | 33 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 5.84774803 | 0.725114523 |
| `twn_israel_h` | hebrew | 33 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 5.84774803 | 0.725114523 |
| `babel_h` | hebrew | 25 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 6.68314061 | 0 |
| `babylon_alt_h` | hebrew | 25 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 6.68314061 | 0 |
| `babylon_h` | hebrew | 25 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 6.68314061 | 0 |
| `bns_babylon_h` | hebrew | 25 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 6.68314061 | 0 |
| `cc_jupiter_h` | hebrew | 16 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 4.17696288 | 1.08767178 |
| `bcd_spoils_h` | hebrew | 15 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 2.50915003 | 0.349895093 |
| `cc_elohim_h` | hebrew | 15 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 2.50915003 | 0 |
| `god_h` | hebrew | 15 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 2.50915003 | 0 |
| `lord_h` | hebrew | 15 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 2.50915003 | 0 |
| `solomon_h` | hebrew | 15 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 2.50915003 | 0.362557261 |

## Read

- Exact center-word presence is not all-or-nothing across editions.
- Multi-version rows are useful for stability review, not automatic claim promotion.
- Single-version rows remain visible because source-specific patterns are part of the stated hypothesis.
- Bible-vs-control density remains necessary even when an exact center-word hit looks contextually strong.
