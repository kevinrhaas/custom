---
id: T-0464
title: Extend the shared south terrain from Madison through Cermak
state: open
epic: SOUTH_TIME
requested_by: owner
seen: false
effort: M
legacy_id: null
opened: 2026-09-01
closed: null
pr: null
claimed_by: null
blocked_on: T-0219
needs_bake: true
---

After T-0219 carries the current 1835 heightfield through Madison, extend the project’s durable geographic frame south far enough to contain the 1812 battle corridor and the Prairie Avenue district: at minimum through modern Cermak/22nd, with a measured buffer so terrain, shoreline and structures do not terminate inside the historical area.

Do not make this a generic flat rectangle. Re-derive the required local-ENU south bound from the project datum, verify whether the present E -320..+1700 width contains the South Branch and historic lakefront over the whole reach, and expand west/east only where evidence requires it. Preserve the current 2.5 m field resolution unless a measured performance/storage reason supports a documented change.

Acceptance: a baked terrain epoch can cover Madison-to-Cermak without out-of-bounds fallback; the exact ENU and modern-street bounds are documented; existing downtown terrain is unchanged within tolerance; and the new field is large enough for both the 1812 and 1880s scene tickets below.
---

**Raised by T-0436, 2026-09-13 — the corporate boundary reaches only to Jackson, and this
ticket goes past it.** The Town of Chicago's limits are now committed geometry
(`data/reconstruction/1835_corporation_limits.json`), resolved from the Trustees' own
survey walk of 7 November 1833. Its south leg is **Jackson Street**. Nothing drawn today
stands south of it, so the boundary is complete for the town as modelled — but this
ticket carries the field to Cermak, 22nd Street, and the moment a building stands down
there, whether the town's by-laws reached it is decided by the extension of **11 February
1835**, which is recorded and NOT resolved: the act's text has not been found in this
corpus, Andreas misprints its year, and Chicago Avenue and Twelfth Street are not
committed as centrelines. See `docs/RESEARCH/corporation_limits.md` § what is still open.
Answer that before this ticket ships a chimney south of Jackson, or the eighteen-inch gate
starts conforming buildings to a by-law that may never have bound them.
