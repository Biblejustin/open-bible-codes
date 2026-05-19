# MT-LXX Reciprocal Presence

This report compares concept-level ELS presence between one Hebrew MT
corpus and one Greek LXX corpus. Because MT and LXX differ by language,
alphabet, text length, translation choices, and sometimes verse alignment,
this is not a same-letter or same-skip comparison. The comparison unit is
concept + aligned center verse/chapter.

## Scope

- Hebrew corpus: `MT_WLC=configs/example_oshb_wlc.toml`
- LXX corpus: `LXX=configs/example_ebible_grclxx.toml`
- Skip range: `2..100`
- Direction: `both`
- Minimum normalized term length: `3`
- Max hits per term per corpus: `100`
- Term files: `terms/theological_terms.csv, terms/prophetic_terms.csv, terms/biblical_tribes.csv, terms/biblical_festivals.csv, terms/biblical_calendar.csv, terms/biblical_narrative_names.csv, terms/biblical_prophets_cohort.csv, terms/eschatology_expanded_terms.csv, terms/isaiah53_servant_cohort.csv, terms/tabernacle_temple_terms.csv, terms/daniel_statue_metals.csv, terms/maccabean_apocrypha_names.csv, terms/frequency_anchors.csv, terms/null_controls.csv`

## Concept Presence Classes

| Class | Concepts |
| --- | ---: |
| `mt_lxx_common_verse` | 30 |
| `mt_lxx_common_chapter` | 93 |
| `both_present_different_loci` | 51 |
| `mt_only_lxx_absent` | 83 |
| `lxx_only_mt_absent` | 20 |
| `absent_both_in_capped_scan` | 80 |

## Hit Counterpart Status

| Status | Hits |
| --- | ---: |
| `alignment_broken_chapter` | 3250 |
| `alignment_broken_verse` | 1181 |
| `lxx_mt_common` | 855 |
| `lxx_only_mt_absent` | 8390 |
| `mt_lxx_common` | 949 |
| `mt_only_lxx_absent` | 19987 |

## Concepts Needing Review

| Concept | Hebrew | Greek | MT hits | LXX hits | Common verses | Common chapters | Class | Read |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| Asher | `אשר` (shr; English: Asher) | `ασηρ` (aser; English: Asher) | 100 | 100 | 1 | 11 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Bashan | `בשן` (bshn; English: Bashan) | `βασαν` (basan; English: Bashan) | 100 | 100 | 1 | 7 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Bride | `כלה` (klh; English: Bride) | `νυμφη` (numphe; English: Bride) | 100 | 18 | 1 | 1 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Carus | `קרוס` (qrws; English: Carus) | `καρος` (karos; English: Carus) | 100 | 100 | 1 | 6 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Day | `יום` (ywm; English: Day) | `ημερα` (emera; English: Day) | 100 | 100 | 1 | 9 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Edom | `אדום` (dwm; English: Edom) | `εδωμ` (edom; English: Edom) | 100 | 100 | 1 | 10 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Elijah | `אליהו` (lyhw; English: Elijah) | `ηλιας` (elias; English: Elijah) | 100 | 100 | 1 | 7 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Eve | `חוה` (chwh; English: Eve) | `ευα` (eua; English: Eve) | 100 | 100 | 1 | 7 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Flesh | `בשר` (bshr; English: Flesh) | `σαρξ` (sarx; English: Flesh) | 100 | 100 | 1 | 8 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Geta | `גטה` (gth; English: Geta) | `γετας` (getas; English: Geta) | 100 | 100 | 1 | 8 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Hannah | `חנה` (chnh; English: Hannah) | `αννα` (anna; English: Hannah) | 100 | 100 | 1 | 9 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Haran | `חרן` (chrn; English: Haran) | `χαραν` (charan; English: Haran) | 100 | 100 | 1 | 6 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Hosea | `הושע` (hwsh; English: Hosea) | `ωσηε` (osee; English: Hosea) | 100 | 100 | 1 | 11 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| House | `בית` (byt; English: House) | `οικος` (oikos; English: House) | 100 | 100 | 2 | 7 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 2 shared verse ref(s) |
| Image | `צלם` (tslm; English: Image) | `εικων` (eikon; English: Image) | 100 | 100 | 1 | 6 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Joel | `יואל` (ywl; English: Joel) | `ιωηλ` (ioel; English: Joel) | 100 | 100 | 1 | 7 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Judah | `יהודה` (Yehudah; English: Judah) | `ιουδα` (iouda; English: Judah) | 100 | 100 | 1 | 6 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Key | `מפתח` (mptch; English: Key) | `κλεις` (kleis; English: Key) | 100 | 100 | 1 | 9 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Law | `תורה` (twrh; English: Law) | `νομος` (nomos; English: Law) | 100 | 100 | 1 | 10 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Media | `מדי` (Madai; English: Media) | `μηδια` (media; English: Media) | 100 | 100 | 1 | 8 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Nahum | `נחום` (nchwm; English: Nahum) | `ναουμ` (naoum; English: Nahum) | 100 | 100 | 1 | 8 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Rome | `רומי` (rwmy; English: Rome); `רומא` (rwm; English: Rome) | `ρωμη` (rome; English: Rome) | 200 | 100 | 2 | 21 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 2 shared verse ref(s) |
| Saint | `קדוש` (qdwsh; English: Saint) | `αγιος` (agios; English: Saint) | 100 | 100 | 1 | 6 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Sarah | `שרה` (shrh; English: Sarah) | `σαρρα` (sarra; English: Sarah) | 100 | 100 | 1 | 7 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Servant | `עבד` (eved; English: Servant) | `παις` (pais; English: Servant) | 100 | 100 | 1 | 10 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Sores | `מכות` (mkwt; English: Sores) | `ελκη` (elke; English: Sores) | 100 | 100 | 1 | 10 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Tabernacle | `משכן` (mshkn; English: Tabernacle) | `σκηνη` (skene; English: Tabernacle) | 100 | 100 | 1 | 4 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Tyre | `צר` (tsar; English: Tyre); `צור` (tswr; English: Tyre) | `τυρος` (turos; English: Tyre) | 100 | 100 | 1 | 7 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| Vision | `חזון` (chazon; English: Vision) | `ορασις` (orasis; English: Vision) | 100 | 100 | 2 | 8 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 2 shared verse ref(s) |
| Word | `דבר` (davar; English: Word) | `λογος` (logos; English: Word) | 100 | 100 | 1 | 3 | `mt_lxx_common_verse` | concept has reciprocal MT/LXX ELS centers in 1 shared verse ref(s) |
| 666 | `שש מאות ששים ושש` (shshmwtshshymwshsh; English: 666); `666`; `תרו` (trw; English: 666) | `εξακοσιοι εξηκοντα εξ` (exakosioiexekontaex; English: 666); `χξς` (chxs; English: 666); `χξϛ` (chx; English: 666) | 100 | 100 | 0 | 3 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 3 shared chapter(s) |
| Abraham | `אברהם` (brhm; English: Abraham) | `αβρααμ` (abraam; English: Abraham) | 100 | 6 | 0 | 2 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 2 shared chapter(s) |
| Adam | `אדם` (dm; English: Adam) | `αδαμ` (adam; English: Adam) | 100 | 100 | 0 | 11 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 11 shared chapter(s) |
| Ahab | `אחאב` (chb; English: Ahab) | `αχααβ` (achaab; English: Ahab) | 100 | 67 | 0 | 2 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 2 shared chapter(s) |
| Amen | `אמן` (mn; English: Amen) | `αμην` (amen; English: Amen) | 100 | 100 | 0 | 10 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 10 shared chapter(s) |
| Ammon | `עמון` (mwn; English: Ammon) | `αμμων` (ammon; English: Ammon) | 100 | 100 | 0 | 8 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 8 shared chapter(s) |
| Amos | `עמוס` (mws; English: Amos) | `αμως` (amos; English: Amos) | 100 | 100 | 0 | 5 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 5 shared chapter(s) |
| Assyria | `אשור` (shwr; English: Assyria) | `ασσυρια` (assuria; English: Assyria) | 100 | 14 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Athens | `אתונה` (twnh; English: Athens) | `αθηναι` (athenai; English: Athens) | 100 | 49 | 0 | 4 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 4 shared chapter(s) |
| Boils | `שחין` (shchyn; English: Boils) | `ελκη` (elke; English: Boils) | 100 | 100 | 0 | 11 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 11 shared chapter(s) |
| Bronze | `נחשת` (nechoshet; English: Bronze) | `χαλκος` (chalkos; English: Bronze) | 100 | 4 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Canaan | `כנען` (knn; English: Canaan) | `χανααν` (chanaan; English: Canaan) | 100 | 42 | 0 | 4 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 4 shared chapter(s) |
| Clay | `חרס` (chrs; English: Clay) | `πηλος` (pelos; English: Clay) | 100 | 100 | 0 | 7 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 7 shared chapter(s) |
| Cyrus | `כורש` (Koresh; English: Cyrus) | `κυρος` (kuros; English: Cyrus) | 100 | 100 | 0 | 8 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 8 shared chapter(s) |
| Darkness | `חשך` (chshk; English: Darkness) | `σκοτος` (skotos; English: Darkness) | 100 | 100 | 0 | 8 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 8 shared chapter(s) |
| Darkness Plague | `חושך` (chwshk; English: Darkness Plague) | `σκοτος` (skotos; English: Darkness Plague) | 100 | 100 | 0 | 12 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 12 shared chapter(s) |
| David | `דוד` (David; English: David) | `δαυιδ` (dauid; English: David) | 100 | 100 | 0 | 7 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 7 shared chapter(s) |
| Death | `מות` (mavet; English: Death) | `θανατος` (thanatos; English: Death) | 100 | 4 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Earthquake | `רעש` (rsh; English: Earthquake) | `σεισμος` (seismos; English: Earthquake) | 100 | 3 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Elam | `עילם` (ylm; English: Elam) | `ελαμ` (Elam; English: Elam) | 100 | 100 | 0 | 7 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 7 shared chapter(s) |
| Ephraim | `אפרים` (prym; English: Ephraim) | `εφραιμ` (ephraim; English: Ephraim) | 100 | 5 | 0 | 2 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 2 shared chapter(s) |
| Esther | `אסתר` (str; English: Esther) | `εσθηρ` (esther; English: Esther) | 100 | 91 | 0 | 9 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 9 shared chapter(s) |
| Faith | `אמונה` (mwnh; English: Faith) | `πιστις` (pistis; English: Faith) | 100 | 87 | 0 | 11 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 11 shared chapter(s) |
| Famine | `רעב` (rb; English: Famine) | `λιμος` (limos; English: Famine) | 100 | 100 | 0 | 7 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 7 shared chapter(s) |
| Gilead | `גלעד` (gld; English: Gilead) | `γαλααδ` (galaad; English: Gilead) | 100 | 9 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Glory | `כבוד` (kbwd; English: Glory) | `δοξα` (doxa; English: Glory) | 100 | 100 | 0 | 6 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 6 shared chapter(s) |
| God | `אלהים` (Elohim; English: God) | `θεος` (theos; English: God) | 100 | 100 | 0 | 8 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 8 shared chapter(s) |
| Grave | `קבר` (qever; English: Grave) | `ταφος` (taphos; English: Grave) | 100 | 100 | 0 | 5 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 5 shared chapter(s) |
| Greece | `יון` (Yavan; English: Greece) | `ελλας` (ellas; English: Greece) | 100 | 100 | 0 | 4 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 4 shared chapter(s) |
| Heaven | `שמים` (shamayim; English: Heaven) | `ουρανος` (ouranos; English: Heaven) | 100 | 7 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Heavens | `שמים` (shamayim; English: Heavens) | `ουρανος` (ouranos; English: Heavens) | 100 | 7 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Holy | `קדש` (qodesh; English: Holy) | `αγιος` (agios; English: Holy) | 100 | 100 | 0 | 6 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 6 shared chapter(s) |
| Horn | `קרן` (qeren; English: Horn) | `κερας` (keras; English: Horn) | 100 | 100 | 0 | 8 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 8 shared chapter(s) |
| Iniquity | `עון` (avon; English: Iniquity) | `ανομια` (anomia; English: Iniquity) | 100 | 100 | 0 | 7 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 7 shared chapter(s) |
| Isaac | `יצחק` (ytschq; English: Isaac) | `ισαακ` (Isaak; English: Isaac) | 100 | 100 | 0 | 6 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 6 shared chapter(s) |
| Isaiah | `ישעיהו` (yshyhw; English: Isaiah); `ישעיהו` (yshyhw; English: Isaiah) | `ησαιας` (esaias; English: Isaiah); `ησαιας` (esaias; English: Isaiah) | 96 | 200 | 0 | 3 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 3 shared chapter(s) |
| Israel | `ישראל` (Yisrael; English: Israel) | `ισραηλ` (israel; English: Israel) | 100 | 25 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Jacob | `יעקב` (Yaakov; English: Jacob) | `ιακωβ` (iakob; English: Jacob) | 100 | 83 | 0 | 10 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 10 shared chapter(s) |
| Jonah | `יונה` (ywnh; English: Jonah) | `ιωνας` (ionas; English: Jonah) | 100 | 100 | 0 | 6 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 6 shared chapter(s) |
| Joseph | `יוסף` (ywsp; English: Joseph) | `ιωσηφ` (ioseph; English: Joseph) | 100 | 40 | 0 | 3 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 3 shared chapter(s) |
| Joseph Tribe | `יוסף` (ywsp; English: Joseph Tribe) | `ιωσηφ` (ioseph; English: Joseph Tribe) | 100 | 40 | 0 | 3 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 3 shared chapter(s) |
| Joshua | `יהושע` (Yehoshua; English: Joshua) | `ιησους` (Iesous; English: Joshua) | 100 | 78 | 0 | 3 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 3 shared chapter(s) |
| Josiah | `יאשיהו` (yshyhw; English: Josiah) | `ιωσιας` (iosias; English: Josiah) | 100 | 100 | 0 | 14 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 14 shared chapter(s) |
| Judgment | `משפט` (mshpt; English: Judgment) | `κρισις` (krisis; English: Judgment) | 81 | 61 | 0 | 4 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 4 shared chapter(s) |
| Lawlessness | `און` (aven; English: Lawlessness) | `ανομια` (anomia; English: Lawlessness) | 100 | 100 | 0 | 11 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 11 shared chapter(s) |
| Leah | `לאה` (lh; English: Leah) | `λεια` (leia; English: Leah) | 100 | 100 | 0 | 6 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 6 shared chapter(s) |
| Levi | `לוי` (lwy; English: Levi) | `λευι` (leui; English: Levi) | 100 | 100 | 0 | 10 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 10 shared chapter(s) |
| Life | `חיים` (chyym; English: Life) | `ζωη` (zoe; English: Life) | 100 | 100 | 0 | 8 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 8 shared chapter(s) |
| Light | `אור` (or; English: Light) | `φως` (phos; English: Light) | 100 | 100 | 0 | 10 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 10 shared chapter(s) |
| Lion | `אריה` (ryh; English: Lion) | `λεων` (leon; English: Lion) | 100 | 100 | 0 | 13 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 13 shared chapter(s) |
| Locust | `ארבה` (rbh; English: Locust) | `ακρις` (akris; English: Locust) | 100 | 100 | 0 | 4 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 4 shared chapter(s) |
| Lord | `אדני` (Adonai; English: Lord) | `κυριος` (kyrios; English: Lord) | 100 | 35 | 0 | 4 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 4 shared chapter(s) |
| Love | `אהבה` (hbh; English: Love) | `αγαπη` (agape; English: Love) | 100 | 100 | 0 | 9 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 9 shared chapter(s) |
| Magog | `מגוג` (Magog; English: Magog) | `μαγωγ` (magog; English: Magog) | 100 | 16 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Mary | `מרים` (mrym; English: Mary) | `μαρια` (Maria; English: Mary) | 100 | 100 | 0 | 10 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 10 shared chapter(s) |
| Mercy | `חסד` (chesed; English: Mercy) | `ελεος` (eleos; English: Mercy) | 100 | 100 | 0 | 9 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 9 shared chapter(s) |
| Moab | `מואב` (mwb; English: Moab) | `μωαβ` (moab; English: Moab) | 100 | 100 | 0 | 11 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 11 shared chapter(s) |
| Nero | `נרון` (nrwn; English: Nero); `נרון` (nrwn; English: Nero) | `νερων` (neron; English: Nero); `νερων` (neron; English: Nero) | 200 | 200 | 0 | 10 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 10 shared chapter(s) |
| Nineveh | `נינוה` (Nineveh; English: Nineveh); `נינוה` (Nineveh; English: Nineveh) | `νινευη` (nineue; English: Nineveh) | 200 | 58 | 0 | 7 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 7 shared chapter(s) |
| Oil | `שמן` (shmn; English: Oil) | `ελαιον` (elaion; English: Oil) | 100 | 100 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Otho | `אותו` (wtw; English: Otho) | `οθων` (othon; English: Otho) | 100 | 100 | 0 | 10 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 10 shared chapter(s) |
| Overcome | `נצח` (ntsch; English: Overcome) | `νικαω` (nikao; English: Overcome) | 100 | 100 | 0 | 4 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 4 shared chapter(s) |
| Passover | `פסח` (Pesach; English: Passover) | `πασχα` (pascha; English: Passover) | 100 | 100 | 0 | 8 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 8 shared chapter(s) |
| Paul | `שאול` (shwl; English: Paul); `פאולוס` (pwlws; English: Paul) | `παυλος` (paulos; English: Paul) | 101 | 20 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Peace | `שלום` (shlwm; English: Peace) | `ειρηνη` (eirene; English: Peace) | 100 | 21 | 0 | 4 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 4 shared chapter(s) |
| Persia | `פרס` (Paras; English: Persia); `פרס חדשה` (prschdshh; English: Persia) | `περσις` (persis; English: Persia); `περσια` (persia; English: Persia) | 100 | 90 | 0 | 13 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 13 shared chapter(s) |
| Peter | `כיפא` (kyp; English: Peter); `פטרוס` (ptrws; English: Peter) | `πετρος` (Petros; English: Peter) | 100 | 24 | 0 | 3 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 3 shared chapter(s) |
| Pit | `בור` (bwr; English: Pit) | `φρεαρ` (phrear; English: Pit) | 100 | 41 | 0 | 2 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 2 shared chapter(s) |
| Plague | `מגפה` (mgph; English: Plague) | `πληγη` (plege; English: Plague) | 100 | 10 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Priest | `כהן` (khn; English: Priest) | `ιερευς` (iereus; English: Priest) | 100 | 76 | 0 | 8 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 8 shared chapter(s) |
| Rachel | `רחל` (rchl; English: Rachel) | `ραχηλ` (rachel; English: Rachel) | 100 | 12 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Ruth | `רות` (rwt; English: Ruth) | `ρουθ` (routh; English: Ruth) | 100 | 100 | 0 | 8 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 8 shared chapter(s) |
| Sacrifice | `זבח` (zbch; English: Sacrifice) | `θυσια` (thusia; English: Sacrifice) | 100 | 100 | 0 | 5 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 5 shared chapter(s) |
| Satan | `שטן` (shtn; English: Satan) | `σατανας` (satanas; English: Satan) | 100 | 42 | 0 | 3 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 3 shared chapter(s) |
| Savior | `מושיע` (mwshy; English: Savior) | `σωτηρ` (soter; English: Savior) | 100 | 100 | 0 | 6 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 6 shared chapter(s) |
| Serpent | `נחש` (nchsh; English: Serpent) | `οφις` (ophis; English: Serpent) | 100 | 100 | 0 | 7 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 7 shared chapter(s) |
| Sidon | `צידון` (tsydwn; English: Sidon) | `σιδων` (sidon; English: Sidon) | 51 | 100 | 0 | 5 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 5 shared chapter(s) |
| Sign | `אות` (wt; English: Sign) | `σημειον` (semeion; English: Sign) | 100 | 2 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Silent | `נאלם` (nlm; English: Silent) | `σιωπαω` (siopao; English: Silent) | 100 | 25 | 0 | 5 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 5 shared chapter(s) |
| Smoke | `עשן` (shn; English: Smoke) | `καπνος` (kapnos; English: Smoke) | 100 | 51 | 0 | 5 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 5 shared chapter(s) |
| Sodom | `סדום` (sdwm; English: Sodom) | `σοδομα` (sodoma; English: Sodom) | 100 | 22 | 0 | 2 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 2 shared chapter(s) |
| Soul | `נפש` (nefesh; English: Soul); `נפש` (nefesh; English: Soul) | `ψυχη` (psuche; English: Soul); `ψυχη` (psuche; English: Soul) | 200 | 58 | 0 | 2 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 2 shared chapter(s) |
| Spirit | `רוח` (rwch; English: Spirit) | `πνευμα` (pneuma; English: Spirit) | 100 | 14 | 0 | 2 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 2 shared chapter(s) |
| Star | `כוכב` (kwkb; English: Star) | `αστηρ` (aster; English: Star) | 100 | 100 | 0 | 4 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 4 shared chapter(s) |
| Temple | `היכל` (hykl; English: Temple); `היכל` (hykl; English: Temple) | `ναος` (naos; English: Temple); `ναος` (naos; English: Temple) | 200 | 200 | 0 | 6 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 6 shared chapter(s) |
| Throne | `כסא` (kisse; English: Throne) | `θρονος` (thronos; English: Throne) | 100 | 19 | 0 | 1 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 1 shared chapter(s) |
| Tobit | `טוביה` (twbyh; English: Tobit) | `τωβιτ` (tobit; English: Tobit) | 67 | 62 | 0 | 5 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 5 shared chapter(s) |
| Unleavened Bread | `מצות` (mtswt; English: Unleavened Bread) | `αζυμα` (azuma; English: Unleavened Bread) | 100 | 23 | 0 | 2 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 2 shared chapter(s) |
| Ur | `אור` (or; English: Ur) | `ουρ` (our; English: Ur) | 100 | 100 | 0 | 10 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 10 shared chapter(s) |
| Winepress | `יקב` (yqb; English: Winepress) | `ληνος` (lenos; English: Winepress) | 100 | 100 | 0 | 5 | `mt_lxx_common_chapter` | concept has reciprocal MT/LXX ELS centers in 5 shared chapter(s) |

## Interpretation Boundary

A `mt_only_lxx_absent` or `lxx_only_mt_absent` row means the counterpart
concept was not found at the aligned locus under this run's term list,
skip range, and cap. It does not mean a literal original-language letter
sequence was mechanically broken across traditions. A row marked
`alignment_broken_*` means the center locus could not be compared cleanly
because the counterpart corpus lacks that exact verse or chapter key.

Use this report to identify reciprocal review candidates. Claim-level
language still requires locked terms, locked alignment rules, matched
controls, and multiple-comparison correction.
