---
id: T-1179
title: Converge the reconstructed resident layer: index, sidecars, town census, People view and gates agree; every reconstructed person carries basis, seed, liberty and substitution rule; the population profile is re-run and the town reads complete against the model
state: open
epic: META
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: null
opened: 2026-09-16
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The closeout of the resident band, the way T-1144 closes the spend. After it, the owner's
sentence holds: *"All people should have a best profile … note for each attribute of the person
what is attested, inferred or reconstructed."*

**Acceptance:**

1. **Fixed point.** `reconstruct_residents_1835.py --check` (every stage), `rebuild_resident_index.py
   --check`, the three mints' `--check`, `compile_scene.py compile_people`, `town_census.py
   --check`, `export_resident_audit.py --check` all re-derive with zero drift; the audit table
   gains the reconstructed rows with their basis.
2. **Per-attribute completeness.** `profile_population_1835.py` re-run: every person has sex,
   age band, arrival, origin, reason, roles (or `not_employed` reason), presence, division,
   household relationship — each at a tier; the report's "unknown" columns read zero or list the
   attested/inferred rows where the sources conflict (T-1146's `contradicted`).
3. **The model met.** Headcount, sex ratio, age pyramid, household sizes, lodging occupancy,
   division split, trades — every table within the model's bracket; the order book's person and
   household buckets read filled; the town census screen shows residents / transients / garrison
   and the dwellings ratio.
4. **Substitution.** `substitute_reconstruction.py` (T-1190) handles persons: a new
   attested/inferred person retires the reconstructed one its `replaceable_by` matches, redirects
   the id, frees the bucket; self-test on a fixture.
5. **Liberties.** One entry per stage with `Scope:` counts the compiler agrees with; L1 restated
   (no figure drawn — a reconstructed person is a card, not a body in the scene).
6. **Visible.** People view: tier filter, transient/fort/reconstructed pills, per-attribute tier
   on the card; the "Reconstructing the town" card's person bars full; `smoke_renderer.mjs` walks
   a reconstructed card at both viewports.
7. `docs/RESEARCH/1835_resident_reconstruction.md` closes with the final tables and the exact
   counts by tier; `docs/STATUS.md` says what is unverified.

**Stop condition:** the resident layer is complete to the model, reproducible, and every invented
fact says how it will be replaced.

**Links:** every ticket in this band · T-1144 · T-1160 · T-1166 · T-1190.

---

**Finding (T-1314, 2026-09-18): the model a stage draws from is re-derived FROM the layer
that stage writes into.** `data/reconstruction/1835_town_model.json` counts the resident
layer — `people_the_layer_can_name`, the household-per-record ratio, the arrival-year
shares — and the reconstruction programme's `model_inputs.rows` point at that same file.
So every stage that adds a person moves the model the NEXT stage draws from. The first
stage to land measured the size of it: three people moved `share_of_the_layer_arriving_in_1835`
from 0.449 to 0.448 and moved no derived population figure at all, so nothing is wrong
today. It will not stay that size once T-1173–T-1178 add hundreds.

The model's own prose is already careful — "A count of the layer, not of the town" — and
that is exactly why this is convergence's problem rather than any one stage's: the fix is
a rule about WHICH people the model may count (the sources' people, not the programme's),
and it has to be made once, for every stage, with the order book re-derived under it. Three
other gates were narrowed the same way by T-1314 and are the precedent for the shape of it:
`spend_person_sex_age` (a reconstructed person no longer teaches the forename table),
`read_newberry_index` (an invented name is no longer a candidate for an archival lead) and
`profile_population_1835` (the refusal is now "no reconstructed person the programme cannot
re-derive", not "none at all").

