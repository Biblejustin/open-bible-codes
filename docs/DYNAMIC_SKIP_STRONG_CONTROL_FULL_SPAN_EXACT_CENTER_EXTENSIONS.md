# Strong Control Full-Span Exact-Center Extensions

This report checks same-skip letters immediately before and after the
exact-center paths. It asks whether an exact-centered hidden term
can extend into a surface word or short phrase from the same corpus.

## Reproduce

```bash
python3 -m scripts.build_dynamic_span_exact_center_extension_hits ... # build hit-compatible exact-center input
python3 -m els extensions ... # one run per corpus in the input directory
python3 -m els extension-summary ... # one summary per corpus with --match-kind-prefix phrase_
python3 -m scripts.build_dynamic_span_exact_center_extensions_report --input-dir reports/dynamic_skip_focus/exact_center_control_extensions --markdown-out docs/DYNAMIC_SKIP_STRONG_CONTROL_FULL_SPAN_EXACT_CENTER_EXTENSIONS.md --manifest-out reports/dynamic_skip_focus/exact_center_control_extensions/report.manifest.json --title 'Strong Control Full-Span Exact-Center Extensions' --top 25 --summary-row-limit 120
```

## Scope

- exact-center paths scanned for extensions: 8,212
- raw same-skip extension rows: 37,878
- phrase-filtered summary groups: 3,274
- strong phrase-extension rows: 50
- input directory: `reports/dynamic_skip_focus/exact_center_control_extensions`

## Corpus Counts

| Corpus | Exact-center paths | Raw extension rows | Phrase summary groups | Strong phrase rows |
| --- | ---: | ---: | ---: | ---: |
| ENG_PG_SHAKESPEARE | 2 | 3 | 0 | 0 |
| HEB_PBY_BIALIK | 8,210 | 37,875 | 3,274 | 50 |

## Strong Phrase Rows

| Corpus | Term | Center | Extension | Match kind | Match count | Matched examples |
| --- | --- | --- | --- | --- | ---: | --- |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `הממשיחימ` (hmmshychym) (before_plus_term_plus_after) | phrase_2 | 3 | הם משיחים,; הם משיחים |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `למשיחאמי` (lmshychmy) (before_plus_term_plus_after) | phrase_2 | 1 | למשיחא89. מי |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `למשיחאמי` (lmshychmy) (before_plus_term_plus_after) | phrase_2 | 1 | למשיחא89. מי |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `הואהמשיח` (hwhmshych) (before_plus_term) | phrase_2 | 1 | הוא ה"משיח" |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `לשמשיחה` (lshmshychh) (before_plus_term_plus_after) | phrase_2 | 4 | לשם שיחה |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `המשיחבא` (hmshychb) (before_plus_term_plus_after) | phrase_2 | 2 | המשיח בא |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `משמשיחת` (mshmshycht) (before_plus_term_plus_after) | phrase_2 | 1 | משם שיחת |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `משמשיחת` (mshmshycht) (before_plus_term_plus_after) | phrase_2 | 1 | משם שיחת |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `ממשיחדש` (mmshychdsh) (before_plus_term_plus_after) | phrase_2 | 1 | ממשי חדש |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `למשיחעד` (lmshychd) (before_plus_term_plus_after) | phrase_2 | 1 | למשיח עד |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `ומשיחלא` (wmshychl) (before_plus_term_plus_after) | phrase_2 | 1 | ומשיח לא |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `המשיחעד` (hmshychd) (before_plus_term_plus_after) | phrase_2 | 1 | המשיח עד |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `המשיחינ` (hmshychyn) (before_plus_term_plus_after) | phrase_2 | 1 | ה. משיחין&nbsp;– |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `המשיחות` (hmshychwt) (before_plus_term_plus_after) | phrase_2 | 1 | הם שיחות |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `המשיחות` (hmshychwt) (before_plus_term_plus_after) | phrase_2 | 1 | הם שיחות |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `המשיחהמ` (hmshychhm) (before_plus_term_plus_after) | phrase_2 | 1 | המשיח הם, |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `המשיחהמ` (hmshychhm) (before_plus_term_plus_after) | phrase_2 | 1 | המשיח הם, |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `המשיחהמ` (hmshychhm) (before_plus_term_plus_after) | phrase_2 | 1 | המשיח הם, |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `במשיחלא` (bmshychl) (before_plus_term_plus_after) | phrase_2 | 1 | במשיח. לא |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `במשיחלא` (bmshychl) (before_plus_term_plus_after) | phrase_2 | 1 | במשיח. לא |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | PBY Bialik | `אמישועה` (myshwh) (before_plus_term_plus_after) | phrase_2 | 1 | אמי שועה |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `משיחאמר` (mshychmr) (term_plus_after) | phrase_2 | 3 | משיח? אמר |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `יבאמשיח` (ybmshych) (before_plus_term) | phrase_2 | 2 | יבא משיח?; יבא משיח |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `יבאמשיח` (ybmshych) (before_plus_term) | phrase_2 | 2 | יבא משיח?; יבא משיח |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah/anointed one) | PBY Bialik | `יבאמשיח` (ybmshych) (before_plus_term) | phrase_2 | 2 | יבא משיח?; יבא משיח |

## Phrase Summary Rows

| Corpus | Term | Skip | Direction | Type | Match kind | Rows | Max length | Max match count |
| --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -923927 | backward | before_match | phrase_2+word | 1 | 3 | 23 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -914151 | backward | before_match | phrase_2+word | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -905116 | backward | before_match | phrase_2+word | 1 | 3 | 906 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -896203 | backward | before_match | phrase_2+word | 1 | 3 | 172 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -880010 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -858922 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -857691 | backward | before_match | phrase_2+word | 1 | 3 | 4 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -845557 | backward | before_match | phrase_2 | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -834459 | backward | before_match | phrase_2 | 1 | 3 | 7 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -832451 | backward | before_match | phrase_2+word | 1 | 3 | 27 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -819549 | backward | before_match | phrase_2+word | 1 | 3 | 10 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -810723 | backward | before_match | phrase_2+phrase_3 | 1 | 3 | 5 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -775884 | backward | after_match | phrase_2+phrase_3+word | 1 | 3 | 24 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -774899 | backward | before_match | phrase_2 | 1 | 4 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -774899 | backward | before_match | phrase_2+word | 1 | 3 | 34 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -769655 | backward | before_match | phrase_2 | 2 | 4 | 3 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -765994 | backward | after_match | phrase_2+phrase_3+word | 1 | 3 | 9 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -763318 | backward | after_match | phrase_2+word | 1 | 3 | 68 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -757508 | backward | after_match | phrase_2 | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -756135 | backward | before_match | phrase_2+word | 1 | 3 | 122 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -755590 | backward | before_match | phrase_2+word | 1 | 3 | 158 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -746814 | backward | before_match | phrase_2+word | 2 | 4 | 87 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -741327 | backward | before_match | phrase_2+word | 1 | 3 | 16 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -737360 | backward | before_match | phrase_2+phrase_3+word | 1 | 3 | 73 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -717367 | backward | before_match | phrase_2+word | 1 | 3 | 11 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -701005 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -700732 | backward | before_match | phrase_2+word | 2 | 4 | 174 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -688234 | backward | before_match | phrase_2+word | 1 | 3 | 13 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -683448 | backward | before_match | phrase_2 | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -681272 | backward | before_match | phrase_2+word | 1 | 3 | 41 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -651019 | backward | before_match | phrase_2+word | 1 | 3 | 23 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -650145 | backward | after_match | phrase_2 | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -638092 | backward | before_match | phrase_2+word | 1 | 3 | 1,093 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -636897 | backward | after_match | phrase_2+word | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -634531 | backward | before_match | phrase_2 | 2 | 4 | 3 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -621932 | backward | before_match | phrase_2 | 1 | 3 | 4 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -608831 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -598697 | backward | before_match | phrase_2 | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -575456 | backward | before_match | phrase_2 | 2 | 4 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -564601 | backward | before_match | phrase_2 | 1 | 4 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -564601 | backward | before_match | phrase_2+word | 1 | 3 | 3 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -560047 | backward | before_match | phrase_2 | 1 | 4 | 4 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -552862 | backward | after_match | phrase_2+word | 1 | 3 | 23 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -540079 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -520571 | backward | after_match | phrase_2+word | 1 | 3 | 6 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -502996 | backward | after_match | phrase_2+word | 1 | 3 | 16 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -501655 | backward | before_match | phrase_2 | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -480221 | backward | after_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -478048 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -457512 | backward | after_match | phrase_2+word | 1 | 3 | 10 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -447391 | backward | after_match | phrase_2+word | 1 | 3 | 723 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -446872 | backward | after_match | phrase_2+word | 1 | 3 | 906 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -446318 | backward | after_match | phrase_2+word | 1 | 3 | 7 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -444226 | backward | after_match | phrase_2 | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -439583 | backward | before_match | phrase_3+word | 1 | 3 | 7 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -437124 | backward | before_match | phrase_2 | 1 | 3 | 10 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -427894 | backward | after_match | phrase_2+word | 1 | 3 | 108 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -427894 | backward | before_match | phrase_2 | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -422192 | backward | before_match | phrase_2+word | 1 | 3 | 3 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -421098 | backward | before_match | phrase_2+word | 1 | 3 | 17 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -414600 | backward | after_match | phrase_2+word | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -414600 | backward | before_match | phrase_2 | 1 | 3 | 242 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -410712 | backward | after_match | phrase_2+word | 1 | 3 | 8 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -410410 | backward | before_match | phrase_2 | 2 | 4 | 242 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -410027 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -397924 | backward | before_match | phrase_2+phrase_3 | 1 | 3 | 5 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -396630 | backward | before_match | phrase_2+word | 1 | 3 | 265 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -394864 | backward | after_match | phrase_2 | 2 | 4 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -391546 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -380667 | backward | before_match | phrase_2+word | 1 | 3 | 1,062 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -378895 | backward | after_match | phrase_2+word | 1 | 3 | 31 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -377500 | backward | after_match | phrase_2+word | 1 | 3 | 542 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -377500 | backward | before_match | phrase_2+word | 1 | 3 | 8 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -365925 | backward | after_match | phrase_2 | 1 | 4 | 5 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -365925 | backward | before_match | phrase_2+word | 1 | 3 | 22 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -364599 | backward | after_match | phrase_2+word | 1 | 3 | 5 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -364599 | backward | before_match | phrase_2+word | 1 | 3 | 13 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -363693 | backward | after_match | phrase_3+word | 1 | 3 | 52 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -362464 | backward | before_match | phrase_2+word | 1 | 3 | 76 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -360241 | backward | after_match | phrase_3 | 1 | 4 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -360054 | backward | after_match | phrase_2 | 1 | 4 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -360054 | backward | after_match | phrase_2+word | 1 | 3 | 6 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -345475 | backward | before_match | phrase_2+word | 1 | 3 | 3 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -339919 | backward | after_match | phrase_2 | 1 | 5 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -329520 | backward | before_match | phrase_2 | 1 | 5 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -322333 | backward | before_match | phrase_2+word | 1 | 3 | 17 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -321978 | backward | before_match | phrase_2 | 1 | 3 | 7 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -318149 | backward | after_match | phrase_2+word | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -317758 | backward | after_match | phrase_2+word | 1 | 3 | 102 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -312347 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -304150 | backward | after_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -303585 | backward | after_match | phrase_3+word | 1 | 3 | 4 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -303585 | backward | before_match | phrase_2 | 2 | 4 | 3 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -301243 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -299334 | backward | after_match | phrase_2+word | 1 | 3 | 330 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -299334 | backward | before_match | phrase_2+word | 1 | 3 | 6 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -299216 | backward | after_match | phrase_2+word | 1 | 3 | 5 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -298673 | backward | after_match | phrase_2+word | 1 | 3 | 140 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -298673 | backward | before_match | phrase_2+word | 1 | 3 | 34 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -292956 | backward | after_match | phrase_2 | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -292616 | backward | before_match | phrase_2 | 2 | 6 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -292616 | backward | before_match | phrase_2+word | 1 | 3 | 1,037 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -291070 | backward | before_match | phrase_2+phrase_3+word | 1 | 3 | 4 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -291057 | backward | after_match | phrase_2 | 1 | 3 | 5 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -291057 | backward | before_match | phrase_2+word | 1 | 3 | 38 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -289570 | backward | before_match | phrase_2 | 1 | 4 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -286011 | backward | after_match | phrase_2 | 1 | 3 | 5 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -284196 | backward | before_match | phrase_2+word | 1 | 3 | 32 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -281038 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -270282 | backward | before_match | phrase_2 | 1 | 4 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -270109 | backward | after_match | phrase_2+word | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -265070 | backward | after_match | phrase_2+word | 1 | 3 | 3 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -258741 | backward | after_match | phrase_2 | 1 | 3 | 2 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -257145 | backward | before_match | phrase_2+word | 1 | 3 | 172 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -253948 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -252025 | backward | before_match | phrase_2 | 1 | 4 | 1 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -252025 | backward | before_match | phrase_2+word | 1 | 3 | 8 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -250765 | backward | before_match | phrase_2+word | 1 | 3 | 6 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -245709 | backward | before_match | phrase_2+word | 1 | 4 | 10 |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua/Jeshua) | -241884 | backward | before_match | phrase_2+word | 1 | 3 | 1,037 |
| ... | ... | ... | ... | ... | ... | ... | ... | 3,154 more rows in CSV |

## Read

- `Strong phrase rows` require the hidden term plus adjacent same-skip letters to match a surface phrase.
- `Phrase summary rows` also include before-only or after-only phrase matches, which are weaker.
- Strong phrase-extension rows remain post-screen review material; compare Bible and control reports before treating a row as notable.
- This remains post-screen review material; matched phrases can occur elsewhere in the corpus and need manual context checks.
