---
id: T-0029
title: The nightly bake check is red on K38 derivative baselines
state: open
epic: PIPELINE
requested_by: steward
seen: false
effort: M
legacy_id: K38
opened: 2026-08-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

`bake` has been red for days: the K38 web-derivative baseline says "decided master
passthrough" for files the bake now compresses. Two stale bake PRs (#164, #175) are parked
behind it. Re-run tools/measure_web_derivatives.py --write-baseline in a commit that states
why each passthrough moved, close or supersede the stale PRs, and the nightly goes green.

**Acceptance:** bake check green on dev; #164/#175 resolved; baseline change explained.
