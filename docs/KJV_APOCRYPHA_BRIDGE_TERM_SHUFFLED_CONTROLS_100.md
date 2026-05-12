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
- bridge terms reviewed: 114
- shuffled samples: 100
- total shuffled min/mean/max: 151 / 186.38 / 236
- terms with observed count above every shuffled sample: 45
- terms with BH q_ge <= 0.05: 50

## Top Terms

| Rank | Term | Concept | Observed | Shuffled max | Shuffled mean | Samples >= obs | p_ge | q_ge | Delta |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `tree` | Tree;Tree | 26 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 26 |
| 2 | `seed` | Seed;Seed;Seed | 21 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 21 |
| 3 | `hits` | Hits | 17 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 17 |
| 4 | `eden` | Eden | 15 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 15 |
| 5 | `leah` | Leah | 11 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 11 |
| 6 | `gate` | Gate | 10 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 10 |
| 7 | `shot` | Shot | 10 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 10 |
| 8 | `nato` | NATO;NATO | 22 | 13 | 7.12 | 0 | 0.009901 | 0.025083 | 9 |
| 9 | `soot` | Soot | 9 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 9 |
| 10 | `thin` | Thin | 9 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 9 |
| 11 | `lane` | Lane | 7 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 7 |
| 12 | `seba` | Seba;Seba | 10 | 5 | 1.14 | 0 | 0.009901 | 0.025083 | 5 |
| 13 | `iron` | Iron | 5 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 5 |
| 14 | `eber` | Eber;Eber | 10 | 6 | 1.84 | 0 | 0.009901 | 0.025083 | 4 |
| 15 | `amos` | Amos | 4 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 4 |
| 16 | `haiti` | Haiti | 4 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 4 |
| 17 | `rent` | Rent | 4 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 4 |
| 18 | `wine` | Wine;Wine;Wine | 4 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 4 |
| 19 | `sign` | Sign;Sign | 6 | 3 | 0.48 | 0 | 0.009901 | 0.025083 | 3 |
| 20 | `aaron` | Aaron;Aaron | 3 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 3 |
| 21 | `obed` | Obed;Obed;Obed | 3 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 3 |
| 22 | `ruth` | Ruth | 3 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 3 |
| 23 | `noah` | Noah;Noah | 14 | 12 | 6.36 | 0 | 0.009901 | 0.025083 | 2 |
| 24 | `satan` | Satan;Satan | 5 | 3 | 0.74 | 0 | 0.009901 | 0.025083 | 2 |
| 25 | `moab` | Moab;Moab | 4 | 2 | 0.47 | 0 | 0.009901 | 0.025083 | 2 |
| 26 | `aloes` | Aloes | 2 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 2 |
| 27 | `annas` | Annas;Annas;Annas | 2 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 2 |
| 28 | `ehyeh` | Ehyeh | 2 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 2 |
| 29 | `hannah` | Hannah | 2 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 2 |
| 30 | `water` | Water;Water;Water | 2 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 2 |
| 31 | `house` | House;House | 3 | 2 | 0.3 | 0 | 0.009901 | 0.025083 | 1 |
| 32 | `sidon` | Sidon;Sidon;Sidon | 3 | 2 | 0.21 | 0 | 0.009901 | 0.025083 | 1 |
| 33 | `abib` | Abib;Abib | 2 | 1 | 0.12 | 0 | 0.009901 | 0.025083 | 1 |
| 34 | `sivan` | Sivan;Sivan | 2 | 1 | 0.03 | 0 | 0.009901 | 0.025083 | 1 |
| 35 | `allah` | Allah | 1 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 1 |
| 36 | `altar` | Altar | 1 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 1 |
| 37 | `baal` | Baal | 1 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 1 |
| 38 | `bread` | Bread;Bread;Bread | 1 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 1 |
| 39 | `gallus` | Gallus;Gallus | 1 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 1 |
| 40 | `gold` | Gold | 1 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 1 |
| 41 | `hosea` | Hosea | 1 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 1 |
| 42 | `joel` | Joel | 1 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 1 |
| 43 | `louis` | Louis | 1 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 1 |
| 44 | `tobit` | Tobit | 1 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 1 |
| 45 | `vine` | Vine | 1 | 0 | 0.0 | 0 | 0.009901 | 0.025083 | 1 |
| 46 | `otho` | Otho;Otho | 23 | 23 | 10.36 | 1 | 0.019802 | 0.045149 | 0 |
| 47 | `amen` | Amen | 8 | 8 | 3.32 | 1 | 0.019802 | 0.045149 | 0 |
| 48 | `tomb` | Tomb;Tomb;Tomb | 3 | 3 | 0.4 | 1 | 0.019802 | 0.045149 | 0 |
| 49 | `isaac` | Isaac;Isaac | 2 | 2 | 0.11 | 1 | 0.019802 | 0.045149 | 0 |
| 50 | `seal` | Seal;Seal;Seal;Seal;Seal | 16 | 17 | 5.67 | 1 | 0.019802 | 0.045149 | -1 |

## Read

- This is a post-screen calibration over already observed bridge terms.
- `p_ge` is add-one empirical tail probability for the term count under
  shuffled insertion blocks.
- `q_ge` is Benjamini-Hochberg correction across the emitted bridge terms.
- It should guide follow-up priority, not convert bridge terms into claims.
