---
id: T-0296
title: T-0258 and T-0260 are sized M on the measurement that split T-0259 into six
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

T-0259 was sized `M` — one run — and a run that claimed it on 2026-08-28 measured the work
before committing to it and found six runs. It was split into T-0289..T-0294, one month
each, and the first of them (July 1834, five issues) filled a whole run: 129 claims, 298
people, five extraction files.

**T-0258 (November 1833 to June 1834, ~30 issues) and T-0260 (January to August 1835, ~34
issues) carry the same `M` and were sized the same way.** They are the same paper, the same
segmenter, the same interleave, and more issues each than T-0259 had. On the July
measurement they are seven and eight runs respectively.

Nothing here says what the right seam is — months worked for T-0259 because the standing
advertisements and the letter lists run in monthly cohorts, and the same is likely true
either side of it. What this ticket asks for is that the sizing be **decided before a run
claims one of them and discovers it mid-flight**, because a run that splits a ticket spends
the front of its budget on bookkeeping rather than on reading.

Note that `ticket.mjs claim` refuses an `L` and `ticket.mjs check` refuses one sitting in
the queue, so the two cannot simply be re-graded `L` and left — they have to be split, or
left `M` on a stated argument that they are not.

**Acceptance:** (state it before working — never weakened to pass)

- T-0258 and T-0260 are either split into pieces each sized on the July measurement, or
  left as they are with the argument written into the ticket.
- Whichever it is, the reasoning names a per-issue cost — claims, pages that have to be
  read, whether a letter list stands in the range — rather than a feeling.
- The children, if any, take the parent's exact place in QUEUE.md. The owner orders that
  file; a split may not re-prioritise.
