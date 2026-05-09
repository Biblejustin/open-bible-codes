# KJVA Apocrypha Bridge Term Shuffled Controls (100 Samples)

Status: term-level shuffled-insertion controls. This is not a claim report.

This control keeps the canonical prefix and apocrypha/deuterocanon block
length fixed, shuffles the block letters, and records bridge rows per
observed bridge term.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_term_shuffled_controls --canonical-label KJVA --canonical-config configs/example_ebible_engkjv_apocrypha.toml --observed reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv --terms terms/english_search_terms.csv --samples 100 --seed 20260509 --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --resume-samples --sample-out reports/kjv_apocrypha_bridge_term_shuffled_controls_100/sample_summary.csv --term-sample-out reports/kjv_apocrypha_bridge_term_shuffled_controls_100/term_samples.csv --term-summary-out reports/kjv_apocrypha_bridge_term_shuffled_controls_100/term_summary.csv --markdown-out docs/KJV_APOCRYPHA_BRIDGE_TERM_SHUFFLED_CONTROLS_100.md --manifest-out reports/kjv_apocrypha_bridge_term_shuffled_controls_100/manifest.json
```

## Summary

- corpus letters: 3816315
- canonical prefix letters: 2483327
- apocrypha block letters: 593090
- bridge terms reviewed: 81
- shuffled samples: 100
- total shuffled min/mean/max: 151 / 186.38 / 236
- terms with observed count above every shuffled sample: 12
- terms with BH q_ge <= 0.05: 0

## Top Terms

| Rank | Term | Concept | Observed | Shuffled max | Shuffled mean | Samples >= obs | p_ge | q_ge | Delta |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `nato` | NATO | 22 | 13 | 7.12 | 0 | 0.009901 | 0.066832 | 9 |
| 2 | `seba` | Seba | 10 | 5 | 1.14 | 0 | 0.009901 | 0.066832 | 5 |
| 3 | `eber` | Eber | 10 | 6 | 1.84 | 0 | 0.009901 | 0.066832 | 4 |
| 4 | `sign` | Sign | 6 | 3 | 0.48 | 0 | 0.009901 | 0.066832 | 3 |
| 5 | `noah` | Noah | 14 | 12 | 6.36 | 0 | 0.009901 | 0.066832 | 2 |
| 6 | `satan` | Satan | 5 | 3 | 0.74 | 0 | 0.009901 | 0.066832 | 2 |
| 7 | `moab` | Moab | 4 | 2 | 0.47 | 0 | 0.009901 | 0.066832 | 2 |
| 8 | `house` | House | 3 | 2 | 0.3 | 0 | 0.009901 | 0.066832 | 1 |
| 9 | `sidon` | Sidon;Sidon | 3 | 2 | 0.21 | 0 | 0.009901 | 0.066832 | 1 |
| 10 | `abib` | Abib | 2 | 1 | 0.12 | 0 | 0.009901 | 0.066832 | 1 |
| 11 | `sivan` | Sivan | 2 | 1 | 0.03 | 0 | 0.009901 | 0.066832 | 1 |
| 12 | `gallus` | Gallus | 1 | 0 | 0.0 | 0 | 0.009901 | 0.066832 | 1 |
| 13 | `otho` | Otho | 23 | 23 | 10.36 | 1 | 0.019802 | 0.094351 | 0 |
| 14 | `amen` | Amen | 8 | 8 | 3.32 | 1 | 0.019802 | 0.094351 | 0 |
| 15 | `tomb` | Tomb;Tomb | 3 | 3 | 0.4 | 1 | 0.019802 | 0.094351 | 0 |
| 16 | `isaac` | Isaac | 2 | 2 | 0.11 | 1 | 0.019802 | 0.094351 | 0 |
| 17 | `seal` | Seal;Seal;Seal | 16 | 17 | 5.67 | 1 | 0.019802 | 0.094351 | -1 |
| 18 | `torah` | Torah | 4 | 4 | 1.01 | 2 | 0.029703 | 0.104606 | 0 |
| 19 | `obal` | Obal | 3 | 3 | 0.55 | 2 | 0.029703 | 0.104606 | 0 |
| 20 | `admah` | Admah | 2 | 2 | 0.37 | 2 | 0.029703 | 0.104606 | 0 |
| 21 | `king` | King;King | 1 | 1 | 0.02 | 2 | 0.029703 | 0.104606 | 0 |
| 22 | `korea` | Korea | 1 | 1 | 0.02 | 2 | 0.029703 | 0.104606 | 0 |
| 23 | `bibi` | Bibi | 1 | 2 | 0.03 | 2 | 0.029703 | 0.104606 | -1 |
| 24 | `life` | Life | 5 | 5 | 1.75 | 3 | 0.039604 | 0.118812 | 0 |
| 25 | `image` | Image | 1 | 1 | 0.03 | 3 | 0.039604 | 0.118812 | 0 |
| 26 | `geta` | Geta | 8 | 9 | 3.38 | 3 | 0.039604 | 0.118812 | -1 |
| 27 | `teeth` | Teeth | 8 | 11 | 3.76 | 3 | 0.039604 | 0.118812 | -3 |
| 28 | `mash` | Mash | 6 | 7 | 2.47 | 4 | 0.049505 | 0.143211 | -1 |
| 29 | `edom` | Edom | 5 | 5 | 2.13 | 5 | 0.059406 | 0.165927 | 0 |
| 30 | `heart` | Heart;Heart | 5 | 7 | 1.82 | 6 | 0.069307 | 0.187129 | -2 |
| 31 | `rome` | Rome | 6 | 7 | 2.62 | 7 | 0.079208 | 0.19442 | -1 |
| 32 | `lion` | Lion | 5 | 6 | 2.01 | 7 | 0.079208 | 0.19442 | -1 |
| 33 | `death` | Death;Death | 4 | 5 | 1.47 | 7 | 0.079208 | 0.19442 | -1 |
| 34 | `hail` | Hail | 8 | 11 | 4.2 | 8 | 0.089109 | 0.212289 | -3 |
| 35 | `ahab` | Ahab | 4 | 6 | 1.47 | 9 | 0.09901 | 0.229137 | -2 |
| 36 | `isis` | ISIS | 4 | 5 | 1.8 | 10 | 0.108911 | 0.234726 | -1 |
| 37 | `aids` | AIDS | 6 | 10 | 3.14 | 10 | 0.108911 | 0.234726 | -4 |
| 38 | `india` | India | 1 | 1 | 0.11 | 11 | 0.118812 | 0.234726 | 0 |
| 39 | `light` | Light;Light | 1 | 1 | 0.11 | 11 | 0.118812 | 0.234726 | 0 |
| 40 | `sadat` | Sadat | 2 | 3 | 0.58 | 11 | 0.118812 | 0.234726 | -1 |
| 41 | `cedar` | Cedar | 1 | 2 | 0.12 | 11 | 0.118812 | 0.234726 | -1 |
| 42 | `eyes` | Eyes | 5 | 8 | 2.53 | 13 | 0.138614 | 0.267327 | -3 |
| 43 | `selah` | Selah | 2 | 4 | 0.86 | 15 | 0.158416 | 0.296384 | -2 |
| 44 | `sheba` | Sheba | 1 | 2 | 0.17 | 16 | 0.168317 | 0.296384 | -1 |
| 45 | `resen` | Resen | 2 | 4 | 0.74 | 16 | 0.168317 | 0.296384 | -2 |
| 46 | `heth` | Heth | 31 | 45 | 24.55 | 16 | 0.168317 | 0.296384 | -14 |
| 47 | `demon` | Demon | 1 | 2 | 0.18 | 17 | 0.178218 | 0.307142 | -1 |
| 48 | `bush` | Bush | 1 | 2 | 0.2 | 19 | 0.19802 | 0.327339 | -1 |
| 49 | `star` | Star | 8 | 12 | 5.49 | 19 | 0.19802 | 0.327339 | -4 |
| 50 | `yhwh` | YHWH;YHWH | 1 | 3 | 0.24 | 20 | 0.207921 | 0.336832 | -2 |

## Read

- This is a post-screen calibration over already observed bridge terms.
- `p_ge` is add-one empirical tail probability for the term count under
  shuffled insertion blocks.
- `q_ge` is Benjamini-Hochberg correction across the emitted bridge terms.
- It should guide follow-up priority, not convert bridge terms into claims.
