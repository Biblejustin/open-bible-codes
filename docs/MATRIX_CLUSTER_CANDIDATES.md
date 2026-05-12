# Matrix Cluster Candidates

This is an opt-in geometry screen over already-exported raw ELS hit rows. It wraps each hit path into a matrix of the locked row width, then records declared-term pairs whose letter paths share a cell or fall within the configured cell-neighborhood distance.

This report is candidate extraction only. It is not claim promotion. Matrix-style claims still require a locked row-width protocol, matched Bible and non-Bible controls, and correction for the widened geometry search family.

## Run Settings

- input files: `reports/surface_context_center_exact_hits.csv`
- row width: `50`
- max cell distance: `1`
- max pairs: `100,000`
- allow same term pairs: `False`
- parsed hit rows: `4,502` of `4,502`
- skipped input rows: `0`
- candidate pairs: `356`

## Relation Counts

| Relation | Pairs |
| --- | ---: |
| diagonal | 171 |
| orthogonal | 149 |
| same_cell | 36 |

## Corpus Counts

| Corpus | Pairs |
| --- | ---: |
| TR_NT | 193 |
| SBLGNT | 163 |

## Sample Candidates

| Relation | Corpus | Left | Right | Left center | Right center | Cells |
| --- | --- | --- | --- | --- | --- | --- |
| same_cell | TR_NT | `ιησουσ` (Iesous; English: Jesus) | `υιοσ` (huios; English: Son) | John 11:4 / `αυτης` (autes) | John 11:4 / `ακουσας` (akousas) | 5739:31 -> 5739:31 |
| diagonal | TR_NT | `υιοσ` (huios; English: Son) | `ζωη` (zoe; English: Life) | John 11:27 / `εγω` (ego; English: I) | John 11:25 / `ζωη` (zoe; English: Life) | 5768:47 -> 5767:48 |
| diagonal | TR_NT | `υιοσ` (huios; English: Son) | `αιμα` (haima; English: Blood) | Matthew 13:55 / `ιουδας` (Ioudas; English: Judas) | Matthew 13:55 / `μαριαμ` (mariam; English: Mary) | 798:30 -> 797:31 |
| orthogonal | TR_NT | `υιοσ` (huios; English: Son) | `αιμα` (haima; English: Blood) | Matthew 13:55 / `λεγεται` (legetai) | Matthew 13:55 / `μαριαμ` (mariam; English: Mary) | 796:33 -> 797:33 |
| orthogonal | TR_NT | `υιοσ` (huios; English: Son) | `αιμα` (haima; English: Blood) | Mark 10:33 / `κατακρινουσιν` (katakrinousin) | Mark 10:34 / `αποκτενουσιν` (apoktenousin) | 2542:30 -> 2542:29 |
| orthogonal | TR_NT | `υιοσ` (huios; English: Son) | `αιμα` (haima; English: Blood) | Mark 10:33 / `κατακρινουσιν` (katakrinousin) | Mark 10:34 / `και` (kai; English: and) | 2541:36 -> 2542:36 |
| diagonal | TR_NT | `υιοσ` (huios; English: Son) | `νωε` (Noe; English: Noah) | 1 John 5:20 / `αληθινω` (alethino) | 1 John 5:20 / `γινωσκωμεν` (ginoskomen) | 12828:35 -> 12827:34 |
| diagonal | TR_NT | `αιμα` (haima; English: Blood) | `νωε` (Noe; English: Noah) | Colossians 1:14 / `απολυτρωσιν` (apolutrosin) | Colossians 1:14 / `αμαρτιων` (amartion) | 10830:18 -> 10831:19 |
| diagonal | TR_NT | `υιοσ` (huios; English: Son) | `νωε` (Noe; English: Noah) | 1 John 5:20 / `αληθινω` (alethino) | 1 John 5:20 / `χριστω` (christo; English: Christ) | 12827:37 -> 12828:38 |
| orthogonal | TR_NT | `υιοσ` (huios; English: Son) | `νωε` (Noe; English: Noah) | 1 John 5:20 / `αληθινω` (alethino) | 1 John 5:20 / `υιω` (uio) | 12828:35 -> 12827:35 |
| diagonal | TR_NT | `αιμα` (haima; English: Blood) | `νωε` (Noe; English: Noah) | Colossians 1:14 / `απολυτρωσιν` (apolutrosin) | Colossians 1:14 / `ω` (o) | 10830:3 -> 10829:2 |
| same_cell | TR_NT | `υιοσ` (huios; English: Son) | `σημ` (Sem; English: Shem) | 1 John 5:5 / `μη` (me; English: not) | 1 John 5:4 / `η` (e) | 12797:38 -> 12797:38 |
| orthogonal | TR_NT | `υιοσ` (huios; English: Son) | `σημ` (Sem; English: Shem) | 1 John 5:5 / `εστιν` (estin) | 1 John 5:4 / `η` (e) | 12797:33 -> 12797:32 |
| diagonal | TR_NT | `νωε` (Noe; English: Noah) | `σημ` (Sem; English: Shem) | 1 Timothy 1:2 / `γνησιω` (gnesio) | 1 Timothy 1:2 / `ιησου` (iesou) | 11203:5 -> 11204:6 |
| diagonal | TR_NT | `νωε` (Noe; English: Noah) | `σημ` (Sem; English: Shem) | 1 Timothy 1:2 / `ημων` (emon) | 1 Timothy 1:2 / `ιησου` (iesou) | 11203:5 -> 11204:6 |
| diagonal | TR_NT | `φωσ` (phos; English: Light) | `σημ` (Sem; English: Shem) | Philippians 2:15 / `φωστηρες` (phosteres) | Philippians 2:16 / `ημεραν` (emeran) | 10715:29 -> 10716:30 |
| diagonal | TR_NT | `υιοσ` (huios; English: Son) | `σημ` (Sem; English: Shem) | 2 Corinthians 1:19 / `υμιν` (umin; English: to you) | 2 Corinthians 1:18 / `ημων` (emon) | 9766:9 -> 9765:10 |
| same_cell | TR_NT | `υιοσ` (huios; English: Son) | `σημ` (Sem; English: Shem) | 2 Corinthians 1:19 / `θεου` (theou) | 2 Corinthians 1:18 / `ημων` (emon) | 9764:40 -> 9764:40 |
| same_cell | TR_NT | `ζωη` (zoe; English: Life) | `σημ` (Sem; English: Shem) | 2 Peter 1:3 / `δυναμεως` (dunameos) | 2 Peter 1:3 / `της` (tes; English: of the) | 12519:29 -> 12519:29 |
| diagonal | TR_NT | `υιοσ` (huios; English: Son) | `σημ` (Sem; English: Shem) | Matthew 12:40 / `τρεις` (treis) | Matthew 12:39 / `δοθησεται` (dothesetai) | 673:18 -> 672:17 |
| same_cell | TR_NT | `υιοσ` (huios; English: Son) | `σημ` (Sem; English: Shem) | John 12:34 / `εις` (eis; English: into/for) | John 12:34 / `απεκριθη` (apekrithe) | 5875:25 -> 5875:25 |
| orthogonal | TR_NT | `αγαπη` (agape; English: Love) | `σημ` (Sem; English: Shem) | 1 John 3:17 / `αυτω` (auto; English: to him) | 1 John 3:19 / `της` (tes; English: of the) | 12740:0 -> 12741:0 |
| orthogonal | TR_NT | `νωε` (Noe; English: Noah) | `σημ` (Sem; English: Shem) | 1 Timothy 1:2 / `γνησιω` (gnesio) | 1 Timothy 1:1 / `ιησου` (iesou) | 11202:48 -> 11201:48 |
| diagonal | TR_NT | `νωε` (Noe; English: Noah) | `σημ` (Sem; English: Shem) | Luke 17:26 / `ουτως` (outos) | Luke 17:27 / `ηλθεν` (elthen) | 4398:21 -> 4399:22 |
| orthogonal | TR_NT | `νωε` (Noe; English: Noah) | `σημ` (Sem; English: Shem) | Luke 17:26 / `ουτως` (outos) | Luke 17:27 / `ηλθεν` (elthen) | 4398:22 -> 4399:22 |
