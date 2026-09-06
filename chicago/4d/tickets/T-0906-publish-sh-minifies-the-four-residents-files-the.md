---
id: T-0906
title: publish.sh minifies the four residents files the T-0838 drift ratchet expects pretty, so every PR that publishes lands the gate red
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

publish.sh minifies the four residents files the T-0838 drift ratchet expects pretty, so every PR that publishes lands the gate red.

FOUND WHILE LANDING T-0769, whose PR runs `./tools/publish.sh` as every 4D PR must.

`tools/synthesize_resident_research.py --drift` is a BYTE comparison: it copies
`chicago/4d/data`, `chicago/4d/docs/RESEARCH` and `site/chicago/4d/data` into a scratch
tree, re-runs the writer over it, and fails on any file whose bytes differ from the
committed one. `tools/publish.sh` publishes the residents layer MINIFIED, on purpose and
only there (see its comment: 1,380 hand-annotated files, `data/residents/` itself stays
diff-readable). The two rules meet on the four files the writer currently stands in the
mirror — `site/chicago/4d/data/residents/index.json` and the `hh_adams_william_h`,
`hh_miller_john` and `hh_murphy_john` households. `dev` carries them PRETTY, which is what
the writer emits and what the ratchet expects; running `publish.sh` rewrites them
MINIFIED, and `tools/check.sh` then goes red with four `has drifted from the writer and is
not on the T-0838 baseline` lines.

The content is identical either way — checked, the parsed JSON of the committed pretty
copy and of the writer's output are equal — so this is a formatting collision and not a
data one. But it means **any** PR that publishes lands the gate red on work it never
touched, and the only way past it today is to revert those four paths by hand, which is
what T-0769's PR did.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

1. `./tools/publish.sh` followed by `./tools/check.sh` is green on an otherwise untouched
   `dev`, and is green again after a change that makes the writer move one of the four.
2. Decided one way and written down: either the minifier skips the paths the drift gate
   compares, or the gate parses instead of comparing bytes for the published mirror, or
   the writer emits the mirror already minified. One of them, with the reason.
3. A case in whichever tool changes, so the collision cannot come back unnoticed.

**Links:** T-0838 (the ratchet) · T-0837 (the spend that emptied its baseline) ·
`tools/publish.sh` § PUBLISHED MINIFIED, AND ONLY HERE ·
`tools/synthesize_resident_research.py` § DRIFT_ROOTS.
