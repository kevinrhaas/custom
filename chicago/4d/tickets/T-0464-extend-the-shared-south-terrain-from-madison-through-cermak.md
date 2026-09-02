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