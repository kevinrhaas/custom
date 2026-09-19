---
id: T-1362
title: The lap re-derives only when it merges, so a branch already current with dev stays stale against a gate dev just added: #1487 sat red on four manifest-owned files while the lap said 'already current — nothing to lap'
state: open
epic: META
requested_by: steward
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-09-18
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The lap re-derives only when it merges, so a branch already current with dev stays stale against a gate dev just added: #1487 sat red on four manifest-owned files while the lap said 'already current — nothing to lap'.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**What happened.** PR #1487 went red on 4 of 513 steps, on head `b0dd27135`:

```
* the closing set is owned, gated and reported as deltas
* research stays inside its historical ratchet and closed unit ledger
* the closing research audit still re-derives from the ledger and the four layers
* the research sign-off re-derives, and its GO still follows from the tree
```

The lap ran eleven minutes later (run 35413941315, 2026-09-19T01:51Z) and its own
output for that PR reads, in full:

```
=== PR #1487  (steward/t-1340-books-arrival-lists)
  already current — nothing to lap
```

So the branch was red, the lap looked at it, and the lap correctly concluded it had
nothing to merge — and therefore did nothing at all.

**Reproduced.** Checked out `b0dd27135` and ran the four gates' own commands: all four
FAIL, each naming its own rebuild (`rebuild_closing_set.py --rebuild`,
`measure_research_spend.py --ledger-build`, `report_research_closing_audit.py --build`,
`report_research_signoff.py --build`). All four files are owned by
`tools/derived_manifest.json`, and `node tools/rederive.mjs --run` turns every one of
them green — measured on this branch, which then gated `CHECK PASS — 513 steps, none
red`.

**The mechanism.** `.github/steward/pr-lap.sh` re-derives INSIDE the merge path only —
once on the conflict branch and once at line 408 for the no-conflict merge. When the
branch is already current with the base, control never reaches either. And "current
with the base" is not "current with the base's GATES": #1480 landed `the closing set is
owned, gated and reported as deltas` on dev, so dev gained a GATE while the branch
agreed with dev about every file. Nothing to merge, so nothing re-derived, so four
manifest-owned artifacts stayed stale and the PR stayed red with nobody to fix it. A
human had to notice.

**This is not T-1282 and not #1333.** T-1282 is the lap failing to re-derive a resident
household card ON A CONFLICT. #1333 (`fix/lap-always-rederive`, 2026-09-14) already
moved the lap from re-deriving only on a conflict to re-deriving on every MERGE — and
its own comment makes this ticket's argument for it:

> `--run` is idempotent by construction — every step re-derives from committed inputs —
> so running it on a branch that needed nothing costs those seconds and changes nothing,
> which is the right trade against a red PR nobody owns.

That reasoning extends exactly to the already-current branch. The script does not take
it there, and this is the case it left behind.

1. A branch already current with the base but stale against a gate the base ADDED is
   re-derived and pushed by the lap. Demonstrated on a reconstruction of this case — a
   branch that merges cleanly and is still red — not asserted from the diff.
2. The already-current path does not push an EMPTY commit. If the re-derive changes
   nothing, the lap leaves the branch alone and says so; a lap that commits on every
   pass to every current branch is worse than the bug.
3. The cost is MEASURED, the way #1333 measured its own (19 seconds for 28 steps on a
   real lapped tree). The already-current path runs on every PR on every lap, so its
   cost is the one that multiplies.
4. A test covers it — `tools/test_pr_lap_list.mjs` is where #1333 put its own, and the
   case is "already current, and stale".
5. The lap's output distinguishes the two outcomes. `already current — nothing to lap`
   must stop meaning both "current and clean" and "current and stale", or the next
   occurrence is just as invisible as this one.

**Finding (2026-09-19, six PRs cleared by hand): CHECK BEFORE REBUILDING — it is what makes this
fix cheap enough to run on every PR on every lap.** The acceptance above asks the lap to
re-derive a branch it is already current with. The obvious implementation is
`rederive.mjs --run`, and that is the expensive answer: ~10 minutes of rebuilding on a tree that
usually needs none of it. Measured the hard way while clearing #1495, #1497, #1499, #1502, #1512
and #1518.

**The cheap answer is to ask first.** Every gate this family of staleness breaks has a `--check`
that answers in seconds:

```
python3 tools/reconstruct_residents_1835.py --check      # the reconstruct stages
python3 tools/model_town_1835.py            --check
python3 tools/profile_population_1835.py    --check
python3 tools/build_order_book_1835.py      --check
python3 tools/model_transients_1835.py      --check
python3 tools/migrate_attribute_tiers.py    --check
node    tools/rederive.mjs                  --check      # the derived manifest
python3 tools/rebuild_closing_set.py        --check
node    tools/check-changelog.mjs
node    tools/audit_step_isolation.mjs      --check --quiet
python3 tools/measure_layer_reads.py        --gate
```

Run those, rebuild ONLY what they name, and re-check. The measurement:

| PR | what was actually stale | blanket re-derive | check-first |
|---|---|---|---|
| #1518 | the closing-set report, nothing else | ~10 min | **under 2 min** |
| #1512 (5th lap) | the changelog stamp, nothing else | ~15 min | **under 1 min** |
| #1512 (laps 1–4) | — | ~15 min each, **lost the race to dev every time** | — |

#1512's first four laps each re-derived the whole layer and were overtaken by dev before they
could merge; the fifth checked first, found only an unstamped changelog, and landed. That is the
difference between a repair that keeps up with the queue and one that cannot.

**#1518 IS THIS TICKET, LIVE.** It sat red for nearly two hours, `mergeable_state` clean, ZERO
commits behind dev — so the lap printed `already current — nothing to lap` and moved on, exactly
as the acceptance above describes. Its entire failure was ONE stale file,
`docs/RESEARCH/closing-convergence-2026-09.md`. Ten of the eleven checks read clean. Had the lap
run the list and rebuilt the one thing it named, nobody would have had to look at that PR at all.

**Two cautions for whoever implements it:**

1. The closing set is the usual culprit and it is stale for an ordering reason, not a merge one:
   `rebuild_closing_set.py` is the LAST step of the derived manifest, and anything that writes
   `site/` afterwards — `stamp-changelog.mjs` mirrors the changelog there — moves a member it
   measures. So rebuild the closing set AFTER the stamp, not before, or it is stale again
   immediately.
2. Rebuild what the check names, then re-run the WHOLE relevant sequence rather than just that
   step — T-1179's corrected finding, for the same reason: the check names the stage that is
   stale, and the cycle can run through a stage it does not name.
