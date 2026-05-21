# Greek Surface New Terms Queue

Status: prospective exact-center surface queue; no claim.

This report summarizes exact-center surface hits from the locked Greek surface
new-terms term screen after prior selected rows were removed. It does not
require same-skip phrase extension and does not run controls.

## Inputs

- Surface hits: `reports/greek_surface_new_terms/surface_context_hits.csv`
- Term scope: `terms/greek_surface_new_terms_clean_lock.csv`
- Compared sources: TR_NT, BYZ_NT, TCG_NT, SBLGNT

## Definition

`exact-center surface` means the ELS hit center falls in a verse where the
normalized term also appears as ordinary surface text. The `Center words`
column reports the actual word at the ELS center offset, so it may differ
from the searched term.

## Scope Counts

| Scope | Patterns |
| --- | ---: |
| `all_sources` | 9 |
| `multi_source` | 8 |
| `source_only` | 21 |

Total exact-center surface patterns: 38.

## Top Term Queue

| Term | Concept | Exact-center hits | Unique patterns | All-source | Multi-source | Source-specific | Read |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `ονομα` (onoma; English: Name) | ὄνομα | 38 | 20 | 5 | 3 | 12 | all-source surface queue; needs controls before interpretation |
| `οικοσ` (oikos; English: House) | οἶκος | 7 | 2 | 1 | 1 | 0 | all-source surface queue; needs controls before interpretation |
| `σοφια` (sophia; English: wisdom) | σοφία | 4 | 1 | 1 | 0 | 0 | all-source surface queue; needs controls before interpretation |
| `θυσια` (thusia; English: Sacrifice) | θυσία | 4 | 1 | 1 | 0 | 0 | all-source surface queue; needs controls before interpretation |
| `σκηνη` (skene; English: Tabernacle) | σκηνή | 4 | 1 | 1 | 0 | 0 | all-source surface queue; needs controls before interpretation |
| `αρτοσ` (artos; English: Bread) | ἄρτος | 4 | 2 | 0 | 1 | 1 | multi-source surface queue; inspect source distribution |
| `σιμων` (simon; English: Simon the Zealot) | Simon the Zealot | 4 | 2 | 0 | 1 | 1 | multi-source surface queue; inspect source distribution |
| `τοξον` (toxon) | τόξον | 3 | 1 | 0 | 1 | 0 | multi-source surface queue; inspect source distribution |
| `ιεσσαι` (iessai; English: Jesse) | Jesse | 3 | 1 | 0 | 1 | 0 | multi-source surface queue; inspect source distribution |
| `στομα` (stoma) | στόμα | 2 | 2 | 0 | 0 | 2 | source-specific surface queue |
| `αγαπη` (agape; English: Love) | ἀγάπη | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `ελεοσ` (eleos; English: Mercy) | ἔλεος | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `νοσοσ` (nosos) | νόσος | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `εθνοσ` (ethnos) | ἔθνος | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `ελλην` (ellen) | Ἕλλην | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |

## All-Source Pattern Examples

| Term | Center | Skip | Direction | Present | Center words |
| --- | --- | ---: | --- | --- | --- |
| `σοφια` (sophia; English: wisdom) | Acts 6:10 | -24 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`σοφίᾳ` (sophia; English: wisdom); BYZ_NT:`σοφια` (sophia; English: wisdom); TCG_NT:`σοφίᾳ` (sophia; English: wisdom); SBLGNT:`σοφίᾳ` (sophia; English: wisdom) |
| `θυσια` (thusia; English: Sacrifice) | Heb 10:11 | -36 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ἁμαρτίας` (amartias); BYZ_NT:`αμαρτιασ` (amartias); TCG_NT:`ἁμαρτίας·` (amartias); SBLGNT:`ἁμαρτίας.` (amartias) |
| `ονομα` (onoma; English: Name) | Luke 19:38 | -15 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`Εὐλογημένος` (eulogemenos); BYZ_NT:`ευλογημενοσ` (eulogemenos); TCG_NT:`Εὐλογημένος` (eulogemenos); SBLGNT:`Εὐλογημένος` (eulogemenos) |
| `ονομα` (onoma; English: Name) | Acts 9:28 | -3 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`παρρησιαζόμενος` (parresiazomenos); BYZ_NT:`παρρησιαζομενοσ` (parresiazomenos); TCG_NT:`παρρησιαζόμενος` (parresiazomenos); SBLGNT:`παρρησιαζόμενος` (parresiazomenos) |
| `ονομα` (onoma; English: Name) | Matt 10:2 | 3 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ὀνόματά` (onomata); BYZ_NT:`ονοματα` (onomata); TCG_NT:`ὀνόματά` (onomata); SBLGNT:`ὀνόματά` (onomata) |
| `ονομα` (onoma; English: Name) | Phil 4:3 | 3 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ὀνόματα` (onomata); BYZ_NT:`ονοματα` (onomata); TCG_NT:`ὀνόματα` (onomata); SBLGNT:`ὀνόματα` (onomata) |
| `ονομα` (onoma; English: Name) | Matt 24:9 | 27 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`μισούμενοι` (misoumenoi); BYZ_NT:`μισουμενοι` (misoumenoi); TCG_NT:`μισούμενοι` (misoumenoi); SBLGNT:`μισούμενοι` (misoumenoi) |
| `οικοσ` (oikos; English: House) | Acts 16:31 | 4 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`Κύριον` (kurion); BYZ_NT:`κυριον` (kurion); TCG_NT:`Κύριον` (kurion); SBLGNT:`κύριον` (kurion) |
| `σκηνη` (skene; English: Tabernacle) | Heb 9:8 | -9 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`τῆς` (tes; English: of the); BYZ_NT:`τησ` (tes; English: of the); TCG_NT:`τῆς` (tes; English: of the); SBLGNT:`τῆς` (tes; English: of the) |

## Read

This queue is broader and weaker than the phrase-extension gate. It is useful
for deciding which exact-center surface rows deserve matched controls.
It does not promote any row to claim status.
