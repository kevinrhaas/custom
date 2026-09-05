---
id: T-0738
title: check.sh is RED on dev: nine steps fail before any branch is cut — the residents mints, six research cohorts and the people sidecar all stopped re-deriving
state: open
epic: META
requested_by: loop
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

**Found by T-0517 (2026-09-05), which could not merge because of it.** `./tools/check.sh`
exits 1 on a clean checkout of `origin/dev` at `85d650116`, before any branch is cut and
with an empty working tree. Nine steps are red, and they are all the residents layer or its
derivatives:

```
sidecars derived from data/
the 75-person real-resident research cohort is fixed
the second non-overlapping 75-person research cohort is fixed
the third non-overlapping 75-person research cohort is fixed
the thirteenth research cohort is fixed
the fourteenth research cohort is fixed
the fifteenth research cohort is fixed
the civic, church, press and book residents re-derive from the ladder
the regraded residents re-derive from the ladder too
```

What each says:

- `python3 tools/compile_scene.py --check` — *"DRIFT: data/sidecars/1835/people.json is not
  what the dataset compiles to"*. The published people sidecar no longer matches the layer.
- `python3 tools/mint_civic_residents.py --check` — five files differ from the derivation:
  `hh_campbell_james_b`, `hh_hale_john`, `hh_lloyd_alexander`, `hh_price_jeremiah` and
  `data/residents/index.json`.
- the six cohort gates — *"data/research/residents/pass_NN_75_cohort.json is stale;
  regenerate without --gate"*.

**Why this is urgent rather than tidy.** `check.sh` is the gate every 4D PR must pass before
it merges, so a red `dev` blocks every run on the app at once, and each of them spends its
budget discovering the same thing. It also hides real regressions: a run that sees nine
failures it did not cause has no cheap way to tell a tenth from the noise. T-0517 had to
prove its own diff added none by running the gate twice, once on a stashed tree, and then
park on `hold`.

**The likely cause is a merge that changed the residents layer without re-deriving what
reads it** — the layer moved four times on 2026-09-04/05 (T-0510 cohort 15 at the tip,
T-0516, T-0512, T-0636). Whichever it was, the repair is small and mechanical; the value of
this ticket is in doing it deliberately and in one PR rather than smuggling it into an
unrelated one.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The cause is named: which merge left which derivative stale, read off the history rather
  than guessed. If a record changed by hand and the derivation is right, the record is
  repaired; if the derivation changed and the records are right, they are rebuilt. Do not
  run `--build` blind over all nine and call it done — one of them may be a real
  disagreement rather than staleness, and the diff has to be read.
- `./tools/check.sh` exits 0 on `dev` with an empty working tree.
- Whether a gate should catch this at merge time rather than at the next branch is answered
  in the PR — the janitor re-runs the app's gate against a PR branch, so a red `dev` gets in
  only when something merges without it.

**Related:** T-0517 (found it) · T-0510, T-0516, T-0512, T-0636 (the four merges in the
window) · `tools/check.sh`
