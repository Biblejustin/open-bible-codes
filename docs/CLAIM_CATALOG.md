# Claim Catalog

Catalog:

- `claims/claim_catalog.csv`

Purpose:

- keep public, user-requested, and project-discovered ELS candidates in one
  reviewable table;
- separate term screening from claim reproduction;
- record current reproduction status without promoting raw hits into claims.

## Status Values

| Status | Meaning |
| --- | --- |
| `reproducible` | Current code reproduces the declared rule and target in the stated corpus. |
| `partially_reproducible` | Some component is reproducible, but the result is not a full claim. |
| `controlled_review_candidate` | Controls and context justify more review, not public promotion. |
| `not_reproducible` | Current declared run did not reproduce the target. |
| `under_specified` | Source, spelling, skip, corpus, layout, or metric is not locked enough. |
| `license_blocked` | Reproduction depends on text/code/data that cannot be redistributed or used. |

## Current Entries

| Group | Status | Entries | Current read |
| --- | --- | ---: | --- |
| Common Torah skip-50 examples | `reproducible` | 5 | Engine sanity checks pass on Koren Torah files. |
| WRR 1994 rabbis | `under_specified` | 1 | Source audit exists; needs locked 298-to-163 pair path, corrected distance, skip caps, and permutation rule. |
| Greek `δοξα` (doxa; English: glory) extension follow-up | `controlled_review_candidate` | 1 | Four-source 5000/5000 and 20000/20000 follow-ups passed their registered review gates; still post-discovery and not a claim. |
| Greek `γωγ` (Gog; English: Gog) centered occurrence | `controlled_review_candidate` | 1 | Hidden `γωγ` (Gog; English: Gog) centers on open `Gog` at Rev 20:8 across four Greek NT source labels; length-3 controls make it contextual rather than frequency-promoted. |
| Greek expanded surface follow-up | `controlled_review_candidate` | 1 | `ανομια` (anomia; English: lawlessness), `ισαακ` (Isaak; English: Isaac), and `τερασ` (teras; English: wonder) pass letter-path and all-available real-word control review; still post-screen and not a claim. |
| All-codes `יום יהוה` (yom YHWH; English: day of YHWH) compound-extension follow-up | `controlled_review_candidate` | 1 | The selected `יום יהוה` (yom YHWH; English: day of YHWH) -> `היומיהוה` (hayom YHWH; English: the day of YHWH) key passes locked 5000/5000 controls in five MT-family sources with conservative all-control q = 0.003599; still post-discovery and not a claim. |
| Greek length-4 surface follow-up | `partially_reproducible` | 1 | Length-4 rows reproduce, but generated vocabulary controls overlap every target and no target survives study-level q <= 0.05. |
| Modern/geopolitical short forms | `partially_reproducible` | 1 | Presence remains reproducible through the wide skip run; controls do not support significance. |
| Full modern country phrases | `not_reproducible` | 1 | Long country and institution phrases remain absent through the wide exact follow-up. |
| Local business/place terms | `partially_reproducible` | 1 | Cowboy has ordinary controlled hits; Simsberry has one MAM-only row; local phrase claims are not supported. |
| Apocrypha bridge-completion study | `mixed` | 2 | LXX bridge rows do not stand out under 100-sample shuffled controls; KJVA bridge rows stand above same-length controls at total and term-review layers plus 250-sample total shuffled controls; 1000-sample term controls left 15 BH q <= 0.05 terms, and locked 5000-sample post-screen controls kept all 15 at q <= 0.01 with 3 above every shuffled sample. This remains post-screen. |
| Bible Code Digest claim families | `under_specified` | 8 | Source audit and BCD-specific term list exist, but exact spellings, row widths, skip limits, proximity metrics, and control rules still need claim-by-claim locks. |
| TheWordNotes / Rambsel / Jeffrey claim families | `under_specified` | 4 | Source audit and term list exist; exact source editions, letter indexes, skip rules, and cluster metrics still need claim-by-claim locks. |
| Cosmic Codes claim families | `under_specified` | 5 | Source audit and term list exist; the source is copyrighted and exact text editions, table geometry, source attributions, and control metrics still need claim-by-claim locks. |
| Mark Tabata Isaiah 53 claim families | `under_specified` | 2 | Public web audit and term list exist; exact Hebrew spellings, table geometry, and statistical framing still need source-locked reproduction. |
| Felcjo Ringo algorithm/control source | `under_specified` | 1 | Methodology audit exists; useful as a naive implementation and non-Bible control caution, not as a positive claim. |
| Bible and Science critique/source families | `under_specified` | 3 | Critique audit and stress-term list exist; useful for source-variation, non-Bible controls, and non-ELS code categories. |
| Religions Wiki scriptural-code critique families | `under_specified` | 4 | Critique audit and stress-term list exist; useful for Qur'an/numeric/theomatics examples, cognitive-bias guardrails, and non-Bible controls. |
| Amandasaurus/Rory Biblecode implementation prior art | `under_specified` | 1 | Public Rust implementation audit exists; useful for KJV/Gutenberg normalization, signed-skip discovery, and matrix-style display cautions. |
| Bible-codes.org pictogram/source families | `under_specified` | 5 | Source audit and term list exist; useful for KJV matrix demos, pictogram clusters, prediction claims, and source-defined authenticity criteria. |
| Public media-style Hebrew claims | `under_specified` | 3 | Terms exist, but claim geometry has not been locked. |
| Critical omissions / word multiples | `partially_reproducible` | 2 | Study artifacts exist; claim rules remain screening-level. |

## Use

Before elevating any row:

1. cite the claim source;
2. lock corpus, spelling, skip range, direction, layout, and metric;
3. run exact source-distribution checks where versions align;
4. run row-local matched controls;
5. save examples, context, and letter paths;
6. update the catalog status and evidence path.

This catalog is deliberately conservative. A term appearing in an ELS screen is
not enough for `reproducible`; the declared claim rule has to be reproduced.

WRR-specific requirements are tracked in `docs/WRR_REPLICATION_PLAN.md`,
`docs/WRR_SOURCE_AUDIT.md`, `docs/WRR_METHODOLOGY_GAPS.md`, and
`docs/WRR_CORRECTED_DISTANCE_NOTES.md`.
Greek surface claim-level requirements are tracked in
`docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md`.
Bible Code Digest source leads are tracked in `docs/BIBLE_CODE_DIGEST_AUDIT.md`.
CRI critique guardrails are tracked in `docs/CRI_ELS_CRITIQUE_AUDIT.md`.
TheWordNotes ELS source leads are tracked in
`docs/THEWORDNOTES_ELS_AUDIT.md`.
Cosmic Codes source leads are tracked in `docs/COSMIC_CODES_AUDIT.md`.
Mark Tabata Isaiah 53 source leads are tracked in
`docs/MARK_TABATA_ISAIAH53_AUDIT.md`.
Felcjo Ringo algorithm/control notes are tracked in
`docs/FELCJO_RINGO_ALGORITHM_AUDIT.md`.
Bible and Science critique/source notes are tracked in
`docs/BIBLE_AND_SCIENCE_CODES_AUDIT.md`.
Religions Wiki critique/source notes are tracked in
`docs/RELIGIONS_WIKI_SCRIPTURAL_CODES_AUDIT.md`.
Amandasaurus/Rory Biblecode prior-art notes are tracked in
`docs/AMANDASAURUS_BIBLECODE_PRIOR_ART_AUDIT.md`.
Bible-codes.org pictogram/source notes are tracked in
`docs/BIBLE_CODES_ORG_AUDIT.md`.
