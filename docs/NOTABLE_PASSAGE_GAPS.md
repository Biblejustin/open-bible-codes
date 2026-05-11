# Notable Passage Gaps

This report records declared passages where selected ELS terms are absent, sparse, or present when centered inside the passage.
It is intentionally a screening ledger: absence inside a short passage is often expected, so the useful rows are the terms that are absent in the passage while recurring elsewhere in the same corpus, or present at notably lower density than a uniform placement expectation.

## Run Settings

- Passages: `configs/notable_passage_gap_passages.csv`
- Terms: `terms/notable_passage_gap_terms.csv`
- Skip range: `2..100`
- Direction: `both`
- Minimum normalized term length: `3`
- Common-elsewhere threshold: `10` centered hits outside the passage

## Highest Gap Passage Rows

These rows rank declared passages by how many eligible terms are absent inside the passage while recurring at least the threshold count elsewhere in the same corpus. Short passages naturally rank high, so use this as a triage list rather than a formal significance test.

| Passage | Corpus | Letters | Present | Absent Common Elsewhere | Low Vs Uniform | Observed Hits | Uniform Expected Hits |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | 150 | 21 | 30 | 0 | 116 | 118.443 |
| Numbers 6 Priestly Blessing | MAM | 150 | 21 | 30 | 0 | 116 | 118.403 |
| Numbers 6 Priestly Blessing | MT_WLC | 150 | 21 | 30 | 0 | 116 | 118.441 |
| Numbers 6 Priestly Blessing | UHB | 150 | 21 | 30 | 0 | 116 | 118.436 |
| Numbers 6 Priestly Blessing | UXLC | 150 | 21 | 30 | 0 | 116 | 118.438 |
| Deuteronomy 6 Shema | MAM | 205 | 25 | 26 | 1 | 229 | 161.817 |
| Deuteronomy 6 Shema | EBIBLE_WLC | 205 | 26 | 25 | 1 | 231 | 161.872 |
| Deuteronomy 6 Shema | MT_WLC | 205 | 26 | 25 | 1 | 231 | 161.870 |
| Deuteronomy 6 Shema | UHB | 205 | 26 | 25 | 1 | 231 | 161.862 |
| Deuteronomy 6 Shema | UXLC | 205 | 26 | 25 | 1 | 231 | 161.866 |
| Psalm 110 Priest King | MAM | 241 | 28 | 23 | 1 | 172 | 190.234 |
| Psalm 110 Priest King | EBIBLE_WLC | 241 | 29 | 22 | 1 | 173 | 190.299 |
| Psalm 110 Priest King | MT_WLC | 241 | 29 | 22 | 1 | 173 | 190.296 |
| Psalm 110 Priest King | UHB | 241 | 29 | 22 | 1 | 173 | 190.287 |
| Psalm 110 Priest King | UXLC | 241 | 29 | 22 | 1 | 173 | 190.291 |
| Isaiah 7 Immanuel | EBIBLE_WLC | 345 | 34 | 17 | 0 | 285 | 272.419 |
| Isaiah 7 Immanuel | MAM | 345 | 34 | 17 | 0 | 285 | 272.327 |
| Isaiah 7 Immanuel | MT_WLC | 345 | 34 | 17 | 0 | 285 | 272.415 |
| Isaiah 7 Immanuel | UHB | 345 | 34 | 17 | 0 | 285 | 272.403 |
| Isaiah 7 Immanuel | UXLC | 345 | 34 | 17 | 0 | 285 | 272.408 |
| Psalm 2 Messianic King | EBIBLE_WLC | 371 | 34 | 17 | 0 | 262 | 292.949 |
| Psalm 2 Messianic King | MAM | 371 | 34 | 17 | 0 | 262 | 292.850 |
| Psalm 2 Messianic King | MT_WLC | 371 | 34 | 17 | 0 | 262 | 292.945 |
| Psalm 2 Messianic King | UXLC | 371 | 34 | 17 | 0 | 262 | 292.937 |
| Psalm 2 Messianic King | UHB | 371 | 35 | 16 | 0 | 259 | 292.931 |
| Isaiah 9 Child King | MAM | 385 | 35 | 16 | 0 | 309 | 303.901 |
| Isaiah 9 Child King | EBIBLE_WLC | 378 | 36 | 15 | 0 | 283 | 298.477 |
| Isaiah 9 Child King | MT_WLC | 378 | 36 | 15 | 0 | 283 | 298.472 |
| Isaiah 9 Child King | UXLC | 378 | 36 | 15 | 0 | 283 | 298.464 |
| Isaiah 9 Child King | UHB | 437 | 36 | 15 | 0 | 319 | 345.043 |

## Passage Summary

| Passage | Corpus | Letters | Eligible Terms | Present | Absent Elsewhere | Absent Common Elsewhere | Low Vs Uniform | Observed Hits | Uniform Expected Hits |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Genesis 1 Creation | MT_WLC | 1671 | 54 | 40 | 13 | 11 | 2 | 1200 | 1319.436 |
| Genesis 22 Binding Of Isaac | MT_WLC | 1155 | 54 | 43 | 10 | 8 | 1 | 1157 | 911.998 |
| Exodus 12 Passover | MT_WLC | 2836 | 54 | 46 | 7 | 5 | 2 | 2311 | 2239.331 |
| Exodus 20 Decalogue | MT_WLC | 1143 | 54 | 41 | 12 | 10 | 0 | 917 | 902.523 |
| Leviticus 16 Day Of Atonement | MT_WLC | 2062 | 54 | 45 | 8 | 6 | 1 | 1691 | 1628.174 |
| Leviticus 23 Festivals | MT_WLC | 2393 | 54 | 46 | 7 | 5 | 0 | 2014 | 1889.534 |
| Leviticus 24 Blasphemy Law | MT_WLC | 1037 | 54 | 40 | 13 | 11 | 0 | 790 | 818.824 |
| Numbers 6 Priestly Blessing | MT_WLC | 150 | 54 | 21 | 32 | 30 | 0 | 116 | 118.441 |
| Deuteronomy 6 Shema | MT_WLC | 205 | 54 | 26 | 27 | 25 | 1 | 231 | 161.870 |
| 2 Samuel 7 Davidic Covenant | MT_WLC | 1758 | 54 | 42 | 11 | 9 | 4 | 1364 | 1388.132 |
| Psalm 2 Messianic King | MT_WLC | 371 | 54 | 34 | 19 | 17 | 0 | 262 | 292.945 |
| Psalm 22 Suffering Psalm | MT_WLC | 985 | 54 | 41 | 12 | 10 | 1 | 626 | 777.765 |
| Psalm 110 Priest King | MT_WLC | 241 | 54 | 29 | 24 | 22 | 1 | 173 | 190.296 |
| Isaiah 7 Immanuel | MT_WLC | 345 | 54 | 34 | 19 | 17 | 0 | 285 | 272.415 |
| Isaiah 9 Child King | MT_WLC | 378 | 54 | 36 | 17 | 15 | 0 | 283 | 298.472 |
| Isaiah 53 Servant Song | MT_WLC | 800 | 54 | 39 | 14 | 12 | 0 | 613 | 631.687 |
| Daniel 7 Son Of Man | MT_WLC | 2022 | 54 | 45 | 8 | 6 | 1 | 1578 | 1596.589 |
| Daniel 9 Seventy Weeks | MT_WLC | 601 | 54 | 36 | 17 | 15 | 0 | 523 | 474.555 |
| Ezekiel 38 Gog | MT_WLC | 1464 | 54 | 42 | 11 | 9 | 0 | 1175 | 1155.987 |
| Ezekiel 39 Gog | MT_WLC | 1681 | 54 | 43 | 10 | 8 | 0 | 1308 | 1327.333 |
| Joel 2 Spirit And Day Of YHWH | MT_WLC | 1547 | 54 | 42 | 11 | 9 | 1 | 1187 | 1221.525 |
| Zechariah 12 Pierced One | MT_WLC | 923 | 54 | 41 | 12 | 10 | 2 | 656 | 728.809 |
| Zechariah 14 Day Of YHWH | MT_WLC | 1417 | 54 | 43 | 10 | 8 | 2 | 989 | 1118.876 |
| Malachi 3 Messenger | MT_WLC | 1103 | 54 | 43 | 10 | 8 | 0 | 848 | 870.939 |
| Genesis 1 Creation | UXLC | 1671 | 54 | 40 | 13 | 11 | 2 | 1200 | 1319.402 |
| Genesis 22 Binding Of Isaac | UXLC | 1155 | 54 | 43 | 10 | 8 | 1 | 1157 | 911.974 |
| Exodus 12 Passover | UXLC | 2836 | 54 | 46 | 7 | 5 | 2 | 2311 | 2239.272 |
| Exodus 20 Decalogue | UXLC | 1143 | 54 | 41 | 12 | 10 | 0 | 917 | 902.499 |
| Leviticus 16 Day Of Atonement | UXLC | 2062 | 54 | 45 | 8 | 6 | 1 | 1691 | 1628.131 |
| Leviticus 23 Festivals | UXLC | 2393 | 54 | 46 | 7 | 5 | 0 | 2014 | 1889.485 |
| Leviticus 24 Blasphemy Law | UXLC | 1037 | 54 | 40 | 13 | 11 | 0 | 790 | 818.803 |
| Numbers 6 Priestly Blessing | UXLC | 150 | 54 | 21 | 32 | 30 | 0 | 116 | 118.438 |
| Deuteronomy 6 Shema | UXLC | 205 | 54 | 26 | 27 | 25 | 1 | 231 | 161.866 |
| 2 Samuel 7 Davidic Covenant | UXLC | 1758 | 54 | 42 | 11 | 9 | 4 | 1364 | 1388.096 |
| Psalm 2 Messianic King | UXLC | 371 | 54 | 34 | 19 | 17 | 0 | 262 | 292.937 |
| Psalm 22 Suffering Psalm | UXLC | 985 | 54 | 41 | 12 | 10 | 1 | 626 | 777.744 |
| Psalm 110 Priest King | UXLC | 241 | 54 | 29 | 24 | 22 | 1 | 173 | 190.291 |
| Isaiah 7 Immanuel | UXLC | 345 | 54 | 34 | 19 | 17 | 0 | 285 | 272.408 |
| Isaiah 9 Child King | UXLC | 378 | 54 | 36 | 17 | 15 | 0 | 283 | 298.464 |
| Isaiah 53 Servant Song | UXLC | 800 | 54 | 39 | 14 | 12 | 0 | 613 | 631.671 |
| Daniel 7 Son Of Man | UXLC | 2022 | 54 | 45 | 8 | 6 | 1 | 1578 | 1596.547 |
| Daniel 9 Seventy Weeks | UXLC | 601 | 54 | 36 | 17 | 15 | 0 | 523 | 474.542 |
| Ezekiel 38 Gog | UXLC | 1464 | 54 | 42 | 11 | 9 | 0 | 1175 | 1155.957 |
| Ezekiel 39 Gog | UXLC | 1681 | 54 | 43 | 10 | 8 | 0 | 1308 | 1327.298 |
| Joel 2 Spirit And Day Of YHWH | UXLC | 1547 | 54 | 42 | 11 | 9 | 1 | 1187 | 1221.493 |
| Zechariah 12 Pierced One | UXLC | 923 | 54 | 41 | 12 | 10 | 2 | 656 | 728.790 |
| Zechariah 14 Day Of YHWH | UXLC | 1417 | 54 | 43 | 10 | 8 | 2 | 989 | 1118.846 |
| Malachi 3 Messenger | UXLC | 1103 | 54 | 43 | 10 | 8 | 0 | 848 | 870.916 |
| Genesis 1 Creation | EBIBLE_WLC | 1671 | 54 | 40 | 13 | 11 | 2 | 1200 | 1319.456 |
| Genesis 22 Binding Of Isaac | EBIBLE_WLC | 1155 | 54 | 43 | 10 | 8 | 1 | 1157 | 912.012 |
| Exodus 12 Passover | EBIBLE_WLC | 2836 | 54 | 46 | 7 | 5 | 2 | 2311 | 2239.364 |
| Exodus 20 Decalogue | EBIBLE_WLC | 1143 | 54 | 41 | 12 | 10 | 0 | 917 | 902.536 |
| Leviticus 16 Day Of Atonement | EBIBLE_WLC | 2062 | 54 | 45 | 8 | 6 | 1 | 1691 | 1628.198 |
| Leviticus 23 Festivals | EBIBLE_WLC | 2393 | 54 | 46 | 7 | 5 | 0 | 2014 | 1889.562 |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | 1037 | 54 | 40 | 13 | 11 | 0 | 790 | 818.837 |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | 150 | 54 | 21 | 32 | 30 | 0 | 116 | 118.443 |
| Deuteronomy 6 Shema | EBIBLE_WLC | 205 | 54 | 26 | 27 | 25 | 1 | 231 | 161.872 |
| 2 Samuel 7 Davidic Covenant | EBIBLE_WLC | 1758 | 54 | 42 | 11 | 9 | 4 | 1364 | 1388.153 |
| Psalm 2 Messianic King | EBIBLE_WLC | 371 | 54 | 34 | 19 | 17 | 0 | 262 | 292.949 |
| Psalm 22 Suffering Psalm | EBIBLE_WLC | 985 | 54 | 41 | 12 | 10 | 1 | 626 | 777.776 |
| Psalm 110 Priest King | EBIBLE_WLC | 241 | 54 | 29 | 24 | 22 | 1 | 173 | 190.299 |
| Isaiah 7 Immanuel | EBIBLE_WLC | 345 | 54 | 34 | 19 | 17 | 0 | 285 | 272.419 |
| Isaiah 9 Child King | EBIBLE_WLC | 378 | 54 | 36 | 17 | 15 | 0 | 283 | 298.477 |
| Isaiah 53 Servant Song | EBIBLE_WLC | 800 | 54 | 39 | 14 | 12 | 0 | 613 | 631.696 |
| Daniel 7 Son Of Man | EBIBLE_WLC | 2022 | 54 | 45 | 8 | 6 | 1 | 1578 | 1596.613 |
| Daniel 9 Seventy Weeks | EBIBLE_WLC | 601 | 54 | 36 | 17 | 15 | 0 | 523 | 474.562 |
| Ezekiel 38 Gog | EBIBLE_WLC | 1464 | 54 | 42 | 11 | 9 | 0 | 1175 | 1156.005 |
| Ezekiel 39 Gog | EBIBLE_WLC | 1681 | 54 | 43 | 10 | 8 | 0 | 1308 | 1327.352 |
| Joel 2 Spirit And Day Of YHWH | EBIBLE_WLC | 1547 | 54 | 42 | 11 | 9 | 1 | 1187 | 1221.543 |
| Zechariah 12 Pierced One | EBIBLE_WLC | 923 | 54 | 41 | 12 | 10 | 2 | 656 | 728.820 |
| Zechariah 14 Day Of YHWH | EBIBLE_WLC | 1417 | 54 | 43 | 10 | 8 | 2 | 989 | 1118.892 |
| Malachi 3 Messenger | EBIBLE_WLC | 1103 | 54 | 43 | 10 | 8 | 0 | 848 | 870.952 |
| Genesis 1 Creation | MAM | 1671 | 54 | 40 | 13 | 11 | 2 | 1200 | 1319.009 |
| Genesis 22 Binding Of Isaac | MAM | 1155 | 54 | 43 | 10 | 8 | 1 | 1157 | 911.703 |
| Exodus 12 Passover | MAM | 2837 | 54 | 44 | 9 | 7 | 0 | 2304 | 2239.395 |
| Exodus 20 Decalogue | MAM | 1147 | 54 | 39 | 14 | 12 | 0 | 905 | 905.388 |
| Leviticus 16 Day Of Atonement | MAM | 2061 | 54 | 45 | 8 | 6 | 1 | 1681 | 1626.857 |
| Leviticus 23 Festivals | MAM | 2391 | 54 | 47 | 6 | 4 | 0 | 1989 | 1887.344 |
| Leviticus 24 Blasphemy Law | MAM | 1037 | 54 | 40 | 13 | 11 | 0 | 790 | 818.559 |
| Numbers 6 Priestly Blessing | MAM | 150 | 54 | 21 | 32 | 30 | 0 | 116 | 118.403 |
| Deuteronomy 6 Shema | MAM | 205 | 54 | 25 | 28 | 26 | 1 | 229 | 161.817 |
| 2 Samuel 7 Davidic Covenant | MAM | 1760 | 54 | 43 | 10 | 8 | 4 | 1364 | 1389.262 |
| Psalm 2 Messianic King | MAM | 371 | 54 | 34 | 19 | 17 | 0 | 262 | 292.850 |
| Psalm 22 Suffering Psalm | MAM | 984 | 54 | 40 | 13 | 11 | 0 | 641 | 776.724 |
| Psalm 110 Priest King | MAM | 241 | 54 | 28 | 25 | 23 | 1 | 172 | 190.234 |
| Isaiah 7 Immanuel | MAM | 345 | 54 | 34 | 19 | 17 | 0 | 285 | 272.327 |
| Isaiah 9 Child King | MAM | 385 | 54 | 35 | 18 | 16 | 0 | 309 | 303.901 |
| Isaiah 53 Servant Song | MAM | 800 | 54 | 39 | 14 | 12 | 0 | 613 | 631.483 |
| Daniel 7 Son Of Man | MAM | 2104 | 54 | 42 | 11 | 9 | 2 | 1697 | 1660.799 |
| Daniel 9 Seventy Weeks | MAM | 610 | 54 | 37 | 16 | 14 | 1 | 523 | 481.506 |
| Ezekiel 38 Gog | MAM | 1466 | 54 | 43 | 10 | 8 | 0 | 1186 | 1157.192 |
| Ezekiel 39 Gog | MAM | 1685 | 54 | 43 | 10 | 8 | 0 | 1305 | 1330.060 |
| Joel 2 Spirit And Day Of YHWH | MAM | 1547 | 54 | 42 | 11 | 9 | 1 | 1187 | 1221.130 |
| Zechariah 12 Pierced One | MAM | 922 | 54 | 40 | 13 | 11 | 2 | 654 | 727.784 |
| Zechariah 14 Day Of YHWH | MAM | 1430 | 54 | 42 | 11 | 9 | 0 | 998 | 1128.775 |
| Malachi 3 Messenger | MAM | 1102 | 54 | 43 | 10 | 8 | 0 | 849 | 869.867 |
| Genesis 1 Creation | UHB | 1671 | 54 | 40 | 13 | 11 | 2 | 1200 | 1319.376 |
| Genesis 22 Binding Of Isaac | UHB | 1155 | 54 | 43 | 10 | 8 | 1 | 1157 | 911.956 |
| Exodus 12 Passover | UHB | 2836 | 54 | 46 | 7 | 5 | 2 | 2311 | 2239.228 |
| Exodus 20 Decalogue | UHB | 1143 | 54 | 41 | 12 | 10 | 0 | 917 | 902.482 |
| Leviticus 16 Day Of Atonement | UHB | 2063 | 54 | 44 | 9 | 7 | 0 | 1701 | 1628.888 |
| Leviticus 23 Festivals | UHB | 2393 | 54 | 46 | 7 | 5 | 0 | 2014 | 1889.447 |
| Leviticus 24 Blasphemy Law | UHB | 1037 | 54 | 40 | 13 | 11 | 0 | 790 | 818.787 |
| Numbers 6 Priestly Blessing | UHB | 150 | 54 | 21 | 32 | 30 | 0 | 116 | 118.436 |
| Deuteronomy 6 Shema | UHB | 205 | 54 | 26 | 27 | 25 | 1 | 231 | 161.862 |
| 2 Samuel 7 Davidic Covenant | UHB | 1758 | 54 | 42 | 11 | 9 | 4 | 1364 | 1388.069 |
| Psalm 2 Messianic King | UHB | 371 | 54 | 35 | 18 | 16 | 0 | 259 | 292.931 |
| Psalm 22 Suffering Psalm | UHB | 988 | 54 | 40 | 13 | 11 | 0 | 628 | 780.098 |
| Psalm 110 Priest King | UHB | 241 | 54 | 29 | 24 | 22 | 1 | 173 | 190.287 |
| Isaiah 7 Immanuel | UHB | 345 | 54 | 34 | 19 | 17 | 0 | 285 | 272.403 |
| Isaiah 9 Child King | UHB | 437 | 54 | 36 | 17 | 15 | 0 | 319 | 345.043 |
| Isaiah 53 Servant Song | UHB | 800 | 54 | 39 | 14 | 12 | 0 | 613 | 631.658 |
| Daniel 7 Son Of Man | UHB | 2022 | 54 | 45 | 8 | 6 | 1 | 1578 | 1596.516 |
| Daniel 9 Seventy Weeks | UHB | 601 | 54 | 36 | 17 | 15 | 0 | 523 | 474.533 |
| Ezekiel 38 Gog | UHB | 1464 | 54 | 42 | 11 | 9 | 0 | 1175 | 1155.934 |
| Ezekiel 39 Gog | UHB | 1681 | 54 | 43 | 10 | 8 | 0 | 1308 | 1327.272 |
| Joel 2 Spirit And Day Of YHWH | UHB | 1827 | 54 | 43 | 10 | 8 | 2 | 1393 | 1442.549 |
| Zechariah 12 Pierced One | UHB | 923 | 54 | 41 | 12 | 10 | 2 | 656 | 728.776 |
| Zechariah 14 Day Of YHWH | UHB | 1417 | 54 | 43 | 10 | 8 | 3 | 989 | 1118.824 |
| Malachi 3 Messenger | UHB | 1103 | 54 | 43 | 10 | 8 | 0 | 848 | 870.899 |

## Notable Absence / Low-Density Rows

Rows are sorted by gap class first, then by how frequently the term appears centered elsewhere in the same corpus.

| Passage | Corpus | Term | Gap Class | Hits Elsewhere | Hits In Passage | Uniform Expected | Sample Center Refs |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| Deuteronomy 6 Shema | MAM | `חיה` (chayah; English: Beast) | absent_in_passage_common_elsewhere | 51404 | 0 | 8.767 |  |
| Deuteronomy 6 Shema | MT_WLC | `חיה` (chayah; English: Beast) | absent_in_passage_common_elsewhere | 51305 | 0 | 8.786 |  |
| Deuteronomy 6 Shema | EBIBLE_WLC | `חיה` (chayah; English: Beast) | absent_in_passage_common_elsewhere | 51302 | 0 | 8.786 |  |
| Deuteronomy 6 Shema | UXLC | `חיה` (chayah; English: Beast) | absent_in_passage_common_elsewhere | 51295 | 0 | 8.785 |  |
| Deuteronomy 6 Shema | UHB | `חיה` (chayah; English: Beast) | absent_in_passage_common_elsewhere | 51252 | 0 | 8.788 |  |
| Numbers 6 Priestly Blessing | MAM | `עונ` (wn; English: Iniquity) | absent_in_passage_common_elsewhere | 44074 | 0 | 5.500 |  |
| Numbers 6 Priestly Blessing | UHB | `עונ` (wn; English: Iniquity) | absent_in_passage_common_elsewhere | 43797 | 0 | 5.495 |  |
| Numbers 6 Priestly Blessing | UXLC | `עונ` (wn; English: Iniquity) | absent_in_passage_common_elsewhere | 43766 | 0 | 5.484 |  |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | `עונ` (wn; English: Iniquity) | absent_in_passage_common_elsewhere | 43764 | 0 | 5.484 |  |
| Numbers 6 Priestly Blessing | MT_WLC | `עונ` (wn; English: Iniquity) | absent_in_passage_common_elsewhere | 43760 | 0 | 5.484 |  |
| Numbers 6 Priestly Blessing | MAM | `שמע` (shm; English: Hear) | absent_in_passage_common_elsewhere | 36040 | 0 | 4.498 |  |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | `שמע` (shm; English: Hear) | absent_in_passage_common_elsewhere | 36000 | 0 | 4.511 |  |
| Numbers 6 Priestly Blessing | MT_WLC | `שמע` (shm; English: Hear) | absent_in_passage_common_elsewhere | 35983 | 0 | 4.509 |  |
| Numbers 6 Priestly Blessing | UXLC | `שמע` (shm; English: Hear) | absent_in_passage_common_elsewhere | 35976 | 0 | 4.508 |  |
| Numbers 6 Priestly Blessing | UHB | `שמע` (shm; English: Hear) | absent_in_passage_common_elsewhere | 35973 | 0 | 4.513 |  |
| Deuteronomy 6 Shema | EBIBLE_WLC | `לחמ` (lchm; English: Bread) | absent_in_passage_common_elsewhere | 33275 | 0 | 5.699 |  |
| Deuteronomy 6 Shema | MT_WLC | `לחמ` (lchm; English: Bread) | absent_in_passage_common_elsewhere | 33267 | 0 | 5.697 |  |
| Deuteronomy 6 Shema | UXLC | `לחמ` (lchm; English: Bread) | absent_in_passage_common_elsewhere | 33263 | 0 | 5.696 |  |
| Deuteronomy 6 Shema | MAM | `לחמ` (lchm; English: Bread) | absent_in_passage_common_elsewhere | 33229 | 0 | 5.667 |  |
| Deuteronomy 6 Shema | UHB | `לחמ` (lchm; English: Bread) | absent_in_passage_common_elsewhere | 33095 | 0 | 5.674 |  |
| Deuteronomy 6 Shema | MAM | `דוד` (dwd; English: David) | absent_in_passage_common_elsewhere | 21144 | 0 | 3.606 |  |
| Psalm 110 Priest King | MAM | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13567 | 0 | 2.720 |  |
| Deuteronomy 6 Shema | MAM | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13567 | 0 | 2.314 |  |
| Numbers 6 Priestly Blessing | MAM | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13567 | 0 | 1.693 |  |
| Daniel 9 Seventy Weeks | UHB | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13472 | 0 | 6.772 |  |
| Psalm 110 Priest King | UHB | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13472 | 0 | 2.716 |  |
| Deuteronomy 6 Shema | UHB | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13472 | 0 | 2.310 |  |
| Numbers 6 Priestly Blessing | UHB | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13472 | 0 | 1.690 |  |
| Daniel 9 Seventy Weeks | UXLC | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13459 | 0 | 6.757 |  |
| Psalm 110 Priest King | UXLC | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13459 | 0 | 2.710 |  |
| Deuteronomy 6 Shema | UXLC | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13459 | 0 | 2.305 |  |
| Numbers 6 Priestly Blessing | UXLC | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13459 | 0 | 1.687 |  |
| Daniel 9 Seventy Weeks | EBIBLE_WLC | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13455 | 0 | 6.755 |  |
| Daniel 9 Seventy Weeks | MT_WLC | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13455 | 0 | 6.755 |  |
| Psalm 110 Priest King | EBIBLE_WLC | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13455 | 0 | 2.709 |  |
| Psalm 110 Priest King | MT_WLC | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13455 | 0 | 2.709 |  |
| Deuteronomy 6 Shema | EBIBLE_WLC | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13455 | 0 | 2.304 |  |
| Deuteronomy 6 Shema | MT_WLC | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13455 | 0 | 2.304 |  |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13455 | 0 | 1.686 |  |
| Numbers 6 Priestly Blessing | MT_WLC | `ארצ` (rts; English: Earth) | absent_in_passage_common_elsewhere | 13455 | 0 | 1.686 |  |
| Numbers 6 Priestly Blessing | MAM | `עבד` (bd; English: Servant) | absent_in_passage_common_elsewhere | 12874 | 0 | 1.607 |  |
| Numbers 6 Priestly Blessing | UXLC | `עבד` (bd; English: Servant) | absent_in_passage_common_elsewhere | 12784 | 0 | 1.602 |  |
| Numbers 6 Priestly Blessing | MT_WLC | `עבד` (bd; English: Servant) | absent_in_passage_common_elsewhere | 12780 | 0 | 1.601 |  |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | `עבד` (bd; English: Servant) | absent_in_passage_common_elsewhere | 12775 | 0 | 1.601 |  |
| Numbers 6 Priestly Blessing | UHB | `עבד` (bd; English: Servant) | absent_in_passage_common_elsewhere | 12737 | 0 | 1.598 |  |
| Zechariah 12 Pierced One | UHB | `קבר` (qbr; English: Grave) | absent_in_passage_common_elsewhere | 10156 | 0 | 7.840 |  |
| Zechariah 12 Pierced One | UXLC | `קבר` (qbr; English: Grave) | absent_in_passage_common_elsewhere | 10155 | 0 | 7.830 |  |
| Psalm 2 Messianic King | UXLC | `קבר` (qbr; English: Grave) | absent_in_passage_common_elsewhere | 10155 | 0 | 3.147 |  |
| Zechariah 12 Pierced One | MT_WLC | `קבר` (qbr; English: Grave) | absent_in_passage_common_elsewhere | 10154 | 0 | 7.829 |  |
| Psalm 2 Messianic King | MT_WLC | `קבר` (qbr; English: Grave) | absent_in_passage_common_elsewhere | 10154 | 0 | 3.147 |  |
| Zechariah 12 Pierced One | EBIBLE_WLC | `קבר` (qbr; English: Grave) | absent_in_passage_common_elsewhere | 10149 | 0 | 7.826 |  |
| Psalm 2 Messianic King | EBIBLE_WLC | `קבר` (qbr; English: Grave) | absent_in_passage_common_elsewhere | 10149 | 0 | 3.145 |  |
| Zechariah 12 Pierced One | MAM | `קבר` (qbr; English: Grave) | absent_in_passage_common_elsewhere | 10078 | 0 | 7.731 |  |
| Psalm 2 Messianic King | MAM | `קבר` (qbr; English: Grave) | absent_in_passage_common_elsewhere | 10078 | 0 | 3.111 |  |
| Deuteronomy 6 Shema | MAM | `רגמ` (rgm; English: Stone Verb) | absent_in_passage_common_elsewhere | 9707 | 0 | 1.656 |  |
| Numbers 6 Priestly Blessing | MAM | `רגמ` (rgm; English: Stone Verb) | absent_in_passage_common_elsewhere | 9707 | 0 | 1.211 |  |
| Deuteronomy 6 Shema | UXLC | `רגמ` (rgm; English: Stone Verb) | absent_in_passage_common_elsewhere | 9627 | 0 | 1.649 |  |
| Numbers 6 Priestly Blessing | UXLC | `רגמ` (rgm; English: Stone Verb) | absent_in_passage_common_elsewhere | 9627 | 0 | 1.206 |  |
| Deuteronomy 6 Shema | MT_WLC | `רגמ` (rgm; English: Stone Verb) | absent_in_passage_common_elsewhere | 9626 | 0 | 1.649 |  |
| Numbers 6 Priestly Blessing | MT_WLC | `רגמ` (rgm; English: Stone Verb) | absent_in_passage_common_elsewhere | 9626 | 0 | 1.206 |  |
| Deuteronomy 6 Shema | EBIBLE_WLC | `רגמ` (rgm; English: Stone Verb) | absent_in_passage_common_elsewhere | 9620 | 0 | 1.647 |  |
| Numbers 6 Priestly Blessing | EBIBLE_WLC | `רגמ` (rgm; English: Stone Verb) | absent_in_passage_common_elsewhere | 9620 | 0 | 1.205 |  |
| Deuteronomy 6 Shema | UHB | `רגמ` (rgm; English: Stone Verb) | absent_in_passage_common_elsewhere | 9604 | 0 | 1.647 |  |
| Numbers 6 Priestly Blessing | UHB | `רגמ` (rgm; English: Stone Verb) | absent_in_passage_common_elsewhere | 9604 | 0 | 1.205 |  |
| Psalm 22 Suffering Psalm | MAM | `שמימ` (shmym; English: Heavens) | absent_in_passage_common_elsewhere | 9413 | 0 | 7.706 |  |
| Zechariah 12 Pierced One | MAM | `שמימ` (shmym; English: Heavens) | absent_in_passage_common_elsewhere | 9413 | 0 | 7.220 |  |
| Psalm 22 Suffering Psalm | UHB | `שמימ` (shmym; English: Heavens) | absent_in_passage_common_elsewhere | 9374 | 0 | 7.746 |  |
| Psalm 110 Priest King | MAM | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8553 | 0 | 1.715 |  |
| Deuteronomy 6 Shema | MAM | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8553 | 0 | 1.459 |  |
| Numbers 6 Priestly Blessing | MAM | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8553 | 0 | 1.067 |  |
| Psalm 110 Priest King | UHB | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8442 | 0 | 1.702 |  |
| Deuteronomy 6 Shema | UHB | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8442 | 0 | 1.447 |  |
| Numbers 6 Priestly Blessing | UHB | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8442 | 0 | 1.059 |  |
| Psalm 110 Priest King | MT_WLC | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8433 | 0 | 1.698 |  |
| Deuteronomy 6 Shema | MT_WLC | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8433 | 0 | 1.444 |  |
| Numbers 6 Priestly Blessing | MT_WLC | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8433 | 0 | 1.057 |  |
| Psalm 110 Priest King | UXLC | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8431 | 0 | 1.697 |  |
| Deuteronomy 6 Shema | UXLC | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8431 | 0 | 1.444 |  |
| Numbers 6 Priestly Blessing | UXLC | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8431 | 0 | 1.056 |  |
| Psalm 110 Priest King | EBIBLE_WLC | `קרנ` (qrn; English: Horn) | absent_in_passage_common_elsewhere | 8428 | 0 | 1.697 |  |

## Output Files

- Detail CSV: `reports/notable_passage_gaps/term_gap_detail.csv`
- Passage summary CSV: `reports/notable_passage_gaps/passage_summary.csv`
- Manifest: `reports/notable_passage_gaps/manifest.json`

## Cautions

- This report does not treat absence as a negative proof. It records silence and lower-density rows so they can be reviewed alongside positive centered hits.
- `expected_in_passage_uniform` is a descriptive baseline only; it is not a formal p-value.
- Short surface terms can be skipped by the minimum term length rule; skipped rows remain in the detail CSV for auditability.
- Passage ranges are resolved independently per source; versification and source differences can change passage letter counts even when the declared start/end refs are the same.
