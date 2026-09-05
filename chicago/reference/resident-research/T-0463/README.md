# T-0463 — third resident-research cohort, 75 people

The durable handoff for the third fixed cohort, written to the contract in
`../README.md`.

**Research completed:** 2026-09-01. **Package written:** 2026-09-05, by T-0511,
from the committed JSON.

## Scope

75 real named people from the 848-person eligible set, non-overlapping with
T-0442 and T-0462, at the 1835-07-01 scene date. Reconstructed people are
excluded. The frame:

| stratum | people |
|---|---:|
| established_profile | 25 |
| letter_list_only_present | 25 |
| letter_list_only_uncertain | 25 |

`chicago/4d/tools/select_resident_research_pass_3.py --gate` re-derives the
cohort.

## Results

| outcome | people |
|---|---:|
| corroborated | 16 |
| candidate | 15 |
| no_corroboration | 44 |
| pending | 0 |

15 candidate rows, 22 sources cited, 225 search-log rows. With T-0442 and T-0462
this closed the first 225 of the 848 eligible people.

The strongest additions connect named Chicago people to dated civic, legal,
commercial, church, institutional and local-history records: Daniel Elston's 1833
merchant and soap/candle, distillery and brewery activity; Stephen F. Gale's 1833
voter record and 1839 printing imprint; Russel E. Heacock's subdivision plat and
directory entry; Benjamin Jones's Chicago merchant and speculator role before his
1836 Manitowoc move.

## Method and confidence rules

Exact-name searching with Chicago, date, occupation and spelling/OCR variants
across the repository corpus, civic and legal records, church and institutional
histories, digitized county histories and broad indexes used as finding aids
only. Enrichments are cited in the sidecar; the original resident row remains the
identity anchor and no enrichment rebuilds a household.

`identity_confidence` is `high` only where the outcome is `corroborated`; every
candidate and every no-find is `unresolved`.

## Unresolved

- 15 candidates retained unasserted, with their conflicts, in
  `T-0463_candidates.csv` — Ben Butterfield's Chicago/Lockport route, Alva
  Dunlap's 1834 Illinois travel, Andrew Miles's 1834 Fox River claim, Charles H.
  Bartlett's 1834 farming diary, Alfred Churchill's Flag Creek civic record and
  Rouse Bly's Ohio record among them. Geography, chronology, spelling and the
  absence of a direct Chicago bridge are recorded as conflicts.
- None of these 75 people carries a `resident_research` block on their household
  record; that is T-0508 to T-0510's work.

## Files

- `T-0463_resident_research.csv` — Residents, on the shared template header.
- `T-0463_candidates.csv` · `T-0463_sources.csv` · `T-0463_search_log.csv` ·
  `T-0463_summary.csv`.
- `T-0463_resident_research_working.xlsx` — the same five as a workbook.

All six are GENERATED. Rebuild and prove them with
`chicago/4d/tools/export_resident_research_package.py T-0463 --build | --check`;
`tools/check.sh` runs the `--check`. Columns the committed JSON does not carry
are left empty rather than filled by inference.

## Sources behind this package

`chicago/4d/data/research/residents/pass_03_75_cohort.json` ·
`chicago/4d/data/research/residents/pass_03_findings.json` ·
`chicago/4d/data/residents/research_pilot.json` ·
`chicago/4d/data/sources/*.json` ·
`chicago/4d/docs/RESEARCH/resident_identity_pass_03_75.md`.
