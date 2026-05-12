# Matrix Cluster Candidates

This is an opt-in geometry screen over already-exported raw ELS hit rows. It wraps each hit path into a matrix of the locked row width, then records declared-term pairs whose letter paths share a cell or fall within the configured cell-neighborhood distance.

This report is candidate extraction only. It is not claim promotion. When the input is CRD output, Bible and secular-control rows are both present; matrix-style claims still require a locked relation-specific metric and correction for the widened geometry search family.

## Run Settings

- input files: `reports/crd/classified_hits.csv`
- row width: `50`
- max cell distance: `1`
- max pairs: `100,000`
- allow same term pairs: `False`
- parsed hit rows: `15,945` of `15,945`
- skipped input rows: `0`
- candidate pairs: `1,181`

## Relation Counts

| Relation | Pairs |
| --- | ---: |
| same_cell | 492 |
| orthogonal | 394 |
| diagonal | 295 |

## Corpus Counts

| Corpus | Pairs |
| --- | ---: |
| UHB | 204 |
| EBIBLE_WLC | 202 |
| UXLC | 202 |
| MT_WLC | 201 |
| MAM | 193 |
| HEB_PBY_AHAD_HAAM | 94 |
| HEB_PBY_BIALIK | 45 |
| HEB_PBY_BRENNER | 40 |

## Corpus Class Counts

| Corpus class | Pairs |
| --- | ---: |
| bible | 1,002 |
| secular_control | 179 |

## Sample Candidates

| Relation | Corpus | Left | Right | Left center | Right center | Cells |
| --- | --- | --- | --- | --- | --- | --- |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | 2Sam 22:8 / `וַ/יִּֽתְגָּעֲשׁ֖וּ` (wytgshw) | 2Sam 22:8 / `יִרְגָּ֑זוּ` (yrgzw) | 9449:16 -> 9449:16 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | 2Sam 22:8 / `וַ/יִּֽתְגָּעֲשׁ֖וּ` (wytgshw) | 2Sam 22:8 / `יִרְגָּ֑זוּ` (yrgzw) | 9449:22 -> 9449:22 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Ps 18:8 / `וַ֝/יִּתְגָּֽעֲשׁ֗וּ` (wytgshw) | Ps 18:8 / `יִרְגָּ֑זוּ` (yrgzw) | 17304:48 -> 17304:48 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Ps 18:8 / `וַ֝/יִּתְגָּֽעֲשׁ֗וּ` (wytgshw) | Ps 18:8 / `יִרְגָּ֑זוּ` (yrgzw) | 17305:4 -> 17305:4 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Josh 6:1 / `וּ/מְסֻגֶּ֔רֶת` (wmsgrt) | Josh 6:1 / `וּ/מְסֻגֶּ֔רֶת` (wmsgrt) | 6228:37 -> 6228:37 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Josh 6:1 / `וּ/מְסֻגֶּ֔רֶת` (wmsgrt) | Josh 6:1 / `וּ/מְסֻגֶּ֔רֶת` (wmsgrt) | 6228:43 -> 6228:43 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | 2Kgs 9:35 / `וְ/הָ/רַגְלַ֖יִם` (whrglym) | 2Kgs 9:35 / `וְ/הָ/רַגְלַ֖יִם` (whrglym) | 10897:1 -> 10897:1 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | 2Kgs 9:35 / `וְ/הָ/רַגְלַ֖יִם` (whrglym) | 2Kgs 9:35 / `וְ/הָ/רַגְלַ֖יִם` (whrglym) | 10897:7 -> 10897:7 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | 1Chr 6:65 / `וְ/אֶת` (wt) | 1Chr 6:65 / `בַּ/גִּלְעָ֖ד` (bgld) | 22169:8 -> 22169:8 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | 1Chr 6:65 / `וְ/אֶת` (wt) | 1Chr 6:65 / `בַּ/גִּלְעָ֖ד` (bgld) | 22169:16 -> 22169:16 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | 1Chr 12:9 / `וּ/מִן` (wmn) | 1Chr 12:8 / `הַ/גְּדֽוֹר` (hgdwr) | 22339:0 -> 22339:0 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | 1Chr 12:9 / `וּ/מִן` (wmn) | 1Chr 12:8 / `הַ/גְּדֽוֹר` (hgdwr) | 22339:8 -> 22339:8 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Jer 51:55 / `וְ/הָמ֤וּ` (whmw) | Jer 51:55 / `וְ/הָמ֤וּ` (whmw) | 14489:24 -> 14489:24 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Jer 51:55 / `וְ/הָמ֤וּ` (whmw) | Jer 51:55 / `וְ/הָמ֤וּ` (whmw) | 14489:32 -> 14489:32 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Jer 27:8 / `וְ/הָיָ֨ה` (whyh) | Jer 27:7 / `גְּדֹלִֽים` (gdlym) | 13631:1 -> 13631:1 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Jer 27:8 / `וְ/הָיָ֨ה` (whyh) | Jer 27:7 / `גְּדֹלִֽים` (gdlym) | 13631:11 -> 13631:11 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Gen 27:15 / `עֵשָׂ֜ו` (shw) | Gen 27:15 / `בְּנָ֤/הּ` (bnh) | 737:31 -> 737:31 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Gen 27:15 / `עֵשָׂ֜ו` (shw) | Gen 27:15 / `בְּנָ֤/הּ` (bnh) | 737:41 -> 737:41 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Gen 49:19 / `וְ/ה֖וּא` (whw) | Gen 49:19 / `וְ/ה֖וּא` (whw) | 1519:9 -> 1519:9 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Gen 49:19 / `וְ/ה֖וּא` (whw) | Gen 49:19 / `וְ/ה֖וּא` (whw) | 1519:19 -> 1519:19 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Jer 27:8 / `וְ/הָיָ֨ה` (whyh) | Jer 27:8 / `וְ/הָיָ֨ה` (whyh) | 13631:1 -> 13631:1 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Jer 27:8 / `וְ/הָיָ֨ה` (whyh) | Jer 27:8 / `וְ/הָיָ֨ה` (whyh) | 13631:11 -> 13631:11 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Deut 33:15 / `עוֹלָֽם` (wlm) | Deut 33:15 / `גִּבְע֥וֹת` (gbwt) | 6070:29 -> 6070:29 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Deut 33:15 / `עוֹלָֽם` (wlm) | Deut 33:15 / `גִּבְע֥וֹת` (gbwt) | 6070:41 -> 6070:41 |
| same_cell | MT_WLC | `גוג` (Gog; English: Gog) | `מגוג` (Magog; English: Magog) | Ps 120:4 / `שְׁנוּנִ֑ים` (shnwnym) | Ps 120:4 / `גִבּ֣וֹר` (gbwr) | 18543:2 -> 18543:2 |
