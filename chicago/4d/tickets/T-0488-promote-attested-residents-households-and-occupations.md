---
id: T-0488
title: Promote attested residents, households, occupations and relationships into canonical data
state: blocked-tech
epic: META
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: null
opened: 2026-09-02
closed: null
pr: null
claimed_by: null
blocked_on: T-0487 must land the complete identity master and its attested/unresolved decisions on dev.
needs_bake: false
---

Use the adjudicated identity master from T-0487 to improve the canonical 1835 resident and household data with facts that are sufficiently attested. This is the conservative promotion pass: add or correct people, household membership, aliases, occupations/trades, kinship, arrival/migration, civic/voter links, addresses/property and other resident attributes only where the evidence reaches the project's documented attestation threshold.

The purpose is to make the reconstruction substantially richer without converting plausible research leads into asserted history. Favor primary and institutional evidence, dated Chicago/Cook County linkage, repeated cross-source agreement and internally consistent chronology. Later census or biographical evidence may support an 1835 fact only when the bridge back to the scene date is explicit.

**Acceptance:**

- T-0487's identity master is the decision input; every promoted identity/fact points back to a master decision and repository source IDs/locators.
- Add attested named residents that the completed research establishes were present or reasonably within the project's scene-date residence rules; merge true duplicates without losing aliases, source history or old stable-ID references.
- Update household composition and relationships only when directly supported or strongly linked; do not create spouse/child/kin relations from surname similarity.
- Update occupations/trades, employer/business links, voter/civic status, addresses/property, migration/arrival and biographical fields when attested. Extend controlled vocabularies rather than forcing documented trades into the wrong category.
- Every changed attribute carries per-attribute provenance/confidence. Contradictory sources remain recorded rather than overwritten silently.
- Do not promote `reasonable_inference_candidate` or unresolved cases in this ticket; those belong to T-0489.
- Produce a before/after change ledger under `chicago/reference/resident-research/final/attested/` with XLSX/CSV/README showing each canonical record changed, old value, new value, decision class, confidence and sources.
- Re-run the resident compilers/sidecars, update published mirrors and any population/occupation/household summaries derived from the canonical data.
- Validate that no previously cited fact loses its provenance and no new canonical fact is uncited.
- The completion PR targets `dev` and reports counts of residents added, duplicates merged, household memberships changed, occupations added/changed and other promoted attributes.
