# KJVA Apocrypha Bridge Term Shuffled Controls (1000 Samples)

Status: term-level shuffled-insertion controls. This is not a claim report.

This control keeps the canonical prefix and apocrypha/deuterocanon block
length fixed, shuffles the block letters, and records bridge rows per
observed bridge term.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_term_shuffled_controls --canonical-label KJVA --canonical-config configs/example_ebible_engkjv_apocrypha.toml --observed reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv --terms terms/english_search_terms.csv --samples 1000 --seed 20260509 --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --resume-samples --sample-out reports/kjv_apocrypha_bridge_term_shuffled_controls_1000/sample_summary.csv --term-sample-out reports/kjv_apocrypha_bridge_term_shuffled_controls_1000/term_samples.csv --term-summary-out reports/kjv_apocrypha_bridge_term_shuffled_controls_1000/term_summary.csv --markdown-out docs/KJV_APOCRYPHA_BRIDGE_TERM_SHUFFLED_CONTROLS_1000.md --manifest-out reports/kjv_apocrypha_bridge_term_shuffled_controls_1000/manifest.json
```

## Summary

- corpus letters: 3816315
- canonical prefix letters: 2483327
- apocrypha block letters: 593090
- bridge terms reviewed: 81
- shuffled samples: 1000
- total shuffled min/mean/max: 130 / 184.306 / 248
- terms with observed count above every shuffled sample: 8
- terms with BH q_ge <= 0.05: 15

## Top Terms

| Rank | Term | Concept | Observed | Shuffled max | Shuffled mean | Samples >= obs | p_ge | q_ge | Delta |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `nato` | NATO | 22 | 18 | 7.431 | 0 | 0.000999 | 0.010115 | 4 |
| 2 | `seba` | Seba | 10 | 7 | 1.335 | 0 | 0.000999 | 0.010115 | 3 |
| 3 | `sign` | Sign | 6 | 4 | 0.445 | 0 | 0.000999 | 0.010115 | 2 |
| 4 | `eber` | Eber | 10 | 9 | 2.043 | 0 | 0.000999 | 0.010115 | 1 |
| 5 | `satan` | Satan | 5 | 4 | 0.707 | 0 | 0.000999 | 0.010115 | 1 |
| 6 | `moab` | Moab | 4 | 3 | 0.359 | 0 | 0.000999 | 0.010115 | 1 |
| 7 | `sidon` | Sidon;Sidon | 3 | 2 | 0.117 | 0 | 0.000999 | 0.010115 | 1 |
| 8 | `sivan` | Sivan | 2 | 1 | 0.015 | 0 | 0.000999 | 0.010115 | 1 |
| 9 | `gallus` | Gallus | 1 | 1 | 0.001 | 1 | 0.001998 | 0.017982 | 0 |
| 10 | `otho` | Otho | 23 | 23 | 10.046 | 2 | 0.002997 | 0.022069 | 0 |
| 11 | `seal` | Seal;Seal;Seal | 16 | 17 | 5.682 | 2 | 0.002997 | 0.022069 | -1 |
| 12 | `house` | House | 3 | 3 | 0.221 | 3 | 0.003996 | 0.026973 | 0 |
| 13 | `tomb` | Tomb;Tomb | 3 | 3 | 0.387 | 6 | 0.006993 | 0.040459 | 0 |
| 14 | `noah` | Noah | 14 | 17 | 6.13 | 6 | 0.006993 | 0.040459 | -3 |
| 15 | `abib` | Abib | 2 | 2 | 0.097 | 7 | 0.007992 | 0.043157 | 0 |
| 16 | `isaac` | Isaac | 2 | 2 | 0.16 | 11 | 0.011988 | 0.060689 | 0 |
| 17 | `amen` | Amen | 8 | 10 | 3.305 | 15 | 0.015984 | 0.076159 | -2 |
| 18 | `torah` | Torah | 4 | 5 | 0.957 | 17 | 0.017982 | 0.080919 | -1 |
| 19 | `life` | Life | 5 | 6 | 1.594 | 21 | 0.021978 | 0.089011 | -1 |
| 20 | `obal` | Obal | 3 | 5 | 0.573 | 21 | 0.021978 | 0.089011 | -2 |
| 21 | `king` | King;King | 1 | 1 | 0.025 | 25 | 0.025974 | 0.100185 | 0 |
| 22 | `heart` | Heart;Heart | 5 | 7 | 1.628 | 31 | 0.031968 | 0.1177 | -2 |
| 23 | `geta` | Geta | 8 | 11 | 3.433 | 34 | 0.034965 | 0.123138 | -3 |
| 24 | `mash` | Mash | 6 | 9 | 2.304 | 37 | 0.037962 | 0.128122 | -3 |
| 25 | `rome` | Rome | 6 | 9 | 2.431 | 48 | 0.048951 | 0.15203 | -3 |
| 26 | `image` | Image | 1 | 1 | 0.051 | 51 | 0.051948 | 0.15203 | 0 |
| 27 | `bibi` | Bibi | 1 | 3 | 0.06 | 54 | 0.054945 | 0.15203 | -2 |
| 28 | `edom` | Edom | 5 | 8 | 2.106 | 54 | 0.054945 | 0.15203 | -3 |
| 29 | `admah` | Admah | 2 | 3 | 0.432 | 59 | 0.05994 | 0.15203 | -1 |
| 30 | `korea` | Korea | 1 | 2 | 0.063 | 59 | 0.05994 | 0.15203 | -1 |
| 31 | `ahab` | Ahab | 4 | 8 | 1.454 | 59 | 0.05994 | 0.15203 | -4 |
| 32 | `death` | Death;Death | 4 | 7 | 1.468 | 61 | 0.061938 | 0.15203 | -3 |
| 33 | `lion` | Lion | 5 | 10 | 2.091 | 61 | 0.061938 | 0.15203 | -5 |
| 34 | `teeth` | Teeth | 8 | 12 | 3.985 | 69 | 0.06993 | 0.166598 | -4 |
| 35 | `hail` | Hail | 8 | 13 | 4.003 | 76 | 0.076923 | 0.178022 | -5 |
| 36 | `light` | Light;Light | 1 | 2 | 0.082 | 80 | 0.080919 | 0.182068 | -1 |
| 37 | `cedar` | Cedar | 1 | 3 | 0.099 | 93 | 0.093906 | 0.205578 | -2 |
| 38 | `aids` | AIDS | 6 | 10 | 3.066 | 98 | 0.098901 | 0.210815 | -4 |
| 39 | `sadat` | Sadat | 2 | 4 | 0.548 | 105 | 0.105894 | 0.219934 | -2 |
| 40 | `isis` | ISIS | 4 | 8 | 1.771 | 113 | 0.113886 | 0.230619 | -4 |
| 41 | `heth` | Heth | 31 | 47 | 23.411 | 120 | 0.120879 | 0.23881 | -16 |
| 42 | `india` | India | 1 | 3 | 0.146 | 137 | 0.137862 | 0.265877 | -2 |
| 43 | `fire` | Fire | 5 | 10 | 2.742 | 143 | 0.143856 | 0.270985 | -5 |
| 44 | `demon` | Demon | 1 | 3 | 0.162 | 152 | 0.152847 | 0.275125 | -2 |
| 45 | `resen` | Resen | 2 | 5 | 0.66 | 152 | 0.152847 | 0.275125 | -3 |
| 46 | `word` | Word | 2 | 5 | 0.739 | 159 | 0.15984 | 0.275469 | -3 |
| 47 | `eyes` | Eyes | 5 | 10 | 2.749 | 159 | 0.15984 | 0.275469 | -5 |
| 48 | `star` | Star | 8 | 14 | 5.264 | 184 | 0.184815 | 0.310465 | -6 |
| 49 | `sheba` | Sheba | 1 | 3 | 0.21 | 187 | 0.187812 | 0.310465 | -2 |
| 50 | `lamb` | Lamb;Lamb | 1 | 3 | 0.234 | 207 | 0.207792 | 0.336623 | -2 |

## Read

- This is a post-screen calibration over already observed bridge terms.
- `p_ge` is add-one empirical tail probability for the term count under
  shuffled insertion blocks.
- `q_ge` is Benjamini-Hochberg correction across the emitted bridge terms.
- It should guide follow-up priority, not convert bridge terms into claims.
