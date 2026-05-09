# KJVA Confirmatory Apocrypha Bridge Term Shuffled Controls (5000 Samples)

Status: term-level shuffled-insertion controls. This is not a claim report.

This control keeps the canonical prefix and apocrypha/deuterocanon block
length fixed, shuffles the block letters, and records bridge rows per
observed bridge term.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_term_shuffled_controls --canonical-label KJVA Confirmatory --canonical-config configs/example_ebible_engkjv_apocrypha.toml --observed reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv --terms terms/kjv_apocrypha_bridge_confirmatory_terms.csv --samples 5000 --seed 20260509 --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --resume-samples --sample-out reports/kjv_apocrypha_bridge_confirmatory_controls_5000/sample_summary.csv --term-sample-out reports/kjv_apocrypha_bridge_confirmatory_controls_5000/term_samples.csv --term-summary-out reports/kjv_apocrypha_bridge_confirmatory_controls_5000/term_summary.csv --markdown-out docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_CONTROLS_5000.md --manifest-out reports/kjv_apocrypha_bridge_confirmatory_controls_5000/manifest.json
```

## Summary

- corpus letters: 3816315
- canonical prefix letters: 2483327
- apocrypha block letters: 593090
- bridge terms reviewed: 15
- shuffled samples: 5000
- total shuffled min/mean/max: 15 / 35.0852 / 66
- terms with observed count above every shuffled sample: 3
- terms with BH q_ge <= 0.05: 15

## Top Terms

| Rank | Term | Concept | Observed | Shuffled max | Shuffled mean | Samples >= obs | p_ge | q_ge | Delta |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `seba` | Seba | 10 | 7 | 1.373 | 0 | 0.0002 | 0.001 | 3 |
| 2 | `nato` | NATO | 22 | 21 | 7.4332 | 0 | 0.0002 | 0.001 | 1 |
| 3 | `sign` | Sign | 6 | 5 | 0.454 | 0 | 0.0002 | 0.001 | 1 |
| 4 | `sidon` | Sidon | 3 | 3 | 0.1274 | 1 | 0.0004 | 0.0015 | 0 |
| 5 | `satan` | Satan | 5 | 5 | 0.6848 | 3 | 0.0008 | 0.001909 | 0 |
| 6 | `gallus` | Gallus | 1 | 1 | 0.0006 | 3 | 0.0008 | 0.001909 | 0 |
| 7 | `otho` | Otho | 23 | 29 | 10.1752 | 4 | 0.001 | 0.001909 | -6 |
| 8 | `moab` | Moab | 4 | 4 | 0.3812 | 5 | 0.0012 | 0.001909 | 0 |
| 9 | `sivan` | Sivan | 2 | 2 | 0.0142 | 5 | 0.0012 | 0.001909 | 0 |
| 10 | `seal` | Seal | 16 | 18 | 5.593 | 6 | 0.0014 | 0.001909 | -2 |
| 11 | `eber` | Eber | 10 | 13 | 2.089 | 6 | 0.0014 | 0.001909 | -3 |
| 12 | `house` | House | 3 | 3 | 0.2214 | 7 | 0.0016 | 0.002 | 0 |
| 13 | `noah` | Noah | 14 | 17 | 6.0594 | 33 | 0.006799 | 0.007845 | -3 |
| 14 | `tomb` | Tomb | 3 | 5 | 0.374 | 42 | 0.008598 | 0.008998 | -2 |
| 15 | `abib` | Abib | 2 | 2 | 0.1048 | 44 | 0.008998 | 0.008998 | 0 |

## Read

- This is a post-screen calibration over already observed bridge terms.
- `p_ge` is add-one empirical tail probability for the term count under
  shuffled insertion blocks.
- `q_ge` is Benjamini-Hochberg correction across the emitted bridge terms.
- It should guide follow-up priority, not convert bridge terms into claims.
