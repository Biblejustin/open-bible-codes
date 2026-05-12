# Windows CPU Broad 2..500 Surface Follow-Up

This is a bounded hit-level follow-up to the Windows CPU broad `2..500`
Bible-control comparison. It uses the 30 strongest original-language
Bible-over-control rows as a review queue, then runs `surface-context`
with `--include-all` so hidden-path-only hits remain visible.

## Scope

- summary input: `reports/windows_cpu/broad_2_500/followup_surface_context_summary.csv`
- hit input: `reports/windows_cpu/broad_2_500/followup_surface_context.csv`
- summary rows: 150
- sampled hit rows: 16755
- summary rows with any surface context: 113
- exact center-word hit rows: 12
- corpora represented in sampled hits: 10

## Main Read

- Exact center-word hits are rare but present in this bounded follow-up.
- The Jesus/Joshua rows share the same normalized Greek spelling (`ιησουσ`), so referent review matters.
- The `Bashan` rows are morphological/substring matches to torment language, not the place name Bashan.
- Rows with context count zero are still retained as hidden-path-only evidence.
- This is a capped review queue, not a complete all-hit export for the selected terms.

## Exact Center-Word Hits

| Term | Corpus | Skip | Center | Surface word | Center verse text | Path | Context refs |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `jacob_g` `ιακωβ` (iakob; English: Jacob) | LXX | 185 | 1CH 1:34 | `Ἰακὼβ` | καὶ ἐγέννησεν Ἁβραὰμ τὸν Ἰσαάκ. καὶ υἱοὶ Ἰσαάκ· Ἰακὼβ καὶ Ἡσαῦ. | 1CH 1:28 -> 1CH 1:42 | 1CH 1:34 |
| `kyrios_gnt` `κυριοσ` (kyrios; English: Lord) | LXX | -224 | JER 11:21 | `Κύριος` | διὰ τοῦτο τάδε λέγει Κύριος ἐπὶ τοὺς ἄνδρας Ἀναθὼθ τοὺς ζητοῦντας τὴν ψυχήν μου, τοὺς λέγοντας· οὐ μὴ προφητεύσεις ἐπὶ τῷ ὀνόματι Κυρίου, εἰ δὲ μή, ἀποθάνῃ ἐν ταῖς χερσὶν ἡμῶν. | JER 12:3 -> JER 11:16 | JER 11:16;JER 11:17;JER 11:21 |
| `kyrios_gnt` `κυριοσ` (kyrios; English: Lord) | LXX | 277 | PSA 117:24 | `Κύριος·` | αὕτη ἡ ἡμέρα, ἣν ἐποίησεν ὁ Κύριος· ἀγαλλιασώμεθα καὶ εὐφρανθῶμεν ἐν αὐτῇ. | PSA 117:12 -> PSA 118:6 | PSA 117:13;PSA 117:14;PSA 117:18;PSA 117:24;PSA 117:27 |
| `kyrios_gnt` `κυριοσ` (kyrios; English: Lord) | LXX | -359 | LEV 24:22 | `Κύριος` | δικαίωσις μία ἔσται τῷ προσηλύτῳ καὶ τῷ ἐγχωρίῳ, ὅτι ἐγώ εἰμι Κύριος ὁ Θεὸς ὑμῶν. | LEV 25:8 -> LEV 24:11 | LEV 24:13;LEV 24:22;LEV 24:23;LEV 25:1 |
| `bashan_g` `βασαν` (basan; English: Bashan) | TR_NT | -62 | REV 11:10 | `ἐβασάνισαν` | Καὶ οἱ κατοικοῦντες ἐπὶ τῆς γῆς χαροῦσιν ἐπ ᾿ αὐτοῖς καὶ εὐφρανθήσονται , καὶ δῶρα πέμψουσιν ἀλλήλοις , ὅτι οὗτοι οἱ δύο προφῆται ἐβασάνισαν τοὺς κατοικοῦντας ἐπὶ τῆς γῆς . | REV 11:11 -> REV 11:9 | REV 11:10 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | BYZ_NT | -192 | JHN 8:6 | `ιησουσ` | τουτο δε ελεγον πειραζοντεσ αυτον ινα εχωσιν κατηγορειν αυτου ο δε ιησουσ κατω κυψασ τω δακτυλω εγραφεν εισ την γην μη προσποιουμενοσ | JHN 8:11 -> JHN 7:52 | JHN 8:1;JHN 8:6;JHN 8:9;JHN 8:10;JHN 8:11 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | BYZ_NT | -192 | JHN 8:6 | `ιησουσ` | τουτο δε ελεγον πειραζοντεσ αυτον ινα εχωσιν κατηγορειν αυτου ο δε ιησουσ κατω κυψασ τω δακτυλω εγραφεν εισ την γην μη προσποιουμενοσ | JHN 8:11 -> JHN 7:52 | JHN 8:1;JHN 8:6;JHN 8:9;JHN 8:10;JHN 8:11 |
| `bashan_g` `βασαν` (basan; English: Bashan) | SBLGNT | 194 | Rev 14:11 | `βασανισμοῦ` | καὶ ὁ καπνὸς τοῦ βασανισμοῦ αὐτῶν εἰς αἰῶνας αἰώνων ἀναβαίνει, καὶ οὐκ ἔχουσιν ἀνάπαυσιν ἡμέρας καὶ νυκτός, οἱ προσκυνοῦντες τὸ θηρίον καὶ τὴν εἰκόνα αὐτοῦ, καὶ εἴ τις λαμβάνει τὸ… | Rev 14:8 -> Rev 14:14 | Rev 14:10;Rev 14:11 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | SBLGNT | -141 | Heb 13:8 | `Ἰησοῦς` | Ἰησοῦς Χριστὸς ἐχθὲς καὶ σήμερον ὁ αὐτός, καὶ εἰς τοὺς αἰῶνας. | Heb 13:12 -> Heb 13:3 | Heb 13:8;Heb 13:12 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | SBLGNT | -192 | John 8:6 | `Ἰησοῦς` | τοῦτο δὲ ἔλεγον πειράζοντες αὐτόν, ἵνα ἔχωσιν κατηγορεῖν αὐτοῦ. ὁ δὲ Ἰησοῦς κάτω κύψας, τῷ δακτύλῳ ἔγραφεν εἰς τὴν γῆν, μὴ προσποιούμενος. | John 8:11 -> John 7:52 | John 8:1;John 8:6;John 8:9;John 8:10;John 8:11 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | SBLGNT | -141 | Heb 13:8 | `Ἰησοῦς` | Ἰησοῦς Χριστὸς ἐχθὲς καὶ σήμερον ὁ αὐτός, καὶ εἰς τοὺς αἰῶνας. | Heb 13:12 -> Heb 13:3 | Heb 13:8;Heb 13:12 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | SBLGNT | -192 | John 8:6 | `Ἰησοῦς` | τοῦτο δὲ ἔλεγον πειράζοντες αὐτόν, ἵνα ἔχωσιν κατηγορεῖν αὐτοῦ. ὁ δὲ Ἰησοῦς κάτω κύψας, τῷ δακτύλῳ ἔγραφεν εἰς τὴν γῆν, μὴ προσποιούμενος. | John 8:11 -> John 7:52 | John 8:1;John 8:6;John 8:9;John 8:10;John 8:11 |

## Highest Surface-Context Summary Rows

| Term | Corpus | Hits sampled | Context hits | Exact center-word | Exact center | Exact span | Same-category span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `kyrios_gnt` `κυριοσ` (kyrios; English: Lord) | LXX | 200 | 114 | 3 | 31 | 114 | 4 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | SBLGNT | 85 | 23 | 2 | 9 | 23 | 0 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | SBLGNT | 85 | 23 | 2 | 9 | 23 | 0 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | BYZ_NT | 79 | 31 | 1 | 8 | 31 | 0 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | BYZ_NT | 79 | 31 | 1 | 8 | 31 | 0 |
| `jacob_g` `ιακωβ` (iakob; English: Jacob) | LXX | 200 | 26 | 1 | 5 | 15 | 17 |
| `bashan_g` `βασαν` (basan; English: Bashan) | SBLGNT | 200 | 16 | 1 | 4 | 9 | 8 |
| `bashan_g` `βασαν` (basan; English: Bashan) | TR_NT | 200 | 15 | 1 | 2 | 8 | 7 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | TR_NT | 94 | 41 | 0 | 6 | 41 | 0 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | TR_NT | 94 | 41 | 0 | 6 | 41 | 0 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | LXX | 200 | 15 | 0 | 4 | 15 | 0 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | LXX | 200 | 15 | 0 | 4 | 15 | 0 |
| `bashan_g` `βασαν` (basan; English: Bashan) | LXX | 200 | 6 | 0 | 4 | 5 | 1 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | TR_NT | 200 | 12 | 0 | 3 | 3 | 11 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | SBLGNT | 200 | 10 | 0 | 3 | 4 | 10 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | BYZ_NT | 200 | 7 | 0 | 3 | 3 | 7 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | TCG_NT | 75 | 25 | 0 | 2 | 25 | 0 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | TCG_NT | 75 | 25 | 0 | 2 | 25 | 0 |
| `bashan_g` `βασαν` (basan; English: Bashan) | TCG_NT | 200 | 15 | 0 | 2 | 10 | 5 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | TCG_NT | 200 | 9 | 0 | 2 | 2 | 8 |
| `gaza_g` `γαζα` (gaza; English: Gaza) | LXX | 200 | 6 | 0 | 2 | 3 | 3 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | 200 | 4 | 0 | 2 | 2 | 2 |
| `syria_g` `συρια` (suria; English: Syria) | LXX | 200 | 3 | 0 | 2 | 3 | 0 |
| `seba_g` `σαβα` (saba; English: Seba) | BYZ_NT | 200 | 2 | 0 | 2 | 2 | 0 |
| `seba_g` `σαβα` (saba; English: Seba) | TCG_NT | 200 | 2 | 0 | 2 | 2 | 0 |
| `kyrios_gnt` `κυριοσ` (kyrios; English: Lord) | SBLGNT | 30 | 8 | 0 | 1 | 8 | 0 |
| `jacob_g` `ιακωβ` (iakob; English: Jacob) | BYZ_NT | 47 | 6 | 0 | 1 | 4 | 3 |
| `cyrus_g` `κυροσ` (kuros; English: Cyrus) | LXX | 200 | 4 | 0 | 1 | 1 | 3 |
| `prophet_isaiah_g` `ησαιασ` (esaias; English: Isaiah) | SBLGNT | 198 | 4 | 0 | 1 | 4 | 0 |
| `jacob_g` `ιακωβ` (iakob; English: Jacob) | SBLGNT | 40 | 4 | 0 | 1 | 2 | 2 |

## Hidden-Path-Only Sample Rows

These sampled rows had hidden hits in the bounded follow-up but no exact,
same-concept, or same-category surface-context promotion.

| Term | Corpus | Hits sampled | Exact center-word | Context hits |
| --- | --- | ---: | ---: | ---: |
| `prophet_isaiah_g` `ησαιασ` (esaias; English: Isaiah) | LXX | 200 | 0 | 0 |
| `syria_g` `συρια` (suria; English: Syria) | TR_NT | 200 | 0 | 0 |
| `javan_g` `ιωυαν` (Iouan; English: Javan) | TR_NT | 200 | 0 | 0 |
| `syria_g` `συρια` (suria; English: Syria) | BYZ_NT | 200 | 0 | 0 |
| `javan_g` `ιωυαν` (Iouan; English: Javan) | BYZ_NT | 200 | 0 | 0 |
| `syria_g` `συρια` (suria; English: Syria) | TCG_NT | 200 | 0 | 0 |
| `seba_g` `σαβα` (saba; English: Seba) | SBLGNT | 200 | 0 | 0 |
| `javan_g` `ιωυαν` (Iouan; English: Javan) | SBLGNT | 200 | 0 | 0 |
| `cainan_g` `καιναν` (kainan; English: Cainan) | TCG_NT | 166 | 0 | 0 |
| `kittim_g` `κιτιοι` (kitioi; English: Kittim) | SBLGNT | 145 | 0 | 0 |
| `year_2001_additive_h` `תתתתתא` (ttttt; English: Gregorian 2001) | MAM | 82 | 0 | 0 |
| `year_2001_additive_h` `תתתתתא` (ttttt; English: Gregorian 2001) | UHB | 79 | 0 | 0 |
| `year_2001_additive_h` `תתתתתא` (ttttt; English: Gregorian 2001) | UXLC | 69 | 0 | 0 |
| `year_2001_additive_h` `תתתתתא` (ttttt; English: Gregorian 2001) | MT_WLC | 68 | 0 | 0 |
| `year_2001_additive_h` `תתתתתא` (ttttt; English: Gregorian 2001) | EBIBLE_WLC | 68 | 0 | 0 |
| `tacitus_g` `τακιτοσ` (takitos; English: Tacitus) | TCG_NT | 20 | 0 | 0 |
| `rosh_hashanah_h` `ראשהשנה` (rshhshnh; English: Rosh Hashanah) | MAM | 10 | 0 | 0 |
| `rosh_hashanah_h` `ראשהשנה` (rshhshnh; English: Rosh Hashanah) | UHB | 10 | 0 | 0 |
| `jobab_g` `ιωβαβ` (iobab; English: Jobab) | SBLGNT | 10 | 0 | 0 |
| `rosh_hashanah_h` `ראשהשנה` (rshhshnh; English: Rosh Hashanah) | MT_WLC | 9 | 0 | 0 |

## Corpus Hit Rows

| Corpus | Sampled hit rows |
| --- | ---: |
| LXX | 4054 |
| SBLGNT | 2852 |
| BYZ_NT | 2838 |
| TR_NT | 2799 |
| TCG_NT | 2799 |
| MAM | 292 |
| UHB | 289 |
| UXLC | 278 |
| MT_WLC | 277 |
| EBIBLE_WLC | 277 |

## Caution

This follow-up intentionally keeps hidden-path-only rows. The meaningful
next distinction is not frequency alone; it is whether a hidden path is
centered on the same word, a related word, a relevant center verse, or
only present as a hidden sequence without surface support.
