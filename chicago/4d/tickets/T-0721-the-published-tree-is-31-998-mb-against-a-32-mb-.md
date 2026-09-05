---
id: T-0721
title: The published tree is 31.998 MB against a 32 MB ceiling: the next data PR cannot land
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The published tree is 31.998 MB against a 32 MB ceiling: the next data PR cannot land.

Found by T-0508, which had to spend a third of its run shrinking prose to fit.

`check.sh` fails the dataset step when `site/chicago/4d` exceeds **32 MB** — GitHub Pages
cannot serve Git LFS objects, so the ceiling is real and the reason is written down. On dev
at 6decede8 the published tree is **33,492,315 bytes**, which leaves **62 KB** of headroom
for any PR that adds data. T-0508 added 76 research rows to 73 household records — about
105 KB before trimming, 60 KB after — and had to cut the wording on every card, twice, to
land at 33,552,333 with **2 KB to spare**. The next data PR of any size cannot merge, and it
will find out at the gate rather than at the plan.

This is not a request to raise the number. The number is a fact about the host.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Say where the 32 MB actually goes, largest first, and propose what comes out. Candidates
worth measuring before arguing: the 372 published GLB pairs and whether every derivative is
still read; the household mirror, which publishes prose the card may not render; and whether
anything under `site/chicago/4d/data/` is shipped that no renderer imports —
`tools/measure_layer_reads.py` already answers that question for records and could answer it
for files. A tonnage table and a ranked list of removals is the deliverable; the removals
themselves are their own tickets.
