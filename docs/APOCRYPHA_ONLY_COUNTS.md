# LXX Apocrypha-Only Counts

Status: ordinary ELS count comparison for the LXX
apocrypha/deuterocanon block. This is not a bridge-completion report
and not a claim report.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_only_counts --corpus-label LXX --config configs/example_ebible_grclxx.toml --control ILIAD=configs/nonbible_greek_perseus_iliad.toml --control ODYSSEY=configs/nonbible_greek_perseus_odyssey.toml --control HERODOTUS=configs/nonbible_greek_perseus_herodotus.toml --terms terms/theological_terms.csv --terms terms/prophetic_terms.csv --terms terms/greek_nt_claim_terms.csv --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/apocrypha_only_counts/counts.csv --summary-out reports/apocrypha_only_counts/summary.csv --markdown-out docs/APOCRYPHA_ONLY_COUNTS.md --manifest-out reports/apocrypha_only_counts/manifest.json
```

## Summary

- queries_tested: 292
- min_skip: 2
- max_skip: 250
- direction: both
- bible_apocrypha:LXX:letters: 560880
- bible_apocrypha:LXX:nonzero_terms: 136
- bible_apocrypha:LXX:total_hits: 78606
- bible_canonical:LXX:letters: 2230979
- bible_canonical:LXX:nonzero_terms: 152
- bible_canonical:LXX:total_hits: 306964
- nonbible_control:ILIAD:letters: 560880
- nonbible_control:ILIAD:nonzero_terms: 138
- nonbible_control:ILIAD:total_hits: 73856
- nonbible_control:ODYSSEY:letters: 560880
- nonbible_control:ODYSSEY:nonzero_terms: 125
- nonbible_control:ODYSSEY:total_hits: 75664
- nonbible_control:HERODOTUS:letters: 560880
- nonbible_control:HERODOTUS:nonzero_terms: 136
- nonbible_control:HERODOTUS:total_hits: 69541

## Top Apocrypha Terms By Hit Count

| Term | Concepts | Hits | Hits/M | Canonical hits/M | Max control hits/M | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `ναοσ` | Temple | 19898 | 71.285782 | 63.342196 | 61.899474 | `above_controls` |
| `υιοσ` | Son | 12054 | 43.18418 | 47.646856 | 32.035253 | `above_controls` |
| `αιμα` | Blood | 10991 | 39.375919 | 39.850049 | 36.026225 | `above_controls` |
| `σιων` | Zion | 5460 | 19.560778 | 17.981899 | 18.102676 | `above_controls` |
| `αμην` | Amen | 2972 | 10.647369 | 9.413603 | 12.542543 | `control_background` |
| `θεοσ` | God | 2569 | 9.203597 | 9.56664 | 14.602515 | `control_background` |
| `ελαμ` | Elam | 1996 | 7.15079 | 7.390808 | 14.362484 | `control_background` |
| `αδησ` | Hades | 1988 | 7.12213 | 6.392464 | 10.403755 | `control_background` |
| `αδαμ` | Adam | 1908 | 6.835525 | 6.462681 | 12.413571 | `control_background` |
| `λεων` | Lion | 1558 | 5.581629 | 5.270789 | 8.834593 | `control_background` |
| `ισαακ` | Isaac | 1412 | 5.059712 | 5.524964 | 2.472522 | `above_controls` |
| `οφισ` | Serpent | 1283 | 4.596425 | 4.447988 | 6.753126 | `control_background` |
| `ελκη` | Boils;Sores | 1097 | 3.930068 | 4.354365 | 4.689571 | `control_background` |
| `τιτοσ` | Titus | 972 | 3.483031 | 3.628092 | 4.393206 | `control_background` |
| `οθων` | Otho | 883 | 3.163401 | 3.050846 | 3.661376 | `control_background` |
| `τερασ` | Wonder | 645 | 2.311271 | 2.180457 | 2.605107 | `control_background` |
| `οργη` | Wrath | 523 | 1.873679 | 1.819345 | 2.185362 | `control_background` |
| `αμνοσ` | Lamb | 512 | 1.834683 | 1.657399 | 2.124936 | `control_background` |
| `σαρρα` | Sarah | 474 | 1.698515 | 1.618687 | 1.723599 | `control_background` |
| `ακρισ` | Locust | 442 | 1.583848 | 1.577275 | 1.014092 | `above_controls` |
| `ελεοσ` | Mercy | 412 | 1.476347 | 1.506154 | 3.088861 | `control_background` |
| `νομοσ` | Law | 395 | 1.415429 | 1.298191 | 1.709265 | `control_background` |
| `μαρια` | Mary | 371 | 1.329429 | 1.432331 | 1.49068 | `control_background` |
| `σαρξ` | Flesh | 365 | 1.307634 | 1.353031 | 1.221653 | `above_controls` |
| `εδωμ` | Edom | 356 | 1.275391 | 1.282814 | 3.733028 | `control_background` |
| `καροσ` | Carus | 349 | 1.250595 | 1.516957 | 0.931675 | `above_controls` |
| `κερασ` | Horn | 343 | 1.229094 | 1.402622 | 1.279262 | `control_background` |
| `αγιοσ` | Holy;Saint | 330 | 1.182511 | 1.159549 | 1.049926 | `above_controls` |
| `νικαω` | Overcome | 325 | 1.164594 | 1.292789 | 0.802674 | `above_controls` |
| `αστηρ` | Star | 311 | 1.114427 | 1.048816 | 0.874341 | `above_controls` |
| `ρωμη` | Rome | 306 | 1.096263 | 1.229701 | 1.536918 | `control_background` |
| `τυροσ` | Tyre | 287 | 1.028426 | 1.182056 | 1.078593 | `control_background` |
| `ηλιασ` | Elijah | 276 | 0.989009 | 0.959689 | 1.032009 | `control_background` |
| `γετασ` | Geta | 244 | 0.874341 | 0.844454 | 1.078593 | `control_background` |
| `εικων` | Image | 239 | 0.856424 | 0.882266 | 0.77759 | `above_controls` |
| `βασαν` | Bashan | 225 | 0.806257 | 0.683306 | 0.458671 | `above_controls` |
| `θυσια` | Sacrifice | 225 | 0.806257 | 0.925479 | 0.648589 | `above_controls` |
| `κλεισ` | Key | 222 | 0.795507 | 0.83095 | 0.895841 | `control_background` |
| `μωαβ` | Moab | 210 | 0.752338 | 0.842606 | 0.537384 | `above_controls` |
| `δοξα` | Glory | 199 | 0.712929 | 0.683267 | 1.210905 | `control_background` |

## Read

- This counts ordinary ELS hits inside the existing LXX
  deuterocanon/apocrypha block.
- Canonical LXX and same-length non-Bible control blocks are comparison
  backgrounds, not final significance tests.
- Short terms dominate raw hit counts; use normalized hits-per-million
  rather than raw totals when comparing segments.
