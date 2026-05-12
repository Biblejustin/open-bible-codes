# Centered Occurrence Index

This is an occurrence-first index. It lists hidden ELS rows where the
center lands on the same surface word, an inflected/containing surface
form, or a related center word/context. Frequency and control reads are
carried alongside the occurrence; they do not remove real occurrences
from review.

## Reproduce

```bash
python3 -m scripts.build_centered_occurrence_index --all-codes-review reports/all_codes_followup_review/review_summary.csv --all-codes-context reports/all_codes_followup_context/context_excerpts.csv --strong-queue reports/dynamic_skip_focus/strong_full_span_exact_center_review_queue.csv --strong-bundle reports/dynamic_skip_focus/strong_full_span_exact_center_review_bundle.csv --original-findings reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_findings.csv --gog-source-review reports/dynamic_skip_focus/gog_promoted_exact_center_source_review.csv --gog-control-review reports/dynamic_skip_focus/gog_length3_surface_control_review.csv --apocrypha-bridge-context reports/apocrypha_bridge_context/context.csv --kjv-apocrypha-bridge-context reports/kjv_apocrypha_bridge_context/context.csv --out reports/centered_occurrence_index/centered_occurrences.csv --summary-out reports/centered_occurrence_index/presence_summary.csv --markdown-out docs/CENTERED_OCCURRENCE_INDEX.md --manifest-out reports/centered_occurrence_index/manifest.json
```

## Bottom Line

- indexed occurrence rows: 923
- unique term-center presence rows: 812
- Bible occurrence rows: 839
- Bible presence rows: 809
- control occurrence rows: 84
- control presence rows: 3
- frequency controls are interpretation context, not deletion criteria.

## Occurrence Types

| Type | Presence rows | Occurrence rows |
| --- | ---: | ---: |
| `centered_self_exact_word` | 526 | 623 |
| `centered_self_surface_form` | 4 | 5 |
| `relevant_center_same_concept` | 3 | 3 |
| `relevant_center_same_category` | 13 | 14 |
| `center_verse_relevant` | 70 | 73 |
| `span_relevant` | 196 | 205 |

## Source Families

| Source family | Presence rows | Occurrence rows |
| --- | ---: | ---: |
| `strong_full_span_exact_center` | 448 | 537 |
| `kjv_apocrypha_bridge_context` | 193 | 203 |
| `original_language_findings` | 73 | 76 |
| `all_codes_followup` | 69 | 74 |
| `apocrypha_bridge_context` | 28 | 29 |
| `gog_source_review` | 1 | 4 |

## Top Presence Rows

| Rank | Type | Source | Corpora | Term | Center | Occurrence rows | Total paths | Frequency read | Context |
| ---: | --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| 1 | `centered_self_exact_word` | `gog_source_review` | BYZ_NT;SBLGNT;TCG_NT;TR_NT | `γωγ` (Gog; English: Gog) | REV 20:8 `Gog` | 4 | 14 | length-3 matched-control rank desc 25/asc 1; controls above target... | Rev 20:8 Gog/Magog context |
| 2 | `centered_self_exact_word` | `original_language_findings` | TCG_NT | `γωγ` (Gog; English: Gog) | REV 20:8 `Γὼγ` (Gog; English: Gog) | 1 | 4 | promote | τέσσαρσι γωνίαις τῆς γῆς, τὸν [Γὼγ] καὶ τὸν Μαγώγ, συναγαγεῖν αὐτοὺς |
| 3 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | 1MA 2:55 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | [Ἰησοῦς] ἐν τῷ πληρῶσαι λόγον ἐγένετο |
| 4 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | DEU 1:38 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | [Ἰησοῦς] υἱὸς Ναυὴ ὁ παρεστηκώς σοι, |
| 5 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | DEU 32:44 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | ὦτα τοῦ λαοῦ, αὐτὸς καὶ [Ἰησοῦς] ὁ τοῦ Ναυή. |
| 6 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | HAG 1:12 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | Σαλαθιὴλ ἐκ φυλῆς Ἰούδα καὶ [Ἰησοῦς] ὁ τοῦ Ἰωσεδὲκ ὁ ἱερεὺς |
| 7 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JDG 2:6 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | Καὶ ἐξαπέστειλεν [Ἰησοῦς] τὸν λαόν, καὶ ἦλθεν ἀνὴρ |
| 8 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:12 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | Τότε ἐλάλησεν [Ἰησοῦς] πρὸς Κύριον, ᾗ ἡμέρᾳ παρέδωκεν |
| 9 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:18 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ εἶπεν [Ἰησοῦς·] κυλίσατε λίθους ἐπὶ τὸ στόμα |
| 10 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:20 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ ἐγένετο ὡς κατέπαυσεν [Ἰησοῦς] καὶ πᾶς υἱὸς Ἰσραὴλ κόπτοντες |
| 11 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:24 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 2 | hold | αὐτοὺς πρὸς Ἰησοῦν, καὶ συνεκάλεσεν [Ἰησοῦς] πάντα Ἰσραήλ, καὶ τοὺς ἐναρχομένους |
| 12 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:31 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ ἀπῆλθεν [Ἰησοῦς] καὶ πᾶς Ἰσραὴλ μετ' αὐτοῦ |
| 13 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:34 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ ἀπῆλθεν [Ἰησοῦς] καὶ πᾶς Ἰσραὴλ μετ' αὐτοῦ |
| 14 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:40 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ ἐπάταξεν [Ἰησοῦς] πᾶσαν τὴν γῆν τῆς ὀρεινῆς |
| 15 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:42 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ τὴν γῆν αὐτῶν ἐπάταξεν [Ἰησοῦς] εἰσάπαξ, ὅτι Κύριος ὁ Θεὸς |
| 16 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:7 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ ἀνέβη [Ἰησοῦς] ἐκ Γαλγάλων, αὐτὸς καὶ πᾶς |
| 17 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 11:15 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | τῷ Ἰησοῖ, καὶ οὕτως ἐποίησεν [Ἰησοῦς·] οὐ παρέβη οὐδὲν ἀπὸ πάντων, |
| 18 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 11:21 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | Καὶ ἦλθεν [Ἰησοῦς] ἐν τῷ καιρῷ ἐκείνῳ καὶ |
| 19 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 13:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | ΚΑΙ [Ἰησοῦς] πρεσβύτερος προβεβηκὼς τῶν ἡμερῶν. καὶ |
| 20 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 17:17 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ εἶπεν [Ἰησοῦς] τοῖς υἱοῖς Ἰωσήφ· εἰ λαὸς |
| 21 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 18:10 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ ἐνέβαλεν αὐτοῖς [Ἰησοῦς] κλῆρον ἐν Σηλὼ ἔναντι Κυρίου. |
| 22 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 18:3 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 3 | hold | καὶ εἶπεν [Ἰησοῦς] τοῖς υἱοῖς Ἰσραήλ· ἕως τίνος |
| 23 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 22:34 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ ἐπωνόμασεν [Ἰησοῦς] τὸν βωμὸν τῶν Ρουβὴν καὶ |
| 24 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 22:6 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ εὐλόγησεν αὐτοὺς [Ἰησοῦς] καὶ ἐξαπέστειλεν αὐτούς, καὶ ἐπορεύθησαν |
| 25 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 22:7 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 3 | hold | Βασανίτιδι, καὶ τῷ ἡμίσει ἔδωκεν [Ἰησοῦς] μετὰ τῶν ἀδελφῶν αὐτοῦ ἐν |
| 26 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 23:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | τῶν ἐχθρῶν αὐτοῦ κυκλόθεν, καὶ [Ἰησοῦς] πρεσβύτερος προβεβηκὼς ταῖς ἡμέραις, |
| 27 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 24:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | ΚΑΙ συνήγαγεν [Ἰησοῦς] πάσας φυλὰς Ἰσραὴλ εἰς Σηλὼ |
| 28 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 24:28 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 2 | hold | καὶ ἀπέστειλεν [Ἰησοῦς] τὸν λαόν, καὶ ἐπορεύθησαν ἕκαστος |
| 29 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 24:30 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 2 | hold | ἐγένετο μετ' ἐκεῖνα καὶ ἀπέθανεν [Ἰησοῦς] υἱὸς Ναυὴ δοῦλος Κυρίου ἑκατὸν |
| 30 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 3:9 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ εἶπεν [Ἰησοῦς] τοῖς υἱοῖς Ἰσραήλ· προσαγάγετε ὧδε |
| 31 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 4:20 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 2 | hold | ἔλαβεν ἐκ τοῦ Ἰορδάνου, ἔστησεν [Ἰησοῦς] ἐν Γαλγάλοις |
| 32 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 4:9 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | ἔστησε δὲ [Ἰησοῦς] καὶ ἄλλους δώδεκα λίθους ἐν |
| 33 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 5:13 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 2 | 2 | hold | τῇ χειρὶ αὐτοῦ. καὶ προσελθὼν [Ἰησοῦς] εἶπεν αὐτῷ· ἡμέτερος εἶ ἢ |
| 34 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 5:4 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | ἐξ Αἰγύπτου, πάντας τούτους περιέτεμεν [Ἰησοῦς·] |
| 35 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 6:10 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | τῷ δὲ λαῷ ἐνετείλατο [Ἰησοῦς] λέγων· μὴ βοᾶτε, μηδὲ ἀκουσάτω |
| 36 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 6:12 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | τῇ ἡμέρᾳ τῇ δευτέρᾳ ἀνέστη [Ἰησοῦς] τὸ πρωΐ, καὶ ᾖραν οἱ |
| 37 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 6:16 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 2 | hold | ἐσάλπισαν οἱ ἱερεῖς, καὶ εἶπεν [Ἰησοῦς] τοῖς υἱοῖς Ἰσραήλ· κεκράξατε, παρέδωκε |
| 38 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 6:26 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ ὥρκισεν [Ἰησοῦς] ἐν τῇ ἡμέρᾳ ἐκείνῃ ἐναντίον |
| 39 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:16 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ ὤρθρισεν [Ἰησοῦς] καὶ προσήγαγε τὸν λαὸν κατὰ |
| 40 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:19 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ εἶπεν [Ἰησοῦς] τῷ Ἄχαρ· δὸς δόξαν σήμερον |
| 41 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:25 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ εἶπεν [Ἰησοῦς] τῷ Ἄχαρ· τί ὠλόθρευσας ἡμᾶς; |
| 42 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:6 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | τὰ ἱμάτια αὐτοῦ, καὶ ἔπεσεν [Ἰησοῦς] ἐπὶ τὴν γῆν ἐπὶ πρόσωπον |
| 43 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:7 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ εἶπεν [Ἰησοῦς·] δέομαι Κύριε· ἱνατί διεβίβασεν ὁ |
| 44 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:10 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ ὀρθρίσας [Ἰησοῦς] τὸ πρωΐ ἐπεσκέψατο τὸν λαόν· |
| 45 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:18 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | τοῦ τόπου αὐτῶν. καὶ ἐξέτεινεν [Ἰησοῦς] τὴν χεῖρα αὐτοῦ, τὸν γαισόν, |
| 46 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:3 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 2 | 5 | hold | ἀναβῆναι εἰς Γαί. ἐπέλεξε δὲ [Ἰησοῦς] τριάκοντα χιλιάδας ἀνδρῶν δυνατοὺς ἐν |
| 47 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:9 `Ἰησοῦς,` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ ἀπέστειλεν αὐτοὺς [Ἰησοῦς,] καὶ ἐπορεύθησαν εἰς τὴν ἐνέδραν |
| 48 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:2 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 2 | 2 | hold | θυσίαν σωτηρίου. 2γ καὶ ἔγραψεν [Ἰησοῦς] ἐπὶ τῶν λίθων τὸ δευτερονόμιον, |
| 49 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:21 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ ἐποίησεν [Ἰησοῦς] πρὸς αὐτοὺς εἰρήνην καὶ διέθεντο |
| 50 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:32 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | αὐτοῖς οὕτως· καὶ ἐξείλατο αὐτοὺς [Ἰησοῦς] ἐν τῇ ἡμέρᾳ ἐκείνῃ ἐκ |
| 51 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:33 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | καὶ κατέστησεν αὐτοὺς [Ἰησοῦς] ἐν τῇ ἡμέρᾳ ἐκείνῃ ξυλοκόπους |
| 52 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:8 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | ἐσμεν. καὶ εἶπε πρὸς αὐτοὺς [Ἰησοῦς·] πόθεν ἐστὲ καὶ πόθεν παραγεγόνατε; |
| 53 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | NEH 9:4 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | ἔστη ἐπὶ ἀναβάσει τῶν Λευιτῶν [Ἰησοῦς] καὶ οἱ υἱοὶ Καδμιήλ, Σεχενία |
| 54 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | NEH 9:5 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 2 | hold | καὶ εἴποσαν οἱ Λευῖται [Ἰησοῦς] καὶ Καδμιήλ· ἀνάστητε, εὐλογεῖτε Κύριον |
| 55 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | NUM 14:6 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | [Ἰησοῦς] δὲ ὁ τοῦ Ναυὴ καὶ |
| 56 | `centered_self_exact_word` | `original_language_findings` | LXX | `ιησουσ` (Iesous; English: Jesus/Joshua) | SIR 46:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | 1 | 1 | hold | ΚΡΑΤΑΙΟΣ ἐν πολέμοις [Ἰησοῦς] Ναυῆ καὶ διάδοχος Μωυσῆ ἐν |
| 57 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 10:18 `יֵשׁ֤וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 68 | background | אֲשֶׁ֥ר הֹשִׁ֖יבוּ נָשִׁ֣ים נָכְרִיּ֑וֹת מִ⁠בְּנֵ֨י [יֵשׁ֤וּעַ] בֶּן־יֽוֹצָדָק֙ וְ⁠אֶחָ֔י⁠ו מַֽעֲ... |
| 58 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 2:2 `יֵשׁ֡וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 83 | background | אֲשֶׁר־בָּ֣אוּ עִם־זְרֻבָּבֶ֗ל [יֵשׁ֡וּעַ] נְ֠חֶמְיָה שְׂרָיָ֨ה רְֽעֵלָיָ֜ה מָרְדֳּכַ֥י בִּלְשָׁ֛ן |
| 59 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 2:36 `יֵשׁ֔וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 63 | background | הַֽ⁠כֹּהֲנִ֑ים בְּנֵ֤י יְדַֽעְיָה֙ לְ⁠בֵ֣ית [יֵשׁ֔וּעַ] תְּשַׁ֥ע מֵא֖וֹת שִׁבְעִ֥ים וּ⁠שְׁלֹשָֽׁה׃ |
| 60 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 2:6 `יֵשׁ֖וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 73 | background | בְּנֵֽי־פַחַ֥ת מוֹאָ֛ב לִ⁠בְנֵ֥י [יֵשׁ֖וּעַ] יוֹאָ֑ב אַלְפַּ֕יִם שְׁמֹנֶ֥ה מֵא֖וֹת וּ⁠שְׁנֵ֥ים |
| 61 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 3:2 `יֵשׁ֨וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 54 | background | וַ⁠יָּקָם֩ [יֵשׁ֨וּעַ] בֶּן־יֽוֹצָדָ֜ק וְ⁠אֶחָ֣י⁠ו הַ⁠כֹּהֲנִ֗ים וּ⁠זְרֻבָּבֶ֤ל בֶּן־שְׁאַלְתִּיאֵל֙ |
| 62 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 3:9 `יֵשׁ֡וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 73 | background | וַ⁠יַּעֲמֹ֣ד [יֵשׁ֡וּעַ] בָּנָ֣י⁠ו וְ֠⁠אֶחָי⁠ו קַדְמִיאֵ֨ל וּ⁠בָנָ֤י⁠ו בְּנֵֽי־יְהוּדָה֙ |
| 63 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 12:7 `יֵשֽׁוּעַ׃` (Yeshua; English: Yeshua/Jeshua) | 1 | 59 | background | אֵ֣לֶּה רָאשֵׁ֧י הַ⁠כֹּהֲנִ֛ים וַ⁠אֲחֵי⁠הֶ֖ם בִּ⁠ימֵ֥י [יֵשֽׁוּעַ׃] |
| 64 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 12:8 `יֵשׁ֧וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 69 | background | וְ⁠הַ⁠לְוִיִּ֗ם [יֵשׁ֧וּעַ] בִּנּ֛וּי קַדְמִיאֵ֥ל שֵׁרֵבְיָ֖ה יְהוּדָ֣ה מַתַּנְיָ֑ה |
| 65 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 7:11 `יֵשׁ֖וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 67 | background | בְּנֵֽי־פַחַ֥ת מוֹאָ֛ב לִ⁠בְנֵ֥י [יֵשׁ֖וּעַ] וְ⁠יוֹאָ֑ב אַלְפַּ֕יִם וּ⁠שְׁמֹנֶ֥ה מֵא֖וֹת שְׁמֹנָ֥ה |
| 66 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 7:39 `יֵשׁ֔וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 56 | background | הַֽ⁠כֹּהֲנִ֑ים בְּנֵ֤י יְדַֽעְיָה֙ לְ⁠בֵ֣ית [יֵשׁ֔וּעַ] תְּשַׁ֥ע מֵא֖וֹת שִׁבְעִ֥ים וּ⁠שְׁלֹשָֽׁה׃ |
| 67 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 7:7 `יֵשׁ֡וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 55 | background | הַ⁠בָּאִ֣ים עִם־זְרֻבָּבֶ֗ל [יֵשׁ֡וּעַ] נְחֶמְיָ֡ה עֲ֠זַרְיָה רַֽעַמְיָ֨ה נַחֲמָ֜נִי מָרְדֳּכַ֥י |
| 68 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 8:17 `יֵשׁ֨וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 85 | background | וַ⁠יֵּשְׁב֣וּ בַ⁠סֻּכּוֹת֒ כִּ֣י לֹֽא־עָשׂ֡וּ מִ⁠ימֵי֩ [יֵשׁ֨וּעַ] בִּן־נ֥וּן כֵּן֙ בְּנֵ֣י יִשְׂ... |
| 69 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 9:4 `יֵשׁ֨וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 66 | background | וַ⁠יָּ֜קָם עַֽל־מַֽעֲלֵ֣ה הַ⁠לְוִיִּ֗ם [יֵשׁ֨וּעַ] וּ⁠בָנִ֜י קַדְמִיאֵ֧ל שְׁבַנְיָ֛ה בֻּנִּ֥י שֵׁ... |
| 70 | `centered_self_exact_word` | `original_language_findings` | UHB | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 9:5 `יֵשׁ֣וּעַ` (Yeshua; English: Yeshua/Jeshua) | 1 | 70 | background | וַ⁠יֹּאמְר֣וּ הַ⁠לְוִיִּ֡ם [יֵשׁ֣וּעַ] וְ֠⁠קַדְמִיאֵל בָּנִ֨י חֲשַׁבְנְיָ֜ה שֵׁרֵֽבְיָ֤ה הֽוֹדִיָּה֙ |
| 71 | `centered_self_exact_word` | `original_language_findings` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one) | 2SA 1:21 `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) | 1 | 33 | background | מָגֵ֣ן גִּבּוֹרִ֔ים מָגֵ֣ן שָׁא֔וּל בְּלִ֖י [מָשִׁ֥יחַ] בַּשָּֽׁמֶן׃ |
| 72 | `centered_self_exact_word` | `original_language_findings` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one) | 2SA 23:1 `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) | 1 | 30 | background | בֶּן־יִשַׁ֗י וּנְאֻ֤ם הַגֶּ֨בֶר֙ הֻ֣קַם עָ֔ל [מְשִׁ֨יחַ֙] אֱלֹהֵ֣י יַֽעֲקֹ֔ב וּנְעִ֖ים זְמִר֥וֹת... |
| 73 | `centered_self_exact_word` | `original_language_findings` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one) | DAN 9:26 `מָשִׁ֖יחַ` (Mashiach; English: Messiah/anointed one) | 1 | 1 | hold | וְאַחֲרֵ֤י הַשָּׁבֻעִים֙ שִׁשִּׁ֣ים וּשְׁנַ֔יִם יִכָּרֵ֥ת [מָשִׁ֖יחַ] וְאֵ֣ין ל֑וֹ וְהָעִ֨יר וְהַ... |
| 74 | `centered_self_exact_word` | `original_language_findings` | EBIBLE_WLC | `משיח` (Mashiach; English: Messiah/anointed one) | LAM 4:20 `מְשִׁ֣יחַ` (Mashiach; English: Messiah/anointed one) | 1 | 11 | background | ר֤וּחַ אַפֵּ֨ינוּ֙ [מְשִׁ֣יחַ] יְהוָ֔ה נִלְכַּ֖ד בִּשְׁחִיתוֹתָ֑ם אֲשֶׁ֣ר אָמַ֔רְנוּ |
| 75 | `centered_self_exact_word` | `strong_full_span_exact_center` | KJV | `jesus` | 1CO 12:3 `Jesus` | 1 | 1 | bible low-count review | no man can say that [Jesus] is the Lord, but by |
| 76 | `centered_self_exact_word` | `strong_full_span_exact_center` | KJV | `jesus` | 1CO 15:57 `Jesus` | 1 | 1 | bible low-count review | the victory through our Lord [Jesus] Christ. |
| 77 | `centered_self_exact_word` | `strong_full_span_exact_center` | KJV | `jesus` | 1CO 1:2 `Jesus` | 1 | 1 | bible low-count review | call upon the name of [Jesus] Christ our Lord, both theirs |
| 78 | `centered_self_exact_word` | `strong_full_span_exact_center` | KJV | `jesus` | 1CO 1:8 `Jesus` | 1 | 1 | bible low-count review | the day of our Lord [Jesus] Christ. |
| 79 | `centered_self_exact_word` | `strong_full_span_exact_center` | KJV | `jesus` | 1CO 2:2 `Jesus` | 1 | 1 | bible low-count review | any thing among you, save [Jesus] Christ, and him crucified. |
| 80 | `centered_self_exact_word` | `strong_full_span_exact_center` | KJV | `jesus` | 1CO 5:4 `Jesus` | 2 | 2 | bible low-count review | the name of our Lord [Jesus] Christ, when ye are gathered |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | 732 more rows in CSV |

## Read

- Presence rows are grouped by term, center reference, source family, and center surface form.
- `centered_self_exact_word` is the strongest occurrence stratum.
- `centered_self_surface_form` includes inflected or containing surface forms and should be manually checked.
- Relevant-center rows are retained because they answer a different question than raw frequency.
- Control rows are kept in the CSV so Bible occurrences can be read against a visible baseline.

