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

---

## Measured again on T-0005's merge, 2026-08-20 — and the sloughs are 9.3k of it

Running the desktop stages against the sloughs branch before merging it (the run that
built it left stage 4 and desktop unrun):

| tree | light tier, desktop |
|---|---|
| dev `48f8c21` | **605,414** tris of 600,000 — 5,414 over |
| this branch (T-0005 carved) | **614,679** tris of 600,000 — 14,679 over |

So the carved swales add **~9,265 triangles** to the light tier and take the overage from
0.9 % to 2.4 %. That is not a new failure — the tier was already red on dev, which is why
this ticket exists — but it is the first attributed contributor, and this ticket's
acceptance asks for exactly that: *"which recent layer pushed the tier past its ceiling
on desktop, with counts"*.

Worth noting for the repair: the terrain is ONE mesh whose density is set by the bake's
`--decimate-deg` (T-0005 used 0.031, a 3 mm fit). So the sloughs' contribution is
adjustable at the bake without touching the carve — a shallower decimation of the terrain
buys the tier back, and the swales stay where the 1833 map puts them.

T-0005 was merged with this recorded rather than held: the ceiling was already breached,
the geometry it adds is owner-requested content, and hiding a 9.3k contribution inside a
figure nobody had attributed would have been the worse outcome.
