# Apocrypha Bridge-Completion Study

Status: completed bridge-completion review layer over declared
apocrypha/deuterocanon source paths. This is review material, not claim
evidence.

## Purpose

The current report set treats this as a tracked review layer over the
already-declared corpora. It keeps two separate questions apart:

1. Which ordinary ELS, centered, surface-context, and extension patterns appear
   inside apocrypha/deuterocanon witnesses?
2. Which partial canonical-text ELS paths become complete only when
   apocrypha/deuterocanon material is inserted into the declared full text
   stream?

The second question is the bridge-completion question. It should not be mixed
with ordinary hit counts.

## Candidate Sources

Current coverage audit: `docs/APOCRYPHA_SOURCE_COVERAGE.md`.
Initial bounded bridge-candidate scan: `docs/APOCRYPHA_BRIDGE_CANDIDATES.md`.
Initial bridge surface-context review: `docs/APOCRYPHA_BRIDGE_CONTEXT.md`.
Initial non-Bible boundary controls: `docs/APOCRYPHA_BRIDGE_CONTROLS.md`.
Initial shuffled apocrypha-block controls:
`docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md`.
Expanded 50-sample shuffled apocrypha-block controls:
`docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_50.md`.
Expanded 100-sample shuffled apocrypha-block controls:
`docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_100.md`.
Ordinary apocrypha-only counts: `docs/APOCRYPHA_ONLY_COUNTS.md`.
KJV + Apocrypha ordinary counts: `docs/KJV_APOCRYPHA_ONLY_COUNTS.md`.
KJV + Apocrypha bridge candidates: `docs/KJV_APOCRYPHA_BRIDGE_CANDIDATES.md`.
KJV + Apocrypha bridge surface-context review:
`docs/KJV_APOCRYPHA_BRIDGE_CONTEXT.md`.
KJV + Apocrypha bridge controls: `docs/KJV_APOCRYPHA_BRIDGE_CONTROLS.md`.
KJV + Apocrypha bridge term-level review:
`docs/KJV_APOCRYPHA_BRIDGE_TERM_REVIEW.md`.
Bridge-completion review packet:
`docs/APOCRYPHA_BRIDGE_COMPLETION_REVIEW.md`.
KJV + Apocrypha bridge term-level shuffled controls:
`docs/KJV_APOCRYPHA_BRIDGE_TERM_SHUFFLED_CONTROLS_1000.md`.
KJV + Apocrypha bridge confirmatory preregistration:
`docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_PREREGISTRATION.md`.
KJV + Apocrypha bridge confirmatory shuffled controls:
`docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_CONTROLS_5000.md`.
KJV + Apocrypha bridge shuffled controls:
`docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md`.
KJV + Apocrypha expanded 50-sample bridge shuffled controls:
`docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_50.md`.
KJV + Apocrypha expanded 100-sample bridge shuffled controls:
`docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_100.md`.
KJV + Apocrypha expanded 250-sample bridge shuffled controls:
`docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_250.md`.
One-command protocol: `protocols/apocrypha_bridge_study.toml`.
Expanded shuffled-control protocol:
`protocols/apocrypha_bridge_shuffled_controls_50.toml`.
Expanded 100-sample shuffled-control protocol:
`protocols/apocrypha_bridge_shuffled_controls_100.toml`.
KJV + Apocrypha expanded 250-sample shuffled-control protocol:
`protocols/kjv_apocrypha_bridge_shuffled_controls_250.toml`.
KJV + Apocrypha bridge term-level review protocol:
`protocols/kjv_apocrypha_bridge_term_review.toml`.
KJV + Apocrypha bridge term-level shuffled-control protocol:
`protocols/kjv_apocrypha_bridge_term_shuffled_controls_1000.toml`.
KJV + Apocrypha bridge confirmatory shuffled-control protocol:
`protocols/kjv_apocrypha_bridge_confirmatory_controls_5000.toml`.

Current first-pass read: the existing GRCLXX stream already has enough
deuterocanon/apocrypha material to test boundary-spanning paths, but the first
Malachi/Tobit boundary scan does not stand above non-Bible boundary controls.
The observed scan found 62 bridge rows; same-length Iliad, Odyssey, and
Herodotus replacement blocks produced 59, 39, and 61 bridge rows. Treat this as
evidence that ordinary boundary opportunities can generate comparable bridge
rows.
The LXX bridge-context pass found no center-word exact rows, one
center-verse exact row, and four span-exact rows. These remain review aids,
not significance claims.
The expanded LXX shuffled-insertion control kept the canonical prefix and
apocrypha block length fixed while shuffling the apocrypha letters. Its 100
samples produced 36 to 73 bridge rows, with 16 samples at or above the 62
observed rows (`p_ge=0.168317`). Under this control, the LXX bridge-row total
does not stand out.
The separate KJVA ordinary-count pass found 254,475 English apocrypha hits
across 575 English queries, compared with 234,606, 227,967, and 232,226 hits in
same-length Shakespeare, War and Peace, and Moby-Dick control blocks.
The KJVA bridge pass found 350 bridge rows across 81 terms. The same-length
English controls produced 182, 140, and 168 bridge rows, so KJVA bridge rows
stand above this first control set, but they still need term-level review,
surface context, and stronger locked controls before claim language.
The KJVA bridge-context pass found no center-word exact rows, four
center-verse exact rows, and seventeen span-exact rows. The highest-priority
queue should be read as "interesting to inspect" rather than "interpreted."
The term-level review found 48 of 81 KJVA bridge terms above all three
same-length non-Bible term controls and 53 terms with some center/span context
bucket beyond hidden-path-only. The 1000-sample term-level shuffled control
found 8 of 81 terms above every shuffled sample, 25 terms with unadjusted
`p_ge <= 0.05`, and 15 terms with Benjamini-Hochberg `q_ge <= 0.05`.
This raises the KJVA bridge-term follow-up priority, but it remains
post-screen calibration rather than claim evidence.
The locked 5000-sample post-screen confirmatory follow-up over those 15 terms
found all 15 with Benjamini-Hochberg `q_ge <= 0.01`, and 3 terms stood above
every shuffled sample. This strengthens follow-up priority, but it is still
post-screen confirmatory calibration rather than original prospective discovery
or claim-grade evidence.
The expanded KJVA shuffled-insertion control produced 149 to 236 bridge rows
across 250 samples against 350 observed rows (`p_ge=0.003984`). That remains a
stronger follow-up signal than the LXX boundary result, but it is still a
screening/control result rather than claim-grade evidence.

Add only sources with clean licensing and stable source metadata. Candidate
families include:

- Greek LXX deuterocanon/apocrypha witnesses.
- Greek Esther and Daniel additions.
- Tobit textual variants where source licensing and verse mapping are clear.
- Sirach, Wisdom, Baruch, Judith, and Maccabees.
- KJV Apocrypha or other open-license English apocrypha witnesses.
- Hebrew or Aramaic fragments only when the text source, license, and alignment
  rules are documented.

Each witness should be imported as its own corpus/source family. Do not merge
them silently into MT, LXX, TR, critical NT, or English Bible corpora.

## Bridge Definition

A bridge-completion candidate is a complete ELS in an expanded stream where:

- the expanded stream includes a declared apocrypha/deuterocanon insertion;
- at least one matched letter is from canonical text;
- at least one matched letter is from apocrypha/deuterocanon text;
- removing the apocrypha/deuterocanon material leaves only a partial path, not a
  complete ELS under the same expanded-stream path;
- the insertion order, book boundaries, normalization, direction, and skip rule
  were declared before running.

This makes the result "partial in canonical-only text, complete in expanded
text" rather than merely "found somewhere in apocrypha."

## Classifications

Report bridge candidates separately from ordinary hits:

- `apocrypha_only`: all matched letters are inside apocrypha/deuterocanon text.
- `canonical_to_apocrypha`: path begins in canonical text and enters
  apocrypha/deuterocanon text.
- `apocrypha_to_canonical`: path begins in apocrypha/deuterocanon text and
  exits into canonical text.
- `canonical_apocrypha_canonical`: path crosses an inserted apocrypha block and
  returns to canonical text.
- `multi_insertion_bridge`: path touches more than one inserted block.

For each candidate, preserve letter-level provenance:

- term letter index;
- matched character;
- corpus/source label;
- book/chapter/verse;
- word at that position where available;
- normalized offset in expanded stream;
- projected canonical-only offset when defined;
- insertion block identifier.

## Required Outputs

The bridge study records these output classes:

- expanded-source manifest with source checksums and insertion order;
- full ordinary ELS hit counts for apocrypha witnesses;
- bridge-completion CSV with letter-level provenance;
- centered-occurrence summary for bridge candidates;
- surface-context and same-skip extension summaries;
- version/source presence comparison;
- non-Bible and shuffled-insertion controls;
- report that distinguishes presence from frequency.

## Controls

Bridge completions need their own controls because adding text mechanically
creates more opportunities. Minimum controls:

- insert comparable non-Bible text blocks at the same declared insertion points;
- shuffle apocrypha/deuterocanon insertion blocks while preserving length and
  alphabet;
- compare bridge-completion rates against same-length terms and scrambled
  controls;
- report multiple-testing correction across the declared bridge search space.

## Read

A bridge-completion row is interesting because it says a hidden path spans the
canonical/apocrypha boundary under a declared textual ordering. It is not by
itself evidence of significance. The final report should call out that the
event exists, show the exact letters and surface context, and then separately
state how common comparable bridge completions are in controls.
