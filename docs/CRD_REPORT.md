# CRD Report

Status: generated from the Centered-Relevance Density matrix.

## Reproduce

```bash
python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --resume
python3 -m scripts.build_crd_comparison
```

## Summary

- density rows: 80
- term/control comparison rows: 10
- edition summary rows: 8
- classifier agreement rows: 0
- rows with secular max density = 0: 10
- manifest status: completed

## Bible vs Secular Controls

| Classifier | Term | Bible max | Secular max | Ratio | Exceeds secular max |
| --- | --- | ---: | ---: | ---: | --- |
| deterministic | `beast_h` | 5.01235546 | 0 |  | true |
| deterministic | `cyrus_h` | 3.3415703 | 0 |  | true |
| deterministic | `darius_h` | 9.15160465 | 0 |  | true |
| deterministic | `dragon_h` | 40.9342362 | 0 |  | true |
| deterministic | `gog_h` | 1.67078515 | 0 |  | true |
| deterministic | `horn_h` | 5.01235546 | 0 |  | true |
| deterministic | `magog_h` | 11.6954961 | 0 |  | true |
| deterministic | `prophet_h` | 2.50617773 | 0 |  | true |
| deterministic | `seal_h` | 2.50617773 | 0 |  | true |
| deterministic | `vision_h` | 6.68314061 | 0 |  | true |

## Representative Relevant Centers

| Term | Corpus | Center ref | Center word | Type | Skip |
| --- | --- | --- | --- | --- | ---: |
| `beast_h` | MAM | Ezek 13:19 | לֹא־תִֽחְיֶ֑ינָה | surface_keyword_match | 2 |
| `beast_h` | MAM | Ezek 14:13 | וְהִשְׁלַחְתִּי־בָ֣הּ | surface_keyword_match | 2 |
| `beast_h` | MAM | Ezek 28:23 | וְשִׁלַּחְתִּי־בָ֞הּ | surface_keyword_match | 2 |
| `beast_h` | MAM | Ezek 33:15 | הַֽחַיִּים֙ | surface_keyword_match | 2 |
| `beast_h` | MAM | Ezek 38:8 | בְּאַחֲרִ֨ית | surface_keyword_match | 2 |
| `beast_h` | MAM | Ezek 3:6 | שְׁלַחְתִּ֔יךָ | surface_keyword_match | 2 |
| `beast_h` | MT_WLC | Ezek 13:19 | תִֽחְיֶ֑ינָה | surface_keyword_match | 2 |
| `beast_h` | MT_WLC | Ezek 14:13 | וְ/הִשְׁלַחְתִּי | surface_keyword_match | 2 |
| `beast_h` | MT_WLC | Ezek 28:23 | וְ/שִׁלַּחְתִּי | surface_keyword_match | 2 |
| `beast_h` | MT_WLC | Ezek 33:15 | הַֽ/חַיִּים֙ | surface_keyword_match | 2 |
| `beast_h` | MT_WLC | Ezek 38:8 | בְּ/אַחֲרִ֨ית | surface_keyword_match | 2 |
| `beast_h` | MT_WLC | Ezek 3:6 | שְׁלַחְתִּ֔י/ךָ | surface_keyword_match | 2 |
| `beast_h` | UXLC | Ezek 13:19 | תִֽחְיֶ֑ינָה | surface_keyword_match | 2 |
| `beast_h` | UXLC | Ezek 14:13 | וְהִשְׁלַחְתִּי־ | surface_keyword_match | 2 |
| `beast_h` | UXLC | Ezek 28:23 | וְשִׁלַּחְתִּי־ | surface_keyword_match | 2 |
| `beast_h` | UXLC | Ezek 33:15 | הַֽחַיִּים֙ | surface_keyword_match | 2 |
| `beast_h` | UXLC | Ezek 38:8 | בְּאַחֲרִ֨ית | surface_keyword_match | 2 |
| `beast_h` | UXLC | Ezek 3:6 | שְׁלַחְתִּ֔יךָ | surface_keyword_match | 2 |
| `cyrus_h` | MAM | Dan 6:14 | וְעַל־אֱסָרָ֖א | surface_keyword_match | 5 |
| `cyrus_h` | MAM | Ezra 4:7 | עַל־אַרְתַּחְשַׁ֖שְׂתְּא | surface_keyword_match | 4 |
| `cyrus_h` | MAM | Isa 36:16 | וּצְא֣וּ | surface_keyword_match | -6 |
| `cyrus_h` | MAM | Isa 52:14 | וְתֹאֲר֖וֹ | surface_keyword_match | -8 |
| `cyrus_h` | MT_WLC | Dan 6:14 | וְ/עַל | surface_keyword_match | 5 |
| `cyrus_h` | MT_WLC | Ezra 4:7 | עַל | surface_keyword_match | 4 |
| `cyrus_h` | MT_WLC | Isa 36:16 | וּ/צְא֣וּ | surface_keyword_match | -6 |

## Read

- CRD is a density screen, not a claim promotion engine.
- Deterministic mode only reports locked exact dictionary matches.
- Concept-code matches require explicit surface/context concept fields; hidden-term metadata alone is not counted.
- Secular-control zeroes can reflect dictionary vocabulary and context coverage, not only signal strength.
- LLM and parallel modes require audit-log review before interpretation.
- Interpret results only against the dictionary and preregistration hashes recorded in the manifest.
