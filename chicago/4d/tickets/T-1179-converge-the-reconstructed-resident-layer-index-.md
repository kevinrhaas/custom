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


---

**Finding (T-1172's closeout read, 2026-09-19): the 1,223-vs-643 gap is a UNIT mismatch, and
this ticket is where it resolves.** Recorded here because the owner asked whether the resident
reconstruction was going to overshoot by design. It is not, and the answer was already written
down in two places that are easy to read past.

`data/reconstruction/1835_readmissions.json` states the tension and then disposes of it in the
same object. `the_tension_this_leaves.what` is the alarming line — the order book models 643
households and ruling 787 more cards present takes the layer to 1,223, "nearly twice the model".
The two fields under it are the answer: the roster "is a licence on WHICH name a filler uses and
never a quota", and **736 of the layer's households are letter-list CONTAINERS holding one
person** — arguing for a person rather than for a dwelling. "A container is not a household in
the model's sense, and the two counts are not yet in the same unit." So the gap is not 787
surplus people; it is households and containers being counted against each other.

Its `whose_it_is` names this ticket: T-1171 draws families into the heads (done) and **T-1179
converges the layer against the model**. Neither could run before the presences were ruled,
which is what T-1172's stage was for.

The measurement on dev at 290cc65d9, for whoever picks this up:

| | |
|---|---|
| cards in the layer (`persons_total`) | 1,588 — attested 410, inferred 875, reconstructed 303 |
| established PRESENT on 1 Jul (`persons_present`) | 457 |
| the model's target (`persons_target`) | 2,535 |
| still to reconstruct | 2,081 |
| households: layer / present / model | 1,258 / 436 / 643 |
| letter-list containers inside that 1,258 | 736 |

Note that `reconstructed: 303` has NOT moved for T-1172's 909 re-admissions, and that is by
design rather than a lag: the stage writes to `data/residents/readmitted/` and declares
`"not_into": "data/residents/households/ and data/residents/index.json"`;
`tools/rebuild_resident_index.py` does not read that directory at all. 726 presence rulings and
183 minted cards are on disk waiting for this convergence. Anyone reading the front screen or
the index for "how far along is the reconstruction" is reading a number that the last stage
deliberately did not touch.

**See also T-1365**, filed the same day: the walk splash fills its bar toward 3,265 (the
NOVEMBER 1835 census) while this programme fills toward 2,535, and counts all 1,588 cards
against it rather than the 457 present. Acceptance 3 here owns the town census screen's final
form, so T-1365 is the interim fix and may be folded into this ticket.

**Finding (T-1174's merge, 2026-09-19): rebuild the MODEL before the stages that draw from
it, and verify the fixed point against `rederive.mjs --run`, not against the stage checks.**
Learned by getting it wrong twice while clearing #1497, and recorded because this ticket has to
do the same convergence for the whole band.

#1497 merged dev with 136 conflicts, 118 of them resident household cards carrying drawn values
the two sides disagreed on (`arrival_year` 1832 against 1835 on the same household). They were
not hand-picked: `reconstruct_residents_1835.py --check` names the remedy itself — "a draw that
cannot be reproduced is not a reconstruction. Run --stage attribute_fill_arrival --build" — so
dev was taken as the base and the programme re-ran its own draws.

**The wrong order cost four passes and was still red.** Rebuilding only the stages —
`attribute_fill_arrival`, then `readmissions`, then `women_and_children`, then the order book —
reached a state where `reconstruct_residents_1835.py --check` exited 0 on every stage. The gate
then failed FIVE steps:

```
* the reconstruction programme answers for every reconstructed resident
* every re-admission re-derives, and no refusal it stands beside has moved
* the 1835 town model re-derives, and every figure is bounded and says what it rests on
* the 1835 population profile re-derives from the resident layer, on every axis
* the 1835 reconstruction order book re-derives, and no bucket is overfilled
```

The cause is the T-1314 finding above, read forwards: the model is re-derived FROM the layer the
stages write into, so a stage rebuild moves the model, and every stage that draws from the model
is then drawing from one that predates its own rebuild. The first pass never rebuilt
`tools/model_town_1835.py` at all. Each stage agreed with itself, which is why the stage checks
were green — a stage's `--check` cannot see that its own input is stale.

**The right order converges in ONE pass:**

```
python3 tools/model_town_1835.py --build
python3 tools/reconstruct_residents_1835.py --stage attribute_fill_arrival  --build
python3 tools/reconstruct_residents_1835.py --stage readmissions            --build
python3 tools/reconstruct_residents_1835.py --stage women_and_children      --build
python3 tools/profile_population_1835.py --build
python3 tools/build_order_book_1835.py --build
```

Then all four of `reconstruct_residents_1835.py --check`, `model_town_1835.py --check`,
`profile_population_1835.py --check` and `build_order_book_1835.py --check` exit 0 — **and still
exit 0 after `node tools/rederive.mjs --run`**, which is the test that matters and the one this
ticket's acceptance 1 is written around. A fixed point that the full derived-layer rebuild undoes
is not a fixed point; the stage checks alone will not tell you which you have.

Acceptance 1 lists the `--check` commands but not an ORDER for the builds, and the order is the
whole difference between one pass and an oscillation. Whoever works this should write it down
where the programme can be run from, not leave it to be rediscovered.

State after that merge, for the next reader: the population profile covers 2,144 persons against
the model's 2,535 target; 900 re-admissions and 124 female-headed households (556 people — 124
women and 432 others) are built and gated, and none of them reaches `index.json` yet.
