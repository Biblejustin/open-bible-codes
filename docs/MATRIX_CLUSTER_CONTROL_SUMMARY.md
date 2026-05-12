# Matrix Cluster Control Summary

Status: relation-specific screening summary, not claim promotion.

This report summarizes matrix-neighborhood candidate pairs by nearest-cell relation and compares Bible rows with language-matched secular-control rows already present in the candidate file. The rate ratio is per observed corpus in each class, not a p-value.

No row in this report is promoted as significant. Claim-grade matrix work still needs a preregistered relation metric, locked row-width family, matched control family, and multiple-comparison correction.

## Settings

- Candidate input: `reports/matrix_clusters/candidates.csv`
- Candidate rows: `1,181`
- Bible candidate rows: `1,002`
- Secular-control candidate rows: `179`

## Relation Summary

| Relation | Bible pairs | Control pairs | Bible corpora | Control corpora | Bible/control rate ratio | Bible max corpus | Control max corpus | Exceeds control max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `all` | 1002 | 179 | 5 | 3 | 3.358659 | 204 | 94 | `yes` |
| `diagonal` | 265 | 30 | 5 | 3 | 5.300000 | 55 | 13 | `yes` |
| `orthogonal` | 357 | 37 | 5 | 3 | 5.789189 | 73 | 18 | `yes` |
| `same_cell` | 380 | 112 | 5 | 3 | 2.035714 | 79 | 63 | `yes` |

## Top Term-Pair Rows

| Relation | Term A | Term B | Bible pairs | Control pairs | Bible/control rate ratio | Exceeds control max |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `same_cell` | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | 273 | 100 | 1.638000 | `yes` |
| `diagonal` | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | 42 | 0 | -- | `yes` |
| `orthogonal` | `דריוש` (Daryavesh; English: Darius) | `גוג` (Gog; English: Gog) | 26 | 2 | 2.600000 | `yes` |
| `diagonal` | `דריוש` (Daryavesh; English: Darius) | `חותמ` (chwtm; English: Seal) | 25 | 0 | -- | `yes` |
| `same_cell` | `כורש` (Koresh; English: Cyrus) | `דריוש` (Daryavesh; English: Darius) | 24 | 1 | 4.800000 | `yes` |
| `same_cell` | `תנינ` (tnyn; English: Dragon) | `נביא` (navi; English: Prophet) | 20 | 0 | -- | `yes` |
| `orthogonal` | `חיה` (chayah; English: Beast) | `תנינ` (tnyn; English: Dragon) | 19 | 0 | -- | `yes` |
| `diagonal` | `קרנ` (qeren; English: Horn) | `חזונ` (chzwn; English: Vision) | 18 | 1 | 3.600000 | `yes` |
| `same_cell` | `חיה` (chayah; English: Beast) | `חזונ` (chzwn; English: Vision) | 17 | 5 | 2.040000 | `yes` |
| `diagonal` | `דריוש` (Daryavesh; English: Darius) | `מגוג` (Magog; English: Magog) | 16 | 3 | 2.133333 | `yes` |
| `orthogonal` | `כורש` (Koresh; English: Cyrus) | `דריוש` (Daryavesh; English: Darius) | 16 | 3 | 3.200000 | `yes` |
| `orthogonal` | `תנינ` (tnyn; English: Dragon) | `חזונ` (chzwn; English: Vision) | 16 | 1 | 3.200000 | `yes` |
| `diagonal` | `חיה` (chayah; English: Beast) | `תנינ` (tnyn; English: Dragon) | 16 | 0 | -- | `yes` |
| `orthogonal` | `דריוש` (Daryavesh; English: Darius) | `תנינ` (tnyn; English: Dragon) | 15 | 3 | 2.000000 | `yes` |
| `orthogonal` | `תנינ` (tnyn; English: Dragon) | `מגוג` (Magog; English: Magog) | 15 | 1 | 3.000000 | `yes` |
| `orthogonal` | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | 15 | 1 | 3.000000 | `yes` |
| `diagonal` | `קרנ` (qeren; English: Horn) | `מגוג` (Magog; English: Magog) | 14 | 0 | -- | `yes` |
| `orthogonal` | `חיה` (chayah; English: Beast) | `דריוש` (Daryavesh; English: Darius) | 14 | 0 | -- | `yes` |
| `orthogonal` | `תנינ` (tnyn; English: Dragon) | `קרנ` (qeren; English: Horn) | 14 | 0 | -- | `yes` |
| `orthogonal` | `דריוש` (Daryavesh; English: Darius) | `חזונ` (chzwn; English: Vision) | 13 | 1 | 2.600000 | `yes` |
| `orthogonal` | `חותמ` (chwtm; English: Seal) | `חזונ` (chzwn; English: Vision) | 12 | 1 | 2.400000 | `yes` |
| `orthogonal` | `קרנ` (qeren; English: Horn) | `מגוג` (Magog; English: Magog) | 11 | 0 | -- | `yes` |
| `diagonal` | `כורש` (Koresh; English: Cyrus) | `גוג` (Gog; English: Gog) | 10 | 2 | 1.000000 | `no` |
| `orthogonal` | `מגוג` (Magog; English: Magog) | `חזונ` (chzwn; English: Vision) | 10 | 2 | 1.000000 | `no` |
| `orthogonal` | `כורש` (Koresh; English: Cyrus) | `תנינ` (tnyn; English: Dragon) | 10 | 1 | 2.000000 | `yes` |
| `orthogonal` | `כורש` (Koresh; English: Cyrus) | `נביא` (navi; English: Prophet) | 10 | 1 | 2.000000 | `yes` |
| `orthogonal` | `תנינ` (tnyn; English: Dragon) | `חותמ` (chwtm; English: Seal) | 10 | 1 | 2.000000 | `yes` |
| `diagonal` | `מגוג` (Magog; English: Magog) | `נביא` (navi; English: Prophet) | 10 | 0 | -- | `yes` |
| `diagonal` | `מגוג` (Magog; English: Magog) | `חזונ` (chzwn; English: Vision) | 10 | 0 | -- | `yes` |
| `orthogonal` | `כורש` (Koresh; English: Cyrus) | `קרנ` (qeren; English: Horn) | 10 | 0 | -- | `yes` |
| `orthogonal` | `גוג` (Gog; English: Gog) | `נביא` (navi; English: Prophet) | 10 | 0 | -- | `yes` |
| `orthogonal` | `גוג` (Gog; English: Gog) | `חותמ` (chwtm; English: Seal) | 10 | 0 | -- | `yes` |
| `orthogonal` | `קרנ` (qeren; English: Horn) | `חותמ` (chwtm; English: Seal) | 10 | 0 | -- | `yes` |
| `diagonal` | `דריוש` (Daryavesh; English: Darius) | `תנינ` (tnyn; English: Dragon) | 9 | 0 | -- | `yes` |
| `orthogonal` | `קרנ` (qeren; English: Horn) | `חזונ` (chzwn; English: Vision) | 9 | 0 | -- | `yes` |
| `diagonal` | `נביא` (navi; English: Prophet) | `חזונ` (chzwn; English: Vision) | 8 | 0 | -- | `yes` |
| `diagonal` | `חיה` (chayah; English: Beast) | `חותמ` (chwtm; English: Seal) | 7 | 2 | 1.400000 | `yes` |
| `diagonal` | `קרנ` (qeren; English: Horn) | `חותמ` (chwtm; English: Seal) | 6 | 3 | 0.800000 | `no` |
| `diagonal` | `דריוש` (Daryavesh; English: Darius) | `נביא` (navi; English: Prophet) | 6 | 1 | 1.200000 | `yes` |
| `diagonal` | `חיה` (chayah; English: Beast) | `דריוש` (Daryavesh; English: Darius) | 6 | 0 | -- | `yes` |
| ... | ... | ... | ... | ... | ... | 55 more rows in CSV |

## Read

- `exceeds_secular_max=yes` means the largest Bible corpus count is above the largest secular-control corpus count for that row.
- Empty ratios mean the control denominator is zero.
- This is useful for review prioritization and control auditing only.
- A later confirmatory matrix study should lock which relation rows count and how they are corrected before reading this report.
