---
id: T-0993
title: Francis Gurtrey Blanchard has two cards: Fergus 1843 prints the man T-0990 ruled on, and 'Gantry Blanchard' is very likely the same person
state: claimed
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-09-10
closed: null
pr: null
claimed_by: run 9/10/2026, 5:15:34 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34464830439
---

Francis Gurtrey Blanchard has two cards: Fergus 1843 prints the man T-0990 ruled on, and 'Gantry Blanchard' is very likely the same person.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**FOUND BY T-0990**, ruling cohort A of the land-sale proposals. The residents layer holds
two Blanchards that on the directories' own printing are one man:

- `blanchard_f_gantry` — **F Gantry Blanchard**. Fergus 1843: *"Blanchard, Francis Gurtrey,
  capitalist, res 45 Wells [died, Brooklyn, N.Y., 1872.]"*; Fergus 1839: *"Blanchard,
  Francis G., real estate dealer, Lake street"*; Norris 1844: *"Blanchard, Francis G.
  residence Wells st"*.
- `blanchard_gantry` — **Gantry Blanchard**, a card whose forename is the OTHER man's middle
  name.

The land register prints four spellings of the surname — `BLANCHARD F G` (2 rows),
`BLANCHARD F G AS` (1), `BLANCHARD FRANCIS G` (1) and `BLANCHARD GURTREY` (6) — and if the
two cards are one man, all ten rows are his. T-0990 ruled only the first three, against
`blanchard_f_gantry`, and said in the ruling that it was not deciding this.

**Why this one is not T-0844's kind.** T-0844's six clusters are the ones the evidence does
not decide. This one the evidence may well decide: *Francis Gurtrey* is printed whole, in
one line, by the town's own 1843 directory. What the run must check is whether
`blanchard_gantry`'s evidence is the same evidence read a second time, or a genuinely
separate reading — and `data/residents/card_merge_rulings.json` is where the answer goes.

**Acceptance.** Either the two cards are merged under the card-merge rule with the reasoning
on the ruling, or the ticket records why they must stand apart; and whichever way it goes,
the six `BLANCHARD GURTREY` rows get a ruling in
`data/research/land_sales/resident_rulings.json` under this ticket's number.
