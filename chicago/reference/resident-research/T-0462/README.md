# T-0462 — second resident-research cohort, 75 people

The durable handoff for the second fixed cohort, written to the contract in
`../README.md`.

**Research completed:** 2026-09-01. **Package written:** 2026-09-05, by T-0511,
from the committed JSON.

## Scope

The next 75 of the 848 eligible attested or inferred named people at the
1835-07-01 scene date, with no overlap with T-0442. Reconstructed people are
excluded. The frame:

| stratum | people |
|---|---:|
| established_profile | 25 |
| letter_list_only_present | 25 |
| letter_list_only_uncertain | 25 |

`chicago/4d/tools/select_resident_research_pass_2.py --gate` re-derives the
cohort and refuses overlap, reconstruction, missing people or stratum drift.

## Results

| outcome | people |
|---|---:|
| corroborated | 27 |
| candidate | 23 |
| no_corroboration | 25 |
| pending | 0 |

23 candidate rows, 48 sources cited, 225 search-log rows. This is the highest
corroboration rate of the first three passes, and the established-profile half
produced nearly all of it.

The 1843 directory extends John Bates Jr.'s exact-name auction trade; *Wilcox v.
Jackson* gives Jean Baptiste Beaubien's 28 May 1835 Cook County land payment; the
edited 1835 incorporation act names John S. C. Hogan a trustee; Papers of Abraham
Lincoln records sharpen Giles Spring's and John Harris Kinzie's migration
chronologies. Institutional sources add sourced household relationships for the
Beaubien, Robinson, Kinzie and Owen families.

## Method and confidence rules

Six parallel research streams combined exact-name searches with Chicago, date,
occupation, office, spouse, migration and spelling/OCR variants, across the
repository corpus, contemporary statutes, a Supreme Court report and city
directory, institutional biographies and finding aids, edited documentary
projects, digitized county histories, memoirs, church histories and broad
indexes. Indexes and trees were discovery aids only. Every cited source has its
own record under `chicago/4d/data/sources/`.

`identity_confidence` is `high` only where the outcome is `corroborated`; every
candidate and every no-find is `unresolved`. A documented no-find is a research
result, not evidence of nonexistence.

## Unresolved

- 23 candidates retained unasserted, with their conflicts, in
  `T-0462_candidates.csv` — among them Billy Caldwell's westward-removal year and
  Robinson's competing dates, which the sources disagree on rather than settle.
- None of these 75 people carries a `resident_research` block on their household
  record; that is T-0508 to T-0510's work, not this package's.

## Files

- `T-0462_resident_research.csv` — Residents, on the shared template header.
- `T-0462_candidates.csv` · `T-0462_sources.csv` · `T-0462_search_log.csv` ·
  `T-0462_summary.csv`.
- `T-0462_resident_research_working.xlsx` — the same five as a workbook.

All six are GENERATED. Rebuild and prove them with
`chicago/4d/tools/export_resident_research_package.py T-0462 --build | --check`;
`tools/check.sh` runs the `--check`. Columns the committed JSON does not carry
are left empty rather than filled by inference.

## Sources behind this package

`chicago/4d/data/research/residents/pass_02_75_cohort.json` ·
`chicago/4d/data/research/residents/pass_02_findings.json` ·
`chicago/4d/data/residents/research_pilot.json` ·
`chicago/4d/data/sources/*.json` ·
`chicago/4d/docs/RESEARCH/resident_identity_pass_02_75.md`.
