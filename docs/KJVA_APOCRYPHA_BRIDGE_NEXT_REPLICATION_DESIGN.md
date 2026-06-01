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
- [Project Gutenberg eBook 30](https://www.gutenberg.org/ebooks/30) plus
  [Project Gutenberg eBook 124](https://www.gutenberg.org/ebooks/124):
  public-domain-USA split KJV plus Apocrypha/deuterocanon candidate. Current
  tracked metadata audit found one KJV-complete component, one
  Apocrypha/deuterocanon component, and one split KJV+Apocrypha metadata
  candidate: `docs/KJVA_GUTENBERG_CANDIDATE_SOURCE_AUDIT.md`. Current
  heading-level coverage probe found all 66 KJV book headings in eBook 30, all
  14 tracked KJVA Apocrypha/deuterocanon coverage rows in eBook 124, and one
  extra Epistle of Jeremiah source heading, while also recording mixed
  Apocrypha/deuterocanon verse-marker shapes that still need collation:
  `docs/KJVA_GUTENBERG_BOOK_COVERAGE_PROBE.md`. Current source-lock prep found
  exact verse-count agreement for all 66 KJV books and 12 of 14 tracked
  Apocrypha/deuterocanon books after rolling the separate Epistle of Jeremiah
  source section into Baruch; Sirach and Prayer of Manasseh still need
  count-drift decisions before any source lock:
  `docs/KJVA_GUTENBERG_SOURCE_LOCK_PREP.md`. Current decision packet
  recommends Gutenberg source order for a future independent Project Gutenberg
  replication stream, rolling Epistle of Jeremiah into BAR for KJVA code
  compatibility, and blocking source lock until Sirach and Prayer of Manasseh
  have citable non-text collation decisions:
  `docs/KJVA_GUTENBERG_SOURCE_LOCK_DECISION_PACKET.md`. Current blocker
  packet narrows the remaining source-lock blockers to a Sirach marker-only
  gap at `SIR 44:23` and a detected Prayer of Manasseh source section with 0
  body markers against 15 local markers:
  `docs/KJVA_GUTENBERG_SOURCE_LOCK_BLOCKER_PACKET.md`. Current Hakkaac
  boundary-candidate audit found visible markers for Sirach 44:23 and Prayer
  of Manasseh 1..15 with a public-domain note, but keeps that as candidate
  evidence only, not a source lock:
  `docs/KJVA_HAKKAAC_APOCRYPHA_BOUNDARY_CANDIDATE.md`. Current Hakkaac
  full-marker coverage audit found exact marker-count agreement for all 14
  tracked Apocrypha/deuterocanon books, 5720 source markers, 5720 local
  markers, 173 chapter rows, and 0 chapter drift rows, but keeps that as
  marker-coverage evidence only, not a source lock:
  `docs/KJVA_HAKKAAC_APOCRYPHA_MARKER_COVERAGE.md`.
- [CrossWire GitLab KJV/KJVA](https://gitlab.com/crosswire-bible-society/kjv):
  possible independent metadata candidate because KJVA/KJVDC path names are
  present. Current tracked status audit:
  `docs/KJVA_CROSSWIRE_CANDIDATE_SOURCE_AUDIT.md`.
- [Wikisource 1911 Ballantyne printing](https://en.wikisource.org/wiki/The_Holy_Bible,_containing_the_Old_%26_New_Testament_%26_the_Apocrypha):
  public-domain-in-US page for a KJV Bible with Apocrypha, stating the text
  follows the standard 1769 version but without the repo's verse-numbered
  import/collation. Current tracked status audit:
  `docs/KJVA_WIKISOURCE_CANDIDATE_SOURCE_AUDIT.md`. Current book-coverage
  probe found 36 existing KJV book links, 30 KJV redlinks, and 0
  apocrypha/deuterocanon book links on the parsed main-page book table:
  `docs/KJVA_WIKISOURCE_BOOK_COVERAGE_PROBE.md`.
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
- `docs/KJVA_WIKISOURCE_BOOK_COVERAGE_PROBE.md`
- `docs/KJVA_GUTENBERG_SOURCE_LOCK_PREP.md`
- `docs/KJVA_GUTENBERG_SOURCE_LOCK_DECISION_PACKET.md`
- `docs/KJVA_GUTENBERG_SOURCE_LOCK_BLOCKER_PACKET.md`
- `docs/KJVA_HAKKAAC_APOCRYPHA_BOUNDARY_CANDIDATE.md`
- `docs/KJVA_HAKKAAC_APOCRYPHA_MARKER_COVERAGE.md`
- `docs/KJVA_OPEN_BIBLES_CANDIDATE_SOURCE_AUDIT.md`
- `docs/KJVA_WIKISOURCE_CANDIDATE_SOURCE_AUDIT.md`
- `configs/prospective_study_lanes.json`
