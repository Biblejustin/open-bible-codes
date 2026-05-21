# Hebrew Concordance Uncorrected Review Queue

Status: queue extracted from the full representative-control run; no claim.

This narrows the Hebrew concordance prospective cohort to the rows that cleared only the uncorrected representative-control screen. These are manual-review prompts, not evidence rows: every row has `representative_best_q = 0.819154`, so none survived the row-family correction.

## Source

- Protocol report: `docs/HEBREW_CONCORDANCE_WORDS_PROSPECTIVE_REPORT.md`
- Generated summary: `reports/hebrew_concordance_words_prospective/controlled_summary.csv`
- Filter: `representative_best_band == paired_uncorrected_p_le_0.05`

## Counts

| Metric | Count |
| --- | ---: |
| Queue rows | 87 |
| Adjusted-support rows | 0 |
| Shared representative q value | 0.819154 |
| `strong_proper_names` rows | 42 |
| `strong_nouns` rows | 30 |
| `strong_adjectives` rows | 13 |
| `strong_particles_other` rows | 2 |

## Read

Treat this as a triage list for manual context review. The best numeric read available here is weak: uncorrected p-values identify places to inspect, while corrected q-values say the family-level result does not support a claim.

Manual review should ask whether each row is only a short-string/common-letter artifact, a surface-word/self-lexeme effect, a proper-name/gloss artifact, or a contextually interesting row worth a fresh preregistered follow-up.

## Queue

| Rank | Term ID | Category | Term | Concept | Exact all-source patterns | p | q |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: |
| 1 | `hcon_h4968` | `strong_proper_names` | `מתושלח` | Methuselah = "man of the dart" | 11 | 0.000999 | 0.819154 |
| 2 | `hcon_h1039` | `strong_proper_names` | `ביתנמרה` | Beth-Nimrah = "house of the leopard" | 3 | 0.005994 | 0.819154 |
| 3 | `hcon_h0041` | `strong_proper_names` | `אבינדב` | Abinadab = "my father is noble" or "my father is willing" | 10 | 0.010989 | 0.819154 |
| 4 | `hcon_h7022` | `strong_nouns` | `קיקלונ` | 1) disgrace, shame | 3 | 0.011988 | 0.819154 |
| 5 | `hcon_h3881` | `strong_adjectives` | `לויי` | Levite = see Levi "joined to" | 18,496 | 0.012987 | 0.819154 |
| 6 | `hcon_h3376` | `strong_proper_names` | `יראייה` | Irijah = "Jehovah sees me" | 107 | 0.012987 | 0.819154 |
| 7 | `hcon_h0380` | `strong_nouns` | `אישונ` | 1) pupil of the eye | 364 | 0.014985 | 0.819154 |
| 8 | `hcon_h2784` | `strong_nouns` | `חרצבה` | 1) bond, fetter, pang, hands | 22 | 0.014985 | 0.819154 |
| 9 | `hcon_h8653` | `strong_nouns` | `תרעלה` | 1) reeling, staggering | 141 | 0.014985 | 0.819154 |
| 10 | `hcon_h1034` | `strong_proper_names` | `ביתלבאות` | Beth-lebaoth = "house of lionesses" | 1 | 0.014985 | 0.819154 |
| 11 | `hcon_h3080` | `strong_proper_names` | `יהויריב` | Jehoiarib = "Jehovah contends" | 6 | 0.014985 | 0.819154 |
| 12 | `hcon_h6138` | `strong_proper_names` | `עקרונ` | Ekron = "emigration" or "torn up by the roots" | 34 | 0.015984 | 0.819154 |
| 13 | `hcon_h1651` | `strong_adjectives` | `גשורי` | Geshuri or Geshurites = see Geshur | 54 | 0.016983 | 0.819154 |
| 14 | `hcon_h4020` | `strong_nouns` | `מגבלה` | 1) twisted, cords | 48 | 0.016983 | 0.819154 |
| 15 | `hcon_h3114` | `strong_proper_names` | `יויריב` | Joiarib = "Jehovah contends" | 78 | 0.016983 | 0.819154 |
| 16 | `hcon_h3224` | `strong_proper_names` | `ימימה` | Jemima = "day by day" | 1,287 | 0.016983 | 0.819154 |
| 17 | `hcon_h0368` | `strong_proper_names` | `אימימ` | Emims = "terrors" | 1,247 | 0.017982 | 0.819154 |
| 18 | `hcon_h1128` | `strong_proper_names` | `בנדקר` | Ben-dekar = "son of stabbing" or "son of Dekar" | 17 | 0.017982 | 0.819154 |
| 19 | `hcon_h1035` | `strong_proper_names` | `ביתלחמ` | Beth-lehem = "house of bread (food)" | 9 | 0.018981 | 0.819154 |
| 20 | `hcon_h0491` | `strong_nouns` | `אלמנות` | 1) widowhood | 31 | 0.019980 | 0.819154 |
| 21 | `hcon_h3732` | `strong_adjectives` | `כפתרי` | Caphtorim = see Caphtor "a crown" | 44 | 0.020979 | 0.819154 |
| 22 | `hcon_h0500` | `strong_proper_names` | `אלעלא` | Elealeh = "God is ascending" | 260 | 0.021978 | 0.819154 |
| 23 | `hcon_h3145` | `strong_proper_names` | `יושויה` | Joshaviah = "Jehovah makes equal" | 99 | 0.021978 | 0.819154 |
| 24 | `hcon_h3119` | `strong_adjectives` | `יוממ` | adv | 15,270 | 0.022977 | 0.819154 |
| 25 | `hcon_h8484` | `strong_adjectives` | `תיכונ` | 1) middle | 199 | 0.022977 | 0.819154 |
| 26 | `hcon_h4842` | `strong_nouns` | `מרקחת` | 1) ointment, mixture of ointment | 17 | 0.022977 | 0.819154 |
| 27 | `hcon_h1152` | `strong_proper_names` | `בסודיה` | Besodeiah = "with the counsel of Jehovah" or "in the secret of the Lord" | 1 | 0.022977 | 0.819154 |
| 28 | `hcon_h6984` | `strong_proper_names` | `קושיהו` | Kushaiah = "bow of Jehovah" | 19 | 0.022977 | 0.819154 |
| 29 | `hcon_h8436` | `strong_proper_names` | `תולונ` | Tilon = "gift" | 365 | 0.023976 | 0.819154 |
| 30 | `hcon_h0460` | `strong_proper_names` | `אליספ` | Eliasaph = "God has added" | 14 | 0.024975 | 0.819154 |
| 31 | `hcon_h6577` | `strong_proper_names` | `פרשנדתא` | Parshandatha = "given by prayer" | 0 | 0.024975 | 0.819154 |
| 32 | `hcon_h2435` | `strong_adjectives` | `חיצונ` | 1) outer, external, outward | 38 | 0.025974 | 0.819154 |
| 33 | `hcon_h4635` | `strong_nouns` | `מערכת` | 1) row, line | 70 | 0.026973 | 0.819154 |
| 34 | `hcon_h4301` | `strong_nouns` | `מטמונ` | 1) hidden treasure, treasure | 35 | 0.027972 | 0.819154 |
| 35 | `hcon_h8399` | `strong_nouns` | `תבלית` | 1) destruction | 244 | 0.027972 | 0.819154 |
| 36 | `hcon_h0742` | `strong_proper_names` | `ארידי` | Aridai = "the lion is enough" | 306 | 0.027972 | 0.819154 |
| 37 | `hcon_h7344` | `strong_proper_names` | `רחבות` | Rehoboth = "wide places or streets" | 79 | 0.027972 | 0.819154 |
| 38 | `hcon_h1127` | `strong_proper_names` | `בנגבר` | Ben-geber = "the son of Geber" or "the son of a man" | 15 | 0.028971 | 0.819154 |
| 39 | `hcon_h4701` | `strong_nouns` | `מצנפת` | 1) turban (of the high priest) | 9 | 0.029970 | 0.819154 |
| 40 | `hcon_h5242` | `strong_adjectives` | `נמואלי` | Nemuelites = see Nemuel "day of God" | 52 | 0.030969 | 0.819154 |
| 41 | `hcon_h3970` | `strong_nouns` | `מאוי` | 1) desire | 14,392 | 0.030969 | 0.819154 |
| 42 | `hcon_h4211` | `strong_nouns` | `מזמרה` | 1) pruning knife | 57 | 0.030969 | 0.819154 |
| 43 | `hcon_h1130` | `strong_proper_names` | `בנהדד` | Ben-hadad = "son of [the false god] Hadad" | 44 | 0.030969 | 0.819154 |
| 44 | `hcon_h4137` | `strong_proper_names` | `מולדה` | Moladah = "birth" or "race" | 254 | 0.030969 | 0.819154 |
| 45 | `hcon_h8498` | `strong_nouns` | `תכונה` | 1) arrangement, preparation, fixed place | 160 | 0.031968 | 0.819154 |
| 46 | `hcon_h1735` | `strong_proper_names` | `דודוהו` | Dodavah = "beloved of Jehovah" | 20 | 0.032967 | 0.819154 |
| 47 | `hcon_h6602` | `strong_proper_names` | `פתואל` | Pethuel = "vision of God" | 98 | 0.032967 | 0.819154 |
| 48 | `hcon_h6597` | `strong_adjectives` | `פתאומ` | adv | 110 | 0.033966 | 0.819154 |
| 49 | `hcon_h8621` | `strong_adjectives` | `תקועי` | Tekoite = see Tekoa "trumpet blast" | 61 | 0.033966 | 0.819154 |
| 50 | `hcon_h1225` | `strong_nouns` | `בצרונ` | 1) stronghold | 30 | 0.033966 | 0.819154 |
| 51 | `hcon_h5865` | `strong_nouns` | `עילומ` | 1) for ever, ever, everlasting, evermore, perpetual, old, ancient, world | 465 | 0.033966 | 0.819154 |
| 52 | `hcon_h6427` | `strong_nouns` | `פלצות` | 1) shuddering, trembling | 22 | 0.033966 | 0.819154 |
| 53 | `hcon_h7611` | `strong_nouns` | `שארית` | 1) rest, residue, remainder, remnant | 233 | 0.033966 | 0.819154 |
| 54 | `hcon_h1769` | `strong_proper_names` | `נוביד` | Dibon = "wasting" | 151 | 0.034965 | 0.819154 |
| 55 | `hcon_h3112` | `strong_proper_names` | `יויכינ` | Jehoiachin = "Jehovah establishes" | 52 | 0.034965 | 0.819154 |
| 56 | `hcon_h6756` | `strong_proper_names` | `צלמונ` | Zalmon = "shady" | 72 | 0.034965 | 0.819154 |
| 57 | `hcon_h8061` | `strong_proper_names` | `שמידע` | Shemida = "wise" | 95 | 0.034965 | 0.819154 |
| 58 | `hcon_h8404` | `strong_proper_names` | `תבערה` | Taberah = "burning" | 119 | 0.034965 | 0.819154 |
| 59 | `hcon_h3227` | `strong_adjectives` | `ימיני` | 1) right, on the right, right hand | 992 | 0.035964 | 0.819154 |
| 60 | `hcon_h4938` | `strong_nouns` | `משענה` | 1) support (of every kind), staff | 102 | 0.035964 | 0.819154 |
| 61 | `hcon_h0190` | `strong_particles_other` | `אויה` | 1) woe! | 14,775 | 0.035964 | 0.819154 |
| 62 | `hcon_h0586` | `strong_particles_other` | `אנחנא` | 1) we (first pers. pl.) | 74 | 0.035964 | 0.819154 |
| 63 | `hcon_h3223` | `strong_proper_names` | `ימואל` | Jemuel = "day of God" | 1,036 | 0.035964 | 0.819154 |
| 64 | `hcon_h3433` | `strong_proper_names` | `ישבילחמ` | Jashubi-lehem = "returner of bread" | 3 | 0.035964 | 0.819154 |
| 65 | `hcon_h5819` | `strong_proper_names` | `עזיזא` | Aziza = "strong" | 10 | 0.036963 | 0.819154 |
| 66 | `hcon_h8454` | `strong_nouns` | `תושיה` | 1) wisdom, sound knowledge, success, sound or efficient wisdom, abiding success | 463 | 0.037962 | 0.819154 |
| 67 | `hcon_h3140` | `strong_proper_names` | `יורי` | Jorai = "Jehovah has taught me" | 14,132 | 0.037962 | 0.819154 |
| 68 | `hcon_h3916` | `strong_nouns` | `ליליא` | 1) night | 987 | 0.038961 | 0.819154 |
| 69 | `hcon_h0298` | `strong_adjectives` | `אחירמי` | Ahiramite = "brother of mother" | 25 | 0.040959 | 0.819154 |
| 70 | `hcon_h8435` | `strong_nouns` | `תולדה` | 1) descendants, results, proceedings, generations, genealogies | 173 | 0.040959 | 0.819154 |
| 71 | `hcon_h8597` | `strong_nouns` | `תפארה` | 1) beauty, splendour, glory | 61 | 0.040959 | 0.819154 |
| 72 | `hcon_h1395` | `strong_adjectives` | `גבעתי` | Gibeathite = "hilliness" | 22 | 0.041958 | 0.819154 |
| 73 | `hcon_h0175` | `strong_proper_names` | `אהרונ` | Aaron = "light bringer" | 353 | 0.041958 | 0.819154 |
| 74 | `hcon_h3078` | `strong_proper_names` | `יהויכינ` | Jehoiachin = "Jehovah establishes" | 4 | 0.041958 | 0.819154 |
| 75 | `hcon_h4921` | `strong_proper_names` | `משלמית` | Meshillemith = "recompense" | 33 | 0.041958 | 0.819154 |
| 76 | `hcon_h4358` | `strong_nouns` | `מכלול` | n m | 330 | 0.042957 | 0.819154 |
| 77 | `hcon_h5082` | `strong_nouns` | `נדיבה` | 1) nobility, nobleness, noble deeds | 118 | 0.042957 | 0.819154 |
| 78 | `hcon_h4103` | `strong_nouns` | `מהומה` | 1) tumult, confusion, disquietude, discomfiture, destruction, trouble, vexed, vexation | 930 | 0.043956 | 0.819154 |
| 79 | `hcon_h4730` | `strong_nouns` | `מקטרת` | 1) censer | 4 | 0.043956 | 0.819154 |
| 80 | `hcon_h8570` | `strong_nouns` | `תנובה` | 1) fruit, produce | 210 | 0.043956 | 0.819154 |
| 81 | `hcon_h0051` | `strong_proper_names` | `אבישור` | Abishur = "my father is a wall" | 33 | 0.043956 | 0.819154 |
| 82 | `hcon_h0222` | `strong_proper_names` | `אוריאל` | Uriel = "God (El) is my light" | 68 | 0.043956 | 0.819154 |
| 83 | `hcon_h1437` | `strong_proper_names` | `גדלתי` | Giddalti = "I make great" | 20 | 0.043956 | 0.819154 |
| 84 | `hcon_h0194` | `strong_nouns` | `אולי` | 1) perhaps, peradventure | 12,738 | 0.044955 | 0.819154 |
| 85 | `hcon_h6242` | `strong_nouns` | `עשרימ` | 1) twenty, twentieth | 185 | 0.044955 | 0.819154 |
| 86 | `hcon_h4321` | `strong_proper_names` | `מיכיהו` | Micah or Micaiah or Michaiah = "who is like God" | 56 | 0.047952 | 0.819154 |
| 87 | `hcon_h0191` | `strong_adjectives` | `אויל` | 1) be foolish, foolish | 12,937 | 0.049950 | 0.819154 |
