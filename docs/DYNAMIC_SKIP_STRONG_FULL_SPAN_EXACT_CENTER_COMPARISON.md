# Strong Full-Span Exact-Center Comparison

This report compares the full-span Bible-over-control rows that had exact
center-word hits against their language-matched control-max rows. It uses the
same hit-level exact-center flag:

`center_normalized_word == normalized_term`

Exact center-word hits are review flags. They are not a claim rule by
themselves, because the rows came from a prior broad full-span screen.

## Inputs

- Bible dense exact-center scan:
  `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_FINDINGS.md`
- Bible manageable exact-hit export:
  `docs/DYNAMIC_SKIP_STRONG_MANAGEABLE_FULL_SPAN_HIT_EXPORT.md`
- Control dense exact-center scan:
  `docs/DYNAMIC_SKIP_STRONG_CONTROL_FULL_SPAN_EXACT_CENTER_FINDINGS.md`
- Control manageable exact-hit export:
  `docs/DYNAMIC_SKIP_STRONG_CONTROL_MANAGEABLE_FULL_SPAN_HIT_EXPORT.md`

## Exact-Center Rate Comparison

Rates are exact-center hits per million exported ELS hits.

| Term | Bible row | Bible hits | Bible exact-center | Bible exact perM | Control row | Control hits | Control exact-center | Control exact perM | Bible/control exact-rate ratio |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| Hebrew `Messiah` | EBIBLE_WLC | 5,252,863 | 75 | 14.277928 | HEB_PBY_BIALIK | 110,129,394 | 7,059 | 64.097329 | 0.222754 |
| Hebrew `Yeshua` | UHB | 11,151,829 | 941 | 84.380777 | HEB_PBY_BIALIK | 206,897,417 | 1,151 | 5.563143 | 15.167824 |
| English `Jesus` | KJV | 79,657 | 492 | 6,176.481665 | ENG_PG_SHAKESPEARE | 87,353 | 2 | 22.895607 | 269.767101 |
| Greek `Jesus` | LXX | 243,700 | 70 | 287.238408 | GRC_PERSEUS_HERODOTUS | 16,741 | 0 | 0.0 | inf |
| Greek `Gog` | TCG_NT | 2,000,884 | 4 | 1.999116 | GRC_PERSEUS_HERODOTUS | 3,079,794 | 0 | 0.0 | inf |

## Manageable Strong Rows With Zero Exact-Center Hits

These Bible-over-control full-span rows were exported directly rather than
through dense partitions. None had exact center-word hits.

| Row | Hits | Exact center-word hits |
| --- | ---: | ---: |
| KJV `Netanyahu` | 27 | 0 |
| TR_NT `Netanyahu` | 1 | 0 |
| KJV `Simsberry` | 2 | 0 |
| TCG_NT `Magog` | 3,271 | 0 |

## Read

- Hebrew `Messiah` does not improve under the exact-center comparison; the
  Bialik control has a higher exact-center rate.
- Hebrew `Yeshua`, English `Jesus`, Greek `Jesus`, and Greek `Gog` improve as
  review candidates under this exact-center flag.
- English and Greek `Jesus` are expected to benefit from surface-word
  occurrence in Bible corpora, so this should be interpreted as a surface-aware
  review filter, not proof by itself.
- Greek `Gog` has only 4 exact-center hits, all in Revelation 20:8 in the Bible
  row, so it is theologically interesting but numerically small.
