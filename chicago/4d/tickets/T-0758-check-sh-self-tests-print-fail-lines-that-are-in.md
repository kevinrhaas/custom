---
id: T-0758
title: check.sh self-tests print FAIL lines that are indistinguishable from a failing step, and three tickets misdiagnosed dev's red on them
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

check.sh self-tests print FAIL lines that are indistinguishable from a failing step, and three tickets misdiagnosed dev's red on them.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Measured 2026-09-05.** `check.sh` marks a failing step with `^ <label> failed` and
nothing else. But several steps are self-tests that deliberately BREAK a derivation and
assert the checks fire, and when a check fires it prints the same `FAIL <sentence>` it
prints for real. On dev today that is 6 lines: `FAIL the seven cross streets have 34
platted faces — got 0`, two `SOUTHERN GROUND FAIL`, and three `FAIL — the far-timber
census disagrees with what is banked`. Every one is the self-test working.

T-0745 read all six as red and wrote three of its four acceptance clauses against them;
had it been worked as filed, a run would have spent itself on street geometry and
terrain that are fine. It is the third ticket in two days to describe dev's red wrongly.

**Acceptance:** a reader of `check.sh` output can tell a fired assertion from a failure
without knowing which steps are self-tests — the cheapest form being a prefix the
self-test steps emit (`fired:` is already used by two of them) or a per-step summary
line, and the failing-step roll-up printed once at the end rather than only inline.
Whatever the shape, `grep` on the output must not be able to find a red that is not one.
