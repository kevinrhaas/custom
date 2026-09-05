---
id: T-0745
title: dev's gate is still red, but not on T-0739's nine: the four that remain are the cross-street faces, blk_washington_clark's southern ground, the far-timber census, and a duplicate ticket id
state: claimed
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-05
closed: null
pr: null
claimed_by: run 9/5/2026, 4:28:19 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/33957698251
---

dev's gate is still red, but not on T-0739's nine: the four that remain are the cross-street faces, blk_washington_clark's southern ground, the far-timber census, and a duplicate ticket id.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Measured, 2026-09-05, by T-0741's run.** `tools/check.sh` was run on a clean worktree of
`origin/dev` at `8ae7d0dec` and on this run's branch. Both exit 1, and their failure lines are
IDENTICAL — the branch introduces none of them. But they are NOT the nine T-0739 records: the
sidecar drift, the three cohort collisions and the two ladder re-derivations all pass now. Four
remain:

- `the seven cross streets have 34 platted faces — got 0`, and with it `both sides of every
  covered cross street are found` (2 checks failed in that step)
- `1 committed platted block(s) stand off the modelled ground: blk_washington_clark` →
  `SOUTHERN GROUND FAIL`, twice: `the programme's stated southern coverage is not what the
  ground measures`
- `the far-timber census disagrees with what is banked (ROADMAP R-BUG5)`, three times
- `ticket queue FAILED: T-0739-the-1830-division-s-recapitulation-counts-53-and.md: DUPLICATE id
  T-0739` — two branches each assigned T-0739 and both merged. The tool prints its own repair:
  `node tools/ticket.mjs restamp <file>` renumbers the younger one, which is the 1830
  recapitulation ticket (merged in #853, after #848 filed the other).

**Acceptance:** `tools/check.sh` exits 0 on `dev`, each of the four repaired rather than
silenced, and T-0739's body corrected or closed — it names nine failures that no longer fire,
which is worse than no record, because the next run to read it will look for the wrong red.

**Why this is filed rather than fixed here.** T-0741 was one unit of work about inventorying
census images. Three of these four are terrain and street geometry and the fourth is ticket
bookkeeping; none of them is that unit, and bundling them into its PR would make one
un-revertible commit out of four unrelated repairs.

---

**WHAT WAS ACTUALLY RED, measured 2026-09-05 on a clean worktree of `origin/dev` at
`cfda02f34` — and three of this ticket's four were never failures at all.** `check.sh`
reports a failing STEP as `^ <label> failed`; the lines this ticket quoted come from
inside three self-test steps, whose whole job is to break the enumeration and prove the
assertions fire. `FAIL the seven cross streets have 34 platted faces — got 0` is the
self-test working. So are the two `SOUTHERN GROUND FAIL` lines and the three far-timber
ones; each is followed by its step's own `self-test OK`. Reading them as red cost this
ticket its diagnosis, and would have cost the next run a day of chasing street geometry
that is fine. The nine real steps were T-0735's nine, one of them since repaired:

```
ticket queue                                              (the duplicate id — real, and this ticket found it)
the 75-person real-resident research cohort is fixed
the second / third non-overlapping 75-person research cohort is fixed
the thirteenth / fourteenth / fifteenth research cohort is fixed
the civic, church, press and book residents re-derive from the ladder
the regraded residents re-derive from the ladder too
```

**CLOSED on the acceptance as written:** `./tools/check.sh` exits 0 on this branch, each
of the nine repaired rather than silenced, and T-0739 corrected — the id collision is
restamped to T-0757 and the duplicate GATE ticket of the same number is withdrawn with
its reasoning. T-0735 is closed by the same PR; it holds the acceptance that was met.
