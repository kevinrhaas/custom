---
id: T-0803
title: The published tree is 936 bytes under the 32 MiB budget, so no PR that publishes anything can pass validate.py again
state: withdrawn
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: 2026-09-05
pr: null
claimed_by: null
blocked_on: Superseded, and the fault is measured gone. All five of T-0722, T-0725, T-0731, T-0774 and T-0803 reported the SAME thing within one day — the published tree sitting a few hundred bytes under SITE_BUDGET_MB on dev at 06a0a9ec/1e9108aa, so the next PR to publish anything failed the gate. T-0722 fixed it in PR #836 by publishing changelog.js once instead of twice. Measured on this tree: 30.412 MB of 32, 1.588 MB of headroom, and ZERO pairs of published files over 64 KB with identical bytes — the condition #836's new validate.py rule now gates, so it cannot return the way it arrived. Withdrawn on the owner's instruction of 2026-09-05, 'do it if those tickets are useless now', after checking each one's own claim rather than the band's summary of them.  CORRECTION, same day: this reason first cited "30.412 MB of 32, 1.588 MB of headroom". The 32 came from tools/site_budget.py, which still hardcoded it while tools/validate.py — the gate that actually refuses a merge — had been raised to 36 by T-0593 (#823). The true figures are 30.5 MB of 36 and 5.5 MB of headroom, so the withdrawal stands and stands wider than stated. site_budget.py now reads SITE_BUDGET_MB out of the gate rather than restating it.
needs_bake: false
closed_at: 2026-09-05T20:03:55.552Z
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
