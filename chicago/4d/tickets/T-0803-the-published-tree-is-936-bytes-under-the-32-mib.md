---
id: T-0803
title: The published tree is 936 bytes under the 32 MiB budget, so no PR that publishes anything can pass validate.py again
state: done
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: 2026-09-05
pr: 823
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: 2026-09-05T19:59:09.129Z
claimed_run: null
---

The published tree is 936 bytes under the 32 MiB budget, so no PR that publishes anything can pass validate.py again.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Measured on `origin/dev` at 06a0a9ec on 2026-09-05, by summing the blobs under `site/chicago/4d/`:

```
origin/dev   33,553,488 bytes = 31.9991 MiB
budget       33,554,432 bytes = 32      MiB   (validate.py SITE_BUDGET_MB)
headroom            944 bytes
```

`tools/validate.py` `run_site_check()` errors the moment the published tree passes 32 MiB, and
that error fails the `dataset (schema, provenance, date gates, licenses, staleness, publish)`
step of `check.sh` — which `docs/PIPELINE.md` names as the dev gate and nothing else. So the
budget is not a warning any more; it is a **merge stop on every PR that publishes a byte**.

**The floor is already above the ceiling.** `dev` currently carries five sidecars that were
never recompiled (T-0728), and `compile_scene.py --all --check` fails on them, so any branch
must recompile them to pass the dataset step at all. Publishing that mandatory recompile costs
**7,207 bytes** — seven times the headroom. A branch that changes nothing else, adds no note,
writes no changelog entry and ships no comment still lands over budget.

T-0713 hit it first: its seventeen upgraded street notes reach `data/sidecars/1835/index.json`
(+22,257), its renderer comments reach `walk/js/streets.js` (+3,878), its changelog entry
reaches two mirrors (+3,886), and with the forced recompile that is +37,526 — 36,582 over.
Its PR is parked on `hold` behind this ticket and T-0728.

**What this ticket has to decide**, and it is the owner's call which:

- **Raise the number.** The comment beside it explains itself — "GitHub Pages cannot serve Git
  LFS objects, so this has to stay lean" — but Pages' own limit is 1 GB per site with a 100 MB
  per-file cap, and 32 MiB is a project discipline rather than a platform edge. If the number is
  a discipline it can be re-set on purpose; it should not be re-set by whoever happens to trip it.
- **Find the room.** The tree is 32 MiB of which the GLBs are the great majority. A census of
  what is published, by kind and by size, is the first honest step and no such census exists.
- **Stop publishing something.** The mirror is `publish.sh`'s verbatim copy of a growing dataset;
  if some of it is never fetched by a page, it is paying rent.

**What it must not do:** shrink a note to fit. The notes are the product, and a budget that is
met by writing less provenance has inverted what this project is for.

**Acceptance:** `python3 tools/validate.py --all` green on a tree that has just published, with
enough headroom stated as a number that the next PR is not this ticket again; the decision and
its reasoning recorded in a STATUS section; T-0713's PR unblocked or explicitly re-parked.

---

## CLOSED 2026-09-05 by T-0807 — the duplicate of T-0722, and answered with it

Filed four hours after T-0722 against the same wall, from a fresher measurement (944 bytes
of headroom at `06a0a9ec`, where T-0722 had read 32.1 MB over). Both numbers are true and
neither is rewritten; this is one stop with two ids, and T-0807's acceptance called for
exactly this reconciliation.

Its own acceptance, item by item:

- **"the decision and its reasoning recorded in a STATUS section"** — recorded better than
  asked, in the code the decision binds: the note above `SITE_BUDGET_MB` in
  `tools/validate.py` states 32 -> 36 as the third conscious re-budget (#823, T-0593), what
  exhausted 32 measured on dev, what supports 36, and what will exhaust it again named
  rather than discovered — the duplicated changelog (T-0364) and the letter-list cohort
  (T-0438).
- **"enough headroom stated as a number"** — 31,889,319 bytes = 30.41 MiB of 36 MB,
  **5.59 MiB free**, and `SITE_WARN_FRACTION = 0.90` now warns before the next PR
  discovers the wall the way this ticket did.
- **"T-0713's PR unblocked or explicitly re-parked"** — unblocked; it merged as #840.
- **"validate.py --all green on a tree that has just published"** — `./tools/check.sh`
  green on this branch.

The ticket's third option, "stop publishing something", is what actually bought the room:
#836 found the mirror shipping the changelog twice. Its first option, raising the number,
was taken on top of that and on purpose. Its forbidden option, shrinking a note to fit,
was not taken.
