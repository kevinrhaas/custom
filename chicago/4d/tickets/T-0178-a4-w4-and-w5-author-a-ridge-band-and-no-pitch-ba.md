---
id: T-0178
title: A4, W4 and W5 author a ridge band and no pitch band, so nothing can choose a pitch that reaches it
state: open
epic: TOWN
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0148
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

A4, W4 and W5 author a ridge band and no pitch band, so nothing can choose a pitch that reaches it.

Piece 5 of 5 of **T-0148 — The A1 stable cannot reach its ridge band at any pitch its family allows**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** a stated decision, carried out, for the three families that author a `ridge_ft`
band and no pitch band — A4 (`gable or shed`, ridge 9-13), W4 (ridge 16-27) and W5 (ridge 20-29).
Either the pitch is derived FROM the two bands the family DOES author (the ridge band and the
eave band bound it, so a pitch inside those bounds is a reconstruction with something behind it)
and the roofs move; or the answer is that the ridge column does not describe how these archetypes
set a roof out, recorded in `docs/LIBERTIES.md` and the three families exempted BY NAME in
`tools/measure_ridge_band.py` rather than by silence. Never by weakening the ridge band.

**Why.** Measured 2026-08-24 under T-0148: 8 of the 59 offenders sit on these three families, and
they are the only ones the sampler cannot argue about. `family_bands.pitch_deg` returns the
generator's type default unchanged where the family authors no `N:12-M:12` band — deliberately,
because inventing a pitch claim the specification does not make is the fault it exists to avoid —
so a default of 32 deg (or 18 deg on a shed) meets a ridge band nothing steered it toward, and
`inf_gunsmith_shop` lands 4.28 ft under its band. This is the one group where a claim really may
have to give way, which is why it is its own ticket.
