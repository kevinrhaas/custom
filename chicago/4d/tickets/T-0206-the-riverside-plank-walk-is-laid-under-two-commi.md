---
id: T-0206
title: The riverside plank walk is laid under two committed wharf decks
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The riverside plank walk is laid under two committed wharf decks.

**Acceptance:** the riverside plank walk no longer has any part of its band inside a committed
wharf deck's outline — either because the march refuses the stretch a deck stands on, the way it
already refuses the stretch a WALL stands on, or because a measured argument says the two may share
that ground and says why. The refusal is recorded per stretch on the record like every other, the
frontage census moves with it, and both gates stay green.

**Found by T-0204**, which made the wharf decks walkable and so made a fault that had been true and
invisible show up as a wall. `river_plank_walk_wharf_reach` — the riverside walk's last reach, from
the La Salle mouth west along the swinging bank — is laid straight across the landward heels of two
committed dock decks:

| deck | plank walk under it |
|---|---:|
| `carpenter_south_water_store__wharf` | **3.75 m** of a 1.83 m-wide band, and its CENTRELINE for 2.5 m |
| `h_jones_store__wharf` | **1.58 m**, on the walk's river-side edge only |

Two committed floors on one piece of ground, at two heights: the walk lies on the bank at about
0.40 m and each deck holds the record's 0.90 m freeboard floor over it. Nothing in the repo asked
the question — `tools/generate_frontage_works.py`'s march refuses every step a WALL stands on, and a
dock deck is the other committed thing standing on that bank.

**What it costs a visitor today.** Walking the reach westward the walker used to pass through the
timber, because a deck was drawn and not solid. Since T-0204 it is solid, so they stop at Carpenter's
landing (local E 389.6) against a 0.62 m step the 0.35 m rule refuses, and the 26 m of walk beyond it
is reached AROUND the dock on the street side rather than along the bank. Stopping at a dock is the
truthful behaviour of the two; being laid under one is not, and that is what this ticket is.

**Do not confuse it with T-0205.** That one is the step from bank to deck at every landing, which is
terrain and needs a bake. This one is a walk drawn on ground a deck already holds, which is the
frontage generator's own rule and needs no bake. They meet at Carpenter's landing and nowhere else.

**Banked in the meantime.** `tools/smoke_renderer.mjs` asserts that exactly two decks carry plank
walk under them, names them, and holds each under 5.0 m — so the fault cannot spread to a third
landing or grow at these two while nobody is looking.

**Links:** T-0204 (which found it) · T-0205 · T-0069 / T-0119 (the walk) · T-0041 (the wharves) ·
`data/frontage/river_walk_frontage.json` · `tools/generate_frontage_works.py`.
