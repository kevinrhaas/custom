---
id: T-0920
title: Any run that publishes turns dev's gate red: publish.sh rewrites four residents files the synthesizer ratchet then refuses, on an untouched dev
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

Any run that publishes turns dev's gate red: publish.sh rewrites four residents files the synthesizer ratchet then refuses, on an untouched dev.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Measured 2026-09-06 in a pristine worktree of `origin/dev` with NO working changes.**
`tools/synthesize_resident_research.py --drift` exits 0. Then `./tools/publish.sh` is run —
nothing else — and the same command exits 1 on four files:

| file | what the ratchet says |
|---|---|
| `site/chicago/4d/data/residents/households/hh_adams_william_h.json` | has drifted from the writer and is not on the T-0838 baseline |
| `site/chicago/4d/data/residents/households/hh_miller_john.json` | same |
| `site/chicago/4d/data/residents/households/hh_murphy_john.json` | same |
| `site/chicago/4d/data/residents/index.json` | same — and it is 21,520 lines SHORTER after the publish |

**All four differences are WHITESPACE.** Parsed and compared as JSON, the committed mirror and
the freshly published one are equal object for object on every one of the four — the index goes
from 21,519 pretty-printed lines to one minified line and nothing in it moves. So the payload a
visitor loads is not wrong today; what is wrong is that the committed mirror was written by a
DIFFERENT formatter than the one `publish.sh` uses now, and the synthesizer's ratchet compares
bytes. Every run is told to publish in the same commit as its change (AGENTS.md, and the
steward prompt), so every run that obeys either lands 21k lines of unrelated residents churn in
its PR or reverts the mirror by hand and says why. T-0916 did the latter on 2026-09-06 and is
what found this.

**Acceptance:** (state it before working — never weakened to pass)
- Say WHICH side is wrong: the committed mirror (publish it and take the diff, with the 21,520
  lines read rather than blessed) or the writer (in which case the source moved and the mirror
  is the correct older state). Do not `--write-baseline` over it without that answer.
- `./tools/publish.sh` followed by `synthesize_resident_research.py --drift` exits 0 on an
  untouched checkout of dev.
- Name what merged the divergence and when — the index.json gap is large enough to have a date.
