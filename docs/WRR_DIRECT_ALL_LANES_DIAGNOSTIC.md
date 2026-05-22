# WRR Direct All-Lane Corrected-Distance Diagnostic

Status: diagnostic-only, not a WRR reproduction.

This note records the direct perturbed-letter corrected-distance run over all
182 imported same-record WRR2 pairs from the working ANU/McKay source. This is
broader than the current length-5..8 smoke lane and intentionally includes
rows still marked `appellation_min_length_candidate` or
`excluded_by_appellation_min_length`.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/wrr_corrected_distance_direct_all_lanes.toml --resume
```

## Current Results

| Run | Pairs | Defined | Ordinary not valid | Under minimum | Min c | Max valid |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all lanes, cap 250 | 182 | 50 | 130 | 2 | 0.008 | 125 |
| all lanes, cap 1000 split | 182 | 72 | 110 | 0 | 0.008 | 125 |

Cap-1000 lane breakdown:

| Candidate lane | Defined | Ordinary not valid |
| --- | ---: | ---: |
| `length_5_8_smoke_candidate` | 46 | 40 |
| `appellation_min_length_candidate` | 12 | 67 |
| `excluded_by_appellation_min_length` | 14 | 3 |

Cap-1000 review-status breakdown:

| Review status | Defined | Ordinary not valid |
| --- | ---: | ---: |
| `needs_primary_source_pair_rule` | 70 | 104 |
| `diagnostic_exclusion_candidate_not_locked` | 2 | 6 |

Cap-1000 diagnostic aggregate:

| Metric | Value |
| --- | ---: |
| defined `c(w,w')` values | 72 |
| P1 | 0.00252257011468 |
| P2 | 1.16472976875e-05 |
| P3 | 0.0184584022574 |
| P4 | 0.000274264355592 |

Printed vs reported-program `D(w)` formula check:

| Run | Changed pairs vs printed |
| --- | ---: |
| all lanes, cap 1000, program formula | 0 |

## Read

The all-lane run is useful for source-shape pressure testing:

- The direct-search driver does produce defined corrected distances outside
  the narrow 5..8 smoke lane.
- The `163` published second-list distance count still is not explained by raw
  imported same-record pair counts: direct all-lane cap 1000 defines 72 values,
  not 163.
- The 14 defined rows in `excluded_by_appellation_min_length` are diagnostic
  only; they should not be promoted into the candidate set without a citable
  pair-universe rule.

Claim language remains blocked by `docs/WRR_CLAIM_READINESS.md`.

For a pair-lane/review-status join over these same outputs, see
`docs/WRR_DEFINED_PAIR_SET_AUDIT.md`.
