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

## Attributed 2026-08-20: T-0005's carve is 9.3k of it

Measured while landing PR #273, running the desktop stages that run had left unrun:

| tree | light tier, desktop |
|---|---|
| dev `48f8c21` (before the sloughs) | **605,414** tris of 600,000 — 5,414 over |
| the sloughs branch | **614,679** tris of 600,000 — 14,679 over |

The carved swales add **~9,265 triangles** and take the overage from 0.9 % to 2.4 %. Not
a new failure — the tier was already red, which is why this ticket exists — but it is the
first attributed contributor, which is what the acceptance above asks for.

**A lead for the repair, from the same measurement:** the terrain is ONE mesh whose
density is set by the bake's `--decimate-deg` (T-0005 used 0.031, a 3 mm fit). The carve's
share is therefore adjustable at the bake without moving a swale — the sloughs stay where
the 1833 map puts them and the tier can still be bought back.

The rest of the overage predates this and is still unattributed: the recent content merges
(boats, signboards, wharves, approach earthworks, shed-roof gables, clapboard variety) are
the candidates, and each is measurable the same way — bake at a known commit, read the
light tier, difference it.

Full stage sweep on the merged tree, for the record: mobile 1/2/4 PASS, mobile 3 = T-0114's
two known road failures; desktop 1/4 PASS, desktop 2 = this ticket, desktop 3 = one of
T-0114's two. No failure outside the two open tickets.

**Measured worse by T-0083, 2026-08-20:** the Green Tree's corrected fabric adds ~310
triangles on top of the above. Still under one percent of the tier by itself; the
attribution method stands unchanged.

**Measured worse by T-0074, 2026-08-20:** the dooryard plantings add ~43k scene
triangles at the light tier — 66 trees at ~433 each and 59 currant clumps at ~164 each
(the clump archetype was cut from 685 to ~164 during the same work, saving ~31k) — so
desktop light now reads 648,404 of 600,000 (was 605,414). Mobile light stays under its
own ceiling at 582,479, measured by the release smoke. Attribution for the trim: the
dooryard layer draws at every level today and is the natural first candidate for the
keep discipline the dealt wood already follows.
