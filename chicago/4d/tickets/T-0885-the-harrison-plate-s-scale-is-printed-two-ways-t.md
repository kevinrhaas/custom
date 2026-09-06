---
id: T-0885
title: The Harrison plate's scale is printed two ways: the source record says 1.06 ft/px (0.32 m/px) and docs/RESEARCH/fort_dearborn.md says 1.10 (0.335) — a measurement between two committed buildings says 0.330
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The Harrison plate's scale is printed two ways: the source record says 1.06 ft/px (0.32 m/px) and docs/RESEARCH/fort_dearborn.md says 1.10 (0.335) — a measurement between two committed buildings says 0.330.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

FOUND BY T-0881 WHILE RE-ESTABLISHING THE READING FRAME. The plate this project takes Fort
Dearborn off carries no scale bar, so the scale is derived — and the derivation is printed
twice with two different answers:

| where | figure |
|---|---|
| `data/sources/harrison_1830_river_mouth.json` note | "about 1.06 feet per pixel … 0.32 m/px" |
| `docs/RESEARCH/fort_dearborn.md` § 3 | "**1.10 ft per pixel** … (0.335 m/px)" |

The same two texts also disagree on one of the two cross-checks the derivation rests on: the
gap between the west and east ranges comes out **74 ft** on the source record and **71 ft** in
the research doc, both against the same 80 ft from the 1855 photograph key.

T-0885's own measurement, made for T-0881 and recorded on
`fort_dearborn_wash_house.drawn_1830.position`: the ink centroids of the guard house and store
house symbols stand 42.96 px apart on the page image, and the two committed records stand 14.19
m apart, which is **0.330 m/px**. That is 1.5 per cent off the research doc and 3 per cent off
the source record, so the doc is the better of the two and neither is exactly right.

It changes nothing already committed — every fort position was read at whatever the reader
used, and the anchor absorbs a constant — but it is a documented number that disagrees with
itself, and the next person to place something off this sheet has to pick one.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- One figure, in both places, with the derivation that produces it written once and cited from
  the other.
- The 74-versus-71 ft cross-check is settled the same way.
- If the settled figure is not the 0.335 the committed fort positions were read at, the note on
  every affected record says so, and nothing is silently re-scaled.
