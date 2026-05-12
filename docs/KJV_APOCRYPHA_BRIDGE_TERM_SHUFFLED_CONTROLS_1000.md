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
- bridge terms reviewed: 114
- shuffled samples: 1000
- total shuffled min/mean/max: 130 / 184.306 / 248
- terms with observed count above every shuffled sample: 41
- terms with BH q_ge <= 0.05: 53

## Top Terms

| Rank | Term | Concept | Observed | Shuffled max | Shuffled mean | Samples >= obs | p_ge | q_ge | Delta |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `tree` | Tree;Tree | 26 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 26 |
| 2 | `seed` | Seed;Seed;Seed | 21 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 21 |
| 3 | `hits` | Hits | 17 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 17 |
| 4 | `eden` | Eden | 15 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 15 |
| 5 | `leah` | Leah | 11 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 11 |
| 6 | `gate` | Gate | 10 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 10 |
| 7 | `shot` | Shot | 10 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 10 |
| 8 | `soot` | Soot | 9 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 9 |
| 9 | `thin` | Thin | 9 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 9 |
| 10 | `lane` | Lane | 7 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 7 |
| 11 | `iron` | Iron | 5 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 5 |
| 12 | `nato` | NATO;NATO | 22 | 18 | 7.431 | 0 | 0.000999 | 0.002778 | 4 |
| 13 | `amos` | Amos | 4 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 4 |
| 14 | `haiti` | Haiti | 4 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 4 |
| 15 | `rent` | Rent | 4 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 4 |
| 16 | `wine` | Wine;Wine;Wine | 4 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 4 |
| 17 | `seba` | Seba;Seba | 10 | 7 | 1.335 | 0 | 0.000999 | 0.002778 | 3 |
| 18 | `aaron` | Aaron;Aaron | 3 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 3 |
| 19 | `obed` | Obed;Obed;Obed | 3 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 3 |
| 20 | `ruth` | Ruth | 3 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 3 |
| 21 | `sign` | Sign;Sign | 6 | 4 | 0.445 | 0 | 0.000999 | 0.002778 | 2 |
| 22 | `aloes` | Aloes | 2 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 2 |
| 23 | `annas` | Annas;Annas;Annas | 2 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 2 |
| 24 | `ehyeh` | Ehyeh | 2 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 2 |
| 25 | `hannah` | Hannah | 2 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 2 |
| 26 | `water` | Water;Water;Water | 2 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 2 |
| 27 | `eber` | Eber;Eber | 10 | 9 | 2.043 | 0 | 0.000999 | 0.002778 | 1 |
| 28 | `satan` | Satan;Satan | 5 | 4 | 0.707 | 0 | 0.000999 | 0.002778 | 1 |
| 29 | `moab` | Moab;Moab | 4 | 3 | 0.359 | 0 | 0.000999 | 0.002778 | 1 |
| 30 | `sidon` | Sidon;Sidon;Sidon | 3 | 2 | 0.117 | 0 | 0.000999 | 0.002778 | 1 |
| 31 | `sivan` | Sivan;Sivan | 2 | 1 | 0.015 | 0 | 0.000999 | 0.002778 | 1 |
| 32 | `allah` | Allah | 1 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 1 |
| 33 | `altar` | Altar | 1 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 1 |
| 34 | `baal` | Baal | 1 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 1 |
| 35 | `bread` | Bread;Bread;Bread | 1 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 1 |
| 36 | `gold` | Gold | 1 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 1 |
| 37 | `hosea` | Hosea | 1 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 1 |
| 38 | `joel` | Joel | 1 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 1 |
| 39 | `louis` | Louis | 1 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 1 |
| 40 | `tobit` | Tobit | 1 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 1 |
| 41 | `vine` | Vine | 1 | 0 | 0.0 | 0 | 0.000999 | 0.002778 | 1 |
| 42 | `gallus` | Gallus;Gallus | 1 | 1 | 0.001 | 1 | 0.001998 | 0.005423 | 0 |
| 43 | `otho` | Otho;Otho | 23 | 23 | 10.046 | 2 | 0.002997 | 0.007765 | 0 |
| 44 | `seal` | Seal;Seal;Seal;Seal;Seal | 16 | 17 | 5.682 | 2 | 0.002997 | 0.007765 | -1 |
| 45 | `house` | House;House | 3 | 3 | 0.221 | 3 | 0.003996 | 0.010123 | 0 |
| 46 | `tomb` | Tomb;Tomb;Tomb | 3 | 3 | 0.387 | 6 | 0.006993 | 0.016962 | 0 |
| 47 | `noah` | Noah;Noah | 14 | 17 | 6.13 | 6 | 0.006993 | 0.016962 | -3 |
| 48 | `abib` | Abib;Abib | 2 | 2 | 0.097 | 7 | 0.007992 | 0.018981 | 0 |
| 49 | `isaac` | Isaac;Isaac | 2 | 2 | 0.16 | 11 | 0.011988 | 0.02789 | 0 |
| 50 | `amen` | Amen | 8 | 10 | 3.305 | 15 | 0.015984 | 0.036444 | -2 |

## Read

- This is a post-screen calibration over already observed bridge terms.
- `p_ge` is add-one empirical tail probability for the term count under
  shuffled insertion blocks.
- `q_ge` is Benjamini-Hochberg correction across the emitted bridge terms.
- It should guide follow-up priority, not convert bridge terms into claims.
