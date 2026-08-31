---
id: T-0448
title: 2,693 drawn flower heads stand over nothing — dev's full smoke has been red on it since 2026-08-30 and every PR inherits it
state: open
epic: FLORA
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: null
opened: 2026-08-31
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

`tools/smoke_renderer.mjs` asserts *"every drawn flower head has a plant under
its own stalk"*. It fails, and it is failing on `dev` itself:

```
FAIL  desktop 1280x800: every drawn flower head has a plant under its own stalk
      2693 of 18893 drawn heads over 40 poses had nothing under the foot of
      their own stalk; worst flora-head-corymb at from_above 270deg,
      foot 0.36 m, 0.36 m over its base over open ground
```

**14.3% of drawn flower heads are floating.** A visitor at a desktop viewport,
looking down from above, sees flower heads over open ground with no plant
beneath them.

## It is dev's, not any branch's — the two runs agree to the digit

| run | commit | date | result |
|---|---|---|---|
| `dev` full smoke | `54921610` | 2026-08-30 | 2693 of 18893, worst `flora-head-corymb` at from_above 270deg, foot 0.36 m |
| PR #560 `smoke (desktop, 10-13)` | `ab4dad40` | 2026-08-31 | 2693 of 18893, worst `flora-head-corymb` at from_above 270deg, foot 0.36 m |

Same count, same pose, same worst offender. No branch introduced it.

## Why it went unnoticed, which is the part worth fixing

The per-PR `gate` does not drive a browser, and the staged smoke only runs the
desktop 10-13 leg on some branches. So a fault that has been live on `dev` for
at least a day was invisible to every PR that did not happen to run that leg —
and when it did surface, it surfaced as *that PR's* failure. #591 fails
`smoke (desktop, 10-12)` and #432 fails five legs; both should be re-read against
this ticket before anyone concludes their own work is at fault.

## What is known about the mechanism

The assertion builds a one-metre grid of every rooted plant, then for each drawn
head looks in the nine cells around the foot of its stalk for a plant whose top
reaches it, allowing `SLACK`. `best === -Infinity` means **no plant at all** in
those nine cells — not a plant that is too short. The reported worst case is
`0.36 m over its base over open ground`, so heads are being drawn where the
instance that should carry them is not being drawn.

That points at the fade/ring ramp — `fadeOf(...)` and `aChiRing` decide WHETHER a
plant is drawn at a given distance from the camera, and T-0035's note above the
check says the ramp is *coverage, not height*, and that a plant is drawn whole or
not at all. A head surviving a ramp its own stalk did not would produce exactly
this. **Unverified — that is the first thing to test, not the answer.**

## MERGED RED, ON THE OWNER'S DECISION — 2026-08-31

PR #560 was merged into `dev` with this assertion failing, on the owner's
explicit instruction, because it is 900 of 901 green and the one failure is
inherited from `dev` rather than caused by the branch. Recorded here so the
exception is visible rather than silent, which is the whole reason this ticket
exists as well as the fix.

**Acceptance:**

1. The mechanism is demonstrated, not guessed: a reproduction that shows WHY a
   head is drawn when its own plant is not.
2. The count goes to **zero** heads over nothing. Not reduced — zero. A head
   with no plant beneath it is a drawing this project cannot defend.
3. The assertion is not weakened, its `SLACK` is not widened, and the pose list
   is not trimmed to avoid the failing view.
4. `dev`'s full smoke is green on `desktop 10-13` afterwards, verified on `dev`
   and not only on the branch.
5. #591 and #432 are re-read against the result — if their smoke failures were
   this fault, they are unblocked by the fix rather than by their own work.
