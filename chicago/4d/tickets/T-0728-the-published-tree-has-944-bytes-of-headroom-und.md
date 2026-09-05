---
id: T-0728
title: The published tree has 944 bytes of headroom under the 32 MB budget, and 2.8 MB of it is two byte-identical copies of changelog.js
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

The published tree has 944 bytes of headroom under the 32 MB budget, and 2.8 MB of it is two byte-identical copies of changelog.js.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Measured 2026-09-05 on `dev` (T-0511's run, which tripped it).

`tools/validate.py`'s `run_site_check` fails the gate when `site/chicago/4d/` exceeds
`SITE_BUDGET_MB = 32`, because GitHub Pages cannot serve Git LFS objects. On `dev` the tree
is **33,553,488 bytes** — 31.9989 MB, **944 bytes under the ceiling**. The note it prints,
`site check: published tree 32.00 MB of 32 MB budget`, rounds the headroom out of sight.

**What that means today:** the next PR that adds more than 944 bytes to the published tree
fails the gate, whatever it is about. T-0511 hit it with a single changelog entry (1,632
bytes, mirrored twice by `publish.sh` = 3,264) and dropped the entry rather than widen into
this. **The project currently cannot ship a changelog entry.**

**Where the room is.** `publish.sh` writes the changelog to two paths and both are contracts:

| path | bytes | who reads it |
|---|---:|---|
| `site/chicago/4d/js/changelog.js` | ~1.4 MB | Manager's ingest and the launcher — the fleet contract path, must not move |
| `site/chicago/4d/walk/js/changelog.js` | ~1.4 MB | the walkthrough's What's-new tab, which imports it |

They are byte-identical. **2.8 MB of a 32 MB budget is one file kept twice**, and it grows
by an entry on every merge — so the headroom shrinks twice as fast as the changelog does.

**Not decided here**, because both paths are contracts and one of them is a fleet contract:

- Have the walkthrough import `../js/changelog.js` and stop mirroring the second copy — a
  one-line renderer change, ~1.4 MB back, needs the What's-new smoke leg. A page importing
  from its own publish mirror is exactly what the changelog contract forbids, so check
  whether that rule bites here before assuming it does not.
- Or split the literal so the walkthrough loads only recent entries and fetches the rest.
- Or raise `SITE_BUDGET_MB`, which is the one answer that is not an answer: the number is a
  Pages constraint, not a preference.

**Acceptance:** the headroom is stated in the gate's own note (bytes, not a rounded MB), and
the published tree has room for a year of changelog entries without a further decision.
