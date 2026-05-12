# KJVA Apocrypha Bridge Term Review

Status: term-level review aid. This is not a claim report.

This report ranks KJVA apocrypha/deuterocanon bridge terms by observed
bridge rows, same-length non-Bible term-control counts, and surface-context
buckets. The 250-sample shuffled-insertion control is total-level, not
term-level, so it is cited as background calibration. The separate
1000-sample term-level shuffled control is summarized below as
post-screen per-term calibration.

## Reproduce

```bash
python3 -m scripts.summarize_kjv_apocrypha_bridge_terms --candidates reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv --context reports/kjv_apocrypha_bridge_context/context.csv --controls reports/kjv_apocrypha_bridge_controls/term_summary.csv --shuffled-summary reports/kjv_apocrypha_bridge_shuffled_controls_250/summary.csv --term-shuffled-summary reports/kjv_apocrypha_bridge_term_shuffled_controls_1000/term_summary.csv --out reports/kjv_apocrypha_bridge_term_review/term_review.csv --markdown-out docs/KJV_APOCRYPHA_BRIDGE_TERM_REVIEW.md --manifest-out reports/kjv_apocrypha_bridge_term_review/manifest.json
```

## Summary

- bridge terms reviewed: 114
- terms above all same-length non-Bible term controls: 71
- terms with any center/span context bucket beyond hidden_path_only: 72
- 250-sample shuffled total rows: observed 350; shuffled min/mean/max 149 / 185.604 / 236; p_ge 0.003984
- 1000-sample term-level shuffled controls: 41 of 114 terms above every shuffled sample; 58 terms with unadjusted p_ge <= 0.05; 53 terms with BH q_ge <= 0.05

## Top Terms

| Rank | Term | Concept | Observed | Control max | Delta | Context hits | Sample refs |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `nato` | NATO | 22 | 4 | 18 | 3 | MAL 4:6->MAL 4:6->TOB 1:1; MAL 4:5->MAL 4:6->TOB 1:1; MAT 1:3->MAT 1:2->2ES 16:78; MAT 1:1->2ES 16:77->2ES 16:76; MAT 1:4->MAT 1:2->2ES 16:77 |
| 2 | `seed` | Seed | 21 | 8 | 13 | 15 | TOB 1:1->MAL 4:6->MAL 4:5; MAL 4:6->TOB 1:1->TOB 1:2; TOB 1:2->TOB 1:1->MAL 4:6; MAT 1:1->2ES 16:77->2ES 16:77; TOB 1:2->TOB 1:1->MAL 4:5 |
| 3 | `otho` | Otho | 23 | 12 | 11 | 2 | MAL 4:6->MAL 4:6->TOB 1:1; TOB 1:1->MAL 4:6->MAL 4:5; TOB 1:1->MAL 4:6->MAL 4:4; 2ES 16:78->MAT 1:2->MAT 1:4; TOB 1:2->TOB 1:1->MAL 4:5 |
| 4 | `hits` | Hits | 17 | 8 | 9 | 15 | TOB 1:2->TOB 1:1->MAL 4:6; MAL 4:6->TOB 1:1->TOB 1:2; TOB 1:1->MAL 4:6->MAL 4:5; 2ES 16:75->2ES 16:77->MAT 1:1; 2ES 16:76->2ES 16:77->MAT 1:2 |
| 5 | `eden` | Eden | 15 | 6 | 9 | 5 | 2ES 16:78->2ES 16:78->MAT 1:1; MAL 4:6->TOB 1:1->TOB 1:2; MAT 1:2->2ES 16:77->2ES 16:76; MAT 1:5->MAT 1:2->2ES 16:77; MAL 4:4->MAL 4:6->TOB 1:2 |
| 6 | `seba` | Seba | 10 | 2 | 8 | 0 | MAL 4:6->TOB 1:1->TOB 1:1; 2ES 16:76->2ES 16:77->MAT 1:3; 2ES 16:78->MAT 1:4->MAT 1:7; 2ES 16:78->MAT 1:4->MAT 1:8; 2ES 16:76->MAT 1:2->MAT 1:6 |
| 7 | `eber` | Eber | 10 | 3 | 7 | 3 | MAT 1:3->MAT 1:1->2ES 16:77; 2ES 16:77->2ES 16:77->MAT 1:1; 2ES 16:78->MAT 1:2->MAT 1:5; TOB 1:2->TOB 1:1->MAL 4:5; MAT 1:5->MAT 1:2->2ES 16:77 |
| 8 | `seal` | Seal | 16 | 10 | 6 | 0 | MAL 4:5->MAL 4:6->TOB 1:1; MAL 4:6->TOB 1:1->TOB 1:2; 2ES 16:78->MAT 1:2->MAT 1:4; TOB 1:2->MAL 4:6->MAL 4:5; MAL 4:4->MAL 4:6->TOB 1:2 |
| 9 | `amen` | Amen | 8 | 2 | 6 | 0 | MAL 4:6->TOB 1:1->TOB 1:2; MAT 1:2->2ES 16:77->2ES 16:75; MAT 1:6->MAT 1:2->2ES 16:77; MAT 1:4->2ES 16:78->2ES 16:76; MAT 1:7->MAT 1:2->2ES 16:77 |
| 10 | `sign` | Sign | 6 | 0 | 6 | 1 | 2ES 16:78->MAT 1:2->MAT 1:3; TOB 1:3->TOB 1:2->MAL 4:6; 2ES 16:76->MAT 1:1->MAT 1:5; 2ES 16:76->2ES 16:78->MAT 1:5; MAT 1:1->2ES 16:76->2ES 16:73 |
| 11 | `noah` | Noah | 14 | 9 | 5 | 4 | TOB 1:1->MAL 4:6->MAL 4:6; 2ES 16:78->MAT 1:1->MAT 1:2; TOB 1:1->MAL 4:6->MAL 4:5; MAT 1:2->2ES 16:78->2ES 16:77; TOB 1:2->MAL 4:6->MAL 4:4 |
| 12 | `gate` | Gate | 10 | 5 | 5 | 9 | MAT 1:3->MAT 1:1->2ES 16:77; TOB 1:1->MAL 4:6->MAL 4:5; TOB 1:2->TOB 1:1->MAL 4:5; TOB 1:1->MAL 4:5->MAL 4:3; MAT 1:6->MAT 1:2->2ES 16:77 |
| 13 | `geta` | Geta | 8 | 3 | 5 | 0 | 2ES 16:75->2ES 16:77->MAT 1:1; MAL 4:5->TOB 1:1->TOB 1:3; MAT 1:5->MAT 1:1->2ES 16:77; MAT 1:5->MAT 1:1->2ES 16:76; MAT 1:3->2ES 16:77->2ES 16:74 |
| 14 | `hail` | Hail | 8 | 3 | 5 | 5 | MAT 1:1->2ES 16:76->2ES 16:74; TOB 1:3->TOB 1:2->MAL 4:5; 2ES 16:76->2ES 16:78->MAT 1:4; MAL 4:6->TOB 1:2->TOB 1:4; MAL 4:3->MAL 4:5->TOB 1:2 |
| 15 | `satan` | Satan | 5 | 0 | 5 | 0 | MAT 1:3->MAT 1:1->2ES 16:77; MAL 4:6->TOB 1:1->TOB 1:2; 2ES 16:70->2ES 16:76->MAT 1:3; MAL 4:1->MAL 4:6->TOB 1:4; 2ES 16:78->MAT 1:7->MAT 1:15 |
| 16 | `mash` | Mash | 6 | 2 | 4 | 2 | MAT 1:4->MAT 1:2->2ES 16:77; MAL 4:6->TOB 1:2->TOB 1:3; 2ES 16:76->2ES 16:77->MAT 1:1; TOB 1:3->TOB 1:1->MAL 4:4; MAT 1:1->2ES 16:76->2ES 16:72 |
| 17 | `moab` | Moab | 4 | 0 | 4 | 0 | MAT 1:8->MAT 1:3->2ES 16:77; 2ES 16:72->2ES 16:76->MAT 1:2; 2ES 16:76->MAT 1:1->MAT 1:6; 2ES 16:77->MAT 1:3->MAT 1:9 |
| 18 | `soot` | Soot | 9 | 6 | 3 | 9 | TOB 1:2->TOB 1:1->MAL 4:6; TOB 1:2->MAL 4:6->MAL 4:4; MAL 4:4->MAL 4:6->TOB 1:1; TOB 1:1->MAL 4:5->MAL 4:2; TOB 1:4->TOB 1:2->MAL 4:4 |
| 19 | `thin` | Thin | 9 | 6 | 3 | 7 | 2ES 16:78->2ES 16:78->MAT 1:1; MAT 1:2->2ES 16:77->2ES 16:76; TOB 1:1->MAL 4:5->MAL 4:3; MAT 1:3->2ES 16:77->2ES 16:76; MAL 4:6->TOB 1:2->TOB 1:3 |
| 20 | `teeth` | Teeth | 8 | 5 | 3 | 4 | MAL 4:6->TOB 1:1->TOB 1:1; MAL 4:3->MAL 4:6->TOB 1:3; TOB 1:4->TOB 1:2->MAL 4:6; TOB 1:1->MAL 4:3->MAL 3:18; MAL 4:1->MAL 4:5->TOB 1:2 |
| 21 | `edom` | Edom | 5 | 2 | 3 | 1 | 2ES 16:77->2ES 16:78->MAT 1:1; 2ES 16:78->MAT 1:3->MAT 1:7; 2ES 16:75->2ES 16:77->MAT 1:3; MAT 1:1->2ES 16:76->2ES 16:72; MAL 4:3->MAL 4:6->TOB 1:3 |
| 22 | `amos` | Amos | 4 | 1 | 3 | 0 | MAT 1:4->2ES 16:78->2ES 16:76; MAT 1:6->MAT 1:2->2ES 16:77; MAT 1:8->MAT 1:3->2ES 16:77; 2ES 16:78->MAT 1:5->MAT 1:10 |
| 23 | `aaron` | Aaron | 3 | 0 | 3 | 2 | TOB 1:1->MAL 4:6->MAL 4:4; MAT 1:9->MAT 1:3->2ES 16:77; MAT 1:7->2ES 16:78->2ES 16:73 |
| 24 | `house` | House | 3 | 0 | 3 | 2 | 2ES 16:78->MAT 1:2->MAT 1:4; MAT 1:2->2ES 16:77->2ES 16:74; MAL 4:6->TOB 1:3->TOB 1:5 |
| 25 | `sidon` | Sidon | 3 | 0 | 3 | 1 | MAT 1:1->2ES 16:77->2ES 16:76; 2ES 16:76->MAT 1:2->MAT 1:7; MAL 4:1->MAL 4:5->TOB 1:3 |
| 26 | `tomb` | Tomb | 3 | 0 | 3 | 3 | 2ES 16:76->2ES 16:77->MAT 1:1; 2ES 16:77->MAT 1:2->MAT 1:7 |
| 27 | `heth` | Heth | 31 | 29 | 2 | 8 | 2ES 16:78->2ES 16:78->MAT 1:1; MAL 4:6->MAL 4:6->TOB 1:1; MAL 4:5->MAL 4:6->TOB 1:1; MAL 4:6->TOB 1:1->TOB 1:2; TOB 1:2->TOB 1:1->MAL 4:6 |
| 28 | `tree` | Tree | 26 | 24 | 2 | 0 | TOB 1:1->MAL 4:6->MAL 4:6; TOB 1:1->TOB 1:1->MAL 4:6; MAL 4:6->MAL 4:6->TOB 1:1; 2ES 16:77->2ES 16:78->MAT 1:1; MAL 4:4->MAL 4:6->TOB 1:1 |
| 29 | `shot` | Shot | 10 | 8 | 2 | 0 | MAL 4:3->MAL 4:5->TOB 1:1; MAL 4:4->TOB 1:1->TOB 1:2; MAL 4:4->MAL 4:6->TOB 1:2; 2ES 16:78->MAT 1:4->MAT 1:7; TOB 1:3->TOB 1:2->MAL 4:6 |
| 30 | `star` | Star | 8 | 6 | 2 | 3 | 2ES 16:78->MAT 1:2->MAT 1:3; MAT 1:1->2ES 16:77->2ES 16:77; TOB 1:2->TOB 1:1->MAL 4:5; TOB 1:1->MAL 4:6->MAL 4:3; TOB 1:3->TOB 1:1->MAL 4:4 |
| 31 | `aids` | AIDS | 6 | 4 | 2 | 0 | MAL 4:6->TOB 1:1->TOB 1:2; TOB 1:2->TOB 1:1->MAL 4:6; MAT 1:2->2ES 16:77->2ES 16:76; MAL 4:6->TOB 1:2->TOB 1:4; MAT 1:9->MAT 1:5->2ES 16:78 |
| 32 | `lion` | Lion | 5 | 3 | 2 | 2 | MAL 4:5->MAL 4:6->TOB 1:2; TOB 1:2->TOB 1:1->MAL 4:6; 2ES 16:74->2ES 16:77->MAT 1:5; TOB 1:4->TOB 1:2->MAL 4:4; TOB 1:1->MAL 4:3->MAL 4:1 |
| 33 | `death` | Death | 4 | 2 | 2 | 1 | MAT 1:9->MAT 1:4->2ES 16:77; MAT 1:8->MAT 1:3->2ES 16:77; MAT 1:2->2ES 16:76->2ES 16:70; MAL 4:3->TOB 1:2->TOB 1:4 |
| 34 | `wine` | Wine | 4 | 2 | 2 | 4 | MAL 4:4->MAL 4:6->TOB 1:1; MAL 4:3->MAL 4:5->TOB 1:1; 2ES 16:77->MAT 1:2->MAT 1:6; MAL 4:6->TOB 1:3->TOB 1:4 |
| 35 | `obal` | Obal | 3 | 1 | 2 | 2 | MAT 1:3->MAT 1:1->2ES 16:77; MAL 4:5->TOB 1:2->TOB 1:4; MAT 1:8->MAT 1:3->2ES 16:77 |
| 36 | `obed` | Obed | 3 | 1 | 2 | 3 | MAT 1:5->2ES 16:78->2ES 16:75; MAT 1:5->2ES 16:78->2ES 16:74 |
| 37 | `abib` | Abib | 2 | 0 | 2 | 0 | MAT 1:3->2ES 16:77->2ES 16:75; MAT 1:5->2ES 16:78->2ES 16:75 |
| 38 | `admah` | Admah | 2 | 0 | 2 | 1 | MAT 1:9->MAT 1:4->2ES 16:78; 2ES 16:69->2ES 16:74->MAT 1:1 |
| 39 | `hannah` | Hannah | 2 | 0 | 2 | 2 | 2ES 16:77->MAT 1:6->MAT 1:12; MAT 1:12->MAT 1:6->2ES 16:77 |
| 40 | `resen` | Resen | 2 | 0 | 2 | 1 | MAL 4:4->TOB 1:1->TOB 1:3; 2ES 16:71->2ES 16:76->MAT 1:3 |
| 41 | `sivan` | Sivan | 2 | 0 | 2 | 2 | TOB 1:4->TOB 1:2->MAL 4:6; MAT 1:1->2ES 16:74->2ES 16:69 |
| 42 | `word` | Word | 2 | 0 | 2 | 0 | 2ES 16:77->MAT 1:2->MAT 1:6; 2ES 16:76->MAT 1:1->MAT 1:6 |
| 43 | `lane` | Lane | 7 | 6 | 1 | 7 | MAL 4:4->MAL 4:6->TOB 1:1; MAT 1:5->MAT 1:2->2ES 16:77; MAL 4:3->MAL 4:6->TOB 1:2; TOB 1:4->TOB 1:2->MAL 4:6; MAL 4:3->MAL 4:6->TOB 1:3 |
| 44 | `hand` | Hand | 6 | 5 | 1 | 6 | MAL 4:6->MAL 4:6->TOB 1:1; TOB 1:1->MAL 4:5->MAL 4:3; MAT 1:2->2ES 16:77->2ES 16:74; MAL 4:3->MAL 4:6->TOB 1:3; TOB 1:3->TOB 1:1->MAL 4:4 |
| 45 | `rome` | Rome | 6 | 5 | 1 | 2 | MAT 1:1->2ES 16:78->2ES 16:77; 2ES 16:77->MAT 1:1->MAT 1:3; 2ES 16:77->MAT 1:2->MAT 1:5; MAL 4:6->TOB 1:2->TOB 1:4; MAL 4:5->TOB 1:2->TOB 1:4 |
| 46 | `fire` | Fire | 5 | 4 | 1 | 3 | TOB 1:1->MAL 4:6->MAL 4:5; MAL 4:6->TOB 1:2->TOB 1:3; 2ES 16:76->2ES 16:77->MAT 1:3; MAL 4:3->TOB 1:1->TOB 1:3; TOB 1:3->TOB 1:1->MAL 4:4 |
| 47 | `horn` | Horn | 5 | 4 | 1 | 3 | TOB 1:1->MAL 4:6->MAL 4:4; 2ES 16:77->MAT 1:2->MAT 1:5; MAT 1:3->2ES 16:78->2ES 16:77; MAL 4:3->MAL 4:6->TOB 1:2; 2ES 16:76->MAT 1:2->MAT 1:6 |
| 48 | `iron` | Iron | 5 | 4 | 1 | 0 | MAL 4:5->MAL 4:6->TOB 1:1; MAL 4:3->MAL 4:6->TOB 1:2; MAL 4:5->TOB 1:1->TOB 1:3; TOB 1:4->TOB 1:2->MAL 4:6; MAT 1:8->MAT 1:4->2ES 16:77 |
| 49 | `ahab` | Ahab | 4 | 3 | 1 | 4 | 2ES 16:77->MAT 1:1->MAT 1:4; TOB 1:3->TOB 1:1->MAL 4:5; TOB 1:3->TOB 1:1->MAL 4:4; 2ES 16:76->2ES 16:78->MAT 1:5 |
| 50 | `adam` | Adam | 2 | 1 | 1 | 2 | MAT 1:9->MAT 1:4->2ES 16:77; 2ES 16:77->MAT 1:3->MAT 1:9 |

## Read

- `observed_gt_all_controls` means the term count is above Shakespeare, War
  and Peace, and Moby-Dick replacement-block term counts.
- Context buckets mark occurrence and review priority; they do not by
  themselves establish statistical significance.
- Bridge terms are still post-screen candidates unless a narrower
  prospective term list and term-level controls are locked before running.
