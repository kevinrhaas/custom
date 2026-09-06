# Kinzie Street's alignment, and the two readings that disagreed by 23 m

**T-0812.** Two readings of the same street stood in this repository at once, and one of
them was carrying a building. `data/streets/1835.json` runs `kinzie` through
`[-320, 263.1]`, `[-181, 262]`, `[1100, 251.8]` in local ENU metres. The placement note
in `data/structures/steamboat_hotel.json`, written 2026-08-11, says instead:

> the Kinzie Street alignment runs due east at local N +276

At local E +968 — the easting the Steamboat Hotel was placed against — the committed
record is at **N +252.85** and the prose at **N +276**. **23.15 m apart**, and the
difference was load-bearing: the hotel stood at `[968, 291]`, which is 15 m north of the
prose line it was placed against and **38.15 m north of the committed one**, on the far
side of Kinzie Street from the river, for a house both sources put *on North Water
Street*.

## The ruling: the committed line, and it is not a close question

`data/traces/street_control.json` holds one control point on this street,
`control.kinzie_canal` — Kinzie × Canal, read from OpenStreetMap under the table's own
`node_rule`. Its `queued_correction` entry, written 2026-08-10, records that two of its
five nodes are the **Kinzie Street bikeway**'s crossing of Canal rather than the
roadway's, and states what the road-only reading is:

> the other three nodes, whose mean is E 446891.71, N 4637657.80

On this project's datum (`origin_utm_e` 447072.7, `origin_utm_n` 4637395.8) that mean is
local **E −180.99, N +262.00**. The committed `kinzie` polyline's second vertex is
`[-181, 262]`. **The committed line passes through the roadway control to a centimetre**,
and the street table says of this street that it is "one of the streets that survives on
its 1835 alignment".

The prose reading has no control behind it at all. It is an eyeball of the Wright 1834
sheet recorded in a paragraph; the phase that carries it declares
`derivation.method: "not_derivable"`; and at the control's own easting it would put
Kinzie at N +276 against a measured N +262 — **14 m north of a modern junction on an
alignment that has not moved**. It is also wrong in bearing: it says "due east", and the
committed line runs 90.46°, a fall of 10.2 m of northing across 1281 m of easting.

So: **the committed `kinzie` record is right and the hotel's prose alignment is wrong.**
`geometry_confidence` on that record is `attested` from the Thompson plat under the
owner's ruling of 2026-09-04 (T-0713), and T-0451 has since re-platted the North Division
around it. Nothing in this ticket moves the street.

## The two readings never disagreed about the convergence

Worth stating, because it is why the error survived a year of reading. North Water
Street's east end is derived (T-0447) as the crossing of the committed bank's offset
curve with the committed `kinzie` line, at **E +973.6, N +252.9**. The hotel's own note
independently puts that convergence at "roughly local E +990" — 16.4 m east, inside the
±20 m the note itself claims. The two readings **agree about where North Water Street
meets Kinzie Street** and disagree only about the **northing it happens at**. A reader
checking the easting would have found nothing wrong.

## What the ruling cost the hotel, and what it bought

The building moves 51.7 m south-south-west onto the committed corridor: see
`data/structures/steamboat_hotel.json`, whose placement note carries the new rule. The
visible consequence recorded on T-0812 — `tools/generate_business_signboards.py` refusing
the Steamboat Hotel a post board because no street lay within `STREET_REACH_M` of the
wall it would stand in front of — was a true statement about the committed records and
goes away when the building stands on them.
