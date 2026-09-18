---
id: T-1316
title: check.sh no longer fits a steward run's 600 s foreground ceiling: 9 m 52 s measured on 2026-09-18, so the gate has to be run in two halves by hand
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-18
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

check.sh no longer fits a steward run's 600 s foreground ceiling: 9 m 52 s measured on 2026-09-18, so the gate has to be run in two halves by hand.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Measured 2026-09-18, on the T-1172 branch, on a steward runner:** `time ./tools/check.sh`
returned `real 9m52.002s` and was killed by the 600 s foreground ceiling a steward run is
held to (AGENTS.md § the smoke budget states the ceiling; the gate is not covered by it and
has quietly grown past it). Two runs of this ticket's own lane lost a full gate pass to
exactly that, one at 580 s and one at 592 s.

**The workaround that got T-1172 through**, and it is a workaround, not a fix: the script
splits cleanly at its one mid-file assignment. Lines 1–2011 plus `check_summary; exit
$CHECK_FAILED` is a valid first half (228 steps), and lines 1–37 plus 2012–end is a valid
second (259 steps) once `_check_tools` is set by hand, because `$0` no longer names the real
script. Both halves ran green inside the ceiling.

**What a fix looks like.** A `CHECK_PART=1|2` (or a `--from`/`--steps` selector) on check.sh
itself, so a run can take the gate in two foreground commands without generating scripts in
`/tmp`; and a printed total so the next growth past the ceiling is a number somebody sees
rather than a timeout somebody debugs. AGENTS.md's claim that the gate "takes seconds and
needs no Blender" is now wrong on the first half of the sentence and should say the measured
figure.

**Why it matters more than it looks.** A gate that cannot be run whole is a gate a run is
tempted to skip, and the culture here rests on it being cheap.
