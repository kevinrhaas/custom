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
claimed_by: run 8/29/2026, 4:31:19 PM CT
blocked_on: Is a corner side a face? MEASURED, not estimated: the ruling seats 12 of the 24 businesses that ask (Dearborn 8 of 18, La Salle 3, Canal 1) — 16 of the 29 side-on roofs are homes or yard buildings and stay refused however the face is read. It seats NONE of this ticket's three storefronts: North Water has no corner-side roof at all, so Wm. Sabine and John Dave are untouched by it, and the Dearborn wine store falls outside the 8 free roofs its 18 rivals compete for. The second candidate — a centreline band is on the face — seats exactly 1: Sabine takes North Water's single off-grid roof and Dave is then short of supply. So the three want three different things, and only new frontage on North Water and Dearborn (T-0375's neighbourhood) seats all three. Which, if either, do you rule?
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
