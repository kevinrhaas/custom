---
id: T-0809
title: The janitor gates the branch un-merged and drops a conflict in silence, and the lane outruns its own merge lap
state: open
epic: META
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-05
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The queue drain (T-0803 → T-0807) empties the pile. This ticket is why it filled, and
without it the pile is back inside a day. **Two causes, both measured, and both live in
`kevinrhaas/polecat-platform` — outside `chicago/4d`'s scope, so this ticket is the
record and the work is a PR there.**

**1. The janitor gates the branch UN-MERGED, then loses the conflict in silence.**
`.github/workflows/steward-janitor.yml` does `git clone --depth 1 -b "$BR"` and runs
`check.sh && smoke_renderer.mjs` on the branch **as it stands** — never merged with the
base it is about to be merged into. So:

- a green branch is merged **without the merge ever having been gated**, which is the
  exact hole T-0674 already filed against bot-opened PRs;
- when the merge then fails on conflict, the code path is
  `echo "merge failed (conflict?)"; SKIPPED=$((SKIPPED+1))` — **no comment on the PR, no
  label, nothing.** The red path comments; the conflict path does not.

That is why 21 PRs accumulated with nobody noticing: each one was swept, silently
skipped, and swept again the next hour. The fix is to merge the base into a scratch
branch first, gate THAT, and on conflict leave one comment naming the conflicting files
— reusing the existing "leave one comment, don't repeat it" guard that the red path
already has.

**2. The lane outruns its own merge lap.** `.github/steward/focus.json` had `custom` at
`slices: 5`, `everyHours: 1` — five PRs an hour into a branch where a merge lap costs
more wall-clock than the interval between merges. #880 wrote it down: *"the lane runs ten
slices an hour, every PR touches the same generated files, and a merge lap costs more
wall-clock than the interval between merges. Landing them one at a time loses ground."*

**Owner's call, 2026-09-05: drop `custom` to `slices: 2`.** That change is made in
polecat-platform and takes effect on the next `steward-focus.yml` tick once it is on
`main`.

**The standing rule the two together imply**, and the thing to write into AGENTS.md:
a `steward/*` PR that cannot merge is not "open", it is ROTTING — its ticket reads
`open` at the top of the queue and the next slice rebuilds the same work. So the janitor
must make an un-mergeable PR VISIBLE within one sweep, and the queue must carry a drain
lap whenever the count goes past what one lap can hold.

**Acceptance:** a PR against `kevinrhaas/polecat-platform` that (1) merges the PR's base
into the clone and gates the merge result, not the bare branch, and (2) comments once,
naming the conflicting paths, on any PR it cannot merge — with the existing
duplicate-comment guard extended to cover it. `focus.json` carries `custom` at
`slices: 2`. A sweep is observed doing both against this repo. AGENTS.md § How work ships
gains the rotting-PR rule with the count that bought it: 21 open, 21 conflicting, 6 build
products between them, five of them past saving.

Filed by the 2026-09-05 open-PR queue pass. T-0234 (the GraphQL quota) touches the same
workflow and should be read alongside it.
