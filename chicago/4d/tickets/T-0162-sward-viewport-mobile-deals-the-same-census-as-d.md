---
id: T-0162
title: SWARD_VIEWPORT=mobile deals the same census as desktop: the viewport does not reach the ring sizes
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-23
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

SWARD_VIEWPORT=mobile deals the same census as desktop: the viewport does not reach the ring sizes.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found by T-0018 while measuring the sward census at both viewports. `tools/measure_sward_draw.mjs`
opens the page at 390x780 when `SWARD_VIEWPORT=mobile` is set, and its own header says *"the
viewport decides the ring sizes and therefore how many slots a station deals, so the census has to
be answerable at both"*. It is not answerable at both: the two runs deal **identical** censuses,
row for row, 7,844 slots either way.

The reason is that `flora.js` sizes its rings off `tune`, which comes from `mergeTune(lowSpec &&
detail === 'full' ? 'light' : detail)` — and `lowSpec` is the DEVICE guess, not the page size, so a
desktop Chromium at a phone's viewport is still `full`. The phone's ring sizes are reached by the
device guess or by an explicit `detail`, and the env var reaches neither.

**Acceptance:** either the tool drives the thing that actually changes the ring sizes and the two
runs are shown to differ, or the flag and its header claim are removed so nothing reads a mobile
figure that is a desktop one. Whichever is chosen, no measurement is left claiming a viewport it
did not stand at.

**Links:** `tools/measure_sward_draw.mjs` (the `VIEWPORT` const and its comment) ·
`renderers/web/js/flora.js` (`mergeTune`, `lowSpec`) · T-0018.
