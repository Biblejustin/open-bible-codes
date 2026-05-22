# WRR Cross-Pair Grid

Status: diagnostic-only, not a WRR reproduction.

The WRR corrected-distance permutation test needs distances for generated
appellation/date pairings, not only the same-record source pairs. This grid
crosses every imported WRR2 appellation with every imported WRR2 date so future
date-label permutation work can read a complete candidate matrix.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/wrr_cross_pair_grid.toml --resume
```

## Current Grid Shape

| Item | Count |
| --- | ---: |
| pairs | 5208 |
| same-record source pairs | 182 |
| cross-record permutation pairs | 5026 |
| appellations | 168 |
| dates | 31 |
| appellation concepts | 30 |
| date concepts | 30 |
| appellation-min-length pairs | 4743 |
| length-5..8 pairs | 2231 |
| WNP disputed Zacut diagnostic pairs | 124 |
| Rabbi-title pairs | 992 |
| non-Rabbi-title pairs | 4216 |
| length-filtered non-Rabbi-title pairs | 1633 |
| zero-hit pairs at count-smoke cap | 3696 |
| pairs with skip-cap target unreached | 2233 |

## Cap-250 Corrected-Distance Diagnostic

| Item | Count |
| --- | ---: |
| selected grid rows | 5208 |
| defined `c(w,w')` rows | 1423 |
| ordinary-not-valid rows | 3720 |
| under-minimum-valid rows | 65 |
| minimum corrected distance | 0.008 |
| maximum valid perturbations for one pair | 125 |

Status by candidate lane:

| Candidate lane | Defined | Ordinary not valid | Under minimum |
| --- | ---: | ---: | ---: |
| `length_5_8_permutation_candidate` | 718 | 1463 | 50 |
| `appellation_min_length_permutation_candidate` | 383 | 2128 | 1 |
| `excluded_by_appellation_min_length` | 322 | 129 | 14 |

Status by review flag:

| Review flag | Defined | Ordinary not valid | Under minimum |
| --- | ---: | ---: | ---: |
| `cross_record_permutation_pair` | 1329 | 3520 | 61 |
| `same_record_source_pair` | 48 | 124 | 2 |
| `diagnostic_exclusion_candidate_not_locked` | 46 | 76 | 2 |

Cap-250 diagnostic aggregate:

| Metric | Value |
| --- | ---: |
| defined `c(w,w')` values | 1423 |
| P1 | 0.321861824814 |
| P2 | 0.202650210076 |
| P3 | 0.174975735761 |
| P4 | 0.137608477166 |

## Date-Permutation Diagnostic

This diagnostic shuffles date-concept labels over the cross-pair matrix. These
runs are repo-defined diagnostics over the current cap-250 corrected-distance
field, not exact WRR reproductions.

| Item | Value |
| --- | ---: |
| permutations | 1000 |
| seed | 1994 |
| sample rows written | 1001 |
| concepts shuffled | 30 |
| observed source rows | 182 |
| observed defined `c(w,w')` values | 50 |
| observed P1 | 0.000932436489421 |
| observed P2 | 6.00241826131e-05 |
| observed P3 | 0.00255008244378 |
| observed P4 | 0.000160565289519 |
| rho P1 | 0.000999000999001 |
| rho P2 | 0.000999000999001 |
| rho P3 | 0.0044955044955 |
| rho P4 | 0.000999000999001 |
| Bonferroni rho0 | 0.003996003996 |
| permutation row range | 169..182 |
| permutation defined-value range | 33..59 |
| identity permutations | 0 |

WNP-dispute-flagged rows excluded, same seed and sample count:

| Item | Value |
| --- | ---: |
| sample rows written | 1 |
| observed source rows | 174 |
| observed defined `c(w,w')` values | 48 |
| observed P1 | 0.003809014117 |
| observed P2 | 0.000200641225415 |
| observed P3 | 0.0102141568845 |
| observed P4 | 0.00054397278983 |
| rho P1 | 0.001998001998 |
| rho P2 | 0.000999000999001 |
| rho P3 | 0.00699300699301 |
| rho P4 | 0.001998001998 |
| Bonferroni rho0 | 0.003996003996 |

Recommended repo-defined 999,999-permutation run:

| Item | Value |
| --- | ---: |
| pair universe | WNP-dispute-flagged rows excluded |
| corrected-distance input | current cap-250 `corrected_distance` field |
| permutation rule | date-label shuffle across 30 concepts |
| permutations | 999999 |
| seed | 1994 |
| sample rows written | 1 |
| observed source rows | 174 |
| observed defined `c(w,w')` values | 48 |
| observed P1 | 0.003809014117 |
| observed P2 | 0.000200641225415 |
| observed P3 | 0.0102141568845 |
| observed P4 | 0.00054397278983 |
| rho P1 | 0.0011565 |
| rho P2 | 0.000215 |
| rho P3 | 0.0069545 |
| rho P4 | 0.000926 |
| Bonferroni rho0 | 0.00086 |
| permutation row range | 165..177 |
| permutation defined-value range | 25..59 |
| identity permutations | 0 |

## Read

- Same-record rows preserve the imported WRR2 source pairing.
- Cross-record rows are generated permutation-prep rows.
- WNP Zacut rows are flagged because the WNP critique disputes those records;
  the recommended repo-defined run excludes that flag.
- Corrected-distance and date-permutation output from this grid is diagnostic
  for the current repo protocol, not exact WRR reproduction language.
