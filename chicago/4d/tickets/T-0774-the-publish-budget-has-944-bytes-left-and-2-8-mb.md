---
id: T-0774
title: The publish budget has 944 bytes left, and 2.8 MB of it is changelog.js kept twice
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The publish budget has 944 bytes left, and 2.8 MB of it is changelog.js kept twice.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Measured 2026-09-05 on `dev` at `06a0a9ec`, by the run that tripped it (T-0511).

`tools/validate.py`'s `run_site_check` fails the gate when `site/chicago/4d/` exceeds
`SITE_BUDGET_MB = 32`, because GitHub Pages cannot serve Git LFS objects. On `dev` the tree
is **33,553,488 bytes** — 31.9989 MB, **944 bytes under the ceiling**. The note the gate
prints, `site check: published tree 32.00 MB of 32 MB budget`, rounds the headroom out of
sight, so the first anyone learns of it is a red gate on unrelated work.

**What that means today:** the next change that adds more than 944 published bytes fails the
gate, whatever it is about. T-0511 hit it twice in one run:

- a single changelog entry costs 1,632 bytes and `publish.sh` mirrors it to two paths, so
  **3,264** — the entry was dropped, and **the project cannot ship a changelog entry**;
- `tools/ticket.mjs` mirrors `tickets.json` to `site/chicago/4d/tickets.json` (T-0154), so
  **filing a ticket costs about 645 published bytes**. T-0511 found two things worth a
  ticket and could afford one. The second is written at the foot of this file for want of
  room to give it its own.

So the two habits AGENTS.md asks of every run — ship a changelog entry, file what you find —
are each larger than the remaining headroom. That is the urgency.

**Where the room is.** `publish.sh` writes the changelog to two paths, and both are contracts:

| path | bytes | who reads it |
|---|---:|---|
| `site/chicago/4d/js/changelog.js` | ~1.4 MB | Manager's ingest and the launcher — the fleet contract path, must not move |
| `site/chicago/4d/walk/js/changelog.js` | ~1.4 MB | the walkthrough's What's-new tab, which imports it |

They are byte-identical. **2.8 MB of a 32 MB budget is one file kept twice**, and it grows by
an entry on every merge, so the headroom shrinks twice as fast as the changelog does.

**Not decided here**, because both paths are contracts and one of them is a fleet contract:

- Have the walkthrough import `../js/changelog.js` and stop mirroring the second copy —
  ~1.4 MB back, needs the What's-new smoke leg. The changelog contract forbids a page
  importing from its own publish mirror; check whether that rule bites here before assuming
  it does not.
- Or split the literal so the walkthrough loads only recent entries and fetches the rest.
- Or compact `tickets.json` — it is generated, pretty-printed at indent 2, and 364 KB. The
  mirror must stay a VERBATIM copy of it (T-0154 gates byte identity), so the source is what
  would change, at the cost of readable diffs.
- Or raise `SITE_BUDGET_MB`, which is the one answer that is not an answer: the number is a
  Pages constraint, not a preference.

**Acceptance:** the gate's own note states the headroom in bytes rather than a rounded MB,
and the published tree has room for a year of changelog entries and tickets without a
further decision.

---

## The second finding, unticketed for want of 645 bytes

**`check.sh` is red on unmodified `dev`.** Measured the same day on a clean worktree of
`origin/dev` at `06a0a9ec` with nothing applied: `./tools/check.sh` exits 1. The dev gate is
`check.sh` and nothing else (`docs/PIPELINE.md`), so every branch inherits a failing gate and
no PR can show a green one on its own merits — T-0511 could only verify itself by diffing its
failure set against dev's, line by line, which is not a gate.

What fails on unmodified `dev`:

- `pilot_75_cohort.json`, `pass_02_75_cohort.json` and `pass_03_75_cohort.json` read **stale**
  against `select_resident_research_pilot.py`, `_pass_2.py` and `_pass_3.py`. Passes 4 and 5
  are current, so whatever moved under them moved recently.
- `pass_13_76_cohort.json`, `pass_14_76_cohort.json`, `pass_15_76_cohort.json` — the same, and
  those three are the cohorts T-0508/T-0509/T-0510 are being researched against right now.
- the seven cross streets have 34 platted faces, got 0; `blk_washington_clark` stands off the
  modelled ground (SOUTHERN GROUND FAIL); the far-timber census disagrees with what is banked
  (ROADMAP R-BUG5).

**The manifests are frozen on purpose** — a cohort is fixed before it is researched — so the
answer is emphatically NOT to regenerate them until it is known what moved. A cohort that
silently re-derives to a different 75 people invalidates the research already filed against
it. Find what moved the population frame first.

Give this its own ticket as soon as there is room for one.
