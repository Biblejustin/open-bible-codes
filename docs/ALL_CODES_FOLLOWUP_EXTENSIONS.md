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

- path rows checked: 295
- selected rows checked: 80
- selected rows with extensions: 66
- extension rows: 676
- selected rows with compound extensions: 12
- compound extension rows containing hidden term: 58
- max extension length: 5
- extension rows by corpus: `{'BYZ_NT': 33, 'EBIBLE_WLC': 98, 'KJV': 25, 'MAM': 103, 'MT_WLC': 111, 'SBLGNT': 31, 'TCG_NT': 33, 'TR_NT': 33, 'UHB': 99, 'UXLC': 110}`
- extension rows by type: `{'after_match': 318, 'before_match': 300, 'before_plus_term': 37, 'term_plus_after': 21}`

## Best Extensions By Selected Row

| Rank | Queue | Bucket | Term | Corpus | Type | Extended sequence | Kind | Count | Examples |
| ---: | --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| 53 | hebrew_screening | `center_verse_exact` | `אדני` (Adonai; English: Lord) | UXLC | `term_plus_after` | `אדניאמר` (dnymr) | `phrase_2` | 2 | אֲדֹנָי֙ אֹמֵ֔ר; אֲדֹנָ֑י אֱמֹ֕ר |
| 45 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | UXLC | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2` | 6 | עַד־ יְהוָ֣ה; עַד־ יְהוָ֤ה; עֵ֧ד יְהוָ֣ה; עַד־ יְהוָ֔ה; עַ֖ד יְהוָ֣ה |
| 71 | hebrew_theology | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | UXLC | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2` | 6 | עַד־ יְהוָ֣ה; עַד־ יְהוָ֤ה; עֵ֧ד יְהוָ֣ה; עַד־ יְהוָ֔ה; עַ֖ד יְהוָ֣ה |
| 21 | english_screening | `hidden_path_only` | `bear` | KJV | `before_plus_term` | `dobear` | `phrase_2` | 2 | do bear |
| 9 | english_screening | `center_verse_exact` | `hand` | KJV | `term_plus_after` | `hando` | `phrase_2` | 5 | hand, O |
| 67 | hebrew_screening | `hidden_path_only` | `יומיהוה` (yom YHWH; English: Day Of The Lord) | UXLC | `before_plus_term` | `היומיהוה` (hayom YHWH; English: the day of YHWH) | `phrase_2` | 3 | הַיּ֔וֹם יְהוָ֖ה; הַיּ֗וֹם יְהוָ֛ה |
| 2 | english_screening | `center_word_exact` | `heth` | KJV | `term_plus_after` | `hethy` | `phrase_2` | 1 | he thy |
| 19 | english_screening | `hidden_path_only` | `heal` | KJV | `before_plus_term` | `iheal` | `phrase_2` | 1 | I heal: |
| 74 | hebrew_theology | `center_word_same_category` | `ברית` (bryt; English: Covenant) | UXLC | `term_plus_after` | `בריתו` (brytw) | `word` | 17 | בְּרִית֔וֹ; בְּרִית֗וֹ; בְּרִית֛וֹ; בְּרִיתֽוֹ׃; בְּרִיתוֹ֙ |
| 77 | hebrew_theology | `center_verse_same_category` | `חכמה` (chkmh; English: Wisdom) | UXLC | `before_plus_term` | `וחכמה` (wchkmh) | `word` | 6 | וְ֝חָכְמָ֗ה; וְחָכְמָ֔ה; וְחָכְמָ֑ה; וְחָכְמָ֥ה; וְחָכְמָֽה׃ |
| 50 | hebrew_screening | `center_word_same_category` | `אמרי` (mry; English: Amorite) | UXLC | `term_plus_after` | `אמריו` (mryw) | `word` | 4 | אֲ֭מָרָיו; אֲ֝מָרָ֗יו; אֲמָרָ֣יו |
| 52 | hebrew_screening | `center_verse_exact` | `אריה` (ryh; English: Lion) | UXLC | `before_plus_term` | `ואריה` (wryh) | `word` | 2 | וְאַרְיֵ֖ה; וְאַרְיֵה֙ |
| 46 | hebrew_screening | `center_word_same_concept` | `רומא` (rwm; English: Rome) | UXLC | `before_match` | `שלומי` (shlwmy) | `word` | 4 | שְׁלוֹמִי֙; שְׁלוֹמִ֜י; שְׁלוֹמִ֔י; שְׁלוֹמִ֨י |
| 63 | hebrew_screening | `span_same_concept` | `תתתתתא` (ttttt; English: Gregorian 2001) | UXLC | `before_match` | `מאותו` (mwtw) | `word` | 3 | מֵאוֹתֽוֹ׃; מֵאוֹת֑וֹ; מֵֽאוֹתוֹ֙ |
| 78 | hebrew_theology | `span_same_category` | `משיח` (Mashiach; English: Messiah) | UXLC | `before_match` | `שבנא` (shbn) | `phrase_2+word` | 6 | שֶׁבְנָ֖א; שֶׁבְנָ֣א; שֵֽׁב־ נָ֣א; שֵׁ֣ב נָ֔א |
| 79 | hebrew_theology | `span_same_category` | `משיח` (Mashiach; English: Messiah) | UXLC | `after_match` | `לובו` (lwbw) | `phrase_2` | 1 | ל֖וֹ בּֽוֹ׃ |
| 51 | hebrew_screening | `center_verse_exact` | `ביבי` (byby; English: Bibi) | UXLC | `after_match` | `יפתח` (yptch) | `word` | 41 | יִפְתַּ֨ח; יִפְתַּ֣ח; יִפְתַּח־; יִפְתָּֽח׃; יִפְתָּ֗ח |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` (naos; English: Temple) | SBLGNT | `before_match` | `υιον` (uion) | `word` | 85 | υἱὸν; υἱόν,; ⸀υἱόν·; υἱόν; υἱόν. |
| 44 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | UXLC | `before_match` | `הילק` (hylq) | `word` | 3 | הַיָּ֑לֶק; הַיֶּ֔לֶק; הַיֶּ֖לֶק |
| 70 | hebrew_theology | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | UXLC | `before_match` | `הילק` (hylq) | `word` | 3 | הַיָּ֑לֶק; הַיֶּ֔לֶק; הַיֶּ֖לֶק |
| 75 | hebrew_theology | `center_verse_same_category` | `אהבה` (hbh; English: Love) | UXLC | `after_match` | `הלהב` (hlhb) | `word` | 3 | הַלַּ֗הַב; הַלַּ֔הַב; הַלַּ֜הַב |
| 68 | hebrew_screening | `hidden_path_only` | `קברריק` (qbrryq; English: Empty Tomb) | UXLC | `after_match` | `שרית` (shryt) | `word` | 2 | שָׂרִ֧יתָ; שֵׁרִ֧ית |
| 60 | hebrew_screening | `span_exact` | `שמימ` (shmym; English: Heaven) | UXLC | `after_match` | `יהי` (yhy) | `word` | 50 | יְהִ֣י; יְהִ֥י; יְהִ֤י; יְהִי־; יְהִ֨י |
| 54 | hebrew_screening | `center_verse_same_concept` | `רומי` (rwmy; English: Rome) | UXLC | `before_match` | `שמת` (shmt) | `word` | 25 | שְׁמֹ֖ת; שְׁמֹ֧ת; שְׁמֹ֨ת; שֵׁמֹ֗ת; שַׂ֤מְתָּ |
| 62 | hebrew_screening | `span_exact` | `מרימ` (mrym; English: Mary) | UXLC | `after_match` | `מרה` (mrh) | `word` | 11 | מָרָֽה׃; מֹרֶֽה׃; מָ֙רָה֙; מָרָ֥ה; מָרָ֖ה |
| 58 | hebrew_screening | `center_verse_same_category` | `מותשני` (mwtshny; English: Second Death) | UXLC | `before_match` | `אפי` (py) | `word` | 20 | אַפִּ֔י; אַפִּ֥י; אַפִּ֣י; אַפִּ֑י; אַפִּ֤י |
| 49 | hebrew_screening | `center_word_same_category` | `אמרי` (mry; English: Amorite) | UXLC | `after_match` | `שבי` (shby) | `word` | 20 | שְׁבִ֧י; שֶֽׁבִי׃; שְׁבִי֙; שְׁבִ֨י; שְׁבִי־ |
| 35 | greek_screening | `span_exact` | `ιραν` (iran; English: Iran) | TR_NT | `before_match` | `εση` (ese) | `word` | 9 | ἔσῃ |
| 57 | hebrew_screening | `center_verse_same_category` | `מותשני` (mwtshny; English: Second Death) | UXLC | `after_match` | `להר` (lhr) | `word` | 8 | לְהַר־; לְהַ֥ר; לְהַ֣ר |
| 64 | hebrew_screening | `span_same_category` | `פתרסימ` (ptrsym; English: Pathrusim) | UXLC | `before_match` | `עכנ` (kn) | `word` | 6 | עָכָ֣ן; עָכָ֞ן; עָכָ֗ן; עָכָ֛ן |
| 65 | hebrew_screening | `span_same_category` | `טימותי` (tymwty; English: Timothy) | UXLC | `before_match` | `חלי` (chly) | `word` | 5 | חֹ֑לִי; חֳלִי֙; חֳלִ֥י; חֳלִ֖י |
| 48 | hebrew_screening | `center_word_same_category` | `גרמניה` (grmnyh; English: Germany) | UXLC | `after_match` | `ערש` (rsh) | `word` | 4 | עֶ֣רֶשׂ; עָֽרֶשׂ׃; עֶ֥רֶשׂ |
| 56 | hebrew_screening | `center_verse_same_concept` | `תתתתתא` (ttttt; English: Gregorian 2001) | UXLC | `after_match` | `עבה` (bh) | `word` | 2 | עָבָ֖ה |
| 73 | hebrew_theology | `center_word_same_category` | `תורה` (twrh; English: Torah) | UXLC | `after_match` | `ואח` (wch) | `word` | 2 | וְאָ֥ח; וָאָ֣ח |
| 43 | hebrew_screening | `center_word_exact` | `שממה` (shmmh; English: Desolation) | UXLC | `before_match` | `עבה` (bh) | `word` | 2 | עָבָ֖ה |
| 61 | hebrew_screening | `span_exact` | `שמימ` (shmym; English: Heaven) | UXLC | `before_match` | `ובר` (wbr) | `word` | 2 | וּֽבַר־; וּ֝בַ֗ר |
| 76 | hebrew_theology | `center_verse_same_category` | `אהבה` (hbh; English: Love) | UXLC | `after_match` | `יבל` (ybl) | `word` | 1 | יָבָ֑ל |
| 39 | greek_screening | `span_same_category` | `γαμερ` (gamer; English: Gomer) | TR_NT | `before_match` | `αο` (ao) | `phrase_2` | 3 | Ἃ ὁ; ἃ ὁ |
| 22 | greek_screening | `center_word_exact` | `νατο` (nato; English: NATO) | TR_NT | `after_match` | `οο` (oo) | `phrase_2` | 2 | ὃ ὁ |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` (Iouan; English: Javan) | TR_NT | `after_match` | `ηα` (ea) | `phrase_2` | 2 | ἢ ἃ; Ἢ ἃ |
| 66 | hebrew_screening | `span_same_category` | `תתתתתכז` (tttttkz; English: Gregorian 2027 additive) | UXLC | `after_match` | `שה` (shh; English: Lamb) | `word` | 24 | שֶׂ֣ה; שֶׂה־; שֶׂ֥ה; שֶׂ֔ה; שֶׂ֖ה |
| 47 | hebrew_screening | `center_word_same_concept` | `רומא` (rwm; English: Rome) | UXLC | `after_match` | `לי` (ly) | `word` | 749 | לִּ֥י; לִ֤י; לִ֣י; לִּ֑י; לִּ֔י |
| 59 | hebrew_screening | `center_verse_same_category` | `טימותי` (tymwty; English: Timothy) | UXLC | `after_match` | `או` (w) | `word` | 321 | א֥וֹ; אוֹ־; א֣וֹ; א֚וֹ; א֖וֹ |
| 42 | greek_screening | `hidden_path_only` | `υιοσ` (huios; English: Son) | TR_NT | `before_match` | `εν` (en) | `word` | 2870 | ἐν; Ἐν; ἓν; ἕν; Ἕν |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` (eual; English: Obal) | TR_NT | `before_match` | `σε` (se) | `word` | 197 | σε; σὲ; σέ |
| 29 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | TR_NT | `before_match` | `τι` (ti) | `word` | 453 | τι; τί; Τί |
| 30 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | TR_NT | `before_match` | `τι` (ti) | `word` | 453 | τι; τί; Τί |
| 17 | english_screening | `span_same_category` | `mash` | KJV | `before_match` | `or` | `word` | 1122 | or; Or; or,; Or, |
| 80 | hebrew_theology | `span_same_category` | `ברית` (bryt; English: Covenant) | UXLC | `after_match` | `דא` (d) | `word` | 5 | דָא־; דָּ֥א; דָּֽא׃; דָ֔א |
| 20 | english_screening | `hidden_path_only` | `cush` | KJV | `before_match` | `ur` | `word` | 5 | Ur; Ur, |
| 13 | english_screening | `span_exact` | `lord` | KJV | `after_match` | `ho` | `word` | 4 | Ho,; ho, |
| 14 | english_screening | `span_exact` | `lord` | KJV | `after_match` | `ho` | `word` | 4 | Ho,; ho, |
| 55 | hebrew_screening | `center_verse_same_concept` | `רומי` (rwmy; English: Rome) | UXLC | `before_match` | `תו` (tav; English: mark/sign) | `word` | 1 | תָּ֜ו |
| 25 | greek_screening | `center_word_same_category` | `λουδ` (loud; English: Lud) | TR_NT | `after_match` | `ηρ` (er) | `word` | 1 | Ἤρ |
| 37 | greek_screening | `span_same_category` | `σαλα` (Sala; English: Shelah) | SBLGNT | `after_match` | `α` (a) | `word` | 117 | ἃ; ⸂ἃ; ⸀ἃ; Ἃ; ἅ |
| 40 | greek_screening | `hidden_path_only` | `σαλα` (Sala; English: Shelah) | SBLGNT | `after_match` | `α` (a) | `word` | 117 | ἃ; ⸂ἃ; ⸀ἃ; Ἃ; ἅ |
| 23 | greek_screening | `center_word_exact` | `ναοσ` (naos; English: Temple) | SBLGNT | `after_match` | `α` (a) | `word` | 117 | ἃ; ⸂ἃ; ⸀ἃ; Ἃ; ἅ |
| 32 | greek_screening | `center_verse_same_category` | `κινα` (kina; English: China) | SBLGNT | `after_match` | `α` (a) | `word` | 117 | ἃ; ⸂ἃ; ⸀ἃ; Ἃ; ἅ |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` (elke; English: Boils) | SBLGNT | `after_match` | `α` (a) | `word` | 117 | ἃ; ⸂ἃ; ⸀ἃ; Ἃ; ἅ |
| 38 | greek_screening | `span_same_category` | `αδαμ` (adam; English: Adam) | TR_NT | `before_match` | `ο` (o) | `word` | 3353 | ὁ; ὅ; Ὁ; ὃ; Ὃ |
| 5 | english_screening | `center_word_same_category` | `shem` | KJV | `before_match` | `o` | `word` | 1065 | O |
| 4 | english_screening | `center_word_same_category` | `edom` | KJV | `before_match` | `a` | `word` | 8181 | a; A; (a |
| 10 | english_screening | `center_verse_same_category` | `sign` | KJV | `before_match` | `t` | `word` | 1 | t |
| 15 | english_screening | `span_exact` | `isis` | KJV | `before_match` | `s` | `word` | 1 | s, |
| 8 | english_screening | `center_verse_exact` | `heal` | KJV | `after_match` | `s` | `word` | 1 | s, |
| 18 | english_screening | `span_same_category` | `adam` | KJV | `after_match` | `t` | `word` | 1 | t |

## Compound Extension Rows

| Rank | Corpus | Term | Type | Extended sequence | Kind | Count | Refs |
| ---: | --- | --- | --- | --- | --- | ---: | --- |
| 53 | UXLC | `אדני` (Adonai; English: Lord) | `term_plus_after` | `אדניאמר` (dnymr) | `phrase_2` | 2 | Isa 6:8; Ezek 21:14 |
| 53 | UHB | `אדני` (Adonai; English: Lord) | `term_plus_after` | `אדניאמר` (dnymr) | `phrase_2` | 2 | ISA 6:8; EZK 21:9 |
| 53 | MT_WLC | `אדני` (Adonai; English: Lord) | `term_plus_after` | `אדניאמר` (dnymr) | `phrase_2` | 2 | Isa 6:8; Ezek 21:14 |
| 53 | MAM | `אדני` (Adonai; English: Lord) | `term_plus_after` | `אדניאמר` (dnymr) | `phrase_2` | 2 | Isa 6:8; Ezek 21:14 |
| 53 | EBIBLE_WLC | `אדני` (Adonai; English: Lord) | `term_plus_after` | `אדניאמר` (dnymr) | `phrase_2` | 2 | ISA 6:8; EZK 21:14 |
| 45 | UXLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2` | 6 | Deut 4:30; Deut 30:2; 1 Sam 12:5; Isa 19:22; Hos 14:2 |
| 71 | UXLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2` | 6 | Deut 4:30; Deut 30:2; 1 Sam 12:5; Isa 19:22; Hos 14:2 |
| 45 | UHB | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2+word` | 6 | DEU 4:30; DEU 30:2; ISA 19:22; LAM 3:40; 1SA 12:5 |
| 71 | UHB | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2+word` | 6 | DEU 4:30; DEU 30:2; ISA 19:22; LAM 3:40; 1SA 12:5 |
| 45 | MT_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2` | 6 | Deut 4:30; Deut 30:2; 1Sam 12:5; Isa 19:22; Hos 14:2 |
| 71 | MT_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2` | 6 | Deut 4:30; Deut 30:2; 1Sam 12:5; Isa 19:22; Hos 14:2 |
| 45 | MAM | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2+word` | 6 | Deut 4:30; Deut 30:2; Isa 19:22; Lam 3:40; 1 Sam 12:5 |
| 71 | MAM | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2+word` | 6 | Deut 4:30; Deut 30:2; Isa 19:22; Lam 3:40; 1 Sam 12:5 |
| 45 | EBIBLE_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2+word` | 6 | DEU 4:30; DEU 30:2; ISA 19:22; LAM 3:40; 1SA 12:5 |
| 71 | EBIBLE_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `עדיהוה` (dyhwh) | `phrase_2+word` | 6 | DEU 4:30; DEU 30:2; ISA 19:22; LAM 3:40; 1SA 12:5 |
| 21 | KJV | `bear` | `before_plus_term` | `dobear` | `phrase_2` | 2 | PSA 89:50; JHN 5:36 |
| 53 | UXLC | `אדני` (Adonai; English: Lord) | `term_plus_after` | `אדניאמ` (dnym) | `phrase_2` | 1 | Gen 18:3 |
| 53 | MT_WLC | `אדני` (Adonai; English: Lord) | `term_plus_after` | `אדניאמ` (dnym) | `phrase_2` | 1 | Gen 18:3 |
| 9 | KJV | `hand` | `term_plus_after` | `hando` | `phrase_2` | 5 | EXO 15:6; PSA 17:14; JER 18:6; DAN 3:17 |
| 67 | UXLC | `יומיהוה` (yom YHWH; English: Day Of The Lord) | `before_plus_term` | `היומיהוה` (hayom YHWH; English: the day of YHWH) | `phrase_2` | 3 | Lev 9:4; 2 Kings 2:3; 2 Kings 2:5 |
| 67 | UHB | `יומיהוה` (yom YHWH; English: Day Of The Lord) | `before_plus_term` | `היומיהוה` (hayom YHWH; English: the day of YHWH) | `phrase_2` | 3 | LEV 9:4; 2KI 2:3; 2KI 2:5 |
| 67 | MT_WLC | `יומיהוה` (yom YHWH; English: Day Of The Lord) | `before_plus_term` | `היומיהוה` (hayom YHWH; English: the day of YHWH) | `phrase_2` | 3 | Lev 9:4; 2Kgs 2:3; 2Kgs 2:5 |
| 67 | MAM | `יומיהוה` (yom YHWH; English: Day Of The Lord) | `before_plus_term` | `היומיהוה` (hayom YHWH; English: the day of YHWH) | `phrase_2` | 3 | Lev 9:4; 2 Kgs 2:3; 2 Kgs 2:5 |
| 67 | EBIBLE_WLC | `יומיהוה` (yom YHWH; English: Day Of The Lord) | `before_plus_term` | `היומיהוה` (hayom YHWH; English: the day of YHWH) | `phrase_2` | 3 | LEV 9:4; 2KI 2:3; 2KI 2:5 |
| 45 | UXLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `phrase_2` | 1 | Dan 5:19 |
| 71 | UXLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `phrase_2` | 1 | Dan 5:19 |
| 45 | MT_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `phrase_2` | 1 | Dan 5:19 |
| 71 | MT_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `phrase_2` | 1 | Dan 5:19 |
| 19 | KJV | `heal` | `before_plus_term` | `iheal` | `phrase_2` | 1 | DEU 32:39 |
| 2 | KJV | `heth` | `term_plus_after` | `hethy` | `phrase_2` | 1 | DEU 32:6 |
| 19 | KJV | `heal` | `term_plus_after` | `heala` | `phrase_2` | 1 | ECC 3:3 |
| 74 | UXLC | `ברית` (bryt; English: Covenant) | `term_plus_after` | `בריתו` (brytw) | `word` | 17 | Ex 2:24; Deut 4:13; Deut 8:18; Deut 17:2; 2 Kings 13:23 |
| 74 | MT_WLC | `ברית` (bryt; English: Covenant) | `term_plus_after` | `בריתו` (brytw) | `word` | 17 | Exod 2:24; Deut 4:13; Deut 8:18; Deut 17:2; 2Kgs 13:23 |
| 21 | KJV | `bear` | `term_plus_after` | `beard` | `word` | 16 | LEV 13:29; LEV 13:30; LEV 14:9; LEV 19:27; LEV 21:5 |
| 74 | UHB | `ברית` (bryt; English: Covenant) | `term_plus_after` | `בריתו` (brytw) | `word` | 10 | DEU 17:2; 2KI 13:23; 1CH 16:15; PSA 25:10; PSA 55:20 |
| 74 | MAM | `ברית` (bryt; English: Covenant) | `term_plus_after` | `בריתו` (brytw) | `word` | 10 | Deut 17:2; 2 Kgs 13:23; Ps 25:10; Ps 55:21; Ps 103:18 |
| 74 | EBIBLE_WLC | `ברית` (bryt; English: Covenant) | `term_plus_after` | `בריתו` (brytw) | `word` | 10 | DEU 17:2; 2KI 13:23; 1CH 16:15; PSA 25:10; PSA 55:21 |
| 77 | UXLC | `חכמה` (chkmh; English: Wisdom) | `before_plus_term` | `וחכמה` (wchkmh) | `word` | 6 | Prov 10:23; Eccl 9:10; Dan 1:17; Dan 5:11; Dan 5:14 |
| 77 | UHB | `חכמה` (chkmh; English: Wisdom) | `before_plus_term` | `וחכמה` (wchkmh) | `word` | 6 | 2CH 9:22; PRO 10:23; ECC 9:10; DAN 1:17; DAN 5:11 |
| 77 | MT_WLC | `חכמה` (chkmh; English: Wisdom) | `before_plus_term` | `וחכמה` (wchkmh) | `word` | 6 | Prov 10:23; Eccl 9:10; Dan 1:17; Dan 5:11; Dan 5:14 |
| 77 | MAM | `חכמה` (chkmh; English: Wisdom) | `before_plus_term` | `וחכמה` (wchkmh) | `word` | 6 | Prov 10:23; Eccl 9:10; Dan 1:17; Dan 5:11; Dan 5:14 |
| 77 | EBIBLE_WLC | `חכמה` (chkmh; English: Wisdom) | `before_plus_term` | `וחכמה` (wchkmh) | `word` | 6 | 2CH 9:22; PRO 10:23; ECC 9:10; DAN 1:17; DAN 5:11 |
| 50 | UXLC | `אמרי` (mry; English: Amorite) | `term_plus_after` | `אמריו` (mryw) | `word` | 4 | Prov 17:27; Job 22:22; Job 32:12; Job 34:37 |
| 50 | UHB | `אמרי` (mry; English: Amorite) | `term_plus_after` | `אמריו` (mryw) | `word` | 4 | JOB 22:22; JOB 32:12; JOB 34:37; PRO 17:27 |
| 50 | MT_WLC | `אמרי` (mry; English: Amorite) | `term_plus_after` | `אמריו` (mryw) | `word` | 4 | Prov 17:27; Job 22:22; Job 32:12; Job 34:37 |
| 50 | MAM | `אמרי` (mry; English: Amorite) | `term_plus_after` | `אמריו` (mryw) | `word` | 4 | Prov 17:27; Job 22:22; Job 32:12; Job 34:37 |
| 50 | EBIBLE_WLC | `אמרי` (mry; English: Amorite) | `term_plus_after` | `אמריו` (mryw) | `word` | 4 | JOB 22:22; JOB 32:12; JOB 34:37; PRO 17:27 |
| 50 | UXLC | `אמרי` (mry; English: Amorite) | `before_plus_term` | `מאמרי` (mmry) | `word` | 3 | Prov 4:5; Prov 5:7; Prov 19:27 |
| 50 | MT_WLC | `אמרי` (mry; English: Amorite) | `before_plus_term` | `מאמרי` (mmry) | `word` | 3 | Prov 4:5; Prov 5:7; Prov 19:27 |
| 52 | UXLC | `אריה` (ryh; English: Lion) | `before_plus_term` | `ואריה` (wryh) | `word` | 2 | Isa 11:7; Isa 65:25 |
| 52 | UHB | `אריה` (ryh; English: Lion) | `before_plus_term` | `ואריה` (wryh) | `word` | 2 | ISA 11:7; ISA 65:25 |
| 52 | MT_WLC | `אריה` (ryh; English: Lion) | `before_plus_term` | `ואריה` (wryh) | `word` | 2 | Isa 11:7; Isa 65:25 |
| 52 | MAM | `אריה` (ryh; English: Lion) | `before_plus_term` | `ואריה` (wryh) | `word` | 2 | Isa 11:7; Isa 65:25 |
| 52 | EBIBLE_WLC | `אריה` (ryh; English: Lion) | `before_plus_term` | `ואריה` (wryh) | `word` | 2 | ISA 11:7; ISA 65:25 |
| 45 | UHB | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `word` | 1 | DAN 5:19 |
| 71 | UHB | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `word` | 1 | DAN 5:19 |
| 45 | EBIBLE_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `word` | 1 | DAN 5:19 |
| 71 | EBIBLE_WLC | `יהוה` (YHWH; English: YHWH) | `before_plus_term` | `דיהוה` (dyhwh) | `word` | 1 | DAN 5:19 |

## Read

The extension lexicon is built from normalized surface words and phrases in
the same corpus. A row here means the same ELS lane can spell a larger
surface-attested token somewhere in that text. It does not mean the hidden
path appears openly at the center verse, and it does not replace controls.
