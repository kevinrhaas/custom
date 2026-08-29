---
id: T-0416
title: Wm. Sabine, John Dave and the Dearborn wine store: the three storefronts the street-face policy refuses for want of a fronting roof
state: blocked-owner
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0387
opened: 2026-08-29
closed: null
pr: null
claimed_by: run 8/29/2026, 4:23:13 PM CT
blocked_on: Is a corner side a face, and is the centreline band? Measured: a corner-side ruling seats +12 shops (Dearborn 8, La Salle 3, Canal 1) and NONE of this ticket's three; adding the band seats one more, Wm. Sabine. The three storefronts here want frontage on North Water and Dearborn, not a widened reading.
needs_bake: false
---

Wm. Sabine, John Dave and the Dearborn wine store: the three storefronts the street-face policy refuses for want of a fronting roof.

Piece 2 of 2 of **T-0387 — The four storefronts the American puts on a street and nothing narrower: Harmon Loomis, Wm. Sabine, John Dave and the Dearborn Street wine store**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**Why these three are a ticket of their own.** T-0354's street-face policy — the owner's
ruling of 2026-08-29 — seats a `street_only` business on a reconstructed roof whose
PLATTED LOT fronts the street the paper names. It refuses all three of these for one
reason, and the refusal is recorded in
`data/research/newspapers/street_face_adoptions.json`:

| business | street | the refusal |
|---|---|---|
| `business_wm_sabine_storage_forwarding_and_commission_merchant` | North Water | 0 roofs front it; 1 stands within the centreline band |
| `business_john_dave_north_water_street` | North Water | the same roof, and it is already the other one's only candidate |
| `business_a_wholesale_wine_and_liquor_store_dearborn_street` | Dearborn | 18 roofs show the street a corner SIDE and 0 have their lot on it |

Neither anchor helps: the register reads both addresses as the street and nothing
narrower (`"NORT[H] WATER STREET"`, `"De[a]rborn Stree[t]"`), so there is no landmark to
resolve. `docs/STREET-FACE-ADOPTION.md` names the only two remedies and says neither is
the policy's to take — **an owner ruling that a corner side is a face**, which would move
18 Dearborn roofs and is one number in `tools/fronting_street.py`; or **a reconstruction
that raises frontage on North Water and Dearborn**, which is T-0375's neighbourhood. So
this piece is an owner question before it is a placement, and should be `block --owner`
rather than argued around.

**Acceptance:** either the ruling is asked for and recorded, or the frontage exists and
these three take it. Seating them on a corner-side roof without the ruling is the one
outcome this ticket refuses.

---

## The question, and the numbers it should be answered on (measured 2026-08-29)

**The finding that changes the question: the remedy this ticket was written around
reaches none of its three businesses.** `tools/adopt_street_faces.py` now DEALS each
widened reading instead of counting eligibility, and the deal says:

| ruling | seated | on today's 19 | where the gain lands |
|---|---|---|---|
| lot front only — **in force** | 19 | — | — |
| a corner side is a face | 31 | **+12** | Dearborn +8, La Salle +3, Canal +1 |
| a corner side **or the band** is a face | 32 | **+13** | the same, and North Water +1 |

- **Wm. Sabine** and **John Dave** are on North Water Street, which has **no** side-only
  roof at all — a corner-side ruling does nothing for either. One roof stands in the
  centreline band, so a ruling that also takes the band seats Sabine (the better
  evidenced) and refuses Dave on supply. The band is the weaker reading of the two: it is
  a distance and not an orientation.
- **The Dearborn Street wine store** is refused under BOTH widenings, on supply. Dearborn
  has eighteen roofs showing it a side, of which five are named households' homes and five
  are yard buildings; eight are free and eighteen advertisements want them. The wine store
  is not among the best-evidenced eight.

So the honest statement of the ask has changed shape. It is no longer "rule that a corner
side is a face and these three stand up" — it is two separable questions:

1. **Is a corner side a face?** It is worth **+12 shops** (Dearborn 8, La Salle 3, Canal
   1) and it is a real weakening of the reading: an advertisement's street is where the
   door is, and a roof whose lot fronts Lake does not have a door on Dearborn because its
   gable end reaches it. It seats **none of this ticket's three**. One number in
   `tools/fronting_street.py` changes it.
2. **Is the centreline band a face?** Worth **one** further shop, and that one is Wm.
   Sabine. The weakest of the three readings for the smallest gain.

**The recommendation this run would make, and it is the owner's to take or refuse:** the
answer for all three of these is FRONTAGE, not a widened reading — a reconstruction that
raises roofs whose platted lots face North Water and Dearborn (T-0375's neighbourhood).
Both widenings are available and measured if he wants the twelve.

**What is NOT waiting on him:** the +12 measurement itself is committed and re-derives on
every `check.sh`, so whenever the ruling comes it is applied rather than re-argued.
