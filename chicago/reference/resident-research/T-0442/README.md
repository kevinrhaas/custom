# T-0442 — the resident-research pilot, 75 people

The first of the fifteen fixed resident-research cohorts, and the pattern the
fourteen after it follow. This folder is its durable handoff, written to the
contract in `../README.md`.

**Research completed:** 2026-08-31. **Package written:** 2026-09-05, by T-0511,
from the committed JSON — the research is the pilot's, the package is not.

## Scope

75 of the 848 attested or inferred named people in the resident layer, at the
1835-07-01 scene date. Reconstructed people are excluded. The frame:

| stratum | people |
|---|---:|
| established_profile | 5 |
| newspaper_profile_unplaced | 20 |
| letter_list_only_present | 25 |
| letter_list_only_uncertain | 25 |

`chicago/4d/tools/select_resident_research_pilot.py --gate` re-derives that
selection and refuses a reconstructed or missing person.

## Results

| outcome | people |
|---|---:|
| corroborated | 4 |
| candidate | 7 |
| no_corroboration | 64 |
| pending | 0 |

7 candidate rows, 12 sources cited, 150 search-log rows.

The strongest resolved case is **J. H. Collins**: the edited Papers of Abraham
Lincoln give James H. Collins's profession and his 1834 Chicago partnership with
John D. Caton — the same distinctive partner and trade the newspaper record
carries — so the bridge is more than an expansion of initials. Caton, Dole and
Carpenter take independent institutional corroboration.

## Method and confidence rules

Queries combined the exact printed name with Chicago, Illinois, 1835, occupation
and genealogy terms, then tested spelling and OCR variants where the newspaper
form was suspect. Surfaces: the repository newspaper corpus, government and
institutional biographies, edited documentary projects, digitized county
histories, historical encyclopedias, and broad genealogy indexes as finding aids
only. The ranked source policy and the identity rules are committed in
`chicago/4d/data/research/residents/source_hierarchy.json`.

An exact name is a search lead, not an identity resolution. `identity_confidence`
is `high` only where an outcome is `corroborated`; every candidate and every
no-find is `unresolved`. A documented no-find is a research result, not evidence
that the person did not exist.

## Unresolved

- The seven candidates are retained unasserted, with their conflicts, in
  `T-0442_candidates.csv`.
- None of these 75 people carries a `resident_research` block on their household
  record. That is the finding behind T-0508 to T-0510 and it is not resolved
  here; the package makes it legible.

## Files

- `T-0442_resident_research.csv` — Residents, on the shared template header.
- `T-0442_candidates.csv` · `T-0442_sources.csv` · `T-0442_search_log.csv` ·
  `T-0442_summary.csv` — the other three contract sheets, and the counts.
- `T-0442_resident_research_working.xlsx` — the same five as a workbook.

All six are GENERATED. Rebuild and prove them with
`chicago/4d/tools/export_resident_research_package.py T-0442 --build | --check`;
`tools/check.sh` runs the `--check`. Columns the committed JSON does not carry
are left empty rather than filled by inference.

## Sources behind this package

`chicago/4d/data/research/residents/pilot_75_cohort.json` (the frozen manifest) ·
`chicago/4d/data/residents/research_pilot.json` (the reviewed outcomes) ·
`chicago/4d/data/sources/*.json` (each cited source) ·
`chicago/4d/docs/RESEARCH/resident_identity_pilot_75.md` (the dossier).
