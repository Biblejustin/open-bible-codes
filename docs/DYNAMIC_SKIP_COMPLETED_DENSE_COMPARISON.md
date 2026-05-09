# Completed Dense Bible-Control Comparison

This report compares only dense full-span rows whose partition exports are complete.
It is a hit-level completion view, not a normalized rate test. Use
`docs/DYNAMIC_SKIP_BIBLE_CONTROL_COMPARISON.md` for normalized count-rate background.

## Reproduce

```bash
python3 -m scripts.summarize_dynamic_span_partition_outputs
python3 -m scripts.compare_completed_dense_partitions
```

## Scope

- compared term/mode rows: 27
- completed on Bible and controls: 20
- completed on Bible only: 2
- completed on controls only: 5
- input term summary: `reports/dynamic_skip_focus/full_span_partition_term_summary.csv`
- output CSV: `reports/dynamic_skip_focus/completed_dense_bible_control_comparison.csv`

## Completed On Both Bible And Controls

| Term | Mode | Bible hits | Control hits | Bible exact center | Control exact center | Control/Bible raw hit ratio |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `dyn_vance_h` | `full-span` | 5,949,061 | 114,203,154 | 0 | 0 | 19.196837 |
| `dyn_messiah_h` | `full-span` | 25,699,997 | 112,614,921 | 672 | 2,498 | 4.381904 |
| `dyn_iran_e` | `full-span` | 64,362,163 | 57,178,184 | 0 | 0 | 0.888382 |
| `dyn_gog_h` | `full-span` | 27,857,390 | 52,524,066 | 1,870 | 220 | 1.885463 |
| `dyn_yeshua_h` | `full-span` | 54,581,830 | 46,208,240 | 2,636 | 112 | 0.846586 |
| `dyn_dragon_h` | `full-span` | 30,656,204 | 33,003,976 | 256 | 0 | 1.076584 |
| `dyn_magog_h` | `full-span` | 1,576,128 | 31,600,311 | 0 | 0 | 20.04933 |
| `dyn_iran_h` | `full-span` | 3,415,682 | 23,575,196 | 0 | 0 | 6.902047 |
| `dyn_iran_g` | `full-span` | 99,713,987 | 14,623,095 | 0 | 0 | 0.14665 |
| `dyn_russia_h` | `full-span` | 703,526 | 13,154,824 | 0 | 21,013 | 18.698419 |
| `dyn_beast_e` | `full-span` | 2,427,966 | 4,936,225 | 934 | 996 | 2.03307 |
| `dyn_gog_g` | `full-span` | 30,371,570 | 4,476,796 | 3,746 | 0 | 0.147401 |
| `dyn_vance_g` | `full-span` | 16,892,641 | 1,746,941 | 0 | 0 | 0.103414 |
| `dyn_vance_e` | `full-span` | 294,941 | 859,869 | 0 | 0 | 2.915393 |
| `dyn_trump_e` | `full-span` | 111,371 | 428,808 | 1 | 18 | 3.850266 |
| `dyn_magog_e` | `full-span` | 118,259 | 347,275 | 17 | 0 | 2.936563 |
| `dyn_russia_g` | `full-span` | 2,627,125 | 251,719 | 0 | 0 | 0.095815 |
| `dyn_christ_e` | `full-span` | 56,561 | 111,185 | 16 | 4 | 1.965754 |
| `dyn_jesus_e` | `full-span` | 79,657 | 87,353 | 492 | 2 | 1.096614 |
| `dyn_trump_g` | `full-span` | 487,148 | 68,470 | 0 | 0 | 0.140553 |

## Bible-Only Completed Rows

| Term | Mode | Corpora | Hits | Exact center hits |
| --- | --- | --- | ---: | ---: |
| `dyn_yhwh_h` | `full-span` | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | 215,724,206 | 4,011,918 |
| `dyn_jesus_g` | `full-span` | LXX | 243,700 | 70 |

## Control-Only Completed Rows

| Term | Mode | Corpora | Hits | Exact center hits |
| --- | --- | --- | ---: | ---: |
| `dyn_gog_e` | `full-span` | ENG_PG_MOBY_DICK, ENG_PG_WAR_PEACE | 114,765,844 | 0 |
| `dyn_netanyahu_h` | `full-span` | HEB_PBY_AHAD_HAAM, HEB_PBY_BIALIK, HEB_PBY_BRENNER | 1,880,460 | 0 |
| `dyn_trump_h` | `full-span` | HEB_PBY_AHAD_HAAM, HEB_PBY_BIALIK, HEB_PBY_BRENNER | 1,079,952 | 0 |
| `dyn_russia_e` | `full-span` | ENG_PG_SHAKESPEARE | 151,995 | 1 |
| `dyn_dragon_e` | `full-span` | ENG_PG_SHAKESPEARE | 60,588 | 1 |

## Read

- Exact center-word hits are retained as flags, not as the gate for inclusion.
- Raw dense hit totals are useful for triage, but corpus lengths differ.
- Completion status matters: absence from this report may mean the dense partition remains deferred.
