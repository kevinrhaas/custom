---
id: T-0148
title: The A1 stable cannot reach its ridge band at any pitch its family allows
state: open
epic: TOWN
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-22
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The A1 stable cannot reach its ridge band at any pitch its family allows.

Found by T-0145's new instrument, `tools/measure_ridge_band.py`. It models every reconstructed
roof's ridge from the archetype's own roof arithmetic and reads back the ridge the committed GLB
carries; the two agree on all 257 records, and **104 of those roofs stand outside the `ridge_ft`
band their family authors** — banked in `tools/ridge_band_baseline.json`.

Most of that is not a sampling error and cannot be repaired by moving a pitch. Three committed
claims disagree, and the disagreement is structural:

- the crosswalk's **footprint band** (how wide and deep the family is),
- the crosswalk's **pitch band** (`roof`, e.g. A1's `7:12-10:12`),
- the crosswalk's **ridge band** (`ridge_ft`, e.g. A1's `17-24`),

plus a fourth thing the crosswalk does not author at all: **which way the archetype points the
ridge.** `outbuilding` runs a gable down the LONG axis, so the roof climbs half the SHORT one, and
an A1 stable drawn inside its own footprint band tops out around 15-17 ft at the steepest pitch A1
allows. Thirteen A1 roofs are banked low for exactly that reason; the D3/D4/D5/D6 groups are banked
HIGH for the mirror of it.

**This is an owner-facing question, not an agent repair.** Satisfying the ridge band means giving up
one of the other three — widening the pitch band, widening the footprint band, or turning the
archetype's ridge — and each is a change to the specification or to a shared generator, not to a
parcel. T-0145 deliberately declined to leave the pitch band to reach the ridge band, on the ground
that satisfying a gate by disobeying the other committed claim is not a repair.

**Acceptance:** for each family group in `tools/ridge_band_baseline.json`, a stated decision about
which of the four claims gives way, carried out and the baseline shrunk accordingly — or, where the
answer is that the specification's ridge column simply does not describe how this project's
archetypes set a roof out, that recorded in `docs/LIBERTIES.md` and the affected families exempted
by name rather than by silence. Gates green, and the baseline smaller than 104 or explicitly
argued to be the wrong instrument.

**Links:** T-0145 (opened this) · T-0144 · L166 · `tools/measure_ridge_band.py` ·
`tools/ridge_model.py` · `tools/ridge_band_baseline.json` ·
`data/reconstruction/1835_family_archetype_crosswalk.json`.
