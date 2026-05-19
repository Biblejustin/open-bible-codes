# Extension Top Hits Review

Scope:

- Source hit file: `reports/protocols/public_baseline/surface_context_hits.csv`
- Extension files:
  - `reports/protocols/public_baseline/surface_context_extensions_tr_nt_top.csv`
  - `reports/protocols/public_baseline/surface_context_extensions_sblgnt_top.csv`
- Settings: same-skip before/after scan, `max_before=12`, `max_after=12`, `phrase_words=4`, `include_both_sided=true`, `max_extensions_per_hit=20`
- Summary filter: `min_extension_length=3`, `min_term_length=4`, `match_kind_prefix=phrase_`, `exclude_term=ουλ` (Oul; English: Hul)

This is a screening review only. It reports what the tool surfaced; it does not treat any row as statistically meaningful.

## Run Totals

| Corpus | Input surface-context hits | Raw extension rows | Kept after filters | Summary groups | Top rows |
| --- | ---: | ---: | ---: | ---: | ---: |
| TR_NT | 28,123 | 37,190 | 485 | 422 | 11 |
| SBLGNT | 28,531 | 36,946 | 452 | 397 | 21 |

Protocol timings on this run:

| Step | Time |
| --- | ---: |
| `surface_extensions_tr_nt` | 3.376s |
| `surface_extensions_sblgnt` | 3.358s |
| `surface_extension_summary_tr_nt` | 0.213s |
| `surface_extension_summary_sblgnt` | 0.213s |

## Shape Of The Top Rows

The top files are now filtered to phrase matches with base terms of at least four normalized letters and extension lengths of at least three. This removes the worst short-term noise.

| Corpus | Top-row term leaders | Extension length shape | Match kind shape |
| --- | --- | --- | --- |
| TR_NT | `υιος` (huios; English: son) 4, `θεος` (theos; English: God) 3, `ναος` (naos; English: temple) 1, `αιμα` (haima; English: blood) 1, `αδαμ` (Adam; English: Adam) 1, `δοξα` (doxa; English: glory) 1 | 10/11 rows have extension length 3 | all 11 rows match phrases |
| SBLGNT | `υιος` (huios; English: son) 8, `αιμα` (haima; English: blood) 5, `σαλα` (Sala; English: Shelah) 2, plus single rows for `ΝΑΤΟ` (NATO; English: NATO), `ισαακ` (Isaak; English: Isaac), `θεος` (theos; English: God), `αδαμ` (Adam; English: Adam), `ναος` (naos; English: temple), `δοξα` (doxa; English: glory) | 20/21 rows have extension length 3 | all 21 rows match phrases |

Interpretation:

- `ουλ` (Oul; English: Hul) was excluded because it dominated the previous top file and mostly extended into ordinary servant/people/Saul surface forms.
- Phrase matches are surface-lexicon matches elsewhere in the same corpus, not conclusive evidence that the hit location itself reads as that phrase.
- Remaining rows are more readable. The first paired-control pass is tracked in
  `docs/EXTENSION_PAIRED_CONTROLS.md`.

## Stronger TR_NT Candidates

Rows below use a rough stricter screen: normalized base term length at least 4 and extension length at least 3.

| Term | Skip | Type | Extended sequence | Surface match | Hit span | Center/context |
| --- | ---: | --- | --- | --- | --- | --- |
| `θεος` (theos; English: God) | -40 | term plus after | `θεοσοτιο` (theosotio; English: hidden extension form from theos) | `Θεός ὅτι ὁ` (Theos hoti ho; English: God, because the) | MAT 24:48-MAT 24:46 | center MAT 24:48 `δὲ` (de; English: but/and); same category center `lord_g` |
| `ναος` (naos; English: temple) | -38 | both-sided | `ηοναοσο` (eonaoso; English: hidden extension form from naos) | `ἢ ὁ ναὸς ὁ` (e ho naos ho; English: or the temple the) | MAT 27:9-MAT 27:8 | center MAT 27:9 `Καὶ` (kai; English: and); same category span |
| `υιος` (huios; English: son) | -4 | term plus after | `υιοστησ` (huiostes; English: hidden extension form from huios) | `υἱὸς τῆς` (huios tes; English: son of the) | JHN 5:13-JHN 5:13 | center JHN 5:13 `γὰρ` (gar; English: for); same category center `jesus_g` |
| `υιος` (huios; English: son) | 25 | before plus term | `οδευιοσ` (odehuios; English: hidden extension form from huios) | `ὁ δὲ υἱὸς` (ho de huios; English: but the son) | MAT 16:19-MAT 16:20 | center MAT 16:20 `τοῖς` (tois; English: to the); same category center `jesus_g`, `christ_g` |
| `αιμα` (haima; English: blood) | -2 | before plus term | `εισαιμα` (eishaima; English: hidden extension form from haima) | `εἰς αἷμα` (eis haima; English: into blood) | 2CO 6:16-2CO 6:16 | center 2CO 6:16 `μοι` (moi; English: to me); same category center `temple_g` |
| `αδαμ` (Adam; English: Adam) | 11 | term plus after | `αδαμεισ` (adameis; English: hidden extension form from Adam) | `Ἀδὰμ εἰς` (Adam eis; English: Adam into) | HEB 13:15-HEB 13:16 | center HEB 13:16 `εὐποιΐας` (eupoiias; English: doing good) |
| `δοξα` (doxa; English: glory) | 21 | term plus after | `δοξανωσ` (doxanos; English: hidden extension form from doxa) | `δόξαν ὡς` (doxan hos; English: glory as) | 2TH 3:1-2TH 3:1 | center 2TH 3:1 `Κυρίου` (Kyriou; English: of the Lord); exact center |

## Stronger SBLGNT Candidates

| Term | Skip | Type | Extended sequence | Surface match | Hit span | Center/context |
| --- | ---: | --- | --- | --- | --- | --- |
| `υιος` (huios; English: son) | 36 | both-sided | `ουιοσει` (ouiosei; English: hidden extension form from huios) | `ὁ υἱός, εἰ` (ho huios ei; English: the son, if) | John 16:33-John 17:1 | center John 16:33 `θαρσεῖτε` (tharseite; English: take courage); exact span John 17:1 |
| `αιμα` (haima; English: blood) | 14 | both-sided | `ναιμανο` (naimano; English: hidden extension form from haima) | `Ναιμὰν ὁ` (Naiman ho; English: Naaman the) | Rev 17:5-Rev 17:6 | center Rev 17:6 `γυναῖκα` (gynaika; English: woman); exact center |
| `ΝΑΤΟ` (NATO; English: NATO) | 19 | both-sided | `ενατομω` (enatomo; English: hidden extension form resembling "in an atom") | `ἐν ἀτόμῳ` (en atomo; English: in an instant/atom) | John 5:35-John 5:36 | center John 5:36 `δὲ` (de; English: but/and) |
| `υιος` (huios; English: son) | 33 | before plus term | `ειουιοσ` (eiouios; English: hidden extension form from huios) | `εἶ ὁ υἱός` (ei ho huios; English: you are the son) | Matt 14:31-Matt 14:33 | center Matt 14:32 `ἀναβάντων` (anabanton; English: having gone up); exact span Matt 14:33 |
| `υιος` (huios; English: son) | -4 | term plus after | `υιοστησ` (huiostes; English: hidden extension form from huios) | `υἱὸς τῆς` (huios tes; English: son of the) | John 5:13-John 5:13 | center John 5:13 `γὰρ` (gar; English: for); same category center `jesus_g` |
| `ισαακ` (Isaak; English: Isaac) | 41 | before plus term | `καιισαακ` (kaiisaak; English: and Isaac) | `καὶ Ἰσαὰκ` (kai Isaak; English: and Isaac) | Luke 22:53-Luke 22:55 | center Luke 22:54 `ἀρχιερέως` (archiereos; English: high priest) |
| `υιος` (huios; English: son) | 25 | before plus term | `ουουιοσ` (ouhuios; English: hidden extension form from huios) | `οὗ ὁ υἱὸς` (hou ho huios; English: whose son) | Luke 19:9-Luke 19:10 | center Luke 19:9 `ἐστιν` (estin; English: is); exact center Luke 19:9-10 |
| `θεος` (theos; English: God) | 36 | before plus term | `εισθεοσ` (eistheos; English: hidden extension form from theos) | `εἷς θεὸς` (heis theos; English: one God) | Jas 4:14-Jas 4:15 | center Jas 4:14 `φαινομένη` (phainomene; English: appearing); same category span |
| `αιμα` (haima; English: blood) | 41 | before plus term | `εισαιμα` (eishaima; English: hidden extension form from haima) | `εἰς αἷμα` (eis haima; English: into blood) | Acts 5:17-Acts 5:19 | center Acts 5:18 `ἔθεντο` (ethento; English: they put/placed); same category span |
| `αδαμ` (Adam; English: Adam) | 11 | term plus after | `αδαμεισ` (adameis; English: hidden extension form from Adam) | `Ἀδὰμ εἰς` (Adam eis; English: Adam into) | Heb 13:15-Heb 13:16 | center Heb 13:16 `εὐποιΐας` (eupoiias; English: doing good) |
| `δοξα` (doxa; English: glory) | 21 | term plus after | `δοξανωσ` (doxanos; English: hidden extension form from doxa) | `δόξαν ὡς` (doxan hos; English: glory as) | 2Thess 3:1-2Thess 3:1 | center 2Thess 3:1 `κυρίου` (Kyriou; English: of the Lord); exact center |

## TR_NT vs SBLGNT Overlap

Strict overlap means same term, skip, direction, extension type, extended sequence, and matched normalized form appeared in both filtered top files. There were 3 strict overlaps.

Representative overlaps:

| Term | Skip | Type | Extended sequence | Surface match | TR_NT span/context | SBLGNT span/context |
| --- | ---: | --- | --- | --- | --- | --- |
| `υιος` (huios; English: son) | -4 | term plus after | `υιοστησ` (huiostes; English: hidden extension form from huios) | `υἱὸς τῆς` (huios tes; English: son of the) | JHN 5:13; same category center | John 5:13; same category center |
| `αδαμ` (Adam; English: Adam) | 11 | term plus after | `αδαμεισ` (adameis; English: hidden extension form from Adam) | `Ἀδὰμ εἰς` (Adam eis; English: Adam into) | HEB 13:15-HEB 13:16 | Heb 13:15-Heb 13:16 |
| `δοξα` (doxa; English: glory) | 21 | term plus after | `δοξανωσ` (doxanos; English: hidden extension form from doxa) | `δόξαν ὡς` (doxan hos; English: glory as) | 2TH 3:1; exact center | 2Thess 3:1; exact center |

## Review Notes

- The strongest-looking rows are mostly ordinary Greek article/preposition completions around theological terms.
- TR_NT and SBLGNT overlaps are useful because they survive text-form variation, but most overlaps occur where the underlying text is essentially the same.
- `ουλ` (Oul; English: Hul) should remain excluded from top-rank review unless analyzed separately.
- Duplicate-looking rows can appear when separate term rows normalize to the same ELS term.
- The first paired null-control pass made these rows a review queue, not a claim.

## Next Analysis Choices

1. Review the stricter overlap-only controls in `docs/EXTENSION_OVERLAP_CONTROLS.md`.
2. Add a human review report generator that joins extension top rows back to surface context fields automatically.
3. Run broader declared term searches and use the stricter summary filters by default.
