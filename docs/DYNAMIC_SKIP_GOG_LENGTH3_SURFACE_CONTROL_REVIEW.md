# Gog Length-3 Surface Control Review

This report builds matched Greek controls for the promoted `γωγ` (Gog; English: Gog) exact-center
row. The control universe is normalized Greek surface words of length 3
that occur exactly once in every compared Greek NT source.

## Reproduce

```bash
python3 -m scripts.build_gog_length3_surface_control_review --target γωγ --length 3 --occurrences-per-source 1 --min-skip 2 --max-skip-mode full-span --corpus TR_NT=configs/example_ebible_grctr.toml --corpus BYZ_NT=configs/example_ebible_grcmt.toml --corpus TCG_NT=configs/example_ebible_grctcgnt.toml --corpus SBLGNT=configs/example_sblgnt.toml --out reports/dynamic_skip_focus/gog_length3_surface_control_review.csv --by-source-out reports/dynamic_skip_focus/gog_length3_surface_control_by_source.csv --paths-out reports/dynamic_skip_focus/gog_length3_surface_control_path_examples.csv --markdown-out docs/DYNAMIC_SKIP_GOG_LENGTH3_SURFACE_CONTROL_REVIEW.md --manifest-out reports/dynamic_skip_focus/gog_length3_surface_control_review.manifest.json
```

## Bottom Line

- matched term universe: 25 terms, including target `γωγ` (Gog; English: Gog)
- non-target controls: 24
- target total exact-center paths: 14
- controls above target: 24 of 24
- controls below target: 0 of 24
- target rank by descending exact-center paths: 25 of 25
- target rank by ascending exact-center paths: 1 of 25

Current read: `γωγ` (Gog; English: Gog) remains a contextually meaningful centered-self
occurrence, not a frequency-promoted row. The hidden word centers on the
open Gog word in the Gog/Magog verse across all compared Greek NT streams.
The matched controls only say its path count is not unusually high among
comparable length-3 surface words.

## Matched Terms

| Rank desc | Rank asc | Term | Target | Total paths | Source counts | Read |
| ---: | ---: | --- | --- | ---: | --- | --- |
| 1 | 25 | `εια` (eia) | False | 14,995 | `BYZ_NT:3785;SBLGNT:3702;TCG_NT:3769;TR_NT:3739` | matched control exceeds target |
| 2 | 24 | `σοσ` (sos) | False | 14,028 | `BYZ_NT:3524;SBLGNT:3418;TCG_NT:3418;TR_NT:3668` | matched control exceeds target |
| 3 | 23 | `ουα` (oua) | False | 12,929 | `BYZ_NT:3189;SBLGNT:3163;TCG_NT:3243;TR_NT:3334` | matched control exceeds target |
| 4 | 22 | `σην` (sen) | False | 12,600 | `BYZ_NT:3262;SBLGNT:3159;TCG_NT:3127;TR_NT:3052` | matched control exceeds target |
| 5 | 21 | `ευα` (eua; English: Eve) | False | 10,864 | `BYZ_NT:2732;SBLGNT:2727;TCG_NT:2707;TR_NT:2698` | matched control exceeds target |
| 6 | 20 | `αρω` (aro) | False | 8,747 | `BYZ_NT:2303;SBLGNT:2064;TCG_NT:2191;TR_NT:2189` | matched control exceeds target |
| 7 | 19 | `αγω` (ago) | False | 8,579 | `BYZ_NT:2174;SBLGNT:2140;TCG_NT:2116;TR_NT:2149` | matched control exceeds target |
| 8 | 18 | `κισ` (kis) | False | 7,082 | `BYZ_NT:1761;SBLGNT:1740;TCG_NT:1794;TR_NT:1787` | matched control exceeds target |
| 9 | 17 | `αψη` (apse) | False | 5,371 | `BYZ_NT:1341;SBLGNT:1300;TCG_NT:1357;TR_NT:1373` | matched control exceeds target |
| 10 | 16 | `πιε` (pie) | False | 5,277 | `BYZ_NT:1365;SBLGNT:1255;TCG_NT:1311;TR_NT:1346` | matched control exceeds target |
| 11 | 15 | `εδυ` (edu) | False | 4,567 | `BYZ_NT:1144;SBLGNT:1102;TCG_NT:1143;TR_NT:1178` | matched control exceeds target |
| 12 | 14 | `ιση` (ise) | False | 4,211 | `BYZ_NT:1097;SBLGNT:1046;TCG_NT:1058;TR_NT:1010` | matched control exceeds target |
| 13 | 13 | `ωον` (oon) | False | 3,960 | `BYZ_NT:986;SBLGNT:991;TCG_NT:979;TR_NT:1004` | matched control exceeds target |
| 14 | 12 | `ιου` (iou) | False | 3,466 | `BYZ_NT:844;SBLGNT:892;TCG_NT:861;TR_NT:869` | matched control exceeds target |
| 15 | 11 | `ηθη` (ethe) | False | 2,668 | `BYZ_NT:614;SBLGNT:700;TCG_NT:690;TR_NT:664` | matched control exceeds target |
| 16 | 10 | `σημ` (Sem; English: Shem) | False | 2,466 | `BYZ_NT:643;SBLGNT:575;TCG_NT:615;TR_NT:633` | matched control exceeds target |
| 17 | 9 | `σηθ` (seth) | False | 1,574 | `BYZ_NT:353;SBLGNT:422;TCG_NT:389;TR_NT:410` | matched control exceeds target |
| 18 | 8 | `δωσ` (dos) | False | 1,300 | `BYZ_NT:341;SBLGNT:336;TCG_NT:313;TR_NT:310` | matched control exceeds target |
| 19 | 7 | `ηχω` (echo) | False | 942 | `BYZ_NT:256;SBLGNT:226;TCG_NT:230;TR_NT:230` | matched control exceeds target |
| 20 | 6 | `αηρ` (aer) | False | 815 | `BYZ_NT:200;SBLGNT:204;TCG_NT:208;TR_NT:203` | matched control exceeds target |
| 21 | 5 | `χρω` (chro) | False | 293 | `BYZ_NT:71;SBLGNT:68;TCG_NT:85;TR_NT:69` | matched control exceeds target |
| 22 | 4 | `ιωβ` (iob) | False | 287 | `BYZ_NT:63;SBLGNT:61;TCG_NT:86;TR_NT:77` | matched control exceeds target |
| 23 | 3 | `χρη` (chre) | False | 221 | `BYZ_NT:58;SBLGNT:57;TCG_NT:57;TR_NT:49` | matched control exceeds target |
| 24 | 2 | `γαδ` (gad; English: Gad) | False | 76 | `BYZ_NT:14;SBLGNT:25;TCG_NT:19;TR_NT:18` | matched control exceeds target |
| 25 | 1 | `γωγ` (Gog; English: Gog) | True | 14 | `BYZ_NT:4;SBLGNT:4;TCG_NT:4;TR_NT:2` | target term |

## Target By Source

| Corpus | Surface centers | Exact-center paths | Max skip | Skip values |
| --- | ---: | ---: | ---: | --- |
| TR_NT | 1 | 2 | 345,415 | `-17;17` |
| BYZ_NT | 1 | 4 | 345,263 | `-17;17;-888;888` |
| TCG_NT | 1 | 4 | 343,956 | `-17;17;-4568;4568` |
| SBLGNT | 1 | 4 | 339,939 | `-7;7;-4423;4423` |

## Target Path Examples

| Corpus | Path | Skip | Span | Letter path |
| --- | ---: | ---: | --- | --- |
| TR_NT | 1 | -17 | REV 20:8 -> REV 20:8 -> REV 20:8 | γ@REV 20:8:συναγαγεῖν[r40296,c3] \| ω@REV 20:8:Γὼγ[r40295,c3] \| γ@REV 20:8:γωνίαις[r40294,c3] |
| TR_NT | 2 | 17 | REV 20:8 -> REV 20:8 -> REV 20:8 | γ@REV 20:8:γωνίαις[r40294,c3] \| ω@REV 20:8:Γὼγ[r40295,c3] \| γ@REV 20:8:συναγαγεῖν[r40296,c3] |
| BYZ_NT | 1 | -17 | REV 20:8 -> REV 20:8 -> REV 20:8 | γ@REV 20:8:συναγαγειν[r40276,c11] \| ω@REV 20:8:γωγ[r40275,c11] \| γ@REV 20:8:γωνιαισ[r40274,c11] |
| BYZ_NT | 2 | 17 | REV 20:8 -> REV 20:8 -> REV 20:8 | γ@REV 20:8:γωνιαισ[r40274,c11] \| ω@REV 20:8:γωγ[r40275,c11] \| γ@REV 20:8:συναγαγειν[r40276,c11] |
| BYZ_NT | 3 | -888 | REV 20:15 -> REV 20:8 -> REV 20:1 | γ@REV 20:15:γεγραμμενοσ[r772,c38] \| ω@REV 20:8:γωγ[r771,c38] \| γ@REV 20:1:μεγαλην[r770,c38] |
| BYZ_NT | 4 | 888 | REV 20:1 -> REV 20:8 -> REV 20:15 | γ@REV 20:1:μεγαλην[r770,c38] \| ω@REV 20:8:γωγ[r771,c38] \| γ@REV 20:15:γεγραμμενοσ[r772,c38] |
| TCG_NT | 1 | -17 | REV 20:8 -> REV 20:8 -> REV 20:8 | γ@REV 20:8:συναγαγεῖν[r40125,c6] \| ω@REV 20:8:Γὼγ[r40124,c6] \| γ@REV 20:8:γωνίαις[r40123,c6] |
| TCG_NT | 2 | 17 | REV 20:8 -> REV 20:8 -> REV 20:8 | γ@REV 20:8:γωνίαις[r40123,c6] \| ω@REV 20:8:Γὼγ[r40124,c6] \| γ@REV 20:8:συναγαγεῖν[r40125,c6] |
| TCG_NT | 3 | -4568 | REV 22:8 -> REV 20:8 -> REV 18:16 | γ@REV 22:8:ἀγγέλου[r150,c1482] \| ω@REV 20:8:Γὼγ[r149,c1482] \| γ@REV 18:16:μεγάλη,[r148,c1482] |
| TCG_NT | 4 | 4568 | REV 18:16 -> REV 20:8 -> REV 22:8 | γ@REV 18:16:μεγάλη,[r148,c1482] \| ω@REV 20:8:Γὼγ[r149,c1482] \| γ@REV 22:8:ἀγγέλου[r150,c1482] |
| SBLGNT | 1 | -7 | Rev 20:8 -> Rev 20:8 -> Rev 20:8 | γ@Rev 20:8:Μαγώγ,[r96304,c3] \| ω@Rev 20:8:Γὼγ[r96303,c3] \| γ@Rev 20:8:γῆς,[r96302,c3] |
| SBLGNT | 2 | 7 | Rev 20:8 -> Rev 20:8 -> Rev 20:8 | γ@Rev 20:8:γῆς,[r96302,c3] \| ω@Rev 20:8:Γὼγ[r96303,c3] \| γ@Rev 20:8:Μαγώγ,[r96304,c3] |
| SBLGNT | 3 | -4423 | Rev 22:7 -> Rev 20:8 -> Rev 18:16 | γ@Rev 22:7:λόγους[r153,c1828] \| ω@Rev 20:8:Γὼγ[r152,c1828] \| γ@Rev 18:16:⸀μαργαρίτῃ,[r151,c1828] |
| SBLGNT | 4 | 4423 | Rev 18:16 -> Rev 20:8 -> Rev 22:7 | γ@Rev 18:16:⸀μαργαρίτῃ,[r151,c1828] \| ω@Rev 20:8:Γὼγ[r152,c1828] \| γ@Rev 22:7:λόγους[r153,c1828] |

## Read

- This is a post-discovery matched control, not a preregistered claim test.
- The control is still valuable because it matches the key mechanics: Greek, length 3, full-span skip, exact-center surface word, one surface occurrence per source.
- `γωγ` (Gog; English: Gog) being source-stable and centered on the Gog/Magog verse is the contextual finding to preserve.
- The matched-control count is a frequency caution, not a reason to remove the centered-self occurrence from the final report.
- A stronger future test would preregister a length-3 surface-control universe before selecting a target.

