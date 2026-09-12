---
id: T-1081
title: The smoke's walking-speed assertion still expects a bare '3.2 mph' and the HUD has read 'walk · 3.2 mph' since T-0823, so mobile part 3 has been red on dev for a week
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-12
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The smoke's walking-speed assertion still expects a bare '3.2 mph' and the HUD has read 'walk · 3.2 mph' since T-0823, so mobile part 3 has been red on dev for a week.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

FOUND BY T-1079's smoke leg, 2026-09-12. `tools/smoke_renderer.mjs` line 8315 asserts
`/^\d+(?:\.\d)? mph$/` on `#v-speed`. Since T-0823 landed the per-pace sliders on
2026-09-05 (167cdc176), `hud.js` paints that element through `gaitReadout('walk')` and it
reads **`walk · 3.2 mph`** — which is the shipped, intended UI. So the UNIT is right and
the ASSERTION is stale: mobile part 3 has been failing on dev for a week for a reason that
is not a defect in the product.

**Acceptance:** the assertion accepts the gait prefix and still refuses `m/s`, the gait
word itself is asserted rather than dropped (the readout naming the gait is the whole of
T-0823), and the same staleness is checked for on the wagon and horse readouts before this
closes — three sliders landed together and only one of them is asserted on.

REPRODUCED BY T-1070, 2026-09-12, on both viewports, running the smoke legs that cover a
street diff:

    mobile 390x780:   FAIL  walking speed is presented in miles per hour — speed label walk · 3.2 mph
    desktop 1280x800: FAIL  walking speed is presented in miles per hour — speed label walk · 3.2 mph

So it is not mobile-only. Every other check in every leg that run passed, which is worth
saying because it makes this one assertion and not a broken part.

And one consequence beyond the count of red parts: this assertion sits on the group that
covers `data/streets/1835.json`, so EVERY run that touches a street line draws a red leg
it must read, attribute and argue past before it can merge. T-1070 spent a leg doing that.
A gate that is red for a reason unrelated to the diff in front of it stops being a gate.
