# Windows CPU Broad 2..500 Surface Follow-Up

This is a full contextual follow-up to the Windows CPU broad `2..500`
Bible-control comparison. It uses the 30 strongest original-language
Bible-over-control rows as a review queue, then runs `surface-context`
without a per-term hit cap. The summary counts all hidden hits in scope;
the hit CSV writes context-bearing rows rather than exporting every hit.

## Scope

- summary input: `reports/windows_cpu/broad_2_500/followup_surface_context_full_context_summary.csv`
- hit input: `reports/windows_cpu/broad_2_500/followup_surface_context_full_context.csv`
- summary rows: 150
- context hit rows written: 8386
- summary rows with any surface context: 121
- exact center-word hit rows: 65
- corpora represented in context hit rows: 10
- control summary rows: 90
- control context hit rows written: 18646
- control exact center-word hit rows: 0

## Main Read

- Exact center-word hits are rare but present in this full contextual follow-up.
- The matched non-Bible controls produced zero exact center-word hits under the same uncapped summary rules.
- The Jesus/Joshua rows share the same normalized Greek spelling (`ιησουσ`), so referent review matters.
- The `Bashan` rows are morphological/substring matches to torment language, not the place name Bashan.
- Summary rows with context count zero are still retained as hidden-path-only evidence.
- This is a complete summary count for the selected terms and corpora, not a full row export of every hit.

## Bible Vs Control Surface Follow-Up

| Cohort | Summary rows | Context hit rows written | Rows with context | Exact center-word hit rows |
| --- | ---: | ---: | ---: | ---: |
| Bible corpora | 150 | 8386 | 121 | 65 |
| Non-Bible controls | 90 | 18646 | 57 | 0 |

## Exact Center-Word Hits

| Term | Corpus | Skip | Center | Surface word | Center verse text | Path | Context refs |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `jacob_g` `ιακωβ` (iakob; English: Jacob) | LXX | 185 | 1CH 1:34 | `Ἰακὼβ` | καὶ ἐγέννησεν Ἁβραὰμ τὸν Ἰσαάκ. καὶ υἱοὶ Ἰσαάκ· Ἰακὼβ καὶ Ἡσαῦ. | 1CH 1:28 -> 1CH 1:42 | 1CH 1:34 |
| `jacob_g` `ιακωβ` (iakob; English: Jacob) | LXX | 302 | PSA 86:2 | `Ἰακώβ.` | ἀγαπᾷ Κύριος τὰς πύλας Σιὼν ὑπὲρ πάντα τὰ σκηνώματα Ἰακώβ. | PSA 85:11 -> PSA 87:5 | PSA 86:2 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | 31 | GEN 24:64 | `Ἰσαὰκ` | καὶ ἀναβλέψασα Ρεβέκκα τοῖς ὀφθαλμοῖς εἶδε τὸν Ἰσαὰκ καὶ κατεπήδησεν ἀπὸ τῆς καμήλου. | GEN 24:63 -> GEN 24:65 | GEN 24:63;GEN 24:64 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | 34 | DEU 34:4 | `Ἰσαὰκ` | καὶ εἶπε Κύριος πρὸς Μωυσῆν· αὕτη ἡ γῆ, ἣν ὤμοσα τῷ Ἁβραὰμ καὶ Ἰσαὰκ καὶ Ἰακὼβ λέγων· τῷ σπέρματι ὑμῶν δώσω αὐτήν· καὶ ἔδειξα τοῖς ὀφθαλμοῖς σου, καὶ ἐκεῖ οὐκ εἰσελεύσῃ. | DEU 34:3 -> DEU 34:4 | DEU 34:4 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | 67 | GEN 26:1 | `Ἰσαὰκ` | ΕΓΕΝΕΤΟ δὲ λιμὸς ἐπὶ τῆς γῆς χωρὶς τοῦ λιμοῦ τοῦ πρότερον, ὃς ἐγένετο ἐν τῷ καιρῷ τοῦ Ἁβραάμ· ἐπορεύθη δὲ Ἰσαὰκ πρὸς Ἀβιμέλεχ βασιλέα Φυλιστιεὶμ εἰς Γέραρα. | GEN 25:34 -> GEN 26:3 | GEN 26:1 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | -86 | 1CH 1:28 | `Ἰσαὰκ` | υἱοὶ δὲ Ἁβραάμ· Ἰσαὰκ καὶ Ἰσμαήλ. | 1CH 1:32 -> 1CH 1:22 | 1CH 1:28 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | 111 | GEN 21:5 | `Ἰσαὰκ` | καὶ Ἁβραὰμ ἦν ἑκατὸν ἐτῶν, ἡνίκα ἐγένετο αὐτῷ Ἰσαὰκ ὁ υἱὸς αὐτοῦ. | GEN 21:2 -> GEN 21:8 | GEN 21:3;GEN 21:4;GEN 21:5;GEN 21:8 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | -126 | GEN 24:62 | `Ἰσαὰκ` | Ἰσαὰκ δὲ διεπορεύετο διὰ τῆς ἐρήμου κατὰ τὸ φρέαρ τῆς ὁράσεως· αὐτὸς δὲ κατώκει ἐν τῇ γῇ τῇ πρὸς λίβα. | GEN 24:65 -> GEN 24:59 | GEN 24:62;GEN 24:63;GEN 24:64 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | 146 | 1KI 18:36 | `Ἰσαὰκ` | καὶ ἀνεβόησεν Ἠλιοὺ εἰς τὸν οὐρανὸν καὶ εἶπε· Κύριε ὁ Θεὸς Ἁβραὰμ καὶ Ἰσαὰκ καὶ Ἰσραήλ, ἐπάκουσόν μου, Κύριε, ἐπάκουσόν μου σήμερον ἐν πυρί, καὶ γνώτωσαν πᾶς ὁ λαὸς οὗτος ὅτι σὺ ε… | 1KI 18:33 -> 1KI 18:38 | 1KI 18:36 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | 205 | GEN 35:28 | `Ἰσαάκ,` | ἐγένοντο δὲ αἱ ἡμέραι Ἰσαάκ, ἃς ἔζησεν, ἔτη ἑκατὸν ὀγδοήκοντα, | GEN 35:21 -> GEN 36:5 | GEN 35:27;GEN 35:28;GEN 35:29 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | -205 | GEN 17:19 | `Ἰσαάκ,` | εἶπε δὲ ὁ Θεὸς πρὸς Ἁβραὰμ· ναί· ἰδοὺ Σάρρα ἡ γυνή σου τέξεταί σοι υἱόν, καὶ καλέσεις τὸ ὄνομα αὐτοῦ Ἰσαάκ, καὶ στήσω τὴν διαθήκην μου πρὸς αὐτὸν εἰς διαθήκην αἰώνιον, εἶναι αὐτῷ… | GEN 17:23 -> GEN 17:15 | GEN 17:19;GEN 17:21 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | -217 | EXO 6:8 | `Ἰσαὰκ` | καὶ εἰσάξω ὑμᾶς εἰς τὴν γῆν, εἰς ἣν ἐξέτεινα τὴν χεῖρά μου, δοῦναι αὐτὴν τῷ Ἁβραὰμ καὶ Ἰσαὰκ καὶ Ἰακώβ, καὶ δώσω ὑμῖν αὐτὴν ἐν κλήρῳ· ἐγὼ Κύριος. | EXO 6:13 -> EXO 6:5 | EXO 6:8 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | -304 | DEU 30:20 | `Ἰσαὰκ` | ἀγαπᾶν Κύριον τὸν Θεόν σου, εἰσακούειν τῆς φωνῆς αὐτοῦ καὶ ἔχεσθαι αὐτοῦ· ὅτι τοῦτο ἡ ζωή σου καὶ ἡ μακρότης τῶν ἡμερῶν σου, κατοικεῖν ἐπὶ τῆς γῆς, ἧς ὤμοσε Κύριος τοῖς πατράσι σο… | DEU 31:6 -> DEU 30:16 | DEU 30:20 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | 311 | GEN 21:5 | `Ἰσαὰκ` | καὶ Ἁβραὰμ ἦν ἑκατὸν ἐτῶν, ἡνίκα ἐγένετο αὐτῷ Ἰσαὰκ ὁ υἱὸς αὐτοῦ. | GEN 20:16 -> GEN 21:12 | GEN 21:3;GEN 21:4;GEN 21:5;GEN 21:8;GEN 21:9;GEN 21:10;GEN 21:12 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | -319 | DEU 1:8 | `Ἰσαὰκ` | ἴδετε, παραδέδωκεν ἐνώπιον ὑμῶν τῆν γῆν· εἰσπορευθέντες κληρονομήσατε τὴν γῆν, ἣν ὤμοσα τοῖς πατράσιν ὑμῶν, τῷ Ἁβραὰμ καὶ Ἰσαὰκ καὶ Ἰακὼβ δοῦναι αὐτοῖς καὶ τῷ σπέρματι αὐτῶν μετ᾿… | DEU 1:15 -> DEU 1:3 | DEU 1:8 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | 328 | GEN 27:46 | `Ἰσαάκ·` | Εἶπε δὲ Ρεβέκκα πρὸς Ἰσαάκ· προσώχθικα τῇ ζωῇ μου διὰ τὰς θυγατέρας τῶν υἱῶν Χέτ· εἰ λήψεται Ἰακὼβ γυναῖκα ἀπὸ τῶν θυγατέρων τῆς γῆς ταύτης, ἵνα τί μοι τὸ ζῆν; | GEN 27:40 -> GEN 28:5 | GEN 27:46;GEN 28:1;GEN 28:5 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | 332 | GEN 48:15 | `Ἰσαάκ,` | καὶ εὐλόγησεν αὐτοὺς καὶ εἶπεν· ὁ Θεός, ᾧ εὐηρέστησαν οἱ πατέρες μου ἐνώπιον αὐτοῦ, Ἁβραὰμ καὶ Ἰσαάκ, ὁ Θεὸς ὁ τρέφων με ἐκ νεότητος ἕως τῆς ἡμέρας ταύτης, | GEN 48:9 -> GEN 48:20 | GEN 48:15;GEN 48:16 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | -372 | GEN 25:5 | `Ἰσαὰκ` | Ἔδωκε δὲ Ἁβραὰμ πάντα τὰ ὑπάρχοντα αὐτοῦ Ἰσαὰκ τῷ υἱῷ αὐτοῦ, | GEN 25:13 -> GEN 24:64 | GEN 24:64;GEN 24:66;GEN 24:67;GEN 25:5;GEN 25:6;GEN 25:9;GEN 25:11 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | -430 | GEN 27:20 | `Ἰσαὰκ` | εἶπε δὲ Ἰσαὰκ τῷ υἱῷ αὐτοῦ· τί τοῦτο, ὃ ταχὺ εὗρες, ὦ τέκνον; ὁ δὲ εἶπεν· ὃ παρέδωκε Κύριος ὁ Θεός σου ἐναντίον μου. | GEN 27:29 -> GEN 27:10 | GEN 27:20;GEN 27:21;GEN 27:22;GEN 27:26 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | -461 | GEN 26:8 | `Ἰσαὰκ` | ἐγένετο δὲ πολυχρόνιος ἐκεῖ· καὶ παρακύψας Ἀβιμέλεχ ὁ βασιλεὺς Γεράρων διὰ τῆς θυρίδος, εἶδε τὸν Ἰσαὰκ παίζοντα μετὰ Ρεβέκκας τῆς γυναικὸς αὐτοῦ. | GEN 26:18 -> GEN 25:34 | GEN 26:1;GEN 26:6;GEN 26:8;GEN 26:9;GEN 26:12;GEN 26:16;GEN 26:17;GEN 26:18 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | -488 | JDT 8:26 | `Ἰσαὰκ` | μνήσθητε ὅσα ἐποίησε μετὰ Ἁβραὰμ καὶ ὅσα ἐπείρασε τὸν Ἰσαὰκ καὶ ὅσα ἐγένετο τῷ Ἰακὼβ ἐν Μεσοποταμίᾳ τῆς Συρίας ποιμαίνοντι τὰ πρόβατα Λάβαν τοῦ ἀδελφοῦ τῆς μητρὸς αὐτοῦ. | JDT 8:35 -> JDT 8:18 | JDT 8:26 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | -5 | 2ES 1:11 | `Σασαβασὰρ` | πάντα τὰ σκεύη τῷ χρυσῷ καὶ τῷ ἀργυρῷ πεντακισχίλια καὶ τετρακόσια, τὰ πάντα ἀναβαίνοντα μετὰ Σασαβασὰρ ἀπὸ τῆς ἀποικίας ἐκ Βαβυλῶνος εἰς Ἱερουσαλήμ. | 2ES 1:11 -> 2ES 1:11 | 2ES 1:11 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | 30 | ISA 7:7 | `σαβαώθ·` | τάδε λέγει Κύριος σαβαώθ· οὐ μὴ μείνῃ ἡ βουλὴ αὕτη οὐδὲ ἔσται· | ISA 7:6 -> ISA 7:8 | ISA 7:7 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | -31 | ISA 6:5 | `σαβαὼθ` | καὶ εἶπον· ὦ τάλας ἐγώ, ὅτι κατανένυγμαι, ὅτι ἄνθρωπος ὢν καὶ ἀκάθαρτα χείλη ἔχων, ἐν μέσῳ λαοῦ ἀκάθαρτα χείλη ἔχοντος ἐγὼ οἰκῶ καὶ τὸν βασιλέα Κύριον σαβαὼθ εἶδον τοῖς ὀφθαλμοῖς… | ISA 6:6 -> ISA 6:5 | ISA 6:5 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | 48 | 2ES 1:11 | `Σασαβασὰρ` | πάντα τὰ σκεύη τῷ χρυσῷ καὶ τῷ ἀργυρῷ πεντακισχίλια καὶ τετρακόσια, τὰ πάντα ἀναβαίνοντα μετὰ Σασαβασὰρ ἀπὸ τῆς ἀποικίας ἐκ Βαβυλῶνος εἰς Ἱερουσαλήμ. | 2ES 1:11 -> 2ES 2:1 | 2ES 1:11 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | -117 | 1SA 15:2 | `Σαβαώθ·` | τάδε εἶπε Κύριος Σαβαώθ· νῦν ἐκδικήσω ἃ ἐποίησεν Ἀμαλὴκ τῷ Ἰσραήλ, ὡς ἀπήντησεν αὐτῷ ἐν τῇ ὁδῷ ἀναβαίνοντος αὐτοῦ ἐξ Αἰγύπτου· | 1SA 15:3 -> 1SA 14:52 | 1SA 15:2 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | -197 | NEH 10:10 | `Σαβανία,` | καὶ οἱ ἀδελφοὶ αὐτοῦ, Σαβανία, Ὠδουΐα, Καλιτάν, Φελία, Ἀνάν, | NEH 10:25 -> NEH 9:38 | NEH 10:10;NEH 10:25 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | 220 | 1ES 9:28 | `Σάβαθος` | καὶ ἐκ τῶν υἱῶν Ζαμώθ, Ἐλιαδάς, Ἐλιάσιμος, Ὀθονίας Ἰαριμὼθ καὶ Σάβαθος καὶ Ζεραλίας· | 1ES 9:23 -> 1ES 9:33 | 1ES 9:28;1ES 9:33 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | 267 | NEH 10:10 | `Σαβανία,` | καὶ οἱ ἀδελφοὶ αὐτοῦ, Σαβανία, Ὠδουΐα, Καλιτάν, Φελία, Ἀνάν, | NEH 9:37 -> NEH 10:28 | NEH 10:10;NEH 10:25 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | 276 | NEH 10:10 | `Σαβανία,` | καὶ οἱ ἀδελφοὶ αὐτοῦ, Σαβανία, Ὠδουΐα, Καλιτάν, Φελία, Ἀνάν, | NEH 9:37 -> NEH 10:28 | NEH 10:10;NEH 10:25 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | -286 | NEH 10:10 | `Σαβανία,` | καὶ οἱ ἀδελφοὶ αὐτοῦ, Σαβανία, Ὠδουΐα, Καλιτάν, Φελία, Ἀνάν, | NEH 10:28 -> NEH 9:37 | NEH 10:10;NEH 10:25 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | 294 | 1ES 9:46 | `Σαβαὼθ` | καὶ ἐν τῷ λῦσαι τὸν νόμον πάντες ὀρθοὶ ἔστησαν. καὶ εὐλόγησεν Ἔσδρας τῷ Κυρίῳ Θεῷ Ὑψίστῳ Θεῷ Σαβαὼθ παντοκράτορι, | 1ES 9:41 -> 1ES 9:50 | 1ES 9:46 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | 312 | 1ES 9:46 | `Σαβαὼθ` | καὶ ἐν τῷ λῦσαι τὸν νόμον πάντες ὀρθοὶ ἔστησαν. καὶ εὐλόγησεν Ἔσδρας τῷ Κυρίῳ Θεῷ Ὑψίστῳ Θεῷ Σαβαὼθ παντοκράτορι, | 1ES 9:41 -> 1ES 9:50 | 1ES 9:46 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | -387 | ISA 13:13 | `σαβαὼθ` | ὁ γὰρ οὐρανὸς θυμωθήσεται καὶ ἡ γῆ σεισθήσεται ἐκ τῶν θεμελίων σαβαὼθ ἐν τῇ ἡμέρᾳ, ᾗ ἂν ἐπέλθῃ ὁ θυμὸς αὐτοῦ. | ISA 13:19 -> ISA 13:8 | ISA 13:13 |
| `syria_g` `συρια` (suria; English: Syria) | LXX | -210 | 1KI 22:31 | `Συρίας` | καὶ βασιλεὺς Συρίας ἐνετείλατο τοῖς ἄρχουσι τῶν ἁρμάτων αὐτοῦ τριάκοντα καὶ δυσὶ λέγων· μὴ πολεμεῖτε μικρὸν καὶ μέγαν, ἀλλ᾿ ἢ τὸν βασιλέα Ἰσραὴλ μονώτατον. | 1KI 22:34 -> 1KI 22:26 | 1KI 22:31 |
| `syria_g` `συρια` (suria; English: Syria) | LXX | 214 | 2KI 9:14 | `Συρίας,` | καὶ συνεστράφη Ἰοὺ υἱὸς Ἰωσαφὰτ υἱοῦ Ναμεσσὶ πρὸς Ἰωρὰμ καὶ Ἰωρὰμ αὐτὸς ἐφύλασσεν ἐν Ρεμμὼθ Γαλαάδ, αὐτὸς καὶ πᾶς Ἰσραὴλ ἀπὸ προσώπου Ἀζαὴλ βασιλέως Συρίας, | 2KI 9:11 -> 2KI 9:16 | 2KI 9:14;2KI 9:15;2KI 9:16 |
| `syria_g` `συρια` (suria; English: Syria) | LXX | -231 | 1MA 11:60 | `Συρίας` | καὶ ἐξῆλθεν Ἰωνάθαν καὶ διεπορεύετο πέραν τοῦ ποταμοῦ καὶ ἐν ταῖς πόλεσι, καὶ ἠθροίσθησαν πρὸς αὐτὸν πᾶσαι αἱ δυνάμεις Συρίας εἰς συμμαχίαν, καὶ ἦλθεν εἰς Ἀσκάλωνα, καὶ ἀπήντησαν… | 1MA 11:63 -> 1MA 11:56 | 1MA 11:60 |
| `syria_g` `συρια` (suria; English: Syria) | LXX | 268 | 1KI 21:22 | `Συρίας` | καὶ προσῆλθεν ὁ προφήτης πρὸς βασιλέα Ἰσραὴλ καὶ εἶπε· κραταιοῦ καὶ γνῶθι καὶ ἴδε τί ποιήσεις, ὅτι ἐπιστρέφοντος τοῦ ἐνιαυτοῦ υἱὸς Ἄδερ βασιλεὺς Συρίας ἀναβαίνει ἐπὶ σέ. | 1KI 21:17 -> 1KI 21:27 | 1KI 21:17;1KI 21:20;1KI 21:21;1KI 21:22;1KI 21:23;1KI 21:26;1KI 21:27 |
| `syria_g` `συρια` (suria; English: Syria) | LXX | 303 | 2SA 10:19 | `Συρία` | καὶ εἶδαν πάντες οἱ βασιλεῖς οἱ δοῦλοι Ἀδρααζὰρ ὅτι ἔπταισαν ἔμπροσθεν Ἰσραήλ, καὶ ηὐτομόλησαν μετὰ Ἰσραὴλ καὶ ἐδούλευσαν αὐτοῖς. καὶ ἐφοβήθη Συρία τοῦ σῶσαι ἔτι τοὺς υἱοὺς Ἀμμών. | 2SA 10:15 -> 2SA 11:4 | 2SA 10:15;2SA 10:16;2SA 10:17;2SA 10:18;2SA 10:19 |
| `syria_g` `συρια` (suria; English: Syria) | LXX | -330 | 2SA 10:18 | `Συρία` | καὶ ἔφυγε Συρία ἀπὸ προσώπου Ἰσραήλ, καὶ ἀνεῖλε Δαυὶδ ἐκ τῆς Συρίας ἑπτακόσια ἅρματα καὶ τεσσαράκοντα χιλιάδας ἱππέων· καὶ τὸν Σωβὰκ τὸν ἄρχοντα τῆς δυνάμεως αὐτοῦ ἐπάταξε, καὶ ἀπ… | 2SA 11:2 -> 2SA 10:12 | 2SA 10:13;2SA 10:14;2SA 10:15;2SA 10:16;2SA 10:17;2SA 10:18;2SA 10:19 |
| `syria_g` `συρια` (suria; English: Syria) | LXX | -343 | 2CH 28:5 | `Συρίας,` | καὶ παρέδωκεν αὐτὸν Κύριος ὁ Θεὸς αὐτοῦ διὰ χειρὸς βασιλέως Συρίας, καὶ ἐπάταξεν ἐν αὐτῷ καὶ ᾐχμαλώτευσεν ἐξ αὐτῶν αἰχμαλωσίαν πολλὴν καὶ ἤγαγεν εἰς Δαμασκόν· καὶ γὰρ εἰς χεῖρας β… | 2CH 28:9 -> 2CH 27:6 | 2CH 28:5 |
| `syria_g` `συρια` (suria; English: Syria) | LXX | -346 | JDT 8:26 | `Συρίας` | μνήσθητε ὅσα ἐποίησε μετὰ Ἁβραὰμ καὶ ὅσα ἐπείρασε τὸν Ἰσαὰκ καὶ ὅσα ἐγένετο τῷ Ἰακὼβ ἐν Μεσοποταμίᾳ τῆς Συρίας ποιμαίνοντι τὰ πρόβατα Λάβαν τοῦ ἀδελφοῦ τῆς μητρὸς αὐτοῦ. | JDT 8:33 -> JDT 8:20 | JDT 8:26 |
| `bashan_g` `βασαν` (basan; English: Bashan) | LXX | -93 | WIS 19:4 | `βασάνοις` | εἷλκε γὰρ αὐτοὺς ἡ ἀξία ἐπὶ τοῦτο τὸ πέρας ἀνάγκη καὶ τῶν συμβεβηκότων ἀμνηστίαν ἐνέβαλεν, ἵνα τὴν λείπουσαν ταῖς βασάνοις προαναπληρώσωσι κόλασιν, | WIS 19:6 -> WIS 19:3 | WIS 19:4 |
| `bashan_g` `βασαν` (basan; English: Bashan) | LXX | -194 | 2MA 9:6 | `βασανισμοὺς` | εἰ δ' οἱ γέροντες τῶν Ἑβραίων διὰ τὴν εὐσέβειαν καὶ βασανισμοὺς ὑπομείναντες εὐσέβησαν, ἀποθάνοιμεν ἂν δικαιότερον ἡμεῖς οἱ νέοι, τὰς βασάνους τῶν σῶν ἀναγκῶν ὑπεριδόντες, ἃς καὶ… | 2MA 9:9 -> 2MA 9:1 | 2MA 9:5;2MA 9:6;2MA 9:7;2MA 9:9 |
| `bashan_g` `βασαν` (basan; English: Bashan) | LXX | 416 | 2MA 6:27 | `βασάνοις` | σὺ οἶσθα, Θεέ, παρόν μοι σῴζεσθαι, βασάνοις καυστικαῖς ἀποθνήσκω διὰ τὸν νόμον. | 2MA 6:17 -> 2MA 7:2 | 2MA 6:27;2MA 6:30;2MA 6:31;2MA 7:2 |
| `bashan_g` `βασαν` (basan; English: Bashan) | LXX | 477 | 2MA 17:3 | `βασάνων` | καθάπερ γὰρ σὺ στέγη ἐπὶ τοὺς στύλους τῶν παίδων γενναίως ἱδρυμένη, ἀκλινὴς ὑπήνεγκας τὸν διὰ τῶν βασάνων σεισμόν. | 2MA 16:18 -> 2MA 17:15 | 2MA 17:3;2MA 17:7;2MA 17:10 |
| `kyrios_gnt` `κυριοσ` (kyrios; English: Lord) | LXX | -224 | JER 11:21 | `Κύριος` | διὰ τοῦτο τάδε λέγει Κύριος ἐπὶ τοὺς ἄνδρας Ἀναθὼθ τοὺς ζητοῦντας τὴν ψυχήν μου, τοὺς λέγοντας· οὐ μὴ προφητεύσεις ἐπὶ τῷ ὀνόματι Κυρίου, εἰ δὲ μή, ἀποθάνῃ ἐν ταῖς χερσὶν ἡμῶν. | JER 12:3 -> JER 11:16 | JER 11:16;JER 11:17;JER 11:21 |
| `kyrios_gnt` `κυριοσ` (kyrios; English: Lord) | LXX | 277 | PSA 117:24 | `Κύριος·` | αὕτη ἡ ἡμέρα, ἣν ἐποίησεν ὁ Κύριος· ἀγαλλιασώμεθα καὶ εὐφρανθῶμεν ἐν αὐτῇ. | PSA 117:12 -> PSA 118:6 | PSA 117:13;PSA 117:14;PSA 117:18;PSA 117:24;PSA 117:27 |
| `kyrios_gnt` `κυριοσ` (kyrios; English: Lord) | LXX | -359 | LEV 24:22 | `Κύριος` | δικαίωσις μία ἔσται τῷ προσηλύτῳ καὶ τῷ ἐγχωρίῳ, ὅτι ἐγώ εἰμι Κύριος ὁ Θεὸς ὑμῶν. | LEV 25:8 -> LEV 24:11 | LEV 24:13;LEV 24:22;LEV 24:23;LEV 25:1 |
| `locust_g` `ακρισ` (akris; English: Locust) | LXX | -190 | EXO 10:12 | `ἀκρὶς` | εἶπε δὲ Κύριος πρὸς Μωυσῆν· ἔκτεινον τὴν χεῖρα ἐπὶ γῆν Αἰγύπτου, καὶ ἀναβήτω ἀκρὶς ἐπὶ τὴν γῆν καὶ κατέδεται πᾶσαν βοτάνην τῆς γῆς καὶ πάντα τὸν καρπὸν τῶν ξύλων, ὃν ὑπελίπετο ἡ χ… | EXO 10:15 -> EXO 10:9 | EXO 10:12;EXO 10:14 |
| `locust_g` `ακρισ` (akris; English: Locust) | LXX | -312 | NAM 3:15 | `ἀκρίς,` | ἐκεῖ καταφάγεταί σε πῦρ, ἐξολοθρεύσει σε ρομφαία, καταφάγεταί σε ὡς ἀκρίς, καὶ βαρυνθήσῃ ὡς βροῦχος. | HAB 1:3 -> NAM 3:9 | NAM 3:15;NAM 3:17 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | TR_NT | 270 | MRK 12:26 | `Ἰσαάκ` | Περὶ δὲ τῶν νεκρῶν , ὅτι ἐγείρονται , οὐκ ἀνέγνωτε ἐν τῇ βίβλῳ Μωσέως , ἐπὶ τῆς βάτου , ὡς εἶπεν αὐτῷ ὁ Θεός , λέγων , Ἐγὼ ὁ Θεὸς Ἀβραάμ , καὶ ὁ Θεὸς Ἰσαάκ , καὶ ὁ Θεὸς Ἰακώβ ; | MRK 12:20 -> MRK 12:32 | MRK 12:26 |
| `seba_g` `σαβα` (saba; English: Seba) | TR_NT | -267 | ACT 1:23 | `Βαρσαβᾶν` | Καὶ ἔστησαν δύο , Ἰωσὴφ τὸν καλούμενον Βαρσαβᾶν , ὃς ἐπεκλήθη Ἰοῦστος , καὶ Ματθίαν . | ACT 2:2 -> ACT 1:19 | ACT 1:23 |
| `bashan_g` `βασαν` (basan; English: Bashan) | TR_NT | -62 | REV 11:10 | `ἐβασάνισαν` | Καὶ οἱ κατοικοῦντες ἐπὶ τῆς γῆς χαροῦσιν ἐπ ᾿ αὐτοῖς καὶ εὐφρανθήσονται , καὶ δῶρα πέμψουσιν ἀλλήλοις , ὅτι οὗτοι οἱ δύο προφῆται ἐβασάνισαν τοὺς κατοικοῦντας ἐπὶ τῆς γῆς . | REV 11:11 -> REV 11:9 | REV 11:10 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | BYZ_NT | -192 | JHN 8:6 | `ιησουσ` | τουτο δε ελεγον πειραζοντεσ αυτον ινα εχωσιν κατηγορειν αυτου ο δε ιησουσ κατω κυψασ τω δακτυλω εγραφεν εισ την γην μη προσποιουμενοσ | JHN 8:11 -> JHN 7:52 | JHN 8:1;JHN 8:6;JHN 8:9;JHN 8:10;JHN 8:11 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | BYZ_NT | -192 | JHN 8:6 | `ιησουσ` | τουτο δε ελεγον πειραζοντεσ αυτον ινα εχωσιν κατηγορειν αυτου ο δε ιησουσ κατω κυψασ τω δακτυλω εγραφεν εισ την γην μη προσποιουμενοσ | JHN 8:11 -> JHN 7:52 | JHN 8:1;JHN 8:6;JHN 8:9;JHN 8:10;JHN 8:11 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | TCG_NT | -273 | MAT 22:32 | `Ἰσαάκ` | Ἐγώ εἰμι ὁ Θεὸς Ἁβραάμ , καὶ ὁ Θεὸς Ἰσαάκ , καὶ ὁ Θεὸς Ἰακώβ ; Οὐκ ἔστιν ὁ Θεὸς Θεὸς νεκρῶν , ἀλλὰ ζώντων . | MAT 22:42 -> MAT 22:24 | MAT 22:32 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | TCG_NT | 422 | MAT 22:32 | `Ἰσαάκ` | Ἐγώ εἰμι ὁ Θεὸς Ἁβραάμ , καὶ ὁ Θεὸς Ἰσαάκ , καὶ ὁ Θεὸς Ἰακώβ ; Οὐκ ἔστιν ὁ Θεὸς Θεὸς νεκρῶν , ἀλλὰ ζώντων . | MAT 22:19 -> MAT 22:46 | MAT 22:32 |
| `seba_g` `σαβα` (saba; English: Seba) | TCG_NT | -267 | ACT 1:23 | `Βαρσαβᾶν,` | Καὶ ἔστησαν δύο, Ἰωσὴφ τὸν καλούμενον Βαρσαβᾶν, ὃς ἐπεκλήθη Ἰοῦστος, καὶ Ματθίαν. | ACT 2:2 -> ACT 1:19 | ACT 1:23 |
| `bashan_g` `βασαν` (basan; English: Bashan) | SBLGNT | 194 | Rev 14:11 | `βασανισμοῦ` | καὶ ὁ καπνὸς τοῦ βασανισμοῦ αὐτῶν εἰς αἰῶνας αἰώνων ἀναβαίνει, καὶ οὐκ ἔχουσιν ἀνάπαυσιν ἡμέρας καὶ νυκτός, οἱ προσκυνοῦντες τὸ θηρίον καὶ τὴν εἰκόνα αὐτοῦ, καὶ εἴ τις λαμβάνει τὸ… | Rev 14:8 -> Rev 14:14 | Rev 14:10;Rev 14:11 |
| `bashan_g` `βασαν` (basan; English: Bashan) | SBLGNT | -374 | Rev 20:10 | `βασανισθήσονται` | καὶ ὁ διάβολος ὁ πλανῶν αὐτοὺς ἐβλήθη εἰς τὴν λίμνην τοῦ πυρὸς καὶ θείου, ὅπου καὶ τὸ θηρίον καὶ ὁ ψευδοπροφήτης, καὶ βασανισθήσονται ἡμέρας καὶ νυκτὸς εἰς τοὺς αἰῶνας τῶν αἰώνων. | Rev 21:2 -> Rev 20:4 | Rev 20:10 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | SBLGNT | -141 | Heb 13:8 | `Ἰησοῦς` | Ἰησοῦς Χριστὸς ἐχθὲς καὶ σήμερον ὁ αὐτός, καὶ εἰς τοὺς αἰῶνας. | Heb 13:12 -> Heb 13:3 | Heb 13:8;Heb 13:12 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | SBLGNT | -192 | John 8:6 | `Ἰησοῦς` | τοῦτο δὲ ἔλεγον πειράζοντες αὐτόν, ἵνα ἔχωσιν κατηγορεῖν αὐτοῦ. ὁ δὲ Ἰησοῦς κάτω κύψας, τῷ δακτύλῳ ἔγραφεν εἰς τὴν γῆν, μὴ προσποιούμενος. | John 8:11 -> John 7:52 | John 8:1;John 8:6;John 8:9;John 8:10;John 8:11 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | SBLGNT | -141 | Heb 13:8 | `Ἰησοῦς` | Ἰησοῦς Χριστὸς ἐχθὲς καὶ σήμερον ὁ αὐτός, καὶ εἰς τοὺς αἰῶνας. | Heb 13:12 -> Heb 13:3 | Heb 13:8;Heb 13:12 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | SBLGNT | -192 | John 8:6 | `Ἰησοῦς` | τοῦτο δὲ ἔλεγον πειράζοντες αὐτόν, ἵνα ἔχωσιν κατηγορεῖν αὐτοῦ. ὁ δὲ Ἰησοῦς κάτω κύψας, τῷ δακτύλῳ ἔγραφεν εἰς τὴν γῆν, μὴ προσποιούμενος. | John 8:11 -> John 7:52 | John 8:1;John 8:6;John 8:9;John 8:10;John 8:11 |

## Highest Surface-Context Summary Rows

| Term | Corpus | Hidden hits counted | Context hits | Exact center-word | Exact center | Exact span | Same-category span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | LXX | 15036 | 1563 | 19 | 91 | 370 | 1557 |
| `seba_g` `σαβα` (saba; English: Seba) | LXX | 28153 | 1864 | 13 | 344 | 1645 | 348 |
| `syria_g` `συρια` (suria; English: Syria) | LXX | 6262 | 317 | 8 | 58 | 244 | 77 |
| `bashan_g` `βασαν` (basan; English: Bashan) | LXX | 1966 | 176 | 4 | 25 | 134 | 44 |
| `kyrios_gnt` `κυριοσ` (kyrios; English: Lord) | LXX | 202 | 116 | 3 | 31 | 116 | 4 |
| `jacob_g` `ιακωβ` (iakob; English: Jacob) | LXX | 415 | 62 | 2 | 9 | 42 | 38 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | SBLGNT | 85 | 23 | 2 | 9 | 23 | 0 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | SBLGNT | 85 | 23 | 2 | 9 | 23 | 0 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | TCG_NT | 2217 | 276 | 2 | 7 | 50 | 273 |
| `bashan_g` `βασαν` (basan; English: Bashan) | SBLGNT | 300 | 33 | 2 | 5 | 20 | 15 |
| `locust_g` `ακρισ` (akris; English: Locust) | LXX | 4362 | 324 | 2 | 4 | 57 | 270 |
| `seba_g` `σαβα` (saba; English: Seba) | TR_NT | 3498 | 99 | 1 | 13 | 84 | 15 |
| `seba_g` `σαβα` (saba; English: Seba) | TCG_NT | 3460 | 87 | 1 | 10 | 75 | 12 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | TR_NT | 2223 | 295 | 1 | 9 | 52 | 292 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | BYZ_NT | 79 | 31 | 1 | 8 | 31 | 0 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | BYZ_NT | 79 | 31 | 1 | 8 | 31 | 0 |
| `bashan_g` `βασαν` (basan; English: Bashan) | TR_NT | 294 | 27 | 1 | 4 | 18 | 9 |
| `seba_g` `σαβα` (saba; English: Seba) | SBLGNT | 3315 | 66 | 0 | 13 | 66 | 0 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | BYZ_NT | 2244 | 302 | 0 | 11 | 63 | 302 |
| `seba_g` `σαβα` (saba; English: Seba) | BYZ_NT | 3408 | 82 | 0 | 11 | 68 | 14 |
| `gaza_g` `γαζα` (gaza; English: Gaza) | LXX | 1120 | 78 | 0 | 7 | 30 | 48 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | TR_NT | 94 | 41 | 0 | 6 | 41 | 0 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | TR_NT | 94 | 41 | 0 | 6 | 41 | 0 |
| `cyrus_g` `κυροσ` (kuros; English: Cyrus) | LXX | 2070 | 139 | 0 | 4 | 12 | 127 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | LXX | 416 | 25 | 0 | 4 | 25 | 0 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | LXX | 416 | 25 | 0 | 4 | 25 | 0 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | SBLGNT | 2176 | 280 | 0 | 3 | 58 | 280 |
| `locust_g` `ακρισ` (akris; English: Locust) | BYZ_NT | 741 | 67 | 0 | 3 | 19 | 48 |
| `bashan_g` `βασαν` (basan; English: Bashan) | TCG_NT | 282 | 27 | 0 | 2 | 20 | 7 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | TCG_NT | 75 | 25 | 0 | 2 | 25 | 0 |

## Highest Control Surface-Context Rows

Controls still produce many center/span surface-context rows. What they
did not produce in this full pass is an exact center-word row.

| Term | Corpus | Hidden hits counted | Context hits | Exact center-word | Exact center | Exact span | Same-category span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `seba_g` `σαβα` (saba; English: Seba) | GRK_HERODOTUS | 4622 | 4622 | 0 | 4622 | 4622 | 4622 |
| `seba_g` `σαβα` (saba; English: Seba) | GRK_ILIAD | 2358 | 2358 | 0 | 2358 | 2358 | 0 |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | GRK_HERODOTUS | 2207 | 2207 | 0 | 2207 | 2207 | 0 |
| `syria_g` `συρια` (suria; English: Syria) | GRK_HERODOTUS | 1071 | 1071 | 0 | 1071 | 1071 | 0 |
| `abimael_h` `אבימאל` (byml; English: Abimael) | HEB_BIALIK | 816 | 816 | 0 | 816 | 816 | 0 |
| `locust_g` `ακρισ` (akris; English: Locust) | GRK_HERODOTUS | 755 | 755 | 0 | 755 | 755 | 755 |
| `locust_g` `ακρισ` (akris; English: Locust) | GRK_ILIAD | 514 | 514 | 0 | 514 | 514 | 514 |
| `bashan_g` `βασαν` (basan; English: Bashan) | GRK_HERODOTUS | 388 | 388 | 0 | 388 | 388 | 388 |
| `cyrus_g` `κυροσ` (kuros; English: Cyrus) | GRK_HERODOTUS | 353 | 353 | 0 | 353 | 353 | 353 |
| `cainan_g` `καιναν` (kainan; English: Cainan) | GRK_HERODOTUS | 189 | 189 | 0 | 189 | 189 | 189 |
| `cyrus_g` `κυροσ` (kuros; English: Cyrus) | GRK_ILIAD | 160 | 160 | 0 | 160 | 160 | 160 |
| `bashan_g` `βασαν` (basan; English: Bashan) | GRK_ILIAD | 157 | 157 | 0 | 157 | 157 | 157 |
| `bashan_g` `βασαν` (basan; English: Bashan) | GRK_ODYSSEY | 131 | 131 | 0 | 131 | 131 | 0 |
| `prophet_isaiah_g` `ησαιασ` (esaias; English: Isaiah) | GRK_ILIAD | 107 | 107 | 0 | 107 | 107 | 0 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | GRK_HERODOTUS | 88 | 88 | 0 | 88 | 88 | 0 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | GRK_HERODOTUS | 88 | 88 | 0 | 88 | 88 | 0 |
| `krisis_gnt` `κρισισ` (krisis; English: Judgment) | GRK_HERODOTUS | 49 | 49 | 0 | 49 | 49 | 49 |
| `kyrios_gnt` `κυριοσ` (kyrios; English: Lord) | GRK_HERODOTUS | 41 | 41 | 0 | 41 | 41 | 41 |
| `witness_g` `μαρτυσ` (martus; English: Witness) | GRK_HERODOTUS | 32 | 32 | 0 | 32 | 32 | 32 |
| `rosh_hashanah_h` `ראשהשנה` (rshhshnh; English: Rosh Hashanah) | HEB_BIALIK | 26 | 26 | 0 | 26 | 26 | 0 |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | GRK_ODYSSEY | 26 | 26 | 0 | 26 | 26 | 0 |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | GRK_ODYSSEY | 26 | 26 | 0 | 26 | 26 | 0 |
| `rosh_hashanah_h` `ראשהשנה` (rshhshnh; English: Rosh Hashanah) | HEB_BRENNER | 19 | 19 | 0 | 19 | 19 | 0 |
| `rosh_hashanah_h` `ראשהשנה` (rshhshnh; English: Rosh Hashanah) | HEB_AHAD_HAAM | 8 | 8 | 0 | 8 | 8 | 0 |
| `probus_g` `προβοσ` (probos; English: Probus) | GRK_HERODOTUS | 5 | 5 | 0 | 5 | 5 | 5 |
| `javan_g` `ιωυαν` (Iouan; English: Javan) | GRK_HERODOTUS | 1067 | 1067 | 0 | 0 | 0 | 1067 |
| `overcome_g` `νικαω` (nikao; English: Overcome) | GRK_HERODOTUS | 665 | 665 | 0 | 0 | 0 | 665 |
| `javan_g` `ιωυαν` (Iouan; English: Javan) | GRK_ILIAD | 482 | 482 | 0 | 0 | 0 | 482 |
| `locust_g` `ακρισ` (akris; English: Locust) | GRK_ODYSSEY | 398 | 398 | 0 | 0 | 0 | 398 |
| `overcome_g` `νικαω` (nikao; English: Overcome) | GRK_ILIAD | 365 | 365 | 0 | 0 | 0 | 365 |

## Hidden-Path-Only Summary Rows

These summary rows had hidden hits in the full contextual follow-up but no exact,
same-concept, or same-category surface-context promotion.

| Term | Corpus | Hidden hits counted | Exact center-word | Context hits |
| --- | --- | ---: | ---: | ---: |
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
| `rosh_hashanah_h` `ראשהשנה` (rshhshnh; English: Rosh Hashanah) | UXLC | 9 | 0 | 0 |
| `rosh_hashanah_h` `ראשהשנה` (rshhshnh; English: Rosh Hashanah) | EBIBLE_WLC | 9 | 0 | 0 |
| `stauros_gnt` `σταυροσ` (stauros; English: Cross) | BYZ_NT | 9 | 0 | 0 |
| `jobab_g` `ιωβαβ` (iobab; English: Jobab) | TR_NT | 7 | 0 | 0 |
| `probus_g` `προβοσ` (probos; English: Probus) | TCG_NT | 7 | 0 | 0 |
| `sabtah_g` `σαβαθα` (sabatha; English: Sabtah) | BYZ_NT | 6 | 0 | 0 |
| `sabtah_g` `σαβαθα` (sabatha; English: Sabtah) | SBLGNT | 6 | 0 | 0 |
| `carinus_g` `καρινοσ` (karinos; English: Carinus) | TR_NT | 4 | 0 | 0 |

## Corpus Hit Rows

| Corpus | Context hit rows written |
| --- | ---: |
| LXX | 5641 |
| TR_NT | 717 |
| BYZ_NT | 711 |
| TCG_NT | 675 |
| SBLGNT | 636 |
| MAM | 2 |
| MT_WLC | 1 |
| UXLC | 1 |
| EBIBLE_WLC | 1 |
| UHB | 1 |

## Caution

This follow-up intentionally keeps hidden-path-only rows. The meaningful
next distinction is not frequency alone; it is whether a hidden path is
centered on the same word, a related word, a relevant center verse, or
only present as a hidden sequence without surface support.
