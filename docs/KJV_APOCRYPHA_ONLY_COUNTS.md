# KJVA Apocrypha-Only Counts

Status: ordinary ELS count comparison for the KJVA
apocrypha/deuterocanon block. This is not a bridge-completion report
and not a claim report.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_only_counts --corpus-label KJVA --config configs/example_ebible_engkjv_apocrypha.toml --control SHAKESPEARE=configs/nonbible_english_pg_shakespeare.toml --control WAR_PEACE=configs/nonbible_english_pg_war_and_peace.toml --control MOBY_DICK=configs/nonbible_english_pg_moby_dick.toml --terms terms/english_search_terms.csv --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/kjv_apocrypha_only_counts/counts.csv --summary-out reports/kjv_apocrypha_only_counts/summary.csv --markdown-out docs/KJV_APOCRYPHA_ONLY_COUNTS.md --manifest-out reports/kjv_apocrypha_only_counts/manifest.json
```

## Summary

- queries_tested: 968
- min_skip: 2
- max_skip: 250
- direction: both
- bible_apocrypha:KJVA:letters: 593090
- bible_apocrypha:KJVA:nonzero_terms: 373
- bible_apocrypha:KJVA:total_hits: 421058
- bible_canonical:KJVA:letters: 3223225
- bible_canonical:KJVA:nonzero_terms: 436
- bible_canonical:KJVA:total_hits: 2316262
- nonbible_control:SHAKESPEARE:letters: 593090
- nonbible_control:SHAKESPEARE:nonzero_terms: 372
- nonbible_control:SHAKESPEARE:total_hits: 379566
- nonbible_control:WAR_PEACE:letters: 593090
- nonbible_control:WAR_PEACE:nonzero_terms: 379
- nonbible_control:WAR_PEACE:total_hits: 379864
- nonbible_control:MOBY_DICK:letters: 593090
- nonbible_control:MOBY_DICK:nonzero_terms: 386
- nonbible_control:MOBY_DICK:total_hits: 382531

## Top Apocrypha Terms By Hit Count

| Term | Concepts | Hits | Hits/M | Canonical hits/M | Max control hits/M | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `tree` | Tree | 27897 | 94.511453 | 84.211756 | 79.448976 | `above_controls` |
| `heth` | Heth | 26945 | 91.286199 | 97.418793 | 48.96152 | `above_controls` |
| `eden` | Eden | 17080 | 57.864846 | 55.266808 | 50.923097 | `above_controls` |
| `rent` | Rent | 14943 | 50.624965 | 45.309038 | 46.454495 | `above_controls` |
| `otho` | Otho | 13833 | 46.864427 | 48.595064 | 38.282949 | `above_controls` |
| `seed` | Seed | 13769 | 46.647604 | 46.272291 | 44.72668 | `above_controls` |
| `nato` | NATO | 12787 | 43.320714 | 42.884082 | 38.160985 | `above_controls` |
| `nero` | Nero | 11375 | 38.537039 | 34.955 | 40.007375 | `control_background` |
| `shot` | Shot | 10961 | 37.13446 | 38.566265 | 31.107437 | `above_controls` |
| `noah` | Noah | 10580 | 35.843681 | 38.567512 | 28.576697 | `above_controls` |
| `thin` | Thin | 10287 | 34.851035 | 35.150019 | 29.403337 | `above_controls` |
| `soot` | Soot | 9854 | 33.384086 | 32.731294 | 41.569184 | `control_background` |
| `heal` | Heal | 9748 | 33.024972 | 37.654103 | 29.254271 | `above_controls` |
| `leah` | Leah | 9687 | 32.818312 | 37.672795 | 29.677755 | `above_controls` |
| `hits` | Hits | 8367 | 28.346321 | 30.432197 | 28.33277 | `above_controls` |
| `lane` | Lane | 7926 | 26.85227 | 29.920663 | 31.056619 | `control_background` |
| `star` | Star | 7647 | 25.907054 | 25.154242 | 28.105782 | `control_background` |
| `horn` | Horn | 7228 | 24.487536 | 23.642071 | 20.445805 | `above_controls` |
| `seal` | Seal | 6917 | 23.433908 | 25.176049 | 29.664203 | `control_background` |
| `hand` | Hand | 6856 | 23.227247 | 26.210954 | 17.979434 | `above_controls` |
| `gate` | Gate | 5950 | 20.157836 | 17.780931 | 20.886228 | `control_background` |
| `geta` | Geta | 5909 | 20.018933 | 17.799 | 20.323841 | `control_background` |
| `amen` | Amen | 5683 | 19.253274 | 18.730477 | 18.064131 | `above_controls` |
| `iran` | Iran | 5666 | 19.19568 | 18.561627 | 24.094543 | `control_background` |
| `adar` | Adar | 5396 | 18.280955 | 19.370984 | 18.396143 | `control_background` |
| `iron` | Iron | 5167 | 17.505132 | 16.116111 | 22.464976 | `control_background` |
| `shem` | Shem | 4819 | 16.326153 | 15.986514 | 15.506288 | `above_controls` |
| `eyes` | Eyes | 4814 | 16.309214 | 17.182792 | 24.484148 | `control_background` |
| `hail` | Hail | 4489 | 15.208155 | 17.756632 | 16.475219 | `control_background` |
| `teeth` | Teeth | 4307 | 14.594665 | 14.034388 | 8.80695 | `above_controls` |
| `eber` | Eber | 3975 | 13.466789 | 12.936627 | 14.513642 | `control_background` |
| `rome` | Rome | 3953 | 13.392256 | 12.171508 | 18.331773 | `control_background` |
| `aids` | AIDS | 3921 | 13.283844 | 14.572787 | 16.417626 | `control_background` |
| `ruth` | Ruth | 3699 | 12.531737 | 11.658728 | 11.894817 | `above_controls` |
| `tyre` | Tyre | 3651 | 12.369119 | 11.969013 | 16.105941 | `control_background` |
| `isis` | ISIS | 3597 | 12.186174 | 12.767778 | 22.095698 | `control_background` |
| `wine` | Wine | 3525 | 11.942247 | 10.79018 | 15.04215 | `control_background` |
| `lion` | Lion | 3483 | 11.799957 | 12.189577 | 15.489349 | `control_background` |
| `edom` | Edom | 3460 | 11.722036 | 11.44938 | 11.207079 | `above_controls` |
| `fire` | Fire | 3230 | 10.942825 | 10.434412 | 10.45836 | `above_controls` |

## Read

- This counts ordinary ELS hits inside the existing KJVA
  deuterocanon/apocrypha block.
- Canonical KJVA and same-length non-Bible control blocks are comparison
  backgrounds, not final significance tests.
- Short terms dominate raw hit counts; use normalized hits-per-million
  rather than raw totals when comparing segments.
