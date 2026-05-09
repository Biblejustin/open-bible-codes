# Dynamic Skip Focus Expectations

This is a planning report for full-distance ELS searches. It does not
count observed hits. It estimates the search space and expected hit count
from corpus-specific letter frequencies before launching expensive
dynamic-skip counts.

Reproduce with:

```bash
python3 -m scripts.analyze_dynamic_skip_expectations
```

## Inputs

- Terms: `terms/dynamic_skip_focus_terms.csv`
- Direction: `both`
- Minimum skip: `2`
- CSV: `reports/dynamic_skip_focus/expectations.csv`

## Recommendation Counts

| Recommendation | Rows |
| --- | ---: |
| `requires_long_run_or_large_span_counter` | 138 |
| `targeted_large_span_count_candidate` | 6 |

## Lowest Expected Rows

| Corpus | Mode | Term | Length | Max skip | Expected hits | Recommendation |
| --- | --- | --- | ---: | ---: | ---: | --- |
| TR_NT | `letters-per-term` | `dyn_netanyahu_g` | 10 | 69083 | 0.132427 | `targeted_large_span_count_candidate` |
| TR_NT | `full-span` | `dyn_netanyahu_g` | 10 | 76758 | 0.133764 | `targeted_large_span_count_candidate` |
| SBLGNT | `letters-per-term` | `dyn_netanyahu_g` | 10 | 67987 | 0.134486 | `targeted_large_span_count_candidate` |
| SBLGNT | `full-span` | `dyn_netanyahu_g` | 10 | 75542 | 0.135845 | `targeted_large_span_count_candidate` |
| KJV | `letters-per-term` | `dyn_simscorner_e` | 10 | 322322 | 0.179569 | `requires_long_run_or_large_span_counter` |
| KJV | `full-span` | `dyn_simscorner_e` | 10 | 358136 | 0.181382 | `requires_long_run_or_large_span_counter` |
| KJV | `letters-per-term` | `dyn_simsberry_e` | 9 | 358136 | 0.623301 | `requires_long_run_or_large_span_counter` |
| KJV | `full-span` | `dyn_simsberry_e` | 9 | 402903 | 0.631092 | `requires_long_run_or_large_span_counter` |
| LXX | `letters-per-term` | `dyn_netanyahu_g` | 10 | 279185 | 1.679423 | `requires_long_run_or_large_span_counter` |
| LXX | `full-span` | `dyn_netanyahu_g` | 10 | 310206 | 1.696388 | `requires_long_run_or_large_span_counter` |
| KJV | `letters-per-term` | `dyn_netanyahu_e` | 9 | 358136 | 22.856559 | `requires_long_run_or_large_span_counter` |
| KJV | `full-span` | `dyn_netanyahu_e` | 9 | 402903 | 23.142263 | `requires_long_run_or_large_span_counter` |
| SBLGNT | `letters-per-term` | `dyn_christ_g` | 7 | 97125 | 79.467456 | `targeted_large_span_count_candidate` |
| SBLGNT | `full-span` | `dyn_christ_g` | 7 | 113313 | 81.123088 | `requires_long_run_or_large_span_counter` |
| TR_NT | `letters-per-term` | `dyn_christ_g` | 7 | 98690 | 84.279969 | `targeted_large_span_count_candidate` |
| TR_NT | `full-span` | `dyn_christ_g` | 7 | 115138 | 86.035771 | `requires_long_run_or_large_span_counter` |
| KJV | `letters-per-term` | `dyn_catering_e` | 8 | 402903 | 97.503169 | `requires_long_run_or_large_span_counter` |
| KJV | `full-span` | `dyn_catering_e` | 8 | 460460 | 99.050828 | `requires_long_run_or_large_span_counter` |
| SBLGNT | `letters-per-term` | `dyn_dragon_g` | 6 | 113313 | 585.496947 | `requires_long_run_or_large_span_counter` |
| TR_NT | `letters-per-term` | `dyn_dragon_g` | 6 | 115138 | 592.334398 | `requires_long_run_or_large_span_counter` |
| SBLGNT | `full-span` | `dyn_dragon_g` | 6 | 135975 | 602.225304 | `requires_long_run_or_large_span_counter` |
| TR_NT | `full-span` | `dyn_dragon_g` | 6 | 138166 | 609.258616 | `requires_long_run_or_large_span_counter` |
| KJV | `letters-per-term` | `dyn_cowboy_e` | 6 | 537204 | 1058.394519 | `requires_long_run_or_large_span_counter` |
| KJV | `full-span` | `dyn_cowboy_e` | 6 | 644644 | 1088.634314 | `requires_long_run_or_large_span_counter` |
| LXX | `letters-per-term` | `dyn_christ_g` | 7 | 398837 | 1278.516495 | `requires_long_run_or_large_span_counter` |
| LXX | `full-span` | `dyn_christ_g` | 7 | 465309 | 1305.152022 | `requires_long_run_or_large_span_counter` |
| SBLGNT | `letters-per-term` | `dyn_beast_g` | 6 | 113313 | 1473.154707 | `requires_long_run_or_large_span_counter` |
| TR_NT | `letters-per-term` | `dyn_beast_g` | 6 | 115138 | 1494.057494 | `requires_long_run_or_large_span_counter` |
| SBLGNT | `full-span` | `dyn_beast_g` | 6 | 135975 | 1515.244523 | `requires_long_run_or_large_span_counter` |
| TR_NT | `full-span` | `dyn_beast_g` | 6 | 138166 | 1536.745804 | `requires_long_run_or_large_span_counter` |
| SBLGNT | `letters-per-term` | `dyn_magog_g` | 5 | 135975 | 3026.49123 | `requires_long_run_or_large_span_counter` |
| SBLGNT | `full-span` | `dyn_magog_g` | 5 | 169969 | 3152.599668 | `requires_long_run_or_large_span_counter` |
| TR_NT | `letters-per-term` | `dyn_magog_g` | 5 | 138166 | 3161.770361 | `requires_long_run_or_large_span_counter` |
| TR_NT | `full-span` | `dyn_magog_g` | 5 | 172707 | 3293.510793 | `requires_long_run_or_large_span_counter` |
| UHB | `letters-per-term` | `dyn_trump_h` | 5 | 239124 | 10386.852516 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `letters-per-term` | `dyn_trump_h` | 5 | 239408 | 10400.737173 | `requires_long_run_or_large_span_counter` |
| UHB | `full-span` | `dyn_trump_h` | 5 | 298905 | 10819.647087 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `full-span` | `dyn_trump_h` | 5 | 299260 | 10834.104239 | `requires_long_run_or_large_span_counter` |
| SBLGNT | `letters-per-term` | `dyn_jesus_g` | 6 | 113313 | 11117.005024 | `requires_long_run_or_large_span_counter` |
| LXX | `letters-per-term` | `dyn_dragon_g` | 6 | 465309 | 11374.681702 | `requires_long_run_or_large_span_counter` |

## Highest Expected Rows

| Corpus | Mode | Term | Length | Max skip | Expected hits | Recommendation |
| --- | --- | --- | ---: | ---: | ---: | --- |
| MT_WLC | `full-span` | `dyn_beast_h` | 3 | 598520 | 162049360.126668 | `requires_long_run_or_large_span_counter` |
| UHB | `full-span` | `dyn_beast_h` | 3 | 597811 | 161642169.716417 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `letters-per-term` | `dyn_beast_h` | 3 | 399014 | 144043875.66825 | `requires_long_run_or_large_span_counter` |
| UHB | `letters-per-term` | `dyn_beast_h` | 3 | 398541 | 143681868.550128 | `requires_long_run_or_large_span_counter` |
| KJV | `full-span` | `dyn_gog_e` | 3 | 1611612 | 112832455.998627 | `requires_long_run_or_large_span_counter` |
| KJV | `letters-per-term` | `dyn_gog_e` | 3 | 1074408 | 100295500.884949 | `requires_long_run_or_large_span_counter` |
| LXX | `full-span` | `dyn_iran_g` | 4 | 930619 | 82302522.751452 | `requires_long_run_or_large_span_counter` |
| LXX | `letters-per-term` | `dyn_iran_g` | 4 | 697964 | 77158587.442404 | `requires_long_run_or_large_span_counter` |
| KJV | `full-span` | `dyn_iran_e` | 4 | 1074408 | 64389117.440479 | `requires_long_run_or_large_span_counter` |
| KJV | `letters-per-term` | `dyn_iran_e` | 4 | 805806 | 60364793.85483 | `requires_long_run_or_large_span_counter` |
| UHB | `full-span` | `dyn_yhwh_h` | 4 | 398541 | 43228930.475937 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `full-span` | `dyn_yhwh_h` | 4 | 399013 | 43214359.072056 | `requires_long_run_or_large_span_counter` |
| UHB | `letters-per-term` | `dyn_yhwh_h` | 4 | 298906 | 40527129.100462 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `letters-per-term` | `dyn_yhwh_h` | 4 | 299260 | 40513441.323215 | `requires_long_run_or_large_span_counter` |
| LXX | `full-span` | `dyn_gog_g` | 3 | 1395929 | 22319951.042919 | `requires_long_run_or_large_span_counter` |
| LXX | `letters-per-term` | `dyn_gog_g` | 3 | 930619 | 19839949.376222 | `requires_long_run_or_large_span_counter` |
| LXX | `full-span` | `dyn_vance_g` | 4 | 930619 | 14917487.004602 | `requires_long_run_or_large_span_counter` |
| LXX | `letters-per-term` | `dyn_vance_g` | 4 | 697964 | 13985139.057542 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `full-span` | `dyn_yeshua_h` | 4 | 399013 | 10840369.38057 | `requires_long_run_or_large_span_counter` |
| UHB | `full-span` | `dyn_yeshua_h` | 4 | 398541 | 10833826.233312 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `letters-per-term` | `dyn_yeshua_h` | 4 | 299260 | 10162841.200292 | `requires_long_run_or_large_span_counter` |
| UHB | `letters-per-term` | `dyn_yeshua_h` | 4 | 298906 | 10156713.792718 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `full-span` | `dyn_dragon_h` | 4 | 399013 | 6152913.065589 | `requires_long_run_or_large_span_counter` |
| UHB | `full-span` | `dyn_dragon_h` | 4 | 398541 | 6134788.281886 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `letters-per-term` | `dyn_dragon_h` | 4 | 299260 | 5768353.107677 | `requires_long_run_or_large_span_counter` |
| UHB | `letters-per-term` | `dyn_dragon_h` | 4 | 298906 | 5751364.976341 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `full-span` | `dyn_gog_h` | 3 | 598520 | 5500488.481557 | `requires_long_run_or_large_span_counter` |
| UHB | `full-span` | `dyn_gog_h` | 3 | 597811 | 5484757.05652 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `full-span` | `dyn_messiah_h` | 4 | 399013 | 5096111.460413 | `requires_long_run_or_large_span_counter` |
| UHB | `full-span` | `dyn_messiah_h` | 4 | 398541 | 5077060.090257 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `letters-per-term` | `dyn_gog_h` | 3 | 399014 | 4889323.094721 | `requires_long_run_or_large_span_counter` |
| UHB | `letters-per-term` | `dyn_gog_h` | 3 | 398541 | 4875337.566966 | `requires_long_run_or_large_span_counter` |
| MT_WLC | `letters-per-term` | `dyn_messiah_h` | 4 | 299260 | 4777602.099426 | `requires_long_run_or_large_span_counter` |
| UHB | `letters-per-term` | `dyn_messiah_h` | 4 | 298906 | 4759744.630813 | `requires_long_run_or_large_span_counter` |
| TR_NT | `full-span` | `dyn_iran_g` | 4 | 230276 | 4629222.200071 | `requires_long_run_or_large_span_counter` |
| SBLGNT | `full-span` | `dyn_iran_g` | 4 | 226626 | 4610750.960876 | `requires_long_run_or_large_span_counter` |
| TR_NT | `letters-per-term` | `dyn_iran_g` | 4 | 172707 | 4339889.530374 | `requires_long_run_or_large_span_counter` |
| SBLGNT | `letters-per-term` | `dyn_iran_g` | 4 | 169969 | 4322572.667882 | `requires_long_run_or_large_span_counter` |
| KJV | `full-span` | `dyn_beast_e` | 5 | 805806 | 2442989.488498 | `requires_long_run_or_large_span_counter` |
| KJV | `letters-per-term` | `dyn_beast_e` | 5 | 644645 | 2345270.151497 | `requires_long_run_or_large_span_counter` |

## Read

Rows marked `requires_long_run_or_large_span_counter` are not impossible,
and they are not excluded from search. The label means the legacy
Python lane scanner is the wrong tool for that span. Use the compiled
dynamic span counter and the full-span protocol when the research
question calls for the full distance.
