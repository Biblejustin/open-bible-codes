# Consolidated Findings

This is the current plain-English read across the public baseline, focused target reports, pair controls, extension review, synthetic controls, broad skip `2..100`, and wide focus skip `2..250` screening runs.

## Bottom Line

The toolkit is ready for serious screening work, but no current result should be treated as a public claim.

Claim tracking is now explicit in `claims/claim_catalog.csv` and summarized in
`docs/CLAIM_CATALOG.md`. The catalog separates reproducible sanity checks,
controlled review candidates, negative runs, and under-specified public/media
claims.

The strongest repeated lesson is methodological:

- raw ELS counts are easy to generate;
- short terms and abbreviations dominate;
- wider skip ranges raise counts predictably;
- same-passage/context filters make review queues smaller;
- matched controls often explain the interesting-looking rows.

Final-report framing should keep two axes separate:

- occurrence/context: hidden term centered on itself or on a relevant surface
  word;
- frequency/control strength: whether that occurrence is unusual against
  matched Bible and non-Bible controls.

Low frequency rank should be reported, but it should not erase a centered-self
or relevant-centered occurrence from the findings list.

The occurrence-first artifact for this layer is
`docs/CENTERED_OCCURRENCE_INDEX.md`; its CSV keeps frequency/control reads
beside each occurrence instead of using them as a deletion filter.

Current centered-occurrence snapshot:

- 812 unique term-center presence rows.
- 809 Bible presence rows and 3 control presence rows.
- 923 raw occurrence rows before presence grouping.
- 839 Bible occurrence rows and 84 control occurrence rows.
- 526 `centered_self_exact_word` presence rows.
- Bridge-context additions contribute 28 LXX and 193 KJVA apocrypha/deuterocanon
  bridge presence rows.
- The top presence row is Greek `γωγ` (Gog; English: Gog) centered on open
  `Gog` at Rev 20:8 across BYZ_NT, SBLGNT, TCG_NT, and TR_NT. It remains frequency-cautioned:
  all 24 matched length-3 non-target controls had more exact-center paths than
  `γωγ` (Gog; English: Gog).

Apocrypha/deuterocanon bridge-completion now has an expanded shuffled-control
read. LXX bridge rows are reproducible but do not stand out under 100 shuffled
apocrypha-block samples: 36 to 73 shuffled rows, with 16 samples at or above
the 62 observed rows (`p_ge=0.168317`). KJVA bridge rows remain a stronger
follow-up candidate under an expanded 250-sample version of the same control
shape: 149 to 236 shuffled rows against 350 observed rows (`p_ge=0.003984`).
The KJVA term-level bridge review found 48 of 81 bridge terms above all three
same-length non-Bible term controls and 53 terms with a center/span context
bucket beyond hidden-path-only. A 1000-sample term-level shuffled control found
8 of 81 terms above every shuffled sample, 25 terms with unadjusted
`p_ge <= 0.05`, and 15 terms with Benjamini-Hochberg `q_ge <= 0.05`.
The locked 5000-sample post-screen confirmatory follow-up over those 15 terms
found all 15 with Benjamini-Hochberg `q_ge <= 0.01`, and 3 terms stood above
every shuffled sample.
Neither result is public-claim evidence.

Clean-lock follow-up lanes added after earlier evidence rows were excluded did
not produce claim-ready material. Hebrew concordance words produced 87
uncorrected-only representative-control prompts and 0 adjusted-support terms.
The audit buckets those prompts as 38 ordinary lexical prompts, 33
proper-name/gloss prompts, 10 high-volume short-string/common-letter prompts, 5
sparse all-source prompts, and 1 control-artifact prompt. Greek surface new
terms produced 5 controlled rows with `q <= 0.05`, but manual context review
found visible local surface-context or direct self-lexeme effects. The strict
follow-up gate leaves 0 Hebrew concordance rows and 0 Greek surface rows as
claim-ready from these clean-lock queues.

## What Looks Weak

### Modern Names And Geopolitical Terms

Most modern terms do not produce meaningful-looking results under current controls.

- `Trump`: present but low/modest; not unusual under controls.
- `Vance`: higher because the form is short; not unusual under controls.
- `Netanyahu`: Hebrew MT-family only and low; Greek form absent.
- `Iran`: high in Greek because `ιραν` (iran; English: Iran) is a 4-letter
  form; paired controls read not unusual.
- `Russia`, `Europe`, `Turkey`, `Germany`: present at low to moderate levels, with no robust control-backed signal.
- Full phrases such as United States, United Nations, European Union, Cowboy Catering, Simsberry, and Simscorner are absent or effectively absent.
- Abbreviations such as USA and United Nations are extremely high, but they are short-form density effects.
- Same-skip extension screening for modern/local terms found only ordinary
  biblical phrases or transliteration collisions in the top phrase rows.

### Gog / Magog

Gog/Magog remains theologically interesting, but the locked Hebrew prospective
pair-control result is negative.

- Raw `Gog` is dense because it is short.
- `Magog` is less dense but still present.
- Same-chapter and same-signed-skip filters reduce the review queue.
- MT_WLC Gog/Magog produced 193 strict close pairs and 189 strict overlaps, but
  its adjusted pair-control read was `not_unusual`.
- UHB Gog/Magog produced 198 strict close pairs and 194 strict overlaps, but
  its adjusted pair-control read was also `not_unusual`.
- Hebrew Beast/Dragon exceeds Gog/Magog in strict observed close-pair counts.
- Synthetic 3+4 Hebrew pairs often match or exceed Gog/Magog close-pair
  density: 73 of 100 synthetic samples met or exceeded the Gog/Magog close-pair
  count in both MT_WLC and UHB.

Current read: the Hebrew prospective pair lane produced no
`prospective_controlled_review_candidate`. Keep Gog/Magog as exploratory only,
not evidential. The Greek Rev 20:8 `γωγ` (Gog; English: Gog) row is still a real source-stable
centered-self occurrence in a direct Gog/Magog verse, so it belongs in the final
occurrence list. It is not frequency-promoted because of the length-3 control
result.

### Broad Skip `2..100` Search

The broader run did not change the conclusion.

- 11 term sets, 10 corpora, skip `2..100`, direction both.
- 5,375 output rows.
- Runtime: 20.650s through `protocols/broad_search.toml`.
- Hebrew now includes five MT-family streams: OSHB WLC direct word tokens,
  UXLC ketiv, MAM, eBible WLC as a packaging check, and UHB as a derived
  MT-family comparison stream.
- Count increases versus skip `2..50` are mostly about 2x, which is expected.
- Top length 4+ rows are still dense short forms like `ναοσ` (naos; English:
  temple), `νατο` (nato; English: NATO), `υιοσ` (huios; English: son),
  `αιμα` (haima; English: blood), `יהוה` (YHWH; English: YHWH), and
  `ιραν` (iran; English: Iran).
- Null controls also produce high counts, including scrambled YHWH at 22,293
  MAM hits, 22,277 MT_WLC hits, 22,271 EBIBLE_WLC hits, 22,269 UXLC hits, and
  22,204 UHB hits.

Current read: broad search is useful for queue-building, not for claims.

### Wide Focus Skip `2..250` Search

The focused wide run also did not change the conclusion.

- 2 focused term sets: `modern_names_dates` and `prophetic_terms`.
- 10 corpora, skip `2..250`, direction both.
- 2,365 output rows.
- Count-step runtime observed: 40.327s through
  `protocols/wide_focus_search.toml`.
- Count increases versus skip `2..50` are mostly about 5x, which is expected.
- Top length 4+ rows remain dense short forms such as Greek `νατο` (nato;
  English: NATO), `αιμα` (haima; English: blood), `κινα` (kina; English:
  China), `ιραν` (iran; English: Iran), and Hebrew `רומי` (Romi; English:
  Rome/Roman).
- Full phrases such as United States, United States of America, United
  Nations, European Union, Cowboy Catering, Catering, and Simscorner remain
  absent in observed Hebrew and Greek corpora.
- `Simsberry` produced one MAM-only Hebrew broad-count hit and zero hits in the
  other observed Hebrew and Greek corpora. Treat this as source-specific
  review noise unless it survives exact-hit review and controls.
- Abbreviations such as United Nations and USA remain extremely high, but they
  are short-form density effects.

Current read: widening skip range helps find review queues, but it mostly
scales short-form noise. It does not make modern/local/geopolitical rows
claim-ready.

### Full-Span Dynamic Follow-Up

The full-span dense export is now complete for the selected dynamic-focus
rows. This uses the broadest requested skip cap: corpus letters divided by
term letters, in both directions.

- 13,646 planned partition outputs completed and summarized.
- 147 dense corpus/term rows completed.
- 13,556,483,793 exported full-span hit rows summarized from manifests.
- 0 partial dense rows remain.
- Dense payloads are archived off local disk under the external-drive archive,
  with local archive markers preserved for reproducibility.
- Exact center-word and example extraction are not computed in this manifest
  summary because scanning 13.56B dense hit rows would be a separate heavy
  pass.

The full-span Bible-control comparison is tracked in
`docs/DYNAMIC_SKIP_BIBLE_CONTROL_COMPARISON.md`.

- 76 normalized Bible-vs-control comparison rows.
- 24 rows have Bible max rate above all observed language-matched controls.
- 4 rows exceed the control median but not the control max.
- 48 rows have a control background equal to or above the Bible max rate.
- Stronger-looking rows include Greek/English `Netanyahu`, Greek `Jesus`,
  Greek `Vance`, Greek `Magog`, Hebrew `Iran`, Greek `Russia`, Greek `Gog`,
  Hebrew `Yeshua`, and Hebrew `Messiah`.
- Several high-volume rows remain control-background rows, including Hebrew
  `Gog`, Hebrew `Magog`, Hebrew/Greek/English `Trump`, Hebrew `Russia`,
  English `Gog`, English `Iran`, and Greek `Iran`.

Current full-span read: full-span search confirms that raw hit volume scales
massively as the skip cap expands. Some rows beat the observed controls by
normalized rate and deserve review queues, but the general pattern still
supports caution: non-Bible controls often match or exceed Bible rates, and
short dense forms dominate.

The targeted exact-center follow-up for those Bible-over-control full-span
rows is tracked in `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_FINDINGS.md`
and `docs/DYNAMIC_SKIP_STRONG_MANAGEABLE_FULL_SPAN_HIT_EXPORT.md`. The
control-side comparison is tracked in
`docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_COMPARISON.md`. A row-level
exact-center export is tracked in
`docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ROWS.md`. The current synthesis
is tracked in
`docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_SYNTHESIS.md`.

- Dense strong subset: 42 archived partitions scanned directly, covering
  36,280,786 hit rows from 8 dense corpus/term rows.
- Dense exact center-word hits: 1,582.
- Exact center-word hits by dense row: UHB `Yeshua` 941, KJV `Jesus` 492,
  EBIBLE_WLC `Messiah` 75, LXX `Jesus` 70, TCG_NT `Gog` 4, and zero for LXX
  `Russia`, LXX `Vance`, and UXLC `Iran`.
- Manageable strong subset: 4 low-hit rows exported directly, covering 3,301
  hit rows.
- Manageable exact center-word hits: zero for KJV `Netanyahu`, TR_NT
  `Netanyahu`, KJV `Simsberry`, and TCG_NT `Magog`.
- Control comparison: Hebrew `Messiah` exact-center rate is higher in the
  Bialik control than in EBIBLE_WLC; Hebrew `Yeshua`, English `Jesus`, Greek
  `Jesus`, and Greek `Gog` remain higher in the Bible rows by this exact-center
  flag.
- Row-level export: 365 partition sources plus 2 manageable hit files scanned
  356,494,786 hit rows and exported 9,794 exact center-word rows. The export
  preserves `center_source`, `center_word_index`, and offsets so non-Bible
  source-level refs can still be traced locally.
- Review queue: `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_REVIEW_QUEUE.md`
  condenses those paths into 537 centered surface-word review units: 453 Bible
  units and 84 control units.
- Context excerpts: `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_CONTEXT.md`
  adds readable center/start/end text for all 537 review units: 453 Bible units
  and 84 control units.
- Same-skip extension scan:
  `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_EXTENSIONS.md` checks the
  1,582 Bible exact-center paths for adjacent same-skip words or phrases. It
  found 2,093 raw extension rows, 38 phrase-filtered summary groups, and 5
  stronger term-plus-adjacent phrase rows, all in KJV `Jesus` rows.
- Control same-skip extension scan:
  `docs/DYNAMIC_SKIP_STRONG_CONTROL_FULL_SPAN_EXACT_CENTER_EXTENSIONS.md`
  checks the 8,212 control exact-center paths. It found 37,878 raw extension
  rows, 3,274 phrase-filtered summary groups, and 50 strong phrase rows in
  HEB_PBY_BIALIK, while ENG_PG_SHAKESPEARE had no phrase-summary groups.
- Matrix export:
  `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_MATRIX.md` exports row/column
  letter paths for all 9,794 exact-center paths: 1,582 Bible paths with 6,956
  letter rows, and 8,212 control paths with 32,850 letter rows.
- Review bundle:
  `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_REVIEW_BUNDLE.md` joins the
  537 review units with context, strong-extension flags, and matrix path counts
  into one manual-review queue. It flags 43 units with strong extension rows:
  5 Bible units and 38 control units.
- Original-language review:
  `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ORIGINAL_LANGUAGE_FINDINGS.md`
  ranks the Hebrew/Greek subset. It flags Greek `Gog` at Rev 20:8 for
  deeper review, holds LXX `Jesus/Joshua` rows for referent discipline, and
  treats Hebrew `Yeshua`/`Messiah` rows as background-pressure rows because
  Bialik controls also produce exact-center rows.
- Gog source follow-up:
  `docs/DYNAMIC_SKIP_GOG_PROMOTED_EXACT_CENTER_SOURCE_REVIEW.md` checks Greek
  `γωγ` (Gog; English: Gog) directly across TR_NT, BYZ_NT, TCG_NT, and SBLGNT. All four sources
  have open `Gog` at Rev 20:8 and exact-center hidden paths. That makes it a
  source-stable centered-self occurrence in the Gog/Magog verse. It is still
  not a claim by itself because the term is only three letters, and the open
  surface word supplies the center anchor.
- Gog matched length-3 controls:
  `docs/DYNAMIC_SKIP_GOG_LENGTH3_SURFACE_CONTROL_REVIEW.md` compares `γωγ` (Gog; English: Gog)
  against normalized Greek length-3 surface words that occur exactly once in
  every compared Greek NT source. The matched universe has 25 terms including
  `γωγ` (Gog; English: Gog); all 24 non-target controls have more exact-center
  paths than `γωγ` (Gog; English: Gog).
  This does not remove the Rev 20:8 Gog row from the final findings list; it
  says the row is contextually meaningful but not frequency-promoted.

Current exact-center read: exact center-word matches do occur in the stronger
full-span queue, especially for terms that also occur plainly in the corpus
surface text. This is meaningful as a review flag, but it is not a standalone
claim test because the candidate set was selected after a broad screen and
because exact-center hits can be driven by ordinary surface vocabulary.

The CRD self-surface and concept-surface broad screens add a separate
centered-relevance view over the fixed `skip_range = 2..100` corpus set. The
self-surface rerun found 1,629,913 classified hit rows and 9,318 relevant
rows. The strict exact `center_word` subset contains 1,153 Bible rows across
154 term IDs, 87 distinct normalized surface forms, and 496 distinct normalized
surface hit paths. Its center-word-only Bible-vs-control summary has 141 terms
exceeding the secular maximum, including 114 Bible-positive/secular-zero terms.
Version presence is mixed rather than all-or-nothing: 63 exact center-word
terms appear in five Bible corpus labels, while 60 appear in only one.
The concept-surface run has the same 1,153 Bible exact center-word row keys;
concept expansion changed only two secular-control center-word max rows and
changed zero exact center-word exceedance decisions. Therefore exact
center-word review can use the self-surface packet without losing
concept-surface Bible rows, while broader center-verse/span relevance should
remain reported separately.

The ChurchAges statistics audit is tracked in
`reports/churchages_statistics/audit.md`.

- `branham` forward: observed 655 vs ChurchAges-style expected 639.705853.
- `branham` backward: observed 612 vs ChurchAges-style expected 639.705853.
- `statist` forward: observed 11,947 vs ChurchAges-style expected
  12,298.959594.

Current ChurchAges read: the published raw count volumes are close to
independent-letter density expectations. That addresses the count-density
claim, not theological meaning or post-hoc cluster selection.

Tracked summary: `docs/WIDE_FOCUS_SEARCH.md`.

The exact-hit follow-up for the same focused row family is tracked in
`docs/WIDE_FOCUS_EXACT_PRESENCE.md`.

- Hebrew exact-hit run: 26 summarized length 4+ terms, 9,691 capped hit
  records, 2,648 exact pattern rows.
- Greek exact-hit run: 24 summarized length 4+ terms, 5,785 capped hit
  records, 3,287 exact pattern rows.
- Hebrew long phrases still absent: United States, United States of America,
  United Nations, European Union, Cowboy Catering, Catering, Simscorner,
  Donald Trump, and Confederacy.
- Greek long/local forms still absent: United States, United States of America,
  United Nations, European Union, Cowboy Catering, Catering, Simsberry,
  Simscorner, Germany, Netanyahu, and Confederacy.
- `Simsberry` remains a one-row MAM-only Hebrew finding.
- Greek multi-source rows are mostly NT-family rows; zero Greek patterns were
  present across the mixed LXX + NT source set.

Representative paired controls for nonzero wide-focus rows are tracked in
`docs/WIDE_FOCUS_PAIRED_CONTROLS.md`.

- 66 representative rows controlled across MT_WLC, UHB, LXX, TR_NT, and
  SBLGNT.
- 63 rows read `not_unusual`.
- 3 rows crossed only the uncorrected p <= 0.05 screen: `TR_NT trump_g`,
  `LXX trump_g`, and `UHB turkey_h`.
- All three had corrected q = `0.780529`, so there is no adjusted paired-control
  support.

### Modern Same-Skip Extensions

The first capped modern extension screen is tracked in
`docs/MODERN_EXTENSION_SCREEN.md`.

It checked whether same-interval letters before/after modern-name hits formed
any surface word or short phrase in the same corpus. The top phrase rows were
not modern-message evidence:

- `ישראל` (Yisrael; English: Israel) / `ισραηλ` (Israel; English: Israel)
  extended into ordinary biblical Israel phrases;
- `מצרימ` (Mitzrayim; English: Egypt/Egyptians) matched an unrelated normalized
  Hebrew phrase, not Egypt;
- Greek `Harris` collided with `χαρις` (charis; English: grace);
- Cowboy Catering, Simsberry, and Simscorner did not produce meaningful
  phrase-extension rows.

Current read: extension scanning is useful for review queues, but the modern
rows remain weak.

The bounded version-presence extension screen is tracked in
`docs/VERSION_PRESENCE_EXTENSION_SCREEN.md`.

It exported all-source Hebrew and Greek version-presence rows into ordinary hit
rows, then checked same-skip letters before and after those hits against
surface word/phrase lexicons in MT_WLC, UHB, TR_NT, and SBLGNT. It found some
standalone before-only and after-only phrase matches, but no strong
`before_plus_term`, `term_plus_after`, or `before_plus_term_plus_after` top rows
under the strict phrase filter.

Current read: the generalized extension bridge works, but this bounded
all-source sample does not produce a stronger compound-word or phrase finding.

The relaxed all-codes follow-up is tracked across
`docs/ALL_CODES_FOLLOWUP_SELECTION.md`,
`docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md`,
`docs/ALL_CODES_FOLLOWUP_CONTEXT.md`,
`docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md`,
`docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md`,
`docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md`, and
`docs/ALL_CODES_FOLLOWUP_REVIEW.md`.

It deliberately keeps hidden-path-only rows visible while also flagging rows
with same-center-word, related surface context, and same-skip before/after
extensions:

- 59 selected follow-up rows from Hebrew theology, broader Hebrew screening,
  and broader Greek screening queues;
- 274 reconstructed path rows and 1,264 hidden-letter audit rows;
- 0 reconstructed sequence mismatches;
- 52 selected rows with at least one same-skip before/after surface extension;
- 8 selected rows with compound same-skip extensions containing the hidden term
  plus adjacent letters;
- 43 deduped compound-extension rows with 250/250 row-local paired controls:
  by min-q screen, 14 rows are q <= 0.05, 7 additional rows are q <= 0.10,
  and 22 are not unusual; by conservative all-control q, 0 rows are q <= 0.05
  and 2 rows are q <= 0.10.
- 5 locked confirmatory rows for the selected `יום יהוה` (yom YHWH; English:
  day of YHWH) -> `היומיהוה` (hayom YHWH; English: the day of YHWH)
  same-skip extension key across EBIBLE_WLC, MAM, MT_WLC, UHB, and UXLC with
  5000 term controls and 5000 random controls per row; all five have
  conservative all-control q = 0.003599.

Current all-codes read: the extension and context exports are useful review
filters, especially for compound rows such as `עדיהוה` (ad YHWH; English:
compound hidden sequence involving YHWH), `אדניאמר` (Adonai amar; English:
the Lord said), and `היומיהוה` (hayom YHWH; English: the day of YHWH). The
confirmatory control run makes the selected `יום יהוה` (yom YHWH; English:
day of YHWH) compound-extension row stronger as a review candidate, but it remains
post-discovery review material, not claim evidence, because the candidate came
from a broad prior queue.

The targeted version-presence join is tracked in
`docs/TARGETED_VERSION_PRESENCE_REVIEW.md`.

It joins the requested modern/geopolitical/local rows against the broader
Hebrew and Greek exact-version matrices, available paired controls, and the
bounded version-presence extension summaries:

- 59 target rows: 31 Hebrew and 28 Greek;
- 25 rows with all-source exact patterns;
- 31 rows absent or unsummarized in the capped exact-version matrix;
- 21 rows with paired controls available;
- 54 representative `2..100` paired-control rows;
- 53 of those representative rows reading `not_unusual`;
- 28 target terms with representative controls joined into the final controlled
  table;
- 0 rows with strong plus-term extension top rows.

Current targeted read: some short forms are stable across source streams, but
paired controls still do not support a claim. The lone representative
uncorrected row was `UHB germany_h` with adjusted q = `1.0`. Longer phrase and
local rows such as United States, United Nations, European Union, Cowboy
Catering, Simsberry, and Simscorner remain absent in the capped exact-version
screen.

The broader Hebrew modern/geopolitical controlled review is tracked in
`docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_REVIEW.md`.

It takes the all-Hebrew-row modern/geopolitical MT-family version-presence run
and runs representative MT_WLC/UHB paired controls for nonzero rows:

- 73 target rows from `terms/modern_names_dates.csv`;
- 54 rows with representative controls;
- 108 representative control-target rows;
- 50 controlled rows reading `not_unusual`;
- 4 rows clearing only an uncorrected p<=0.05 screen;
- 0 rows with adjusted representative-control support.

Current broad modern/geopolitical controlled read: the same short-form
version-stable rows remain review material only. The controlled follow-up does
not promote any modern/geopolitical/local row to claim status.

The broader Hebrew screening controlled review is tracked in
`docs/HEBREW_SCREENING_CONTROLLED_REVIEW.md` with a concise read in
`docs/HEBREW_SCREENING_CONTROLLED_FINDINGS.md`.

It expands the representative-control pass to the broader Hebrew screening term
set:

- 417 target rows;
- 306 terms with representative controls;
- 610 representative control-target rows;
- 295 controlled rows reading `not_unusual`;
- 11 rows clearing only an uncorrected p<=0.05 screen;
- 0 rows with adjusted representative-control support.

Current broader screening controlled read: the broader row set confirms the
same pattern. Stable short-form ELS rows are common, but representative paired
controls do not promote any row to claim status.

## What Still Deserves Review

### Version-Presence Framing

Not every pattern should be expected in every textual source. The more useful
question is which exact pattern appears in which source.

The Hebrew exact-hit MT-family matrix now applies that rule to modern/local
Hebrew terms across MT_WLC, UXLC, EBIBLE_WLC, MAM, and UHB:

- 1,202 exact ref-key pattern rows in the capped run;
- 749 patterns present in all observed Hebrew sources;
- 187 more patterns stable across the three Leningrad-family streams;
- 244 source-specific patterns.

Current Hebrew read: many short transliterated modern forms are stable across
MT-family streams, but this mostly reflects shared consonantal density. It does
not make modern-name claims stronger. Longer phrase/local rows such as United
States, United Nations, European Union, Cowboy Catering, Simsberry, and
Simscorner remain absent in the capped screen.

Tracked summary: `docs/HEBREW_HIT_VERSION_PRESENCE.md`.

An optional STEP/Tyndale `TAHOT` selected Hebrew stream is now available for
separate source-family survival review. It is not part of the Leningrad-family
label because its upstream header says the selected text may follow qere,
restore missing text, and include LXX-preserved additions converted to Hebrew.

Current STEP_TAHOT focused read:

- 39 books, 23,261 verses, and 1,197,732 normalized letters loaded.
- Against MT_WLC, 23,011 refs aligned; 20,037 were equal and 2,974 differed.
- In the focused modern/local exact-hit pass, 961 of 1,236 pattern rows included
  STEP_TAHOT, and 34 rows were STEP_TAHOT-only.
- In the broader Hebrew screening pass, 12,084 of 15,478 pattern rows included
  STEP_TAHOT, and 379 rows were STEP_TAHOT-only.
- The STEP_TAHOT-only policy audit found 80 of those 379 rows touch `Q`, `R`,
  or `X` words on the ELS letter path; the other 299 are L-only paths but can
  still be source-specific because selected readings shift the global stream.
- Full phrases such as United States, United Nations, European Union, Cowboy
  Catering, Simsberry, and Simscorner remained absent in the capped scan.

Tracked summaries: `docs/STEP_TAHOT_SOURCE_AUDIT.md`,
`docs/STEP_TAHOT_VERSION_PRESENCE_REVIEW.md`, and
`docs/STEP_TAHOT_SCREENING_VERSION_PRESENCE.md`. Source-policy audit:
`docs/STEP_TAHOT_POLICY_HIT_AUDIT.md`.

The broader Hebrew screening matrix extends the same exact-hit check to Hebrew
rows from theological, modern, Table of Nations, prophetic, Hebrew claim, tribe,
festival, and calendar term files:

- 557 selected Hebrew rows, 417 summarized after length filtering;
- 60,630 capped hit records;
- 15,099 exact ref-key pattern rows;
- 9,432 all-source rows;
- 2,166 Leningrad-family rows;
- 2,600 source-specific rows, mostly `UHB` and `MAM`.

Current broader Hebrew read: the same pattern holds at larger scale. Short forms
dominate exact all-source stability, and longer modern/local phrases such as
United States, United Nations, European Union, Cowboy Catering, Simsberry, and
Simscorner remain absent.

Tracked summary: `docs/HEBREW_SCREENING_VERSION_PRESENCE.md`.

The broad Hebrew modern/geopolitical run applies the exact same MT-family
version-distribution method to every Hebrew row in `terms/modern_names_dates.csv`:

- 82 declared Hebrew modern/geopolitical/local/date rows;
- 73 rows summarized after the minimum-length filter;
- 29,835 capped hit records;
- 7,567 exact ref-key pattern rows;
- 4,612 patterns present in all observed Hebrew sources;
- 1,260 more patterns stable across the three Leningrad-family streams;
- 1,577 source-specific patterns.

Current modern/geopolitical read: short strings and biblical/common-word
collisions dominate stable rows. `USA` abbreviation, Vance, Iran, France,
Russia, Netanyahu, Europe, Germany, Trump, and Cowboy have detected rows where
present. Longer phrase rows such as United States, United States of America,
United Nations, European Union, Confederacy, Cowboy Catering, Simsberry, and
Simscorner remain absent in this capped exact-version scan.

Tracked summary: `docs/HEBREW_MODERN_GEOPOLITICAL_VERSION_PRESENCE.md`.

The compiled Hebrew claim-term matrix gives the same read at larger scale:

- 143 declared Hebrew claim terms;
- 22,811 capped hit records;
- 5,603 exact ref-key pattern rows;
- 3,635 patterns present in all observed Hebrew sources;
- 798 more patterns stable across the three Leningrad-family streams;
- 956 source-specific patterns;
- 50 summarized terms with no hits.

Current claim-term read: short forms such as `משיח` (Mashiach; English:
Messiah/anointed one), `ישוע` (Yeshua; English: Yeshua/Jeshua), `רמבמ` (Rambam;
English: Maimonides), `יהוה` (YHWH; English: YHWH),
`תורה` (Torah; English: Torah), and `נביא` (navi; English: prophet) are
stable and dense. Longer phrases are often sparse or
absent. That supports version-distribution review, not significance.

Tracked summary: `docs/HEBREW_CLAIM_VERSION_PRESENCE.md`.

The Hebrew control version-presence matrix reinforces that caution:

- 23 declared Hebrew null/frequency rows;
- 13 rows summarized after the minimum-length filter;
- 981 exact ref-key pattern rows;
- 526 patterns present in all observed Hebrew sources;
- scrambled YHWH, Messiah, Torah, and Israel controls all have many stable
  all-source exact patterns.

Current control read: exact version stability is a reproducibility filter, not
a significance signal.

Tracked summary: `docs/HEBREW_CONTROL_VERSION_PRESENCE.md`.

The same control principle holds after adding `STEP_TAHOT` as a selected
sixth stream:

- 1,005 exact null/frequency control pattern rows;
- 749 rows include `STEP_TAHOT`;
- 24 rows are `STEP_TAHOT`-only;
- `STEP_TAHOT`-only control rows include scrambled YHWH, scrambled Elohim,
  scrambled Israel, scrambled Torah, and a nonsense 5-letter row.
- source-policy audit of those 24 control-only rows found 3 touching `Q` and
  21 L-only paths.

Tracked summary: `docs/STEP_TAHOT_CONTROL_VERSION_PRESENCE.md`.

The STEP_TAHOT final gate now combines the real-term and control-term
source-only reads:

- real screening rows were `STEP_TAHOT`-only at 2.449%;
- null/frequency controls were `STEP_TAHOT`-only at 2.388%;
- the real/control source-only rate ratio was 1.025;
- all 379 real `STEP_TAHOT`-only rows remain held: 80 by selected-reading
  source-policy path and 299 as L-only source-specific rows.

Tracked summary: `docs/STEP_TAHOT_FINAL_GATE.md`.

The side-by-side comparison makes that explicit: all-source exact pattern rates
are 62.3% for the modern/local focus, 60.9% for all Hebrew
modern/geopolitical rows, 64.9% for Hebrew claim terms, 53.6% for Hebrew
controls, and 62.5% for broader Hebrew screening. Controls still produce
hundreds of stable rows, so stability cannot be treated as semantic evidence.

Tracked comparison: `docs/HEBREW_VERSION_PRESENCE_COMPARISON.md`.

The source-specific breakdown also points mostly to MAM and UHB:

- modern/local source-specific rows: MAM 140, UHB 88, UXLC 9, EBIBLE_WLC 5, MT_WLC 2;
- claim-term source-specific rows: UHB 449, MAM 441, UXLC 50, EBIBLE_WLC 11, MT_WLC 5;
- control source-specific rows: UHB 74, MAM 65, UXLC 16, EBIBLE_WLC 10, MT_WLC 5.

Current source-specific read: most Hebrew version-specific behavior is MAM/UHB
behavior, not instability among the three Leningrad-family streams.

Tracked distribution: `docs/HEBREW_VERSION_SPECIFIC_DISTRIBUTION.md`.

The four-source Greek exact-center matrix now keeps that distinction visible:

- `δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ` (doxa; English: glory;
  doxanos = hidden extension form): TR_NT, BYZ_NT, TCG_NT, SBLGNT;
- `υιοσ|25|forward|before_plus_term|ουουιοσ|ουουιοσ` (huios; English: son;
  ouhuios = hidden extension form): BYZ_NT, SBLGNT;
- `αιμα|14|forward|before_plus_term_plus_after|ναιμανο|ναιμανο` (haima;
  English: blood; naimano = hidden extension form): SBLGNT only;
- `υιοσ|-46|backward|before_plus_term|ειουιοσ|ειουιοσ` (huios; English: son;
  eiouios = hidden extension form): BYZ_NT only.

Current read: source-specific rows should not be promoted, but they also should
not be discarded. They become version-specific review queues.

A current consolidated table is tracked in
`docs/GREEK_PATTERN_VERSION_SUMMARY.md`.

The reporting rule is now stated as project methodology in
`docs/VERSION_DISTRIBUTION_METHOD.md`.

The broader Greek NT exact-hit version-presence screen now applies the same
version-distribution rule outside the exact-center extension workflow:

- Greek NT claim terms: 787 exact pattern rows, 109 all-source rows, 250
  multi-source rows, and 428 source-specific rows.
- Greek controls: 826 exact pattern rows, 270 all-source rows, 237
  multi-source rows, and 319 source-specific rows.
- SBLGNT-only rows dominate the source-specific claim-term bucket with 212 rows.
- Controls have a higher all-source row rate than claim terms: 32.7% vs. 13.9%.

Current Greek exact-hit read: source/version distribution is useful, but
version stability is still not significance because controls are also stable.

Tracked summaries: `docs/GREEK_NT_CLAIM_VERSION_PRESENCE.md`,
`docs/GREEK_CONTROL_VERSION_PRESENCE.md`, and
`docs/GREEK_VERSION_PRESENCE_COMPARISON.md`.

The broader Greek screening matrix extends the exact-hit check to Greek rows
from theological, modern, Table of Nations, prophetic, Greek NT claim, tribe,
and festival term files:

- 413 selected Greek rows, 398 summarized after length filtering;
- 22,501 capped hit records;
- 11,103 exact ref-key pattern rows;
- 2,192 all-source rows;
- 3,416 multi-source rows;
- 5,495 source-specific rows, with SBLGNT-only rows largest.

Current broader Greek read: short forms such as `αραμ` (Aram; English: Aram),
`κινα` (kina; English: China), `λευι` (Leui; English: Levi), `θεοσ` (theos;
English: God), `αμην` (amen; English: amen), `ναοσ` (naos; English: temple),
`ιραν` (iran; English: Iran), `νατο` (nato; English: NATO), and `αιμα` (haima;
English: blood) dominate all-source stability. Long
modern/local phrases such as United States, United Nations, European Union,
Cowboy Catering, Simsberry, and Simscorner remain absent.

Tracked summary: `docs/GREEK_SCREENING_VERSION_PRESENCE.md`.

LXX should be handled as corpus presence, not NT version support. The broad
search shows 14 of 32 Greek NT claim terms present in LXX plus all four Greek NT
corpora, 4 present in multiple corpora, 2 LXX-only rows, and 12 absent across
the observed Greek corpus set. LXX counts are often higher because the corpus is
much larger than the NT.

Tracked read: `docs/GREEK_LXX_NT_CORPUS_PRESENCE.md`.

### Greek Exact-Center Extension Row: `δοξα` (doxa; English: glory)

The `δοξα` (doxa; English: glory) / `δοξανωσ` (doxanos; English: hidden extension form from doxa)
extension is the strongest review row so far, but still not a claim.

Why it remains interesting:

- exact-center surface context exists;
- exact extension key appears in both TR_NT and SBLGNT;
- exact extension key now also appears in BYZ_NT, the eBible GRCMT
  Robinson-Pierpont 2018 Byzantine Textform source;
- deeper 200/200 controls gave q = 0.004975 in both texts.
- deeper 1000/1000 controls gave q = 0.000999 in both texts.
- three-source 1000/1000 controls gave q = 0.001249 in TR_NT, BYZ_NT, and
  SBLGNT.
- four-source 1000/1000 controls with added TCG_NT kept the same exact key in
  TR_NT, BYZ_NT, TCG_NT, and SBLGNT with best q = 0.001332.
- the locked four-source 5000/5000 claim follow-up kept the same exact key in
  TR_NT, BYZ_NT, TCG_NT, and SBLGNT with q values from 0.0008 to 0.0016.
- the stricter locked 20000/20000 confirmatory follow-up kept the same exact
  key in all four Greek NT labels with combined q = 0.0009 in every row and
  conservative all-control q <= 0.05.

Why it remains review-level rather than a public claim:

- the full extension phrase is hidden-path only, which is a normal ELS
  candidate type rather than a failure;
- it has related surface context, but not the rarer same-span surface echo;
- same-length synthetic controls show broad any-type extension scoring can produce comparable-looking hidden phrases;
- synthetic match review showed those synthetic phrases also appear elsewhere, not in the hit span.
- the matched phrase `δόξαν ὡς` (doxan hos; English: glory as) appears at
  John 1:14 / JHN 1:14, not as surface text in the 2 Thessalonians 3:1 hit
  passage.

Current read: `δοξα` (doxa; English: glory) is a four-source claim-follow-up review candidate, not a
claim.

### Other Exact-Center Rows

The exact-center cohort also surfaced SBLGNT-only `αιμα` (haima; English:
blood) and `υιος` (huios; English: son) rows.
After adding BYZ_NT, `υιος` (huios; English: son) is no longer source-only under the locked
three-source protocol: it appears in BYZ_NT and SBLGNT with q <= 0.001998.

Current read:

- `υιος` (huios; English: son): multi-source hidden-path candidate across BYZ_NT and SBLGNT, but
  not TR_NT or TCG_NT;
- `αιμα` (haima; English: blood): source-specific hidden-path candidate;
- both remain review candidates, not claims.

## Controls Matter Most

The control work has been the most clarifying part of the project.

Useful controls now present:

- shuffled-letter controls;
- shuffled-term controls;
- same-length random controls;
- pair proximity controls;
- strict same-chapter / same-signed-skip pair filters;
- synthetic Hebrew pair baselines;
- synthetic Greek extension baselines;
- synthetic extension match context review;
- frequency anchors and null-control term lists.

These controls consistently push interpretation away from raw counts and toward review queues.

## Practical Claim Standard

Before promoting anything externally, require at least:

1. predeclared term list and skip range;
2. matched shuffled-term and same-length random controls;
3. correction across tested rows;
4. surface or passage context, not only hidden letters;
5. cross-text support when comparing TR_NT and SBLGNT;
6. synthetic/null baseline comparison;
7. saved examples and letter paths.

Under that standard, no current result is a claim yet.

The first formal report assembly plan is now tracked in
`docs/REAL_REPORT_RUN.md`. It runs preflight checks, refreshes the locked
STEP_TAHOT and Greek exact-center final gates, refreshes the locked doxa
four-source follow-up, expanded Greek surface queue, length-4 Greek surface
follow-up, generated length-4 vocabulary controls, relaxed all-codes follow-up
audits, all-codes compound-extension controls, WRR source/import audit state,
and current WRR repo-defined diagnostic status. It then builds a generated
report index and writes `reports/real_report_run/summary.md`. It does not
expand declared screening lists, widen skip ranges, or promote rows to claims.

WRR now has locked local evidence: the cap-1000 keep-all 999,999 date-label
permutation run uses the selected full source universe, observes 182 rows with
72 defined `c(w,w')` values, and reports Bonferroni `rho0 = 0.000404`. Exact
published WRR reproduction remains caveated by source-transcription limits and
the 163-distance gap. Current source-policy scenarios remain diagnostic:
baseline 165 >=5 pairs, exclude WNP Zacut 157, and exclude all source-review
flags 154. The single-term Zacut diagnostic narrows the count gap further:
`ZKWTA`, `ZKWTW`, `M$HZKWTA`, and `M$HZKWTW` each individually leave
163 >=5 pairs with gap 0 if excluded, but no source policy is selected from
that count alone.
Visual triage now separates OCR misses from title-prefix and Chelm source-rule
questions, but those notes do not exclude pairs automatically.

## Best Next Work

The most useful next work is not more raw counting. The broad search and
all-codes lanes have already produced review queues. The next useful work needs
one narrow target set, one locked rule, and controls fixed before the next
result-producing run.

Current viable choices:

- a genuinely new Greek surface prospective cohort, if a clean new term source
  is supplied;
- a true prospective compound-extension study, using a predeclared term list
  rather than rows selected from the existing all-codes queue.

Completed lanes should not be rerun as claim-oriented studies without a
materially new hypothesis or term source:

- Hebrew/modern/geopolitical source-distribution study: completed as weak or
  negative controlled review material;
- Gog/Magog prophetic-symbol pair-control study: completed as weak or negative
  controlled prospective material;
- local-term negative/curiosity appendix: completed.

The Greek surface public-claim standard is now written in
`docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md`. Use it before launching a
new result-producing surface study.

Current next target status: `docs/PROSPECTIVE_STUDY_READINESS.md` now reports
no remaining `ready_for_preflight` lane. Any further result-producing work
needs a genuinely new term/source target set and a fresh lock before running.
Avoid more raw count expansion unless the claim standard is fixed in advance.

That post-discovery follow-up design is now frozen in
`docs/DOXA_FOLLOWUP_PREREGISTRATION.md`. The first locked follow-up run is
summarized in `docs/DOXA_FOLLOWUP_REPORT.md`.

The broader Greek exact-center cohort design is now locked in
`docs/GREEK_EXACT_CENTER_COHORT_PREREGISTRATION.md`; its protocol should be run
before inspecting any new cohort results.

The locked cohort run is summarized in
`docs/GREEK_EXACT_CENTER_COHORT_REPORT.md`: it found no new controlled
cross-text candidate beyond `δοξα` (doxa; English: glory).

The weaker source-only SBLGNT follow-up for `αιμα` (haima; English: blood) and
`υιος` (huios; English: son) is locked in
`docs/SBLGNT_SOURCE_ONLY_EXACT_CENTER_PREREGISTRATION.md` and summarized in
`docs/SBLGNT_SOURCE_ONLY_EXACT_CENTER_REPORT.md`.

The BYZ_NT source-only follow-up for `υιοσ|-46|backward|before_plus_term` (huios;
English: son) is locked in
`docs/BYZ_SOURCE_ONLY_EXACT_CENTER_PREREGISTRATION.md` and summarized
in `docs/BYZ_SOURCE_ONLY_EXACT_CENTER_REPORT.md`. It stayed at q = `0.000999`
inside BYZ_NT, but remains source-specific and hidden-path only.

The independent-source Greek follow-up is locked in
`docs/GREEK_EXACT_CENTER_THREE_SOURCE_PREREGISTRATION.md` and summarized in
`docs/GREEK_EXACT_CENTER_THREE_SOURCE_REPORT.md`. It moves `δοξα` (doxa;
English: glory) to all-three source support and moves `υιος` (huios; English:
son) to BYZ_NT + SBLGNT support, both still as
controlled review candidates only.

The three-source synthetic follow-up in
`docs/GREEK_EXACT_CENTER_THREE_SOURCE_SYNTHETIC_BASELINES.md` keeps that caution:
all five rows had same-length synthetic any-type matches at or above the target
score, and two rows had same-type synthetic matches. The synthetic matched
phrases also stayed outside their extension spans. That is caution against a
claim, not a rejection of hidden-path candidates as such.

The added-source Greek follow-up is locked in
`docs/GREEK_EXACT_CENTER_FOUR_SOURCE_PREREGISTRATION.md` and summarized in
`docs/GREEK_EXACT_CENTER_FOUR_SOURCE_REPORT.md`. It keeps `δοξα` (doxa;
English: glory) as a
four-source controlled surface-anchored hidden candidate and does not move
`υιος` (huios; English: son) into the locked TCG-overlap set.

The stronger single-row `δοξα` (doxa; English: glory) four-source claim follow-up is locked in
`docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_PREREGISTRATION.md` and summarized in
`docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md`. It ran 5000 shuffled-term and
5000 same-length random controls per row. All four Greek NT rows passed the
registered q <= 0.01 criterion, with q values from 0.0008 to 0.0016. The status
remains `claim_followup_review_candidate`, not a claim.

The stricter single-row `δοξα` (doxa; English: glory) confirmatory follow-up is locked in
`docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_PREREGISTRATION.md` and summarized
in `docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md`. It ran 20000
shuffled-term and 20000 same-length random controls per row. All four Greek NT
rows again passed the registered q <= 0.01 criterion, with combined q = 0.0009
in every source. The status remains `claim_followup_review_candidate`, not a
claim.

The expanded prospective Greek exact-center screen is locked in
`docs/GREEK_EXPANDED_PROSPECTIVE_PREREGISTRATION.md` and summarized in
`docs/GREEK_EXPANDED_PROSPECTIVE_REPORT.md`. It used 291 new Greek terms after
excluding the prior exact-center cohort by normalized form. The run produced
exact-center surface hits, but zero exact-center phrase-extension pattern rows
under the locked same-skip phrase gate. No new row enters the control queue from
that prospective screen.

The post-screen expanded Greek surface queue is tracked in
`docs/GREEK_EXPANDED_SURFACE_QUEUE.md`. It summarizes the exact-center surface
rows without requiring same-skip phrase extension. In that report,
`exact-center surface` means the ELS center falls in a verse where the term
appears as surface text; the center word itself may be a different word. It
found 161 exact-center surface patterns: 27 all-source, 58 multi-source, and 76
source-only. This is useful for choosing future matched-control targets, but it
is broader and weaker than the phrase-extension gate and does not promote any
row to claim status.

The tighter post-screen surface triage is tracked in
`docs/GREEK_EXPANDED_SURFACE_TRIAGE.md`. Its mechanical filter keeps only
all-source patterns with normalized term length >= 5. That leaves three review
rows: `ανομια` (anomia; English: lawlessness) at Matthew 7:23, `ισαακ` (Isaak;
English: Isaac) at Hebrews 11:9, and `τερασ` (teras; English: wonder)
at Hebrews 9:11. It deliberately excludes the dense length-4 bucket, including
`αμην` (amen; English: amen), without making a term-specific judgment. The
subsequent control design compares against real Greek terms matched by length
and surface frequency, not random strings that cannot satisfy surface context.

The selected-row letter-path audit is tracked in
`docs/GREEK_EXPANDED_SURFACE_LETTER_PATHS.md`. It reconstructs every selected
ELS letter in TR_NT, BYZ_NT, TCG_NT, and SBLGNT and records the source word at
each letter position. All selected paths spell the normalized target sequence.
This is an audit layer, not a new statistical test.

The first real-word surface control pool is tracked in
`docs/GREEK_EXPANDED_SURFACE_CONTROL_POOL.md`. It measured normalized
surface-substring verse frequency for all 291 expanded Greek terms across
TR_NT, BYZ_NT, TCG_NT, and SBLGNT. It found 165 terms present by that rule in
all four sources and selected 10 same-length, closest-surface-frequency control
candidates for each of `ανομια` (anomia; English: lawlessness), `ισαακ` (Isaak;
English: Isaac), and `τερασ` (teras; English: wonder). This is still not a
significance test; it is the fair control pool needed before running one.

The first matched-control evaluation is tracked in
`docs/GREEK_EXPANDED_SURFACE_CONTROL_EVALUATION.md`. All three selected targets
had one all-source exact-center surface pattern, while none of their 10 matched
controls had one. Because the pool has only 10 controls per target, the best
possible add-one empirical p-value is 1/11 = 0.090909, and all three rows have
q = 0.090909. Current read: useful triage evidence, not statistical support.

The all-available matched-control follow-up is tracked in
`docs/GREEK_EXPANDED_SURFACE_AVAILABLE_CONTROL_EVALUATION.md`. It used every
same-length all-source surface-present control available from the frozen
expanded Greek term list, excluding the selected target rows from the control
pool: 32 controls for `ισαακ` (Isaak; English: Isaac), 32 for `τερασ` (teras;
English: wonder), and 30 for `ανομια` (anomia; English: lawlessness). All three
selected rows exceed their available matched controls on all-source
surface-pattern count, with q = 0.032258. Current read: stronger triage
evidence, but still post-screen and not public-claim support.

The compact selected-row follow-up is tracked in
`docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md`. It joins the three selected
surface rows, their four-source letter paths, and the all-available real-word
control results into one review sheet. Current status:
`post_screen_surface_followup_review_candidate`, not a claim.

The prospective Greek surface claim standard is tracked in
`docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md`. It states that the existing
`δοξα` (doxa; English: glory), `υιος` (huios; English: son), `αιμα` (haima;
English: blood), `ανομια` (anomia; English: lawlessness), `ισαακ` (Isaak;
English: Isaac), and `τερασ` (teras; English: wonder) rows are prior evidence,
not new prospective discoveries. A future surface study must commit the term
file, protocol, source configs, control design, and correction rule before any
new result-producing run.

The first locked Greek surface prospective cohort is tracked in
`docs/GREEK_SURFACE_PROSPECTIVE_PREREGISTRATION.md` and summarized in
`docs/GREEK_SURFACE_PROSPECTIVE_REPORT.md`. After removing prior selected
surface rows, it tested 288 terms across TR_NT, BYZ_NT, TCG_NT, and SBLGNT.
The registered primary rule required all-source exact-center surface rows with
normalized length >= 5. No row met that primary rule, so the prospective result
is negative.

That same run exposed a post-discovery length-4 bucket, tracked in
`docs/GREEK_SURFACE_LENGTH4_FOLLOWUP_TRIAGE.md`: `αμην` (amen; English: amen),
`αραμ` (Aram; English: Aram), `ασηρ` (Aser; English: Asher), `δασα` (dasa;
English: generated control-like form), `σαβα` (Saba; English: Sheba/Seba),
`σιων` (Sion; English: Zion), and `χουσ` (Chous; English: Cush). Against the declared screening-term control
pool, those rows exceeded the available same-length controls, but only 14
controls were available per target and the add-one floor was q = `0.066667`.
The generated vocabulary-control follow-up in
`docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROL_EVALUATION.md` broadened the
pool to 572 real Greek length-4 surface-vocabulary controls and matched 200
controls per target. Under that larger pool, controls overlap every target and
no target survives study-level q <= 0.05; q values range from `0.278607` to
`0.905473`. Current read: the length-4 bucket is a useful control-design
lesson, not a claim candidate.

The Greek exact-center final gate is tracked in
`docs/GREEK_EXACT_CENTER_FINAL_GATE.md`. It labels hidden-path findings as
candidate types rather than disqualifying them:

- `δοξα` (doxa; English: glory): `cross_version_controlled_surface_anchored_hidden_candidate`;
- `υιος` (huios; English: son): `multi_source_hidden_path_candidate`;
- `αιμα` (haima; English: blood): `source_specific_hidden_path_candidate`.
