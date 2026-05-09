# Dynamic Full-Span Hit Export

This report exports full hit metadata for dynamic-span count rows whose
observed count is below the configured threshold. High-density rows are
not discarded; they are deferred for partitioned export because they can
contain millions or billions of paths.

## Reproduce

```bash
python3 -m scripts.export_dynamic_span_hits --max-count-row-hits 50000
```

## Run Counts

- selected count rows: 88
- skipped count rows: 156
- exported hit rows: 918,266
- max count row hits: 50,000
- max export hits per term/corpus/mode: 50,000
- hit CSV: `reports/dynamic_skip_focus/full_span_exported_hits.csv`

## Status Counts

| Status | Rows |
| --- | ---: |
| `exported_all_hits` | 88 |
| `skipped_above_hit_threshold` | 147 |
| `skipped_zero_hits` | 9 |

## Exported Rows

| Corpus | Term | Mode | Count row hits | Exported hits | Status |
| --- | --- | --- | ---: | ---: | --- |
| BYZ_NT | `dyn_beast_g` | `full-span` | 1583 | 1583 | `exported_all_hits` |
| BYZ_NT | `dyn_christ_g` | `full-span` | 79 | 79 | `exported_all_hits` |
| BYZ_NT | `dyn_dragon_g` | `full-span` | 579 | 579 | `exported_all_hits` |
| BYZ_NT | `dyn_jesus_g` | `full-span` | 11706 | 11706 | `exported_all_hits` |
| BYZ_NT | `dyn_magog_g` | `full-span` | 3071 | 3071 | `exported_all_hits` |
| BYZ_NT | `dyn_trump_g` | `full-span` | 31645 | 31645 | `exported_all_hits` |
| EBIBLE_WLC | `dyn_netanyahu_h` | `full-span` | 33283 | 33283 | `exported_all_hits` |
| EBIBLE_WLC | `dyn_trump_h` | `full-span` | 10628 | 10628 | `exported_all_hits` |
| ENG_PG_MOBY_DICK | `dyn_catering_e` | `full-span` | 22 | 22 | `exported_all_hits` |
| ENG_PG_MOBY_DICK | `dyn_christ_e` | `full-span` | 6769 | 6769 | `exported_all_hits` |
| ENG_PG_MOBY_DICK | `dyn_cowboy_e` | `full-span` | 149 | 149 | `exported_all_hits` |
| ENG_PG_MOBY_DICK | `dyn_dragon_e` | `full-span` | 3621 | 3621 | `exported_all_hits` |
| ENG_PG_MOBY_DICK | `dyn_jesus_e` | `full-span` | 4116 | 4116 | `exported_all_hits` |
| ENG_PG_MOBY_DICK | `dyn_magog_e` | `full-span` | 15488 | 15488 | `exported_all_hits` |
| ENG_PG_MOBY_DICK | `dyn_netanyahu_e` | `full-span` | 1 | 1 | `exported_all_hits` |
| ENG_PG_MOBY_DICK | `dyn_russia_e` | `full-span` | 7368 | 7368 | `exported_all_hits` |
| ENG_PG_MOBY_DICK | `dyn_trump_e` | `full-span` | 14601 | 14601 | `exported_all_hits` |
| ENG_PG_MOBY_DICK | `dyn_vance_e` | `full-span` | 34314 | 34314 | `exported_all_hits` |
| ENG_PG_SHAKESPEARE | `dyn_catering_e` | `full-span` | 233 | 233 | `exported_all_hits` |
| ENG_PG_SHAKESPEARE | `dyn_cowboy_e` | `full-span` | 4684 | 4684 | `exported_all_hits` |
| ENG_PG_SHAKESPEARE | `dyn_netanyahu_e` | `full-span` | 20 | 20 | `exported_all_hits` |
| ENG_PG_SHAKESPEARE | `dyn_simsberry_e` | `full-span` | 1 | 1 | `exported_all_hits` |
| ENG_PG_SHAKESPEARE | `dyn_simscorner_e` | `full-span` | 1 | 1 | `exported_all_hits` |
| ENG_PG_WAR_PEACE | `dyn_catering_e` | `full-span` | 103 | 103 | `exported_all_hits` |
| ENG_PG_WAR_PEACE | `dyn_christ_e` | `full-span` | 47240 | 47240 | `exported_all_hits` |
| ENG_PG_WAR_PEACE | `dyn_cowboy_e` | `full-span` | 1058 | 1058 | `exported_all_hits` |
| ENG_PG_WAR_PEACE | `dyn_dragon_e` | `full-span` | 32283 | 32283 | `exported_all_hits` |
| ENG_PG_WAR_PEACE | `dyn_jesus_e` | `full-span` | 20410 | 20410 | `exported_all_hits` |
| ENG_PG_WAR_PEACE | `dyn_netanyahu_e` | `full-span` | 6 | 6 | `exported_all_hits` |
| ENG_PG_WAR_PEACE | `dyn_russia_e` | `full-span` | 43322 | 43322 | `exported_all_hits` |
| ENG_PG_WAR_PEACE | `dyn_simscorner_e` | `full-span` | 1 | 1 | `exported_all_hits` |
| GRC_PERSEUS_HERODOTUS | `dyn_beast_g` | `full-span` | 2349 | 2349 | `exported_all_hits` |
| GRC_PERSEUS_HERODOTUS | `dyn_christ_g` | `full-span` | 220 | 220 | `exported_all_hits` |
| GRC_PERSEUS_HERODOTUS | `dyn_dragon_g` | `full-span` | 1334 | 1334 | `exported_all_hits` |
| GRC_PERSEUS_HERODOTUS | `dyn_jesus_g` | `full-span` | 16741 | 16741 | `exported_all_hits` |
| GRC_PERSEUS_HERODOTUS | `dyn_magog_g` | `full-span` | 4528 | 4528 | `exported_all_hits` |
| GRC_PERSEUS_ILIAD | `dyn_beast_g` | `full-span` | 1189 | 1189 | `exported_all_hits` |
| GRC_PERSEUS_ILIAD | `dyn_christ_g` | `full-span` | 69 | 69 | `exported_all_hits` |
| GRC_PERSEUS_ILIAD | `dyn_dragon_g` | `full-span` | 590 | 590 | `exported_all_hits` |
| GRC_PERSEUS_ILIAD | `dyn_jesus_g` | `full-span` | 4121 | 4121 | `exported_all_hits` |
| GRC_PERSEUS_ILIAD | `dyn_magog_g` | `full-span` | 1517 | 1517 | `exported_all_hits` |
| GRC_PERSEUS_ILIAD | `dyn_trump_g` | `full-span` | 23534 | 23534 | `exported_all_hits` |
| GRC_PERSEUS_ODYSSEY | `dyn_beast_g` | `full-span` | 764 | 764 | `exported_all_hits` |
| GRC_PERSEUS_ODYSSEY | `dyn_christ_g` | `full-span` | 32 | 32 | `exported_all_hits` |
| GRC_PERSEUS_ODYSSEY | `dyn_dragon_g` | `full-span` | 340 | 340 | `exported_all_hits` |
| GRC_PERSEUS_ODYSSEY | `dyn_jesus_g` | `full-span` | 2779 | 2779 | `exported_all_hits` |
| GRC_PERSEUS_ODYSSEY | `dyn_magog_g` | `full-span` | 872 | 872 | `exported_all_hits` |
| GRC_PERSEUS_ODYSSEY | `dyn_russia_g` | `full-span` | 33099 | 33099 | `exported_all_hits` |
| GRC_PERSEUS_ODYSSEY | `dyn_trump_g` | `full-span` | 13100 | 13100 | `exported_all_hits` |
| KJV | `dyn_catering_e` | `full-span` | 96 | 96 | `exported_all_hits` |
| KJV | `dyn_cowboy_e` | `full-span` | 998 | 998 | `exported_all_hits` |
| KJV | `dyn_dragon_e` | `full-span` | 39738 | 39738 | `exported_all_hits` |
| KJV | `dyn_netanyahu_e` | `full-span` | 27 | 27 | `exported_all_hits` |
| KJV | `dyn_russia_e` | `full-span` | 49202 | 49202 | `exported_all_hits` |
| KJV | `dyn_simsberry_e` | `full-span` | 2 | 2 | `exported_all_hits` |
| LXX | `dyn_beast_g` | `full-span` | 21650 | 21650 | `exported_all_hits` |
| LXX | `dyn_christ_g` | `full-span` | 1280 | 1280 | `exported_all_hits` |
| LXX | `dyn_dragon_g` | `full-span` | 11437 | 11437 | `exported_all_hits` |
| LXX | `dyn_magog_g` | `full-span` | 35515 | 35515 | `exported_all_hits` |
| LXX | `dyn_netanyahu_g` | `full-span` | 2 | 2 | `exported_all_hits` |
| MAM | `dyn_netanyahu_h` | `full-span` | 33608 | 33608 | `exported_all_hits` |
| MAM | `dyn_trump_h` | `full-span` | 10936 | 10936 | `exported_all_hits` |
| MT_WLC | `dyn_netanyahu_h` | `full-span` | 33401 | 33401 | `exported_all_hits` |
| MT_WLC | `dyn_trump_h` | `full-span` | 10636 | 10636 | `exported_all_hits` |
| SBLGNT | `dyn_beast_g` | `full-span` | 1470 | 1470 | `exported_all_hits` |
| SBLGNT | `dyn_christ_g` | `full-span` | 85 | 85 | `exported_all_hits` |
| SBLGNT | `dyn_dragon_g` | `full-span` | 569 | 569 | `exported_all_hits` |
| SBLGNT | `dyn_jesus_g` | `full-span` | 11218 | 11218 | `exported_all_hits` |
| SBLGNT | `dyn_magog_g` | `full-span` | 3021 | 3021 | `exported_all_hits` |
| SBLGNT | `dyn_trump_g` | `full-span` | 31044 | 31044 | `exported_all_hits` |
| TCG_NT | `dyn_beast_g` | `full-span` | 1534 | 1534 | `exported_all_hits` |
| TCG_NT | `dyn_christ_g` | `full-span` | 80 | 80 | `exported_all_hits` |
| TCG_NT | `dyn_dragon_g` | `full-span` | 616 | 616 | `exported_all_hits` |
| TCG_NT | `dyn_jesus_g` | `full-span` | 11972 | 11972 | `exported_all_hits` |
| TCG_NT | `dyn_magog_g` | `full-span` | 3271 | 3271 | `exported_all_hits` |
| TCG_NT | `dyn_netanyahu_g` | `full-span` | 1 | 1 | `exported_all_hits` |
| TCG_NT | `dyn_trump_g` | `full-span` | 32265 | 32265 | `exported_all_hits` |
| TR_NT | `dyn_beast_g` | `full-span` | 1507 | 1507 | `exported_all_hits` |
| TR_NT | `dyn_christ_g` | `full-span` | 73 | 73 | `exported_all_hits` |
| TR_NT | `dyn_dragon_g` | `full-span` | 558 | 558 | `exported_all_hits` |
| TR_NT | `dyn_jesus_g` | `full-span` | 11829 | 11829 | `exported_all_hits` |
| TR_NT | `dyn_magog_g` | `full-span` | 3217 | 3217 | `exported_all_hits` |
| TR_NT | `dyn_netanyahu_g` | `full-span` | 1 | 1 | `exported_all_hits` |
| TR_NT | `dyn_trump_g` | `full-span` | 32068 | 32068 | `exported_all_hits` |
| UHB | `dyn_netanyahu_h` | `full-span` | 33663 | 33663 | `exported_all_hits` |
| UHB | `dyn_trump_h` | `full-span` | 10468 | 10468 | `exported_all_hits` |
| UXLC | `dyn_netanyahu_h` | `full-span` | 32953 | 32953 | `exported_all_hits` |
| UXLC | `dyn_trump_h` | `full-span` | 10692 | 10692 | `exported_all_hits` |

## Deferred Rows

| Corpus | Term | Mode | Count row hits | Status |
| --- | --- | --- | ---: | --- |
| HEB_PBY_BRENNER | `dyn_beast_h` | `full-span` | 3663683890 | `skipped_above_hit_threshold` |
| HEB_PBY_BIALIK | `dyn_beast_h` | `full-span` | 3152690416 | `skipped_above_hit_threshold` |
| HEB_PBY_BRENNER | `dyn_yhwh_h` | `full-span` | 1090879372 | `skipped_above_hit_threshold` |
| HEB_PBY_AHAD_HAAM | `dyn_beast_h` | `full-span` | 816402749 | `skipped_above_hit_threshold` |
| HEB_PBY_BIALIK | `dyn_yhwh_h` | `full-span` | 803341146 | `skipped_above_hit_threshold` |
| HEB_PBY_BRENNER | `dyn_gog_h` | `full-span` | 266462544 | `skipped_above_hit_threshold` |
| HEB_PBY_BIALIK | `dyn_gog_h` | `full-span` | 259364876 | `skipped_above_hit_threshold` |
| HEB_PBY_AHAD_HAAM | `dyn_yhwh_h` | `full-span` | 230979253 | `skipped_above_hit_threshold` |
| ENG_PG_SHAKESPEARE | `dyn_gog_e` | `full-span` | 217556768 | `skipped_above_hit_threshold` |
| HEB_PBY_BIALIK | `dyn_yeshua_h` | `full-span` | 206897417 | `skipped_above_hit_threshold` |
| HEB_PBY_BRENNER | `dyn_yeshua_h` | `full-span` | 188603935 | `skipped_above_hit_threshold` |
| EBIBLE_WLC | `dyn_beast_h` | `full-span` | 165249617 | `skipped_above_hit_threshold` |
| UHB | `dyn_beast_h` | `full-span` | 164784929 | `skipped_above_hit_threshold` |
| MAM | `dyn_beast_h` | `full-span` | 164260192 | `skipped_above_hit_threshold` |
| UXLC | `dyn_beast_h` | `full-span` | 163014892 | `skipped_above_hit_threshold` |
| MT_WLC | `dyn_beast_h` | `full-span` | 163013648 | `skipped_above_hit_threshold` |
| HEB_PBY_BRENNER | `dyn_dragon_h` | `full-span` | 145655795 | `skipped_above_hit_threshold` |
| HEB_PBY_BIALIK | `dyn_dragon_h` | `full-span` | 143129945 | `skipped_above_hit_threshold` |
| ENG_PG_SHAKESPEARE | `dyn_iran_e` | `full-span` | 113877707 | `skipped_above_hit_threshold` |
| KJV | `dyn_gog_e` | `full-span` | 112614748 | `skipped_above_hit_threshold` |
| HEB_PBY_BIALIK | `dyn_messiah_h` | `full-span` | 110129394 | `skipped_above_hit_threshold` |
| ENG_PG_WAR_PEACE | `dyn_gog_e` | `full-span` | 98950428 | `skipped_above_hit_threshold` |
| HEB_PBY_BRENNER | `dyn_messiah_h` | `full-span` | 90027862 | `skipped_above_hit_threshold` |
| LXX | `dyn_iran_g` | `full-span` | 81141888 | `skipped_above_hit_threshold` |
| KJV | `dyn_iran_e` | `full-span` | 64362163 | `skipped_above_hit_threshold` |
| HEB_PBY_AHAD_HAAM | `dyn_gog_h` | `full-span` | 52524066 | `skipped_above_hit_threshold` |
| HEB_PBY_BRENNER | `dyn_vance_h` | `full-span` | 52306899 | `skipped_above_hit_threshold` |
| HEB_PBY_BIALIK | `dyn_vance_h` | `full-span` | 51012008 | `skipped_above_hit_threshold` |
| ENG_PG_WAR_PEACE | `dyn_iran_e` | `full-span` | 50720110 | `skipped_above_hit_threshold` |
| HEB_PBY_AHAD_HAAM | `dyn_yeshua_h` | `full-span` | 46208240 | `skipped_above_hit_threshold` |
| MAM | `dyn_yhwh_h` | `full-span` | 43619325 | `skipped_above_hit_threshold` |
| UXLC | `dyn_yhwh_h` | `full-span` | 43283917 | `skipped_above_hit_threshold` |
| MT_WLC | `dyn_yhwh_h` | `full-span` | 43283141 | `skipped_above_hit_threshold` |
| UHB | `dyn_yhwh_h` | `full-span` | 42792278 | `skipped_above_hit_threshold` |
| EBIBLE_WLC | `dyn_yhwh_h` | `full-span` | 42745545 | `skipped_above_hit_threshold` |
| HEB_PBY_AHAD_HAAM | `dyn_dragon_h` | `full-span` | 33003976 | `skipped_above_hit_threshold` |
| HEB_PBY_AHAD_HAAM | `dyn_messiah_h` | `full-span` | 22587059 | `skipped_above_hit_threshold` |
| LXX | `dyn_gog_g` | `full-span` | 22427984 | `skipped_above_hit_threshold` |
| ENG_PG_MOBY_DICK | `dyn_gog_e` | `full-span` | 15815416 | `skipped_above_hit_threshold` |
| HEB_PBY_BIALIK | `dyn_magog_h` | `full-span` | 14781780 | `skipped_above_hit_threshold` |
| LXX | `dyn_vance_g` | `full-span` | 14641657 | `skipped_above_hit_threshold` |
| HEB_PBY_BRENNER | `dyn_magog_h` | `full-span` | 13906679 | `skipped_above_hit_threshold` |
| HEB_PBY_BIALIK | `dyn_iran_h` | `full-span` | 11349335 | `skipped_above_hit_threshold` |
| EBIBLE_WLC | `dyn_yeshua_h` | `full-span` | 11156131 | `skipped_above_hit_threshold` |
| UHB | `dyn_yeshua_h` | `full-span` | 11151829 | `skipped_above_hit_threshold` |
| HEB_PBY_AHAD_HAAM | `dyn_vance_h` | `full-span` | 10884247 | `skipped_above_hit_threshold` |
| MAM | `dyn_yeshua_h` | `full-span` | 10824700 | `skipped_above_hit_threshold` |
| UXLC | `dyn_yeshua_h` | `full-span` | 10724706 | `skipped_above_hit_threshold` |
| MT_WLC | `dyn_yeshua_h` | `full-span` | 10724464 | `skipped_above_hit_threshold` |
| HEB_PBY_BRENNER | `dyn_iran_h` | `full-span` | 10108513 | `skipped_above_hit_threshold` |
| GRC_PERSEUS_HERODOTUS | `dyn_iran_g` | `full-span` | 9046396 | `skipped_above_hit_threshold` |
| ENG_PG_MOBY_DICK | `dyn_iran_e` | `full-span` | 6458074 | `skipped_above_hit_threshold` |
| HEB_PBY_BRENNER | `dyn_russia_h` | `full-span` | 6304561 | `skipped_above_hit_threshold` |
| EBIBLE_WLC | `dyn_dragon_h` | `full-span` | 6204591 | `skipped_above_hit_threshold` |
| UHB | `dyn_dragon_h` | `full-span` | 6186847 | `skipped_above_hit_threshold` |
| MAM | `dyn_dragon_h` | `full-span` | 6135698 | `skipped_above_hit_threshold` |
| MT_WLC | `dyn_dragon_h` | `full-span` | 6066657 | `skipped_above_hit_threshold` |
| UXLC | `dyn_dragon_h` | `full-span` | 6062411 | `skipped_above_hit_threshold` |
| EBIBLE_WLC | `dyn_gog_h` | `full-span` | 5606606 | `skipped_above_hit_threshold` |
| MAM | `dyn_gog_h` | `full-span` | 5593814 | `skipped_above_hit_threshold` |
| HEB_PBY_BIALIK | `dyn_russia_h` | `full-span` | 5590218 | `skipped_above_hit_threshold` |
| UHB | `dyn_gog_h` | `full-span` | 5587606 | `skipped_above_hit_threshold` |
| UXLC | `dyn_gog_h` | `full-span` | 5536796 | `skipped_above_hit_threshold` |
| MT_WLC | `dyn_gog_h` | `full-span` | 5532568 | `skipped_above_hit_threshold` |
| EBIBLE_WLC | `dyn_messiah_h` | `full-span` | 5252863 | `skipped_above_hit_threshold` |
| UHB | `dyn_messiah_h` | `full-span` | 5240076 | `skipped_above_hit_threshold` |
| MAM | `dyn_messiah_h` | `full-span` | 5093697 | `skipped_above_hit_threshold` |
| MT_WLC | `dyn_messiah_h` | `full-span` | 5057448 | `skipped_above_hit_threshold` |
| UXLC | `dyn_messiah_h` | `full-span` | 5055913 | `skipped_above_hit_threshold` |
| BYZ_NT | `dyn_iran_g` | `full-span` | 4749326 | `skipped_above_hit_threshold` |
| TR_NT | `dyn_iran_g` | `full-span` | 4625438 | `skipped_above_hit_threshold` |
| SBLGNT | `dyn_iran_g` | `full-span` | 4615073 | `skipped_above_hit_threshold` |
| TCG_NT | `dyn_iran_g` | `full-span` | 4582262 | `skipped_above_hit_threshold` |
| GRC_PERSEUS_ILIAD | `dyn_iran_g` | `full-span` | 3579561 | `skipped_above_hit_threshold` |
| ENG_PG_SHAKESPEARE | `dyn_beast_e` | `full-span` | 3418141 | `skipped_above_hit_threshold` |
| GRC_PERSEUS_HERODOTUS | `dyn_gog_g` | `full-span` | 3079794 | `skipped_above_hit_threshold` |
| HEB_PBY_AHAD_HAAM | `dyn_magog_h` | `full-span` | 2911852 | `skipped_above_hit_threshold` |
| KJV | `dyn_beast_e` | `full-span` | 2427966 | `skipped_above_hit_threshold` |
| LXX | `dyn_russia_g` | `full-span` | 2218044 | `skipped_above_hit_threshold` |
| HEB_PBY_AHAD_HAAM | `dyn_iran_h` | `full-span` | 2117348 | `skipped_above_hit_threshold` |
| TR_NT | `dyn_gog_g` | `full-span` | 2016958 | `skipped_above_hit_threshold` |
| TCG_NT | `dyn_gog_g` | `full-span` | 2000884 | `skipped_above_hit_threshold` |
| GRC_PERSEUS_ODYSSEY | `dyn_iran_g` | `full-span` | 1997138 | `skipped_above_hit_threshold` |
| BYZ_NT | `dyn_gog_g` | `full-span` | 1990638 | `skipped_above_hit_threshold` |
| SBLGNT | `dyn_gog_g` | `full-span` | 1935106 | `skipped_above_hit_threshold` |
| ENG_PG_WAR_PEACE | `dyn_beast_e` | `full-span` | 1264733 | `skipped_above_hit_threshold` |
| HEB_PBY_AHAD_HAAM | `dyn_russia_h` | `full-span` | 1260045 | `skipped_above_hit_threshold` |
| GRC_PERSEUS_HERODOTUS | `dyn_vance_g` | `full-span` | 1235733 | `skipped_above_hit_threshold` |
| MAM | `dyn_vance_h` | `full-span` | 1224569 | `skipped_above_hit_threshold` |
| MT_WLC | `dyn_vance_h` | `full-span` | 1191206 | `skipped_above_hit_threshold` |
| UXLC | `dyn_vance_h` | `full-span` | 1189894 | `skipped_above_hit_threshold` |
| EBIBLE_WLC | `dyn_vance_h` | `full-span` | 1173157 | `skipped_above_hit_threshold` |
| UHB | `dyn_vance_h` | `full-span` | 1170235 | `skipped_above_hit_threshold` |
| HEB_PBY_BRENNER | `dyn_netanyahu_h` | `full-span` | 920932 | `skipped_above_hit_threshold` |
| GRC_PERSEUS_ILIAD | `dyn_gog_g` | `full-span` | 895700 | `skipped_above_hit_threshold` |
| HEB_PBY_BIALIK | `dyn_netanyahu_h` | `full-span` | 763870 | `skipped_above_hit_threshold` |
| MAM | `dyn_iran_h` | `full-span` | 696330 | `skipped_above_hit_threshold` |
| UXLC | `dyn_iran_h` | `full-span` | 692152 | `skipped_above_hit_threshold` |
| MT_WLC | `dyn_iran_h` | `full-span` | 691579 | `skipped_above_hit_threshold` |
| UHB | `dyn_iran_h` | `full-span` | 668069 | `skipped_above_hit_threshold` |
| EBIBLE_WLC | `dyn_iran_h` | `full-span` | 667552 | `skipped_above_hit_threshold` |
| BYZ_NT | `dyn_vance_g` | `full-span` | 573495 | `skipped_above_hit_threshold` |
| TR_NT | `dyn_vance_g` | `full-span` | 568362 | `skipped_above_hit_threshold` |
| ENG_PG_SHAKESPEARE | `dyn_vance_e` | `full-span` | 560612 | `skipped_above_hit_threshold` |
| SBLGNT | `dyn_vance_g` | `full-span` | 557336 | `skipped_above_hit_threshold` |
| TCG_NT | `dyn_vance_g` | `full-span` | 551791 | `skipped_above_hit_threshold` |
| HEB_PBY_BIALIK | `dyn_trump_h` | `full-span` | 526134 | `skipped_above_hit_threshold` |
| GRC_PERSEUS_ODYSSEY | `dyn_gog_g` | `full-span` | 501302 | `skipped_above_hit_threshold` |
| LXX | `dyn_trump_g` | `full-span` | 487148 | `skipped_above_hit_threshold` |
| HEB_PBY_BRENNER | `dyn_trump_h` | `full-span` | 461367 | `skipped_above_hit_threshold` |
| ENG_PG_SHAKESPEARE | `dyn_trump_e` | `full-span` | 335790 | `skipped_above_hit_threshold` |
| GRC_PERSEUS_ILIAD | `dyn_vance_g` | `full-span` | 325999 | `skipped_above_hit_threshold` |
| MAM | `dyn_magog_h` | `full-span` | 322697 | `skipped_above_hit_threshold` |
| UXLC | `dyn_magog_h` | `full-span` | 320231 | `skipped_above_hit_threshold` |
| MT_WLC | `dyn_magog_h` | `full-span` | 320111 | `skipped_above_hit_threshold` |
| EBIBLE_WLC | `dyn_magog_h` | `full-span` | 307083 | `skipped_above_hit_threshold` |
| UHB | `dyn_magog_h` | `full-span` | 306006 | `skipped_above_hit_threshold` |
| ENG_PG_WAR_PEACE | `dyn_vance_e` | `full-span` | 299257 | `skipped_above_hit_threshold` |
| KJV | `dyn_vance_e` | `full-span` | 294941 | `skipped_above_hit_threshold` |
| ENG_PG_MOBY_DICK | `dyn_beast_e` | `full-span` | 253351 | `skipped_above_hit_threshold` |
| ENG_PG_SHAKESPEARE | `dyn_magog_e` | `full-span` | 248036 | `skipped_above_hit_threshold` |
| LXX | `dyn_jesus_g` | `full-span` | 243700 | `skipped_above_hit_threshold` |
| HEB_PBY_AHAD_HAAM | `dyn_netanyahu_h` | `full-span` | 195658 | `skipped_above_hit_threshold` |
| GRC_PERSEUS_ODYSSEY | `dyn_vance_g` | `full-span` | 185209 | `skipped_above_hit_threshold` |
| GRC_PERSEUS_HERODOTUS | `dyn_russia_g` | `full-span` | 184242 | `skipped_above_hit_threshold` |
| ENG_PG_SHAKESPEARE | `dyn_russia_e` | `full-span` | 151995 | `skipped_above_hit_threshold` |
| EBIBLE_WLC | `dyn_russia_h` | `full-span` | 142783 | `skipped_above_hit_threshold` |
| UHB | `dyn_russia_h` | `full-span` | 142713 | `skipped_above_hit_threshold` |
| MAM | `dyn_russia_h` | `full-span` | 142463 | `skipped_above_hit_threshold` |
| MT_WLC | `dyn_russia_h` | `full-span` | 137828 | `skipped_above_hit_threshold` |
| UXLC | `dyn_russia_h` | `full-span` | 137739 | `skipped_above_hit_threshold` |
| KJV | `dyn_magog_e` | `full-span` | 118259 | `skipped_above_hit_threshold` |
| KJV | `dyn_trump_e` | `full-span` | 111371 | `skipped_above_hit_threshold` |
| ENG_PG_SHAKESPEARE | `dyn_christ_e` | `full-span` | 111185 | `skipped_above_hit_threshold` |
| TR_NT | `dyn_russia_g` | `full-span` | 103855 | `skipped_above_hit_threshold` |
| TCG_NT | `dyn_russia_g` | `full-span` | 103404 | `skipped_above_hit_threshold` |
| BYZ_NT | `dyn_russia_g` | `full-span` | 102577 | `skipped_above_hit_threshold` |
| SBLGNT | `dyn_russia_g` | `full-span` | 99245 | `skipped_above_hit_threshold` |
| ENG_PG_WAR_PEACE | `dyn_magog_e` | `full-span` | 99239 | `skipped_above_hit_threshold` |
| ENG_PG_WAR_PEACE | `dyn_trump_e` | `full-span` | 93018 | `skipped_above_hit_threshold` |
| HEB_PBY_AHAD_HAAM | `dyn_trump_h` | `full-span` | 92451 | `skipped_above_hit_threshold` |
| ENG_PG_SHAKESPEARE | `dyn_jesus_e` | `full-span` | 87353 | `skipped_above_hit_threshold` |
| KJV | `dyn_jesus_e` | `full-span` | 79657 | `skipped_above_hit_threshold` |
| GRC_PERSEUS_HERODOTUS | `dyn_trump_g` | `full-span` | 68470 | `skipped_above_hit_threshold` |
| GRC_PERSEUS_ILIAD | `dyn_russia_g` | `full-span` | 67477 | `skipped_above_hit_threshold` |
| ENG_PG_SHAKESPEARE | `dyn_dragon_e` | `full-span` | 60588 | `skipped_above_hit_threshold` |
| KJV | `dyn_christ_e` | `full-span` | 56561 | `skipped_above_hit_threshold` |
| BYZ_NT | `dyn_netanyahu_g` | `full-span` | 0 | `skipped_zero_hits` |
| ENG_PG_MOBY_DICK | `dyn_simsberry_e` | `full-span` | 0 | `skipped_zero_hits` |
| ENG_PG_MOBY_DICK | `dyn_simscorner_e` | `full-span` | 0 | `skipped_zero_hits` |
| ENG_PG_WAR_PEACE | `dyn_simsberry_e` | `full-span` | 0 | `skipped_zero_hits` |
| GRC_PERSEUS_HERODOTUS | `dyn_netanyahu_g` | `full-span` | 0 | `skipped_zero_hits` |
| GRC_PERSEUS_ILIAD | `dyn_netanyahu_g` | `full-span` | 0 | `skipped_zero_hits` |
| GRC_PERSEUS_ODYSSEY | `dyn_netanyahu_g` | `full-span` | 0 | `skipped_zero_hits` |
| KJV | `dyn_simscorner_e` | `full-span` | 0 | `skipped_zero_hits` |
| SBLGNT | `dyn_netanyahu_g` | `full-span` | 0 | `skipped_zero_hits` |
