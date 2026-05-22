# KJVA Prospective Apocrypha Bridge Term Shuffled Controls (5000 Samples)

Status: term-level shuffled-insertion controls. This is not a claim report.

This control keeps the canonical prefix and apocrypha/deuterocanon block
length fixed, shuffles the block letters, and records bridge rows per
registered term.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_term_shuffled_controls --canonical-label KJVA Prospective --canonical-config configs/example_ebible_engkjv_apocrypha.toml --observed reports/kjv_apocrypha_bridge_prospective/bridge_candidates.csv --terms terms/kjv_apocrypha_bridge_prospective_terms.csv --samples 5000 --seed 20260522 --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --resume-samples --sample-out reports/kjv_apocrypha_bridge_prospective/sample_summary.csv --term-sample-out reports/kjv_apocrypha_bridge_prospective/term_samples.csv --term-summary-out reports/kjv_apocrypha_bridge_prospective/term_summary.csv --markdown-out docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md --manifest-out reports/kjv_apocrypha_bridge_prospective/manifest.json
```

## Summary

- corpus letters: 3816315
- canonical prefix letters: 2483327
- apocrypha block letters: 593090
- bridge terms reviewed: 7
- shuffled samples: 5000
- total shuffled min/mean/max: 0 / 0.1022 / 2
- terms with observed count above every shuffled sample: 0
- terms with BH q_ge <= 0.05: 0

## Top Terms

| Rank | Term | Concept | Observed | Shuffled max | Shuffled mean | Samples >= obs | p_ge | q_ge | Delta |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `tobit` | Tobit | 1 | 2 | 0.1016 | 485 | 0.097181 | 0.680267 | -1 |
| 2 | `antiochus` | Antiochus | 0 | 0 | 0.0 | 5000 | 1.0 | 1.0 | 0 |
| 3 | `eleazar` | Eleazar | 0 | 0 | 0.0 | 5000 | 1.0 | 1.0 | 0 |
| 4 | `holofernes` | Holofernes | 0 | 0 | 0.0 | 5000 | 1.0 | 1.0 | 0 |
| 5 | `judasmaccabeus` | Judas Maccabeus | 0 | 0 | 0.0 | 5000 | 1.0 | 1.0 | 0 |
| 6 | `mattathias` | Mattathias | 0 | 0 | 0.0 | 5000 | 1.0 | 1.0 | 0 |
| 7 | `judith` | Judith | 0 | 1 | 0.0006 | 5000 | 1.0 | 1.0 | -1 |

## Read

- This is a prospective control run over registered terms.
- `p_ge` is add-one empirical tail probability for the term count under
  shuffled insertion blocks.
- `q_ge` is Benjamini-Hochberg correction across the registered terms.
- It should guide follow-up priority, not convert bridge terms into claims.
