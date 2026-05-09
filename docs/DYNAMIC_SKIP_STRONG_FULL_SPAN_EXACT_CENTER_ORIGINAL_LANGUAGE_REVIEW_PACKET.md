# Strong Full-Span Exact-Center Original-Language Review Packet

This packet is a human-review entry point for original-language Bible rows
from the full-span exact-center run. It keeps English KJV rows and
non-Bible controls out of the primary table, but still reports matched
control summaries where available.

## Reproduce

```bash
python3 -m scripts.build_dynamic_span_exact_center_original_language_review_packet --bundle reports/dynamic_skip_focus/strong_full_span_exact_center_review_bundle.csv --exact-rows reports/dynamic_skip_focus/strong_full_span_exact_center_rows.csv --context reports/dynamic_skip_focus/strong_full_span_exact_center_context.csv --matrix-dir reports/dynamic_skip_focus/exact_center_matrix --exact-summary reports/dynamic_skip_focus/strong_full_span_exact_center_rows_summary.csv --review-out reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_review_packet.csv --paths-out reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_review_paths.csv --markdown-out docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ORIGINAL_LANGUAGE_REVIEW_PACKET.md --manifest-out reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_review_packet.manifest.json
```

## Scope

- review units: 76
- path rows joined: 1,090
- review CSV: `reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_review_packet.csv`
- path CSV: `reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_review_paths.csv`

## Corpus Counts

| Corpus | Review units | Path rows |
| --- | ---: | ---: |
| LXX | 57 | 70 |
| UHB | 14 | 941 |
| EBIBLE_WLC | 4 | 75 |
| TCG_NT | 1 | 4 |

## Term Counts

| Term | Review units |
| --- | ---: |
| `ιησουσ` | 57 |
| `ישוע` | 14 |
| `משיח` | 4 |
| `γωγ` | 1 |

## Available Control Summaries

| Control corpus | Term | Exact-center rows | Rows per million hits | Top center words |
| --- | --- | ---: | ---: | --- |
| ENG_PG_SHAKESPEARE | `jesus` | 2 | 22.895607 | Jesus=2 |
| GRC_PERSEUS_HERODOTUS | `γωγ` | 0 | 0.0 |  |
| GRC_PERSEUS_HERODOTUS | `ιησουσ` | 0 | 0.0 |  |
| HEB_PBY_BIALIK | `ישוע` | 1,151 | 5.563143 | ישוע=825; "ישוע=184; (ישוע=142 |
| HEB_PBY_BIALIK | `משיח` | 7,059 | 64.097329 | משיח=4399; משיח,=1077; משיח.=639; משיח?=561; משיח3430=106; משיח1755=95; משיח179=75; משי... |

## Review Units

| Rank | Corpus | Term | Center | Paths | Example span | Matrix | Control read | Context |
| ---: | --- | --- | --- | ---: | --- | --- | --- | --- |
| 1 | UHB | `ישוע` | NEH 8:17 `יֵשׁ֨וּעַ` | 85 | NEH 9:6 -> NEH 8:17 -> NEH 8:9 | 4 rows @ width 391 | language-matched controls also produce exact-center rows; treat as background-rate warning | וַ⁠יֵּשְׁב֣וּ בַ⁠סֻּכּוֹת֒ כִּ֣י לֹֽא־עָשׂ֡וּ מִ⁠ימֵי֩ [יֵשׁ֨וּעַ] בִּן־נ֥וּן כֵּן֙ בְּנֵ֣י יִשְׂ... |
| 2 | UHB | `ישוע` | EZR 2:2 `יֵשׁ֡וּעַ` | 83 | 2CH 34:22 -> EZR 2:2 -> EZR 5:5 | 4 rows @ width 3498 | language-matched controls also produce exact-center rows; treat as background-rate warning | אֲשֶׁר־בָּ֣אוּ עִם־זְרֻבָּבֶ֗ל [יֵשׁ֡וּעַ] נְ֠חֶמְיָה שְׂרָיָ֨ה רְֽעֵלָיָ֜ה מָרְדֳּכַ֥י בִּלְשָׁ֛ן |
| 3 | UHB | `ישוע` | EZR 3:9 `יֵשׁ֡וּעַ` | 73 | EZR 2:36 -> EZR 3:9 -> EZR 4:21 | 4 rows @ width 1278 | language-matched controls also produce exact-center rows; treat as background-rate warning | וַ⁠יַּעֲמֹ֣ד [יֵשׁ֡וּעַ] בָּנָ֣י⁠ו וְ֠⁠אֶחָי⁠ו קַדְמִיאֵ֨ל וּ⁠בָנָ֤י⁠ו בְּנֵֽי־יְהוּדָה֙ |
| 4 | UHB | `ישוע` | EZR 2:6 `יֵשׁ֖וּעַ` | 73 | 2CH 36:7 -> EZR 2:6 -> EZR 3:3 | 4 rows @ width 1475 | language-matched controls also produce exact-center rows; treat as background-rate warning | בְּנֵֽי־פַחַ֥ת מוֹאָ֛ב לִ⁠בְנֵ֥י [יֵשׁ֖וּעַ] יוֹאָ֑ב אַלְפַּ֕יִם שְׁמֹנֶ֥ה מֵא֖וֹת וּ⁠שְׁנֵ֥ים |
| 5 | UHB | `ישוע` | NEH 9:5 `יֵשׁ֣וּעַ` | 70 | NEH 9:12 -> NEH 9:5 -> NEH 8:15 | 4 rows @ width 384 | language-matched controls also produce exact-center rows; treat as background-rate warning | וַ⁠יֹּאמְר֣וּ הַ⁠לְוִיִּ֡ם [יֵשׁ֣וּעַ] וְ֠⁠קַדְמִיאֵל בָּנִ֨י חֲשַׁבְנְיָ֜ה שֵׁרֵֽבְיָ֤ה הֽוֹדִיָּה֙ |
| 6 | UHB | `ישוע` | NEH 12:8 `יֵשׁ֧וּעַ` | 69 | NEH 9:27 -> NEH 12:8 -> EST 1:3 | 4 rows @ width 2788 | language-matched controls also produce exact-center rows; treat as background-rate warning | וְ⁠הַ⁠לְוִיִּ֗ם [יֵשׁ֧וּעַ] בִּנּ֛וּי קַדְמִיאֵ֥ל שֵׁרֵבְיָ֖ה יְהוּדָ֣ה מַתַּנְיָ֑ה |
| 7 | UHB | `ישוע` | EZR 10:18 `יֵשׁ֤וּעַ` | 68 | NEH 11:6 -> EZR 10:18 -> 2CH 35:9 | 4 rows @ width 11909 | language-matched controls also produce exact-center rows; treat as background-rate warning | אֲשֶׁ֥ר הֹשִׁ֖יבוּ נָשִׁ֣ים נָכְרִיּ֑וֹת מִ⁠בְּנֵ֨י [יֵשׁ֤וּעַ] בֶּן־יֽוֹצָדָק֙ וְ⁠אֶחָ֔י⁠ו מַֽעֲ... |
| 8 | UHB | `ישוע` | NEH 7:11 `יֵשׁ֖וּעַ` | 67 | NEH 4:7 -> NEH 7:11 -> NEH 9:10 | 4 rows @ width 2825 | language-matched controls also produce exact-center rows; treat as background-rate warning | בְּנֵֽי־פַחַ֥ת מוֹאָ֛ב לִ⁠בְנֵ֥י [יֵשׁ֖וּעַ] וְ⁠יוֹאָ֑ב אַלְפַּ֕יִם וּ⁠שְׁמֹנֶ֥ה מֵא֖וֹת שְׁמֹנָ֥ה |
| 9 | UHB | `ישוע` | NEH 9:4 `יֵשׁ֨וּעַ` | 66 | NEH 2:8 -> NEH 9:4 -> EST 1:20 | 4 rows @ width 7519 | language-matched controls also produce exact-center rows; treat as background-rate warning | וַ⁠יָּ֜קָם עַֽל־מַֽעֲלֵ֣ה הַ⁠לְוִיִּ֗ם [יֵשׁ֨וּעַ] וּ⁠בָנִ֜י קַדְמִיאֵ֧ל שְׁבַנְיָ֛ה בֻּנִּ֥י שֵׁ... |
| 10 | UHB | `ישוע` | EZR 2:36 `יֵשׁ֔וּעַ` | 63 | 2CH 34:18 -> EZR 2:36 -> EZR 6:15 | 4 rows @ width 4294 | language-matched controls also produce exact-center rows; treat as background-rate warning | הַֽ⁠כֹּהֲנִ֑ים בְּנֵ֤י יְדַֽעְיָה֙ לְ⁠בֵ֣ית [יֵשׁ֔וּעַ] תְּשַׁ֥ע מֵא֖וֹת שִׁבְעִ֥ים וּ⁠שְׁלֹשָֽׁה׃ |
| 11 | UHB | `ישוע` | NEH 12:7 `יֵשֽׁוּעַ׃` | 59 | EST 9:20 -> NEH 12:7 -> NEH 3:19 | 4 rows @ width 10023 | language-matched controls also produce exact-center rows; treat as background-rate warning | אֵ֣לֶּה רָאשֵׁ֧י הַ⁠כֹּהֲנִ֛ים וַ⁠אֲחֵי⁠הֶ֖ם בִּ⁠ימֵ֥י [יֵשֽׁוּעַ׃] |
| 12 | UHB | `ישוע` | NEH 7:39 `יֵשׁ֔וּעַ` | 56 | NEH 7:45 -> NEH 7:39 -> NEH 7:32 | 4 rows @ width 122 | language-matched controls also produce exact-center rows; treat as background-rate warning | הַֽ⁠כֹּהֲנִ֑ים בְּנֵ֤י יְדַֽעְיָה֙ לְ⁠בֵ֣ית [יֵשׁ֔וּעַ] תְּשַׁ֥ע מֵא֖וֹת שִׁבְעִ֥ים וּ⁠שְׁלֹשָֽׁה׃ |
| 13 | UHB | `ישוע` | NEH 7:7 `יֵשׁ֡וּעַ` | 55 | EZR 6:6 -> NEH 7:7 -> EST 2:23 | 4 rows @ width 11329 | language-matched controls also produce exact-center rows; treat as background-rate warning | הַ⁠בָּאִ֣ים עִם־זְרֻבָּבֶ֗ל [יֵשׁ֡וּעַ] נְחֶמְיָ֡ה עֲ֠זַרְיָה רַֽעַמְיָ֨ה נַחֲמָ֜נִי מָרְדֳּכַ֥י |
| 14 | UHB | `ישוע` | EZR 3:2 `יֵשׁ֨וּעַ` | 54 | NEH 3:20 -> EZR 3:2 -> 2CH 30:3 | 4 rows @ width 10793 | language-matched controls also produce exact-center rows; treat as background-rate warning | וַ⁠יָּקָם֩ [יֵשׁ֨וּעַ] בֶּן־יֽוֹצָדָ֜ק וְ⁠אֶחָ֣י⁠ו הַ⁠כֹּהֲנִ֗ים וּ⁠זְרֻבָּבֶ֤ל בֶּן־שְׁאַלְתִּיאֵל֙ |
| 15 | EBIBLE_WLC | `משיח` | 2SA 1:21 `מָשִׁ֥יחַ` | 33 | 2SA 2:15 -> 2SA 1:21 -> 1SA 31:12 | 4 rows @ width 791 | language-matched controls also produce exact-center rows; treat as background-rate warning | מָגֵ֣ן גִּבּוֹרִ֔ים מָגֵ֣ן שָׁא֔וּל בְּלִ֖י [מָשִׁ֥יחַ] בַּשָּֽׁמֶן׃ |
| 16 | EBIBLE_WLC | `משיח` | 2SA 23:1 `מְשִׁ֨יחַ֙` | 30 | 1KI 5:22 -> 2SA 23:1 -> 2SA 16:4 | 4 rows @ width 8885 | language-matched controls also produce exact-center rows; treat as background-rate warning | בֶּן־יִשַׁ֗י וּנְאֻ֤ם הַגֶּ֨בֶר֙ הֻ֣קַם עָ֔ל [מְשִׁ֨יחַ֙] אֱלֹהֵ֣י יַֽעֲקֹ֔ב וּנְעִ֖ים זְמִר֥וֹת ... |
| 17 | EBIBLE_WLC | `משיח` | LAM 4:20 `מְשִׁ֣יחַ` | 11 | EZK 1:24 -> LAM 4:20 -> LAM 3:16 | 4 rows @ width 1356 | language-matched controls also produce exact-center rows; treat as background-rate warning | ר֤וּחַ אַפֵּ֨ינוּ֙ [מְשִׁ֣יחַ] יְהוָ֔ה נִלְכַּ֖ד בִּשְׁחִיתוֹתָ֑ם אֲשֶׁ֣ר אָמַ֔רְנוּ |
| 18 | TCG_NT | `γωγ` | REV 20:8 `Γὼγ` | 4 | REV 20:8 -> REV 20:8 -> REV 20:8 | 3 rows @ width 17 | available language-matched control summary has zero exact-center rows for this normalized term | τέσσαρσι γωνίαις τῆς γῆς, τὸν [Γὼγ] καὶ τὸν Μαγώγ, συναγαγεῖν αὐτοὺς |
| 19 | LXX | `ιησουσ` | JOS 22:7 `Ἰησοῦς` | 3 | 1SA 14:26 -> JOS 22:7 -> DEU 10:2 | 6 rows @ width 54232 | available language-matched control summary has zero exact-center rows for this normalized term | Βασανίτιδι, καὶ τῷ ἡμίσει ἔδωκεν [Ἰησοῦς] μετὰ τῶν ἀδελφῶν αὐτοῦ ἐν |
| 20 | LXX | `ιησουσ` | JOS 8:3 `Ἰησοῦς` | 3 | NUM 9:18 -> JOS 8:3 -> 1SA 23:14 | 6 rows @ width 85420 | available language-matched control summary has zero exact-center rows for this normalized term | ἀναβῆναι εἰς Γαί. ἐπέλεξε δὲ [Ἰησοῦς] τριάκοντα χιλιάδας ἀνδρῶν δυνατοὺς ἐν |
| 21 | LXX | `ιησουσ` | JOS 18:3 `Ἰησοῦς` | 3 | NUM 17:23 -> JOS 18:3 -> 2SA 3:21 | 6 rows @ width 86975 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ εἶπεν [Ἰησοῦς] τοῖς υἱοῖς Ἰσραήλ· ἕως τίνος |
| 22 | LXX | `ιησουσ` | NEH 9:5 `Ἰησοῦς` | 2 | JOB 30:9 -> NEH 9:5 -> 2CH 26:12 | 6 rows @ width 23792 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ εἴποσαν οἱ Λευῖται [Ἰησοῦς] καὶ Καδμιήλ· ἀνάστητε, εὐλογεῖτε Κύριον |
| 23 | LXX | `ιησουσ` | JOS 4:20 `Ἰησοῦς` | 2 | DEU 9:23 -> JOS 4:20 -> JDG 6:29 | 6 rows @ width 33728 | available language-matched control summary has zero exact-center rows for this normalized term | ἔλαβεν ἐκ τοῦ Ἰορδάνου, ἔστησεν [Ἰησοῦς] ἐν Γαλγάλοις |
| 24 | LXX | `ιησουσ` | JOS 8:3 `Ἰησοῦς` | 2 | 1SA 3:12 -> JOS 8:3 -> NUM 30:12 | 6 rows @ width 59022 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ἀνέστη [Ἰησοῦς] καὶ πᾶς ὁ λαὸς ὁ |
| 25 | LXX | `ιησουσ` | JOS 24:30 `Ἰησοῦς` | 2 | NUM 19:2 -> JOS 24:30 -> 2SA 16:4 | 6 rows @ width 94531 | available language-matched control summary has zero exact-center rows for this normalized term | ἐγένετο μετ' ἐκεῖνα καὶ ἀπέθανεν [Ἰησοῦς] υἱὸς Ναυὴ δοῦλος Κυρίου ἑκατὸν |
| 26 | LXX | `ιησουσ` | JOS 24:28 `Ἰησοῦς` | 2 | NUM 10:6 -> JOS 24:28 -> 2SA 23:22 | 6 rows @ width 106268 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ἀπέστειλεν [Ἰησοῦς] τὸν λαόν, καὶ ἐπορεύθησαν ἕκαστος |
| 27 | LXX | `ιησουσ` | JOS 6:16 `Ἰησοῦς` | 2 | 2SA 24:17 -> JOS 6:16 -> LEV 4:28 | 6 rows @ width 130919 | available language-matched control summary has zero exact-center rows for this normalized term | ἐσάλπισαν οἱ ἱερεῖς, καὶ εἶπεν [Ἰησοῦς] τοῖς υἱοῖς Ἰσραήλ· κεκράξατε, παρέδωκε |
| 28 | LXX | `ιησουσ` | JOS 10:24 `Ἰησοῦς` | 2 | EXO 23:23 -> JOS 10:24 -> 1KI 20:19 | 6 rows @ width 161889 | available language-matched control summary has zero exact-center rows for this normalized term | αὐτοὺς πρὸς Ἰησοῦν, καὶ συνεκάλεσεν [Ἰησοῦς] πάντα Ἰσραήλ, καὶ τοὺς ἐναρχομένους |
| 29 | LXX | `ιησουσ` | JOS 9:33 `Ἰησοῦς` | 1 | JOS 13:4 -> JOS 9:33 -> JOS 6:26 | 6 rows @ width 4234 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ κατέστησεν αὐτοὺς [Ἰησοῦς] ἐν τῇ ἡμέρᾳ ἐκείνῃ ξυλοκόπους |
| 30 | EBIBLE_WLC | `משיח` | DAN 9:26 `מָשִׁ֖יחַ` | 1 | EZK 47:17 -> DAN 9:26 -> AMO 5:14 | 4 rows @ width 14679 | language-matched controls also produce exact-center rows; treat as background-rate warning | וְאַחֲרֵ֤י הַשָּׁבֻעִים֙ שִׁשִּׁ֣ים וּשְׁנַ֔יִם יִכָּרֵ֥ת [מָשִׁ֖יחַ] וְאֵ֣ין ל֑וֹ וְהָעִ֨יר וְהַ... |
| 31 | LXX | `ιησουσ` | JOS 5:4 `Ἰησοῦς·` | 1 | JOS 17:17 -> JOS 5:4 -> DEU 27:19 | 6 rows @ width 15049 | available language-matched control summary has zero exact-center rows for this normalized term | ἐξ Αἰγύπτου, πάντας τούτους περιέτεμεν [Ἰησοῦς·] |
| 32 | LXX | `ιησουσ` | JOS 13:1 `Ἰησοῦς` | 1 | JDG 6:37 -> JOS 13:1 -> DEU 28:27 | 6 rows @ width 23629 | available language-matched control summary has zero exact-center rows for this normalized term | ΚΑΙ [Ἰησοῦς] πρεσβύτερος προβεβηκὼς τῶν ἡμερῶν. καὶ |
| 33 | LXX | `ιησουσ` | NUM 14:6 `Ἰησοῦς` | 1 | DEU 4:40 -> NUM 14:6 -> LEV 15:11 | 6 rows @ width 37005 | available language-matched control summary has zero exact-center rows for this normalized term | [Ἰησοῦς] δὲ ὁ τοῦ Ναυὴ καὶ |
| 34 | LXX | `ιησουσ` | JOS 9:2 `Ἰησοῦς` | 1 | DEU 9:26 -> JOS 9:2 -> JDG 13:9 | 6 rows @ width 38593 | available language-matched control summary has zero exact-center rows for this normalized term | θυσίαν σωτηρίου. 2γ καὶ ἔγραψεν [Ἰησοῦς] ἐπὶ τῶν λίθων τὸ δευτερονόμιον, |
| 35 | LXX | `ιησουσ` | DEU 1:38 `Ἰησοῦς` | 1 | JOS 1:12 -> DEU 1:38 -> NUM 6:5 | 6 rows @ width 42091 | available language-matched control summary has zero exact-center rows for this normalized term | [Ἰησοῦς] υἱὸς Ναυὴ ὁ παρεστηκώς σοι, |
| 36 | LXX | `ιησουσ` | 1MA 2:55 `Ἰησοῦς` | 1 | SIR 20:9 -> 1MA 2:55 -> 2MA 10:18 | 6 rows @ width 43876 | available language-matched control summary has zero exact-center rows for this normalized term | [Ἰησοῦς] ἐν τῷ πληρῶσαι λόγον ἐγένετο |
| 37 | LXX | `ιησουσ` | JOS 4:9 `Ἰησοῦς` | 1 | JDG 15:13 -> JOS 4:9 -> NUM 36:11 | 6 rows @ width 46472 | available language-matched control summary has zero exact-center rows for this normalized term | ἔστησε δὲ [Ἰησοῦς] καὶ ἄλλους δώδεκα λίθους ἐν |
| 38 | LXX | `ιησουσ` | JOS 5:13 `Ἰησοῦς` | 1 | NUM 32:39 -> JOS 5:13 -> JDG 20:28 | 6 rows @ width 52297 | available language-matched control summary has zero exact-center rows for this normalized term | τῇ χειρὶ αὐτοῦ. καὶ προσελθὼν [Ἰησοῦς] εἶπεν αὐτῷ· ἡμέτερος εἶ ἢ |
| 39 | LXX | `ιησουσ` | HAG 1:12 `Ἰησοῦς` | 1 | ESG 8:12υ -> HAG 1:12 -> EZK 33:19 | 6 rows @ width 52761 | available language-matched control summary has zero exact-center rows for this normalized term | Σαλαθιὴλ ἐκ φυλῆς Ἰούδα καὶ [Ἰησοῦς] ὁ τοῦ Ἰωσεδὲκ ὁ ἱερεὺς |
| 40 | LXX | `ιησουσ` | JOS 8:18 `Ἰησοῦς` | 1 | RUT 3:4 -> JOS 8:18 -> NUM 34:16 | 6 rows @ width 53401 | available language-matched control summary has zero exact-center rows for this normalized term | τοῦ τόπου αὐτῶν. καὶ ἐξέτεινεν [Ἰησοῦς] τὴν χεῖρα αὐτοῦ, τὸν γαισόν, |
| 41 | LXX | `ιησουσ` | JOS 24:1 `Ἰησοῦς` | 1 | DEU 10:8 -> JOS 24:1 -> 1SA 17:17 | 6 rows @ width 56542 | available language-matched control summary has zero exact-center rows for this normalized term | ΚΑΙ συνήγαγεν [Ἰησοῦς] πάσας φυλὰς Ἰσραὴλ εἰς Σηλὼ |
| 42 | LXX | `ιησουσ` | JOS 22:6 `Ἰησοῦς` | 1 | 1SA 29:10 -> JOS 22:6 -> NUM 31:2 | 6 rows @ width 75945 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ εὐλόγησεν αὐτοὺς [Ἰησοῦς] καὶ ἐξαπέστειλεν αὐτούς, καὶ ἐπορεύθησαν |
| 43 | LXX | `ιησουσ` | JOS 10:31 `Ἰησοῦς` | 1 | NUM 20:12 -> JOS 10:31 -> 1SA 19:20 | 6 rows @ width 76119 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ἀπῆλθεν [Ἰησοῦς] καὶ πᾶς Ἰσραὴλ μετ' αὐτοῦ |
| 44 | LXX | `ιησουσ` | JDG 2:6 `Ἰησοῦς` | 1 | 2SA 6:23 -> JDG 2:6 -> NUM 32:42 | 6 rows @ width 78931 | available language-matched control summary has zero exact-center rows for this normalized term | Καὶ ἐξαπέστειλεν [Ἰησοῦς] τὸν λαόν, καὶ ἦλθεν ἀνὴρ |
| 45 | LXX | `ιησουσ` | JOS 7:7 `Ἰησοῦς·` | 1 | NUM 14:3 -> JOS 7:7 -> 1SA 17:56 | 6 rows @ width 79498 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ εἶπεν [Ἰησοῦς·] δέομαι Κύριε· ἱνατί διεβίβασεν ὁ |
| 46 | LXX | `ιησουσ` | DEU 32:44 `Ἰησοῦς` | 1 | NUM 4:29 -> DEU 32:44 -> 1SA 16:11 | 6 rows @ width 84272 | available language-matched control summary has zero exact-center rows for this normalized term | ὦτα τοῦ λαοῦ, αὐτὸς καὶ [Ἰησοῦς] ὁ τοῦ Ναυή. |
| 47 | LXX | `ιησουσ` | JOS 8:9 `Ἰησοῦς,` | 1 | 1SA 25:13 -> JOS 8:9 -> NUM 7:88 | 6 rows @ width 87562 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ἀπέστειλεν αὐτοὺς [Ἰησοῦς,] καὶ ἐπορεύθησαν εἰς τὴν ἐνέδραν |
| 48 | LXX | `ιησουσ` | JOS 9:32 `Ἰησοῦς` | 1 | 1SA 28:7 -> JOS 9:32 -> NUM 8:25 | 6 rows @ width 88930 | available language-matched control summary has zero exact-center rows for this normalized term | αὐτοῖς οὕτως· καὶ ἐξείλατο αὐτοὺς [Ἰησοῦς] ἐν τῇ ἡμέρᾳ ἐκείνῃ ἐκ |
| 49 | LXX | `ιησουσ` | JOS 17:17 `Ἰησοῦς` | 1 | NUM 15:10 -> JOS 17:17 -> 2SA 6:12 | 6 rows @ width 90387 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ εἶπεν [Ἰησοῦς] τοῖς υἱοῖς Ἰωσήφ· εἰ λαὸς |
| 50 | LXX | `ιησουσ` | JOS 10:34 `Ἰησοῦς` | 1 | NUM 7:49 -> JOS 10:34 -> 2SA 2:28 | 6 rows @ width 93150 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ἀπῆλθεν [Ἰησοῦς] καὶ πᾶς Ἰσραὴλ μετ' αὐτοῦ |
| 51 | LXX | `ιησουσ` | JOS 10:7 `Ἰησοῦς` | 1 | NUM 4:12 -> JOS 10:7 -> 2SA 5:3 | 6 rows @ width 97524 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ἀνέβη [Ἰησοῦς] ἐκ Γαλγάλων, αὐτὸς καὶ πᾶς |
| 52 | LXX | `ιησουσ` | JOS 7:25 `Ἰησοῦς` | 1 | LEV 23:31 -> JOS 7:25 -> 2SA 10:13 | 6 rows @ width 106560 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ εἶπεν [Ἰησοῦς] τῷ Ἄχαρ· τί ὠλόθρευσας ἡμᾶς; |
| 53 | LXX | `ιησουσ` | JOS 7:19 `Ἰησοῦς` | 1 | LEV 19:5 -> JOS 7:19 -> 2SA 13:32 | 6 rows @ width 112033 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ εἶπεν [Ἰησοῦς] τῷ Ἄχαρ· δὸς δόξαν σήμερον |
| 54 | LXX | `ιησουσ` | JOS 22:34 `Ἰησοῦς` | 1 | LEV 27:26 -> JOS 22:34 -> 1KI 5:23 | 6 rows @ width 119233 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ἐπωνόμασεν [Ἰησοῦς] τὸν βωμὸν τῶν Ρουβὴν καὶ |
| 55 | LXX | `ιησουσ` | JOS 18:10 `Ἰησοῦς` | 1 | 1KI 2:22 -> JOS 18:10 -> LEV 22:32 | 6 rows @ width 120348 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ἐνέβαλεν αὐτοῖς [Ἰησοῦς] κλῆρον ἐν Σηλὼ ἔναντι Κυρίου. |
| 56 | LXX | `ιησουσ` | JOS 11:15 `Ἰησοῦς·` | 1 | LEV 14:51 -> JOS 11:15 -> 1KI 1:9 | 6 rows @ width 123910 | available language-matched control summary has zero exact-center rows for this normalized term | τῷ Ἰησοῖ, καὶ οὕτως ἐποίησεν [Ἰησοῦς·] οὐ παρέβη οὐδὲν ἀπὸ πάντων, |
| 57 | LXX | `ιησουσ` | SIR 46:1 `Ἰησοῦς` | 1 | DAG 7:7 -> SIR 46:1 -> AMO 1:6 | 6 rows @ width 125885 | available language-matched control summary has zero exact-center rows for this normalized term | ΚΡΑΤΑΙΟΣ ἐν πολέμοις [Ἰησοῦς] Ναυῆ καὶ διάδοχος Μωυσῆ ἐν |
| 58 | LXX | `ιησουσ` | JOS 6:12 `Ἰησοῦς` | 1 | 2SA 20:21 -> JOS 6:12 -> LEV 8:16 | 6 rows @ width 126013 | available language-matched control summary has zero exact-center rows for this normalized term | τῇ ἡμέρᾳ τῇ δευτέρᾳ ἀνέστη [Ἰησοῦς] τὸ πρωΐ, καὶ ᾖραν οἱ |
| 59 | LXX | `ιησουσ` | JOS 9:21 `Ἰησοῦς` | 1 | LEV 5:17 -> JOS 9:21 -> 1KI 3:20 | 6 rows @ width 133965 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ἐποίησεν [Ἰησοῦς] πρὸς αὐτοὺς εἰρήνην καὶ διέθεντο |
| 60 | LXX | `ιησουσ` | JOS 6:10 `Ἰησοῦς` | 1 | 1KI 3:28 -> JOS 6:10 -> EXO 36:13 | 6 rows @ width 138923 | available language-matched control summary has zero exact-center rows for this normalized term | τῷ δὲ λαῷ ἐνετείλατο [Ἰησοῦς] λέγων· μὴ βοᾶτε, μηδὲ ἀκουσάτω |
| 61 | LXX | `ιησουσ` | JOS 7:6 `Ἰησοῦς` | 1 | EXO 30:31 -> JOS 7:6 -> 1KI 9:3 | 6 rows @ width 146855 | available language-matched control summary has zero exact-center rows for this normalized term | τὰ ἱμάτια αὐτοῦ, καὶ ἔπεσεν [Ἰησοῦς] ἐπὶ τὴν γῆν ἐπὶ πρόσωπον |
| 62 | LXX | `ιησουσ` | JOS 9:8 `Ἰησοῦς·` | 1 | 1KI 11:43 -> JOS 9:8 -> EXO 32:10 | 6 rows @ width 148539 | available language-matched control summary has zero exact-center rows for this normalized term | ἐσμεν. καὶ εἶπε πρὸς αὐτοὺς [Ἰησοῦς·] πόθεν ἐστὲ καὶ πόθεν παραγεγόνατε; |
| 63 | LXX | `ιησουσ` | JOS 8:10 `Ἰησοῦς` | 1 | 1KI 16:33 -> JOS 8:10 -> EXO 21:34 | 6 rows @ width 160294 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ὀρθρίσας [Ἰησοῦς] τὸ πρωΐ ἐπεσκέψατο τὸν λαόν· |
| 64 | LXX | `ιησουσ` | JOS 6:26 `Ἰησοῦς` | 1 | 1KI 20:3 -> JOS 6:26 -> EXO 14:17 | 6 rows @ width 166676 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ὥρκισεν [Ἰησοῦς] ἐν τῇ ἡμέρᾳ ἐκείνῃ ἐναντίον |
| 65 | LXX | `ιησουσ` | JOS 23:1 `Ἰησοῦς` | 1 | EXO 21:36 -> JOS 23:1 -> 2KI 19:6 | 6 rows @ width 178920 | available language-matched control summary has zero exact-center rows for this normalized term | τῶν ἐχθρῶν αὐτοῦ κυκλόθεν, καὶ [Ἰησοῦς] πρεσβύτερος προβεβηκὼς ταῖς ἡμέραις, |
| 66 | LXX | `ιησουσ` | JOS 10:18 `Ἰησοῦς·` | 1 | 2KI 10:36 -> JOS 10:18 -> EXO 6:9 | 6 rows @ width 182582 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ εἶπεν [Ἰησοῦς·] κυλίσατε λίθους ἐπὶ τὸ στόμα |
| 67 | LXX | `ιησουσ` | JOS 9:2 `Ἰησοῦς` | 1 | GEN 46:17 -> JOS 9:2 -> 2KI 16:2 | 6 rows @ width 191331 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ μετὰ ταῦτα οὕτως ἀνέγνω [Ἰησοῦς] πάντα τὰ ρήματα τοῦ νόμου |
| 68 | LXX | `ιησουσ` | JOS 10:40 `Ἰησοῦς` | 1 | 2KI 19:26 -> JOS 10:40 -> GEN 47:5 | 6 rows @ width 193890 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ἐπάταξεν [Ἰησοῦς] πᾶσαν τὴν γῆν τῆς ὀρεινῆς |
| 69 | LXX | `ιησουσ` | JOS 3:9 `Ἰησοῦς` | 1 | 2KI 14:23 -> JOS 3:9 -> GEN 38:14 | 6 rows @ width 195762 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ εἶπεν [Ἰησοῦς] τοῖς υἱοῖς Ἰσραήλ· προσαγάγετε ὧδε |
| 70 | LXX | `ιησουσ` | JOS 7:16 `Ἰησοῦς` | 1 | GEN 30:16 -> JOS 7:16 -> 1CH 4:10 | 6 rows @ width 211301 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ὤρθρισεν [Ἰησοῦς] καὶ προσήγαγε τὸν λαὸν κατὰ |
| 71 | LXX | `ιησουσ` | JOS 5:13 `Ἰησοῦς` | 1 | 1CH 2:22 -> JOS 5:13 -> GEN 28:4 | 6 rows @ width 211810 | available language-matched control summary has zero exact-center rows for this normalized term | Καὶ ἐγένετο ὡς ἦν [Ἰησοῦς] ἐν Ἱεριχώ, καὶ ἀναβλέψας τοῖς |
| 72 | LXX | `ιησουσ` | JOS 10:20 `Ἰησοῦς` | 1 | GEN 29:13 -> JOS 10:20 -> 1CH 12:18 | 6 rows @ width 217142 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ ἐγένετο ὡς κατέπαυσεν [Ἰησοῦς] καὶ πᾶς υἱὸς Ἰσραὴλ κόπτοντες |
| 73 | LXX | `ιησουσ` | JOS 10:42 `Ἰησοῦς` | 1 | 2CH 2:2 -> JOS 10:42 -> GEN 16:14 | 6 rows @ width 234932 | available language-matched control summary has zero exact-center rows for this normalized term | καὶ τὴν γῆν αὐτῶν ἐπάταξεν [Ἰησοῦς] εἰσάπαξ, ὅτι Κύριος ὁ Θεὸς |
| 74 | LXX | `ιησουσ` | JOS 11:21 `Ἰησοῦς` | 1 | GEN 12:6 -> JOS 11:21 -> 2CH 6:40 | 6 rows @ width 239516 | available language-matched control summary has zero exact-center rows for this normalized term | Καὶ ἦλθεν [Ἰησοῦς] ἐν τῷ καιρῷ ἐκείνῳ καὶ |
| 75 | LXX | `ιησουσ` | JOS 10:12 `Ἰησοῦς` | 1 | 2CH 12:13 -> JOS 10:12 -> GEN 1:7 | 6 rows @ width 248095 | available language-matched control summary has zero exact-center rows for this normalized term | Τότε ἐλάλησεν [Ἰησοῦς] πρὸς Κύριον, ᾗ ἡμέρᾳ παρέδωκεν |
| 76 | LXX | `ιησουσ` | NEH 9:4 `Ἰησοῦς` | 1 | EZK 34:13 -> NEH 9:4 -> JOS 6:10 | 6 rows @ width 292090 | available language-matched control summary has zero exact-center rows for this normalized term | ἔστη ἐπὶ ἀναβάσει τῶν Λευιτῶν [Ἰησοῦς] καὶ οἱ υἱοὶ Καδμιήλ, Σεχενία |

## Path Detail Sample

| Review | Path | Corpus | Term | Skip | Span | Matrix | Letters |
| ---: | ---: | --- | --- | ---: | --- | --- | --- |
| 1 | 1 | UHB | `ישוע` | -391 | NEH 9:6 -> NEH 8:17 -> NEH 8:9 | rows 1809-1812, col 177 | י@NEH 9:6:מְחַיֶּ֣ה[r1812,c177] \| ש@NEH 9:2:יִשְׂרָאֵ֔ל[r1811,c177] \| ו@NEH 8:15:צְא֣וּ[r1810,c177] \| ע@NEH 8:9:כְּ⁠שָׁמְעָ֖⁠ם[r1809,c177] |
| 1 | 2 | UHB | `ישוע` | 1182 | NEH 7:67 -> NEH 8:17 -> NEH 9:24 | rows 597-600, col 658 | י@NEH 7:67:אֲלָפִ֔ים[r597,c658] \| ש@NEH 8:9:כְּ⁠שָׁמְעָ֖⁠ם[r598,c658] \| ו@NEH 9:6:וּ⁠צְבָ֥א[r599,c658] \| ע@NEH 9:24:וַ⁠תַּכְנַ֨ע[r600,c658] |
| 1 | 3 | UHB | `ישוע` | 2300 | NEH 7:8 -> NEH 8:17 -> NEH 10:28 | rows 306-309, col 833 | י@NEH 7:8:וּ⁠שְׁנָֽיִם׃[r306,c833] \| ש@NEH 8:3:אֲשֶׁ֣ר[r307,c833] \| ו@NEH 9:15:הוֹצֵ֥אתָ[r308,c833] \| ע@NEH 10:28:מֵ⁠עַמֵּ֤י[r309,c833] |
| 1 | 4 | UHB | `ישוע` | 3867 | NEH 5:13 -> NEH 8:17 -> NEH 11:26 | rows 181-184, col 2358 | י@NEH 5:13:לֹֽא־יָקִ֜ים[r181,c2358] \| ש@NEH 7:63:עַל־שְׁמָֽ⁠ם׃[r182,c2358] \| ו@NEH 9:25:וַ⁠יִּֽתְעַדְּנ֖וּ[r183,c2358] \| ע@NEH 11:26:וּ⁠ב... |
| 1 | 5 | UHB | `ישוע` | 22898 | 2CH 33:19 -> NEH 8:17 -> JOB 16:10 | rows 29-32, col 9696 | י@2CH 33:19:לִ⁠פְנֵ֖י[r29,c9696] \| ש@NEH 1:11:מַשְׁקֶ֖ה[r30,c9696] \| ו@EST 1:18:שָֽׁמְעוּ֙[r31,c9696] \| ע@JOB 16:10:עָלַ֨⁠י[r32,c9696] |
| 1 | 6 | UHB | `ישוע` | -24146 | JOB 19:18 -> NEH 8:17 -> 2CH 32:25 | rows 27-30, col 19922 | י@JOB 19:18:וַ⁠יְדַבְּרוּ־בִֽ⁠י׃[r30,c19922] \| ש@EST 2:4:וַ⁠יַּ֥עַשׂ[r29,c19922] \| ו@NEH 1:3:וּ⁠שְׁעָרֶ֖י⁠הָ[r28,c19922] \| ע@2CH 32:25:עָ... |
| 1 | 7 | UHB | `ישוע` | 24390 | 2CH 32:19 -> NEH 8:17 -> JOB 20:2 | rows 27-30, col 12970 | י@2CH 32:19:עַמֵּ֣י[r27,c12970] \| ש@NEH 1:2:וַ⁠אֲנָשִׁ֖ים[r28,c12970] \| ו@EST 2:7:וַ⁠יְהִ֨י[r29,c12970] \| ע@JOB 20:2:שְׂעִפַּ֣⁠י[r30,c12970] |
| 1 | 8 | UHB | `ישוע` | -25240 | JOB 21:18 -> NEH 8:17 -> 2CH 32:1 | rows 26-29, col 13984 | י@JOB 21:18:יִהְי֗וּ[r29,c13984] \| ש@EST 2:12:אֲחַשְׁוֵר֗וֹשׁ[r28,c13984] \| ו@EZR 10:29:יָשׁ֖וּב[r27,c13984] \| ע@2CH 32:1:עַל־הֶ⁠עָרִ֣ים[... |
| 1 | 9 | UHB | `ישוע` | -26675 | JOB 24:14 -> NEH 8:17 -> 2CH 30:20 | rows 25-28, col 1198 | י@JOB 24:14:יִֽקְטָל־עָנִ֥י[r28,c1198] \| ש@EST 2:21:שְׁנֵֽי־סָרִיסֵ֤י[r27,c1198] \| ו@EZR 10:14:וָ⁠עִ֖יר[r26,c1198] \| ע@2CH 30:20:אֶת־הָ⁠ע... |
| 1 | 10 | UHB | `ישוע` | -30134 | JOB 32:3 -> NEH 8:17 -> 2CH 28:6 | rows 21-24, col 30070 | י@JOB 32:3:וַ֝⁠יַּרְשִׁ֗יעוּ[r24,c30070] \| ש@EST 4:6:אֲשֶׁ֖ר[r23,c30070] \| ו@EZR 9:7:וּ⁠בַ⁠עֲוֺנֹתֵ֡י⁠נוּ[r22,c30070] \| ע@2CH 28:6:וְ⁠עֶש... |
| 1 | 11 | UHB | `ישוע` | 31724 | 2CH 26:1 -> NEH 8:17 -> JOB 34:29 | rows 20-23, col 26017 | י@2CH 26:1:וַ⁠יִּקְח֞וּ[r20,c26017] \| ש@EZR 8:33:נִשְׁקַ֣ל[r21,c26017] \| ו@EST 5:1:וְ֠⁠הַ⁠מֶּלֶךְ[r22,c26017] \| ע@JOB 34:29:וְ⁠עַל־אָדָ֣ם... |
| 1 | 12 | UHB | `ישוע` | 36977 | 2CH 20:35 -> NEH 8:17 -> PSA 5:2 | rows 17-20, col 24009 | י@2CH 20:35:מֶֽלֶךְ־יִשְׂרָאֵ֑ל[r17,c24009] \| ש@EZR 7:16:בִ⁠ירוּשְׁלֶֽם׃[r18,c24009] \| ו@EST 7:10:וַ⁠יִּתְלוּ֙[r19,c24009] \| ע@PSA 5:2:שׁ... |
| 1 | 13 | UHB | `ישוע` | 38439 | 2CH 20:2 -> NEH 8:17 -> PSA 10:2 | rows 16-19, col 35403 | י@2CH 20:2:וַ⁠יַּגִּ֤ידוּ[r16,c35403] \| ש@EZR 7:5:בֶּן־אֲבִישׁ֗וּעַ[r17,c35403] \| ו@EST 8:9:וְ⁠עֶשְׂרִים֮[r18,c35403] \| ע@PSA 10:2:עָנִ֑י... |
| 1 | 14 | UHB | `ישוע` | -42699 | PSA 22:31 -> NEH 8:17 -> 2CH 14:11 | rows 15-18, col 3552 | י@PSA 22:31:יָ֭בֹאוּ[r18,c3552] \| ש@EST 9:21:וְ⁠שָׁנָֽה׃[r17,c3552] \| ו@EZR 5:13:לְ⁠כ֥וֹרֶשׁ[r16,c3552] \| ע@2CH 14:11:אֵֽין־עִמְּ⁠ךָ֤[r15... |
| 1 | 15 | UHB | `ישוע` | -42994 | PSA 24:7 -> NEH 8:17 -> 2CH 14:4 | rows 14-17, col 41675 | י@PSA 24:7:שְׁעָרִ֨ים[r17,c41675] \| ש@EST 9:23:לַ⁠עֲשׂ֑וֹת[r16,c41675] \| ו@EZR 5:11:וְ⁠אַרְעָ֗⁠א[r15,c41675] \| ע@2CH 14:4:וְ⁠לַ⁠עֲשׂ֖וֹת[... |
| 1 | 16 | UHB | `ישוע` | 43305 | 2CH 13:17 -> NEH 8:17 -> PSA 25:11 | rows 14-17, col 36856 | י@2CH 13:17:אִ֥ישׁ[r14,c36856] \| ש@EZR 5:9:שְׁאֵ֨לְנָא֙[r15,c36856] \| ו@EST 9:25:אֹת֛⁠וֹ[r16,c36856] \| ע@PSA 25:11:לְמַֽעַן־שִׁמְ⁠ךָ֥[r17... |
| 1 | 17 | UHB | `ישוע` | -46293 | PSA 34:8 -> NEH 8:17 -> 2CH 10:3 | rows 13-16, col 36834 | י@PSA 34:8:אַֽשְׁרֵ֥י[r16,c36834] \| ש@JOB 1:13:וְ⁠שֹׁתִ֣ים[r15,c36834] \| ו@EZR 4:12:סְלִ֨קוּ֙[r14,c36834] \| ע@2CH 10:3:אֶל־רְחַבְעָ֖ם[r13... |
| 1 | 18 | UHB | `ישוע` | 50038 | 2CH 6:32 -> NEH 8:17 -> PSA 42:9 | rows 12-15, col 32571 | י@2CH 6:32:יִשְׂרָאֵל֮[r12,c32571] \| ש@EZR 3:1:הַ⁠חֹ֣דֶשׁ[r13,c32571] \| ו@JOB 3:17:יָ֝נ֗וּחוּ[r14,c32571] \| ע@PSA 42:9:סַלְעִ⁠י֮[r15,c32571] |
| 1 | 19 | UHB | `ישוע` | -71942 | PSA 104:18 -> NEH 8:17 -> 1CH 12:13 | rows 8-11, col 24633 | י@PSA 104:18:סְ֝לָעִ֗ים[r11,c24633] \| ש@JOB 19:9:רֹאשִֽׁ⁠י׃[r10,c24633] \| ו@2CH 32:29:וְ⁠עָרִים֙[r9,c24633] \| ע@1CH 12:13:עָשָֽׂר׃[r8,c24... |
| 1 | 20 | UHB | `ישוע` | 80924 | 1CH 4:35 -> NEH 8:17 -> PSA 121:1 | rows 7-10, col 20229 | י@1CH 4:35:בֶּן־י֣וֹשִׁבְיָ֔ה[r7,c20229] \| ש@2CH 30:13:לַ⁠עֲשׂ֛וֹת[r8,c20229] \| ו@JOB 25:3:לֹא־יָק֥וּם[r9,c20229] \| ע@PSA 121:1:עֵ֭ינַ⁠י[... |
| 1 | 21 | UHB | `ישוע` | 83621 | 1CH 2:11 -> NEH 8:17 -> PSA 136:15 | rows 6-9, col 80925 | י@1CH 2:11:הוֹלִ֥יד[r6,c80925] \| ש@2CH 29:29:וַ⁠יִּֽשְׁתַּחֲוֽוּ׃[r7,c80925] \| ו@JOB 28:10:בַּ֭⁠צּוּרוֹת[r8,c80925] \| ע@PSA 136:15:לְ⁠עוֹ... |
| 1 | 22 | UHB | `ישוע` | 87117 | 2KI 24:2 -> NEH 8:17 -> PSA 147:20 | rows 6-9, col 54708 | י@2KI 24:2:כַשְׂדִּים֩[r6,c54708] \| ש@2CH 29:3:הָ⁠רִאשׁוֹנָ֨ה[r7,c54708] \| ו@JOB 30:18:לְבוּשִׁ֑⁠י[r8,c54708] \| ע@PSA 147:20:בַּל־יְדָע֗ו... |
| 1 | 23 | UHB | `ישוע` | 92045 | 2KI 20:1 -> NEH 8:17 -> PRO 8:28 | rows 6-9, col 17745 | י@2KI 20:1:כִּ֛י[r6,c17745] \| ש@2CH 27:1:וְ⁠חָמֵ֤שׁ[r7,c17745] \| ו@JOB 33:8:וְ⁠ק֖וֹל[r8,c17745] \| ע@PRO 8:28:מִ⁠מָּ֑עַל[r9,c17745] |
| 1 | 24 | UHB | `ישוע` | 92046 | 2KI 20:1 -> NEH 8:17 -> PRO 8:28 | rows 6-9, col 17739 | י@2KI 20:1:כִּ֛י[r6,c17739] \| ש@2CH 27:1:שָׁנָה֙[r7,c17739] \| ו@JOB 33:8:וְ⁠ק֖וֹל[r8,c17739] \| ע@PRO 8:28:בַּ֝⁠עֲז֗וֹז[r9,c17739] |
| 1 | 25 | UHB | `ישוע` | 99810 | 2KI 14:24 -> NEH 8:17 -> PRO 22:23 | rows 5-8, col 59317 | י@2KI 14:24:יָרָבְעָ֣ם[r5,c59317] \| ש@2CH 24:24:אֲנָשִׁ֜ים[r6,c59317] \| ו@JOB 38:3:וְ⁠הוֹדִיעֵֽ⁠נִי׃[r7,c59317] \| ע@PRO 22:23:וְ⁠קָבַ֖ע[r... |
| 1 | 26 | UHB | `ישוע` | 102652 | 2KI 12:5 -> NEH 8:17 -> PRO 27:12 | rows 5-8, col 40844 | י@2KI 12:5:יִקְח֤וּ[r5,c40844] \| ש@2CH 24:4:יוֹאָ֔שׁ[r6,c40844] \| ו@JOB 39:13:וְ⁠נֹצָֽה׃[r7,c40844] \| ע@PRO 27:12:נֶעֱנָֽשׁוּ׃[r8,c40844] |
| 1 | 27 | UHB | `ישוע` | -113240 | SNG 2:7 -> NEH 8:17 -> 2KI 4:12 | rows 4-7, col 85264 | י@SNG 2:7:יְרוּשָׁלִַ֨ם֙[r7,c85264] \| ש@PSA 7:15:בְּ⁠שַׁ֣חַת[r6,c85264] \| ו@2CH 20:18:יְהוֹשָׁפָ֛ט[r5,c85264] \| ע@2KI 4:12:וַֽ⁠תַּעֲמֹ֖ד[... |
| 1 | 28 | UHB | `ישוע` | -118566 | ISA 4:2 -> NEH 8:17 -> 1KI 22:10 | rows 4-7, col 55970 | י@ISA 4:2:לִ⁠צְבִ֖י[r7,c55970] \| ש@PSA 15:1:מִֽי־יִ֝שְׁכֹּ֗ן[r6,c55970] \| ו@2CH 18:21:וְ⁠גַם־תּוּכָ֔ל[r5,c55970] \| ע@1KI 22:10:שַׁ֣עַר[r4... |
| 1 | 29 | UHB | `ישוע` | -126558 | ISA 16:7 -> NEH 8:17 -> 1KI 16:19 | rows 4-7, col 12015 | י@ISA 16:7:יְיֵלִ֑יל[r7,c12015] \| ש@PSA 22:7:בְ֝⁠שָׂפָ֗ה[r6,c12015] \| ו@2CH 15:8:אוּלָ֥ם[r5,c12015] \| ע@1KI 16:19:בְּ⁠עֵינֵ֣י[r4,c12015] |
| 1 | 30 | UHB | `ישוע` | -127239 | ISA 17:12 -> NEH 8:17 -> 1KI 16:2 | rows 4-7, col 8268 | י@ISA 17:12:יֶהֱמָי֑וּ⁠ן[r7,c8268] \| ש@PSA 22:18:וְ⁠עַל־לְ֝בוּשִׁ֗⁠י[r6,c8268] \| ו@2CH 15:2:וְ⁠אִֽם־תִּדְרְשֻׁ֨⁠הוּ֙[r5,c8268] \| ע@1KI 16... |
| 1 | 31 | UHB | `ישוע` | -129000 | ISA 21:8 -> NEH 8:17 -> 1KI 14:21 | rows 3-6, col 127584 | י@ISA 21:8:אֲדֹנָ֗⁠י[r6,c127584] \| ש@PSA 24:7:וְֽ֭⁠הִנָּשְׂאוּ[r5,c127584] \| ו@2CH 14:4:אֲבוֹתֵי⁠הֶ֑ם[r4,c127584] \| ע@1KI 14:21:נַעֲמָ֖ה[... |
| 1 | 32 | UHB | `ישוע` | 129449 | 1KI 14:11 -> NEH 8:17 -> ISA 22:6 | rows 3-6, col 125563 | י@1KI 14:11:הַ⁠שָּׁמָ֑יִם[r3,c125563] \| ש@2CH 13:21:עֶשְׂרֵ֖ה[r4,c125563] \| ו@PSA 25:4:יְ֭הוָה[r5,c125563] \| ע@ISA 22:6:וְ⁠עֵילָם֙[r6,c12... |
| 1 | 33 | UHB | `ישוע` | 131146 | 1KI 13:6 -> NEH 8:17 -> ISA 24:19 | rows 3-6, col 117925 | י@1KI 13:6:אֶת־פְּנֵ֣י[r3,c117925] \| ש@2CH 13:9:וַ⁠תַּעֲשׂ֨וּ[r4,c117925] \| ו@PSA 26:11:וַ֭⁠אֲנִי[r5,c117925] \| ע@ISA 24:19:הִֽתְרֹעֲעָ֖ה... |
| 1 | 34 | UHB | `ישוע` | 143947 | 1KI 5:9 -> NEH 8:17 -> ISA 42:2 | rows 3-6, col 60324 | י@1KI 5:9:אֲשִׂימֵ֨⁠ם[r3,c60324] \| ש@2CH 8:13:וְ⁠לֶ֣⁠חֳדָשִׁ֔ים[r4,c60324] \| ו@PSA 37:28:וְ⁠לֹא־יַעֲזֹ֣ב[r5,c60324] \| ע@ISA 42:2:וְ⁠לֹֽא־... |
| 1 | 35 | UHB | `ישוע` | -144722 | ISA 43:1 -> NEH 8:17 -> 1KI 4:24 | rows 3-6, col 56836 | י@ISA 43:1:אַל־תִּירָא֙[r6,c56836] \| ש@PSA 37:40:וְ⁠יוֹשִׁיעֵ֑⁠ם[r5,c56836] \| ו@2CH 8:7:וְ⁠הַ⁠פְּרִזִּי֙[r4,c56836] \| ע@1KI 4:24:וְ⁠עַד־ע... |
| 1 | 36 | UHB | `ישוע` | 157343 | 2SA 19:17 -> NEH 8:17 -> ISA 62:1 | rows 3-6, col 42 | י@2SA 19:17:לִ⁠פְנֵ֥י[r3,c42] \| ש@2CH 4:13:הַ⁠שְּׂבָכ֑וֹת[r4,c42] \| ו@PSA 50:4:וְ⁠אֶל־הָ֝⁠אָ֗רֶץ[r5,c42] \| ע@ISA 62:1:יִבְעָֽר׃[r6,c42] |
| 1 | 37 | UHB | `ישוע` | 159211 | 2SA 18:10 -> NEH 8:17 -> ISA 65:13 | rows 2-5, col 150845 | י@2SA 18:10:לְ⁠יוֹאָ֑ב[r2,c150845] \| ש@2CH 3:16:וַ⁠יַּ֤עַשׂ[r3,c150845] \| ו@PSA 51:12:וְ⁠ר֖וּחַ[r4,c150845] \| ע@ISA 65:13:עֲבָדַ֤⁠י[r5,c1... |
| 1 | 38 | UHB | `ישוע` | 161955 | 2SA 16:1 -> NEH 8:17 -> JER 2:16 | rows 2-5, col 141242 | י@2SA 16:1:חֲמֹרִ֜ים[r2,c141242] \| ש@2CH 2:12:שֵׂ֣כֶל[r3,c141242] \| ו@PSA 55:13:אֱנ֣וֹשׁ[r4,c141242] \| ע@JER 2:16:יִרְע֖וּ⁠ךְ[r5,c141242] |
| 1 | 39 | UHB | `ישוע` | -171409 | JER 11:6 -> NEH 8:17 -> 2SA 7:24 | rows 2-5, col 108153 | י@JER 11:6:הַ⁠בְּרִ֣ית[r5,c108153] \| ש@PSA 66:14:שְׂפָתָ֑⁠י[r4,c108153] \| ו@1CH 28:11:הָ⁠אוּלָם֩[r3,c108153] \| ע@2SA 7:24:עַד־עוֹלָ֑ם[r2,... |
| 1 | 40 | UHB | `ישוע` | 180684 | 1SA 29:9 -> NEH 8:17 -> JER 22:4 | rows 2-5, col 75689 | י@1SA 29:9:אָכִישׁ֮[r2,c75689] \| ש@1CH 25:19:עָשָׂר֙[r3,c75689] \| ו@PSA 73:4:לְ⁠מוֹתָ֗⁠ם[r4,c75689] \| ע@JER 22:4:עַל־כִּסְא֗⁠וֹ[r5,c75689] |
| 1 | 41 | UHB | `ישוע` | 186716 | 1SA 24:2 -> NEH 8:17 -> JER 27:6 | rows 2-5, col 54578 | י@1SA 24:2:וַ⁠יֵּ֗לֶךְ[r2,c54578] \| ש@1CH 23:13:וּ⁠מֹשֶׁ֑ה[r3,c54578] \| ו@PSA 78:8:רוּחֽ⁠וֹ׃[r4,c54578] \| ע@JER 27:6:לְ⁠עָבְדֽ⁠וֹ׃[r5,c54... |
| 1 | 42 | UHB | `ישוע` | 186873 | 1SA 23:26 -> NEH 8:17 -> JER 27:9 | rows 2-5, col 54028 | י@1SA 23:26:עֹֽטְרִ֛ים[r2,c54028] \| ש@1CH 23:11:וִ⁠יע֤וּשׁ[r3,c54028] \| ו@PSA 78:11:וְ֝⁠נִפְלְאוֹתָ֗י⁠ו[r4,c54028] \| ע@JER 27:9:וְ⁠אֶל־עֹ... |
| 1 | 43 | UHB | `ישוע` | -187066 | JER 27:13 -> NEH 8:17 -> 1SA 23:23 | rows 2-5, col 53351 | י@JER 27:13:אֶל־הַ⁠גּ֕וֹי[r5,c53351] \| ש@PSA 78:14:אֵֽשׁ׃[r4,c53351] \| ו@1CH 23:9:שלמות[r3,c53351] \| ע@1SA 23:23:וּ⁠דְע֗וּ[r2,c53351] |
| 1 | 44 | UHB | `ישוע` | 190804 | 1SA 20:13 -> NEH 8:17 -> JER 31:7 | rows 2-5, col 40270 | י@1SA 20:13:יֹסִ֗יף[r2,c40270] \| ש@1CH 21:24:לֹא־אֶשָּׂ֤א[r3,c40270] \| ו@PSA 79:3:קוֹבֵֽר׃[r4,c40270] \| ע@JER 31:7:אֶֽת־עַמְּ⁠ךָ֔[r5,c40270] |
| 1 | 45 | UHB | `ישוע` | 192127 | 1SA 19:6 -> NEH 8:17 -> JER 31:39 | rows 2-5, col 35638 | י@1SA 19:6:אִם־יוּמָֽת׃[r2,c35638] \| ש@1CH 21:15:הַ⁠מַּשְׁחִית֙[r3,c35638] \| ו@PSA 80:8:גּ֝וֹיִ֗ם[r4,c35638] \| ע@JER 31:39:גִּבְעַ֣ת[r5,c... |
| 1 | 46 | UHB | `ישוע` | 192692 | 1SA 18:23 -> NEH 8:17 -> JER 32:12 | rows 2-5, col 33661 | י@1SA 18:23:בְ⁠עֵֽינֵי⁠כֶם֙[r2,c33661] \| ש@1CH 21:12:שָׁנִ֜ים[r3,c33661] \| ו@PSA 80:19:יְה֘וָ֤ה[r4,c33661] \| ע@JER 32:12:לְ⁠עֵינֵי֙[r5,c3... |
| 1 | 47 | UHB | `ישוע` | -194322 | JER 33:6 -> NEH 8:17 -> 1SA 17:40 | rows 2-5, col 27958 | י@JER 33:6:הִנְ⁠נִ֧י[r5,c27958] \| ש@PSA 83:2:רֹֽאשׁ׃[r4,c27958] \| ו@1CH 20:5:וַ⁠תְּהִי־ע֥וֹד[r3,c27958] \| ע@1SA 17:40:הָ⁠רֹעִ֧ים[r2,c27958] |
| 1 | 48 | UHB | `ישוע` | -199914 | JER 38:4 -> NEH 8:17 -> 1SA 14:13 | rows 2-5, col 8386 | י@JER 38:4:י֣וּמַת[r5,c8386] \| ש@PSA 89:7:בְּ⁠סוֹד־קְדֹשִׁ֣ים[r4,c8386] \| ו@1CH 17:24:צְבָאוֹת֙[r3,c8386] \| ע@1SA 14:13:עַל־יָדָי⁠ו֙[r2,c... |
| 1 | 49 | UHB | `ישוע` | -206945 | JER 44:26 -> NEH 8:17 -> 1SA 7:4 | rows 1-4, col 190722 | י@JER 44:26:בִּ⁠שְׁמִ֤⁠י[r4,c190722] \| ש@PSA 94:21:עַל־נֶ֣פֶשׁ[r3,c190722] \| ו@1CH 15:24:בַּ⁠חֲצֹ֣צְר֔וֹת[r2,c190722] \| ע@1SA 7:4:אֶת־הַ⁠... |
| 1 | 50 | UHB | `ישוע` | -210431 | JER 49:4 -> NEH 8:17 -> 1SA 3:5 | rows 1-4, col 182006 | י@JER 49:4:מִ֖י[r4,c182006] \| ש@PSA 99:5:קָד֥וֹשׁ[r3,c182006] \| ו@1CH 14:8:דָּוִ֤יד[r2,c182006] \| ע@1SA 3:5:אֶל־עֵלִ֗י[r1,c182006] |
| 1 | 51 | UHB | `ישוע` | -221971 | EZK 1:19 -> NEH 8:17 -> JDG 18:2 | rows 1-4, col 153155 | י@EZK 1:19:יִנָּשְׂא֖וּ[r4,c153155] \| ש@PSA 106:47:לְ⁠שֵׁ֣ם[r3,c153155] \| ו@1CH 10:7:וַ⁠יֵּשְׁב֖וּ[r2,c153155] \| ע@JDG 18:2:עַד־בֵּ֣ית[r1... |
| 1 | 52 | UHB | `ישוע` | -225887 | EZK 7:2 -> NEH 8:17 -> JDG 13:25 | rows 1-4, col 143367 | י@EZK 7:2:יְהוִ֛ה[r4,c143367] \| ש@PSA 109:11:לְ⁠כָל־אֲשֶׁר־ל֑⁠וֹ[r3,c143367] \| ו@1CH 9:12:בֶּן־פַּשְׁח֖וּר[r2,c143367] \| ע@JDG 13:25:צָרְ... |
| 1 | 53 | UHB | `ישוע` | 233285 | JDG 8:7 -> NEH 8:17 -> EZK 16:4 | rows 1-4, col 124871 | י@JDG 8:7:בְּ⁠יָדִ֑⁠י[r1,c124871] \| ש@1CH 6:79:וְ⁠אֶת־מִגְרָשֶׁ֔י⁠הָ[r2,c124871] \| ו@PSA 118:26:יְהוָֽה׃[r3,c124871] \| ע@EZK 16:4:לְ⁠מִשׁ... |
| 1 | 54 | UHB | `ישוע` | 234127 | JDG 7:15 -> NEH 8:17 -> EZK 16:28 | rows 1-4, col 122766 | י@JDG 7:15:וַ⁠יִּשְׁתָּ֑חוּ[r1,c122766] \| ש@1CH 6:70:לְ⁠מִשְׁפַּ֥חַת[r2,c122766] \| ו@PSA 119:15:וְ֝⁠אַבִּ֗יטָה[r3,c122766] \| ע@EZK 16:28:... |
| 1 | 55 | UHB | `ישוע` | -241155 | EZK 21:29 -> NEH 8:17 -> JDG 1:29 | rows 1-4, col 105196 | י@EZK 21:29:חַֽלְלֵ֣י[r4,c105196] \| ש@PSA 119:153:שָׁכָֽחְתִּי׃[r3,c105196] \| ו@1CH 5:9:עַד־לְ⁠ב֣וֹא[r2,c105196] \| ע@JDG 1:29:הַֽ⁠כְּנַעֲ... |
| 1 | 56 | UHB | `ישוע` | -243332 | EZK 23:30 -> NEH 8:17 -> JOS 24:11 | rows 1-4, col 99754 | י@EZK 23:30:גוֹיִ֔ם[r4,c99754] \| ש@PSA 122:4:שֶׁ⁠שָּׁ֨ם[r3,c99754] \| ו@1CH 4:27:וּ⁠לְ⁠אֶחָ֕י⁠ו[r2,c99754] \| ע@JOS 24:11:וַ⁠תַּעַבְר֣וּ[r1... |
| 1 | 57 | UHB | `ישוע` | -245660 | EZK 26:1 -> NEH 8:17 -> JOS 22:16 | rows 1-4, col 93934 | י@EZK 26:1:וַ⁠יְהִ֛י[r4,c93934] \| ש@PSA 127:5:אֲשֶׁ֤ר[r3,c93934] \| ו@1CH 4:1:וְ⁠שׁוֹבָֽל׃[r2,c93934] \| ע@JOS 22:16:מָֽה־הַ⁠מַּ֤עַל[r1,c93... |
| 1 | 58 | UHB | `ישוע` | 246445 | JOS 21:45 -> NEH 8:17 -> EZK 26:20 | rows 1-4, col 91971 | י@JOS 21:45:יְהוָ֖ה[r1,c91971] \| ש@1CH 3:15:הַ⁠שְּׁלִשִׁי֙[r2,c91971] \| ו@PSA 129:7:וְ⁠חִצְנ֥⁠וֹ[r3,c91971] \| ע@EZK 26:20:מֵֽ⁠עוֹלָם֙[r4,... |
| 1 | 59 | UHB | `ישוע` | -246696 | EZK 27:8 -> NEH 8:17 -> JOS 21:38 | rows 1-4, col 91342 | י@EZK 27:8:יֹשְׁבֵ֤י[r4,c91342] \| ש@PSA 130:3:תִּשְׁמָר־יָ֑הּ[r3,c91342] \| ו@1CH 3:10:בְנ֖⁠וֹ[r2,c91342] \| ע@JOS 21:38:בַּ⁠גִּלְעָ֖ד[r1,c... |
| 1 | 60 | UHB | `ישוע` | -246842 | EZK 27:11 -> NEH 8:17 -> JOS 21:33 | rows 1-4, col 90977 | י@EZK 27:11:סָבִ֔יב[r4,c90977] \| ש@PSA 130:6:מִ⁠שֹּׁמְרִ֥ים[r3,c90977] \| ו@1CH 3:8:וְ⁠אֶלְיָדָ֛ע[r2,c90977] \| ע@JOS 21:33:עִ֖יר[r1,c90977] |
| 1 | 61 | UHB | `ישוע` | 247602 | JOS 21:9 -> NEH 8:17 -> EZK 27:35 | rows 1-4, col 89079 | י@JOS 21:9:בְּנֵ֣י[r1,c89079] \| ש@1CH 2:55:וּ⁠מִשְׁפְּח֤וֹת[r2,c89079] \| ו@PSA 132:7:לְ⁠מִשְׁכְּנוֹתָ֑י⁠ו[r3,c89079] \| ע@EZK 27:35:רָעֲמ֖... |
| 1 | 62 | UHB | `ישוע` | 250542 | JOS 18:8 -> NEH 8:17 -> EZK 31:6 | rows 1-4, col 81729 | י@JOS 18:8:וַ⁠יָּקֻ֥מוּ[r1,c81729] \| ש@1CH 2:16:שְׁלֹשָֽׁה׃[r2,c81729] \| ו@PSA 136:9:חַסְדּֽ⁠וֹ׃[r3,c81729] \| ע@EZK 31:6:בִּ⁠סְעַפֹּתָ֤י⁠... |
| 1 | 63 | UHB | `ישוע` | 250666 | JOS 18:5 -> NEH 8:17 -> EZK 31:9 | rows 1-4, col 81419 | י@JOS 18:5:וּ⁠בֵ֥ית[r1,c81419] \| ש@1CH 2:14:הַ⁠חֲמִישִֽׁי׃[r2,c81419] \| ו@PSA 136:12:וּ⁠בִ⁠זְר֣וֹעַ[r3,c81419] \| ע@EZK 31:9:עֲשִׂיתִ֔י⁠ו[... |
| 1 | 64 | UHB | `ישוע` | 262210 | JOS 7:20 -> NEH 8:17 -> EZK 40:47 | rows 1-4, col 52558 | י@JOS 7:20:חָטָ֨אתִי֙[r1,c52558] \| ש@2KI 23:32:אֲשֶׁר־עָשׂ֖וּ[r2,c52558] \| ו@PSA 148:14:עַֽם־קְרֹב֗⁠וֹ[r3,c52558] \| ע@EZK 40:47:מְרֻבָּ֑ע... |
| 1 | 65 | UHB | `ישוע` | 263135 | JOS 7:1 -> NEH 8:17 -> EZK 41:21 | rows 1-4, col 50245 | י@JOS 7:1:בְנֵֽי־יִשְׂרָאֵ֛ל[r1,c50245] \| ש@2KI 23:26:אֲשֶׁר־חָרָ֥ה[r2,c50245] \| ו@PRO 1:1:בֶן־דָּוִ֑ד[r3,c50245] \| ע@EZK 41:21:רְבֻעָ֑ה[... |
| 1 | 66 | UHB | `ישוע` | 265748 | JOS 4:9 -> NEH 8:17 -> EZK 44:11 | rows 1-4, col 43712 | י@JOS 4:9:רַגְלֵ֣י[r1,c43712] \| ש@2KI 23:10:אִ֜ישׁ[r2,c43712] \| ו@PRO 2:14:לַ⁠עֲשׂ֥וֹת[r3,c43712] \| ע@EZK 44:11:יַעַמְד֥וּ[r4,c43712] |
| 1 | 67 | UHB | `ישוע` | 268358 | JOS 1:11 -> NEH 8:17 -> EZK 46:18 | rows 1-4, col 37190 | י@JOS 1:11:יְהוָ֣ה[r1,c37190] \| ש@2KI 22:15:אֲשֶׁר־שָׁלַ֥ח[r2,c37190] \| ו@PRO 4:2:אַֽל־תַּעֲזֹֽבוּ׃[r3,c37190] \| ע@EZK 46:18:הָ⁠עָ֗ם[r4,c... |
| 1 | 68 | UHB | `ישוע` | -276511 | DAN 4:18 -> NEH 8:17 -> DEU 28:34 | rows 1-4, col 16805 | י@DAN 4:18:דִּ֛י[r4,c16805] \| ש@PRO 8:34:לִ⁠שְׁקֹ֣ד[r3,c16805] \| ו@2KI 19:36:וַ⁠יִּסַּ֣ע[r2,c16805] \| ע@DEU 28:34:מְשֻׁגָּ֑ע[r1,c16805] |
| 1 | 69 | UHB | `ישוע` | 277237 | DEU 28:13 -> NEH 8:17 -> DAN 4:33 | rows 1-4, col 14993 | י@DEU 28:13:אָנֹכִ֧י[r1,c14993] \| ש@2KI 19:29:וּ⁠בַ⁠שָּׁנָ֣ה[r2,c14993] \| ו@PRO 9:11:וְ⁠יוֹסִ֥יפוּ[r3,c14993] \| ע@DAN 4:33:שַׂעְרֵ֛⁠הּ[r4... |
| 1 | 70 | UHB | `ישוע` | 284345 | DEU 20:1 -> NEH 8:17 -> DAN 10:6 | rows 0-3, col 281567 | י@DEU 20:1:מִצְרָֽיִם׃[r0,c281567] \| ש@2KI 18:13:וַֽ⁠יִּתְפְּשֵֽׂ⁠ם׃[r1,c281567] \| ו@PRO 14:3:וְ⁠שִׂפְתֵ֥י[r2,c281567] \| ע@DAN 10:6:וְ⁠עֵ... |
| 1 | 71 | UHB | `ישוע` | 286739 | DEU 17:3 -> NEH 8:17 -> DAN 12:1 | rows 0-3, col 277974 | י@DEU 17:3:וַ⁠יִּשְׁתַּ֖חוּ[r0,c277974] \| ש@2KI 17:34:יִשְׂרָאֵֽל׃[r1,c277974] \| ו@PRO 15:10:יָמֽוּת׃[r2,c277974] \| ע@DAN 12:1:עַמֶּ⁠ךָ֒[... |
| 1 | 72 | UHB | `ישוע` | -287383 | HOS 1:5 -> NEH 8:17 -> DEU 16:8 | rows 0-3, col 277009 | י@HOS 1:5:בַּ⁠יּ֣וֹם[r3,c277009] \| ש@PRO 15:22:מַ֭חֲשָׁבוֹת[r2,c277009] \| ו@2KI 17:30:בְּנ֔וֹת[r1,c277009] \| ע@DEU 16:8:תַעֲשֶׂ֖ה[r0,c277... |
| 1 | 73 | UHB | `ישוע` | -288655 | HOS 4:1 -> NEH 8:17 -> DEU 14:28 | rows 0-3, col 275103 | י@HOS 4:1:דְבַר־יְהוָ֖ה[r3,c275103] \| ש@PRO 16:11:מִ֭שְׁפָּט[r2,c275103] \| ו@2KI 17:21:יְהוָ֔ה[r1,c275103] \| ע@DEU 14:28:אֶת־כָּל־מַעְשַׂ... |
| 1 | 74 | UHB | `ישוע` | -290507 | HOS 8:2 -> NEH 8:17 -> DEU 12:28 | rows 0-3, col 272325 | י@HOS 8:2:יִשְׂרָאֵֽל׃[r3,c272325] \| ש@PRO 17:9:מְבַקֵּ֣שׁ[r2,c272325] \| ו@2KI 17:8:הַ⁠גּוֹיִ֔ם[r1,c272325] \| ע@DEU 12:28:לְמַעַן֩[r0,c27... |
| 1 | 75 | UHB | `ישוע` | 291338 | DEU 12:8 -> NEH 8:17 -> HOS 9:15 | rows 0-3, col 271077 | י@DEU 12:8:כָּל־הַ⁠יָּשָׁ֥ר[r0,c271077] \| ש@2KI 17:1:בְ⁠שֹׁמְר֛וֹן[r1,c271077] \| ו@PRO 17:23:אָרְח֥וֹת[r2,c271077] \| ע@HOS 9:15:מַֽעַלְלֵ... |
| 1 | 76 | UHB | `ישוע` | 291719 | DEU 11:31 -> NEH 8:17 -> HOS 10:9 | rows 0-3, col 270506 | י@DEU 11:31:וִֽ⁠ישַׁבְתֶּם־בָּֽ⁠הּ׃[r0,c270506] \| ש@2KI 16:18:אֲשֶׁר־בָּנ֣וּ[r1,c270506] \| ו@PRO 18:2:בִּ⁠תְבוּנָ֑ה[r2,c270506] \| ע@HOS 1... |
| 1 | 77 | UHB | `ישוע` | 295050 | DEU 9:3 -> NEH 8:17 -> JOL 2:26 | rows 0-3, col 265507 | י@DEU 9:3:יַשְׁמִידֵ֛⁠ם[r0,c265507] \| ש@2KI 15:30:עֶשְׂרִ֔ים[r1,c265507] \| ו@PRO 20:7:בְּ⁠תֻמּ֣⁠וֹ[r2,c265507] \| ע@JOL 2:26:עִמָּ⁠כֶ֖ם[r3... |
| 1 | 78 | UHB | `ישוע` | -297149 | AMO 2:15 -> NEH 8:17 -> DEU 6:22 | rows 0-3, col 262359 | י@AMO 2:15:יְמַלֵּ֑ט[r3,c262359] \| ש@PRO 21:14:וְ⁠שֹׁ֥חַד[r2,c262359] \| ו@2KI 15:14:וַ⁠יִּמְלֹ֥ךְ[r1,c262359] \| ע@DEU 6:22:בְּ⁠פַרְעֹ֥ה[r... |
| 1 | 79 | UHB | `ישוע` | 298660 | DEU 5:14 -> NEH 8:17 -> AMO 5:12 | rows 0-3, col 260092 | י@DEU 5:14:הַ⁠שְּׁבִיעִ֔י[r0,c260092] \| ש@2KI 15:1:שָׁנָ֔ה[r1,c260092] \| ו@PRO 22:10:מָד֑וֹן[r2,c260092] \| ע@AMO 5:12:וַ⁠עֲצֻמִ֖ים[r3,c26... |
| 1 | 80 | UHB | `ישוע` | -303597 | JON 4:3 -> NEH 8:17 -> DEU 2:4 | rows 0-3, col 252688 | י@JON 4:3:כִּ֛י[r3,c252688] \| ש@PRO 24:30:אִישׁ־עָצֵ֣ל[r2,c252688] \| ו@2KI 13:17:הַ⁠חַלּ֛וֹן[r1,c252688] \| ע@DEU 2:4:בְּנֵי־עֵשָׂ֔ו[r0,c2... |
| 1 | 81 | UHB | `ישוע` | 310138 | NUM 32:17 -> NEH 8:17 -> HAB 2:16 | rows 0-3, col 242878 | י@NUM 32:17:חֻשִׁ֗ים[r0,c242878] \| ש@2KI 11:9:אִ֣ישׁ[r1,c242878] \| ו@PRO 28:21:לֹא־ט֑וֹב[r2,c242878] \| ע@HAB 2:16:שָׂבַ֤עְתָּ[r3,c242878] |
| 1 | 82 | UHB | `ישוע` | 315659 | NUM 27:11 -> NEH 8:17 -> ZEC 2:11 | rows 0-3, col 234594 | י@NUM 27:11:יְהוָ֖ה[r0,c234594] \| ש@2KI 10:5:וַ⁠יִּשְׁלַ֣ח[r1,c234594] \| ו@PRO 31:23:בְּ֝⁠שִׁבְתּ֗⁠וֹ[r2,c234594] \| ע@ZEC 2:11:לְ⁠עָ֑ם[r3... |
| 1 | 83 | UHB | `ישוע` | -317165 | ZEC 6:5 -> NEH 8:17 -> NUM 26:29 | rows 0-3, col 232338 | י@ZEC 6:5:אֵלָ֑⁠י[r3,c232338] \| ש@ECC 1:13:נַעֲשָׂ֖ה[r2,c232338] \| ו@2KI 9:28:וַ⁠יִּקְבְּר֨וּ[r1,c232338] \| ע@NUM 26:29:אֶת־גִּלְעָ֑ד[r0,... |
| 1 | 84 | UHB | `ישוע` | -317785 | ZEC 7:5 -> NEH 8:17 -> NUM 26:7 | rows 0-3, col 231407 | י@ZEC 7:5:צַמְתֻּ֖⁠נִי[r3,c231407] \| ש@ECC 2:1:בְ⁠שִׂמְחָ֖ה[r2,c231407] \| ו@2KI 9:25:וַ⁠יֹּ֗אמֶר[r1,c231407] \| ע@NUM 26:7:וְ⁠אַרְבָּעִים֙... |
| 1 | 85 | UHB | `ישוע` | -322791 | MAL 1:3 -> NEH 8:17 -> NUM 21:7 | rows 0-3, col 223898 | י@MAL 1:3:שָׂנֵ֑אתִי[r3,c223898] \| ש@ECC 4:2:שֶׁ⁠כְּבָ֣ר[r2,c223898] \| ו@2KI 8:15:עַל־פָּנָ֖י⁠ו[r1,c223898] \| ע@NUM 21:7:הָ⁠עָֽם׃[r0,c223... |
| 2 | 1 | UHB | `ישוע` | 3498 | 2CH 34:22 -> EZR 2:2 -> EZR 5:5 | rows 193-196, col 565 | י@2CH 34:22:אֵלֶ֖י⁠הָ[r193,c565] \| ש@2CH 36:11:בִּ⁠ירוּשָׁלִָֽם׃[r194,c565] \| ו@EZR 2:64:רִבּ֔וֹא[r195,c565] \| ע@EZR 5:5:עַד־טַעְמָ֖⁠א[r1... |
| 2 | 2 | UHB | `ישוע` | -7359 | EZR 8:28 -> EZR 2:2 -> 2CH 31:17 | rows 91-94, col 219 | י@EZR 8:28:אֱלֹהֵ֥י[r94,c219] \| ש@EZR 4:7:עַל־ארתחששתא[r93,c219] \| ו@2CH 35:10:וַ⁠יַּֽעַמְד֨וּ[r92,c219] \| ע@2CH 31:17:וּ⁠לְ⁠מָ֑עְלָ⁠ה[r9... |
| 2 | 3 | UHB | `ישוע` | 8567 | 2CH 30:21 -> EZR 2:2 -> EZR 9:15 | rows 77-80, col 8417 | י@2CH 30:21:וַ⁠יַּעֲשׂ֣וּ[r77,c8417] \| ש@2CH 35:1:הָ⁠רִאשֽׁוֹן׃[r78,c8417] \| ו@EZR 4:15:וּֽ⁠מְהַנְזְקַ֤ת[r79,c8417] \| ע@EZR 9:15:עַל־זֹֽא... |
| 2 | 4 | UHB | `ישוע` | -14201 | NEH 5:12 -> EZR 2:2 -> 2CH 25:16 | rows 46-49, col 6377 | י@NEH 5:12:וָֽ⁠אַשְׁבִּיעֵ֔⁠ם[r49,c6377] \| ש@EZR 6:12:בִ⁠ירוּשְׁלֶ֑ם[r48,c6377] \| ו@2CH 33:21:אָמ֣וֹן[r47,c6377] \| ע@2CH 25:16:כִּֽי־יָעַ... |
| 2 | 5 | UHB | `ישוע` | 14815 | 2CH 25:4 -> EZR 2:2 -> NEH 6:5 | rows 44-47, col 6842 | י@2CH 25:4:לֹא־יָמ֣וּתוּ[r44,c6842] \| ש@2CH 33:16:שְׁלָמִ֖ים[r45,c6842] \| ו@EZR 6:17:וְ⁠הַקְרִ֗בוּ[r46,c6842] \| ע@NEH 6:5:פַּ֥עַם[r47,c6842] |
| 2 | 6 | UHB | `ישוע` | 28619 | 2CH 9:23 -> EZR 2:2 -> EST 4:17 | rows 22-25, col 8379 | י@2CH 9:23:מְבַקְשִׁ֖ים[r22,c8379] \| ש@2CH 29:34:יִתְקַדְּשׁ֣וּ[r23,c8379] \| ו@EZR 10:23:וֶ⁠אֱלִיעֶֽזֶר׃[r24,c8379] \| ע@EST 4:17:וַֽ⁠יַּע... |
| 2 | 7 | UHB | `ישוע` | 30436 | 2CH 7:21 -> EZR 2:2 -> EST 7:10 | rows 20-23, col 26550 | י@2CH 7:21:וְ⁠לַ⁠בַּ֥יִת[r20,c26550] \| ש@2CH 29:21:שִׁבְעָה֙[r21,c26550] \| ו@NEH 1:5:וּ⁠לְ⁠שֹׁמְרֵ֥י[r22,c26550] \| ע@EST 7:10:עַל־הָ⁠עֵ֖ץ... |
| 2 | 8 | UHB | `ישוע` | -31392 | EST 8:17 -> EZR 2:2 -> 2CH 7:1 | rows 20-23, col 5998 | י@EST 8:17:וְ⁠י֣וֹם[r23,c5998] \| ש@NEH 1:11:הָ⁠אִ֣ישׁ[r22,c5998] \| ו@2CH 29:15:וַ⁠יִּֽתְקַדְּשׁ֔וּ[r21,c5998] \| ע@2CH 7:1:הָ⁠עֹלָ֖ה[r20,c... |
| 2 | 9 | UHB | `ישוע` | 39540 | 1CH 28:1 -> EZR 2:2 -> JOB 13:19 | rows 15-18, col 28513 | י@1CH 28:1:וְ⁠שָׂרֵ֣י[r15,c28513] \| ש@2CH 26:11:הַ⁠שּׁוֹטֵ֑ר[r16,c28513] \| ו@NEH 4:12:וַ⁠יֹּ֤אמְרוּ[r17,c28513] \| ע@JOB 13:19:עִמָּדִ֑⁠י[... |
| 2 | 10 | UHB | `ישוע` | 44931 | 1CH 22:9 -> EZR 2:2 -> JOB 24:20 | rows 13-16, col 29425 | י@1CH 22:9:יִהְיֶ֣ה[r13,c29425] \| ש@2CH 24:27:עַל־מִדְרַ֖שׁ[r14,c29425] \| ו@NEH 6:8:בוֹדָֽא⁠ם׃[r15,c29425] \| ע@JOB 24:20:כָּ⁠עֵ֣ץ[r16,c29... |
| 2 | 11 | UHB | `ישוע` | -48558 | JOB 32:17 -> EZR 2:2 -> 1CH 17:23 | rows 12-15, col 25391 | י@JOB 32:17:אַף־אֲנִ֣י[r15,c25391] \| ש@NEH 7:31:וּ⁠שְׁנָֽיִם׃[r14,c25391] \| ו@2CH 24:1:בִּֽ⁠ירוּשָׁלִָ֑ם[r13,c25391] \| ע@1CH 17:23:וַ⁠עֲש... |
| 2 | 12 | UHB | `ישוע` | 50410 | 1CH 16:5 -> EZR 2:2 -> JOB 36:8 | rows 12-15, col 389 | י@1CH 16:5:וִֽ⁠יעִיאֵ֗ל[r12,c389] \| ש@2CH 23:10:וְ⁠אִ֣ישׁ[r13,c389] \| ו@NEH 7:63:מִ⁠בְּנ֞וֹת[r14,c389] \| ע@JOB 36:8:בְּ⁠חַבְלֵי־עֹֽנִי׃[r... |
| 2 | 13 | UHB | `ישוע` | -50439 | JOB 36:10 -> EZR 2:2 -> 1CH 16:5 | rows 11-14, col 50436 | י@JOB 36:10:וַ֝⁠יֹּ֗אמֶר[r14,c50436] \| ש@NEH 7:63:אִשָּׁ֔ה[r13,c50436] \| ו@2CH 23:10:וַ⁠יַּעֲמֵ֨ד[r12,c50436] \| ע@1CH 16:5:יְעִיאֵ֡ל[r11,... |
| 2 | 14 | UHB | `ישוע` | 59397 | 1CH 7:5 -> EZR 2:2 -> PSA 19:1 | rows 9-12, col 57257 | י@1CH 7:5:שְׁמוֹנִ֤ים[r9,c57257] \| ש@2CH 20:15:וְ⁠יֹשְׁבֵ֣י[r10,c57257] \| ו@NEH 9:32:וּ⁠לְ⁠כָל־עַמֶּ֑⁠ךָ[r11,c57257] \| ע@PSA 19:1:הָ⁠רָקִ... |
| 2 | 15 | UHB | `ישוע` | -60287 | PSA 22:7 -> EZR 2:2 -> 1CH 6:60 | rows 9-12, col 47912 | י@PSA 22:7:יַפְטִ֥ירוּ[r12,c47912] \| ש@NEH 10:1:הַ⁠תִּרְשָׁ֛תָא[r11,c47912] \| ו@2CH 20:8:וַ⁠יֵּשְׁב֖וּ־בָ֑⁠הּ[r10,c47912] \| ע@1CH 6:60:כּ... |
| 2 | 16 | UHB | `ישוע` | 61150 | 1CH 6:21 -> EZR 2:2 -> PSA 24:9 | rows 9-12, col 38850 | י@1CH 6:21:יוֹאָ֤ח[r9,c38850] \| ש@2CH 19:11:וַ⁠עֲשׂ֔וּ[r10,c38850] \| ו@NEH 10:28:הַ֠⁠לְוִיִּם[r11,c38850] \| ע@PSA 24:9:שְׁעָרִ֨ים[r12,c38... |
| 2 | 17 | UHB | `ישוע` | -80454 | PSA 78:14 -> EZR 2:2 -> 2KI 15:26 | rows 6-9, col 77521 | י@PSA 78:14:וְ⁠כָל־הַ֝⁠לַּ֗יְלָה[r9,c77521] \| ש@EST 2:17:מִ⁠כָּל־הַ⁠נָּשִׁ֔ים[r8,c77521] \| ו@2CH 11:21:וַ⁠יֶּאֱהַ֨ב[r7,c77521] \| ע@2KI 15... |
| 2 | 18 | UHB | `ישוע` | 86770 | 2KI 10:11 -> EZR 2:2 -> PSA 94:4 | rows 6-9, col 30149 | י@2KI 10:11:יֵה֗וּא[r6,c30149] \| ש@2CH 9:15:שֵׁ֤שׁ[r7,c30149] \| ו@EST 5:7:וַ⁠תַּ֥עַן[r8,c30149] \| ע@PSA 94:4:יַבִּ֣יעוּ[r9,c30149] |
| 2 | 19 | UHB | `ישוע` | 87122 | 2KI 10:4 -> EZR 2:2 -> PSA 94:23 | rows 6-9, col 27508 | י@2KI 10:4:וְ⁠אֵ֖יךְ[r6,c27508] \| ש@2CH 9:12:אֲשֶׁר־הֵבִ֣יאָה[r7,c27508] \| ו@EST 5:9:וְ⁠לֹא־זָ֣ע[r8,c27508] \| ע@PSA 94:23:עֲלֵי⁠הֶ֨ם[r9,c... |
| 2 | 20 | UHB | `ישוע` | -89219 | PSA 102:28 -> EZR 2:2 -> 2KI 8:22 | rows 6-9, col 11781 | י@PSA 102:28:יִכּֽוֹן׃[r9,c11781] \| ש@EST 6:10:כַּ⁠אֲשֶׁ֣ר[r8,c11781] \| ו@2CH 8:15:וְ⁠הַ⁠לְוִיִּ֛ם[r7,c11781] \| ע@2KI 8:22:תִּפְשַׁ֥ע[r6,... |
| 2 | 21 | UHB | `ישוע` | -89603 | PSA 103:20 -> EZR 2:2 -> 2KI 8:12 | rows 6-9, col 8904 | י@PSA 103:20:מַלְאָ֫כָ֥י⁠ו[r9,c8904] \| ש@EST 6:13:לְ⁠זֶ֤רֶשׁ[r8,c8904] \| ו@2CH 8:13:שָׁל֥וֹשׁ[r7,c8904] \| ע@2KI 8:12:תְּבַקֵּֽעַ׃[r6,c8904] |
| 2 | 22 | UHB | `ישוע` | 94190 | 2KI 4:38 -> EZR 2:2 -> PSA 111:10 | rows 5-8, col 68688 | י@2KI 4:38:הַ⁠נְּבִיאִ֔ים[r5,c68688] \| ש@2CH 7:1:מֵֽ⁠הַ⁠שָּׁמַ֔יִם[r6,c68688] \| ו@EST 8:17:ט֑וֹב[r7,c68688] \| ע@PSA 111:10:לָ⁠עַֽד׃[r8,c6... |
| 2 | 23 | UHB | `ישוע` | 94373 | 2KI 4:34 -> EZR 2:2 -> PSA 112:10 | rows 5-8, col 67501 | י@2KI 4:34:וַ⁠יַּ֜עַל[r5,c67501] \| ש@2CH 6:41:יִלְבְּשׁ֣וּ[r6,c67501] \| ו@EST 9:1:וְ⁠דָת֖⁠וֹ[r7,c67501] \| ע@PSA 112:10:רָ֘שָׁ֤ע[r8,c67501] |
| 2 | 24 | UHB | `ישוע` | 94896 | 2KI 4:20 -> EZR 2:2 -> PSA 115:11 | rows 5-8, col 64101 | י@2KI 4:20:וַ⁠יְבִיאֵ֖⁠הוּ[r5,c64101] \| ש@2CH 6:37:וְ⁠רָשָֽׁעְנוּ׃[r6,c64101] \| ו@EST 9:4:וְ⁠שָׁמְע֖⁠וֹ[r7,c64101] \| ע@PSA 115:11:עֶזְרָ֖... |
| 2 | 25 | UHB | `ישוע` | 95179 | 2KI 4:11 -> EZR 2:2 -> PSA 116:8 | rows 5-8, col 62260 | י@2KI 4:11:וַ⁠יְהִ֥י[r5,c62260] \| ש@2CH 6:35:מִשְׁפָּטָֽ⁠ם׃[r6,c62260] \| ו@EST 9:7:דַּֽלְפ֖וֹן[r7,c62260] \| ע@PSA 116:8:אֶת־עֵינִ֥⁠י[r8,c... |
| 2 | 26 | UHB | `ישוע` | 96045 | 2KI 3:17 -> EZR 2:2 -> PSA 119:8 | rows 5-8, col 56632 | י@2KI 3:17:וּ⁠מִקְנֵי⁠כֶ֖ם[r5,c56632] \| ש@2CH 6:30:לָ⁠אִישׁ֙[r6,c56632] \| ו@EST 9:15:וַ⁠יַּֽהַרְג֣וּ[r7,c56632] \| ע@PSA 119:8:עַד־מְאֹֽד׃... |
| 2 | 27 | UHB | `ישוע` | 97824 | 2KI 2:1 -> EZR 2:2 -> PSA 119:113 | rows 5-8, col 45067 | י@2KI 2:1:הַ⁠שָּׁמָ֑יִם[r5,c45067] \| ש@2CH 6:18:הַ⁠שָּׁמַ֨יִם֙[r6,c45067] \| ו@EST 9:27:הַ⁠יְּהוּדִים֩[r7,c45067] \| ע@PSA 119:113:סֵעֲפִ֥י... |
| 2 | 28 | UHB | `ישוע` | 99029 | 1KI 22:48 -> EZR 2:2 -> PSA 121:1 | rows 5-8, col 37237 | י@1KI 22:48:יְהוֹשָׁפָ֡ט[r5,c37237] \| ש@2CH 6:10:אֲשֶׁ֣ר[r6,c37237] \| ו@EST 10:3:וְ⁠רָצ֖וּי[r7,c37237] \| ע@PSA 121:1:עֵ֭ינַ⁠י[r8,c37237] |
| 2 | 29 | UHB | `ישוע` | 100595 | 1KI 22:8 -> EZR 2:2 -> PSA 132:5 | rows 5-8, col 27057 | י@1KI 22:8:מֶֽלֶךְ־יִשְׂרָאֵ֣ל[r5,c27057] \| ש@2CH 5:11:לִ⁠שְׁמ֥וֹר[r6,c27057] \| ו@JOB 1:13:וּ⁠בְנֹתָ֤י⁠ו[r7,c27057] \| ע@PSA 132:5:עַד־אֶמ... |
| 2 | 30 | UHB | `ישוע` | 109732 | 1KI 15:22 -> EZR 2:2 -> PRO 8:6 | rows 4-7, col 77400 | י@1KI 15:22:אֵ֣ין[r4,c77400] \| ש@2CH 1:15:בִּ⁠ירוּשָׁלִַ֖ם[r5,c77400] \| ו@JOB 7:7:לֹא־תָשׁ֥וּב[r6,c77400] \| ע@PRO 8:6:שִׁ֭מְעוּ[r7,c77400] |
| 2 | 31 | UHB | `ישוע` | 111822 | 1KI 14:2 -> EZR 2:2 -> PRO 11:30 | rows 4-7, col 65904 | י@1KI 14:2:וְ⁠הִשְׁתַּנִּ֔ית[r4,c65904] \| ש@1CH 29:29:הָ⁠רִאשֹׁנִ֖ים[r5,c65904] \| ו@JOB 8:22:אֵינֶֽ⁠נּוּ׃[r6,c65904] \| ע@PRO 11:30:עֵ֣ץ[r... |
| 2 | 32 | UHB | `ישוע` | 116393 | 1KI 11:6 -> EZR 2:2 -> PRO 20:4 | rows 4-7, col 40763 | י@1KI 11:6:יְהוָ֑ה[r4,c40763] \| ש@1CH 28:16:לְ⁠שֻׁלְחֲנ֥וֹת[r5,c40763] \| ו@JOB 12:4:וַֽ⁠יַּעֲנֵ֑⁠הוּ[r6,c40763] \| ע@PRO 20:4:עָצֵ֣ל[r7,c4... |
| 2 | 33 | UHB | `ישוע` | -119811 | PRO 25:20 -> EZR 2:2 -> 1KI 8:49 | rows 4-7, col 21966 | י@PRO 25:20:בַּ֝⁠שִּׁרִ֗ים[r7,c21966] \| ש@JOB 14:12:שָׁ֭מַיִם[r6,c21966] \| ו@1CH 27:24:וַ⁠יְהִ֥י[r5,c21966] \| ע@1KI 8:49:וְ⁠שָׁמַעְתָּ֤[r... |
| 2 | 34 | UHB | `ישוע` | -120451 | PRO 26:25 -> EZR 2:2 -> 1KI 8:35 | rows 4-7, col 18444 | י@PRO 26:25:כִּ֤י[r7,c18444] \| ש@JOB 14:22:אַךְ־בְּ֭שָׂר⁠וֹ[r6,c18444] \| ו@1CH 27:16:לַ⁠שִּׁ֨מְעוֹנִ֔י[r5,c18444] \| ע@1KI 8:35:תַעֲנֵֽ⁠ם׃... |
| 2 | 35 | UHB | `ישוע` | 125046 | 1KI 6:11 -> EZR 2:2 -> ECC 3:4 | rows 3-6, col 118216 | י@1KI 6:11:וַֽ⁠יְהִי֙[r3,c118216] \| ש@1CH 26:6:הַ⁠מִּמְשָׁלִ֖ים[r4,c118216] \| ו@JOB 18:8:וְ⁠עַל־שְׂ֝בָכָ֗ה[r5,c118216] \| ע@ECC 3:4:עֵ֥ת[r... |

## Read

- This is a manual-review packet, not a claim report.
- Exact-center means the hidden path centers on a matching surface word.
- Hebrew controls show substantial background exact-center pressure for `ישוע` and `משיח` in the Bialik control corpus.
- Greek Herodotus controls currently show zero exact-center rows for `ιησουσ` and `γωγ`, but that does not by itself create a claim.
- A promoted row still needs source/version comparison, surface-frequency checks, controls, and manual passage reading.

