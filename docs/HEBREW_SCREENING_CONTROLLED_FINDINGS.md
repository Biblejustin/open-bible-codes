# Hebrew Screening Controlled Findings

Status: broader Hebrew screening controlled follow-up complete; no claim-level
row.

Source reports:

- `docs/HEBREW_SCREENING_VERSION_PRESENCE.md`
- `docs/HEBREW_SCREENING_CONTROLLED_REVIEW.md`

## What Was Run

The broader Hebrew screening matrix checked Hebrew rows from theology,
modern/geopolitical/local/date, Table of Nations, prophetic, Hebrew claim,
tribe, festival, and calendar term files across MT_WLC, UXLC, EBIBLE_WLC, MAM,
and UHB.

The controlled review then ran representative paired controls for nonzero rows
in MT_WLC and UHB:

- shuffled-letter controls preserving target letters;
- same-length random controls drawn from same-corpus letter frequencies;
- `100` samples for each control family;
- Benjamini-Hochberg correction across emitted representative rows.

## Results

| Metric | Count |
| --- | ---: |
| Target rows | 417 |
| Rows with all-source exact patterns | 299 |
| Rows absent or unsummarized | 103 |
| Terms with representative controls | 306 |
| Representative-control rows | 610 |
| Terms not unusual under representative controls | 295 |
| Terms with only uncorrected p<=0.05 prompts | 11 |
| Terms with adjusted representative-control support | 0 |

Uncorrected-only prompts:

| Term | Concept | Normalized | Exact hits | Best p | Best q |
| --- | --- | --- | ---: | ---: | ---: |
| `second_death_h` | Second Death | `מותשני` (mavet sheni; English: second death) | 213 | 0.009901 | 0.862801 |
| `day_of_lord_h` | Day Of The Lord | `יומיהוה` (yom YHWH; English: day of YHWH) | 105 | 0.009901 | 0.862801 |
| `timothy_h` | Timothy | `טימותי` (Timothy; English: Timothy) | 60 | 0.039604 | 1.0 |
| `germany_h` | Germany | `גרמניה` (Germanyah; English: Germany) | 38 | 0.049505 | 1.0 |
| `empty_tomb_h` | Empty Tomb | `קברריק` (kever reik; English: empty tomb) | 18 | 0.019802 | 1.0 |
| `rosh_hashanah_h` | Rosh Hashanah | `ראשהשנה` (Rosh Hashanah; English: head of the year) | 21 | 0.009901 | 0.862801 |
| `pathrusim_h` | Pathrusim | `פתרסימ` (Pathrusim; English: Pathrusim) | 17 | 0.009901 | 0.862801 |
| `2027_additive_h` | Gregorian 2027 additive | `תתתתתכז` (t-t-t-t-t-k-z; English: additive Hebrew-number control for 2027) | 11 | 0.049505 | 1.0 |
| `2025_additive_h` | Gregorian 2025 additive | `תתתתתכה` (t-t-t-t-t-k-h; English: additive Hebrew-number control for 2025) | 6 | 0.039604 | 1.0 |
| `carthage_h` | Carthage | `קרתחדשה` (Qart Chadashah; English: Carthage/new city) | 5 | 0.019802 | 1.0 |
| `yeshu_declared_perfect_h` | Jesus Declared Perfect | `הצהרישומושלמ` (hutshar Yeshu mushlam; English: Jesus was declared perfect) | 5 | 0.009901 | 0.862801 |

Those rows are review prompts only. None survived correction across the
representative row family.

## Selected Requested Terms

| Term ID | Exact read | Control read |
| --- | --- | --- |
| `torah_h` | present; capped at 250 hits; 31 all-source exact patterns | not unusual |
| `yhwh_h` | present; capped at 250 hits; 43 all-source exact patterns | not unusual |
| `messiah_h` | present; capped at 250 hits; 43 all-source exact patterns | not unusual |
| `yeshua_h` | present; capped at 250 hits; 35 all-source exact patterns | not unusual |
| `trump_h` | present; 31 capped hits; 6 all-source exact patterns | not unusual |
| `vance_h` | present; capped at 250 hits; 43 all-source exact patterns | not unusual |
| `netanyahu_h` | present; 131 capped hits; 15 all-source exact patterns | not unusual |
| `iran_h` | present; capped at 250 hits; 44 all-source exact patterns | not unusual |
| `russia_h` | present; capped at 250 hits; 31 all-source exact patterns | not unusual |
| `magog_h` | present; capped at 250 hits; 39 all-source exact patterns | not unusual |
| `hamas_h` | present; capped at 250 hits; 37 all-source exact patterns | not unusual |
| `france_h` | present; capped at 250 hits; 46 all-source exact patterns | not unusual |
| `europe_h` | present; 105 capped hits; 10 all-source exact patterns | not unusual |
| `germany_h` | present; 38 capped hits; 3 all-source exact patterns | uncorrected-only prompt |
| `united_states_h` | absent in capped exact-version matrix | not controlled |
| `united_nations_h` | absent in capped exact-version matrix | not controlled |
| `cowboy_h` | present; 62 capped hits; 8 all-source exact patterns | not unusual |

## Interpretation

The broader run confirms the same pattern as the modern-only run:

- many short Hebrew strings produce stable exact paths across MT-family streams;
- long phrase rows are often absent in the capped screen;
- paired controls explain the stable short-form rows well enough that no row
  currently deserves claim-level treatment.

Current status: broader review material only. The next claim-grade path would
be a narrower preregistered study with a fixed term list, fixed skip range, and
study-level control budget before looking at counts.
