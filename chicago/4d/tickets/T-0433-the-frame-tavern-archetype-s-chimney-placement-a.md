---
id: T-0433
title: The frame_tavern archetype's chimney placement assumed a ridge direction the roof generator does not always take, and no other archetype was checked for the same assumption
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The frame_tavern archetype's chimney placement assumed a ridge direction the roof generator does not always take, and no other archetype was checked for the same assumption.

Found by T-0333, which measured every stack in the town against the eighteen inches
the ordinance of 5 August 1835 requires and the four feet Andreas says no chimney in
this town exceeded. Nine stacks on five buildings stood over four feet — up to
**3.217 m** on the Western Hotel — and all nine were `frame_tavern`'s `frontage`
placement, which spaced its stacks across the frontage **at the depth midline**
regardless of which way the roof runs. The roof above it is built
`ridge_along_x=(w >= d)`, so on a block deeper than it is wide the depth midline is a
slope and not the ridge, and the stack breaks the roof a third of the way down it while
still rising to `ridge_z + 0.55`. T-0333 fixed that one branch: it now turns with the
ridge, exactly as the `gable_ends` branch beside it always has, and on a block at least
as wide as it is deep the two expressions are identical, so the six taverns that were
already right rebuilt byte for byte.

**What was NOT fixed, and is the reason for this ticket.** Three other archetypes make
a placement decision against an axis the roof generator chooses separately, and nothing
checks that the two agree:

- `log_dwelling._stack` stands its stacks against the **±x faces** unconditionally,
  while `log_dwelling._ridge_along_x(x0, y0, x1, y1)` puts the ridge along whichever
  axis is longer. On a cabin deeper than it is wide the ±x faces are the EAVE walls, so
  the stack the docstring describes as standing "against the log core's -x gable" —
  the frontier arrangement, built outside the wall so a stick-and-clay flue can be
  pulled down when it fires — is standing against the long side instead.
  `harmon_log_cabin` is 6.096 m by 7.925 m and is one of these. This costs no HEIGHT
  (all 47 log stacks measure 0.720 m above their own roof shell's ridge) so T-0333's
  gate is green on it; what it costs is that the prose and the geometry disagree.
- `fort_structure._chimneys` spaces across the width while its roof is
  `ridge_along_x=(x1 - x0) >= (y1 - y0)`, the same shape of assumption.
- `frame_storefront` alone asks `_ridge_along_x(p)` in its own `_chimneys` and is the
  archetype that got this right; it is the model for the other two.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- Every archetype that places a stack reads the SAME ridge decision its own roof was
  built with, or states why it does not, and `frame_storefront`'s shape is the one
  adopted rather than a fourth spelling of it.
- The census in `tools/measure_stove_pipe_ordinance.py` is extended, or a companion
  measurement is added, so that a stack standing against a wall the archetype's prose
  calls a gable and the roof calls an eave is REPORTED — the height gate cannot see
  this class, which is why it survived.
- Every building whose stack moves is rebaked in the same commit, and the count that
  did NOT move is stated, the way T-0333 stated its six.
- No confidence is upgraded and `docs/LIBERTIES.md` L26 continues to own the
  arrangement; this is the archetype keeping its own stated promise, not a new claim.

**Links:** T-0333 (the ordinance, the census and the fix to the tavern branch) ·
T-0137 (the last time an archetype was left behind by a town-wide stack repair) ·
`docs/LIBERTIES.md` L26.
