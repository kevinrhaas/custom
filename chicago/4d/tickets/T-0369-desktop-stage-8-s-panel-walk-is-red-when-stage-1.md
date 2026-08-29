---
id: T-0369
title: Desktop stage 8's panel walk is red when stage 1 runs before it and green when stage 8 runs alone
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Desktop stage 8's panel walk is red when stage 1 runs before it and green when stage 8 runs alone.

**Acceptance:** the desktop smoke's stage 8 gives the same verdict whether it runs alone or after
stage 1, and the reason for today's difference is written down rather than worked around.

**Measured 2026-08-29 on an UNMODIFIED `dev`** (published mirror, `--published`), by T-0316's run
while establishing whether its own branch was red:

```
SMOKE_VIEWPORT=desktop SMOKE_STAGE=8    → 37 passed, 0 failed   SMOKE PASS
SMOKE_VIEWPORT=desktop SMOKE_STAGE=1,8  → 75 passed, 1 failed
  FAIL desktop 1280x800: the suite body ran to completion
       Error: clickChrome: .panel-tab[data-tab="settings"] is covered at its own centre by <h2>
```

Same commit, same viewport, same target, one command apart. Stage 8 alone reaches the settings tab;
stage 8 after stage 1 finds it covered by an `<h2>` — so a run's verdict on stage 8 depends on which
other stage it was asked for in the same invocation, and the stage split exists precisely so a run
can ask for a subset.

This is the SECOND instance of the shape **T-0349** records ("The signboard gate is red when stage 1
runs before it and green when stage 2 runs alone"), on a different gate. Whatever stage 1 leaves
behind in the page — the panel it opened, a scroll position, a `localStorage` key — is the shared
cause worth finding once. Both tickets should probably be answered by the same repair; whoever takes
one should read the other.

**Why it matters beyond the two gates.** A steward run cannot take the whole desktop gate (T-0346),
so it takes stages — and a subset that is red only because of its own composition costs every branch
an argument about whose failure it is. This run had to re-run `dev` twice to establish that its own
change was innocent.
