---
id: T-0060
title: The smoke's mobile half no longer fits the runner's ten-minute command ceiling
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-18
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The smoke's mobile half no longer fits the runner's ten-minute command ceiling.

**Measured 2026-08-18 on T-0036's run**, serving the published mirror:
`SMOKE_VIEWPORT=mobile` was killed at 570 s having reached **208 passed / 2 failed**;
`SMOKE_VIEWPORT=desktop` was killed at 570 s at **143 passed / 0 failed**. ROADMAP § THE RUN
BUDGET records the last measurement, 2026-08-15: mobile finished in **4 m 43 s** at 214
assertions and only the desktop half overran. The suite has since grown past 300 assertions per
viewport, so **neither half fits any more** — and the assertion that goes unrun is always the same
one, because `zero page errors` is the LAST line of each viewport. A run can now merge without
ever having been told whether the page threw.

That section already names the durable fix: *"the smoke should take a test-name or section filter
the way it takes `SMOKE_VIEWPORT`, so the desktop half can be run as two commands that each fit."*
It is now the mobile half too, and it is load-bearing rather than a convenience.

**Acceptance:** `tools/smoke_renderer.mjs` takes a section or name filter (alongside
`SMOKE_VIEWPORT`, and saying out loud that a filtered run is not the gate, exactly as that flag
does), the page-error assertion is taken in EVERY filtered run rather than only in the tail, and
one run demonstrates the full mobile gate completing as two commands that each finish inside ten
minutes with the same total assertion count as an unfiltered pass. Update ROADMAP § THE RUN BUDGET
with the new measurements in the same PR.
