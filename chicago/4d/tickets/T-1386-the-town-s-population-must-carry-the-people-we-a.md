---
id: T-1386
title: The town's population must carry the people we already know: 276 of 410 attested residents sit outside it on an unruled 'uncertain', not on evidence of absence, and the owner's rule is that an attested person is the ideal case
state: open
epic: META
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-19
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The town's population must carry the people we already know: 276 of 410 attested residents sit outside it on an unruled 'uncertain', not on evidence of absence, and the owner's rule is that an attested person is the ideal case.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**The owner's direction, 2026-09-19, in his words:** *"You should not be so dogmatic about the
scene date, put more of those attested people back into the population, I want a full population
of the city to work from."* And earlier the same morning, the rule behind it: *"if they are
attested that's ideal if we know them already."*

**The measurement that makes this a defect rather than a preference.** Of the 410 people the
layer grades `attested`:

| `present_on_scene_date` | people |
|---|---|
| `uncertain` | **276** |
| `present` | 133 |
| `absent` | **1** |

The one absence is `hh_porthier_joseph` — Joseph Porthier, who is one of the six documented
departures T-1354 owns. So of the 277 attested people the town census leaves out of its
population, **276 are out because nobody has ruled them, and exactly one is out on evidence.**
Every one of those 276 has attested evidence that they lived in this town. None of them has
evidence they were elsewhere on 1 July 1835. They are missing from the population because a
field says `uncertain`, and `uncertain` here means unadjudicated, not disputed.

That is the wrong side of the project's own standard. T-1144's rule is "no false Chicago
resident, and no 1835 claim above its dated evidence" — which refuses INVENTING a resident. It
does not ask the layer to forget one it has attested evidence for. Holding 276 known people out
of the town's population to protect a single day's precision reads the rule backwards, and it
is worse the better the research gets: every attested person the corpus gains arrives
`uncertain` and lands outside the town.

Note also that all 276 carry `tier: None` on the presence — they have no tier at all, so this
is not a case of a weak tier being honestly recorded. Nothing has been decided about them.

1. The town's population carries the attested. An attested person is in the population unless
   there is EVIDENCE they were not — a documented departure, a dated appearance elsewhere, a
   source that places them outside. `uncertain` with no tier and no contrary reading is not that
   evidence and does not exclude anybody.
2. **Rule the 276, one at a time, and record the tier.** Each gets a presence and a tier that
   says how it was reached: attested where a source dates them at Chicago across 1 July;
   `inferred` where attested evidence places them in the town in a window that spans the scene
   date; `reconstructed` only where the persistence model is genuinely what carries it. A blanket
   flip to `present` is refused by this ticket — it would put an undeclared claim on 276 cards
   and is the fault this acceptance exists to prevent.
3. **An attested person never takes a reconstructed presence when an inferred one is available.**
   T-1172's R1 leg re-rules `uncertain` presences at tier `reconstructed`; for a person whose
   residence is attested that is a downgrade dressed as progress. The owner's rule governs:
   attested is the ideal case and the tier must not fall below what the evidence already
   supports.
4. **The splash reads the population, and says what it is counting.** After T-1365 the gate
   screen shows the scene-established count, which is honest but is not "the population of the
   city". Whatever this unit lands, the front screen states plainly which question its number
   answers, and the scene-date figure stays available rather than being overwritten — they are
   two real measures and the project needs both.
5. Joseph Porthier stays out, and the file says why: a documented departure, owned by T-1354. One
   evidenced absence is the shape of a correct exclusion; 276 unruled ones are not.
6. The order book, the town census, the population profile and the front screen all move together
   and re-derive — this changes `persons_present`, which the model's own targets are measured
   against, so the convergence set of T-1179 runs over it (model first; the whole sequence).

**NOT IN SCOPE:** inventing anybody, or relaxing T-1144's refusal of a false resident. This
ticket moves people the project has ALREADY attested from outside the town to inside it, with a
ruling and a tier on each. It adds no new names.
