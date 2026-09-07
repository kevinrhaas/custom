---
id: T-0942
title: The SCHOOLS block of 33S7-9YYJ-L3 carries ink and is unread: the landed reading took the TOTAL column and the footer row and swept nothing to their right
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-07
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

**Salvaged from PR #1013 by T-0927, 2026-09-07, before that PR was closed as superseded.**
Filed there as T-0924; that number was never on `dev` and the ticket file has never
existed there.

The reading of 33S7-9YYJ-L3 that landed as PR #1014 took the TOTAL column and the footer
row and swept nothing to their right. The leaf's SCHOOLS block carries ink and no pass has
committed it. On `dev` the page file has no `schools_block_as_read` key at all.

PR #1015 — parked on `hold`, and not landed — did read it, and what it read is why this
matters rather than being tidy-up: its `schools_block_as_read` names a figure on line 1 and
a footing, on a leaf whose seventh SCHOOLS column is already recorded elsewhere as unread
for a different reason (T-0755: `No. of Scholars at public charge` sits in the binding
gutter of 33S7-9YYJ-6H and is recorded unread rather than blank). Two leaves, the same
column, unread twice.

**Acceptance:**

1. The SCHOOLS block of 33S7-9YYJ-L3 is read cell by cell at the exposure the rest of the
   leaf was read at, and each cell is committed, or recorded unread with the reason.
2. A cell with no ink is recorded as carrying no ink — not as a zero — in the form the
   other blocks on this leaf already use.
3. The block's own footing is read and the column closure is stated, closing or not, with
   nothing adjusted to make it close.
4. If #1015's reading of the block is used, it is cited as the source and re-verified at
   the image rather than copied.

**Links:** T-0744 · T-0755 · T-0927 · PR #1013 (closed) · PR #1015 (`hold`) · T-0941.
