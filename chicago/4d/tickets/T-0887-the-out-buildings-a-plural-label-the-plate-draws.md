---
id: T-0887
title: The Out Buildings: a plural label the plate draws TWICE, on the fort's outer ground where the enclosure fence turns down to the river
state: done
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0881
opened: 2026-09-06
closed: 2026-09-06
pr: 985
claimed_by: run 9/6/2026, 8:10:27 AM CT
blocked_on: null
needs_bake: false
closed_at: 2026-09-06T14:06:21.753Z
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34034744403
---

The Out Buildings: a plural label the plate draws TWICE, on the fort's outer ground where the enclosure fence turns down to the river.

Piece 1 of 2 of **T-0881 — The fort's well and the Out Buildings: the class T-0592 refused the town, and a plural label the plate draws once**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**WHAT THE PARENT GOT WRONG, AND IT IS WHY THIS IS ITS OWN TICKET.** T-0881's title says
the plate "draws once". It draws **twice**: two solid blocks under one plural label, on the
outer ground where the enclosure fence turns down to the river — measured at leaf resolution
here, where the parent read them at a glance. So the plural is not a label without a referent;
it is a label with two, and the record is two buildings rather than one.

**Acceptance:**

1. Both drawn blocks are placed off the 1830 Harrison plan by **the same transform and the
   same checks T-0883 used** — leaf, pixel, scale, anchor, and the garrison garden as the
   witness — with every number written on the record so a reader can recompute it by hand.
   No new transform is invented for these two.
2. Neither carries a grade above `inferred` for position and nothing above `reconstructed`
   for fabric: the plate gives a filled parallelogram, a plural noun and nothing else, and
   Hubbard does not name them. Every invented element is a liberty in `docs/LIBERTIES.md`.
3. The 665-roof programme's fort district absorbs two more standing roofs as an ADDITION,
   the way T-0883 did — documented buildings are not paid for out of invented ones — and the
   reconciliation states it.
4. Baked with `./tools/bake.sh --only` per structure and `tools/publish.sh` in the same
   commit; `bash tools/check.sh` green, including the staleness gate.
5. `docs/RESEARCH/fort_dearborn.md` § 7 moves these two out of "attested and not built".
