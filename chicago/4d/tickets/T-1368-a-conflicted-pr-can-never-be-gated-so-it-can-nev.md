---
id: T-1368
title: A conflicted PR can never be gated, so it can never be merged: no merge ref means no pull_request run, merge-ready only takes clean, and the lap stops at REAL CONFLICT — three PRs hit it in one evening and each needed hands
state: open
epic: META
requested_by: steward
seen: false
effort: M
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

A conflicted PR can never be gated, so it can never be merged: no merge ref means no pull_request run, merge-ready only takes clean, and the lap stops at REAL CONFLICT — three PRs hit it in one evening and each needed hands.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**The deadlock, stated as a cycle.** A pull request whose conflicts the lap will not clear
cannot be merged by anything in this repo, and cannot become mergeable by waiting:

1. The PR is `dirty`, so GitHub cannot compute its merge ref.
2. `.github/workflows/chicago-4d-check.yml` gates on `pull_request` — and a `pull_request` run
   needs that merge ref, so the gate never starts. The PR carries **ZERO check runs**.
3. `gate` is a REQUIRED check on `dev`, so GitHub never calls the PR `clean`.
4. `.github/steward/merge-ready.sh` merges **only** on `clean` — deliberately, and its own
   comment measured why — so it passes over the PR every time.
5. `.github/steward/pr-lap.sh` prints `REAL CONFLICT — left alone` and stops, which is correct:
   it will not hand-merge a file no tool owns.

Nothing in that loop advances. The PR sits at zero checks for as long as it is left.

**Measured, three times in one evening (2026-09-19):**

| PR | ticket | conflicts | outcome |
|---|---|---|---|
| #1495 | T-1172 | 12, five "NOT the manifest's to clear" | hand-resolved; merge-ready merged it **within two minutes** of the push |
| #1497 | T-1174 | 136, 118 of them resident household cards | hand-resolved; merge-ready merged it at 04:33:48Z |

Both merged themselves almost immediately after the push — #1495 within two minutes. That is
the proof that the rest of the automation is sound: the ONLY thing missing was a gate run, and
the only way to get one was a person resolving conflicts.

**AND THE SHAPE ALONE DOES NOT IDENTIFY IT — corrected at filing, 2026-09-19.** This ticket was
first written citing THREE instances. The third, #1499 (T-1343), was `dirty` with zero check
runs and looked identical to the other two. It was not the deadlock: its steward run was still
going, and it went on to rebase onto `dev` twice, re-derive on each rebase, push, and clear
itself. It reached `blocked` with a gate running, entirely without hands. Counting it was wrong
and the table above is the corrected one.

So `dirty` + zero check runs is the SYMPTOM and not the diagnosis. A PR mid-run looks exactly
like a PR nothing will ever touch again. The distinguishing fact is whether the run that owns
the ticket is still alive: read `claim/t-NNNN` for the branch's ticket, take the `run:` URL out
of the marker body, and ask GitHub whether that run is still `in_progress`. #1499's was — its
`Run steward` step had been going 1h49m and it had opened the PR mid-run. A marker that no
longer exists means no run holds the ticket, which is the same answer as a finished one.

This matters twice over: anything that acts on the symptom will "fix" PRs that were about to fix
themselves, and colliding with a live run costs more than waiting — measured on #1495, where the
owning run's own convergence was better than the mechanical merge that raced it.

**Where it came from, and the part that matters.** The gate's push trigger is filtered:

```yaml
push:
  branches: [dev, main]
```

T-1288 added that filter, for a real and measured reason: a steward branch with an open PR
satisfied BOTH triggers, so every push ran the 439-step suite TWICE on one commit, and because a
PR is not `clean` until every required check passes, the PR waited on the SLOWER of two identical
runs. Four PRs were seen sitting `blocked` with one gate green and its twin still going. That
finding is not in question and this ticket must not undo it.

But an unfiltered push trigger fires on a branch push **regardless of mergeability**, which is
exactly the case `pull_request` cannot serve. T-1288 wrote down what it believed it was giving
up — "a steward branch pushed BEFORE its pull request exists is not gated by that push", closed
by the PR opening in the same run — and that list did not include this one: a PR that EXISTS and
is `dirty`, where `pull_request` structurally cannot run. So the filter removed the only trigger
that could have gated a conflicted branch, and the trade-off as recorded did not know it.

1. A conflicted PR either gets gated, or it is made LOUD. Both are defensible and the unit picks
   one with its reading written down; what must not survive is a PR sitting at zero checks with
   nothing reporting it. Options that exist, none of them prescribed here: dispatch the gate for
   a branch the lap left alone (`workflow_dispatch` is already on the workflow); have the lap
   label the PR and say so on it when it prints `REAL CONFLICT`; or have merge-ready report the
   `dirty` + zero-checks shape rather than passing over it silently.
2. **T-1288's measurement is preserved.** Whatever is done, one commit does not get two identical
   gate runs, and a PR does not wait on the slower of a pair. If the fix touches the push
   trigger, it is measured the same way T-1288 measured — count the check runs on one head sha —
   and the count is in the ticket.
3. The lap's own behaviour is unchanged where it is right. `REAL CONFLICT — left alone` is the
   correct call for a file no tool owns (T-1282); this ticket is about what happens NEXT, not
   about making the lap merge things it should not.
4. Demonstrated on a reconstruction of the deadlock — a branch conflicted against `dev` with an
   open PR — not asserted from the workflow files. Show the zero-check state before and whatever
   the fix produces after.
4b. **Whatever acts does not act on a PR whose run is still alive.** The check is the one above:
   the branch's `claim/t-NNNN` marker names its run, and a run still `in_progress` means the PR
   is being worked, not stuck. A fix that labels, comments on, dispatches a gate for or
   otherwise touches a mid-run PR is a fault of this ticket, because #1499 proves such a PR
   commonly resolves itself.
5. The hand-resolution path stays available and documented. Some conflicts genuinely need a
   person (118 resident cards carrying drawn values did), and the goal is that such a PR is
   VISIBLE and gateable, never that no PR ever needs hands.

**Not T-1362.** That one is the lap skipping its re-derive when a branch is already current with
the base — a branch that merges cleanly and is stale. This is a branch that does not merge at
all. They meet only in that both leave a PR red or stuck with no automation able to move it.

---

## FINDING (2026-09-19, while landing the T-1397 queue): the cause is the MERGE DRIVERS

The ticket above reads `dirty` as "a conflicted PR". Measured today across four open
PRs — #1518, #1521, #1526, #1529 — **that is not what `dirty` means here**:

```
steward/t-1372-hulls-in-port             GitHub: dirty    real conflicts: 0
steward/t-1377-free-black-1835           GitHub: dirty    real conflicts: 0
steward/t-1394-resident-closeout         GitHub: dirty    real conflicts: 0
steward/t-1183-business-staffing-model   GitHub: dirty    real conflicts: 0
```

All four merged **cleanly** locally. `git merge origin/dev` on each printed the
drivers doing their job — `merge-queue: QUEUE.md reconciled`, `merge-changelog:
1 entry of ours placed on top of 986 from theirs`, `merge-smoke-state: 60 ours +
5 new from theirs` — and left zero conflicted paths.

**GitHub does not have those drivers.** `.gitattributes` registers them, but a merge
driver is local git config: it is configured by the checkout, not carried in the
repository. GitHub's mergeability probe runs a plain three-way merge, so every PR
that touches `QUEUE.md`, `renderers/web/js/changelog.js`, `tools/dev-smoke-state.json`
or any of the other driver-managed files is reported `dirty` **by construction** —
and those are exactly the files a branch and `dev` both always touch.

So the deadlock is not rare and it is not about conflicts:

1. a PR is opened, `dev` moves once, and GitHub calls it `dirty`;
2. `dirty` means no merge ref, so no `pull_request` gate ever runs;
3. `merge-ready.sh` takes only `clean`, so it will not touch it;
4. the lap CAN clear it — a pushed merge commit makes the branch a descendant of
   `dev`, which GitHub can see without any driver — but the next merge into `dev`
   re-arms it on every other open PR.

**Confirmed both directions on #1518 today.** At `b75254dc1` (a lap onto
`4509d5ac1`) GitHub said `mergeable: False, dirty`. `dev` moved to `918c43d1d`;
re-lapped to `b974e0393` and GitHub said `mergeable: True, blocked` with the gate
running. The lap commit is the whole difference.

### What this means for the fix

The remedy in acceptance is "resolve by hand", and that is treating the symptom.
The cheap structural options, in the order they are worth measuring:

- **Lap on `dev` movement, not on a schedule.** The lap already knows how to clear
  this; it just does not run at the moment `dev` moves. A push to `dev` that laps
  every open PR would keep the whole queue `clean` continuously. Cost: one lap per
  open PR per merge, which is the thing to measure before building.
- **Shrink what the drivers own.** `QUEUE.md` and `changelog.js` conflict on every
  merge because every branch appends to them. T-0937 and T-0938 already took the
  board and the mirror off the PR surface; T-1355 asks the same question for the
  four derived research reports. Anything taken off the PR surface stops
  manufacturing a false `dirty`.
- **Do not rely on `mergeable_state` alone.** `merge-ready.sh` could test
  mergeability the way this finding did — a real merge in a scratch worktree — and
  merge a PR that GitHub calls `dirty` but git does not. That inverts the deadlock:
  the driver-managed files stop being a reason a PR cannot land.

### The cost, measured

Four PRs, all green or greenable, none merged in the ~90 minutes this took. `dev`
moved twice under the laps (#1528, #1531) and invalidated all four, each costing
~8 minutes of re-derive plus a CI round. The owner paused the steward's `custom`
lane and the janitor (polecat-platform `focus.json`, 2026-09-19) because hands were
the only remedy left — which is the clearest statement of this ticket's cost there
is going to be.
