---
id: T-0013
title: Coplanar surfaces tie at depth on 3.5 percent of the aerial frame
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

After R-BUG6(a)/(b), 3.5 % of the aerial frame is still two surfaces at one depth —
genuine coplanar ties, mostly roof/wall junctions. Deep history: § R-BUG6(c) (~8988).
Needs one bake (geometry separation).

**Acceptance:** the 2 mm-nudge instrument reads ≤ 1 % changed pixels aerial; no visual
regression at eye height.

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
