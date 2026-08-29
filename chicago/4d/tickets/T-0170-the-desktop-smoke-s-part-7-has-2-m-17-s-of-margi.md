---
id: T-0170
title: The desktop smoke's part 7 has 2 m 17 s of margin, and it is the one measured over the ceiling on another runner
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0121
opened: 2026-08-23
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The desktop smoke's part 7 has 2 m 17 s of margin, and it is the one measured over the ceiling on another runner.

**Acceptance:** part 7 is halved at a section boundary re-verified for crossing bindings and
each half is measured at 1280x800 with at least four minutes of margin, its second half given
whatever idempotent prologue its first line needs, and the two halves' staged-check counts sum
to the 36 part 7 takes today — never dropping a check. The ROADMAP profile
(§ THE RUN BUDGET) gets the two new readings.

**Why, and why it is not already done.** T-0167 measured the desktop profile the eight-way cut
had never been sized from, and cut part 8 — the thinnest margin at 1 m 14 s, and the most
check-dense part of the suite. Part 7 is what is left at the bottom of that table: **7 m 43 s,
2 m 17 s of margin**. Two readings have to be held together and they disagree — the same part,
on a body that had not grown in between, was **killed at 10 m 00 s on T-0166's runner** three
days earlier. The desktop numbers move by minutes between runs because SwiftShader's cost tracks
whatever else the machine is doing, so part 7 is a part that HAS overrun, and 2 m 17 s is not
enough margin to say it will not again.

**What T-0167 left for this ticket rather than doing.** Part 7 has no `// --- section ---`
headers inside it, unlike part 8, so its boundary has to be found rather than picked: the
`SMOKE_TIMING=1` profile of it puts the cost at 0 m 48 s → 2 m 56 s (the flora census and the
sward), 3 m 38 s → 4 m 50 s, and 5 m 43 s → 7 m 43 s, so there is more than one candidate. It
also holds one half of the `streetLayer` reading taken above the stage split under
`anyStage(5, 7)` — whichever half keeps the street checks has to be the one named in that guard,
and if they end up split across both halves the guard becomes `anyStage(5, 7, 8)` with the
renumbering that implies. Part 7 is NOT the tail, so unlike T-0167's cut this one renumbers
every part after it, including the mobile recipe and the pairing rule.

**A third reading, and it is the third that decides it — 2026-08-29, from T-0358's gate.**
Desktop part 7 was **killed twice on one runner** on the published tree, at `timeout 590` and
again at `timeout 592`, so it cost **more than 9 m 50 s on both attempts**. That is not the
2 m 17 s margin; it is a breach, and it reproduces. The rest of the same gate fitted on the same
runner in the same hour — desktop 4 at 9 m 49 s (11 s of margin, T-0173's ticket), 5 at 8 m 51 s,
9 at 4 m 21 s, and every mobile leg — so the machine was not simply slow. Two readings could be
called a disagreement; three, with two of them kills, are a part that does not fit. The T-0358 PR
had to report the desktop repeat of part 7 as unrun and lean on the mobile leg, which covers the
same assertions, to say the change was gated.
