# STEP TAHOT Final Gate

Last run: 2026-05-05.

## Scope

This report consolidates:

- the broader Hebrew screening version-presence run with `STEP_TAHOT`;
- the `STEP_TAHOT`-only source-policy path audit;
- the matching null/frequency control version-presence run;
- the matching `STEP_TAHOT`-only control source-policy audit.

Reproduce after the upstream STEP_TAHOT screening/control protocols have been
run:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_final_gate.toml --resume
```

Generated local outputs:

- `reports/step_tahot_final_gate/summary.csv`
- `reports/step_tahot_final_gate/term_summary.csv`
- `reports/step_tahot_final_gate/row_gate.csv`
- `reports/step_tahot_final_gate/step_tahot_final_gate.md`
- `reports/step_tahot_final_gate/manifest.json`

## Summary

| Metric | Real terms | Controls | Read |
| --- | ---: | ---: | --- |
| Pattern rows | 15,478 | 1,005 | screen size |
| Patterns with `STEP_TAHOT` | 12,084 | 749 | `STEP_TAHOT` participates broadly |
| `STEP_TAHOT`-only rows | 379 | 24 | source-only rows exist in terms and controls |
| `STEP_TAHOT`-only rate | 2.449% | 2.388% | real/control ratio 1.025 |
| Policy-touch rows | 80 | 3 | hidden path touches Q/R/X/other source policy |
| Policy-touch rate among `STEP_TAHOT`-only rows | 21.108% | 12.500% | within source-only rows |
| L-only path rows | 299 | 21 | letters are in L-prefixed TAHOT words |
| Q rows | 65 | 3 | qere-selected path rows |
| R rows | 2 | 0 | restored-word path rows |
| X rows | 13 | 0 | LXX-based Hebrew-addition path rows |

## Gate Counts

| Gate | Rows |
| --- | ---: |
| `hold_l_only_step_tahot_specific` | 299 |
| `hold_selected_reading_policy_path` | 80 |

## Top Real `STEP_TAHOT`-Only Terms

| Term | Source-only rows | Policy-touch | L-only | Read |
| --- | ---: | ---: | ---: | --- |
| `benjamin_h` | 8 | 2 | 6 | mixed policy-touch and L-only source-specific rows |
| `dodanim_h` | 7 | 1 | 6 | mixed policy-touch and L-only source-specific rows |
| `wings_h` | 7 | 1 | 6 | mixed policy-touch and L-only source-specific rows |
| `lake_of_fire_h` | 6 | 2 | 4 | mixed policy-touch and L-only source-specific rows |
| `edom_h` | 6 | 0 | 6 | L-only source-specific rows; compare against controls |
| `jd_h` | 6 | 0 | 6 | L-only source-specific rows; compare against controls |
| `peace_h` | 6 | 0 | 6 | L-only source-specific rows; compare against controls |

## Read

No `STEP_TAHOT`-only row is promoted by this gate.

The most important number is the rate comparison: real screening rows were
`STEP_TAHOT`-only at 2.449%, while null/frequency controls were
`STEP_TAHOT`-only at 2.388%. That near-match means `STEP_TAHOT`-only behavior
is not special to the meaningful screening terms.

Rows with `hold_selected_reading_policy_path` touch qere, restored, LXX-based
Hebrew addition, or other non-L source-policy words on the hidden-letter path.
Rows with `hold_l_only_step_tahot_specific` avoid those path flags, but controls
also produce `STEP_TAHOT`-only L-path rows. Those rows remain source-specific
review rows, not claim rows.
