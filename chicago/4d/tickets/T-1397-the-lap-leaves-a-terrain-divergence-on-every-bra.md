---
id: T-1397
title: The lap leaves a terrain divergence on every branch it laps: two unrelated PRs carry a byte-identical river, hydrology and landings diff against dev and fail the same four terrain gates, and neither side re-derives back to the other
state: open
epic: META
requested_by: steward
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-19
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The lap leaves a terrain divergence on every branch it laps: two unrelated PRs carry a byte-identical river, hydrology and landings diff against dev and fail the same four terrain gates, and neither side re-derives back to the other.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**THE MEASUREMENT (2026-09-19).**

Two pull requests that share NO commits — #1518 (`steward/t-1372-hulls-in-port`) and #1521
(`steward/t-1377-free-black-1835`) — carry a BYTE-IDENTICAL diff against `dev` over
`chicago/4d/data/terrain/` and `chicago/4d/data/wharves/`. The sha256 of
`git diff origin/dev...<branch>` over those paths is `4637a39c77c10865` on both.

On each branch the commit that introduces it is the lap's:

```
#1518   15d4a9222  Lap onto dev: generated files regenerated, not merged
#1521   52b9939e4  Lap onto dev: generated files regenerated, not merged
```

It is a real geometry change and not a formatting or precision artefact —
`data/wharves/river_landings.json` moves `vertices` 88 -> 92 and `length_m` 2932.6 -> 2952.0,
and `river.geojson` moves 694 lines.

**IT BREAKS FOUR GATES ON EVERY BRANCH THE LAP TOUCHES.** #1518 and #1521 fail the identical
four, neither of them anything to do with the ticket being worked:

```
* dataset (schema, provenance, date gates, licenses, staleness, publish)
* the NA re-read of the north-side slough still lands on the committed centreline
* the frontage works re-derive from the rule that chose their walls
* West Water still stands one half-corridor off the bank, and the two refusals still hold
```

`dev` itself is green — gate `success` on `3845cb41c`, `a2afbecae` and `08d8cf094`.

**THE THREE DIRECT GENERATORS REPRODUCE `dev` EXACTLY.** `generate_frontage_works.py`,
`generate_river_wharves.py` and `derive_north_water.py`, run against a clean `dev` checkout,
change ZERO files. So the committed terrain is reproducible from its own generators and `dev` is
not carrying a stale artefact.

**WHY THIS MATTERS MORE THAN THE TWO PRs.** The lap runs on every open pull request. Any branch
it laps acquires this diff and fails these four gates, regardless of what the branch is for. It
manufactures red gates across the whole queue, and each one costs a human the work of deciding
whether the failure is the branch's own — which is exactly the misattribution this ticket's
filer made on #1518 before checking `git log` on the file (corrected at
https://github.com/kevinrhaas/custom/pull/1518#issuecomment-5743234204).


**WHAT IS ESTABLISHED, AND WHAT IS NOT.** Stated separately on purpose, because the filer got
this wrong once already by inferring a cause from partial evidence.

ESTABLISHED, each by a command run today:

1. The two branches' terrain diffs against `dev` are BYTE-IDENTICAL (sha256 `4637a39c77c10865`
   over `data/terrain` + `data/wharves`), and the branches share no commits.
2. On each branch the introducing commit is `Lap onto dev: generated files regenerated, not
   merged` — `15d4a9222` on #1518, `52b9939e4` on #1521.
3. `dev` REPRODUCES ITSELF. `node tools/rederive.mjs --run` over all 151 steps on a clean `dev`
   checkout changes ZERO files under `data/terrain` or `data/wharves`. So do
   `generate_frontage_works.py`, `generate_river_wharves.py` and `derive_north_water.py` run
   directly, and so do `compile_scene.py --all` and `resolve_id_collisions.mjs`.
4. THE BRANCH ALSO REPRODUCES ITSELF. Running those same three generators on #1518's branch
   changes ZERO files, and the branch still differs from `dev` by the same three afterwards.
5. So both trees are self-consistent and disagree with each other, and nothing in the manifest
   moves either one toward the other. This is a committed divergence that no re-derive corrects.
6. `dev`'s gate is green (`3845cb41c`, `a2afbecae`, `08d8cf094`); the lapped branches fail four
   terrain gates that `dev` passes.

NOT ESTABLISHED, and this ticket's first job:

- **WHICH tree is right.** The gates pass on `dev`'s terrain and fail on the branches', which is
  evidence for `dev` but is not proof — the gates' own committed references could be the stale
  thing. Decide it on the sources, not on which one is greener.
- **HOW the lap produced a terrain change that nothing reproduces today.** The regeneration must
  have run against inputs that no longer exist in that state. Until that is known, the same lap
  can mint the same fossil again on the next branch.

**A SEPARATE FINDING FROM THE SAME RUN, worth its own attention:** the clean-`dev` re-derive
changed exactly one file — `data/reconstruction/1835_reconstruction_order_book.json`. `dev` is
therefore carrying an order book that does not re-derive from its own inputs. It is not what
breaks the terrain gates and it is not this ticket, but it is a committed derived file out of
step with its generator on the integration branch, and somebody should look at it.

1. The question "which terrain is correct" is answered from the sources and WRITTEN DOWN, and
   the losing tree is corrected — either `dev`'s terrain is rebuilt and the gates' references move
   with it, or the branches' fossil is reverted and the lap is stopped from re-minting it.
2. The mechanism is found and closed. A lap that can commit generator output which no later
   re-derive reproduces will do it again; naming the trigger is what makes this ticket stay
   closed. If the trigger cannot be reproduced, say so in writing and gate against the SHAPE
   instead — see 3.
3. **The lap does not commit regenerated files that the gate has not passed.** Its own note says
   "gating is CI's — every push above re-runs the gate", and that is what leaves a red branch
   behind with nothing to roll it back. Whatever this unit does, a regeneration that breaks a gate
   must not survive as a commit on the branch.
4. Demonstrated on a reconstruction, not asserted: a branch lapped after the fix does not acquire
   a terrain diff, and #1518 and #1521 go green on those four gates without their own work being
   touched.
5. The cost is stated. Every branch the lap touches inherits four red gates that have nothing to
   do with its ticket, and each one costs a person the work of deciding whether the failure is the
   branch's own. On 2026-09-19 that cost this filer a wrong public attribution on #1518 before
   `git log` on the file corrected it.
