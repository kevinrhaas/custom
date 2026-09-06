---
id: T-0884
title: tools/publish.sh minifies three household mirrors the resident writer owns, and the T-0838 drift gate fails the next PR that publishes
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

tools/publish.sh minifies three household mirrors the resident writer owns, and the T-0838 drift gate fails the next PR that publishes.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

FOUND BY T-0881, WHICH TRIPPED IT AND WORKED AROUND IT. `tools/publish.sh` copies
`data/residents/` into the mirror and MINIFIES it — deliberately, and the comment there says
why. `tools/synthesize_resident_research.py` also writes into `site/chicago/4d/data`, and it
writes PRETTY. Whichever ran last owns the bytes.

Dev today is in the writer's state for exactly four files —
`site/chicago/4d/data/residents/households/hh_adams_william_h.json`, `hh_miller_john.json`,
`hh_murphy_john.json` and `site/chicago/4d/data/residents/index.json` — every other household
mirror is minified (400 of 400 sampled). So the writer ran after the last publish, and the
T-0838 drift baseline is EMPTY, which means the next run to call `publish.sh` re-minifies those
four and `check.sh` goes red on drift it did not cause.

T-0881 got past it by `git checkout -- site/chicago/4d/data/residents/` after publishing, which
is a workaround and not a fix: the same four files will trip the next slice, and the one after.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- One writer owns those bytes. Either `publish.sh` stops minifying what the synthesis writer
  publishes, or the synthesis writer publishes what `publish.sh` would, or the drift gate is
  taught which paths `publish.sh` owns — argued, not chosen by whichever is easiest.
- `bash tools/check.sh` green after a `tools/publish.sh` run with no hand-reverting of any file.
- The four files above are on whichever side the ruling puts them, in the same commit.
