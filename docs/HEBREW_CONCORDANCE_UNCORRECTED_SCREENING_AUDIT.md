# Hebrew Concordance Uncorrected Screening Audit

Status: generated audit for the Hebrew concordance uncorrected queue; no claim.

This audit classifies the 87 Hebrew concordance rows that cleared only
the uncorrected representative-control screen. It does not upgrade them:
the corrected family-level result is still negative.

## Inputs

- Summary: `reports/hebrew_concordance_words_prospective/controlled_summary.csv`
- Examples: `reports/hebrew_concordance_words_prospective/controlled_examples.csv`
- CSV audit: `reports/hebrew_concordance_words_prospective/uncorrected_screening_audit.csv`

## Counts

| Metric | Count |
| --- | ---: |
| Audit rows | 87 |
| Adjusted-support rows | 0 |
| Distinct representative q values | 1 |
| `strong_proper_names` rows | 42 |
| `strong_nouns` rows | 30 |
| `strong_adjectives` rows | 13 |
| `strong_particles_other` rows | 2 |
| `no_adjusted_support` flags | 87 |
| `proper_name_gloss` flags | 42 |
| `high_pattern_volume` flags | 10 |
| `short_string` flags | 7 |
| `sparse_all_source_patterns` flags | 5 |
| `no_all_source_exact_patterns` flags | 1 |

## Read Buckets

| Read | Rows |
| --- | ---: |
| ordinary lexical prompt; no adjusted representative-control support | 38 |
| proper-name/gloss prompt; needs manual context review before any follow-up | 33 |
| high-volume short-string/common-letter risk; triage only | 10 |
| sparse all-source pattern count; too thin for a context claim | 5 |
| control artifact only; no all-source exact row to review | 1 |

## Audit Rows

| Rank | Term | Category | All-source patterns | p | q | Flags | Sample centers | Read |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | --- |
| 1 | `hcon_h4968` `מתושלח` (Methuselah = "man of the dart") | `strong_proper_names` | 11 | 0.000999 | 0.819154 | no_adjusted_support; proper_name_gloss | רעש; בשמחת; די; דימהימנ; זבינא | proper-name/gloss prompt; needs manual context review before any follow-up |
| 2 | `hcon_h1039` `ביתנמרה` (Beth-Nimrah = "house of the leopard") | `strong_proper_names` | 3 | 0.005994 | 0.819154 | no_adjusted_support; sparse_all_source_patterns; proper_name_gloss | ותגנב; אלהינו; העננ; תתנ; לבנייהודה | sparse all-source pattern count; too thin for a context claim |
| 3 | `hcon_h0041` `אבינדב` (Abinadab = "my father is noble" or "my father is willing") | `strong_proper_names` | 10 | 0.010989 | 0.819154 | no_adjusted_support; proper_name_gloss | תפתח; וילכ; אחימעצ; השטנ; תשפתני | proper-name/gloss prompt; needs manual context review before any follow-up |
| 4 | `hcon_h7022` `קיקלונ` (1) disgrace, shame) | `strong_nouns` | 3 | 0.011988 | 0.819154 | no_adjusted_support; sparse_all_source_patterns | נכונ; ירוצונ; להקטיר; מנחת; מנחתערב | sparse all-source pattern count; too thin for a context claim |
| 5 | `hcon_h3881` `לויי` (Levite = see Levi "joined to") | `strong_adjectives` | 18,496 | 0.012987 | 0.819154 | no_adjusted_support; short_string; high_pattern_volume | ויפיע; יהוה; בריתיהוה; ויזואל; אלעוזי | high-volume short-string/common-letter risk; triage only |
| 6 | `hcon_h3376` `יראייה` (Irijah = "Jehovah sees me") | `strong_proper_names` | 107 | 0.012987 | 0.819154 | no_adjusted_support; proper_name_gloss | הזיתימ; אשוב; רדפ; ממני; מלכישראל | proper-name/gloss prompt; needs manual context review before any follow-up |
| 7 | `hcon_h0380` `אישונ` (1) pupil of the eye) | `strong_nouns` | 364 | 0.014985 | 0.819154 | no_adjusted_support | אשר; אשא; קדש; שמרי; בשבי | ordinary lexical prompt; no adjusted representative-control support |
| 8 | `hcon_h2784` `חרצבה` (1) bond, fetter, pang, hands) | `strong_nouns` | 22 | 0.014985 | 0.819154 | no_adjusted_support | יצרו; אתיצרו; רצינ; עצמו; עצמולי | ordinary lexical prompt; no adjusted representative-control support |
| 9 | `hcon_h8653` `תרעלה` (1) reeling, staggering) | `strong_nouns` | 141 | 0.014985 | 0.819154 | no_adjusted_support | ירבעמ; ובערת; העיר; אתהעיר; עמהמ | ordinary lexical prompt; no adjusted representative-control support |
| 10 | `hcon_h1034` `ביתלבאות` (Beth-lebaoth = "house of lionesses") | `strong_proper_names` | 1 | 0.014985 | 0.819154 | no_adjusted_support; sparse_all_source_patterns; proper_name_gloss | מבקשי; ויעמד; ואתהעצימ; בבטנכ | sparse all-source pattern count; too thin for a context claim |
| 11 | `hcon_h3080` `יהויריב` (Jehoiarib = "Jehovah contends") | `strong_proper_names` | 6 | 0.014985 | 0.819154 | no_adjusted_support; proper_name_gloss | הפנימית; והפיצהו; והשמתי; יהוה; בקיעי | proper-name/gloss prompt; needs manual context review before any follow-up |
| 12 | `hcon_h6138` `עקרונ` (Ekron = "emigration" or "torn up by the roots") | `strong_proper_names` | 34 | 0.015984 | 0.819154 | no_adjusted_support; proper_name_gloss | שמרה; הנותרימ; כדרכיו; סוררימ; יעבר | proper-name/gloss prompt; needs manual context review before any follow-up |
| 13 | `hcon_h1651` `גשורי` (Geshuri or Geshurites = see Geshur) | `strong_adjectives` | 54 | 0.016983 | 0.819154 | no_adjusted_support | וכפ; ויעשו; וידרכו; ומרעה; וראו | ordinary lexical prompt; no adjusted representative-control support |
| 14 | `hcon_h4020` `מגבלה` (1) twisted, cords) | `strong_nouns` | 48 | 0.016983 | 0.819154 | no_adjusted_support | ויבא; ארבה; בנ; בניעור; בניעיר | ordinary lexical prompt; no adjusted representative-control support |
| 15 | `hcon_h3114` `יויריב` (Joiarib = "Jehovah contends") | `strong_proper_names` | 78 | 0.016983 | 0.819154 | no_adjusted_support; proper_name_gloss | ירמיהו; ובינ; עירינ; עליהודה; בנאוריה | proper-name/gloss prompt; needs manual context review before any follow-up |
| 16 | `hcon_h3224` `ימימה` (Jemima = "day by day") | `strong_proper_names` | 1,287 | 0.016983 | 0.819154 | no_adjusted_support; high_pattern_volume; proper_name_gloss | ויאמר; חיימ; מהית; כי; הרי | high-volume short-string/common-letter risk; triage only |
| 17 | `hcon_h0368` `אימימ` (Emims = "terrors") | `strong_proper_names` | 1,247 | 0.017982 | 0.819154 | no_adjusted_support; high_pattern_volume; proper_name_gloss | ויאמר; המליכ; כיהמליכ; מי; מייראנו | high-volume short-string/common-letter risk; triage only |
| 18 | `hcon_h1128` `בנדקר` (Ben-dekar = "son of stabbing" or "son of Dekar") | `strong_proper_names` | 17 | 0.017982 | 0.819154 | no_adjusted_support; proper_name_gloss | צדיק; מדבר; מדברצנ; עבדונ; ידבר | proper-name/gloss prompt; needs manual context review before any follow-up |
| 19 | `hcon_h1035` `ביתלחמ` (Beth-lehem = "house of bread (food)") | `strong_proper_names` | 9 | 0.018981 | 0.819154 | no_adjusted_support; proper_name_gloss | לבית; המלכ; עלהמלכ; יהודה; אתיהודה | proper-name/gloss prompt; needs manual context review before any follow-up |
| 20 | `hcon_h0491` `אלמנות` (1) widowhood) | `strong_nouns` | 31 | 0.019980 | 0.819154 | no_adjusted_support | המחנה; אלהמחנה; והשמימ; שימונ; שערימ | ordinary lexical prompt; no adjusted representative-control support |
| 21 | `hcon_h3732` `כפתרי` (Caphtorim = see Caphtor "a crown") | `strong_adjectives` | 44 | 0.020979 | 0.819154 | no_adjusted_support | נתתי; אתה; במסתרימ; ונמתהו; מחתות | ordinary lexical prompt; no adjusted representative-control support |
| 22 | `hcon_h0500` `אלעלא` (Elealeh = "God is ascending") | `strong_proper_names` | 260 | 0.021978 | 0.819154 | no_adjusted_support; proper_name_gloss | אלישע; אלאלישע; ויעבר; על; עלשלשה | proper-name/gloss prompt; needs manual context review before any follow-up |
| 23 | `hcon_h3145` `יושויה` (Joshaviah = "Jehovah makes equal") | `strong_proper_names` | 99 | 0.021978 | 0.819154 | no_adjusted_support; proper_name_gloss | וישבו; וישתחוו; אפדתו; אלהי; ומגיד | proper-name/gloss prompt; needs manual context review before any follow-up |
| 24 | `hcon_h3119` `יוממ` (adv) | `strong_adjectives` | 15,270 | 0.022977 | 0.819154 | no_adjusted_support; short_string; high_pattern_volume | גמ; גמהמ; ומלואימ; במקמו; המבונימ | high-volume short-string/common-letter risk; triage only |
| 25 | `hcon_h8484` `תיכונ` (1) middle) | `strong_adjectives` | 199 | 0.022977 | 0.819154 | no_adjusted_support | נעורכ; וימלכ; לכסא; כצנה; בכברה | ordinary lexical prompt; no adjusted representative-control support |
| 26 | `hcon_h4842` `מרקחת` (1) ointment, mixture of ointment) | `strong_nouns` | 17 | 0.022977 | 0.819154 | no_adjusted_support | ויקמ; בקנה; כצדקי; המקמות; בכלהמקמות | ordinary lexical prompt; no adjusted representative-control support |
| 27 | `hcon_h1152` `בסודיה` (Besodeiah = "with the counsel of Jehovah" or "in the secret of the Lord") | `strong_proper_names` | 1 | 0.022977 | 0.819154 | no_adjusted_support; sparse_all_source_patterns; proper_name_gloss | אלה; כלאלה; יהוה; מגנימ; וחצריהמ | sparse all-source pattern count; too thin for a context claim |
| 28 | `hcon_h6984` `קושיהו` (Kushaiah = "bow of Jehovah") | `strong_proper_names` | 19 | 0.022977 | 0.819154 | no_adjusted_support; proper_name_gloss | וישמע; וימשהו; מפניכמ; ילטוש; וימליכו | proper-name/gloss prompt; needs manual context review before any follow-up |
| 29 | `hcon_h8436` `תולונ` (Tilon = "gift") | `strong_proper_names` | 365 | 0.023976 | 0.819154 | no_adjusted_support; proper_name_gloss | ילכו; וילכו; ואלמו; אל; אלשועתמ | proper-name/gloss prompt; needs manual context review before any follow-up |
| 30 | `hcon_h0460` `אליספ` (Eliasaph = "God has added") | `strong_proper_names` | 14 | 0.024975 | 0.819154 | no_adjusted_support; proper_name_gloss | תחיה; אינ; דבריכ; פלילימ; ראיתי | proper-name/gloss prompt; needs manual context review before any follow-up |
| 31 | `hcon_h6577` `פרשנדתא` (Parshandatha = "given by prayer") | `strong_proper_names` | 0 | 0.024975 | 0.819154 | no_adjusted_support; no_all_source_exact_patterns; proper_name_gloss | מני; מניימ | control artifact only; no all-source exact row to review |
| 32 | `hcon_h2435` `חיצונ` (1) outer, external, outward) | `strong_adjectives` | 38 | 0.025974 | 0.819154 | no_adjusted_support | מצבה; יצא; למקצעת; למצבת; ויצפהו | ordinary lexical prompt; no adjusted representative-control support |
| 33 | `hcon_h4635` `מערכת` (1) row, line) | `strong_nouns` | 70 | 0.026973 | 0.819154 | no_adjusted_support | ברית; ערימ; לאור; לרגלי; ברמה | ordinary lexical prompt; no adjusted representative-control support |
| 34 | `hcon_h4301` `מטמונ` (1) hidden treasure, treasure) | `strong_nouns` | 35 | 0.027972 | 0.819154 | no_adjusted_support | מאחריו; וממטה; עיניהמ; שלמה; מעל | ordinary lexical prompt; no adjusted representative-control support |
| 35 | `hcon_h8399` `תבלית` (1) destruction) | `strong_nouns` | 244 | 0.027972 | 0.819154 | no_adjusted_support | להיות; הבעל; אתהבעל; באלהיכ; לשפט | ordinary lexical prompt; no adjusted representative-control support |
| 36 | `hcon_h0742` `ארידי` (Aridai = "the lion is enough") | `strong_proper_names` | 306 | 0.027972 | 0.819154 | no_adjusted_support; proper_name_gloss | בי; ושמתיה; לי; אחבשהלי; כי | proper-name/gloss prompt; needs manual context review before any follow-up |
| 37 | `hcon_h7344` `רחבות` (Rehoboth = "wide places or streets") | `strong_proper_names` | 79 | 0.027972 | 0.819154 | no_adjusted_support; proper_name_gloss | ובני; אביו; ואעזבה; בינ; הרב | proper-name/gloss prompt; needs manual context review before any follow-up |
| 38 | `hcon_h1127` `בנגבר` (Ben-geber = "the son of Geber" or "the son of a man") | `strong_proper_names` | 15 | 0.028971 | 0.819154 | no_adjusted_support; proper_name_gloss | נגעת; שגיאנ; גזמ; בניגזמ; עגלי | proper-name/gloss prompt; needs manual context review before any follow-up |
| 39 | `hcon_h4701` `מצנפת` (1) turban (of the high priest)) | `strong_nouns` | 9 | 0.029970 | 0.819154 | no_adjusted_support | ציונ; עלהרציונ; בני; חנ; הנני | ordinary lexical prompt; no adjusted representative-control support |
| 40 | `hcon_h5242` `נמואלי` (Nemuelites = see Nemuel "day of God") | `strong_adjectives` | 52 | 0.030969 | 0.819154 | no_adjusted_support | אסור; לאאסור; אשוב; ולאאשוב; שמעי | ordinary lexical prompt; no adjusted representative-control support |
| 41 | `hcon_h3970` `מאוי` (1) desire) | `strong_nouns` | 14,392 | 0.030969 | 0.819154 | no_adjusted_support; short_string; high_pattern_volume | יהוה; ומאה; תתיהוה; ומלאה | high-volume short-string/common-letter risk; triage only |
| 42 | `hcon_h4211` `מזמרה` (1) pruning knife) | `strong_nouns` | 57 | 0.030969 | 0.819154 | no_adjusted_support | רחבעמ; לאמר; דלימ; מראה | ordinary lexical prompt; no adjusted representative-control support |
| 43 | `hcon_h1130` `בנהדד` (Ben-hadad = "son of [the false god] Hadad") | `strong_proper_names` | 44 | 0.030969 | 0.819154 | no_adjusted_support; proper_name_gloss | מה; מהדודכ; יעשה; הזה; שלשה | proper-name/gloss prompt; needs manual context review before any follow-up |
| 44 | `hcon_h4137` `מולדה` (Moladah = "birth" or "race") | `strong_proper_names` | 254 | 0.030969 | 0.819154 | no_adjusted_support; proper_name_gloss | גדולה; לקדש; לעולמ; ילכו; ולא | proper-name/gloss prompt; needs manual context review before any follow-up |
| 45 | `hcon_h8498` `תכונה` (1) arrangement, preparation, fixed place) | `strong_nouns` | 160 | 0.031968 | 0.819154 | no_adjusted_support | ופניה; ואכלת; דודי; יחלפונ; והרסתיו | ordinary lexical prompt; no adjusted representative-control support |
| 46 | `hcon_h1735` `דודוהו` (Dodavah = "beloved of Jehovah") | `strong_proper_names` | 20 | 0.032967 | 0.819154 | no_adjusted_support; proper_name_gloss | חציר; יהוה; אל; אליהוה; ודבר | proper-name/gloss prompt; needs manual context review before any follow-up |
| 47 | `hcon_h6602` `פתואל` (Pethuel = "vision of God") | `strong_proper_names` | 98 | 0.032967 | 0.819154 | no_adjusted_support; proper_name_gloss | אחות; ואת; ואתאשקלונ; ויאמר; יהיו | proper-name/gloss prompt; needs manual context review before any follow-up |
| 48 | `hcon_h6597` `פתאומ` (adv) | `strong_adjectives` | 110 | 0.033966 | 0.819154 | no_adjusted_support | האפוד; אתו; אשר; הזאת; אינ | ordinary lexical prompt; no adjusted representative-control support |
| 49 | `hcon_h8621` `תקועי` (Tekoite = see Tekoa "trumpet blast") | `strong_adjectives` | 61 | 0.033966 | 0.819154 | no_adjusted_support | קצות; קצותעמימ; אותכ; ולמה; יהוה | ordinary lexical prompt; no adjusted representative-control support |
| 50 | `hcon_h1225` `בצרונ` (1) stronghold) | `strong_nouns` | 30 | 0.033966 | 0.819154 | no_adjusted_support | מצרימ; ויאמר; יראו; ויאמרו; לרעה | ordinary lexical prompt; no adjusted representative-control support |
| 51 | `hcon_h5865` `עילומ` (1) for ever, ever, everlasting, evermore, perpetual, old, ancient, world) | `strong_nouns` | 465 | 0.033966 | 0.819154 | no_adjusted_support | לא; מכל; אלהינו; ויולדו; עליהמ | ordinary lexical prompt; no adjusted representative-control support |
| 52 | `hcon_h6427` `פלצות` (1) shuddering, trembling) | `strong_nouns` | 22 | 0.033966 | 0.819154 | no_adjusted_support | ארצה; השרצ; ארצ; צדקי; צדקיבה | ordinary lexical prompt; no adjusted representative-control support |
| 53 | `hcon_h7611` `שארית` (1) rest, residue, remainder, remnant) | `strong_nouns` | 233 | 0.033966 | 0.819154 | no_adjusted_support | ויברח; אמרתי; הפר; אתהפר; השרפה | ordinary lexical prompt; no adjusted representative-control support |
| 54 | `hcon_h1769` `נוביד` (Dibon = "wasting") | `strong_proper_names` | 151 | 0.034965 | 0.819154 | no_adjusted_support; proper_name_gloss | וישב; ויעברו; יעקב; מעבדוהי; כלמעבדוהי | proper-name/gloss prompt; needs manual context review before any follow-up |
| 55 | `hcon_h3112` `יויכינ` (Jehoiachin = "Jehovah establishes") | `strong_proper_names` | 52 | 0.034965 | 0.819154 | no_adjusted_support; proper_name_gloss | בירכתימ; מיכה; בספרתכ; פתלחמ; באימ | proper-name/gloss prompt; needs manual context review before any follow-up |
| 56 | `hcon_h6756` `צלמונ` (Zalmon = "shady") | `strong_proper_names` | 72 | 0.034965 | 0.819154 | no_adjusted_support; proper_name_gloss | אלגומימ; עמו; לכלעמו; ימלכו; ומוציאי | proper-name/gloss prompt; needs manual context review before any follow-up |
| 57 | `hcon_h8061` `שמידע` (Shemida = "wise") | `strong_proper_names` | 95 | 0.034965 | 0.819154 | no_adjusted_support; proper_name_gloss | הששי; יכלו; דינ; שנתימ; ביתו | proper-name/gloss prompt; needs manual context review before any follow-up |
| 58 | `hcon_h8404` `תבערה` (Taberah = "burning") | `strong_proper_names` | 119 | 0.034965 | 0.819154 | no_adjusted_support; proper_name_gloss | הקרקע; עדהקרקע; הריעו; בישועתכ; יעקב | proper-name/gloss prompt; needs manual context review before any follow-up |
| 59 | `hcon_h3227` `ימיני` (1) right, on the right, right hand) | `strong_adjectives` | 992 | 0.035964 | 0.819154 | no_adjusted_support | ויפנו; מגיחנ; ויענ; חמתי; הישבימ | ordinary lexical prompt; no adjusted representative-control support |
| 60 | `hcon_h4938` `משענה` (1) support (of every kind), staff) | `strong_nouns` | 102 | 0.035964 | 0.819154 | no_adjusted_support | כענ; בשבע; בעמלו; על; עלבשרו | ordinary lexical prompt; no adjusted representative-control support |
| 61 | `hcon_h0190` `אויה` (1) woe!) | `strong_particles_other` | 14,775 | 0.035964 | 0.819154 | no_adjusted_support; short_string; high_pattern_volume | האחוחי; וזיזה; ולכהנימ; הבית; וביתה | high-volume short-string/common-letter risk; triage only |
| 62 | `hcon_h0586` `אנחנא` (1) we (first pers. pl.)) | `strong_particles_other` | 74 | 0.035964 | 0.819154 | no_adjusted_support | נכח; אלנכח; חטאתי; ולאחטאתי; ויחזק | ordinary lexical prompt; no adjusted representative-control support |
| 63 | `hcon_h3223` `ימואל` (Jemuel = "day of God") | `strong_proper_names` | 1,036 | 0.035964 | 0.819154 | no_adjusted_support; high_pattern_volume; proper_name_gloss | וישמהו; אמרו; אלהינו; ויגד; ימשחו | high-volume short-string/common-letter risk; triage only |
| 64 | `hcon_h3433` `ישבילחמ` (Jashubi-lehem = "returner of bread") | `strong_proper_names` | 3 | 0.035964 | 0.819154 | no_adjusted_support; sparse_all_source_patterns; proper_name_gloss | שניהמ; יהוה; בני; והוכיח | sparse all-source pattern count; too thin for a context claim |
| 65 | `hcon_h5819` `עזיזא` (Aziza = "strong") | `strong_proper_names` | 10 | 0.036963 | 0.819154 | no_adjusted_support; proper_name_gloss | כי; ויחזיה; עליהמ; שמימ; מעלשמימ | proper-name/gloss prompt; needs manual context review before any follow-up |
| 66 | `hcon_h8454` `תושיה` (1) wisdom, sound knowledge, success, sound or efficient wisdom, abiding success) | `strong_nouns` | 463 | 0.037962 | 0.819154 | no_adjusted_support | וימשחו; איש; אשר; נטשה; שלשה | ordinary lexical prompt; no adjusted representative-control support |
| 67 | `hcon_h3140` `יורי` (Jorai = "Jehovah has taught me") | `strong_proper_names` | 14,132 | 0.037962 | 0.819154 | no_adjusted_support; short_string; high_pattern_volume; proper_name_gloss | וחרשי; גרשומ; וירמיה; וזרחיה; ורעותי | high-volume short-string/common-letter risk; triage only |
| 68 | `hcon_h3916` `ליליא` (1) night) | `strong_nouns` | 987 | 0.038961 | 0.819154 | no_adjusted_support | לבית; מלכ; כימלכ; אלהימ; ואל | ordinary lexical prompt; no adjusted representative-control support |
| 69 | `hcon_h0298` `אחירמי` (Ahiramite = "brother of mother") | `strong_adjectives` | 25 | 0.040959 | 0.819154 | no_adjusted_support | כי; למה; לדוד; ההררי; סגר | ordinary lexical prompt; no adjusted representative-control support |
| 70 | `hcon_h8435` `תולדה` (1) descendants, results, proceedings, generations, genealogies) | `strong_nouns` | 173 | 0.040959 | 0.819154 | no_adjusted_support | וילכדו; ועל; ועלידו; הלכו; אליהמ | ordinary lexical prompt; no adjusted representative-control support |
| 71 | `hcon_h8597` `תפארה` (1) beauty, splendour, glory) | `strong_nouns` | 61 | 0.040959 | 0.819154 | no_adjusted_support | אלי; בארצ; בארצמצרימ; איש; באדני | ordinary lexical prompt; no adjusted representative-control support |
| 72 | `hcon_h1395` `גבעתי` (Gibeathite = "hilliness") | `strong_adjectives` | 22 | 0.041958 | 0.819154 | no_adjusted_support | ענת; בנענת; עלוהי; מבלעיכ; הזרע | ordinary lexical prompt; no adjusted representative-control support |
| 73 | `hcon_h0175` `אהרונ` (Aaron = "light bringer") | `strong_proper_names` | 353 | 0.041958 | 0.819154 | no_adjusted_support; proper_name_gloss | מראה; הארצ; אתהארצ; אמר; ואמר | proper-name/gloss prompt; needs manual context review before any follow-up |
| 74 | `hcon_h3078` `יהויכינ` (Jehoiachin = "Jehovah establishes") | `strong_proper_names` | 4 | 0.041958 | 0.819154 | no_adjusted_support; proper_name_gloss | יתקדשו; יתקדשוקדש; בניו; אלי; חיי | proper-name/gloss prompt; needs manual context review before any follow-up |
| 75 | `hcon_h4921` `משלמית` (Meshillemith = "recompense") | `strong_proper_names` | 33 | 0.041958 | 0.819154 | no_adjusted_support; proper_name_gloss | המלכימ; עצי; עצישמנ; ויוציאהו; שכמו | proper-name/gloss prompt; needs manual context review before any follow-up |
| 76 | `hcon_h4358` `מכלול` (n m) | `strong_nouns` | 330 | 0.042957 | 0.819154 | no_adjusted_support | מלאכימ; אלהיכ; אלהיכמ; וילכ; המשכיל | ordinary lexical prompt; no adjusted representative-control support |
| 77 | `hcon_h5082` `נדיבה` (1) nobility, nobleness, noble deeds) | `strong_nouns` | 118 | 0.042957 | 0.819154 | no_adjusted_support | ישבי; בני; תשימ; אפיקי; בית | ordinary lexical prompt; no adjusted representative-control support |
| 78 | `hcon_h4103` `מהומה` (1) tumult, confusion, disquietude, discomfiture, destruction, trouble, vexed, vexation) | `strong_nouns` | 930 | 0.043956 | 0.819154 | no_adjusted_support | והלוימ; הגוימ; מנהגוימ; ומבוקה; ואני | ordinary lexical prompt; no adjusted representative-control support |
| 79 | `hcon_h4730` `מקטרת` (1) censer) | `strong_nouns` | 4 | 0.043956 | 0.819154 | no_adjusted_support | בשטימ; משפטי; משפטיצדק; וממטה; וממטהגד | ordinary lexical prompt; no adjusted representative-control support |
| 80 | `hcon_h8570` `תנובה` (1) fruit, produce) | `strong_nouns` | 210 | 0.043956 | 0.819154 | no_adjusted_support | ואבדה; יהוה; צבאות; תוכ; אלתוכ | ordinary lexical prompt; no adjusted representative-control support |
| 81 | `hcon_h0051` `אבישור` (Abishur = "my father is a wall") | `strong_proper_names` | 33 | 0.043956 | 0.819154 | no_adjusted_support; proper_name_gloss | וישת; ירמיהו; שדרכ; ימימ; יהויקימ | proper-name/gloss prompt; needs manual context review before any follow-up |
| 82 | `hcon_h0222` `אוריאל` (Uriel = "God (El) is my light") | `strong_proper_names` | 68 | 0.043956 | 0.819154 | no_adjusted_support; proper_name_gloss | עשר; ויאסרהו; ותעלנה; מצפונ; אדני | proper-name/gloss prompt; needs manual context review before any follow-up |
| 83 | `hcon_h1437` `גדלתי` (Giddalti = "I make great") | `strong_proper_names` | 20 | 0.043956 | 0.819154 | no_adjusted_support; proper_name_gloss | מלכות; ישראל; האלכ; כלב; אלי | proper-name/gloss prompt; needs manual context review before any follow-up |
| 84 | `hcon_h0194` `אולי` (1) perhaps, peradventure) | `strong_nouns` | 12,738 | 0.044955 | 0.819154 | no_adjusted_support; short_string; high_pattern_volume | וישלחו; לו; מלכותא; אשור; אדומ | high-volume short-string/common-letter risk; triage only |
| 85 | `hcon_h6242` `עשרימ` (1) twenty, twentieth) | `strong_nouns` | 185 | 0.044955 | 0.819154 | no_adjusted_support | בשפר; תורתכ; ספרימ; מיער; הישר | ordinary lexical prompt; no adjusted representative-control support |
| 86 | `hcon_h4321` `מיכיהו` (Micah or Micaiah or Michaiah = "who is like God") | `strong_proper_names` | 56 | 0.047952 | 0.819154 | no_adjusted_support; proper_name_gloss | ויהי; ראה; הדברימ; אתהדברימ; מעשהו | proper-name/gloss prompt; needs manual context review before any follow-up |
| 87 | `hcon_h0191` `אויל` (1) be foolish, foolish) | `strong_adjectives` | 12,937 | 0.049950 | 0.819154 | no_adjusted_support; short_string; high_pattern_volume | האלהימ; באלהימ; אלפימ; אלהיו; ויבאו | high-volume short-string/common-letter risk; triage only |

## Follow-Up Gate

Do not use this audit as a claim list. A stricter follow-up should be
preregistered before new searching. Minimum gates should include: adjusted
support, non-sparse all-source pattern counts, exclusion or separate handling
of high-volume short strings, and a context-distance rule that prevents
surface-word and gloss artifacts from driving interpretation.
