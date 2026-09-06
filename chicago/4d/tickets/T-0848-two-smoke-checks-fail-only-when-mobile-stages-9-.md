---
id: T-0848
title: Two smoke checks fail only when mobile stages 9-12 run together — the facade-tone and shadow-reach sensitivity deltas collapse in a combined range
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-05
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Two smoke checks fail only when mobile stages 9-12 run together — the facade-tone and shadow-reach sensitivity deltas collapse in a combined range.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

`SMOKE_VIEWPORT=mobile SMOKE_STAGE=9-12 node tools/smoke_renderer.mjs --published` fails
two checks, and the SAME two, on a pristine `origin/dev` at b77b1ae14 as on a branch that
touches only resident JSON:

    FAIL  the facade tones reach the render — winding the tone off changed 370
          structure(s) (want >=300) and moved the worst cell by 2, mean 0.01
          (need worst>=3, mean>=0.03)
    FAIL  the shadow reach reaches the render — winding ±120 m back to ±60 m moved
          the worst cell by 2, mean 0.00 (need worst>=4)

Run each of those stages ALONE and every one of them passes — 9 (23/0), 10 (32/0),
11 (22/0), 12 (67/0), 128 staged checks between them and no failure. Only the combined
range fails, and it fails on both trees, so it is not a finding about either.

Both failing checks are DELTA measurements: they wind a knob off, re-render, and assert
that the frame moved by at least so much. What moves that measurement is what the camera
is looking at when it is taken, and a combined range reaches the section with a page that
has already walked through three other stages' worth of interaction. So the likely fault
is that the delta section does not restore the view it measures from, and the assertion
silently becomes an assertion about wherever the previous stage left the camera.

WHY IT MATTERS BEYOND THE NOISE: `tools/smoke_budget.mjs --for-diff` prints combined
ranges, because that is what fits under the foreground ceiling. So the shape the budget
tool tells every run to use is the one shape these two checks cannot survive, and every
run that takes the advice meets a red it did not cause and has to spend its remaining
budget proving whose it is. This one spent three extra legs and a second checkout of dev.

**Acceptance:** the two checks either pass in a combined range or state, in the check
itself, the view they require and take it — and `--for-diff`'s advice stops producing a
red on an unchanged tree. A reading filed with `dev-smoke-state.mjs` (2026-09-06, both
trees) is the evidence.
