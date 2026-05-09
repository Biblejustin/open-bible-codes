# KJVA Apocrypha Bridge Term Shuffled Controls (300 Samples)

Status: term-level shuffled-insertion controls. This is not a claim report.

This control keeps the canonical prefix and apocrypha/deuterocanon block
length fixed, shuffles the block letters, and records bridge rows per
observed bridge term.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_term_shuffled_controls --canonical-label KJVA --canonical-config configs/example_ebible_engkjv_apocrypha.toml --observed reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv --terms terms/english_search_terms.csv --samples 300 --seed 20260509 --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --resume-samples --sample-out reports/kjv_apocrypha_bridge_term_shuffled_controls_300/sample_summary.csv --term-sample-out reports/kjv_apocrypha_bridge_term_shuffled_controls_300/term_samples.csv --term-summary-out reports/kjv_apocrypha_bridge_term_shuffled_controls_300/term_summary.csv --markdown-out docs/KJV_APOCRYPHA_BRIDGE_TERM_SHUFFLED_CONTROLS_300.md --manifest-out reports/kjv_apocrypha_bridge_term_shuffled_controls_300/manifest.json
```

## Summary

- corpus letters: 3816315
- canonical prefix letters: 2483327
- apocrypha block letters: 593090
- bridge terms reviewed: 81
- shuffled samples: 300
- total shuffled min/mean/max: 149 / 185.156667 / 236
- terms with observed count above every shuffled sample: 10
- terms with BH q_ge <= 0.05: 14

## Top Terms

| Rank | Term | Concept | Observed | Shuffled max | Shuffled mean | Samples >= obs | p_ge | q_ge | Delta |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `nato` | NATO | 22 | 18 | 7.426667 | 0 | 0.003322 | 0.026908 | 4 |
| 2 | `eber` | Eber | 10 | 6 | 1.883333 | 0 | 0.003322 | 0.026908 | 4 |
| 3 | `seba` | Seba | 10 | 6 | 1.343333 | 0 | 0.003322 | 0.026908 | 4 |
| 4 | `sign` | Sign | 6 | 3 | 0.406667 | 0 | 0.003322 | 0.026908 | 3 |
| 5 | `noah` | Noah | 14 | 13 | 6.353333 | 0 | 0.003322 | 0.026908 | 1 |
| 6 | `satan` | Satan | 5 | 4 | 0.686667 | 0 | 0.003322 | 0.026908 | 1 |
| 7 | `moab` | Moab | 4 | 3 | 0.396667 | 0 | 0.003322 | 0.026908 | 1 |
| 8 | `sidon` | Sidon;Sidon | 3 | 2 | 0.14 | 0 | 0.003322 | 0.026908 | 1 |
| 9 | `sivan` | Sivan | 2 | 1 | 0.02 | 0 | 0.003322 | 0.026908 | 1 |
| 10 | `gallus` | Gallus | 1 | 0 | 0.0 | 0 | 0.003322 | 0.026908 | 1 |
| 11 | `otho` | Otho | 23 | 23 | 10.216667 | 1 | 0.006645 | 0.038446 | 0 |
| 12 | `house` | House | 3 | 3 | 0.263333 | 1 | 0.006645 | 0.038446 | 0 |
| 13 | `abib` | Abib | 2 | 2 | 0.103333 | 1 | 0.006645 | 0.038446 | 0 |
| 14 | `seal` | Seal;Seal;Seal | 16 | 17 | 5.596667 | 1 | 0.006645 | 0.038446 | -1 |
| 15 | `tomb` | Tomb;Tomb | 3 | 3 | 0.416667 | 2 | 0.009967 | 0.050458 | 0 |
| 16 | `isaac` | Isaac | 2 | 2 | 0.136667 | 2 | 0.009967 | 0.050458 | 0 |
| 17 | `amen` | Amen | 8 | 8 | 3.25 | 4 | 0.016611 | 0.079147 | 0 |
| 18 | `obal` | Obal | 3 | 3 | 0.523333 | 5 | 0.019934 | 0.089703 | 0 |
| 19 | `torah` | Torah | 4 | 4 | 0.99 | 6 | 0.023256 | 0.094187 | 0 |
| 20 | `mash` | Mash | 6 | 8 | 2.296667 | 6 | 0.023256 | 0.094187 | -2 |
| 21 | `life` | Life | 5 | 6 | 1.73 | 9 | 0.033223 | 0.128146 | -1 |
| 22 | `king` | King;King | 1 | 1 | 0.033333 | 10 | 0.036545 | 0.128702 | 0 |
| 23 | `geta` | Geta | 8 | 10 | 3.343333 | 10 | 0.036545 | 0.128702 | -2 |
| 24 | `edom` | Edom | 5 | 7 | 2.086667 | 11 | 0.039867 | 0.129169 | -2 |
| 25 | `heart` | Heart;Heart | 5 | 7 | 1.67 | 11 | 0.039867 | 0.129169 | -2 |
| 26 | `image` | Image | 1 | 1 | 0.04 | 12 | 0.043189 | 0.129567 | 0 |
| 27 | `bibi` | Bibi | 1 | 2 | 0.046667 | 12 | 0.043189 | 0.129567 | -1 |
| 28 | `lion` | Lion | 5 | 6 | 2.016667 | 13 | 0.046512 | 0.129913 | -1 |
| 29 | `admah` | Admah | 2 | 3 | 0.41 | 13 | 0.046512 | 0.129913 | -1 |
| 30 | `korea` | Korea | 1 | 2 | 0.053333 | 14 | 0.049834 | 0.130211 | -1 |
| 31 | `teeth` | Teeth | 8 | 11 | 3.863333 | 14 | 0.049834 | 0.130211 | -3 |
| 32 | `ahab` | Ahab | 4 | 8 | 1.333333 | 16 | 0.056478 | 0.14296 | -4 |
| 33 | `rome` | Rome | 6 | 9 | 2.496667 | 19 | 0.066445 | 0.163092 | -3 |
| 34 | `death` | Death;Death | 4 | 6 | 1.47 | 20 | 0.069767 | 0.16621 | -2 |
| 35 | `hail` | Hail | 8 | 12 | 4.096667 | 23 | 0.079734 | 0.184527 | -4 |
| 36 | `light` | Light;Light | 1 | 1 | 0.083333 | 25 | 0.086379 | 0.194353 | 0 |
| 37 | `isis` | ISIS | 4 | 7 | 1.693333 | 27 | 0.093023 | 0.203645 | -3 |
| 38 | `aids` | AIDS | 6 | 10 | 3.046667 | 30 | 0.10299 | 0.219531 | -4 |
| 39 | `cedar` | Cedar | 1 | 2 | 0.106667 | 31 | 0.106312 | 0.220802 | -1 |
| 40 | `sadat` | Sadat | 2 | 4 | 0.59 | 38 | 0.129568 | 0.262375 | -2 |
| 41 | `india` | India | 1 | 2 | 0.14 | 40 | 0.136213 | 0.269104 | -1 |
| 42 | `demon` | Demon | 1 | 2 | 0.146667 | 42 | 0.142857 | 0.27522 | -1 |
| 43 | `heth` | Heth | 31 | 45 | 24.18 | 43 | 0.146179 | 0.27522 | -14 |
| 44 | `resen` | Resen | 2 | 5 | 0.646667 | 44 | 0.149502 | 0.27522 | -3 |
| 45 | `eyes` | Eyes | 5 | 8 | 2.7 | 47 | 0.159468 | 0.287042 | -3 |
| 46 | `fire` | Fire | 5 | 10 | 2.88 | 54 | 0.182724 | 0.321753 | -5 |
| 47 | `sheba` | Sheba | 1 | 2 | 0.21 | 56 | 0.189369 | 0.325166 | -1 |
| 48 | `star` | Star | 8 | 13 | 5.406667 | 57 | 0.192691 | 0.325166 | -5 |
| 49 | `word` | Word | 2 | 3 | 0.82 | 60 | 0.202658 | 0.332421 | -1 |
| 50 | `lamb` | Lamb;Lamb | 1 | 2 | 0.223333 | 62 | 0.209302 | 0.332421 | -1 |

## Read

- This is a post-screen calibration over already observed bridge terms.
- `p_ge` is add-one empirical tail probability for the term count under
  shuffled insertion blocks.
- `q_ge` is Benjamini-Hochberg correction across the emitted bridge terms.
- It should guide follow-up priority, not convert bridge terms into claims.
