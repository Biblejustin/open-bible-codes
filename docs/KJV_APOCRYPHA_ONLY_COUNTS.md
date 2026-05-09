# KJVA Apocrypha-Only Counts

Status: ordinary ELS count comparison for the KJVA
apocrypha/deuterocanon block. This is not a bridge-completion report
and not a claim report.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_only_counts --corpus-label KJVA --config configs/example_ebible_engkjv_apocrypha.toml --control SHAKESPEARE=configs/nonbible_english_pg_shakespeare.toml --control WAR_PEACE=configs/nonbible_english_pg_war_and_peace.toml --control MOBY_DICK=configs/nonbible_english_pg_moby_dick.toml --terms terms/english_search_terms.csv --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/kjv_apocrypha_only_counts/counts.csv --summary-out reports/kjv_apocrypha_only_counts/summary.csv --markdown-out docs/KJV_APOCRYPHA_ONLY_COUNTS.md --manifest-out reports/kjv_apocrypha_only_counts/manifest.json
```

## Summary

- queries_tested: 575
- min_skip: 2
- max_skip: 250
- direction: both
- bible_apocrypha:KJVA:letters: 593090
- bible_apocrypha:KJVA:nonzero_terms: 272
- bible_apocrypha:KJVA:total_hits: 254475
- bible_canonical:KJVA:letters: 3223225
- bible_canonical:KJVA:nonzero_terms: 315
- bible_canonical:KJVA:total_hits: 1424993
- nonbible_control:SHAKESPEARE:letters: 593090
- nonbible_control:SHAKESPEARE:nonzero_terms: 270
- nonbible_control:SHAKESPEARE:total_hits: 234606
- nonbible_control:WAR_PEACE:letters: 593090
- nonbible_control:WAR_PEACE:nonzero_terms: 277
- nonbible_control:WAR_PEACE:total_hits: 227967
- nonbible_control:MOBY_DICK:letters: 593090
- nonbible_control:MOBY_DICK:nonzero_terms: 278
- nonbible_control:MOBY_DICK:total_hits: 232226

## Top Apocrypha Terms By Hit Count

| Term | Concepts | Hits | Hits/M | Canonical hits/M | Max control hits/M | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `heth` | Heth | 26945 | 91.286199 | 97.418793 | 48.96152 | `above_controls` |
| `otho` | Otho | 13833 | 46.864427 | 48.595064 | 38.282949 | `above_controls` |
| `nato` | NATO | 12787 | 43.320714 | 42.884082 | 38.160985 | `above_controls` |
| `nero` | Nero | 11375 | 38.537039 | 34.955 | 40.007375 | `control_background` |
| `noah` | Noah | 10580 | 35.843681 | 38.567512 | 28.576697 | `above_controls` |
| `heal` | Heal | 9748 | 33.024972 | 37.654103 | 29.254271 | `above_controls` |
| `star` | Star | 7647 | 25.907054 | 25.154242 | 28.105782 | `control_background` |
| `horn` | Horn | 7228 | 24.487536 | 23.642071 | 20.445805 | `above_controls` |
| `seal` | Seal | 6917 | 23.433908 | 25.176049 | 29.664203 | `control_background` |
| `hand` | Hand | 6856 | 23.227247 | 26.210954 | 17.979434 | `above_controls` |
| `geta` | Geta | 5909 | 20.018933 | 17.799 | 20.323841 | `control_background` |
| `amen` | Amen | 5683 | 19.253274 | 18.730477 | 18.064131 | `above_controls` |
| `iran` | Iran | 5666 | 19.19568 | 18.561627 | 24.094543 | `control_background` |
| `adar` | Adar | 5396 | 18.280955 | 19.370984 | 18.396143 | `control_background` |
| `shem` | Shem | 4819 | 16.326153 | 15.986514 | 15.506288 | `above_controls` |
| `eyes` | Eyes | 4814 | 16.309214 | 17.182792 | 24.484148 | `control_background` |
| `hail` | Hail | 4489 | 15.208155 | 17.756632 | 16.475219 | `control_background` |
| `teeth` | Teeth | 4307 | 14.594665 | 14.034388 | 8.80695 | `above_controls` |
| `eber` | Eber | 3975 | 13.466789 | 12.936627 | 14.513642 | `control_background` |
| `rome` | Rome | 3953 | 13.392256 | 12.171508 | 18.331773 | `control_background` |
| `aids` | AIDS | 3921 | 13.283844 | 14.572787 | 16.417626 | `control_background` |
| `tyre` | Tyre | 3651 | 12.369119 | 11.969013 | 16.105941 | `control_background` |
| `isis` | ISIS | 3597 | 12.186174 | 12.767778 | 22.095698 | `control_background` |
| `lion` | Lion | 3483 | 11.799957 | 12.189577 | 15.489349 | `control_background` |
| `edom` | Edom | 3460 | 11.722036 | 11.44938 | 11.207079 | `above_controls` |
| `fire` | Fire | 3230 | 10.942825 | 10.434412 | 10.45836 | `above_controls` |
| `mash` | Mash | 3034 | 10.278802 | 10.930369 | 9.716416 | `above_controls` |
| `elam` | Elam | 2864 | 9.702864 | 10.49298 | 11.793181 | `control_background` |
| `aram` | Aram | 2726 | 9.235338 | 9.259318 | 11.288388 | `control_background` |
| `seba` | Seba | 2612 | 8.849121 | 9.614463 | 11.881266 | `control_background` |
| `adam` | Adam | 2479 | 8.398534 | 9.564618 | 7.195839 | `above_controls` |
| `ahab` | Ahab | 2361 | 7.998765 | 10.07179 | 7.839535 | `above_controls` |
| `bear` | Bear | 2336 | 7.914068 | 8.507283 | 9.635107 | `control_background` |
| `lord` | Lord | 2193 | 7.429602 | 7.528453 | 8.422249 | `control_background` |
| `life` | Life | 2139 | 7.246657 | 7.908521 | 7.991989 | `control_background` |
| `trees` | Trees | 1622 | 5.496296 | 4.913656 | 5.231986 | `above_controls` |
| `heart` | Heart | 1454 | 4.927013 | 4.764115 | 3.34454 | `above_controls` |
| `elul` | Elul | 1446 | 4.898862 | 5.600077 | 8.012316 | `control_background` |
| `sign` | Sign | 1422 | 4.817553 | 4.313455 | 7.355069 | `control_background` |
| `earth` | Earth | 1421 | 4.815189 | 4.717384 | 3.415701 | `above_controls` |

## Read

- This counts ordinary ELS hits inside the existing KJVA
  deuterocanon/apocrypha block.
- Canonical KJVA and same-length non-Bible control blocks are comparison
  backgrounds, not final significance tests.
- Short terms dominate raw hit counts; use normalized hits-per-million
  rather than raw totals when comparing segments.
