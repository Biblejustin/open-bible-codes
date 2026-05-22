# All-Codes Follow-Up Extensions

Status: same-skip extension audit, not a claim or statistical test.

This report checks whether the hidden ELS path can be extended before,
after, or on both sides at the same skip interval into a surface-attested
word or phrase in that corpus. Hidden-path-only rows are retained; a
same-skip extension is an added review feature, not a requirement.

## Inputs

- Path summary: `reports/all_codes_followup_letter_paths/path_summary.csv`
- Compound extension CSV: `reports/all_codes_followup_extensions/compound_extensions.csv`
- Max before letters: 12
- Max after letters: 12
- Max surface phrase words in lexicon: 4
- Both-sided extensions: True

## Counts

- path rows checked: 310
- selected rows checked: 83
- selected rows with extensions: 69
- extension rows: 692
- selected rows with compound extensions: 13
- compound extension rows containing hidden term: 55
- max extension length: 5
- extension rows by corpus: `{'BYZ_NT': 28, 'EBIBLE_WLC': 103, 'KJV': 35, 'MAM': 109, 'MT_WLC': 116, 'SBLGNT': 26, 'TCG_NT': 28, 'TR_NT': 28, 'UHB': 104, 'UXLC': 115}`
- extension rows by type: `{'after_match': 302, 'before_match': 335, 'before_plus_term': 39, 'term_plus_after': 16}`

## Best Extensions By Selected Row

| Rank | Queue | Bucket | Term | Corpus | Type | Extended sequence | Kind | Count | Examples |
| ---: | --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| 45 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | UXLC | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2` | 6 | עַד־ יְהוָ֣ה; עַד־ יְהוָ֤ה; עֵ֧ד יְהוָ֣ה; עַד־ יְהוָ֔ה; עַ֖ד יְהוָ֣ה |
| 74 | hebrew_theology | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | UXLC | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2` | 6 | עַד־ יְהוָ֣ה; עַד־ יְהוָ֤ה; עֵ֧ד יְהוָ֣ה; עַד־ יְהוָ֔ה; עַ֖ד יְהוָ֣ה |
| 1 | english_screening | `center_word_exact` | `baal` | KJV | `before_plus_term` | `tobaal` | `phrase_2` | 1 | to Baal; |
| 9 | english_screening | `center_verse_exact` | `hand` | KJV | `term_plus_after` | `hando` | `phrase_2` | 5 | hand, O |
| 70 | hebrew_screening | `hidden_path_only` | `יומיהוה` (yom YHWH; English: Day Of The Lord) | UXLC | `before_plus_term` | `היומיהוה` (hayom YHWH; English: the day of YHWH) | `phrase_2` | 3 | הַיּ֔וֹם יְהוָ֖ה; הַיּ֗וֹם יְהוָ֛ה |
| 3 | english_screening | `center_word_exact` | `heth` | KJV | `term_plus_after` | `hethy` | `phrase_2` | 1 | he thy |
| 19 | english_screening | `hidden_path_only` | `heal` | KJV | `before_plus_term` | `iheal` | `phrase_2` | 1 | I heal: |
| 15 | english_screening | `span_exact` | `wine` | KJV | `before_plus_term` | `swine` | `word` | 16 | swine,; swine; swine.; swine: |
| 13 | english_screening | `span_exact` | `thin` | KJV | `term_plus_after` | `thine` | `word` | 937 | thine; thine,; thine.; thine;; thine: |
| 77 | hebrew_theology | `center_word_same_category` | `ברית` (bryt; English: Covenant) | UXLC | `term_plus_after` | `בריתו` (brytw) | `word` | 17 | בְּרִית֔וֹ; בְּרִית֗וֹ; בְּרִית֛וֹ; בְּרִיתֽוֹ׃; בְּרִיתוֹ֙ |
| 80 | hebrew_theology | `center_verse_same_category` | `חכמה` (chkmh; English: Wisdom) | UXLC | `before_plus_term` | `וחכמה` (wchkmh) | `word` | 6 | וְ֝חָכְמָ֗ה; וְחָכְמָ֔ה; וְחָכְמָ֑ה; וְחָכְמָ֥ה; וְחָכְמָֽה׃ |
| 51 | hebrew_screening | `center_word_same_category` | `אמרי` (mry; English: Amorite) | UXLC | `term_plus_after` | `אמריו` (mryw) | `word` | 4 | אֲ֭מָרָיו; אֲ֝מָרָ֗יו; אֲמָרָ֣יו |
| 53 | hebrew_screening | `center_verse_exact` | `אריה` (ryh; English: Lion) | UXLC | `before_plus_term` | `ואריה` (wryh) | `word` | 2 | וְאַרְיֵ֖ה; וְאַרְיֵה֙ |
| 47 | hebrew_screening | `center_word_same_concept` | `רומא` (rwm; English: Rome) | UXLC | `before_match` | `שלומי` (shlwmy) | `word` | 4 | שְׁלוֹמִי֙; שְׁלוֹמִ֜י; שְׁלוֹמִ֔י; שְׁלוֹמִ֨י |
| 65 | hebrew_screening | `span_same_concept` | `תתתתתא` (ttttt; English: Gregorian 2001) | UXLC | `before_match` | `מאותו` (mwtw) | `word` | 3 | מֵאוֹתֽוֹ׃; מֵאוֹת֑וֹ; מֵֽאוֹתוֹ֙ |
| 81 | hebrew_theology | `span_same_category` | `משיח` (Mashiach; English: Messiah) | UXLC | `before_match` | `שבנא` (shbn; English: Shebna = "vigour") | `phrase_2+word` | 6 | שֶׁבְנָ֖א; שֶׁבְנָ֣א; שֵֽׁב־ נָ֣א; שֵׁ֣ב נָ֔א |
| 82 | hebrew_theology | `span_same_category` | `משיח` (Mashiach; English: Messiah) | UXLC | `after_match` | `לובו` (lwbw) | `phrase_2` | 1 | ל֖וֹ בּֽוֹ׃ |
| 52 | hebrew_screening | `center_verse_exact` | `ביבי` (byby; English: Bibi) | UXLC | `after_match` | `יפתח` (yptch; English: Jephthah or Jiphtah = "he opens") | `word` | 41 | יִפְתַּ֨ח; יִפְתַּ֣ח; יִפְתַּח־; יִפְתָּֽח׃; יִפְתָּ֗ח |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` (naos; English: Temple) | SBLGNT | `before_match` | `υιον` (uion; English: son) | `word` | 85 | υἱὸν; υἱόν,; ⸀υἱόν·; υἱόν; υἱόν. |
| 40 | greek_screening | `hidden_path_only` | `ναοσ` (naos; English: Temple) | SBLGNT | `before_match` | `υιον` (uion; English: son) | `word` | 85 | υἱὸν; υἱόν,; ⸀υἱόν·; υἱόν; υἱόν. |
| 44 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | UXLC | `before_match` | `הילק` (hylq) | `word` | 3 | הַיָּ֑לֶק; הַיֶּ֔לֶק; הַיֶּ֖לֶק |
| 73 | hebrew_theology | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | UXLC | `before_match` | `הילק` (hylq) | `word` | 3 | הַיָּ֑לֶק; הַיֶּ֔לֶק; הַיֶּ֖לֶק |
| 78 | hebrew_theology | `center_verse_same_category` | `אהבה` (hbh; English: Love) | UXLC | `after_match` | `הלהב` (hlhb) | `word` | 3 | הַלַּ֗הַב; הַלַּ֔הַב; הַלַּ֜הַב |
| 71 | hebrew_screening | `hidden_path_only` | `קברריק` (qbrryq; English: Empty Tomb) | UXLC | `after_match` | `שרית` (shryt) | `word` | 2 | שָׂרִ֧יתָ; שֵׁרִ֧ית |
| 56 | hebrew_screening | `center_verse_same_concept` | `התשח` (htshch; English: Hebrew year 5708) | UXLC | `before_match` | `יברא` (ybr) | `word` | 1 | יִבְרָ֣א |
| 61 | hebrew_screening | `span_exact` | `שמימ` (shamayim; English: Heaven) | UXLC | `after_match` | `יהי` (yhy) | `word` | 50 | יְהִ֣י; יְהִ֥י; יְהִ֤י; יְהִי־; יְהִ֨י |
| 55 | hebrew_screening | `center_verse_same_concept` | `רומי` (rwmy; English: Rome) | UXLC | `before_match` | `שמת` (shmt) | `word` | 25 | שְׁמֹ֖ת; שְׁמֹ֧ת; שְׁמֹ֨ת; שֵׁמֹ֗ת; שַׂ֤מְתָּ |
| 64 | hebrew_screening | `span_same_concept` | `רומא` (rwm; English: Rome) | UXLC | `after_match` | `עלו` (lw) | `word` | 41 | עֻלּ֖וֹ; עֲל֥וּ; עָל֥וּ; עָל֖וּ; עָל֤וּ |
| 63 | hebrew_screening | `span_exact` | `מרימ` (mrym; English: Mary) | UXLC | `after_match` | `מרה` (mrh) | `word` | 11 | מָרָֽה׃; מֹרֶֽה׃; מָ֙רָה֙; מָרָ֥ה; מָרָ֖ה |
| 59 | hebrew_screening | `center_verse_same_category` | `מותשני` (mwtshny; English: Second Death) | UXLC | `before_match` | `אפי` (py) | `word` | 20 | אַפִּ֔י; אַפִּ֥י; אַפִּ֣י; אַפִּ֑י; אַפִּ֤י |
| 50 | hebrew_screening | `center_word_same_category` | `אמרי` (mry; English: Amorite) | UXLC | `after_match` | `שבי` (shby) | `word` | 20 | שְׁבִ֧י; שֶֽׁבִי׃; שְׁבִי֙; שְׁבִ֨י; שְׁבִי־ |
| 35 | greek_screening | `span_exact` | `ιραν` (iran; English: Iran) | TR_NT | `before_match` | `εση` (ese) | `word` | 9 | ἔσῃ |
| 58 | hebrew_screening | `center_verse_same_category` | `מותשני` (mwtshny; English: Second Death) | UXLC | `after_match` | `להר` (lhr) | `word` | 8 | לְהַר־; לְהַ֥ר; לְהַ֣ר |
| 54 | hebrew_screening | `center_verse_exact` | `יואל` (ywl; English: Joel) | UXLC | `after_match` | `נזמ` (nzm) | `word` | 7 | נֶ֣זֶם; נֶ֥זֶם; נֶ֙זֶם֙ |
| 67 | hebrew_screening | `span_same_category` | `פתרסימ` (ptrsym; English: Pathrusim) | UXLC | `before_match` | `עכנ` (kn) | `word` | 6 | עָכָ֣ן; עָכָ֞ן; עָכָ֗ן; עָכָ֛ן |
| 68 | hebrew_screening | `span_same_category` | `טימותי` (tymwty; English: Timothy) | UXLC | `before_match` | `חלי` (chly) | `word` | 5 | חֹ֑לִי; חֳלִי֙; חֳלִ֥י; חֳלִ֖י |
| 46 | hebrew_screening | `center_word_same_concept` | `ערוב` (rwb; English: Flies Plague) | UXLC | `before_match` | `מרו` (mrw) | `word` | 4 | מָר֥וּ; מָ֥רוּ; מָ֝ר֗וּ; מָר֖וֹ |
| 49 | hebrew_screening | `center_word_same_category` | `גרמניה` (grmnyh; English: Germany) | UXLC | `after_match` | `ערש` (rsh) | `word` | 4 | עֶ֣רֶשׂ; עָֽרֶשׂ׃; עֶ֥רֶשׂ |
| 76 | hebrew_theology | `center_word_same_category` | `תורה` (twrh; English: Torah) | UXLC | `after_match` | `ואח` (wch) | `word` | 2 | וְאָ֥ח; וָאָ֣ח |
| 43 | hebrew_screening | `center_word_exact` | `שממה` (shemamah; English: Desolation) | UXLC | `before_match` | `עבה` (bh) | `word` | 2 | עָבָ֖ה |
| 62 | hebrew_screening | `span_exact` | `שמימ` (shamayim; English: Heaven) | UXLC | `before_match` | `ובר` (wbr) | `word` | 2 | וּֽבַר־; וּ֝בַ֗ר |
| 79 | hebrew_theology | `center_verse_same_category` | `אהבה` (hbh; English: Love) | UXLC | `after_match` | `יבל` (ybl) | `word` | 1 | יָבָ֑ל |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` (Iouan; English: Javan) | TR_NT | `after_match` | `ηα` (ea) | `phrase_2` | 2 | ἢ ἃ; Ἢ ἃ |
| 69 | hebrew_screening | `span_same_category` | `תתתתתכז` (tttttkz; English: Gregorian 2027 additive) | UXLC | `after_match` | `שה` (shh; English: Lamb) | `word` | 24 | שֶׂ֣ה; שֶׂה־; שֶׂ֥ה; שֶׂ֔ה; שֶׂ֖ה |
| 60 | hebrew_screening | `center_verse_same_category` | `טימותי` (tymwty; English: Timothy) | UXLC | `after_match` | `או` (w) | `word` | 321 | א֥וֹ; אוֹ־; א֣וֹ; א֚וֹ; א֖וֹ |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` (eual; English: Obal) | TR_NT | `before_match` | `σε` (se) | `word` | 197 | σε; σὲ; σέ |
| 23 | greek_screening | `center_word_exact` | `αννα` (anna; English: Hannah) | TCG_NT | `after_match` | `γε` (ge) | `word` | 28 | γε; γε, |
| 29 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | TR_NT | `before_match` | `τι` (ti) | `word` | 453 | τι; τί; Τί |
| 30 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | TR_NT | `before_match` | `τι` (ti) | `word` | 453 | τι; τί; Τί |
| 17 | english_screening | `span_same_category` | `mash` | KJV | `before_match` | `or` | `word` | 1122 | or; Or; or,; Or, |
| 83 | hebrew_theology | `span_same_category` | `ברית` (bryt; English: Covenant) | UXLC | `after_match` | `דא` (d) | `word` | 5 | דָא־; דָּ֥א; דָּֽא׃; דָ֔א |
| 21 | english_screening | `hidden_path_only` | `cush` | KJV | `before_match` | `ur` | `word` | 5 | Ur; Ur, |
| 66 | hebrew_screening | `span_same_concept` | `התשח` (htshch; English: Hebrew year 5708) | UXLC | `before_match` | `הכ` (hk) | `word` | 4 | הַךְ־; הַ֨ךְ; הַ֤ךְ |
| 48 | hebrew_screening | `center_word_same_concept` | `ערוב` (rwb; English: Flies Plague) | UXLC | `before_match` | `לח` (lch) | `word` | 3 | לַ֖ח; לָ֔ח; לַח֩ |
| 57 | hebrew_screening | `center_verse_same_concept` | `רומי` (rwmy; English: Rome) | UXLC | `before_match` | `תו` (tav; English: mark/sign) | `word` | 1 | תָּ֜ו |
| 25 | greek_screening | `center_word_same_category` | `λουδ` (loud; English: Lud) | TR_NT | `after_match` | `ηρ` (er) | `word` | 1 | Ἤρ |
| 37 | greek_screening | `span_same_category` | `σαλα` (Sala; English: Shelah) | SBLGNT | `after_match` | `α` (a) | `word` | 117 | ἃ; ⸂ἃ; ⸀ἃ; Ἃ; ἅ |
| 41 | greek_screening | `hidden_path_only` | `σαλα` (Sala; English: Shelah) | SBLGNT | `after_match` | `α` (a) | `word` | 117 | ἃ; ⸂ἃ; ⸀ἃ; Ἃ; ἅ |
| 22 | greek_screening | `center_word_exact` | `παισ` (pais; English: Servant) | SBLGNT | `before_match` | `α` (a) | `word` | 117 | ἃ; ⸂ἃ; ⸀ἃ; Ἃ; ἅ |
| 32 | greek_screening | `center_verse_same_category` | `κινα` (kina; English: China) | SBLGNT | `after_match` | `α` (a) | `word` | 117 | ἃ; ⸂ἃ; ⸀ἃ; Ἃ; ἅ |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` (elke; English: Boils) | SBLGNT | `after_match` | `α` (a) | `word` | 117 | ἃ; ⸂ἃ; ⸀ἃ; Ἃ; ἅ |
| 38 | greek_screening | `span_same_category` | `αδαμ` (adam; English: Adam) | TR_NT | `before_match` | `ο` (o) | `word` | 3353 | ὁ; ὅ; Ὁ; ὃ; Ὃ |
| 4 | english_screening | `center_word_same_category` | `obed` | KJV | `before_match` | `a` | `word` | 8181 | a; A; (a |
| 5 | english_screening | `center_word_same_category` | `obed` | KJV | `before_match` | `a` | `word` | 8181 | a; A; (a |
| 6 | english_screening | `center_word_same_category` | `edom` | KJV | `before_match` | `a` | `word` | 8181 | a; A; (a |
| 10 | english_screening | `center_verse_same_category` | `sign` | KJV | `before_match` | `t` | `word` | 1 | t |
| 20 | english_screening | `hidden_path_only` | `sign` | KJV | `before_match` | `t` | `word` | 1 | t |
| 8 | english_screening | `center_verse_exact` | `heal` | KJV | `after_match` | `s` | `word` | 1 | s, |
| 18 | english_screening | `span_same_category` | `adam` | KJV | `after_match` | `t` | `word` | 1 | t |

## Compound Extension Rows

| Rank | Corpus | Term | Type | Extended sequence | Kind | Count | Refs |
| ---: | --- | --- | --- | --- | --- | ---: | --- |
| 45 | UXLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2` | 6 | Deut 4:30; Deut 30:2; 1 Sam 12:5; Isa 19:22; Hos 14:2 |
| 74 | UXLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2` | 6 | Deut 4:30; Deut 30:2; 1 Sam 12:5; Isa 19:22; Hos 14:2 |
| 45 | UHB | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2+word` | 6 | DEU 4:30; DEU 30:2; ISA 19:22; LAM 3:40; 1SA 12:5 |
| 74 | UHB | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2+word` | 6 | DEU 4:30; DEU 30:2; ISA 19:22; LAM 3:40; 1SA 12:5 |
| 45 | MT_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2` | 6 | Deut 4:30; Deut 30:2; 1Sam 12:5; Isa 19:22; Hos 14:2 |
| 74 | MT_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2` | 6 | Deut 4:30; Deut 30:2; 1Sam 12:5; Isa 19:22; Hos 14:2 |
| 45 | MAM | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2+word` | 6 | Deut 4:30; Deut 30:2; Isa 19:22; Lam 3:40; 1 Sam 12:5 |
| 74 | MAM | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2+word` | 6 | Deut 4:30; Deut 30:2; Isa 19:22; Lam 3:40; 1 Sam 12:5 |
| 45 | EBIBLE_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2+word` | 6 | DEU 4:30; DEU 30:2; ISA 19:22; LAM 3:40; 1SA 12:5 |
| 74 | EBIBLE_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2+word` | 6 | DEU 4:30; DEU 30:2; ISA 19:22; LAM 3:40; 1SA 12:5 |
| 1 | KJV | `baal` | `before_plus_term` | `tobaal` | `phrase_2` | 1 | 2KI 10:19 |
| 1 | KJV | `baal` | `term_plus_after` | `baalis` | `word` | 1 | JER 40:14 |
| 9 | KJV | `hand` | `term_plus_after` | `hando` | `phrase_2` | 5 | EXO 15:6; PSA 17:14; JER 18:6; DAN 3:17 |
| 70 | UXLC | `יומיהוה` (yom YHWH; English: Day Of The Lord) | `before_plus_term` | `היומיהוה` (hayom YHWH; English: the day of YHWH) | `phrase_2` | 3 | Lev 9:4; 2 Kings 2:3; 2 Kings 2:5 |
| 70 | UHB | `יומיהוה` (yom YHWH; English: Day Of The Lord) | `before_plus_term` | `היומיהוה` (hayom YHWH; English: the day of YHWH) | `phrase_2` | 3 | LEV 9:4; 2KI 2:3; 2KI 2:5 |
| 70 | MT_WLC | `יומיהוה` (yom YHWH; English: Day Of The Lord) | `before_plus_term` | `היומיהוה` (hayom YHWH; English: the day of YHWH) | `phrase_2` | 3 | Lev 9:4; 2Kgs 2:3; 2Kgs 2:5 |
| 70 | MAM | `יומיהוה` (yom YHWH; English: Day Of The Lord) | `before_plus_term` | `היומיהוה` (hayom YHWH; English: the day of YHWH) | `phrase_2` | 3 | Lev 9:4; 2 Kgs 2:3; 2 Kgs 2:5 |
| 70 | EBIBLE_WLC | `יומיהוה` (yom YHWH; English: Day Of The Lord) | `before_plus_term` | `היומיהוה` (hayom YHWH; English: the day of YHWH) | `phrase_2` | 3 | LEV 9:4; 2KI 2:3; 2KI 2:5 |
| 45 | UXLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `phrase_2` | 1 | Dan 5:19 |
| 74 | UXLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `phrase_2` | 1 | Dan 5:19 |
| 45 | MT_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `phrase_2` | 1 | Dan 5:19 |
| 74 | MT_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `phrase_2` | 1 | Dan 5:19 |
| 1 | KJV | `baal` | `before_plus_term` | `obaal` | `phrase_2` | 1 | 1KI 18:26 |
| 19 | KJV | `heal` | `before_plus_term` | `iheal` | `phrase_2` | 1 | DEU 32:39 |
| 3 | KJV | `heth` | `term_plus_after` | `hethy` | `phrase_2` | 1 | DEU 32:6 |
| 19 | KJV | `heal` | `term_plus_after` | `heala` | `phrase_2` | 1 | ECC 3:3 |
| 13 | KJV | `thin` | `term_plus_after` | `thine` | `word` | 937 | GEN 13:14; GEN 14:20; GEN 14:23; GEN 15:4; GEN 20:7 |
| 77 | UXLC | `ברית` (bryt; English: Covenant) | `term_plus_after` | `בריתו` (brytw) | `word` | 17 | Ex 2:24; Deut 4:13; Deut 8:18; Deut 17:2; 2 Kings 13:23 |
| 77 | MT_WLC | `ברית` (bryt; English: Covenant) | `term_plus_after` | `בריתו` (brytw) | `word` | 17 | Exod 2:24; Deut 4:13; Deut 8:18; Deut 17:2; 2Kgs 13:23 |
| 15 | KJV | `wine` | `before_plus_term` | `swine` | `word` | 16 | LEV 11:7; DEU 14:8; MAT 7:6; MAT 8:30; MAT 8:31 |
| 77 | UHB | `ברית` (bryt; English: Covenant) | `term_plus_after` | `בריתו` (brytw) | `word` | 10 | DEU 17:2; 2KI 13:23; 1CH 16:15; PSA 25:10; PSA 55:20 |
| 77 | MAM | `ברית` (bryt; English: Covenant) | `term_plus_after` | `בריתו` (brytw) | `word` | 10 | Deut 17:2; 2 Kgs 13:23; Ps 25:10; Ps 55:21; Ps 103:18 |
| 77 | EBIBLE_WLC | `ברית` (bryt; English: Covenant) | `term_plus_after` | `בריתו` (brytw) | `word` | 10 | DEU 17:2; 2KI 13:23; 1CH 16:15; PSA 25:10; PSA 55:21 |
| 80 | UXLC | `חכמה` (chkmh; English: Wisdom) | `before_plus_term` | `וחכמה` (wchkmh) | `word` | 6 | Prov 10:23; Eccl 9:10; Dan 1:17; Dan 5:11; Dan 5:14 |
| 80 | UHB | `חכמה` (chkmh; English: Wisdom) | `before_plus_term` | `וחכמה` (wchkmh) | `word` | 6 | 2CH 9:22; PRO 10:23; ECC 9:10; DAN 1:17; DAN 5:11 |
| 80 | MT_WLC | `חכמה` (chkmh; English: Wisdom) | `before_plus_term` | `וחכמה` (wchkmh) | `word` | 6 | Prov 10:23; Eccl 9:10; Dan 1:17; Dan 5:11; Dan 5:14 |
| 80 | MAM | `חכמה` (chkmh; English: Wisdom) | `before_plus_term` | `וחכמה` (wchkmh) | `word` | 6 | Prov 10:23; Eccl 9:10; Dan 1:17; Dan 5:11; Dan 5:14 |
| 80 | EBIBLE_WLC | `חכמה` (chkmh; English: Wisdom) | `before_plus_term` | `וחכמה` (wchkmh) | `word` | 6 | 2CH 9:22; PRO 10:23; ECC 9:10; DAN 1:17; DAN 5:11 |
| 51 | UXLC | `אמרי` (mry; English: Amorite) | `term_plus_after` | `אמריו` (mryw) | `word` | 4 | Prov 17:27; Job 22:22; Job 32:12; Job 34:37 |
| 51 | UHB | `אמרי` (mry; English: Amorite) | `term_plus_after` | `אמריו` (mryw) | `word` | 4 | JOB 22:22; JOB 32:12; JOB 34:37; PRO 17:27 |
| 51 | MT_WLC | `אמרי` (mry; English: Amorite) | `term_plus_after` | `אמריו` (mryw) | `word` | 4 | Prov 17:27; Job 22:22; Job 32:12; Job 34:37 |
| 51 | MAM | `אמרי` (mry; English: Amorite) | `term_plus_after` | `אמריו` (mryw) | `word` | 4 | Prov 17:27; Job 22:22; Job 32:12; Job 34:37 |
| 51 | EBIBLE_WLC | `אמרי` (mry; English: Amorite) | `term_plus_after` | `אמריו` (mryw) | `word` | 4 | JOB 22:22; JOB 32:12; JOB 34:37; PRO 17:27 |
| 51 | UXLC | `אמרי` (mry; English: Amorite) | `before_plus_term` | `מאמרי` (mmry) | `word` | 3 | Prov 4:5; Prov 5:7; Prov 19:27 |
| 51 | MT_WLC | `אמרי` (mry; English: Amorite) | `before_plus_term` | `מאמרי` (mmry) | `word` | 3 | Prov 4:5; Prov 5:7; Prov 19:27 |
| 53 | UXLC | `אריה` (ryh; English: Lion) | `before_plus_term` | `ואריה` (wryh) | `word` | 2 | Isa 11:7; Isa 65:25 |
| 53 | UHB | `אריה` (ryh; English: Lion) | `before_plus_term` | `ואריה` (wryh) | `word` | 2 | ISA 11:7; ISA 65:25 |
| 53 | MT_WLC | `אריה` (ryh; English: Lion) | `before_plus_term` | `ואריה` (wryh) | `word` | 2 | Isa 11:7; Isa 65:25 |
| 53 | MAM | `אריה` (ryh; English: Lion) | `before_plus_term` | `ואריה` (wryh) | `word` | 2 | Isa 11:7; Isa 65:25 |
| 53 | EBIBLE_WLC | `אריה` (ryh; English: Lion) | `before_plus_term` | `ואריה` (wryh) | `word` | 2 | ISA 11:7; ISA 65:25 |
| 45 | UHB | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `word` | 1 | DAN 5:19 |
| 74 | UHB | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `word` | 1 | DAN 5:19 |
| 1 | KJV | `baal` | `term_plus_after` | `baali` | `word` | 1 | HOS 2:16 |
| 45 | EBIBLE_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `word` | 1 | DAN 5:19 |
| 74 | EBIBLE_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `word` | 1 | DAN 5:19 |

## Read

The extension lexicon is built from normalized surface words and phrases in
the same corpus. A row here means the same ELS lane can spell a larger
surface-attested token somewhere in that text. It does not mean the hidden
path appears openly at the center verse, and it does not replace controls.
