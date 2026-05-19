# CRD Center-Word Version Presence Findings

Status: local summary generated from ignored CRD exact center-word outputs.

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
make crd-center-word-findings
```

## Summary

- exact center-word term rows: 169
- distinct normalized surface forms: 89
- exact center-word hit rows: 1,379
- distinct normalized surface hit paths: 504
- terms exceeding secular max in the center-word-only summary: 155
- language distribution: Hebrew 90, Greek 42, English 37
- corpus-count distribution: 69 terms in 5 corpus labels, 1 term in 4 corpus labels, 6 terms in 3 corpus labels, 30 terms in 2 corpus labels, 63 terms in 1 corpus label

## Strongest Distinct Surface Forms

This table collapses duplicate term IDs that use the same normalized hidden spelling. The raw term-row table remains below.

| Term | Language | Term rows | Unique paths | Corpus count | Corpora | Exceeds secular max | Bible max | Secular max |
| --- | --- | ---: | ---: | ---: | --- | --- | ---: | ---: |
| `יהוה` (YHWH; English: YHWH)<br>`bns_esther_yhwh_h, cc_yhwh_h, dyn_yhwh_h, ...` | hebrew | 8 | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `ישראל` (Yisrael; English: Israel)<br>`cc_israel_h, htp_israel_h, israel_h, ...` | hebrew | 5 | 33 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 5.84774803 | 0.725114523 |
| `זהב` (zahav; English: gold)<br>`daniel_gold_h` | hebrew | 1 | 30 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 5.01830007 | 0 |
| `בבל` (Bavel; English: Babylon)<br>`atbash_babylon_h, babel_h, babylon_alt_h, ...` | hebrew | 6 | 25 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 6.68314061 | 0 |
| `כסף` (kesef; English: silver)<br>`daniel_silver_h` | hebrew | 1 | 22 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 4.17696288 | 0 |
| `שלמה` (Shlomo; English: Solomon)<br>`narrative_solomon_h, solomon_h` | hebrew | 2 | 15 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 2.50915003 | 0.362557261 |
| `שלל` (shalal; English: spoil/plunder)<br>`bcd_spoils_h` | hebrew | 1 | 15 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 2.50915003 | 0.349895093 |
| `אלהים` (Elohim; English: God/Elohim)<br>`cc_elohim_h, god_h` | hebrew | 2 | 15 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 2.50915003 | 0 |
| `אדני` (Adonai; English: Lord)<br>`lord_h` | hebrew | 1 | 15 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 2.50915003 | 0 |
| `צדק` (tzedek; English: righteousness/Jupiter)<br>`cc_jupiter_h` | hebrew | 1 | 12 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 4.17696288 | 1.08767178 |
| `ספר` (sefer; English: book/Sephar)<br>`sephar_h` | hebrew | 1 | 12 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 2.50617773 | 0.362557261 |
| `שממה` (shemamah; English: desolation)<br>`desolation_h` | hebrew | 1 | 10 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 1.67276669 | 0.174947546 |
| `קדש` (qodesh; English: holiness/sacred)<br>`holy_h, npg_holy_h` | hebrew | 2 | 10 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 1.67276669 | 0 |
| `ענן` (anan; English: cloud)<br>`cc_annas_h, mt_annas_h, twn_annas_h` | hebrew | 3 | 10 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 1.67276669 | 0 |
| `יין` (yayin; English: wine)<br>`cc_wine_h, mt_wine_h, twn_wine_h` | hebrew | 3 | 10 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 1.67276669 | 0.179491289 |
| `יהודה` (Yehudah; English: Judah)<br>`judah_h, mt_judas_absence_h` | hebrew | 2 | 10 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 1.67276669 | 0 |
| `חסד` (chesed; English: mercy/steadfast love)<br>`htp_mercy_h, mercy_h` | hebrew | 2 | 10 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 1.67276669 | 0.349895093 |
| `σοφια` (sophia; English: wisdom)<br>`wisdom_g, wisdom_gxc` | greek | 2 | 7 | 5 | BYZ_NT; LXX; SBLGNT; TCG_NT; TR_NT | true | 2.89633859 | 0 |
| `פרץ` (prts; English: Pharez)<br>`twn_pharez_h` | hebrew | 1 | 7 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 1.67078515 | 0 |
| `שנים` (shnym; English: Teeth)<br>`teeth_h` | hebrew | 1 | 5 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 0.836383345 | 0 |

## Strongest Multi-Version Rows

| Term | Language | Rows | Corpus count | Corpora | Exceeds secular max | Bible max | Secular max |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: |
| `יהוה` (YHWH; English: YHWH)<br>`bns_esther_yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `יהוה` (YHWH; English: YHWH)<br>`cc_yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `יהוה` (YHWH; English: YHWH)<br>`htp_yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `יהוה` (YHWH; English: YHWH)<br>`npg_yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `יהוה` (YHWH; English: YHWH)<br>`twn_yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `יהוה` (YHWH; English: YHWH)<br>`word_edge_yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `יהוה` (YHWH; English: YHWH)<br>`yhwh_h` | hebrew | 54 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 10.0247109 | 0 |
| `ישראל` (Yisrael; English: Israel)<br>`cc_israel_h` | hebrew | 33 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 5.84774803 | 0.725114523 |
| `ישראל` (Yisrael; English: Israel)<br>`htp_israel_h` | hebrew | 33 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 5.84774803 | 0.725114523 |
| `ישראל` (Yisrael; English: Israel)<br>`israel_h` | hebrew | 33 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 5.84774803 | 0.725114523 |
| `ישראל` (Yisrael; English: Israel)<br>`npg_israel_h` | hebrew | 33 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 5.84774803 | 0.725114523 |
| `ישראל` (Yisrael; English: Israel)<br>`twn_israel_h` | hebrew | 33 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 5.84774803 | 0.725114523 |
| `זהב` (zahav; English: gold)<br>`daniel_gold_h` | hebrew | 30 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 5.01830007 | 0 |
| `בבל` (Bavel; English: Babylon)<br>`atbash_babylon_h` | hebrew | 25 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 6.68314061 | 0 |
| `בבל` (Bavel; English: Babylon)<br>`babel_h` | hebrew | 25 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 6.68314061 | 0 |
| `בבל` (Bavel; English: Babylon)<br>`babylon_alt_h` | hebrew | 25 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 6.68314061 | 0 |
| `בבל` (Bavel; English: Babylon)<br>`babylon_h` | hebrew | 25 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 6.68314061 | 0 |
| `בבל` (Bavel; English: Babylon)<br>`bns_babylon_h` | hebrew | 25 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 6.68314061 | 0 |
| `בבל` (Bavel; English: Babylon)<br>`word_edge_babylon_h` | hebrew | 25 | 5 | EBIBLE_WLC; MAM; MT_WLC; UHB; UXLC | true | 6.68314061 | 0 |

## Read

- Exact center-word presence is not all-or-nothing across editions.
- Multi-version rows are useful for stability review, not automatic claim promotion.
- Single-version rows remain visible because source-specific patterns are part of the stated hypothesis.
- Bible-vs-control density remains necessary even when an exact center-word hit looks contextually strong.
