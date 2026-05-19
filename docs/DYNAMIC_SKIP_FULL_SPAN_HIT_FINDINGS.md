# Dynamic Full-Span Hit Findings

This report summarizes the exported dynamic full-span hit file without
requiring a surface-center match. Every exported hit remains available
in the hit CSV; exact center-word matches are reported as an additional
flag, not as the admission rule.

## Reproduce

```bash
python3 -m scripts.summarize_dynamic_span_hits \
  --db reports/db/open_bible_codes.duckdb \
  --hits-table dynamic_skip_focus_full_span_exported_hits
```

## Scope

- exported term/corpus rows summarized: 88
- exported hit rows summarized: 918,266
- low-count threshold for examples: 100
- exact center-word hits found: 248
- summary CSV: `reports/dynamic_skip_focus/full_span_hit_summary.csv`
- example CSV: `reports/dynamic_skip_focus/full_span_hit_examples.csv`
- version CSV: `reports/dynamic_skip_focus/full_span_version_presence.csv`
- report database: `reports/db/open_bible_codes.duckdb`

## Version Presence Read

Version presence is taken from the full-span count rows, including rows
whose hit-level detail was deferred for partitioned export. That keeps
the version question separate from the practical export threshold.

| Term | Language | Bible present | Control present | Bible max | Control max |
| --- | --- | --- | --- | ---: | ---: |
| `νετανιαχου` (netaniachou; English: Netanyahu)<br>`dyn_netanyahu_g` | greek | LXX=2; TCG_NT=1; TR_NT=1 |  | LXX=2 | none=0 |
| `Beast`<br>`dyn_beast_e` | english | KJV=2427966 | ENG_PG_MOBY_DICK=253351; ENG_PG_SHAKESPEARE=3418141; ENG_PG_WAR_PEACE=1264733 | KJV=2427966 | ENG_PG_SHAKESPEARE=3418141 |
| `Catering`<br>`dyn_catering_e` | english | KJV=96 | ENG_PG_MOBY_DICK=22; ENG_PG_SHAKESPEARE=233; ENG_PG_WAR_PEACE=103 | KJV=96 | ENG_PG_SHAKESPEARE=233 |
| `Christ`<br>`dyn_christ_e` | english | KJV=56561 | ENG_PG_MOBY_DICK=6769; ENG_PG_SHAKESPEARE=111185; ENG_PG_WAR_PEACE=47240 | KJV=56561 | ENG_PG_SHAKESPEARE=111185 |
| `Cowboy`<br>`dyn_cowboy_e` | english | KJV=998 | ENG_PG_MOBY_DICK=149; ENG_PG_SHAKESPEARE=4684; ENG_PG_WAR_PEACE=1058 | KJV=998 | ENG_PG_SHAKESPEARE=4684 |
| `Dragon`<br>`dyn_dragon_e` | english | KJV=39738 | ENG_PG_MOBY_DICK=3621; ENG_PG_SHAKESPEARE=60588; ENG_PG_WAR_PEACE=32283 | KJV=39738 | ENG_PG_SHAKESPEARE=60588 |
| `Gog`<br>`dyn_gog_e` | english | KJV=112614748 | ENG_PG_MOBY_DICK=15815416; ENG_PG_SHAKESPEARE=217556768; ENG_PG_WAR_PEACE=98950428 | KJV=112614748 | ENG_PG_SHAKESPEARE=217556768 |
| `Iran`<br>`dyn_iran_e` | english | KJV=64362163 | ENG_PG_MOBY_DICK=6458074; ENG_PG_SHAKESPEARE=113877707; ENG_PG_WAR_PEACE=50720110 | KJV=64362163 | ENG_PG_SHAKESPEARE=113877707 |
| `Jesus`<br>`dyn_jesus_e` | english | KJV=79657 | ENG_PG_MOBY_DICK=4116; ENG_PG_SHAKESPEARE=87353; ENG_PG_WAR_PEACE=20410 | KJV=79657 | ENG_PG_SHAKESPEARE=87353 |
| `Magog`<br>`dyn_magog_e` | english | KJV=118259 | ENG_PG_MOBY_DICK=15488; ENG_PG_SHAKESPEARE=248036; ENG_PG_WAR_PEACE=99239 | KJV=118259 | ENG_PG_SHAKESPEARE=248036 |
| `Netanyahu`<br>`dyn_netanyahu_e` | english | KJV=27 | ENG_PG_MOBY_DICK=1; ENG_PG_SHAKESPEARE=20; ENG_PG_WAR_PEACE=6 | KJV=27 | ENG_PG_SHAKESPEARE=20 |
| `Russia`<br>`dyn_russia_e` | english | KJV=49202 | ENG_PG_MOBY_DICK=7368; ENG_PG_SHAKESPEARE=151995; ENG_PG_WAR_PEACE=43322 | KJV=49202 | ENG_PG_SHAKESPEARE=151995 |
| `Simsberry`<br>`dyn_simsberry_e` | english | KJV=2 | ENG_PG_SHAKESPEARE=1 | KJV=2 | ENG_PG_SHAKESPEARE=1 |
| `Trump`<br>`dyn_trump_e` | english | KJV=111371 | ENG_PG_MOBY_DICK=14601; ENG_PG_SHAKESPEARE=335790; ENG_PG_WAR_PEACE=93018 | KJV=111371 | ENG_PG_SHAKESPEARE=335790 |
| `Vance`<br>`dyn_vance_e` | english | KJV=294941 | ENG_PG_MOBY_DICK=34314; ENG_PG_SHAKESPEARE=560612; ENG_PG_WAR_PEACE=299257 | KJV=294941 | ENG_PG_SHAKESPEARE=560612 |
| `θηριον` (therion; English: Beast)<br>`dyn_beast_g` | greek | BYZ_NT=1583; LXX=21650; SBLGNT=1470; TCG_NT=1534; TR_NT=1507 | GRC_PERSEUS_HERODOTUS=2349; GRC_PERSEUS_ILIAD=1189; GRC_PERSEUS_ODYSSEY=764 | LXX=21650 | GRC_PERSEUS_HERODOTUS=2349 |
| `χριστος` (Christos; English: Christ)<br>`dyn_christ_g` | greek | BYZ_NT=79; LXX=1280; SBLGNT=85; TCG_NT=80; TR_NT=73 | GRC_PERSEUS_HERODOTUS=220; GRC_PERSEUS_ILIAD=69; GRC_PERSEUS_ODYSSEY=32 | LXX=1280 | GRC_PERSEUS_HERODOTUS=220 |
| `δρακων` (drakon; English: Dragon)<br>`dyn_dragon_g` | greek | BYZ_NT=579; LXX=11437; SBLGNT=569; TCG_NT=616; TR_NT=558 | GRC_PERSEUS_HERODOTUS=1334; GRC_PERSEUS_ILIAD=590; GRC_PERSEUS_ODYSSEY=340 | LXX=11437 | GRC_PERSEUS_HERODOTUS=1334 |
| `γωγ` (Gog; English: Gog)<br>`dyn_gog_g` | greek | BYZ_NT=1990638; LXX=22427984; SBLGNT=1935106; TCG_NT=2000884; TR_NT=2016958 | GRC_PERSEUS_HERODOTUS=3079794; GRC_PERSEUS_ILIAD=895700; GRC_PERSEUS_ODYSSEY=501302 | LXX=22427984 | GRC_PERSEUS_HERODOTUS=3079794 |
| `ιραν` (iran; English: Iran)<br>`dyn_iran_g` | greek | BYZ_NT=4749326; LXX=81141888; SBLGNT=4615073; TCG_NT=4582262; TR_NT=4625438 | GRC_PERSEUS_HERODOTUS=9046396; GRC_PERSEUS_ILIAD=3579561; GRC_PERSEUS_ODYSSEY=1997138 | LXX=81141888 | GRC_PERSEUS_HERODOTUS=9046396 |
| `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | greek | BYZ_NT=11706; LXX=243700; SBLGNT=11218; TCG_NT=11972; TR_NT=11829 | GRC_PERSEUS_HERODOTUS=16741; GRC_PERSEUS_ILIAD=4121; GRC_PERSEUS_ODYSSEY=2779 | LXX=243700 | GRC_PERSEUS_HERODOTUS=16741 |
| `μαγωγ` (magog; English: Magog)<br>`dyn_magog_g` | greek | BYZ_NT=3071; LXX=35515; SBLGNT=3021; TCG_NT=3271; TR_NT=3217 | GRC_PERSEUS_HERODOTUS=4528; GRC_PERSEUS_ILIAD=1517; GRC_PERSEUS_ODYSSEY=872 | LXX=35515 | GRC_PERSEUS_HERODOTUS=4528 |
| `ρωσια` (rosia; English: Russia)<br>`dyn_russia_g` | greek | BYZ_NT=102577; LXX=2218044; SBLGNT=99245; TCG_NT=103404; TR_NT=103855 | GRC_PERSEUS_HERODOTUS=184242; GRC_PERSEUS_ILIAD=67477; GRC_PERSEUS_ODYSSEY=33099 | LXX=2218044 | GRC_PERSEUS_HERODOTUS=184242 |
| `τραμπ` (tramp; English: Trump)<br>`dyn_trump_g` | greek | BYZ_NT=31645; LXX=487148; SBLGNT=31044; TCG_NT=32265; TR_NT=32068 | GRC_PERSEUS_HERODOTUS=68470; GRC_PERSEUS_ILIAD=23534; GRC_PERSEUS_ODYSSEY=13100 | LXX=487148 | GRC_PERSEUS_HERODOTUS=68470 |
| `βανς` (bans; English: Vance)<br>`dyn_vance_g` | greek | BYZ_NT=573495; LXX=14641657; SBLGNT=557336; TCG_NT=551791; TR_NT=568362 | GRC_PERSEUS_HERODOTUS=1235733; GRC_PERSEUS_ILIAD=325999; GRC_PERSEUS_ODYSSEY=185209 | LXX=14641657 | GRC_PERSEUS_HERODOTUS=1235733 |
| `חיה` (chayah; English: Beast)<br>`dyn_beast_h` | hebrew | EBIBLE_WLC=165249617; MAM=164260192; MT_WLC=163013648; UHB=164784929; UXLC=163014892 | HEB_PBY_AHAD_HAAM=816402749; HEB_PBY_BIALIK=3152690416; HEB_PBY_BRENNER=3663683890 | EBIBLE_WLC=165249617 | HEB_PBY_BRENNER=3663683890 |
| `תנין` (tannin; English: Dragon)<br>`dyn_dragon_h` | hebrew | EBIBLE_WLC=6204591; MAM=6135698; MT_WLC=6066657; UHB=6186847; UXLC=6062411 | HEB_PBY_AHAD_HAAM=33003976; HEB_PBY_BIALIK=143129945; HEB_PBY_BRENNER=145655795 | EBIBLE_WLC=6204591 | HEB_PBY_BRENNER=145655795 |
| `גוג` (Gog; English: Gog)<br>`dyn_gog_h` | hebrew | EBIBLE_WLC=5606606; MAM=5593814; MT_WLC=5532568; UHB=5587606; UXLC=5536796 | HEB_PBY_AHAD_HAAM=52524066; HEB_PBY_BIALIK=259364876; HEB_PBY_BRENNER=266462544 | EBIBLE_WLC=5606606 | HEB_PBY_BRENNER=266462544 |
| `איראן` (yrn; English: Iran)<br>`dyn_iran_h` | hebrew | EBIBLE_WLC=667552; MAM=696330; MT_WLC=691579; UHB=668069; UXLC=692152 | HEB_PBY_AHAD_HAAM=2117348; HEB_PBY_BIALIK=11349335; HEB_PBY_BRENNER=10108513 | MAM=696330 | HEB_PBY_BIALIK=11349335 |
| `מגוג` (Magog; English: Magog)<br>`dyn_magog_h` | hebrew | EBIBLE_WLC=307083; MAM=322697; MT_WLC=320111; UHB=306006; UXLC=320231 | HEB_PBY_AHAD_HAAM=2911852; HEB_PBY_BIALIK=14781780; HEB_PBY_BRENNER=13906679 | MAM=322697 | HEB_PBY_BIALIK=14781780 |
| `משיח` (Mashiach; English: Messiah)<br>`dyn_messiah_h` | hebrew | EBIBLE_WLC=5252863; MAM=5093697; MT_WLC=5057448; UHB=5240076; UXLC=5055913 | HEB_PBY_AHAD_HAAM=22587059; HEB_PBY_BIALIK=110129394; HEB_PBY_BRENNER=90027862 | EBIBLE_WLC=5252863 | HEB_PBY_BIALIK=110129394 |
| `נתניהו` (ntnyhw; English: Netanyahu)<br>`dyn_netanyahu_h` | hebrew | EBIBLE_WLC=33283; MAM=33608; MT_WLC=33401; UHB=33663; UXLC=32953 | HEB_PBY_AHAD_HAAM=195658; HEB_PBY_BIALIK=763870; HEB_PBY_BRENNER=920932 | UHB=33663 | HEB_PBY_BRENNER=920932 |
| `רוסיה` (rwsyh; English: Russia)<br>`dyn_russia_h` | hebrew | EBIBLE_WLC=142783; MAM=142463; MT_WLC=137828; UHB=142713; UXLC=137739 | HEB_PBY_AHAD_HAAM=1260045; HEB_PBY_BIALIK=5590218; HEB_PBY_BRENNER=6304561 | EBIBLE_WLC=142783 | HEB_PBY_BRENNER=6304561 |
| `טראמפ` (trmp; English: Trump)<br>`dyn_trump_h` | hebrew | EBIBLE_WLC=10628; MAM=10936; MT_WLC=10636; UHB=10468; UXLC=10692 | HEB_PBY_AHAD_HAAM=92451; HEB_PBY_BIALIK=526134; HEB_PBY_BRENNER=461367 | MAM=10936 | HEB_PBY_BIALIK=526134 |
| `ואנס` (wns; English: Vance)<br>`dyn_vance_h` | hebrew | EBIBLE_WLC=1173157; MAM=1224569; MT_WLC=1191206; UHB=1170235; UXLC=1189894 | HEB_PBY_AHAD_HAAM=10884247; HEB_PBY_BIALIK=51012008; HEB_PBY_BRENNER=52306899 | MAM=1224569 | HEB_PBY_BRENNER=52306899 |
| `ישוע` (Yeshua; English: Yeshua)<br>`dyn_yeshua_h` | hebrew | EBIBLE_WLC=11156131; MAM=10824700; MT_WLC=10724464; UHB=11151829; UXLC=10724706 | HEB_PBY_AHAD_HAAM=46208240; HEB_PBY_BIALIK=206897417; HEB_PBY_BRENNER=188603935 | EBIBLE_WLC=11156131 | HEB_PBY_BIALIK=206897417 |
| `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | hebrew | EBIBLE_WLC=42745545; MAM=43619325; MT_WLC=43283141; UHB=42792278; UXLC=43283917 | HEB_PBY_AHAD_HAAM=230979253; HEB_PBY_BIALIK=803341146; HEB_PBY_BRENNER=1090879372 | MAM=43619325 | HEB_PBY_BRENNER=1090879372 |
| `Simscorner`<br>`dyn_simscorner_e` | english |  | ENG_PG_SHAKESPEARE=1; ENG_PG_WAR_PEACE=1 | none=0 | ENG_PG_SHAKESPEARE=1 |

## Bible-Over-Control Signals

| Term | Language | Bible max corpus | Bible max rate | Control max rate | Ratio |
| --- | --- | --- | ---: | ---: | ---: |
| `νετανιαχου` (netaniachou; English: Netanyahu)<br>`dyn_netanyahu_g` | greek | TR_NT | 1.9e-05 | 0.0 | inf |
| `Simsberry`<br>`dyn_simsberry_e` | english | KJV | 2e-06 | 0.0 | inf |
| `Netanyahu`<br>`dyn_netanyahu_e` | english | KJV | 2.1e-05 | 1e-05 | 2.1 |
| `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | greek | LXX | 0.156329 | 0.090406 | 1.729188 |
| `Jesus`<br>`dyn_jesus_e` | english | KJV | 0.030669 | 0.021227 | 1.444811 |
| `βανς` (bans; English: Vance)<br>`dyn_vance_g` | greek | LXX | 5.635415 | 4.003941 | 1.407467 |
| `איראן` (yrn; English: Iran)<br>`dyn_iran_h` | hebrew | UXLC | 1.932174 | 1.389463 | 1.39059 |
| `μαγωγ` (magog; English: Magog)<br>`dyn_magog_g` | greek | TCG_NT | 0.027649 | 0.01991 | 1.388699 |
| `ρωσια` (rosia; English: Russia)<br>`dyn_russia_g` | greek | LXX | 1.138269 | 0.885589 | 1.285324 |
| `γωγ` (Gog; English: Gog)<br>`dyn_gog_g` | greek | TCG_NT | 8.456437 | 6.65261 | 1.271146 |
| `ישוע` (Yeshua; English: Yeshua)<br>`dyn_yeshua_h` | hebrew | UHB | 23.40353 | 18.997337 | 1.231937 |
| `משיח` (Mashiach; English: Messiah)<br>`dyn_messiah_h` | hebrew | EBIBLE_WLC | 10.997699 | 10.112089 | 1.087579 |

## Low-Count Exported Rows

Low-count rows are useful for human review because they are not dense
letter-background fields. They still need controls and contextual
review before any claim language.

| Corpus | Term | Hits | Min abs skip | Center refs | Center words |
| --- | --- | ---: | ---: | --- | --- |
| ENG_PG_MOBY_DICK | `Netanyahu`<br>`dyn_netanyahu_e` | 1 | 5071 | PG Moby Dick=1 | in=1 |
| ENG_PG_SHAKESPEARE | `Simsberry`<br>`dyn_simsberry_e` | 1 | 91413 | PG Shakespeare=1 | before=1 |
| ENG_PG_SHAKESPEARE | `Simscorner`<br>`dyn_simscorner_e` | 1 | 86428 | PG Shakespeare=1 | joy=1 |
| ENG_PG_WAR_PEACE | `Simscorner`<br>`dyn_simscorner_e` | 1 | 84818 | PG War and Peace=1 | when=1 |
| TCG_NT | `νετανιαχου` (netaniachou; English: Netanyahu)<br>`dyn_netanyahu_g` | 1 | 50218 | ROM 4:2=1 | `καυχημα` (kauchema)=1 |
| TR_NT | `νετανιαχου` (netaniachou; English: Netanyahu)<br>`dyn_netanyahu_g` | 1 | 71517 | ACT 9:43=1 | `εγενετο` (egeneto)=1 |
| KJV | `Simsberry`<br>`dyn_simsberry_e` | 2 | 144748 | PSA 48:5=1; 1CH 12:17=1 | troubled=1; be=1 |
| LXX | `νετανιαχου` (netaniachou; English: Netanyahu)<br>`dyn_netanyahu_g` | 2 | 35170 | LEV 25:39=1; 1SA 22:23=1 | `σοι` (soi)=1; `ζητω` (zeto)=1 |
| ENG_PG_WAR_PEACE | `Netanyahu`<br>`dyn_netanyahu_e` | 6 | 6875 | PG War and Peace=6 | situation=1; no=1; any=1; shouting=1; adopting=1 |
| ENG_PG_SHAKESPEARE | `Netanyahu`<br>`dyn_netanyahu_e` | 20 | 817 | PG Shakespeare=20 | done=2; and=2; noble=1; not=1; son=1 |
| ENG_PG_MOBY_DICK | `Catering`<br>`dyn_catering_e` | 22 | 5063 | PG Moby Dick=22 | proportionate=1; utmost=1; possibly=1; timor=1; appears=1 |
| KJV | `Netanyahu`<br>`dyn_netanyahu_e` | 27 | 1906 | 1CH 2:31=1; EZK 31:12=1; EZK 22:14=1; 1CH 26:1=1; PSA 104:8=1 | and=4; upon=2; man=2; children=1; mountains=1 |
| GRC_PERSEUS_ODYSSEY | `χριστος` (Christos; English: Christ)<br>`dyn_christ_g` | 32 | 1066 | Perseus Odyssey=32 | `κτεατεσσιν` (kteatessin)=2; `αυτοσ` (autos)=2; `νεστορα` (nestora)=1; `σημανεω` (semaneo)=1; `φθισεσθαι` (phthisesthai)=1 |
| GRC_PERSEUS_ILIAD | `χριστος` (Christos; English: Christ)<br>`dyn_christ_g` | 69 | 595 | Perseus Iliad=69 | `διοσ` (dios)=2; `σε` (se)=2; `ωσ` (hos; English: as)=2; `τελαμωνιοσ` (telamonios)=1; `χροοσ` (chroos)=1 |
| TR_NT | `χριστος` (Christos; English: Christ)<br>`dyn_christ_g` | 73 | 193 | 2CO 12:11=2; ACT 4:7=1; ACT 21:24=1; ACT 24:16=1; ACT 9:43=1 | `εισ` (eis; English: into/for)=4; `πατροσ` (patros)=2; `αυτουσ` (autous; English: them)=2; `εστιν` (estin)=2; `ιησουσ` (Iesous; English: Jesus/Joshua)=2 |
| BYZ_NT | `χριστος` (Christos; English: Christ)<br>`dyn_christ_g` | 79 | 1414 | ACT 6:9=1; ACT 13:38=1; JHN 3:26=1; JHN 6:34=1; JHN 9:15=1 | `αυτοισ` (autois)=4; `αυτουσ` (autous; English: them)=3; `τησ` (tes; English: of the)=2; `τουσ` (tous; English: the/those)=2; `οιτινεσ` (oitines)=2 |
| TCG_NT | `χριστος` (Christos; English: Christ)<br>`dyn_christ_g` | 80 | 3289 | ACT 4:23=1; ACT 5:3=1; ACT 16:38=1; ACT 4:28=1; JHN 16:14=1 | `πιστεωσ` (pisteos)=3; `ωσ` (hos; English: as)=3; `τουσ` (tous; English: the/those)=2; `απολυθεντεσ` (apoluthentes)=1; `νοσφισασθαι` (nosphisasthai)=1 |
| SBLGNT | `χριστος` (Christos; English: Christ)<br>`dyn_christ_g` | 85 | 737 | Acts 27:16=2; Acts 7:45=1; Acts 13:28=1; Acts 16:23=1; Acts 12:3=1 | `εισ` (eis; English: into/for)=6; `τησ` (tes; English: of the)=4; `πατροσ` (patros)=2; `ουτωσ` (outos)=2; `υμασ` (umas; English: you)=2 |
| KJV | `Catering`<br>`dyn_catering_e` | 96 | 2169 | PSA 111:5=1; PSA 119:25=1; JOB 3:10=1; JOB 22:2=1; NEH 5:5=1 | and=5; shall=4; of=4; they=3; i=2 |

## Example Hits

| Type | Corpus | Term | Skip | Start | Center | End | Center word |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| `exact_center_word` | BYZ_NT | `χριστος` (Christos; English: Christ)<br>`dyn_christ_g` | -7527 | 2CO 7:14 | 1CO 12:12 | ROM 16:18 | `χριστοσ` (Christos; English: Christ) |
| `exact_center_word` | TCG_NT | `χριστος` (Christos; English: Christ)<br>`dyn_christ_g` | 9387 | 2CO 12:16 | PHP 2:11 | 1TI 3:16 | `Χριστός,` (Christos; English: Christ) |
| `exact_center_word` | LXX | `χριστος` (Christos; English: Christ)<br>`dyn_christ_g` | 65649 | JOS 13:27 | 1SA 24:11 | 1KI 20:10 | `χριστὸς` (Christos; English: Christ) |
| `exact_center_word` | ENG_PG_MOBY_DICK | `Christ`<br>`dyn_christ_e` | 116374 | PG Moby Dick | PG Moby Dick | PG Moby Dick | Christ! |
| `exact_center_word` | SBLGNT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -120184 | 1Pet 4:14 | John 21:4 | Matt 5:33 | `Ἰησοῦς` (Iesous; English: Jesus) |
| `exact_center_word` | SBLGNT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -111545 | Heb 11:7 | John 20:15 | Matt 12:10 | `Ἰησοῦς·` (Iesous; English: Jesus) |
| `exact_center_word` | SBLGNT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -103617 | Col 3:22 | John 9:41 | Matt 7:29 | `Ἰησοῦς·` (Iesous; English: Jesus) |
| `exact_center_word` | SBLGNT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -93353 | Eph 1:5 | John 9:39 | Matt 15:12 | `Ἰησοῦς·` (Iesous; English: Jesus) |
| `exact_center_word` | SBLGNT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -87337 | Gal 4:1 | John 12:23 | Matt 23:20 | `Ἰησοῦς` (Iesous; English: Jesus) |
| `exact_center_word` | BYZ_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -111783 | HEB 4:10 | JHN 17:1 | MAT 10:15 | `ιησουσ` (Iesous; English: Jesus) |
| `exact_center_word` | BYZ_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -110755 | 1TI 4:14 | JHN 11:5 | MAT 5:17 | `ιησουσ` (Iesous; English: Jesus) |
| `exact_center_word` | BYZ_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -108780 | COL 4:15 | JHN 8:1 | MAT 2:6 | `ιησουσ` (Iesous; English: Jesus) |
| `exact_center_word` | BYZ_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -101495 | GAL 4:10 | JHN 4:48 | MAT 4:6 | `ιησουσ` (Iesous; English: Jesus) |
| `exact_center_word` | BYZ_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -90160 | EPH 3:13 | JHN 14:6 | MAT 24:22 | `ιησουσ` (Iesous; English: Jesus) |
| `exact_center_word` | TR_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -103329 | 1TI 6:2 | JHN 18:8 | MAT 17:2 | `Ἰησοῦς` (Iesous; English: Jesus) |
| `exact_center_word` | TR_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -100505 | COL 1:6 | JHN 11:32 | MAT 13:22 | `Ἰησοῦς` (Iesous; English: Jesus) |
| `exact_center_word` | TR_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -100098 | PHP 3:20 | JHN 11:13 | MAT 13:18 | `Ἰησοῦς` (Iesous; English: Jesus) |
| `exact_center_word` | TR_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -76588 | 1CO 10:27 | JHN 8:49 | MAT 27:24 | `Ἰησοῦς` (Iesous; English: Jesus) |
| `exact_center_word` | TR_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -68034 | ACT 9:2 | LUK 7:22 | MAT 4:10 | `Ἰησοῦς` (Iesous; English: Jesus) |
| `exact_center_word` | TCG_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -123507 | 1PE 4:2 | JHN 19:9 | MAT 1:18 | `Ἰησοῦς` (Iesous; English: Jesus) |
| `exact_center_word` | TCG_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -122663 | 1PE 2:12 | JHN 18:37 | MAT 2:3 | `Ἰησοῦς,` (Iesous; English: Jesus) |
| `exact_center_word` | TCG_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -122037 | 1PE 5:8 | JHN 20:30 | MAT 5:32 | `Ἰησοῦς` (Iesous; English: Jesus) |
| `exact_center_word` | TCG_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -108998 | HEB 7:23 | JHN 20:21 | MAT 15:2 | `Ἰησοῦς` (Iesous; English: Jesus) |
| `exact_center_word` | TCG_NT | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | -104792 | HEB 2:3 | JHN 21:5 | MAT 19:7 | `Ἰησοῦς,` (Iesous; English: Jesus) |
| `exact_center_word` | ENG_PG_WAR_PEACE | `Jesus`<br>`dyn_jesus_e` | -278882 | PG War and Peace | PG War and Peace | PG War and Peace | Jesus?” |
| `exact_center_word` | ENG_PG_WAR_PEACE | `Jesus`<br>`dyn_jesus_e` | -142915 | PG War and Peace | PG War and Peace | PG War and Peace | Jesus |
| `exact_center_word` | ENG_PG_WAR_PEACE | `Jesus`<br>`dyn_jesus_e` | 80356 | PG War and Peace | PG War and Peace | PG War and Peace | Jesus?” |
| `exact_center_word` | MT_WLC | `נתניהו` (ntnyhw; English: Netanyahu)<br>`dyn_netanyahu_h` | -175540 | 2Chr 2:9 | Jer 40:8 | Deut 9:11 | `נְתַנְיָ֡הוּ` (ntnyhw; English: Netanyahu) |
| `exact_center_word` | LXX | `μαγωγ` (magog; English: Magog)<br>`dyn_magog_g` | -314092 | 3MA 5:15 | EZK 38:2 | PSA 30:8 | `Μαγώγ,` (magog; English: Magog) |
| `exact_center_word` | LXX | `μαγωγ` (magog; English: Magog)<br>`dyn_magog_g` | -91298 | 2CH 36:15 | 1CH 1:5 | 1KI 2:39 | `Μαγώγ,` (magog; English: Magog) |

## Read

- Hidden-code presence and exact surface-center matches are separate observations.
- The current export includes all hits for manageable count rows and defers dense rows for partitioned export.
- A version-specific hit can be meaningful as a distribution fact even when the same term is absent elsewhere.
- Non-Bible controls are comparison backgrounds, not negative conclusion by themselves.
