# Strong Full-Span Exact-Center Review Queue

This report condenses exact-center ELS paths into surface-word review units.
One review unit is one corpus, term, center ref/source, and center word index.

## Reproduce

```bash
python3 -m scripts.build_dynamic_span_exact_center_review_queue --input reports/dynamic_skip_focus/strong_full_span_exact_center_rows.csv --out reports/dynamic_skip_focus/strong_full_span_exact_center_review_queue.csv --markdown-out docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_REVIEW_QUEUE.md
```

## Scope

- input exact rows: `reports/dynamic_skip_focus/strong_full_span_exact_center_rows.csv`
- exact-center paths read: 9,794
- word-level review units: 537
- Bible review units: 453
- control review units: 84
- queue CSV: `reports/dynamic_skip_focus/strong_full_span_exact_center_review_queue.csv`

## Top Bible Review Units

| Rank | Corpus | Term | Center | Word index | Surface word | Paths | Skip range | Example path |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: | --- |
| 1 | UHB | `dyn_yeshua_h` | NEH 8:17 | 11 | יֵשׁ֨וּעַ | 85 | 391..322791 | NEH 9:6 -> NEH 8:17 -> NEH 8:9 (backward -391) |
| 2 | UHB | `dyn_yeshua_h` | EZR 2:2 | 3 | יֵשׁ֡וּעַ | 83 | 3498..342979 | 2CH 34:22 -> EZR 2:2 -> EZR 5:5 (forward 3498) |
| 3 | UHB | `dyn_yeshua_h` | EZR 3:9 | 2 | יֵשׁ֡וּעַ | 73 | 1278..336179 | EZR 2:36 -> EZR 3:9 -> EZR 4:21 (forward 1278) |
| 4 | UHB | `dyn_yeshua_h` | EZR 2:6 | 4 | יֵשׁ֖וּעַ | 73 | 1475..340457 | 2CH 36:7 -> EZR 2:6 -> EZR 3:3 (forward 1475) |
| 5 | UHB | `dyn_yeshua_h` | NEH 9:5 | 3 | יֵשׁ֣וּעַ | 70 | 384..318890 | NEH 9:12 -> NEH 9:5 -> NEH 8:15 (backward -384) |
| 6 | UHB | `dyn_yeshua_h` | NEH 12:8 | 2 | יֵשׁ֧וּעַ | 69 | 2788..317618 | NEH 9:27 -> NEH 12:8 -> EST 1:3 (forward 2788) |
| 7 | UHB | `dyn_yeshua_h` | EZR 10:18 | 9 | יֵשׁ֤וּעַ | 68 | 11909..330774 | NEH 11:6 -> EZR 10:18 -> 2CH 35:9 (backward -11909) |
| 8 | UHB | `dyn_yeshua_h` | NEH 7:11 | 4 | יֵשׁ֖וּעַ | 67 | 2825..320907 | NEH 4:7 -> NEH 7:11 -> NEH 9:10 (forward 2825) |
| 9 | UHB | `dyn_yeshua_h` | NEH 9:4 | 4 | יֵשׁ֨וּעַ | 66 | 7519..314871 | NEH 2:8 -> NEH 9:4 -> EST 1:20 (forward 7519) |
| 10 | UHB | `dyn_yeshua_h` | EZR 2:36 | 5 | יֵשׁ֔וּעַ | 63 | 4294..333411 | 2CH 34:18 -> EZR 2:36 -> EZR 6:15 (forward 4294) |
| 11 | UHB | `dyn_yeshua_h` | NEH 12:7 | 10 | יֵשֽׁוּעַ׃ | 59 | 10023..314758 | EST 9:20 -> NEH 12:7 -> NEH 3:19 (backward -10023) |
| 12 | UHB | `dyn_yeshua_h` | NEH 7:39 | 5 | יֵשׁ֔וּעַ | 56 | 122..321474 | NEH 7:45 -> NEH 7:39 -> NEH 7:32 (backward -122) |
| 13 | UHB | `dyn_yeshua_h` | NEH 7:7 | 3 | יֵשׁ֡וּעַ | 55 | 11329..324643 | EZR 6:6 -> NEH 7:7 -> EST 2:23 (forward 11329) |
| 14 | UHB | `dyn_yeshua_h` | EZR 3:2 | 2 | יֵשׁ֨וּעַ | 54 | 10793..336435 | NEH 3:20 -> EZR 3:2 -> 2CH 30:3 (backward -10793) |
| 15 | EBIBLE_WLC | `dyn_messiah_h` | 2SA 1:21 | 16 | מָשִׁ֥יחַ | 33 | 791..290705 | 2SA 2:15 -> 2SA 1:21 -> 1SA 31:12 (backward -791) |
| 16 | EBIBLE_WLC | `dyn_messiah_h` | 2SA 23:1 | 12 | מְשִׁ֨יחַ֙ | 30 | 8885..310656 | 1KI 5:22 -> 2SA 23:1 -> 2SA 16:4 (backward -8885) |
| 17 | EBIBLE_WLC | `dyn_messiah_h` | LAM 4:20 | 3 | מְשִׁ֣יחַ | 11 | 1356..93592 | EZK 1:24 -> LAM 4:20 -> LAM 3:16 (backward -1356) |
| 18 | TCG_NT | `dyn_gog_g` | REV 20:8 | 14 | Γὼγ | 4 | 17..4568 | REV 20:8 -> REV 20:8 -> REV 20:8 (backward -17) |
| 19 | KJV | `dyn_jesus_e` | MRK 10:5 | 2 | Jesus | 4 | 80380..261470 | JHN 8:20 -> MRK 10:5 -> ZEC 1:21 (backward -80380) |
| 20 | KJV | `dyn_jesus_e` | MAT 4:10 | 3 | Jesus | 4 | 126093..301051 | EZK 28:13 -> MAT 4:10 -> LUK 24:18 (forward 126093) |
| 21 | KJV | `dyn_jesus_e` | MAT 3:13 | 3 | Jesus | 3 | 8937..334349 | ZEC 12:9 -> MAT 3:13 -> MAT 9:20 (forward 8937) |
| 22 | KJV | `dyn_jesus_e` | ACT 18:28 | 15 | Jesus | 3 | 12081..126059 | ACT 25:20 -> ACT 18:28 -> ACT 12:11 (backward -12081) |
| 23 | KJV | `dyn_jesus_e` | MAT 12:15 | 3 | Jesus | 3 | 12817..218422 | MAT 4:12 -> MAT 12:15 -> MAT 19:16 (forward 12817) |
| 24 | KJV | `dyn_jesus_e` | MAT 26:17 | 15 | Jesus, | 3 | 19575..216725 | MAT 15:1 -> MAT 26:17 -> MRK 8:12 (forward 19575) |
| 25 | KJV | `dyn_jesus_e` | JHN 12:21 | 21 | Jesus. | 3 | 21130..198964 | ACT 4:27 -> JHN 12:21 -> JHN 1:42 (backward -21130) |
| 26 | KJV | `dyn_jesus_e` | MAT 21:24 | 2 | Jesus | 3 | 25740..85717 | MRK 6:34 -> MAT 21:24 -> MAT 6:8 (backward -25740) |
| 27 | KJV | `dyn_jesus_e` | MAT 18:1 | 9 | Jesus, | 3 | 29694..237352 | MRK 5:37 -> MAT 18:1 -> MAL 1:11 (backward -29694) |
| 28 | KJV | `dyn_jesus_e` | JHN 21:20 | 9 | Jesus | 3 | 47391..186079 | ACT 27:3 -> JHN 21:20 -> LUK 20:20 (backward -47391) |
| 29 | LXX | `dyn_jesus_g` | JOS 22:7 | 15 | Ἰησοῦς | 3 | 54232..239038 | 1SA 14:26 -> JOS 22:7 -> DEU 10:2 (backward -54232) |
| 30 | KJV | `dyn_jesus_e` | MAT 20:22 | 2 | Jesus | 3 | 63495..330487 | LUK 7:33 -> MAT 20:22 -> MIC 2:9 (backward -63495) |
| 31 | KJV | `dyn_jesus_e` | LUK 9:42 | 17 | Jesus | 3 | 65612..186127 | JHN 19:38 -> LUK 9:42 -> MAT 22:16 (backward -65612) |
| 32 | KJV | `dyn_jesus_e` | MAT 2:1 | 3 | Jesus | 3 | 68041..253377 | MRK 11:33 -> MAT 2:1 -> DAN 9:22 (backward -68041) |
| 33 | KJV | `dyn_jesus_e` | MAT 20:25 | 2 | Jesus | 3 | 71252..333616 | AMO 7:12 -> MAT 20:25 -> LUK 10:29 (forward 71252) |
| 34 | KJV | `dyn_jesus_e` | MAT 8:34 | 10 | Jesus: | 3 | 73543..333151 | LUK 2:51 -> MAT 8:34 -> DAN 11:36 (backward -73543) |
| 35 | KJV | `dyn_jesus_e` | MRK 5:27 | 6 | Jesus, | 3 | 78484..138864 | JHN 3:10 -> MRK 5:27 -> HAB 3:10 (backward -78484) |
| 36 | LXX | `dyn_jesus_g` | JOS 8:3 | 16 | Ἰησοῦς | 3 | 85420..229460 | NUM 9:18 -> JOS 8:3 -> 1SA 23:14 (forward 85420) |
| 37 | LXX | `dyn_jesus_g` | JOS 18:3 | 3 | Ἰησοῦς | 3 | 86975..221129 | NUM 17:23 -> JOS 18:3 -> 2SA 3:21 (forward 86975) |
| 38 | KJV | `dyn_jesus_e` | LUK 17:17 | 2 | Jesus | 3 | 193659..249630 | PHM 1:1 -> LUK 17:17 -> DAN 4:13 (backward -193659) |
| 39 | KJV | `dyn_jesus_e` | MRK 10:23 | 2 | Jesus | 3 | 236088..298323 | LAM 2:10 -> MRK 10:23 -> 1TI 5:21 (forward 236088) |
| 40 | KJV | `dyn_jesus_e` | JHN 20:26 | 16 | Jesus, | 2 | 275..114782 | JHN 20:21 -> JHN 20:26 -> JHN 21:1 (forward 275) |

## Top Control Review Units

| Rank | Corpus | Term | Center | Word index | Surface word | Paths | Skip range | Example path |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: | --- |
| 454 | HEB_PBY_BIALIK | `dyn_yeshua_h` | PBY Bialik | 541334 | ישוע | 247 | 5560..1475773 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 5560) |
| 455 | HEB_PBY_BIALIK | `dyn_yeshua_h` | PBY Bialik | 865644 | "ישוע | 184 | 981..1435946 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 981) |
| 456 | HEB_PBY_BIALIK | `dyn_yeshua_h` | PBY Bialik | 871945 | ישוע | 153 | 3129..1424579 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -3129) |
| 457 | HEB_PBY_BIALIK | `dyn_yeshua_h` | PBY Bialik | 353843 | ישוע | 151 | 842..978689 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 842) |
| 458 | HEB_PBY_BIALIK | `dyn_yeshua_h` | PBY Bialik | 324778 | ישוע | 149 | 4025..896203 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -4025) |
| 459 | HEB_PBY_BIALIK | `dyn_yeshua_h` | PBY Bialik | 353850 | (ישוע | 142 | 15234..978004 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -15234) |
| 460 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 743033 | משיח | 137 | 1781..1754232 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 1781) |
| 461 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 779652 | משיח, | 136 | 25360..1690129 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 25360) |
| 462 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 793960 | משיח | 131 | 288..1598511 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 288) |
| 463 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 826039 | משיח | 131 | 288..1556342 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 288) |
| 464 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 515876 | משיח | 128 | 11634..1411826 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -11634) |
| 465 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 443837 | משיח | 127 | 1071..1221663 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -1071) |
| 466 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 580119 | משיח. | 127 | 14413..1579094 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 14413) |
| 467 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 515884 | משיח. | 125 | 212..1379623 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 212) |
| 468 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 443388 | משיח? | 125 | 5622..1184066 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -5622) |
| 469 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 530016 | משיח, | 122 | 15372..1440490 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 15372) |
| 470 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 566756 | משיח, | 120 | 4706..1537132 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -4706) |
| 471 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 483529 | משיח? | 120 | 8525..1307063 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 8525) |
| 472 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 443887 | משיח | 117 | 1204..1207318 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -1204) |
| 473 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 500714 | משיח | 117 | 2719..1352977 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 2719) |
| 474 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 441513 | משיח | 116 | 3497..1189003 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 3497) |
| 475 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 483498 | משיח | 116 | 6413..1313612 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -6413) |
| 476 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 510906 | משיח | 116 | 15319..1401915 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -15319) |
| 477 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 442532 | משיח | 115 | 230..1218901 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -230) |
| 478 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 443975 | משיח | 115 | 11709..1178018 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -11709) |
| 479 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 568119 | משיח | 114 | 1678..1546013 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -1678) |
| 480 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 483546 | משיח. | 114 | 22843..1315406 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -22843) |
| 481 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 500991 | משיח | 113 | 686..1376868 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 686) |
| 482 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 483518 | משיח, | 113 | 4073..1327582 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -4073) |
| 483 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 501465 | משיח | 112 | 3638..1378083 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 3638) |
| 484 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 444482 | משיח | 110 | 43080..1219615 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -43080) |
| 485 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 444411 | משיח | 109 | 2274..1224892 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 2274) |
| 486 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 443827 | משיח, | 108 | 2015..1223859 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 2015) |
| 487 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 444674 | משיח | 107 | 4945..1224964 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -4945) |
| 488 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 444705 | משיח | 107 | 15613..1202215 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -15613) |
| 489 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 922594 | משיח | 107 | 74186..1285668 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 74186) |
| 490 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 468543 | משיח3430 | 106 | 3050..1267849 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 3050) |
| 491 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 467815 | משיח | 106 | 29591..1273167 | PBY Bialik -> PBY Bialik -> PBY Bialik (backward -29591) |
| 492 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 444250 | משיח, | 105 | 17439..1223827 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 17439) |
| 493 | HEB_PBY_BIALIK | `dyn_messiah_h` | PBY Bialik | 444605 | משיח | 104 | 2709..1220148 | PBY Bialik -> PBY Bialik -> PBY Bialik (forward 2709) |

## Corpus Summary

| Corpus | Class | Review units | Exact-center paths |
| --- | --- | ---: | ---: |
| EBIBLE_WLC | bible | 4 | 75 |
| KJV | bible | 377 | 492 |
| LXX | bible | 57 | 70 |
| TCG_NT | bible | 1 | 4 |
| UHB | bible | 14 | 941 |
| ENG_PG_SHAKESPEARE | control | 1 | 2 |
| HEB_PBY_BIALIK | control | 83 | 8,210 |

## Read

- This is a review queue, not a claim promotion rule.
- High path count means many hidden paths center on the same surface word.
- Bible rows should still be read against language-matched controls and ordinary surface frequency.
- Non-Bible controls often use source-level refs; inspect `center_source`, `center_word_index`, and offsets in the CSV.
