# Strong Full-Span Exact-Center Review Bundle

This report joins exact-center queue rows with readable context, strong
same-skip extension flags, and matrix path counts. The CSV is the working
manual-review bundle.

## Reproduce

```bash
python3 -m scripts.build_dynamic_span_exact_center_review_bundle --queue reports/dynamic_skip_focus/strong_full_span_exact_center_review_queue.csv --context reports/dynamic_skip_focus/strong_full_span_exact_center_context.csv --matrix-dir reports/dynamic_skip_focus/exact_center_matrix --bible-extension-dir reports/dynamic_skip_focus/exact_center_extensions --control-extension-dir reports/dynamic_skip_focus/exact_center_control_extensions --out reports/dynamic_skip_focus/strong_full_span_exact_center_review_bundle.csv --markdown-out docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_REVIEW_BUNDLE.md --manifest-out reports/dynamic_skip_focus/strong_full_span_exact_center_review_bundle.manifest.json --markdown-row-limit 80
```

## Scope

- bundle rows: 537
- rows with strong extension flag: 43
- bundle CSV: `reports/dynamic_skip_focus/strong_full_span_exact_center_review_bundle.csv`

## Top Bundle Rows

| Rank | Priority | Corpus | Term | Center | Paths | Strong ext rows | Best extension | Matrix paths | Context |
| ---: | --- | --- | --- | --- | ---: | ---: | --- | ---: | --- |
| 32 | bible_exact_center_with_strong_extension | KJV | `jesus` | MAT 2:1 | 3 | 1 | jesusthe | 3 | Now when [Jesus] was born in Bethlehem of |
| 49 | bible_exact_center_with_strong_extension | KJV | `jesus` | ACT 9:29 | 2 | 1 | jesusand | 2 | the name of the Lord [Jesus,] and disputed against the Grecians: |
| 87 | bible_exact_center_with_strong_extension | KJV | `jesus` | JHN 19:40 | 2 | 1 | jesusyet | 2 | took they the body of [Jesus,] and wound it in linen |
| 222 | bible_exact_center_with_strong_extension | KJV | `jesus` | PHP 2:5 | 1 | 1 | jesusout | 1 | which was also in Christ [Jesus:] |
| 301 | bible_exact_center_with_strong_extension | KJV | `jesus` | 2CO 1:14 | 1 | 1 | forjesus | 1 | the day of the Lord [Jesus.] |
| 454 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `ישוע` | PBY Bialik | 247 | 1 | אמישועה | 247 | איש כפר סכניא לרפאותו משום [ישוע] בן פנטרא, ולא הניח לו |
| 460 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 137 | 1 | אתהמשיח | 137 | ברך ונותן את לבו כלב [משיח] אלהים כל ההפכים האלה חברו |
| 467 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 125 | 1 | למשיחעד | 125 | כ"ד, טז. צביונו רצונו להעשות [משיח.] שם כ"ד, טז. שם כ"ד, |
| 468 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 125 | 1 | לשמשיחה | 125 | אחד לר' אבהו: אימתי יבוא [משיח?] אמר לו: לכשיכסה חשך לאותם |
| 469 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 122 | 2 | המשיחבא | 122 | ישב על הקרקע517 וישרק יבוא [משיח,] שנאמר: "אשרקה להם ואקבצם"518. והלא |
| 470 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 120 | 1 | משיחאיש | 120 | שלשה באים בהסח־הדעת2901, ואלו הם: [משיח,] מציאה ועקרב2902 (סנה' צז.). ז |
| 471 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 120 | 1 | יבאמשיח | 120 | ולא אמר שירה לפניך, תעשהו [משיח?] לכך נסתתם.4343 מיד פתחה הארץ |
| 472 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 117 | 2 | משמשיחת | 117 | על פניו ואמר: בודאי זהו [משיח] שעתיד להפיל לי ולכל שרי |
| 473 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 117 | 3 | המשיחעד | 117 | תהלים צ"ה, ז. בן דוד [משיח] בן דוד. תבקשו ממני אות |
| 474 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 116 | 1 | משיחובנ | 116 | שלשה1699 שמעתי. אמר לו: אימתי [משיח] בא? אמר לו: לך אצלו |
| 476 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 116 | 1 | באפמשיח | 116 | ירבו מחלוקות בפירושי הכתובים. קץ [משיח] בדניאל. תרגום מביא לידי משנה |
| 477 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 115 | 3 | ממשיחדש | 115 | אמר לו שבור־מלכא1765 לשמואל: אמרתם [משיח] על חמור בא אשגר1766 לו |
| 479 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 114 | 1 | להממשיח | 114 | וגיהנם וכסא־הכבוד ובית־המקדש ושמו של [משיח] (שם נד.). עו שבעה כמנדים2978 |
| 480 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 114 | 1 | המשיחהמ | 114 | שירה תחת צדיק זה ועשהו [משיח.] פתחה ואמרה שירה לפניו, שנאמר: |
| 489 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 107 | 1 | כלבמשיח | 107 | בן-ישי ונאם הגבר הקם על, [משיח] אלהי יעקב ונעים זמרות ישראל. |
| 491 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 106 | 1 | דודמשיח | 106 | יודעים לשמע. אמר הקדוש־ברוך־הוא: הריני [משיח] עמהם בלשון מצרי. פתח ואמר |
| 492 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 105 | 1 | לכהמשיח | 105 | את־ישראל, שלשה ימים קדם שיבוא [משיח,] בא אליהו ועומד על הרי |
| 495 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 103 | 1 | משיחעלו | 103 | ויצא; ילק"ש שופטים נא). ז. [משיח] נו "באורך נראה־אור"1843 איזה אור |
| 497 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 101 | 1 | משיחחסר | 101 | אלו באלו צפה לרגלו של [משיח] (ב"ר מב). כו אמר ר' |
| 499 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 100 | 1 | להממשיח | 100 | המשיח, ונופלים על פניהם לפני [משיח] ולפני ישראל ואומרים: נהיה לך |
| 501 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 100 | 1 | המשיחות | 100 | י. בראשית א', י. אפרים [משיח] צדקי לפי האגדה, קודם שיבוא |
| 502 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 99 | 1 | באהמשיח | 99 | מג:). כא אמר אביי: אין [משיח] בא אלא בתשעה־באב, לפי שקבעוהו |
| 504 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 96 | 2 | הממשיחימ | 96 | מה־יעשה אדם וינצל מחבלו של [משיח?] יעסק בתורה ובגמילות־חסדים"; ומר הא |
| 506 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 95 | 1 | המשיחהמ | 95 | ר' הלל אומר: אין להם [משיח] לישראל, שכבר אכלוהו1758 בימי חזקיהו. |
| 507 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 94 | 1 | משיחעלו | 94 | מין לר' אבהו: אימתי יבא [משיח?] אמר לו: כשיכסה החשך את־בני |
| 508 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 93 | 2 | בובמשיח | 93 | שעה אומר לו הקדוש־ברוך־הוא: אפרים [משיח] צדקי, כבר קבלת עליך מששת |
| 511 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 88 | 2 | יבאמשיח | 88 | אומרים לו אבות העולם: אפרים [משיח] צדקנו, תנוח דעתך, שהנחת דעת |
| 512 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 87 | 2 | למשיחאמי | 87 | שמעתי. אמר לו: אימתי יבוא [משיח?] אמר לו: לך שאל אותו. |
| 513 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 86 | 1 | משיחאיש | 86 | עוד אחד נתלוה עמו, והוא [משיח,] ובן לוי לא ראהו. שנים |
| 514 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 83 | 1 | המשיחהמ | 83 | על יד הדרך. אם יבא [משיח] הריני מוכן2442 (ירוש' כלא' פ"ט, |
| 516 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 79 | 1 | המשיחות | 79 | הגיעתך כן, שנאמר: "רוח אפינו [משיח] יי נלכד בשחיתותם"1244. אמר לו |
| 517 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 75 | 1 | משיחהיו | 75 | דיך! מה־טעם? משום שיש־בו קץ [משיח179] (מג/ ג.; ע"י). לו שנו |
| 518 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 72 | 1 | במשיחלא | 72 | כו. מלאתם&nbsp;– שלמותם. בן פרץ&nbsp;– [משיח.] חסר&nbsp;– מעט. שנקנסה&nbsp;– שנגזרה. עמוד |
| 521 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 70 | 1 | למשיחאמי | 70 | (ירמיה י"ז, יב); שמו של [משיח&nbsp;—] "לפני שמש ינון שמו" (תהל' |
| 523 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 66 | 1 | במשיחלא | 66 | שירות ותשבחות לפניך, לא עשיתו [משיח,] חזקיה, שעשית לו כל־הנסים הללו |
| 528 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 51 | 2 | הואהמשיח | 51 | שירה תחת צדיק זה ועשהו [משיח.] פתחה ואמרה שירה לפניו, שנאמר: |
| 529 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 49 | 2 | משיחהיו | 49 | והיא שוקלת כל הרוחות2547 זה [משיח.] "איש על־העדה אשר־יצא לפניהם ואשר |
| 530 | control_exact_center_with_strong_extension | HEB_PBY_BIALIK | `משיח` | PBY Bialik | 39 | 1 | משמשיחת | 39 | ולא אמר שירה לפניך, תעשהו [משיח?] לכך נסתתם. מיד פתחה הארץ |
| 1 | bible_exact_center | UHB | `ישוע` | NEH 8:17 | 85 | 0 |  | 85 | וַ⁠יֵּשְׁב֣וּ בַ⁠סֻּכּוֹת֒ כִּ֣י לֹֽא־עָשׂ֡וּ מִ⁠ימֵי֩ [יֵשׁ֨וּעַ] בִּן־נ֥וּן כֵּן֙ בְּנֵ֣י יִשְׂ... |
| 2 | bible_exact_center | UHB | `ישוע` | EZR 2:2 | 83 | 0 |  | 83 | אֲשֶׁר־בָּ֣אוּ עִם־זְרֻבָּבֶ֗ל [יֵשׁ֡וּעַ] נְ֠חֶמְיָה שְׂרָיָ֨ה רְֽעֵלָיָ֜ה מָרְדֳּכַ֥י בִּלְשָׁ֛ן |
| 3 | bible_exact_center | UHB | `ישוע` | EZR 3:9 | 73 | 0 |  | 73 | וַ⁠יַּעֲמֹ֣ד [יֵשׁ֡וּעַ] בָּנָ֣י⁠ו וְ֠⁠אֶחָי⁠ו קַדְמִיאֵ֨ל וּ⁠בָנָ֤י⁠ו בְּנֵֽי־יְהוּדָה֙ |
| 4 | bible_exact_center | UHB | `ישוע` | EZR 2:6 | 73 | 0 |  | 73 | בְּנֵֽי־פַחַ֥ת מוֹאָ֛ב לִ⁠בְנֵ֥י [יֵשׁ֖וּעַ] יוֹאָ֑ב אַלְפַּ֕יִם שְׁמֹנֶ֥ה מֵא֖וֹת וּ⁠שְׁנֵ֥ים |
| 5 | bible_exact_center | UHB | `ישוע` | NEH 9:5 | 70 | 0 |  | 70 | וַ⁠יֹּאמְר֣וּ הַ⁠לְוִיִּ֡ם [יֵשׁ֣וּעַ] וְ֠⁠קַדְמִיאֵל בָּנִ֨י חֲשַׁבְנְיָ֜ה שֵׁרֵֽבְיָ֤ה הֽוֹדִיָּה֙ |
| 6 | bible_exact_center | UHB | `ישוע` | NEH 12:8 | 69 | 0 |  | 69 | וְ⁠הַ⁠לְוִיִּ֗ם [יֵשׁ֧וּעַ] בִּנּ֛וּי קַדְמִיאֵ֥ל שֵׁרֵבְיָ֖ה יְהוּדָ֣ה מַתַּנְיָ֑ה |
| 7 | bible_exact_center | UHB | `ישוע` | EZR 10:18 | 68 | 0 |  | 68 | אֲשֶׁ֥ר הֹשִׁ֖יבוּ נָשִׁ֣ים נָכְרִיּ֑וֹת מִ⁠בְּנֵ֨י [יֵשׁ֤וּעַ] בֶּן־יֽוֹצָדָק֙ וְ⁠אֶחָ֔י⁠ו מַֽעֲ... |
| 8 | bible_exact_center | UHB | `ישוע` | NEH 7:11 | 67 | 0 |  | 67 | בְּנֵֽי־פַחַ֥ת מוֹאָ֛ב לִ⁠בְנֵ֥י [יֵשׁ֖וּעַ] וְ⁠יוֹאָ֑ב אַלְפַּ֕יִם וּ⁠שְׁמֹנֶ֥ה מֵא֖וֹת שְׁמֹנָ֥ה |
| 9 | bible_exact_center | UHB | `ישוע` | NEH 9:4 | 66 | 0 |  | 66 | וַ⁠יָּ֜קָם עַֽל־מַֽעֲלֵ֣ה הַ⁠לְוִיִּ֗ם [יֵשׁ֨וּעַ] וּ⁠בָנִ֜י קַדְמִיאֵ֧ל שְׁבַנְיָ֛ה בֻּנִּ֥י שֵׁ... |
| 10 | bible_exact_center | UHB | `ישוע` | EZR 2:36 | 63 | 0 |  | 63 | הַֽ⁠כֹּהֲנִ֑ים בְּנֵ֤י יְדַֽעְיָה֙ לְ⁠בֵ֣ית [יֵשׁ֔וּעַ] תְּשַׁ֥ע מֵא֖וֹת שִׁבְעִ֥ים וּ⁠שְׁלֹשָֽׁה׃ |
| 11 | bible_exact_center | UHB | `ישוע` | NEH 12:7 | 59 | 0 |  | 59 | אֵ֣לֶּה רָאשֵׁ֧י הַ⁠כֹּהֲנִ֛ים וַ⁠אֲחֵי⁠הֶ֖ם בִּ⁠ימֵ֥י [יֵשֽׁוּעַ׃] |
| 12 | bible_exact_center | UHB | `ישוע` | NEH 7:39 | 56 | 0 |  | 56 | הַֽ⁠כֹּהֲנִ֑ים בְּנֵ֤י יְדַֽעְיָה֙ לְ⁠בֵ֣ית [יֵשׁ֔וּעַ] תְּשַׁ֥ע מֵא֖וֹת שִׁבְעִ֥ים וּ⁠שְׁלֹשָֽׁה׃ |
| 13 | bible_exact_center | UHB | `ישוע` | NEH 7:7 | 55 | 0 |  | 55 | הַ⁠בָּאִ֣ים עִם־זְרֻבָּבֶ֗ל [יֵשׁ֡וּעַ] נְחֶמְיָ֡ה עֲ֠זַרְיָה רַֽעַמְיָ֨ה נַחֲמָ֜נִי מָרְדֳּכַ֥י |
| 14 | bible_exact_center | UHB | `ישוע` | EZR 3:2 | 54 | 0 |  | 54 | וַ⁠יָּקָם֩ [יֵשׁ֨וּעַ] בֶּן־יֽוֹצָדָ֜ק וְ⁠אֶחָ֣י⁠ו הַ⁠כֹּהֲנִ֗ים וּ⁠זְרֻבָּבֶ֤ל בֶּן־שְׁאַלְתִּיאֵל֙ |
| 15 | bible_exact_center | EBIBLE_WLC | `משיח` | 2SA 1:21 | 33 | 0 |  | 33 | מָגֵ֣ן גִּבּוֹרִ֔ים מָגֵ֣ן שָׁא֔וּל בְּלִ֖י [מָשִׁ֥יחַ] בַּשָּֽׁמֶן׃ |
| 16 | bible_exact_center | EBIBLE_WLC | `משיח` | 2SA 23:1 | 30 | 0 |  | 30 | בֶּן־יִשַׁ֗י וּנְאֻ֤ם הַגֶּ֨בֶר֙ הֻ֣קַם עָ֔ל [מְשִׁ֨יחַ֙] אֱלֹהֵ֣י יַֽעֲקֹ֔ב וּנְעִ֖ים זְמִר֥וֹת... |
| 17 | bible_exact_center | EBIBLE_WLC | `משיח` | LAM 4:20 | 11 | 0 |  | 11 | ר֤וּחַ אַפֵּ֨ינוּ֙ [מְשִׁ֣יחַ] יְהוָ֔ה נִלְכַּ֖ד בִּשְׁחִיתוֹתָ֑ם אֲשֶׁ֣ר אָמַ֔רְנוּ |
| 18 | bible_exact_center | TCG_NT | `γωγ` | REV 20:8 | 4 | 0 |  | 4 | τέσσαρσι γωνίαις τῆς γῆς, τὸν [Γὼγ] καὶ τὸν Μαγώγ, συναγαγεῖν αὐτοὺς |
| 19 | bible_exact_center | KJV | `jesus` | MRK 10:5 | 4 | 0 |  | 4 | And [Jesus] answered and said unto them, |
| 20 | bible_exact_center | KJV | `jesus` | MAT 4:10 | 4 | 0 |  | 4 | Then saith [Jesus] unto him, Get thee hence |
| 21 | bible_exact_center | KJV | `jesus` | MAT 3:13 | 3 | 0 |  | 3 | Then cometh [Jesus] from Galilee to Jordan unto |
| 22 | bible_exact_center | KJV | `jesus` | ACT 18:28 | 3 | 0 |  | 3 | shewing by the scriptures that [Jesus] was Christ. |
| 23 | bible_exact_center | KJV | `jesus` | MAT 12:15 | 3 | 0 |  | 3 | But when [Jesus] knew it he withdrew himself |
| 24 | bible_exact_center | KJV | `jesus` | MAT 26:17 | 3 | 0 |  | 3 | bread the disciples came to [Jesus,] saying unto him, Where wilt |
| 25 | bible_exact_center | KJV | `jesus` | JHN 12:21 | 3 | 0 |  | 3 | saying, Sir, we would see [Jesus.] |
| 26 | bible_exact_center | KJV | `jesus` | MAT 21:24 | 3 | 0 |  | 3 | And [Jesus] answered and said unto them, |
| 27 | bible_exact_center | KJV | `jesus` | MAT 18:1 | 3 | 0 |  | 3 | time came the disciples unto [Jesus,] saying, Who is the greatest |
| 28 | bible_exact_center | KJV | `jesus` | JHN 21:20 | 3 | 0 |  | 3 | about, seeth the disciple whom [Jesus] loved following; which also leaned |
| 29 | bible_exact_center | LXX | `ιησουσ` | JOS 22:7 | 3 | 0 |  | 3 | Βασανίτιδι, καὶ τῷ ἡμίσει ἔδωκεν [Ἰησοῦς] μετὰ τῶν ἀδελφῶν αὐτοῦ ἐν |
| 30 | bible_exact_center | KJV | `jesus` | MAT 20:22 | 3 | 0 |  | 3 | But [Jesus] answered and said, Ye know |
| 31 | bible_exact_center | KJV | `jesus` | LUK 9:42 | 3 | 0 |  | 3 | down, and tare him And [Jesus] rebuked the unclean spirit, and |
| 33 | bible_exact_center | KJV | `jesus` | MAT 20:25 | 3 | 0 |  | 3 | But [Jesus] called them unto him and |
| 34 | bible_exact_center | KJV | `jesus` | MAT 8:34 | 3 | 0 |  | 3 | city came out to meet [Jesus:] and when they saw him, |
| 35 | bible_exact_center | KJV | `jesus` | MRK 5:27 | 3 | 0 |  | 3 | When she had heard of [Jesus,] came in the press behind, |
| 36 | bible_exact_center | LXX | `ιησουσ` | JOS 8:3 | 3 | 0 |  | 3 | ἀναβῆναι εἰς Γαί. ἐπέλεξε δὲ [Ἰησοῦς] τριάκοντα χιλιάδας ἀνδρῶν δυνατοὺς ἐν |
| 37 | bible_exact_center | LXX | `ιησουσ` | JOS 18:3 | 3 | 0 |  | 3 | καὶ εἶπεν [Ἰησοῦς] τοῖς υἱοῖς Ἰσραήλ· ἕως τίνος |
| 38 | bible_exact_center | KJV | `jesus` | LUK 17:17 | 3 | 0 |  | 3 | And [Jesus] answering said, Were there not |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | 457 more rows in CSV |

## Read

- Priority is a queueing label, not a claim label.
- Strong extension flags come from the capped top-extension CSVs.
- Matrix path count equals the exact-center path count for the review unit; use the matrix CSVs for exact path geometry.
- Control rows remain in the bundle because they are the comparison baseline.
