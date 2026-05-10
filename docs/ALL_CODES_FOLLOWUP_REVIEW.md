# All-Codes Follow-Up Review

Status: manual review packet, not a claim.

This combines the compact all-codes follow-up selection with reconstructed
letter paths. It keeps both categories visible: hidden-path-only rows and
the rarer rows where the hidden path is centered on, or near, related
surface wording.

## Run

| Field | Value |
| --- | --- |
| Local report build commit | recorded in local manifest only |
| Selection protocol | `protocols/all_codes_followup_selection.toml` |
| Letter-path protocol | `protocols/all_codes_followup_letter_paths.toml` |
| Selection rows | 80 |
| Path rows | 295 |
| Letter rows | 1,348 |
| Path mismatches | 0 |
| Rows with same-skip extensions | 66 |
| Rows with compound same-skip extensions | 12 |
| Extension rows | 676 |

For resumed protocol runs, this subreport can remain cached. The build
commit is recorded in the local manifest; the top-level
`reports/real_report_run/summary.md` records the current assembly commit.

## Counts

| Group | Count |
| --- | ---: |
| queue `english_screening` | 21 |
| queue `greek_screening` | 21 |
| queue `hebrew_screening` | 27 |
| queue `hebrew_theology` | 11 |
| status `center_verse_context_review` | 24 |
| status `hidden_path_review` | 9 |
| status `related_center_word_review` | 14 |
| status `span_context_review` | 22 |
| status `strongest_manual_review` | 11 |

| Review class | Rows |
| --- | ---: |
| `center_verse_contains_related_category` | 12 |
| `center_verse_contains_related_concept` | 3 |
| `center_verse_contains_term` | 9 |
| `hidden_path_only` | 9 |
| `related_surface_word_at_center_same_category` | 12 |
| `related_surface_word_at_center_same_concept` | 2 |
| `same_surface_word_at_center` | 11 |
| `span_contains_related_category` | 12 |
| `span_contains_related_concept` | 1 |
| `span_contains_term` | 9 |

## Review Rows

| Rank | Queue | Status | Term | Concept | Skip | Center | Center word | Corpora | Best extension | Note |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | english_screening | `strongest_manual_review` | `heth` | Heth | -2 | Acts 25:20 | `whether` | KJV |  | all_source; hidden term centered on same normalized surface word |
| 2 | english_screening | `strongest_manual_review` | `heth` | Heth | -2 | Deut 24:14 | `whether` | KJV | `hethy` (term_plus_after; KJV) | all_source; hidden term centered on same normalized surface word; compound same-skip extension `hethy` in KJV |
| 3 | english_screening | `strongest_manual_review` | `aids` | AIDS | -3 | Isa 47:7 | `saidst,` | KJV |  | all_source; hidden term centered on same normalized surface word |
| 4 | english_screening | `related_center_word_review` | `edom` | Edom | -2 | 1Chr 19:1 | `Ammon` | KJV | `a` (before_match; KJV) | all_source; center surface word is related by concept/category flag; adjacent same-skip extension `a` in KJV (before_match) |
| 5 | english_screening | `related_center_word_review` | `shem` | Shem | -2 | 1Chr 4:26 | `Hamuel` | KJV | `o` (before_match; KJV) | all_source; center surface word is related by concept/category flag; adjacent same-skip extension `o` in KJV (before_match) |
| 6 | english_screening | `related_center_word_review` | `seba` | Seba | -2 | 1Chr 4:28 | `Beer-sheba,` | KJV |  | all_source; center surface word is related by concept/category flag |
| 7 | english_screening | `center_verse_context_review` | `hand` | Hand | -2 | 1Chr 2:2 | `and` | KJV |  | all_source; center verse carries exact/related surface context |
| 8 | english_screening | `center_verse_context_review` | `heal` | Heal | -2 | 1Kgs 1:6 | `displeased` | KJV | `s` (after_match; KJV) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `s` in KJV (after_match) |
| 9 | english_screening | `center_verse_context_review` | `hand` | Hand | -2 | 1Kgs 3:6 | `according` | KJV | `hando` (term_plus_after; KJV) | all_source; center verse carries exact/related surface context; compound same-skip extension `hando` in KJV |
| 10 | english_screening | `center_verse_context_review` | `sign` | Sign | -2 | 1Chr 10:13 | `against` | KJV | `t` (before_match; KJV) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `t` in KJV (before_match) |
| 11 | english_screening | `center_verse_context_review` | `adar` | Adar | -2 | 1Chr 11:19 | `And` | KJV |  | all_source; center verse carries exact/related surface context |
| 12 | english_screening | `center_verse_context_review` | `adam` | Adam | -2 | 1Chr 12:31 | `and` | KJV |  | all_source; center verse carries exact/related surface context |
| 13 | english_screening | `span_context_review` | `lord` | Lord | -3 | 1Sam 30:24 | `who` | KJV | `ho` (after_match; KJV) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `ho` in KJV (after_match) |
| 14 | english_screening | `span_context_review` | `lord` | Lord | -3 | 1Sam 30:24 | `who` | KJV | `ho` (after_match; KJV) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `ho` in KJV (after_match) |
| 15 | english_screening | `span_context_review` | `isis` | ISIS | -3 | Josh 15:19 | `springs.` | KJV | `s` (before_match; KJV) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `s` in KJV (before_match) |
| 16 | english_screening | `span_context_review` | `adar` | Adar | -2 | 1Sam 15:14 | `And` | KJV |  | all_source; start-to-end span carries exact/related surface context |
| 17 | english_screening | `span_context_review` | `mash` | Mash | -2 | 1Sam 28:18 | `day.` | KJV | `or` (before_match; KJV) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `or` in KJV (before_match) |
| 18 | english_screening | `span_context_review` | `adam` | Adam | -2 | 1Sam 9:22 | `And` | KJV | `t` (after_match; KJV) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `t` in KJV (after_match) |
| 19 | english_screening | `hidden_path_review` | `heal` | Heal | -2 | 1Chr 10:11 | `Jabesh-gilead` | KJV | `iheal` (before_plus_term; KJV) | all_source; no surface echo required; paths audited in 1 corpora; compound same-skip extension `iheal` in KJV |
| 20 | english_screening | `hidden_path_review` | `cush` | Cush | -2 | 1Chr 10:4 | `these` | KJV | `ur` (before_match; KJV) | all_source; no surface echo required; paths audited in 1 corpora; adjacent same-skip extension `ur` in KJV (before_match) |
| 21 | english_screening | `hidden_path_review` | `bear` | Bear | 2 | 1Chr 11:8 | `repaired` | KJV | `dobear` (before_plus_term; KJV) | all_source; no surface echo required; paths audited in 1 corpora; compound same-skip extension `dobear` in KJV |
| 22 | greek_screening | `strongest_manual_review` | `νατο` (nato; English: NATO) | NATO | 8 | Rom 5:10 | `θανάτου` (thanatou) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `οο` (oo) (after_match; TR_NT) | all_source; hidden term centered on same normalized surface word; adjacent same-skip extension `οο` (oo) in TR_NT (after_match) |
| 23 | greek_screening | `strongest_manual_review` | `ναοσ` (naos; English: Temple) | Temple | -9 | Matt 23:17 | `ναὸς` (naos; English: temple) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `α` (a) (after_match; SBLGNT) | all_source; hidden term centered on same normalized surface word; adjacent same-skip extension `α` (a) in SBLGNT (after_match) |
| 24 | greek_screening | `strongest_manual_review` | `αιμα` (haima; English: Blood) | Blood | -10 | Rev 19:13 | `αἵματι` (aimati) | BYZ_NT,SBLGNT,TCG_NT,TR_NT |  | all_source; hidden term centered on same normalized surface word |
| 25 | greek_screening | `related_center_word_review` | `λουδ` (loud; English: Lud) | Lud | -2 | Phil 2:7 | `δούλου` (doulou) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `ηρ` (er) (after_match; TR_NT) | all_source; center surface word is related by concept/category flag; adjacent same-skip extension `ηρ` (er) in TR_NT (after_match) |
| 26 | greek_screening | `related_center_word_review` | `ιωυαν` (Iouan; English: Javan) | Javan | -2 | 1Pet 5:13 | `Βαβυλῶνι` (babuloni) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `ηα` (ea) (after_match; TR_NT) | all_source; center surface word is related by concept/category flag; adjacent same-skip extension `ηα` (ea) in TR_NT (after_match) |
| 27 | greek_screening | `related_center_word_review` | `ευαλ` (eual; English: Obal) | Obal | -3 | 1Tim 5:14 | `Βούλομαι` (boulomai) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `σε` (se) (before_match; TR_NT) | all_source; center surface word is related by concept/category flag; adjacent same-skip extension `σε` (se) in TR_NT (before_match) |
| 28 | greek_screening | `center_verse_context_review` | `δασα` (dasa; English: Lasha) | Lasha | -2 | Acts 9:11 | `Ταρσέα` (tarsea) | BYZ_NT,SBLGNT,TCG_NT,TR_NT |  | all_source; center verse carries exact/related surface context |
| 29 | greek_screening | `center_verse_context_review` | `αιμα` (haima; English: Blood) | Blood | 2 | Matt 13:55 | `Μαριάμ` (mariam) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `τι` (ti) (before_match; TR_NT) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `τι` (ti) in TR_NT (before_match) |
| 30 | greek_screening | `center_verse_context_review` | `αιμα` (haima; English: Blood) | Blood | 2 | Matt 13:55 | `Μαριάμ` (mariam) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `τι` (ti) (before_match; TR_NT) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `τι` (ti) in TR_NT (before_match) |
| 31 | greek_screening | `center_verse_context_review` | `ναοσ` (naos; English: Temple) | Temple | 2 | 1Cor 10:16 | `τοῦ` (tou) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `υιον` (uion) (before_match; SBLGNT) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `υιον` (uion) in SBLGNT (before_match) |
| 32 | greek_screening | `center_verse_context_review` | `κινα` (kina; English: China) | China | 2 | 1John 2:1 | `δίκαιον` (dikaion) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `α` (a) (after_match; SBLGNT) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `α` (a) in SBLGNT (after_match) |
| 33 | greek_screening | `center_verse_context_review` | `ελκη` (elke; English: Boils) | Boils | 2 | 1Pet 5:13 | `συνεκλεκτή` (suneklekte) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `α` (a) (after_match; SBLGNT) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `α` (a) in SBLGNT (after_match) |
| 34 | greek_screening | `span_context_review` | `θεοσ` (theos; English: God) | God | 2 | Rom 14:2 | `ἐσθίει` (esthiei) | BYZ_NT,SBLGNT,TCG_NT,TR_NT |  | all_source; start-to-end span carries exact/related surface context |
| 35 | greek_screening | `span_context_review` | `ιραν` (iran; English: Iran) | Iran | -4 | Mark 14:48 | `ἀποκριθεὶς` (apokritheis) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `εση` (ese) (before_match; TR_NT) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `εση` (ese) in TR_NT (before_match) |
| 36 | greek_screening | `span_context_review` | `νατο` (nato; English: NATO) | NATO | 7 | 1Cor 1:27 | `μωρὰ` (mora) | BYZ_NT,SBLGNT,TCG_NT,TR_NT |  | all_source; start-to-end span carries exact/related surface context |
| 37 | greek_screening | `span_context_review` | `σαλα` (Sala; English: Shelah) | Shelah | 2 | Acts 7:42 | `Ἰσραήλ` (israel) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `α` (a) (after_match; SBLGNT) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `α` (a) in SBLGNT (after_match) |
| 38 | greek_screening | `span_context_review` | `αδαμ` (adam; English: Adam) | Adam | 2 | Gal 4:27 | `ἄνδρα` (andra) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `ο` (o) (before_match; TR_NT) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `ο` (o) in TR_NT (before_match) |
| 39 | greek_screening | `span_context_review` | `γαμερ` (gamer; English: Gomer) | Gomer | -3 | 2Cor 10:3 | `στρατευόμεθα` (strateuometha) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `αο` (ao) (before_match; TR_NT) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `αο` (ao) in TR_NT (before_match) |
| 40 | greek_screening | `hidden_path_review` | `σαλα` (Sala; English: Shelah) | Shelah | 2 | 1Cor 10:18 | `Ἰσραὴλ` (israel) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `α` (a) (after_match; SBLGNT) | all_source; no surface echo required; paths audited in 4 corpora; adjacent same-skip extension `α` (a) in SBLGNT (after_match) |
| 41 | greek_screening | `hidden_path_review` | `αμην` (amen; English: Amen) | Amen | 2 | 1Cor 1:10 | `μὴ` (me) | BYZ_NT,SBLGNT,TCG_NT,TR_NT |  | all_source; no surface echo required; paths audited in 4 corpora |
| 42 | greek_screening | `hidden_path_review` | `υιοσ` (huios; English: Son) | Son | 2 | 1Cor 5:12 | `τοὺς` (tous) | BYZ_NT,SBLGNT,TCG_NT,TR_NT | `εν` (en) (before_match; TR_NT) | all_source; no surface echo required; paths audited in 4 corpora; adjacent same-skip extension `εν` (en) in TR_NT (before_match) |
| 43 | hebrew_screening | `strongest_manual_review` | `שממה` (shmmh; English: Desolation) | Desolation | 2 | Mic 1:7 | `שְׁמָמָ֑ה` (shmmh) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `עבה` (bh) (before_match; UXLC) | all_source; hidden term centered on same normalized surface word; adjacent same-skip extension `עבה` (bh) in UXLC (before_match) |
| 44 | hebrew_screening | `strongest_manual_review` | `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 1Chr 26:27 | `יְהוָֽה׃` (yhwh) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `הילק` (hylq) (before_match; UXLC) | all_source; hidden term centered on same normalized surface word; adjacent same-skip extension `הילק` (hylq) in UXLC (before_match) |
| 45 | hebrew_screening | `strongest_manual_review` | `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 1Chr 28:20 | `יְהוָֽה׃` (yhwh) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `עדיהוה` (dyhwh) (before_plus_term; UXLC) | all_source; hidden term centered on same normalized surface word; compound same-skip extension `עדיהוה` (dyhwh) in UXLC |
| 46 | hebrew_screening | `related_center_word_review` | `רומא` (rwm; English: Rome) | Rome | 5 | Job 5:12 | `עֲרוּמִ֑ים` (rwmym) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `שלומי` (shlwmy) (before_match; UXLC) | all_source; center surface word is related by concept/category flag; adjacent same-skip extension `שלומי` (shlwmy) in UXLC (before_match) |
| 47 | hebrew_screening | `related_center_word_review` | `רומא` (rwm; English: Rome) | Rome | -42 | Eccl 10:6 | `בַּמְּרוֹמִ֖ים` (bmrwmym) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `לי` (ly) (after_match; UXLC) | all_source; center surface word is related by concept/category flag; adjacent same-skip extension `לי` (ly) in UXLC (after_match) |
| 48 | hebrew_screening | `related_center_word_review` | `גרמניה` (grmnyh; English: Germany) | Germany | -18 | Jer 42:15 | `מִצְרַ֔יִם` (mtsrym) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `ערש` (rsh) (after_match; UXLC) | all_source; center surface word is related by concept/category flag; adjacent same-skip extension `ערש` (rsh) in UXLC (after_match) |
| 49 | hebrew_screening | `related_center_word_review` | `אמרי` (mry; English: Amorite) | Amorite | -2 | 1Chr 15:22 | `בַּמַּשָּׂ֔א` (bmsh) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `שבי` (shby) (after_match; UXLC) | all_source; center surface word is related by concept/category flag; adjacent same-skip extension `שבי` (shby) in UXLC (after_match) |
| 50 | hebrew_screening | `related_center_word_review` | `אמרי` (mry; English: Amorite) | Amorite | 2 | 1Chr 15:27 | `הַמְשֹֽׁרְרִ֑ים` (hmshrrym) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `אמריו` (mryw) (term_plus_after; UXLC) | all_source; center surface word is related by concept/category flag; compound same-skip extension `אמריו` (mryw) in UXLC |
| 51 | hebrew_screening | `center_verse_context_review` | `ביבי` (byby; English: Bibi) | Bibi | -2 | 1Chr 2:55 | `ישבו` (yshbw) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `יפתח` (yptch) (after_match; UXLC) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `יפתח` (yptch) in UXLC (after_match) |
| 52 | hebrew_screening | `center_verse_context_review` | `אריה` (ryh; English: Lion) | Lion | 2 | 1Kgs 13:26 | `אִ֣ישׁ` (ysh) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `ואריה` (wryh) (before_plus_term; UXLC) | all_source; center verse carries exact/related surface context; compound same-skip extension `ואריה` (wryh) in UXLC |
| 53 | hebrew_screening | `center_verse_context_review` | `אדני` (Adonai; English: Lord) | Lord | -2 | 1Kgs 20:9 | `בֶן־הֲדַ֗ד` (bnhdd) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `אדניאמר` (dnymr) (term_plus_after; UXLC) | all_source; center verse carries exact/related surface context; compound same-skip extension `אדניאמר` (dnymr) in UXLC |
| 54 | hebrew_screening | `center_verse_context_review` | `רומי` (rwmy; English: Rome) | Rome | -6 | 1Kgs 7:40 | `וְאֶת־הַמִּזְרָק֑וֹת` (wthmzrqwt) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `שמת` (shmt) (before_match; UXLC) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `שמת` (shmt) in UXLC (before_match) |
| 55 | hebrew_screening | `center_verse_context_review` | `רומי` (rwmy; English: Rome) | Rome | 6 | Josh 22:5 | `אֶתְכֶם֮` (tkm) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `תו` (tav; English: mark/sign) (before_match; UXLC) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `תו` (tav; English: mark/sign) in UXLC (before_match) |
| 56 | hebrew_screening | `center_verse_context_review` | `תתתתתא` (ttttt; English: Gregorian 2001) | Gregorian 2001 | 11 | Ezek 7:8 | `עָלַ֔יִךְ` (lyk) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `עבה` (bh) (after_match; UXLC) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `עבה` (bh) in UXLC (after_match) |
| 57 | hebrew_screening | `center_verse_context_review` | `מותשני` (mwtshny; English: Second Death) | Second Death | 9 | Jer 43:3 | `בָּבֶֽל׃` (bbl) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `להר` (lhr) (after_match; UXLC) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `להר` (lhr) in UXLC (after_match) |
| 58 | hebrew_screening | `center_verse_context_review` | `מותשני` (mwtshny; English: Second Death) | Second Death | -11 | Num 29:29 | `אַרְבָּעָ֥ה` (rbh) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `אפי` (py) (before_match; UXLC) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `אפי` (py) in UXLC (before_match) |
| 59 | hebrew_screening | `center_verse_context_review` | `טימותי` (tymwty; English: Timothy) | Timothy | 16 | Gen 30:20 | `אֶת־שְׁמ֖וֹ` (tshmw) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `או` (w) (after_match; UXLC) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `או` (w) in UXLC (after_match) |
| 60 | hebrew_screening | `span_context_review` | `שמימ` (shmym; English: Heaven) | Heaven | 2 | Judg 19:3 | `וַיָּ֨קָם` (wyqm) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `יהי` (yhy) (after_match; UXLC) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `יהי` (yhy) in UXLC (after_match) |
| 61 | hebrew_screening | `span_context_review` | `שמימ` (shmym; English: Heaven) | Heaven | 2 | Neh 3:1 | `וַיָּ֡קָם` (wyqm) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `ובר` (wbr) (before_match; UXLC) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `ובר` (wbr) in UXLC (before_match) |
| 62 | hebrew_screening | `span_context_review` | `מרימ` (mrym; English: Mary) | Mary | -3 | Mic 6:5 | `זְכָר־נָא֙` (zkrn) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `מרה` (mrh) (after_match; UXLC) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `מרה` (mrh) in UXLC (after_match) |
| 63 | hebrew_screening | `span_context_review` | `תתתתתא` (ttttt; English: Gregorian 2001) | Gregorian 2001 | 35 | Eccl 3:10 | `לַעֲנ֥וֹת` (lnwt) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `מאותו` (mwtw) (before_match; UXLC) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `מאותו` (mwtw) in UXLC (before_match) |
| 64 | hebrew_screening | `span_context_review` | `פתרסימ` (ptrsym; English: Pathrusim) | Pathrusim | -52 | Isa 26:17 | `תִּזְעַ֖ק` (tzq) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `עכנ` (kn) (before_match; UXLC) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `עכנ` (kn) in UXLC (before_match) |
| 65 | hebrew_screening | `span_context_review` | `טימותי` (tymwty; English: Timothy) | Timothy | -66 | Jer 46:28 | `יַֽעֲקֹב֙` (yqb) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `חלי` (chly) (before_match; UXLC) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `חלי` (chly) in UXLC (before_match) |
| 66 | hebrew_screening | `span_context_review` | `תתתתתכז` (tttttkz; English: Gregorian 2027 additive) | Gregorian 2027 additive | 86 | Deut 11:16 | `יִפְתֶּ֖ה` (ypth) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `שה` (shh) (after_match; UXLC) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `שה` (shh) in UXLC (after_match) |
| 67 | hebrew_screening | `hidden_path_review` | `יומיהוה` (yom YHWH; English: Day Of The Lord) | Day Of The Lord | 4 | Song 4:6 | `שֶׁיָּפ֨וּחַ֙` (shypwch) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `היומיהוה` (hayom YHWH; English: the day of YHWH) (before_plus_term; UXLC) | all_source; no surface echo required; paths audited in 5 corpora; compound same-skip extension `היומיהוה` (hayom YHWH; English: the day of YHWH) in UXLC |
| 68 | hebrew_screening | `hidden_path_review` | `קברריק` (qbrryq; English: Empty Tomb) | Empty Tomb | 8 | Ezek 5:2 | `בְּת֣וֹךְ` (btwk) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `שרית` (shryt) (after_match; UXLC) | all_source; no surface echo required; paths audited in 5 corpora; adjacent same-skip extension `שרית` (shryt) in UXLC (after_match) |
| 69 | hebrew_screening | `hidden_path_review` | `הצהרישומושלמ` (htshryshwmwshlm; English: Jesus Declared Perfect) | Jesus Declared Perfect | 9 | Gen 22:8 | `לְעֹלָ֖ה` (llh) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | all_source; no surface echo required; paths audited in 5 corpora |
| 70 | hebrew_theology | `strongest_manual_review` | `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 1Chr 26:27 | `יְהוָֽה׃` (yhwh) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `הילק` (hylq) (before_match; UXLC) | all_source; hidden term centered on same normalized surface word; adjacent same-skip extension `הילק` (hylq) in UXLC (before_match) |
| 71 | hebrew_theology | `strongest_manual_review` | `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 1Chr 28:20 | `יְהוָֽה׃` (yhwh) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `עדיהוה` (dyhwh) (before_plus_term; UXLC) | all_source; hidden term centered on same normalized surface word; compound same-skip extension `עדיהוה` (dyhwh) in UXLC |
| 72 | hebrew_theology | `related_center_word_review` | `תורה` (twrh; English: Torah) | Torah | 7 | 1Chr 5:1 | `בֶּן־יִשְׂרָאֵ֑ל` (bnyshrl) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | all_source; center surface word is related by concept/category flag |
| 73 | hebrew_theology | `related_center_word_review` | `תורה` (twrh; English: Torah) | Torah | -7 | 2Kgs 17:20 | `יִשְׂרָאֵל֙` (Yisrael; English: Israel) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `ואח` (wch) (after_match; UXLC) | all_source; center surface word is related by concept/category flag; adjacent same-skip extension `ואח` (wch) in UXLC (after_match) |
| 74 | hebrew_theology | `related_center_word_review` | `ברית` (bryt; English: Covenant) | Covenant | 8 | Deut 34:9 | `חָכְמָ֔ה` (chkmh) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `בריתו` (brytw) (term_plus_after; UXLC) | all_source; center surface word is related by concept/category flag; compound same-skip extension `בריתו` (brytw) in UXLC |
| 75 | hebrew_theology | `center_verse_context_review` | `אהבה` (hbh; English: Love) | Love | 2 | 2Sam 14:21 | `הַדָּבָ֣ר` (hdbr) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `הלהב` (hlhb) (after_match; UXLC) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `הלהב` (hlhb) in UXLC (after_match) |
| 76 | hebrew_theology | `center_verse_context_review` | `אהבה` (hbh; English: Love) | Love | 2 | 2Sam 15:27 | `שֻׁ֥בָה` (shbh) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `יבל` (ybl) (after_match; UXLC) | all_source; center verse carries exact/related surface context; adjacent same-skip extension `יבל` (ybl) in UXLC (after_match) |
| 77 | hebrew_theology | `center_verse_context_review` | `חכמה` (chkmh; English: Wisdom) | Wisdom | 3 | Isa 49:8 | `כֹּ֣ה` (kh) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `וחכמה` (wchkmh) (before_plus_term; UXLC) | all_source; center verse carries exact/related surface context; compound same-skip extension `וחכמה` (wchkmh) in UXLC |
| 78 | hebrew_theology | `span_context_review` | `משיח` (Mashiach; English: Messiah) | Messiah | 6 | Ezra 2:5 | `וְשִׁבְעִֽים׃` (wshbym) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `שבנא` (shbn) (before_match; UXLC) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `שבנא` (shbn) in UXLC (before_match) |
| 79 | hebrew_theology | `span_context_review` | `משיח` (Mashiach; English: Messiah) | Messiah | 6 | Neh 7:10 | `וּשְׁנָֽיִם׃` (wshnym) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `לובו` (lwbw) (after_match; UXLC) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `לובו` (lwbw) in UXLC (after_match) |
| 80 | hebrew_theology | `span_context_review` | `ברית` (bryt; English: Covenant) | Covenant | -10 | Prov 30:4 | `עָלָֽה־שָׁמַ֨יִם` (lhshmym) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC | `דא` (d) (after_match; UXLC) | all_source; start-to-end span carries exact/related surface context; adjacent same-skip extension `דא` (d) in UXLC (after_match) |

## Read

These rows are a human-review work queue. The strongest manual-review
subtype is `center_word_exact`, where the hidden word is centered on the
same normalized surface word. Related center-word, center-verse, and
span-context rows are weaker but still useful for review. Hidden-path-only
rows stay in the packet because an open-text echo is not required for an
ELS candidate.

Same-skip extension rows show that a hidden lane can be extended into a
surface-attested word or phrase. Compound extensions contain the hidden
term plus adjacent before/after letters. Adjacent-only extensions are
logged but weaker because they do not contain the hidden term.

This report does not add statistical support. It packages rows for
inspection after the broad screen.
