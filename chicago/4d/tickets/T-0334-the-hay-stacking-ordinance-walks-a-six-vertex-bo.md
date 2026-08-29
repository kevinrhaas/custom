---
id: T-0334
title: The hay-stacking ordinance walks a six-vertex boundary round the built town, and nothing draws or tests it
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Section 22 of the ordinance passed **5 August 1835** makes it unlawful to stack hay inside a
boundary the town walks street by street, read under [[T-0335]]
(`chicago_democrat_1835_08_19.json` c006):

> commencing on Washington street at the United States Reservation, and running thence West
> to the intersection of Canal Street, thence North to the intersection of Kinzie Street,
> thence East to the intersection of Wolcott street, thence to Illinois Street, and thence to
> Lake Michigan

Six vertices, every one of them a street this reconstruction already carries, under a penalty
of twenty-five dollars — the heaviest in the whole ordinance except gaming. It is a fire rule,
and that is exactly what makes it evidence: the Trustees drew this line round the ground they
thought was built up densely enough that a hay stack in it would take the town with it.

**This project has no other documented statement of where the BUILT town ended in the scene
year.** Every judgement about density, about which blocks get roofs and which stay open
ground, has been made from the plat, from the deal, and from measured street frontage. This
is the town's own answer, in the town's own words, six weeks after the scene date.

## What it could be worth

- A polygon in `data/`, derived from committed street control the way `datum.json` is derived,
  never hand-typed — with the ordinance claim as its source record.
- A cross-check on the block-infill programme: does the ground the schedule treats as built
  agree with the ground the Trustees fenced? Where they disagree, which is right?
- Possibly something a visitor can SEE, though what that is needs deciding: this is a legal
  boundary and not a fence, and drawing an invisible line as a visible one would be an
  invention that `docs/LIBERTIES.md` would have to carry.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- The boundary is derived from committed street geometry, not typed in, and re-derives under
  `check.sh` the way the datum does.
- The PR states, as a measured number, how many modelled structures stand inside it and how
  many outside, and names every disagreement with the block-infill programme's own idea of
  the built town.
- Nothing is drawn in the scene without a stated decision about what a legal line may look
  like; if something IS drawn, `docs/LIBERTIES.md` carries it.
