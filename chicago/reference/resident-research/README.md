# Resident research artifacts

This directory is the durable, human-reviewable research record for the Chicago resident-identity programme. It complements the application-facing JSON findings/source ledgers under `chicago/4d/data/research/residents/`; it does not replace them.

The model is intentionally similar to `chicago/reference/census1840/validation/`: preserve a working spreadsheet, a machine-readable export, and a method/readme so later workers can audit and reuse the research rather than relying on chat history.

## One package per cohort ticket

Each completed resident-research ticket creates a folder:

`chicago/reference/resident-research/T-NNNN/`

Minimum committed files:

1. `T-NNNN_resident_research_working.xlsx` — human-reviewable working workbook.
2. `T-NNNN_resident_research.csv` — machine-readable export of the resident-level results.
3. `README.md` — methods, source scope, date researched, confidence rules, unresolved issues, candidate/no-find counts, and links/paths to the JSON findings and source records.
4. The ticket's completed JSON findings ledger and new/updated source records remain in the 4D research tree and must be traceable from the workbook/CSV by stable IDs.

The XLSX is a research artifact, not a presentation document. Preserve useful intermediate evidence and conflicts rather than polishing away uncertainty.

## Workbook sheets

At minimum:

- **Residents** — one row per manifest person and final research outcome.
- **Candidates** — one row per plausible external identity or duplicate considered, including rejected candidates when they materially affected the decision.
- **Sources** — one row per source used or materially consulted, keyed to the repository source ID where one exists.
- **Search_Log** — important searches, archives/databases queried, date accessed, result/negative result, and limitations.

Additional sheets are welcome when useful (households, property, census crosswalks, voter crosswalks, occupations, chronology), but the four sheets above are the common handoff.

## Resident CSV / Residents sheet fields

Use the shared template header in `cohort_research_template.csv`. Required concepts include:

- ticket/cohort and stable `person_id` / `household_id`;
- name as transcribed in the seed source and normalized display name;
- research outcome (`corroborated`, `candidate`, `no_corroboration`) and confidence;
- scene-date presence / letter-list context;
- candidate identity or duplicate IDs when relevant;
- proposed birth/death, migration/arrival, occupation/trade, address/property, spouse/kin, civic/voter/census and household facts;
- evidence supporting and contradicting each proposed identity/fact;
- repository `source_ids`, source URLs/locators, source tier, query/access date and limitations;
- recommended downstream action and notes.

Do not collapse competing candidates into one row of asserted facts. Use the Candidates sheet and reference candidate IDs from Residents.

## Evidence discipline

A surname or generic exact-name match is a search clue, not an identity resolution. Heritage, ethnicity, immigration origin, kinship, marriage, occupation, address and household membership require resolving evidence.

Cohort tickets research **named, non-reconstructed people**. They do not silently convert uncertain matches or aggregate census counts into named residents. Ambiguous matches remain candidates. Negative searches remain documented negative searches, not proof of nonexistence.

Facts promoted later into canonical resident/household data must retain per-attribute provenance. Conflicting evidence stays visible. The later synthesis tickets distinguish:

- **attested** people/facts — directly supported strongly enough to promote;
- **inferred** people/facts — reasonable reconstruction from multiple linked observations, explicitly marked as inference and never presented as direct attestation;
- **unresolved candidates** — retained in research artifacts but not promoted as fact.

## Completion rule

A cohort ticket is not complete while any manifest person remains `pending`, or while its XLSX/CSV/README package exists only locally. The completion PR to `dev` is the research receipt: it must contain the durable artifact package, completed findings ledger, source records and necessary compiler/sidecar integration.
