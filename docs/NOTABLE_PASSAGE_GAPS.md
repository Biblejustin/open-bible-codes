# Notable Passage Gaps

This report records declared passages where selected ELS terms are absent, sparse, or present when centered inside the passage.
It is intentionally a screening ledger: absence inside a short passage is often expected, so the useful rows are the terms that are absent in the passage while recurring elsewhere in the same corpus, or present at notably lower density than a uniform placement expectation.

## Run Settings

- Passages: `configs/notable_passage_gap_passages.csv`
- Terms: `terms/notable_passage_gap_terms.csv`
- Skip range: `2..500`
- Direction: `both`
- Jobs: `0`
- Minimum normalized term length: `3`
- Common-elsewhere threshold: `10` centered hits outside the passage

## Highest Gap Passage Rows

These rows rank declared passages by how many eligible terms are absent inside the passage while recurring at least the threshold count elsewhere in the same corpus. Short passages naturally rank high, so use this as a triage list rather than a formal significance test.

| Passage | Corpus | Letters | Present | Absent Common Elsewhere | Low Vs Uniform | Observed Hits | Uniform Expected Hits |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | 150 | 36 | 16 | 1 | 603 | 596.441 |
| Numbers 6 Priestly Blessing | MAM | 150 | 36 | 16 | 1 | 581 | 596.253 |
| Numbers 6 Priestly Blessing | MT_WLC | 150 | 36 | 16 | 1 | 603 | 596.452 |
| Numbers 6 Priestly Blessing | UHB | 150 | 36 | 16 | 1 | 603 | 596.304 |
| Numbers 6 Priestly Blessing | UXLC | 150 | 36 | 16 | 1 | 603 | 596.458 |
| Psalm 110 Priest King | EBIBLE_WLC | 241 | 39 | 13 | 1 | 757 | 958.282 |
| Psalm 110 Priest King | MT_WLC | 241 | 39 | 13 | 1 | 757 | 958.299 |
| Psalm 110 Priest King | UHB | 241 | 39 | 13 | 1 | 757 | 958.062 |
| Psalm 110 Priest King | UXLC | 241 | 39 | 13 | 1 | 757 | 958.309 |
| Psalm 110 Priest King | MAM | 241 | 39 | 13 | 0 | 832 | 957.979 |
| Deuteronomy 6 Shema | EBIBLE_WLC | 205 | 40 | 12 | 3 | 1041 | 815.136 |
| Deuteronomy 6 Shema | MAM | 205 | 40 | 12 | 3 | 1037 | 814.878 |
| Deuteronomy 6 Shema | MT_WLC | 205 | 40 | 12 | 3 | 1041 | 815.151 |
| Deuteronomy 6 Shema | UHB | 205 | 40 | 12 | 3 | 1041 | 814.949 |
| Deuteronomy 6 Shema | UXLC | 205 | 40 | 12 | 3 | 1041 | 815.159 |
| Isaiah 7 Immanuel | EBIBLE_WLC | 345 | 41 | 11 | 2 | 1464 | 1371.814 |
| Isaiah 7 Immanuel | MAM | 345 | 41 | 11 | 2 | 1466 | 1371.381 |
| Isaiah 7 Immanuel | MT_WLC | 345 | 41 | 11 | 2 | 1464 | 1371.839 |
| Isaiah 7 Immanuel | UHB | 345 | 41 | 11 | 2 | 1464 | 1371.500 |
| Isaiah 7 Immanuel | UXLC | 345 | 41 | 11 | 2 | 1464 | 1371.853 |
| Isaiah 9 Child King | MAM | 385 | 41 | 11 | 1 | 1464 | 1530.382 |
| Psalm 2 Messianic King | EBIBLE_WLC | 371 | 42 | 10 | 1 | 1377 | 1475.197 |
| Daniel 9 Seventy Weeks | MAM | 610 | 42 | 10 | 0 | 2663 | 2424.760 |
| Daniel 9 Seventy Weeks | EBIBLE_WLC | 601 | 43 | 9 | 1 | 2698 | 2389.740 |
| Daniel 9 Seventy Weeks | MT_WLC | 601 | 43 | 9 | 1 | 2698 | 2389.784 |
| Daniel 9 Seventy Weeks | UHB | 601 | 43 | 9 | 1 | 2698 | 2389.192 |
| Daniel 9 Seventy Weeks | UXLC | 601 | 43 | 9 | 1 | 2698 | 2389.807 |
| Isaiah 53 Servant Song | MAM | 800 | 44 | 8 | 1 | 2961 | 3180.014 |
| Exodus 20 Decalogue | MAM | 1147 | 44 | 8 | 1 | 4304 | 4559.344 |
| Psalm 2 Messianic King | UHB | 371 | 44 | 8 | 0 | 1417 | 1474.859 |

## Declared Gap-Target Passages

These rows isolate passages explicitly registered as gap targets, instead of letting short high-profile passages dominate the global ranking.

| Passage | Corpus | Letters | Present | Absent Common Elsewhere | Low Vs Uniform | Observed Hits | Uniform Expected Hits |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Leviticus 24 Blasphemy Law | MT_WLC | 1037 | 45 | 7 | 1 | 3836 | 4123.471 |
| Leviticus 24 Blasphemy Law | UXLC | 1037 | 45 | 7 | 1 | 3836 | 4123.511 |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | 1037 | 45 | 7 | 1 | 3836 | 4123.395 |
| Leviticus 24 Blasphemy Law | MAM | 1037 | 45 | 7 | 1 | 3814 | 4122.093 |
| Leviticus 24 Blasphemy Law | UHB | 1037 | 45 | 7 | 1 | 3836 | 4122.449 |
| Leviticus 24 Blasphemy Law LXX | LXX | 2074 | 6 | 3 | 0 | 55 | 42.402 |
| Leviticus 24 Blasphemy Law KJVA | KJVA | 2230 | 6 | 1 | 0 | 211 | 260.823 |

## Declared Gap-Target Detail

| Passage | Corpus | Term | Gap Class | Hits Elsewhere | Hits In Passage | Uniform Expected | Uniform Zero P | Uniform Zero Q | Sample Center Refs |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Leviticus 24 Blasphemy Law | UXLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11262 | 0 | 9.756 | 0.000058 | 0.000513 |  |
| Leviticus 24 Blasphemy Law | MT_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11258 | 0 | 9.753 | 0.000058 | 0.000513 |  |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11256 | 0 | 9.751 | 0.000058 | 0.000513 |  |
| Leviticus 24 Blasphemy Law | MAM | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11254 | 0 | 9.709 | 0.000061 | 0.000530 |  |
| Leviticus 24 Blasphemy Law | UHB | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11202 | 0 | 9.716 | 0.000060 | 0.000526 |  |
| Leviticus 24 Blasphemy Law | MAM | `פסח` (Pesach; English: Passover) | absent_in_passage_common_elsewhere | 3163 | 0 | 2.729 | 0.065293 | 0.276038 |  |
| Leviticus 24 Blasphemy Law | UHB | `פסח` (Pesach; English: Passover) | absent_in_passage_common_elsewhere | 3049 | 0 | 2.644 | 0.071042 | 0.291905 |  |
| Leviticus 24 Blasphemy Law | MT_WLC | `פסח` (Pesach; English: Passover) | absent_in_passage_common_elsewhere | 3049 | 0 | 2.641 | 0.071265 | 0.291905 |  |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | `פסח` (Pesach; English: Passover) | absent_in_passage_common_elsewhere | 3047 | 0 | 2.640 | 0.071388 | 0.291905 |  |
| Leviticus 24 Blasphemy Law | UXLC | `פסח` (Pesach; English: Passover) | absent_in_passage_common_elsewhere | 3045 | 0 | 2.638 | 0.071512 | 0.291905 |  |
| Leviticus 24 Blasphemy Law | UXLC | `מגוג` (Magog; English: Magog) | absent_in_passage_common_elsewhere | 914 | 0 | 0.792 | 0.453029 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | `מגוג` (Magog; English: Magog) | absent_in_passage_common_elsewhere | 912 | 0 | 0.790 | 0.453814 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | MT_WLC | `מגוג` (Magog; English: Magog) | absent_in_passage_common_elsewhere | 912 | 0 | 0.790 | 0.453814 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | MAM | `מגוג` (Magog; English: Magog) | absent_in_passage_common_elsewhere | 909 | 0 | 0.784 | 0.456468 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | UHB | `מגוג` (Magog; English: Magog) | absent_in_passage_common_elsewhere | 877 | 0 | 0.761 | 0.467363 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | UHB | `חבורה` (chabburah; English: Wound) | absent_in_passage_common_elsewhere | 768 | 0 | 0.666 | 0.513703 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | MAM | `חבורה` (chabburah; English: Wound) | absent_in_passage_common_elsewhere | 763 | 0 | 0.658 | 0.517743 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | `חבורה` (chabburah; English: Wound) | absent_in_passage_common_elsewhere | 761 | 0 | 0.659 | 0.517236 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | MT_WLC | `חבורה` (chabburah; English: Wound) | absent_in_passage_common_elsewhere | 757 | 0 | 0.656 | 0.519032 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | UXLC | `חבורה` (chabburah; English: Wound) | absent_in_passage_common_elsewhere | 756 | 0 | 0.655 | 0.519482 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | MAM | `משפט` (mshpt; English: Judgment) | absent_in_passage_common_elsewhere | 445 | 0 | 0.384 | 0.681184 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | UHB | `משפט` (mshpt; English: Judgment) | absent_in_passage_common_elsewhere | 430 | 0 | 0.373 | 0.688698 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | `משפט` (mshpt; English: Judgment) | absent_in_passage_common_elsewhere | 408 | 0 | 0.353 | 0.702260 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | UXLC | `משפט` (mshpt; English: Judgment) | absent_in_passage_common_elsewhere | 407 | 0 | 0.353 | 0.702869 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | MT_WLC | `משפט` (mshpt; English: Judgment) | absent_in_passage_common_elsewhere | 406 | 0 | 0.352 | 0.703478 | 0.997247 |  |
| Leviticus 24 Blasphemy Law LXX | LXX | `κρισισ` (krisis; English: Judgment) | absent_in_passage_common_elsewhere | 289 | 0 | 0.215 | 0.806791 | 0.997247 |  |
| Leviticus 24 Blasphemy Law KJVA | KJVA | `magog` | absent_in_passage_common_elsewhere | 170 | 0 | 0.099 | 0.905438 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | UHB | `יומיהוה` (yom YHWH; English: Day Of YHWH) | absent_in_passage_common_elsewhere | 119 | 0 | 0.103 | 0.901936 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | MAM | `יומיהוה` (yom YHWH; English: Day Of YHWH) | absent_in_passage_common_elsewhere | 111 | 0 | 0.096 | 0.908678 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | `יומיהוה` (yom YHWH; English: Day Of YHWH) | absent_in_passage_common_elsewhere | 109 | 0 | 0.094 | 0.909894 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | MT_WLC | `יומיהוה` (yom YHWH; English: Day Of YHWH) | absent_in_passage_common_elsewhere | 106 | 0 | 0.092 | 0.912262 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | UXLC | `יומיהוה` (yom YHWH; English: Day Of YHWH) | absent_in_passage_common_elsewhere | 106 | 0 | 0.092 | 0.912262 | 0.997247 |  |
| Leviticus 24 Blasphemy Law LXX | LXX | `μαγωγ` (magog; English: Magog) | absent_in_passage_common_elsewhere | 60 | 0 | 0.045 | 0.956406 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | UHB | `ירושלימ` (yrwshlym; English: Jerusalem) | absent_in_passage_common_elsewhere | 29 | 0 | 0.025 | 0.975161 | 0.997247 |  |
| Leviticus 24 Blasphemy Law LXX | LXX | `λυχνια` (luchnia; English: Lampstand) | absent_in_passage_common_elsewhere | 27 | 0 | 0.020 | 0.980142 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | MAM | `ירושלימ` (yrwshlym; English: Jerusalem) | absent_in_passage_common_elsewhere | 25 | 0 | 0.022 | 0.978662 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | `ירושלימ` (yrwshlym; English: Jerusalem) | absent_in_passage_common_elsewhere | 22 | 0 | 0.019 | 0.981122 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | MT_WLC | `ירושלימ` (yrwshlym; English: Jerusalem) | absent_in_passage_common_elsewhere | 22 | 0 | 0.019 | 0.981122 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | UXLC | `ירושלימ` (yrwshlym; English: Jerusalem) | absent_in_passage_common_elsewhere | 22 | 0 | 0.019 | 0.981122 | 0.997247 |  |
| Leviticus 24 Blasphemy Law | MAM | `כסא` (kisse; English: Throne) | low_in_passage_vs_uniform | 23834 | 4 | 20.566 | 0.000000 | 0.000000 | Lev 24:14 |

## Passage Summary

| Passage | Corpus | Letters | Eligible Terms | Present | Absent Elsewhere | Absent Common Elsewhere | Low Vs Uniform | Observed Hits | Uniform Expected Hits |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Genesis 1 Creation | MT_WLC | 1671 | 54 | 46 | 7 | 6 | 2 | 5348 | 6644.474 |
| Genesis 22 Binding Of Isaac | MT_WLC | 1155 | 54 | 45 | 8 | 7 | 4 | 5707 | 4592.679 |
| Exodus 12 Passover | MT_WLC | 2836 | 54 | 47 | 6 | 5 | 0 | 11531 | 11276.917 |
| Exodus 20 Decalogue | MT_WLC | 1143 | 54 | 46 | 7 | 6 | 1 | 4300 | 4544.963 |
| Leviticus 16 Day Of Atonement | MT_WLC | 2062 | 54 | 49 | 4 | 3 | 2 | 8541 | 8199.225 |
| Leviticus 23 Festivals | MT_WLC | 2393 | 54 | 48 | 5 | 4 | 1 | 9844 | 9515.396 |
| Leviticus 24 Blasphemy Law | MT_WLC | 1037 | 54 | 45 | 8 | 7 | 1 | 3836 | 4123.471 |
| Numbers 6 Priestly Blessing | MT_WLC | 150 | 54 | 36 | 17 | 16 | 1 | 603 | 596.452 |
| Deuteronomy 6 Shema | MT_WLC | 205 | 54 | 40 | 13 | 12 | 3 | 1041 | 815.151 |
| 2 Samuel 7 Davidic Covenant | MT_WLC | 1758 | 54 | 46 | 7 | 6 | 5 | 6672 | 6990.416 |
| Psalm 2 Messianic King | MT_WLC | 371 | 54 | 47 | 6 | 5 | 0 | 1374 | 1475.224 |
| Psalm 22 Suffering Psalm | MT_WLC | 985 | 54 | 46 | 7 | 6 | 0 | 3419 | 3916.701 |
| Psalm 110 Priest King | MT_WLC | 241 | 54 | 39 | 14 | 13 | 1 | 757 | 958.299 |
| Isaiah 7 Immanuel | MT_WLC | 345 | 54 | 41 | 12 | 11 | 2 | 1464 | 1371.839 |
| Isaiah 9 Child King | MT_WLC | 378 | 54 | 45 | 8 | 7 | 1 | 1382 | 1503.059 |
| Isaiah 53 Servant Song | MT_WLC | 800 | 54 | 46 | 7 | 6 | 1 | 2970 | 3181.077 |
| Daniel 7 Son Of Man | MT_WLC | 2022 | 54 | 49 | 4 | 3 | 0 | 7987 | 8040.171 |
| Daniel 9 Seventy Weeks | MT_WLC | 601 | 54 | 43 | 10 | 9 | 1 | 2698 | 2389.784 |
| Ezekiel 38 Gog | MT_WLC | 1464 | 54 | 46 | 7 | 6 | 0 | 5735 | 5821.370 |
| Ezekiel 39 Gog | MT_WLC | 1681 | 54 | 49 | 4 | 4 | 0 | 6607 | 6684.237 |
| Joel 2 Spirit And Day Of YHWH | MT_WLC | 1547 | 54 | 48 | 5 | 4 | 0 | 6080 | 6151.407 |
| Zechariah 12 Pierced One | MT_WLC | 923 | 54 | 46 | 7 | 6 | 1 | 3460 | 3670.167 |
| Zechariah 14 Day Of YHWH | MT_WLC | 1417 | 54 | 49 | 4 | 3 | 0 | 5254 | 5634.482 |
| Malachi 3 Messenger | MT_WLC | 1103 | 54 | 48 | 5 | 4 | 0 | 4381 | 4385.909 |
| Genesis 1 Creation | UXLC | 1671 | 54 | 46 | 7 | 6 | 2 | 5348 | 6644.538 |
| Genesis 22 Binding Of Isaac | UXLC | 1155 | 54 | 45 | 8 | 7 | 4 | 5707 | 4592.724 |
| Exodus 12 Passover | UXLC | 2836 | 54 | 47 | 6 | 5 | 0 | 11531 | 11277.026 |
| Exodus 20 Decalogue | UXLC | 1143 | 54 | 46 | 7 | 6 | 1 | 4300 | 4545.007 |
| Leviticus 16 Day Of Atonement | UXLC | 2062 | 54 | 49 | 4 | 3 | 2 | 8541 | 8199.304 |
| Leviticus 23 Festivals | UXLC | 2393 | 54 | 48 | 5 | 4 | 1 | 9844 | 9515.488 |
| Leviticus 24 Blasphemy Law | UXLC | 1037 | 54 | 45 | 8 | 7 | 1 | 3836 | 4123.511 |
| Numbers 6 Priestly Blessing | UXLC | 150 | 54 | 36 | 17 | 16 | 1 | 603 | 596.458 |
| Deuteronomy 6 Shema | UXLC | 205 | 54 | 40 | 13 | 12 | 3 | 1041 | 815.159 |
| 2 Samuel 7 Davidic Covenant | UXLC | 1758 | 54 | 46 | 7 | 6 | 5 | 6672 | 6990.484 |
| Psalm 2 Messianic King | UXLC | 371 | 54 | 47 | 6 | 5 | 0 | 1374 | 1475.239 |
| Psalm 22 Suffering Psalm | UXLC | 985 | 54 | 46 | 7 | 6 | 0 | 3419 | 3916.739 |
| Psalm 110 Priest King | UXLC | 241 | 54 | 39 | 14 | 13 | 1 | 757 | 958.309 |
| Isaiah 7 Immanuel | UXLC | 345 | 54 | 41 | 12 | 11 | 2 | 1464 | 1371.853 |
| Isaiah 9 Child King | UXLC | 378 | 54 | 45 | 8 | 7 | 1 | 1382 | 1503.073 |
| Isaiah 53 Servant Song | UXLC | 800 | 54 | 46 | 7 | 6 | 1 | 2970 | 3181.107 |
| Daniel 7 Son Of Man | UXLC | 2022 | 54 | 49 | 4 | 3 | 0 | 7987 | 8040.249 |
| Daniel 9 Seventy Weeks | UXLC | 601 | 54 | 43 | 10 | 9 | 1 | 2698 | 2389.807 |
| Ezekiel 38 Gog | UXLC | 1464 | 54 | 46 | 7 | 6 | 0 | 5735 | 5821.427 |
| Ezekiel 39 Gog | UXLC | 1681 | 54 | 49 | 4 | 4 | 0 | 6607 | 6684.302 |
| Joel 2 Spirit And Day Of YHWH | UXLC | 1547 | 54 | 48 | 5 | 4 | 0 | 6080 | 6151.467 |
| Zechariah 12 Pierced One | UXLC | 923 | 54 | 46 | 7 | 6 | 1 | 3460 | 3670.203 |
| Zechariah 14 Day Of YHWH | UXLC | 1417 | 54 | 49 | 4 | 3 | 0 | 5254 | 5634.537 |
| Malachi 3 Messenger | UXLC | 1103 | 54 | 48 | 5 | 4 | 0 | 4381 | 4385.952 |
| Genesis 1 Creation | EBIBLE_WLC | 1671 | 54 | 46 | 7 | 6 | 2 | 5348 | 6644.352 |
| Genesis 22 Binding Of Isaac | EBIBLE_WLC | 1155 | 54 | 45 | 8 | 7 | 4 | 5707 | 4592.596 |
| Exodus 12 Passover | EBIBLE_WLC | 2836 | 54 | 47 | 6 | 5 | 0 | 11531 | 11276.711 |
| Exodus 20 Decalogue | EBIBLE_WLC | 1143 | 54 | 46 | 7 | 6 | 1 | 4300 | 4544.880 |
| Leviticus 16 Day Of Atonement | EBIBLE_WLC | 2062 | 54 | 49 | 4 | 3 | 2 | 8541 | 8199.075 |
| Leviticus 23 Festivals | EBIBLE_WLC | 2393 | 54 | 48 | 5 | 4 | 1 | 9844 | 9515.222 |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | 1037 | 54 | 45 | 8 | 7 | 1 | 3836 | 4123.395 |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | 150 | 54 | 36 | 17 | 16 | 1 | 603 | 596.441 |
| Deuteronomy 6 Shema | EBIBLE_WLC | 205 | 54 | 40 | 13 | 12 | 3 | 1041 | 815.136 |
| 2 Samuel 7 Davidic Covenant | EBIBLE_WLC | 1758 | 54 | 46 | 7 | 6 | 5 | 6672 | 6990.288 |
| Psalm 2 Messianic King | EBIBLE_WLC | 371 | 54 | 42 | 11 | 10 | 1 | 1377 | 1475.197 |
| Psalm 22 Suffering Psalm | EBIBLE_WLC | 985 | 54 | 46 | 7 | 6 | 0 | 3419 | 3916.629 |
| Psalm 110 Priest King | EBIBLE_WLC | 241 | 54 | 39 | 14 | 13 | 1 | 757 | 958.282 |
| Isaiah 7 Immanuel | EBIBLE_WLC | 345 | 54 | 41 | 12 | 11 | 2 | 1464 | 1371.814 |
| Isaiah 9 Child King | EBIBLE_WLC | 378 | 54 | 45 | 8 | 7 | 1 | 1382 | 1503.031 |
| Isaiah 53 Servant Song | EBIBLE_WLC | 800 | 54 | 46 | 7 | 6 | 1 | 2970 | 3181.019 |
| Daniel 7 Son Of Man | EBIBLE_WLC | 2022 | 54 | 49 | 4 | 3 | 0 | 7987 | 8040.024 |
| Daniel 9 Seventy Weeks | EBIBLE_WLC | 601 | 54 | 43 | 10 | 9 | 1 | 2698 | 2389.740 |
| Ezekiel 38 Gog | EBIBLE_WLC | 1464 | 54 | 46 | 7 | 6 | 0 | 5735 | 5821.264 |
| Ezekiel 39 Gog | EBIBLE_WLC | 1681 | 54 | 49 | 4 | 4 | 0 | 6607 | 6684.115 |
| Joel 2 Spirit And Day Of YHWH | EBIBLE_WLC | 1547 | 54 | 48 | 5 | 4 | 0 | 6080 | 6151.295 |
| Zechariah 12 Pierced One | EBIBLE_WLC | 923 | 54 | 46 | 7 | 6 | 1 | 3460 | 3670.100 |
| Zechariah 14 Day Of YHWH | EBIBLE_WLC | 1417 | 54 | 49 | 4 | 3 | 0 | 5254 | 5634.379 |
| Malachi 3 Messenger | EBIBLE_WLC | 1103 | 54 | 46 | 7 | 6 | 0 | 4251 | 4385.829 |
| Genesis 1 Creation | MAM | 1671 | 54 | 46 | 7 | 6 | 2 | 5348 | 6642.253 |
| Genesis 22 Binding Of Isaac | MAM | 1155 | 54 | 45 | 8 | 7 | 4 | 5707 | 4591.145 |
| Exodus 12 Passover | MAM | 2837 | 54 | 47 | 6 | 5 | 1 | 11543 | 11277.123 |
| Exodus 20 Decalogue | MAM | 1147 | 54 | 44 | 9 | 8 | 1 | 4304 | 4559.344 |
| Leviticus 16 Day Of Atonement | MAM | 2061 | 54 | 49 | 4 | 3 | 1 | 8530 | 8192.510 |
| Leviticus 23 Festivals | MAM | 2391 | 54 | 48 | 5 | 4 | 1 | 9739 | 9504.266 |
| Leviticus 24 Blasphemy Law | MAM | 1037 | 54 | 45 | 8 | 7 | 1 | 3814 | 4122.093 |
| Numbers 6 Priestly Blessing | MAM | 150 | 54 | 36 | 17 | 16 | 1 | 581 | 596.253 |
| Deuteronomy 6 Shema | MAM | 205 | 54 | 40 | 13 | 12 | 3 | 1037 | 814.878 |
| 2 Samuel 7 Davidic Covenant | MAM | 1760 | 54 | 47 | 6 | 5 | 1 | 6686 | 6996.030 |
| Psalm 2 Messianic King | MAM | 371 | 54 | 47 | 6 | 5 | 0 | 1374 | 1474.731 |
| Psalm 22 Suffering Psalm | MAM | 984 | 54 | 47 | 6 | 5 | 0 | 3397 | 3911.417 |
| Psalm 110 Priest King | MAM | 241 | 54 | 39 | 14 | 13 | 0 | 832 | 957.979 |
| Isaiah 7 Immanuel | MAM | 345 | 54 | 41 | 12 | 11 | 2 | 1466 | 1371.381 |
| Isaiah 9 Child King | MAM | 385 | 54 | 41 | 12 | 11 | 1 | 1464 | 1530.382 |
| Isaiah 53 Servant Song | MAM | 800 | 54 | 44 | 9 | 8 | 1 | 2961 | 3180.014 |
| Daniel 7 Son Of Man | MAM | 2104 | 54 | 48 | 5 | 4 | 0 | 8660 | 8363.436 |
| Daniel 9 Seventy Weeks | MAM | 610 | 54 | 42 | 11 | 10 | 0 | 2663 | 2424.760 |
| Ezekiel 38 Gog | MAM | 1466 | 54 | 47 | 6 | 5 | 0 | 5742 | 5827.375 |
| Ezekiel 39 Gog | MAM | 1685 | 54 | 48 | 5 | 4 | 0 | 6588 | 6697.904 |
| Joel 2 Spirit And Day Of YHWH | MAM | 1547 | 54 | 48 | 5 | 4 | 0 | 6111 | 6149.351 |
| Zechariah 12 Pierced One | MAM | 922 | 54 | 47 | 6 | 5 | 0 | 3369 | 3664.966 |
| Zechariah 14 Day Of YHWH | MAM | 1430 | 54 | 50 | 3 | 2 | 0 | 5285 | 5684.274 |
| Malachi 3 Messenger | MAM | 1102 | 54 | 47 | 6 | 5 | 0 | 4393 | 4380.469 |
| Genesis 1 Creation | UHB | 1671 | 54 | 46 | 7 | 6 | 2 | 5348 | 6642.828 |
| Genesis 22 Binding Of Isaac | UHB | 1155 | 54 | 45 | 8 | 7 | 4 | 5707 | 4591.542 |
| Exodus 12 Passover | UHB | 2836 | 54 | 47 | 6 | 5 | 0 | 11531 | 11274.124 |
| Exodus 20 Decalogue | UHB | 1143 | 54 | 46 | 7 | 6 | 1 | 4294 | 4543.838 |
| Leviticus 16 Day Of Atonement | UHB | 2063 | 54 | 48 | 5 | 4 | 1 | 8484 | 8201.170 |
| Leviticus 23 Festivals | UHB | 2393 | 54 | 48 | 5 | 4 | 1 | 9844 | 9513.039 |
| Leviticus 24 Blasphemy Law | UHB | 1037 | 54 | 45 | 8 | 7 | 1 | 3836 | 4122.449 |
| Numbers 6 Priestly Blessing | UHB | 150 | 54 | 36 | 17 | 16 | 1 | 603 | 596.304 |
| Deuteronomy 6 Shema | UHB | 205 | 54 | 40 | 13 | 12 | 3 | 1041 | 814.949 |
| 2 Samuel 7 Davidic Covenant | UHB | 1758 | 54 | 46 | 7 | 6 | 5 | 6672 | 6988.685 |
| Psalm 2 Messianic King | UHB | 371 | 54 | 44 | 9 | 8 | 0 | 1417 | 1474.859 |
| Psalm 22 Suffering Psalm | UHB | 988 | 54 | 44 | 9 | 8 | 0 | 3392 | 3927.657 |
| Psalm 110 Priest King | UHB | 241 | 54 | 39 | 14 | 13 | 1 | 757 | 958.062 |
| Isaiah 7 Immanuel | UHB | 345 | 54 | 41 | 12 | 11 | 2 | 1464 | 1371.500 |
| Isaiah 9 Child King | UHB | 437 | 54 | 46 | 7 | 6 | 1 | 1581 | 1737.233 |
| Isaiah 53 Servant Song | UHB | 800 | 54 | 45 | 8 | 7 | 1 | 2973 | 3180.289 |
| Daniel 7 Son Of Man | UHB | 2022 | 54 | 49 | 4 | 3 | 0 | 7987 | 8038.180 |
| Daniel 9 Seventy Weeks | UHB | 601 | 54 | 43 | 10 | 9 | 1 | 2698 | 2389.192 |
| Ezekiel 38 Gog | UHB | 1464 | 54 | 46 | 7 | 6 | 0 | 5734 | 5819.928 |
| Ezekiel 39 Gog | UHB | 1681 | 54 | 49 | 4 | 4 | 0 | 6618 | 6682.582 |
| Joel 2 Spirit And Day Of YHWH | UHB | 1827 | 54 | 49 | 4 | 3 | 0 | 7138 | 7262.985 |
| Zechariah 12 Pierced One | UHB | 923 | 54 | 46 | 7 | 6 | 1 | 3460 | 3669.258 |
| Zechariah 14 Day Of YHWH | UHB | 1417 | 54 | 49 | 4 | 3 | 0 | 5254 | 5633.087 |
| Malachi 3 Messenger | UHB | 1103 | 54 | 46 | 7 | 6 | 0 | 4251 | 4384.823 |
| Leviticus 24 Blasphemy Law LXX | LXX | 2074 | 11 | 6 | 3 | 3 | 0 | 55 | 42.402 |
| Leviticus 24 Blasphemy Law KJVA | KJVA | 2230 | 11 | 6 | 2 | 1 | 0 | 211 | 260.823 |

## Notable Absence / Low-Density Rows

Rows are sorted by gap class first, then by how frequently the term appears centered elsewhere in the same corpus.

| Passage | Corpus | Term | Gap Class | Hits Elsewhere | Hits In Passage | Uniform Expected | Uniform Zero P | Uniform Zero Q | Sample Center Refs |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Deuteronomy 6 Shema | MAM | `רגמ` (ragam; English: Stone Verb) | absent_in_passage_common_elsewhere | 47982 | 0 | 8.183 | 0.000279 | 0.002318 |  |
| Numbers 6 Priestly Blessing | MAM | `רגמ` (ragam; English: Stone Verb) | absent_in_passage_common_elsewhere | 47982 | 0 | 5.988 | 0.002509 | 0.017865 |  |
| Deuteronomy 6 Shema | UXLC | `רגמ` (ragam; English: Stone Verb) | absent_in_passage_common_elsewhere | 47586 | 0 | 8.149 | 0.000289 | 0.002335 |  |
| Numbers 6 Priestly Blessing | UXLC | `רגמ` (ragam; English: Stone Verb) | absent_in_passage_common_elsewhere | 47586 | 0 | 5.963 | 0.002572 | 0.017882 |  |
| Deuteronomy 6 Shema | MT_WLC | `רגמ` (ragam; English: Stone Verb) | absent_in_passage_common_elsewhere | 47582 | 0 | 8.149 | 0.000289 | 0.002335 |  |
| Numbers 6 Priestly Blessing | MT_WLC | `רגמ` (ragam; English: Stone Verb) | absent_in_passage_common_elsewhere | 47582 | 0 | 5.962 | 0.002574 | 0.017882 |  |
| Deuteronomy 6 Shema | EBIBLE_WLC | `רגמ` (ragam; English: Stone Verb) | absent_in_passage_common_elsewhere | 47540 | 0 | 8.141 | 0.000291 | 0.002335 |  |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | `רגמ` (ragam; English: Stone Verb) | absent_in_passage_common_elsewhere | 47540 | 0 | 5.957 | 0.002587 | 0.017882 |  |
| Deuteronomy 6 Shema | UHB | `רגמ` (ragam; English: Stone Verb) | absent_in_passage_common_elsewhere | 47483 | 0 | 8.141 | 0.000291 | 0.002335 |  |
| Numbers 6 Priestly Blessing | UHB | `רגמ` (ragam; English: Stone Verb) | absent_in_passage_common_elsewhere | 47483 | 0 | 5.957 | 0.002587 | 0.017882 |  |
| Numbers 6 Priestly Blessing | UXLC | `נקב` (nqb; English: Pierce Name) | absent_in_passage_common_elsewhere | 41114 | 0 | 5.152 | 0.005788 | 0.037234 |  |
| Numbers 6 Priestly Blessing | MT_WLC | `נקב` (nqb; English: Pierce Name) | absent_in_passage_common_elsewhere | 41091 | 0 | 5.149 | 0.005805 | 0.037234 |  |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | `נקב` (nqb; English: Pierce Name) | absent_in_passage_common_elsewhere | 41082 | 0 | 5.148 | 0.005811 | 0.037234 |  |
| Numbers 6 Priestly Blessing | UHB | `נקב` (nqb; English: Pierce Name) | absent_in_passage_common_elsewhere | 41023 | 0 | 5.147 | 0.005819 | 0.037234 |  |
| Numbers 6 Priestly Blessing | MAM | `נקב` (nqb; English: Pierce Name) | absent_in_passage_common_elsewhere | 40988 | 0 | 5.115 | 0.006005 | 0.038166 |  |
| Numbers 6 Priestly Blessing | MAM | `ישוע` (Yeshua; English: Yeshua) | absent_in_passage_common_elsewhere | 27440 | 0 | 3.424 | 0.032570 | 0.160645 |  |
| Numbers 6 Priestly Blessing | UHB | `ישוע` (Yeshua; English: Yeshua) | absent_in_passage_common_elsewhere | 27200 | 0 | 3.412 | 0.032961 | 0.161731 |  |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | `ישוע` (Yeshua; English: Yeshua) | absent_in_passage_common_elsewhere | 27048 | 0 | 3.389 | 0.033730 | 0.163280 |  |
| Numbers 6 Priestly Blessing | UXLC | `ישוע` (Yeshua; English: Yeshua) | absent_in_passage_common_elsewhere | 27036 | 0 | 3.388 | 0.033781 | 0.163280 |  |
| Numbers 6 Priestly Blessing | MT_WLC | `ישוע` (Yeshua; English: Yeshua) | absent_in_passage_common_elsewhere | 27033 | 0 | 3.387 | 0.033794 | 0.163280 |  |
| Numbers 6 Priestly Blessing | MAM | `דקר` (dqr; English: Pierced) | absent_in_passage_common_elsewhere | 24883 | 0 | 3.105 | 0.044813 | 0.214055 |  |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | `דקר` (dqr; English: Pierced) | absent_in_passage_common_elsewhere | 24728 | 0 | 3.099 | 0.045111 | 0.214055 |  |
| Numbers 6 Priestly Blessing | MT_WLC | `דקר` (dqr; English: Pierced) | absent_in_passage_common_elsewhere | 24708 | 0 | 3.096 | 0.045224 | 0.214055 |  |
| Numbers 6 Priestly Blessing | UXLC | `דקר` (dqr; English: Pierced) | absent_in_passage_common_elsewhere | 24706 | 0 | 3.096 | 0.045235 | 0.214055 |  |
| Numbers 6 Priestly Blessing | UHB | `דקר` (dqr; English: Pierced) | absent_in_passage_common_elsewhere | 24642 | 0 | 3.092 | 0.045433 | 0.214055 |  |
| Genesis 1 Creation | MAM | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23838 | 0 | 33.140 | 0.000000 | 0.000000 |  |
| Daniel 9 Seventy Weeks | MAM | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23838 | 0 | 12.098 | 0.000006 | 0.000063 |  |
| Psalm 110 Priest King | MAM | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23838 | 0 | 4.780 | 0.008399 | 0.049717 |  |
| Deuteronomy 6 Shema | MAM | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23838 | 0 | 4.066 | 0.017152 | 0.088759 |  |
| Numbers 6 Priestly Blessing | MAM | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23838 | 0 | 2.975 | 0.051055 | 0.235509 |  |
| Genesis 1 Creation | MT_WLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23465 | 0 | 32.756 | 0.000000 | 0.000000 |  |
| Daniel 9 Seventy Weeks | MT_WLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23465 | 0 | 11.781 | 0.000008 | 0.000081 |  |
| Psalm 110 Priest King | MT_WLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23465 | 0 | 4.724 | 0.008878 | 0.051684 |  |
| Deuteronomy 6 Shema | MT_WLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23465 | 0 | 4.019 | 0.017980 | 0.091701 |  |
| Numbers 6 Priestly Blessing | MT_WLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23465 | 0 | 2.940 | 0.052846 | 0.235509 |  |
| Genesis 1 Creation | EBIBLE_WLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23462 | 0 | 32.752 | 0.000000 | 0.000000 |  |
| Daniel 9 Seventy Weeks | EBIBLE_WLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23462 | 0 | 11.780 | 0.000008 | 0.000081 |  |
| Psalm 110 Priest King | EBIBLE_WLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23462 | 0 | 4.724 | 0.008883 | 0.051684 |  |
| Deuteronomy 6 Shema | EBIBLE_WLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23462 | 0 | 4.018 | 0.017989 | 0.091701 |  |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23462 | 0 | 2.940 | 0.052866 | 0.235509 |  |
| Genesis 1 Creation | UXLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23455 | 0 | 32.742 | 0.000000 | 0.000000 |  |
| Daniel 9 Seventy Weeks | UXLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23455 | 0 | 11.776 | 0.000008 | 0.000081 |  |
| Psalm 110 Priest King | UXLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23455 | 0 | 4.722 | 0.008896 | 0.051684 |  |
| Deuteronomy 6 Shema | UXLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23455 | 0 | 4.017 | 0.018011 | 0.091701 |  |
| Numbers 6 Priestly Blessing | UXLC | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23455 | 0 | 2.939 | 0.052912 | 0.235509 |  |
| Genesis 1 Creation | UHB | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23368 | 0 | 32.659 | 0.000000 | 0.000000 |  |
| Daniel 9 Seventy Weeks | UHB | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23368 | 0 | 11.746 | 0.000008 | 0.000081 |  |
| Psalm 110 Priest King | UHB | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23368 | 0 | 4.710 | 0.009003 | 0.051987 |  |
| Deuteronomy 6 Shema | UHB | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23368 | 0 | 4.007 | 0.018194 | 0.092138 |  |
| Numbers 6 Priestly Blessing | UHB | `כסא` (kisse; English: Throne) | absent_in_passage_common_elsewhere | 23368 | 0 | 2.932 | 0.053307 | 0.235509 |  |
| Psalm 2 Messianic King | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah) | absent_in_passage_common_elsewhere | 12904 | 0 | 3.999 | 0.018328 | 0.092322 |  |
| Isaiah 7 Immanuel | MAM | `משיח` (Mashiach; English: Messiah) | absent_in_passage_common_elsewhere | 12903 | 0 | 3.704 | 0.024637 | 0.123446 |  |
| Genesis 22 Binding Of Isaac | UXLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11262 | 0 | 10.866 | 0.000019 | 0.000185 |  |
| Exodus 20 Decalogue | UXLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11262 | 0 | 10.754 | 0.000021 | 0.000195 |  |
| Leviticus 24 Blasphemy Law | UXLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11262 | 0 | 9.756 | 0.000058 | 0.000513 |  |
| Deuteronomy 6 Shema | UXLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11262 | 0 | 1.929 | 0.145340 | 0.553326 |  |
| Genesis 22 Binding Of Isaac | MT_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11258 | 0 | 10.863 | 0.000019 | 0.000185 |  |
| Exodus 20 Decalogue | MT_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11258 | 0 | 10.750 | 0.000021 | 0.000195 |  |
| Leviticus 24 Blasphemy Law | MT_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11258 | 0 | 9.753 | 0.000058 | 0.000513 |  |
| Deuteronomy 6 Shema | MT_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11258 | 0 | 1.928 | 0.145440 | 0.553326 |  |
| Genesis 22 Binding Of Isaac | EBIBLE_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11256 | 0 | 10.861 | 0.000019 | 0.000185 |  |
| Exodus 20 Decalogue | EBIBLE_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11256 | 0 | 10.748 | 0.000021 | 0.000195 |  |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11256 | 0 | 9.751 | 0.000058 | 0.000513 |  |
| Psalm 2 Messianic King | EBIBLE_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11256 | 0 | 3.489 | 0.030544 | 0.152238 |  |
| Deuteronomy 6 Shema | EBIBLE_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11256 | 0 | 1.928 | 0.145489 | 0.553326 |  |
| Genesis 22 Binding Of Isaac | MAM | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11254 | 0 | 10.814 | 0.000020 | 0.000191 |  |
| Leviticus 24 Blasphemy Law | MAM | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11254 | 0 | 9.709 | 0.000061 | 0.000530 |  |
| Daniel 9 Seventy Weeks | MAM | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11254 | 0 | 5.711 | 0.003308 | 0.021907 |  |
| Psalm 110 Priest King | MAM | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11254 | 0 | 2.256 | 0.104720 | 0.425622 |  |
| Deuteronomy 6 Shema | MAM | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11254 | 0 | 1.919 | 0.146695 | 0.553467 |  |
| Genesis 22 Binding Of Isaac | UHB | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11202 | 0 | 10.821 | 0.000020 | 0.000191 |  |
| Exodus 20 Decalogue | UHB | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11202 | 0 | 10.709 | 0.000022 | 0.000200 |  |
| Leviticus 24 Blasphemy Law | UHB | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11202 | 0 | 9.716 | 0.000060 | 0.000526 |  |
| Psalm 2 Messianic King | UHB | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11202 | 0 | 3.476 | 0.030932 | 0.153364 |  |
| Deuteronomy 6 Shema | UHB | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 11202 | 0 | 1.921 | 0.146507 | 0.553467 |  |
| Numbers 6 Priestly Blessing | UXLC | `ציונ` (Tziyon; English: Zion) | absent_in_passage_common_elsewhere | 8731 | 0 | 1.094 | 0.334851 | 0.980431 |  |
| Numbers 6 Priestly Blessing | MT_WLC | `ציונ` (Tziyon; English: Zion) | absent_in_passage_common_elsewhere | 8724 | 0 | 1.093 | 0.335144 | 0.980431 |  |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | `ציונ` (Tziyon; English: Zion) | absent_in_passage_common_elsewhere | 8717 | 0 | 1.092 | 0.335438 | 0.980431 |  |
| Numbers 6 Priestly Blessing | UHB | `ציונ` (Tziyon; English: Zion) | absent_in_passage_common_elsewhere | 8630 | 0 | 1.083 | 0.338680 | 0.981038 |  |
| Numbers 6 Priestly Blessing | MAM | `ציונ` (Tziyon; English: Zion) | absent_in_passage_common_elsewhere | 8549 | 0 | 1.067 | 0.344084 | 0.981038 |  |

## Output Files

- Detail CSV: `reports/notable_passage_gaps/term_gap_detail.csv`
- Passage summary CSV: `reports/notable_passage_gaps/passage_summary.csv`
- Manifest: `reports/notable_passage_gaps/manifest.json`

## Cautions

- This report does not treat absence as a negative proof. It records silence and lower-density rows so they can be reviewed alongside positive centered hits.
- `expected_in_passage_uniform` is a descriptive baseline only; it is not a formal p-value.
- `uniform_zero_probability` is the simple Poisson `exp(-expected)` probability of zero hits under that uniform baseline; it is a triage aid, not a formal independence test.
- `uniform_zero_bh_q` applies Benjamini-Hochberg correction to that simple zero-hit triage probability over absent/low-density detail rows.
- Short surface terms can be skipped by the minimum term length rule; skipped rows remain in the detail CSV for auditability.
- Passage ranges are resolved independently per source; versification and source differences can change passage letter counts even when the declared start/end refs are the same.
