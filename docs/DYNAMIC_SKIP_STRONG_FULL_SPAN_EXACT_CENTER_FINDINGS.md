# Strong Full-Span Exact-Center Findings

This targeted follow-up scans archived dense hit payloads for the
full-span rows whose Bible max normalized rate exceeded all observed
language-matched controls. It is not a new search; it summarizes hit-level
metadata from already-completed partition exports.

This report summarizes completed dense full-span partition outputs.
It is additive to the manageable-row export: a dense row becomes
complete when all planned partition outputs exist and summarize.

## Reproduce

```bash
python3 -m scripts.summarize_dynamic_span_partition_outputs --plan reports/dynamic_skip_focus/strong_bible_over_control_full_span_plan.csv --cache-only --examples-per-partition 5
```

## Scope

- planned partitions: 42
- completed partition outputs summarized: 42
- completed dense rows: 8
- partial dense rows: 0
- exported partition hit rows summarized: 36,280,786
- exact center-word hits in completed partitions: 1,582
- partition summary CSV: `reports/dynamic_skip_focus/strong_bible_over_control_full_span_partition_summary.csv`
- term summary CSV: `reports/dynamic_skip_focus/strong_bible_over_control_full_span_term_summary.csv`
- examples CSV: `reports/dynamic_skip_focus/strong_bible_over_control_full_span_examples.csv`

## Completed Dense Rows

| Corpus | Term | Hits | Exact center-word hits |
| --- | --- | ---: | ---: |
| EBIBLE_WLC | `משיח` (Mashiach; English: Messiah)<br>`dyn_messiah_h` | 5,252,863 | 75 |
| KJV | `Jesus`<br>`dyn_jesus_e` | 79,657 | 492 |
| LXX | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | 243,700 | 70 |
| LXX | `ρωσια` (rosia; English: Russia)<br>`dyn_russia_g` | 2,218,044 | 0 |
| LXX | `βανς` (bans; English: Vance)<br>`dyn_vance_g` | 14,641,657 | 0 |
| TCG_NT | `γωγ` (Gog; English: Gog)<br>`dyn_gog_g` | 2,000,884 | 4 |
| UHB | `ישוע` (Yeshua; English: Yeshua)<br>`dyn_yeshua_h` | 11,151,829 | 941 |
| UXLC | `איראן` (yrn; English: Iran)<br>`dyn_iran_h` | 692,152 | 0 |

## Partial Dense Rows

| Corpus | Term | Completed partitions | Hits so far | Skip ranges |
| --- | --- | ---: | ---: | --- |

## Completed Partitions

| Partition | Exported hits | Estimated hits | Delta | Exact center-word hits |
| --- | ---: | ---: | ---: | ---: |
| `EBIBLE_WLC__dyn_messiah_h__full_span__p00001_of_00006__skip_2_66503` | 1,564,744 | 875,478 | 689,266 | 21 |
| `EBIBLE_WLC__dyn_messiah_h__full_span__p00002_of_00006__skip_66504_133005` | 1,303,189 | 875,478 | 427,711 | 15 |
| `EBIBLE_WLC__dyn_messiah_h__full_span__p00003_of_00006__skip_133006_199507` | 1,034,192 | 875,478 | 158,714 | 18 |
| `EBIBLE_WLC__dyn_messiah_h__full_span__p00004_of_00006__skip_199508_266009` | 751,644 | 875,478 | -123,834 | 17 |
| `EBIBLE_WLC__dyn_messiah_h__full_span__p00005_of_00006__skip_266010_332511` | 450,918 | 875,478 | -424,560 | 4 |
| `EBIBLE_WLC__dyn_messiah_h__full_span__p00006_of_00006__skip_332512_399013` | 148,176 | 875,478 | -727,302 | 0 |
| `KJV__dyn_jesus_e__full_span__p00001_of_00001__skip_2_805806` | 79,657 | 79,657 | 0 | 492 |
| `LXX__dyn_jesus_g__full_span__p00001_of_00001__skip_2_558371` | 243,700 | 243,700 | 0 | 70 |
| `LXX__dyn_russia_g__full_span__p00001_of_00003__skip_2_232655` | 1,225,960 | 739,347 | 486,613 | 0 |
| `LXX__dyn_russia_g__full_span__p00002_of_00003__skip_232656_465309` | 738,565 | 739,347 | -782 | 0 |
| `LXX__dyn_russia_g__full_span__p00003_of_00003__skip_465310_697964` | 253,519 | 739,351 | -485,832 | 0 |
| `LXX__dyn_vance_g__full_span__p00001_of_00015__skip_2_62042` | 1,898,645 | 976,108 | 922,537 | 0 |
| `LXX__dyn_vance_g__full_span__p00002_of_00015__skip_62043_124083` | 1,764,503 | 976,108 | 788,395 | 0 |
| `LXX__dyn_vance_g__full_span__p00003_of_00015__skip_124084_186124` | 1,672,095 | 976,108 | 695,987 | 0 |
| `LXX__dyn_vance_g__full_span__p00004_of_00015__skip_186125_248165` | 1,554,250 | 976,108 | 578,142 | 0 |
| `LXX__dyn_vance_g__full_span__p00005_of_00015__skip_248166_310207` | 1,410,054 | 976,124 | 433,930 | 0 |
| `LXX__dyn_vance_g__full_span__p00006_of_00015__skip_310208_372248` | 1,240,444 | 976,108 | 264,336 | 0 |
| `LXX__dyn_vance_g__full_span__p00007_of_00015__skip_372249_434289` | 1,081,767 | 976,108 | 105,659 | 0 |
| `LXX__dyn_vance_g__full_span__p00008_of_00015__skip_434290_496330` | 959,344 | 976,108 | -16,764 | 0 |
| `LXX__dyn_vance_g__full_span__p00009_of_00015__skip_496331_558371` | 836,804 | 976,108 | -139,304 | 0 |
| `LXX__dyn_vance_g__full_span__p00010_of_00015__skip_558372_620413` | 694,048 | 976,124 | -282,076 | 0 |
| `LXX__dyn_vance_g__full_span__p00011_of_00015__skip_620414_682454` | 540,900 | 976,108 | -435,208 | 0 |
| `LXX__dyn_vance_g__full_span__p00012_of_00015__skip_682455_744495` | 420,105 | 976,108 | -556,003 | 0 |
| `LXX__dyn_vance_g__full_span__p00013_of_00015__skip_744496_806536` | 303,235 | 976,108 | -672,873 | 0 |
| `LXX__dyn_vance_g__full_span__p00014_of_00015__skip_806537_868577` | 195,144 | 976,108 | -780,964 | 0 |
| `LXX__dyn_vance_g__full_span__p00015_of_00015__skip_868578_930619` | 70,319 | 976,124 | -905,805 | 0 |
| `TCG_NT__dyn_gog_g__full_span__p00001_of_00003__skip_2_114652` | 1,111,342 | 666,958 | 444,384 | 4 |
| `TCG_NT__dyn_gog_g__full_span__p00002_of_00003__skip_114653_229304` | 668,964 | 666,964 | 2,000 | 0 |
| `TCG_NT__dyn_gog_g__full_span__p00003_of_00003__skip_229305_343956` | 220,578 | 666,964 | -446,386 | 0 |
| `UHB__dyn_yeshua_h__full_span__p00001_of_00012__skip_2_33212` | 1,732,253 | 929,301 | 802,952 | 88 |
| `UHB__dyn_yeshua_h__full_span__p00002_of_00012__skip_33213_66424` | 1,608,955 | 929,329 | 679,626 | 101 |
| `UHB__dyn_yeshua_h__full_span__p00003_of_00012__skip_66425_99636` | 1,486,108 | 929,329 | 556,779 | 118 |
| `UHB__dyn_yeshua_h__full_span__p00004_of_00012__skip_99637_132847` | 1,340,267 | 929,301 | 410,966 | 93 |
| `UHB__dyn_yeshua_h__full_span__p00005_of_00012__skip_132848_166059` | 1,183,128 | 929,329 | 253,799 | 97 |
| `UHB__dyn_yeshua_h__full_span__p00006_of_00012__skip_166060_199271` | 1,026,828 | 929,329 | 97,499 | 84 |
| `UHB__dyn_yeshua_h__full_span__p00007_of_00012__skip_199272_232482` | 864,568 | 929,301 | -64,733 | 89 |
| `UHB__dyn_yeshua_h__full_span__p00008_of_00012__skip_232483_265694` | 706,333 | 929,329 | -222,996 | 86 |
| `UHB__dyn_yeshua_h__full_span__p00009_of_00012__skip_265695_298906` | 539,433 | 929,329 | -389,896 | 92 |
| `UHB__dyn_yeshua_h__full_span__p00010_of_00012__skip_298907_332117` | 366,722 | 929,301 | -562,579 | 81 |
| `UHB__dyn_yeshua_h__full_span__p00011_of_00012__skip_332118_365329` | 221,271 | 929,329 | -708,058 | 12 |
| `UHB__dyn_yeshua_h__full_span__p00012_of_00012__skip_365330_398541` | 75,963 | 929,329 | -853,366 | 0 |
| `UXLC__dyn_iran_h__full_span__p00001_of_00001__skip_2_299260` | 692,152 | 692,152 | 0 | 0 |

## Example Hits

| Type | Corpus | Term | Skip | Center | Center word |
| --- | --- | --- | ---: | --- | --- |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -64168 | LAM 4:20 | `מְשִׁ֣יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -21294 | 2SA 23:1 | `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -10396 | LAM 4:20 | `מְשִׁ֣יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -8885 | 2SA 23:1 | `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -1356 | LAM 4:20 | `מְשִׁ֣יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -127736 | 2SA 23:1 | `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -112064 | 2SA 23:1 | `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -107024 | 2SA 1:21 | `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -88647 | LAM 4:20 | `מְשִׁ֣יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -83549 | 2SA 23:1 | `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -192856 | 2SA 23:1 | `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -191946 | 2SA 23:1 | `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -188689 | 2SA 1:21 | `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -185417 | 2SA 23:1 | `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -174401 | 2SA 1:21 | `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -261062 | 2SA 1:21 | `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -257625 | 2SA 1:21 | `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -244516 | 2SA 1:21 | `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -227309 | 2SA 23:1 | `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -221294 | 2SA 1:21 | `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | -290705 | 2SA 1:21 | `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | 270253 | 2SA 1:21 | `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | 281875 | 2SA 23:1 | `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one)<br>`dyn_messiah_h` | 310656 | 2SA 23:1 | `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) |
| `exact_center_word` | KJV | `Jesus`<br>`dyn_jesus_e` | -342678 | MAT 4:7 | Jesus |
| `exact_center_word` | KJV | `Jesus`<br>`dyn_jesus_e` | -333151 | MAT 8:34 | Jesus: |
| `exact_center_word` | KJV | `Jesus`<br>`dyn_jesus_e` | -317646 | MAT 9:10 | Jesus |
| `exact_center_word` | KJV | `Jesus`<br>`dyn_jesus_e` | -317136 | MAT 9:4 | Jesus |
| `exact_center_word` | KJV | `Jesus`<br>`dyn_jesus_e` | -316997 | MAT 3:15 | Jesus |
| `exact_center_word` | LXX | `ιησους` (Iesous; English: Jesus/Joshua)<br>`dyn_jesus_g` | -292090 | NEH 9:4 | `Ἰησοῦς` (Iesous; English: Jesus/Joshua) |

## Read

- Completed partition rows are no longer deferred; their hit-level metadata exists.
- Exact center-word hits are flags, not the admission rule.
- `not_computed` means the manifest-only path was used; hit counts still come from export manifests.
- Partition estimates are planning estimates; exported hit rows are observed counts.
- The ignored partition CSVs are reproducible from the tracked plan and runner.
