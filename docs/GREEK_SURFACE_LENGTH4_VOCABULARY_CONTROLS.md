# Greek Surface Length-4 Vocabulary Controls

Status: generated real-word control universe; no claim.

This file documents the generated term list used to broaden the length-4
Greek surface controls. The generated CSV lives under ignored `reports/`
output because it is derived from local corpus files.

## Inputs

- Source terms: `terms/greek_surface_prospective_terms.csv`
- Selected targets: `reports/greek_surface_length4_followup/selected_patterns.csv`
- Output term CSV: `reports/greek_surface_length4_vocab_controls/terms.csv`

## Rule

- include selected target terms from the locked length-4 follow-up;
- add normalized Greek surface words with length 4..4;
- require presence in at least 4 compared Greek NT sources;
- exclude generated controls with the same normalized spelling as a selected target;
- give each generated control its own category so same-category surface
  context does not inflate the hit output.

## Counts

- selected target terms: 7
- generated control terms: 572
- unique normalized surface words scanned: 19,175

## Selected Targets

| Term ID | Term | Concept |
| --- | --- | --- |
| `gpx_amen_g` | `αμην` (amen; English: Amen) | Amen |
| `gpx_aram_g` | `αραμ` (aram; English: Aram) | Aram |
| `gpx_asher_g` | `ασηρ` (aser; English: Asher) | Asher |
| `gpx_cush_g` | `χουσ` (chous; English: Cush) | Cush |
| `gpx_lasha_g` | `δασα` (dasa; English: Lasha) | Lasha |
| `gpx_seba_g` | `σαβα` (saba; English: Seba) | Seba |
| `gpx_zion_g` | `σιων` (Sion; English: Zion) | Zion |

## Control Preview

| Term ID | Term | Notes |
| --- | --- | --- |
| `gsvocab_0001_d035328d` | `αββα` (abba; English: Abba) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:3/SBLGNT:3/TCG_NT:3/TR_NT:3 |
| `gsvocab_0002_6cb77401` | `αβελ` (abel) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:4/SBLGNT:4/TCG_NT:4/TR_NT:4 |
| `gsvocab_0003_9a510b16` | `αβια` (abia; English: Abijah) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:2/SBLGNT:2/TCG_NT:2/TR_NT:2 |
| `gsvocab_0004_958bcf84` | `αγαρ` (agar) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:2/SBLGNT:2/TCG_NT:2/TR_NT:2 |
| `gsvocab_0005_d614136a` | `αγει` (agei) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:2/SBLGNT:2/TCG_NT:2/TR_NT:2 |
| `gsvocab_0006_c2c91076` | `αγια` (agia) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:13/SBLGNT:13/TCG_NT:13/TR_NT:13 |
| `gsvocab_0007_049e81b9` | `αγιε` (agie) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:1/SBLGNT:1/TCG_NT:1/TR_NT:1 |
| `gsvocab_0008_2774a178` | `αγιω` (agio) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:25/SBLGNT:26/TCG_NT:25/TR_NT:25 |
| `gsvocab_0009_eef24c9d` | `αγνα` (agna) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:1/SBLGNT:1/TCG_NT:1/TR_NT:1 |
| `gsvocab_0010_85e5c0e1` | `αγνη` (agne) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:1/SBLGNT:1/TCG_NT:1/TR_NT:1 |
| `gsvocab_0011_04485e9d` | `αγρα` (agra) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:1/SBLGNT:1/TCG_NT:1/TR_NT:1 |
| `gsvocab_0012_43f2c9cb` | `αγρω` (agro) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:9/SBLGNT:9/TCG_NT:9/TR_NT:10 |
| `gsvocab_0013_03dcfb3b` | `αδαμ` (adam; English: Adam) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:7/SBLGNT:7/TCG_NT:7/TR_NT:7 |
| `gsvocab_0014_102fd535` | `αδδι` (addi) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:1/SBLGNT:1/TCG_NT:1/TR_NT:1 |
| `gsvocab_0015_887957e3` | `αδησ` (ades; English: Hades) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:3/SBLGNT:3/TCG_NT:3/TR_NT:3 |
| `gsvocab_0016_c2af8211` | `αδου` (adou) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:6/SBLGNT:4/TCG_NT:6/TR_NT:6 |
| `gsvocab_0017_a9a5cbb0` | `αερα` (aera) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:5/SBLGNT:5/TCG_NT:5/TR_NT:5 |
| `gsvocab_0018_f65abce2` | `αετω` (aeto) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:1/SBLGNT:1/TCG_NT:1/TR_NT:1 |
| `gsvocab_0019_155dae59` | `αζωρ` (azor; English: Azor) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:2/SBLGNT:2/TCG_NT:2/TR_NT:2 |
| `gsvocab_0020_b2cc863e` | `αθλη` (athle) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:1/SBLGNT:1/TCG_NT:1/TR_NT:1 |
| `gsvocab_0021_baf09972` | `αιμα` (haima; English: blood) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:41/SBLGNT:42/TCG_NT:41/TR_NT:42 |
| `gsvocab_0022_bbf44314` | `αιρε` (aire) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:3/SBLGNT:3/TCG_NT:3/TR_NT:3 |
| `gsvocab_0023_bbec2f2f` | `ακοη` (akoe) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:9/SBLGNT:9/TCG_NT:9/TR_NT:9 |
| `gsvocab_0024_d0312fcb` | `ακων` (akon) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:1/SBLGNT:1/TCG_NT:1/TR_NT:1 |
| `gsvocab_0025_2a5347e5` | `αλασ` (alas) | generated normalized Greek surface vocabulary control; verse_counts=BYZ_NT:3/SBLGNT:3/TCG_NT:3/TR_NT:3 |

Preview only; 547 additional control rows are in `reports/greek_surface_length4_vocab_controls/terms.csv`.

## Read

This broadens the control universe for the length-4 follow-up. It is still
post-discovery, but it avoids making the result depend on the much smaller
declared screening-term file.
