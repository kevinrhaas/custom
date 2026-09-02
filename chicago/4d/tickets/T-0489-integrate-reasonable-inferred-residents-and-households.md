---
id: T-0489
title: Integrate reasonable inferred residents and household members with explicit inference provenance
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
blocked_on: T-0488 must land the attested canonical resident and household improvements on dev.
needs_bake: false
---

After attested facts have been promoted, revisit the project's reconstructed/inferred people and household composition using the completed research corpus plus census, voter, directory, newspaper and other evidence. Add or improve inferred residents and household members only when the inference is useful, internally consistent and supported by an explicit chain of observations.

This ticket must preserve the distinction between **attested person**, **named inferred person**, and **unnamed/aggregate inferred household member**. Aggregate census composition can justify an inferred household member or demographic slot; it cannot by itself supply a name, occupation or kinship relation. A named inferred resident requires enough independent linkage to make that identity reasonably likely, while still being labeled inferred rather than attested.

**Acceptance:**

- Use T-0487's `reasonable_inference_candidate` decisions and T-0488's attested canonical baseline; do not reopen attested decisions without new contradictory evidence.
- Reconcile `inf_*`, unnamed/count placeholders and other inferred household members against the 1830/1840 census bridge, 1833–34 voter material, letter lists, directories, newspapers, property/land, probate, church/marriage, immigration/naturalization, military and household evidence where relevant.
- A named inferred person is created only when multiple linked observations make the identity reasonably likely; the record remains explicitly graded/typed as inferred and includes the inference chain and confidence.
- Census household totals/age-sex bands may create or refine unnamed inferred members, but must not invent names, occupations, exact ages or relationships that the evidence does not support.
- Household membership, spouse/kin relations, occupations, origins and addresses are inferred independently per attribute; confidence in one attribute does not automatically propagate to the others.
- Preserve alternative hypotheses where more than one household/person reconstruction remains plausible.
- Produce `chicago/reference/resident-research/final/inferred/` with XLSX/CSV/README listing every inferred record created/changed, the observations used, inference logic, alternatives, confidence and source IDs/locators.
- Re-run population/household consistency checks so inferred members do not double-count attested residents or violate the committed census/household constraints.
- Re-run resident compilers/sidecars and published mirrors; user-facing provenance must distinguish attested from inferred information.
- The completion PR targets `dev` and reports counts of named inferred residents, unnamed inferred members, household changes, rejected inference candidates and unresolved cases.
