---
id: T-0487
title: Adjudicate the complete resident research corpus into one identity master
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
blocked_on: Complete the resident-research cohort packages through T-0486, including T-0479's 66 pending people and the pass-4/T-0478 baseline; every cohort manifest must have zero pending outcomes on dev.
needs_bake: false
---

Build the final identity-adjudication layer after the cohort research programme has finished. This ticket does **not** promote uncertain facts into the reconstruction yet. Its job is to combine all of the durable cohort research artifacts and the wider historical reference corpus into a single auditable master crosswalk that says which records refer to the same person, which proposed identities are strong enough to treat as attested, which are reasonable inference candidates, and which remain unresolved or rejected.

Use all resident-research XLSX/CSV/JSON/source ledgers plus the strongest available cross-period material: 1830 and 1840 census work (including the 1840 IPUMS/name-validation artifacts), 1833–34 voter lists, post-office letter lists, newspapers, directories, land/property and tax material, probate, naturalization/immigration, marriage/church, military records, published reminiscences and other repository references. A later record may corroborate an 1835 identity but must not be back-projected without an explicit linkage chain.

**Acceptance:**

- All cohort completion artifacts through T-0486 are on `dev`, every manifest person has a non-pending outcome, and every cohort has its durable XLSX/CSV/README package or a documented equivalent for the earlier passes.
- Create `chicago/reference/resident-research/final/identity/` with a master working XLSX, machine-readable CSV, README/method note and a machine-readable decision ledger keyed by stable resident/person IDs.
- The master contains every researched named resident and every material candidate/duplicate considered. It records seed names/IDs, aliases and spelling variants, source chronology, candidate links, evidence for/against, source IDs/locators, and explicit confidence.
- Each identity decision is classified at minimum as `attested`, `reasonable_inference_candidate`, `unresolved`, `duplicate_of`, or `rejected_candidate`; the classification criteria are documented and applied consistently.
- Census, voter, directory, newspaper, property, probate/church/marriage, immigration/naturalization and other evidence are cross-linked where they materially resolve or contradict an identity.
- No canonical household/person fact is silently promoted merely to make the crosswalk cleaner. Competing candidates and contradictory geography/occupation/kinship remain visible.
- Produce counts for researched people, attested identities, inference candidates, unresolved cases, duplicates and rejected candidates, with enough detail for the next ticket to reproduce every promotion decision.
- The completion PR targets `dev`; it is research synthesis/provenance, not yet the canonical resident-data rewrite.
