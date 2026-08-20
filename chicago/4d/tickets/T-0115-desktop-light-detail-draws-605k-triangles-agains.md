---
id: T-0115
title: Desktop light detail draws 605k triangles against its own 600k ceiling
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-20
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Desktop light detail draws 605k triangles against its own 600k ceiling.

Found 2026-08-20 by the first unfiltered smoke pass to reach the scene-detail checks in
days (chicago-4d-smoke.yml run 32346862982, on T-0060's branch — the staged-gate work,
which changes no geometry): `desktop 1280x800: scene detail 'light' stays inside its own
ceiling — 605414 tris of 600000, 52 calls`. Mobile passes the same check. Less than one
percent over, which is exactly how a ceiling erodes: the recent content merges (boats,
signboards, wharves, approach earthworks, shed-roof gables, clapboard variety) each added
their triangles and nothing re-measured the "light" tier against its budget on desktop.

**Acceptance:** the overage is attributed (which recent layer pushed the tier past its
ceiling on desktop, with counts), and either the light tier draws under 600k again by
trimming what it draws at that level, or the ceiling is consciously re-budgeted in the
same place the 600k figure is set — with the reasoning written down, never silently.
