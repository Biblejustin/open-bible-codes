# Hebrew Claim Terms

Term list:

- `terms/hebrew_claim_terms.csv`
- Bible Code Digest source-audit supplement:
  `terms/bible_code_digest_claim_terms.csv`
- CRI critique stress-test supplement:
  `terms/cri_els_critique_terms.csv`
- TheWordNotes ELS PDF source-audit supplement:
  `terms/thewordnotes_els_claim_terms.csv`
- Cosmic Codes source-audit supplement:
  `terms/cosmic_codes_claim_terms.csv`
- Mark Tabata Isaiah 53 source-audit supplement:
  `terms/mark_tabata_isaiah53_claim_terms.csv`
- Bible-codes.org pictogram/source-audit supplement:
  `terms/bible_codes_org_claim_terms.csv`
- Bible and Science critique/source-audit supplement:
  `terms/bible_and_science_codes_terms.csv`
- Religions Wiki scriptural-codes critique supplement:
  `terms/religions_wiki_scriptural_codes_terms.csv`

Purpose:

- Compile a broad Hebrew-only list of claim-driven ELS search terms before running another large search.
- Keep supplied spellings and phrases explicit.
- Keep date encodings explicit because numeric digits are not part of the normalized Hebrew Bible stream.

Included categories:

- core/foundational terms
- rabbinic names
- historical and modern names/events
- Israeli and political figures
- Jesus/Messianic phrases and variants
- prophetic/theological phrases
- trees and bonus single words
- textual September 11 forms
- Hebrew gematria-style encodings for 1939-1945, 1948, 1967, 1973, 1982, and 2001
- Bible Code Digest source leads: Yeshua/Messiah extensions, Isaiah 53,
  Psalm 22, "Who is like God", King David, Ezekiel war/Temple, Shimon Peres,
  Obama/election, terrorism, disasters, economy, climate, and religion-comparison
  claim families
- TheWordNotes source leads: Torah/YHWH opening examples, Grant Jeffrey-style
  historical clusters, Rambsel Yeshua/Messiah examples, and the Isaiah 52-54
  table family
- Cosmic Codes source leads: Torah/YHWH examples, Genesis tree clusters,
  Holocaust and historical clusters, Rambsel Yeshua examples, Isaiah 53 table
  rows, Rabin scripta-continua examples, and sevenfold count terms
- Mark Tabata source leads: Isaiah 52:13-53:12 ELS cluster terms and the
  article's WRR/Gans statistical-apologetic framing
- Bible-codes.org source leads: ELS matrix slides, John 3:16 KJV demo words,
  pictogram clusters, overlapping-image claims, authenticity criteria,
  prophecy/prediction claims, and warnings against misuse
- Bible and Science source leads: ELS critique controls, manuscript-variation
  guardrails, acrostics, Atbash cryptograms, and gematria examples
- Religions Wiki source leads: broad scriptural-code critique, Qur'an 19,
  theomatics, Chinese-character arguments, non-Bible controls, and
  multiple-comparison guardrails

Current runs:

- `protocols/hebrew_claim_version_presence.toml` compares exact ref-key patterns
  for this file across MT_WLC, UXLC, EBIBLE_WLC, MAM, and UHB.
- `protocols/broad_search.toml` includes this file in the broader skip `2..100`
  screening run.
- Public/media-style claims remain under-specified unless their exact source,
  spelling, skip, layout, and metric are locked in `claims/claim_catalog.csv`.
- Bible Code Digest leads are tracked in `docs/BIBLE_CODE_DIGEST_AUDIT.md` and
  remain `under_specified` until exact spellings and geometry are locked.
- CRI critique examples are tracked in `docs/CRI_ELS_CRITIQUE_AUDIT.md`; they
  are stress-test inputs for ambiguity and control design, not positive claims.
- TheWordNotes PDF leads are tracked in `docs/THEWORDNOTES_ELS_AUDIT.md` and
  remain `under_specified` until exact source editions, letter paths, and
  cluster metrics are locked.
- Cosmic Codes leads are tracked in `docs/COSMIC_CODES_AUDIT.md`; the companion
  PDF is copyrighted and not committed.
- Mark Tabata Isaiah 53 leads are tracked in
  `docs/MARK_TABATA_ISAIAH53_AUDIT.md`.
- Bible-codes.org leads are tracked in `docs/BIBLE_CODES_ORG_AUDIT.md`.
- Bible and Science critique leads are tracked in
  `docs/BIBLE_AND_SCIENCE_CODES_AUDIT.md`.
- Religions Wiki critique leads are tracked in
  `docs/RELIGIONS_WIKI_SCRIPTURAL_CODES_AUDIT.md`.

Ad hoc count command:

```bash
python3 -m els batch \
  --terms terms/hebrew_claim_terms.csv \
  --corpus MT_WLC=configs/example_oshb_wlc.toml \
  --min-skip 2 --max-skip 100 \
  --min-term-length 3 \
  --jobs 0 \
  --out reports/hebrew_claim_terms_counts.csv \
  --manifest-out reports/hebrew_claim_terms_counts.manifest.json
```

Cautions:

- Raw digits such as `1948` and `11.9` normalize away. Use declared Hebrew encodings for meaningful runs.
- Short forms like `בא` (ba; English: came), `קם` (qam; English: rose/stood), `עד` (ed; English: witness/until), and `צר` (tsar; English: foe/adversary) are noisy or skipped by default.
- These terms are a screening list, not claims of significance.
- The current claim-catalog entries for Rabin, Hitler/Shoah, and Hebrew Jesus
  phrases are `under_specified`, not reproduced claims.
