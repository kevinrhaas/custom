---
id: T-0897
title: census_1840 sits 291 under its read-vs-ruled ceiling after T-0698's spend, and --tighten can only lower every domain at once
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

census_1840 sits 291 under its read-vs-ruled ceiling after T-0698's spend, and --tighten can only lower every domain at once.

Found by T-0698, which earned the slack and could not spend it.

`tools/measure_research_spend.py` reads census_1840 at **819 ruled on against 812 read**
after T-0698 wrote the 1840 head crosswalk's 27 rulings onto the cards they name. Its
`unspent_ceiling` is still **284**, the figure the domain's worst day earned, so the meter
prints *reclaimable: census_1840 sits 291 under its ceiling* — which is the ratchet saying,
correctly, that the domain could read 291 names ahead of its adjudication again without
anything going red.

Lowering a ceiling is free by construction ("can only make this gate stricter, and is
therefore free") and the tool has `--tighten` for it. The catch is that `--tighten` lowers
EVERY ceiling that sits above what its domain now reads, in one pass — newberry_index is
560 under its own — and those are other tickets' earnings, banked by other runs, with their
own reasons. T-0698 left it rather than bundle a fleet-wide ratchet tightening into a PR
about one crosswalk.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- Every domain sitting under its ceiling is tightened, in one deliberate pass, with the
  before-and-after figure for each stated in the PR — or `--tighten` gains a `--domain`
  argument and this ticket spends census_1840's 291 alone. Either is a decision; drifting
  is not.
- `tools/measure_research_spend.py --gate` green afterwards, and `--self-test` still fires.
- No ceiling moves UP in this ticket. A raise is a separate decision with a written reason.

**Links:** T-0598 (the third hop) · T-0602 · T-0698 (which earned this) ·
`tools/research_spend_baseline.json`.
