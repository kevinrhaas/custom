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
pr: 566
claimed_by: run 8/29/2026, 4:23:56 PM CT
blocked_on: Is a CORNER SIDE a face? May a documented shop take a reconstructed roof whose platted lot fronts a DIFFERENT street, because its gable end reaches the street its advertisement names? Costed with 'python3 tools/adopt_street_faces.py --what-if' and written up in docs/STREET-FACE-ADOPTION.md § The two widenings, COSTED. A yes seats +12 advertisements (19 -> 31) and puts twelve documented doors on a building whose front is on another street; a no leaves 24 waiting. NOTE, because it changes the ask: the widening does NOT seat this ticket's own three. Every roof it adds already fronts another street by its lot, so it adds no supply and only lets two faces deal one roof — Dearborn's 18 advertisements would compete for 8 roofs and the anonymous wine store is not among the 8 the evidence ranking serves; North Water has no corner side at all, so only a further widening to the 25 m centreline band reaches it, and that is one roof for Sabine AND John Dave. Closing these three needs the other remedy instead: a reconstruction that raises frontage on Dearborn and North Water (T-0375's neighbourhood), which costs this policy nothing because the pass re-derives.
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
