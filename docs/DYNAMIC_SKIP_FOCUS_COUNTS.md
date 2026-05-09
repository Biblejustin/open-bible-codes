# Dynamic Skip Focus Counts

This report records completed full-distance ELS counts for the selected
focus terms. These are observed counts, not expectation-only planning
numbers. `letters-per-term` uses `floor(corpus_letters / term_letters)`;
`full-span` uses the largest skip where the term can still fit in the
corpus.

Reproduce with:

```bash
python3 -m scripts.run_protocol protocols/dynamic_skip_focus_counts.toml --resume
python3 -m scripts.summarize_dynamic_span_counts
```

The full-span rows are intentional search targets. Expected-hit estimates
are useful for planning runtime and controls, but they do not replace
running the search.

Bible and non-Bible rows are intentionally listed together here so the
same search rule can be compared across language-matched background
texts. English rows are secondary evidence only; absence or presence in
English translation does not decide an original-language hypothesis.

## Run Counts

- Rows counted: 488
- Modes: `{'full-span': 244, 'letters-per-term': 244}`
- Corpora: `{'BYZ_NT': 22, 'EBIBLE_WLC': 24, 'ENG_PG_MOBY_DICK': 30, 'ENG_PG_SHAKESPEARE': 30, 'ENG_PG_WAR_PEACE': 30, 'GRC_PERSEUS_HERODOTUS': 22, 'GRC_PERSEUS_ILIAD': 22, 'GRC_PERSEUS_ODYSSEY': 22, 'HEB_PBY_AHAD_HAAM': 24, 'HEB_PBY_BIALIK': 24, 'HEB_PBY_BRENNER': 24, 'KJV': 30, 'LXX': 22, 'MAM': 24, 'MT_WLC': 24, 'SBLGNT': 22, 'TCG_NT': 22, 'TR_NT': 22, 'UHB': 24, 'UXLC': 24}`

## Selected Local / Modern Rows

| Corpus | Mode | Term | Count | Rate / 1M positions | Forward | Backward | Max skip | Seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ENG_PG_MOBY_DICK | `full-span` | `dyn_catering_e` | 22 | 0.000169 | 13 | 9 | 136453 | 0.028 |
| ENG_PG_MOBY_DICK | `letters-per-term` | `dyn_catering_e` | 21 | 0.000164 | 13 | 8 | 119397 | 0.028 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_catering_e` | 233 | 9.9e-05 | 104 | 129 | 579602 | 0.429 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_catering_e` | 230 | 9.9e-05 | 101 | 129 | 507152 | 0.449 |
| ENG_PG_WAR_PEACE | `full-span` | `dyn_catering_e` | 103 | 0.000114 | 54 | 49 | 359558 | 0.187 |
| ENG_PG_WAR_PEACE | `letters-per-term` | `dyn_catering_e` | 101 | 0.000113 | 54 | 47 | 314614 | 0.179 |
| KJV | `full-span` | `dyn_catering_e` | 96 | 6.5e-05 | 40 | 56 | 460460 | 0.155 |
| KJV | `letters-per-term` | `dyn_catering_e` | 95 | 6.5e-05 | 40 | 55 | 402903 | 0.143 |
| ENG_PG_MOBY_DICK | `full-span` | `dyn_cowboy_e` | 149 | 0.000817 | 74 | 75 | 191035 | 0.026 |
| ENG_PG_MOBY_DICK | `letters-per-term` | `dyn_cowboy_e` | 145 | 0.000817 | 71 | 74 | 159196 | 0.022 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_cowboy_e` | 4684 | 0.001423 | 2368 | 2316 | 811444 | 0.591 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_cowboy_e` | 4546 | 0.00142 | 2302 | 2244 | 676203 | 0.74 |
| ENG_PG_WAR_PEACE | `full-span` | `dyn_cowboy_e` | 1058 | 0.000835 | 521 | 537 | 503382 | 0.176 |
| ENG_PG_WAR_PEACE | `letters-per-term` | `dyn_cowboy_e` | 1031 | 0.000837 | 505 | 526 | 419485 | 0.166 |
| KJV | `full-span` | `dyn_cowboy_e` | 998 | 0.00048 | 488 | 510 | 644644 | 0.153 |
| KJV | `letters-per-term` | `dyn_cowboy_e` | 973 | 0.000482 | 473 | 500 | 537204 | 0.152 |
| ENG_PG_MOBY_DICK | `full-span` | `dyn_iran_e` | 6458074 | 21.235366 | 3221445 | 3236629 | 318392 | 0.47 |
| ENG_PG_MOBY_DICK | `letters-per-term` | `dyn_iran_e` | 6066150 | 21.276435 | 3025065 | 3041085 | 238794 | 0.42 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_iran_e` | 113877707 | 20.754086 | 56539327 | 57338380 | 1352406 | 9.458 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_iran_e` | 106696316 | 20.741638 | 52906493 | 53789823 | 1014305 | 6.444 |
| ENG_PG_WAR_PEACE | `full-span` | `dyn_iran_e` | 50720110 | 24.019645 | 25587818 | 25132292 | 838970 | 3.897 |
| ENG_PG_WAR_PEACE | `letters-per-term` | `dyn_iran_e` | 47447664 | 23.967901 | 23944368 | 23503296 | 629228 | 4.583 |
| KJV | `full-span` | `dyn_iran_e` | 64362163 | 18.585397 | 30612275 | 33749888 | 1074408 | 4.006 |
| KJV | `letters-per-term` | `dyn_iran_e` | 60142774 | 18.524796 | 28878687 | 31264087 | 805806 | 3.825 |
| BYZ_NT | `full-span` | `dyn_iran_g` | 4749326 | 29.881168 | 2347365 | 2401961 | 230175 | 0.185 |
| BYZ_NT | `letters-per-term` | `dyn_iran_g` | 4455938 | 29.90433 | 2205604 | 2250334 | 172631 | 0.181 |
| GRC_PERSEUS_HERODOTUS | `full-span` | `dyn_iran_g` | 9046396 | 29.311538 | 4564262 | 4482134 | 320744 | 0.388 |
| GRC_PERSEUS_HERODOTUS | `letters-per-term` | `dyn_iran_g` | 8481467 | 29.313196 | 4273358 | 4208109 | 240558 | 0.347 |
| GRC_PERSEUS_ILIAD | `full-span` | `dyn_iran_g` | 3579561 | 35.234254 | 1781181 | 1798380 | 184024 | 0.159 |
| GRC_PERSEUS_ILIAD | `letters-per-term` | `dyn_iran_g` | 3356718 | 35.243502 | 1675663 | 1681055 | 138018 | 0.142 |
| GRC_PERSEUS_ODYSSEY | `full-span` | `dyn_iran_g` | 1997138 | 32.853146 | 999230 | 997908 | 142350 | 0.089 |
| GRC_PERSEUS_ODYSSEY | `letters-per-term` | `dyn_iran_g` | 1873395 | 32.872048 | 935615 | 937780 | 106763 | 0.087 |
| LXX | `full-span` | `dyn_iran_g` | 81141888 | 31.230634 | 40722473 | 40419415 | 930619 | 3.136 |
| LXX | `letters-per-term` | `dyn_iran_g` | 76103789 | 31.244304 | 38278160 | 37825629 | 697964 | 2.549 |
| SBLGNT | `full-span` | `dyn_iran_g` | 4615073 | 29.953138 | 2279426 | 2335647 | 226626 | 0.183 |
| SBLGNT | `letters-per-term` | `dyn_iran_g` | 4329245 | 29.971279 | 2141346 | 2187899 | 169969 | 0.17 |
| TCG_NT | `full-span` | `dyn_iran_g` | 4582262 | 29.049493 | 2276296 | 2305966 | 229304 | 0.186 |
| TCG_NT | `letters-per-term` | `dyn_iran_g` | 4299461 | 29.073797 | 2139014 | 2160447 | 171978 | 0.172 |
| TR_NT | `full-span` | `dyn_iran_g` | 4625438 | 29.076099 | 2296648 | 2328790 | 230276 | 0.191 |
| TR_NT | `letters-per-term` | `dyn_iran_g` | 4339610 | 29.098013 | 2158343 | 2181267 | 172707 | 0.166 |
| EBIBLE_WLC | `full-span` | `dyn_iran_h` | 667552 | 1.863505 | 330660 | 336892 | 299260 | 0.394 |
| EBIBLE_WLC | `letters-per-term` | `dyn_iran_h` | 639496 | 1.859569 | 317932 | 321564 | 239408 | 0.403 |
| HEB_PBY_AHAD_HAAM | `full-span` | `dyn_iran_h` | 2117348 | 1.113288 | 1066357 | 1050991 | 689546 | 1.835 |
| HEB_PBY_AHAD_HAAM | `letters-per-term` | `dyn_iran_h` | 2031750 | 1.112792 | 1022322 | 1009428 | 551637 | 1.743 |
| HEB_PBY_BIALIK | `full-span` | `dyn_iran_h` | 11349335 | 1.389463 | 5653959 | 5695376 | 1428999 | 10.194 |
| HEB_PBY_BIALIK | `letters-per-term` | `dyn_iran_h` | 10892887 | 1.389148 | 5439423 | 5453464 | 1143199 | 9.156 |
| HEB_PBY_BRENNER | `full-span` | `dyn_iran_h` | 10108513 | 1.302672 | 4952336 | 5156177 | 1392825 | 8.633 |
| HEB_PBY_BRENNER | `letters-per-term` | `dyn_iran_h` | 9710668 | 1.303544 | 4777968 | 4932700 | 1114260 | 7.997 |
| MAM | `full-span` | `dyn_iran_h` | 696330 | 1.927918 | 353369 | 342961 | 300493 | 0.419 |
| MAM | `letters-per-term` | `dyn_iran_h` | 667107 | 1.923967 | 338544 | 328563 | 240395 | 0.391 |
| MT_WLC | `full-span` | `dyn_iran_h` | 691579 | 1.930578 | 350026 | 341553 | 299260 | 0.417 |
| MT_WLC | `letters-per-term` | `dyn_iran_h` | 662614 | 1.926793 | 335234 | 327380 | 239408 | 0.391 |
| UHB | `full-span` | `dyn_iran_h` | 668069 | 1.869375 | 330871 | 337198 | 298905 | 0.402 |
| UHB | `letters-per-term` | `dyn_iran_h` | 640409 | 1.866645 | 318385 | 322024 | 239124 | 0.389 |
| UXLC | `full-span` | `dyn_iran_h` | 692152 | 1.932174 | 351032 | 341120 | 299260 | 0.446 |
| UXLC | `letters-per-term` | `dyn_iran_h` | 662722 | 1.927104 | 336075 | 326647 | 239408 | 0.383 |
| ENG_PG_MOBY_DICK | `full-span` | `dyn_netanyahu_e` | 1 | 9e-06 | 0 | 1 | 119397 | 0.029 |
| ENG_PG_MOBY_DICK | `letters-per-term` | `dyn_netanyahu_e` | 1 | 9e-06 | 0 | 1 | 106130 | 0.03 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_netanyahu_e` | 20 | 1e-05 | 11 | 9 | 507152 | 1.891 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_netanyahu_e` | 20 | 1e-05 | 11 | 9 | 450802 | 1.262 |
| ENG_PG_WAR_PEACE | `full-span` | `dyn_netanyahu_e` | 6 | 8e-06 | 2 | 4 | 314614 | 0.216 |
| ENG_PG_WAR_PEACE | `letters-per-term` | `dyn_netanyahu_e` | 6 | 8e-06 | 2 | 4 | 279657 | 0.264 |
| KJV | `full-span` | `dyn_netanyahu_e` | 27 | 2.1e-05 | 8 | 19 | 402903 | 0.277 |
| KJV | `letters-per-term` | `dyn_netanyahu_e` | 27 | 2.1e-05 | 8 | 19 | 358136 | 0.262 |
| BYZ_NT | `full-span` | `dyn_netanyahu_g` | 0 | 0.0 | 0 | 0 | 76725 | 0.016 |
| BYZ_NT | `letters-per-term` | `dyn_netanyahu_g` | 0 | 0.0 | 0 | 0 | 69052 | 0.016 |
| GRC_PERSEUS_HERODOTUS | `full-span` | `dyn_netanyahu_g` | 0 | 0.0 | 0 | 0 | 106914 | 0.033 |
| GRC_PERSEUS_HERODOTUS | `letters-per-term` | `dyn_netanyahu_g` | 0 | 0.0 | 0 | 0 | 96223 | 0.032 |
| GRC_PERSEUS_ILIAD | `full-span` | `dyn_netanyahu_g` | 0 | 0.0 | 0 | 0 | 61341 | 0.012 |
| GRC_PERSEUS_ILIAD | `letters-per-term` | `dyn_netanyahu_g` | 0 | 0.0 | 0 | 0 | 55207 | 0.011 |
| GRC_PERSEUS_ODYSSEY | `full-span` | `dyn_netanyahu_g` | 0 | 0.0 | 0 | 0 | 47450 | 0.005 |
| GRC_PERSEUS_ODYSSEY | `letters-per-term` | `dyn_netanyahu_g` | 0 | 0.0 | 0 | 0 | 42705 | 0.005 |
| LXX | `full-span` | `dyn_netanyahu_g` | 2 | 2e-06 | 1 | 1 | 310206 | 0.203 |
| LXX | `letters-per-term` | `dyn_netanyahu_g` | 2 | 2e-06 | 1 | 1 | 279185 | 0.17 |
| SBLGNT | `full-span` | `dyn_netanyahu_g` | 0 | 0.0 | 0 | 0 | 75542 | 0.016 |
| SBLGNT | `letters-per-term` | `dyn_netanyahu_g` | 0 | 0.0 | 0 | 0 | 67987 | 0.015 |
| TCG_NT | `full-span` | `dyn_netanyahu_g` | 1 | 1.9e-05 | 1 | 0 | 76434 | 0.015 |
| TCG_NT | `letters-per-term` | `dyn_netanyahu_g` | 1 | 1.9e-05 | 1 | 0 | 68791 | 0.016 |
| TR_NT | `full-span` | `dyn_netanyahu_g` | 1 | 1.9e-05 | 1 | 0 | 76758 | 0.015 |
| TR_NT | `letters-per-term` | `dyn_netanyahu_g` | 0 | 0.0 | 0 | 0 | 69083 | 0.015 |
| EBIBLE_WLC | `full-span` | `dyn_netanyahu_h` | 33283 | 0.116139 | 16719 | 16564 | 239408 | 0.343 |
| EBIBLE_WLC | `letters-per-term` | `dyn_netanyahu_h` | 32299 | 0.115926 | 16281 | 16018 | 199507 | 0.35 |
| HEB_PBY_AHAD_HAAM | `full-span` | `dyn_netanyahu_h` | 195658 | 0.128595 | 96021 | 99637 | 551636 | 1.968 |
| HEB_PBY_AHAD_HAAM | `letters-per-term` | `dyn_netanyahu_h` | 190236 | 0.128604 | 93403 | 96833 | 459697 | 1.863 |
| HEB_PBY_BIALIK | `full-span` | `dyn_netanyahu_h` | 763870 | 0.116898 | 380351 | 383519 | 1143199 | 10.056 |
| HEB_PBY_BIALIK | `letters-per-term` | `dyn_netanyahu_h` | 742722 | 0.116909 | 369305 | 373417 | 952666 | 8.858 |
| HEB_PBY_BRENNER | `full-span` | `dyn_netanyahu_h` | 920932 | 0.148349 | 457400 | 463532 | 1114260 | 12.447 |
| HEB_PBY_BRENNER | `letters-per-term` | `dyn_netanyahu_h` | 894191 | 0.148157 | 444130 | 450061 | 928550 | 11.666 |
| MAM | `full-span` | `dyn_netanyahu_h` | 33608 | 0.116313 | 16731 | 16877 | 240394 | 0.343 |
| MAM | `letters-per-term` | `dyn_netanyahu_h` | 32765 | 0.116635 | 16375 | 16390 | 200329 | 0.359 |
| MT_WLC | `full-span` | `dyn_netanyahu_h` | 33401 | 0.116551 | 16414 | 16987 | 239408 | 0.356 |
| MT_WLC | `letters-per-term` | `dyn_netanyahu_h` | 32519 | 0.116715 | 16017 | 16502 | 199507 | 0.329 |
| UHB | `full-span` | `dyn_netanyahu_h` | 33663 | 0.117744 | 16764 | 16899 | 239124 | 0.344 |
| UHB | `letters-per-term` | `dyn_netanyahu_h` | 32750 | 0.117824 | 16358 | 16392 | 199270 | 0.35 |
| UXLC | `full-span` | `dyn_netanyahu_h` | 32953 | 0.114988 | 16307 | 16646 | 239408 | 0.368 |
| UXLC | `letters-per-term` | `dyn_netanyahu_h` | 32117 | 0.115272 | 15933 | 16184 | 199507 | 0.332 |
| ENG_PG_MOBY_DICK | `full-span` | `dyn_simsberry_e` | 0 | 0.0 | 0 | 0 | 119397 | 0.019 |
| ENG_PG_MOBY_DICK | `letters-per-term` | `dyn_simsberry_e` | 0 | 0.0 | 0 | 0 | 106130 | 0.018 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_simsberry_e` | 1 | 0.0 | 1 | 0 | 507152 | 0.376 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_simsberry_e` | 1 | 0.0 | 1 | 0 | 450802 | 0.343 |
| ENG_PG_WAR_PEACE | `full-span` | `dyn_simsberry_e` | 0 | 0.0 | 0 | 0 | 314614 | 0.085 |
| ENG_PG_WAR_PEACE | `letters-per-term` | `dyn_simsberry_e` | 0 | 0.0 | 0 | 0 | 279657 | 0.076 |
| KJV | `full-span` | `dyn_simsberry_e` | 2 | 2e-06 | 1 | 1 | 402903 | 0.124 |
| KJV | `letters-per-term` | `dyn_simsberry_e` | 2 | 2e-06 | 1 | 1 | 358136 | 0.114 |
| ENG_PG_MOBY_DICK | `full-span` | `dyn_simscorner_e` | 0 | 0.0 | 0 | 0 | 106130 | 0.053 |
| ENG_PG_MOBY_DICK | `letters-per-term` | `dyn_simscorner_e` | 0 | 0.0 | 0 | 0 | 95517 | 0.044 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_simscorner_e` | 1 | 1e-06 | 0 | 1 | 450802 | 1.605 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_simscorner_e` | 1 | 1e-06 | 0 | 1 | 405722 | 1.125 |
| ENG_PG_WAR_PEACE | `full-span` | `dyn_simscorner_e` | 1 | 1e-06 | 1 | 0 | 279656 | 0.358 |
| ENG_PG_WAR_PEACE | `letters-per-term` | `dyn_simscorner_e` | 1 | 1e-06 | 1 | 0 | 251691 | 0.348 |
| KJV | `full-span` | `dyn_simscorner_e` | 0 | 0.0 | 0 | 0 | 358136 | 0.331 |
| KJV | `letters-per-term` | `dyn_simscorner_e` | 0 | 0.0 | 0 | 0 | 322322 | 0.317 |
| ENG_PG_MOBY_DICK | `full-span` | `dyn_trump_e` | 14601 | 0.064015 | 6844 | 7757 | 238794 | 0.052 |
| ENG_PG_MOBY_DICK | `letters-per-term` | `dyn_trump_e` | 13953 | 0.063723 | 6560 | 7393 | 191035 | 0.046 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_trump_e` | 335790 | 0.081597 | 168762 | 167028 | 1014305 | 0.884 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_trump_e` | 321599 | 0.081404 | 161302 | 160297 | 811444 | 0.651 |
| ENG_PG_WAR_PEACE | `full-span` | `dyn_trump_e` | 93018 | 0.058734 | 45865 | 47153 | 629228 | 0.308 |
| ENG_PG_WAR_PEACE | `letters-per-term` | `dyn_trump_e` | 89149 | 0.058637 | 44046 | 45103 | 503382 | 0.426 |
| KJV | `full-span` | `dyn_trump_e` | 111371 | 0.04288 | 56380 | 54991 | 805806 | 0.3 |
| KJV | `letters-per-term` | `dyn_trump_e` | 106975 | 0.042903 | 54418 | 52557 | 644645 | 0.283 |
| BYZ_NT | `full-span` | `dyn_trump_g` | 31645 | 0.265467 | 15856 | 15789 | 172631 | 0.051 |
| BYZ_NT | `letters-per-term` | `dyn_trump_g` | 30471 | 0.26627 | 15259 | 15212 | 138105 | 0.05 |
| GRC_PERSEUS_HERODOTUS | `full-span` | `dyn_trump_g` | 68470 | 0.295804 | 34297 | 34173 | 240558 | 0.095 |
| GRC_PERSEUS_HERODOTUS | `letters-per-term` | `dyn_trump_g` | 65855 | 0.296361 | 33073 | 32782 | 192447 | 0.083 |
| GRC_PERSEUS_ILIAD | `full-span` | `dyn_trump_g` | 23534 | 0.308867 | 11959 | 11575 | 138018 | 0.053 |
| GRC_PERSEUS_ILIAD | `letters-per-term` | `dyn_trump_g` | 22580 | 0.308695 | 11461 | 11119 | 110414 | 0.045 |
| GRC_PERSEUS_ODYSSEY | `full-span` | `dyn_trump_g` | 13100 | 0.287331 | 6539 | 6561 | 106762 | 0.026 |
| GRC_PERSEUS_ODYSSEY | `letters-per-term` | `dyn_trump_g` | 12571 | 0.287217 | 6259 | 6312 | 85410 | 0.024 |
| LXX | `full-span` | `dyn_trump_g` | 487148 | 0.249998 | 253005 | 234143 | 697964 | 0.755 |
| LXX | `letters-per-term` | `dyn_trump_g` | 467153 | 0.249726 | 242038 | 225115 | 558371 | 0.619 |
| SBLGNT | `full-span` | `dyn_trump_g` | 31044 | 0.268647 | 15711 | 15333 | 169969 | 0.046 |
| SBLGNT | `letters-per-term` | `dyn_trump_g` | 29850 | 0.269078 | 15113 | 14737 | 135975 | 0.047 |
| TCG_NT | `full-span` | `dyn_trump_g` | 32265 | 0.272729 | 16274 | 15991 | 171978 | 0.047 |
| TCG_NT | `letters-per-term` | `dyn_trump_g` | 31080 | 0.273659 | 15652 | 15428 | 137582 | 0.055 |
| TR_NT | `full-span` | `dyn_trump_g` | 32068 | 0.268779 | 16199 | 15869 | 172707 | 0.048 |
| TR_NT | `letters-per-term` | `dyn_trump_g` | 30916 | 0.269921 | 15623 | 15293 | 138166 | 0.047 |
| EBIBLE_WLC | `full-span` | `dyn_trump_h` | 10628 | 0.029669 | 5415 | 5213 | 299260 | 0.013 |
| EBIBLE_WLC | `letters-per-term` | `dyn_trump_h` | 10212 | 0.029695 | 5208 | 5004 | 239408 | 0.014 |
| HEB_PBY_AHAD_HAAM | `full-span` | `dyn_trump_h` | 92451 | 0.04861 | 46089 | 46362 | 689546 | 0.129 |
| HEB_PBY_AHAD_HAAM | `letters-per-term` | `dyn_trump_h` | 88735 | 0.0486 | 44244 | 44491 | 551637 | 0.121 |
| HEB_PBY_BIALIK | `full-span` | `dyn_trump_h` | 526134 | 0.064413 | 271693 | 254441 | 1428999 | 0.715 |
| HEB_PBY_BIALIK | `letters-per-term` | `dyn_trump_h` | 503435 | 0.064202 | 259652 | 243783 | 1143199 | 0.654 |
| HEB_PBY_BRENNER | `full-span` | `dyn_trump_h` | 461367 | 0.059456 | 235167 | 226200 | 1392825 | 0.787 |
| HEB_PBY_BRENNER | `letters-per-term` | `dyn_trump_h` | 444176 | 0.059625 | 226088 | 218088 | 1114260 | 0.654 |
| MAM | `full-span` | `dyn_trump_h` | 10936 | 0.030278 | 5602 | 5334 | 300493 | 0.013 |
| MAM | `letters-per-term` | `dyn_trump_h` | 10593 | 0.030551 | 5416 | 5177 | 240395 | 0.015 |
| MT_WLC | `full-span` | `dyn_trump_h` | 10636 | 0.029691 | 5443 | 5193 | 299260 | 0.013 |
| MT_WLC | `letters-per-term` | `dyn_trump_h` | 10266 | 0.029852 | 5233 | 5033 | 239408 | 0.013 |
| UHB | `full-span` | `dyn_trump_h` | 10468 | 0.029291 | 5377 | 5091 | 298905 | 0.013 |
| UHB | `letters-per-term` | `dyn_trump_h` | 10073 | 0.02936 | 5169 | 4904 | 239124 | 0.014 |
| UXLC | `full-span` | `dyn_trump_h` | 10692 | 0.029847 | 5371 | 5321 | 299260 | 0.015 |
| UXLC | `letters-per-term` | `dyn_trump_h` | 10336 | 0.030056 | 5194 | 5142 | 239408 | 0.013 |
| ENG_PG_MOBY_DICK | `full-span` | `dyn_vance_e` | 34314 | 0.150442 | 17301 | 17013 | 238794 | 0.023 |
| ENG_PG_MOBY_DICK | `letters-per-term` | `dyn_vance_e` | 32959 | 0.150522 | 16623 | 16336 | 191035 | 0.024 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_vance_e` | 560612 | 0.136228 | 273226 | 287386 | 1014305 | 0.444 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_vance_e` | 535915 | 0.135653 | 261167 | 274748 | 811444 | 0.365 |
| ENG_PG_WAR_PEACE | `full-span` | `dyn_vance_e` | 299257 | 0.18896 | 156373 | 142884 | 629228 | 0.211 |
| ENG_PG_WAR_PEACE | `letters-per-term` | `dyn_vance_e` | 286537 | 0.188467 | 149281 | 137256 | 503382 | 0.239 |
| KJV | `full-span` | `dyn_vance_e` | 294941 | 0.113557 | 147222 | 147719 | 805806 | 0.16 |
| KJV | `letters-per-term` | `dyn_vance_e` | 283997 | 0.1139 | 141863 | 142134 | 644645 | 0.165 |
| BYZ_NT | `full-span` | `dyn_vance_g` | 573495 | 3.608238 | 311322 | 262173 | 230175 | 0.029 |
| BYZ_NT | `letters-per-term` | `dyn_vance_g` | 532257 | 3.57204 | 288944 | 243313 | 172631 | 0.028 |
| GRC_PERSEUS_HERODOTUS | `full-span` | `dyn_vance_g` | 1235733 | 4.003941 | 616144 | 619589 | 320744 | 0.053 |
| GRC_PERSEUS_HERODOTUS | `letters-per-term` | `dyn_vance_g` | 1163484 | 4.021172 | 580498 | 582986 | 240558 | 0.051 |
| GRC_PERSEUS_ILIAD | `full-span` | `dyn_vance_g` | 325999 | 3.208866 | 167720 | 158279 | 184024 | 0.017 |
| GRC_PERSEUS_ILIAD | `letters-per-term` | `dyn_vance_g` | 306926 | 3.222537 | 157145 | 149781 | 138018 | 0.017 |
| GRC_PERSEUS_ODYSSEY | `full-span` | `dyn_vance_g` | 185209 | 3.046709 | 91212 | 93997 | 142350 | 0.01 |
| GRC_PERSEUS_ODYSSEY | `letters-per-term` | `dyn_vance_g` | 174806 | 3.067282 | 86057 | 88749 | 106763 | 0.009 |
| LXX | `full-span` | `dyn_vance_g` | 14641657 | 5.635415 | 7533880 | 7107777 | 930619 | 0.628 |
| LXX | `letters-per-term` | `dyn_vance_g` | 13769567 | 5.653076 | 7101558 | 6668009 | 697964 | 0.538 |
| SBLGNT | `full-span` | `dyn_vance_g` | 557336 | 3.617269 | 302638 | 254698 | 226626 | 0.028 |
| SBLGNT | `letters-per-term` | `dyn_vance_g` | 517428 | 3.582144 | 280976 | 236452 | 169969 | 0.026 |
| TCG_NT | `full-span` | `dyn_vance_g` | 551791 | 3.498108 | 301045 | 250746 | 229304 | 0.028 |
| TCG_NT | `letters-per-term` | `dyn_vance_g` | 512457 | 3.465335 | 279376 | 233081 | 171978 | 0.027 |
| TR_NT | `full-span` | `dyn_vance_g` | 568362 | 3.572797 | 309541 | 258821 | 230276 | 0.029 |
| TR_NT | `letters-per-term` | `dyn_vance_g` | 527131 | 3.534526 | 286822 | 240309 | 172707 | 0.03 |
| EBIBLE_WLC | `full-span` | `dyn_vance_h` | 1173157 | 2.45619 | 627223 | 545934 | 399013 | 0.097 |
| EBIBLE_WLC | `letters-per-term` | `dyn_vance_h` | 1105311 | 2.468421 | 585079 | 520232 | 299260 | 0.097 |
| HEB_PBY_AHAD_HAAM | `full-span` | `dyn_vance_h` | 10884247 | 4.292144 | 5522245 | 5362002 | 919394 | 0.709 |
| HEB_PBY_AHAD_HAAM | `letters-per-term` | `dyn_vance_h` | 10189764 | 4.286164 | 5165388 | 5024376 | 689546 | 0.631 |
| HEB_PBY_BIALIK | `full-span` | `dyn_vance_h` | 51012008 | 4.683926 | 26931175 | 24080833 | 1905332 | 3.501 |
| HEB_PBY_BIALIK | `letters-per-term` | `dyn_vance_h` | 47878160 | 4.689256 | 25189641 | 22688519 | 1428999 | 3.138 |
| HEB_PBY_BRENNER | `full-span` | `dyn_vance_h` | 52306899 | 5.055542 | 26013568 | 26293331 | 1857100 | 3.463 |
| HEB_PBY_BRENNER | `letters-per-term` | `dyn_vance_h` | 48905972 | 5.041959 | 24327330 | 24578642 | 1392825 | 2.981 |
| MAM | `full-span` | `dyn_vance_h` | 1224569 | 2.542827 | 651441 | 573128 | 400658 | 0.101 |
| MAM | `letters-per-term` | `dyn_vance_h` | 1150614 | 2.548545 | 610524 | 540090 | 300493 | 0.097 |
| MT_WLC | `full-span` | `dyn_vance_h` | 1191206 | 2.493978 | 629600 | 561606 | 399013 | 0.101 |
| MT_WLC | `letters-per-term` | `dyn_vance_h` | 1119832 | 2.50085 | 591227 | 528605 | 299260 | 0.097 |
| UHB | `full-span` | `dyn_vance_h` | 1170235 | 2.455887 | 625307 | 544928 | 398541 | 0.104 |
| UHB | `letters-per-term` | `dyn_vance_h` | 1102787 | 2.468628 | 583469 | 519318 | 298906 | 0.1 |
| UXLC | `full-span` | `dyn_vance_h` | 1189894 | 2.491227 | 629433 | 560461 | 399014 | 0.104 |
| UXLC | `letters-per-term` | `dyn_vance_h` | 1118804 | 2.49855 | 591039 | 527765 | 299260 | 0.095 |

## Highest Counts

| Corpus | Mode | Term | Count | Rate / 1M positions | Forward | Backward | Max skip | Seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| HEB_PBY_BRENNER | `full-span` | `dyn_beast_h` | 3663683890 | 236.066963 | 1792563226 | 1871120664 | 2785650 | 11.897 |
| HEB_PBY_BRENNER | `letters-per-term` | `dyn_beast_h` | 3244013040 | 235.154 | 1588402936 | 1655610104 | 1857100 | 10.284 |
| HEB_PBY_BIALIK | `full-span` | `dyn_beast_h` | 3152690416 | 192.986749 | 1572071879 | 1580618537 | 2857999 | 10.766 |
| HEB_PBY_BIALIK | `letters-per-term` | `dyn_beast_h` | 2779486065 | 191.409367 | 1390497494 | 1388988571 | 1905333 | 9.212 |
| HEB_PBY_BRENNER | `full-span` | `dyn_yhwh_h` | 1090879372 | 105.435155 | 546231593 | 544647779 | 1857100 | 37.969 |
| HEB_PBY_BRENNER | `letters-per-term` | `dyn_yhwh_h` | 1025070165 | 105.679571 | 508977483 | 516092682 | 1392825 | 33.169 |
| HEB_PBY_AHAD_HAAM | `full-span` | `dyn_beast_h` | 816402749 | 214.629105 | 411007375 | 405395374 | 1379092 | 2.626 |
| HEB_PBY_BIALIK | `full-span` | `dyn_yhwh_h` | 803341146 | 73.762845 | 397480634 | 405860512 | 1905332 | 31.208 |
| HEB_PBY_BIALIK | `letters-per-term` | `dyn_yhwh_h` | 750178065 | 73.473514 | 372666828 | 377511237 | 1428999 | 27.888 |
| HEB_PBY_AHAD_HAAM | `letters-per-term` | `dyn_beast_h` | 726225924 | 214.787215 | 365674244 | 360551680 | 919395 | 2.37 |
| HEB_PBY_BRENNER | `full-span` | `dyn_gog_h` | 266462544 | 17.169332 | 133231272 | 133231272 | 2785650 | 1.069 |
| HEB_PBY_BIALIK | `full-span` | `dyn_gog_h` | 259364876 | 15.876594 | 129682438 | 129682438 | 2857999 | 1.084 |
| HEB_PBY_BRENNER | `letters-per-term` | `dyn_gog_h` | 236139146 | 17.117399 | 118069573 | 118069573 | 1857100 | 0.885 |
| HEB_PBY_AHAD_HAAM | `full-span` | `dyn_yhwh_h` | 230979253 | 91.085419 | 115567068 | 115412185 | 919394 | 7.463 |
| HEB_PBY_BIALIK | `letters-per-term` | `dyn_gog_h` | 230546384 | 15.876582 | 115273192 | 115273192 | 1905333 | 0.899 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_gog_e` | 217556768 | 26.432967 | 108778384 | 108778384 | 2028610 | 1.561 |
| HEB_PBY_AHAD_HAAM | `letters-per-term` | `dyn_yhwh_h` | 217049309 | 91.298375 | 108811566 | 108237743 | 689546 | 7.059 |
| HEB_PBY_BIALIK | `full-span` | `dyn_yeshua_h` | 206897417 | 18.997337 | 105093398 | 101804019 | 1905332 | 10.338 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_gog_e` | 195401464 | 26.708755 | 97700732 | 97700732 | 1352407 | 2.754 |
| HEB_PBY_BIALIK | `letters-per-term` | `dyn_yeshua_h` | 193278640 | 18.929987 | 97657710 | 95620930 | 1428999 | 8.932 |
| HEB_PBY_BRENNER | `full-span` | `dyn_yeshua_h` | 188603935 | 18.228858 | 94124359 | 94479576 | 1857100 | 9.035 |
| HEB_PBY_BRENNER | `letters-per-term` | `dyn_yeshua_h` | 177328499 | 18.281675 | 88411275 | 88917224 | 1392825 | 7.758 |
| EBIBLE_WLC | `full-span` | `dyn_beast_h` | 165249617 | 230.650211 | 81298593 | 83951024 | 598520 | 0.506 |
| UHB | `full-span` | `dyn_beast_h` | 164784929 | 230.547499 | 81138119 | 83646810 | 597811 | 0.501 |
| MAM | `full-span` | `dyn_beast_h` | 164260192 | 227.391182 | 79001910 | 85258282 | 600987 | 0.511 |
| UXLC | `full-span` | `dyn_beast_h` | 163014892 | 227.530672 | 78430890 | 84584002 | 598521 | 0.499 |
| MT_WLC | `full-span` | `dyn_beast_h` | 163013648 | 227.529316 | 78424064 | 84589584 | 598520 | 0.501 |
| EBIBLE_WLC | `letters-per-term` | `dyn_beast_h` | 145720847 | 228.81664 | 71375480 | 74345367 | 399014 | 0.458 |
| HEB_PBY_BRENNER | `full-span` | `dyn_dragon_h` | 145655795 | 14.077855 | 73609067 | 72046728 | 1857100 | 8.674 |
| UHB | `letters-per-term` | `dyn_beast_h` | 145320748 | 228.730066 | 71247177 | 74073571 | 398541 | 0.445 |
| MAM | `letters-per-term` | `dyn_beast_h` | 145064411 | 225.920102 | 70073524 | 74990887 | 400658 | 0.498 |
| MT_WLC | `letters-per-term` | `dyn_beast_h` | 143940754 | 226.021468 | 69545127 | 74395627 | 399014 | 0.447 |
| UXLC | `letters-per-term` | `dyn_beast_h` | 143929815 | 226.004008 | 69544905 | 74384910 | 399014 | 0.451 |
| HEB_PBY_BIALIK | `full-span` | `dyn_dragon_h` | 143129945 | 13.142202 | 69685826 | 73444119 | 1905332 | 9.321 |
| HEB_PBY_BRENNER | `letters-per-term` | `dyn_dragon_h` | 136577711 | 14.080474 | 68741850 | 67835861 | 1392825 | 7.869 |
| HEB_PBY_BIALIK | `letters-per-term` | `dyn_dragon_h` | 133977408 | 13.121939 | 65147942 | 68829466 | 1428999 | 8.388 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_iran_e` | 113877707 | 20.754086 | 56539327 | 57338380 | 1352406 | 9.458 |
| KJV | `full-span` | `dyn_gog_e` | 112614748 | 21.679279 | 56307374 | 56307374 | 1611612 | 0.553 |
| HEB_PBY_BIALIK | `full-span` | `dyn_messiah_h` | 110129394 | 10.112089 | 58687488 | 51441906 | 1905332 | 6.936 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_iran_e` | 106696316 | 20.741638 | 52906493 | 53789823 | 1014305 | 6.444 |

## Lowest Nonzero Counts

| Corpus | Mode | Term | Count | Rate / 1M positions | Forward | Backward | Max skip | Seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| TCG_NT | `letters-per-term` | `dyn_netanyahu_g` | 1 | 1.9e-05 | 1 | 0 | 68791 | 0.016 |
| TR_NT | `full-span` | `dyn_netanyahu_g` | 1 | 1.9e-05 | 1 | 0 | 76758 | 0.015 |
| TCG_NT | `full-span` | `dyn_netanyahu_g` | 1 | 1.9e-05 | 1 | 0 | 76434 | 0.015 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_simsberry_e` | 1 | 0.0 | 1 | 0 | 450802 | 0.343 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_simscorner_e` | 1 | 1e-06 | 0 | 1 | 405722 | 1.125 |
| ENG_PG_WAR_PEACE | `letters-per-term` | `dyn_simscorner_e` | 1 | 1e-06 | 1 | 0 | 251691 | 0.348 |
| ENG_PG_MOBY_DICK | `letters-per-term` | `dyn_netanyahu_e` | 1 | 9e-06 | 0 | 1 | 106130 | 0.03 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_simsberry_e` | 1 | 0.0 | 1 | 0 | 507152 | 0.376 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_simscorner_e` | 1 | 1e-06 | 0 | 1 | 450802 | 1.605 |
| ENG_PG_WAR_PEACE | `full-span` | `dyn_simscorner_e` | 1 | 1e-06 | 1 | 0 | 279656 | 0.358 |
| ENG_PG_MOBY_DICK | `full-span` | `dyn_netanyahu_e` | 1 | 9e-06 | 0 | 1 | 119397 | 0.029 |
| KJV | `letters-per-term` | `dyn_simsberry_e` | 2 | 2e-06 | 1 | 1 | 358136 | 0.114 |
| LXX | `letters-per-term` | `dyn_netanyahu_g` | 2 | 2e-06 | 1 | 1 | 279185 | 0.17 |
| KJV | `full-span` | `dyn_simsberry_e` | 2 | 2e-06 | 1 | 1 | 402903 | 0.124 |
| LXX | `full-span` | `dyn_netanyahu_g` | 2 | 2e-06 | 1 | 1 | 310206 | 0.203 |
| ENG_PG_WAR_PEACE | `letters-per-term` | `dyn_netanyahu_e` | 6 | 8e-06 | 2 | 4 | 279657 | 0.264 |
| ENG_PG_WAR_PEACE | `full-span` | `dyn_netanyahu_e` | 6 | 8e-06 | 2 | 4 | 314614 | 0.216 |
| ENG_PG_SHAKESPEARE | `letters-per-term` | `dyn_netanyahu_e` | 20 | 1e-05 | 11 | 9 | 450802 | 1.262 |
| ENG_PG_SHAKESPEARE | `full-span` | `dyn_netanyahu_e` | 20 | 1e-05 | 11 | 9 | 507152 | 1.891 |
| ENG_PG_MOBY_DICK | `letters-per-term` | `dyn_catering_e` | 21 | 0.000164 | 13 | 8 | 119397 | 0.028 |
| ENG_PG_MOBY_DICK | `full-span` | `dyn_catering_e` | 22 | 0.000169 | 13 | 9 | 136453 | 0.028 |
| KJV | `letters-per-term` | `dyn_netanyahu_e` | 27 | 2.1e-05 | 8 | 19 | 358136 | 0.262 |
| KJV | `full-span` | `dyn_netanyahu_e` | 27 | 2.1e-05 | 8 | 19 | 402903 | 0.277 |
| GRC_PERSEUS_ODYSSEY | `letters-per-term` | `dyn_christ_g` | 31 | 0.001041 | 15 | 16 | 61007 | 0.007 |
| GRC_PERSEUS_ODYSSEY | `full-span` | `dyn_christ_g` | 32 | 0.001053 | 15 | 17 | 71175 | 0.008 |
| GRC_PERSEUS_ILIAD | `letters-per-term` | `dyn_christ_g` | 68 | 0.001367 | 35 | 33 | 78867 | 0.017 |
| GRC_PERSEUS_ILIAD | `full-span` | `dyn_christ_g` | 69 | 0.001358 | 35 | 34 | 92012 | 0.017 |
| TR_NT | `letters-per-term` | `dyn_christ_g` | 70 | 0.000898 | 33 | 37 | 98690 | 0.016 |
| TR_NT | `full-span` | `dyn_christ_g` | 73 | 0.000918 | 35 | 38 | 115138 | 0.018 |
| BYZ_NT | `letters-per-term` | `dyn_christ_g` | 77 | 0.000989 | 37 | 40 | 98646 | 0.017 |
| TCG_NT | `letters-per-term` | `dyn_christ_g` | 79 | 0.001023 | 32 | 47 | 98273 | 0.017 |
| BYZ_NT | `full-span` | `dyn_christ_g` | 79 | 0.000994 | 39 | 40 | 115087 | 0.016 |
| SBLGNT | `letters-per-term` | `dyn_christ_g` | 80 | 0.00106 | 39 | 41 | 97125 | 0.016 |
| TCG_NT | `full-span` | `dyn_christ_g` | 80 | 0.001014 | 32 | 48 | 114652 | 0.016 |
| SBLGNT | `full-span` | `dyn_christ_g` | 85 | 0.001103 | 40 | 45 | 113313 | 0.016 |
| KJV | `letters-per-term` | `dyn_catering_e` | 95 | 6.5e-05 | 40 | 55 | 402903 | 0.143 |
| KJV | `full-span` | `dyn_catering_e` | 96 | 6.5e-05 | 40 | 56 | 460460 | 0.155 |
| ENG_PG_WAR_PEACE | `letters-per-term` | `dyn_catering_e` | 101 | 0.000113 | 54 | 47 | 314614 | 0.179 |
| ENG_PG_WAR_PEACE | `full-span` | `dyn_catering_e` | 103 | 0.000114 | 54 | 49 | 359558 | 0.187 |
| ENG_PG_MOBY_DICK | `letters-per-term` | `dyn_cowboy_e` | 145 | 0.000817 | 71 | 74 | 159196 | 0.022 |

## Read

- Zero-count rows: 19
- Large counts are expected for short terms and large skip spaces.
- These counts answer presence/density. Context, exact center-word,
  same-skip extension, and non-Bible controls remain separate reports.
