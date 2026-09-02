---
id: T-0467
title: Add south-scene camera anchors, navigation and map extents
state: open
epic: SOUTH_TIME
requested_by: owner
seen: false
effort: S
legacy_id: null
opened: 2026-09-01
closed: null
pr: null
claimed_by: null
blocked_on: T-0464
needs_bake: false
---

Once the land exists, make it reachable. Extend overview-map bounds, walker navigation and jump targets so a visitor can travel continuously from Fort Dearborn to the 1812 battle corridor and later Prairie Avenue landmarks without teleporting outside modeled ground.

Add evidence-aware anchors at the fort, the historic shoreline route, the approximate battle area, 16th/Prairie, 18th/Prairie and the south end near 22nd/Cermak. Anchor names must describe what the selected year actually contains; do not show an 1880s mansion label in 1812.

Acceptance: all south anchors resolve on modeled land, year switching preserves valid camera placement, overview/map bounds include the new field, and a desktop smoke path can traverse from the fort to the southern historical area.