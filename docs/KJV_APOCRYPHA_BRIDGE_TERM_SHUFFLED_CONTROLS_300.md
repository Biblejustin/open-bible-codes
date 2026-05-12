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
- bridge terms reviewed: 114
- shuffled samples: 300
- total shuffled min/mean/max: 149 / 185.156667 / 236
- terms with observed count above every shuffled sample: 43
- terms with BH q_ge <= 0.05: 51

## Top Terms

| Rank | Term | Concept | Observed | Shuffled max | Shuffled mean | Samples >= obs | p_ge | q_ge | Delta |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `tree` | Tree;Tree | 26 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 26 |
| 2 | `seed` | Seed;Seed;Seed | 21 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 21 |
| 3 | `hits` | Hits | 17 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 17 |
| 4 | `eden` | Eden | 15 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 15 |
| 5 | `leah` | Leah | 11 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 11 |
| 6 | `gate` | Gate | 10 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 10 |
| 7 | `shot` | Shot | 10 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 10 |
| 8 | `soot` | Soot | 9 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 9 |
| 9 | `thin` | Thin | 9 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 9 |
| 10 | `lane` | Lane | 7 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 7 |
| 11 | `iron` | Iron | 5 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 5 |
| 12 | `nato` | NATO;NATO | 22 | 18 | 7.426667 | 0 | 0.003322 | 0.008807 | 4 |
| 13 | `eber` | Eber;Eber | 10 | 6 | 1.883333 | 0 | 0.003322 | 0.008807 | 4 |
| 14 | `seba` | Seba;Seba | 10 | 6 | 1.343333 | 0 | 0.003322 | 0.008807 | 4 |
| 15 | `amos` | Amos | 4 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 4 |
| 16 | `haiti` | Haiti | 4 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 4 |
| 17 | `rent` | Rent | 4 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 4 |
| 18 | `wine` | Wine;Wine;Wine | 4 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 4 |
| 19 | `sign` | Sign;Sign | 6 | 3 | 0.406667 | 0 | 0.003322 | 0.008807 | 3 |
| 20 | `aaron` | Aaron;Aaron | 3 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 3 |
| 21 | `obed` | Obed;Obed;Obed | 3 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 3 |
| 22 | `ruth` | Ruth | 3 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 3 |
| 23 | `aloes` | Aloes | 2 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 2 |
| 24 | `annas` | Annas;Annas;Annas | 2 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 2 |
| 25 | `ehyeh` | Ehyeh | 2 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 2 |
| 26 | `hannah` | Hannah | 2 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 2 |
| 27 | `water` | Water;Water;Water | 2 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 2 |
| 28 | `noah` | Noah;Noah | 14 | 13 | 6.353333 | 0 | 0.003322 | 0.008807 | 1 |
| 29 | `satan` | Satan;Satan | 5 | 4 | 0.686667 | 0 | 0.003322 | 0.008807 | 1 |
| 30 | `moab` | Moab;Moab | 4 | 3 | 0.396667 | 0 | 0.003322 | 0.008807 | 1 |
| 31 | `sidon` | Sidon;Sidon;Sidon | 3 | 2 | 0.14 | 0 | 0.003322 | 0.008807 | 1 |
| 32 | `sivan` | Sivan;Sivan | 2 | 1 | 0.02 | 0 | 0.003322 | 0.008807 | 1 |
| 33 | `allah` | Allah | 1 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 1 |
| 34 | `altar` | Altar | 1 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 1 |
| 35 | `baal` | Baal | 1 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 1 |
| 36 | `bread` | Bread;Bread;Bread | 1 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 1 |
| 37 | `gallus` | Gallus;Gallus | 1 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 1 |
| 38 | `gold` | Gold | 1 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 1 |
| 39 | `hosea` | Hosea | 1 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 1 |
| 40 | `joel` | Joel | 1 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 1 |
| 41 | `louis` | Louis | 1 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 1 |
| 42 | `tobit` | Tobit | 1 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 1 |
| 43 | `vine` | Vine | 1 | 0 | 0.0 | 0 | 0.003322 | 0.008807 | 1 |
| 44 | `otho` | Otho;Otho | 23 | 23 | 10.216667 | 1 | 0.006645 | 0.016118 | 0 |
| 45 | `house` | House;House | 3 | 3 | 0.263333 | 1 | 0.006645 | 0.016118 | 0 |
| 46 | `abib` | Abib;Abib | 2 | 2 | 0.103333 | 1 | 0.006645 | 0.016118 | 0 |
| 47 | `seal` | Seal;Seal;Seal;Seal;Seal | 16 | 17 | 5.596667 | 1 | 0.006645 | 0.016118 | -1 |
| 48 | `tomb` | Tomb;Tomb;Tomb | 3 | 3 | 0.416667 | 2 | 0.009967 | 0.023189 | 0 |
| 49 | `isaac` | Isaac;Isaac | 2 | 2 | 0.136667 | 2 | 0.009967 | 0.023189 | 0 |
| 50 | `amen` | Amen | 8 | 8 | 3.25 | 4 | 0.016611 | 0.037873 | 0 |

## Read

- This is a post-screen calibration over already observed bridge terms.
- `p_ge` is add-one empirical tail probability for the term count under
  shuffled insertion blocks.
- `q_ge` is Benjamini-Hochberg correction across the emitted bridge terms.
- It should guide follow-up priority, not convert bridge terms into claims.
