---
id: T-0012
title: Ship the 16-bit ground the script already computes
state: open
epic: RENDERING
requested_by: loop
seen: true
effort: M
legacy_id: R-W6(b)
opened: 2026-08-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
---

The 16-bit ground exists in the bake script and not in the file a visitor loads — the
committed derivative still quantises POSITION to 14 bits (306 mm lattice, held down only by
the load-time conform). Deep history: § R-W6(b) (~5403). Needs one bake, or the owner's word
to hand-run it.

**Acceptance:** shipped terrain GLB carries 16-bit POSITION; check_published's derivative
report shows it; worst error ≤ 13 mm.
