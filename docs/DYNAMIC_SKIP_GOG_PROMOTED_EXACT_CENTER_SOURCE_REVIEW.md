# Gog Promoted Exact-Center Source Review

This report follows up the promoted original-language exact-center finding:
Greek `γωγ` centered on open `Γὼγ` at `REV 20:8` in `TCG_NT`.
It checks the same exact-center condition directly against Greek NT sources
without exporting every full-span hit.

## Reproduce

```bash
python3 -m scripts.build_gog_promoted_exact_center_source_review --term γωγ --min-skip 2 --max-skip-mode full-span --corpus TR_NT=configs/example_ebible_grctr.toml --corpus BYZ_NT=configs/example_ebible_grcmt.toml --corpus TCG_NT=configs/example_ebible_grctcgnt.toml --corpus SBLGNT=configs/example_sblgnt.toml --out reports/dynamic_skip_focus/gog_promoted_exact_center_source_review.csv --paths-out reports/dynamic_skip_focus/gog_promoted_exact_center_source_review_paths.csv --markdown-out docs/DYNAMIC_SKIP_GOG_PROMOTED_EXACT_CENTER_SOURCE_REVIEW.md --manifest-out reports/dynamic_skip_focus/gog_promoted_exact_center_source_review.manifest.json
```

## Bottom Line

- sources with exact-center `γωγ` paths: TR_NT, BYZ_NT, TCG_NT, SBLGNT
- sources with open `γωγ` but no exact-center path: none
- sources where normalized open `γωγ` was absent: none
- `TCG_NT` has four exact-center paths: skip `±17` inside `REV 20:8`, and skip `±4568` spanning `REV 18:16` / `REV 20:8` / `REV 22:8`.
- This is a contextually meaningful centered-self occurrence: hidden `γωγ` centers on open `Gog` in the Gog/Magog verse across all compared sources.
- Frequency strength must be reported separately because the term is only three letters and the surface word supplies the center anchor.

## Source Comparison

| Corpus | Letters | Max skip | Surface centers | Exact-center paths | Center refs | Skip values | Read |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| TR_NT | 690,831 | 345,415 | 1 | 2 | REV 20:8=2 | `-17;17` | comparison source also has exact-center hidden paths |
| BYZ_NT | 690,527 | 345,263 | 1 | 4 | REV 20:8=4 | `-17;17;-888;888` | comparison source also has exact-center hidden paths |
| TCG_NT | 687,914 | 343,956 | 1 | 4 | REV 20:8=4 | `-17;17;-4568;4568` | promoted source retains exact-center hidden paths |
| SBLGNT | 679,879 | 339,939 | 1 | 4 | Rev 20:8=4 | `-7;7;-4423;4423` | comparison source also has exact-center hidden paths |

## Exact-Center Paths

| Corpus | Path | Skip | Span | Matrix | Letter path |
| --- | ---: | ---: | --- | --- | --- |
| TR_NT | 1 | -17 | REV 20:8 -> REV 20:8 -> REV 20:8 | 3 rows @ width 17 | γ@REV 20:8:συναγαγεῖν[r40296,c3] \| ω@REV 20:8:Γὼγ[r40295,c3] \| γ@REV 20:8:γωνίαις[r40294,c3] |
| TR_NT | 2 | 17 | REV 20:8 -> REV 20:8 -> REV 20:8 | 3 rows @ width 17 | γ@REV 20:8:γωνίαις[r40294,c3] \| ω@REV 20:8:Γὼγ[r40295,c3] \| γ@REV 20:8:συναγαγεῖν[r40296,c3] |
| BYZ_NT | 1 | -17 | REV 20:8 -> REV 20:8 -> REV 20:8 | 3 rows @ width 17 | γ@REV 20:8:συναγαγειν[r40276,c11] \| ω@REV 20:8:γωγ[r40275,c11] \| γ@REV 20:8:γωνιαισ[r40274,c11] |
| BYZ_NT | 2 | 17 | REV 20:8 -> REV 20:8 -> REV 20:8 | 3 rows @ width 17 | γ@REV 20:8:γωνιαισ[r40274,c11] \| ω@REV 20:8:γωγ[r40275,c11] \| γ@REV 20:8:συναγαγειν[r40276,c11] |
| BYZ_NT | 3 | -888 | REV 20:15 -> REV 20:8 -> REV 20:1 | 3 rows @ width 888 | γ@REV 20:15:γεγραμμενοσ[r772,c38] \| ω@REV 20:8:γωγ[r771,c38] \| γ@REV 20:1:μεγαλην[r770,c38] |
| BYZ_NT | 4 | 888 | REV 20:1 -> REV 20:8 -> REV 20:15 | 3 rows @ width 888 | γ@REV 20:1:μεγαλην[r770,c38] \| ω@REV 20:8:γωγ[r771,c38] \| γ@REV 20:15:γεγραμμενοσ[r772,c38] |
| TCG_NT | 1 | -17 | REV 20:8 -> REV 20:8 -> REV 20:8 | 3 rows @ width 17 | γ@REV 20:8:συναγαγεῖν[r40125,c6] \| ω@REV 20:8:Γὼγ[r40124,c6] \| γ@REV 20:8:γωνίαις[r40123,c6] |
| TCG_NT | 2 | 17 | REV 20:8 -> REV 20:8 -> REV 20:8 | 3 rows @ width 17 | γ@REV 20:8:γωνίαις[r40123,c6] \| ω@REV 20:8:Γὼγ[r40124,c6] \| γ@REV 20:8:συναγαγεῖν[r40125,c6] |
| TCG_NT | 3 | -4568 | REV 22:8 -> REV 20:8 -> REV 18:16 | 3 rows @ width 4568 | γ@REV 22:8:ἀγγέλου[r150,c1482] \| ω@REV 20:8:Γὼγ[r149,c1482] \| γ@REV 18:16:μεγάλη,[r148,c1482] |
| TCG_NT | 4 | 4568 | REV 18:16 -> REV 20:8 -> REV 22:8 | 3 rows @ width 4568 | γ@REV 18:16:μεγάλη,[r148,c1482] \| ω@REV 20:8:Γὼγ[r149,c1482] \| γ@REV 22:8:ἀγγέλου[r150,c1482] |
| SBLGNT | 1 | -7 | Rev 20:8 -> Rev 20:8 -> Rev 20:8 | 3 rows @ width 7 | γ@Rev 20:8:Μαγώγ,[r96304,c3] \| ω@Rev 20:8:Γὼγ[r96303,c3] \| γ@Rev 20:8:γῆς,[r96302,c3] |
| SBLGNT | 2 | 7 | Rev 20:8 -> Rev 20:8 -> Rev 20:8 | 3 rows @ width 7 | γ@Rev 20:8:γῆς,[r96302,c3] \| ω@Rev 20:8:Γὼγ[r96303,c3] \| γ@Rev 20:8:Μαγώγ,[r96304,c3] |
| SBLGNT | 3 | -4423 | Rev 22:7 -> Rev 20:8 -> Rev 18:16 | 3 rows @ width 4423 | γ@Rev 22:7:λόγους[r153,c1828] \| ω@Rev 20:8:Γὼγ[r152,c1828] \| γ@Rev 18:16:⸀μαργαρίτῃ,[r151,c1828] |
| SBLGNT | 4 | 4423 | Rev 18:16 -> Rev 20:8 -> Rev 22:7 | 3 rows @ width 4423 | γ@Rev 18:16:⸀μαργαρίτῃ,[r151,c1828] \| ω@Rev 20:8:Γὼγ[r152,c1828] \| γ@Rev 22:7:λόγους[r153,c1828] |

## Read

- This direct scan asks whether the hidden `γωγ` path centers on an open surface `γωγ` word.
- The existence of that centered-self occurrence is the finding to preserve in the final report.
- It does not claim frequency significance by itself; that question belongs to matched controls and source-version comparison.
- Because `γωγ` is length 3, the report should show both axes: contextual relevance and frequency/control strength.

