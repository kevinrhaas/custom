---
id: T-0013
title: The interior flicker — 624 px where structures and trees fight themselves
state: open
epic: RENDERING
requested_by: loop
seen: false
effort: M
legacy_id: R-BUG6(c)
opened: 2026-08-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
---

**RE-AIMED 2026-08-23 on the owner's ruling** ("re-aim it at the interior flicker",
both layers, as one ticket). What this ticket asked for before is preserved below,
along with the measurement that retired it, because the original framing was wrong in
a way worth keeping visible.

Under a 2 mm camera nudge from `from_above`, 705 px of the aerial frame are **interior**
flicker — a layer fighting ITSELF, as opposed to the silhouette between one layer and
the next, which is what any camera does to any edge and is not a defect. Two layers own
624 of those 705:

| layer | interior px | worst interior cell | silhouette px | total flicker |
|---|---|---|---|---|
| **structures** | **367** | 60 | 180 | 547 |
| **trees** | **257** | 44 | 345 | 602 |
| ground | 71 | 30 | 369 | 440 |
| streets | 8 | 20 | 10 | 18 |
| water | 2 | 8 | 36 | 38 |

**Nobody has asked WHY yet.** `measure_tie_class.mjs` answers *which layer owns a
flickering pixel* — it does not answer what is fighting inside it. The exact-depth-tie
hypothesis is already dead (25 px, see below), so the mechanism for both layers is
genuinely unknown and is the first thing to establish. Candidates worth ruling in or
out rather than assuming: self-overlap within a batched layer, alpha-tested foliage
cards crossing each other, LOD or billboard reorientation under the nudge, normal-map
or specular aliasing on near-tangent faces, and shadow-acne inside the layer's own
geometry — though R-BUG6(a) already took the shadow map out of this measurement.

**Sizing.** This is one ticket by the owner's ruling, and its FIRST demonstration is the
diagnosis: name the mechanism for each layer with evidence, not by analogy. If the
repair that follows is not small for either layer, `ticket.mjs split` it at that point
rather than shipping a self-invented "(1/2)" — that is the house rule and this ticket
is a likely candidate for it.

`needs_bake` is left `true` because a structures-side repair may well move geometry;
the diagnosis itself does not need a bake.

**Acceptance**, and none of it may be met by weakening an instrument:

1. The mechanism is **named per layer, with evidence** — a measurement or a controlled
   toggle that distinguishes the cause from its neighbours, in the manner of the
   LessEqual→Less switch that killed the depth-tie hypothesis in 25 px.
2. For each layer actually repaired, its **interior** count falls by at least half
   (structures 367 → ≤ 184, trees 257 → ≤ 129), read off `measure_tie_class.mjs` at
   `from_above`, with the run's own control and return-to-pose both reading **0 px**.
3. **Silhouette is explicitly out of scope.** A change that reduces the total by
   smoothing edges between layers has not fixed this and does not count.
4. No visual regression at eye height, and no page errors at either release viewport.
5. If a layer's interior flicker turns out to be irreducible, that is a legitimate
   outcome — recorded with the measurement that shows it, not quietly dropped.

---

## The original ticket, and the measurement that retired it

> After R-BUG6(a)/(b), 3.5 % of the aerial frame is still two surfaces at one depth —
> genuine coplanar ties, mostly roof/wall junctions. Deep history: § R-BUG6(c) (~8988).
> Needs one bake (geometry separation).
>
> **Acceptance:** the 2 mm-nudge instrument reads ≤ 1 % changed pixels aerial; no visual
> regression at eye height.

---

## MEASURED 2026-08-22 — the premise above is wrong, and the acceptance is already met

`measure_tie_class.mjs` could not be run by anyone until T-0153 fixed it (it was one of
twelve instruments that could not be pointed at a browser). Run against the published
mirror the moment it worked, `from_above`, 1280×800, 2 mm nudge:

```
the frame flickers on 1984 pixels of 1024000          =  0.19 % of the frame

layer          footprint px   its flicker   share    INTERIOR   silhouette
structures            21304           547   27.6 %        367          180
trees                 61724           602   30.3 %        257          345
ground               712203           440   22.2 %         71          369
unattributed              -           333   16.8 %
water/streets/flora        -            62    3.1 %

INTERIOR TOTAL: 705 of 1984 (35.5 %) — where a layer fights ITSELF
EXACTLY CO-PLANAR (LessEqual → Less across all 22 materials):
  the switch moves    36198 px of the frame
  of which flickering    25 px   ← 1.3 % of the flicker, 0.0024 % of the frame
  of which interior       9 px
control (same pose twice): 0 px · return to base pose: 0 px
```

Three things follow, and they change what this ticket should be:

1. **The 3.5 % figure is not what the frame does.** Flicker is 0.19 % of the aerial
   frame, so the stated acceptance — *≤ 1 % changed pixels aerial* — is met by a factor
   of five, and was met before any work was done. That number appears to have been
   carried forward as an estimate and never re-measured.
2. **Exactly-coplanar ties are 25 pixels.** The depth-function switch is an exact test
   for "two surfaces at the same depth", and it moves 25 of the 1,984 flickering pixels.
   The geometry separation and the bake this ticket asks for would be spent on 0.0024 %
   of the frame.
3. **Two thirds of the flicker is silhouette**, which is what any camera movement does
   to any edge and is not a defect. The genuine interior share — where a layer fights
   ITSELF — is 705 px, and it is owned as follows:

   | layer | interior px | silhouette px | total flicker |
   |---|---|---|---|
   | **structures** | **367** | 180 | 547 |
   | trees | 257 | 345 | 602 |
   | ground | 71 | 369 | 440 |
   | streets | 8 | 10 | 18 |
   | water | 2 | 36 | 38 |

   So the ticket's instinct about WHERE was right: `structures` is the largest interior
   owner, and roof/wall junctions are inside it. What the ticket got wrong is the
   magnitude (0.19 %, not 3.5 %) and the mechanism — these are not exact depth ties, so
   separating geometry is not the lever.

   (An earlier revision of this note named **trees** as the largest interior owner. That
   was wrong: trees lead on TOTAL flicker at 30.3 %, structures lead on INTERIOR at 367
   px. Corrected here against a second run of the instrument, which reproduced the
   partition exactly.)

Nothing here was changed to make a check pass; the control and the return-to-pose both
read 0 px, so the partition is sound.
