# KJVA Apocrypha Bridge Next Replication Design

Status: planning document only. This is not a result report.

The completed KJVA prospective bridge lane is negative under its registered
controls. It reviewed 7 registered terms, found 1 observed `tobit` bridge row,
found 0 terms with BH `q_ge <= 0.05`, found 0 terms above every shuffled sample,
and had 1 of 3 non-Bible controls at or above the observed total. No KJVA
apocrypha bridge claim language is supported by current controls.

## Boundary

- Current KJVA bridge outputs remain review material, not claims.
- The completed KJVA lane must not be rebranded as a new prospective discovery.
- Do not run a result-bearing KJVA replication until a new study-lock manifest
  and preflight sidecar exist.
- A future replication must use a fresh term/source target set before seeing new
  output.

## Recommended Design

Use this order if KJVA bridge work resumes.

1. Source lock: choose the exact KJVA/apocrypha source stream and book order.
   If no lawful independent source is available, keep this lane as planning
   only.
2. Term lock: build a fresh proper-name or thematic term list from rules stated
   before the run. Exclude terms used in the post-screen confirmatory and
   completed prospective bridge lanes.
3. Leakage audit: document that every registered term is new against prior KJVA
   bridge term files and prior result-bearing outputs.
4. Candidate rule: count only ELS paths that cross the declared
   canonical/apocrypha boundary under fixed skip, direction, and minimum-length
   settings.
5. Controls: run shuffled apocrypha-block controls and same-length non-Bible
   insertion controls at the same boundary.
6. Correction: use Benjamini-Hochberg correction across all registered terms.
7. Promotion gate: a future row must survive corrected shuffled controls and
   must not be matched or exceeded by the non-Bible insertion controls before it
   can leave review status.

## Source Candidate Scan

Current rollup: `docs/KJVA_SOURCE_CANDIDATE_STATUS.md`.

Current local source inventory has only `configs/example_ebible_engkjv_apocrypha.toml`
for KJVA/apocrypha bridge work. That source comes from eBible's public-domain
King James Version + Apocrypha USFM family, so it is usable for reruns but is
not an independent replication source.

Online source candidates found for possible future audit:

- [eBible King James Version + Apocrypha](https://ebible.org/details.php?id=eng-kjv):
  public-domain KJV + Apocrypha source with USFM and other downloads. This is
  the current source family, not an independent local witness.
- [Wikisource 1911 Ballantyne printing](https://en.wikisource.org/wiki/The_Holy_Bible,_containing_the_Old_%26_New_Testament_%26_the_Apocrypha):
  public-domain-in-US page for a KJV Bible with Apocrypha, stating the text
  follows the standard 1769 version but without the repo's verse-numbered
  import/collation. Current tracked status audit:
  `docs/KJVA_WIKISOURCE_CANDIDATE_SOURCE_AUDIT.md`.
- [`seven1m/open-bibles` KJV OSIS](https://github.com/seven1m/open-bibles):
  public-domain KJV OSIS listing. Current tracked status audit found KJV OSIS
  metadata but no apocrypha/deuterocanon path markers, so this remains KJV-only
  for KJVA bridge purposes: `docs/KJVA_OPEN_BIBLES_CANDIDATE_SOURCE_AUDIT.md`.

None of these candidates is locked for result-bearing replication until it has
a source audit, checksum, verse mapping, book-order decision, and study-lock
sidecar.

## Not Allowed

- No reuse of the completed 7-term prospective lane as a fresh discovery.
- No reuse of post-screen bridge terms as fresh prospective terms.
- No claim wording from the single observed `tobit` bridge row.
- No significance wording from raw bridge counts alone.
- No source-order or term-list changes after seeing output.

## Current Evidence Links

- `terms/kjv_apocrypha_bridge_prospective_terms.csv`
- `reports/kjv_apocrypha_bridge_prospective/bridge_candidates.csv`
- `reports/kjv_apocrypha_bridge_prospective/term_summary.csv`
- `reports/kjv_apocrypha_bridge_prospective_nonbible_controls/control_summary.csv`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CANDIDATES.md`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md`
- `docs/KJVA_SOURCE_CANDIDATE_STATUS.md`
- `docs/KJVA_OPEN_BIBLES_CANDIDATE_SOURCE_AUDIT.md`
- `docs/KJVA_WIKISOURCE_CANDIDATE_SOURCE_AUDIT.md`
- `configs/prospective_study_lanes.json`
