YªçŠx-®éÜj×¢ëiºÚ+Š§j[h‘éÜ¢éíß|ë­õóÏ<o+^²‰¢¶×# ROADMAP

The build order and the work parcels. `docs/PLAN.md` carries the full reasoning; this is the
operational view â€” what to pick up next, and what it depends on.

```
S0 scaffold â”€â”¬â”€â–º S1 georeference + datum â”€â”€â–º S2 terrain e1834 â”€â”€â–º S3 M0 Sauganash walkable
   [DONE]     â”‚        [DONE]
              â”œâ”€â–º R1 renderer shell (synthetic geometry) â”€â”€â”€â”€â”€â”€â”€â”€â”˜
              â”œâ”€â–º P1 research dossiers (read-only) â”€â”€â–º S5 structure records â”€â”€â–º S8 M1
              â””â”€â–º S4 archetype generators (golden params) â”€â”€â”€â”€â”€â”€â–º S5 bakes
S2 â”€â”€â–º S6 flora + fauna â”€â”€â–º S7 polish, audio, perf â”€â”€â–º release sweep
```

**Critical path: S1 â†’ S2 â†’ S3.** The datum gates every coordinate in the project. Work that does
not need coordinates is deliberately structured to proceed in parallel.

### Resident identity research â€” third pass in progress 2026-09-02

Three reproducible passes now cover 225 of 848 eligible real named people (26.5%):
47 corroborated findings, 45 unmerged candidate identities and 133 documented no-find
outcomes cumulatively. `docs/RESEARCH/resident_identity_pass_03_75.md` records the third
cohort, evidence, duplicate probes and limits. The next parcel should inspect original
newspaper columns, adjudicate the strongest regional candidates and continue through land,
probate, naturalization, marriage and church records with a new non-overlapping manifest.
Reconstructed residents remain outside this programme.

---

## THE OVERNIGHT LANES â€” 2026-08-14 Â· **START HERE**

Two lanes, opened on the owner's instruction of 2026-08-14 alongside the activation of
`docs/RENDERING.md` and the `dev` â†’ `main` pipeline. Everything below:

- **targets `dev`.** Branch `steward/<topic>` off `dev`, PR into `dev`, merge when the dev
  gate is green. Production moves only when the owner dispatches
  `chicago-4d-promote-to-prod.yml`. See `docs/PIPELINE.md`.
- **is ONE parcel per run.** Claim it first (the K16-style heading below), check `git log`
  and open PRs, then work only inside your parcel's file list.
- **is disjoint by construction.** Lane 1 touches renderer and tool files; lane 2 touches
  data and docs. **They cannot collide**, so one of each may run at the same time. Two
  parcels from the SAME lane may not.
- **stays vocabulary-agnostic on confidence names while K16 is in flight.** Name the three
  levels by function â€” source-attested, reasoned-from-specific-evidence,
  invented-to-fill-a-need â€” and read `docs/PROVENANCE.md` at your arrival date for the
  current strings.
- **never installs Blender.** Geometry arrives via the nightly `chicago-4d-bake.yml`, which
  now branches off `dev` and PRs into `dev`. A parcel needing new geometry ships the
  data/archetype half and says so.

### THE RUN BUDGET IS 150 MINUTES, AND THE SMOKE COSTS 26 OF THEM

Set 2026-08-14 on the owner's instruction â€” *"if it's too long we will want to break it into
pieces"* â€” after a run was cancelled at exactly 150 minutes having committed nothing.

**The arithmetic, measured rather than estimated.** `steward-improve` allows 150 minutes
(raised from 90 that day, because runs of 95, 81 and 70 minutes were real work being destroyed
at the ceiling). One `tools/smoke_renderer.mjs` pass costs **~26 minutes** at both viewports.
`tools/critic_shots.mjs --metrics` costs ~12 minutes for the full station set, ~3 with
`--stations`. So a parcel gets **roughly four smoke-equivalents in total**, and it also has to
read, think, write, publish and open a PR inside that.

**The rule: a parcel whose acceptance needs more than TWO full smoke passes must be split
before it is claimed.** Measure-then-fix parcels are the ones that breach this, and they split
along a seam they already have:

- **(a) land the failing gate** â€” build the measurement, prove it fails on the current build,
  commit it red with the numbers quoted. One smoke.
- **(b) fix it green** â€” take (a)'s committed numbers as the baseline. One smoke.

This is better than a time-saving trick: it forces the measurement to be committed *before*
anyone knows which candidate cause is guilty, so the fix cannot quietly redefine success. It
is exactly how R-BUG2 succeeded â€” *"measure before choosing"* refuted its own prime suspect.

**Use `--stations` and `SMOKE_VIEWPORT`.** `critic_shots.mjs --stations a,b,c` runs in about
2 minutes instead of 13; the smoke takes `SMOKE_VIEWPORT=desktop` for a single viewport while
iterating. Full runs belong at the end, not in the loop. (**Corrected 2026-08-15 by R-W4a**:
this paragraph promised a `--stations` flag that did not exist and a `--only` flag the smoke
does not have, so every run that took the advice ran the full set. `--stations` exists now and
was measured at 2 min 03 s for three desktop stations. The full both-viewport `--metrics` run
now costs 13 min with R-W4a's second capture.)
**Updated 2026-08-15 by R-W4c(a), which added a THIRD capture (flower heads hidden).** Measured
on the same three desktop stations: **3 min 45 s**, against R-W4a's 2 min 58 s for two captures
and the original 2 min 03 s for one. The full both-viewport run was **not** re-measured â€” 13 min
is R-W4a's figure and the third capture will have added to it. `--no-mask` drops both extra
captures.
**Use `--stations` and `SMOKE_VIEWPORT`.** `critic_shots.mjs --stations a,b,c` runs in 3 minutes
instead of 12; `SMOKE_VIEWPORT=mobile` runs one viewport while iterating. Full runs belong at the
end, not in the loop.

**AND A CEILING THE RUN BUDGET DOES NOT COVER, measured 2026-08-15 (K21): an agent's single
foreground command is capped at TEN MINUTES, and the desktop half of the smoke does not fit in
it.** The 150-minute figure above is the *run's* budget; the harness a steward run executes in also
caps each individual command, and that is the binding constraint for this gate. Measured on this
runner, serving the published mirror: **`SMOKE_VIEWPORT=mobile` finished in 4 m 43 s, 214 passed /
0 failed. `SMOKE_VIEWPORT=desktop` was killed at 10 m 00 s having passed 151 with 0 failed** â€” an
estimated ~13 minutes end to end, so it fails by about three. Both halves in one command is ~18
minutes and never fits. The trailing `page.click: Target page â€¦ has been closed` in such a log is
the kill, not a failure.

**So a parcel whose acceptance needs the desktop half cannot self-verify it here, and should say so
in its PR rather than quietly merging on the mobile half.** `tools/check.sh` â€” which is the actual
dev gate (`.github/workflows/chicago-4d-check.yml` runs it and nothing else) â€” is unaffected at
~90 s. The durable fix is for the smoke to take a test-name or section filter the way it takes
`SMOKE_VIEWPORT`, so the desktop half can be run as two commands that each fit; until then, the
desktop half belongs to a runner without the per-command ceiling.

**RESOLVED 2026-08-20 by T-0060: the smoke takes `SMOKE_STAGE=1..4`, and each stage fits the
ten-minute command.** The body of each viewport is cut at three section boundaries verified for
crossing bindings (two crossed â€” `terrainLoad`, `streetLayer` â€” and both are now read before the
split; the scans that missed them are written up in the ticket). Measured on the improve runner,
mobile against the published mirror: **stage 1 â€” 1 m 54 s, 74 staged checks Â· stage 2 â€” 3 m 00 s,
91 Â· stage 3 â€” 3 m 17 s, 33 Â· stage 4 â€” 7 m 30 s, 143**, plus 9 always-on checks (boot, loader
problems, run-to-completion, page errors, vendor) taken in EVERY invocation â€” the run prints that
split so the halves can be audited to add up to an unfiltered pass: 341 staged + 9 = 350. The
page-error assertion is no longer the tail of an unrunnable body: a mid-suite throw is caught,
recorded as its own FAIL, and the tail still runs. The unfiltered single-process reference lives
in `.github/workflows/chicago-4d-smoke.yml` (push-to-its-own-path or dispatch on main) â€” that is
the "runner without the per-command ceiling" this section asked for. Desktop stage timings are
not yet measured; stage 4 is the one to watch (its mobile 7 m 30 s includes the shared
street-layer reading), and if it overruns on desktop the fifth cut goes in then, the same way.

**RE-CUT 2026-08-24 by T-0166 (piece 1 of T-0121): the four stages are EIGHT parts, and
`SMOKE_STAGE` takes a range.** The four had eroded exactly as the paragraph above feared, and
faster: by 2026-08-23 three of the four DESKTOP quarters ran past the ten-minute ceiling and the
fourth cleared it by two minutes, so the desktop half a steward run could reach was stage 1
alone. Each quarter is now halved at a section boundary re-verified for crossing bindings, so
**part 2k-1 plus part 2k is exactly T-0060's stage k** â€” the cheap viewport is still four
commands (`SMOKE_STAGE=1-2`, `3-4`, `5-6`, `7-8`) and nothing about the audit changes.

Three of the four new second halves inherited page state rather than a binding, which the
scope-aware scan cannot see and only a part run alone from a fresh boot will show: part 6 and
part 8 boot at the GATE SCREEN (`enterTown()`, T-0060's inline accommodation, now one function
called at the head of four parts), part 8 also needs the PANEL open because its first statement
clicks a tab inside it, and part 4 needs the Sauganash framed because its first check picks
whatever is down the crosshair. All three prologues are guarded on the state they establish, so
an unfiltered run runs them as no-ops.

**The mobile fit, measured on the improve runner against the published mirror** â€” part 1
**1 m 41 s**, 66 staged checks Â· part 2 **1 m 17 s**, 66 Â· part 3 **0 m 52 s**, 65 Â· part 4
**3 m 17 s**, 38 Â· part 5 **2 m 52 s**, 19 Â· part 6 **0 m 44 s**, 14 Â· part 7 **3 m 48 s**, 36 Â·
part 8 **4 m 19 s**, 107 â€” 411 staged checks plus the 9 always-on ones every invocation takes,
and 18 m 50 s of wall clock for eight boots. Every part is inside the ceiling by at least five
minutes. (Part 5 carries T-0114's two road-legibility failures, which are red on `dev` today and
are that ticket's, not this cut's.)

**The audit was taken against the old code rather than asserted.** Running `origin/dev`'s own
`smoke_renderer.mjs` beside the re-cut one, at mobile on the published mirror: old stage 1 gives
**132 staged / 9 always-on / 141 passed**, and new `SMOKE_STAGE=1-2` gives **132 / 9 / 141**. Old
stage 3 gives 33 staged with T-0114's two failures; new parts 5 and 6 give 19 + 14 = 33 with the
same two failures, which is also where those failures are demonstrated to be `dev`'s and not this
cut's.

**Every invocation now prints its own wall clock on its last line**, which is the cheapest
possible early warning: this ceiling has been breached three times and each breach cost a run a
hand measurement to discover.

**THE DESKTOP FIT WAS NOT CLAIMED BY T-0166, AND T-0167 IS WHERE IT IS.** The reason it was
deferred stands: `SMOKE_VIEWPORT=desktop SMOKE_STAGE=7` was killed at 10 m 00 s on T-0166's
runner against 3 m 48 s for the same part at mobile, while part 6 cost 0 m 44 s at mobile and
1 m 53 s at desktop â€” so the desktop cost of a part is NOT a fixed multiple of its mobile cost,
the camera-heavy parts scale several times harder than the DOM-heavy ones, and an eight-way cut
sized on the mobile profile could not be assumed to fit.

**THE DESKTOP PROFILE, MEASURED 2026-08-24 by T-0167** â€” eight foreground commands at 1280x800
on the improve runner against the published mirror, one part each, `SMOKE_TIMING=1`:

| part | desktop | margin | staged checks | mobile (T-0166) |
|---|---|---|---|---|
| 1 | **3 m 31 s** | 6 m 29 s | 66 | 1 m 41 s |
| 2 | **2 m 37 s** | 7 m 23 s | 66 | 1 m 17 s |
| 3 | **1 m 40 s** | 8 m 20 s | 65 | 0 m 52 s |
| 4 | **7 m 07 s** | 2 m 53 s | 35 | 3 m 17 s |
| 5 | **6 m 40 s** | 3 m 20 s | 19 | 2 m 52 s |
| 6 | **1 m 24 s** | 8 m 36 s | 14 | 0 m 44 s |
| 7 | **7 m 43 s** | 2 m 17 s | 36 | 3 m 48 s |
| 8 | **8 m 46 s** | 1 m 14 s | 107 | 4 m 19 s |

408 staged checks plus the 9 always-on ones every invocation takes, and **39 m 28 s** of wall
clock for eight boots. (Mobile's 411 is these 408 plus the three checks part 4 takes only at
mobile.)

**The table above was taken at `ac1abb80`**, and T-0166's mobile column at the same commit.
T-0114 merged into `dev` while this run was measuring and changed `streets.js`, so the parts
that read the roads â€” 5 and 7 â€” will have moved a little since, and part 5's reading was taken
with T-0114's road-legibility check still failing. The re-cut readings below, and the audit,
were re-taken on top of T-0114.

**NOTHING OVERRAN, AND THAT IS NOT THE SAME AS FITTING.** Two readings have to be held together:
part 7 measured 7 m 43 s here and was KILLED at 10 m 00 s on T-0166's runner three days earlier,
on a body that had not grown in between. **These desktop numbers move by minutes between runs**
â€” SwiftShader is a software renderer and its cost tracks whatever else the machine is doing â€” so
a part is not sized by whether one reading cleared the ceiling but by how much margin it has when
it does. A 74-second margin is not a margin.

**RE-CUT 2026-08-24 by T-0167 (piece 2 of T-0121): part 8 is halved and there are NINE parts.**
Part 8 was both the thinnest margin on the profile and the most check-dense part of the suite by
a factor of three, which is the combination worth cutting. It is also the TAIL, so the new part
is APPENDED and parts 1-7 keep their numbers: the pairing rule survives as 1+2, 3+4, 5+6, **7+8+9**,
and the mobile recipe's last command widens from `7-8` to `7-9` â€” still four commands. The
boundary is the Evidence panel: the profile put 6 m 05 s of the old part 8 above it and 2 m 41 s
below, and the scope-aware scan found three names crossing it (`eye`, `toggles`, `typed`) of which
all three are prose or a different local (`typedE.typed`), so nothing crosses in fact. Part 9's
prologue is `enterTown()` alone â€” the liberties reading already carries its own guarded panel-open
and clicks its own tab, so unlike part 8 it needs no panel guard bolted on.

**Measured after the cut, at desktop: part 8 â€” 6 m 10 s, 28 staged Â· part 9 â€” 3 m 09 s, 79
staged.** 28 + 79 = 107, exactly the old part 8's count, which is how "never dropping a check" is
demonstrated rather than asserted. Both were taken twice, once at `ac1abb80` (6 m 08 s / 3 m 08 s)
and again on top of T-0114 â€” the same counts and within two seconds either way, which is also a
reading on how much of the desktop variance is the scene and how much is the machine. The worst
desktop margin is now **part 7 at 2 m 17 s**, and it is the next one to go â€” T-0170, which also
records why it was not taken in the same run: part 7 has no section headers to cut at, it holds
one half of the `anyStage(5, 7)` street-layer reading, and it is not the tail, so cutting it
renumbers everything after it. The audit was taken at mobile too: old `SMOKE_STAGE=7-8` gives 143
staged / 9 always-on / 152 passed and new `7-9` gives **143 / 9 / 152**, in 5 m 53 s against
5 m 49 s.

**AND THE HEADING OF THIS SECTION IS OUT OF DATE BY A FACTOR OF TWO.** "The smoke costs 26 of
them" was measured on 2026-08-14. T-0167's profile puts the staged gate at **39 m 58 s of desktop
across nine commands plus 13 m 26 s of mobile across four** â€” call it **53 minutes**, better than a
third of the 150-minute run budget, and that is before a part is re-run after a fix. The two-full-
passes rule above should be read as ONE full pass and a re-run of the parts a change touches; a
parcel whose acceptance needs the whole gate twice has already outgrown a run.

**RE-CUT 2026-08-30 by T-0173: part 7 is halved and there are TWELVE parts.** T-0346 cut part 4
into three that morning; part 7 went the same way by the evening. Profiled with `SMOKE_TIMING=1`
on the steward runner at **load average 0.81-2.86, 4 cores**, part 7 was **killed at 9 m 25 s**
with its last two assertions unrun â€” so the reading in T-0167's table above, 7 m 43 s, is again a
description of a machine rather than of the part. **7 m 04 s of that cost was ONE block**: the
three road-legibility stations, each teleporting to its own viewpoint and reading
`page.screenshot` frames through five distance bands (`south_water` 2 m 13 s, `from_above`
2 m 02 s, `lake_market` 2 m 49 s). Around it, 20 s of boot, 33 s of navigation and the street
checks, 1 m 04 s of the R-A1 aid and the batch merge under it.

**So the boundary is not a section header, and T-0170 had already said why it could not be.** The
best of part 7's own `// --- ` boundaries leaves 7 m 37 s against 1 m 30 s. The cut falls at the
STATION â€” the grain the block is made of â€” and nothing crosses it: `roadRuns` is local, the
movement report built from it is printed and never gated and has always compared only what the
invocation measured, and `--update-road-bands` merges per band. R-A1's three assertions are taken
standing at `lake_market`, so that station moves into the new part with them.

**Measured after the cut, at desktop, on the same runner in the same hour: part 7 â€” 5 m 05 s, 12
staged Â· part 8 â€” 5 m 06 s, 8 staged, both SMOKE PASS.** 12 + 8 = 20, exactly the old part 7's
count. Both clear the ceiling by 4 m 55 s. Part 7 keeps the shared `streetLayer` reading, so the
guard becomes `anyStage(7, 10)`; part 8's profile â€” boot at 0 m 17 s, first station at 3 m 17 s â€”
is the proof it does not pay for it. Parts 8-11 are renumbered 9-12; the pairing rule survives as
1+2, 3+4+5+6, **7+8+9**, **10+11+12**, ranges `1-2 3-6 7-9 10-12`. The audit was taken at mobile
too: old `SMOKE_STAGE=7-8` gave 43 passed and new `7-9` gives **43 passed, 34 staged** in 7 m 33 s,
and `10-12` gives 168 passed / 159 staged in 9 m 33 s. **The worst desktop margin left on the
profile is what was part 7 and is now part 10 â€” T-0170, still open**, which this cut re-labels
rather than takes.

**RE-CUT 2026-08-30 by T-0170 (the last piece of T-0121): part 10 is HALVED and there are
THIRTEEN.** Part 10 â€” the part T-0173 above hands on as "the worst desktop margin left" â€” was
never inside the ceiling at all. Profiled at 1280x800 on an **idle** runner (load average
0.27-1.48, zero other Chromium processes, so this is the friendliest reading the suite can be
given) it was **killed at 9 m 20 s with the street readouts and the Settings units still to
run**. That is the third and fourth kill of the same part; T-0167's 7 m 43 s is the outlier in
the record rather than the reading to size a cut from.

**Why it had been left, and what changed.** This part carried no `// --- section ---` headers at
all, which is exactly why T-0167 cut part 8 instead: the boundary had to be MADE before it could
be taken. Its seams are named now â€” eight of them, five in the head and three in the tail â€” so
the next cut in this part is a choice from a list rather than a fresh profile.

**The cut is the second candidate, and the first one is in the record because it was measured
and rejected.** Cutting above R-BUG7's flower-head census gave **5 m 05 s / 6 m 24 s** â€” a
3 m 36 s margin on the second half, and this section's own rule is that a margin that thin is
not a margin. Moving that one section up into the first half balances it:

| part | desktop | margin | staged checks | what it is |
|---|---|---|---|---|
| 10 | **5 m 59 s** | 4 m 01 s | 23 | the drawn population, the horizon timber, the sward census in every community, the marsh substrate, T-0035's pop-in, R-BUG7's heads |
| 11 | **4 m 41 s** | 5 m 19 s | 13 | the ragged boundary and its fringe, each community's recorded ground cover, the street readouts, the navigation guide, the Settings units |

23 + 13 = **36**, exactly the count the part took before the cut, which is how "never dropping a
check" is demonstrated rather than asserted. The second half is SMOKE PASS; the first half's one
red is **T-0279's flower heads** (2,693 of 18,893), which `tools/dev-smoke-state.json` already
records as dev's on 2026-08-29 at 2,526 of 18,911 â€” it moved parts, not sides, and it does not
fire at mobile at all.

**The audit was taken against the old code rather than asserted.** Running the pre-cut
`smoke_renderer.mjs` beside the re-cut one, at mobile on the published mirror and on the same
tree: the single part gives **45 passed / 0 failed / 36 staged / 9 always-on in 5 m 59 s**, and
the pair gives **45 / 0 / 36 / 9 in 6 m 01 s** â€” one boot for the pair, which is why the mobile
recipe does not grow a command.

**One binding crosses the new boundary and it is the one that already crossed the stage split.**
`streetLayer`, and BOTH halves read it â€” the head for the road panels and the horizon band, the
tail for the readouts â€” so the guard becomes `anyStage(7, 10, 11)`. The scan turned up six other
names below the line (`headSupport`, `horizon`, `over`, `planted`, `popIn`, `sward`) and every
occurrence is prose or a string. The second half's prologue is `enterTown()` and `setFly(false)`:
every camera-bearing section below it teleports itself, but all of them read the drawing from a
walker on the ground and the last thing the part does is fly.

**AND THESE READINGS WERE TAKEN AT LOAD 0.9-5.1 WITH NO OTHER AGENT ON THE BOX**, which is the
condition this section demands be recorded. T-0215's factor of twenty applies to them the same as
to every row above: 4 m 01 s of margin is a margin against the machine that measured it, and no
cut of this suite survives load 50. Old parts 11-12 are renumbered 12-13; the pairing rule
survives as 1+2, 3+4+5+6, 7+8+9, **10+11+12+13**, ranges `1-2 3-6 7-9 10-13`.

**`SMOKE_TIMING=1` stamps every check line with the elapsed clock**, and T-0167 added it because
the profile could not have been taken without it. A part that BREACHES the ceiling is killed
*before* it prints its wall clock, so the parts actually worth cutting were the only ones a plain
run reported nothing about â€” T-0166's part 7 reading is literally ">10 m", and nothing else. With
the stamp on, a killed run is still a profile of everything it reached, which is what places the
next cut. It is off by default so the gate's own output stays comparable between runs.

**AND EVERY NUMBER IN THE TABLE ABOVE IS A READING OF THE MACHINE AS MUCH AS OF THE SUITE â€”
T-0167 said so, and 2026-08-27 put a factor on it.** T-0167 wrote that "these desktop numbers move
by minutes between runs because SwiftShader's cost tracks whatever else the machine is doing", and
sized its cuts on margin rather than on any single reading. **T-0215 measured how far that goes.**
On a box carrying a dozen parallel agents â€” load average **38.7-51.7**, **71-115** concurrent
Chromium processes â€” ten consecutive animation frames of this scene cost

**17,036 Â· 29 Â· 333 Â· 21,451 Â· 20,211 Â· 119 Â· 4,420 Â· 22,280 Â· 12,242 Â· 26,580 ms**

against the **0.46-1.10 s** of 2026-08-13. That is a factor of twenty on the quantity every
Playwright action is denominated in, and the 29 ms frames in the same sample are the proof it is
contention rather than the scene. Boot to `ready` measured **29 s, 106.8 s and 127.4 s** on one
tree inside twenty minutes, against the 30 s the boot check allows; two runs had their browser
killed outright; a `page.goto` against a **local static file server** timed out at 30 s. So:

- **A part's timing is only comparable to another taken under the same load.** Record the load
  average and the Chromium process count beside any reading added to the table above, the way
  T-0215's are recorded in its ticket. A margin measured at load 2 is not a margin at load 50.
- **A `page.click` timeout on this suite is a question, not a verdict.** It has now twice been
  read as a broken control and twice been the budget â€” 2026-08-13 and 2026-08-27, the second time
  by three separate agents on one day. The smoke now prints what a frame costs whenever an action
  times out, and `clickChrome` (part 8's fourteen chrome clicks) takes the panel chrome out of the
  race entirely without dropping one assertion. See STATUS 2026-08-27.
- **The ten-minute ceiling this section exists to fit is not the binding constraint on a loaded
  box.** Part 8 measured 6 m 10 s at desktop on 2026-08-24 and could not reach its first assertion
  in 4 m 23 s on 2026-08-27. Cutting parts finer does not help that; running fewer of them at once
  does (T-0216).

**AND THE CONTROLLED A/B, TAKEN WHEN THE BOX DRAINED.** `origin/dev`'s own unmodified harness, on
the same tree, at load 10.4-13.7 with 20-24 Chromium processes: **37 passed, 0 failed, all 28
staged checks, SMOKE PASS â€” in 14 m 33 s.** Two readings to hold together. Stage 8 was never
broken: the harness that failed three agents is green on a quieter machine. And it does not fit:
**14 m 33 s is four and a half minutes past the ten-minute ceiling**, on a part T-0167 measured at
6 m 10 s three days earlier and cut to that size deliberately. So the table above is a *floor* on
what these parts cost on a shared box, not a description of it. T-0215's `clickChrome` puts part 8
back at **6 m 10 s** â€” T-0167's figure to the second, all 28 checks â€” by not paying for frames
where the frames are not the subject. Desktop-only: the same part costs 2 m 52 s at 390Ã—780, where
a frame covers a quarter the pixels.

### NEXT UP â€” every row says whether a visitor can SEE it

**Rewritten 2026-08-15 on the owner's report that the loop does research and organisation rather
than work on the app. Measured: 15 of the last 30 changelog entries say nothing you can see
changed, and v124â€“v137 is fourteen invisible runs in a row.** Two causes, both fixed here. The
first is the rule â€” see AGENTS.md Â§ THE VISIBLE-PROGRESS RULE, which caps invisible runs at one in
four. The second is this table: it had grown ~20 completed rows above the live picks, so the
visible parcels were the hardest ones to find. Completed work now lives in its own section below,
not at the top of the queue.

> ## â›” THIS TABLE IS FROZEN AS OF 2026-08-17 â€” THE LIVE QUEUE IS `tickets/QUEUE.md`
>
> On the owner's direct request the operational backlog moved to **`tickets/`**: one file
> per ticket, `QUEUE.md` holding the priority order (the owner orders it; agents only append
> and remove), `BOARD.md` generated, and `tools/ticket.mjs check` gating it all in check.sh.
> His requests were untraceable in this file â€” the K-series he asked for in August was
> sitting below line 9,300 with no status tags while the loop picked from this table â€” and
> he could not reorder priorities without editing prose. Every open parcel below became a
> ticket carrying its old id in `legacy_id`; the deep boxes in this file remain the
> reasoning archive and tickets link into them. **Do not add rows here. Do not pick from
> here. Read AGENTS.md Â§ THE QUEUE.**

| # | lane | parcel | why first |
|---|---|---|---|
| â€” | RENDERING | ~~R-BUG7~~ | **SEEN** | **DONE 2026-08-17 â€” the stalk was aimed at the stem and then TURNED to a random bearing, and now the flower is hung by its foot.** `maybeHead` computes `tiltAz` so the stalk leans back to the stem and passes a random `yaw` beside it; `push`'s Euler is `YXZ`, so the yaw spins the whole tilted head and the azimuth with it â€” and `push`'s own docstring says *"Pass `yaw` 0 alongside a tilt"*. **Four repairs computed that bearing correctly and not one reached the geometry.** The repair is not a fifth aim: the archetype's origin moved to the FOOT of its own stalk, so the offset from the stem is generated by the rotation and `foot <= plantH` makes attachment an invariant at every fade rather than a number. **38 of 11,752 drawn heads over 32 poses â†’ 0**, all 38 `corymb`, worst foot **58 cm** from any stem; foot-to-stem median **21 mm â†’ 0**. Read its box before adding a per-instance rotation to any set |
| â€” | RENDERING | ~~R-BUG5b~~ | **SEEN** | **DONE 2026-08-16 â€” it was the PLANTER after all, and the whole near-field wood was drawn mirrored.** The loop asks every question in ENU (`isWater`, `communityAt`, `surfaceHeight`, `blocked`, `noteStation`) and hands its ENU north straight to `addTree`, which takes a three world **z** â€” and `enuToWorld` is `(e, y, -n)`. So every tree was TESTED at `(px, pz)` and DRAWN at `(px, -pz)`: **391 stations, 0 wet, 64 of the same 391 wet at their mirror, 10,734 vertices of timber over open water and the worst 48 m from dry ground.** Three green gates all walk `stations`, which is the point that was TESTED â€” **nothing had ever read the geometry back**. Read its box before trusting any placement gate in this file |
| â€” | RENDERING | ~~R-BUG5~~ | **DONE 2026-08-16 Â· a real second fault, but NOT the owner's picture (see R-BUG5b)** â€” it was the SKYLINE, not the planter. Both of the owner's populations are ONE body of far timber authored **between the two banks** of the main stem, 39 of 39 samples over water and **3.347 m** under its surface; the scatter is the horizon solver's own gap modulation breaking the same run into crowns. Both existing gates were green because both count the near-field planter's 632 m square, and **nothing had ever asked the five `FAR_TIMBER` polylines where they stand**. Read its box before quoting any horizon-timber number |
| â€” | RENDERING | ~~R-BUG5(b)~~ | **SEEN** | **DONE 2026-08-27 (T-0031) â€” the owner picked route 1 and the belt is back on the skyline.** `main_stem_belt_east` is now DERIVED from the committed `south_water` centreline â€” offset half a platted corridor south, clipped east at the committed `wells` easting `timberEastLimits()` already hands the near planter â€” and `tools/derive_timber_belt.py --check` re-derives it on every commit. Census **39 of 39 samples over water, 3.347 m deep â†’ 0 of 136**; the old stub also ended **66.7 m east** of the street it was named for. The side of the street is the one assertion and it is **L182** |
| â€” | RENDERING | ~~R-BUG3c~~ | **DONE 2026-08-15** â€” neither surface moved: the publish step quantises the ground onto a **306 mm** vertical lattice AFTER the only gate that measures it, burying the road and the flora by up to **228 mm**. The heights are read back off the field at load, and two gates now hold the file that SHIPS. Read the box before quoting any ground number |
| â€” | RENDERING | ~~R-W4c(a)~~ | **DONE 2026-08-15** â€” the flower-load recipe's hue cut at 50Â° runs through the middle of a July prairie's bloom, so `0.0012` is not a count of flowers. (a) landed the honest measurement; **(b) is the tuning half and must take (a)'s committed numbers as its baseline** |
| â€” | RENDERING | ~~R-W4c(b1)~~ | **DONE 2026-08-15** â€” **there is no 4â€“6 % target.** Its remnant half cites no photograph this repository holds; its planting half does not reproduce (**5.54 %**, and 12.91 % is not on that frame under either ordering); and the repair R-W4c(a)'s diagnosis implies **fails** â€” reordering the tests takes precision **0.998 â†’ 0.062**, so the flower test cannot see a flower either. Read its box before quoting any flower number |
| â€” | RENDERING | ~~R-W4c(b2)~~ | **DONE 2026-08-27 as T-0034 â€” the bar that governs the bloom is the LATTICE, and the records already asked for more bloom than it can draw.** `forbShare` clamps at one plant per lattice slot â€” **0.346 forbs per mÂ²** â€” and the mesic prairie's own records sum to **0.408** at their upper bounds, so nothing had to be invented: the forb stratum is dealt off the TOP of every recorded range instead of its midpoint (L182), which is **1.236x** at the mesic prairie, **1.254x** at the wet prairie, **1.572x** on the sand prairie and, measurably, **nothing at the other six** â€” they were already over the ceiling. `prairie_west` **206 forbs / 1,617 heads â†’ 256 / 1,968**. **It is the last raise either prairie can be given**: both now read a share of 1.000. Read its box before raising any flora density |
| â€” | RENDERING | ~~R-W6~~ | **DONE 2026-08-16** â€” **yes, at 16 bits**, and the artefact was not invisible: the 14-bit ground stands up to **46.3 mm** above the field, past the 22 mm road lift at 87 sample points, **one of them 1.9 m from South Water Street's centreline**. 16 bits costs **1,116 bytes** and takes the worst error to 12.9 mm, under the lift everywhere; the uncompressed 5.8 MB would buy 12.9 â†’ 7.7 mm, and 7.7 is DECIMATION the master carries too. Read its box before quoting any payload or lattice number. **Its 12.9 mm no longer describes the tree** â€” re-measured 2026-08-23 on the terrain as extended east, the same 16-bit ground is **77.1 mm** worst with **56** samples past the lift, on 60â€“90 % slopes that did not exist in the box R-W6 measured. T-0152 |
| â€” | RENDERING | ~~R-BUG4~~ | **DONE 2026-08-15** â€” the wet-corner rule deleted the dry half of a road panel with the wet half. Clipped at the waterline now: **28 panels / 62.7 m** of roadway recovered, and the gate asserts the invariant rather than the number |
| â€” | RENDERING | ~~R-W4a~~ | **DONE 2026-08-15** â€” the horizon figure counted the town's roofs as timber (62 % of it at `prairie_south`), the Gâˆ’B discriminator this project named was measured and **refuted**, and the replacement cannot move when a block lands. Read its box before quoting any horizon number |
| 2 | RENDERING | **R-BUG4** | XS, owner-reported. A wet CORNER deletes a whole road panel, dry half included: **28 panels / 62.7 m** of roadway removed where the centreline is dry land |
| 3 | RENDERING | **R-W4a** | the horizon-timber metric counts gable ends as trees, so W4's headline number is unmeasurable and a town parcel already banked a false pass. Prior to every other W4 half Â· *promoted 2026-08-15: R-M1b, which was #1, is blocked on the owner* |
| â€” | RENDERING | ~~R-M1~~ | **R-M1a DONE 2026-08-15** â€” the two scales are measured and their baseline is committed. **R-M1b is NOT a pick: it is blocked on a threshold source, because the photograph R-M1 named to derive from contains no dirt track.** Read R-M1b's box before touching it |
| â€” | RENDERING | ~~R-M1c~~ | **SEEN** | **DONE 2026-08-16 â€” the road score divided by probes SEEN, so an occluder RAISED it.** One band, three builds, one evening: **seen 157 â†’ 177 â†’ 163** and the old score **62 % â†’ 54 % â†’ 59 %**, while the number of readable stretches never moved off **96** and `nBare` was **182 in all three**. The build with the whole wood on the wrong side of the river scored HIGHEST; K45(b2) would have gone green by planting more timber in front of the road. **The instrument was already built and already printing** â€” `shotMF`'s own comment says the marked-only denominator "drops instead of failing" â€” and nothing had ever divided by it. Scored on `nBare`: **53.3 / 52.7 / 52.7 %**, under the 0.55 bar in all three. Read its box before quoting any road-contrast percentage taken before this date |
| â€” | RENDERING | ~~R-W1~~ | **SEEN** | **LANDED ON `dev` 2026-08-16 â€” the light was wrong by 1.9Ã— and 2.9Ã— red against its own sky, and the honest sky costs the roads.** Literal black pixels 12,063 â†’ 0 at three stations; `south_water` 250â€“600 m falls **71 % â†’ 16 %**. **NOT FOR PROMOTION** until the owner walks `/dev/` or R-W2 buys the contrast back â€” read its release-condition box before any promotion. Its third finding is R-M1d: the suite reported **229/2 before and after**, because a station already red on another band hides a 55-point collapse |
| â€” | RENDERING | ~~R-W2a~~ | **DONE 2026-08-16** â€” the material sheet, measured out of the shipped GLBs: **1,353 material slots, 32 names, 41 colours, 18 roughness values, zero textures**. Five findings, and two of them block texturing outright: **the chimney is not a material here** (219 stacks painted `roof`) and **no record states a roof covering** (315 roof types, 0 coverings). Read `docs/RESEARCH/materials.md` Â§4 before quoting any material number |
| â€” | TOWN | ~~T-A15~~ | **DONE 2026-08-15** â€” `blk_randolph_clark`, the block opposite the courthouse: the first with a store on it, the face rule EXTENDED to rank one (**K32**), the end rule measured at **1.02Ã— / 7.5 m** and declared exhausted (**K31**), and **two of T-A14's three adoption candidacies refuted** â€” the laundress and teamster arguments never claim a floor, so they fail rule 6's test 1. Read finding 3 before quoting any adoption test |
| â€” | TOWN | ~~T-A16~~ | **DONE 2026-08-15** â€” `blk_randolph_lasalle` is **the public square** and is not a building site. It was withdrawn rather than built: no lots, no roofs, a gate, and **two documented buildings moved off it**. The block parcel's own gates all passed on the old placement, because not one of them asks whether the ground was for sale. Read its box before scheduling anything anywhere |
| â€” | TOWN | ~~T-A3h~~ | **DONE 2026-08-15** â€” the last open block entry, and the two adoptions it predicted are the two it made: `blk_randolph_dearborn`'s D3 to the carpenters and its D1 to the labourers, measured with `tools/measure_adoption_tests.py` rather than recalled. **Its finding is about the other two**: the D4 and the D2 that pass as a "second roof" are pairs this layer has NEVER housed â€” the D4 evidence is one household in the NORTH, the D2's is four in the NORTH and WEST â€” so every second-roof refusal K28 has collected is a candidacy built from two projections of one table. Read its box and K28's before quoting any adoption test |
| â€” | TOWN | ~~T-V1(a)~~ | **DONE 2026-08-15** â€” the stamp is **not** at `south_water`: every twin in the town is in the North Division parcel, **36 of its 60 roofs**, and the census found something bigger â€” **40 eaves outside the band their own note cites**, 18 of them in a parcel that samples its footprints and says so. (b) is written, measured and **blocked by a circular dependency in the pipeline** â€” read its box before touching any dimension on a baked record |
| 2 | TOWN | **T-V1(b)** | the sixty North records: **NEEDS ONE BAKE**, and cannot go green on the improve runner. A policy question for the owner, not an engineering one |
| â€” | TOWN | ~~T-I3(a)~~ | **DONE 2026-08-16** â€” the town's public buildings are **three roofs** and this project already had all three, so the refusal is now absolute rather than argued. The finding is the fourth building: **the court-house was not built yet** â€” Andreas fixes the season, the month AND the corner the record said nothing fixed, and the citation it had was a **picture caption** â€” so a record is taken OUT of a scene on evidence for the first time. Read its box before quoting any civic number |
| â€” | TOWN | ~~T-I3(b)~~ | **DONE 2026-08-27 as ticket T-0032, route 1** â€” the owner's "close it at 665 or 662" is closed at **662**: `roof_total` 665 â†’ 662, `I3` 6 â†’ 3, `principal_functional` 511 â†’ 508. The correction found a **second** fault in the same row â€” `institutional_public` was apportioned south 10 / west 1 / north 1 while the named records stand **south 5 / west 1 / north 3** â€” so the south district goes 370 â†’ **365** and the north 150 â†’ **152**, not the 370 â†’ 367 the box predicted. Every I3 slot has left the block schedule and the gate screen now reads *of the 662 the town held*. Read its box before quoting any civic or roof-total number |
| â€” | TOWN | ~~K30(a)~~ | **DONE 2026-08-16** â€” it is **29 buildings on eight streets**, not three on one, and every one of them is a record a PERSON placed: **zero** generated roofs lap a corridor, across 332 placed phases. The depths are bimodal with an empty gap at 1.98â€“3.48 m, and **13 of the 17 deep ones are South Water**. T-A7's "fourteen" does not reproduce **at its own commit** (16 there, the same 16 today), and the anchor-convention suspect is **refuted** â€” recentring makes 10 of the 29 worse. Read its box before quoting any intrusion number |
| â€” | TOWN | ~~K30(b)~~ | **DONE 2026-08-16 Â· ITS CAUSE IS REFUTED 2026-08-22 â€” read K30(d) before quoting any of this row.** The anchors it compares with the half-width are BACK corners, so the comparison could not see the displacement it looked for; the real cause is the committed `south_water` centreline standing 4.3â€“8.8 m south of the control the placements were offset from. Its own text follows: the cause is the **drawing**, and the Wacker made-ground suspect is **refuted** by arithmetic: the anchors sit 11.64â€“15.30 m from the centreline against a 12.192 m half-width, with both signs, so no displacement of 4.51â€“8.17 m is there. The records are derived to their FRONTAGE and drawn with the body growing north from it (331 of 333 footprints grow from the minimum corner), so each stands in the road by its own depth â€” **all 17** deep records, and reflection takes 12 of them under 1 m. **The residual law** settles the shallow tail without moving anything: what survives correct drawing IS the point's own penetration, to 0.10 m. Read its box before quoting any intrusion cause |
| â€” | TOWN | ~~K20~~ | **DONE 2026-08-16** â€” the invented-name allocator, measured properly for the first time: **73 of 113 renamed by ONE new household**, not the 17â€“25 the eleven by-product measurements reported, and never zero in the two big buckets. It is **10** now, and the report prints each bucket's **pool pressure** so the residual cannot be misread â€” at 0.14Ã— it renames **one**, at 2.03Ã— it renames ten, and that is the pool being too small. Unwelding the given name from the surname exposed **two identical residents**. Read its box before quoting any churn number |
| â€” | TOWN | ~~K29~~ | **SEEN** | **DONE 2026-08-27 (T-0022) â€” ITS PREMISE IS REFUTED AND THE RE-APPORTIONMENT IS REFUSED.** L99 and L100 worried that the schedule "will keep dealing cabins to commercial frontage"; measured, the fault ran the other way. South Water Street's line carried **15 invented buildings and NOT ONE of them log**, against a documented line of 8 with Hogan's log store on it, because the recipes' own face rule â€” "the two meanest take Lake" â€” had put all five dealt log dwellings on the OTHER principal thoroughfare. The owner's plate of the row draws it as *log and frame shoulder to shoulder* and this project had taken only the half of that sentence about shape. **No schedule term was written**: ten records changed places, nothing was added, and `tools/measure_frontage_fabric.py` now holds it. K29's other half â€” weighting the trade families ONTO the business front, which the same census supports at 80 % â€” **shipped 2026-08-27 as T-0213**: the documented trade share is monotone in the committed street hierarchy (0.7778 principal / 0.4545 ordinary / 0.0000 light) and `tools/reconcile_665.py` now weights each platted block by its own four faces. Read its box before quoting any frontage rule |
| â€” | TOWN | ~~K28~~ | **DONE 2026-08-16** â€” three questions, three clauses, **two gates, and not one record moved**. The table is **projections** (the pair reading is refused because it refuses T-A4's fourteenth labouring household, one of the four rule 6 says its third test recovers); there **is** a cap, one adoption per trade per block, which is what makes the projections safe; and test 1 means the trade's **own committed text**, so the laundresses' D2 and the teamsters' D4 are refused with the remedy named. All **21** standing block adoptions already obeyed it. Read its box before quoting any adoption rule |
| â€” | TOWN | ~~K25a~~ | **DONE 2026-08-15** â€” it is **98 values on 80 of 249 records**, not 54 on 193, and **24 causes, not 98**: seven metre values hold all 54 eaves and six degree constants hold all 38 pitches, because the generator authors the archetype's constant and the note cites the family's band. **Roof pitch had never been measured by anything.** The sub-1-ft question is decided â€” they are failures, and nearness is the diagnosis. Read its box before quoting any band number |
| â€” | TOWN | ~~K33~~ | **DONE 2026-08-15** â€” it is **623 values on 227 of 249 records**, not 581, and the extra 42 are the finding: `roof_pitch_deg` cites a band on five families whose roof line is **"gable or shed"**, a form with no slope, and K25(a) could not see them because **a value with no band is never tested against one**. Route 2 (split the note), and route 3 is measured as unavailable â€” the confidence floats are in the mesh hash and prose is not. The assertion is **absolute, not a ratchet**. Read its box before quoting any citation number |
| â€” | GROUND | ~~T-E2~~ | **DONE 2026-08-15** â€” 26.5 % of the modelled land above the water surface is the reservation or the bar, and every gate this project had would have built on it. Nothing moved: **zero** anonymous roofs were there. Read its box before quoting any buildable-ground figure |
| â€” | GROUND | ~~T-E4~~ | **REFUTED 2026-08-24 (T-0026)** â€” there is no southern buildable ground to widen onto. The modelled box ends at local **N -400 m**, INSIDE Washington Street's own platted corridor; of the 0.0819 ha of land south of that corridor, **0.0000 ha** is in the South Division. Madison â€” the plat's south boundary â€” is **125.2 m** further south, and the plat's last tier (6 blocks, 48 lots, 6.28 ha) has **0 of 24** boundary points on modelled ground. The South's 120 roofs were gated on street control; the blocker is **terrain**, and street control stops where the ground does. Read its box before quoting any southern-ground figure |

**Every row is tagged. `SEEN` means a screenshot from the same spot looks different when it
merges. `UNSEEN` means it does not â€” those are real work and this project needs them, but they are
rationed.**

| # | lane | parcel | seen? | why |
|---|---|---|---|---|
| â€” | RENDERING | ~~K49(f)~~ | **SEEN** | **DONE 2026-08-16 â€” 2 species absent â†’ 0, and the block's own phase pays for itself twice.** The even deal dealt the SAME 64 values of `u` in every block of the world, so a band narrower than 1/64 fell between two of them EVERYWHERE: **45 matrix bands, exactly 2 under one step, and exactly those 2 were the species drawn nowhere.** Matrix deviation **282.90 â†’ 219.19**. Its finding is not the repair: **K49(e)'s leading explanation is refuted for the bigger of the two rows it was written about** â€” the settled town recovers 23.66 of its 24.87 regression on a change that touches no filter. Read its box before quoting K49(d) on a regressed row |
| â€” | RENDERING | ~~R-A1~~ | **SEEN** | **DONE 2026-08-16 â€” the Road visibility slider, off by default, and the first parcel taken by PULLING A SEEN ROW UP when every numbered one was blocked.** Its finding is about gates, not roads: **an inertness assertion needs a liveness assertion beside it**, because "the default is unchanged" passes identically whether a control is wired correctly or wired to nothing â€” R-BUG1's dead `--no-sun-shadow` one parcel earlier. And the instrument was measured before its threshold was set: the 12Â² frame signature scores the aid at **worst 2 against a residual of 0**, the same difference at 48Â² is **worst 6**, and nothing about the scene changed between the two runs. Read its box before adding any preference to Settings |
| â€” | RENDERING | ~~K24~~ | **SEEN** | **DONE 2026-08-17 â€” the Brightness slider, off by default, and the SECOND parcel taken by pulling a SEEN row up when every numbered one was blocked.** Owner-requested on 2026-08-14 and deferred behind PR #125 by a sequencing note that turned out to be a claim about a diff nobody had checked: the aid is one constant and one method, not a `world.js` rewrite. **Its finding is about R-A1's gate rather than about light** â€” `Object.assign` copies what a getter returns, so `get roadAid()` had been a frozen `0` since it shipped, and both of R-A1's readback assertions expect `0`. The control was live; its report of itself was not. Read its box before adding any reading to `window.__chicago4d` |
| â€” | RENDERING | ~~K51~~ | **SEEN** | **DONE 2026-08-17 â€” 139 researched animals reached no browser at all, and the whole layer is now a card in the Evidence panel.** Fauna figures reaching a visitor **0 of 30 â†’ 30 of 30**; the dataset's unread population **58 of 100 â†’ 28**. Its findings are about instruments, not animals: K42's assertion 3a **fired exactly as designed** the moment the directory was opened, and **two of that gate's own controls had been written against the repository's state** â€” one became a copy of the measurement and the other printed SILENT rather than failing. And `docs/LIBERTIES.md` **L2 said "ambient wildlife is rendered sparsely" for eight days while nothing was rendered at all**. Read its box before quoting any layer-read number |
| â€” | RENDERING | ~~R-BUG6(a)~~ | **SEEN in motion** | **DONE 2026-08-17 â€” the shadow box was re-centred on the visitor's exact position, so its texel lattice slid under every step and re-quantised every shadow edge in the town.** It moves in whole texels now: with the camera held still and the box slid half a texel, `from_above` **2,023 changed pixels â†’ 0** and `descend_main_stem` **5,650 â†’ 0**. Three findings, and two of them are about instruments: **the control that "cleared the shadow map" was inert** (a compile-time flag is not a runtime handle â€” it moves 5,439 px now), and **a sub-pixel nudge cannot measure a shadow box at all** â€” scaled up to a half texel it changes 29,138 px with the fix and 28,784 without, sign included. The answer to the parcel's title: **the shadow map is 14â€“16 % of the town's flicker**, not the cause of it. Read its box before quoting any flicker number |
| â€” | RENDERING | ~~R-BUG6(b)~~ | â€” | **DONE 2026-08-17 â€” the premise was wrong and two tests say so. The residual is NOT co-planar ties: switching the depth test from `LessEqual` to `Less` moves 36,187 px of the frame and only 13 of the 1,108 flickering ones (1.2 %), and 5Ã— the depth precision leaves 604 of 607 surviving.** It is the town's own edges being resampled, which is antialiasing and not a defect â€” R-BUG1's near plane had already taken the real one. Three findings: **an exact tie is STABLE and a near tie is what flickers** (which is why 3.5 % of this frame is co-planar and none of it shimmers); the ownership instrument (`tools/measure_tie_class.mjs`, 0 unattributed, buildings + trees own 94.5 % of the flicker on 7.7 % of the frame); and **`measure_river_edge.mjs`'s bank mask counts the SKY as water** â€” rows 0â€“200 are 1,280 of 1,280 "waterish", so no bank-line pixel count from it is a statement about the river. Read its box before quoting any flicker or bank number |
| â€” | TOWN | ~~K52~~ | **SEEN** | **DONE 2026-08-17 â€” the layer that already had a reader was hiding seventeen households, and the reader is the reason nobody looked.** A household reaches a visitor only through a building it `lives_at` or `works_at`, so the 17 whose residence AND workplace are both unattested on 1 July 1835 attached to no building and appeared **on no card anywhere** â€” 20 person entries, one of them the **Mark Beaubien** household, dropped for exactly the thin evidence that makes its record interesting. And the join carried a third of each record it did reach: arrival, origin, reason for coming, presence, a person's age, sex, name basis and sources, and all ten `researched_not_resident` findings reached nothing. **K42's assertion 3a did not fire** â€” the census tool names `flora` and `fauna` only, which is K52(b). The third parcel taken by pulling a SEEN row up when every numbered one was bake-blocked. Read its box before assuming a layer with a reader is a layer that is read |
| **1** | RENDERING | **R-BUG6(c)** | UNSEEN | **NEEDS ONE BAKE.** The 36,187 co-planar pixels above are steady but arbitrary: two surfaces of different colours at one depth, with draw order picking the winner. A question about the models, opened by (b) |
| â€” | RENDERING | ~~K53~~ | **SEEN** | **DONE 2026-08-17 â€” twenty-one shrub records were drawn with the forb archetype, and the clamp that made that survivable was hiding the recorded width.** Shrubs 0 â†’ **14** drawn over 32 poses, clump width **0.40 m clamped â†’ 1.80 m median**, and the census is identical plant for plant (2,201 forb-layer plants before, 2,187 + 14 after, every zone conserved). Its finding is the reason the number is 14 and not 140 â€” **the forb lottery deals by HEAD COUNT, so a hazel covering 7 mÂ² competes as one plant against 40 wild leeks per mÂ²**, and the wet woods' attested dominant shrub gets 0.2 % of the slots. Opened as **K54**. Read its box before quoting a shrub count |
| â€” | RENDERING | ~~K54~~ | **SEEN** | **DONE 2026-08-17 â€” the two strata were sharing one lattice, and where the herb layer saturates it the deal is a subsample by head count. 4 bushes standing over the eight stations â†’ 181.** The shrubs are dealt from their own pass at their own recorded clump density: `z06_dense_forest` **2 â†’ 156** drawn and **40.1 %** of its recorded 94.9 % cover, the riverbank dogwood belt **20.1 % against a recorded 19.5 %**, matrix deviation unmoved to the second decimal and **0 of 98** pairs drawn nowhere. Two findings: **the slot count still mixed units** and planted the riverbank understory **8.8Ã—** too thickly (K55), and **the instrument this parcel named cannot answer its question** â€” "deviation from the recorded cover" has measured the lattice against its own target since K49(c2). Read its box before quoting 89.11 or any deviation sum across two builds |
| â€” | RENDERING | ~~K56~~ | **SEEN** | **DONE 2026-08-17 â€” 16 sprays â†’ 32, shell fill 17.7 % â†’ 30.9 %, and the lowest band arches down over the stems.** The size did NOT move: a spray is a leaf MASS, not a leaf, so shrinking it would have bought a smaller plate with more sky round it. Follow-up **K57** |
| â€” | RENDERING | ~~K57~~ | **SEEN** | **DONE 2026-08-17 â€” the question cannot be asked at a fixed plate area, because the plates are what carries the RECORDED clump width.** 64 sprays at the shipped total area buy 8.5 points of cover and pay **reach 0.990 â†’ 0.890** of the recorded half-width for them, plate 37 â†’ 26 cm. So the grain trades against TRIANGLES: at the shipped plate size, 32 â†’ 48 â†’ 64 sprays cover **36.9 % â†’ 46.9 % â†’ 51.3 %** of the outline for 72 â†’ 104 â†’ 136 triangles, and **48 is where the return halves**. Stem cover 40.9 % â†’ 51.3 %, 38.8 % of the frame changed. Two findings: **K56's 17.7 %/30.9 % were taken by a script nobody committed** â€” the instrument is `tools/measure_spray_grain.mjs` now, reproducing K56's plate area to the digit off `renderers/web/js/shrub-grain.js`, which imports nothing; and the wet woods' ring is **167 shrubs, not the 156 K54 and K56 quote**. Opened **K59**, which is now DONE and spent the 4.4 points: read K59's box before timing anything in a browser here. Read this one before shrinking any archetype plate |
| â€” | RENDERING | ~~K55~~ | **SEEN, and only just** | **DONE 2026-08-17 â€” the same fault runs BOTH WAYS, and for the herbs it ran the other one.** A cover fraction read as a count over-planted the 2.25 m dogwood by 8.8Ã— and UNDER-planted the riverbank's 10 cm ground layer by **96Ã—**: `z05` 0.025 â†’ 2.407 plants/mÂ², `z03` 0.123 â†’ 1.254, forb slots **781 â†’ 923** over the eight stations, `z03`'s own layer **31 â†’ 84**, matrix and shrub unchanged to the second decimal. Three findings: the sign of the fault is decided by whether one plant covers more or less than a square metre, so the queue inherited "over-planting" from the case measured first; **three of the parcel's six named rows were never faults** â€” the `basis` column was printing `subsetOn`'s default argument and the matrix slot count comes off `cover.matrix_fraction`; and the count moved a fifth while the frame moved **0.15 %**, with `z10_settled_town` â€” the parcel's predicted visible half â€” not moving at all, because its share was clamped before and after. Opened **K58**. Read its box before quoting a forb count or calling a mixed list a defect |
| â€” | RENDERING | ~~K58~~ | **SEEN** | **DONE 2026-08-28 as T-0019 â€” it is NINE forb layers of ten, not six, and the shortfall is now declared rather than derived.** `tools/forb_clamp_baseline.json` names every (community, side) the 0.346 plants/mÂ² lattice ceiling binds, and `measure_sward_draw.mjs --gate` fails when the set drifts. K58's six were counted at the recorded MIDPOINTS; T-0034 deals the forb stratum off the upper bound, so `z06_dense_forest` asks **66.381 /mÂ² and draws 0.5 %**, the marsh 22.000 and 1.6 %, and the two prairies and the lakeshore joined the clamp. The marsh's WET side is measured for the first time. No ceiling was raised: every route out buys plants with geometry in the two layers already carrying the most, and the detail ceilings are breached on dev. Read its box before quoting a forb density or the count of clamped layers **AMENDED 2026-08-28 by T-0282 â€” it is TEN, and the tenth is a stratum the declaration could not see.** `flora.js` deals four (stratum, side) lotteries through the same `shareOf` against the same ceiling; T-0019 declared the forb ones. `z06_dense_forest`'s SHRUB layer asks 0.403 clumps/mÂ² against 0.346 and has been over it since K54 named it, and `shrubShareWet`/`shrubDensityWet` were not exported at all. The declared identity is now (community, stratum, side), and `docs/LIBERTIES.md` **L201** is the visitor's copy of the table. |
| â€” | TOWN | ~~K30(c)~~ | **SEEN** | **REFUTED 2026-08-22 (T-0009, K30(d)) â€” DO NOT RUN THIS REPAIR.** The 29 buildings are still drawn standing in the roadway, but not for this reason: `--anchors` finds the record's point at the BACK corner on **all 17** of the deep records and on the kerb face on **none** of them, so the street-facing FACE is what was placed on the frontage and reflection would take twelve documented buildings a full depth behind their own frontage. The cause is the committed `south_water` centreline, deliberately shifted 4.3â€“8.8 m south of the control the placements were offset from. **What to do about it is the owner's, and T-0009 is blocked on him** |
| **2** | RENDERING | **R-W2b** | **SEEN** | wire R-W2a's committed material sheet into the params and records â€” 1,353 materials measured out of the shipped GLBs and currently reaching nothing. **This is what repaints the town**, and R-W2 owns the worst-scored axis on R-G1's whole table (texture, **1.4**) |
| â€” | RENDERING | ~~R-W2c~~ | **SEEN** | **DONE 2026-08-22 (T-0008) â€” the stack is not the roof.** 157 stacks on 143 buildings now carry a masonry material of their own: **brick on 112 framed buildings**, off `frame_tavern`'s committed Petford value moved into the sheet, and a **cat-and-clay daub on 31 log cabins** at the midpoint of the two committed values that bound it. `docs/RESEARCH/chimneys.md` is the fabric argument; L168 records the invention. **Three findings.** It was NOT a one-file fix and it was not palette-only: the two dispositions the archetypes had already argued in prose are two materials, and the fabric had to be researched before either could be chosen. **It cost NO draw call** â€” `buildings.js::materialKey` batches on maps and flags, never on colour or roughness, both of which ride per vertex, so 113 calls before and 113 after at `south_water`. And R-W2a's *219 stacks on 199 buildings* does not reproduce: the resolved parameters of the committed masters give **157 on 143** across four archetypes. Left standing: the fort (**T-0137**) and the placeholders' second brick (**T-0138**) |
| â€” | TOWN | ~~T-V2~~ | **DONE 2026-08-16** â€” the anchor named South Water Street stood 101 m from it, in a field. Now in the street at Wells, both coordinates read from committed data. **It sat on `hold` two days on a number other parcels had already fixed**: the far band it was parked for reads **2.1 L\* / 71 %** today, not 0.5 / 30 %. Its real finding is R-M1c's, from a second direction â€” the field stand scored **100 % on six probes of 510** and the street stand shows **93 perceptible stretches against 31** and scores lower. T-V2b folded into R-M1c; baseline re-shoot is T-V2c |
| **5** | GROUND | **T-E3** | **SEEN** | the heightfield east (= `S2e`). Ground a visitor can walk onto that is not there today |
| 6 | TOWN | **T-V1(b)** | SEEN | the sixty North records â€” but **NEEDS ONE BAKE** and cannot go green on the improve runner. Claim only with the bake available |
| **1** | RENDERING | **R-W2** | **SEEN** | **PROMOTED 2026-08-16 â€” R-W1 landed on `dev` and cannot leave it until this parcel runs.** Textured coverage is the only thing that buys back the contrast the honest sky costs: R-W1 takes `south_water` 250â€“600 m from **71 % to 16 %**, and the near band's opaque *ceiling* is 3.4â€“4.3 L\* whatever the light does. Every road band in the suite is now under or near its bar, and no amount of relighting fixes a surface with no texture on it. Read R-W2a's material sheet first â€” its findings 1 and 2 (the chimney is not a material; no record states a roof covering) bound what can be textured today |
| â€” | RENDERING | ~~R-W3b(a)~~ | **SEEN** | **DONE 2026-08-17 â€” the sun threw a shadow within 60 m of the visitor and nowhere else: 5 to 8 of 331 structures and 0 to 41 of 730 stems, measured at all eight anchors.** It is Â±120 m now, at the SAME texel size (the map doubles with the box), and `green_tree` goes 8 â†’ 27 structures, `south_water` 8 â†’ 26 and 12 â†’ 54 stems. **Its finding is the ceiling: the reach is DRAW-CALL-bound, not fill-bound** â€” every batch entering the box is another call in the shadow pass, and the worst anchor reads 70 calls at 60 m, 74 at 120, 78 at 150 and **exactly 80 at 180, which is the budget**, with the town still two thirds outside the box. Read its box before raising the number |
| â€” | RENDERING | ~~R-W5a2 + R-W3b(a2)~~ | **SEEN** | **DONE 2026-08-17 â€” 16 batches â†’ 1, and the reach went straight from Â±120 m to Â±240 m on the calls it freed.** Roughness is the last thing that was splitting the town, and it is per-vertex now; the worst anchor reads **50 draw calls of 80 where it read 74 this morning**, at the SAME 11.7 cm texel. `green_tree` 27 â†’ **49** of 331 structures and 0 â†’ **70** of 730 stems; `south_water` 26 â†’ **91** and 54 â†’ **239**. **Its finding is that the batch merge is not neutral after all** â€” 942 pixels of 7,168,000 move across seven poses, all of them depth ties between co-planar surfaces of different materials, which is R-BUG6's own class one draw call in. Read its box before quoting a draw-call figure taken before this date |
| â€” | RENDERING | ~~R-W4c(b2)~~ | â€” | **DONE 2026-08-27 as T-0034** â€” the bar is the lattice, the records already ask for 18 % more bloom than it can draw, and the prairies are on the ceiling now |
| â€” | TOWN | ~~T-I3(b)~~ | â€” | **DONE 2026-08-27 as ticket T-0032** â€” closed at **662** on the owner's delegated pick; the institutional matrix row is now the census, and the target is gated against a civic ledger re-derived on every run |
| â€” | GROUND | ~~T-E5(b)~~ | **SEEN** | **DONE 2026-08-24 as T-0027 â€” and it refuted its own question. There is no wet fraction to read: 43,885 samples at 0.5 m over the platted block, 0 of them at or below the water surface, and the block's whole relief is 1.49 in â€” INSIDE the spec's own micro-relief noise, so the terrain models no basin here and a fraction read off it would be a read of the seed. The answer is a DEPTH: the dossier's own bed for zone 15 is +1.0 to +2.0 ft and the committed ground stands 0.84 to 1.96 ft above it, so the pond has to be DUG, not chosen. What was wrong was the SWARD â€” `docs/research/02-flora.md` heads ZONE 3 with the Public Square by name and `z03`'s elevation-band extent could never reach a block drawn at the plain's height. Read its box before proposing an extent for zone 15 |
| â€” | RENDERING | ~~K45(b) change one~~ | **SEEN** | **DONE 2026-08-17 as K45(b4) â€” 88 poplars stand on 4.30 ha of lakeshore sand that had never been offered a stem, and the placement rule is the SWARD'S.** The dune is a substrate and the heightfield does not carry substrate, so `communityAt` asks `flora.js` which zone a point is in rather than carrying a second copy of the beach. Two findings: the 40.2 ha refused east of the limits is **4.30 ha of plantable lakeshore and 33.6 ha of sand prairie whose own record carries no tree at all**, so most of it was never a woody omission; and **`SPECIES` is keyed by species id, which breaks the first time a species is recorded twice** â€” `populus_deltoides` is a 22â€“30 m gallery emergent AND a 5â€“15 m dune leaner, and the beach was one line from being planted with the wrong one. Read its box before adding a species to a second zone |
| â€” | RENDERING | ~~K45(b3)~~ | **SEEN on `light`** | **DONE 2026-08-17 â€” the control was inert for the wood and was quietly halving the one thing that must not thin.** Measured before the repair: the three levels planted **472 / 470 / 437 trees** â€” one wood planted three times, exactly as K45(b2) predicted â€” while the point-bar willow screen went **258 / 190 / 133 stools**, because the thicket roll is a fixed per-cell chance and a coarser grid visits fewer bar cells. **So the only thing scene detail did was break the screen its own comment says must not be broken.** `keep` is now a fraction on the tree acceptance roll (1 / 0.80 / 0.60, the levels' own triangle ceilings read as a ratio â€” L121) and the thicket roll scales with its cell instead: **`light` 437 â†’ 257 trees and 133 â†’ 182 stools**, scene triangles **416,222 â†’ 370,738**, `full` unchanged to the stem, and the wood reaches N +391.8 m at `light` against `full`'s +397.7. Read its box before quoting a stem count at any level but `full` |
| â€” | RENDERING | ~~K45(b2)~~ | **SEEN** | **DONE 2026-08-16** â€” the planter sweeps the field (reach 27.05 % â†’ 98.37 %), the timber gets the east end Andreas gives it, and `z05`'s own note had Wells Street 440 m from where the committed centreline puts it. Read its box before quoting a reach number or moving a woody east limit |
| â€” | RENDERING | ~~K48~~ | **SEEN** | **DONE 2026-08-16 â€” and it refuted its own premise. 0 sycamores became 2.** Both repairs it named are impossible: rescaling to the bands is an unsolvable system in two of four communities (`wet_woods` floors sum to 100/ha under a stand ceiling of 84), and deriving `perHa` from the mix sum contradicts the same dossier's own canopy sentence. The share is not the defect; the **draw** was. Read its box before proposing a change to any weight, density or band |
| â€” | RENDERING | ~~K49(d)~~ | **SEEN** | **DONE 2026-08-16 â€” the block permutation works and `prairie_west` does not stripe: matrix deviation 368.80 â†’ 282.89, and the 31.47-slot row is now 3.67.** Its finding is not the repair: **the stratum size is a U-curve**, and K49(b) finding 3's rule is only its left half â€” a block also has a CEILING, because exactness over the block is read through a sub-window. Measured at five sizes, and the smallest is 7.4Ã— WORSE than doing nothing. Read its box before setting a stratum size anywhere |
| â€” | RENDERING | ~~R-BUG1~~ | **SEEN** | **DONE 2026-08-16 â€” the owner's flickering river edge was the NEAR PLANE, and 15.6 % of the drawn bank line is now 3.3 %.** A fixed 0.1 m near against a 3,000 m far leaves two surfaces 350 m away needing 10 cm of separation before the depth buffer can order them, and the waterline is co-planar BY DESIGN. The instrument is the finding: **move the camera 2 mm and photograph the same view twice** â€” the control is 0 px, so anything that changes is a tie. **Most of what flickers is not the bank (R-BUG6), and its suspect is UNTESTED because the flag written to test it changes nothing.** Read its box before biasing any surface to settle a tie |
| â€” | RENDERING | ~~K49(e)~~ | UNSEEN | **DONE 2026-08-23 (T-0018) â€” REFUTED, and in the opposite direction.** The filters do not eat the stratification: over 7,844 dealt slots the survivors sit at **0.65** of what a rank-BLIND filter of the same size departs by, and the riverbank row the parcel was left on refuses **0.0 %** of its slots. The instrument was shown red before it was believed â€” a width-selective control on the same vectors reads 3.9â€“5.0. Read its box before blaming a filter for a census row |
| â€” | RENDERING | ~~K49(b)~~ | **SEEN** | **DONE 2026-08-16 â€” all six species are standing, 6 absent â†’ 0 over 6,795 slots.** And the screenshot the parcel asked for vetoed half its own repair: on the dense matrix layers the same construction rows the prairie. Read its box before proposing a low-discrepancy draw anywhere else â€” the answer is layer-dependent, and the census would have merged the striped version |
| â€” | RENDERING | ~~K49(c1)~~ | â€” | **DONE 2026-08-16 â€” the 25 footprints are in, `unconvertible` 25 â†’ 0, and the conversion is measured and NOT shipped.** It moves the shares by up to 3Ã— (June grass 8.1 % â†’ 24.0 %, wood nettle 1.1 % â†’ 6.3 %) and improves both deviations (matrix 219.19 â†’ 197.46, forb 107.18 â†’ 89.11), and it puts *Scirpus atrovirens* at **1.10 slots owed, 0 drawn** â€” K49(f)'s absolute gate. Read its box before dealing a sward slot off any number |
| â€” | RENDERING | ~~K49(c2)~~ | **SEEN** | **DONE 2026-08-16 â€” the conversion is SHIPPED and the tail gate is green on the mirror: matrix deviation 219.19 â†’ 154.19, forb 107.18 â†’ 89.11, worst shortfall 15.21 â†’ 8.50.** Route 1 was built and is **refuted at frame scale** (the sweep alone leaves *S. cyperinus* drawn nowhere at 1.11 owed, because a frame does not hold whole blocks â€” K49(e)'s question); route 3, which K49(c1) said was "not a route to green", **is** what got there. Read its box before proposing a construction to fix a tail |
| â€” | RENDERING | ~~K49(a)~~ | â€” | **DONE 2026-08-16.** The drawn census of the sward, in every community, + the abundance-unit audit. **And the lesson that is not about flora: the gate's own station reports 0 species absent, because it stands in one community of ten.** Read its box before quoting a flora share or a per-frame figure the smoke prints |
| â€” | RENDERING | ~~K49~~ | **SEEN** | **opened 2026-08-16 by K48.** Every other weighted draw in this project is the same shape and none has been asked what its tail does â€” the 63 inferred households, the roof coverings, the massing-variety picker. K48's own finding is that a small weighted sample loses its rare end permanently when the seed is fixed. Pick one, census what it actually draws, and it is visible wherever the answer is a building |
| â€” | RENDERING | ~~K47~~ | â€” | **DONE 2026-08-16 â€” and it inverted: claimed SEEN, delivered UNSEEN.** The sycamore's archetype is built and `drawn_as_another_species` is empty; the tree is **0 of 163 stems**. Read its box before quoting v139 or K45(b1) on what stands by the river |
| â€” | RENDERING | ~~K46~~ | **SEEN** | **DONE 2026-08-16** â€” the written weight plants the stem, and route 3 was refuted by the DATASET: ZONE 6a and 6b are one record, so a zone-keyed density cannot hold the elm at 60 in the thicket and 12 in the pocket. 23 of 26 weights sit inside their own cited band, 3 below, **none above**. Read its box before quoting a mix weight or a species share |

**If you are about to claim an UNSEEN parcel, stop and read the rule.** It needs one of three
written exemptions: an owner-reported bug, the second half of a measure-then-fix split, or a gate
that is blocking a named SEEN parcel. "It would be good to have" is not one of them.

**And if the SEEN rows above are all blocked, that is the finding** â€” say so in the PR and pull a
SEEN parcel up from the sections below rather than defaulting to another gate.

**AND THAT IS WHAT HAPPENED â€” 2026-08-16, R-A1, the first run to take this paragraph rather than
the table.** Every numbered SEEN pick was blocked (K30(c), T-E3, R-W2c, T-V1(b) need a bake; T-V2
and R-W1 were parked on `hold` â€” **both landed 2026-08-16 when the whole `hold` queue was worked
down; see R-M1c for why three of the four holds were one instrument fault**; R-W2b is a 315-record
schema change with no source stating a roof
covering), and the only unblocked NEXT UP row was **K49(e)**, which is UNSEEN â€” and the visible-
progress cap forbade it: v148 is already the one invisible run in the last four, so a second would
have made it two in four. So a SEEN parcel was pulled up from the sections below and shipped. **It
took ~25 minutes of budget to establish that, which is what the box below exists to save** â€” but
the pull-up route is now proven, and `R-A1`'s own section is the model: a parcel deferred for a
reason, whose stated precondition another parcel has since met, is a SEEN pick hiding in the file.
Search for *"deferred"* and *"unblocked"* the way T-E5(a) searched for `not_modelled`.

**THE TABLE ABOVE IS NEARLY OUT OF PICKS THIS RUNNER CAN CLOSE â€” counted 2026-08-16 by K28, and
stated here because the next run will otherwise spend a third of its budget rediscovering it.**
Of the numbered picks left standing, **T-V1(b), K30(c), T-E3 and R-W2c all say NEEDS A BAKE** and
cannot go green on the improve runner; **T-V2 landed 2026-08-16 (its `hold` was withdrawn â€” the
number it was parked on had been fixed by other parcels), and R-W1 is still on `hold` PR #125**;
**R-M1b is blocked on the owner** (R-W4c(b2) closed 2026-08-27 as T-0034, and T-I3(b)
as ticket T-0032 on the owner's delegated pick); and **R-W5a2's own box says to take it
only when the lane has nothing sharper**. That leaves **R-W2b** â€” whose R-W2a finding 2 makes it a
schema change across 315 records with no source yet stating a roof covering, so it is larger than
"unblocked" reads â€” and **T-E5**, whose ground half also needs a bake though its research and
`docs/LIBERTIES.md` half does not. **The lane needs new parcels opened more than it needs the next
one picked**, and the bake-shaped backlog is the reason: four parcels are waiting on a nightly.

**AND THE COUNT IS BETTER THAN IT WAS â€” 2026-08-16, K45(b2).** The box above says the lane needs
new parcels more than it needs the next pick, and this run left **two runner-closable SEEN ones**
where it took one: **K45(b) change one** (the dune community, whose hard question K45(b2) removed
rather than answered) and **K45(b3)** (the detail control, which K45(b2) measured as doing nothing
at all). Both are rows 1a and 1b in the table above. Neither needs a bake.

**T-E5 WAS THE LAST OF THOSE TWO AND IT IS TAKEN â€” 2026-08-16, T-E5(a).** The count above was
right and the paragraph's own advice is now the binding one: **the lane needs new parcels opened
more than it needs the next one picked.** T-E5's bake-free half is spent, its successor T-E5(b)
needs a bake, and every other numbered pick still sits behind a bake, a `hold` PR or the owner. So
the next runner-closable unit here is most likely **a parcel this file does not yet contain**, and
the honest way to find one is the way T-E5(a) found its own: read a deferral, a `not_modelled`
entry or a "deferred to parcel (c)" phrase and ask **what question it was never asked**. That is
where four of the last six findings came from.

**AND IT PAID A THIRD TIME, ONE LINK FURTHER IN â€” 2026-08-16, K36(b).** The successor to the
paragraph below took its own advice literally: K36(a) had gated a transformation and named its
output a fault about NAMES, so K36(b) asked what else that transformation changes. The answer
was the town's draw-call budget, breached at half its scene anchors, on a flag whose
documentation says it does the opposite. **The generalisation: when a tool's own justification
for a step is a number, measure the number in YOUR system.** `--palette` merges materials
inside one file; this renderer batches across files; those are not the same currency and
nothing had ever converted between them. The lane is full of steps justified by a
tool's README â€” `--simplify`, `--compress`, `meshopt`'s bit depths, the AO bake's own nightly
(B-A1 asks exactly this question of it, and is still unclaimed).
**And it opened TWO runner-closable parcels, K37 and R-W6(b)**, which is the count the box
above says the lane needs more than it needs the next pick.
**K37 IS SPENT â€” 2026-08-16 â€” and it opened two more of the same shape.** Its own finding was
that the parcel's question ("are these 90 special?") had the wrong subject: the discriminator was
not the asset's kind but a number nobody had taken, and taking it convicted three assets the
parcel never suspected. The two it leaves open are both *writers of `assets/web/` that nothing
decided*: `generators/inferred_placeholder.py`, which seeds the tree from the master on every
run, and `tools/publish.sh`, which copies a master through on an **mtime** comparison. Three
scripts write that directory and only one of them is the step. **The generalisation, and it is
the K36(a) seam one turn further: when a directory has more than one writer, the gate on its
contents is a gate on the last writer only.**

**AND THAT SENTENCE WAS WORTH A PARCEL ON ITS OWN â€” 2026-08-16, K38.** It took K37's
declined paragraph verbatim and the answer was worse than the paragraph guessed: the count
is not three writers but **four passthrough branches across three scripts**, three of them
silent, and the fault is reachable in one command. Two masters `touch`ed and
`tools/publish.sh` run put **1,212,760 uncompressed bytes into the payload** and drew
**CHECK PASS** from the entire dev gate â€” because a master copied over its own derivative
satisfies assertions 1 through 7 *by construction*. **The generalisation one turn further:
a gate written against a transformation is not a gate on its output directory**, and the
difference is invisible for as long as only the transformation writes there. Two of this
project's directories now have more writers than gates, and `assets/gltf/` â€” written by
`generators/build.py`, by the nightly, and by whatever a parcel does with `--only` â€” has
never been asked the question at all. K38's own successor K39 is the narrower half: the
step knows which master it compressed and writes it down nowhere, so staleness is still a
timestamp.

**AND THE NARROW HALF WAS THE ONE THAT PAID â€” 2026-08-16, K39.** The record itself is
exactly what K38 predicted and took an afternoon. The finding came from trying to VERIFY
it: a seeded hash wants a reproduction control, this repository claims one in as many
words (*"it reproduces 331 of 334"*), and **the claim is false** â€” 6 of 20, with the other
14 reproducing byte-for-byte under a flag K36(b) turned off two parcels ago. **The
generalisation, and it is the K36(b) seam turned on ourselves: when a repair regenerates
SOME of a set, the remainder becomes the output of a step that no longer exists.** K36(b)
regenerated 38 of 241 and said so honestly; nothing asked what the other 203 were. This
project has done partial regenerations at least three times â€” K36(b)'s 38, K37's 3, and
R-W6's terrain that never reached the file at all â€” and each one left a cohort behind.
K40 is this instance. The question is worth asking of `assets/gltf/` too, where the
nightly, a `--only` run and `generators/build.py` all write.

**THE SEAM IS STILL OPEN, AND IT PAID AGAIN â€” 2026-08-16, K36(a).** Same move as K34, one link
further out: instead of a rule about a record, take a rule about a FILE â€” *"a stale committed GLB
is a check failure, not a warning"*, *"the bytes a visitor downloads have to be the bytes
something tested"* â€” and ask which of the steps between the data and the browser anything
actually measures. Two of three, it turned out, and the ungated one had been shipping 75
textures out of a repository that contains none. **The generalisation worth carrying forward:
this project gates its ARTEFACTS at their ends and not at their transformations**, and every
transformation here is a script with a flag in it. `publish.sh`, `compile_scene.py` and the dev
preview assembler are the same shape of thing; two of them now have a gate and the question is
worth asking of anything that rewrites a file on its way out.

**THE ADVICE WORKS, AND THE RICHEST SEAM IS NOT THE DEFERRALS â€” 2026-08-16, K34.** It took the
paragraph above and widened it one step: instead of a deferral, read a **rule this project states
about itself** and ask what enforces it. AGENTS.md's standing constraint on the removal is the
most important sentence in this repository and nothing had ever measured what it covers; the
answer was "the buildings, and not the people", plus one record that claimed the flag in prose
and never carried it. **`docs/` and `AGENTS.md` are full of sentences of that shape** â€” a rule
stated, a mechanism named, and nothing that runs. K35 is the successor this one opened, and the
seam is not exhausted.

**R-W5a is DONE (2026-08-15) â€” the town was paying one draw call per COLOUR OF PAINT, and the
growth term is now zero.** All 47 building batches were the same `MeshStandardMaterial` in every
respect a renderer distinguishes â€” metalness 0, no map of any kind, `DoubleSide`, opaque, no alpha
test, smooth-shaded. The only fields that differed were `color` (39 distinct values) and
`roughness` (16). Base colour moved to a per-vertex attribute and left the key, so **47 batches
became 16** and **11 of 22 station-viewports over the â‰¤ 80 budget became 0**. Full table and the
identity proof under R-W5a below. Three things came out of it that are not the number:

- **R-G1's "+11 draw calls per 19 roofs" was 11 new MATERIAL GROUPS, not 11 objects** â€” which is
  why it was uniform at bearings 150Â° apart: it counts paints in frame, not buildings. That term
  is now **zero by construction**: a new roof of any colour joins an existing batch. T-A8 and the
  399 roofs behind it are unblocked, and no future block parcel needs to think about this.
- **Triangles are identical to the triangle at all 22 station-viewports**, which is the proof that
  nothing was dropped to buy the calls.
- **The frame is not byte-identical and the difference is quantified rather than waved at**:
  2 of 22 shots hash the same, the rest differ on ~0.013 % of pixels in scattered 7â€“56 px specks
  at building silhouettes â€” depth ties resolving the other way under a changed draw order â€” for a
  whole-frame mean |Î”| of **0.003â€“0.005 of one 8-bit count**. No surface is repainted; the albedo
  arithmetic is the same product in a different order.

**R-BUG3 is REOPENED (2026-08-15) â€” the owner reproduced it WITH the fix in.** What it fixed is
real and stays; what it claimed is not. See **R-BUG3c** and **R-BUG4** below, and read them before
quoting any road number. The original write-up follows, corrected:

**R-BUG3's near-field contrast half is done (2026-08-15)** â€” the owner-reported invisible-at-your-feet road was **the alpha,
and NOT the grass**: the near band scored **1.5 L\* / 30 %** and now scores **3.1 of a measured
ceiling of 3.4 with 80 % perceptible on mobile, 3.2 of 4.3 with 60 % on desktop**, and the alpha
half of the fix fades to nothing by 40 m, so every band past it is unchanged to the decimal. (Those
figures are re-measured on the merge of 2026-08-15; an earlier draft of this line quoted *2.8 of
3.7 / 60 %*, which was one iteration stale and matched neither viewport. The gate prints the bands
â€” quote it, do not paraphrase it.) Two things were found
that are not the fix and matter more. **The near band was empty at both gated stations, because
neither one stands on a road** â€” `south_water` is 101 m from its own centreline (T-V2) and
`from_above` is in the air â€” so the parcel's own first move, adding `[2, 40]`, measured nothing
until a station stood on the roadway. And **a band gated on probes SEEN gates itself out exactly
when the road goes invisible**; the bands are now gated on probes PROJECTED, so that failure is
loud. Full findings under R-BUG3 below â€” read them before pointing any gate at anything.

**R-BUG2 is DONE (2026-08-14)** â€” the owner-reported vanishing roads were **two** faults, not one,
and the parcel's prime suspect was **refuted by measurement**. The gate could not see any of it and
now can: `roadContrast()` scores the fault at **0.3 L\* / 14 %** on foot at range and **1.1 L\* /
0 %** from the air, against **4.0 / 92 %** and **2.9 / 91 %** with the fix. Full findings under
R-BUG2 below â€” read the refutation before reaching for a mip-filter fix anywhere else.

**K21 is DONE (2026-08-15)** â€” the four trades whose adoption test was silent are silent no longer:
every roof this layer raises now carries the family band its own prose has always named, **29 of 29
census trades resolve across 44 trade-family pairs**, and a gate fails if a household is ever housed
on a roof that names no family. No liberty was owed â€” the value was already committed twice over â€”
and rule 6 gains no clause. The parcel's own Watch note was **refuted**: the two sawyer roofs differ
because they were dealt different families. The real archetype split, and the finding underneath it
â€” **54 of 193 roofs sit outside the band their note cites** â€” are **K25**. Full findings under K21
below; read the refutation before massing anything off an archetype.

**T-A7 is DONE (2026-08-15)** â€” a lot was known to be free by the *absence of a centroid*, and a
building standing proud of its own frontage has its centroid in the road, so four documented
buildings â€” the Temple Building, Harmon & Loomis's store, the Chicago Democrat's office and the
Cook County courthouse â€” stood on lots the schedule was offering to anonymous roofs. Occupancy is
now measured by area, in ONE module both halves import. **266 stand and 399 remain, 61 of them on
covered ground** (was 66). Full findings under T-A7 below; read them before claiming a block.

**T-A6 is DONE (2026-08-15)** â€” the schedule was dealing five of the ten open blocks roofs their
own lots could not hold, and the deal now derives lot occupancy the same way the block generator
does. **266 stand and 399 remain, 66 of them on covered ground** (was 71 â€” five roofs never had
anywhere to stand; **re-derived to 61 by T-A7**). Full findings under T-A6 below.

**T-A5 is DONE (2026-08-14)** â€” `blk_randolph_market` carries eight roofs, so **266 stand and 399
remain**, 71 of them on covered ground (**re-derived to 66 by T-A6**). It is the first block whose standing roofs this project's
*own inferred-residents layer* had put there, and it **settles the division question T-A4 left
open**: rule 6 takes three tests, the third being the roof's division, and the written test recovers
all four adoption decisions made before it. It also found what the tests cannot answer â€” four trades
are housed only in family-less bespoke records, so test 2 is silent rather than negative for them
(**K21**). Full findings under T-A5 below.

**T-A4 is DONE (2026-08-14)** â€” `blk_randolph_clinton`, the first West Division block, carries
seven roofs and one adopted household, so **258 stand and 407 remain**, 79 of them on covered
ground. It is the first block parcel to arrive at ground that was already partly built, and the
gates that assumed an empty block are what it fixed. Full findings under T-A4 below.

**T-E1 is DONE (2026-08-14)** â€” the 1830 sheet is registered and read, and it is a **land-title
map, not a settlement map**: a name on a tract is who took title between 1828 and **1836**, not
who lived there and not that anything was built. A named tract may never license an anonymous
roof. Full findings under T-E1 below; read them before T-E2 or T-E4.

**T-A2h is DONE (2026-08-14)** â€” two of `blk_randolph_wells`'s ten roofs carry an argued
household and eight stay anonymous, under a **two-test rule now written into the household
programme's own `method` list**: a block roof may be adopted only where the trade's committed
argument calls its count a floor rather than a bound, AND the roof's family is one this layer
already houses that trade in. **The adoption is no longer a parcel of its own.** The generator
carries the gate in both directions, so T-A4 onward applies the rule in the same run as the
block â€” `T-A3h` was the one outstanding backfill because its block landed first, and it is **DONE (2026-08-15)**: every block this lane has placed has now been asked the question, and what the backfill found about the tests themselves is in its box and in K28.

**LANE 3 (ground) is a THIRD lane, opened 2026-08-14** â€” it touches terrain, sources and the
infill generator's eligibility rule. It is **disjoint from lane 1** (renderer) but **overlaps
lane 2** at `tools/generate_block_infill.py` and the inventory, so **a lane-2 block parcel and
a lane-3 parcel may not run at the same time.** Lane 1 may always run alongside either.

**Why it matters now:** only 86 of the 414 remaining roofs sit on covered ground. Lane 2
exhausts them in roughly a day and a half and then has nowhere to build. Lane 3 is what keeps
the town growing after that â€” and the owner's condition on opening it is that the geography be
real, not convenient.

**R-G0 is DONE (2026-08-14)** â€” the harness and the baseline are in, so every parcel below
opens with `node tools/critic_shots.mjs --metrics` and closes with the same command, and
quotes the two tables rather than an adjective.

**R-G1 is DONE (2026-08-14) â€” the baseline scores 4.18 of 10, every axis below 7.** Texture
**1.4** is the floor, historical accuracy **6.8** the ceiling, and the five-point gap between
them is the shape of this project. Full tables and per-axis justification in `docs/STATUS.md`
Â§ "The baseline scored". **Three findings came out of it that are not scores**, and each is
written into the parcel that owns it below:

- **Â§1 item 7's mechanism does not survive.** 94â€“100 % of the literal-black pixels lie in
  components entirely above the land/sky row â€” they are the shaded near canopy, not a shadow â€”
  and the darkest-decile figure reaches the same surface a second way, because the metric's
  per-column "ground" starts at the top of a crown. **R-W1** owns it; raising a shadow floor
  will not move either number.
- **The horizon-timber metric counts a gable as a tree.** `prairie_south` gained 20 % on that
  metric between two runs with no renderer change, from 19 new roofs. **R-W4** owns the target
  and needs a discriminator before its â‰¥ 90 % acceptance number means anything.
- **19 roofs cost +11 draw calls at seven of eleven stations**, taking the over-budget count
  from 4 to 6 desktop. Extrapolated over the 414 remaining roofs that is about +240 against a
  budget of 80. **R-W5** owns it and should treat batching as its first question.

**T-A3 is DONE (2026-08-14)** â€” `blk_randolph_dearborn` carries **nine of the ten roofs the
schedule dealt it**, so **251 stand and 414 remain**, 86 of them on covered ground. The tenth was
a civic roof and is deferred with its reasoning: the parcel shape repeated exactly as T-A2
predicted, and what it found was that one family cannot be massed at all. See T-I3.

**T-A2 is DONE (2026-08-14)** â€” `blk_randolph_wells` carries ten roofs, so **242 stand and 423
remain**, 95 of them on covered ground. The parcel authors no coordinates: block parcels are now
a recipe entry read against the committed lot polygons, which is what makes T-A3 onward cheap.

**T-A1 is DONE (2026-08-14)** â€” 232 roofs stood, 433 remained, and
`data/reconstruction/1835_665_roof_programme.json` schedules them per block. Only **105 of
the 433** have modelled ground to stand on, so lane 2 has about ten block parcels of work in
it and then it is blocked on S9 street control and the terrain extensions, not on recipes.

---

## LANE 1 â€” RENDERING Â· phases from `docs/RENDERING.md`

Acceptance numbers are copied from RENDERING Â§5 so a builder does not have to hold two
documents open. Where a phase has a bake-dependent half, it is marked â€” ship the half you
can and say so.

### T-0179 â€” three families offer a shed their ridge band cannot carry Â· **DONE 2026-08-27 â€” two held, one refuted, and a fourth nobody had measured**

**The reasoning archive for L182 and the STATUS box of the same date.** T-0148's sweep printed C1,
F1 and F4 as NOTE lines: families whose crosswalk roof line offers a SHED their own `ridge_ft` band
cannot carry, latent because no generator dealt them one. Asked of what the archetypes actually
build:

| family | ticket | measured | the reason |
|---|---|---|---|
| C1 | 231 of 441 | **231 of 441** | `frame_storefront._shed_roof` always falls back-to-front; the run is the 20-30 ft depth |
| F1 | 399 of 441 | **399 of 441** | `outbuilding` with no open side, so the fall is down 32-50 ft |
| F4 | 441 of 441 | **0 of 441** | F4's own entry is `1/open`, "open posts", "part-open sides" â€” the fall goes across the 24-36 ft width (L73) |
| W5 | â€” | **84 of 441** | never swept: the sweep reports a family with no pitch band before testing any FORM |

**Three findings worth keeping.** (1) The sweep constrained a claim it did not know it was
constraining â€” the AXIS a shed falls down â€” exactly as T-0145 had constrained the eave; the shape of
that error is now twice-observed and worth watching for a third time. (2) `ridge_model` turned the
shed's span with `gable_front`; all three archetypes that build a shed ignore the orientation
entirely, and no committed GLB is a shed on those archetypes, so the gate that exists to keep the
model honest had nothing to compare against. **A model checked only against what has been built is
unchecked wherever the build has not gone.** (3) The shed set was written five times and had drifted
over A5 â€” one roof stands on the difference â€” which is the same one-rule-two-files fault
`family_bands.py` was created to end, three files later.

**Owner question, unresolved and not blocking:** the `ridge_ft` column is authored for a gable's
half-span. Retiring the shed reading for C1, F1 and W5 in the crosswalk would be cleaner than
recording a refusal on every one of their records; recording it is what an agent may do, editing the
specification is not. See L182 "How to resolve".

**Still owed:** T-0212, the one A5 roof held on a gable pending a bake.

### R-BUG5b â€” the trees are still in the river Â· **DONE 2026-08-16 Â· the whole wood was drawn mirrored**

**THE WOOD WAS TESTED IN ENU AND DRAWN IN WORLD SPACE, AND THE TWO POINT OPPOSITE WAYS.** The
near-field planter in `renderers/web/js/trees.js` walks a 4 m grid and asks every question in local
ENU metres â€” `terrain.isWater(e, n)`, `communityAt(e, n)`, `terrain.surfaceHeight(e, n)`,
`cellAt(e, n)`, `blocked(e, n)`, `noteStation(e, n, y)`. Then it called
`addTree(buf, spec, px, gy, pz, rnd)`, and `addTree`'s fifth argument is a **three world z**.
`terrain.js`'s own `enuToWorld` is `(e, y, -n)`. The sign was never taken. **Every tree in the wood
was tested at `(px, pz)` and drawn at `(px, -pz)` â€” the entire near-field woodland mirrored across
the datum's eastâ€“west line through the forks.**

**The numbers, measured on `dev` as it stood (the build in the owner's screenshot):**

| | |
|---|---|
| stations recorded | **391** |
| stations wet at the point that was TESTED | **0** â€” which is why every gate was green |
| stations wet at the point that was DRAWN | **64** (16.4 %) |
| drawn vertices over the water mask | **12,285 of 77,688** (15.8 %) |
| â€¦more than 4 m from the nearest dry ground | **10,734** |
| worst distance from dry ground | **48 m** â€” at E 160.1, N 47.8, 0.61 m above the water |
| nearest station to a vertex, read as ENU `n = -z` | **âˆ** (no station anywhere near the geometry) |
| nearest station to a vertex, read as ENU `n = +z` | **13.1 m** â€” one crown radius. That is the proof |

**THE FINDING IS NOT THE SIGN. It is that three gates agreed with each other and all three were
measuring the same wrong thing.** `wetTreeStations`, `drownedTreeStations` and
`tools/measure_far_timber.py` all walk `stations` â€” the list the planter writes at the moment it
DECIDES to plant. That list is correct and always was; not one entry of it is in the water. **No
check anywhere read the merged geometry back and asked where a tree was DRAWN**, so a fault that
separates the decision from the drawing was invisible to all of them simultaneously. This is the
generalisation, and it is the sixth green-gate-versus-window disagreement on this project: **a gate
on a placement is not a gate on a picture. If a layer decides in one coordinate system and draws in
another, only a gate that reads the drawn buffers back can see the step between them.**
`renderers/web/js/flora.js` had it right the whole time â€” `_m.setPosition(e, y, -n2)` â€” which is
exactly why the sward has never been in the channel and the wood always was.

**R-BUG5 (#196) IS NOT RETRACTED, AND SAYING SO PRECISELY MATTERS.** `main_stem_belt_east` really
is authored between the two banks, really is 39 of 39 samples over water, and really should not be
drawn; that clip stands and its gate stands. What #196 got wrong is the ATTRIBUTION: it explained
the owner's photograph with the horizon band, shipped, and told the owner it was fixed. The band
was a second, genuine fault that happens to sit in the same direction from the same viewpoint. The
lesson it paid for is the one its own box asked for and did not get â€” **reproduce the frame before
choosing a cause.** This parcel's first commit was a screenshot, not a diagnosis.

**How the frame was reproduced, so the next person does not have to find it again.** The owner's
pose is `local_e -100, local_n -40, yaw_deg 76, altitude_m 1.22` â€” the south bank west of the
forks, 4 ft up, ENE 076Â°, which is what the HUD reads in his screenshot. The line of crowns is
at 130â€“190 m, over the main stem. `tools/shoot.mjs` puts the camera there in one command.

**The repair** is one named function, `worldZ(n) => -n`, applied at the two `addTree` call sites,
plus the comment block that says why it is named rather than inlined. Nothing about which trees
grow where, how many stand, or the evidence behind any of it moved: `perHa`, `edgeFade`,
`clearedFactor`, the waterline gate, the species draw and the seed are all untouched. **Every tree
simply moved to the side of the river it was already recorded as standing on** â€” so the North
Division's body of timber is now on the North Side, and the south bank of the main stem opens out,
which is what the sources describe and what the town's own `blocked()` footprints were being tested
against all along.

**The two new gates, in `tools/smoke_renderer.mjs`, and both were demonstrated RED on the unfixed
published mirror before the fix went in:**

- *every tree drawn stands at its own station* â€” every vertex of the merged timber within 24 m of
  some entry in `stations`. **This is the one that could never have passed through the bug**: under
  the mirror the nearest station is twice the vertex's own northing away. Structural, not a
  threshold.
- *no timber is drawn out in the channel* â€” no vertex over the water mask further than 12 m from
  dry ground, which is a bank willow's lean (see `TREE_DRY_MARGIN_M`'s box and `lean` in `SPECIES`)
  and no more. This is the owner's report in the owner's terms.

**Neither may ever be relaxed into a test of the placement. That is the test that was already
green.**

**LANDED WITH ONE GATE KNOWINGLY RED, AND THE `hold` IT WAS FIRST PARKED UNDER WAS WITHDRAWN ON
MEASUREMENT.** With the wood repaired, `the roads reach the screen from the air, at the aerial
anchor` fails â€” the FLYING station; **both on-foot road stations are green**, so nothing a walker
sees regressed. It is not a regression in the streets either: not one street vertex moved, and every
street gate â€” drape, wet vertices, the R-BUG4 panel invariant â€” is still green.

This parcel was first parked on `hold` asking the owner to accept that red. **The premise of the
question was measurable, and measuring it reversed the answer.** Both columns below were taken the
same evening on the same runner, mobile 390Ã—780, published mirror, with nothing but `trees.js`
between them â€” `dev` at 3ea4e00 and this branch rebased onto it. The earlier figures in this box
were taken against the pre-R-BUG1 base and are superseded by these:

| aerial anchor, gated bands | `dev` (wood mirrored) | wood repaired |
|---|---|---|
| 100â€“250 m â€” seen of 63 projected | 46 | **60** |
| 100â€“250 m â€” perceptible | 80 % â†’ **37 probes** | 85 % â†’ **51 probes** |
| 250â€“600 m â€” seen of 186 projected | 157 | **177** |
| 250â€“600 m â€” median Î”L\* | 2.7 of 6.1 opaque | 2.3 of 4.8 opaque |
| 250â€“600 m â€” perceptible | 62 % â†’ **~97 probes** | 54 % â†’ **~96 probes** |
| 250â€“600 m â€” weber / ground L\* | 0.1104 / 53.9 | 0.0951 / 52.8 |
| **gated probes a visitor can SEE** | **203** | **237** |
| **gated probes that are PERCEPTIBLE** | **~134** | **~147** |

**The repaired build shows about thirteen MORE perceptible stretches of road and scores lower.**
That is the metric, not the town: `perceptible` is a ratio over probes **seen**, and `seen` is
exactly the quantity an occluder shrinks. **A gate whose score improves when something hides the
thing it measures is dividing by the wrong number.**

**This is R-BUG3's own lesson surviving one level below where R-BUG3 fixed it.** `roadContrast()`
already moved the decision of WHETHER to gate a band from "enough probes were seen" to "enough were
PROJECTED", and the comment beside it says exactly why: *"a band nobody can see reports n=0 and
gates itself out, which is indistinguishable from a band with no road in it."* The band's SCORE
still divides by `seen`. Score the same band on `nProjected` â€” fixed at 186 whatever stands in the
way â€” and **`dev` reads 52 % and this branch reads 52 %.** `dev` is under the 0.55 bar too, and has
been; it reports 62 % only because twenty-nine of its probes stand behind trees that were never
supposed to be there. **The band did not regress today. It stopped being flattered.**

**`ROAD_MIN_PERCEPTIBLE` is NOT lowered** â€” AGENTS.md Â§ "never weaken an assertion to pass", and
cutting a bar to admit the probes an occluder was hiding is the exact shape of that mistake. Note
too that the honest denominator would not have let this branch through either, which is what makes
it a finding rather than a route: it fails both builds. The band's real fix is **R-W2**'s textured
coverage â€” its ceiling is 4.8 L\* opaque, so the contrast is there to be spent â€” and the denominator
is **R-M1c**, opened below by this parcel. **R-W1** (`hold` PR #125) and **R-M1b** (no threshold
source) remain the owner's.

**Why it merged rather than waiting.** Holding a correct, visible, owner-reported fix behind a gate
that was passing on an artefact of the very bug being fixed inverts what the gate is for. Merging to
dev is stage, not ship: it publishes the `/dev/` preview only, and production moves solely on owner
dispatch. Recorded here so no later run reads the red as fresh breakage â€” it is red on merit, red on
`dev` as much as here, and it belongs to R-W2 and R-M1c.

**What this leaves open, and it is a real question rather than a courtesy.** Every other layer that
decides in ENU and draws in world space should be asked the same question by the same method â€”
reading its buffers back rather than its intentions. `flora.js` is measured and clean.
`streets.js`, `buildings.js` and `ground.js` have not been asked, and the ROADMAP entry for it is
**K50** below.

<details>
<summary>The parcel as it was written when it was claimed (2026-08-16)</summary>

**The owner reshot the river at 3:14 PM CT, standing 4 ft up on the south bank looking ENE 076Â°, on
the build whose What's-New panel says â€” in the same screenshot â€” "The trees standing in the river
are gone Â· Fixed Â· Aug 16, 2026, 1:31 PM CT". A straight line of crowns still runs across the
channel, with scattered ones beside it. The two sights #196 said were "one thing seen twice" are
both still there.**

**#196 is not to be trusted as a starting point, and this is the point of the parcel.** It shipped
`trees.js` (+74), `tools/measure_far_timber.py` (+484), a committed baseline and a new smoke
assertion â€” and the thing a visitor sees did not change. **Three instruments agreed with each other
and disagreed with the window.** That is now the FIFTH time on this project that a green gate and
the owner's screen have disagreed, after R-BUG2, R-BUG3, R-BUG3c and R-BUG4.

**The first job is NOT the trees. It is to reproduce the owner's frame and see them in it.** Until a
harness stands at that pose and photographs the trees over the water, nothing measured about timber
means anything, and any further fix is aimed at a target nobody has sighted.

**Do this in order and do not skip to the third:**

1. **Stand where the owner stood** â€” south bank of the main stem, 4 ft eye height, bearing 076Â°.
   Screenshot it. **If the trees are not in your frame, your pose is wrong, not his screenshot.**
2. **Make the gate FAIL on the current build.** #196's assertion passes today with the defect on
   screen, so it is measuring something else â€” find out what, and say so, before changing it. A
   check that passed through this bug is evidence about the check.
3. **Only then** work out why the crowns are over water, and fix it.

**One reading of #196 worth testing first, because it is cheap.** #196 changed `trees.js` and the
tools â€” **it changed no data.** Its own account says the South Water timber belt is *written*
between the two banks, every point over the channel, the worst 3.33 m under the surface. If the
committed line still runs across the river and the fix only taught the renderer to cull crowns over
water, then the cull is either not reaching this band, not reaching this viewpoint, or being applied
in a space where the water test does not answer â€” the ENU-vs-world swap and the single `y = 0`
water quad are both still live candidates from R-BUG5. **Fixing the record so the belt runs beside
the street it is named after may be the honest repair, not culling the symptom.**

**Acceptance, and it is stricter than #196's because #196 met its own and shipped a defect:**
a screenshot from the owner's pose with no crown over water, posted in the PR **beside the "before"
from the same pose**; the gate demonstrated FAILING on `dev` as it stands today and passing after;
and the What's-New entry does not say "fixed" unless that pair of screenshots is in the PR.

</details>

### K51 â€” the fauna layer reaches a visitor Â· **DONE 2026-08-17 â€” 139 animal records were read by nothing, and the gate that was supposed to notice had been told to expect it**

**Read this box before quoting any layer-read number taken before today.** The census line printed
by `tools/measure_layer_reads.py --gate` ended in the words *"which no renderer opens"* until this
parcel, and by then that clause was a claim rather than a measurement: it was true when K42 wrote
it and the gate had no way to keep it true. It is gone, and the line now separates a figure that
moves a vertex from one a visitor reads on a card, because rolling the two together is how a layer
with no geometry starts sounding drawn.

**What shipped.** The Evidence panel's *What was living here* section: ten habitats in the
manifest's own order, and inside each one every species researched into it â€” **139 records**, each
with its July status, its presence mode, its abundance, what it would be doing, what it would look
like, its voice, the sign it leaves, and the sources behind the three graded claims. The citations
are the joined records `citations.js` renders everywhere else, not bare ids.

**Numbers, measured rather than promised.** Fauna figures reaching a visitor: **0 of 30 â†’ 30 of
30**. Whole-dataset: **58 of 100 figures reached nothing â†’ 28**, and `data/fauna`'s share of that
is **30 â†’ 0**. Habitats on the card **10 of 10**, species **139 of 139**, citations rendered **54**,
zero page errors at 390Ã—780.

**FINDING 1 â€” the gate did exactly what it was built for, and that is the part worth carrying.**
K42 wrote assertion 3a to fail *the moment* a layer with no declared reads gains a reader â€”
*"because the whole of this layer's unread bank rests on nobody opening it"* â€” and it fired on the
first commit that opened the directory. Thirty figures had to be classified in the same commit
instead of riding on a sentence that had quietly expired. **A gate written against an absence has
to name the event that ends the absence**, or the absence becomes permanent by default.

**FINDING 2 â€” two of that gate's own controls were written against the repository's state, and
both went silent when the state moved.** Its self-test asserted `not layer_is_opened(src, "fauna")`
and constructed its 3a case by setting `opened["fauna"] = True`. Opening the layer turned the first
into a second copy of the measurement and the second into a case that could not be built at all â€”
it printed **SILENT** rather than failing, which is the quieter of the two ways a control dies.
Both are synthetic now: a scanner that cannot say *no* about a directory nothing names is broken
whatever this repository happens to contain today. **This is the sixth time on this project that a
green reading came from an instrument pointed at nothing**, and the first where the instrument was
a self-test rather than a flag.

**FINDING 3 â€” `docs/LIBERTIES.md` L2 has said "ambient wildlife is rendered sparsely" since
2026-08-09, and nothing was rendered at all.** Not sparsely: none. The entry's own revision of
2026-08-11 added a paragraph of measured detail about a dataset no renderer had opened, which is
how a liberty about the scene becomes a liberty about a file. L2 now states what the renderer does
â€” nothing is drawn, heard or traced â€” and keeps the decision as the standing intent for whenever
animals *are* drawn.

**What it does NOT do.** No animal is in the 3-D scene, no animal geometry is proposed, and the
standing constraint on depicting people is untouched. Every one of the thirty read declarations is
`shown` and none is `mesh`, deliberately: a state that said otherwise would be the read map making
a claim about the town. K42's route 1 â€” *"leave it and say so"*, which needs `data/scenes/1835.json`
and L2 to stop implying a reader â€” is **half discharged**: L2 is corrected here, and the `layers`
list is now honest for a different reason, because the layer does reach the browser.

**Files:** `renderers/web/js/fauna.js` (new) Â· `renderers/web/index.html` Â·
`renderers/web/js/main.js` Â· `renderers/web/css/walk.css` Â· `tools/publish.sh` Â·
`tools/check_published.mjs` (the copy rule) Â· `tools/compile_scene.py` (the citation join only) Â·
`tools/measure_layer_reads.py` + `tools/layer_reads_baseline.json` Â· `tools/smoke_renderer.mjs` Â·
`docs/LIBERTIES.md` L2.

**Not claimed:** the desktop half of the smoke â€” ~13 min against this runner's 10-minute
per-command ceiling; see the run-budget box at the top of this file. The section was photographed
at 1280Ã—800 by hand and reads correctly there.

**What it opens.** K42's third route, *give it a reader in the scene*, is untouched and is a much
larger parcel behind a bake. The narrower successor is **K52**: the same question asked of
`data/residents/` â€” that layer IS published and IS read by the building card, and nothing has ever
censused which of its figures reach a visitor. The read map covers flora and fauna and the two
generators declare their own `CONSUMED`; the population layer is declared by nothing, which is the
state `data/fauna` was in this morning.

### K52 â€” nobody has censused what the residents' figures reach Â· **DONE 2026-08-17 â€” the layer with a reader was hiding seventeen households, and the reader is why nobody looked**

**The census answer, and it is worse than the fauna one it was written to be safer than.**
`data/residents/` had exactly one reader: `tools/compile_scene.py`'s `compile_residents()`
attaches a household to a building's sidecar and `popup.js` names it on the building card.
That join reaches a building through `lives_at` or `works_at` â€” so **a household whose
residence AND workplace are both unattested at the scene date attaches to nothing and
appeared on no card anywhere in this project.**

| | households | person entries |
|---|---|---|
| in `data/residents/` | 173 | 209 |
| reachable through a building card | 156 | 189 |
| **reachable nowhere, before today** | **17** | **20** |

**One of the seventeen is the Mark Beaubien household** â€” the man who built the Sauganash,
whose house held the incorporation election of 10 August 1833, and whose own record calls
itself *"the most famous household in the town and one of the thinnest records in this
parcel."* He is unreachable for exactly the reason his record is interesting: he had left
the Sauganash by 1834 and the Exchange by August 1834, so where he slept on 1 July 1835 is
not in the record, `lives_at` is `null`, and the join drops him. **The layer was dropping
records for being poorly evidenced, which is the opposite of what the confidence model is
for.**

**Finding 2 â€” a reader is not a read map, and this one carried a third of each record it
did reach.** `compile_residents()` copies id, name, division, the relation, its note, and a
person's name, relationship, grade and occupation *word*. Everything else stopped at the
repository: `arrival`, `origin`, `reason_for_coming`, `party_size_on_arrival`,
`present_on_scene_date`, `touches_removal`, a person's `sex`, `age_on_scene_date`,
`birth_year`, `name_basis` and their own `sources`, the occupation's grade and reasoning,
and the ten `researched_not_resident` findings whose own manifest doc calls them *"as
load-bearing as the households"*. **This is what K52's box predicted in as many words** â€” *"a
layer with one reader is exactly where an unread figure hides, because 'the browser has it'
reads as 'somebody looks at it'."* It was right, and the hiding place was bigger than the
fauna layer's, which at least had the decency to have no reader at all.

**Finding 3 â€” K42's assertion 3a did NOT fire here, and that is a hole rather than a pass.**
`tools/measure_layer_reads.py` scans `flora` and `fauna` and nothing else, so giving
`residents` a reader tripped no gate. The fauna parcel was caught by its own instrument; this
one was caught by reading the join. **Extending the census tool to `data/residents/` is not
done and is opened as K52(b)** â€” the tool is built around flora/fauna figure kinds and the
extension is its own parcel, not a line in this one.

**What shipped.** `renderers/web/js/residents.js`, the Evidence panel's people section: the
manifest in one fetch, all 173 households listed with their division, their people and their
grade tallies, the 17 marked on their own rows in the conjectural colour, and each household's
full record fetched the first time its row is opened. Every graded claim shows its value, its
confidence swatch, its reasoning and its joined citations; the ten researched non-residents
are published with theirs. **Nothing is drawn** â€” L1 and the standing constraint on depicting
people are untouched, and nothing in `docs/LIBERTIES.md` needed a line because nothing was
invented: this parcel published records that already existed.

**Files:** `renderers/web/js/residents.js` (new) Â· `renderers/web/index.html` Â·
`renderers/web/js/main.js` Â· `renderers/web/css/walk.css` Â·
`tools/compile_scene.py` (`compile_residents_sources`, the citation join, 11 sources) Â·
`tools/smoke_renderer.mjs` (ten assertions) Â· `data/sidecars/1835/residents_sources.json`.

**Not verified here:** the desktop half of the smoke does not fit the runner's ten-minute
per-command ceiling (Â§ THE RUN BUDGET). The mobile half ran on the published mirror: **263
passed, 2 failed**, and both failures are the road-contrast bands `dev` already carries red â€”
see `docs/STATUS.md` Â§ *Landed with two bands red*. This parcel changes no 3-D rendering.

### K52(b) â€” extend the read census to `data/residents/` Â· **DONE 2026-08-28 (T-0021) â€” the census found 113 person rows reading `[object Object]`, which is what a figure looks like when it is shipped, fetched, rendered and still not read**

`tools/measure_layer_reads.py` covered `flora` and `fauna` **by name** â€” its kinds, its
baseline and its self-test's negative control all written around those two â€” so `residents`
gaining a reader on 2026-08-17 fired nothing. The layer list is one table now (`LAYER_KINDS`),
read by the record walk, the citation census and assertion 3a alike, and the self-test carries
a new control for the shape of the hole itself: **every layer with a read map is a layer this
file walks.** A blind gate and a wrong gate are the same outcome from a visitor's side.

**69 residents figures classified: 64 `shown`, 0 `mesh`, 5 unread.** None is `mesh` and none
ever will be â€” L1 stands, v1 draws no human figures, so no figure of a person moves a vertex.

**AND THE CENSUS FOUND WHAT A CENSUS IS FOR.** Three of a person's figures â€”
`age_on_scene_date`, `birth_year` and `name_basis` â€” are graded claim blocks
(`{value, confidence, note, sources}`) and `personHtml` was handing all three **whole** to a
text renderer. **113 of the 209 person rows read "How this person is named â€” [object Object]"**
and nine said it twice more for the age and the birth year. Every assertion in the stage-9
suite passed throughout, because a card that renders the wrong string still renders a string;
what was lost is the pool an invented name was drawn from, on the 113 people whose names this
project invented. They go through `claimRow` now, with the swatch, the reasoning and the
citations every other graded claim on the card gets, and three smoke checks hold it â€” each one
verified to FAIL against the old render path before it was kept.

**Two smaller holes, wired in the same commit.** `counts.by_grade` reached nothing behind the
sentence *"every one of them graded"*, which is true and tells a reader nothing; the note now
gives the tally (76 attested, 20 inferred, 113 reconstructed). And `vocabulary.sexes` was the
one closed set the panel withheld while showing the value it governs.

**Five figures reach nobody and stay that way, each with a written reason in the bank**
(`refused_because`, new in `tools/layer_reads_baseline.json`): `counts.households` and
`households[].present_on_scene_date` and the household's own `division` are denormalised
copies of things already shown â€” showing the poorer copy would be showing less â€” and
`head`, in both copies, is a foreign key into `persons[].id` whose fact already reaches the
visitor as that person's `relationship`. A refusal is **not a permission**: the entries stay
banked, assertion 4 still fails on a new one and assertion 5 still fails if one leaves.

**Files:** `tools/measure_layer_reads.py` Â· `tools/layer_reads_baseline.json` Â·
`renderers/web/js/residents.js` Â· `tools/smoke_renderer.mjs` (stage 9).

### K53 â€” every shrub in the town is drawn as a giant forb Â· **DONE 2026-08-17 â€” the archetype is in, the recorded width is drawn, and the reason only fourteen of them stand is measured**

**The whole shrub layer is drawn with `forbGeometry()`** â€” one 12-triangle herbaceous stalk with
four broad leaves, scaled to the record's height. Twenty-one records across eight zones carry
`form: 'shrub_low'`, and `FORB_FORMS` contains that string, so a 3 m American hazel, a 2.5 m
elderberry, a multi-stemmed black-oak grub and a *sprawling mat* of sand cherry are all the same
wand of leaves at four different sizes. `placeForb`'s own comment names the damage and treats the
symptom: *"a riverbank shrub recorded at two metres across therefore grew sixty-centimetre leaves"*
â€” so the recorded clump width is CLAMPED to 0.40 m of spread, which is the shrub layer being made
narrow enough to look like a forb rather than being drawn as a shrub.

**It is SEEN and needs no exemption.** `corylus_americana` is the wet woods' *attested* dominant
shrub at 20â€“50 % cover â€” the dossier's own headline finding, with *"under-rendering hazel is the
specific mistake this record exists to prevent"* written beside it â€” and it is a wand. So is the
elder at the gallery edge, the dogwood on the river bank, the currant in the fenced dooryards and
the willow scrub on the lakeshore back slope, which is the population K45(b4) recorded as *"still
not planted"* in as many words.

**What it is NOT:** it is not a new record, not a new density and not a bake. Every number this
draws with â€” height, clump width, foliage greens, the July head â€” is committed and already read;
the archetype that consumes them is what is missing. The shrub form itself is a **reconstruction**
and gets a `docs/LIBERTIES.md` entry, exactly as the nine flower archetypes did.

**Files:** `renderers/web/js/flora.js` (a `shrubGeometry` archetype, a set beside `rosetteSet`, a
`placeShrub`) Â· `data/liberties.json` + `docs/LIBERTIES.md` Â· the flora gates' baselines if a read
moves Â· `renderers/web/js/changelog.js` Â· `site/chicago/4d/` Â· `docs/STATUS.md`.

**WHAT SHIPPED.** `shrubGeometry()` â€” four woody stems from one root, sixteen leaf sprays over
them, 40 triangles against the forb's 12 â€” on its own instanced set `flora-shrub`, dealt from the
forb lattice so it takes slots the forb archetype used to take rather than adding any. `placeShrub`
reads `width_m` as what it is on a shrub: the clump diameter. **Measured on the published mirror, at
all eight anchors and four bearings each:**

| | before | after |
|---|---|---|
| plants drawn with the shrub archetype | **0** | **14** |
| clump width | 0.40 m, the forb clamp | **1.80 m median, 2.00 m worst** |
| forb-layer plants, all archetypes | 2,201 | 2,187 + 14 = **2,201** |
| flora triangles, worst view | 41,754 | 41,772 |

**The census is identical plant for plant**, per zone as well as in total (`z08_lakeshore` 131 â†’
122 + 9, `z05_riverbank_timber` 61 â†’ 57 + 4, `z06_dense_forest` 222 â†’ 221 + 1). Nothing was redealt,
no density moved, and no record changed: this parcel changes what a plant is DRAWN as and nothing
else, which is why the sward census gate reads the same 6,809 slots and the same 154.19 / 89.11
deviations K49(c2) banked.

**FINDING 1 â€” the wands were only survivable because the width was clamped away.** `placeForb`
clamps spread to 0.40 m, and its own comment says why: *"a riverbank shrub recorded at two metres
across therefore grew sixty-centimetre leaves"*. That is the leaf archetype being protected from a
number that was never a leaf. `prunus_pumila`'s committed appearance is *"low sprawling mats 1-3 m
across"* and it was drawn 0.7 m wide and vertical. **A clamp that exists to protect one archetype
from another's data is a missing archetype, stated as a bound.**

**FINDING 2 â€” and it is why this is fourteen plants and not a hundred and forty: the forb lottery
deals by HEAD COUNT, so it under-draws exactly the plants that are big.** K49(c2) moved the lottery
onto `stems` â€” plants per mÂ² â€” to fix the opposite fault, a species recorded as covering 25 % of the
ground being dealt as 0.25 plants/mÂ². The conversion for a cover-recorded species is
`cover / (Ï€ Â· (width/2)Â²)`, so a hazel that covers 7 mÂ² of ground converts to 0.088 plants/mÂ² and
competes for slots against `allium_tricoccum` at **40 plants/mÂ²**. Measured over each zone's forb
list, the shrubs' share of the lottery is:

| zone | shrub share of the forb list | the species that takes the rest |
|---|---|---|
| `z10_settled_town` | **0.1 %** | four weeds at 0.4â€“1.1 plants/mÂ² |
| `z06_dense_forest` | **1.0 %** | `allium_tricoccum`, 99.0 % |
| `z08_lakeshore` | 2.6 % | `artemisia_campestris`, `campanula_rotundifolia` |
| `z05_riverbank_timber` | 3.0 % | `allium_canadense`, 97.0 % |
| `z09_sand_prairie` | 7.6 % | `allium_cernuum`, `monarda_punctata` |

So `corylus_americana`, **attested** at 20â€“50 % ground cover and named in its own note as the
specific under-rendering this record exists to prevent, is drawn as **1 plant of 221** in the wet
woods. The count is not wrong â€” one hazel IS one plant â€” but the layer is a SAMPLE of ~220 slots
against a population of tens of thousands, and a sample drawn by count reproduces the population's
head count while reproducing none of its ground cover. **Both readings are defensible and this
parcel changes neither**; the numbers are banked and the question is opened as **K54** rather than
retuned here, because K49(c2) moved this lottery deliberately and moving it back is a decision, not
a repair.

**FINDING 3 â€” the first cut of the archetype was the wand at a larger size.** Four stems each
carrying one 60 cm paddle reads as a candelabra, not a bush; the shot showed it and the fix was
sixteen small sprays over two heights rather than four big ones. **A silhouette is made by its
outer shell**, which is the same thing `trees.js` says about a crown in its own comment â€” and it is
worth writing down that the archetype had to be LOOKED at, twice, after it measured correct.

**Verified:** `tools/check.sh` â€” CHECK PASS (the dev gate; `chicago-4d-check.yml` runs it and
nothing else), after `tools/publish.sh` in the same commit. `tools/measure_sward_draw.mjs --gate` â€”
PASS, 0 of 98 (list, species) pairs drawn nowhere, 6,809 slots, deviations unmoved. The before/after
readings above are `flora-shrub`/`flora-forb`/`flora-rosette` instance counts and their `aFlora`
attributes read back off the published mirror at 1280Ã—800, against a worktree of `origin/dev` for
the before column. Evidence: `docs/evidence/k53-{before,after}.png`, the river-bank stand at
E âˆ’288 / N +368 facing SSE. **Zero page errors** in every run.

**NOT verified here:** neither half of `tools/smoke_renderer.mjs`. The desktop half has never fitted
this runner's ten-minute per-command ceiling and K45(b4) recorded the mobile half outgrowing it too;
the three gates in it that read the flora sets by NAME were extended to `flora-shrub` in this commit
(rooted-plant anchoring, the pop-in walk, head support) plus `tools/measure_head_support.mjs`, so
the new set is inside them rather than invisible to them â€” but that extension is unexecuted here and
is the first thing to run on a runner without the ceiling.

### K54 â€” the forb lottery deals by head count, and the shrub layer is the population it loses Â· **DONE 2026-08-17 â€” route 2, and neither reading of the sample was the fault: the two strata were sharing one lattice**

**The answer to "which quantity should a sample reproduce" is that this sample did not have to
choose.** A lattice slot is 2.89 mÂ² of ground and carries one plant, so where the herb layer's own
recorded density SATURATES the lattice â€” five of the ten communities â€” the deal stops being a
population draw and becomes a count-proportional subsample. A subsample by head count thins the
shrubs by the whole saturation ratio, and in the wet woods that ratio is **117**. But a hazel clump
stands OVER the leeks rather than instead of them, and the records state the two separately: nine
`shrub_low` records in `z06_dense_forest` summing to **94.9 %** ground cover, above a herb layer
recorded at **40 plants/mÂ²**. So the shrub stratum is dealt from **its own lattice pass over the same
ring**, at its own recorded clump density, with a different salt so the two draws are independent.
**Nothing is taken from the herb layer to pay for it, and no share, cap or tuning number was
authored.**

| `tools/measure_sward_draw.mjs`, published mirror, 8 communities stood in | before | after |
|---|---|---|
| shrub instances standing, summed over the 8 stations | **4** | **181** |
| shrubs drawn standing in `z06_dense_forest` | 2 | **156** |
| drawn shrub cover there, against a recorded 94.9 % | ~0 | **40.1 %** |
| drawn shrub cover, `z05_riverbank_timber`, recorded 19.5 % | 2.0 % *(the whole forb list)* | **20.1 %** |
| deviation per 100 slots â€” matrix | 2.58 over 5,965 | **2.58 over 5,965** |
| deviation per 100 slots â€” forb | 10.56 over 844 | **10.40 over 781** |
| deviation per 100 slots â€” shrub | â€” | **10.41 over 181** |
| (list, species) pairs owed a whole slot and drawn nowhere | 0 of 98 | **0 of 98** |

**The gain K54 required is kept, and the raw sums cannot show it** â€” `forb 89.11` became
`forb 81.22 + shrub 18.84` because the deviation is an absolute sum over slots and this parcel split
one list into two. Per 100 slots the herb list IMPROVED and the new shrub list draws at the same
fidelity. Hence the tool's new per-slot column: **a discrepancy sum cannot compare two draws of
different sizes**, and every previous parcel that quoted 89.11 against another build was comparing
lists of the same length by luck.

**FINDING 1 â€” the slot count still mixed units, and it planted the riverbank understory 8.8Ã— too
thickly.** K49(c2) moved the LOTTERY onto `stems` and its own comment says the slot count was left
on the recorded sum. That sum adds cover fractions to plants per mÂ², and sixteen of the twenty-one
shrub records state an area: `z05_riverbank_timber`'s forb share was **0.636 where its herb records
give 0.072**, and `z07_bur_oak_savanna`'s hazel â€” its only forb-list species â€” was planted at **4Ã—**
its own recorded clump density. So the riverbank swap is not only more shrubs: it is **11 dogwood,
elder and ninebark clumps carrying 20.1 % cover in place of 33 herbs carrying 2.0 %**, and the herbs
that left were never in the record. Dealing the shrub stratum off `stems` closes it for that
stratum; **four herb lists still carry it (`z03`, `z05`, `z06`, `z10`), and the tool now names them
with a `basis` column. Opened as K55.**

**FINDING 2 â€” the instrument K54's own box named cannot answer K54's question, and had been
mislabelled since K49(c2).** `expected` is `share Ã— slots` and `share` is the species' share of the
LOTTERY, so *"deviation from the recorded cover"* â€” the line this box quoted as *"the very quantity
in question"* â€” measures the lattice's disagreement with its own target distribution and never
touches a record. It is the right figure for comparing two draws and the wrong one for judging
fidelity to the data. The tool prints a real `cover` column now, and **its first denominator was
wrong in R-M1c's exact way**: dividing a community's drawn plants by the whole ring reported 17.9 %
where that community holds a fifth of the ring. It divides by the community's own MEASURED plantable
ground inside the ring â€” 1 mÂ² samples through `zoneAt` and `plantableAt`, the placer's own rules.

**What it costs and what is NOT verified.** One extra lattice pass over the forb ring per rebuild;
`flora-shrub` was already a committed set and a committed draw call, so the frame gains instances and
no batch. Neither half of `tools/smoke_renderer.mjs` ran â€” the desktop half has never fitted this
runner's ten-minute per-command ceiling and the mobile half has outgrown it (K45(b4), K53) â€” and the
scene was not measured at `full` detail, where the lattice offers ~1,113 slots against the set's
900-instance cap, so a saturated community may cap there. The forb set has the identical lattice and
cap and sits just under it today. `tools/check.sh` CHECK PASS after `tools/publish.sh` in the same
commit; `--gate` PASS; zero page errors in every run.

**Two station-row diagnostics appeared and are not the gate.** `solidago_riddellii` (owed 1.77 at one
station) and `physocarpus_opulifolius` (owed 1.17 at one station) are drawn nowhere in the ring at
one station each, having been drawn there before; both are drawn elsewhere in the scene, so the
K49(f) scene-wide gate reads 0 of 98 as it did. They moved because removing the shrubs renormalised
those lists' shares. Read K49(a) before quoting a station row as a scene figure.

**The routes NOT taken.** Route 1 (a fixed slot share off `cover_fraction`) authors a quantity no
record states, and the measurement that decided against it is worth keeping: dealt on cover, the
shrubs would take **30â€“100 %** of the forb list's slots in seven of ten communities, because the herb
forbs' own summed cover is under 1 % of the ground in most of them â€” the ground cover in a prairie
belongs to the MATRIX list, which is dealt separately. Route 3 (say it on the card) was available and
is now unnecessary.

**FINDING 3 â€” and it came from LOOKING, which is K53's finding 3 one parcel later: the archetype
was designed and photographed at fourteen instances in the whole scene, and the wet woods now
carries 158 in one ring.** `docs/evidence/k54-{before,after}.png`, the same station (E âˆ’54 / N +314,
bearing 135Â°) at 1280Ã—800 on the published mirror: the before frame is an open field with a log
building 15 m away and ONE shrub in the corner; the after frame is a thicket the building shows
through. That is what the record asks for â€” `z06_dense_forest` reads_as *"a hazel shrub layer
through all of it"* and its nine shrub records sum to 94.9 % cover â€” and it is also the first time
anyone has seen this archetype repeated. **At that density its leaf sprays read as ~0.4 m paddles**,
which is the shell L122 bounded to 0.30â€“0.55 of the recorded half-width and is defensible on a
2.25 m hazel; whether it should scale that way is now a question a visitor can answer, and it is
opened as **K56**. Flora triangles at the station **46,904 â†’ 58,868**; the herb layer is untouched
(forb 194 â†’ 195, rosette 35 â†’ 31) which is the arithmetic proof that nothing was taken to pay for
it; zero page errors.

### K54 â€” original statement, for the record Â· **superseded by the box above**

**The arithmetic is banked in K53 finding 2 and is not in dispute.** The forb layer deals ~220
slots over the ring; each slot is one plant; species compete for slots on `stems`, plants per mÂ².
A hazel covering 7 mÂ² of ground is 0.088 plants/mÂ² and a wild leek is 40, so the wet woods are
drawn as leeks with one shrub in them, and the shrub layer their own dossier calls the dominant
one takes **1.0 %** of the deal.

**The question is which quantity a SAMPLE should reproduce.** By head count the current deal is
exactly right and the frame is wrong; by ground cover the frame would be right and the head count
wrong. Three routes, none of them free:

1. **Deal a fixed share of the slots to the shrub sub-list**, off the recorded `cover_fraction` â€”
   the field the shrubs mostly carry â€” and deal the rest by count as today. Honest, cheap, and it
   makes the layer's slot mix a second authored quantity that no record states.
2. **Give the shrubs their own lattice**, the way `trees.js` has one: a sparse layer dealt on
   plants per hectare over a wider radius, which is what a shrub layer physically is. The most
   faithful and the largest.
3. **Leave it and say so on the card.** The layer is a count-faithful sample; the Evidence panel
   could say that a drawn plant is one plant and that ground cover is not what the sward reproduces.

**Do not take this as a tuning.** K49(c2) moved this lottery onto counts deliberately and measured
the improvement; whatever lands here has to keep that gain (matrix 154.19 / forb 89.11 deviation,
0 species drawn nowhere) and say which quantity it is now faithful to. **`tools/measure_sward_draw.mjs`
already prints everything needed to judge it** â€” it reports the deviation from recorded cover, which
is the very quantity in question.

**Files:** `renderers/web/js/flora.js` (`compileZones`, `dealt`) Â· `tools/measure_sward_draw.mjs`
(a cover-share column) Â· `docs/LIBERTIES.md` if a share is authored.

### K55 â€” four herb lists still deal their SLOT COUNT off a sum of areas and counts Â· **DONE 2026-08-17 â€” the same fault runs BOTH WAYS, and for the herbs it ran the other one: the riverbank's ground layer was planted 96Ã— too THINLY**

**The repair.** `SLOT_BASIS` is one object naming which sum each stratum's slot count is dealt off,
and both lattice strata now read `stems`. The forb half is what moved; the arithmetic is K54's and
was not re-derived.

| forb layer | density before | after | ratio | forbShare before â†’ after |
|---|---|---|---|---|
| `z05_riverbank_timber` | 0.025 /mÂ² | **2.407** | **96Ã—** | 0.072 â†’ **1.0 (clamped)** |
| `z10_settled_town` | 0.395 | **7.760** | 19.6Ã— | 1.0 â†’ **1.0, no slot moves** |
| `z03_sedge_meadow` | 0.123 | **1.254** | 10.2Ã— | 0.354 â†’ **1.0 (clamped)** |
| `z06_dense_forest` | 40.615 | **44.545** | 1.10Ã— | 1.0 â†’ 1.0 |
| the other six | unchanged to the digit | | 1Ã— | unchanged |

Drawn, on the published mirror over the census's eight stations: **forb slots 781 â†’ 923**,
`z03_sedge_meadow`'s own layer **31 â†’ 84** (cover 1.0 % â†’ 2.8 % of a recorded 11.0 %),
`z05_riverbank_timber`'s **1 â†’ 16** at its own station and **4 â†’ 50** standing in the wet woods, with
a row at `z03` that did not exist before (**0 â†’ 14**). Forb deviation per 100 slots **10.40 â†’ 9.33**.
**Matrix and shrub are unchanged to the second decimal** â€” 154.19 and 18.84, the same figures K54
banked â€” and `0 of 98` pairs are drawn nowhere.

### Finding 1 â€” a cover fraction read as a count is wrong in whichever direction the plant's own size points

K54 measured this fault OVERSTATING by 8.8Ã— and fixed it downward. The herb lists have it
understating by up to 96Ã—, and the two are the same division: `stems = cover Ã· Ï€(width/2)Â²`, so the
sign is decided by whether one plant covers more or less than a square metre. A 2.25 m dogwood
clump covers ~4 mÂ², so its cover fraction is a bigger number than its count; a 10 cm forb covers
~0.008 mÂ², so its cover fraction is ~125Ã— smaller. **"Adding an area to a count" was banked here as
over-planting because that is the case that was measured first**, and the queue inherited the
direction along with the diagnosis.

### Finding 2 â€” the report was naming three refusals as work, because it printed a default argument

The parcel's own box suspected the matrix half was a refusal and it is: `matrixShare` comes off
`cover.matrix_fraction` directly, and `subsetOn`'s `density` was **computed for the matrix and read
by nobody**. The `basis` column that named `z03.matrix`, `z08.matrix` and `z09.matrix` as K55 work
was printing `subsetOn`'s default parameter, not a fact about the renderer â€” so three of the parcel's
six named rows were never faults at all. Both the renderer and the report read `SLOT_BASIS` now, and
the matrix's entry is `null` rather than a label, so there is no number left to misread.

### Finding 3 â€” it is SEEN, and only just: the count moved a fifth and the picture moved 0.15 %

`docs/evidence/k55-{before,after}.png`, `z05_riverbank_timber` at E âˆ’300 / N +398 bearing 090Â°,
1280Ã—800 on the published mirror: **1,586 changed pixels of 1,024,000 (0.15 %)** â€” a scatter of white
flower heads through the near grass. At the `z03_sedge_meadow` station the same comparison is **24
pixels at 135Â° and nothing at 315Â°**, because the added plants are small and stand under a dense
matrix layer. **The parcel's own prediction that `z10_settled_town`'s weeds were "the visible half"
is refused by the table above**: that share was over the lattice ceiling before and after, so the
one community a visitor spends the walk in is the one community that does not move. Quote the
counts for this parcel, not a screenshot.

### Successor â€” K58, the forb lattice's ceiling now binds six communities of ten

`forbShare` clamps at one plant per slot, and K55 takes the clamped count from four communities to
six (`z05` and `z03` join `z04`, `z08`, `z10`, `z06`). A clamped share means the record is asking for
more plants than the lattice can carry, so the drawn cover is bounded by `TUNE.forb` rather than by
any research figure â€” `z06_dense_forest` reaching 40.1 % of a recorded 94.9 % is that ceiling, not a
data gap. Opened below.

### K55 â€” original statement, for the record Â· **superseded by the box above**

**The arithmetic is banked in K54 finding 1 and is not in dispute.** `subsetOn`'s `density` sums
`s.recorded` â€” the abundance in whatever unit the record used â€” and `forbShareOf` reads that sum as
plants per mÂ². Where a list mixes the two, the slot count is a cover fraction added to a count.
K49(c2) left it there deliberately and said so; K54 fixed the shrub stratum's half of it by dealing
that list off `stems`. **What is left, printed every run by `tools/measure_sward_draw.mjs` under
`slot count off 'recorded'`:** `z03_sedge_meadow.matrix`, `z03_sedge_meadow.forb`,
`z06_dense_forest.forb`, `z08_lakeshore.matrix`, `z09_sand_prairie.matrix` â€” and `z05`'s and `z10`'s
forb lists, which are ENTIRELY area-recorded and therefore do not register as "mixed" at all. That
last case is the trap: a list where every species records an area reads as consistent and its slot
count is still wrong by the same conversion.

**It is SEEN and it is not a free change.** `z10_settled_town`'s forb layer is the weeds in the
streets of the town a visitor spends most of their walk in, and its share is currently saturated at
1.0; dealt on `stems` it may not be. So this is a measure-then-fix parcel: land the before/after
census with the per-100-slot column K54 added, and expect the town to look different.

**The matrix lists are the harder half and may be a refusal.** `matrixShare` comes off the record's
own `cover.matrix_fraction` and is not this sum at all, so a matrix list's `mixed` row is about the
LOTTERY only, which K49(c2) already put on `stems`. Check that before changing anything there.

**Files:** `renderers/web/js/flora.js` (`subsetOn`, `forbShareOf`) Â· `tools/measure_sward_draw.mjs`
baselines Â· `docs/STATUS.md`.

### K56 â€” the shrub's leaf spray is scaled off the clump width, and 158 of them in one ring is the first look anyone has had at that Â· **DONE 2026-08-17 â€” the spray is a leaf MASS, so the size was never the number: sixteen of them covered 17.7 % of the shell and you could see straight through every clump**

`shrubGeometry`'s sprays are a fraction of the recorded half-width (L122), so a `corylus_americana`
recorded 2.25 m across carries sprays about 0.4 m long. At fourteen instances scattered over the
whole scene that was invisible; at **158 in the wet woods' ring** it is the near-field texture of a
whole community â€” `docs/evidence/k54-after.png`.

**The question is not whether 0.4 m is right, it is what the spray STANDS FOR.** A grass tuft in
this renderer is a bundle of shoots and says so; if a spray is a bundle of leaves then its size is a
rendering choice bounded by the plant's shell and the answer may be "unchanged". If it is meant to
read as a leaf, a hazel leaf is ~10 cm and no scaling off the clump width can produce one at 40
triangles. **Decide which, write it into L122 or a new liberty, and only then change a number.**

Cheap and visible: one archetype function, one before/after pair at the station K54 used, and
`tools/measure_sward_draw.mjs` is unaffected because no count moves.

**Files:** `renderers/web/js/flora.js` (`shrubGeometry`) Â· `docs/LIBERTIES.md` Â· `docs/evidence/`.

**THE ANSWER TO THE QUESTION THE PARCEL ASKED, because it decides which number moves.** A spray
stands for **a mass of leaves on one shoot**, not a leaf. That is the same abstraction the tree
canopy's plates and the near tuft's bundle of shoots already use in this renderer, and it is the
only one two triangles can carry: a hazel leaf is ~10 cm and no scaling off the clump width
produces one. So the honest reading of the 0.4 m spray is **not wrong**, and shrinking it would
have bought a smaller plate with more sky around it. Written into `docs/LIBERTIES.md` as **L124**
before any number changed, which is the order the parcel asked for.

**WHAT THE LOOKING FOUND, and it is the count.** Summed over the archetype's own loop, the sixteen
sprays' plates cover **17.7 %** of the shell they are spread over â€” a clump a visitor sees straight
through, which is why an isolated plate reads as one enormous leaf: nothing overlaps it. **32
sprays cover 30.9 %.** `docs/evidence/k56-{before,after}.png`, the same station K54 used (E âˆ’54 /
N +314, bearing 135Â°) at 1280Ã—800 on the published mirror.

| | before | after |
|---|---|---|
| leaf sprays per shrub | 16 | **32** |
| spray bands | 2 | **3, the lowest arching DOWN** |
| plate area, archetype unitsÂ² | 1.399 | **2.698** |
| shell fill | 17.7 % | **30.9 %** |
| triangles per shrub | 40 | **72** (+5,056 in the wet woods' ring, of a 1,000,000 ceiling) |
| spray length on a 2.25 m clump | 0.26â€“0.44 m | **0.26â€“0.44 m â€” unchanged** |
| drawn reach, as a fraction of the recorded half-width | 0.91 | **0.98** |

**FINDING â€” nothing in the first cut hung below its own attachment.** All sixteen sprays rose, so
the shell stayed open exactly where the four stems are most exposed, and `k0 = shade(0.16)` makes
those stems a black stick wherever foliage does not cover them â€” which the archetype's own comment
had feared in the abstract and the before frame shows happening. The lowest of the three bands now
arches down over them, bounded so no tip is pushed below the plant's base.

**No census moved.** Same species in the same places, plant for plant; `spread`, `height` and the
lattice are untouched. The gate `tools/measure_sward_draw.mjs` is unaffected, as the parcel
predicted, because no count moves.

### K57 â€” the spray's GRAIN, which trades triangles against the size of a leaf mass Â· **DONE 2026-08-17 â€” asked at a fixed plate area it cannot be asked at all, because the plates carry the recorded clump width; 48 sprays ship at K56's plate size and 48 is where the return halves**

K56 answered *what a spray stands for* and moved the count. It did **not** answer the finer
question underneath: at a fixed total plate area, is the shell better read as 32 masses of 0.4 m or
64 of 0.2 m? That is a grain question and it costs triangles â€” 32 sprays is 72 triangles a shrub,
64 would be 136 â€” so it needs a **frame-time and triangle budget measured in the wet woods**, where
158 of them stand in one ring and the matrix layer is densest, rather than a preference.

**What bounds the answer.** The plate may not shrink below the size at which it reads as a single
leaf against its neighbours, which is the fault K56 diagnosed and would rebuild at a smaller scale
if the count did not rise with it. So grain and count move together or not at all.

Cheap and visible: one archetype function, one before/after pair at the same station, and the
triangle line printed by the smoke at both viewports is the budget half.

**Files:** `renderers/web/js/flora.js` (`shrubGeometry`) Â· `docs/LIBERTIES.md` Â· `docs/evidence/`.

**What it measured, banked so nothing re-derives it.** 24 bearings, orthographic, on the archetype the
scene draws â€” foliage cover is the UNION of the projected plates over the convex hull of them, because
"you can see straight through it" is a statement about union and a sum counts an overlap twice:

| candidate | plate area | cover | worst bearing | stem cover | reach | plate cm | triangles |
|---|---|---|---|---|---|---|---|
| 32 @ 1.000 (K56) | 2.698 | 36.9 % | 33.0 % | 40.9 % | 0.990 | 37.3 | 72 |
| 48 @ 0.816 (area held) | 2.604 | 43.3 % | 39.3 % | 46.8 % | 0.930 | 29.3 | 104 |
| 64 @ 0.707 (area held) | 2.624 | 45.4 % | 41.5 % | 48.3 % | 0.890 | 25.8 | 136 |
| **48 @ 1.000 (shipped)** | 3.812 | **46.9 %** | **43.0 %** | **51.3 %** | **0.998** | 35.0 | **104** |
| 64 @ 1.000 | 4.986 | 51.3 % | 47.3 % | 54.2 % | 0.997 | 34.6 | 136 |

**The generalisation, and it is not about shrubs.** An archetype's numbers divide into the ones the
RECORD owns and the ones the renderer owns, and a tuning question phrased as "hold X and improve Y" is
only answerable once you know which side X is on. Here X was the total plate area, which sounds like a
renderer number and is a researched one wearing a disguise: the plates ARE the silhouette, and the
silhouette is the record's `height_m` and half-width. **Before holding a quantity fixed in any
archetype, ask which side of that line it is on.** The same trap is live in every other plate-based
archetype here â€” the tree canopy, the near tuft, the forb head.

### K59 â€” the last 4.4 points of the shrub's shell, and whether a frame can afford them Â· **DONE 2026-08-23 (T-0020) â€” the frame was read and the points are spent: 64 sprays ship, for +3.0 % of a frame on desktop and +2.1 % on mobile against a 0.2 % A/B/A control**

K57 shipped 48 sprays at the knee and left 64 measured and unspent: **cover 46.9 % â†’ 51.3 %, worst
bearing 43.0 % â†’ 47.3 %, stem cover 51.3 % â†’ 54.2 %, for 104 â†’ 136 triangles a shrub** and 17,368 â†’
22,712 in the wet woods' ring of 167, of a 1,000,000 ceiling. Reach is unaffected (0.998 â†’ 0.997), so
this is a pure budget question and the numbers are already banked â€” nothing needs re-measuring.

**What is NOT known, and it is the whole parcel:** no frame-time figure has been taken anywhere in this
archetype's history. K57 justified 104 on a triangle count and a draw-call count, which is not a frame.
The batch does not split â€” one instanced set, one draw call, K56 and K57 both â€” so the cost is fill and
vertex work, and neither has been read. **Take this parcel only with a frame-time measurement in
hand**, in the wet woods where 167 of them stand; without one it is a preference wearing a table, which
is exactly what K57 refused.

**Files:** `renderers/web/js/shrub-grain.js` (`SHRUB_GRAIN.fill`) Â· `tools/measure_spray_grain.mjs`
Â· `docs/LIBERTIES.md` Â· `docs/STATUS.md`.

**THE ANSWER, 2026-08-23 (T-0020). The parcel's own condition was met before any×­µçkh‘éì¶»§q«^uÅÕ•Õ”è™É½´M½ÕÑ )]…Ñ•ÈÌ½µµ¥ÑÑ••¹ÑÉ•±¥¹”Ñ¡”ÑÉ…•€ÄàÌĞİ…Ñ•É±¥¹”¥Ì€¨¨ÄÀ¸ÜÔ´…İ…ä…Ğ€¬ÄàÀ……¥¹ÍĞ„(ÄÈ¸Ää´¡…±˜µ½ÉÉ¥‘½È¨¨°Í¼Ñ¡”Á±…ÑÑ•ÍÑÉ••ĞÑ¡•É”ÉÕ¹Ì€Ä¸Ğ´¥¹Ñ¼Ñ¡”É¥Ù•È…¹„‰Õ¥±‘¥¹œ½¸)¥ÑÌ¹½ÉÑ Í¥‘”…¹¹½Ğ‰”‰½Ñ ±•…È½˜Ñ¡”½ÉÉ¥‘½È…¹½¸‘Éä±…¹¸Q¡…Ğ¥ÌÑ¡”Á±…Ğµ½‘Õ±”…¹)Ñ¡”‘É…İ¸‰…¹¬‘¥Í…É••¥¹œ°…¹¥Ğİ…¹ÑÌ„É•…‘¥¹œ½˜Ñ¡”ÑÉ…Ù•±±•İ…ä€¡0Üä¤°¹½Ğ„¹Õ‘”Ñ¼)Ñ¡¥ÉÑ••¸É•½É‘Ì¸Q¡”M…Õ…¹…Í Ì™¥ÉÍĞ…‰¥¸É•µ…¥¹ÌÑ¡”É•µ¥¹‘•ÈÑ¡…Ğ„‰Õ¥±‘¥¹œ¥¸Ñ¡”ÍÑÉ••Ğ)¥ÌÍ½µ•Ñ¥µ•Ì„™…Ğ°…¹Í±½Õ¡}±½}‰É¥‘•€¥¸Ñ¡”M½ÕÑ ]…Ñ•È½ÉÉ¥‘½È¥ÌÑ¡”É•µ¥¹‘•ÈÑ¡…Ğ)Í½µ•Ñ¥µ•Ì¥Ğ¥ÌÑ¡”Á½¥¹Ğ¸€¡ˆ¤Q¡”É¥)½Ù•ÉÌ€Ää½˜Ñ¡”Á±…ĞÌ€Ôà‰±½­ÌìÑ¡”9½ÉÑ ¥Ù¥Í¥½¸¥Ì…‰Í•¹Ğ‰•…ÕÍ”¥ÑÌÍÑÉ••Ğ½¹ÑÉ½°¥Ì)İ¡…Ğƒ
œLäÍÑ¥±°É•½É‘Ì…Ì½İ•°…¹‰±­}Í½ÕÑ¡}İ…Ñ•É}µ…É­•Ñ€ƒŠP½¹”½˜Ñ¡”µ½ÍĞ‰Õ¥±ĞµÕÀ‰±½­Ì)¥¸Ñ½İ¸ƒŠP¥ÌÉ•™ÕÍ•½¹±ä‰•…ÕÍ”Ñ¡”ÍÑÉ••Ğ±…å•È‘½•Ì¹½Ğ…ÉÉäM½ÕÑ ]…Ñ•Èİ•ÍĞ½˜€¬ÄÀÀ¸(¡Œ¤Qİ¼Á¥Ñ¡•Ì‘¥Í…É•”İ¥Ñ Ñ¡”€ÄàÌĞÑÉ…Ù•ÉÍ•Ì€¡•…É‰½É»ŠIMÑ…Ñ”€ÄÈà¸À´°1…­—ŠII…¹‘½±Á €ÄĞÈ¸à´¤)…¹…É”É•½É‘•É…Ñ¡•ÈÑ¡…¸…Ù•É…•¸€¡¤9¼Í½ÕÉ”¥¸‘…Ñ„½Í½ÕÉ•Ì½€¥Ù•Ì„Q¡½µÁÍ½¸1=P)AQ ìÑ¡”‘•ÁÑ¡Ì¡•É”…É”É•Í¥‘Õ…±Ì½˜Ñ¡”‰±½¬°…¹™¥¹‘¥¹œ„ÍÑ…Ñ•½¹”¥Ìİ¡…Ğİ½Õ±µ½Ù”)Ñ¡”±½Ğ±¥¹•Ì½™˜½¹©•ÑÕÉ”¸€¡”¤9½Ñ¡¥¹œ‘É…İÌÑ¡”É¥ƒŠPİ¡•¸Ñ¡”±½Ğ±¥¹•ÌÉ•… Ñ¡”ÍÉ••¸)Ñ¡•ä¹••„±¥‰•ÉÑä…¹„½¹™¥‘•¹”ÑÉ•…Ñµ•¹Ğİ¥Ñ Ñ¡•´¸((ŒŒŒ,àƒŠPI¥Ù•È‰…¹¬¡•¥¡ÑÌ€¨¡É•Í•…É ™¥ÉÍĞ°Ñ¡•¸Ñ•ÉÉ…¥¸¤¨ƒ
Ü€¨©=9€ÈÀÈØ´Àà´ÈÀ€¡P´ÀÀÀĞ¤¨¨)Q¡”½İ¹•Èè‰…¹­Ì±½½¬Ñ½¼±½Ü……¥¹ÍĞÑ¡”™½ÉĞÙ¥•İÌ€ ÄÃŠLÈÀ™Ğİ¥Ñ É…‘Õ…Ñ•Í±½Á•Ì¤¸Q¡”)‘½ÍÍ¥•È¥Ù•Ì€¬ËŠLĞ™Ğ‰…¹­Ì…ĞÑ¡”™½É­Ì€¡‘½Õµ•¹Ñ•¤‰ÕĞÑ¡”=IPÍÑ½½½¸‘¥ÍÑ¥¹Ñ±äÉ¥Í¥¹œ)É½Õ¹ƒŠP€‰Ñ¡”™±…ÑÑ•¹•µ½Õ¹ˆ°Ñ¡”€ÄàÌÀ!…ÉÉ¥Í½¸Á±…¸Ì‰…¹¬°Mİ•…É¥¹•¸Ì€Äàµ™ĞÁ½½°…ĞÑ¡”)™½ÉĞ‰•¹¸A…É•°èÉ”µÉ•…€ÀÄµÑ•ÉÉ…¥¸µ¡å‘É½±½ä¹µ‘€…¹Ñ¡”ÁÉ¥µ…Éä…½Õ¹ÑÌìÉ…¥Í”…¹)IUQÑ¡”™½ÉĞµÉ•… Í½ÕÑ ‰…¹¬…ÌÑ¡”•Ù¥‘•¹”ÍÕÁÁ½ÉÑÌìÉ•½ÉÑ¡”‘¥Í…É••µ•¹Ğ‰•Ñİ••¸)Ñ¡”Ñ¥•È´Ô±¥Ñ¡½É…Á¡Ì…¹Ñ¡”‘½ÍÍ¥•ÈÉ…Ñ¡•ÈÑ¡…¸…Ù•É…¥¹œ¥Ğì­••ÀÑ¡”™½É­Ì‰…¹­Ì…ĞÑ¡•¥È)‘½Õµ•¹Ñ•¡•¥¡Ğ¸É…‘¥•¹Ğ…Õ‘¥ĞÉ”µÉÕ¸ì•á•µÁÑ¥½¸¥Ñ•µ¥Í•±¥­”Ñ¡”½Ñ¡•ÉÌ¸((¨©M¡¥ÁÁ•¨¨èÑ¡”µ½Õ¹É…¥Í•™É½´Ñ¡”é½¹”Ìµ¥µÉ…¹”Ñ¼¥ÑÌÍÑ…Ñ•…Á•àƒŠP)™½ÉÑ}‘•…É‰½É¹}µ½Õ¹¹É¥Í•}™Ñ€€È¸àƒŠH€Ì¸à°™±…ĞÑ½À€¬ÄÄ¸ÀƒŠH€¬ÄÈ¸À™Ğ°Ñ¡”¹½ÉÑ ™…”…ÉÉå¥¹œ)Ñ¡”™Õ±°É¥Í”Ñ¼Ñ¡”İ…Ñ•É±¥¹”…Ğ€ÄèØ¸à€¡¥¹Í¥‘”Ñ¡”‰…¹¬‰±½¬Ì€ÄèÛŠLÄèÄÀ‰…¹¤¸Q¡”)‘¥Í…É••µ•¹Ğ¥ÌÑ¡É•”µ½É¹•É•°¹½ĞÑİ¼°…¹¥ÌÉ•½É‘•É…Ñ¡•ÈÑ¡…¸…Ù•É…•¥¸)‘½Ì½IMI ½™½ÉÑ}É•…¡}‰…¹­}¡•¥¡ÑÌ¹µ‘€èÑ¡”İ¥Ñ¹•ÍÍ•Ì€¡Mİ•…É¥¹•¸€ÄàÀÌÑ¥•È´Äøà™Ğì)!Õ‰‰…É€ÄààÄ€‰¹½Ğ½Ù•È•¥¡Ğ™••Ğˆ°„½ÉÉ•Ñ¥½¸ÁÕÍ¡¥¹œ=]8¤­••ÀÑ¡”	9,°é½¹”€ØÌ(¬ÄÃŠLÄÈ½…Á•à€¬ÄÈÑ…­•ÌÑ¡”µ½Õ¹°…¹Ñ¡”Á±…Ñ•Ìœ€ÄÃŠLÈÀ™Ğ¥ÌÉ•™ÕÍ•…Ì„‰Õ¥±¥¹ÁÕĞ¸)!Õ‰‰…ÉµÙÌµé½¹”´ØÍÑ…¹‘ÌÕ¹É•Í½±Ù•½¸Ñ¡”É•½ÉƒŠP¥˜Ñ¡”½İ¹•ÈÉÕ±•ÌÑ¡”İ¥Ñ¹•ÍÍ•Ì½ÕÑÉ…¹¬)Ñ¡”‘½ÍÍ¥•ÈÌÉ•½¹¥±¥…Ñ¥½¸°Ñ¡”µ½Õ¹‘É½ÁÌÑ¼ø¬àìÑ¡…Ğ¥Ì„ÉÕ±¥¹œ°¹½Ğ„É•Í•…É …À¸)5•…ÍÕÉ•è€È°ÄØä¡…¹••±±Ì°µ…à€¬À¸ÌÀÔ´°é•É¼½ÕÑÍ¥‘”Ñ¡”µ½Õ¹Ì€ÜÔ´É…‘¥ÕÌƒŠPÑ¡”™½É­Ì)‰åÑ”µ¥‘•¹Ñ¥…°¸É…‘¥•¹Ğ…Õ‘¥ĞAML€¡Á±…¥¸µ…à€À¸ĞØà¤°µ½Õ¹‰…¹¥Ñ•µ¥Í•…Ì‰•™½É”¸Q¡”)‰…¹¬¹½ÜÍÑ…¹‘¥¹œ¥Ìİ¡…ĞÕ¹‰±½­ÌP´ÀÀääÌÑÉ…¬™É½´Ñ¡”¹½ÉÑ …Ñ”‘½İ¸Ñ¼Ñ¡”İ…Ñ•È¸((ŒŒŒ,äƒŠP9…Ù¥…Ñ¥½¸…¹Í•ÑÑ¥¹ÌU$ƒ
Ü€¨©=9€ÈÀÈØ´Àà´ÄÌ¨¨(¡„¤€¨¨‰¼Ñ¼ˆÑ…ˆ¨¨ƒŠP‰Õ¥±‘¥¹Ì…¹ÍÑÉ••Ğ¥¹Ñ•ÉÍ•Ñ¥½¹Ì°=U59Q•¹ÑÉ¥•Ì½¹±ä™½È¹½Ü(¡¥¹™•ÉÉ•±½…Ñ¥½¹Ì©½¥¸±…Ñ•È½¹”,Ä±…¹‘Ì¤ì¥ĞÉ•Á±…•ÌÑ¡”½Ù•É±…ÁÁ¥¹œY¥•İÁ½¥¹ÑÌ±¥ÍĞ…¹)Í¥ÑÌ…Ì¥ÑÌ½İ¸Ñ…ˆ…™Ñ•È½¹ÑÉ½±Ì¸€¡ˆ¤Q¡”Á…¹•°½Á•¹•È‰•½µ•Ì„€¨©¡…µ‰ÕÉ•Èµ•¹Ô¨¨€¡¥Ğ¥Ì)µ½É”Ñ¡…¸Í•ÑÑ¥¹Ì¤ìÉ•…ÍÍ•ÍÌÑ¡”€ˆüˆ¥½¸¸5½‰¥±”€ÌäÃ\ÜàÀ…Ñ”ìÍµ½­”Ñ•ÍÑÌÕÁ‘…Ñ•İ¥Ñ Ñ¡”)U$°¹•Ù•Èİ•…­•¹•¸((¨©M¡¥ÁÁ•¨¨è½¹”±¥ÍĞƒŠP€à…ÕÑ¡½É•Ù¥•İÁ½¥¹ÑÌ°€ĞÙ•É¥™¥•©Õ¹Ñ¥½¹Ì…¹…±°€ÈÈÈ±½…‘•)ÍÑÉÕÑÕÉ•ÌƒŠP¥¸„½Ñ½€Ñ…ˆÍ•½¹¥¸Ñ¡”ÍÑÉ¥À°½Á•¹•‰ä€ñ­‰ùğ½­‰ø€¡İ¡¥ ™½ÕÍ•ÌÑ¡”)Í•…É ½¸„­•å‰½…É…¹‘•±¥‰•É…Ñ•±ä‘½•Ì¹½Ğ½¸„Á¡½¹”°İ¡•É”¥Ğİ½Õ±É…¥Í”Ñ¡”½¸µÍÉ••¸)­•å‰½…É½Ù•ÈÑ¡”±¥ÍĞ¤¸Q¡”M•ÑÑ¥¹Ì½Á¥•Ì…É”½¹”èÑ¡”Ù¥•İÁ½¥¹Ğ¡¥ÁÌ…¹Ñ¡”‘ÕÁ±¥…Ñ”)Í•…É …É”‰½Ñ É•Ñ¥É•Ñ¼¥Ğ¸€‰Ñ¸µ¡•±Á€¥Ì„¡…µ‰ÕÉ•Èİ¥Ñ …É¥„µ±…‰•°ô‰5•¹Ô‰€¸((¨©Q¡”½¹”‘•Á…ÉÑÕÉ”™É½´Ñ¡”Á…É•°…ÌİÉ¥ÑÑ•¸°…¹İ¡ä¸¨¨%Ğ‘½•Ì9=P±¥ÍĞ‘½Õµ•¹Ñ••¹ÑÉ¥•Ì)½¹±ä¸,Ä¡…Ì±…¹‘•Í¥¹”Ñ¡¥Ìİ…ÌİÉ¥ÑÑ•¸°…¹Ñ¡”¡½¹•ÍĞÉ•…‘¥¹œ½˜€‰¥¹™•ÉÉ•±½…Ñ¥½¹Ì©½¥¸)±…Ñ•Èˆ¥Ì¹½ÜÑ¡”Í•½¹½¹”è€¨©¹¼ÍÑÉÕÑÕÉ”Á½Í¥Ñ¥½¸¥¸Ñ¡¥Ì‘…Ñ…Í•Ğ¥Ì‘½Õµ•¹Ñ•‘€¨¨ƒŠP€ÔĞ…É”)¥¹™•ÉÉ•‘€…¹€ÄØà½¹©•ÑÕÉ…±€ƒŠPÍ¼„‘½Õµ•¹Ñ•µ½¹±äµ•¹Ôİ½Õ±¡…Ù”¡•±™½ÕÈ©Õ¹Ñ¥½¹Ì…¹)¹½Ñ¡¥¹œ•±Í”¸Ù•ÉäÍÑÉÕÑÕÉ”¥¹ÍÑ•……ÉÉ¥•Ì¥ÑÌ½İ¸Á±…•µ•¹Ğ¹Á½Í¥Ñ¥½¹}½¹™¥‘•¹•€…Ì„¡¥À°)¥¸Ñ¡”Á½ÁÕÀÌÑ¡É•”İ½É‘Ì…¹Ñ¡É•”½±½ÕÉÌ°…¹Ñ¡”…Ñ”½µÁ…É•Ì•Ù•Éä¡¥À……¥¹ÍĞÑ¡”)É•½É¥Ğ©ÕµÁÌÑ¼¸Y¥•İÁ½¥¹ÑÌ…¹©Õ¹Ñ¥½¹Ì…ÉÉä¹½¹”è¹•¥Ñ¡•È¥Ì„±…¥´…‰½ÕĞÑ¡”Ñ½İ¸¸((¨©]¡…Ğ¥Ğ¥¹¡•É¥ÑÌ¸¨¨€¡„¤Q¡”Ñ…±±ä¥¸Ñ¡”Ñ…ˆ¥Ì½Õ¹Ñ•™É½´Ñ¡”±¥ÍĞ°Í¼¥Ğµ½Ù•Ìİ¡•¸Ñ¡”)‘…Ñ…Í•Ğ‘½•ÌƒŠP¹½Ñ¡¥¹œÑ¼É•ÍÑ…Ñ”¡•É”İ¡•¸„Á½Í¥Ñ¥½¸¥ÌÉ•É…‘•¸€¡ˆ¤¥Ù”Ñ…‰Ì™¥Ğİ¥Ñ …‰½ÕĞ(ÈÀÁà½˜Í±…¬…Ğ‰½Ñ Ù¥•İÁ½ÉÑÌ€¡‘•Í­Ñ½ÀÁ…¹•°İ¥‘•¹•€ÌØÀƒŠH€ÌàÀÁà°Ñ…ˆÁ…‘‘¥¹œ€äƒŠH€ØÁà°)µ½‰¥±”ÑåÁ”€ÄÈ¸ÔƒŠH€ÄÄ¸ÔÁà¤ì„€¨©Í¥áÑ Ñ…ˆ‘½•Ì¹½Ğ™¥Ğ¨¨…¹Ñ¡”…Ñ”İ¥±°Í…äÍ¼É…Ñ¡•ÈÑ¡…¸)Í¡¥ÁÁ¥¹œ„Ñİ¼µÉ½ÜÍÑÉ¥À¸€¡Œ¤Q¡”…Ñ”Ì½İ¸‘•Í­Ñ½À¡…±˜¡…¹½Ğ‰••¸ÉÕ¹¹¥¹œèÍ•”ƒ
œÑ¡”Íµ½­”)‰Õ‘•Ğ¥¸MQQUL¸((ŒŒŒ,ÄÀƒŠP	É¥‘”…ÁÁÉ½…¡•Ì(‰!½Üİ½Õ±„İ…½¸É½ÍÌÑ¡…ĞüˆÙ•Éä‰É¥‘”ÕÉÉ•¹Ñ±ä™±½…ÑÌ½Ù•È¥ÑÌ‰…¹­Ì(¡…ÁÁÉ½…¡}¹½Ñ}µ½‘•±±•‘€¤¸	Õ¥±…‰ÕÑµ•¹Ğ•…ÉÑ¡İ½É­Ì½É…µÁÌÑ¡…Ğµ••ĞÑ¡”‘•¬…ĞÉ…‘”½¸‰½Ñ )•¹‘ÌƒŠP•Ù¥‘•¹”èÑ¡”€ÄààÌÍ•ÑÑ±•ÉÌœÍÑ…Ñ•µ•¹Ğ€¡±½œ…‰ÕÑµ•¹ÑÌ%8Ñ¡”Í¡…±±½Üİ…Ñ•È¹•…ÈÑ¡”)‰…¹­Ì¤°‘•¬¡•¥¡ÑÌ…±É•…‘ä‘½Õµ•¹Ñ•¸]…±­…‰±”•¹Ñ¼•¹°İ…½¸µÁ±…ÕÍ¥‰±”É…‘¥•¹ÑÌì)É•É…‘”É½Õ¹‘}½¹Ñ…Ñ€…Ì•… ‰É¥‘”…ÑÕ…±±ä±…¹‘Ììµ½Ù”Ñ¡”É•±•Ù…¹Ğ±¥‰•ÉÑäÑ•áĞ¸((ŒŒŒ,ÄÄƒŠPQÉ••ÌÍÑ…¹‘¥¹œ¥¸Ñ¡”É¥Ù•Èƒ
Ü€¨©=9€ÈÀÈØ´Àà´ÄÌ¨¨)Q¡”É¥Ù•Èµ…Í¬€¡¥Í]…Ñ•É€¤‰•¥¹Ì€ÄÀÀµ´	1=\Ñ¡”İ…Ñ•ÈÁ±…¹”°Í¼„ÍÑ•´½Õ±É½½Ğ¥¸Ñ¡…Ğ)‰…¹°Á…ÍÌÑ¡”µ…Í¬…¹É•¹‘•ÈÍÑ…¹‘¥¹œ¥¸½Á•¸İ…Ñ•ÈƒŠP€ÌØ½˜€ØÄàÍÑ…Ñ¥½¹Ìİ•É”‘½¥¹œ¥Ğ¸)ÑÉ••Ì¹©Í€¹½ÜÉ•ÅÕ¥É•Ì•Ù•ÉäÑÉ•”…¹Ñ¡¥­•ĞÑ¼ÍÑ…¹QI}Ie}5I%9}5€€ô€À¸ÈÀ´±•…È½˜)Ñ¡”•Á½ Ì½İ¸İ…Ñ•É}ÍÕÉ™…•}µ€€ À¸ÄÔ´½˜ÍÕ¹¬‰½±”€¬Ñ¡”€À¸ÀÌ´É½Õ¹µµ•Í Ñ½±•É…¹”°)Á±ÕÌ€ÈÀµ´¤¸€ÄäÜ…¹‘¥‘…Ñ•ÌÉ•©•Ñ•ì±½İ•ÍĞÍÕÉÙ¥Ù¥¹œÍÑ…Ñ¥½¸€¬À¸ÈÀÄ´¸9•ÜÍµ½­”…ÍÍ•ÉÑ¥½¸(¨¨‰¹¼ÑÉ•”ÍÑ…¹‘Ì‰•±½ÜÑ¡”İ…Ñ•É±¥¹”ˆ¨¨°…±½¹Í¥‘”ƒŠP¹½ĞÉ•Á±…¥¹œƒŠPÑ¡”É¥Ù•Èµµ…Í¬¡•¬¸(((ŒŒŒ,ÄÈƒŠP1½½À¡å¥•¹”€¨¡ÍÑ…¹‘¥¹œ¥¹ÍÑÉÕÑ¥½¸Ñ¼•Ù•ÉäÍÑ•İ…ÉÉÕ¸¤¨)Ù•ÉäÉÕ¸Ñ¡…Ğ…‘‘Ì…¹åÑ¡¥¹œÕÍ•ÈµÙ¥Í¥‰±”İÉ¥Ñ•Ì¥ÑÌ¡…¹•±½œ•¹ÑÉä€¡Øè¹Õ±°°ÑÌè€œœ¤%8Q!)M5IU8ƒŠPÑ¡”½Ù•É¹¥¡ĞÁÕÍ ½˜€ÈÀÈØ´Àà´ÄÄ±…¹‘•øÔÀ‰Õ¥±‘¥¹Ìİ¥Ñ ¹¼¡…¹•±½œ•¹ÑÉä…¹)Ñ¡”½İ¹•È¹½Ñ¥•‰•™½É”İ”‘¥¸AÕ‰±¥Í €¡Ñ½½±Ì½ÁÕ‰±¥Í ¹Í¡€¤…¹µ•É”Ñ¼µ…¥¸Í¼Ñ¡”‘•Á±½ä)…ÑÕ…±±äÍ¡¥ÁÌìµ…¥¸¥ÌÑ¡”½¹±ä‰É…¹ A…•ÌÁÕ‰±¥Í¡•Ì¸((¨¨ÈÀÈØ´Àà´ÄÌƒŠPÑ¡”¡…¹•±½œİ…Ì½ÉÉÕÁÑ•‰ä„5I°…¹Ñ¡”…Ñ”¹½ÜÉÕ¹Ì¥¸¡•¬¹Í¡€¸¨¨)µ…¥¹€…ÉÉ¥•„É•¹‘•É•ÉÌ½İ•ˆ½©Ì½¡…¹•±½œ¹©Í€Ñ¡…Ğ‘¥¹½ĞÁ…ÉÍ”°…¹¡…‘½¹”Í¥¹”µ•É”)€ØÕŒá‘”Å€¸=¹”µ¥ÍÍ¥¹œtô±€Íİ…±±½İ•€ØĞ•¹ÑÉ¥•Ì¥¹Ñ¼½¹”ì„‘ÕÁ±¥…Ñ”Øè€ØÑ€É½‘”…±½¹œ¸Q¡”)]¡…ĞÌµ¹•ÜÑ…ˆİ…Ì‘•…½¸Ñ¡”±¥Ù”Í¥Ñ”…¹Ñ¡¥ÌÁÉ½©•ĞÉ•Á½ÉÑ•¹¼É•±•…Í•ÌÑ¼5…¹…•È½ÈÑ¡”)±…Õ¹¡•È¸€¨©	½Ñ Á…É•¹ÑÌ½˜Ñ¡…Ğµ•É”Á…ÉÍ”ìÑ¡”µ•É”‘½•Ì¹½Ğ¨¨ƒŠP€¹¥Ñ…ÑÑÉ¥‰ÕÑ•Í€µ•É•ÌÑ¡¥Ì)™¥±”µ•É”õÕ¹¥½¹€°…¹Ñ¡”Õ¹¥½¸‘É¥Ù•ÈÉÕ¹Ì‘ÕÉ¥¹œÑ¡”µ•É”°Í¼„É••¸AH…¸ÍÑ¥±°ÁÉ½‘Õ”„)É•µ…¥¹€¸I•Á…¥É•°…¹Ñ½½±Ì½¡•¬¹Í¡€¹½ÜÉÕ¹ÌÑ½½±Ì½¡•¬µ¡…¹•±½œ¹µ©Í€…Ì„ÍÑ•À(¡ÁÉ•Ù¥½ÕÍ±ä„¡…¹µÉÕ¸¥¹ÍÑÉÕÑ¥½¸¥¸9QL¹µ°İ¡¥ ¥ÌÁÉ•¥Í•±äİ¡…Ğ„µ•É”µÑ¥µ”½ÉÉÕÁÑ¥½¸)•Ù…‘•Ì¤¸Q¡”½¹ÑÉ…Ğ¡•¬¹½ÜÉ•…‘ÌÑ¡”±¥Ñ•É…°ÌÍ¡…Á”…ÌQaP‰•™½É”•á•ÕÑ¥¹œ¥Ğ°…¹¹…µ•Ì)Ñ¡”•¹ÑÉäÑ¡…Ğ±½ÍĞ¥ÑÌÑ•Éµ¥¹…Ñ½È…¹Ñ¡”•¹ÑÉäÑ¡…Ğ½ĞÍİ…±±½İ•¸•Ñ…¥°¥¸MQQUL¸((¨©]¡…Ğ¥ÌÍÑ¥±°½Á•¸°…¹¥Ğ¥Ì¹½ĞÑ¡¥ÌÁ…É•°ÌÑ¼™¥à¸¨¨9½Ñ¡¥¹œÉÕ¹Ì½¸„µ•É”½µµ¥Ğ)¥ÑÍ•±˜¸Q¡”É•Á½Í¥Ñ½ÉäÌ$±¥Ù•Ì½ÕÑÍ¥‘”¡¥…¼¼Ñ‘€…¹½ÕÑÍ¥‘”Ñ¡¥Ì±…¹”ÌÍ½Á”°Í¼„µ•É”)Á•É™½Éµ•½¸¥Ñ!Õˆ…¸ÍÑ¥±°ÁÕ‰±¥Í „Õ¹¥½¸µ½ÉÉÕÁÑ•¡…¹•±½œİ¥Ñ ¹¼…Ñ”‰•Ñİ••¸¥Ğ…¹)A…•Ì¸Qİ¼…¹‘¥‘…Ñ”™¥á•Ì°‰½Ñ ¹••‘¥¹œ„‘•¥Í¥½¸É…Ñ¡•ÈÑ¡…¸„Í±¥”èÉÕ¸Ñ¡”ÍÕ‰ÑÉ•”Ì…Ñ”)™É½´Ñ¡”É•Á¼Ì½İ¸İ½É­™±½Ü½¸ÁÕÍ¡•ÌÑ¼µ…¥¹€°½ÈÉ•Á±…”µ•É”õÕ¹¥½¹€½¸Ñ¡¥ÌÁ…Ñ İ¥Ñ „)µ•É”‘É¥Ù•ÈÑ¡…ĞÕ¹‘•ÉÍÑ…¹‘ÌÑ¡”±¥Ñ•É…°¸€¨©Q¡”ÍÑ…¹‘¥¹œ¥¹ÍÑÉÕÑ¥½¸Õ¹Ñ¥°Ñ¡•¸è…¹ä…•¹ĞÑ¡…Ğ)Á•É™½ÉµÌ„µ•É”…™™•Ñ¥¹œ¡…¹•±½œ¹©Í€É”µÉÕ¹ÌÑ½½±Ì½¡•¬µ¡…¹•±½œ¹µ©Í€QHÑ¡”µ•É”°)¹½Ğ½¹±ä‰•™½É”¥Ğ¸¨¨(((ŒŒŒ,ÄÌƒŠPQ¡”1„M…±±”MÑÉ••ĞÉ”µ•¹ÑÉ…¹Ğ°…¹Ñ¡”½Ñ¡•È5…¥¸	É…¹ Í±½Õ¡Ì)]É¥¡Ğ‘É…İÌ„¹…ÉÉ½Üİ…Ñ•É½ÕÉÍ”‘É½ÁÁ¥¹œÍ½ÕÑ ½™˜Ñ¡”µ…¥¸ÍÑ•´‰•Ñİ••¸Á±…Ğ‰±½­Ì€Ää…¹(Äà°…Ğ±½…°€¬ĞØÈƒŠ˜€¬ĞØäƒŠP1„M…±±”MÑÉ••Ğ¸Q¡”İ…Ñ•É±¥¹”ÑÉ…”…ÉÉ¥•Ì¥ÑÌµ½ÕÑ €¡Ñ¡…Ğ¥Ì)…Ì™…È…Ì]É¥¡Ğİ…Í¡•Ì¥Ğ¤…¹¹½Ñ¡¥¹œ‰•å½¹¸Q¡”‘½ÍÍ¥•ÈÉ•½É‘ÌÑ¡…ĞÑ¡”€ÄàÌÀQ¡½µÁÍ½¸)Á±…ĞÍ¡½İÌ€¨©Ñ¡É•”Í±½Õ¡Ì½™˜Ñ¡”5…¥¸	É…¹ ¨¨°…¹I=5@ƒ
œLÉ”µ…­•Ì½¹±•ä½MÑ•±é•È€ÄàÌÌ)Ñ¡”ÁÉ¥µ…ÉäÕ¥‘”™½Èİ¡•É”Ñ¡”ÍÑÉ•…µÌ½µ”¥¸…¹İ¡•É”Ñ¡•äÑ•Éµ¥¹…Ñ”¸A…É•°è¥‘•¹Ñ¥™ä)Ñ¡”Ñ¡É•”°…¹…ÉÉäÑ¡”½¹•ÌÑ¡…Ğ…É”…ÑÑ•ÍÑ•…Ì¡å‘É½±½ä¹•½©Í½¹€9QI1%9L¥¸Ñ¡”)™½É´Ñ¡”¹½ÉÑ µÍ¥‘”Í±½Õ …±É•…‘äÑ…­•ÌƒŠP¹•Ù•È…ÌÑÉ…•‰½Õ¹‘…É¥•Ì°‰•…ÕÍ”Ñ¡”‰…¹¬İ…Í )¥Ì¹½ĞÑ¡•É”Ñ¼ÑÉ…”¸É½ÍÌµ¡•¬Ñ¡”MÑ…Ñ”MÑÉ••ĞÍ±½Õ µ½ÕÑ Ñ¡”ÑÉ…”…±É•…‘ä…ÉÉ¥•Ì…Ğ)€¬àÔÀƒŠ˜€¬àÔØ……¥¹ÍĞ‘½ÍÍ¥•Èé½¹”€ÄĞ¸((ŒŒŒ,ÄĞƒŠPQ¡”Ñ•ÉÉ…¥¸‘•¥µ…Ñ½ËŠeÌÑ½±•É…¹”±¥™˜ƒ
Ü€¨©=9€ÈÀÈØ´Àà´ÄÌ¨¨)•¹•É…Ñ½ÉÌ½Ñ•ÉÉ…¥¹}•¸¹Áä€´µ‘•¥µ…Ñ”µ‘•€‰•¡…Ù•Ì…Ì„±¥™˜°¹½Ğ„‘¥…°°……¥¹ÍĞ)5M!}%Q}Q=1I9}5€è…™Ñ•ÈÑ¡”,Ø½ÉÉ•Ñ¥½¸°€À¸ÀĞÀ…¹€À¸ÀÌà‰½Ñ ±…¹…Ğ€ÌÀµ´…¹…É”)É•™ÕÍ•°İ¡¥±”€À¸ÀÌÀ±…¹‘Ì…Ğ€Ì¸Äµ´ƒŠP…¹½ÍÑÌ€ÈĞÜ€ÔÈÜÑÉ¥…¹±•Ì€¼€Ø¸Ğ5……¥¹ÍĞÑ¡”)ÁÉ•Ù¥½ÕÌ€ÄÌÔ€ÈĞä€¼€Ì¸Ô5¸Q¡”1¹½Ü½µµ¥ÑÑ•¥ÌÑ¡”€À¸ÀÌÀ½¹”¸]½ÉÑ „±½½¬…Ğİ¡•Ñ¡•È)Ñ¡”Á±…¹…È‘•¥µ…Ñ”¥ÌÑ¡”É¥¡Ğ½Á•É…Ñ½È¡•É”°½Èİ¡•Ñ¡•ÈÑ¡”™¥ĞÍ¡½Õ±‰”•¹™½É•‰ä„)ÅÕ…‘É¥Œµ•ÉÉ½È‰Õ‘•Ğ¥¹ÍÑ•…½˜„‘¥¡•‘É…°…¹±”ìÑ¡”Á…å±½…¥Ì¥¹Í¥‘”Ñ¡”€ÈÔ5‰Õ‘•Ğ(¡Ñ½½±Ì½ÁÕ‰±¥Í ¹Í¡€É•Á½ÉÑÌ€Ää¸ÄØ5¤‰ÕĞÑ¡”É½Õ¹¥Ì¹½ÜÑ¡”±…É•ÍĞÍ¥¹±”…ÍÍ•Ğ‰ä„)İ¥‘”µ…É¥¸¸€¨©Q¡”É•¹‘•É•µÑÉ¥…¹±”‰Õ‘•Ğ¥ÌÑ¡”Ñ¥¡Ñ•È½¹ÍÑÉ…¥¹Ğ¨¨èÑ¡”Íµ½­”µ•…ÍÕÉ•Ì(¨¨ÔØĞ€ØàÄÑÉ¥Ì…Ğ€ÄÈàÃ\àÀÀ……¥¹ÍĞ„€ØÀÀ€ÀÀÀ‰Õ‘•Ğ¨¨ƒŠP€Ø€”½˜¡•…‘É½½´°İ¡•É”‰•™½É”Ñ¡¥Ì)¡…¹”Ñ¡•É”İ…ÌÉ½Õ¡±ä€ÈÔ€”¸Q¡”Ñ•ÉÉ…¥¸¥Ì™ÉÕÍÑÕµÕ±±•€ô™…±Í•€°Í¼…±°€ÈĞÜ€ÔÈÜ½˜¥ÑÌ)ÑÉ¥…¹±•Ì…É”¥¸•Ù•Éä™É…µ”¸Q¡”¹•áĞÁ…É•°Ñ¡…Ğ…‘‘Ì•½µ•ÑÉäİ¥±°¡¥ĞÑ¡¥Ì•¥±¥¹œ)‰•™½É”¥Ğ¡¥ÑÌÑ¡”Á…å±½…½¹”¸((¨©IM=1Y€ÈÀÈØ´Àà´ÄÌ°…¹¹½Ğİ¡•É”Ñ¡¥Ì¥Ñ•´İ…Ì±½½­¥¹œ¸¨¨Q¡”‘•¥µ…Ñ½Èİ…Ì¹•Ù•ÈÑ¡”)ÁÉ½‰±•´İ½ÉÑ Í½±Ù¥¹œèÑ¡”É½Õ¹İ…Ì=9µ•Í İ¥Ñ ™ÉÕÍÑÕµÕ±±•€ô™…±Í•€°Í¼¥ÑÌİ¡½±”(ÈĞÜ€ÔÈÜÑÉ¥…¹±•Ìİ•É”‘É…İ¸•Ù•Éä™É…µ”¹¼µ…ÑÑ•Èİ¡¥ İ…äÑ¡”İ…±­•È™…•¸ÕĞ¥¹Ñ¼„(¨¨ÄÈƒ\€ÌÉ¥‰äÑÉ¥…¹±”•¹ÑÉ½¥¨¨€¡É•¹‘•É•ÉÌ½İ•ˆ½©Ì½Ñ•ÉÉ…¥¸¹©ÌÑ¥±•É½Õ¹ ¥€¤°•… Ñ¥±”)…ÉÉ¥•Ì¥ÑÌ½İ¸‰½Õ¹‘¥¹œÍÁ¡•É”…¹Ñ¡”½¹•Ì‰•¡¥¹å½Ô…É”Í­¥ÁÁ•¸•Í­Ñ½Àİ•¹Ğ€¨¨ÔÔÀ€ÔÄÌƒŠH(ĞØÄ€ÄÄÈÑÉ¥…¹±•Ì¨¨…Ğ€ÜÄ½˜€àÀ‘É…Ü…±±Ìì¡•…‘É½½´¥Ì¹½Ü€¨¨ÄÌà€ààà¨¨İ¡•É”¥Ğİ…Ì€Ğä€ĞàÜ¸)É¥Á¥­•‰äµ•…ÍÕÉ•µ•¹ĞƒŠP€ã\Ğ¥Ù•ÌÑ¡”Í…µ”‘É…Ü…±±Ì™½È€ÈÜ€ÀÀÀ5=IÑÉ¥…¹±•Ì°€ÄË\Ø)Í…Ù•Ì…¹½Ñ¡•È€ÈØ€ÀÀÀ‰ÕĞ±•…Ù•Ì=9‘É…Ü…±°ÍÁ…É”°İ¡¥ ¥Ì¹½Ğ¡•…‘É½½´¸(¨©Qİ¼Ñ¡¥¹ÌÍÑ¥±°½¸Ñ¡”Ñ…‰±”¨¨°¹•¥Ñ¡•ÈÑ…­•¸è€¡„¤€ÄË\Ø½È™¥¹•È°¥˜Ñ¡”‘É…Üµ…±°‰Õ‘•Ğ¥Ì)•Ù•È‘•±¥‰•É…Ñ•±äÉ•Ù¥Í¥Ñ•ƒŠPÑ¡”Ñ•ÉÉ…¥¸Ñ¥±•Ì…É”¡•…À…±±ÌÍ¡…É¥¹œ½¹”µ…Ñ•É¥…°°‰ÕĞÑ¡”)‰Õ‘•Ğ¥Ì„…Ñ”…¹µ½Ù¥¹œ¥Ğ¥Ì„‘•¥Í¥½¸°¹½Ğ„Í¥‘”•™™•Ğì€¡ˆ¤Ñ¡”‘•¥µ…Ñ½ÈÅÕ•ÍÑ¥½¸…Ì)½É¥¥¹…±±äİÉ¥ÑÑ•¸°İ¡¥ ¥Ì¹½Ü…‰½ÕĞAe1=É…Ñ¡•ÈÑ¡…¸™É…µ”½ÍĞ…¹¥ÌµÕ ±•ÍÌÕÉ•¹Ğ)Í¥¹”Ñ¡”ÁÕ‰±¥Í¡•ÑÉ•”™•±°Ñ¼€ÄÀ¸Üà5€¡Í•”Ñ¡”µ•Í¡½ÁĞ™¥à½˜Ñ¡”Í…µ”‘…ä¤¸(¨©Q¡”Á…å±½…™¥ÕÉ”ÅÕ½Ñ•…‰½Ù”¥ÌÍÑ…±”¨¨ƒŠP€Ää¸ÄØ5İ…Ìµ•…ÍÕÉ•İ¡•¸Ñ¡”…¹½¹åµ½ÕÌÉ½½™Ì)İ•É”Á±…•¡½±‘•Èµ…ÍÍ¥¹œ…¹•Ù•Éäİ•ˆ‘•É¥Ù…Ñ¥Ù”İ…Ì…¸Õ¹½µÁÉ•ÍÍ•½Áä½˜¥ÑÌµ…ÍÑ•È¸(ŒŒŒ,ÄàƒŠPQ¡”¥¹Ù•¹Ñ•É•Í¥‘•¹ÑÌ¡…Ù”¹…µ•Ìƒ
Ü€¨©=9€ÈÀÈØ´Àà´ÄĞ¨¨()Ù•ÉäÉ•½¹ÍÑÉÕÑ•É•Í¥‘•¹ĞÕÍ•Ñ¼É•…€‰‰…­•È€¡¥¹™•ÉÉ•É•Í¥‘•¹Ğ°Õ¹¹…µ•¤ˆ°…¹Ñ¡”É•½É)…ÉÕ•™½È¥Ğè…¸¥¹Ù•¹Ñ•ÍÕÉ¹…µ”İ½Õ±µ…­”Ñ¡”•¹ÑÉä¥¹‘¥ÍÑ¥¹Õ¥Í¡…‰±”…Ğ„±…¹”™É½´Ñ¡”)‘½Õµ•¹Ñ•±…å•È‰•Í¥‘”¥Ğ¸Q¡…Ğ¥ÌÍ½Õ¹…‰½ÕĞÑ¡”Q…¹İÉ½¹œ…‰½ÕĞÑ¡”Q=]8ƒŠP„Á±…”)İ¡•É”µ½ÍĞ¡½ÕÍ•¡½±‘Ì…É”…±±•€‰…¸¥¹™•ÉÉ•½½Á•ÈÌ¡½ÕÍ•¡½±ˆÉ•…‘Ì…Ì„ÍÁÉ•…‘Í¡••Ğ°¹½Ğ„)Ñ½İ¸¸Q¡”½İ¹•È…Í­•™½È¹…µ•Ì¸((¨©]¡…Ğ‰½Õ¹‘ÌÑ¡”¥¹Ù•¹Ñ¥½¸¸¨¨Q¡”Á½½±Ì¥¸‘…Ñ„½É•½¹ÍÑÉÕÑ¥½¸¼ÄàÌÕ}¥¹Ù•¹Ñ•‘}¹…µ•}Á½½±Ì¹©Í½¹€)…É”Í••‘•™É½´Ñ¡”€¨¨ÜØQQMQÉ•Í¥‘•¹ÑÌÑ¡¥ÌÁÉ½©•Ğ…±É•…‘ä¡½±‘Ì¨¨ƒŠPÉ•…°Á•½Á±”°¹…µ•)™É½´¥Ñ•Í½ÕÉ•ÌƒŠPÍ¼…¸¥¹Ù•¹Ñ•½½Á•È¥Ì¹…µ•Ñ¡”İ…äÑ¡¥ÌÑ½İ¸ÌÉ•…°½½Á•ÉÌİ•É”¹…µ•)É…Ñ¡•ÈÑ¡…¸Ñ¡”İ…ä„¹½Ù•°İ½Õ±¹…µ”½¹”¸Q¡É•”½µµÕ¹¥Ñ¥•Ì°•… İ¥Ñ Ñ¡”•Ù¥‘•¹”Ñ¡…ĞÁÕÑÌ)¥Ğ¡•É”è9•Ü¹±…¹…¹9•Üe½É¬€¡Ñ¡”‘½Õµ•¹Ñ•½É¥¥¹ÌÉÕ¸Y•Éµ½¹Ğ°½¹¹•Ñ¥ÕĞ°9•Üe½É¬¤°)É•¹ ½±½¹¥…°…¹µ•Ñ¥Ì½˜Ñ¡”•ÑÉ½¥Ğ…¹5¥±İ…Õ­•”½Õ¹ÑÉä€¡	•…Õ‰¥•¸…ÁÁ•…ÉÌÑ¡É•”Ñ¥µ•Ì)…µ½¹œÑ¡”¹…µ•É•Í¥‘•¹ÑÌ¤°…¹%É¥Í €¡½¹”…ÑÑ•ÍÑ•½É¥¥¸¥¸½Õ¹Ñä-•ÉÉäì…¸…¹…Í•ä¤¸((¨©]¡•É”„İ•¥¡Ñ¥¹œ¥Ì¥ÑÍ•±˜„Õ•ÍÌ°¥ĞÍ…åÌÍ¼¸¨¨	½…Ñµ•¸‘É…ÜÉ•¹ ½±½¹¥…°=8Y%9ƒŠP)Ñ¡”…ÉÉå¥¹œÑÉ…‘”½˜Ñ¡¥ÌÉ¥Ù•Èİ…Ìİ½É­•‰äÑ¡…Ğ½µµÕ¹¥Ñä¸1…‰½ÕÉ•ÉÌ‘É…ÜY91d°…¹Ñ¡”)¹½Ñ”•áÁ±…¥¹Ìİ¡äèÑ¡”%É¥Í ±…‰½ÕÉ¥¹œ¡¥…¼½˜Á½ÁÕ±…Èµ•µ½Éä…ÉÉ¥Ù•Ìİ¥Ñ Ñ¡”…¹…°)½¹ÑÉ…ÑÌ½˜€¨¨ÄàÌØ¨¨°…™Ñ•ÈÑ¡¥ÌÍ•¹”°Í¼İ•¥¡Ñ¥¹œ€ÄàÌÔ±…‰½ÕÉ•ÉÌ%É¥Í İ½Õ±‰”¥µÁ½ÉÑ¥¹œ„)±…Ñ•È‘•…‘”¥¹Ñ¼Ñ¡¥Ì½¹”¸((¨©]¡…ĞÍÑ½ÁÌ¥Ğ‰•½µ¥¹œ„±…Õ¹‘•É¥¹œÉ½ÕÑ”¸¨¨¹…µ”±½½­Ì±¥­”„™…Ğ¥¸„İ…ä€‰İ…±°¡•¥¡Ğ(Ì¸ÈÔ´ˆ‘½•Ì¹½Ğ°İ¡¥ µ…­•Ì¥ĞÑ¡”•…Í¥•ÍĞİ…ä™½È…¸¥¹Ù•¹Ñ¥½¸Ñ¼‰”µ¥ÍÑ…­•¸™½È„™¥¹‘¥¹œ¸)M¼è•Ù•ÉäÉ•½¹ÍÑÉÕÑ•Á•ÉÍ½¸…ÉÉ¥•Ì„¹…µ•}‰…Í¥Í€‰±½¬°É…‘•É•½¹ÍÑÉÕÑ•‘€°İ¡½Í”¹½Ñ”)½Á•¹Ì€‰Q!95%L%9Y9QˆìÙ…±¥‘…Ñ”¹Áå€€¨©•ÉÉ½ÉÌ¨¨¥˜„É•½¹ÍÑÉÕÑ•Á•ÉÍ½¸±…­Ì½¹”°¥˜)¥ÑÌÉ…‘”¥Ì…¹åÑ¡¥¹œ‰•ÑÑ•È°½È¥˜…¸…ÑÑ•ÍÑ•Á•ÉÍ½¸…ÉÉ¥•Ì½¹”…Ğ…±°€¡Ñ¡•¥È¹…µ”½µ•Ì™É½´)„Í½ÕÉ”…¹µ…É­¥¹œ¥Ğ¥¹Ù•¹Ñ•İ½Õ±Õ¹‘•ÉÍÑ…Ñ”İ¡…Ğ¥Ì­¹½İ¸…‰½ÕĞ„É•…°Á•ÉÍ½¸¤¸Q¡É•”)Í•±˜µÑ•ÍÑÌ¡½±…±°Ñ¡É•”‘¥É•Ñ¥½¹Ì¸ÍÍ¥¹µ•¹Ğ¥Ì‘•Ñ•Éµ¥¹¥ÍÑ¥Œ™É½´Ñ¡”Á•ÉÍ½¸Ì¥…¹)¡•¬¹Í¡€É”µ‘•É¥Ù•Ì¥Ğ°Í¼„¹…µ”Ñ¡…Ğµ½Ù•İ¥Ñ¡½ÕĞÑ¡”Á½½±Ìµ½Ù¥¹œ¥Ì„™¥¹‘¥¹œ¸()9…µ•Ì…É”€¨©‘•…±Ğ¨¨É½Õ¹•… Á½½°É…Ñ¡•ÈÑ¡…¸‘É…İ¸¥¹‘•Á•¹‘•¹Ñ±äè¥¹‘•Á•¹‘•¹Ğ‘É…İÌÁÕĞ™½ÕÈ)Õ¹É•±…Ñ•¡½ÕÍ•¡½±‘ÌÕ¹‘•È€‰1åµ…¸ˆ…¹™½ÕÈÕ¹‘•È€‰¥±‰•ÉĞˆ°…¹„Í¡…É•ÍÕÉ¹…µ”É•…‘Ì…Ì)­¥¹Í¡¥ÀÑ¡¥Ì±…å•È±…¥µÌ¹½Ñ¡¥¹œ…‰½ÕĞ¸€ØÄ‘¥ÍÑ¥¹ĞÍÕÉ¹…µ•Ì…É½ÍÌ€äÈÁ•½Á±”¸((ŒŒŒ,ÄÜƒŠP!¥‘¥¹œ„±•Ù•°°™½±‘•¥¹Ñ¼Ñ¡”½¹™¥‘•¹”½¹ÑÉ½°ƒ
Ü€¨©=9€ÈÀÈØ´Àà´ÄĞ¨¨()Q¡”½¹™¥‘•¹”¡¥À½±½ÕÉ•Ñ¡”Ñ½İ¸‰ä•Ù¥‘•¹”¸%Ğ¹½Ü…±Í¼¡…Ì„…É•Ğ°…¹‰•¡¥¹¥ĞÑ¡É•”)¡•­‰½á•Ìè€¨©ÑÑ•ÍÑ•€ÄÄƒ
Ü%¹™•ÉÉ•€Øäƒ
ÜI•½¹ÍÑÉÕÑ•€ÄØÈ¨¨°½Õ¹Ñ•™É½´Ñ¡”±½…‘•É•¥ÍÑÉä)É…Ñ¡•ÈÑ¡…¸İÉ¥ÑÑ•¸‘½İ¸¸QÕÉ¹¥¹œ½¹”½™˜É•µ½Ù•Ì¥Ğ™É½´Ñ¡”Ù¥•Ü½ÕÑÉ¥¡Ğ¸((¨©!¥‘¥¹œ¥Ì‘•±¥‰•É…Ñ•±ä¥¹‘•Á•¹‘•¹Ğ½˜Ñ¡”½±½ÕÉ¥¹œ¸¨¨Q¡•ä…É”Ñİ¼ÅÕ•ÍÑ¥½¹Ì…¹Ñ¡”Í•½¹)¥ÌÑ¡”µ½É”Í•…É¡¥¹œ½¹”è½±½ÕÉ¥¹œ…Í­Ì¡½ÜÍÕÉ”İ”…É”°¡¥‘¥¹œ…Í­Ì€©İ¡…Ğ¥Ì±•™Ğ¥˜å½Ô­••À)½¹±äİ¡…ĞÍ½µ•‰½‘äİÉ½Ñ”‘½İ¸¨¸Qå¥¹œ¥ĞÑ¼Ñ¡”½±½ÕÈµ½‘”İ½Õ±µ•…¸å½Ô½Õ±½¹±ä…Í¬¥Ğ)İ¡¥±”Ñ¡”İ¡½±”Ñ½İ¸İ…Ì…µ‰•È…¹‘¥Ñ¡•É•°…¹Ñ¡”…¹Íİ•ÈÉ•…‘Ì™…È‰•ÑÑ•È¥¸‘…å±¥¡Ğ¸QÕÉ¸)½™˜É•½¹ÍÑÉÕÑ•‘€…¹µ½ÍĞ½˜Ñ¡”Ñ½İ¸Ù…¹¥Í¡•Ì¸Q¡…Ğ¥ÌÑ¡”¡½¹•ÍĞÁ¥ÑÕÉ”½˜¡½ÜµÕ ½˜(ÄàÌÔ¡¥…¼¥ÌÉ•½Ù•É…‰±”°¥Ğ¥Ì¹½Ğ„½µ™½ÉÑ…‰±”Ñ¡¥¹œ™½ÈÑ¡¥ÌÁÉ½©•ĞÑ¼Í¡½Ü°…¹¥Ğ¥Ì)¹½Ü½¹”±¥¬…İ…ä¸()%µÁ±•µ•¹Ñ•…Ì½¹”Õ!¥‘•1•Ù•±€Õ¹¥™½É´‰…¹‘•™É½´Ñ¡”Í…µ”Ñ¡É•Í¡½±‘Ì…Ì±•Ù•±=˜ ¥€°Í¼Ñ¡”)Í¡…‘•È…¹Ñ¡”±…‰•±Ì…¹¹½Ğ‘¥Í…É•”…‰½ÕĞİ¡¥ ±•Ù•°„™É…µ•¹Ğ¥Ì¥¸¸Q¡”¡½¥”Á•ÉÍ¥ÍÑÌ°)¥Ì…ÁÁ±¥•‰•™½É”Ñ¡”™¥ÉÍĞ™É…µ”€¡„É•ÑÕÉ¹¥¹œÙ¥Í¥Ñ½ÈÍ¡½Õ±¹½Ğİ…Ñ Ñ¡”¡¥‘‘•¸Ñ½İ¸™±…Í )¥¸¤°…¹Ñ¡”…É•Ğ…ÉÉ¥•Ì„‘½Ğİ¡¥±”…¹åÑ¡¥¹œ¥Ì¡¥‘‘•¸ƒŠP„½¹ÑÉ½°Ñ¡…ĞÅÕ¥•Ñ±äÉ•µ½Ù•ÌÑİ¼)Ñ¡¥É‘Ì½˜Ñ¡”‰Õ¥±‘¥¹Ì¡…ÌÑ¼Í…äÍ¼İ¡¥±”¥ÑÌÁ…¹•°¥ÌÍ¡ÕĞ¸((ŒŒŒ,ÄäƒŠPQ¡”Ñ½İ¸Í¡¥ÁÁ•…Ì€ÈĞÈÑİ¼µµ•ÑÉ”‰½á•Ì°…¹Ñ¡”…Ñ”İ…ÌÉ••¸ƒ
Ü€¨©=9€ÈÀÈØ´Àà´ÄÌ¨¨((ø€¨©=9¸¨¨¥á•¥¸‰Õ¥±‘¥¹Ì¹©Í€€¬Ñ•ÉÉ…¥¸¹©Í€ì¹•Ü…Ñ•Ì¥¸Íµ½­•}É•¹‘•É•È¹µ©Í€ìÑ¡”ÑÉ…À(ø¥ÌİÉ¥ÑÑ•¸ÕÀ¥¸‘½Ì½1µ=9QIP¹µ‘€ƒ
œ€©EÕ…¹Ñ¥Í••½µ•ÑÉäè™±½…Ğ‰•™½É”å½ÔÑÉ…¹Í™½É´¨¸((¨©]¡…ĞÑ¡”Ù¥Í¥Ñ½ÈÍ…Ü¸¨¨Ù•Éä‰Õ¥±‘¥¹œ…ĞÉ½Õ¡±ä„Í¥áÑ ½˜¥ÑÌÍ¥é”¸ĞM½ÕÑ ]…Ñ•È…¹)1…­”ƒŠPÑ¡”‰ÕÍ¥•ÍĞ½É¹•È¥¸Ñ¡”Ñ½İ¸ƒŠPÑİ¼­¹•”µ¡¥ ‰½á•Ì…¹Í½µ”Ù•Éä±…É”ÑÉ••Ì¸1¥Ù”™½È)Í•Ù•É…°‘…åÌ°Ñ¡É½Õ Ñİ¼…ÑÑ•µÁÑ•™¥á•Ì¸((¨©Q¡”‘•™•Ğ°•á…Ñ±ä¸¨¨U¹‘•È-!I}µ•Í¡}ÅÕ…¹Ñ¥é…Ñ¥½¹€„A=M%Q%=8¥Ì„€©¹½Éµ…±¥é•¨%¹ĞÄÙÉÉ…å€+ŠPÍÑ½É•¥¹Ñ••È½Ù•È€ÌÈÜØÜ°Í¼Ñ¡”…ÑÑÉ¥‰ÕÑ”…¸½¹±äÉ•ÁÉ•Í•¹Ğl´Ä°€Åu€ƒŠP…¹Ñ¡”µ•ÑÉ•Ì½µ”)™É½´„‘•ÅÕ…¹Ñ¥Í…Ñ¥½¸Í…±”½¸Ñ¡”¹½‘”€ Ø¸ÈÔ½¸Ñ¡”M…Õ…¹…Í ¤¸)	Õ™™•ÉÑÑÉ¥‰ÕÑ”¹…ÁÁ±å5…ÑÉ¥àÑ€É•…‘Ì‘•¹½Éµ…±¥Í•™±½…ÑÌ°ÑÉ…¹Í™½ÉµÌÑ¡•´°…¹İÉ¥Ñ•ÌÑ¡”É•ÍÕ±Ğ(¨©‰…¬¥¹Ñ¼Ñ¡…ĞÍ…µ”¹½Éµ…±¥é•%¹ĞÄÙÉÉ…å€¨¨¸ÁÁ±å¥¹œÑ¡”‘•ÅÕ…¹Ñ¥Í…Ñ¥½¸Ñ¡•É•™½É”±…µÁ•)•Ù•Éä½½É‘¥¹…Ñ”½Ù•È„µ•ÑÉ”Ñ¼•á…Ñ±ä½¹”µ•ÑÉ”¸	½Ñ Í…±”É•É•ÍÍ¥½¹Ìİ•É”Ñ¡¥Ì½¹”)İÉ¥Ñ”µ‰…¬è‘¥Í…É‘¥¹œÑ¡”¹½‘”ÑÉ…¹Í™½É´…Ù”Ñİ¼µµ•ÑÉ”‰Õ¥±‘¥¹Ì°…ÁÁ±å¥¹œ¥Ğ…Ù”Ñİ¼µµ•ÑÉ”)‰Õ¥±‘¥¹Ì€©¥¸Á¥••Ì¨°‰•…ÕÍ”Ñ¡”±…µÀ¥ÌÁ•Èµ…á¥Ì…¹„‰Õ¥±‘¥¹œ¥Ì¹½Ğ•¹ÑÉ•½¸¥ÑÌ)½É¥¥¸¸Q¡”™¥à¥ÌÑ¼™±½…Ğ™¥ÉÍĞ…¹ÑÉ…¹Í™½É´Í•½¹°¥¸‰½Ñ µ½‘Õ±•Ì¸((¨©]¡äÑ¡É•”É½Õ¹‘Ì½˜‘¥…¹½Í¥Ìµ¥ÍÍ•¥Ğ¸¨¨Ù•ÉäÉ•…‘¥¹œİ…ÌÑ…­•¸™É½´„ÑÉ•”Ñ¡…Ğ‘½•Ì¹½Ğ)¡…Ù”Ñ¡”‰Õœ¸Í¥‘•…ÈÌ±Ñ˜¼ñ¹…µ”ø¹±‰€É•Í½±Ù•Ì……¥¹ÍĞ…ÍÍ•ÑÌ½€¥¸Ñ¡”Í½ÕÉ”ÑÉ•”ƒŠPÑ¡”)Õ¹½µÁÉ•ÍÍ•µ…ÍÑ•ÉÌƒŠP…¹……¥¹ÍĞ‘…Ñ„½€½¸Ñ¡”Í¥Ñ”°İ¡¥ ÁÕ‰±¥Í ¹Í¡€™¥±±Ì™É½´)…ÍÍ•ÑÌ½İ•ˆ½€¸Q¡”Íµ½­”¡…¹•Ù•È½¹”±½…‘•„½µÁÉ•ÍÍ•…ÍÍ•Ğ¸1½…°…ÁÑÕÉ•ÌÉ•¹‘•É•)½ÉÉ•Ñ±ä°µ•…ÍÕÉ•‰Õ¥±‘¥¹Ì…µ”½ÕĞ…ĞÍ•¹Í¥‰±”Í¥é•Ì°…¹…±°½˜¥Ğİ…ÌÑÉÕ”…¹¥ÉÉ•±•Ù…¹Ğ¸((¨©Q¡É•”…Ñ•Ì¹½Ü•á¥ÍĞÑ¡…Ğİ½Õ±¡…Ù”…Õ¡Ğ¥Ğ½¸‘…ä½¹”è¨¨((Ä¸Íµ½­•}É•¹‘•É•È¹µ©Ì€´µÁÕ‰±¥Í¡•‘€Í•ÉÙ•ÌÑ¡”µ¥ÉÉ½È…¹•¹Ñ•ÉÌ…Ğ€½İ…±¬½€ƒŠPÑ¡”Ù¥Í¥Ñ½ÈÌ(€€•á…Ğ‰åÑ•Ì…¹±…å½ÕĞ¸‰…­”¹Í¡€ÉÕ¹Ì¥Ğ…™Ñ•ÈÁÕ‰±¥Í ¸Q¡¥Ì…±Í¼½Ù•ÉÌÑ¡”½Ñ¡•È™…¥±ÕÉ”(€€Ñ¡¥ÌÁÉ½©•Ğ­••ÁÌ¡¥ÑÑ¥¹œè„™¥±”Ñ¡…Ğ•á¥ÍÑÌ¥¸Ñ¡”Í½ÕÉ”ÑÉ•”°¥Ì¹•Ù•È½Á¥•°…¹€ĞÀÑÌ(€€½¹±äİ¡•¸±¥Ù”¸(È¸A•ÈµÍÑÉÕÑÕÉ”Í¥é”…ÍÍ•ÉÑ¥½¹Ì¸Q¡”½±¡•¬Ñ½½¬Ñ¡”€¨©Ñ…±±•ÍĞ¨¨‰Õ¥±‘¥¹œ¥¸Ñ¡”Í•¹”…¹(€€…Í­•İ¡•Ñ¡•È¥Ğİ…Ì‰•Ñİ••¸€Ì…¹€ÌÀ´ƒŠPİ¡¥ Á…ÍÍ•Ìİ¥Ñ ½¹”½ÉÉ•Ğ‰Õ¥±‘¥¹œ…¹€ÈĞÄ(€€‰É½­•¸½¹•Ì°…¹Ñ¡…Ğ¥ÌÑ¡”Í•¹”Ñ¡…ĞÍ¡¥ÁÁ•¸Ù•ÉäÍÑÉÕÑÕÉ”¥Ì¹½Üµ•…ÍÕÉ•……¥¹ÍĞ¥ÑÌ(€€½İ¸É•½É°¥¹±Õ‘¥¹œ¥ÑÌ‘½Õµ•¹Ñ•İ…±±}¡•¥¡Ñ}µ€¸I•¥¹ÑÉ½‘Õ¥¹œÑ¡”™…Õ±Ğ™…¥±ÌÑ¡”¹•Ü(€€¡•­Ì‰ä¹…µ”½¸…±°€ÈĞÈ…¹ÅÕ½Ñ•ÌÑ¡”¡•¥¡ÑÌÑ¡•äÍ¡½Õ±¡…Ù”¡…¸(Ì¸Ñ½½±Ì½µ•…ÍÕÉ•}±‰Ì¹Áå€µ•…ÍÕÉ•Ì…ÍÍ•ÑÌ……¥¹ÍĞÉ•½É‘Ìİ¥Ñ ¹¼‰É½İÍ•È…Ğ…±°°…¹(€€Ñ½½±Ì½Í¡½½Ğ¹µ©Í€Ñ…­•ÌÁ¥ÑÕÉ•ÌÉ…Ñ¡•ÈÑ¡…¸…ÍÍ•ÉÑ¥½¹ÌƒŠP‰•…ÕÍ”Ñ¡”…ÍÍ•ÉÑ¥½¹Ìİ•É”É••¸(€€…¹Ñ¡”Ñ½İ¸İ…Ì¹½Ğ¸((¨©Q¡”±•ÍÍ½¸İ½ÉÑ ­••Á¥¹œè¨¨„…Ñ”Ñ¡…Ğ…¹¹½ĞÉ•… Ñ¡”‰åÑ•ÌÑ¡…ĞÍ¡¥À¥Ì¹½Ğ„…Ñ”°…¹…¸)…É•…Ñ”…ÍÍ•ÉÑ¥½¸€¡µ…á€°…¹å€°Ñ¡”Ñ…±±•ÍÑ€¤¡¥‘•Ì•á…Ñ±äÑ¡”™…¥±ÕÉ”µ½‘”İ¡•É”…±µ½ÍĞ)•Ù•ÉåÑ¡¥¹œ¥Ì‰É½­•¸¸9•¥Ñ¡•È½˜Ñ¡½Í”¥ÌÍÁ•¥™¥ŒÑ¼ÅÕ…¹Ñ¥Í…Ñ¥½¸¸((ŒŒŒ,ÄÔƒŠPQ¡”Ñİ¼É•Í•ÉÙ•…¹½¹åµ½ÕÌÁ…É•±Ìƒ
Ü€¨©]MPAIP=9€ÈÀÈØ´Àà´ÄÌƒ
ÜM=UQ MQ%101%5¨¨((ø€¨©]MPè=9¸¨¨Ñ½½±Ì½•¹•É…Ñ•}İ•ÍÑ}¥¹™¥±°¹Áå€•µ¥ÑÌ€¨¨ÈÀ½˜Ñ¡”€ÔÔ¨¨…¹¥ÌÉ”µ‘•É¥Ù•‰ä(øÑ½½±Ì½¡•¬¹Í¡€¸Q¡”½Ñ¡•È€¨¨ÌÔ…É”¡•±‰äÑ¡”É•¥Á”Ì½İ¸Ñ•ÉÉ…¥¸…Ñ”¨¨ƒŠPÑ¡•¥È•¹ÑÉ•Ì±¥”(øİ•ÍĞ½˜±½…°€´ÌÀÀ´…¹Ñ¡”½µµ¥ÑÑ•É½Õ¹ÍÑ½ÁÌ…Ğ€´ÌÈÀ´¸Q¡•ä…É”¹½Ğ±½ÍĞè¥‘Ì…¹(ø™…µ¥±ä…±±½…Ñ¥½¸…É”­•ÁĞ°…¹•áÑ•¹‘¥¹œÑ¡”Ñ•ÉÉ…¥¸‰½àİ•ÍĞÉ•±•…Í•ÌÑ¡•´İ¥Ñ¡½ÕĞ(øÉ”µ…ÕÑ¡½É¥¹œ¸‘µ¥ÍÍ¥½¸è‘½Ì½1%	IQ%L¹µ‘€€¨©0äÀ¨¨¸€¨©¥¡Ğ½˜Ñ¡”Ñİ•¹ÑäÍÑ½½¥¹Í¥‘”„(øÁ±…ÑÑ•ÍÑÉ••Ğ¨¨‰ä€È¸ËŠLÄÄ¸Ü´…¹İ•É”Í•Ğ‰…¬€¡±…É•ÍĞµ½Ù”€ÄÈ¸Ô´°¥¹Í¥‘”Ñ¡”É•¥Á”Ì½İ¸(øƒ
ÄÈÀ´¤ìÑ¡”É•¥Á”ÁÉ•‘…Ñ•Ì,ÜÌÁ±…ĞÉ¥°Í¼¹½Ñ¡¥¹œ½Õ±¡…Ù”…Õ¡Ğ¥Ğ‰•™½É”¸É½é•¸(ø½¹ÍÑ…¹ÑÌ¥¸Ñ¡”•¹•É…Ñ½È°¹½Ğ„Í•…É …Ğ•¹•É…Ñ¥½¸Ñ¥µ”¸(ø(ø€¨©M=UQ èÍÑ¥±°±…¥µ•°…¹¥Ğ¥ÌÑ¡”¡…É‘•È¡…±˜¨¨ƒŠPÑ¡”É•¥Á”¡…Ì±ÕÍÑ•ÉÍ€…¹„(øÁ±…•µ•¹Ñ}Í¡•µ…€‰ÕĞ9<Á±…•µ•¹ÑÍ€°Í¼¥ÑÌ€àĞÍ±½ÑÌµÕÍĞ‰”UQ!=I……¥¹ÍĞÑ¡”±ÕÍÑ•È(ø½Ù•É±…Àµ½¹ÑÉ½±Ì€¡É•Í•ÉÙ”•¹Ù•±½Á•Ì…É½Õ¹•Ù•Éä¹…µ•M½ÕÑ ]…Ñ•È…¹1…­”MÑÉ••ĞÉ•½É°­••À(ø½ÕĞ½˜Ñ¡”AÕ‰±¥ŒMÅÕ…É”°É•ÍÁ•ĞÑ¡”•ÍÑÉ…äµÁ•¸•¹Ù•±½Á”¤…¹Ñ¡•¸•¹•É…Ñ•Ñ¡”Í…µ”İ…ä¸(ø(ø€¨©1%4ƒŠPÍÑ•İ…É°Í­¥ÀÑ¡”M½ÕÑ ¡…±˜¸¨¨Q…­•¸‰äÑ¡”¥¹Ñ•É…Ñ¥Ù”Í•ÍÍ¥½¸½¸€ÈÀÈØ´Àà´ÄÌ…™Ñ•È(ø,ÄĞ™É••Ñ¡”ÑÉ¥…¹±”¡•…‘É½½´¥Ğ¹••‘Ì¸%Ğ¥Ì„±…É”°Í¥¹±”°¥¹‘¥Ù¥Í¥‰±”Õ¹¥Ğ€¡Ñİ¼(ø•¹•É…Ñ½ÉÌ°øÄÌäÉ•½É‘Ì°½¹”±¥‰•ÉÑ¥•Ì‰±½¬¤…¹Ñİ¼ÉÕ¹Ì‰Õ¥±‘¥¹œ¥Ğ½¹ÕÉÉ•¹Ñ±äİ½Õ±(ø½±±¥‘”½¸‘…Ñ„½ÍÑÉÕÑÕÉ•Ì½€…¹½¸Ñ¡”€ØØÔµÉ½½˜±•‘•È°İ¡¥ ¥Ì•á…Ñ±äÑ¡”­¥¹½˜(ø½¹™±¥ĞÑ¡…Ğ¥Ì•áÁ•¹Í¥Ù”É…Ñ¡•ÈÑ¡…¸µ•É•±ä…¹¹½å¥¹œ¸Q…­”€¨©,È°,Ğ°,Ô°,à½È,ÄÀ¨¨(ø¥¹ÍÑ•…¸Q¡¥Ì±…¥´¥ÌÙ½¥¥˜¹¼½µµ¥ĞÑ½Õ¡¥¹œ¥Ğ±…¹‘Ì‰ä€¨¨ÈÀÈØ´Àà´ÄÔ¨¨ƒŠP„±…¥´Ñ¡…Ğ(ø½ÕÑ±¥Ù•ÌÑ¡”İ½É¬¥Ì„±½¬°…¹¹½‰½‘äÍ¡½Õ±‰”‰±½­•‰ä…¸…‰…¹‘½¹•½¹”¸()Qİ¼É•¥Á•Ì¡…Ù”‰••¸Í¥ÑÑ¥¹œ™Õ±±äÍÁ•¥™¥•…¹Õ¹¥¹ÍÑ…¹Ñ¥…Ñ•°…¹Ñ½•Ñ¡•ÈÑ¡•ä…É”Ñ¡”)±…É•ÍĞÉ•µ…¥¹¥¹œ‰±½¬½˜‰Õ¥±‘¥¹Ì¥¸Ñ¡”ÁÉ½©•Ğè((´€¨©‘…Ñ„½É•½¹ÍÑÉÕÑ¥½¸¼ÄàÌÕ}Á¡…Í”É}İ•ÍÑ}İ½±™}Á½¥¹Ñ}…ÁÁÉ½…¡•Ì¹©Í½¹€¨¨€¡ÍÑ…ÑÕÌè(€É•Í•…É¡}É•¥Á•}¹½Ñ}¥¹ÍÑ…¹Ñ¥…Ñ•‘€¤ƒŠP€¨¨ÔÔÉ½½™Ì¨¨°€ĞĞÁÉ¥¹¥Á…°€¬€ÄÄ…¹¥±±…Éä°€ĞÀ¸Ü€”½˜Ñ¡”(€€ÄÌÔµÉ½½˜]•ÍĞ¥Ù¥Í¥½¸Ñ…É•Ğ¸É½ÕÀµ¥à…¹Á•Èµ™…µ¥±ä½Õ¹ÑÌ€¡ÇŠMÜ° ÇŠM È°ÇŠMÈ°\ÇŠM\Ô°(€Ä°ÇŠMÔ¤…É”…±É•…‘äİÉ¥ÑÑ•¸¸5•µ¼è‘½Ì½IMI ½İ•ÍÑ}‘¥Ù¥Í¥½¹}¥¹™¥±±|ÄàÌÔ¹µ‘€¸(´€¨©‘…Ñ„½É•½¹ÍÑÉÕÑ¥½¸¼ÄàÌÕ}Á¡…Í”É}Í½ÕÑ¡}½É•}…¹‘}µ¥á•‘}É•¥Á”¹©Í½¹€¨¨€¡ÍÑ…ÑÕÌè(€ÁÉ½Á½Í•‘}¹½Ñ}•¹•É…Ñ•‘€¤ƒŠP€¨¨àĞÉ½½™Ì¨¨°€ØØÁÉ¥¹¥Á…°€¬€Äà…¹¥±±…Éä°……¥¹ÍĞ„€ÌÜÀµÉ½½˜M½ÕÑ (€¥Ù¥Í¥½¸Ñ…É•Ğ¸…ÉÉ¥•Ì„Á±…•µ•¹Ñ}Í¡•µ…€…¹„½½É‘¥¹…Ñ•}ÍåÍÑ•µ€‰±½¬İ¥Ñ Ñ¡”UQ4(€½¹Ù•ÉÍ¥½¸ÍÁ•±±•½ÕĞ¸5•µ¼è‘½Ì½IMI ½Á¡…Í”É}Í½ÕÑ¡}½É•}…¹‘}µ¥á•¹µ‘€¸((¨©Q¡”Á…ÑÑ•É¸Ñ¼™½±±½Ü…±É•…‘ä•á¥ÍÑÌÑİ¥”¨¨èÑ½½±Ì½•¹•É…Ñ•}¥¹™•ÉÉ•‘}¥¹™¥±°¹Áå€€¡M½ÕÑ )Á¡…Í”€Ä°€Ğà¤…¹Ñ½½±Ì½•¹•É…Ñ•}¹½ÉÑ¡}¥¹™¥±°¹Áå€€¡9½ÉÑ °€ØÀ¤°‰½Ñ É”µ‘•É¥Ù•‰åÑ”µ™½Èµ‰åÑ”‰ä)„€´µ¡•­€ÍÑ•À¥¸Ñ½½±Ì½¡•¬¹Í¡€¸Ñ¡¥É…¹™½ÕÉÑ •¹•É…Ñ½È¥¸Ñ¡…ĞÍ¡…Á”¥ÌÑ¡”©½ˆƒŠP)9=P¡…¹µİÉ¥ÑÑ•¸É•½É‘Ì°‰•…ÕÍ”€ÄÌä¡…¹µÁ±…•‰Õ¥±‘¥¹Ì…¹¹½Ğ‰”É”µ‘•É¥Ù•…¹Ñ¡”)Á±…•µ•¹Ğ…Ñ”İ½Õ±¡…Ù”¹½Ñ¡¥¹œÑ¼¡•¬……¥¹ÍĞ¸((¨©Q¡”ÑÉ…ÁÌ°…±°½˜Ñ¡•´…±É•…‘äÁ…¥™½È½¹”¸¨¨€¡„¤Q¡”½Õ¹Ñ¥¹œÉÕ±”¥Ì¥¸Ñ¡”M½ÕÑ É•¥Á”Ì)½İ¸İ½É‘Ìè€©„‰•ÑÑ•Èµ•Ù¥‘•¹•É½½˜MU	MQ%QUQL™½È„Í±½Ğì¥Ğ¹•Ù•È¥¹É•…Í•ÌÑ¡”€ØØÔÑ…É•Ğ¨ƒŠP)Í¼Ñ¡•Í”€ÄÌä‘¼¹½ĞÍÑ…¬½¸Ñ½À½˜,ÄÌ€Ìà¸€¡ˆ¤Ñ½½±Ì½•¹•É…Ñ•}¥¹™•ÉÉ•‘}¡½ÕÍ•¡½±‘Ì¹Áå€Á±…•),ÄÁ¡…Í”Ñİ¼İ¡¥±”…Ñ¥Ù•±ä…Ù½¥‘¥¹œÑ¡•Í”Í±½ÑÌ°Í¼Ñ¡•ä…É”ÍÑ¥±°±•…ÈƒŠP­••À¥ĞÑ¡…Ğİ…ä°…¹)É”µÉÕ¸¥ÑÌ€´µ¡•­€…™Ñ•È¸€¡Œ¤Ù•Éä½¹©•ÑÕÉ…°•á¥ÍÑ•¹”°Á½Í¥Ñ¥½¸…¹™½½ÑÁÉ¥¹Ğ½İ•Ì„)‘½Ì½1%	IQ%L¹µ‘€•¹ÑÉäİ¥Ñ ½Ù•ÉÌé€Ñ½­•¹Ì°¥¸‰½Ñ ‘¥É•Ñ¥½¹Ì¸€¡¤A±…•µ•¹ĞµÕÍĞÁ…ÍÌÑ¡”)•á¥ÍÑ¥¹œ…Ñ•Ìè¹¼™½½ÑÁÉ¥¹Ğİ¥Ñ¡¥¸€Ì´½˜…¹ä½Ñ¡•È°Ñ•ÉÉ…¥¸½Ù•É•°‘Éä°ƒŠ&À¸ÌÀ´Á•É¥µ•Ñ•È)É•±¥•˜ƒŠP…¹!•¥¡Ñ™¥•±¹½Ù•ÉÌ ¥€•á¥ÍÑÌ‰•…ÕÍ”„ÍÑÉÕÑÕÉ”½¹”±…¹‘•€àÌÈ´…‘É¥™Ğ…¹)É•Á½ÉÑ•„Á•É™•Ğ™¥Ğ¸€¡”¤QÉ¥…¹±”‰Õ‘•Ğè€ÄÌäÉ½½™Ì…ĞÑ¡”øÜÈÌÑÉ¥ÌÑ¡”,Ä‰…­”…Ù•É…•¥Ì)øÄÀÀ€ÀÀÀ°……¥¹ÍĞ€ÔÜĞ€ĞĞÀ½˜¡•…‘É½½´…ĞÕ±°‘•Ñ…¥°¸%Ğ™¥ÑÌ¹½Üì¥Ğ‘¥¹½Ğ‰•™½É”,ÄĞ¸((ŒŒŒ,ÄØƒŠPQ¡”½¹™¥‘•¹”Ù½…‰Õ±…Éä¥ÌİÉ½¹œ°…¹Ñ¡”½İ¹•È¹…µ•Ñ¡”™¥àƒ
Ü€¨©1=M€ÈÀÈØ´Àà´ÄÔƒŠPMUAIM°<9=P=11=\¨¨((ø€¨©1=M‰ä,ÈÍ„¸¨¨Q¡”É•¹…µ”¡…ÁÁ•¹•°‰ÕĞ€¨©¹½ĞÑ¼Ñ¡”İ½É‘ÌİÉ¥ÑÑ•¸‰•±½Ü¨¨¸Q¡¥ÌÁ…É•°(øÁÉ½Á½Í•‘½Õµ•¹Ñ•€¼‘•É¥Ù•€¼¥¹™•ÉÉ•‘€ìİ¡…Ğ…ÑÕ…±±äÍ¡¥ÁÁ•¥¸Ñ¡”ØÜØµ•É”½˜(ø€ÈÀÈØ´Àà´ÄÌ¥Ì€¨©…ÑÑ•ÍÑ•€¼¥¹™•ÉÉ•€¼É•½¹ÍÑÉÕÑ•‘€¨¨°…¹Ñ½½±Ì½Ù…±¥‘…Ñ”¹Áå€Ì=9%9€(øÑÕÁ±”¥ÌÑ¡”•¹™½É•µ•¹Ğ¸Ù•ÉåÑ¡¥¹œ™É½´€‰Q¡”É•¹…µ”°İ¡¥ ¥Ì„É•¹…µ”…¹¹½Ğ„¹•ÜÑ¥•Èˆ(ø½¹İ…É‘•ÍÉ¥‰•Ì„Ù½…‰Õ±…ÉäÑ¡¥ÌÁÉ½©•Ğ‘½•Ì¹½ĞÕÍ”ƒŠP€¨©„É•½ÉİÉ¥ÑÑ•¸Ñ¼Ñ¡”Ñ…‰±”‰•±½Ü(ø™…¥±ÌÑ¡”‰Õ¥±¸¨¨‘½Ì½AI=Y99¹µ‘€¥ÌÑ¡”ÕÉÉ•¹Ğ…ÕÑ¡½É¥Ñä…¹¹½Ü…ÉÉ¥•Ì„‘…Ñ•¹½Ñ”(øÍ…å¥¹œÍ¼¸(ø(øQ¡”Á…É•°¥Ì­•ÁĞÉ…Ñ¡•ÈÑ¡…¸‘•±•Ñ•‰•…ÕÍ”¥ÑÌ€©É•…Í½¹¥¹œ¨¥ÌÑ¡”É•…Í½¹¥¹œ‰•¡¥¹Ñ¡”(øİ½É‘ÌÑ¡…Ğ‘¥Í¡¥À°…¹‰•…ÕÍ”¥Ğ¥ÌÑ¡”½É¥¥¸½˜Ñ¡”™…Õ±Ğ,ÈÍ„Íİ•ÁĞÕÀè¥Ğ±•™ĞÑ¡”(øÍÑ…¹‘¥¹œ¥¹ÍÑÉÕÑ¥½¸Ñ¼ÍÑ…ä€‰Ù½…‰Õ±…Éäµ…¹½ÍÑ¥Œİ¡¥±”,ÄØ¥Ì¥¸™±¥¡Ğˆ°…¹Õ¹‘•ÈÑ¡…Ğ(ø¥¹ÍÑÉÕÑ¥½¸€ÄäÌ•¹•É…Ñ•¹…µ•Ìİ•¹Ğ½¸Í…å¥¹œ%¹™•ÉÉ•‘€™½ÈÑ¡É•”İ••­Ì…™Ñ•È¥¹™•ÉÉ•‘€(øÍÑ½ÁÁ•µ•…¹¥¹œ¥¹Ù•¹Ñ•¸€¨©Q¡…Ğ¥¹ÍÑÉÕÑ¥½¸¥ÌÍÁ•¹Ğ¸¨¨I•…Ñ¡”ÍÑÉ¥¹Ì½™˜(ø‘½Ì½AI=Y99¹µ‘€°¹½Ğ½™˜Ñ¡¥ÌÍ•Ñ¥½¸¸()Q¡”½İ¹•ÈÌ½ÉÉ•Ñ¥½¸°€ÈÀÈØ´Àà´ÄÌ°¥¸Ñ¡•¥Èİ½É‘Ìè€¨‰$‘½¸Ğİ…¹ĞÑ¼ÕÍ”¥¹™•ÉÉ•¥¸Ñ¡½Í”­¥¹)½˜…Í•Ìİ¡•É”Ñ¡•É”İ…ÌÍ½µ”Í½±¥É•Í•…É ‰•¡¥¹¥ÓŠ˜Ñ¡”½Ù•É¹µ•¹Ğ‰±…­Íµ¥Ñ Í¡½ÀÍ••µÌ)™…¥É±ä½½¥¸±½…Ñ¥½¸…¹å½Ô±…‰•±•¥Ğ¥¹™•ÉÉ•¸%¹™•ÉÉ•¥ÌÑ¡”¹…µ”™½Èİ¡•¸å½Ôµ…­”å½ÕÈ)É•Í•…É ½µ‰¥¹…Ñ¥½¸…¹¥¹Ù•¹Ğ„Á•ÉÍ½¸‰…Í•½¸±¥­•±ä¹••‘Ì½˜Ñ¡”¥Ñä…¹Á½ÁÕ±…Ñ¥½¸¸ˆ¨()Q¡•ä…É”É¥¡Ğ°…¹Ñ¡”™…Õ±Ğ¥ÌÑ¡…ĞÑİ¼Ù•Éä‘¥™™•É•¹Ğ…ÑÌÍ¡…É”½¹”İ½É¸A±…¥¹œÑ¡”…•¹ä)‰±…­Íµ¥Ñ Í¡½À™É½´¹‘É•…ÌÌ‘•ÍÉ¥ÁÑ¥½¸¥ÌIMI ì¥¹Ù•¹Ñ¥¹œ„½½Á•È‰•…ÕÍ”„Ñ½İ¸Á…­¥¹œ)Ñİ¼Ñ¡½ÕÍ…¹¡½Ì¹••‘Ì½¹”¥Ì%9Y9Q%=8¸	½Ñ ÕÉÉ•¹Ñ±äÉ•…¥¹™•ÉÉ•‘€¸((¨©Q¡”É•¹…µ”°İ¡¥ ¥Ì„É•¹…µ”…¹¹½Ğ„¹•ÜÑ¥•È¨¨ƒŠPÑ¡”Ñ¡É•”•á¥ÍÑ¥¹œ±•Ù•±Ì­••ÀÑ¡•¥È)µ•…¹¥¹Ì…¹Ñ¡•¥ÈÁ…¥¹Ğ°…¹Ñİ¼½˜Ñ¡•´•Ğ¡½¹•ÍĞ¹…µ•Ìè()ğ¹½Üğ‰•½µ•ÌğÁ…¥¹Ğğµ•…¹Ìğ)ğ´´µğ´´µğ´´µğ´´µğ)ğ‘½Õµ•¹Ñ•‘€ğ‘½Õµ•¹Ñ•‘€ğİ¡¥Ñ”€¼Õ¹µ…É­•ğ„Í½ÕÉ”…ÑÑ•ÍÑÌÑ¡¥Ì…ĞÑ¡”Í•¹”‘…Ñ”ğ)ğ¥¹™•ÉÉ•‘€ğ€¨©‘•É¥Ù•‘€¨¨ğ½±ğÉ•…Í½¹•™É½´ÍÁ•¥™¥Œ•Ù¥‘•¹”	=UPQ!%LQ!%9ƒŠP„‘•ÍÉ¥‰•±½…Ñ¥½¸°„µ•…ÍÕÉ•±½Ğ°…¸…‘©…•¹ĞÉ•½É¸I•Í•…É¡•…¹±¥­•±ä¸ğ)ğ½¹©•ÑÕÉ…±€ğ€¨©¥¹™•ÉÉ•‘€¨¨ğ‘¥Ñ¡•É•ğ¥¹Ù•¹Ñ•Ñ¼™¥±°„‘•µ½¹ÍÑÉ…‰±”¹••½˜Ñ¡”Ñ½İ¸¸9¼•Ù¥‘•¹”™½ÈÑ¡¥ÌÁ…ÉÑ¥Õ±…ÈÑ¡¥¹œ¸€¨©9½Ğ„€‰Õ•ÍÌˆ¨¨ƒŠPÑ¡”½İ¹•È…Í­•™½ÈÑ¡…Ğİ½ÉÑ¼¼¸ğ()Q¡¥Ì…±Í¼U9%%LÑ¡”Ñİ¼…á•Ìè‘…Ñ„½É•Í¥‘•¹ÑÌ½€…±É•…‘äÉ…‘•ÌÁ•½Á±”)‘½Õµ•¹Ñ•‘€€¼‘•É¥Ù•‘€€¼¥¹™•ÉÉ•‘€İ¥Ñ …±µ½ÍĞ•á…Ñ±äÑ¡•Í”µ•…¹¥¹Ì€¡‘½Ì½AI=Y99¹µ…¹)‘…Ñ„½É•Í¥‘•¹ÑÌ½¥¹‘•à¹©Í½¹€¤¸™Ñ•ÈÑ¡”É•¹…µ”½¹”Ù½…‰Õ±…Éä½Ù•ÉÌ‰½Ñ ¸((¨©=É‘•Èµ…ÑÑ•ÉÌ°‰•…ÕÍ”Ñ¡”İ½É‘Ì½±±¥‘”µ¥µ™±¥¡Ğ¸¨¨½¹©•ÑÕÉ…±ƒŠI¥¹™•ÉÉ•‘€…¹¹½ĞÉÕ¸)‰•™½É”¥¹™•ÉÉ•‘ƒŠI‘•É¥Ù•‘€°½È•Ù•Éä½±¥¹™•ÉÉ•‘€¥ÌÍİ…±±½İ•¸¼¥Ğ…Ì=9ÍÉ¥ÁÑ•Á…ÍÌ)İ¥Ñ „Ñİ¼µÁ¡…Í”ÍÕ‰ÍÑ¥ÑÕÑ¥½¸Ñ¡É½Õ „Í•¹Ñ¥¹•°°É”µ‘•É¥Ù”•Ù•Éä•¹•É…Ñ•É•½É°…¹‘¥™˜Ñ¡”)½Õ¹Ğ½˜•… ±•Ù•°‰•™½É”…¹…™Ñ•ÈèÑ¡”Ñ½Ñ…±ÌµÕÍĞµ½Ù”…Ì„Á•ÉµÕÑ…Ñ¥½¸°¹½Ğ¡…¹”¸((¨©]¡…ĞµÕÍĞµ½Ù”İ¥Ñ ¥Ğè¨¨Í¡•µ…Ì¼¨¹©Í½¹€•¹ÕµÌƒ
ÜÑ½½±Ì½Ù…±¥‘…Ñ”¹Áå€€¡¥¹±Õ‘¥¹œ)¡•­}±¥‰•ÉÑ¥•Í}½Ù•É…•€°İ¡¥ ­•åÌ½¸½¹©•ÑÕÉ…±€ƒŠP…™Ñ•ÈÑ¡”É•¹…µ”Ñ¡”±¥‰•ÉÑ¥•ÌÑÉ¥•È)¥Ì¥¹™•ÉÉ•‘€¤ƒ
ÜÑ¡”Ñ¡É•”¥¹™¥±°•¹•É…Ñ½ÉÌ…¹Ñ¡”¡½ÕÍ•¡½±•¹•É…Ñ½È°İ¡½Í”±¥Ñ•É…°ÍÑÉ¥¹Ì)…É”É”µ‘•É¥Ù•‰åÑ”™½È‰åÑ”ƒ
ÜÉ•¹‘•É•ÉÌ½İ•ˆ½©Ì½½¹™¥‘•¹”¹©Í€ƒ
ÜÑ¡”Ù¥‘•¹”±••¹¥¸)¥¹‘•à¹¡Ñµ±€ƒ
ÜÁ½ÁÕÀ¹©Í€ƒ
Ü‘½Ì½AI=Y99¹µ‘€°9QL¹µ‘€°‘½Ì½1%	IQ%L¹µ‘€ÁÉ½Í”¸(¨©¼¹½ĞÉ•İÉ¥Ñ”Ñ¡”¡¥ÍÑ½É¥…°ÁÉ½Í”¥¸‘½Ì½MQQUL¹µ‘€½ÈÍ¡¥ÁÁ•¡…¹•±½œ•¹ÑÉ¥•Ì¨¨ƒŠPÑ¡•ä)…É”„É•½É½˜İ¡…Ğİ…ÌÍ…¥…ĞÑ¡”Ñ¥µ”¸((ŒŒŒ,ÄÜ€¡ÍÁ•Œ¤ƒŠP½¹™¥‘•¹”Ù¥•Üè‘¥Ñ¡•ÈÑ¡”É½½™Ì°…¹±•Ğ„±•Ù•°‰”Íİ¥Ñ¡•½™˜ƒ
Ü€¨©%M!I€ÈÀÈØ´Àà´ÄĞ¨¨((ø	Õ¥±Ğ¸Q¡”É½½˜¡…±˜±…¹‘•İ¥Ñ ,ÈÁˆ°İ¡¥ µ…‘”Ñ¡”İ¡½±”½˜„É•½¹ÍÑÉÕÑ•‰Õ¥±‘¥¹œ(ø‘¥Ñ¡•ÈÑ½•Ñ¡•ÈƒŠPİ…±±Ì°É½½˜°ÑÉ¥´…¹¡¥µ¹•äƒŠPÉ…Ñ¡•ÈÑ¡…¸±•…Ù¥¹œ„¡½ÍĞİ¥Ñ „Í½±¥(ø¡¥µ¹•ä½¸¥Ğ¸Q¡”Íİ¥Ñ µ„µ±•Ù•°µ½™˜¡…±˜¥ÌÑ¡”,ÄÜ•¹ÑÉä…‰½Ù”¸Q¡”½É¥¥¹…°ÍÁ•Œ¥Ì­•ÁĞ(ø‰•±½Ü‰•…ÕÍ”¥Ğ¥Ìİ¡…Ğİ…Ì…Í­•™½È…¹Ñ¡”•¹ÑÉä…‰½Ù”¥Ìİ¡…Ğİ…Ì‰Õ¥±Ğ¸(()•Á•¹‘Ì½¸,ÄØÌÙ½…‰Õ±…Éä¸Q¡É•”Ñ¡¥¹ÌÑ¡”½İ¹•È…Í­•™½È½¸€ÈÀÈØ´Àà´ÄÌè((Ä¸€¨©Q¡”É½½™Ì‘¼¹½Ğ‘¥Ñ¡•È¸¨¨%¸Ñ¡”½¹™¥‘•¹”Ù¥•ÜÑ¡”İ…±±ÌÑ…­”Ñ¡”‘¥Ñ¡•É•ÑÉ•…Ñµ•¹Ğ…¹(€€Ñ¡”É½½˜Á±…¹•Ì‘¼¹½Ğ°Í¼„‰Õ¥±‘¥¹œÑ¡…Ğ¥Ì•¹Ñ¥É•±ä¥¹Ù•¹Ñ•ÍÑ¥±°É•…‘Ì…Ì¡…±˜µÍ½±¥¸(€€¥¹½ÕĞİ¡•Ñ¡•ÈÑ¡”É½½˜µ…Ñ•É¥…°µ¥ÍÍ•ÌÑ¡”}½¹™¥‘•¹•€…ÑÑÉ¥‰ÕÑ”½ÈÑ¡”Á…Ñ °…¹•¥Ñ¡•È(€€‘¥Ñ¡•È¥Ğ½ÈƒŠPÑ¡”½İ¹•ÈÌ½İ¸ÍÕ•ÍÑ¥½¸ƒŠP¥Ù”Ñ¡”É½½˜„‘¥ÍÑ¥¹ĞÑÉ•…Ñµ•¹ĞÍ¼„‘¥Ñ¡•É•(€€İ…±°…¹„‘¥Ñ¡•É•É½½˜ÍÑ…ä±•¥‰±”……¥¹ÍĞ•… ½Ñ¡•È¸(È¸€¨©¡¥‘”µ½‘”¸¨¨€¨‰$İ½Õ±±¥­”Ñ¼‰”…‰±”Ñ¼Ñ½±”Ñ¡…ĞÙ¥•ÜÑ¼µ…­”Ñ¡”‰Õ¥±‘¥¹Ì½‰©•ÑÌ(€€¥Ñ•µÌ‘¥Í…ÁÁ•…È…±Ñ½•Ñ¡•È‰…Í•½¸Ñ¡½Í”±•Ù•±Ì¸ˆ¨M¼Ñ¡”½¹™¥‘•¹”Ù¥•Ü…¥¹Ì„µ½‘”è=1=UH(€€€¡Ñ½‘…äÌ‰•¡…Ù¥½ÕÈ¤½È!%°İ¡•É”„±•Ù•°Ì•½µ•ÑÉä¥ÌÉ•µ½Ù•™É½´Ñ¡”Í•¹”É…Ñ¡•ÈÑ¡…¸(€€Ñ¥¹Ñ•ƒŠPİ…±¬„Ñ½İ¸½˜½¹±äİ¡…Ğ¥Ì‘½Õµ•¹Ñ•°Ñ¡•¸½¹±äİ¡…Ğ¥Ì‘½Õµ•¹Ñ•…¹‘•É¥Ù•¸(€€Q¡”½İ¹•ÈÍÕ•ÍÑÌ½¹Í½±¥‘…Ñ¥¹œ¥Ğ¥¹Ñ¼Ñ¡”½¹™¥‘•¹”½¹ÑÉ½°É…Ñ¡•ÈÑ¡…¸…‘‘¥¹œ„Í•½¹(€€½¹”°İ¡¥ ¥ÌÉ¥¡Ğè¥Ğ¥ÌÑ¡”Í…µ”ÅÕ•ÍÑ¥½¸…Í­•Ñİ¼İ…åÌ¸(Ì¸A•Èµ±•Ù•°Ñ½±•Ì°Í¼Ñ¡”Ñ¡É•”±•Ù•±Ì…¸‰”Í¡½İ¸½È¡¥‘‘•¸¥¹‘•Á•¹‘•¹Ñ±ä¸((¨©Q¡”¡½¹•ÍĞÑÉ…Àè¨¨¡¥‘¥¹œ‰ä±•Ù•°µÕÍĞ¡¥‘”İ¡½±”=	)QL‰äÑ¡•¥ÈÉ•½ÉÌÉ…‘”°¹½Ğ)¥¹‘¥Ù¥‘Õ…°…ÑÑÉ¥‰ÕÑ•ÌƒŠP„‰Õ¥±‘¥¹œİ¡½Í”Á½Í¥Ñ¥½¸¥Ì‘•É¥Ù•‰ÕĞİ¡½Í”É½½˜Á¥Ñ ¥Ì¥¹™•ÉÉ•¥Ì)½¹”‰Õ¥±‘¥¹œ°…¹¥Ğ¡…ÌÑ¼‰”Í½µ•İ¡•É”¸•¥‘”…¹İÉ¥Ñ”‘½İ¸İ¡¥ …ÑÑÉ¥‰ÕÑ”½Ù•É¹Ì…¸)½‰©•ĞÌÙ¥Í¥‰¥±¥Ñä€¡•á¥ÍÑ•¹”°ÍÕÉ•±ä¤‰•™½É”‰Õ¥±‘¥¹œÑ¡”½¹ÑÉ½°¸((ŒŒŒ,Äà€¡ÍÁ•Œ¤ƒŠP%¹Ù•¹ĞÁ•É¥½µ…ÁÁÉ½ÁÉ¥…Ñ”¹…µ•Ì™½È¥¹™•ÉÉ•É•Í¥‘•¹ÑÌƒ
Ü€¨©%M!I€ÈÀÈØ´Àà´ÄĞ¨¨((ø	Õ¥±ĞƒŠPÍ•”Ñ¡”,Äà•¹ÑÉä…‰½Ù”™½ÈÑ¡”Á½½±Ì°Ñ¡”İ•¥¡Ñ¥¹œ…¹Ñ¡”Ù…±¥‘…Ñ½ÈÉÕ±”Ñ¡…Ğ(ø­••ÁÌ…¸¥¹Ù•¹Ñ•¹…µ”™É½´•Ù•ÈÉ…‘¥¹œ…‰½Ù”Ñ¡”¥¹Ù•¹Ñ¥½¸¸MÁ•Œ­•ÁĞ™½ÈÑ¡”É•½É¸(()Q¡”½İ¹•È°€ÈÀÈØ´Àà´ÄÌè€¨‰™½È¥¹™•ÉÉ•Á•½Á±”å½Ô…¸¥¹Ù•¹Ğ½É•…Ñ”Á•É¥½…ÁÁÉ½ÁÉ¥…Ñ”¹…µ•Ì™½È)Ñ¡•·Š˜½˜½ÕÉÍ”¥ĞÌ½¹”½˜Ñ¡”¥¹™•É•¹•ÌÍ¼$´ÍÕÉ”¥Ğİ¥±°‰”±•…ËŠ˜ÕÍ”İ¡…Ñ•Ù•È¡¥ÍÑ½É¥…°)É•Í•…É ¥ÌÉ•…Í½¹…‰±”™½È¹…µ•Ì±¥­”‘½Ñ½ÉÌµ¥¡Ğ¡…Ù”Í½µ”¹…µ•Ì…¹±…‰½É•ÉÌİ½Õ±¡…Ù”)½Ñ¡•ÉÌ¸ˆ¨()Q¡¥ÌIYIMLÑ¡”ÍÑ…¹‘¥¹œÉÕ±”¥¸‘½Ì½1%	IQ%L¹µ‘€0àĞ…¹‘…Ñ„½É•Í¥‘•¹ÑÌ½¥¹‘•à¹©Í½¹€°İ¡¥ )Í…ä¹¼¥¹™•ÉÉ•Á•ÉÍ½¸¥Ì¹…µ•¸Q¡…ĞÉ•Ù•ÉÍ…°¥ÌÑ¡”½İ¹•ÈÌ…±°…¹¥Ğ¥Ìµ…‘”ƒŠP‰ÕĞÑ¡”)É•…Í½¸™½ÈÑ¡”½±ÉÕ±”¡…ÌÑ¼‰”…¹Íİ•É•É…Ñ¡•ÈÑ¡…¸™½É½ÑÑ•¸è„¹…µ•¥¹Ù•¹Ñ•Á•ÉÍ½¸µÕÍĞ)¹•Ù•È‰”µ¥ÍÑ…­…‰±”™½È„‘½Õµ•¹Ñ•½¹”¸M¼Ñ¡”¹…µ”¥Ì…¸…ÑÑÉ¥‰ÕÑ”±¥­”…¹ä½Ñ¡•È…¹…ÉÉ¥•Ì)Ñ¡”¥¹™•ÉÉ•‘€É…‘”Ñ¡”Á•ÉÍ½¸…±É•…‘ä¡…ÌìÑ¡”…ÉµÕÍĞÍ¡½ÜÑ¡”¹…µ”…¹Ñ¡”É…‘”Ñ½•Ñ¡•È¸((¨©¼Ñ¡”É•Í•…É É…Ñ¡•ÈÑ¡…¸Á¥­¥¹œÁ±•…Í…¹Ğ¹…µ•Ì¸¨¨€ÄàÌÔ¡¥…¼Ì¥¹™•ÉÉ•Á½ÁÕ±…Ñ¥½¸Í¡½Õ±)‘É…Ü½¸Ñ¡”‘½Õµ•¹Ñ•½¹”Ì½İ¸½µÁ½Í¥Ñ¥½¸ƒŠPÑ¡”€ÄàÌÌÑÉ…‘”É½ÍÑ•È…¹Ñ¡”É•Í¥‘•¹ÑÌ…±É•…‘ä¥¸)‘…Ñ„½É•Í¥‘•¹ÑÌ½€…É”Ñ¡”Í…µÁ±”è9•Ü¹±…¹…¹9•Üe½É¬e…¹­••Ì°9•Üe½É¬ÕÑ °%É¥Í …¹)•Éµ…¸…ÉÉ¥Ù…±Ì½¸Ñ¡”…¹…°İ½É­Ì°É•¹ µ…¹…‘¥…¸…¹7¥Ñ¥Ì™…µ¥±¥•Ì…ĞÑ¡”™½É­Ì¸QÉ…‘”)½ÉÉ•±…Ñ•Ìİ¥Ñ ½É¥¥¸¥¸İ…åÌÑ¡”Í½ÕÉ•ÌÍÕÁÁ½ÉĞ€¡…¹…°±…‰½ÕÈ¡•…Ù¥±ä%É¥Í ìµ•É¡…¹ÑÌ…¹)ÁÉ½™•ÍÍ¥½¹…±Ì‘¥ÍÁÉ½Á½ÉÑ¥½¹…Ñ•±äe…¹­•”¤°…¹Ñ¡…Ğ½ÉÉ•±…Ñ¥½¸ƒŠP¹½Ğ„É…¹‘½´‘É…ÜƒŠP¥Ìİ¡…Ğ)µ…­•Ì…¸¥¹Ù•¹Ñ•¹…µ”‘•™•¹Í¥‰±”¸MÕÉ¹…µ•Ì…¹¥Ù•¸¹…µ•ÌÍ¡½Õ±½µ”™É½´Á•É¥½µ…ÑÑ•ÍÑ•)±¥ÍÑÌ°…¹Ñ¡”µ•µ¼µÕÍĞÍ…äİ¡¥ …¹İ¡ä°Á•ÈÑ¡”ÍÑ…¹‘¥¹œÉÕ±”Ñ¡…Ğ„Í½ÕÉ•}¥É•Í½±Ù•Ì¸()‘¹…µ•}‰…Í¥Í€€¡½È•ÅÕ¥Ù…±•¹Ğ¤Ñ¼Ñ¡”Á•ÉÍ½¸É•½ÉÍ¼Ñ¡”…É…¸Í…ä]!dÑ¡¥Ì¹…µ”…¹¹½Ğ)…¹½Ñ¡•È°…¹•áÑ•¹Ñ½½±Ì½Ù…±¥‘…Ñ”¹Áå€Í¼…¸¥¹™•ÉÉ•Á•ÉÍ½¸Ì¹…µ”…¹¹½Ğ‰”É…‘•…‰½Ù”)¥¹™•ÉÉ•‘€¸((´´´((ŒŒLÄƒŠP•½É•™•É•¹”…¹Ù•É¥™äÑ¡”‘…ÑÕ´ƒ
Ü€¨©=9€ÈÀÈØ´Àà´Àä¨¨()=É¥¥¸è€ĞĞÜÀÜÈ¸Ü°8€ĞØÌÜÌäÔ¸à€¡AMèÈØäÄØ¤€ô€ĞÄ¸ààØÜÈÄ°€´àÜ¸ØÌÜäÔÄƒŠPÑ¡”]É¥¡Ğµ‘É…İ¸™½É­Ì°)•¥¡Ğµ@™¥ĞI5L€ÄÜ¸Ô´°É½ÍÌµ¡•­•……¥¹ÍĞ…¸¥¹‘•Á•¹‘•¹Ğ!…Ñ¡…İ…ä•½É•™•É•¹”€ ÔÜ¸ä´¤)…¹Ñ¡”µ½‘•É¸=M4©Õ¹Ñ¥½¸€ Ìä¸Ğ´¤¸Q¡”ÁÕ‰±¥Í¡•±±µ…ÁÌ€ÌµÁ½¥¹ĞÑÉ…¹Í™½É´İ…Ìµ•…ÍÕÉ•(¡I5L€ÈÔ¸ä´……¥¹ÍĞ¥¹‘•Á•¹‘•¹Ğ½¹ÑÉ½°¤…¹ÍÕÁ•ÉÍ•‘•ì¹¼…¹¹½Ñ…Ñ¥½¸•á¥ÍÑ•™½ÈÑ¡”1=)!…Ñ¡…İ…ä°Í¼Ñ¡…Ğ•½É•™•É•¹”¥Ì¹•Üİ½É¬¸5•µ¼è‘½Ì½IMI ½‘…ÑÕµ}‘•É¥Ù…Ñ¥½¸¹µ‘€ì)•¹™½É•µ•¹ĞèÑ½½±Ì½É•‘•É¥Ù•}‘…ÑÕ´¹Áå€¥¸¡•¬¹Í¡€¸…ÉÉäµ™½Éİ…Éèƒ
ÄÈÀ´İ½É­¥¹œÕ¹•ÉÑ…¥¹Ñä)™½È…¹åÑ¡¥¹œÑÉ…•™É½´Ñ¡”€ÄàÌĞÍ¡••ÑÌì•¹•É…Ñ”ÍÑÉ••Ğ•½µ•ÑÉä…¹…±åÑ¥…±±ä™É½´Á±…Ğ)‘¥µ•¹Í¥½¹Ì€¡!…Ñ¡…İ…ä…¹¹½Ñ…Ñ•ÌÑ¡•´¤…¹Í¹…ÀÑ¼½¹ÑÉ½°É…Ñ¡•ÈÑ¡…¸ÑÉ…¥¹œÁ¥á•±Ì¸((ŒŒLÈƒŠPQ•ÉÉ…¥¸°•Á½ ”ÄàÌÑ}¡…É‰½É}ÕÑ€((ŒŒŒLÉ”ƒŠP•áÑ•¹Ñ¡”É½Õ¹MPÑ¼Ñ¡”±…­”ƒ
Ü€¨©%8AI=IMLƒŠPÁ…É•°€¡„¤=9€ÈÀÈØ´Àà´ÄÀ¨¨()AÉ½µ½Ñ•…‰½Ù”Ñ¡”É•ÍĞ½˜LÈ‰•…ÕÍ”Ñ¡”™É•”µ™±ä…µ•É„µ…‘”Ñ¡”…À¥µÁ½ÍÍ¥‰±”Ñ¼)µ¥ÍÌ™É½´Ñ¡”…¥Èè€¨©Ñ¡”µ½‘•±±•É½Õ¹ÍÑ½ÁÌ€àÀÀ´Í¡½ÉĞ½˜½ÉĞ•…É‰½É¸…¹…‰½ÕĞ„)­¥±½µ•ÑÉ”Í¡½ÉĞ½˜1…­”5¥¡¥…¸¸¨¨()Q¡”¹Õµ‰•ÉÌ°µ•…ÍÕÉ•……¥¹ÍĞ‘…Ñ„½‘…ÑÕ´¹©Í½¹€É…Ñ¡•ÈÑ¡…¸•ÍÑ¥µ…Ñ•è()ğğ±½…°ğ¥¹Í¥‘”Ñ¡”‰½àüğ)ğ´´µğ´´µğ´´µğ)ğÕÉÉ•¹ĞÑ•ÉÉ…¥¸‰½àğƒŠ"HÌÈÀƒŠ˜€¨¨¬ÌÈÀ¨¨ğƒŠPğ)ğ1…­”MĞ€˜MÑ…Ñ”MĞğ€¬àĞÈğ¹¼ğ)ğ€¨©½ÉĞ•…É‰½É¸Í¥Ñ”¨¨€¡5¥¡¥…¸Ù”‰É¥‘”¤ğ€¨¨¬ÄÄÈÜ¨¨ğ¹¼°€Ì¸×\‰•å½¹Ñ¡”•‘”ğ)ğµ½‘•É¸±…­•™É½¹Ğ…ĞÑ¡”É¥Ù•Èµ½ÕÑ ğ€¬ÈÄÔÔğ¹¼ğ((¡1…¹‘µ…É¬Á½Í¥Ñ¥½¹Ì…É”µ½‘•É¸µÍÕ•ÍÍ½ÈÍ½Á¥¹œ™¥ÕÉ•Ì°¹½Ğ‘…Ñ…Í•Ğ±…¥µÌƒŠPÑ¡•äÍ…ä)¡½Ü™…ÈÑ¡”‰½à™…±±ÌÍ¡½ÉĞ°¹½Ñ¡¥¹œ…‰½ÕĞ€ÄàÌÔ¸¤((¨©Q¡”€ÄàÌÔ±…­”•‘”¥Ì¹½İ¡•É”¹•…ÈÑ¡”µ½‘•É¸½¹”¨¨ƒŠP•Ù•ÉåÑ¡¥¹œ•…ÍĞ½˜É½Õ¡±ä5¥¡¥…¸)Ù•¹Õ”¥Ì±…Ñ•È±…¹‘™¥±°°µÕ ½˜¥Ğ™¥É”‘•‰É¥Ì…™Ñ•È€ÄàÜÄƒŠPÍ¼‘É…İ¥¹œÑ½‘…äÌ½…ÍĞ)İ½Õ±‰”Ñ¡”Í¥¹±”±…É•ÍĞ™…±Í”±…¥´¥¸Ñ¡”‘…Ñ…Í•Ğ¸%Ğ½µ•Ì½™˜]É¥¡Ğ€ÄàÌĞ¸Q¡¥Ì¥Ì)ÁÉ•¥Í•±äÑ¡”…Í”Ñ¡”å•…ÈµÁ…É…µ•Ñ•É¥é•…É¡¥Ñ•ÑÕÉ”•á¥ÍÑÌ™½Èè‘½Ì½A=!L¹µ‘€ÑÉ•…ÑÌ)Ñ•ÉÉ…¥¸…ÌÙ•ÉÍ¥½¹•Á•È•Á½ °Í¼„±…Ñ•Èå•…È•ÑÌ¥ÑÌ½İ¸Í¡½É•±¥¹”É…Ñ¡•ÈÑ¡…¸•‘¥Ñ¥¹œ)Ñ¡¥Ì½¹”¸((¨©]¡¥ Í½ÕÉ”‘É¥Ù•Ìİ¡¥ •±•µ•¹Ğ¨¨€¡Í•Ğ€ÈÀÈØ´Àà´ÄÀ‰ä-•Ù¥¸°İ¡¼¥ÌÉ¥¡ĞÑ¡…ĞÑ¡”)•…É±¥•ÈÉ•…‘¥¹œ½˜Ñ¡•Í”Í½ÕÉ•Ìİ…Ì½Ù•Èµ…ÕÑ¥½ÕÌƒŠPÍ•”‘½Ì½AI=Y99¹µ‘€ƒ
œÑ¥•È€Ô¤è()ğ•±•µ•¹ĞğÍ½ÕÉ”ğ½¹™¥‘•¹”¥ĞÍÕÁÁ½ÉÑÌğ)ğ´´µğ´´µğ´´µğ)ğ±…­”Í¡½É”°¡…É‰½ÕÈÕĞ°Á¥•ÉÌ°Í…¹Ñ½¹Õ”°Ñ¡”½±Í½ÕÑ¡İ…É¡…¹¹•°ğ€¨©]É¥¡Ğ€ÄàÌĞ¨¨ƒŠP„ÍÕÉÙ•ä°…¹Ñ¡”µ…ÍÑ•Èİ…ÉÁ¥¹œÉ…ÍÑ•Èğ¥¹™•ÉÉ•‘€°ƒ
ÄÈÀ´ì„™…¥È•ÍÑ¥µ…Ñ”¥Ì•áÁ•Ñ•É…Ñ¡•ÈÑ¡…¸…Ù½¥‘•ğ)ğÑ¡”É¥Ù•ÈÑ¡É½Õ Ñ¡”•¹ÑÉ…°‰±½­ÌìÍÑÉ••Ğ…¹‰±½¬•½µ•ÑÉäğ€¨©Q¡½µÁÍ½¸Á±…Ğ€ÄàÌÀ¨¨ƒŠP€àÀµ™ĞÍÑÉ••ÑÌ°€Äàµ™Ğ…±±•åÌ°•¹•É…Ñ•…¹…±åÑ¥…±±ä™É½´Ñ¡”µ½‘Õ±”°¹½ĞÑÉ…•ğ‘½Õµ•¹Ñ•‘€™½ÈÑ¡”µ½‘Õ±”°¥¹™•ÉÉ•‘€™½ÈÑ¡”™¥Ğğ)ğÑ¡”ÍÑÉ•…µÌ½µ¥¹œ¥¸°…¹İ¡•É”•… ½¹”Ñ•Éµ¥¹…Ñ•Ìğ€¨©½¹±•ä½MÑ•±é•È€ÄàÌÌ¨¨…ÌÁÉ¥µ…ÉäÕ¥‘”°]É¥¡Ğ…ÌÑ¡”¡•¬ğ¥¹™•ÉÉ•‘€°¹…µ•¥¸Ñ¡”¹½Ñ”ğ)ğ€¨©‰É¥‘”Á½Í¥Ñ¥½¹Ì¨¨ğ€¨©½¹±•ä½MÑ•±é•È€ÄàÌÌ¨¨ƒŠP¥Ğ‘É…İÌÑ¡•´¥¸Á±…”ğ¥¹™•ÉÉ•‘€ğ)ğ•¹•É…°É½ÍÌµ¡•¬½¸…±°½˜Ñ¡”…‰½Ù”ğ…¸€ÄàÌØµ…ÀƒŠP€¨©¹½Ğå•Ğ¥¸‘…Ñ„½Í½ÕÉ•Ì½€ì™¥¹…¹É•½É½¹”™¥ÉÍĞ¨¨ğƒŠPğ()Q¡”ÍÑ…¹‘¥¹œÉÕ±”ÍÑ¥±°¡½±‘Ìİ¡•É”¥Ğ•…É¹Ì¥ÑÌ­••Àè¹½Ñ¡¥¹œÑÉ…•™É½´„Á¥Ñ½É¥…°)Í¡••Ğ‰•½µ•Ì…¸€©½ÕÑ±¥¹”¨¸É•½¹ÍÑÉÕÑ¥½¸Ñ•±±Ìå½Ô„‰É¥‘”İ…Ì¡•É”ì¥Ğ‘½•Ì¹½ĞÑ•±°)å½Ô¥ÑÌÁ±…¸¸A½Í¥Ñ¥½¸¥¹™•ÉÉ•‘€İ¥Ñ „¹½Ñ”°•½µ•ÑÉä™É½´Ñ¡”…É¡•ÑåÁ”¸((¨©¼¹½Ğ±•Ğƒ
ÄÈÀ´ÍÑ½ÀÑ¡”İ½É¬¸¨¨Q¡”Õ¹•ÉÑ…¥¹Ñä¥ÌÉ•½É‘•Á•ÈÍÑÉÕÑÕÉ”…¹Í¡½İ¸¥¸)Ñ¡”Á½ÁÕÀìÑ¡…Ğ¥ÌÑ¡”µ•¡…¹¥Í´™½È¡…¹‘±¥¹œ¥Ğ¸1•…Ù¥¹œÑ¡”•…ÍĞ¡…±˜½˜Ñ¡”Ñ½İ¸•µÁÑä)‰•…ÕÍ”Ñ¡”Í¡½É”…¹¹½Ğ‰”™¥á•Ñ¼Ñ¡”µ•ÑÉ”¥ÌÑ¡”µ½É”µ¥Í±•…‘¥¹œ½˜Ñ¡”Ñİ¼½ÁÑ¥½¹Ì¸((¨©M½Á”°¹½Üµ•…ÍÕÉ•½™˜Ñ¡”Í¡••ĞÉ…Ñ¡•ÈÑ¡…¸Õ•ÍÍ•¸¨¨¥ÉÍĞÉ•…‘¥¹Ì…É”½µµ¥ÑÑ•¥¸)‘…Ñ„½ÑÉ…•Ì½Ù•Ñ½ÉÌ½İÉ¥¡Ñ|ÄàÌÑ}•…ÍĞ¹©Í½¹€°‘•É¥Ù•‰äÑ½½±Ì½İÉ¥¡Ñ}Áà¹Áå€™É½´Ñ¡”Í…µ”)™¥ÑÑ•…™™¥¹”Ñ¡”‘…ÑÕ´¥Ì¡•­•……¥¹ÍĞè()ğ™•…ÑÕÉ”°™É½´]É¥¡Ğ€ÄàÌĞğ±½…°ğ±½…°8ğ)ğ´´µğ´´µğ´´µğ)ğ½ÉĞ•…É‰½É¸€¡±…‰•°•¹ÑÉ”¤ğ€¨¨¬ÄÄÔÈ¨¨ğ€¬ÈÈÄğ)ğÉ¥Ù•Èµ½ÕÑ °Í½ÕÑ ‰…¹¬ğ€¬ÄÄàÀğ€¬ÈÜÈğ)ğ±…­”Í¡½É”¹½ÉÑ ½˜Ñ¡”¡…É‰½ÕÈğ€¨¨¬ÄÌÌÄƒŠ˜€¬ÄÌØÔ¨¨ğ€¬ÌÌÀƒŠ˜€¬ÜÌÔğ)ğ¹½ÉÑ Á¥•È°½ÕÑ•È•¹ğ€¨¨¬ÄÔĞĞ¨¨ğ€¬ÄÜàğ()M¼Ñ¡”‰½àµÕÍĞÉ•… …‰½ÕĞ€¨©€¬ÄÜÀÀ¨¨°¹½ĞÑ¡”€¬ÄÔÀÀ$™¥ÉÍĞ•ÍÑ¥µ…Ñ•ƒŠPÑ¡”¡…É‰½ÕÈ)İ½É­ÌÉÕ¸™ÕÉÑ¡•È½ÕĞÑ¡…¸Ñ¡”Í¡½É”‘½•Ì¸Q¡…Ğ¥Ù•Ì„øÈ¸À­´ƒ\€À¸Ü­´™¥•±ì…ĞÑ¡”)ÕÉÉ•¹Ğ€È¸Ô´•±°°øÈÈÑ¬Í…µÁ±•Ì€¡øĞÔÀ-¥¹ĞÄØ¤……¥¹ÍĞÑ½‘…äÌ€ØÙ¬€ ÄÌÈ-¤¸]•±°¥¹Í¥‘”)Ñ¡”€ÈÔ5ÁÕ‰±¥Í ‰Õ‘•Ğ°‰ÕĞİ½ÉÑ „½…ÉÍ•È•±°•…ÍĞ½˜Ñ¡”‰Õ¥±Ğ‰±½­Ì°İ¡•É”Ñ¡”)•Ù¥‘•¹”‘½•Ì¹½ĞÍÕÁÁ½ÉĞ€È¸Ô´‘•Ñ…¥°…¹åİ…ä¸()Qİ¼Ñ¡¥¹ÌÑ¡”™¥ÉÍĞÁ…ÍÌÍ•ÑÑ±•°…¹½¹”¥Ğ‘¥¹½Ğè((´€¨©Q¡”½ÉĞ•…É‰½É¸Á½Í¥Ñ¥½¸¥ÌÉ½ÍÌµ¡•­•¸¨¨]É¥¡ĞÁÕÑÌ¥Ğ…Ğ€¬ÄÄÔÈ°8€¬ÈÈÄìÑ¡”(€µ½‘•É¸ÍÕ•ÍÍ½È±…¹‘µ…É¬€¡5¥¡¥…¸Ù•¹Õ”‰É¥‘”¤¥¹‘•Á•¹‘•¹Ñ±ä¥Ù•Ì€¬ÄÄÈÜ°8€¬ÄäÔ¸(€€ÌÔ´…Á…ÉĞ°™É½´µ•Ñ¡½‘ÌÍ¡…É¥¹œ¹¼¥¹ÁÕĞ¸Q¡…Ğ¥Ìİ¡…Ğ±¥•¹Í•Ì¥¹™•ÉÉ•‘€¸(´€¨©]É¥¡Ğ±…‰•±ÌÑ¡”É•Í•ÉÙ…Ñ¥½¸°¹½ĞÑ¡”™½ÉĞ¸¨¨Q¡•É”¥Ì¹¼Á…±¥Í…‘”Á±…¸½¸Ñ¡¥ÌÍ¡••Ğ°(€Í¼Ñ¡”™½½ÑÁÉ¥¹Ğ¡…ÌÑ¼½µ”™É½´•±Í•İ¡•É”ƒŠP¹‘É•…Ì°½ÈÑ¡”™½ÉĞÌ½İ¸ÁÕ‰±¥Í¡•Á±…¹Ì¸(€¼¹½ĞÑÉ…”…¸½ÕÑ±¥¹”½™˜Ñ¡”‰…¹¹•È¸(´€¨©Q¡”Í…¹‰…È…¹Ñ¡”½±Í½ÕÑ¡İ…É¡…¹¹•°…É”¹½ÜÉ•…¨¨€¡Í•½¹Á…ÍÌ°Í…µ”‘…ä¤¸Q¡É•”(€¥¹¬±¥¹•Ì°¹•ÍÑ•İ•ÍĞÑ¼•…ÍĞèÑ¡”µ…¥¹±…¹‰…¹¬½˜Ñ¡”‘•…å¥¹œ½±¡…¹¹•°°Ñ¡”‰…ÈÌ(€¡…¹¹•°Í¥‘”°…¹Ñ¡”‰…ÈÌ±…­”µ™…¥¹œÍ¥‘”¸¡•­•™½È½¡•É•¹”É…Ñ¡•ÈÑ¡…¸•å•‰…±±•(€ƒŠP…Ğ•Ù•ÉäÍ…µÁ±•¹½ÉÑ¡¥¹œÑ¡”Ñ¡É•”¹•ÍĞ¥¸½É‘•È…¹Ñ¡”‰…È½µ•Ì½ÕĞ€ÜÇŠLÄÜÄ´İ¥‘”°(€¹…ÉÉ½İ¥¹œÑ¼¥ÑÌÍ½ÕÑ¡•É¸¡½½¬°İ¡¥ ¥Ìİ¡…Ğ„±¥ÑÑ½É…°ÍÁ¥ĞÍ¡½Õ±‘¼¸U¹•ÉÑ…¥¹Ñä¥Ì(€É•½É‘•…Ğ€ÌÀ´É…Ñ¡•ÈÑ¡…¸Ñ¡”Í¡½É”Ì€ÈÔèÑ¡•Í”…É”¥¹¬±¥¹•Ì½Ù•È„İ…Í °…¹Ñ¡”(€Í½ÕÑ¡•É¸¡½½¬¥ÌÑ¡”±•…ÍĞ•ÉÑ…¥¸Í¡…Á”¥¸Ñ¡¥ÌÅÕ…‘É…¹Ğ¸((¨©Q¡”½…ÍÑ±¥¹”…Ñ”¥ÌÑ¡•É•™½É”±•…É•¸¨¨M¡½É”°¡…É‰½ÕÈÁ¥•ÉÌ°Í…¹‰…È…¹½±¡…¹¹•°)…É”…±°¥¸‘…Ñ„½ÑÉ…•Ì½Ù•Ñ½ÉÌ½İÉ¥¡Ñ|ÄàÌÑ}•…ÍĞ¹©Í½¹€¥¸±½…°9T¸]¡…ĞLÉ”ÍÑ¥±°¹••‘Ì¥Ì)Ñ¡”€©¡•¥¡Ñ™¥•±¨İ½É¬ƒŠP•áÑ•¹‘¥¹œÑ¡”é½¹”Ñ…‰±”•…ÍĞ½Ù•ÈøÈ¸À­´ƒ\€À¸Ü­´°İ¥Ñ Ñ¡”‰…È)…ÌÍ…¹…¹Ñ¡”½±¡…¹¹•°…Ìİ…Ñ•ÈƒŠP¹½Ğµ½É”ÑÉ…¥¹œ¸()U¹‰±½­ÌÑ¡”€¨©½ÉĞ•…É‰½É¸¨¨…¹€¨©!…É‰½Èİ½É­Ì¨¨Á…É•±Ì¥¸LÔ°İ¡¥ …¹¹½Ğ‰”Á±…•)½¹Ñ¼É½Õ¹Ñ¡…Ğ‘½•Ì¹½Ğ•á¥ÍĞ¸%Ğ…±Í¼É•Ñ¥É•ÌÑ¡”…•É¥…°Ù¥•ÜÌİ½ÉÍĞ…ÉÑ•™…Ğè™É½´(ÄÔÀ´ÕÀå½ÔÕÉÉ•¹Ñ±äÍ•”Ñ¡”É½Õ¹Í¥µÁ±ä•¹¸()A…É•±Ì€¡Á…É…±±•°½¹”LÄ±…¹‘Ì¤è((´€¨¨¡„¤M¡½É•±¥¹”€¬É¥Ù•ÈÙ•Ñ½ÉÌ¨¨ƒŠP€¨©=9€ÈÀÈØ´Àà´ÄÀ¸¨¨Ñ½½±Ì½ÑÉ…•}Í¡½É•±¥¹”¹Áå€ƒŠH(€‘…Ñ„½Ñ•ÉÉ…¥¸½•Á½¡Ì½”ÄàÌÑ}¡…É‰½É}ÕĞ½Í¡½É•±¥¹”¹•½©Í½¹€èÑ¡”µ…¥¸ÍÑ•´™É½´Ñ¡”‰½à•‘”(€•…ÍĞ°Ñ¡”€ÄàÌĞÕĞ‰•Ñİ••¸¥ÑÌÁ¥•ÉÌ°Ñ¡”½±Í½ÕÑ¡İ…É¡…¹¹•°°Ñ¡”€¨©Í…¹‰…È…Ì…¸(€¥Í±…¹¨¨€¡Ñ¡”İ…Ñ•ÈÁ½±å½¸Ì¥¹Ñ•É¥½ÈÉ¥¹œ¤°…¹Ñ¡”µ…¥¹±…¹±…­”Í¡½É”ƒŠP€È€ĞØØ´½˜Í½ÕÑ (€Í¡½É”°€Ä€ÔØà´½˜¹½ÉÑ Í¡½É”°„€Ä¸Ô­´‰…ÈÁ•É¥µ•Ñ•È°…±°½™˜Ñ¡”Í…µ”]É¥¡Ğ€ÄàÌĞÍ¡••Ğ(€Ñ¡É½Õ Ñ¡”Í…µ”…™™¥¹”°ƒ
ÄÈÀ´¸5•µ¼è‘½Ì½IMI ½Í¡½É•±¥¹•}¡…É‰½É|ÄàÌĞ¹µ‘€¸Qİ¼‰½Õ¹‘…Éä(€ÉÕ¹Ìİ•É”™½Õ¹…¹‘É½ÁÁ•½¸ÁÕÉÁ½Í”èÑ¡”½ÕÑ•È•‘”½˜Ñ¡”±…­”İ…Í ¥Ìİ¡•É”Ñ¡”(€‘É…Õ¡ÑÍµ…¸ÍÑ½ÁÁ•İ…Í¡¥¹œ°¹½Ğ„½…ÍĞ¸€¨©5•…ÍÕÉ•°İ¡¥ ¡…¹•ÌÑ¡”‰½àè¨¨Ñ¡”µ…¥¹±…¹(€Í¡½É”É•…¡•Ì€¬ÄÈÔÜ…¹Ñ¡”‰…ÈÌ•…ÍĞ•‘”€¬ÄĞäÜ°Í¼Ñ¡”ÁÉ½Á½Í•€¬ÄÔÀÀ±¥ÁÌÑ¡”‰…È‰ä(€€Ì´ƒŠP€¨©ÕÍ”€¬ÄÔØÀ¨¨°¥¹Í¥‘”Ñ¡”ÑÉ…•İ¥¹‘½ÜÌ€¬ÄÔÜÀ¸Q¡”Ñİ¼İ¥¹‘½İÌ½Ù•É±…À‰ä€àÀ´…¹(€…É•”Ñ¡•É”Ñ¼€À¸ÇŠLÔ¸Ü´°İ¡¥ ¥ÌÑ¡”¡•¬Ñ¡…ĞÑ¡”Í•µ•¹Ñ…Ñ¥½¸¥ÌÉ•…‘¥¹œÑ¡”µ…ÀÉ…Ñ¡•È(€Ñ¡…¸¥ÑÌ½İ¸Á…É…µ•Ñ•ÉÌ¸9½Ğå•Ğ½¹ÍÕµ•‰äÑ•ÉÉ…¥¹}•¸¹Áå€ì¥Ğ¥ÌÑ¡”•Ù¥‘•¹”°¹½ĞÑ¡”(€É½Õ¹¸(´€¨¨¡ˆ¤!•¥¡Ñ™¥•±¨¨ƒŠPÑ¡”€ÌÀµé½¹”Ñ…‰±”¥¸‘½Ì½É•Í•…É ¼ÀÄµÑ•ÉÉ…¥¸µ¡å‘É½±½ä¹µ‘€°ÅÕ…¹Ñ¥é•ƒŠ&À¸ÈÔ™Ğ…Ğ€×ŠLÄÀ™Ğ•±±Ì¸=¹”Ñ¡¥¹œÑ¡¥ÌÁ…É•°¹¼±½¹•È¡…ÌÑ¼‰Õ‘•Ğ™½È€ ÈÀÈØ´Àà´ÄÀ°MQQULƒ
œ€ÌĞ¤è€¨©ÁÉ½Í”¥¸Ñ•ÉÉ…¥¹}ÍÁ•Œ¹©Í½¹€¥Ì½ÕĞ½˜Ñ¡”Ñ•ÉÉ…¥¸ÌÍÑ…±•¹•ÍÌ¡…Í ¨¨°Í¼„é½¹”ÌÉ•…Í½¹¥¹œ°…Ù•…Ğ½È¥Ñ…Ñ¥½¸…¸‰”İÉ¥ÑÑ•¸°…ÉÕ•…¹É•İÉ¥ÑÑ•¸İ¥Ñ¡½ÕĞ„‰…­”ƒŠP…¹¥ĞµÕÍĞ‰”°‰•…ÕÍ”…¸¥¹™•ÉÉ•‘€É½Õ¹±…¥´İ¥Ñ ¹¼ÍÑ…Ñ•É•…Í½¹¥¹œ¥Ì¹½Ü…¸•ÉÉ½ÈÉ…Ñ¡•ÈÑ¡…¸„İ…É¹¥¹œ¸¹Õµ‰•È°…¸¥½È„½¹™¥‘•¹”ÍÑ¥±°ÍÑ…±•ÌÑ¡”É½Õ¹°Í¼Ñ¡”ÍÁ•ŒÌ™¥ÕÉ•Ì…¹Ñ¡”‰…­”…É”ÍÑ¥±°½¹”Í±¥”¸hôÀ…ĞÑ¡”€ÄàÌÔ±…­”ÍÕÉ™…”¸€¨©9•áĞÍ±¥”¨¨°…¹¥Ğ¹••‘Ì„‰…­”™½ÈÑ¡”É½Õ¹1°Í¼É•½É€¬µ•Í ±…¹Ñ½•Ñ¡•È¸Qİ¼Ñ¡¥¹ÌÁ…É•°€¡„¤¡…¹‘Ì¥ĞèÑ¡”‰…È¥Ì€©±…¹¥¹Í¥‘”İ…Ñ•È¨°Í¼Ñ¡”Í¥¹•µ‘¥ÍÑ…¹”ÉÕ±”Ñ¡…Ğ‰Õ¥±‘ÌÑ¡”™½É­ÌÉ½Õ¹¡…ÌÑ¼Õ¹‘•ÉÍÑ…¹¥Í±…¹‘Ì°¹½Ğ½¹±ä‰…¹­Ìì…¹¹¼•±•Ù…Ñ¥½¸™½ÈÑ¡”‰…È•á¥ÍÑÌ¥¸…¹äÍ½ÕÉ”°Í¼¥ÑÌ¡•¥¡Ğ¥Ì„ÍÁ•Œ…ÉÕµ•¹ĞÑ¼‰”µ…‘”¥¸Ñ¡”½Á•¸°¹½Ğ„¹Õµ‰•ÈÑ¼Á¥¬¸(´€¨¨¡Œ¤!å‘É½±½ä¨¨ƒŠPÑ¡”Í±½Õ €¡ÁÕ‰±¥ŒµÍÅÕ…É”Á½¹ƒŠHÁ…ÍĞ1…­”€˜•…É‰½É¸ƒŠHÉ¥Ù•È…ĞÑ¡”™½½Ğ½˜MÑ…Ñ”¤°É½œA½¹…Ğ1…­”€˜1…M…±±”°Ñ¡”]•±±ÌMÑÉ••Ğµ…ÉÍ °Ñ¡”µ…ÉÍ¡äÉ¥Ù•ÈµÍ¡½É”ÍÑÉ¥À¸(´€¨¨¡¤Ñ•ÉÉ…¥¹}•¸¹Áå€¨¨ƒŠPÍÁ•Œ€¬Ù•Ñ½ÉÌƒŠHÑ•ÉÉ…¥¸µ•Í €¬¡•¥¡Ñ™¥•±¹‰¥¹€™½È½±±¥Í¥½¸¸()I•µ¥¹‘•ÈèÁ¥•ÉÌ…¹‰É¥‘•Ì…É”€¨©ÍÑÉÕÑÕÉ•Ìİ¥Ñ Á¡…Í•Ì¨¨°¹½ĞÑ•ÉÉ…¥¸€¡Í•”‘½Ì½A=!L¹µ‘€¤¸((ŒŒHÄƒŠPI•¹‘•É•ÈÍ¡•±°ƒ
Ü€©…¸ÍÑ…ÉĞ¹½Ü°¹••‘Ì¹¼‘…ÑÕ´¨()A…É•±Ìè€¡„¤Í¡•±°€¬¥¹ÁÕĞµ¥¹Ñ•¹Ğ±…å•È€¬İ…±­•Èì€¡ˆ¤½¹™¥‘•¹”Í¡…‘•È€¬ÁÉ½Ù•¹…¹”Á½ÁÕÀ)……¥¹ÍĞ„¡…¹µİÉ¥ÑÑ•¸Ñ•ÍĞÍ¥‘•…Èì€¡Œ¤Ñ½½±Ì½Íµ½­”¹µ©Í€¸()	Õ¥±……¥¹ÍĞÍå¹Ñ¡•Ñ¥Œ•½µ•ÑÉä…¹™±…ĞÉ½Õ¹¸½¹ÑÉ…Ğ¥¸‘½Ì½A18¹µ‘€¸5½‰¥±”( ÌäÃ\ÜàÀ¤¥Ì„É•±•…Í”…Ñ”™É½´Ñ¡”™¥ÉÍĞİ…±­…‰±”½µµ¥ĞƒŠPÉ•ÑÉ½™¥ÑÑ¥¹œÑ½Õ ¥¹Ñ¼„€Í)İ…±­Ñ¡É½Õ ±…Ñ•È¥ÌÑ¡”•áÁ•¹Í¥Ù”İ…äÑ¼‘¼¥Ğ¸((ŒŒHÈƒŠPI•¹‘•É¥¹œÁÉ½É…´ƒ
Ü€¨©Q%YƒŠP½İ¹•ÈÉ•Ù¥•İ•…¹µ•É•€ÈÀÈØ´Àà´ÄĞ€¡AH€ŒÄÀØ¤¨¨()Q¡”Á¡…Í•Á±…¸™½È¡¥¡•Èµ™¥‘•±¥ÑäÉ•¹‘•É¥¹œƒŠPQÉ…¬€Ä€¡İ…±¬½€¥µÁÉ½Ù•¥¸Á±…”è±¥¡Ğ°)Ñ•áÑÕÉ•Ì°<°…Í…‘•Ì°…Ñµ½ÍÁ¡•É”°İ…Ñ•È°½¹Ñ•¹Ğ¤°QÉ…¬€È€¡„Í•½¹¡¥ µ™¥‘•±¥Ñäİ•ˆ)É•¹‘•É•È…Ğİ…±¬µ¡½€¤°QÉ…¬€Ì€¡„¹…Ñ¥Ù”µ•¹¥¹”É•¹‘•É•È¤ƒŠP±¥Ù•Ì¥¸‘½Ì½I9I%9¹µ‘€°)İ¥Ñ Á•ÈµÁ¡…Í”…Ñ•Ì°…•ÁÑ…¹”¹Õµ‰•ÉÌ…¹ÉÕ¹¹•ÈÉ½ÕÑ¥¹œ¸((¨©Q¡”\ÑÉ…¬…¹À…É”‰Õ¥±‘…‰±”¹½Ü¸ …¹8ÍÑ…ä…Ñ•¨¨‰•¡¥¹Ñ¡”=]9H%M%=9€)¥Ñ•µÌ¥¸I9I%9ƒ
œà°…Ì‘¼Ñ¡”½Á•¸‰Õ‘•Ğ…¹‘¥ÍÑÉ¥‰ÕÑ¥½¸ÅÕ•ÍÑ¥½¹Ì¸Q¡”±…¥µ…‰±”)Á…É•±Ì…É”Ñ¡”€¨©I9I%9±…¹”¨¨‰•±½Üì•… ½¹”¹…µ•Ì¥ÑÌI9I%9Á¡…Í”°¥ÑÌ™¥±”±¥ÍĞ°)¥ÑÌ…•ÁÑ…¹”¹Õµ‰•ÉÌ…¹¥ÑÌÉÕ¹¹•È¸((¨©Ù•ÉåÑ¡¥¹œ±…¹‘Ì½¸‘•Ù€¨¨€¡‘½Ì½A%A1%9¹µ‘€¤¸AÉ½‘ÕÑ¥½¸µ½Ù•Ì½¹±äİ¡•¸Ñ¡”½İ¹•È)‘¥ÍÁ…Ñ¡•Ì¡¥…¼´ÑµÁÉ½µ½Ñ”µÑ¼µÁÉ½¹åµ±€¸((ŒŒLÌƒŠP5¥±•ÍÑ½¹”€ÀèÑ¡”M…Õ…¹…Í °•¹Ñ¼•¹()•™¥¹¥Ñ¥½¸½˜‘½¹”¥¸‘½Ì½A18¹µ‘€¸Q¡”É•½É°Ñ¡”Í½ÕÉ•Ì°…¹Ñ¡”‘½ÍÍ¥•È…É”…±É•…‘ä)İÉ¥ÑÑ•¸ìİ¡…ĞÉ•µ…¥¹Ì¥ÌÑ¡”™É…µ•}Ñ…Ù•É¹€…É¡•ÑåÁ”°Ñ¡”™¥ÉÍĞ‰…­”°…¹Ñ¡”İ…±­…‰±”Á…”)İ¥Ñ „İ½É­¥¹œ½¹™¥‘•¹”Ñ½±”¸()MÕ•ÍÌ¥Ì¹½Ğ€‰„‰Õ¥±‘¥¹œ…ÁÁ•…ÉÌˆ¸MÕ•ÍÌ¥ÌÑ¡…Ğ„Ù¥•İ•È…¸Ñ½±”Ñ¡”½¹™¥‘•¹”Ù¥•Ü)…¹Í•”•á…Ñ±äİ¡¥ Á…ÉÑÌ½˜Ñ¡”M…Õ…¹…Í İ”…¸‘•™•¹ƒŠPÑ¡”İ¡¥Ñ”Ñİ¼µÍÑ½Éä‰±½¬…¹Ñ¡”)‰±Õ”Í¡ÕÑÑ•ÉÌÍ½±¥°Ñ¡”¥¹Ù•¹Ñ•™½½ÑÁÉ¥¹Ğ…¹Ñ¡”‘¥ÍÁÕÑ•…±±•Éä‘¥Ñ¡•É•¸((ŒŒLäƒŠPMÑÉ••ÑÌ°É½…‘Ì…¹Á…Ñ¡Ìƒ
Ü€¨©Y%M%	1IQ 1eH€¬1%Y95L=9€ÈÀÈØ´Àà´ÄÄ¨¨()Í­•™½È…Ì€‰ÍÑÉ••ÑÌ°É½…‘Ì°Á…Ñ¡Ì¥¸…ÕÉ…Ñ”ÍÕÉ™…”…¹•±•Ù…Ñ¥½¹Ìˆ°Ñ¡•¸•áÁ…¹‘•Ñ¼„)Ñ½±•…‰±”€ÄàÌÔ½ÕÉÉ•¹Ğµ¹…µ”É•…‘½ÕĞ¸Q¡”™¥ÉÍĞ‘…Ñ•Ù¥Í¥‰±”±…å•È¥Ì¹½Ü¥¸èÍ•Ù•¹Ñ••¸•…ÉÑ )ÑÉ…Ù•±İ…åÌ½µÁ¥±•¥¹Ñ¼Ñ¡”Í•¹”¥¹‘•à°‘É…Á•½¸Ñ¡”¡•¥¡Ñ™¥•±°ÕĞ…Ğİ…Ñ•È°±•…É•½¹±ä)Ñ¡É½Õ Ñ¡”¹…ÉÉ½ÜÑÉ…Ù•±±•ÍÑÉ¥À°‘É…İ¸½¸Ñ¡”½Ù•ÉÙ¥•Üµ…À…¹ÅÕ•É¥•±¥Ù”™½ÈÑ¡”ÍÑÉ••Ğ)Õ¹‘•É™½½Ğ½ÈÑ¡”¹•áĞÉ½ÍÌÍÑÉ••Ğ…¡•…¸Q¡”É•µ…¥¹¥¹œİ½É¬¥ÌÑ¼•áÑ•¹½¹ÑÉ½°½¸9½ÉÑ ]…Ñ•È)…¹Ñ¡”¹½ÉÑ µÍ¥‘”É¥°É•Í•…É …¹ä‘…Ñ•Á±…¹¬™½½Ñİ…±­ÌÍ•Á…É…Ñ•±ä°…¹É•Á±…”0ÜäÌÙ¥ÍÕ…°)İ•…Èİ¥‘Ñ¡Ìİ¡•É•Ù•È„ÍÁ•¥™¥…Ñ¥½¸½È‘•Á¥Ñ¥½¸ÍÕÉÙ¥Ù•Ì¸((¨©!…±˜½˜Ñ¡…ĞÍ•¹Ñ•¹”¥Ì½µµ¥ÑÑ•‘…Ñ„…Ì½˜€ÈÀÈØ´Àà´ÄÀ¸¨¨‘…Ñ„½ÑÉ…•Ì½ÍÑÉ••Ñ}½¹ÑÉ½°¹©Í½¹€)¡½±‘ÌÑ¡”µ½‘Õ±”€ àÀ™ĞÍÑÉ••ÑÌ°¥¹™•ÉÉ•‘€°İ¥Ñ Ñ¡”€ØØ™Ğ‘¥ÍÍ•¹ĞÉ•½É‘•‰•Í¥‘”¥Ğ¤…¹Ñ¡”)½¹ÑÉ½°Ñ…‰±”Ñ¡¥ÌÁÉ½©•Ğ…ÑÕ…±±äÍ¹…ÁÌÑ¼°•… ÍÑÉ••Ğ…ÉÉå¥¹œ¥ÑÌ…á¥Ì…¹¥ÑÌµ½‘•É¸)•ÅÕ¥Ù…±•¹ĞƒŠP…¹°Í¥¹”€ÈÀÈØ´Àà´ÄÀ°Ñ¡”ÉÕ±”Ñ¡…Ğµ…­•Ì„½¹ÑÉ½°Á½¥¹ĞÉ”µ‘•É¥Ù…‰±”É…Ñ¡•ÈÑ¡…¸)µ•É•±äÉ”µ™•Ñ¡…‰±”€¡¹½‘•}ÉÕ±•€èÑ¡”¹½‘•ÌÍ¡…É•‰äÑ¡”Ñİ¼¹…µ•ÍÕÉ™…”É½…‘İ…åÌ°…Ù•É…•°)İ¥Ñ ‰¥­•İ…åÌ…¹ÍÑ…­•±½İ•Èµ±•Ù•°ÍÑÉ••ÑÌ•á±Õ‘•¤¸]¡…Ğ¥ÌÍÑ¥±°µ¥ÍÍ¥¹œ™½ÈÑ¡¥ÌÁ…É•°¥Ì)Ñ¡”Á±…ĞÌ€¨©‰±½¬‘¥µ•¹Í¥½¹Ì…¹•áÑ•¹Ğ¨¨ƒŠPÑ¡…Ğ™¥±”¡½±‘Ì½¹±äİ¡…ĞÑ¡”•á¥ÍÑ¥¹œÁ±…•µ•¹ÑÌ)ÕÍ•¸M•”‘½Ì½IMI ½ÍÑÉ••Ñ}µ½‘Õ±•|ÄàÌÀ¹µ‘€¸((¨©¹Ñ¡”µ½‘Õ±”¥Ìµ•…ÍÕÉ•É…Ñ¡•ÈÑ¡…¸…¹¹½Ñ…Ñ•°€ÈÀÈØ´Àà´ÄÀ¨¨€¡MQQULƒ
œ€ĞÈ°)‘½Ì½IMI ½ÍÑÉ••Ñ}µ½‘Õ±•|ÄàÌÀ¹µ‘€ƒ
œ€à°‘…Ñ„½ÑÉ…•Ì½Ù•Ñ½ÉÌ½ÍÑÉ••Ñ}½ÉÉ¥‘½ÉÍ|ÄàÌĞ¹©Í½¹€¤¸)¥¡ĞÁ±…ÑÑ•½ÉÉ¥‘½ÉÌÉ•…½™˜	=Q €ÄàÌĞÍ¡••ÑÌ°€ÜÔ¸Ü´äÈ¸à™Ğ°¹½¹”İ¥Ñ¡¥¸€ä™Ğ½˜€ØØèÑ¡”)‘¥ÍÍ•¹Ğ¥Ì•á±Õ‘•…¹Í¼¥ÌÑ¡”É•½¹¥±¥…Ñ¥½¸Ñ¡…Ğ¥Ğµ¥¡Ğ‰”…‰½ÕĞ‘¥™™•É•¹ĞÍÑÉ••ÑÌ¸Qİ¼)Ñ¡¥¹ÌÑ¡¥ÌÁ…É•°¥¹¡•É¥ÑÌ¸¥ÉÍĞ°„€¨©µ•…ÍÕÉ•‰±½¬Á¥Ñ ¨¨ƒŠPÍ•Ù•¸½¹Í•ÕÑ¥Ù”½ÉÉ¥‘½È)ÍÁ…¥¹Ì½˜€ÄÄØ¸Ø´ÄÈÌ¸È´°Ñ¡”€ÌÀÀ™Ğ‰±½¬Á±ÕÌ½¹”ÍÑÉ••ĞƒŠPİ¡¥ ¥ÌÑ¡”‰•¥¹¹¥¹œ½˜Ñ¡”‰±½¬)‘¥µ•¹Í¥½¹ÌÑ¡¥ÌÍ•Ñ¥½¸…Í­Ì™½È°Ñ¡½Õ ¹½Ğå•ĞÑ¡”Á±…ĞÌ•áÑ•¹Ğ¸M•½¹°„€¨©µ•Ñ¡½ÁÉ½‰±•´Ñ¼)Í½±Ù”‰•™½É”Ñ¡”µ\ÍÑÉ••ÑÌ…¸‰”µ•…ÍÕÉ•¨¨èÑ¡”8µLÑÉ…Ù•ÉÍ”É•…‘Ì]É¥¡ĞÌ±½Ğ±¥¹•Ì°İ¡½Í”)‘•ÁÑ¡Ì…É”„Á±…ÑÑ•ÍÑÉ••ĞÌİ¥‘Ñ …¹İ¡½Í”±¥¹•ÌÉÕ¸…Ì™…È…Ì„‰±½¬™…”‘½•Ì°Í¼„½ÉÉ¥‘½È)¡•É”¡…ÌÑ¼‰”¥‘•¹Ñ¥™¥•‰äÍ½µ•Ñ¡¥¹œ½Ñ¡•ÈÑ¡…¸¥ÑÌİ¥‘Ñ ¸1…­”°I…¹‘½±Á °M½ÕÑ ]…Ñ•È…¹)5…É­•Ğ…É”Õ¹µ•…ÍÕÉ•Õ¹Ñ¥°Ñ¡…Ğ•á¥ÍÑÌ¸((¨©M=1Y€ÈÀÈØ´Àà´ÄÄ¨¨€¡MQQULƒ
œ€ÔÈ°µ•µ¼ƒ
œ€ÄÀ¤¸Q¡”Ñ¡É•”Ñ•ÍÑÌÑ¡…Ğ™…¥±•…É”…±°É•…‘¥¹Ì)Ñ…­•¸€©…É½ÍÌ¨„…¹‘¥‘…Ñ”…Ğ½¹”Á±…”ìÑ¡”½¹”Ñ¡…Ğİ½É­ÌÑÕÉ¹Ì¹¥¹•Ñä‘•É••Ì…¹…Í­Ì¡½Ü™…È)„…¹‘¥‘…Ñ”¥Ì½Á•¸É½Õ¹€¨©‘½İ¸¥ÑÌ½İ¸•¹ÑÉ•±¥¹”¨¨°İ¡¥ „ÍÑÉ••Ğ¥Ì™½È„İ¡½±”‰±½¬…¹„)ÍÑÉ¥À½˜±½ÑÌ¹•Ù•È¥Ì¸Q¡”Ñ¡É•Í¡½±¥Ì‘•É¥Ù•™É½´Ñ¡”µ½‘Õ±”‰…¹€ äÔƒŠ"H€ÌÀ€ô€ØÔ´¤É…Ñ¡•È)Ñ¡…¸ÑÕ¹•¸€¨©1…­”É•…‘Ì€Üä¸Ğ™Ğ…¹I…¹‘½±Á €àÄ¸Ô™Ğ¨¨½¸]É¥¡ĞƒŠP‰½Ñ ¹…µ•‰äÑ¡•¥È½µµ¥ÑÑ•)µ½‘•É¸©Õ¹Ñ¥½¹ÌÑ¼€À¸ä´°¹½Ğ‰ä½Õ¹Ñ¥¹œƒŠPİ¥Ñ ½¹”Õ¹¹…µ•½ÉÉ¥‘½È„‰±½¬™ÕÉÑ¡•ÈÍ½ÕÑ …Ğ(àØ¸Ô™ĞìÑ•¸±½ĞÍÑÉ¥ÁÌİ•É”É•©•Ñ•…¹¹½¹”½˜Ñ¡”•¥¡Ğ…±É•…‘äµ½µµ¥ÑÑ•½ÉÉ¥‘½ÉÌİ…Ì¸)Q¡É•”Ñ¡¥¹ÌÑ¡¥ÌÁ…É•°¥¹¡•É¥ÑÌ™É½´¥Ğ¸€¨©Q¡”µ\Á¥Ñ ¥Ì€ÄÌĞ´ÄÌØ´……¥¹ÍĞ€ÄÄØ¸Ø´ÄÈÌ¸È´Ñ¡”)½Ñ¡•Èİ…ä¨¨°Í¼Ñ¡”‰±½­Ì…É”9=PÍÅÕ…É”…¹Ñ¡”€ÌÀÀ™Ğ‰±½¬Ñ¡…Ğ™¥ÑÌÑ¡”8µLÍÑÉ••ÑÌ‘½•Ì¹½Ğ)‘•ÍÉ¥‰”Ñ¡•´ƒŠPÑ¡…Ğ¥ÌÑ¡”É•ÍĞ½˜Ñ¡”‰±½¬‘¥µ•¹Í¥½¹ÌÑ¡¥ÌÍ•Ñ¥½¸…Í­Ì™½È°…¹¥Ğ½µ•Ì½™˜)Ñİ¼ÍÁ…¥¹Ì½¸½¹”Í¡••Ğ°Í¼µ•…ÍÕÉ”µ½É”‰•™½É”•¹•É…Ñ¥¹œ„É¥™É½´¥Ğ¸€¨©Q¡”µ\İ¥‘Ñ¡Ì)É•ÍĞ½¸½¹”Í¡••Ğ¨¨è!…Ñ¡…İ…äÌ8µLÑÉ…Ù•ÉÍ”½µµ¥ÑÌ¹½Ñ¡¥¹œ°Í¼Ñ¡•ä¡…Ù”¹¼É½ÍÌµ¡•¬¸¹(¨©M½ÕÑ ]…Ñ•È…¹5…É­•Ğ…É”ÍÑ¥±°Õ¹µ•…ÍÕÉ•¨¨ƒŠP5…É­•Ğ™…±±Ì½ÕÑÍ¥‘”‰½Ñ ÑÉ…Ù•ÉÍ•Ì°…¹•Ù•Éä)…¹‘¥‘…Ñ”¹½ÉÑ ½˜1…­”¥Ì‰½Õ¹‘•‰ä„±¥¹”Ñ¡…ĞÍÑ½ÁÌ…™Ñ•È€ÈĞ´ÌÈ´¸	½Ñ ¹••„ÑÉ…Ù•ÉÍ”)Á±…•™½ÈÑ¡•´°¹½Ğ„±½½Í•È™¥±Ñ•È¸((¨©…ÕÑ¥½¸™½ÈÑ¡”•¹•É…Ñ½È°™É½´Ñ¡”Í…µ”Í±¥”¸¨¨Q¡”½ÉÉ¥‘½ÉÌ‘É…İ¸½¸Ñ¡•Í”Í¡••ÑÌÉÕ¸)…‰½ÕĞ€Ô™Ğİ¥‘•ÈÑ¡…¸€àÀ™Ğ½¸‰½Ñ °…¹Ñ¡…Ğ¥ÌÁ…Á•ÈÍÑÉ•Ñ Á±ÕÌÁ•¸Á±…•µ•¹Ğ°¹½Ğ•Ù¥‘•¹”)½˜„İ¥‘•ÈÍÑÉ••Ğ¸•¹•É…Ñ”Ñ¡”É¥™É½´Ñ¡”Á±…ÑÑ•µ½‘Õ±”€£
œ…‰½Ù”¤…¹Í¹…À¥ĞÑ¼½¹ÑÉ½°ƒŠP)‘¼¹½Ğ™¥Ğ¥ĞÑ¼Ñ¡”ÑÉ…•½ÉÉ¥‘½Èİ¥‘Ñ¡Ì°İ¡¥ İ½Õ±‰…­”€Ğ”½˜Á…Á•È‘¥ÍÑ½ÉÑ¥½¸¥¹Ñ¼Ñ¡”)Ñ½İ¸¸((¨©•½µ•ÑÉä½µ•Ì™É½´Ñ¡”Q¡½µÁÍ½¸µ½‘Õ±”°•¹•É…Ñ•°¹½ĞÑÉ…•¸¨¨Q¡”€ÄàÌÀÁ±…Ğ¥Ù•Ì(àÀµ™ĞÍÑÉ••ÑÌ…¹€Äàµ™Ğ…±±•åÌ½Ù•ÈÑ¡”½É¥¥¹…°€À¸ÌÜÔÍÄµ¤ì]É¥¡Ğ€ÄàÌĞÍ¡½İÌÑ¡”Í…µ”)É¥•áÑ•¹‘•°…¹‰½Ñ Í¡••ÑÌ…ÉÉäƒ
ÄÈÀ´½˜•½É•™•É•¹¥¹œÍ±½ÀÑ¡…ĞÑÉ…¥¹œİ½Õ±‰…­”)¥¸…Ìİ½‰‰±”¸•¹•É…Ñ”Ñ¡”É¥…¹…±åÑ¥…±±ä™É½´Ñ¡”µ½‘Õ±”…¹Í¹…À¥ĞÑ¼½¹ÑÉ½°¸)ÍÑÉ••ĞÑ¡…Ğ¥ÌÍÑÉ…¥¡Ğ‰•…ÕÍ”Ñ¡”ÍÕÉÙ•å½Èµ…‘”¥ĞÍÑÉ…¥¡ĞÍ¡½Õ±¹½Ğ…ÉÉ¥Ù”‰•¹Ğ)‰•…ÕÍ”İ”ÑÉ…•„™½±‘•Í¡••Ğ¸((¨¨‰ÕÉ…Ñ”ÍÕÉ™…”ˆ¥¸€ÄàÌÔµ•…¹Ì•…ÉÑ °¹½ĞÉ…Ù•°¸¨¨Q¡”™¥ÉÍĞ¥¹ÍÑ¥¹ĞƒŠP„É½İ¹•°)­•É‰•°É…Ù•±±•½ÈÁ…Ù•É½…‘İ…äƒŠP¥ÌİÉ½¹œ™½ÈÑ¡”‘…Ñ”°‰ÕĞÑ¡”•…É±¥•Èİ½É‘¥¹œ¡•É”İ…Ì)Ñ½¼‰É½…¥¸Ñ¡”½ÁÁ½Í¥Ñ”‘¥É•Ñ¥½¸¸Q¡”½™™¥¥…°€ÄàäÄµÕ¹¥¥Á…°¡É½¹½±½äÉ•½É‘ÌM½ÕÑ )]…Ñ•È½É‘•É•Á¥Ñ¡•‰äÁÉ¥°€ÄàÌĞ…¹É…‘•™½È‘É…¥¹…”Ñ¡…Ğ)Õ±ä°…¹…±±ÌM½ÕÑ ]…Ñ•È)…¹1…­”Ñ¡”Ñİ¼ÁÉ¥¹¥Á…°•…É±äÑÕÉ¹Á¥­•…¹É…‘•ÍÑÉ••ÑÌ¸%ĞÍ•Á…É…Ñ•±ä‘…Ñ•Ì…¹…°°)1…­”İ•ÍĞÑ¼•ÍÁ±…¥¹•Ì…¹I…¹‘½±Á ÑÕÉ¹Á¥­¥¹œÑ¼™…±°€ÄàÌØìÍÑÉ••ĞÁ±…¹­¥¹œ‰•¥¹Ì¥¸€ÄàĞĞ°)•¹•É…°Á±…¹­¥¹œ¥¸€ÄàĞä°±¥µ•ÍÑ½¹”‰±½¬¥¸€ÄàÔÔ°…¹µ……‘…´½½‰‰±”¥¸€ÄàÔØ¸=¸€Ä)Õ±ä€ÄàÌÔ)Ñ¡”‘•™•¹Í¥‰±”Ù¥ÍÕ…°Ù½…‰Õ±…Éä¥ÌÑ¡•É•™½É”€¨©É…‘•½ÈÑ¡É½İ¸µÕÀ•…ÉÑ ½¸Ñ¡”ÁÉ¥¹¥Á…°)É½ÕÑ•Ì°İ½É¸¹…Ñ¥Ù”Í½¥°½¸±•ÍÍ•ÈÍÑÉ••ÑÌ°É…ÍÍäµ…É¥¹Ì°¹¼É…Ù•°½È¡…ÉÁ…Ù¥¹œ¨¨¸…Ñ•)Á±…¹¬™½½Ñİ…±­ÌÉ•µ…¥¸„Í•Á…É…Ñ”É•Í•…É Á…É•°…¹…É”¹½ĞÍ¥±•¹Ñ±äÍÕÁÁ±¥•‰äÑ¡”É½…¸((¨¨‰ÕÉ…Ñ”•±•Ù…Ñ¥½¹Ìˆµ•…¹Ìµ½‘•ÍĞ•…É±äÉ…‘¥¹œ¥Ì¹½ĞÑ¡”±…Ñ•ÈI…¥Í¥¹œ½˜¡¥…¼¸¨¨)M½ÕÑ ]…Ñ•ÈÌ‘½Õµ•¹Ñ•‘É…¥¹…”½É‘•Èµ•…¹Ì€‰¹½Ñ¡¥¹œ¡…‰••¸É…‘•ˆİ…Ì™…±Í”¸]¡…Ğ¹¼)Í½ÕÉ”ÍÕÁÁ±¥•Ì¥ÌÑ¡”…µ½Õ¹Ğ°É½ÍÌµÍ•Ñ¥½¸°É½İ¸½È™¥±°ÁÉ½™¥±”°Í¼Ñ¡¥Ì™¥ÉÍĞ±…å•È‘½•Ì)¹½Ğ•‘¥ĞÑ¡”¡•¥¡Ñ™¥•±½È¥¹Ù•¹Ğ½¹”è¥ÑÌÙ•ÉÑ¥•ÌÍ…µÁ±”Ñ¡”•á¥ÍÑ¥¹œÉ½Õ¹•á…Ñ±ä…¹Í¥Ğ(ÈÈµ´…‰½Ù”¥Ğ½¹±äÑ¼…Ù½¥‘•ÁÑ ™¥¡Ñ¥¹œ¸Q¡”İ…±¬…µ•É„¹½Ü±½­ÌÑ¼Ñ¡…ĞÍ…µ”‰¥±¥¹•…È)ÍÕÉ™…”•… ™É…µ”¥¹ÍÑ•…½˜•…Í¥¹œ‰•¡¥¹¥Ğ½¸É¥Í•Ì…¹™…±±Ì¸]¡•É”„ÍÑÉ••ĞÉ•…¡•Ìİ…Ñ•È°)Ñ¡”É¥‰‰½¸ÍÑ½ÁÌì„É½ÍÍ¥¹œ¥Ì½¹Ñ•¹ĞÑ¼É•Í•…É °¹½Ğ„É•¹‘•É¥¹œ…ÉÑ•™…ĞÑ¼™±…ÑÑ•¸…İ…ä¸((ŒŒLÕ„ƒŠP½ÉĞ•…É‰½É¸ƒ
Ü€¨©=9€ÈÀÈØ´Àà´ÄÄ¨¨()-•Ù¥¸Ì…±°°…¹Ñ¡”‘•Á•¹‘•¹ä¡”¹…µ•¥ÌÍ…Ñ¥Í™¥•èÑ¡”½…ÍÑ±¥¹”°Ñ¡”Í…¹‰…È…¹Ñ¡”)¡…É‰½ÕÈİ½É­Ì…É”É•…°Í¼Ñ¡•É”¥ÌÉ½Õ¹Ñ¼ÁÕĞ¥Ğ½¸½¹”LÉ”‰Õ¥±‘ÌÑ¡”¡•¥¡Ñ™¥•±¸((´€¨©A½Í¥Ñ¥½¸¥ÌÍ•ÑÑ±•…¹É½ÍÌµ¡•­•¨¨è±½…°€¬ÄÄÔÈ°8€¬ÈÈÄ°Ñİ¼¥¹‘•Á•¹‘•¹Ğµ•Ñ¡½‘Ì(€€ÌÔ´…Á…ÉĞ€¡Í•”LÉ”¤¸(´€¨©]¡…Ğ¥Ğ€©İ…Ì¨½¸€ÄàÌÔ´ÀÜ´ÀÄ¥ÌMQQ1°€ÈÀÈØ´Àà´ÄÀ¨¨ƒŠP‘½Ì½IMI ½™½ÉÑ}‘•…É‰½É¸¹µ‘€¸(€¸€¨©½ÕÁ¥•U¹¥Ñ•MÑ…Ñ•ÌÉµäÁ½ÍĞ°½µµ…¹‘•‰ä5…©½È)½¡¸É••¹”¨¨°İ¡¼¡•±¥Ğ™É½´(€€Äà••µ‰•È€ÄàÌÌÕ¹Ñ¥°€ÄØM•ÁÑ•µ‰•È€ÄàÌÔ¸Q¡É•”Í•Á…É…Ñ•±äİÉ¥ÑÑ•¸…½Õ¹ÑÌ…É•”Ñ¡”™½ÉĞ(€İ…Ì…ÉÉ¥Í½¹•Ñ¡É½Õ €ÄàÌÔ…¹Ñ¡”Á½ÍĞÍÕÉ•½¸ÌÁÉ•ÍÉ¥ÁÑ¥½¸‰½½¬¡…Ì…¸•¹ÑÉä‘…Ñ•(€€ÄÔ5…É €ÄàÌÔ¸Q¡”Í½±‘¥•ÉÌ±•™Ğ½¸€Èä••µ‰•È€ÄàÌØ…¹Ñ¡”Á½ÍĞİ…Ì¹½Ğ¥Ù•¸ÕÀÕ¹Ñ¥°(€)Õ¹”½È)Õ±ä€ÄàÌÜƒŠPİ¡¥ ¥Ì¡½Ü¹‘É•…Ìµ…¹…•ÌÑ¼¥Ù”€ÄàÌØ¥¸½¹”¡…ÁÑ•È…¹(€€ÄÀ5…ä€ÄàÌÜ¥¸…¹½Ñ¡•È¸9½Ñ¡¥¹œ¡•É”½•ÌÑ¼‘…Ñ„½•á±ÕÍ¥½¹Ì¹©Í½¹€ìÑ¡”™½ÉĞİ…Ì¡•É”¸(´€¨©Q¡”™½½ÑÁÉ¥¹Ğ¥ÌÍÑ¥±°9=PÍ½ÕÉ•°‰ÕĞÑ¡”Í•…É ¥Ì¹…ÉÉ½İ•Ñ¼Ñ¡É•”…¹‘¥‘…Ñ•Ì¸¨¨(€]É¥¡Ğ€©±…‰•±Ì¨Ñ¡”É•Í•ÉÙ…Ñ¥½¸…¹‘É…İÌ¹¼Á±…¸ì¹•¥Ñ¡•È‘½•Ì!…Ñ¡…İ…ä¸Q¡”‰•ÍĞ±•…¥Ì(€„ÍÕÉÙ•ä°¹½Ğ„Á¥ÑÕÉ”èÑ¡”]…È•Á…ÉÑµ•¹ĞÌ…•¹Ğ°É•Á½ÉÑ¥¹œ½¸€ÈÄ9½Ù•µ‰•È€ÄàĞÀ°¹…µ•Ì(€Ñ¡”Á±…ÑÑ•±½ÑÌ½˜Ñ¡”€¨©½ÉĞµ•…É‰½É¸‘‘¥Ñ¥½¸€ ÄàÌä¤¨¨Ñ¡…Ğİ•É”İ¥Ñ¡¡•±™É½´Í…±”(€‰•…ÕÍ”Ñ¡•ä½Ù•É•€‰Ñ¡”™½ÉÑÉ•ÍÌ½˜½ÉĞ•…É‰½É¸€©İ¥Ñ¡¥¸Ñ¡”Á¥­•ÑÌ¨ˆ¸¥¹Ñ¡…ĞÁ±…Ğ°(€™¥Ğ¥Ğ€¡¥ÑÌÍÑÉ••ÑÌÍÕÉÙ¥Ù”¥¸Ñ¡”µ½‘•É¸É¥¤…¹É•…Ñ¡”İ¥Ñ¡¡•±±½ÑÌ¸M•½¹è€¨©!•¹Éä(€!…ÉĞÌ€ÄàÔÌÍÕÉÙ•ä½˜Ñ¡”™½ÉĞ¨¨°¹…µ•‰ÕĞ¹½Ğå•Ğ±½…Ñ•¸Q¡¥Éè„]…È•Á…ÉÑµ•¹ĞÁ±…¸(€½˜Ñ¡”É•‰Õ¥±Ğ™½ÉĞ°¹•Ù•È±½½­•™½È¸IÕ±•½ÕĞİ¥Ñ É•…Í½¹Ì¥¸Ñ¡”µ•µ¼ƒ
œ€ÜƒŠP‘¼¹½Ğ(€É”µÉÕ¸Ñ¡•´¸MÑ¥±°è‘¼¹½Ğ¥¹™•È„ÍÑ½­…‘”½ÕÑ±¥¹”™É½´„‰…¹¹•È¸(´€¨©½ÕÈ½¹ÍÑÉ…¥¹ÑÌ•á¥ÍĞ¹½ÜÑ¡…Ğ‘¥¹½Ğ¸¨¨ÕÉ‘½¸L¸!Õ‰‰…É°½ÉÉ•Ñ¥¹œÑ¡”€©]…Ôµ	Õ¸¨(€Ù¥•Ü¥¸€ÄààÄ°ÍÑ…Ñ•ÌÑ¡…ĞÑ¡”•¹±½ÍÕÉ”É…¸€‰¹•…É±ä¹½ÉÑ …¹Í½ÕÑ °•…ÍĞ…¹İ•ÍĞˆìÑ¡…Ğ(€Ñ¡”¹½ÉÑ Á¥­•Ğ±¥¹”ÍÑ½½¹½İ¡•É”µ½É”Ñ¡…¸€àÀ™Ğ™É½´Ñ¡”İ…Ñ•È…¹€ÔÀ´ØÀ™Ğ½ÁÁ½Í¥Ñ”(€Ñ¡”¹½ÉÑ …Ñ”ìÑ¡…ĞÑ¡”É½Õ¹…ĞÑ¡”™½ÉĞİ…Ì€‰¹½Ğ½Ù•È•¥¡Ğ™••Ğ…‰½Ù”Ñ¡”I¥Ù•È…Ğ¥ÑÌ(€±½İ•ÍĞÍÑ…”ˆì…¹Ñ¡…ĞÑ¡”¹½ÉÑ …¹Í½ÕÑ …Ñ•Ìİ•É”½¸½¹”Í¥¡Ğ±¥¹”¸Q¡”™¥ÉÍĞÑİ¼…É”(€ÕÍ…‰±”……¥¹ÍĞÑ¡”ÑÉ…•€ÄàÌĞ‰…¹¬¸€¨©Q¡”Ñ¡¥É¥Ì„™¥¹‘¥¹œ…‰½ÕĞÑ¡”Ñ•ÉÉ…¥¸¨¨è…¸€à™Ğ(€Á±…Ñ™½É´¥ÌÑ…±±•ÈÑ¡…¸…¹ä±…¹‘™½É´¥¸Ñ¡”µ½‘•±±•‰½à€¡Ñ½Ñ…°É•±¥•˜€Ğ¸ÌÀ™Ğ¤°Í¼¥Ğ(€‰•±½¹ÌÑ¼LÉ”Á…É•°€¡ˆ¤…ÌµÕ …ÌÑ¼Ñ¡¥ÌÁ…É•°¸(´%Ğ¥Ì„€¨©½µÁ±•à°¹½Ğ„‰Õ¥±‘¥¹œ¨¨èLÔÌ½ÉĞ•…É‰½É¸Á…É•°…±É•…‘ä¥Ñ•µ¥Í•ÌÁ…±¥Í…‘”°(€‰±½­¡½ÕÍ”°‰…ÍÑ¥½¸°µ……é¥¹”°ÅÕ…ÉÑ•ÉÌ°‰…ÉÉ…­Ì°ÍÕÑ±•È°¡½ÍÁ¥Ñ…°°Á…É…‘”…¹…É‘•¹Ì¸(€áÁ•ĞÍ•Ù•É…°É•½É‘Ì…¹Í•Ù•É…°‰…­•Ì°¹½Ğ½¹”¸Q¡”¥¹Ñ•É¥½È…ÉÉ…¹•µ•¹Ğ¥Ì¹½Ü…ÑÑ•ÍÑ•(€•±•µ•¹Ğ‰ä•±•µ•¹Ğ€¡µ•µ¼ƒ
œ€Ô¤…¹Ñ¡”½¹”½Á•¸‘¥Í…É••µ•¹Ğ¥Ìİ¡•Ñ¡•ÈÑ¡•É”İ•É”Ñİ¼(€‰…ÍÑ¥½¹Ì½È½¹”¸(´€¨©…ÕÑ¥½¸Ñ¡”µ•µ¼Á…åÌ™½È¸¨¨Q¡É•”•¹±½ÍÕÉ•Ì•Ğ½¹™ÕÍ•¥¸Ñ¡¥Ì±¥Ñ•É…ÑÕÉ”…¹½¹±ä(€½¹”¥ÌÑ¡”€ÄàÌÔ™½ÉĞèÑ¡”€ÄàÄØÍÑ½­…‘”°Ñ¡”Á½ÍĞµ…Éµä½µÁ½Õ¹½˜€ÄàÔÀ€¡Á¥­•ÑÌ½¹”°„(€İ¡¥Ñ•İ…Í¡•‰½…É™•¹”°€‰Í…ä€ĞÀÀ™••Ğˆ¤°…¹Ñ¡”€ÔÏ
ğµ…É”É•Í•ÉÙ…Ñ¥½¸¸Q¡”€ĞÀÀ™Ğ™¥ÕÉ”(€¥ÌÑ¡”µ¥‘‘±”½¹”…¹µÕÍĞ¹½Ğ‰”É•……Ì„Á…±¥Í…‘”¸((¨©!½Ü‰½Ñ …Ñ•Ìİ•É”±•…É•°…¹İ¡…Ğ¥Ğ½ÍĞ¸¨¨((´€¨©Q¡”Á±…¸Í½ÕÉ”•á¥ÍÑÌ…¹¥Ğ¥Ì„ÍÕÉÙ•ä¸¨¨€©5…À½˜Ñ¡”5½ÕÑ ½˜¡¥…¼I¥Ù•È¨°¸!…ÉÉ¥Í½¸(€)È¸°ÍÌĞT¹L¸¥Ù¥°¹¥¹••È°™½ÈÑ¡”ÁÉ½Á½Í•¡…É‰½ÕÈ¥µÁÉ½Ù•µ•¹ÑÌ°…ÁÁÉ½Ù•‰ä]¥±±¥…´(€!½İ…É€ÈĞ•‰ÉÕ…Éä€ÄàÌÀƒŠPÉ•ÁÉ½‘Õ•¥¸€¨©¹‘É•…ÌÙ½°¸€ÄÀ¸€ÄÄÌ¨¨…¹±¥ÍÑ•¥¸Ñ¡…ĞÙ½±Õµ”Ì(€½İ¸Ñ…‰±”½˜µ…ÁÌ…Ì€‰½ÉĞ•…É‰½É¸¥¸€ÄàÌÀ´ÌÈˆ¸%Ğ‘É…İÌÑ¡”™½ÉĞ¥¸Á±…¸…¹¹…µ•ÌÑ¡”É½Õ¹(€É½Õ¹¥Ğ€¡…É‘•¸™½ÈÑ¡”…ÉÉ¥Í½¸°Õ±Ñ¥Ù…Ñ•¥•±°	¥œ	…É¸İ¥Ñ ÕÁ½±„°]…Í ¡½ÕÍ”°]•±°°(€M¡½À°½ÉĞ•µ•Ñ•Éä°Ñ¡”•ÉÉä¤¸I•½É‘•…Ì¡…ÉÉ¥Í½¹|ÄàÌÁ}É¥Ù•É}µ½ÕÑ¡€°…ÍÍ•Ñ}ÕÍ”è•½µ•ÑÉå€°(€Ñ¥•È€ÈƒŠP‰•…ÕÍ”Ñ¡”Á±…Ñ”Í…åÌ½¸¥ÑÌ™…”Ñ¡…Ğ¥Ğ…ÉÉ¥•Ì€‰…‘‘¥Ñ¥½¹Ì…¹¡…¹•ÌƒŠ˜ÍÕ•ÍÑ•(€‰äÑ¡”5•µ½Éä½˜…É±äM•ÑÑ±•ÉÌˆ°Í¼¥Ğ¥Ì„Á•É¥½ÍÕÉÙ•äÁ±ÕÌ™¥™Ñäµå•…Èµ½±É•½±±•Ñ¥½¸(€µ¥á•½¸½¹”Á±…Ñ”¸€¨©9½Ñ¡¥¹œÑ…­•¸™É½´¥Ğ¥ÌÉ…‘•‘½Õµ•¹Ñ•‘€¸¨¨(´€¨©Q¡”Á±…Ñ”¡…Ì¹¼Í…±”‰…È°…¹Ñ¡…Ğ¥ÌÑ¡”İ¡½±”‘¥™™¥Õ±Ñä¸¨¨Q¡”Í…±”¥Ì‘•É¥Ù•‰ä(€Í•ÑÑ¥¹œÑ¡”‘É…İ¸¹½ÉÑ É…¹”•ÅÕ…°Ñ¼Ñ¡”½µµ…¹‘…¹ĞÌÅÕ…ÉÑ•ÉÌ…Ğ€‰…‰½ÕĞ€ÈÔà€ÔÀ™Ğˆ™É½´Ñ¡”(€€ÄàÔÔÁ¡½Ñ½É…Á ­•äƒŠP€Ä¸ÄÀ™Ğ½ÁàƒŠP…¹¡•­•Ñİ¥”½¸Ñ¡”Í…µ”Á±…Ñ”€¡‘É…İ¸…ÍÁ•Ğ€Ä¸äèÄ(€……¥¹ÍĞ„ÍÑ…Ñ•€È¸ÀèÄìÁ…É…‘”İ¥‘Ñ €ÜÄ™Ğ……¥¹ÍĞ„ÍÑ…Ñ•€àÀ™Ğ¤¸€¨«
ÄÈÀ€”¨¨½¸•Ù•Éä‘•É¥Ù•(€‘¥µ•¹Í¥½¸°½¸Ñ½À½˜Ñ¡”‘…ÑÕ´Ìƒ
ÄÈÀ´¸Q¡”ÍÑ½­…‘”½µ•Ì½ÕĞ…‰½ÕĞ€¨¨ÔÌ´€ ÄÜĞ™Ğ¤ÍÅÕ…É”¨¨¸(€€¨©9¼‘¥µ•¹Í¥½¸½˜Ñ¡”€ÄàÄØ™½ÉĞ•á¥ÍÑÌ¥¸Ñ¡”±¥Ñ•É…ÑÕÉ”¨¨èEÕ…¥™”Ìµ½¹½É…Á ÁÉ¥¹ÑÌ(€]¡¥ÍÑ±•ÈÌµ•…ÍÕÉ•€ÄàÀà‘É…Õ¡Ğ½˜Ñ¡”%IMP™½ÉĞ…¹ÍÑ…Ñ•Ì¹½¹”™½ÈÑ¡”Í•½¹…¹åİ¡•É”¸(´€¨©Q¡”…ÉÉ…¹•µ•¹Ğ¥ÌµÕ ‰•ÑÑ•È•Ù¥‘•¹”Ñ¡…¸Ñ¡”Í…±”¨¨°…¹¥Ğ¥Ìİ¡…Ğ±¥•¹Í•Ì¥¹™•ÉÉ•‘€(€É…Ñ¡•ÈÑ¡…¸½¹©•ÑÕÉ…±€™½ÈÑ¡”Á½Í¥Ñ¥½¹Ìè…¸€ÄàÌÀ•¹¥¹••ÈÌÁ±…¸…¹ÕÉ‘½¸!Õ‰‰…ÉÌ€ÄàÈÜ(€İ…±¬É½Õ¹Ñ¡”¥¹Í¥‘”…É•”‰Õ¥±‘¥¹œ‰ä‰Õ¥±‘¥¹œ°½¸Ñ¡”Í…µ”Í¥‘•Ì½˜Ñ¡”Í…µ”Ñİ¼…Ñ•Ì¸(´€¨©Q¡”…ÉÉ¥Í½¸¥ÌÍ•ÑÑ±•¸¨¨!•±½¹Ñ¥¹Õ½ÕÍ±ä€¨©)Õ¹”€ÄàÌÈƒŠH€Èä••µ‰•È€ÄàÌØ¨¨ì¹‘É•…Ì(€‰É…­•ÑÌÑ¡”Í•¹”‘…Ñ”…¹Ñ¡”‘É±½¥¡©½ÕÉ¹…°¡É½¹½±½ä™¥±±ÌÑ¡”‰É…­•Ğİ¥Ñ €¨©5…¨¸)½¡¸(€É••¹”°€ÕÑ %¹™…¹ÑÉä¨¨¸Qİ¼½µÁ…¹¥•Ì¥¸€ÄàÌÌì€¨©¹¼ÍÑÉ•¹Ñ ™¥ÕÉ”™½Èµ¥´ÄàÌÔİ…Ì™½Õ¹…¹(€¹½¹”¥Ì±…¥µ•¨¨¸Q¡”™½ÉĞ¥Ìµ½‘•±±•µ…¥¹Ñ…¥¹•°İ¥Ñ ¥ÑÌ…Ñ•ÌÍ¡ÕĞ¸(´€¨©½ÕÉÑ••¸É•½É‘Ì°Ñİ¼¹•Ü…É¡•ÑåÁ•Ì°™½ÕÉÑ••¸‰…­•Ì°øÄÜ°ÀÀÀÑÉ¥…¹±•Ì¸¨¨Á…±¥Í…‘•€(€€¡Á¥­•ĞÍÑ½­…‘”İ¥Ñ ¹…µ•…Ñ•Ì…¹½É¹•Èİ½É­Ììİ½É´É…¥°™•¹”™½ÈÑ¡”…É‘•¸¤…¹(€™½ÉÑ}ÍÑÉÕÑÕÉ•€€¡•±•Ù•¸­¥¹‘ÌƒŠPÅÕ…ÉÑ•ÉÌ°‰…ÉÉ…­Ì°‰±½­¡½ÕÍ”°µ……é¥¹”°ÍÑ½É”°Õ…É°(€ÍÕÑ±•È°…ÉÑ¥±±•Éä°Á…É…‘”°É½½Ğ¡½ÕÍ”°Ñ½İ•È¤¸Q¡”±¥¡Ñ¡½ÕÍ”½˜€ÄàÌÈ…µ”İ¥Ñ Ñ¡•´¸(´€¨©¥Ù”•á±ÕÍ¥½¹Ì°™½ÕÈ½˜Ñ¡•´İÉ½¹œµ™½ÉĞ™¥¹‘¥¹Ì¨¨èÑ¡”™¥ÉÍĞ™½ÉĞ¥ÑÍ•±˜°Ñ¡”Í…±±äµÁ½ÉĞ°(€Ñ¡”Ñ¡É•”…ÉÑ¥±±•ÉäÁ¥••Ì…¹Ñ¡”™¥™Ñä¥¹Ù…±¥‘Ì°Ñ¡”€ÄàÔÁÌ‰½…É™•¹”…¹ÑÕÉ¹ÍÑ¥±”ƒŠPÁ±ÕÌ(€€¨©Ñ¡•É”¥Ì¹¼¡½ÍÁ¥Ñ…°‰Õ¥±‘¥¹œ¨¨°½¹±äÑ¡”™½ÉĞ€©‰•½µ¥¹œ¨„•¹•É…°¡½ÍÁ¥Ñ…°¥¸Ñ¡”€ÄàÌÈ(€¡½±•É„¸Q¡É•”½ÉÉ•Ñ¥½¹ÌÑ¼‘½Ì½É•Í•…É ¼ÀĞµÍÑÉÕÑÕÉ•ÌµÍ½ÕÑ ¹µ‘€…É”É•½É‘•¥¸(€‘½Ì½IMI ½™½ÉÑ}‘•…É‰½É¸¹µ‘€ƒ
œ€Ø°…¹½¹”Ñ¼ƒ
œ€È¥¸(€‘½Ì½IMI ½¡¥…½}±¥¡Ñ¡½ÕÍ•|ÄàÌÈ¹µ‘€¸(´€¨©%ĞÍÑ½½½¸¹½Ñ¡¥¹œ™½È…‰½ÕĞ™½ÕÈ¡½ÕÉÌ¸¨¨Q¡”½µÁ±•à¥Ì€àÌÈ´•…ÍĞ½˜İ¡•É”Ñ¡”(€¡•¥¡Ñ™¥•±ÕÍ•Ñ¼ÍÑ½À°…¹İ¡¥±”¥Ğİ…ÌÑ¡•É”¥Ğ•áÁ½Í•„É•…°‰±¥¹ÍÁ½Ğ¥¸Ñ¡”(€É½Õ¹µ½¹Ñ…Ğ…Ñ”ƒŠPÑ¡”±…µÁ••‘”µ…‘”„™½ÉĞ¥¸Ñ¡”Ù½¥É•Á½ÉĞ„Á•É™•Ğ±…¹‘¥¹œ¸M•”(€MQQULƒ
œ€‰-¹½İ¸İ•…­¹•ÍÍ•Ìˆ€Á„¸€¨©LÉ”Á…É•°€¡ˆ¤Ñ¡•¸±…¹‘•Ñ¡”Í…µ”‘…ä¨¨èÑ¡”™¥•±É•…¡•Ì(€€¬ÄÜÀÀ°Ñİ•±Ù”½˜Ñ¡”™½ÕÉÑ••¸ÍÑÉÕÑÕÉ•Ì±…¹°…¹Ñ¡”±¥¡Ñ¡½ÕÍ”…¹Ñ¡”É½½Ğ¡½ÕÍ”ƒŠP‰½Ñ (€½¹©•ÑÕÉ…±€¥¸Á½Í¥Ñ¥½¸ƒŠPµ½Ù•½™˜Ñ¡”¡…¹¹•°…¹½¹Ñ¼Ñ¡”‰…¹¬Ñ½À¹½ÜÑ¡…ĞÑ¡•É”¥Ì„(€ÍÕÉ™…”Ñ¼‰”İÉ½¹œ…‰½ÕĞ¸Q¡”Ñİ¼Ñ¡…ĞÉ•µ…¥¸½™˜Ñ¡”É½Õ¹…É”Ñ¡”ÍÑ½­…‘”…¹Ñ¡”(€½µµ…¹‘…¹ĞÌÅÕ…ÉÑ•ÉÌ°İ¡½Í”¹½ÉÑ Í¥‘•ÌÉ½ÍÌÑ¡”Ñ½À½˜Ñ¡”É¥Ù•È‰…¹¬‰ä€Ä¸ĞÀ´…¹€À¸ĞØ´°(€‰•…ÕÍ”€¨©¹¼ÕĞ°™¥±°°É•Ù•Ñµ•¹Ğ½È™½Õ¹‘…Ñ¥½¸¥Ìµ½‘•±±•…¹åİ¡•É”¥¸Ñ¡¥ÌÁÉ½©•Ğ¨¨¸0ĞØ¸((¨©Q¡”…Ñ•Ìİ•É”½Á•¸°…¹ÀÑ|Á€¹•Ù•È‘É•ÜÑ¡”½É¹•Èİ½É­Ì¥Ğİ…ÌÍ…¥Ñ¼€¡P´ÀÀäÔ°(ÈÀÈØ´Àà´ÈĞ¤¸¨¨Qİ¼™¥¹‘¥¹Ì°½¹”µ•…ÍÕÉ•½™˜Ñ¡”Í¡••Ğ…¹½¹”½™˜Ñ¡”Í¡¥ÁÁ•µ•Í ƒŠP)‘½Ì½IMI ½™½ÉÑ}‘•…É‰½É¹}…Ñ•}…¹‘}½É¹•É}İ½É­Ì¹µ‘€°¡•±‰ä)Ñ½½±Ì½µ•…ÍÕÉ•}™½ÉÑ}İ½É­Í}Á±…Ñ”¹Áå€…¹Ñ½½±Ì½µ•…ÍÕÉ•}™½ÉÑ}…Ñ•Ì¹Áå€¸((´€¨©Q¡”Á±…Ñ”É…¥Í•Ì¹¼İ½É¬…Ğ•¥Ñ¡•È…¹±”¥Ğ‘É…İÌ¸¨¨%ĞÉ…¥Í•Ì•á…Ñ±äÑİ¼É½½™•°(€±…¹Ñ•É¹•°±½œµ™…•İ½É­Ì…¹‰½Ñ ÍÑ…¹½Ù•ÈÑ¡”5%1½˜Ñ¡”İ…±°°…Ğ€¨¨À¸ĞÌÔ…¹(€€À¸ÔÈÄ¨¨½˜Ñ¡”‘É…İ¸ÉÕ¸ì„½É¹•Èİ½É¬ÍÑ…¹‘Ì…Ğ€À¸ÀÀÀ½È€Ä¸ÀÀÀ¸Q¡”½¹”…¹±”¥ĞÍ¡½İÌ(€Õ¹½±Õ‘•¥ÌÑ¡”¹½ÉÑ µ•…ÍĞ…¹¥Ğ¥Ì‘É…İ¸Á±…¥¸ƒŠPİ¡¥ ¥Ìİ¡…ĞÑ¡”É•½ÉÍ…åÌ½˜Ñ¡…Ğ(€…¹±”¸Q¡”¹½ÉÑ µİ•ÍĞ…¹±”°Ñ¡”½¹”Ñ¡”É•½É‘½•ÌÁÕĞ„İ½É¬…Ğ°¥Ì‰•¡¥¹Ñ¡”ÑÉ•”(€½ÕÑÍ¥‘”Ñ¡”İ…±±Ì¸€¨©9½Ñ¡¥¹œİ…Ìµ…ÍÍ•…ĞÑ¡”…¹±•Ì¨¨°…¹Ñ¡”±½œµ™…•İ½É¬½Ù•ÈÑ¡”(€…Ñ”İ…Ì¹½Ğ‰Õ¥±Ğ•¥Ñ¡•ÈèÑ¡”Í¡••Ğ…±É•…‘ä…ÉÉ¥•Ì„•ÉÑ¥™¥•%IMPµ™½ÉĞ™•…ÑÕÉ”€¡Ñ¡”(€™±…ÍÑ…™˜°‘…Ñ„½•á±ÕÍ¥½¹Ì¹©Í½¹€¤…¹Ñİ¼É½½™•±…¹Ñ•É¹•±½œÑ½İ•ÉÌ¥ÌÑ¡…Ğ™½ÉĞÌ½İ¸(€Í¥¹…ÑÕÉ”¥¸•Ù•ÉåÑ¡¥¹œ‰ÕĞÁ½Í¥Ñ¥½¸¸M…µ”™…¥±ÕÉ”…ÌP´ÀÀäĞ°½¹”‘…ä…Á…ÉĞ°½¸Ñ¡”Í…µ”(€Í¡••ĞèÑ¡”Á±…Ñ”É•…‰ä•å”¸(´€¨©	½Ñ ‘½Õµ•¹Ñ•…Ñ•ÌÍÑ½½„ÅÕ…ÉÑ•È½Á•¸¸¨¨=¹”±•…˜½˜•… Á…¥Èİ…ÌÁ±…•™É½´„(€µ¥‘Á½¥¹ĞÑ¡…Ğ½±±…ÁÍ•½¹Ñ¼¥ÑÌ½İ¸©…µˆ°Í¼€¨¨À¸äÀ´½˜Ñ¡”€Ì¸Ø´…Ñ•İ…äİ…Ì‘…å±¥¡Ğ(€ÍÑÉ…¥¡ĞÑ¡É½Õ Ñ¡”İ…±°¨¨…¹€À¸äÀ´½˜±•…˜±…ä…É½ÍÌÑ¡”Á¥­•ÑÌ½ÕÑÍ¥‘”Ñ¡”™É…µ”ƒŠP(€¥¸Ñ¡”½µµ¥ÑÑ•1°Í¼¥¸Ñ¡”‰åÑ•Ì„Ù¥Í¥Ñ½È‘½İ¹±½…‘•¸½ÕÈ±¥¹•Ì¥¸Á…±¥Í…‘”¹Áå€°(€½¹”…ÍÍ•ĞÉ•‰…­•€¡™½ÉÑ}‘•…É‰½É¹}Á…±¥Í…‘•}}Á¥­•Ñ|ÄàÄÙ€¤¸Q¡”…Ñ”Ñ¡…Ğ¡½±‘Ì¥ĞÉ•…‘ÌÑ¡”(€Í¡¥ÁÁ•µ•Í É…Ñ¡•ÈÑ¡…¸É”µ‘•É¥Ù¥¹œÑ¡”Á±…•µ•¹Ğ°‰•…ÕÍ”Ñ¡”‘•É¥Ù…Ñ¥½¸İ…ÌÑ¡”™…Õ±Ğ¸(´€¨©Q¡”Í½ÕÑ µİ•ÍĞ‰±½­¡½ÕÍ”…±É•…‘äÉ•……‰½Ù”Ñ¡”ÕÉÑ…¥¸¨¨…¹¹½Ü¡…Ì„¹Õµ‰•Èè€ä¸Ğà´(€½˜‰Õ¥±‘¥¹œ½Ù•È„€Ì¸àÀ´ÕÉÑ…¥¸°™É½´¥ÑÌ½İ¸¥¹ÍÑ…¹”‰½Õ¹‘Ì¥¸Ñ¡”Í•¹”¸((¨©MÑ¥±°½Á•¸¥¸Ñ¡¥ÌÅÕ…‘É…¹Ğ°¥¸Ñ¡”½É‘•ÈÑ¡”•Ù¥‘•¹”ÍÕÁÁ½ÉÑÌè¨¨Ñ¡”¹…µ•É½Õ¹½¸Ñ¡”€ÄàÌÀ)Á±…¸Ñ¡…Ğ¥Ì‘É…İ¸…Ì„Íåµ‰½°…¹„±…‰•°…¹¹½Ñ¡¥¹œ•±Í”€¡	¥œ	…É¸İ¥Ñ ÕÁ½±„°]…Í ¡½ÕÍ”°)]•±°°M¡½À°=ÕĞ	Õ¥±‘¥¹Ì°T¹L¸…Ñ½ÈÌ!½ÕÍ”°Õ±Ñ¥Ù…Ñ•¥•±°Ñ¡”•ÉÉäƒŠPÑ¡”½ÉĞ•µ•Ñ•Éä)‘•±¥‰•É…Ñ•±ä±•™Ğ…±½¹”¤ìÑ¡”‘É¥±°É½Õ¹Í½ÕÑ ½˜Ñ¡”Á¥­•ÑÌ°İ¡¥ -¥¹é¥”…ÑÑ•ÍÑÌ…¹‘½•Ì¹½Ğ)µ•…ÍÕÉ”ìÑ¡”…É‘•¸ÌÁ±…¹Ñ¥¹œ°İ¡¥ ¥Ì‘½Õµ•¹Ñ•…¹¹••‘Ì„€¨©Õ±Ñ¥Ù…Ñ•™±½É„é½¹”¨¨É…Ñ¡•È)Ñ¡…¸„ÍÑÉÕÑÕÉ”ì…¹„­••Á•ÈÌ‘İ•±±¥¹œ‰•Í¥‘”Ñ¡”±¥¡Ñ¡½ÕÍ”°İ¡¥ ¥ÌÁ±…ÕÍ¥‰±”…¹)Õ¹…ÑÑ•ÍÑ•¸(((ŒŒLĞƒŠPÉ¡•ÑåÁ”•¹•É…Ñ½ÉÌ()=¹”Á…É•°Á•È…É¡•ÑåÁ”°•… İ¥Ñ „½±‘•¸µÁ…É…µ•Ñ•È1…¹„É•™•É•¹”Í¡½Ğè()™É…µ•}Ñ…Ù•É¹€ƒ
Ü™É…µ•}ÍÑ½É•™É½¹Ñ€ƒ
Ü™É…µ•}‘İ•±±¥¹€ƒ
Ü±½}‘İ•±±¥¹€ƒ
Ü¥¹ÍÑ¥ÑÕÑ¥½¹…±€ƒ
Ü)™½ÉÑ}ÍÑÉÕÑÕÉ•€ƒ
Ü½ÕÑ‰Õ¥±‘¥¹€ƒ
ÜÁ±…¹­}İ…±­€ƒ
Ü‰É¥‘•}Ñ¥µ‰•É€ƒ
ÜÁ¥•É}É¥‰€ƒ
ÜÁ…±¥Í…‘•€()	…±±½½¸µ™É…µ”±½¥Œ€¡ÍÑÕÍÁ…¥¹œ°Í¡•…Ñ¡¥¹œ°ÁÉ½Á½ÉÑ¥½¹Ì¤¥Ì„™¥ÉÍĞµ±…ÍÌÉ•ÅÕ¥É•µ•¹Ğ°¹½Ğ„)‘•Ñ…¥°è€ÄàÌÏŠLÌÔ¡¥…¼¥Ìİ¡•É”‰…±±½½¸™É…µ¥¹œİ…Ì¥¹Ù•¹Ñ•°…¹¥Ğ¥ÌÑ¡”™¥ÉÍĞÑ¡¥¹œ„)­¹½İ±•‘•…‰±”Ù¥•İ•È¡•­Ì¸((¨©™É…µ•}‘İ•±±¥¹€=9€ÈÀÈØ´Àà´ÄÄ¨¨ƒŠP…¹¥Ğ¥ÌÑ¡”½¹”Ñ¡…ĞÕ¹‰±½­Ì¡½ÕÍ•Ì¸U¹Ñ¥°¥Ğ•á¥ÍÑ•)•Ù•Éä™É…µ”É•½É¡…Ñ¼‰”„Ñİ¼µÍÑ½É•äÁÕ‰±¥Œ¡½ÕÍ”½È„±½œ…‰¥¸°Í¼Ñ¡”‘…Ñ…Í•Ğ¡•±)Ñ…Ù•É¹Ì°ÍÑ½É•Ì…¹„‰É¥‘”…¹¹½Ğ½¹”‘İ•±±¥¹œ¸%ĞÑ…­•ÌÍÑ½É¥•Í€€Ä°€Ä¸Ô½È€È€¡‘•™…Õ±ĞÑ¡”)ÍÑ½Éäµ…¹µ„µ¡…±˜°­¹•”İ…±°…¹…‰±”µ•¹…ÑÑ¥Œİ¥¹‘½Ü°İ¡¥ ¥ÌÑ¡”™½É´½˜Ñ¡•Í”å•…ÉÌ¤ìÉ•…‘Ì)Ñ¡”É•…È€¨©•±°½™˜Ñ¡”™½½ÑÁÉ¥¹ĞÁ½±å½¸¨¨É…Ñ¡•ÈÑ¡…¸½™˜¥¹Ù•¹Ñ•‘¥µ•¹Í¥½¹Ì°Í¼…¸0µÍ¡…Á•)Á±…¸¥Ì‰Õ¥±Ğ…Ì…¸0…¹I=U9}=9QPèÁ•É¥µ•Ñ•É€¥Ì±¥Ñ•É…±±äÑÉÕ”½˜Ñ¡”µ•Í ì‰Õ¥±‘Ì„)ÍÑ½½À½È„Íµ…±°É½½™•Á½É °¹•Ù•ÈÑ¡”Ñ…Ù•É¸Ì…±±•Éäì…¹µ…­•Ì½¹ÍÑÉÕÑ¥½¹€Ñ¡”™¥ÉÍĞ)…ÑÑÉ¥‰ÕÑ”¥¸Ñ¡¥ÌÁÉ½©•ĞÑ¡…Ğ5=YLYIQ`É…Ñ¡•ÈÑ¡…¸Í¥ÑÑ¥¹œÕ¹É•…¥¸Ñ¡”Í¥‘•…ÈƒŠPÑ¡”)ÍÑÕµ½‘Õ±”€ ÄØ¥¸‰…±±½½¸°€ÈĞ¥¸‰É…•¤Á±…•Ì•Ù•Éä½Á•¹¥¹œ°Ñ¡”±…Á‰½…É‰ÕÑĞ©½¥¹ÑÌ™…±°½¸)ÍÑÕ±¥¹•Ì°…¹„‰É…•™É…µ”•ÑÌÑ¡”¥ÉĞ‰…¹…Ğ¥ÑÌÕÁÁ•È™±½½ÈÑ¡…Ğ„‰…±±½½¸™É…µ”¡…Ì¹¼)±¥¹”™½È¸Á±…¹€€¬‰…åÍ€…É”€¨©0ÈÌÌ½İ¸ÍÑ…Ñ•É•Í½±ÕÑ¥½¸¨¨ƒŠP„‰…ä½Õ¹Ğ‘•É¥Ù•™É½´™É½¹Ñ…”)…¹„É¡åÑ¡´Ñ¡…Ğ½µ•Ì™É½´Ñ¡”É½½´…ÉÉ…¹•µ•¹ĞƒŠPÍ¼Ñ¡”‘•™…Õ±Ğ™É½¹Ğ¥Ì…Íåµµ•ÑÉ¥Œ…¹)Õ¹•Ù•¹±äÍÁ…•É…Ñ¡•ÈÑ¡…¸Ñ¡”M…Õ…¹…Í Ì™¥Ù”‰…åÌİ½É¸‰ä•Ù•Éä‰Õ¥±‘¥¹œ¸()MÑ¥±°½Á•¸½¸¥Ğ°…¹İ½ÉÑ „É•½ÉÌ…ÑÑ•¹Ñ¥½¸‰•™½É”Ñ¡”™¥ÉÍĞ¡½ÕÍ”±…¹‘Ìè¹¼‘½Éµ•È€¡Ñ¡”)¡…±˜ÍÑ½É•ä¥Ì±¥Ğ½¹±ä™É½´Ñ¡”…‰±”•¹‘Ì¤°¹¼™½Õ¹‘…Ñ¥½¸½È•±±…È°¹¼µÕ¹Ñ¥¹Ì¥¸Ñ¡”Í…Í °)…¹Ñ¡”ÍÑ½½ÀÁÉ½©•ÑÌ½ÕÑÍ¥‘”Ñ¡”É•½É‘•™½½ÑÁÉ¥¹Ğ¸±°™½ÕÈ…É”¥¸Ñ¡”É•Á½ÉĞ…ÑÑ…¡•Ñ¼)Ñ¡”Á…É•°…¹‰•±½¹œ¥¸‘½Ì½1%	IQ%L¹µÑ¡”‘…ä„™É…µ•}‘İ•±±¥¹€É•½É‘½•Ì¸((¨©½ÕÑ‰Õ¥±‘¥¹€=9€ÈÀÈØ´Àà´ÄÄ¨¨ƒŠPÍÑ…‰±•Ì°Í¡•‘Ì°É¥‰Ì°Íµ½­•¡½ÕÍ•Ì°ÁÉ¥Ù¥•Ì¸	Õ¥±Ğ…Ì„)5%1dÉ…Ñ¡•ÈÑ¡…¸„Í¡…Á”°‰•…ÕÍ”„Í¥¹±”Í•Ğ½˜ÁÉ½Á½ÉÑ¥½¹ÌÑ¡…Ğ™±…ÑÑ•ÉÌÑ¡”µ¥‘‘±”½˜Ñ¡”)É…¹”‰É•…­Ì‰½Ñ •¹‘Ìè™¥Ù”½±‘•¸Ù…É¥…¹ÑÌÍÁ…¸„€Ä¸ÈÔ´ÁÉ¥ÙäÑ¼„€ÄÌ´¡½Ñ•°ÍÑ…‰±”°…¹)I=U9}=9QPèÁ•É¥µ•Ñ•É€¥ÌÙ•É¥™¥•½¸…±°™¥Ù”É…Ñ¡•ÈÑ¡…¸½¸½¹”¸•±¥‰•É…Ñ”…‰Í•¹•Ì…ÉÉä)…ÌµÕ ½˜Ñ¡”‘•Í¥¸…ÌÑ¡”Á…É…µ•Ñ•ÉÌƒŠPÍÑ½É¥•Í€¥Ì9=P½¹ÍÕµ•°‰•…ÕÍ”Ñİ¼ÍÑ½É•åÌ½˜İ…±°½¸)„Í•½¹‘…Éä‰Õ¥±‘¥¹œ¥Ì„±…¥´…¹İ…±±}¡•¥¡Ñ}µ€¥ÌÑ¡”¡½¹•ÍĞİ…äÑ¼µ…­”¥Ğì½¹ÍÑÉÕÑ¥½¹€)¹…µ•Ì±½œ½Á±…¹¬½±¥¡Ñ}™É…µ”É…Ñ¡•ÈÑ¡…¸‰…±±½½¸½‰É…•°‰•…ÕÍ”¹½Ñ¡¥¹œ‰•¡¥¹Ñ¡”‰½…É‘Ì½˜„Í¡•)¥ÌÙ¥Í¥‰±”…ĞÑ¡¥Ì1=…¹¹¼Í½ÕÉ”‘•ÍÉ¥‰•ÌÑ¡”™É…µ¥¹œ½˜…¹ä½ÕÑ‰Õ¥±‘¥¹œ¡•É”°Í¼Ñ¡”)Ù½…‰Õ±…Éä¹…µ•Ì½¹±äİ¡…Ğ„Ù¥•İ•È…¸Í•”¸()Qİ¼Ñ¡¥¹Ì¥Ğ¡…¹‘ÌÕÁİ…É¸€¨©0ÄÀÍ¡½Õ±‰”9II=]°¹½ĞÉ•Í½±Ù•¨¨èÑ¡¥Ì…É¡•ÑåÁ”…¸‰Õ¥±Ñ¡”)]•ÍÑ•É¸!½Ñ•°ÌÍÑ…‰±”‰ÕĞ¹½Ğ¥ÑÌİ…½¸å…É°…¹„å…É¥Ì…¸•¹±½ÍÕÉ”ƒŠP„™•¹”±¥¹”°Ñİ¼)…Ñ•İ…åÌ°ÑÉ½‘‘•¸É½Õ¹ƒŠPÍ¼‰Õ¥±‘¥¹œ¥Ğ½ÕĞ½˜…¸½ÕÑ‰Õ¥±‘¥¹œİ½Õ±‰”…±±¥¹œ„™•¹”„)‰Õ¥±‘¥¹œ¸Q¡”Í…µ”…ÀÍİ…±±½İÌÑ¡”•ÍÑÉ…äÁ•¸…¹±å‰½ÕÉ¸ÌÍÑ½­å…É°…¹…¸•¹±½ÍÕÉ•€)…É¡•ÑåÁ”¥Ì¹½Ü„¹…µ•İ…¹Ğ¸¹€¨©É•¥ÍÑ•É¥¹œ…¹ä…É¡•ÑåÁ”É•ÍÑ…±•Ì•Ù•Éä½µµ¥ÑÑ•1¨¨è)µ•Í¡}¥¹ÁÕÑÌ¹}½‘•}Í¡…Í€¡…Í¡•Ì‰Õ¥±¹Áå€Ì‰åÑ•Ì™½È•Ù•Éä…É¡•ÑåÁ”°…¹‰Õ¥±¹Áå€…ÉÉ¥•ÌÑ¡”)I!QeAM€É•¥ÍÑÉ…Ñ¥½¸Ñ…‰±”°Í¼…‘‘¥¹œ„É½ÜÑ¼¥Ğ¡…¹•ÌÑ¡”¡…Í ½˜‰Õ¥±‘¥¹Ì¥Ğ¹•Ù•È)Ñ½Õ¡•¸Qİ¼Á…É•±Ì¡¥ĞÑ¡¥Ì¥¹‘•Á•¹‘•¹Ñ±ä…¹‰½Ñ Ù•É¥™¥•Ñ¡”É”µ‰…­”¥Ì‰åÑ”µ¥‘•¹Ñ¥…°¸Q¡”)™¥à¥ÌÑ¼ÍÁ±¥ĞÑ¡”•áÁ½ÉĞÁ…Ñ ½ÕĞ½˜‰Õ¥±¹Áå€Í¼Ñ¡”É•¥ÍÑÉ…Ñ¥½¸Ñ…‰±”ÍÑ½ÁÌ‰•¥¹œ„µ•Í )¥¹ÁÕĞìÕ¹Ñ¥°Ñ¡•¸½¹”‰…Ñ¡•É”µ‰…­”±•…ÉÌ¥Ğ¸((¨©™É…µ•}ÍÑ½É•™É½¹Ñ€=9€ÈÀÈØ´Àà´ÄÄ¨¨ƒŠP€ÈÌ½¹ÍÕµ•…ÑÑÉ¥‰ÕÑ•Ì°…±°€ÄÌ±¥Ù”ÍÑ½É•™É½¹ĞÉ•½É‘Ì)É•Í½±Ù¥¹œİ¥Ñ ¹¼•½µ•ÑÉäé€‘•±…É…Ñ¥½¸½İ•¸%Ğ¥ÌÑ¡”…É¡•ÑåÁ”İ¡•É”½¹ÍÑÉÕÑ¥½¹€™¥¹…±±ä)Í•Á…É…Ñ•Ì™É½´™É…µ•}Ñ…Ù•É¹€è‰…±±½½¸™É…µ”•ÑÌ„Ñ¡¥¸€Ğ¥¸½É¹•È‰½…É°¹¼¥ÉĞ…¹„€ÄØ¥¸)µ½‘Õ±”ì‰É…•™É…µ”•ÑÌ„€Ø¥¸½É¹•ÈÁ½ÍĞ…¹„¥ÉĞ±¥¹”…ĞÑ¡”Í•½¹™±½½È¸±…‘‘¥¹€¥Ì)É•…É…Ñ¡•ÈÑ¡…¸¥¹½É•°İ¡¥ ¥ÌÑ¡”0ÈÈ‘•™•Ğ¹½ĞÉ•Á•…Ñ•¸¹Ñ¡”Õ¹™¥¹¥Í¡•ÍÑ…Ñ”¥Ì)‰Õ¥±‘…‰±”ƒŠP½Á•¸ÍÑÕ‘İ½É¬½Ù•È€ä¥¸‰½…ÉÍ¡•…Ñ¡¥¹œ½¸Ñ¡”±½…‘¥¹œ…‰±”°…ÑÑ•ÍÑ•¥¸­¥¹‰ä)¹‘É•…Ì™½ÈÑ¡”€©¡¥…¼•µ½É…Ğ¨Ì½İ¸‰Õ¥±‘¥¹œ…ĞM½ÕÑ ]…Ñ•È…¹±…É¬°€‰Õ¹™¥¹¥Í¡•…ĞÑ¡”)Ñ¥µ”ˆ¥¸9½Ù•µ‰•È€ÄàÌÌ¸9•Ù•È„‘•™…Õ±Ğ¸((ŒŒŒQ¡É•”‰ÕÌ¥Ğ™½Õ¹¥¸¹•¥¡‰½ÕÉ¥¹œ½‘”ƒŠP9=P™¥á•°…¹Ñ¡”Ñ¡¥É¥Ì„…Ñ”¡½±”((Ä¸€¨©5•Í¡	Õ¥±‘•È¹…‘‘}…‰±•}É½½™€™¥±±Ì•… …‰±”•¹İ¥Ñ „Í½±¥ÑÉ¥…¹±”€À¸ÈÔ´=UQ	=I½˜(€€Ñ¡”İ…±°¸¨¨M¼…¹åÑ¡¥¹œ‘É…İ¸½¸„…‰±”…ĞÑ¡”İ…±°Á±…¹”¥Ì€©¥¹Í¥‘”¨Ñ¡”É½½˜…¹¥¹Ù¥Í¥‰±”¸(€€±½}‘İ•±±¥¹œ¹}±½™Ñ}½Á•¹¥¹€‘½•Ì•á…Ñ±äÑ¡¥Ìè¥ÑÌ±½™Ğ½Á•¹¥¹Ì…É”¹½Ğ¥¸Ñ¡”½µµ¥ÑÑ•(€€É•™•É•¹”¥µ…”…¹¹•Ù•Èİ•É”¸•¹•É…Ñ½ÈÑ¡…ĞÍ¥±•¹Ñ±äÍİ…±±½İÌ¥ÑÌ½İ¸½ÕÑÁÕĞ¥ÌÑ¡”İ½ÉÍĞ(€€­¥¹½˜‰Õœ¡•É”°‰•…ÕÍ”Ñ¡”É•™•É•¹”É•¹‘•È¥Ìİ¡…Ğ„É•Ù¥•İ•È¡•­Ì¸(È¸€¨©±½}‘İ•±±¥¹€Ì‰…­•1¡…Ìå}µ¥¸€ô€´À¸ÀØÕ€¨¨İ¡¥±”‘•±…É¥¹œI=U9}=9QPè(€€Á•É¥µ•Ñ•É€ƒŠP…¸½Á•¹¥¹œÍÕÉÉ½Õ¹‰•±½ÜÉ…‘”¸Q¡”Í…µ”‰Õœİ…Ì™½Õ¹…¹±…µÁ•¥¹Í¥‘”(€€™É…µ•}ÍÑ½É•™É½¹Ñ€ìÑ¡¥Ì½¹”¥Ì±¥Ù”¥¸Ñ¡”½µµ¥ÑÑ•…ÍÍ•Ğ°Í¼„É•½É¥Ìµ…­¥¹œ„™…±Í”(€€É½Õ¹µ½¹Ñ…Ğ±…¥´É¥¡Ğ¹½Ü¸(Ì¸€¨©™É…µ•}Ñ…Ù•É¹€‘•±…É•Ì½¹ÍÑÉÕÑ¥½¹€…¹…±±•Éå€¥¸=9MU5…¹‰Õ¥±‘Ì¹•¥Ñ¡•È¨¨ƒŠP(€€…¹Ñ•ÍÑ}½¹ÍÕµ•‘}…ÑÑÉ¥‰ÕÑ•Í}…ÑÕ…±±å}É•…¡}Ñ¡•}Á…É…µ•Ñ•ÉÍ€AMML°‰•…ÕÍ”¥Ğ½¹±äÉ•ÅÕ¥É•Ì(€€Ñ¡”É•Í½±Ù•€©Á…É…µ•Ñ•ÉÌ¨Ñ¼µ½Ù”°¹½ĞÑ¡”•½µ•ÑÉä¸Q½‘…ä•Ù•ÉäÉ•½ÉÍ…åÌ…±±•Éäè™…±Í•€°(€€Í¼Ñ¡”™…±ÍäÉÕ±”¡¥‘•Ì¥Ğì€¨©Ñ¡”™¥ÉÍĞÉ•½ÉÑ¡…ĞÍ…åÌÑÉÕ•€•ÑÌ•áÕÍ•™É½´„(€€•½µ•ÑÉäé€‘•±…É…Ñ¥½¸™½È„…±±•ÉäÑ¡…Ğ¥Ì¹•Ù•È‰Õ¥±Ğ¸¨¨Q¡…Ğ¥ÌÑ¡”•á…Ğ™…¥±ÕÉ”Ñ¡”(€€=9MU5½¹ÑÉ…Ğ•á¥ÍÑÌÑ¼ÁÉ•Ù•¹Ğ°Í¥ÑÑ¥¹œ¥¹Í¥‘”Ñ¡”Ñ•ÍĞÑ¡…Ğ¥ÌÍÕÁÁ½Í•Ñ¼•¹™½É”¥Ğ¸(€€¥á¥¹œ¥Ğµ•…¹ÌÑ¡”Ñ•ÍĞ¡…ÌÑ¼½µÁ…É”Ù•ÉÑ¥•Ì°¹½ĞÁ…É…µ•Ñ•ÉÌ¸((ŒŒLÔƒŠPMÑÉÕÑÕÉ”É•½É‘Ì((¨©EÕ•Õ•™¥ÉÍĞ°…¹¥Ğ¥Ì„É•É…‘”É…Ñ¡•ÈÑ¡…¸…¸…‘‘¥Ñ¥½¸è€ÈÄ‘½Õµ•¹Ñ•‘€Ù…±Õ•ÌÉ•ÍĞ½¸)±…Ñ•ÈÍ¡½±…ÉÍ¡¥À…±½¹”¨¨€ ÈÀÈØ´Àà´ÄÀ°MQQULƒ
œ€ĞÌ¤¸Q¡”•Ù¥‘•¹”±…‘‘•È¡…Ì„…Ñ”¹½Ü°…¹¥ÑÌ)™½ÕÉÑ ÉÕ±”¥Ì„½Õ¹Ñ•İ…É¹¥¹œÉ…Ñ¡•ÈÑ¡…¸…¸•ÉÉ½Èè„‘½Õµ•¹Ñ•‘€Ù…±Õ”İ¥Ñ ¹¼Í½ÕÉ”…Ğ)Ñ¥•È€Ì½È‰•ÑÑ•ÈƒŠP¹¼Á•É¥½‘½Õµ•¹Ğ°¹¼•å•İ¥Ñ¹•ÍÌÉ•½±±•Ñ¥½¸°¹¼½µÁ¥±…Ñ¥½¸™É½´Á¥½¹••È)Ñ•ÍÑ¥µ½¹äƒŠP¥Ì•¥Ñ¡•È…¸½Ù•ÈµÉ…‘•Ù…±Õ”½È…¸Õ¹‘•ÈµÑ¥•É•Í½ÕÉ”°…¹½¹±äÉ•…‘¥¹œÑ¡”Á…”)Í•ÑÑ±•Ìİ¡¥ ¸((¨©Q¡”Í½ÕÉ”¡…±˜¥Ì=9€ÈÀÈØ´Àà´ÄÀ…¹¥Ğİ…Ì™¥™Ñ••¸½˜Ñ¡”Ñİ•¹Ñäµ½¹”¨¨€¡MQQULƒ
œ€ĞĞ°)‘½Ì½IMI ½•Ù¥‘•¹•}Ñ¥•ÉÍ}¡¥…½±½ä¹µ‘€¤¸ÁÉ•™¥É”ÄÈİ€°ÁÉ•™¥É”ÈÜÍ€…¹ÁÉ•™¥É”ÈÜá€İ•É”)™•Ñ¡•…¹É•…¥¸™Õ±°ì…±°Ñ¡É•”ÑÉ…¹ÍÉ¥‰”¹•…ÈµÁÉ¥µ…ÉäÉ•½±±•Ñ¥½¸ƒŠPÑ¡”€©%¹Ñ•È=•…¸¨)½±µÍ•ÑÑ±•È¥¹Ñ•ÉÙ¥•İÌ½˜€Ä…¹€ÈÈ)Õ±ä€ÄààÌ°…¹Ñ¡”€©¡¥…¼5……é¥¹”¨½˜€ÄÔ5…ä€ÄàÔÜ‰Õ¥±Ğ½¸)!Õ‰‰…ÉÌ½İ¸…½Õ¹ĞƒŠP…¹…±°Ñ¡É•”İ•É”É…‘•€Ğ¸Q¡•ä…É”€È°¹¼Ù…±Õ”µ½Ù•°¹¼µ•Í İ•¹Ğ)ÍÑ…±”°…¹Ñ¡”½Õ¹ĞÉ•…‘Ì€¨©Í¥à¨¨¸Q¡”©Õ‘•µ•¹Ğ¥Ì…±Í¼„‘•±…É…Ñ¥½¸¹½ÜÉ…Ñ¡•ÈÑ¡…¸„ÑåÁ•)¹Õµ‰•Èè„É•½É‘…Ñ¥¹œ¥ÑÌ½İ¸É•ÑÉ¥•Ù…°…¹±…¥µ¥¹œ„Ñ•ÍÑ¥µ½¹äÉÕ¹œµÕÍĞ‘•±…É”)ÑÉ…¹ÍÉ¥‰•Í€°…¹¥ÑÌÑ¥•È¥ÌÑ¡”‰•ÍĞÉÕ¹œ¥Ğ‘•±…É•Ì¸((¨©Q¡”™½ÕÈÍ¡…ÉÀ½¹•Ì…É”İ¡…Ğ¥Ì±•™Ğ°…¹Ñ¡•ä…É”Ñ¡”•áÁ•¹Í¥Ù”¡…±˜¨¨èÍ…Õ…¹…Í¡}¡½Ñ•±€)™½É´¹ÍÑ½É¥•Í€…¹™½É´¹½¹ÍÑÉÕÑ¥½¹€°µ¥±±•É}¡½ÕÍ•€™½É´¹™É…µ•}…‘‘¥Ñ¥½¹}ÍÑ½É¥•Í€…¹)İ½±™}Á½¥¹Ñ}Ñ…Ù•É¹€™½É´¹Í¥¹€…É”ÍÕÁÁ½ÉÑ•‰ä¹½Ñ¡¥¹œ‰ÕĞÑ¡”Ñİ¼‘É±½¥¡€‰±½œ½µÁ¥±…Ñ¥½¹Ì°)İ¡½Í”½İ¸Í½ÕÉ”É•½É‘ÌÍ…ä€©¹•Ù•È…ÌÍ½±”•Ù¥‘•¹”¨¸I”µÑ¥•É¥¹œ…¹¹½ĞÑ½Õ Ñ¡•´ƒŠPÑ¡”Á…•Ì)…É”Õ¹™½½Ñ¹½Ñ•°µÕÑÕ…±±ä½¹ÑÉ…‘¥Ñ½Éä…¹Õ¹…É¡¥Ù•ƒŠPÍ¼Ñ¡¥Ì¥Ì„É•É…‘”½˜Ñ¡”Y1U°…¹)„½¹™¥‘•¹”¥Ì„µ•Í ¥¹ÁÕĞèÑ¡”Í±¥”ÍÑ…±•ÌÑ¡½Í”1	Ì…¹±…¹‘Ìİ¥Ñ „‰…­”¸	•¡¥¹¥Ğ°Ñ¡”)µ…¡¥¹”µÉ•…‘…‰±”¡…±˜ƒŠP„¹•Ù•É}Í½±•}•Ù¥‘•¹•€™±…œ½¸„Í½ÕÉ”É•½É°İ¡¥ ÑÕÉ¹ÌÑ¡½Í”™½ÕÈ)¥¹Ñ¼•ÉÉ½ÉÌƒŠPÍÑ…åÌ‘•±¥‰•É…Ñ•±ä‰•¡¥¹Ñ¡”É•É…‘”°‰•…ÕÍ”„…Ñ”Ñ¡…Ğ™…¥±ÌÑ¡”½µµ¥ÑÑ•)‘…Ñ…Í•Ğ½¸Ñ¡”‘…ä¥Ğ±…¹‘Ì¥Ì„…Ñ”Ñ¡…Ğ•ÑÌÍİ¥Ñ¡•½™˜¸((¨©Q¡”½Ñ¡•ÈÑİ¼…É”½ÕÑÍ¥‘”Ñ¡”‰Õ¥±‘¥¹Ì¨¨èÉ½Õ¹ÍÕÉ™…•}µ…Ñ•É¥…±Ì¹Í½ÕÑ¡}‘¥Ù¥Í¥½¹€(¡¡¥…½}…É¡¥Ñ•ÑÕÉ•}¡¥ÍÑ½Éå|ÄÄÕ€¤…¹É½Õ¹İ…Ñ•É€€¡İ¥­¥Á•‘¥…}¡¥…½}É¥Ù•É€¤¸ùùQ¡”™¥ÉÍĞ)½˜Ñ¡½Í”¡…Ì¹½Ğ‰••¸½Á•¹•¹ùø€¨©	½Ñ …É”É•……¹‰½Ñ …É”½Ù•ÈµÉ…‘•Y1UL¨¨ƒŠPİ…Ñ•É€½¸(ÈÀÈØ´Àà´ÄÄ€£
œ€ĞØ°‘½Ì½IMI ½Íİ•…É¥¹•¹|ÄàÀÌ¹µ‘€¤…¹Ñ¡”Í½¥°ÁÉ½™¥±”Ñ¡”Í…µ”‘…ä(¡MQQULƒ
œ€ÔÄ°‘½Ì½IMI ½ÍÕÉ™…•}µ…Ñ•É¥…±Í}Í½ÕÑ¡}‘¥Ù¥Í¥½¸¹µ‘€¤¸Q¡”Í½¥°Á…”¥Ì„€ÈÀÈÈ•ÍÍ…ä)Ñ¡…Ğ¥Ì¥ÑÌ½İ¸‘½Õµ•¹Ğ°½ÉÉ•Ñ±ä…ĞÉÕ¹œ€Ğ°…¹¥ĞÁÉ¥¹ÑÌ€¨©¹¼™½½Ñ¹½Ñ”°•¹‘¹½Ñ”½ÈÉ•™•É•¹”)…¹åİ¡•É”¥¸¥Ğ¨¨ìÑ¡”½¹”İ¥Ñ¹•ÍÌ½¸¥ĞƒŠP)½¡¸5¥±±ÌY…¸=Í‘•°°‰±½¬µÅÕ½Ñ•İ¥Ñ ¹¼ÁÕ‰±¥…Ñ¥½¸°)‘…Ñ”½ÈÁ…”°…¹Õ¹µ•¹Ñ¥½¹•‰äÑ¡¥ÌÁÉ½©•ĞÌ½İ¸‘½ÍÍ¥•ÈƒŠP…ÑÑ•ÍÑÌÑ¡”=IH½˜Ñ¡”ÍÑÉ…Ñ„…¹)Ñ¡”‘É…¥¹…”™…¥±ÕÉ”…¹¥Ù•Ì€¨©¹¼‰±…¬±½…´…¹¹½Ğ½¹”Ñ¡¥­¹•ÍÌ¨¨°Í¼Ñ¡”Ñ¡É•”™¥ÕÉ•Ì¥¸)Ñ¡”±…¥´¡…Ù”¹½‰½‘ä‰•¡¥¹Ñ¡•´¸‘½Õµ•¹Ñ•‘€ƒŠH¥¹™•ÉÉ•‘€°…¹¥Ğ±…¹‘Ìİ¥Ñ Ñ¡”‰…­”¸((¨©Q¡”Ñ¡É•”Á…•ÌÑ¡…Ğ±½½­•±¥­”Ñ¡”Í…µ”…Í”İ•É”½Á•¹•€ÈÀÈØ´Àà´ÄÄ¨¨€¡MQQULƒ
œ€ĞÔ°)‘½Ì½IMI ½•Ù¥‘•¹•}Ñ¥•ÉÍ}É½Õ¹‘}Ñİ¼¹µ‘€¤°…¹Ñİ¼½˜Ñ¡•´İ•É”¸ÁÉ•™¥É”ÀØÉ€É•ÁÉ¥¹ÑÌ(¨©¹‘É•…Ì¨¨°İ¡¼ÅÕ½Ñ•ÌÑ¡”€©¡¥…¼µ•É¥…¸¨½˜€ä)Õ±ä€¨¨ÄàÌØ¨¨€¡¹½Ğ€ÄàÌÔ¤™½ÈÑ¡”1…­”…¹)1„M…±±”™É½œÁ½¹ƒŠPÑ¥•È€Ì°½¸¹‘É•…Ì…¹‘•±¥‰•É…Ñ•±ä¹½Ğ½¸Ñ¡”¹•İÍÁ…Á•È¹½‰½‘ä¡•É”¡…Ì)½Á•¹•¸ÁÉ•™¥É”ÈÜÙ€É•ÁÉ¥¹ÑÌÑ¡”€©¡¥…¼5……é¥¹”¨½˜€ÄÔ5…ä€ÄàÔÜ°Ñ¡”Í…µ”‘½Õµ•¹Ğ…¹Ñ¡”)Í…µ”É•…‘¥¹œ…ÌÁÉ•™¥É”ÈÜÍ€ƒŠPÑ¥•È€È°İ¥Ñ Ñ¡”€ÄàÔØ€©QÉ¥‰Õ¹”¨¹½Ñ¥”‰•Í¥‘”¥Ğ±•™ĞÕ¹‘•±…É•)‰•…ÕÍ”¹¼±…¥´¡•É”É•ÍÑÌ½¸¥Ğ¸9•¥Ñ¡•ÈÁ…”¥Ì¥Ñ•‰ä…¹åÑ¡¥¹œÑ½‘…ä°Í¼Ñ¡”±…‘‘•È½Õ¹Ğ)ÍÑ…åÌ…ĞÍ¥àì‰½Ñ …É”ÅÕ•Õ•É•Í•…É €¡LÈÁ…É•°€¡Œ¤ÌÁ½¹°…¹Ñ¡”™½ÉĞ¤Ñ¡…Ğ…¸¹½Ü‰”)É…‘•¡½¹•ÍÑ±äİ¡•¸¥Ğ¥ÌİÉ¥ÑÑ•¸¸((¨©İ¥­¥Á•‘¥…}¡¥…½}É¥Ù•É€İ…Ì9=PÑ¡”…Í”°…¹Ñ¡…Ğ¥ÌÑ¡”™¥¹‘¥¹œİ¥Ñ „½¹Í•ÅÕ•¹”¸¨¨%Ğ)É•ÁÉ¥¹ÑÌ¹½Ñ¡¥¹œƒŠP½¹”Í•¹Ñ•¹”½˜•¹å±½Á•‘¥„ÁÉ½Í”Á…É…Á¡É…Í¥¹œMİ•…É¥¹•¸İ¥Ñ „™½½Ñ¹½Ñ”Ñ¼(¨©EÕ…¥™”€ÄäÄÌ°ÁÀ¸€ÌÜÌ´ÌÜÜ¨¨°İ¡¥ ¥ÌÑ¡”ÁÉ¥µ…ÉäÁÉ¥¹Ñ¥¹œÑ¡”É•½É¡…Ì…Í­•™½ÈÍ¥¹”¥Ğİ…Ì)İÉ¥ÑÑ•¸¸Qİ¼Ñ¡¥¹Ì½µ”½™˜¥Ğè()ğÅÕ•Õ•ğİ¡…Ğ¥Ğ½ÍÑÌğ)ğ´´µğ´´µğ)ğùù•Ñ EÕ…¥™”€ÄäÄÌÁÀ¸€ÌÜÌ´ÌÜÜ…¹É•½ÉMİ•…É¥¹•¸Ì€ÄàÀÌÍ½Õ¹‘¥¹Ì…ĞÑ¡•¥È½İ¸ÉÕ¹ùøğ€¨©=9€ÈÀÈØ´Àà´ÄÄ¨¨ƒŠPÅÕ…¥™•|ÄäÄÍ}Íİ•…É¥¹•¹€°Ñ¡”‘…Ñ…Í•ĞÌ™¥ÉÍĞÑ¥•È´ÄİÉ¥ÑÑ•¸•å•İ¥Ñ¹•ÍÌ‘½Õµ•¹Ğìµ•µ¼‘½Ì½IMI ½Íİ•…É¥¹•¹|ÄàÀÌ¹µ‘€¸¹€¨©Ñ¡”ÁÉ¥”…‰½Ù”İ…ÌİÉ½¹œ¨¨è•¹•É…Ñ½ÉÌ½Ñ•ÉÉ…¥¹}¥¹ÁÕÑÌ¹Áå€ÍÑÉ¥ÁÌÍ½ÕÉ•Í€™É½´Ñ¡”Ñ•ÉÉ…¥¸¡…Í …±½¹œİ¥Ñ Ñ¡”ÁÉ½Í”°Í¼¥Ñ¥¹œ¥Ğ™É½´Ñ•ÉÉ…¥¹}ÍÁ•Œ¹©Í½¹€½ÍĞ¹½Ñ¡¥¹œ…¹İ…Ì‘½¹”¥¸Ñ¡”Í…µ”Í±¥”¸½¹™¥‘•¹•€¥ÌÑ¡”µ•Í ¥¹ÁÕĞ°¹½Ğ„¥Ñ…Ñ¥½¸ğ)ğ€¨©É½Õ¹İ…Ñ•É€è‘½Õµ•¹Ñ•‘€ƒŠH¥¹™•ÉÉ•‘€¨¨ƒŠPÑ¡”™±…ĞÍÕÉ™…”É•ÍÑÌ½¸…¸Õ¹™½½Ñ¹½Ñ••¹å±½Á•‘¥„Í•¹Ñ•¹”…‰½ÕĞÍ±Õ¥Í ™±½Ü°¹½Ğ½¸Mİ•…É¥¹•¸°İ¡¼¥Ù•Ì¹¼É…‘¥•¹Ğ…¹µ•…ÍÕÉ•Ì€Ä¸Èµ¥±•Ì‘½İ¹ÍÑÉ•…´ğ„½¹™¥‘•¹”¥Ì„µ•Í ¥¹ÁÕĞè¥ĞÍÑ…±•ÌÑ¡”É½Õ¹…¹±…¹‘Ìİ¥Ñ ¥ÑÌ	±•¹‘•È‰…­”°•á…Ñ±ä±¥­”Ñ¡”™½ÕÈ‘É±½¥¡€Ù…±Õ•Ì¸€¨©	•ÑÑ•È…ÉÕ•…Ì½˜€ÈÀÈØ´Àà´ÄÄ…¹Õ¹¡…¹•¥¸‘¥É•Ñ¥½¸¨¨èÉ•…‘¥¹œMİ•…É¥¹•¸µ…‘”Ñ¡”…Í”ÍÑÉ½¹•ÈÉ…Ñ¡•ÈÑ¡…¸É•ÍÕ¥¹œ¥Ğ°‰•…ÕÍ”¡¥Ì€‘•…İ…Ñ•Èœ¥Ì…ÑÑÉ¥‰ÕÑ•¥¸Ñ¡”Í…µ”±…ÕÍ”Ñ¼„µ½ÕÑ ÍÑ½ÁÁ•‰äÍ…¹ƒŠPÑ¡””ÄàÌÁ}¹…ÑÕÉ…±€½¹‘¥Ñ¥½¸Ñ¡”€ÄàÌĞÕĞÉ•µ½Ù•¸!”¥Ì‘•±¥‰•É…Ñ•±ä9=P¥Ñ•½¸Ñ¡”İ…Ñ•ÈÁ±…¹”ìÑ¡”‰±½¬Ì¹½Ñ”Í…åÌÍ¼İ¡•É”„Ù¥Í¥Ñ½ÈÉ•…‘Ì¥Ğğ()Q¡…Ğ¥ÌÑ¡”€¨©™¥ÉÍĞ½˜Ñ¡”Í¥àİ…É¹¥¹ÌÍ•ÑÑ±•¥¸Ñ¡”½Ù•ÈµÉ…‘•‘¥É•Ñ¥½¸¨¨ƒŠPÑ¡”Í½ÕÉ”¥Ì)½ÉÉ•Ñ±äÑ¥•É•…¹Ñ¡”Ù…±Õ”¥Ì¹½Ğ¸((¨©¹Ñ¡”ÁÉ¥µ…ÉäÁÉ¥¹Ñ¥¹œ…ÉÉ¥Ù•€ÈÀÈØ´Àà´ÄÄ°İ¡¥ ½ÍĞÑ¡”•¹å±½Á•‘¥„½¹”½˜¥ÑÌÑİ¼‰…¹¬)™¥ÕÉ•Ì¨¨€¡MQQULƒ
œ€ĞØ°‘½Ì½IMI ½Íİ•…É¥¹•¹|ÄàÀÌ¹µ‘€¤¸EÕ…¥™”ÌÁÁ•¹‘¥à$¥Ì¹½Ü)ÅÕ…¥™•|ÄäÄÍ}Íİ•…É¥¹•¹€…ĞÑ¥•È€Ä°É•…™É½´Ñİ¼%¹Ñ•É¹•ĞÉ¡¥Ù”Í…¹ÌÑ¡…Ğ…É•”¡…É…Ñ•È)™½È¡…É…Ñ•È¸]¥­¥Á•‘¥„Ì€¨ˆØ™Ğ½¸Ñ¡”¹½ÉÑ ˆ¨¥Ì¹½İ¡•É”¥¸Ñ¡”©½ÕÉ¹…°èMİ•…É¥¹•¸¥Ù•Ì¹¼)¹½ÉÑ µ‰…¹¬¡•¥¡Ğ°½¹±ä„‰½Õ¹‘•‘¥™™•É•¹”™±…•…Ìµ…‘”€©‰ä…ÁÁ•…É…¹•Ì¨°…¹€Ø¥Ìİ¡…Ğ„)±…Ñ•ÈİÉ¥Ñ•È½Ğ‰äÍÕ‰ÑÉ…Ñ¥¹œÑ¡”µ…á¥µÕ´™É½´€à¸]¡…ĞÑ¡”Á…É…Á¡É…Í”‘É½ÁÁ•µ…ÑÑ•ÉÌµ½É”ƒŠP(¨‰Ñ¡”‰…¹­Ì…‰½Ù”…É”ÅÕ¥Ñ”±½Üˆ¨¥ÌÑ¡”½¹±äÍ•¹Ñ•¹”¥¸Ñ¡”Á…ÍÍ…”…‰½ÕĞÑ¡”É•… Ñ¡¥Ì)ÁÉ½©•Ğµ½‘•±Ì°…¹¥Ğ¥Ì…ÑÑ…¡•Ñ¼Ñ¡”ÍÁ•ŒÌ‰…¹­€‰±½¬¹½Ü°İ¡¥ ¥Ñ•¹½Ñ¡¥¹œ‰•™½É”¸)½ÕÉÑ ¥Ñ…Ñ¥½¸™½Õ¹µ¥Í‘•ÍÉ¥‰¥¹œ¥ÑÌ½İ¸Á…”°…¹Ñ¡”™¥ÉÍĞ™½Õ¹‰ä½Á•¹¥¹œÑ¡”‘½Õµ•¹Ğ)É…Ñ¡•ÈÑ¡…¸Ñ¡”¡½ÍĞ¸ùùM¥àÁ…•Ì…ĞÑ¥•È€Ğ½Èİ•…­•ÈÍÑ¥±°‘•±…É”¹½Ñ¡¥¹œ(¡¡¥…½}Ñ•µÁ±•}¡¥ÍÑ½Éå€°¡¥…½±½å}™¥ÉÍÑ}Á½ÍÑ}½™™¥•€°¡¥…½±½å}±…ÍÑİ…É‘…¹•€°)¡¥…½±½å}ÁÉ•™¥É”ÈÜÑ€°‘É±½¥¡}¡½Ñ•±Í€°‘É±½¥¡}İ½±™}Á½¥¹Ñ€¤°½Õ¹Ñ•‰äÑ¡”Ù…±¥‘…Ñ½È•Ù•Éä)ÉÕ¸°…¹Ñ¡”Ñİ¼‘É±½¥¡€Á…•Ì…É”¹½ĞÍ½±Ù…‰±”Ñ¡¥Ìİ…ä¹ùø((¨©Q¡”™½ÕÈÑ¡…Ğ½Õ±‰”½Á•¹•İ•É”½Á•¹•€ÈÀÈØ´Àà´ÄÄ°…¹Ñ¡”½Õ¹ĞÉ•…‘ÌÑİ¼¨¨€¡MQQULƒ
œ€ĞÜ°)‘½Ì½IMI ½•Ù¥‘•¹•}Ñ¥•ÉÍ}É½Õ¹‘}Ñ¡É•”¹µ‘€¤¸¡¥…½±½å}±…ÍÑİ…É‘…¹•€¥ÌÑ¡”€©¡¥…¼)QÉ¥‰Õ¹”¨½˜€ÄĞÕÕÍĞ€ÄäÄÀÁÉ¥¹Ñ¥¹œ€¨©)½¡¸•…¸…Ñ½¸Ì½İ¸İÉ¥ÑÑ•¸É•½±±•Ñ¥½¸¨¨ƒŠP…¸)¥‘•¹Ñ¥™¥••å•İ¥Ñ¹•ÍÌ°¹½ĞÑ¡”€‰±…Ñ•È½µÁ¥±…Ñ¥½¸½˜É•½±±•Ñ¥½¹ÌˆÑ¡”É•½É±…¥µ•ƒŠP…¹¥Ì)ÉÕ¹œ€È¸¡¥…½±½å}ÁÉ•™¥É”ÈÜÑ€¥Ì€©¡¥…¼5……é¥¹”¨°5…É €ÄàÔÜ°Ñ¡”¥¹ÍÑ…±±µ•¹Ğ‰•™½É”)ÁÉ•™¥É”ÈÜÙ€°…¹¥ÌÑ¡”™¥ÉÍĞÍ½ÕÉ”¡•É”É…‘•€¨©‰äİ¡¥ Á…ÉĞ½˜¥Ğå½ÔÍÑ…¹½¸¨¨èÉÕ¹œ€È)™½ÈÑ¡”±…¹‘™½É´Ñ¡¥ÌÁÉ½©•Ğ¥Ñ•Ì°¹¼‰•ÑÑ•ÈÑ¡…¸€Ì™½È¥ÑÌ€ÄàÀÌ´ÄàÄÈ™½ÉĞ¹…ÉÉ…Ñ¥Ù”°İ¡¥ )¹½Ñ¡¥¹œ¥Ñ•Ì¸¡¥…½±½å}™¥ÉÍÑ}Á½ÍÑ}½™™¥•€İ…ÌÉ•……¹€¨©±•™Ğ…Ğ€Ğ¨¨ƒŠPÕÉÉ•ä€ÄäÈÈ¹…µ¥¹œ)¹¼…ÕÑ¡½É¥Ñä™½ÈÑ¡”Á½ÍĞµ½™™¥”™…ÑÌƒŠPİ¡¥ ¥Ìİ¡…ĞÑ¡¥ÌÍ•Ñ¥½¸µ•…¹Ğ‰ä€©Õ¹É•…É…Ñ¡•ÈÑ¡…¸)İÉ½¹œ¨¸¡¥…½}Ñ•µÁ±•}¡¥ÍÑ½Éå€É•ÁÉ¥¹ÑÌ¹½Ñ¡¥¹œ…¹Í…åÌÍ¼¥¸…ÉÉ¥•Í}¹½}‘½Õµ•¹Ñ€ì¥ÑÌ)µ¥ÍÍ¥¹œ…É¡¥Ù•‘}ÕÉ±€¥Ì™¥±±•™É½´„€ÈÀÈØ´ÀØ´ÀÔÍ¹…ÁÍ¡½ĞÙ•É¥™¥•……¥¹ÍĞ‰½Ñ ÅÕ½Ñ…Ñ¥½¹Ì°)½¹”ÍÑ…¹‘¥¹œİ…É¹¥¹œ½¹”¸((¨©Q¡”™¥¹‘¥¹œ¥Ì½¸Ñ¡”Á½ÍĞµ½™™¥”Á…”…¹¥ĞÑ½Õ¡•ÌLä¸¨¨Q¡”€ØØ™ĞÍÑÉ••Ğµ½‘Õ±”ƒŠPÑ¡”)‘¥ÍÍ•¹Ğ……¥¹ÍĞÑ¡”€àÀ™Ğ•Ù•ÉäÁ±…ÑÑ•Á±…•µ•¹Ğ¥Ì½™™Í•Ğ™É½´ƒŠP¥Ì€©¹½ĞÁ…ÉĞ½˜ÕÉÉ•äÌ)…ÉÑ¥±”¨è¥Ğ¥¹Ñ•ÉÉÕÁÑÌ¡¥Ì¡É½¹½±½ä°¥ÑÌÍÕ‰©•Ğ¥Ì„ÍÕÉÙ•ä¥¸…¸…ÉÑ¥±”…‰½ÕĞ‰Õ¥±‘¥¹Ì°)…¹¥Ğ¥ÌÑ¡”½¹”Á…É…É…Á ¹…µ¥¹œ¹¼…ÕÑ¡½É¥Ñäİ¡¥±”İÉ¥Ñ¥¹œ€‰‘½İ¹ÍÑ…Ñ”I…¹‘½±Á ½Õ¹Ñäˆ¸%Ğ¥Ì)Õ¹‘•±…É•°½™˜Ñ¡”±…‘‘•È°…¹‘…Ñ„½ÑÉ…•Ì½ÍÑÉ••Ñ}½¹ÑÉ½°¹©Í½¹€¹¼±½¹•ÈÍ…åÌ€‰ÕÉÉ•äÍÑ…Ñ•Ìˆ¸)9¼¹Õµ‰•Èµ½Ù•ÌƒŠPÑ¡”™¥ÕÉ”İ…Ì…±É•…‘ä•á±Õ‘•‰äµ•…ÍÕÉ•µ•¹ĞƒŠP‰ÕĞÑ¡”‘¥ÍÍ•¹Ğ¥Ì¹½Ü„)Í½ÕÉ•±•ÍÌİ•‰Í¥Ñ”Í•¹Ñ•¹”É…Ñ¡•ÈÑ¡…¸„¹…µ•¡¥ÍÑ½É¥…¸°İ¡¥ ¥Ì„‘¥™™•É•¹ĞÑ¡¥¹œ™½ÈÑ¡”)ÍÑÉ••ÑÌÁ…É•°Ñ¼İ•¥ ¸((¨©]¡…Ğ¥Ì±•™Ğ½˜Ñ¡¥ÌÑ¡É•…¥Ì¹½ĞÉ•Í•…É °…¹…Ì½˜€ÈÀÈØ´Àà´ÄÄÑ¡…Ğ¥ÌÑÉÕ”½˜…±°Í¥à¸¨¨)=¹±ä‘É±½¥¡}¡½Ñ•±Í€…¹‘É±½¥¡}İ½±™}Á½¥¹Ñ€ÍÑ¥±°‘•±…É”¹½Ñ¡¥¹œ°…¹Ñ¡¥Ìµ•Ñ¡½‘½•Ì¹½ĞÉ•… )Ñ¡•´èÑ¡”Á…•Ì…É”Õ¹™½½Ñ¹½Ñ•°µÕÑÕ…±±ä½¹ÑÉ…‘¥Ñ½Éä…¹Õ¹…É¡¥Ù•°…¹Ñ¡•¥È™½ÕÈÙ…±Õ•Ì¹••)Ñ¡”Y1UÉ•É…‘•°İ¡¥ ¥Ì„µ•Í ¥¹ÁÕĞ¸€¨©Q¡…ĞÍ±¥”°É½Õ¹İ…Ñ•É€…¹É½Õ¹)ÍÕÉ™…•}µ…Ñ•É¥…±Ì¹Í½ÕÑ¡}‘¥Ù¥Í¥½¹€…É”½¹”‰…­”¨¨ƒŠP™¥Ù”Ù…±Õ•Ì°Í¥àİ…É¹¥¹Ì°Ñ…­”Ñ¡•´Ñ½•Ñ¡•È)½¸„ÉÕ¹¹•Èİ¥Ñ 	±•¹‘•È¸Ù•ÉäÁ…”‰•¡¥¹Ñ¡”Í¥à¡…Ì¹½Ü‰••¸½Á•¹•…¹Ñ¡”Ù•É‘¥Ğ½¸•Ù•Éä)½¹”½˜Ñ¡•´¥ÌÑ¡”Í…µ”èÑ¡”Í½ÕÉ”¥ÌÑ¥•É•½ÉÉ•Ñ±ä…¹Ñ¡”Ù…±Õ”¥ÌÉ…‘•Ñ½¼¡¥ ¸(((¨©Q¡”É•Á…¥ÈÅÕ•Õ”Ñ¡…Ğ…µ”‰•™½É”¥Ğ°…±°½˜¥Ğ=9ƒŠPÑ¡É•”…ÑÑÉ¥‰ÕÑ•ÌÑ¡…Ğİ•É”É•½É‘•)…¹Õ¹‰Õ¥±Ğ¸¨¨½Õ¹‰äÑ¡”½µ¥ÍÍ¥½¸…Ñ”½¸€ÈÀÈØ´Àà´ÄÀ…¹…‘µ¥ÑÑ•µ•…¹İ¡¥±”‰ä0ÈÀ…¹0ÈÄ¸()ğÉ•½Éğ…ÑÑÉ¥‰ÕÑ”ğİ¡…ĞÑ¡”…É¡•ÑåÁ”É•…‘Ìğ•™™•Ğğ)ğ´´µğ´´µğ´´µğ´´µğ)ğùùİ½±™}Á½¥¹Ñ}Ñ…Ù•É¹ùøğùù™É…µ•}•áÑ•¹Í¥½¹ùøğ™É…µ•}…‘‘¥Ñ¥½¹€ğ€¨©=9€ÈÀÈØ´Àà´ÄÀ¨¨ƒŠPÉ•¹…µ•°‘¥µ•¹Í¥½¹•…¹É”µ‰…­•¥¸½¹”Í±¥”ğ)ğùùİ½±™}Á½¥¹Ñ}Ñ…Ù•É¹ùøğùùÍ¥¹…•ùøğÍ¥¹€ğ€¨©=9€ÈÀÈØ´Àà´ÄÀ¨¨ƒŠPÑ¡”‰½…É¡…¹Ì½¸Ñ¡”É¥Ù•È™É½¹ĞìÑ¡”İ½±˜¥Ì¹½Ğ‘É…İ¸€¡0ÈÔ¤ğ)ğùùµ¥±±•É}¡½ÕÍ•ùøğùù¡¥µ¹•åÌè€Éùøğ¡¥µ¹•å€€¡„‰½½±•…¸¤ğ€¨©=9€ÈÀÈØ´Àà´ÄÀ¨¨ƒŠPÑ¡”½Õ¹Ğ¥Ì„Á…É…µ•Ñ•È½˜‰½Ñ …É¡•ÑåÁ•ÌìÑ¡”Í•½¹ÍÑ…¬ÍÑ…¹‘Ì½¸Ñ¡”™É…µ”É…¹”ğ((¨©Q¡”½¹”É•Á…¥È™½Õ¹‰äÉ•…‘¥¹œÉ…Ñ¡•ÈÑ¡…¸‰ä„…Ñ”¥Ì=9¨¨€ ÈÀÈØ´Àà´ÄÀ°MQQULƒ
œ€ÈÌƒŠHƒ
œ€ÈĞ¤è()ğÉ•½Éğ…ÑÑÉ¥‰ÕÑ”ğİ¡…ĞÑ¡”•Ù¥‘•¹”Í…åÌğ•™™•Ğğ)ğ´´µğ´´µğ´´µğ´´µğ)ğùù¹½ÉÑ¡}‰É…¹¡}‰É¥‘•ùøğùùÁ¥•É}ÍÁ…¥¹}µùø€ ÄÔÉ¥‰Ì…ĞÑ¡”…É¡•ÑåÁ”‘•™…Õ±Ğ¤ğ€¨©Ñİ¼€‰‰•¹ÑÌˆ½˜™½ÕÈ¡•…Ùä±½ÌÉ•ÍÑ¥¹œ½¸Ñ¡”‰½ÑÑ½´¨¨ğ€¨©=9¨¨ƒŠPÁ¥•É}½Õ¹Ğè€É€É•Á±…•ÌÑ¡”ÍÁ…¥¹œ¥¸É•½É…¹…É¡•ÑåÁ”ì0ÈäÉ•Í½±Ù•°0ÌÄ¹•Üğ)ğùù¹½ÉÑ¡}‰É…¹¡}‰É¥‘•ùøğùùÁ¥•É}­¥¹èÉ¥‰ùøğÑ¡”Í•ÑÑ±•ÉÌœ½İ¸İ½É¥Ì€¨©‰•¹ÑÌ¨¨ƒŠP…¹±•…Ù•ÈÍ¥¹•¥Ğğ€¨©=9¨¨ƒŠP‰•¹Ñ€‰•Í¥‘”É¥‰€…¹Á¥±•€ì™½ÕÈ¡•…Ùä±½ÌÕ¹‘•È„…Àğ)ğùù¹½ÉÑ¡}‰É…¹¡}‰É¥‘•ùøğùù±•…É…¹•}µùø€¡¥¹™•ÉÉ•‘€°Á…”¹½Ğ™½Õ¹¤ğ€¨¨‰…‰½ÕĞÍ¥à™••Ğ…‰½Ù”Ñ¡”İ…Ñ•È°Í¼Ñ¡…ĞÑ•…µÌÁ…ÍÍ•Õ¹‘•ÈÑ¡•´½¸Ñ¡”¥”™É••±äˆ¨¨ğ€¨©=9¨¨ƒŠP‘½Õµ•¹Ñ•‘€½¸½±‘}Í•ÑÑ±•ÉÍ}‰É¥‘•Í|ÄààÍ€ìÑ¡”‘•¬…¹ÍÑÉ¥¹•ÉÌ½µ”½ÕĞ½˜‘¥Ñ¡•É¥¹œğ)ğùù¹½ÉÑ¡}‰É…¹¡}‰É¥‘•ùøğùù‘•­ùø€¡…É¡•ÑåÁ”Ì°Õ¹ÍÑ…Ñ•¤ğ€¨¨‰ÁÕ¹¡•½¹Ì½ÈÍÁ±¥Ğ±½Ìİ•É”±…¥™½È„™±½½Èˆ¨¨ğ€¨©=9¨¨ƒŠP‘•­}­¥¹èÁÕ¹¡•½¹€°„Ù…±Õ”Ñ¡”•¹•É…Ñ½ÈÉ•…‘Ìğ()±°™½ÕÈİ•É”µ•Í ¥¹ÁÕÑÌ°Í¼Ñ¡”É•½É°Ñ¡”…É¡•ÑåÁ”¡…¹”…¹Ñ¡”‰…­”±…¹‘•…Ì½¹”Í±¥”ƒŠP)Ñ¡”Í…µ”½ÕÁ±¥¹œÑ¡”¹½Ñ”‰•±½Ü‘•ÍÉ¥‰•Ì°…ÉÉ¥Ù¥¹œ™É½´„¹•Ü‘¥É•Ñ¥½¸¸Q¡”•Ù¥‘•¹”¥Ì„)Í¥¹•€ÄààÌÍÑ…Ñ•µ•¹Ğ‰ä™½ÕÈµ•¸İ¡¼ÕÍ•Ñ¡”‰É¥‘”°ÁÉ¥¹Ñ•…Ì„™½½Ñ¹½Ñ”…Ğ¹‘É•…Ì)ÁÀ¸€ØÌÄ´ØÌÈ…¹µ¥ÍÍ•‰äÑ¡”™Õ±°µÑ•áĞ¥¹‘•àìÍ•”‘½Ì½IMI ½¹½ÉÑ¡}‰É…¹¡}‰É¥‘”¹µ‘€ƒ
œ€Ø¸((¨©Q¡”±•ÍÍ½¸¥Ì…‰½ÕĞÑ¡”Á…É…µ•Ñ•È°¹½ĞÑ¡”¹Õµ‰•È¸¨¨‰É¥‘•}Ñ¥µ‰•É€‘¥Ù¥‘•„ÍÁ…¸‰ä„)ÍÁ…¥¹œ°Í¼¥Ğ½Õ±½¹±ä•Ù•ÈÁÉ½‘Õ”„½±½¹¹…‘”ì¹¼Í½ÕÉ”İ¥±°•Ù•ÈÍÑ…Ñ”„ÍÁ…¥¹œ°…¹İ¡…Ğ)„İ¥Ñ¹•ÍÌÉ•µ•µ‰•ÉÌ¥Ì„½Õ¹Ğ…¹„™½É´¸M•ÑÑ¥¹œ€Ğ¸Ô´Ñ¼€ÈÌ¸äĞ´İ½Õ±¡…Ù”™¥á•Ñ¡¥Ì‰É¥‘”)…¹±•™ĞÑ¡”¹•áĞ½¹”Ñ¼‰”™½Õ¹‰äÑ¡”Í…µ”…¥‘•¹Ğ¸]½ÉÑ …Í­¥¹œ½˜…¹ä…É¡•ÑåÁ”İ¡½Í”)‘•™…Õ±ÑÌ…É”…‰½ÕĞÑ¼‰”½Ù•ÉÉ¥‘‘•¸è¥Ì¥Ğ…Í­¥¹œ™½ÈÑ¡”­¥¹½˜¹Õµ‰•È„Í½ÕÉ”½Õ±½¹Ñ…¥¸ü)]¡…ĞÑ¡”É•Á…¥È½Õ±¹½ĞÍ•ÑÑ±”¥Ìİ¡•É”…±½¹œÑ¡”ÍÁ…¸Ñ¡”Ñİ¼‰•¹ÑÌÍÑ½½ƒŠPÑ¡”±•ÑÑ•È±½…Ñ•Ì)Ñ¡•´‰ä‘•ÁÑ °¥¸„É¥Ù•Èİ¡½Í”‰•Ñ¡¥ÌÁÉ½©•Ğ‘½•Ì¹½Ğµ½‘•°ƒŠPÍ¼Ñ¡•äÍ¥Ğ…ĞÑ¡”Ñ¡¥ÉÁ½¥¹ÑÌ)…¹€¨©0ÌÄ¨¨…‘µ¥ÑÌ¥Ğ°Ñ½•Ñ¡•Èİ¥Ñ Ñ¡”ÍÁ±¥•Ì¥¸Ñ¡É•”€ÈÌ¸ä´ÍÑÉ¥¹•ÈÉÕ¹ÌÑ¡…Ğ¹¼Í½ÕÉ”)Á±…•Ì¸()… ½˜Ñ¡”•…É±¥•ÈÉ•Á…¥ÉÌİ…Ì„Íµ…±°‘…Ñ„•‘¥ĞÁ±ÕÌ„É”µ‰…­”°Í¼€¨©É•½É…¹•½µ•ÑÉä±…¹‘•¥¸½¹”Í±¥”¨¨ƒŠPÑ¡”)Í…µ”½ÕÁ±¥¹œÑ¡”¹½Ñ”‰•±½Ü‘•ÍÉ¥‰•Ì¸±°Ñ¡É•”…É”‘½¹”¸((¨©Q¡”±¥ÍĞÉ•™¥±±Ì¥ÑÍ•±˜°İ¡¥ ¥ÌÑ¡”Á½¥¹Ğ½˜Ñ¡”…Ñ”¸¨¨5…­¥¹œÑ¡”¡¥µ¹•ä½Õ¹ĞÉ•…°)É•ÅÕ¥É•Á±…¥¹œ5¥±±•ÈÌÍ•½¹ÍÑ…¬°…¹Á±…¥¹œ¥Ğ•áÁ½Í•Ñ¡”¹•áĞÉ•Á…¥È½˜•á…Ñ±äÑ¡”)Í…µ”­¥¹è()ğÉ•½Éğ…ÑÑÉ¥‰ÕÑ”ğİ¡…ĞÑ¡”…É¡•ÑåÁ”‘½•Ìğ•™™•Ğğ)ğ´´µğ´´µğ´´µğ´´µğ)ğùùµ¥±±•É}¡½ÕÍ•ùøğùù™É…µ•}…‘‘¥Ñ¥½¹€€¡‘½Õµ•¹Ñ•°Õ¹‘¥µ•¹Í¥½¹•¥ùøğÁ¥­ÌÍ¥‘”°İ¥‘Ñ °‘•ÁÑ …¹ÍÑ½É•ä½Õ¹Ğ™É½´¥ÑÌ‘•™…Õ±ÑÌğ€¨©=9€ÈÀÈØ´Àà´ÄÀ¨¨ƒŠPÑ¡”É•½ÉÍÑ…Ñ•Ì…±°™¥Ù”°Ñ¡”Ñİ¼¥¹Ù•¹Ñ•½¹•Ì…É”0ÈÜ°É”µ‰…­•¥¸Ñ¡”Í±¥”ğ()Q¡…Ğİ…Ì0ÈĞÌ‘•™•Ğ½¹”‰Õ¥±‘¥¹œ½Ù•È°…¹¥Ğ…µ”İ¥Ñ „Í•½¹½¹”Õ¹‘•É¹•…Ñ ¥ĞÑ¡…Ğİ…Ì)¹½Ğ½¸…¹ä±¥ÍĞ¸€¨©ÍÑ½É¥•Ìè€È°‘½Õµ•¹Ñ•‘€İ…ÌÑ¡”™É…µ”É…¹”Ì…¹±½}‘İ•±±¥¹€É•…‘Ì¥Ğ…Ì)Ñ¡”±½œ½É”Ì¨¨°Í¼Ñ¡”‘½Õµ•¹Ñ•±…¥´İ…ÌÍÁ•¹Ğ½¸Ñ¡”…‰¥¸°Ñ¡”É…¹”Ñ½½¬„€Ğ¸Ü´‘•™…Õ±Ğ°)…¹Ñ¡”µ½‘•°ÍÑ½½„Ñİ¼µÍÑ½É•ä±½œ…‰¥¸‰•¡¥¹„Í¡½ÉÑ•È™É…µ”‰±½¬ƒŠPÑ¡”½µÁ½Í¥Ñ¥½¸)¥¹Ù•ÉÑ•¸Q¡”É•½É¹½ÜÍ•Á…É…Ñ•ÌÑ¡•´è™É…µ•}…‘‘¥Ñ¥½¹}ÍÑ½É¥•Ìè€É€‘½Õµ•¹Ñ•°ÍÑ½É¥•Ìè€Å€)¥¹™•ÉÉ•™½ÈÑ¡”…‰¥¸°™É…µ•}…‘‘¥Ñ¥½¹}¡•¥¡Ñ}´è€Ô¸É€…¹İ…±±}¡•¥¡Ñ}´è€È¸Ù€¸Qİ¼½˜Ñ¡”™½ÕÈ)ÅÕ•Õ•…ÑÑÉ¥‰ÕÑ•ÌÑÕÉ¹•½ÕĞÑ¼‰”…ÑÑ•ÍÑ•É…Ñ¡•ÈÑ¡…¸¥¹Ù•¹Ñ•ƒŠPÑ¡”Í¥‘”°‰•…ÕÍ”Ñ¡”Í½ÕÉ”)Í…åÌ€©™É½¹Ñ¥¹œÑ¡”É¥Ù•È¨°…¹Ñ¡”ÍÑ½É•ä½Õ¹ĞƒŠP…¹½¹±äÑ¡”İ¥‘Ñ …¹‘•ÁÑ …É”Õ•ÍÍ•Ì°Ñ…­•¸)½™˜Ñ¡”É•½ÉÌ½İ¸™½½ÑÁÉ¥¹Ğ±¥µˆ€ äƒ\€Ø´¤É…Ñ¡•ÈÑ¡…¸Á¥­•…™É•Í ¸0ÄÌµ½Ù•ÌÑ¼I•Í½±Ù•°)0ÈÜ¥Ì¹•Ü¸€¨©Q¡”É•Á…¥ÈÅÕ•Õ”¥Ì•µÁÑä…¹¹½Ñ¡¥¹œÉ•™¥±±•¥ĞèLÔ¥Ì…‘‘¥Ñ¥½¹Ì……¥¸¸¨¨()Q¡”±•ÍÍ½¸İ½ÉÑ …ÉÉå¥¹œÁ…ÍĞÑ¡¥ÌÑ…‰±”èÑ¡”½µ¥ÍÍ¥½¸…Ñ”™½Õ¹Ñ¡É•”µ¥ÍÍÁ•±±¥¹Ì…¹Ñ¡”)™½ÕÉÑ ™…Õ±Ğİ…Ì¹½Ğ½¹”¸ÍÑ½É¥•Í€İ…Ì„¹…µ”Ñ¡”…É¡•ÑåÁ”€©™½Õ¹¨…¹É•……Ì‰•¥¹œ…‰½ÕĞÑ¡”)½Ñ¡•È¡…±˜½˜„Ñİ¼µÁ…ÉĞ‰Õ¥±‘¥¹œƒŠPİ¡¥ ¥Ì¥¹Ù¥Í¥‰±”Ñ¼„ÍÁ•±±¥¹œ¡•¬…¹Ñ¼)Ñ•ÍÑ}½¹ÍÕµ•‘}…ÑÑÉ¥‰ÕÑ•Í}…ÑÕ…±±å}É•…¡}Ñ¡•}Á…É…µ•Ñ•ÉÍ€°Í¥¹”Ñ¡”Ù…±Õ”‘½•Ìµ½Ù”•½µ•ÑÉä°)©ÕÍĞÑ¡”İÉ½¹œ•½µ•ÑÉä¸¹ä…É¡•ÑåÁ”…ÑÑÉ¥‰ÕÑ”Ñ¡…Ğµ•…¹Ì‘¥™™•É•¹ĞÑ¡¥¹ÌÑ¼‘¥™™•É•¹Ğ)•±•µ•¹ÑÌ½˜„½µÁ½Í¥Ñ”‰Õ¥±‘¥¹œ¥ÌÑ¡”Í…µ”ÑÉ…Àìİ…±±}¡•¥¡Ñ}µ€İ…ÌÑ¡”Í•½¹½¹”¥¸Ñ¡¥Ì)É•½É¸((¨©Q¡”]½±˜A½¥¹ĞÁ…¥È±…¹‘•Ñ½•Ñ¡•È°İ¡¥ ¥ÌÑ¡”Í¡…Á”¨¨€ ÈÀÈØ´Àà´ÄÀ¤¸	½Ñ É•¹…µ•Ì°Ñ¡”™½ÕÈ)…ÑÑÉ¥‰ÕÑ•ÌÑ¡”™É…µ”‰…ä¹••‘•°Ñ¡”É”µ‰…­”°Ñ¡”ÁÕ‰±¥Í …¹Ñ¡”±¥‰•ÉÑ¥•Ìµ½Ù•¥¸½¹”AH¸Qİ¼)Ñ¡¥¹Ì…É”İ½ÉÑ …ÉÉå¥¹œ™½Éİ…É¸¥ÉÍĞ°„É•¹…µ”¥Ì¹•Ù•È½¹±ä„É•¹…µ”è™É…µ•}…‘‘¥Ñ¥½¸èÑÉÕ•€)…±½¹”İ½Õ±¡…Ù”±•ĞÑ¡”…É¡•ÑåÁ”¡½½Í”Ñ¡”‰…äÌÍ¥‘”°İ¥‘Ñ °‘•ÁÑ …¹ÍÑ½É•ä½Õ¹Ğ™É½´¥ÑÌ)‘•™…Õ±ÑÌ°Í¼„‘½Õµ•¹Ñ•™•…ÑÕÉ”İ½Õ±¡…Ù”…ÉÉ¥Ù•…Ğ…¸¥¹Ù•¹Ñ•Í¥é”İ¥Ñ ¹½Ñ¡¥¹œ…‘µ¥ÑÑ¥¹œ)¥ĞƒŠPÑ¡”É•½É¹½ÜÍÑ…Ñ•Ì…±°™½ÕÈ…¹0ÈĞ…‘µ¥ÑÌÑ¡”Ñ¡É•”Ñ¡…Ğ…É”½¹©•ÑÕÉ…°¸M•½¹°Ñ¡”)ÍÑ…±•¹•ÍÌ…Ñ”‘¥•á…Ñ±äİ¡…Ğ¥Ğİ…ÌİÉ¥ÑÑ•¸™½ÈèÑ¡”É•½É•‘¥ĞÑÕÉ¹•Ñ¡”Ñ…Ù•É¸Ì1MQ1)½¸Ñ¡”ÍÁ½Ğ…¹Ñ¡”½µµ¥Ğ½Õ±¹½Ğ¼É••¸Õ¹Ñ¥°Ñ¡”‰…­”±…¹‘•İ¥Ñ ¥Ğ¸((¨©¹Ñ¡”½Õ¹Ğ½˜„Ñ¡¥¹œ¥Ì¹½ĞÑ¡”Ñ¡¥¹œ¨¨€ ÈÀÈØ´Àà´ÄÀ¤¸¡¥µ¹•åÍ€İ…ÌÍÑ…Ñ•‰ä•Ù•ÉäÉ•½É)…¹É•…‰ä¹•¥Ñ¡•È…É¡•ÑåÁ”è™É…µ•}Ñ…Ù•É¹€‰Õ¥±ĞÑİ¼ÍÑ…­Ì…¹±½}‘İ•±±¥¹€‰Õ¥±Ğ½¹”°)İ¡…Ñ•Ù•ÈÑ¡”¹Õµ‰•ÈÍ…¥¸	½Ñ Ñ…­”Ñ¡”½Õ¹Ğ¹½Ü°…¹Ñ¡”™É…µ”Á…¥È­••ÁÌ¥ÑÌ•á…ĞÁ½Í¥Ñ¥½¹ÌÍ¼)Ñ¡…ĞÁ…É…µ•Ñ•É¥Í¥¹œ„¹Õµ‰•È‘¥¹½Ğµ½Ù”„‰Õ¥±‘¥¹œİ¡½Í”½Õ¹Ğİ…Ì…±É•…‘äÉ¥¡Ğ¸Q¡”)±½}‘İ•±±¥¹€¡…±˜İ…ÌÑ¡”™É…µ•}•áÑ•¹Í¥½¹€½Í¥¹…•€™…¥±ÕÉ”„Ñ¡¥ÉÑ¥µ”ƒŠPÑ¡”Á…É…µ•Ñ•Èİ…Ì)¡¥µ¹•å€…¹¹¼É•½É¡…Ì•Ù•È½¹Ñ…¥¹•Ñ¡…Ğİ½ÉƒŠPÍ¼Ñ¡”±…ÍÌ¡…Ì„¡•¬¹½ÜÉ…Ñ¡•ÈÑ¡…¸)…¹½Ñ¡•È‘¥Í½Ù•É•ÈèÑ•ÍÑ}½¹ÍÕµ•‘}…ÑÑÉ¥‰ÕÑ•Í}…ÑÕ…±±å}É•…¡}Ñ¡•}Á…É…µ•Ñ•ÉÍ€Á•ÉÑÕÉ‰Ì•Ù•ÉäÍÑ…Ñ•)Ù…±Õ”…¸…É¡•ÑåÁ”‘•±…É•Ì¥Ğ½¹ÍÕµ•Ì…¹É•ÅÕ¥É•ÌÑ¡”É•Í½±Ù•Á…É…µ•Ñ•ÉÌÑ¼¡…¹”¸]¡…ĞÑ¡”)½Õ¹ĞÍÑ¥±°‘½•Ì¹½Ğ…ÉÉä¥Ìİ¡•É”„ÍÑ…¬ÍÑ½½°¡½Ü‰¥œ¥Ğİ…Ì½Èİ¡…Ğ¥Ğİ…Ìµ…‘”½˜ì¹½Ñ¡¥¹œ)¥¸Ñ¡”‘…Ñ…Í•ĞÉ•½É‘ÌÑ¡…Ğ™½È…¹ä‰Õ¥±‘¥¹œ°…¹0ÈØ¥Ìİ¡•É”¥Ğ¥Ì…‘µ¥ÑÑ•¸((¨©e½Ô…¹¹½Ğ±…¹¡…±˜½˜½¹”…¹äµ½É”¨¨€ ÈÀÈØ´Àà´ÄÀ¤¸¡•¬¹Í¡€É•½µÁÕÑ•Ì•… ½µµ¥ÑÑ•1Ì)¥¹ÁÕÑÌ…¹™…¥±Ìİ¡•¸Ñ¡”É•½É…¹Ñ¡”µ•Í ‘¥Í…É•”¸Q¡”İ½É­¥¹œÍ¡…Á”èÁÉ•Á…É”Ñ¡”É•½É½¸)„‰É…¹ °±•ĞÑ¡”‰…­”İ½É­™±½ÜÉÕ¸……¥¹ÍĞÑ¡…Ğ‰É…¹ €¡¥ĞÑÉ¥•ÉÌ½¸…¹äÁÕÍ Õ¹‘•È)¡¥…¼¼Ñ½‘…Ñ„¼¨©€½È•¹•É…Ñ½ÉÌ¼¨©€¤°Ñ…­”¥ÑÌ‰…­•…ÍÍ•ÑÌ½¹Ñ¼Ñ¡”Í…µ”‰É…¹ °…¹µ•É”)½¹”AH…ÉÉå¥¹œ‰½Ñ ¸M•”•¹•É…Ñ½ÉÌ½µ•Í¡}¥¹ÁÕÑÌ¹Áå€™½Èİ¡…Ğ½Õ¹ÑÌ…Ì…¸¥¹ÁÕĞ…¹İ¡…Ğ)‘•±¥‰•É…Ñ•±ä‘½•Ì¹½Ğ¸((¨©Q¡”™¥ÉÍĞ‰É¥‘”±…¹‘•€ÈÀÈØ´Àà´ÄÀ°…¹¥Ğ¥ÌÑ¡”™¥ÉÍĞÉ•½Éİ¡½Í”Í¥é”¥Ì•Ù¥‘•¹”¸¨¨Q¡”)9½ÉÑ 	É…¹ É½ÍÍ¥¹œ…Ğ-¥¹é¥”MÑÉ••ĞƒŠP¡¥…¼Ì™¥ÉÍĞ‰É¥‘”°€ÄàÌÈ´ÄàÌäƒŠP¥Ì„É•½É°„‰…­”)…¹„ÁÕ‰±¥Í¡•µ•Í ½¸Ñ¡”‰É¥‘•}Ñ¥µ‰•É€…É¡•ÑåÁ”°İ¡¥ ¡…‰••¸İÉ¥ÑÑ•¸…¹¹•Ù•ÈÕÍ•¸)Q¡É•”Ñ¡¥¹Ìİ½ÉÑ …ÉÉå¥¹œ¥¹Ñ¼Ñ¡”É•ÍĞ½˜LÔè((´€¨©É½ÍÍ¥¹œ…¸‰”µ•…ÍÕÉ•İ¡•É”„‰Õ¥±‘¥¹œ…¹¹½Ğ¸¨¨%ÑÌ€ÜÄ¸àÌ´ÍÁ…¸¥ÌÑ¡”‘¥ÍÑ…¹”(€‰•Ñİ••¸Ñ¡”Ñİ¼ÑÉ…•€ÄàÌĞİ…Ñ•É±¥¹•Ì…±½¹œÑ¡”-¥¹é¥”…±¥¹µ•¹Ğ°É•…½™˜É¥Ù•È¹•½©Í½¹€°(€…¹¥ÑÌ€Ì¸ÀĞà´İ¥‘Ñ ¥Ì±•…Ù•ÈÌ€‰Ñ•¸™••Ğİ¥‘”ˆƒŠPÍ¼Ñ¡”™½½ÑÁÉ¥¹Ğ¥Ì‘•É¥Ù•É…Ñ¡•ÈÑ¡…¸„(€Á±…•¡½±‘•È¸¹åÑ¡¥¹œÑ¡…Ğµ••ÑÌÑ¡”ÑÉ…•İ…Ñ•È€¡Ñ¡”Á¥•ÉÌ°Ñ¡”İ¡…ÉÙ•Ì°Ñ¡”É…™Ğ‰É¥‘”¤…¸(€‰”‘¥µ•¹Í¥½¹•Ñ¡”Í…µ”İ…ä¸¹åÑ¡¥¹œÑ¡…Ğ‘½•Ì¹½ĞÍÑ¥±°•ÑÌ„Á±…•¡½±‘•È¸(´€¨©Q¡”¥¹Ù•¹Ñ¥½¸µ½Ù•™É½´Ñ¡”½ÕÑ±¥¹”Ñ¼Ñ¡”¥¹Ñ•É¥½È¸¨¨‰Õ¥±‘¥¹œÌÁ±…•¡½±‘•È¥Ì¥ÑÌ(€™½½ÑÁÉ¥¹ĞìÑ¡¥Ì‰É¥‘”Ì¥ÌÑ¡”™¥™Ñ••¸É¥‰ÌÑ¡”…É¡•ÑåÁ”ÁÕÑÌÕ¹‘•È„ÍÁ…¸¹½‰½‘ä‘•ÍÉ¥‰•(€Ñ¡”µ¥‘‘±”½˜€¡0Èä¤¸M…µ”±…ÍÌ½˜™…Õ±Ğ°‘¥™™•É•¹ĞÁ±…”Ñ¼±½½¬™½È¥Ğ¸(´€¨©Q¡”½¹ÑÉ…ĞÌİ…Ñ•È…¹¡½È¥Ì¥µÁ±•µ•¹Ñ•¹½Ü¨¨ƒŠPYIQ%1}9!=I€½¸Ñ¡”…É¡•ÑåÁ”°(€Á±…•µ•¹Ğ¹Ù•ÉÑ¥…±}…¹¡½É€¥¸Ñ¡”Í¥‘•…È°„±¥Ñ•É…°ä€ô€Á€¥¸Ñ¡”É•¹‘•É•È°…¹„Íµ½­”(€…ÍÍ•ÉÑ¥½¸İÉ¥ÑÑ•¸…ÌÑ¡”‘¥™™•É•¹”‰•Ñİ••¸Ñ¡”Ñİ¼…¹¡½ÉÌ¸Q¡”¹•áĞÍÑÉÕÑÕÉ”½Ù•Èİ…Ñ•È(€¹••‘Ì¹¼É•¹‘•É•Èİ½É¬¸€¨©]¡…Ğ¥ÌÍÑ¥±°µ¥ÍÍ¥¹œ¥Ìİ…±­¥¹œ½¸¥Ğ¨¨èÑ¡”İ…±­•È™½±±½İÌÑ¡”(€Ñ•ÉÉ…¥¸°Í¼Ñ¡”‘•¬¥ÌÍ•¹•Éä¸Q¡…Ğ¥Ì¥ÑÌ½İ¸Õ¹¥Ğ…¹¥Ğ¥ÌÉ•½É‘•¥¸MQQUL°¹½Ğ™…­•¸((¨©Q¡”™¥ÉÍĞ‰Õ¥±‘¥¹œİ¡½Í”™½½ÑÁÉ¥¹Ğ¥Ì•Ù¥‘•¹”±…¹‘•€ÈÀÈØ´Àà´ÄÀ¨¨°…¹¥Ğ¥Ì…¸%Q%=8)É…Ñ¡•ÈÑ¡…¸„É•Á…¥ÈƒŠPÑ¡”™¥ÉÍĞÍ¥¹”Ñ¡”ÅÕ•Õ”•µÁÑ¥•¸¡½…¹}ÍÑ½É•€°Ñ¡”±½œÍÑ½É”…ĞÑ¡”)İ•ÍĞ•¹½˜Ñ¡”1…­”MÑÉ••Ğ‰±½¬İ¡•É”Ñ¡”U¹¥Ñ•MÑ…Ñ•Ì½Á•¹•„Á½ÍĞ½™™¥”…Ğ¡¥…¼½¸(ÌÄ5…É €ÄàÌÄ°…ÉÉ¥•Ì„‘½Õµ•¹Ñ•‘€™½½ÑÁÉ¥¹Ğè¹‘É•…ÌÍÑ…Ñ•Ì¥ÑÌÍ¥é”Ñİ¥”°Ñİ•¹Ñä‰ä)™½ÉÑäµ™¥Ù”™••Ğ°‰½Ñ Ñ¥µ•Ì…Ì…¸…Í¥‘”…‰½ÕĞ¡½Ü±¥ÑÑ±”É½½´Ñ¡”Ñ½İ¸Ìµ…¥°¹••‘•¸Q¡É•”)Ñ¡¥¹Ìİ½ÉÑ …ÉÉå¥¹œ¥¹Ñ¼Ñ¡”É•ÍĞ½˜LÔè((´€¨©‰Õ¥±‘¥¹œ…¸‰”µ•…ÍÕÉ•…™Ñ•È…±°°İ¡•¸Ñ¡”Í½ÕÉ”¥Ì‘•ÍÉ¥‰¥¹œÍ½µ•Ñ¡¥¹œ•±Í”¸¨¨Q¡”(€‰É¥‘”Ì¹Õµ‰•ÉÌ…µ”™É½´„İ¥Ñ¹•ÍÌ‘•ÍÉ¥‰¥¹œÑ¡”‰É¥‘”¸Q¡¥Ì½¹”Ì…µ”™É½´„İÉ¥Ñ•È(€µ…­¥¹œ„Á½¥¹Ğ…‰½ÕĞÑ¡”€©Á½ÍĞ½™™¥”Ì¨É…µÁ•ÅÕ…ÉÑ•ÉÌ¸¥µ•¹Í¥½¹Ì¥¸Ñ¡¥Ì±¥Ñ•É…ÑÕÉ”¡¥‘”(€¥¹Í¥‘”…ÉÕµ•¹ÑÌ…‰½ÕĞÍ½µ•Ñ¡¥¹œ½Ñ¡•ÈÑ¡…¸Ñ¡”‰Õ¥±‘¥¹œ°Í¼Í•…É Ñ¡”ÁÉ½Í”…É½Õ¹…¸(€¥¹ÍÑ¥ÑÕÑ¥½¸É…Ñ¡•ÈÑ¡…¸Ñ¡”•¹ÑÉä™½È„ÍÑÉÕÑÕÉ”¸(´€¨©I•…‘¥¹œ„Á…”½ÉÉ•Ñ•Ñ¡”‘½ÍÍ¥•ÈÌ¡É½¹½±½ä‰äÑİ•¹Ñäµ½¹Ñ¡Ì¸¨¨‘½Ì½É•Í•…É ½€(€ƒ
œ€Ğ‘…Ñ•Ñ¡”Á½ÍĞ½™™¥”Ìµ½Ù”Ñ¼É…¹­±¥¸…¹M½ÕÑ ]…Ñ•È™É½´Ñ¡”‘…ä!½…¸‰•…µ”(€Á½ÍÑµ…ÍÑ•È€ È9½Ø€ÄàÌÈ¤ì¹‘É•…ÌÍ…åÌÑİ¥”¥Ğµ½Ù•…‰½ÕĞ)Õ±ä€ÄàÌĞ¸Q¡”‘½ÍÍ¥•ÈÌÍÕµµ…Éä(€Ñ…‰±•Ì…É”™¥¹‘¥¹œ…¥‘Ì°…¹„Ñ…‰±”É½Ü¥Ì¹½ĞÑ¡”Á…”¸M•”‘½Ì½IMI ½¡½…¹}ÍÑ½É”¹µ‘€(€ƒ
œ€Ì¸(´€¨©Q¡”™¥ÉÍĞÉ•½Éİ¥Ñ ¹½Ñ¡¥¹œ½¹©•ÑÕÉ…°¥¸¥Ğ¸¨¨%ÑÌ…ÁÌ…É”…ÁÌ¥¸Ñ¡”Í½ÕÉ•Ìœ(€ÁÉ•¥Í¥½¸É…Ñ¡•ÈÑ¡…¸™¥±±•¡½±•Ì°Í¼¥Ğ¹••‘Ì¹¼±¥‰•ÉÑäƒŠPİ¡¥ ™¥¹…±±ä•á•É¥Í•ÌÑ¡”(€ÁÉ½Ù•¹…¹”Á½ÁÕÀÌ•µÁÑä€‰]¡…Ğİ”µ…‘”ÕÀ¡•É”ˆÍÑ…Ñ”Ñ¡…ĞMQQULƒ
œ€ÄÄÉ•½É‘•…ÌÕ¹•á•É¥Í•(€‰äÉ•…°‘…Ñ„¸%ÑÌİ•…¬Á½¥¹Ğ¥Ì¥¹ÍÑ•…¥ÑÌ€¨©ÍÕÉÙ¥Ù…°¨¨è…ÑÑ•ÍÑ•Ñ¼…‰½ÕĞ)Õ±ä€ÄàÌĞ…¹(€Á±…•¥¸„Í•¹”•±•Ù•¸µ½¹Ñ¡Ì±…Ñ•È½¸„½¹Ñ¥¹Õ¥Ñä…ÉÕµ•¹Ğ°ÍÑ…Ñ•…ÌÍÕ ½¸Ñ¡”É•½É¸()A•Èµ±ÕÍÑ•ÈÁ…É•±Ì°•… ½¹”™¥±”Á•ÈÍÑÉÕÑÕÉ”Í¼Á…É…±±•°…•¹ÑÌ¹•Ù•È½±±¥‘”è()ğÁ…É•°ğ½¹Ñ•¹ÑÌğ)ğ´´µğ´´µğ)ğ]½±˜A½¥¹Ğİ•ÍĞ‰…¹¬ğ]½±˜Q…Ù•É¸€¡Á…¥¹Ñ•İ½±˜Í¥¸¤°É••¸QÉ•”°]•ÍÑ•É¸!½Ñ•°°)…µ•Ì-¥¹é¥”¡½ÕÍ”°H¸¸-¥¹é¥”ÍÑ½É”ğ)ğ9½ÉÑ ‰…¹¬ğ5¥±±•È!½ÕÍ”°5¥±±•ÈÑ…¹¹•Éä°½‰İ•ˆ…ÍÑ±”°]…±­•ÈÌµ••Ñ¥¹œ¡½ÕÍ”°MÑ•…µ‰½…Ğ!½Ñ•°°1…­”!½ÕÍ”€¡Õ¹‘•È½¹ÍÑÉÕÑ¥½¸¤ğ)ğM½ÕÑ ]…Ñ•È‰±½­ÌŠMğÑ¡”‰±½¬µ‰äµ‰±½¬Í­•Ñ ¥¸‘½Ì½É•Í•…É ¼ÀĞµÍÑÉÕÑÕÉ•ÌµÍ½ÕÑ ¹µ‘€¥ÌÑ¡”İ½É¬½É‘•È¸ùù!½…¸ÌÍÑ½É”€¼Ñ¡”™¥ÉÍĞÁ½ÍĞ½™™¥”°1…­”…ĞM½ÕÑ ]…Ñ•Éùø€¨©=9€ÈÀÈØ´Àà´ÄÀ¨¨¸9•áĞ½¸Ñ¡¥Ì‰±½¬èA¡¥±¼…ÉÁ•¹Ñ•ÈÌ±½œ‘ÉÕœÍÑ½É”°€‰¥µµ•‘¥…Ñ•±ä…‘©…•¹ĞÑ¼Ñ¡”M…Õ…¹…Í ÌÁÕ‰±¥Œ‰…Èˆ°İ¡¥ ¡…Ì¹¼‘¥µ•¹Í¥½¹Ì…Ğ…±°ì…¹Ñ¡”€¨©É…¹­±¥¸MÑÉ••ĞÁ½ÍĞ½™™¥”¨¨°Ñ¡”‰Õ¥±‘¥¹œ…ÑÕ…±±ä¡½±‘¥¹œÑ¡”µ…¥°½¸Ñ¡”Í•¹”‘…Ñ”°½˜İ¡¥ ¹½Ñ¡¥¹œ‰ÕĞ„ÍÑÉ••Ğ©Õ¹Ñ¥½¸¥Ì…ÑÑ•ÍÑ•ƒŠPÍ•”‘½Ì½IMI ½¡½…¹}ÍÑ½É”¹µ‘€ƒ
œ€Ğ‰•™½É”‰Õ¥±‘¥¹œ¥Ğğ)ğ1…­”MÑÉ••ĞğQÉ•µ½¹Ğ!½ÕÍ”$°5…¹Í¥½¸!½ÕÍ”°á¡…¹”½™™•”!½ÕÍ”°MĞ¸5…ÉäÌ°¥ÉÍĞAÉ•Í‰åÑ•É¥…¸°Q¡½µ…Ì¡ÕÉ ÍÑ½É”ğ)ğ¥Ù¥ŒÍÅÕ…É”ğ•ÍÑÉ…äÁ•¸°±½œ©…¥°°½ÕÉÑ¡½ÕÍ”€¡Õ¹‘•È½¹ÍÑÉÕÑ¥½¸°µ½¹Ñ Õ¹™¥á•¤ğ)ğ½ÉĞ•…É‰½É¸ğÁ…±¥Í…‘”°‰±½­¡½ÕÍ”°‰…ÍÑ¥½¸°µ……é¥¹”°ÅÕ…ÉÑ•ÉÌ°‰…ÉÉ…­Ì°ÍÕÑ±•È°¡½ÍÁ¥Ñ…°°Á…É…‘”°…É‘•¹Ìğ)ğ!…É‰½Èİ½É­Ìğ¹½ÉÑ Á¥•È°Í½ÕÑ Á¥•È°Ñ¡”ÕĞ°Ñ¡”±¥¡Ñ¡½ÕÍ”°İ¡…ÉÙ•Ìğ)ğÉ½ÍÍ¥¹Ìğùù9½ÉÑ 	É…¹ ‰É¥‘•ùø€¨©=9€ÈÀÈØ´Àà´ÄÀ¨¨ƒ
ÜM½ÕÑ 	É…¹ É…™Ğ‰É¥‘”€¡™±½…Ñ¥¹œƒŠP¹••‘Ì¥ÑÌ½İ¸…É¡•ÑåÁ”°Í•”‰É¥‘•}Ñ¥µ‰•É}Á…É…µÍ€¤ƒ
Ü•…É‰½É¸MÑÉ••Ğ‘É…İ‰É¥‘”€ ÈÀÀ™Ğİ¥Ñ „€ØÀµ™Ğ‘É…Ü°„‘¥™™•É•¹Ğ…¹¥µ…°…¹½ÕÑÍ¥‘”Ñ¡”ÕÉÉ•¹ĞÑ•ÉÉ…¥¸‰½à¤ğ((ŒŒLØƒŠP±½É„…¹™…Õ¹„((¨©¹Ñ¡”É½Õ¹ÌÍÕÉ™…”°İ¡¥ ¥Ì¹½Ü„‘•±…É•½µ¥ÍÍ¥½¸É…Ñ¡•ÈÑ¡…¸…¸Õ¹ÍÑ…Ñ•½¹”¨¨( ÈÀÈØ´Àà´ÄÀ°0ÌÔ¤èÑ¡”Ñ•ÉÉ…¥¸ÍÁ•ŒÉ…‘•Ì™¥Ù”ÍÕÉ™…”µ…Ñ•É¥…±ÌƒŠPÑ¡”‘¥Ù¥Í¥½¹Ìœ±½…´½Ù•È)ÅÕ¥­Í…¹½Ù•È‰±Õ”±…ä°Ñ¡”µ…ÉÍ ÍÑÉ¥ÀÌÁ•…Ğ…¹Í•‘”°Ñ¡”¡…¹¹•°ÌÍ¥±ĞƒŠP…¹Ñ¡”µ•Í ¥Ì)½¹”•…ÉÑ ½±½ÕÈ¸Á•Èµé½¹”ÍÕÉ™…”ÑÉ•…Ñµ•¹Ğ‘É¥Ù•¸‰äÑ¡½Í”•¹ÑÉ¥•ÌÉ•Ñ¥É•Ì0ÌÔìÑ¡”Á…±•ÑÑ”)¡…ÌÑ¼‰”…ÉÕ•™É½´Ñ¡”Í½ÕÉ•ÌÉ…Ñ¡•ÈÑ¡…¸Á¥­•°İ¡¥ ¥ÌÑ¡”Í…µ”ÑÉ…ÀÑ¡”ÍÑÉ••ĞÍÕÉ™…”)¥Ì€£
œLä¤¸()A•Èµé½¹”Á…É•±Ì™É½´Ñ¡”‘½ÍÍ¥•ÉÌè€ÄÀ™±½É„é½¹•Ì°€Ü™…Õ¹„é½¹•Ì¸!½¹½ÈÑ¡”)Õ±äÁ¡•¹½±½ä)ÉÕ±•ÌƒŠP‰¥œ‰±Õ•ÍÑ•´¥ÌÙ••Ñ…Ñ¥Ù”¥¸)Õ±ä°½É‘É…ÍÌ¥ÌÑ¡”Ñ…±°™±½İ•É¥¹œ•±•µ•¹Ğ°É…µÁÌ…É”)±•…™±•ÍÌÍ…Á•Ì¸9•…Ñ¥Ù”™¥¹‘¥¹Ì€¡¹¼É¥¹œµ‰¥±±•Õ±±Ì°¹¼‰•…Ù•È°¹¼Á•É¥½‘¥…°¥…‘…Ì¤¼)¥¹Ñ¼Ñ¡”‘…Ñ„…Ì…‰Í•¹Ñ€•¹ÑÉ¥•Ìİ¥Ñ ¥Ñ…Ñ¥½¹Ì°Í¼¹½‰½‘äÉ”µ…‘‘ÌÑ¡•´±…Ñ•È¸((ŒŒŒLÙ„ƒŠPÑ¡”•å”µ¡•¥¡ĞÍİ…Éƒ
Ü€¨©I=U9€Ä%8€ÈÀÈØ´Àà´ÄÀ¨¨()É•¹‘•É•ÉÌ½İ•ˆ½©Ì½™±½É„¹©Í€‘É…İÌÑ¡”É…µ¥¹½¥µ…ÑÉ¥à°Ñ¡”™½Éˆ±…å•È°Ñ¡”•µ•É•¹ÑÌ…¹Ñ¡”)±½ÜÍ¡ÉÕ‰Ì™É½´‘…Ñ„½™±½É„½€°µ½Õ¹Ñ•¥¸µ…¥¸¹©Í€‰•Í¥‘”ÑÉ••Ì¹©Í€¸	±…‘”•½µ•ÑÉäÉÕ¹Ìİ¥Ñ¡¥¸)…‰½ÕĞ€Ü¸Ø´…¹…µ•É„µ™…¥¹œ±ÕµÀ…É‘ÌÑ¼€ÈÜ´ì‰•å½¹Ñ¡•´Ñ¡”…ÑÕ…°Ñ•ÉÉ…¥¸ÌÁÉ½•‘ÕÉ…°)ÁÉ…¥É¥”Ñ•áÑÕÉ”…ÉÉ¥•ÌÕ¹É•Í½±Ù•½±½ÕÈ¸A±…•µ•¹Ğ¥Ì„‘•Ñ•Éµ¥¹¥ÍÑ¥Œİ½É±±…ÑÑ¥”)É”µ•¹ÑÉ•½¸Ñ¡”İ…±­•È…¹Õ±±•Ñ¼„€ØË
À½¹”°Í¼¹½Ñ¡¥¹œÍİ¥µÌÕ¹‘•É™½½Ğ…¹¹½Ñ¡¥¹œ¥Ì)Á…¥™½È‰•¡¥¹å½ÕÈ¡•…¸!•¥¡ÑÌ°É••¹Ì°½Ù•È°Á¡•¹½±½ä…¹Á•ÈµÁ±…¹Ğ½¹™¥‘•¹”…±°½µ”)™É½´Ñ¡”É•½É‘ÌìÑ¡”ÑÕ™Ğ‘•¹Í¥Ñä…¹™…ÈµÑ•áÑÕÉ”½µÁÉ•ÍÍ¥½¸…É”±¥‰•ÉÑ¥•Ì€¡0ÌÈ°0àÀ¤¸((¨©½ÉÉ•Ñ•…™Ñ•ÈÑ¡”€ÈÀÈØ´Àà´ÄÄÉ•…°µ‘•Ù¥”É•Ù¥•Üè¨¨Ñ¡”™½Éµ•È0ÌÌ™…Èµ™¥•±…¹½Áäİ…Ì„)Í½±¥ÍÕÉ™…”…ĞÁ±…¹ĞµÑ½À¡•¥¡Ğ¸%Ğ±½½­•±¥­”„Í•½¹Ñ•ÉÉ…¥¸±…å•È°¡¥™½Õ¹‘…Ñ¥½¹Ì…¹)É½½ÑÌ°…¹½Õ±‰”İ…±­•Õ¹‘•É¹•…Ñ ¸%Ğİ…ÌÉ•µ½Ù•É…Ñ¡•ÈÑ¡…¸µ…­¥¹œÑ¡”İ…±­•È…¹•Ù•Éä)‰Õ¥±‘¥¹œÍÑ…¹½¸™…±Í”Á±…¹ĞµÑ½ÀÑ½Á½É…Á¡ä¸Q•ÉÉ…¥¸¥Ì¹½ÜÑ¡”Í½±”Á¡åÍ¥…°…¹Ù¥Í¥‰±”)ÍÕÉ™…”ì…±°‘•Ñ…¥±•™±½É„…¹ÍÑÉÕÑÕÉ•ÌÍ¡…É”¥ÑÌÍ…µÁ±•È¸0àÀÉ•½É‘ÌÑ¡”É•Á±…•µ•¹Ğ¸((¨©)Õ‘•……¥¹ÍĞ]=I,½‰…É€¨¨ƒŠPÑİ¼Ù•É¥™¥•Á¡½Ñ½É…Á¡Ì½˜ÍÕÉÙ¥Ù¥¹œ%±±¥¹½¥ÌÑ…±±É…ÍÌ¥¸)µ¥µ)Õ±ä€¡„¡¥…¼µÉ•¥½¸É•µ¹…¹Ğ°€Èä)Õ±ä€ÈÀÈÄì„ÕA…”É•ÍÑ½É…Ñ¥½¸°€ÈĞ)Õ±ä€ÈÀÄà¤…¹…¸)=Ñ½‰•È¹•…Ñ¥Ù”½¹ÑÉ½°¸]¡•É”É½Õ¹€ÄÍÑ…¹‘Ì°µ•…ÍÕÉ•½¸Ñ¡”ÁÉ¥µ…ÉäÍ¡½ĞÉ…Ñ¡•ÈÑ¡…¸)…ÍÍ•ÉÑ•è()ğÑ•±°ğÉ•™•É•¹”ğÉ½Õ¹€Äğ)ğ´´µğ´´µğ´´µğ)ğÑ¡”É½Õ¹¥Ì¡¥‘‘•¸…Ğ•å”¡•¥¡Ğğ¥¹Ù¥Í¥‰±”ğ¡¥‘‘•¸Á…ÍĞøÌ´°Á…Ñ¡ä¥¸Ñ¡”¹•…É•ÍĞ€È´ğ)ğÍ•Ù•É…°¡•¥¡ÑÌ°Í•Ù•É…°É••¹Ìğ€Ğ´Ô±…å•ÉÌğ€ÔÍÁ•¥•Ì¡•¥¡ÑÌ°Ñİ¼É••¹Ì•… °Á•ÈÉ•½Éğ)ğ)Õ±ä¡Õ”€¡É••¸°¹½ĞÑ…İ¹ä¤ğH½€À¸ÜØ´À¸äÌğ€¨¨À¸ÜÌ´À¸àÀ¨¨ğ)ğ±½…°½¹ÑÉ…ÍĞ€¡ÀäÀƒŠ"HÀÄÀ±Õµ¥¹…¹”¤ğ€¨¨ÄĞÄ´ÈÄÈ¨¨ğ€¨¨ÄÀÄ¹•…È°€àÌµ¥°€ĞØ™…È¨¨ğ)ğ¹¼™±½İ•É¥¹œ‰±Õ•ÍÑ•´½%¹‘¥…¸É…ÍÌ½Íİ¥Ñ¡É…ÍÌğ¹½¹”ğ¹½¹”°ÍÑÉÕÑÕÉ…±±äğ((ŒŒŒLÙ„¹•áĞƒŠPÑ¡”½Á•¸İ½É¬°¥¸Ñ¡”½É‘•È¥Ğ¥Ìİ½ÉÑ ‘½¥¹œ((¨©I•½É‘•É•€ÈÀÈØ´Àà´ÄÀ…™Ñ•È„Ñ¡É•”µÉ¥Ñ¥Œ‰±¥¹É½Õ¹½¸½¹”¥‘•¹Ñ¥…°Í¡½ĞÍ•Ğ¸¨¨Ù•Éä¥Ñ•´)‰•±½Ü…ÉÉ¥•Ì„µ•…ÍÕÉ•Ñ…É•Ğ…¹Ñ¡”‘•™¥¹¥Ñ¥½¸¥Ğ¥Ìµ•…ÍÕÉ•İ¥Ñ °‰•…ÕÍ”Ñİ¼É½Õ¹‘Ì½˜)Ñ¡¥Ìİ½É¬İ•É”ÍÁ•¹Ğ¡…Í¥¹œ¹Õµ‰•ÉÌÑ¡…Ğ•¥Ñ¡•È‘¥¹½ĞÉ•ÁÉ½‘Õ”½È‘¥¹½Ğ•á¥ÍĞ¥¸Ñ¡”)É•™•É•¹”¸M•”MQQUL¹µƒ
œ€‰-¹½İ¸İ•…­¹•ÍÍ•Ìˆ€ÀÀ™½ÈÑ¡”™Õ±°µ•…ÍÕÉ•µ•¹ÑÌ¸Q¡”½±±¥ÍĞÌ)¥Ñ•µÌ€ÇŠLÌİ•É”¹½ĞİÉ½¹œìÑ¡•äİ•É”…¥µ•…ĞÑ¡”¹•…È™¥•±°…¹Ñ¡”‰±¥¹Ñ•ÍĞ¥Ì‰•¥¹œ±½ÍĞ)¥¸Ñ¡”€¨©µ¥¨¨™¥•±¸((Ä¸€¨©I•ÍÑ½É”‘¥ÍÑ…¹ĞÙ••Ñ…Ñ¥½¸İ¥Ñ¡½ÕĞÉ•ÍÑ½É¥¹œ„Í•½¹ÍÕÉ™…”¸¨¨Q¡”É•µ½Ù•0ÌÌÍ¡••Ğ(€€…¹¹½ĞÉ•ÑÕÉ¸è…¹ä¥µÁ½ÍÑ½È½ÈÍÁ…ÉÍ”™…È•½µ•ÑÉäµÕÍĞ‰”É½½Ñ•½¸Ñ¡”¡•¥¡Ñ™¥•±°É•µ…¥¸(€€Ù¥Í¥‰±äÁ½É½ÕÌ°…¹Á…ÍÌÑ¡”Í…µ”É½½Ğ½‰Õ¥±‘¥¹œ½İ…±­•ÈÍÕÉ™…”¡•­Ì…ÌÑ¡”‘•Ñ…¥±•™¥•±¸(€€Q¡”Ñ•ÉÉ…¥¸Ñ•áÑÕÉ”¥ÌÑ¡”¡½¹•ÍĞÕÉÉ•¹Ğ™…±±‰…¬‰•å½¹€ÈÜ´¸(È¸€¨©¥Ù”Ñ¡”™…ÈÑ•ÉÉ…¥¸Ñ•áÑÕÉ”É…¥¸…Ğ™É…µ•¹ĞÍ…±”¸¨¨-••À¥Ğ½¸Ñ¡”Á¡åÍ¥…°Ñ•ÉÉ…¥¸°(€€İ¥Ñ •¹½Õ ¥ÉÉ•Õ±…È½¹ÑÉ…ÍĞÑ¼ÍÕ•ÍĞÕ¹É•Í½±Ù•Ù••Ñ…Ñ¥½¸İ¥Ñ¡½ÕĞ…ÍÍ•ÉÑ¥¹œ„Í•½¹(€€¡•¥¡Ğ½ÈÍÁ•¥•ÌÍ¥±¡½Õ•ÑÑ”¸I”µµ•…ÍÕÉ”Ñ¡”½±¡¥ µÁ…ÍÌÑ…É•Ğ……¥¹ÍĞÑ¡”½ÉÉ•Ñ•(€€É•¹‘•É•È‰•™½É”É•ÕÍ¥¹œ¥ĞìÑ¡”ÁÉ¥½È€ÄĞ¸Ø™¥ÕÉ”µ•…ÍÕÉ•Ñ¡”É•µ½Ù•Í¡••Ğ¸(Ì¸€¨©-¥±°Ñ¡”µ¥‘‘±”µ‘¥ÍÑ…¹”É¥¹œÍ•…´¸¨¨ƒ
Ü€¨©=9€ÈÀÈØ´Àà´ÄÌ¸¨¨QU9¹µ¥¹É…‘¥ÕÌ€ô€ÈÜ¸Á€‘¥(€€µ…ÀÑ¼„½¹ÍÑ…¹ĞÍÉ••¸É½Ü½¸™±…ĞÉ½Õ¹°…¹Ñ¡”µ•…ÍÕÉ•µ•¹ĞÑ¡…ĞÍ…åÌÍ¼¥Ì¹½Ü¥¸Ñ¡”(€€…Ñ”è‰¥¸Ñ¡”Ù¥•Ü‰ä‰•…É¥¹œ°…Í¬•… ‰¥¸¡½Ü™…È¥ÑÌ½İ¸Íİ…ÉÉ•…¡•Ì°½¹Ù•ÉĞÑ¼Ñ¡”É½Ü(€€¥Ğ±…¹‘Ì½¸¸=¸Ñ¡”É¥¹œ…Ì¥ĞÍÑ½½Ñ¡½Í”É½İÌÍÁ…¹¹•€¨¨Ä¸ĞÁà¨¨ƒŠPÑ¡”™¥¹‘¥¹œÌ€‰É…é½È(€€ÍÑÉ…¥¡Ğ…É½ÍÌ…±°€ÄÈàÀ½±Õµ¹Ìˆ°¥¸½¹”¹Õµ‰•È¸¥á•Ñ¡”Í•½¹İ…äÑ¡”¥Ñ•´½™™•ÉÌ°¹½Ğ(€€Ñ¡”™¥ÉÍĞè•Ù•Éä±…ÑÑ¥”Í±½Ğ…ÉÉ¥•Ì¥ÑÌ½İ¸½ÕÑ•ÈÉ…‘¥ÕÌ°™…‘•lÁu€Á±ÕÌ„İ½É±µ…¹¡½É•(€€½™™Í•Ğ½˜ÕÀÑ¼€¨«
ÄÌ´¨¨€£
ÄÄ¸Ø´½¸„Á¡½¹”ƒŠP…‰½ÕĞ…¸•¥¡Ñ ½˜Ñ¡”É¥¹œ…Ğ•Ù•Éä‘•Ñ…¥°(€€Í•ÑÑ¥¹œ¤°™É½´Íµ½½Ñ €Ğ´Ù…±Õ”µ¹½¥Í”±½‰•Ìİ¥Ñ „Á•ÈµÍ±½Ğ‘¥Ñ¡•È½¸Ñ½À¸5•…ÍÕÉ•…™Ñ•Èè(€€€¨¨Ô¸äÁà¨¨½˜ÍÁÉ•……Ğ€ÄÈàÃ\àÀÀ…¹€¨¨ÄÜ¸ĞÁà¨¨…Ğ€ÌäÃ\ÜàÀ°É•…¡¥¹œ€ÈÔ¸ÃŠLÈà¸Ğ´…‰½ÕĞ„(€€¹½µ¥¹…°€ÈØ¸Ğ¸Ù•Éä…É¥ÌÍÑ¥±°É½½Ñ•½¸Ñ¡”Ñ•ÉÉ…¥¸…¹¹½Ñ¡¥¹œµ½Ù•Ù•ÉÑ¥…±±ä¸(€€€´€¨©]¥‘•¹¥¹œÑ¡”™…‘”İ…ÌÑ¡”İÉ½¹œ¡…±˜½˜Ñ¡”¡½¥”¸¨¨Q¡”‰…¹¥Ì…±É•…‘ä€Ü´°İ¡¥ ¥Ì(€€€€€ÄàÁà½˜Ñ¡”™É…µ”…ĞÑ¡…Ğ‘¥ÍÑ…¹”ìÑ¡”±¥¹”¥Ì¹½ĞÑ¡”É…µÀ°¥Ğ¥Ìİ¡•É”Ñ¡”É…µÀÉ•…¡•Ì(€€€€é•É¼°…¹„İ¥‘•ÈÉ…µÀÍÑ¥±°É•…¡•Ìé•É¼•Ù•Éåİ¡•É”…Ğ½¹”¸(€€€´€¨©%Ğ¥Ì¹•…É±ä™É•”°…¹Ñ¡…Ğ¥Ì„ÁÉ½Á•ÉÑä½˜Ñ¡”‘•Í¥¸É…Ñ¡•ÈÑ¡…¸±Õ¬¸¨¨QÉ¥…¹±•Ì…É”(€€€€Á…¥™½È‰äÑ¡”1QQ%°¹½Ğ‰äÑ¡”™…‘”°Í¼„Í±½ĞÑ¡”™É¥¹”ÁÕÍ¡•Ì‰•å½¹É•… ¥Ì(€€€€‘É½ÁÁ•…ĞÉ•‰Õ¥±¥¹ÍÑ•…½˜‘É…İ¸…Ğé•É¼¡•¥¡ĞìÑ¡”±…ÑÑ¥”É•Ü‰äÑ¡”…µÁ±¥ÑÕ‘”Ñ¼(€€€€…ÉÉäÑ¡”½¹•Ì¥ĞÁÕÍ¡•Ì¥¸°…¹İ¥Ñ „Íåµµ•ÑÉ¥Œ½™™Í•ĞÑ¡”µ•…¸½ÍĞ¥Ì(€€€€É…‘¥ÕÏ
È€¬Ù…É¥…¹•€É…Ñ¡•ÈÑ¡…¸€¡É…‘¥ÕÌ€¬…µÁ±¥ÑÕ‘”§
É€¸5•…ÍÕÉ•½…Ğ€ÄÈàÃ\àÀÀ…ĞÑ¡É•”(€€€€™¥á•ÍÑ…Ñ¥½¹Ìè½Á•¸ÁÉ…¥É¥”€¨¨ÄÜĞ€ÌØÌƒŠH€ÄÜØ€ØÔØ¨¨ÑÉ¥…¹±•Ì€ ¬Ä¸Ì€”°€Ì€ÜĞÈƒŠH€Ì€àÔÀ™±½É„(€€€€¥¹ÍÑ…¹•Ì¤°Í•ÑÑ±•Ñ½İ¸€¨¨Ìàä€ÌØäƒŠH€Ìàä€ÈÔÌ¨¨€£Š"HÀ¸ÀÌ€”¤°É¥Ù•È‰…¹¬€¨¨ÌÔÀ€ÄÀäƒŠH€ÌÔÀ€ÄÀÔ¨¨¸(€€€€É…Ü…±±ÌÕ¹¡…¹•…Ğ€ÌÜ€¼€ØØ€¼€ÜÈ¸A…å¥¹œ™½ÈÑ¡”İ¡½±”…¹¹Õ±ÕÌ¥¹ÍÑ•…ƒŠP‘É…İ¥¹œÑ¡”(€€€€ÁÕÍ¡•µ½ÕĞÍ±½ÑÌ…Ğé•É¼¡•¥¡ĞƒŠPİ½Õ±¡…Ù”‰••¸Ñ¡”…µÁ±¥ÑÕ‘”Ñİ¥”½Ù•È¸(€€€´€¨©Q¡”½™™Í•Ğ¥Ì„™Õ¹Ñ¥½¸½˜İ½É±Á½Í¥Ñ¥½¸½¹±ä¨¨°Í¼Ñ¡”É…••‘”¥Ì…¹¡½É•Ñ¼Ñ¡”(€€€€É½Õ¹è¥Ğ‘½•Ì¹½ĞÍİ¥´…ÌÑ¡”İ…±­•Èµ½Ù•Ì°…¹¥Ğ¥ÌÑ¡”Í…µ”•‘”İ¡¥¡•Ù•Èİ…äÑ¡•ä(€€€€™…”¸Q¡”…Ñ”…Í­ÌÑ¡”Á±…•È€¡™±½É„¹™É¥¹•Ñ€¤™½È¥ĞÉ…Ñ¡•ÈÑ¡…¸É”µ‘•É¥Ù¥¹œÑ¡”¹½¥Í”°(€€€€…¹¡•­Ì¹¥¹”Á½¥¹ÑÌ…¹Íİ•È¥‘•¹Ñ¥…±±ä™É½´Ñİ¼…µ•É…Ì€ĞÀ´…Á…ÉĞ¸(€€€´€¨©Q¡”™½ÉˆÉ¥¹œ•¹‘Ìİ¥Ñ¡¥¸„µ•ÑÉ”½˜Ñ¡”µ¥É¥¹œ¨¨°Í¼Ñ¡”™±½İ•ÉÌİ½Õ±¡…Ù”½¹”½¸(€€€€‘É…İ¥¹œÑ¡”±¥¹”Ñ¡”É…ÍÌ¹¼±½¹•È‘½•Ìì¥Ğ…ÉÉ¥•ÌÑ¡”Í…µ”™É¥¹”¸%Ğ¥Ì…Ñ•½¸¥ÑÌ(€€€€I%9LÉ…Ñ¡•ÈÑ¡…¸½¸¥ÑÌ‘É…İ¸•‘”ƒŠP…Ğ€Ì¸Ğ´•±±Ì„€Ì¸Ü×
À‰¥¸¡½±‘Ì½¹”½ÈÑİ¼™½É‰Ì°Í¼(€€€€€‰Ñ¡”™ÕÉÑ¡•ÍĞ½¹”‘É…İ¸ˆ¥Ì„Í…µÁ±¥¹œÍÑ…Ñ¥ÍÑ¥Œ°…¹µ•…ÍÕÉ•Ñ¡…Ğİ…ä¥ĞÉ•Á½ÉÑ•„¹¥¹”(€€€€µ•ÑÉ”¡½±”¥¸É½Õ¹Ñ¡…Ğ¡…Ì¹½¹”¸(€€€´€¨©Q¡”Á½Àµ¥¸…Ñ”¡…Ñ¼‰”µ…‘”¥¹ÍÑ…¹”µ…İ…É”Ñ¼ÍÑ…ä¡½¹•ÍĞ¸¨¨%Ğ…Í­•Ñ¡”±…å•ÈÌ(€€€€¹½µ¥¹…°É¥¹œ¡½Ü™…‘•…¸…ÉÉ¥Ù¥¹œÁ±…¹Ğİ…Ì°…¹Ñ¡”¹½µ¥¹…°É¥¹œ…¹Íİ•ÉÌ€©é•É¼¨ƒŠP„™É•”(€€€€Á…ÍÌƒŠP™½È•á…Ñ±äÑ¡”Á±…¹ÑÌÑ¡”™É¥¹”ÁÕÍ¡•Ì™ÕÉÑ¡•ÍĞ½ÕĞ¸%ĞÉ•…‘Ì•… ¥¹ÍÑ…¹”Ì½İ¸(€€€€…¡¥I¥¹€¹½Ü¸M…µ”‰½Õ¹°Í…µ”µ•…ÍÕÉ•€À¸À€”…ÉÉ¥Ù…°¡•¥¡Ğ¸(Íˆ¸€¨©Q¡”9H½5%¡…¹‘½Ù•È¥Ì„‘•¹Í¥Ñä¡…¹‘½Ù•È¸¨¨ƒ
Ü€¨©=9€ÈÀÈØ´Àà´ÈĞ°P´ÀÀäÌ¸¨¨Q¡”Í¥‰±¥¹œ½˜(€€¥Ñ•´€ÌèÑ¡…Ğ½¹”İ…Ì…‰½ÕĞİ¡•É”Ñ¡”Íİ…ÉMQ=AL°Ñ¡¥Ì½¹”¥Ì…‰½ÕĞİ¡•É”¥ÑÌÑİ¼(€€É•ÁÉ•Í•¹Ñ…Ñ¥½¹ÌÍİ…À½Ù•È¸I•…Ñ¡¥Ì‰½à‰•™½É”ÅÕ½Ñ¥¹œ„¹•…ÈµÉ¥¹œ‰…¹½È‰•™½É”…ÍÍÕµ¥¹œ„(€€É¥¹œ¹…µ•¥¸„Ñ¥­•Ğ¥ÌÑ¡”É¥¹œ‘É…İ¥¹œÑ¡”…ÉÑ•™…Ğ¸(€€€´€¨©Q¡”¥¹ÍÑÉÕµ•¹Ğ™¥ÉÍĞ¨¨°‰•…ÕÍ”Ñ¡•É”İ…Ì¹½¹”èÑ½½±Ì½µ•…ÍÕÉ•}¹•…É}Ù•É”¹µ©Í€±…ÍÍ•Ì•Ù•Éä(€€€€™±½É„¥¹ÍÑ…¹”Ñ¡”İ…äÑ¡”™É…µ•¹ĞÍ¡…‘•ÈÌ½İ¸Õ…É‘½•ÌƒŠPİ¡½±•€€¡½Ù•É…”€Ä°Ñ¡”	…å•È(€€€€‰É…¹ ¥ÌÍ­¥ÁÁ•¤°Á…ÉÑ¥…±€€ À€ğ½Ù•É…”€ğ€Ä°€¨©•Ù•Éä™É…µ•¹ĞÑ¡É•Í¡½±‘•ƒŠPÑ¡”‘½ÑÌ¨¨¤°(€€€€…‰Í•¹Ñ€ƒŠP½™˜Ñ¡”…¡¥I¥¹€Ñ¡…Ğİ•¹ĞÑ¼Ñ¡”AT°Ñ¡•¸ÁÉ½©•ÑÌ•… ‘É…İ¸Á±…¹ĞÌÉ•½É‘•(€€€€¡•¥¡Ğ…¹ÍÁÉ•…Ñ¼ÍÉ••¸…¹ÍÕµÌÑ¡”™½½ÑÁÉ¥¹ÑÌ¸%¹ÍÑ…¹”½Õ¹ÑÌ…É”Ñ¡”İÉ½¹œÕ¹¥Ğè„(€€€€¡Õ¹‘É•Á±…¹ÑÌ…Ğ™½ÉÑäµ•ÑÉ•Ì…É”™½ÕÈÁ¥á•±Ì¸5½‰¥±”ÉÕ¹Ì…Ğ‘•Ù¥•M…±•…Ñ½Èè€Ä¸Õ€°¹½Ğ(€€€€Ñ¡”Íµ½­”Ì€È°Í¼½¹”µ•…ÍÕÉ•Á¥á•°¥Ì½¹”‘É…İ¥¹œµ‰Õ™™•ÈÁ¥á•°ƒŠPÑ¡”ÍÉ••¸‘½½È¥Ì±½­•(€€€€Ñ¼±}É…½½É‘€…¹„€Ğ¼ÌÉ•Í…µÁ±”Íµ•…ÉÌÑ¡”É…¥¸¸(€€€´€¨©Q!Q%-PLAI%5MUMAP%L!1Q!UQ!=H°9P%QL=]8Q]<MQ9L%P%L9=9=%P¸¨¨(€€€€P´ÀÀàØÌÑİ¼ÍÑ…¹‘Ì…É”¥¸„É½…‘İ…ä…¹ÍÑ…Ñ¥½¸ ¥€±•…ÉÌÑ¡”ÑÉ…Ù•°ÑÉ…¬ƒŠP€ÄÀ¸Ô´½¸M½ÕÑ (€€€€]…Ñ•È°€Ü´½¸]•±±ÌƒŠPÍ¼…Ğ€©M½ÕÑ ]…Ñ•È…ÁÁÉ½…¡¥¹œ]•±±Ì¨Ñ¡”¹•…ÈÉ¥¹œÁ±…•Ì€¨¨ÀÑÕ™ÑÌ…Ğ(€€€€±¥¡Ñ€°€Ä…Ğ™Õ±±€¨¨¸Ğ€©]•±±Ì…ÁÁÉ½…¡¥¹œ1…­”¨½¸„Á¡½¹”Ñ¡”¹•…ÈÍ•Ğ¥Ì•µÁÑä…¹Ñ¡”(€€€€İ¡½±”ÍÉ••¸µ‘½½É•Ù•É”€ Ä¸ÜÈä€”½˜Ñ¡”™É…µ”¤¥ÌİÉ¥ÑÑ•¸‰äÑ¡”€¨©µ¥É¥¹œÌ¥¹¹•ÈÉ…µÀ(€€€€™…‘¥¹œ%8…É½ÍÌ€Ğ¸×ŠLÜ¸Ô´¨¨¸=¹±ä¥¸½Á•¸ÁÉ…¥É¥”‘½•ÌÑ¡”¹•…ÈÉ¥¹œ‘½µ¥¹…Ñ”è€Ô¸äÀ€”……¥¹ÍĞ(€€€€Ñ¡”µ¥Ì€Ì¸ØÔ€”•áÁ½Í•…Ğ±¥¡Ñ€¸M¼‰½Ñ ‰½Õ¹‘…É¥•Ìİ•É”½¹Ù•ÉÑ•°¹½ĞÑ¡”¹…µ•½¹”¸(€€€´€¨©Q¡”‰…¹¥Ì¹½Ğİ¡•É”Ñ¡”Ñ¥­•ĞÍ…åÌ•¥Ñ¡•È¸¨¨É¥¹Í½É€¥¹Í•ÑÌ•Ù•Éä™…‘”É¥¹œ¥¹Í¥‘”¥ÑÌ(€€€€±…ÑÑ¥”‰äÑ¡”€À¸Ø´É•‰Õ¥±ÍÑ•À°Í¼Ñ¡”É…µÀÉÕ¹Ì€¨¨Ğ¸àÃŠLÜ¸ÀÀ´¨¨…Ğ™Õ±±€€¡µ•…ÍÕÉ•…ÌÑ¡”(€€€€‘€É…¹”½˜Ñ¡”Á…ÉÑ¥…°¥¹ÍÑ…¹•Ì¤°¹½Ğ€Ô¸ÓŠLÜ¸Øì…¹…Ğ±¥¡Ñ€Ñ¡”É¥¹œ¥Ì€Ğ¸Ø´°Í¼Ñ¡”É…µÀ(€€€€¥Ì€¨¨Ä¸àÃŠLĞ¸ÀÀ´¨¨ƒŠPÕ¹‘•ÈÑ¡”İ…±­•ÈÌ™••Ğ°İ¡¥ ¥Ìİ¡äÑ¡”Á¡½¹”™É…µ”¥ÌÑ¡”‘É…µ…Ñ¥Œ½¹”(€€€€€ ÔÌ¸ØÔĞ€”½˜¥ĞÍÉ••¸µ‘½½É•¥¸½Á•¸ÁÉ…¥É¥”°……¥¹ÍĞ€ĞÔ¸ÄÜÌ€”½¸Ñ¡”‘•Í­Ñ½À¤¸(€€€´€¨©Q¡”™¥à¥ÌP´ÀÀàØÌ…¹Íİ•È½¸„É¥¹œÑ¡…ĞÍÑ¥±°¡…Ì…¸•‘”¥¸¥Ğ¸¨¨QU9€(€€€€¹•…È¹ÍÁÉ•…‘=ÕÑ•É€€¼µ¥¹ÍÁÉ•…‘%¹¹•É€µ½Ù”Ñ¡”‰…¹½ÕĞ½˜Ñ¡”É…µÀ…¹¥¹Ñ¼„Á•ÈµÍ±½Ğ(€€€€ÍÁÉ•…½˜Ñ¡”‰½Õ¹‘…Éäè™…‘•lÁtƒŠ"H‰…¹ƒ\¡…¹‘½Ù•ÉI…¹¬¡”°¸¥€°İ½É±µ…¹¡½É•…¹ÅÕ…¹Ñ¥Í•Ñ¼(€€€€ƒŠl´…Ì™…ÉI…¹­€¥Ì°İ¥Ñ Ñ¡”Í¡…‘•ÈÌÉ¥¹œ±•™Ğ…Ì„ÍÑ•À€¡!I€¤¸Q¡”™É…Ñ¥½¸½˜Í±½ÑÌ(€€€€‘É…İ¸…Ğ‘€¥Ì±…µÀ ¡™…‘•lÁtƒŠ"H¤€¼‰…¹¥€ƒŠP€¨©Ñ¡”Í…µ”¹Õµ‰•ÈÑ¡”…±Á¡„ÕÍ•Ñ¼İÉ¥Ñ”¨¨ƒŠP(€€€€Í¼•áÁ•Ñ•½Ù•È¥ÌÕ¹¡…¹•Ñ¼Ñ¡”…É¥Ñ¡µ•Ñ¥Œ…¹¹¼ÑÕ¹¥¹œ™¥ÕÉ”µ•…¹Ì…¹åÑ¡¥¹œ¹•Ü¸(€€€´€¨©A±…•µ•¹Ğ¥ÌÕ¹Ñ½Õ¡•½¸ÁÕÉÁ½Í”¸¨¨Q¡”µ¥É¥¹œÌÉ•ÑÕÉ¹€™½ÈÍ±½ÑÌÑ¡”™É¥¹”ÁÕÍ¡•Ì½ÕĞ(€€€€½˜É•… ¥Ì‘•±¥‰•É…Ñ•±ä9=P½Á¥•Ñ¼Ñ¡”¹•…ÈÁ…ÍÌè•Ù•ÉäÍ±½Ğ¥ÌÍÑ¥±°‘•…±Ğ„ÍÁ•¥•Ì…¹(€€€€ÍÑ¥±°½Õ¹Ñ•°Í¼¹¼½µµÕ¹¥ÑäÌÁ½ÁÕ±…Ñ¥½¸½È½Ù•È™¥ÕÉ”µ½Ù•Ì¸%Ğ½ÍÑÌ¹½Ñ¡¥¹œƒŠPÑ¡”(€€€€Ù•ÉÑ•àÁÉ½É…´…±É•…‘ä½±±…ÁÍ•…¸½ÕĞµ½˜µÉ¥¹œÁ±…¹ĞÑ¼„Á½¥¹ĞƒŠP…¹¥ĞÍ…Ù•Ì™¥±°°‰•…ÕÍ”(€€€€¡…±˜Ñ¡”‰…¹Ì™É…µ•¹ÑÌ…É”¹¼±½¹•ÈÉ…ÍÑ•É¥Í•½¹±äÑ¼‰”‘¥Í…É‘•¸(€€€´€¨©Qİ¼­¹½¬µ½¹Ì¸¨¨!•…‘ÌÉ¥‘”Ñ¡•¥ÈA19PÌÉ¥¹œ¹½Ü°¹½ĞÑ¡”±…å•ÈÌè½¸„ÍÁÉ•…‰½Õ¹‘…ÉäÑ¡”(€€€€±…å•ÈÌÉ¥¹œ…¹Íİ•ÉÌ™½È¹¼Á…ÉÑ¥Õ±…ÈÑÕ™Ğ°…¹„¡•…¡Õ¹œ½¸¥Ğ¥ÌHµ	UÜ™É½´Ñ¡”½Ñ¡•È(€€€€•¹¸¹™±½É„¹™…‘•Ñ€½¡•¥¡ÑÑ€Ñ…­”…±°™½ÕÈÉ¥¹œ¹Õµ‰•ÉÌ°‰•…ÕÍ”„É•…‘•È…ÉÉå¥¹œ½¹±ä(€€€€Ñ¡”½ÕÑ•ÈÉ…‘¥ÕÌİ½Õ±‰”Ñ½±•Ù•Éäµ¥…ÉÁ…ÍĞ€Ğ¸Ô´¥Ì‘É…İ¸¸(€€€´€¨©Q¡”É•Í¥‘Õ”°¡•±É…Ñ¡•ÈÑ¡…¸±½Í•¸¨¨Q¡”µ¥…¹™½ÉˆÉ¥¹Ìœ½İ¸=UQHÉ…µÁÌ…É”ÍÑ¥±°(€€€€½Ù•É…”É…µÁÌ°…¹…Ğ±¥¡Ñ€Ñ¡•äÉ•… ¥¸Ñ¼€¨¨Ô¸Ğ´¨¨…¹€¨¨Ü¸Ğ´¨¨ƒŠP¥¹Í¥‘”Ñ¡”Ù•É”½¸„(€€€€Á¡½¹”¸Q¡…Ğ¥ÌÑ¡”µ¥“ŠI™…È¡…¹‘½Ù•È°İ¡¥ P´ÀÀàØ…¹Íİ•É•‰äÍÑ…¹‘¥¹œÑ¡”™…È‰…¹½Ù•È¥Ğì(€€€€Ñ¡”…Ñ”¡½±‘Ì¥Ğ……¥¹ÍĞÑ½½±Ì½¹•…É}Ù•É•}‰…Í•±¥¹”¹©Í½¹€Í¼¥Ğ…¹¹½ĞÉ½Ü°…¹¥Ğ¥Ì™¥±•¸(€€€€€¨©±½Í•€ÈÀÈØ´Àà´ÈÜ‰ä¥Ñ•´€ÍŒ‰•±½Ü°…¹9=PÑ¡”İ…äÑ¡¥Ì‰½à•áÁ•Ñ•¸¨¨(ÍŒ¸€¨©Q¡”½ÕÑ•ÈÉ…µÁÌœ]%Q °¹½ĞÑ¡•¥È­¥¹¸¨¨ƒ
Ü€¨©=9€ÈÀÈØ´Àà´ÈÜ°P´ÀÄàÜ¸¨¨Q¡”É•Í¥‘Õ”¥Ñ•´€Íˆ(€€‰…¹­•è…Ğ±¥¡Ñ€Ñ¡”µ¥…¹™½ÉˆÉ¥¹Ìœ½ÕÑ•È½Ù•É…”É…µÁÌ‰•…¸€Ô¸Ğ´…¹€Ü¸Ğ´…¡•…½˜(€€Ñ¡”İ…±­•È…¹€ÄÔ¸Ğ€”½˜Ñ¡”Á¡½¹”Ì™É…µ”¥¹Í¥‘”¹¥¹”µ•ÑÉ•Ìİ…ÌİÉ¥ÑÑ•¸Ñ¡É½Õ Ñ¡”ÍÉ••¸(€€‘½½È¸I•…Ñ¡¥Ì‰½à‰•™½É”ÁÉ½Á½Í¥¹œ„‘•¹Í¥Ñä¡…¹‘½Ù•È½¸…¹ä=UQH•‘”¸(€€€´€¨©Q¡”…ÕÍ”¥Ì½¹”±¥¹”Ñ¡…Ğİ…Ì¹•Ù•ÈÍ…±•¸¨¨1=]€…¹5%€ÕĞÉ…‘¥ÕÍ€…¹Í…±•(€€€€™É¥¹•€İ¥Ñ ¥ĞƒŠP€‰…‰½ÕĞ…¸•¥¡Ñ ½˜Ñ¡”É…‘¥ÕÌ…Ğ•Ù•ÉäÍ•ÑÑ¥¹œˆ°¥ÑÌ½İ¸½µµ•¹ĞƒŠP…¹±•™Ğ(€€€€‰…¹‘€…ĞQU9Ì€Ü¸À´…¹€Ô¸À´¸É…µÀÍ¥é•™½È€ÄãŠLÈÜ´Ñ¡•É•™½É”Í…Ğ½¸„€ÄÌ´É¥¹œ…¹(€€€€…µ”½ÕĞ…É½ÍÌÑ¡”µ¥‘‘±”½˜Ñ¡”Á¡½¹”Ì™¥•±¸‰…±…¹•‘€¡…¥ĞÑ½¼èÑ¡”µ¥É…µÀ‰•…¸…Ğ(€€€€€¨¨à¸È´¨¨Ñ¡•É”°…±Í¼¥¹Í¥‘”Ñ¡”Ù•É”¸9½Ñ¡¥¹œ…‰½ÕĞÑ¡”Á¡½¹”İ…ÌÍÁ•¥…°ìÑ¡”¹Õµ‰•ÈÍ¥µÁ±ä(€€€€İ…Ì¹½Ğ…ÉÉ¥•‘½İ¸¸(€€€´€¨©Q!=	Y%=UL%`]LAI%9IUM°…¹Ñ¡”¹Õµ‰•È¥ÌÑ¡”É•…Í½¸¸¨¨!…¹‘¥¹œÑ¡•Í”•‘•Ì(€€€€½Ù•È‰ä‘•¹Í¥ÑäƒŠPÍÁÉ•…‘=ÕÑ•É€°P´ÀÀäÌÌ½İ¸…¹Íİ•ÈƒŠPİ…ÌÍ¥µÕ±…Ñ•Í±½Ğ‰äÍ±½Ğ½¸Ñ¡”(€€€€ÁÕ‰±¥Í¡•µ¥ÉÉ½È……¥¹ÍĞ•Ù•Éäµ¥¥¹ÍÑ…¹”Ì½İ¸…¡¥I¥¹€…¹Ñ¡”…Ñ”Ì½İ¸€ÄØ‰•…É¥¹œ(€€€€‰¥¹Ì¸%ĞÑ…­•ÌÑ¡”µ•…¸‘É…İ¸É•… ™É½´€¨¨ÈØ¸àÄ´Ñ¼€ÈÔ¸ĞÈ´…Ğ™Õ±±€¨¨°İ¡¥ Ñ¡”‰½Õ¹‘…Éä(€€€€¡•¬ÍÕÉÙ¥Ù•Ì€¡‰…È€ÈĞ¸äÀ¤°…¹™É½´€¨¨ÄÄ¸àä´Ñ¼€ä¸ØĞ´…Ğ±¥¡Ñ€¨¨°İ¡•É”Ñ¡”‰…ÈÍÑ…¹‘Ì…Ğ(€€€€€¨¨ÄÄ¸ØÀ´…¹½¹±ä€À¸Èä´½˜¥Ğİ…ÌÕ¹ÍÁ•¹Ğ¨¨¸Ù•¸„½¹”µµ•ÑÉ”ÍÁÉ•…±…¹‘Ì…Ğ€ÄÄ¸Ğà´¸Q¡”(€€€€±½ÍÌ¥Ì¹½Ğ„ÑÕ¹¥¹œ…ÉÑ•™…ĞèÑ¡”‘É…İ¸•‘”½˜„ÍÑ½¡…ÍÑ¥ŒÑ¡¥¹¹¥¹œ¥ÌÑ¡”‘•ÁÑ …Ğİ¡¥ (€€€€Ñ¡”Ñ¡¥¹¹¥¹œÍÑ¥±°±•…Ù•Ì„Á±…¹ĞÍÑ…¹‘¥¹œ¥¸„¥Ù•¸‰•…É¥¹œ°…¹Ñ¡”µ¥±…ÑÑ¥”‘•…±Ì…‰½ÕĞ(€€€€½¹”Í±½ĞÁ•Èµ•ÑÉ”Á•È‰¥¸…Ğ€ÄÈ´……¥¹ÍĞÑİ¼…¹„Ñ¡¥É…Ğ€ÈØ´¸(€€€´€¨©Q¡”‰…È¥Ğ™…¥±Ì¥ÌÉ•ÍÑ¥¹œ½¸Á±…¹ÑÌ¹½‰½‘ä…¸Í•”°…¹Ñ¡…Ğ¥Ì¹½Ü¥ÑÌ½İ¸Ñ¥­•Ğ¸¨¨Q¡”(€€€€É•… …‘µ¥ÑÌ…¹äÁ±…¹Ğ…Ğ™…‘•Ğ€ø€À¸ÀÉ€ƒŠPÑİ¼Á•È•¹Ğ½Ù•É…”°½¹”Á¥á•°¥¸™¥™ÑäÑ¡É½Õ (€€€€Ñ¡”	…å•Èµ…ÑÉ¥à¸=¸„½Ù•É…”É…µÀÑ¡…Ğ¥Ì•Ù•ÉäÁ±…•Í±½Ğ°Í¼Ñ¡”ÍÑ…Ñ¥ÍÑ¥ŒÉ•Á½ÉÑÌİ¡•É”(€€€€Ñ¡”Á±…•ÈÍÑ½ÁÁ•Á±…¥¹œÉ…Ñ¡•ÈÑ¡…¸İ¡•É”Ñ¡”™¥•±•¹‘Ì°…¹¥Ğ…¸½¹±ä•Ù•È‰”µ•Ğ‰ä(€€€€‘É…İ¥¹œ¡½ÍÑÌ¸€¨©P´ÀÈÀä¸¨¨Q¡”‰…ÉÌİ•É”±•™Ğ•á…Ñ±äİ¡•É”Ñ¡•äÍÑ½½¸(€€€´€¨©M¼Ñ¡”É…µÀ¥ÌÕĞÑ¼Ñ¡”É¥¹œ¥¹ÍÑ•…¸¨¨Q¡”ÉÕ±”è…¸½ÕÑ•È‰…¹µ…ä¹½Ğ	%8¥¹Í¥‘”Ñ¡”(€€€€Ù•É”ƒŠPÉ…‘¥ÕÌƒŠ"HÍÑ•ÀƒŠ"H™É¥¹”ƒŠ"H€ä¸Á€°Ñ¡”¹¥¹”µ•ÑÉ•ÌÑ½½±Ì½µ•…ÍÕÉ•}¹•…É}Ù•É”¹µ©Í€…±±Ì(€€€€Ñ¡”É½Õ¹„İ…±­•È±½½­Ì…Ğ¸±¥¡Ñ€Ñ…­•Ì€¨¨Ä¸Ø´¨¨½¸‰½Ñ É¥¹Ì€¡Ñ¡”±•…É…¹”‰¥¹‘Ì…Ğ(€€€€€Ä¸àì¥Ğ±…¹‘Ì•ÅÕ…°Ñ¼Ñ¡”™É¥¹”°Í¼Ñ¡”•‘”Ñ¡¥¹Ì½Ù•È¹¼µ½É”É½Õ¹Ñ¡…¸¥Ğ¥ÌÉ…•(€€€€‰ä¤ì‰…±…¹•‘€Ñ…­•ÌÑ¡”ÁÉ½Á½ÉÑ¥½¹…Ñ”€¨¨Ğ¸Ü´¨¨…¹€¨¨Ì¸Ğ´¨¨°İ¡¥ …±É•…‘ä±•…È¥Ğì™Õ±±€(€€€€¥ÌÕ¹¡…¹•…Ğ€Ü¸À´…¹€Ô¸À´°±•…É¥¹œ‰ä€ÄØ¸Ğ´…¹€ÄÜ¸Ğ´¸(€€€´€¨©]¡…Ğ¥Ğ½ÍÑÌ…¹İ¡…Ğ¥Ğ‰ÕåÌ¸¨¨Q¡”±…ÑÑ¥”¥ÌÕ¹Ñ½Õ¡•°Í¼ÑÉ¥…¹±•Ì°¥¹ÍÑ…¹•Ì…¹‘É…Ü(€€€€…±±Ì…É”Õ¹¡…¹•ƒŠPÑ¡”É…µÀÌ½İ¸½µµ•¹Ğ¥¸¥Ñ•´€Ì…±É•…‘äÍ…åÌÑ¡”±…ÑÑ¥”Á…åÌ™½ÈÑ¡”(€€€€•½µ•ÑÉä…¹Ñ¡”™…‘”Á…åÌ™½È¹½Ñ¡¥¹œ¸]¡…Ğ¡…¹•Ì¥Ì™¥±°èÑ¡”É½Õ¹Ñ¡”É…µÀÕÍ•Ñ¼(€€€€Ñ¡¥¸¥Ì‘É…İ¸Í½±¥°…¹Ñ¡”Á¡½¹”ÌÍİ…ÉÍÑ½ÁÌ½Á•¹¥¹œÕÀ™¥Ù”µ•ÑÉ•Ì…¡•…½˜Ñ¡”İ…±­•È¸(€€€€=™˜¥‘•¹Ñ¥…°Á±…•µ•¹Ğ°™±½É„µµ¥‘€‘É…İ¸]!=1½•Ì€¨¨ÄÜƒŠH€ÄĞĞ¨¨¥¸½Á•¸ÁÉ…¥É¥”°€ÈƒŠH€ÜÄ…Ğ(€€€€]•±±Ì°€ØƒŠH€ÌÄ½¸Ñ¡”M½ÕÑ ]…Ñ•ÈÙ•É”¸Q¡”™±½İ•È¡•…‘ÌÉ•… ™ÕÉÑ¡•È½ÕĞİ¥Ñ ¥Ğ°‰•…ÕÍ”(€€€€¡•…‘I¥¹=™€¡…¹ÌÑ¡”¡•…É¥¹œ½™˜Ñ¡”‰…¹€¡™…‘•lÁtƒŠ"H€À¸ÌÔƒ\‰…¹‘€¤è…Ğ±¥¡Ñ€Ñ¡”™½Éˆ(€€€€¡•…‘ÌÉÕ¸Ñ¼€ÄÄ¸à´İ¡•É”Ñ¡•äÍÑ½ÁÁ•…Ğ€ÄÀ¸À´¸(€€€´€¨©¹Ñ¡”É•… ¥Ğİ…ÌÉ•™ÕÍ•™½Èİ•¹ĞU@¸¨¨A…ÉĞ€Ü…Ğ€ÌäÃ\ÜàÀ…™Ñ•Èèµ¥¸€¨¨ÄÀ¸ÌÈ´¨¨(€€€€€¡Õ¹µ½Ù•¤°µ•…¸€¨¨ÄÄ¸àäƒŠH€ÄÄ¸äØ´¨¨°µ…à€¨¨ÄÈ¸ÜØƒŠH€ÄÌ¸ÈÈ´¨¨°‰½Õ¹‘…ÉäÉ½İÌ€¨¨ÄÜ¸ĞƒŠH€Ää¸àÁà¨¨°(€€€€‰½Ñ ‰…ÉÌÉ••¸İ¡•É”Ñ¡•äÍÑ½½¸É¥Ñ¡µ•Ñ¥ŒÉ…Ñ¡•ÈÑ¡…¸±Õ¬ƒŠPÑ¡”Íµ½­”Õ±±Ì‰•±½Ü(€€€€™…‘•Ğ€ğô€À¸ÀÉ€°İ¡¥ ¥Ì€À¸ÄĞ´½˜É•… ½¸„€Ü´‰…¹…¹€À¸ÀÌ´½¸„€Ä¸Ø´½¹”¸]¡¥ ¥Ì(€€€€Ñ¡”µ¥ÉÉ½È¥µ…”½˜İ¡äÑ¡”‘•¹Í¥Ñä¡…¹‘½Ù•È½Õ±¹½Ğ‰”¡…è¥Ğ‘½•Ì¹½Ğ‘É…ÜÑ¡”½ÕÑ•Éµ½ÍĞ(€€€€Á±…¹ÑÌ…Ğ…±°¸(Ğ¸€¨©I”µ‰…Í•±¥¹”Ñ¡”É½İ¸µ•ÑÉ¥Ì¸¨¨Q¡”ÁÉ•Ù¥½ÕÌÉ½İ¸™¥¹”µ‘•Ñ…¥°°‘…É­¹•ÍÌ…¹¡Õ”Ñ…É•ÑÌ(€€µ•…ÍÕÉ•„ÍÕÉ™…”Ñ¡…Ğ¹¼±½¹•È•á¥ÍÑÌ¸ÍÑ…‰±¥Í ¹•Ü¹•…È½µ¥…¹™…ÈµÑ•ÉÉ…¥¸‰…¹‘Ì‰•™½É”(€€ÑÕ¹¥¹œ½±½ÕÈ½È½¹ÑÉ…ÍĞì¹•Ù•È¥µÁÉ½Ù”Ñ¡”Í½É”‰ä±½Í¥¹œÑ¡”™…È™¥•±¥¹Ñ¼„Í¡••Ğ¸(Ô¸€¨©!½É¥é½¸½¹Ñ¥¹Õ¥Ñä¸¨¨½±Õµ¹Ì…ÉÉå¥¹œÑ¥µ‰•È€¨¨ÌÄ€”ƒŠHƒŠ&”€äÀ€”¨¨€¡É•™•É•¹”€ÄÀÀ€”¥¸•Ù•Éä(€€‰…¹¤¸	…¹€©¡•¥¡Ğ¨ÍÑ…åÌ€ÇŠLĞÁàƒŠPÑ¡…Ğ…É¥Ñ¡µ•Ñ¥Œ¥Ì¡½¹•ÍĞ¸Qİ¼µ•¡…¹¥ÍµÌè‘É½À(€€¡…é•¥ÍÁ±…å1¥¹•…È ¥€ÌLÍÑ•ÀÍ¼Ñ¡”‰…¹ÍÑ½ÁÌ‰•¥¹œ…¥µ•€ÄØH€¼€ÄÈÁ…ÍĞÑ¡”É½Õ¹(€€¥ĞÑ½Õ¡•Ì°…¹ÍÕÁÁÉ•ÍÌÑ¡”É½İ¸½…Àµ½‘Õ±…Ñ¥½¸­€İ¡•¹•Ù•È„É½İ¸ÍÕ‰Ñ•¹‘ÌÕ¹‘•ÈøÈÁà°(€€İ¡•É”¥Ğ‘•±•Ñ•ÌÑ¡”Í¥±¡½Õ•ÑÑ”É…Ñ¡•ÈÑ¡…¸Ñ•áÑÕÉ¥¹œ¥Ğ¸(€€€¨©	=Q 5!9%M5L=9€ÈÀÈØ´Àà´ÄÌ¸Q¡”Á¡½Ñ½É…Á¡¥Œ½±Õµ¸½Õ¹Ğ¥Ì9=PÉ”µµ•…ÍÕÉ•°…¹(€€Ñ¡…Ğ¡…±˜½˜Ñ¡”¥Ñ•´ÍÑ…åÌ½Á•¸¨¨ƒŠPÑ¡”Í¡½Ğ¡…É¹•ÍÌÑ¡”€ÌÄ€”…µ”™É½´¥Ì¹½Ğ¥¸Ñ¡”…Ñ”°(€€…¹ÅÕ½Ñ¥¹œ„¹Õµ‰•ÈÑ¡¥ÌÍ±¥”‘¥¹½Ğµ•…ÍÕÉ”İ½Õ±‰”•á…Ñ±äÑ¡”™…¥±ÕÉ”ƒ
œLÙ„İ…Ì(€€É•½É‘•É•Ñ¼ÍÑ½À¸(€€€´€¨©Q¡”½±½ÕÈ¥Ì½¹”±¥¹”…¹¥Ğİ…Ì…É¥Ñ¡µ•Ñ¥Œ…¹Íİ•É¥¹œÑ¡”İÉ½¹œÅÕ•ÍÑ¥½¸¸¨¨(€€€€¡…é•¥ÍÁ±…å1¥¹•…È ¥€É…¸!=I%i=9}!i€Ñ¡É½Õ LÑ¼É•… Ñ¡”‰…¹Ì‘¥ÍÁ±…ä½±½ÕÈ¸(€€€€Q¡”‰…¹¥ÌÑ½¹•5…ÁÁ•è™…±Í”°™½œè™…±Í•€°Í¼¥ÑÌ™É…µ•¹Ğ½•Ì½Á…ÅÕ”ƒŠH½±½ÉÍÁ…•€(€€€€…¹„±¥¹•…ÈÙ•ÉÑ•à½±½ÕÈ‘¥ÍÁ±…åÌ…ÌÑ¡”¡•à¥Ğ‘•½‘•Ì™É½´ìÑ¡”™½•É½Õ¹½•Ì(€€€€½Á…ÅÕ”ƒŠHÑ½¹•µ…ÁÁ¥¹œƒŠH½±½ÉÍÁ…”ƒŠH™½€İ¥Ñ ™½½±½É€ÕÁ±½…‘•¥¸Ñ¡”=UQAUP½±½ÕÈ(€€€€ÍÁ…”°Í¼¥Ğ½¹Ù•É•Ì½¸Ñ¡…ĞÍ…µ”±¥Ñ•É…°¡•à¸=¹”‘•½‘”•… ¸Q¡”Ñ½¹”ÕÉÙ”İ…Ì(€€€€…ÁÁ±¥•Ñ¼½¹”•¹…¹Ñ¼¹½Ñ¡¥¹œ¥Ğ¡…Ñ¼µ…Ñ °İ¡¥ ¥ÌÑ¡”€ÄØH€¼€ÄÈƒŠP…¹Ñ¡”€Øä(€€€€¥¸‰±Õ”…ĞÁÉ…¥É¥•}İ•ÍÑ€ƒŠP½˜0ÌÔ¸	½Ñ •¹‘Ì¹½ÜÉ•Á½ÉĞ€¨¨Œàá„ÍŒÀ¨¨…¹Ñ¡”…Ñ”½µÁ…É•Ì(€€€€Ñ¡”‰…¹Ì½İ¸¡…é••¹……¥¹ÍĞÍ•¹”¹™½œ¹½±½É€É…Ñ¡•ÈÑ¡…¸……¥¹ÍĞ„¡•à¥¸•¥Ñ¡•È(€€€€™¥±”¸Í•½¹½¹Í•ÅÕ•¹”°Õ¹ÍÑ…Ñ•¥¸Ñ¡”¥Ñ•´èÑ¡”‰…¹Ì™…È•¹İ…Ì‘¥ÍÁ±…å¥¹œ…Ğ(€€€€€¨©0€ÄÜÀ……¥¹ÍĞ„¡½É¥é½¸Í­ä½˜0€ÄØÈ¨¨ƒŠP„€©Á…±”¨‰…¹°‰É¥¡Ñ•ÈÑ¡…¸Ñ¡”Í­ä‰•¡¥¹¥Ğ°(€€€€İ¡¥ ¥ÌÑ¡”½¹”Ñ¡¥¹œ„ÑÉ••±¥¹”¹•Ù•È¥Ì¸%Ğ¥Ì0€ÄÔä¹½Ü°Ñ¡É•”‰•±½Ü¥ÑÌÍ­ä¸(€€€´€¨©Q¡”µ½‘Õ±…Ñ¥½¸¥Ì™±½½É•¥¸A%a1L°İ¡¥ ¥Ìİ¡äÑ¡”‰…¹¥Ì¹½ÜÍ½±Ù•……¥¹ÍĞÑ¡”(€€€€Ù¥•İÁ½ÉĞ¸¨¨5%9}M%1!=UQQ}A`€ô€Ä¸Á€èÑ¡”É½İ¸½…ÀÑ•É´µ…äÕĞ„‰•…É¥¹œÑ¼½¹”Á¥á•°(€€€€…¹¹¼™ÕÉÑ¡•È°…¹İ¡•É”Ñ¡”É…ÜÉ½İ¸¥Ì¥ÑÍ•±˜ÍÕˆµÁ¥á•°¥Ğ¥ÌÍÕÁÁÉ•ÍÍ•½ÕÑÉ¥¡Ğ(€€€€€¡­±½½É€É•…¡•Ì€Ä¤¸™±½½È½¸Ñ¡”IMU1PÉ…Ñ¡•ÈÑ¡…¸„…À½¸­€‰¥¹‘Ì½¹±äİ¡•É”(€€€€Á¥á•±Ì…É”Í…É”ƒŠP„€ĞÀÀ´ÑÉ••±¥¹”¥Ì€ĞÀÁàÑ…±°…¹­••ÁÌ¥ÑÌ…ÁÌÑ¼Ñ¡”±…ÍĞÁ•È(€€€€•¹Ğ¸µ…¥¸¹©Í€Á…ÍÍ•ÌÁ¥á•±ÍA•ÉI…‘¥…¹€™É½´Ñ¡”±¥Ù”É•¹‘•É•ÈÍ¥é”…¹…µ•É„™¥•±°Í¼(€€€€„Á¡½¹”€ ĞÜÔÁà½É……Ğ¥ÑÌ€äÓ
À±…µÀ¤…¹„‘•Í­Ñ½À€ àÌÌÁà½É……Ğ€Ô×
À¤•ĞÑ¡•¥È½İ¸(€€€€…¹Íİ•È¥¹ÍÑ•…½˜½¹”¡…Éµ½‘•™¥•±ì„Ù¥•İÁ½ÉĞ¡…¹”É”µÍ½±Ù•ÌÑ¡”‰…¹•á…Ñ±ä…Ì(€€€€İ…±­¥¹œ‘½•Ì¸(€€€´€¨©5•…ÍÕÉ•…ĞÑ¡”ÍÁ…İ¸ÍÑ…Ñ¥½¸°İ¥Ñ Ñ¡”™±½½ÈÉ•µ½Ù•…¹Ñ¡•¸¥¸Á±…”¸¨¨€ÈàÄ½˜€äÀÀ(€€€€‰•…É¥¹Ì…ÉÉä„‰½‘ä¸]¥Ñ¡½ÕĞÑ¡”™±½½ÈÑ¡”µ½‘Õ±…Ñ¥½¸‘É•Ü€¨¨ÈÔÄ½˜€ÈàÀ¨¨É•Í½±Ù…‰±”(€€€€‰•…É¥¹Ì…Ğ„Á¥á•°½Èµ½É”½¸Ñ¡”Á¡½¹”…¹€¨¨ÈØÜ½˜€ÈàÄ¨¨½¸Ñ¡”‘•Í­Ñ½À°İ½ÉÍĞ(€€€€Í¥±¡½Õ•ÑÑ”€¨¨À¸ÄàÁà¨¨…¹€¨¨À¸ÌÄÁà¨¨¸]¥Ñ ¥Ğ°€¨¨ÈàÀ¼ÈàÀ…¹€ÈàÄ¼ÈàÄ¨¨°İ½ÉÍĞ(€€€€€¨¨Ä¸ÀÀÁà¨¨°…¹Ñ¡”¡½É¥é½¸‰…¹ÌÑÉ¥…¹±”½Õ¹Ğ¥ÌÕ¹¡…¹•…Ğ€ÔØÈƒŠPÑ¡”™±½½Èµ½Ù•Ì(€€€€Ù•ÉÑ¥•Ì°¹•Ù•ÈÑ¡•¥È¹Õµ‰•È¸(€€€´€¨©Q¡”…Ñ”¥Ì•Ù•ÉäÉ•Í½±Ù…‰±”‰•…É¥¹œ°¹½Ğ„Á•É•¹Ñ…”¨¨°‰•…ÕÍ”€äÀ€”İ½Õ±¡…Ù”Á…ÍÍ•(€€€€Ñ¡”‘•Í­Ñ½À¡…±˜½˜Ñ¡”‘•™•Ğ€ ÈØÜ¼ÈàÄ¥Ì€äÔ€”¤¸%Ğ…ÉÉ¥•Ì‰½Ñ …¹Ñ¤µÙ…Õ¥ÑäÕ…É‘ÌƒŠP„(€€€€Í½±Ù•ÈÑ¡…ĞÍÑ½ÁÁ•ÁÕÑÑ¥¹œÑ¥µ‰•ÈÕÀİ½Õ±½Ñ¡•Éİ¥Í”É•Á½ÉĞ„Á•É™•Ğ™É…Ñ¥½¸½˜¹½Ñ¡¥¹œ(€€€€ƒŠP…¹„Ñ¡¥É…ÍÍ•ÉÑ¥½¸Ñ¡…ĞÑ¡”‰…¹İ…ÌÍ½±Ù•……¥¹ÍĞQ!%LÙ¥•İÁ½ÉĞ°Í¥¹”„™±½½È(€€€€µ•…ÍÕÉ•¥¸Á¥á•±Ì¥Ìµ•…¹¥¹±•ÍÌ……¥¹ÍĞ„¡…Éµ½‘•™¥•±¸(Ø¸€¨©±½Í”Ñ¡”¹•…È™¥•±İ¥Ñ É½½Ñ••½µ•ÑÉä¸¨¨•Ñ…¥°µ™É•”…É•„€ ×\Ô±Õµ¥¹…¹”Í¥µ„€ğ(€€€È¼ÈÔÔ°‰•±½Üµ¡½É¥é½¸°É•Í…µÁ±•Ñ¼€ÄÈàÀİ¥‘”¤İ…Ì€¨¨ÄÌ¸Ü€”¨¨¥¸Ñ¡”¹•…É•ÍĞÅÕ…ÉÑ•È……¥¹ÍĞ(€€É•™•É•¹•Ì…Ğ€À¸ÏŠLÄ¸Ô€”ìÉ”µµ•…ÍÕÉ”¥Ğ…™Ñ•ÈÑ¡”½¹”µÍÕÉ™…”½ÉÉ•Ñ¥½¸¸‘„€¨©‰É½…µ±•…˜¨¨(€€•±•µ•¹ĞƒŠP¥¸‰½Ñ É•™•É•¹•ÌÑ¡”Ù¥ÍÕ…°µ…ÍÌ…Ğ•Ù•Éä‘¥ÍÑ…¹”¥Ì‘¥½Ğ±•…˜°¹½ĞÉ…ÍÌ(€€‰±…‘”ƒŠP…¹‘••Á•¸Ñ¡”Í¡…‘”İ¥Ñ¡½ÕĞ‘¥µµ¥¹œÑ¡”™±•­Ì¸Ù•Éä¹•Ü¥¹ÍÑ…¹”µÕÍĞ‰•¥¸½¸(€€Ñ•ÉÉ…¥¸¹ÍÕÉ™…•!•¥¡Ğ ¥€É…Ñ¡•ÈÑ¡…¸‰½ÉÉ½İ¥¹œÙ¥ÍÕ…°±½ÍÕÉ”™É½´…¸•±•Ù…Ñ•Í¡••Ğ¸(Ü¸€¨©±½İ•È±½…°……¥¹ÍĞÑ¡”½ÉÉ•Ñ•‰…È¸¨¨ùù]¡½±”µÍİ…É¡É½µ„™±½İ•È€¨¨Ä¸Ğä€”ƒŠH€ÓŠLØ€”¨¨(€€€ ©¹½Ğ¨€ÄÌ¸àä€”¤ƒ
Ü¹•…É•ÍĞÅÕ…ÉÑ•È€¨¨À¸ÀÜ€”ƒŠH€Ì¸À€”¨¨°İ¡¥ €©¥Ì¨É¥¡ĞƒŠP¥Ğ¥Ìİ¡…Ğ„(€€¹•Ù•ÈµÁ±½İ•É•µ¹…¹ĞÍ¡½İÌ…Ğ„µ…Ñ¡•±½½¬µ…¹±”¹ùø€¨©YId1=]H%UI%8Q!%L%Q4%L(€€]%Q!I]8°€ÈÀÈØ´Àà´ÄÔ‰äHµ\ÑŒ¡ˆÄ¤¸¨¨Q¡•É”¥Ì¹¼€ÓŠLØ€”‰…Èè¹¼É•µ¹…¹ĞÁ¡½Ñ½É…Á ¥Ì(€€½µµ¥ÑÑ•°€ÄÈ¸äÄ€”‘½•Ì¹½ĞÉ•ÁÉ½‘Õ”½¸Ñ¡”Á±…¹Ñ¥¹œÑ¡…Ğ¥Ì°…¹Ñ¡”É•¥Á”…±°™½ÕÈ¹Õµ‰•ÉÌ(€€İ•É”É•…İ¥Ñ ¡…ÌÉ•…±°€À¸ÀÔÔ¸I•…Hµ\ÑŒ¡ˆÄ¤Ì‰½à‰•™½É”É•ÍÑ…Ñ¥¹œ…¹ä½˜Ñ¡•´¸(€€½±½ÕÈÙ…É¥•Ñäè•™™8µ…™Ñ•Èµµ•‘¥…¸…Ğ•ÅÕ…°8(€€€¨¨ÄĞĞƒŠHƒŠ&”€ÌÀÀ¨¨°É••¸¡Õ”%EH€¨¨Ô¸Û
ÀƒŠHƒŠ&”€à¸×
À¨¨°É••¸¡É½µ„ÀÈÔ€¨¨ÌÈ¸ÌƒŠHƒŠ&€ÈØ¨¨€¡İ¡…Ğ¥Ì(€€µ¥ÍÍ¥¹œ¥ÌÑ¡”É•äµÉ••¸…¹±…Õ½ÕÌ™½±¥…”°¹½ĞÑ¡”Í…ÑÕÉ…Ñ•™±½İ•ÉÌ¤¸(à¸€¨©¥àÑ¡”Í¡½ĞÍ•Ğ‰•™½É”ÑÉÕÍÑ¥¹œ…¹ä½˜Ñ¡”…‰½Ù”¸¨¨ÁÉ…¥É¥•}Í½ÕÑ¡€Í¥ÑÌ¥¹Í¥‘”Ñ¡”(€€…±±•ÉäÑ¥µ‰•È€ ÈÌ¸Ğ€”½Á•¸Í­ä¤°Í¼Ñ¡•É”¥Ì•á…Ñ±ä½¹”½Á•¸µÁÉ…¥É¥”Ù¥•Ü…¹(€€ÁÉ…¥É¥•}İ•ÍÑ€¡…Ì‰••¸ÑÕ¹•……¥¹ÍĞ¥ÑÍ•±˜İ¥Ñ ¹¼½¹ÑÉ½°¸5½Ù”¥Ğ°…¹…‘„Í¡½Ğ(€€ÍÑ…¹‘¥¹œ¥¸€¨©èÀÈµ•Í¥ŒÁÉ…¥É¥”¨¨ƒŠPÑ¡”…µ•É„…ĞÁÉ…¥É¥•}İ•ÍÑ€ÍÑ…¹‘Ì€Ô´‰•±½ÜÑ¡”èÀÈ(€€•±•Ù…Ñ¥½¸Ñ¡É•Í¡½±°İ¡¥ ¥Ìİ¡äİ¥±‰•É…µ½Ğ°å•±±½Ü½¹•™±½İ•È°É…ÑÑ±•Í¹…­”µ…ÍÑ•È…¹(€€Á…±”ÁÕÉÁ±”½¹•™±½İ•ÈÉ•¹‘•Èé•É¼Á¥á•±Ì¥¸•Ù•Éä™É…µ”¸Q¡…ĞÑ¡É•Í¡½±¥Ì…‘µ¥ÑÑ•‘±ä½ÕÉÌ(€€€¡Ñ¡”é½¹”Ì½İ¸¹½Ñ”è€‰„É•…‘¥¹œ½˜Ñ¡”Ñ•ÉÉ…¥¸°¹½Ğ•Ù¥‘•¹”ˆ¤¸€¨©¼¹½Ğµ½Ù”ÍÁ•¥•Ì(€€‰•Ñİ••¸é½¹•ÌÑ¼Í…Ñ¥Í™ä„…µ•É„¸¨¨(ä¸€¨©É¥Ù•É}‰…¹­€¥Ì¹½Ğ¡½¹½ÕÉ¥¹œ¥ÑÌ½İ¸‘…Ñ…Í•Ğ¸¨¨i½¹”€ÄÍÁ•¥™¥•Ì½É‘É…ÍÌ…Ğ€Ä¸ËŠLÈ¸À´(€€…¹€ĞÃŠLÔÔ€”½Ù•Èİ¥Ñ ‰…É•}Í½¥±}™É…Ñ¥½¸è€À¸Á€ìÑ¡”™É…µ”Í¡½İÌøÈÔ´ÍÁÉ¥Ì½¸‰…É”(€€Í½¥°¥¸¹•…ÈµÉ½İÌ¸Q¡”‘…Ñ„¥ÌÉ¥¡ĞìÑ¡”É•¹‘•É•È¥Ì¹½ĞÉ•…‘¥¹œ¥Ğ¸(€€€¨©Q¡”•¹•É…°¡…±˜¥Ì=9€ÈÀÈØ´Àà´ÄÌ¨¨ƒŠPÍ•”,Ìè•Ù•Éä½µµÕ¹¥Ñä¥Ì¹½ÜÁ±…¹Ñ•…Ğ¥ÑÌ½İ¸(€€É•½É‘•½Ù•È¹µ…ÑÉ¥á}™É…Ñ¥½¹€°İ¡¥ ¹½Ñ¡¥¹œ¡…É•…¸€¨©Q¡”¥Ñ•´Ì½İ¸É•…‘¥¹œ¥ÌİÉ½¹œ(€€¥¸Ñİ¼İ…åÌ°‰½Ñ µ•…ÍÕÉ•É…Ñ¡•ÈÑ¡…¸…ÉÕ•¸¨¨Q¡”‰…¹¬¥Ì¹½Ğé½¹”€Äèİ¥Ñ¡¥¸•¥¡Ğµ•ÑÉ•Ì(€€½˜İ…Ñ•ÈÑ¡”•áÑ•¹Ğ¥ÌÑ¡”µ…ÉÍ €¡èÀÑ€°ÁÉ¥½É¥Ñä€ÜÀ¤°…¹Ñ¡”Í¡½ĞÌÍİ…É¥Ì•¹Ñ¥É•±äèÀĞ(€€…¹èÄÀ¸¹Ñ¡”ÍÁÉ¥Ìİ•É”¹½Ğ„‘•¹Í¥ÑäÁÉ½‰±•´ƒŠP¹ÕÁ¡…É}…‘Ù•¹…€…¹¹åµÁ¡…•…}½‘½É…Ñ…€°(€€™±½…Ñ¥¹œµ±•…Ù•…ÅÕ…Ñ¥ÌÉ•½É‘•€À¸ÀÇŠLÀ¸ÄÀ´Ñ…±°°İ•É”€Ø¸Ô€”½˜Ñ¡”ÑÕ™ÑÌÁ±…¹Ñ•½¸Ñ¡…Ğ(€€‘Éä‰…¹¬°‰•…ÕÍ”É½±”è•µ•É•¹Ñ€İ…Ì…±°Ñ¡”É•¹‘•É•È½Õ±Í•”…¹¹½Ñ¡¥¹œ¥¸Ñ¡”(€€Ù½…‰Õ±…ÉäÍ…¥„±¥±ä™±½…ÑÌ¸€¨©=9€ÈÀÈØ´Àà´ÄÌ¨¨ƒŠPÑ¡”ÁÕ‰±¥Í¡•Ù½…‰Õ±…Éä…¥¹•(€€ÍÕ‰ÍÑÉ…Ñ•€…¹Ñ¡”Á±…•ÈÉ•…‘Ì¥ĞìÍ•”,Ì¸]¡…ĞÉ•µ…¥¹Ì½˜Ñ¡¥Ì¥Ñ•´¥ÌÑ¡”µ¥µ™¥•±(€€½Ù•É…”ÅÕ•ÍÑ¥½¸¥¸¥Ñ•µÌ€ÇŠLÜ°¹½ĞÑ¡”±¥±¥•Ì…¹¹½Ğé½¹”€Ä¸(ÄÀ¸€¨©‘…ÁÑ¥Ù”‰Õ‘•Ğ¸¨¨Q¡¥¸Ñ¡”Íİ…É…ÕÑ½µ…Ñ¥…±±äİ¡•¸µ•…ÍÕÉ•™É…µ”Ñ¥µ”•á••‘Ì„(€€€Ñ¡É•Í¡½±°Í¼„Í±½Ü‘•Ù¥”‘•É…‘•Ì¥¹ÍÑ•…½˜ÍÑÕÑÑ•É¥¹œ¸5½‰¥±”¥Ì„É•±•…Í”…Ñ”…¹(€€€Ñ¡”±½ÜµÍÁ•Œ™¥•±¥ÌÕÉÉ•¹Ñ±ä„™¥á•°¡…¹µÑÕ¹•É•‘ÕÑ¥½¸¸(ÄÄ¸€¨©]¥¹¸¨¨=¹”ÑÉ…Ù•±±¥¹œİ…Ù”…¹„ÕÍĞìÑ¡”É•™•É•¹•ÌÍ¡½Ü½µ‰¥¹œ…ĞÍ•Ù•É…°Í…±•Ì¸()•™•ÉÉ•°İ¥Ñ Ñ¡”É•…Í½¸è…¸€¨©Õ¹‘•ÉÍÑ½Éä‰•±½Ü€Ì´¨¨İ½Õ±™¥à„É•…°…¹µ•…ÍÕÉ•¥¹Ù•ÉÍ¥½¸(¡½ÕÈÑÉ••±¥¹”‰…Í”¥Ì€©‰É¥¡Ñ•È¨Ñ¡…¸¥ÑÌÉ½İ¹ÌƒŠP‰…Í”½É½İ¸€Ä¸àĞ……¥¹ÍĞÑ¡”Á¡½Ñ½É…Á Ì(À¸ÜĞ°İ½ÉÑ øØÀ0¤‰ÕĞ¥Ğ¥Ì¥¹Ù¥Í¥‰±”Õ¹Ñ¥°Ñ¡”É½İ¹ÌÍÑ½ÀÉ•…‘¥¹œ…Ì‰½Õ±‘•ÉÌ¸¥á¥¹œ¥Ğ)™¥ÉÍĞÁÕÑÌ„‘…É¬Í­¥ÉĞÕ¹‘•È„Á¥±”½˜Í±…Ñ”¸((ŒŒLÜƒŠPA½±¥Í ()A•É™½Éµ…¹”……¥¹ÍĞÑ¡”‰Õ‘•ÑÌ°±¥•¹Í•…µ‰¥•¹”…Õ‘¥¼°ÁÉ½Ù•¹…¹”µÁ½ÁÕÀU`°1%	IQ%L¹µ‘€)½µÁ±•Ñ•¹•ÍÌÁ…ÍÌ°µ½‰¥±”É•±•…Í”…Ñ”¸((¨©½¹”€ÈÀÈØ´Àà´ÄÄƒŠP¹…Ù¥…Ñ¥½¸Ñ¡…ĞÉ½İÌİ¥Ñ Ñ¡”‘…Ñ…Í•Ğ¸¨¨±¥Ù”½µÁ…ÍÌÍ¡½İÌÑ¡”)İ…±­•ÈÌÍ¥áÑ••¸µÁ½¥¹Ğ¡•…‘¥¹œ…¹¹Õµ•É¥Œ‰•…É¥¹œ¸¹½ÉÑ µÕÀ½Ù•ÉÙ¥•Ü‘É…İÌ±…¹…¹İ…Ñ•È)™É½´Ñ¡”±½…‘•¡•¥¡Ñ™¥•±°•Ù•ÉäÍÑÉÕÑÕÉ”™É½´¥ÑÌ½µÁ¥±•™½½ÑÁÉ¥¹Ğ°…¹Ñ¡”µ½Ù¥¹œÙ¥Í¥Ñ½È)µ…É­•È™É½´Ñ¡”İ…±­•ÈÍÑ…Ñ”ì‰½Ñ ½Ù•É±…åÌ…É”¥¹‘•Á•¹‘•¹Ñ±äÁ•ÉÍ¥ÍÑ•¹ĞÍ•ÑÑ¥¹Ì¸Q¡”½±)…¹¡½È‰ÕÑÑ½¹ÌÉ•µ…¥¸…Ì…ÕÑ¡½É•Ù¥•İÁ½¥¹ÑÌ°İ¡¥±”Ñ¡”Í•…É¡…‰±”©ÕµÀ¥¹‘•à¹½Ü•¹Õµ•É…Ñ•Ì)…±°€ÜØ±½…‘•ÍÑÉÕÑÕÉ•Ì…¹…±°™½ÕÈÙ•É¥™¥•ÍÑÉ••Ğµ½¹ÑÉ½°¥¹Ñ•ÉÍ•Ñ¥½¹Ì¸%¹Ñ•ÉÍ•Ñ¥½¹Ì…É”)½µÁ¥±•¥¹Ñ¼Í¥‘•…ÉÌ¼ñÍ•¹”ø½¥¹‘•à¹©Í½¹€™É½´ÍÑÉ••Ñ}½¹ÑÉ½°¹©Í½¹€…¹Ñ¡”‘…ÑÕ´°Í¼Ñ¡”)É•¹‘•É•ÈÍÑ¥±°½¹ÍÕµ•Ì‘•É¥Ù•Í•¹”‘…Ñ„…¹¹¼½¹ÑÉ½°½½É‘¥¹…Ñ”¥Ì½Á¥•¥¹Ñ¼Ñ¡”U$¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠP™É•”µ™±ä°…¹Ñ¡”Ñ½İ¸Í••¸İ¡½±”¸¨¨€€¡½ÈÑ¡”ƒŠZÈ¡¥À¤±¥™ÑÌÑ¡”Ù¥Í¥Ñ½È)½™˜Ñ¡”ÁÉ…¥É¥”ìMÁ…•€½E€…¹„Ñ½Õ Á…É¥Í”…¹‘•Í•¹ìÑ¡”™É½µ}…‰½Ù•€…¹¡½È…ÉÉ¥Ù•Ì)…±É•…‘ä¥¸Ñ¡”…¥È¸½Éİ…É™½±±½İÌÑ¡”±½½¬‘¥É•Ñ¥½¸…¹ÍÑÉ…™”ÍÑ…åÌ±•Ù•°ì¡½É¥é½¹Ñ…°ÍÁ••)Í…±•Ìİ¥Ñ …±Ñ¥ÑÕ‘”°…ÁÁ•°‰•…ÕÍ”…Ğ€ÌÀÀ´„İ…±­¥¹œÁ…”É•…‘Ì…Ì¹½Ğµ½Ù¥¹œ¸Q•ÉÉ…¥¸)É•µ…¥¹Ì„™±½½ÈƒŠPÑ¡”ÍÑ•ÀµÕÀÉÕ±”…¹Ñ¡”™½½ÑÁÉ¥¹Ğ…ÁÍÕ±”…É”‘•±¥‰•É…Ñ•±ä€©¹½Ğ¨…ÁÁ±¥•°)Í¥¹”Ñ¡•ä…É”•á…Ñ±äİ¡…Ğå½Ô…Í­•Ñ¼±•…Ù”¸1•…Ù¥¹œ™É•”µ™±äÍ¹…ÁÌÑ¼Ñ¡”É½Õ¹É…Ñ¡•È)Ñ¡…¸‘•Í•¹‘¥¹œèÑ¡”İ…±¬Á…Ñ ÌÉ½Õ¹µÍµ½½Ñ¡¥¹œ¥Ì•áÁ½¹•¹Ñ¥…°…Ğ€ÄĞ½Ì°İ¡¥ ™É½´€ÄÜÔ´¥Ì„(ÄÔÀ´½ÌÁ±Õµµ•Ğ™½±±½İ•‰ä„É…İ°¸()]½ÉÑ ­¹½İ¥¹œ™½Èİ¡½•Ù•ÈÑ…­•ÌÑ¡”¹•áĞÍ±¥”è€¨©Ñ¡”…•É¥…°Ù¥•Ü¥ÌÑ¡”µ½ÍĞ¡½¹•ÍĞÁ¥ÑÕÉ”½˜)¡½Ü±¥ÑÑ±”¥Ì‰Õ¥±Ğ¸¨¨M¥àÍÑÉÕÑÕÉ•Ì…É½ÍÌ„€ØĞÀ´‰½à°…¹Ñ¡”•‘”½˜Ñ¡”µ½‘•±±•É½Õ¹¥Ì)Ù¥Í¥‰±”™É½´…‰½ÕĞ€ÄÔÀ´ÕÀ¸Q¡…Ğ¥Ì0ÄÜİ½É­¥¹œ…Ì¥¹Ñ•¹‘•°¹½Ğ„‰ÕœÑ¼¡¥‘”ƒŠP‰ÕĞ¥Ğµ…­•Ì)LÔ€¡µ½É”ÍÑÉÕÑÕÉ•Ì¤Ñ¡”½‰Ù¥½ÕÌ¹•áĞÕ¹¥Ğ°…¹¥Ğ…ÉÕ•Ì™½È…¸•Ù•¹ÑÕ…°¡…é”½•áÑ•¹ĞÑÉ•…Ñµ•¹Ğ)É…Ñ¡•ÈÑ¡…¸„‰¥•ÈÍ­¥ÉĞ¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”±¥‰•ÉÑ¥•Ì…É”¥¸Ñ¡”İ…±­Ñ¡É½Õ ¸¨¨‘½Ì½1%	IQ%L¹µ‘€ÍÑ…åÌÑ¡”)…ÁÁ•¹µ½¹±äÍ½ÕÉ”½˜ÑÉÕÑ ìÑ½½±Ì½½µÁ¥±•}±¥‰•ÉÑ¥•Ì¹Áå€‘•É¥Ù•Ì‘…Ñ„½±¥‰•ÉÑ¥•Ì¹©Í½¹€°)¡•¬¹Í¡€É”µ‘•É¥Ù•Ì¥Ğ…¹™…¥±Ì½¸‘É¥™Ğ°…¹Ñ¡”Ù¥‘•¹”Á…¹•°±¥ÍÑÌ…±°•¥¡Ñ••¸İ¥Ñ )Ñ¡•¥ÈÉ•…Í½¹¥¹œ¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠP…¹…ÑÑ…¡•Ñ¼Ñ¡•¥È‰Õ¥±‘¥¹Ì¸¨¨Q¡”ÁÉ½Ù•¹…¹”Á½ÁÕÀÉ•…‘ÌÍÕ‰©•ÑÍ€)…¹Í¡½İÌÑ¡”±¥‰•ÉÑ¥•ÌÑ…­•¸İ¥Ñ Ñ¡”‰Õ¥±‘¥¹œ‰•¥¹œ¥¹ÍÁ•Ñ•°Õ¹‘•È€‰]¡…Ğİ”µ…‘”ÕÀ¡•É”ˆ°)‰•Ñİ••¸Ñ¡”…ÑÑÉ¥‰ÕÑ”Ñ…‰±”…¹Ñ¡”¥Ñ…Ñ¥½¹Ì¸A…¹•°…¹…ÉÍ¡…É”½¹”•¹ÑÉäÉ•¹‘•É•È(¡±¥‰•ÉÑå¹ÑÉå!Ñµ±€¤Í¼Ñ¡•ä…¹¹½Ğ‘É¥™ĞìÑ¡”Íµ½­”…ÍÍ•ÉÑÌÁ•Èµ‰Õ¥±‘¥¹œ™¥±Ñ•É¥¹œÉ…Ñ¡•ÈÑ¡…¸)„½Õ¹Ğ°İ¡¥ ¥ÌÑ¡”…ÍÍ•ÉÑ¥½¸„Á½ÁÕÀ‘ÕµÁ¥¹œ…±°•¥¡Ñ••¸İ½Õ±ÍÑ¥±°¡…Ù”Á…ÍÍ•¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”‘½Õµ•¹Ğ¥Ì¡•­•™½È…ÁÌ¸¨¨Q¡”¥¹Ù•ÉÍ”¡•¬ÉÕ¹Ì¥¸)Ù…±¥‘…Ñ”¹Áå€€¡¡•­}±¥‰•ÉÑ¥•Í}½Ù•É…•€¤…¹Ñ¡•É•™½É”¥¸¡•¬¹Í¡€è•Ù•ÉäÁ¡…Í”İ¡½Í”)™½½ÑÁÉ¥¹Ñ€½ÈÁ½Í¥Ñ¥½¹€¥Ì½¹©•ÑÕÉ…±€µÕÍĞ‰”¹…µ•‰ä„±¥‰•ÉÑäÑ¡…Ğ¥Ì€©…‰½ÕĞÑ¡…Ğ)…ÍÁ•Ğ¨°µ…Ñ¡•……¥¹ÍĞÑ¡”•¹ÑÉäÌ½İ¸ÁÉ½Í”¸9…µ¥¹œÑ¡”‰Õ¥±‘¥¹œ¥Ì‘•±¥‰•É…Ñ•±ä¹½Ğ)ÍÕ™™¥¥•¹Ğ°…¹Ñ¡”Í•±˜µÑ•ÍĞ…ÍÍ•ÉÑÌ•á…Ñ±äÑ¡…Ğ…Í”¸M¥à¥¹Ù•¹Ñ¥½¹Ì¥¸Ñ¡”½µµ¥ÑÑ•‘…Ñ„°)Í¥à½Ù•É•¸Q¡”Ù¥‘•¹”Á…¹•°ÍÑ…Ñ•ÌÑ¡”Õ…É…¹Ñ•”°‰•…ÕÍ”„ÁÉ½µ¥Í”„Ù¥Í¥Ñ½È…¹¹½ĞÉ•…)¥Ì¹½Ğ½¹”¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠP½Ù•É…”¥Ì¹½Ü…ÍÍ•ÉÑ•°¹½Ğ¥¹™•ÉÉ•¸¨¨¹ÑÉ¥•Ì…ÉÉä„€¨©½Ù•ÉÌè¨©€)™¥•±½˜ÍÑÉÕÑÕÉ•}¥‘l¹Á¡…Í•}¥‘t¹…ÍÁ•Ñ€Ñ½­•¹Ìì½µÁ¥±•}±¥‰•ÉÑ¥•Ì¹Áå€Á…ÉÍ•Ì¥Ğ°…¹)¡•­}±¥‰•ÉÑ¥•Í}½Ù•É…•€µ…Ñ¡•ÌÑ¡”±…¥µÌ……¥¹ÍĞÑ¡”É•½É‘Ì€¨©¥¸‰½Ñ ‘¥É•Ñ¥½¹Ì¨¨ƒŠP…¸)¥¹Ù•¹Ñ¥½¸İ¥Ñ ¹¼…‘µ¥ÍÍ¥½¸™…¥±Ì°…¹Í¼‘½•Ì…¸…‘µ¥ÍÍ¥½¸İ¡½Í”Ù…±Õ”¥Ì¹½Ğ½¹©•ÑÕÉ…°(¡•á•µÁĞÕ¹‘•È€¨©I•Í½±Ù•¨¨°Í¼•Ù¥‘•¹”¥Ì…±±½İ•Ñ¼…ÉÉ¥Ù”İ¥Ñ¡½ÕĞ‰É•…­¥¹œÑ¡”…Ñ”¤¸Q¡”)­•åİ½Éµ…Ñ ½Ù•ÈÁÉ½Í”¥Ì½¹”°…¹Ñ¡”Í•±˜µÑ•ÍĞÌ‘¥ÍÉ¥µ¥¹…Ñ¥¹œ…Í”¥Ì¹½Ü…¸•¹ÑÉäÑ¡…Ğ)Ñ…±­Ì…‰½ÕĞ™½½ÑÁÉ¥¹ÑÌ…¹Á±…•µ•¹Ğİ¡¥±”±…¥µ¥¹œ¹½Ñ¡¥¹œ¸]É¥Ñ¥¹œÑ¡”±…¥µÌ‘½İ¸¥µµ•‘¥…Ñ•±ä)™½Õ¹„‘É¥™ĞÑ¡”¡•ÕÉ¥ÍÑ¥Œİ…Ì¥¹‘¥™™•É•¹ĞÑ¼è0ÄÈ‘•ÍÉ¥‰•Ñ¡”]…±­•Èµ••Ñ¥¹œ¡½ÕÍ”Á½Í¥Ñ¥½¸)…Ì¥¹™•ÉÉ•‘€µ½¹Ñ¡Ì…™Ñ•ÈÑ¡”É•½Éİ…Ì‘½İ¹É…‘•Ñ¼½¹©•ÑÕÉ…±€¸Q¡”¡¥ÁÌ…É”¥¸Ñ¡”)Ù¥‘•¹”Á…¹•°…¹½¸Ñ¡”ÁÉ½Ù•¹…¹”…É°‰•…ÕÍ”„Õ…É…¹Ñ•”•¹™½É•½¹±ä¥¸Ñ¡”É•Á½Í¥Ñ½Éä)¥ÌÑ¡”™¥±•½¹™•ÍÍ¥½¸Ñ¡¥Ìİ¡½±”±¥¹”½˜İ½É¬•á¥ÍÑÌÑ¼ÍÑ½À‰•¥¹œ¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”ÉÕ±”¹½Ü½Ù•ÉÌİ¡…Ğ„‰Õ¥±‘¥¹œ€©¥Ì¨°¹½Ğ½¹±äİ¡•É”¥ĞÍÑ…¹‘Ì¸¨¨Q¡”)½Ù•ÉÌé€Ù½…‰Õ±…Éäİ…Ì™½½ÑÁÉ¥¹Ñ€½Á½Í¥Ñ¥½¹€ì¥Ğ¥Ì¹½Ü•Ù•Éä…ÑÑ•ÍÑ•Ù…±Õ”¥¸„É•½ÉƒŠP)Ñ¡½Í”Ñİ¼°‘½Õµ•¹Ñ•‘}É…¹•€°Ñ¡”ÍÑÉÕÑÕÉ”µ±•Ù•°™Õ¹Ñ¥½¹€…¹½ÕÁ…¹ÑÍ€°…¹™½É´¸ñ…ÑÑÈù€)™½È…¹åÑ¡¥¹œÕ¹‘•È„Á¡…Í”Ì™½É´°•¹Õµ•É…Ñ•™É½´Ñ¡”‘…Ñ„É…Ñ¡•ÈÑ¡…¸™É½´„±¥ÍĞÍ¼„¹•Ü)…É¡•ÑåÁ”…ÑÑÉ¥‰ÕÑ”¥Ì¥¹Í¥‘”Ñ¡”ÉÕ±”Ñ¡”‘…ä¥Ğ…ÁÁ•…ÉÌ¸Q¡”…ÉÕµ•¹Ğ¥ÌÑ¡…Ğ„½¹©•ÑÕÉ…°)É½½™}ÑåÁ•€¥Ì¹½Ğ…¸…‰Í•¹”¥¸Ñ¡”µ½‘•°è„…‰±”•ÑÌ‰Õ¥±Ğ…¹Ñ¡”Ù¥Í¥Ñ½ÈÍ••Ì„…‰±”°…¹)„½¹©•ÑÕÉ…°…±±•Éäè™…±Í•€¥ÌÑ¡”Í…µ”±…¥´¥¸Ñ¡”¹•…Ñ¥Ù”ƒŠP„Á±…¥¸™É½¹ĞÉ•¹‘•É•‰•…ÕÍ”)¹½‰½‘ä™½Õ¹•Ù¥‘•¹”•¥Ñ¡•Èİ…ä°İ¡¥ É•…‘Ì…ÌÑ¡”™¥¹‘¥¹œ¸½ÕÈ¥¹Ù•¹Ñ¥½¹Ìİ•É”½İ•…¸)…‘µ¥ÍÍ¥½¸…¹¡…¹½¹”èÑ¡”M…Õ…¹…Í Ì€ÄàÈä…‰¥¸¡•¥¡Ğ…¹É½½˜€¡0Äà¤…¹Ñ¡”É••¸QÉ•”Ì…¹)Ñ¡”]•ÍÑ•É¸Ì…±±•É¥•Ì€¡0Ää¤¸Q•¸½¹©•ÑÕÉ…°Ù…±Õ•Ì°Ñ•¸‘•±…É…Ñ¥½¹Ì¸Q¡”¡¥ÁÌÉ•……Ì)…ÑÑÉ¥‰ÕÑ•ÌƒŠP€‰M…Õ…¹…Í !½Ñ•°É½½˜ÑåÁ”ˆƒŠPİ¡¥±”Ñ¡”Ñ½­•¸Ñ¡”…Ñ”µ…Ñ¡•Ì­••ÁÌ¥ÑÌ™½É´¹€)ÁÉ•™¥à¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”¡…É¡…±˜è½µ¥ÍÍ¥½¹Ì…¹Í¥µÁ±¥™¥…Ñ¥½¹Ì…É”•¹™½É•¸¨¨Q¡”µ¥ÍÍ¥¹œ)±…¥´ÑÕÉ¹•½ÕĞÑ¼‰•±½¹œÑ¼Ñ¡”€©•¹•É…Ñ½È¨°¹½ĞÑ¼Ñ¡”É•½É½ÈÑ¡”‘½Õµ•¹Ğ¸… )•¹•É…Ñ½ÉÌ½…É¡•ÑåÁ•Ì¼©}Á…É…µÌ¹Áå€¹½Ü‘•±…É•Ì=9MU5€°Ñ¡”™½É´…ÑÑÉ¥‰ÕÑ•Ì¥ÑÌ™É½µ}Á¡…Í•€)…ÑÕ…±±äÉ•…‘Ì°…¹Ù…±¥‘…Ñ”¹Áå€¡½±‘Ì•Ù•Éä…ÑÑÉ¥‰ÕÑ”½ÕÑÍ¥‘”Ñ¡…ĞÍ•ĞÑ¼„•½µ•ÑÉäé€)‘•±…É…Ñ¥½¸½¸Ñ¡”É•½ÉƒŠP…‰Í•¹Ñ€€¡¹½Ñ¡¥¹œ½˜¥Ğ¥Ì‰Õ¥±Ğ¤°Í¥µÁ±¥™¥•‘€€¡„™¥á•‘•™…Õ±Ğ)ÍÑ…¹‘Ì¥¸¥ÑÌÁ±…”¤½ÈÉ•½É‘}½¹±å€€¡„É•©•Ñ•É•…‘¥¹œ°İ¡¥ ½İ•Ì¹½Ñ¡¥¹œ¤¸…‰Í•¹Ñ€…¹)Í¥µÁ±¥™¥•‘€¹••„½Ù•ÉÌé€Ñ½­•¸•á…Ñ±ä…Ì…¸¥¹Ù•¹Ñ¥½¸‘½•Ì°¡•­•‰½Ñ İ…åÌ°…¹Ñ¡”)Á½ÁÕÀµ…É­ÌÑ¡½Í”É½İÌ€©¹½Ğ‰Õ¥±Ğ¨€¼€©¹½Ğµ½‘•±±•™É½´Ñ¡¥Ì¨Í¼Ñ¡”…‘µ¥ÍÍ¥½¸É•…¡•Ì„Ù¥Í¥Ñ½È)…¹¹½Ğ½¹±ä„É•Ù¥•İ•È¸Qİ•¹Ñäµ½¹”…ÑÑÉ¥‰ÕÑ•Ì…É½ÍÌÍ¥à‰Õ¥±‘¥¹ÌÉ•… ¹¼Ù•ÉÑ•àì0ä…¹0ÄÀ)¹½Ü±…¥´Ñ¡•¥ÉÌ°…¹0ÈÃŠM0ÈÌ…É”¹•Ü¸()Mİ¥Ñ¡¥¹œ¥Ğ½¸™½Õ¹„É•…°‘•™•Ğ°İ¡¥ ¥ÌÑ¡”…ÉÕµ•¹Ğ™½ÈÑ¡”ÉÕ±”¥¸½¹”±¥¹”è€¨©Ñ¡”]½±˜)A½¥¹ĞQ…Ù•É¸Ì™É…µ”•áÑ•¹Í¥½¸…¹¥ÑÌÁ…¥¹Ñ•İ½±˜Í¥¸…É”‰½Ñ ‘½Õµ•¹Ñ•‘€…¹¹•¥Ñ¡•È¥Ì)µ½‘•±±•¸¨¨Q¡”É•½ÉÍÁ•±±ÌÑ¡•´™É…µ•}•áÑ•¹Í¥½¹€…¹Í¥¹…•€ì±½}‘İ•±±¥¹€É•…‘Ì)™É…µ•}…‘‘¥Ñ¥½¹€…¹Í¥¹€ìÑ¡”…‰Í•¹Ğ…ÑÑÉ¥‰ÕÑ•ÌÉ•Í½±Ù•Ñ¼‘•™…Õ±ÑÌ…¹¹½Ñ¡¥¹œ½µÁ±…¥¹•¸)	½Ñ İ•É”™¥á•Ñ¡”Í…µ”‘…ä°¥¸½¹”Í±¥”İ¥Ñ Ñ¡”É”µ‰…­”ƒŠPÍ•”LÔ¸Q¡”ÍÑ…¹‘¥¹œ±¥µ¥Ğ¥Ì)Õ¹¡…¹•…¹İ½ÉÑ É•Á•…Ñ¥¹œè¹½Ñ¡¥¹œ…¸…Ñ „±¥‰•ÉÑäÑ…­•¸Ñ¡…Ğ¹½‰½‘ä¹½Ñ¥•Ñ…­¥¹œƒŠP‰ÕĞ)…¸…ÑÑÉ¥‰ÕÑ”É•½É‘•…¹¹•Ù•È‰Õ¥±Ğ¥Ì¹¼±½¹•È¥¸Ñ¡…Ğ…Ñ•½Éä¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠP…¹Ñ¡”‘•™•Ğ¥Ğ™½Õ¹¥ÌÉ•Á…¥É•èÑ¡”İ½±˜Í¥¸¡…¹Ì¸¨¨Q¡”ÉÕ±”Ìİ¡½±”)…ÉÕµ•¹Ğİ…Ì½¹”‰Õ¥±‘¥¹œ°Í¼¡•É”¥ÌÑ¡…Ğ‰Õ¥±‘¥¹œ™¥¹¥Í¡•¸Q¡”É•½ÉÌ™É…µ•}•áÑ•¹Í¥½¹€…¹)Í¥¹…•€…É”¹½Ü™É…µ•}…‘‘¥Ñ¥½¹€…¹Í¥¹€°Ñ¡”¹…µ•Ì±½}‘İ•±±¥¹€É•…‘ÌìÑ¡”™É…µ”‰…ä…¹)Ñ¡”Í¥¹‰½…É…É”‰…­•°ÁÕ‰±¥Í¡•…¹Ù¥Í¥‰±”ì…¹Ñ¡”Á½ÁÕÀÌ‘½Õµ•¹Ñ•‘€¡¥ÁÌ½Ù•È‰½Ñ ¹½Ü)‘•ÍÉ¥‰”Í½µ•Ñ¡¥¹œ„Ù¥Í¥Ñ½È…¸İ…±¬ÕÀÑ¼¸Q¡”É•¹…µ”…±½¹”İ½Õ±¡…Ù”‰••¸Ñ¡”Íµ…±±•È¡…±˜½˜)Ñ¡”™¥à¸™É…µ”…‘‘¥Ñ¥½¸İ¥Ñ ¹¼‘¥µ•¹Í¥½¹ÌÉ•½É‘•Ñ…­•ÌÑ¡”…É¡•ÑåÁ”Ì‘•™…Õ±ÑÌƒŠP„Ñİ¼µÍÑ½É•ä)‰±½¬…É½ÍÌÑ¡”É¥Ù•È™É½¹Ğ°½¸„Ñ…Ù•É¸Ñ¡”Í½ÕÉ•Ì‘•ÍÉ¥‰”…Ì±½ÜƒŠPÍ¼Ñ¡”É•½ÉÍÑ…Ñ•ÌÑ¡”)‰…äÌÍ¥‘”°İ¥‘Ñ °‘•ÁÑ …¹ÍÑ½É•ä½Õ¹Ğ°…¹0ÈĞ…‘µ¥ÑÌÑ¡”Ñ¡É•”½˜Ñ¡½Í”Ñ¡…Ğ…É”¥¹Ù•¹Ñ•¸)Q¡”‰½…É¥Ì‘•±¥‰•É…Ñ•±ä‰±…¹¬èÑ¡”Í¥¸¥Ì‘½Õµ•¹Ñ•…¹Ñ¡”Á…¥¹Ñ¥¹œ½¸¥Ğ¥Ì¹½Ğ€¡0ÈÔ¤¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPİ¡…Ğ¥Ì¹½Ğ¡•É”°…¹Ñ¡”™¥±”Ñ¡…ĞÍ…¥Í¼É•…¡¥¹œ„Ù¥Í¥Ñ½È¸¨¨Ù•Éä)…Ñ”…‰½Ù”…Í­Ìİ¡•Ñ¡•Èİ¡…Ğİ”€©‰Õ¥±Ğ¨¥Ì¡½¹•ÍĞ¸9½¹”½˜Ñ¡•´½Õ±É•… Ñ¡”ÍÑÉÕÑÕÉ•Ì)Ñ¡¥ÌÁÉ½©•ĞÉ•Í•…É¡•…¹‘•±¥‰•É…Ñ•±ä‘¥¹½Ğ‰Õ¥±è‘…Ñ„½•á±ÕÍ¥½¹Ì¹©Í½¹€¡…Ì¡•±)™½ÕÉÑ••¸½˜Ñ¡•´°İ¥Ñ Ñ¡”•Ù¥‘•¹”Ñ¡…Ğ‘…Ñ•Ì•… ½¹”°Í¥¹”Ñ¡”Í…™™½±ƒŠP…¹¥ĞÍ¡¥ÁÁ•)¹½İ¡•É”„Ù¥Í¥Ñ½È½Õ±É•…¥Ğ¸Q¡”Ù¥‘•¹”Á…¹•°¹½Ü…ÉÉ¥•ÌÑ¡•´Õ¹‘•È€¨©]¡…Ğ¥Ì¹½Ğ)¡•É”¨¨°‘•É¥Ù•Á•ÈÍ•¹”‰ä½µÁ¥±•}Í•¹”¹Áå€İ¥Ñ ¥Ñ…Ñ¥½¹Ì©½¥¹•°¥¸Ñ¡”Í…µ”•¹ÑÉäÑ¡”)±¥‰•ÉÑ¥•ÌÕÍ”¸Q¡”Á…¹•°ÍÑ…Ñ•Ì°…¹Ñ¡”Íµ½­”…ÍÍ•ÉÑÌ°Ñ¡…ĞÑ¡¥Ì¥Ì€¨©¹½Ğ¨¨„±¥ÍĞ½˜)•Ù•ÉåÑ¡¥¹œµ¥ÍÍ¥¹œè•¥¡Ğ½˜É½Õ¡±ä™½ÉÑäÉ•Í•…É¡•ÍÑÉÕÑÕÉ•ÌÍÑ…¹°…¹Ñ¡”…•É¥…°Ù¥•Ü)É•µ…¥¹ÌÑ¡”¡½¹•ÍĞÁ¥ÑÕÉ”½˜Ñ¡”É•ÍĞ¸()Mİ¥Ñ¡¥¹œ¥Ğ½¸™½Õ¹Ñ¡”½¹”™¥±”İ¡•É”ÉÕ±”€Äİ…Ì¹•Ù•È•¹™½É•¸Ù•ÉäÍ½ÕÉ•}¥‘€¥¸Ñ¡¥Ì)ÁÉ½©•ĞµÕÍĞÉ•Í½±Ù”¥¸‘…Ñ„½Í½ÕÉ•Ì½€ì¹½Ñ¡¥¹œÉ•…Ñ¡”•á±ÕÍ¥½¹Ì™¥±”Ì°Í¼„¥Ñ…Ñ¥½¸)Ñ¡•É”½Õ±¡…Ù”¹…µ•„Í½ÕÉ”Ñ¡…Ğ¹•Ù•È•á¥ÍÑ•¸¡•­}•á±ÕÍ¥½¹Í€¹½ÜÉ•ÅÕ¥É•Ì„Í±Õœ¥°)„¹…µ”°„ÍÑ…Ñ•É•…Í½¸…¹„¥Ñ…Ñ¥½¸Ñ¡…ĞÉ•Í½±Ù•ÌƒŠPÑ¡”½µµ¥ÑÑ•™¥±”Á…ÍÍ•ÌÕ¹¡…¹•°)…¹Ñ¡”¹•áĞ•¹ÑÉä…¹¹½ĞÍ­¥À¥Ğ¸Q¡”‘…Ñ”…Ñ”…±Í¼ÉÕ¹Ì‰…­İ…É‘Ì¹½Üè…¸•¹ÑÉä‘…Ñ¥¹œ„)‰Õ¥±‘¥¹œÑ¼€ÄàÌÜ¥Ì„½ÉÉ•Ğ•á±ÕÍ¥½¸™É½´€ÄàÌÔ…¹„İÉ½¹œ½¹”™É½´€ÄàÌÜ°İ¡¥ ¹¼)½µÁ…É¥Í½¸……¥¹ÍĞÑ¡”É•½É‘Ì…¸…Ñ °‰•…ÕÍ”…¸•á±Õ‘•ÍÑÉÕÑÕÉ”¡…Ì¹¼É•½É¸()¹Ñ¡”Í¥‘•…ÉÌ…É”É”µ‘•É¥Ù•½¸•Ù•Éä½µµ¥Ğ€¡½µÁ¥±•}Í•¹”¹Áä€´µ…±°€´µ¡•­€°¥¸)¡•¬¹Í¡€¤¸Q¡•ä…É”½µµ¥ÑÑ•Í¼Ñ¡”Í¥Ñ”¹••‘Ì¹¼‰Õ¥±ÍÑ•À°İ¡¥ ½¹±ä­••ÁÌÑ¡”)İ…±­Ñ¡É½Õ …¹Ñ¡”…É¡¥Ù”Ñ½•Ñ¡•È¥˜„É•½É•‘¥Ñ•İ¥Ñ¡½ÕĞ„É•½µÁ¥±”¥Ì„…Ñ”™…¥±ÕÉ”)É…Ñ¡•ÈÑ¡…¸„‘¥Í½Ù•Éä½¸Ñ¡”‘•Á±½å•Í¥Ñ”¸±°•¥¡Ğİ•É”‰åÑ”µ¥‘•¹Ñ¥…°½¸Ñ¡”™¥ÉÍĞÉÕ¸¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”Ñ¡¥É…Ñ•½Éä°…¹Ñ¡”ÁÉ½µ¥Í”¥¹Í¥‘”¥Ğ¸¨¨Q¡”•¹ÑÉä…‰½Ù”•¹‘Ì‰ä)Í…å¥¹œÑ¡”İ…Ñ ±¥ÍĞ¥Ì‘•±¥‰•É…Ñ•±ä¹½ĞÍ¡½İ¸…¹Ñ¡…Ğ¥ÑÌÕ¹•ÉÑ…¥¹Ñä‰•±½¹Ì½¸Ñ¡”É•½É‘Ì)…¹¥¸Ñ¡”Á½ÁÕÀ¸Q¡…Ğİ…ÌÉ¥¡Ğ…‰½ÕĞÑ¡”½¹”½˜Ñ¡”™½ÕÈÑ¡…Ğ¥ÌMQ9%9…¹İÉ½¹œ…‰½ÕĞÑ¡”)Ñ¡É•”Ñ¡…Ğ…É”¹½Ğè…¸•µÁÑä±½Ğ…¹¹½ĞÍ…ä€©É•Í•…É¡•°…¹ÍÑ¥±°½Á•¸¨…¹äµ½É”Ñ¡…¸¥Ğ½Õ±)Í…ä€©É•Í•…É¡•…¹ÉÕ±•½ÕĞ¨¸Q¡”™½ÕÈ…É”ÍÑÉÕÑÕÉ•‘…Ñ„¹½ÜƒŠPİ¡…Ğ¥Ì½Á•¸°İ¡…ĞÍ•ÑÑ±¥¹œ¥Ğ)İ½Õ±¡…¹”°„‘½ÍÍ¥•ÈÁ½¥¹Ñ•ÈÑ¡…ĞµÕÍĞÉ•Í½±Ù”Ñ¼„½µµ¥ÑÑ•™¥±”…¹Ñ¼„±¥¹”¥¹Í¥‘”¥Ğ°)…¹¥Ñ…Ñ¥½¹ÌÑ¡…ĞÉ•Í½±Ù”½È„Í•¹Ñ•¹”Í…å¥¹œİ¡äÑ¡•É”…É”¹½¹”ƒŠP…¹Ñ¡•äÉ•¹‘•ÈÕ¹‘•È€¨©]¡…Ğ)¥ÌÍÑ¥±°…¸½Á•¸ÅÕ•ÍÑ¥½¸¨¨°İ¥Ñ Ñ¡”ÍÑ…¹‘¥¹œ½¹”¡¥ÁÁ•€©ÍÑ…¹‘¥¹œ¡•É”¨É…Ñ¡•ÈÑ¡…¸±¥ÍÑ•)…µ½¹œ…‰Í•¹•Ì¸¡•­}İ…Ñ¡}±¥ÍÑ€•¹™½É•ÌÑ¡”™¥±”Ì½İ¸Í•¹Ñ•¹”°İ¡¥ ¡…¹•Ù•È‰••¸)•¹™½É•è…¸•¹ÑÉä¹…µ¥¹œ„½µµ¥ÑÑ•É•½ÉµÕÍĞ¹…µ”Ñ¡”±…¥´…ÉÉå¥¹œÑ¡”‘½Õ‰Ğ°…¹Ñ¡…Ğ)±…¥´µ…ä¹½Ğ‰”‘½Õµ•¹Ñ•‘€°Í¼Ñ¡”‘…äÑ¡”•Ù¥‘•¹”…ÉÉ¥Ù•ÌÑ¡”…Ñ”™…¥±Ì¥¹ÍÑ•…½˜Ñ¡”±¥ÍĞ)ÅÕ¥•Ñ±ä½¥¹œ½ÕĞ½˜‘…Ñ”¸9½Ñ¡¥¹œ¥¸Ñ¡”½µµ¥ÑÑ•™½ÕÈİ…ÌİÉ½¹œƒŠPÑ¡”Ù…±Õ”¥ÌÑ¡”¹•áĞ•¹ÑÉä+ŠP…¹Ñ¡”¹•…Èµ¥ÍÌ¥Ğ‘¥ÍÕÉ™…”¥Ìİ•ÍÑ•É¹}¡½Ñ•±€°İ¡½Í”±¥¹”ÍÑ¥±°É•……ÌÑ¡½Õ ¥ÑÌ)‰Õ¥±µ‘…Ñ”ÅÕ•ÍÑ¥½¸İ•É”½Á•¸„‘…ä…™Ñ•ÈÑ¡”É•½ÉÍ•ÑÑ±•¥Ğ¸M•”MQQULƒ
œ€ÌÜ¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”…É…¹Íİ•ÉÌ€‰İ…Ì¥Ğ¡•É”üˆ°İ¡¥ ¥Ğ¹•Ù•È¡…¸¨¨Ù•Éä…Ñ”…¹•Ù•Éä)Á…¹•°…‰½Ù”…Í­Ì¡½ÜÍÕÉ”İ”…É”½˜Í½µ•Ñ¡¥¹œİ”‰Õ¥±Ğ¸9½¹”½˜Ñ¡•´İ…Ì…Í­¥¹œÑ¡”ÅÕ•ÍÑ¥½¸„)Ù¥Í¥Ñ½È…Í­Ì™¥ÉÍĞ°…¹Ñ¡”…É½Õ±¹½Ğ…¹Íİ•È¥ĞèÁ½ÁÕÀ¹©Í€¡…ÌÉ•…)Í¥‘•…È¹‘½Õµ•¹Ñ•‘}É…¹•€Í¥¹”Ñ¡”…Éİ…ÌİÉ¥ÑÑ•¸…¹½µÁ¥±•}Í•¹”¹Áå€¹•Ù•È•µ¥ÑÑ•Ñ¡”)™¥•±°Í¼Ñ¡”±¥¹”É•¹‘•É•…Ì¹½Ñ¡¥¹œ½¸•Ù•Éä‰Õ¥±‘¥¹œ™½ÈÑ¡”±¥™”½˜Ñ¡”ÁÉ½©•Ğ¸Q¡”Á¡…Í”Ì)±…¥´…‰½ÕĞ¥ÑÍ•±˜¹½ÜÑÉ…Ù•±ÌÑ¼Ñ¡”…É¥¸Ñ¡”…ÑÑÉ¥‰ÕÑ”Í¡…Á”ƒŠPÑ¡”‘…Ñ•ÍÁ…¸İ¥Ñ ¥ÑÌ)½¹™¥‘•¹”°Í½ÕÉ•Ì…¹É•…Í½¹¥¹œìÑ¡”Á¡…Í”Ì¡…¹•}¹½Ñ•€¥¸Ñ¡”É•½ÉÌ½İ¸İ½É‘Ìì…¹Ñ¡”)Á½Í¥Ñ¥½¸Ì…ÉÕµ•¹Ğ‰•¡¥¹„İ¡å€½¸Ñ¡”±¥¹”Ñ¡…Ğ…±É•…‘äÍ¡½İ•¥ÑÌ¡¥À¸…Ñ•ÌÁÉ¥¹Ğ…Ì)É•½É‘•°‰•…ÕÍ”Í•Ù•¸½˜Ñ¡”•¥¡ĞÍÁ…¹Ì•¹½¸€ÌÄ••µ‰•È½˜„å•…È…¹Ñ¡…Ğ¥Ì„‰½Õ¹°¹½Ğ)„‘…ä…¹å‰½‘äİÉ½Ñ”‘½İ¸¸()Q¡”™…¥±ÕÉ”±…ÍÌ¥Ìİ½ÉÑ …ÉÉå¥¹œÉ…Ñ¡•ÈÑ¡…¸Ñ¡”™¥àè€¨©Ñİ¼¡…±Ù•Ì•… ½ÉÉ•Ğ…‰½ÕĞÑ¡•¥È)½İ¸Í¥‘”½˜…¸¥¹Ñ•É™…”¹•¥Ñ¡•ÈÍÑ…Ñ•Ì¨¨¸Q¡”½µÁ¥±•Èİ…Ì½¹Í¥ÍÑ•¹Ğİ¥Ñ ¥ÑÍ•±˜°İ¡¥ ¥Ì…±°)€´µ¡•­€ÁÉ½Ù•ÌìÑ¡”É•½ÉÙ…±¥‘…Ñ•±•…¸ìÑ¡”µ…É­ÕÀİ…ÌÉ¥¡Ğ¸M¼Ñ¡”Ñ•ÍĞ½Á•¹ÌÑ¡”…ÑÕ…°)…É…¹É•…‘Ìİ¡…Ğ„Ù¥Í¥Ñ½Èİ½Õ±Í•”°…¹…ÍÍ•ÉÑÌÑ¡”‘¥ÍÉ¥µ¥¹…Ñ¥¹œÁ…¥ÈƒŠPÑ¡”M…Õ…¹…Í )‘½Õµ•¹Ñ•‘€°!½…¸ÌÍÑ½É”¥¹™•ÉÉ•‘€ƒŠP‰•…ÕÍ”„…ÉÍÑ…µÁ¥¹œ½¹”É…‘”½¸…±°•¥¡Ğİ½Õ±)¡…Ù”Á…ÍÍ•…¹ä¡•¬™½È€‰Ñ¡•É”¥Ì„¡¥Àˆ¸¹ä½Ñ¡•ÈÍ¥‘•…È™¥•±Ñ¡”É•¹‘•É•ÈÉ•…‘Ì¥Ì¥¸Ñ¡”)Í…µ”…Ñ•½ÉäìÑ•ÍÑ}Ñ¡•}…É‘}¥Í}™•‘}Ñ¡•}±…¥µÍ}¥Ñ}É•¹‘•ÉÍ€¥Ìİ¡•É”Ñ¡”¹•áĞ½¹”½•Ì¸)=¹”…Ñ”…µ”İ¥Ñ ¥Ğè„‘½Õµ•¹Ñ•‘€‘…Ñ”ÍÁ…¸¹½Ü½İ•Ì„É•Í½±Ù¥¹œÍ½ÕÉ”°±¥­”•Ù•Éä½Ñ¡•È)‘½Õµ•¹Ñ•‘€Ù…±Õ”¸MÑ¥±°¹½Ğ½¸Ñ¡”…ÉèÑ¡”™½½ÑÁÉ¥¹ĞÌÉ•…Í½¹¥¹œ°‰•…ÕÍ”Ñ¡”™½½ÑÁÉ¥¹Ğ¡…Ì)¹¼‘¥ÍÁ±…äÙ…±Õ”Ñ¡…Ğ¥Ì¹½Ğ¥ÑÍ•±˜„‘•É¥Ù…Ñ¥½¸ƒŠPÍ•”MQQULƒ
œ€Èà¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”Í¥‘•…È¥¹Ñ•É™…”¥ÌÍÑ…Ñ•°…¹ÍÑ…Ñ¥¹œ¥Ğ™½Õ¹Ñ¡”Í•½¹™¥•±)™…±±¥¹œÑ¡É½Õ ¥Ğ¸¨¨Q¡”•¹ÑÉä…‰½Ù”•¹‘Ìİ¥Ñ „Í•¹Ñ•¹”İ¡•É”„µ•¡…¹¥Í´‰•±½¹ÌƒŠP€©…¹ä)½Ñ¡•ÈÍ¥‘•…È™¥•±Ñ¡”É•¹‘•É•ÈÉ•…‘Ì¥Ì¥¸Ñ¡”Í…µ”…Ñ•½Éä¨ƒŠP…¹½¹”½˜Ñ¡•´İ…Ì…±É•…‘ä)‰É½­•¸¸Q¡”ÁÉ½Ù•¹…¹”…É…Í­ÌÑ¡”Í¥‘•…È…ÍÍ•Ñ}¥Í}Á±…•¡½±‘•É€°„™¥•±½µÁ¥±•}Í•¹”¹Áå€)¡…Ì¹•Ù•ÈİÉ¥ÑÑ•¸…¹°½µÁ¥±¥¹œ™É½´‘…Ñ„½€…±½¹”°…¹¹½ĞèÍ¼Ñ¡”¹½Ñ”Ñ•±±¥¹œ„Ù¥Í¥Ñ½È€©Ñ¡¥Ì)Í¡…Á”¥Ì„ÍÑ…¹µ¥¸°¹½Ğ„‰…­”™É½´Ñ¡”É•½É¨¡…Ì¹•Ù•ÈÉ•¹‘•É•½¸…¹ä‰Õ¥±‘¥¹œ¸()¡•­}Í¥‘•…É}½¹ÑÉ…Ñ€‘•É¥Ù•ÌÑ¡”¥¹Ñ•É™…”™É½´‰½Ñ ¡…±Ù•ÌÉ…Ñ¡•ÈÑ¡…¸…Í­¥¹œ•¥Ñ¡•ÈÑ¼)‘•±…É”¥ĞƒŠPİ¡…Ğ¥Ì•µ¥ÑÑ•½µ•Ì½™˜Ñ¡”½µµ¥ÑÑ•Í¥‘•…ÉÌ°İ¡¥ €´µ¡•­€…±É•…‘äÁÉ½Ù•Ì)…É”İ¡…ĞÑ¡”‘…Ñ…Í•Ğ½µÁ¥±•ÌÑ¼°…¹İ¡…Ğ¥ÌÉ•…¥ÌÍ…¹¹•½ÕĞ½˜Ñ¡”É•¹‘•É•ÈÌ½İ¸µ½‘Õ±•Ì¸(ÈÜÉ•…‘Ì…É½ÍÌÍ¥àµ½‘Õ±•Ìì½¹”É•Í½±Ù•Ñ¼¹½Ñ¡¥¹œ¸Q¡”™¥àµ½Ù•ÌÑ¡”™…Ğ¥¹ÍÑ•…½˜¥¹Ù•¹Ñ¥¹œ)„™¥•±è„Á±…•¡½±‘•È¥ÌÍ½µ•Ñ¡¥¹œÑ¡”1Í…åÌ…‰½ÕĞ¥ÑÍ•±˜°Í•¹”µ±½…‘•É€¡…ÌÉ•…¥Ğ…Ğ±½…)Ñ¥µ”…±°…±½¹œ°…¹¥Ğ¹½ÜÉ•…¡•ÌÑ¡”…É½¸Ñ¡”É•¥ÍÑÉä•¹ÑÉä¸Q¡”Í…¸Í••Ì„É•…Ñ¡…Ğ)¹…µ•Ì„™¥•±İ¡¥±”Ñ¡”Í¥‘•…È¥Ì¥¸¡…¹…¹¹½Ğ½¹”µ…‘”Ñ¡É½Õ „™Õ¹Ñ¥½¸Á…É…µ•Ñ•ÈƒŠPİ¡¥ )¥ÌÑ¡”‘¥É•Ñ¥½¸‰½Ñ ™…Õ±ÑÌ…µ”™É½´°Í¥¹”Ñ¡…Ğ¥Ìİ¡•É”Ñ¡”™¥•±¹…µ”¥Ì¡½Í•¸¸Q¡”)É•Ù•ÉÍ”‘¥É•Ñ¥½¸¥Ì„¹½Ñ”°¹½Ğ…¸•ÉÉ½È°…¹¥Ğ¡…Ì½¹”™¥¹‘¥¹œ¥¸¥ĞèÉ•Í•…É¡}¹½Ñ•€¥Ì)½µÁ¥±•¥¹Ñ¼•Ù•ÉäÍ¥‘•…È…¹Í¡½İ¸¹½İ¡•É”¸Q¡…Ğ¥Ì…¸Õ¹Í¡¥ÁÁ•±…¥´É…Ñ¡•ÈÑ¡…¸‘•…)İ•¥¡Ğ°…¹¥Ğ‰•±½¹ÌÑ¼İ¡½•Ù•È¹•áĞİ½É­Ì½¸Ñ¡”…É¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠP…¹Ñ¡…Ğ±…¥´¥ÌÍ¡¥ÁÁ•èÑ¡”É•½ÉÌ½İ¸…½Õ¹Ğ¥Ì½¸Ñ¡”…É¸¨¨Q¡”)±…ÍĞ•¹ÑÉä•¹‘Ì‰ä¡…¹‘¥¹œÉ•Í•…É¡}¹½Ñ•€Ñ¼İ¡½•Ù•È¹•áĞİ½É­•¡•É”°…¹Ñ¡¥Ì¥ÌÑ¡…ĞÍ±¥”¸)%Ğ¥Ì„‘¥™™•É•¹Ğ™…Õ±Ğ™É½´Ñ¡”Ñİ¼…‰½Ù”¥Ğ…¹Ñ¡”‘¥™™•É•¹”¥ÌÑ¡”Á½¥¹Ğè¹½Ñ¡¥¹œİ…Ì)‰É½­•¸¸Q¡”…É…Í­•™½È¹½Ñ¡¥¹œ¥Ğİ…Ì¹½Ğ¥Ù•¸°Ñ¡”½µÁ¥±•ÈİÉ½Ñ”İ¡…Ğ¥ĞÍ¡½Õ±°•Ù•Éä)…Ñ”İ…ÌÉ¥¡ĞƒŠP€¨©Ñ¡”™¥•±Í¥µÁ±ä¡…¹¼ÍÕÉ™…”¨¨°İ¡¥ ¥Ì¡½Ü„±…¥´½•ÌÕ¹Í¡¥ÁÁ•İ¡•¸)Ñ¡•É”¥Ì¹¼™…Õ±Ğ™½È„¡•¬Ñ¼™¥¹¸Ù•ÉäÍÑÉÕÑÕÉ”É•½É…ÉÉ¥•Ì½¹”°İÉ¥ÑÑ•¸™½È„É•…‘•Èè)İ¡…Ğ¥Ğ…ÑÕ…±±ä…ÍÍ•ÉÑÌ°İ¡¥ Í½ÕÉ•Ì‘¥Í…É•”°İ¡¥ İ…Ì‰•±¥•Ù•…¹İ¡ä°…¹İ¡•É”Ñ¡”)É•½É¥Ìİ•…­•ÍĞ¸()M¡½İ¸€¨©Ù•É‰…Ñ¥´¨¨°…¹Ñ¡”Íµ½­”Á¥¹ÌÑ¡…Ğİ¥Ñ …¸•á…ĞÍÑÉ¥¹œ½µÁ…É¥Í½¸……¥¹ÍĞÑ¡”Í¥‘•…È)É…Ñ¡•ÈÑ¡…¸„ÍÕ‰ÍÑÉ¥¹œµ…Ñ ƒŠP„¹½Ñ”İ¡½Í”ÍÕ‰©•Ğ¥ÌÑ¡”±¥µ¥Ğ½˜Ñ¡”•Ù¥‘•¹”¥ÌÑ¡”±…ÍĞ)Ñ•áĞ½¸Ñ¡¥Ì…ÉÑ¡…Ğ„ÁÉ½É…´Í¡½Õ±ÑÉ¥´½ÈÍÕµµ…É¥Í”°…¹„™¥ÉÍĞÍ•¹Ñ•¹”İ¥Ñ …¸•±±¥ÁÍ¥Ì)İ½Õ±Á…ÍÌ…¹ä±½½Í•È¡•¬¸Q¡”‘¥ÍÉ¥µ¥¹…Ñ¥¹œ…Í”¥Ì…ÍÍ•ÉÑ•…Ì•Ù•Éåİ¡•É”•±Í”½¸Ñ¡¥Ì)…Éè„Í•½¹‰Õ¥±‘¥¹œ•ÑÌ¥ÑÌ½İ¸…½Õ¹Ğ°Í¼½¹”™¥á•‰±½¬½˜ÁÉ½Í”™…¥±Ì¸½±±…ÁÍ•‰ä)‘•™…Õ±Ğ™½ÈÑ¡”±¥‰•ÉÑ¥•ÌœÉ•…Í½¸ƒŠPÍ•Ù•É…°¡Õ¹‘É•İ½É‘Ì½Á•¸İ½Õ±ÁÕÍ Ñ¡”¥Ñ…Ñ¥½¹Ì½™˜„(ØÉÙ Á…¹•°½¸„Á¡½¹”¸Q¡”Õ¹É•…µ™¥•±¹½Ñ”¥Ì‘½İ¸Ñ¼…É¡•ÑåÁ•€°Í•¹•€…¹Ñ…É•Ñ}‘…Ñ•€°)İ¡¥ …É”µ…¡¥¹•Éä„Ù¥Í¥Ñ½È¡…Ì¹¼É•…Í½¸Ñ¼Í•”°Í¼Ñ¡”±¥ÍĞ¥Ì•µÁÑä½˜Õ¹Í¡¥ÁÁ•±…¥µÌ¸)U¹Ñ•ÍÑ•…¹ÍÑ…Ñ•èÑ¡”•µÁÑäÍÑ…Ñ”°Í¥¹”…±°•¥¡ĞÉ•½É‘Ì…ÉÉä„¹½Ñ”¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”½ÕÑ±¥¹”Í…åÌ¡½ÜµÕ ½˜¥ÑÍ•±˜¥Ì•Ù¥‘•¹”°…¹Ñ¡”Í¥±•¹”¥Ì½Õ¹Ñ…‰±”)¹½Ü¸¨¨Q¡”…ÉÉ…‘•„É½½˜Á¥Ñ …¹Í…¥¹½Ñ¡¥¹œİ¡…Ñ•Ù•È…‰½ÕĞÑ¡”±…É•ÍĞ±…¥´„Ù¥Í¥Ñ½È¥Ì)ÍÑ…¹‘¥¹œ¥¸™É½¹Ğ½˜è½µÁ¥±•}Í•¹”¹Áå€…ÉÉ¥•™½½ÑÁÉ¥¹Ğ¹½¹™¥‘•¹•€…¹‘É½ÁÁ•)™½½ÑÁÉ¥¹Ğ¹Í½ÕÉ•Í€…¹™½½ÑÁÉ¥¹Ğ¹¹½Ñ•€°Í¼Í¥àÁ±…•¡½±‘•ÉÌÑ¡…ĞÍ…äA1!=1H¥¸Ñ¡•¥È½İ¸)™¥ÉÍĞ±¥¹”É•…¡•¹½‰½‘ä°…¹¹•¥Ñ¡•È‘¥Ñ¡”Ñİ¼™½½ÑÁÉ¥¹ÑÌÑ¡…Ğ…É”•Ù¥‘•¹”¸€¨©]…Ì¥ĞÑ¡¥Ì)Í¡…Á”ü¨¨¥Ì„Í•Ñ¥½¸½˜¥ÑÌ½İ¸°É•¹‘•É•‰äÑ¡”Í…µ”±…¥´É•¹‘•É•È…ÌÑ¡”ÁÉ•Í•¹”±¥¹”Í¼Ñ¡”)Ñİ¼…¹¹½Ğ‰”ÅÕ…±¥™¥•‘¥™™•É•¹Ñ±ä¸()Q¡”…ÉÁÉ¥¹ÑÌ€¨©¹¼‘¥µ•¹Í¥½¸¨¨°…¹MQQULƒ
œ€ÈàÌ…ÉÕµ•¹Ğ™½ÈÑ¡…Ğ¥ÌÕ¹¡…¹•ƒŠPÑ¡”½¹±ä)ÁÉ¥¹Ñ…‰±”Ù…±Õ”¥ÌÑ¡”Á½±å½¸°É•‘Õ¥¹œ¥ĞÑ¼„‰½à¥Ì„µ•…ÍÕÉ•µ•¹ĞÑ¡”É•½É‘½•Ì¹½Ğµ…­”°…¹)Ñ¡”Í¡…Á”¥Ì…±É•…‘ä¥¸™É½¹Ğ½˜Ñ¡”Ù¥Í¥Ñ½È…Ğ™Õ±°Í¥é”¸±…¥µI½İ€É•¹‘•ÉÌ¹¼Ù…±Õ”•±°™½È„)¹Õ±±€Ù…±Õ”…¹Ñ¡”Íµ½­”Á¥¹ÌÑ¡…Ğ…É½ÍÌ…±°•¥¡Ğ‰Õ¥±‘¥¹Ì¸()Qİ¼Ñ¡¥¹Ìİ½ÉÑ …ÉÉå¥¹œ¸€¨©Q¡”½µÁ•¹Í…Ñ¥¹œ‘¥Í±½ÍÕÉ”İ…Ì„Í•¹Ñ•¹”°¹½Ğ„‰Õ¥±¨¨èÑ¡”µ…ÍÍ¥¹œ)ÉÕ±”İ…Ì¹…ÉÉ½İ•Ñ¼ÍÑ½À‘¥Ñ¡•É¥¹œ„‘½Õµ•¹Ñ•‰Õ¥±‘¥¹œ½Ù•È…¸Õ¹­¹½İ¸M%i°½¸Ñ¡”É•½É‘•)Õ¹‘•ÉÍÑ…¹‘¥¹œÑ¡…ĞÑ¡”Í¥é”İ½Õ±‰”…ÉÉ¥•½¸Ñ¡”…É°…¹¹½Ñ¡¥¹œ…ÉÉ¥•¥Ğ¸€¨©¹Ñ¡¥Ì¥ÌÑ¡”)Í•½¹É…‘•µ…¹µÍ¥±•¹Ğ±…¥´™½Õ¹‰äÉ•…‘¥¹œ„™¥±”¨¨€¡‘½Õµ•¹Ñ•‘}É…¹•€İ…ÌÑ¡”™¥ÉÍĞ¤°Í¼¥Ğ)¡…Ì„½Õ¹ĞÉ…Ñ¡•ÈÑ¡…¸„Ñ¡¥É‘¥Í½Ù•É•ÈèÑ¡”Íµ½­”µ…Ñ¡•Ì•… É•½ÉÌÉ…‘•±…¥µÌ……¥¹ÍĞ)Ñ¡”¡¥ÁÌ¥ÑÌ…É‘É…İÌ°™½È•Ù•Éä‰Õ¥±‘¥¹œ°…¹É•Á½ÉÑÌ…±°•¥¡Ğ½¹”¡¥ÀÍ¡½ÉĞİ¡•¸ÉÕ¸……¥¹ÍĞ)Ñ¡”ÁÉ•Ù¥½ÕÌ½µµ¥Ğ¸]¡…Ğ¥Ğ…¹¹½ĞÍ•”¥Ì„¡¥Àİ¡½Í”É•…Í½¹¥¹œ¥ÌİÉ½¹œ°…¹¥Ğ…¹¹½ĞÉ•… „)™¥•±Ñ¡”½µÁ¥±•È¹•Ù•ÈİÉ¥Ñ•ÌƒŠP¡•­}Í¥‘•…É}½¹ÑÉ…Ñ€ÌÕ¹É•…É•Á½ÉĞ¥ÌÑ½Àµ±•Ù•°½¹±ä°…¹)İ¥‘•¹¥¹œ¥ĞÑ¼±•…Ù•Ìİ…ÌÉ•™ÕÍ•‰•…ÕÍ”Ñ¡”Í…¸…¹¹½Ğ™½±±½Ü„Ù…±Õ”¥¹Ñ¼„™Õ¹Ñ¥½¸¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”½Á•¸ÅÕ•ÍÑ¥½¸É•…¡•ÌÑ¡”‰Õ¥±‘¥¹œ¥Ğ¥Ì…‰½ÕĞ°…¹Ñ¡”Á…¹•°ÌÁÉ½µ¥Í”)…‰½ÕĞÑ¡”…É¥Ì„…Ñ”¸¨¨ƒ
œ€ÈØÍ…¥Ñ¡”İ…Ñ ±¥ÍĞÌÕ¹•ÉÑ…¥¹Ñä‰•±½¹Ì½¸Ñ¡”É•½É‘Ì…¹¥¸Ñ¡”)ÁÉ½Ù•¹…¹”Á½ÁÕÀ…¹±•™Ğ¥ĞÕ¹ÅÕ•Õ•ìÑ¡”Á…¹•°¡…±˜Í¡¥ÁÁ•…¹¥ÑÌ•¹ÑÉä™½ÈÑ¡”½¹”MQ9%9)ÍÑÉÕÑÕÉ”Ñ•±±Ì„Ù¥Í¥Ñ½È°¥¸É•¹‘•É•Ñ•áĞ°Ñ¡…Ğ€©Ñ¡”ÁÉ½Ù•¹…¹”…ÉÍ¡½İÌ¥Ğ¨¸Q¡”…ÉÍ¡½İ•)Ñ¡”‘…Ñ•±…¥´İ¥Ñ …¸¥¹™•ÉÉ•‘€¡¥À…¹¹•Ù•ÈÑ¡…ĞÑ¡”±…¥´¥Ì„ÑÉ…­•½Á•¸ÅÕ•ÍÑ¥½¸ƒŠP¹½Ğ)Ñ¡”‘¥ÍÁÕÑ”‰•¡¥¹¥Ğ€¡Ñ¡”‰Õ¥±‘•ÈÌ½İ¸ÍÑ…Ñ•µ•¹Ğ……¥¹ÍĞ„¡½Ñ•°¡É½¹½±½ä¤°¹½ĞÑ¡…ĞÑ¡”±…Ñ•È)‘…Ñ”İ½Õ±µ…­”Ñ¡”]•ÍÑ•É¸!½Ñ•°‰É…¹¹•Ü½¸Ñ¡”Í•¹”‘…Ñ”°¹½ĞÑ¡…ĞÑ¡”É…‘”¥Ì¡•±‘½İ¸½¸)ÁÕÉÁ½Í”¸Q¡”…É¹½Ü…ÉÉ¥•ÌÑ¡”Á…¹•°Ì½İ¸•¹ÑÉäÑ¡É½Õ Ñ¡”Á…¹•°Ì½İ¸É•¹‘•É•Èİ¥Ñ …¸)½¹…É‘€™±…œ°™¥±Ñ•É•‰ä½Á•¹EÕ•ÍÑ¥½¹Í½É€•á…Ñ±ä…ÌÑ¡”±¥‰•ÉÑ¥•Ì…É”°Í¼½¹”Õ¹•ÉÑ…¥¹Ñä)…¹¹½Ğ‰”‘•ÍÉ¥‰•Ñİ¼İ…åÌ¸Q¡”½Ñ¡•ÈÍ•Ù•¸‰Õ¥±‘¥¹ÌÉ•¹‘•È¹½Ñ¡¥¹œÉ…Ñ¡•ÈÑ¡…¸„É•…ÍÍÕÉ…¹”°)‰•…ÕÍ”€‰¹¼½Á•¸ÅÕ•ÍÑ¥½¹ÌÉ•½É‘•ˆİ½Õ±É•……ÌÍ•ÑÑ±•…¹Ñ¡”±¥ÍĞ…¹¹½ĞÁÉ½µ¥Í”Ñ¡…Ğ¸)¹¡•­}İ…Ñ¡}±¥ÍÑ€¹½Ü¡½±‘Ì…ÉÉ¥•‘}‰å€Ñ¼„±…¥´Ñ¡”…ÉÉ•…±±äÉ•¹‘•ÉÌƒŠPÑ¡”Á…Ñ ¥ÌÉ•…)½ÕĞ½˜Á½ÁÕÀ¹©Í€‰äƒ
œ€ÈäÌÍ…¹¹•ÈƒŠPİ¡¥ ¥ÌÑ¡”Ñ¡¥É¥¹ÍÑ…¹”½˜„Í•¹Ñ•¹”¥¸Ñ¡¥ÌÁÉ½©•Ğ)‘•ÍÉ¥‰¥¹œ„ÍÕÉ™…”¥Ğ½Õ±¹½ĞÍ•”¸…Ñ„…¹µ•Í¡•ÌÕ¹Ñ½Õ¡•ì¹½Ñ¡¥¹œİ…ÌÉ”µ‰…­•¸MQQULƒ
œ€ĞÄ¸((¨©½¹”€ÈÀÈØ´Àà´ÄÄƒŠP„ÉÕ¹œ¥Ì„©Õ‘•µ•¹Ğ…‰½ÕĞ„‘½Õµ•¹Ğ°…¹Ñ¡”‘½Õµ•¹Ğ¡…¹•Ù•ÈÉ•…¡•)Ñ¡”…É¸¨¨½ÕÈÍ±¥•Ì€£
œ€ĞĞ´ĞÜ¤•ÍÑ…‰±¥Í¡•İ¡¥ Á…”…ÉÉ¥•Ìİ¡¥ ‘½Õµ•¹Ğ…¹İ¡…Ğ•… )½¹”…¹¹½ĞÍÕÁÁ±äì…±°½˜¥Ğ±…¹‘•¥¸‘…Ñ„½Í½ÕÉ•Ì¼¨¹©Í½¹€…¹¹½¹”½˜¥Ğ±•™ĞÑ¡”É•Á½Í¥Ñ½Éä¸)M¼„Ù¥Í¥Ñ½È™½±±½İ¥¹œ„¥Ñ…Ñ¥½¸É•…¡•„ÁÉ•Í•¹Ğµ‘…ä‰±½œÍÑ…µÁ•€©Ñ¥•È€Èƒ
Ü¹•…ÈµÁÉ¥µ…Éä)É•½±±•Ñ¥½¸¨İ¥Ñ ¹½Ñ¡¥¹œÍ…å¥¹œ¥ĞÉ•ÁÉ¥¹ÑÌÑ¡”€©¡¥…¼QÉ¥‰Õ¹”¨½˜€ÄĞÕÕÍĞ€ÄäÄÀ…ÉÉå¥¹œ))½¡¸•…¸…Ñ½¸Ì½İ¸…½Õ¹ĞƒŠPÑ¡”±…‘‘•Èµ…‘”Ñ¼±½½¬±¥­”…¸½Ù•ÈµÉ…‘”‰äÑ¡”½¹”™¥•±Ñ¡…Ğ)İ½Õ±¡…Ù”•áÁ±…¥¹•¥Ğ¸Ù•Éä¥Ñ…Ñ¥½¸¹½Ü…ÉÉ¥•ÌÑ¡”‘½Õµ•¹Ğ¥ĞÉ•ÁÉ¥¹ÑÌİ¥Ñ Ñ¡…Ğ)‘½Õµ•¹ĞÌ‘…Ñ”°½ÈÑ¡”™¥¹‘¥¹œÑ¡…ĞÑ¡”Á…”É•ÁÉ¥¹ÑÌ¹½¹”°…¹Ñ¡”Í½ÕÉ”Ì½İ¸)İ¡…Ñ}¥Ñ}ÍÕÁÁ±¥•Í€€¼İ¡…Ñ}¥Ñ}‘½•Í}¹½Ñ}ÍÕÁÁ±å€‰•¡¥¹„€ñ‘•Ñ…¥±Ìù€¸()Q¡”™…Õ±Ğ¥Ì„Ñ¡¥É­¥¹…¹¥Ğ¥Ìİ¡äÑ¡”…Ñ”¥ÌÍ¡…Á•Ñ¡”İ…ä¥Ğ¥Ì¸ƒ
œ€Èàİ…Ì„™¥•±É•…)…¹¹•Ù•È•µ¥ÑÑ•ìƒ
œ€ÌÀİ…Ì„™¥•±•µ¥ÑÑ•…¹¹•Ù•ÈÉ•…¸Q¡¥Ì½¹”€¨©¹•Ù•È•¹Ñ•É•Ñ¡”)¥¹Ñ•É™…”¨¨°İ¡¥ ¹•¥Ñ¡•È‘¥É•Ñ¥½¸½˜¡•­}Í¥‘•…É}½¹ÑÉ…Ñ€…¸Í•”ƒŠP„Í¡…Á”Õ¹¥½¹•½Ù•È)İ¡…Ğ¥Ì•µ¥ÑÑ•…¹¹½ĞÉ•Á½ÉĞİ¡…Ğİ…Ì¹•Ù•È½™™•É•¸Q¡”‰½Õ¹‘•Í•Ğ¥ÌÑ¡”Í¡•µ„°Í¼)½µÁ¥±•}Í•¹”¹M=UI}%1}MUI€Á…ÉÑ¥Ñ¥½¹Ì…±°€ÈÈÁÉ½Á•ÉÑ¥•Ì…¹¡•­}Í½ÕÉ•}ÍÕÉ™…•€)™…¥±Ì½¸„ÁÉ½Á•ÉÑä¥¸¹•¥Ñ¡•È¡…±˜°½¸„Ù¥Í¥Ñ½Èµ™…¥¹œ™¥•±¹¼½µÁ¥±•¥Ñ…Ñ¥½¸…ÉÉ¥•Ì°…¹)½¸½¹”¥Ñ…Ñ¥½¹Ì¹©Í€¹•Ù•ÈÉ•…‘Ì¸‘‘¥¹œ„™¥•±Ñ¼„Í½ÕÉ”É•½É¹½Ü½ÍÑÌ½¹”±¥¹”Í…å¥¹œ)İ¡•Ñ¡•È„Ù¥Í¥Ñ½ÈÍ••Ì¥Ğ¸()Q¡É•”Ñ¡¥¹Ìİ½ÉÑ …ÉÉå¥¹œè((´€¨©Á…ÉÑ¥Ñ¥½¸¥¹Í¥‘”„™¥•±¥Ì±•¥Ñ¥µ…Ñ”…¹¡…ÌÑ¼‰”…ÉÕ•¸¨¨Q¡”…É•ÑÌÑ¡”‘½Õµ•¹Ğ(€…¹Ñ¡”±¥µ¥ÑÌì¥Ğ‘½•Ì¹½Ğ•ĞÑ¡”¹½Ñ•€½¸„ÑÉ…¹ÍÉ¥‰•Í€•¹ÑÉä½ÈÑ¡”É•…‘¥¹œ¥¸(€…ÉÉ¥•Í}¹½}‘½Õµ•¹Ñ€°‰•…ÕÍ”‰½Ñ ÅÕ½Ñ”ÉÕ¹œ¹Õµ‰•ÉÌ°¹…µ”™¥±•Ì¥¸‘…Ñ„½€…¹É•½É!QQ@(€ÍÑ…ÑÕÍ•ÌƒŠPÑ¡•ä…É”…‘‘É•ÍÍ•Ñ¼İ¡½•Ù•ÈÉ”µÉ…‘•ÌÑ¡”Í½ÕÉ”¸MÑ…Ñ•¥¸¥Ñ…Ñ¥½¹Ì¹©Í€…¹¥¸(€MQQULƒ
œ€ĞàÉ…Ñ¡•ÈÑ¡…¸±•™Ğ±½½­¥¹œ±¥­”…¸½Ù•ÉÍ¥¡Ğ¸(´€¨©=¹”É•¹‘•É•È™½È•Ù•Éä½¹Ñ•áĞÍÑ½ÁÁ•‰•¥¹œÉ¥¡Ğ°…¹„Ñ•ÍĞÍ…¥Í¼™¥ÉÍĞ¸¨¨Q¡”É•ÁÉ¥¹ÑÌ(€±¥¹”…ÉÉ¥Ù•Õ¹‘•È€‰]¡…Ğ¥Ì¹½Ğ¡•É”ˆ…¹¹…µ•€¨‰Q¡”=±]•ÍÑ•É¸!½Ñ•°ˆ¨ƒŠP„‰Õ¥±‘¥¹œÍÑ…¹‘¥¹œ(€€ÈÀÀ´…İ…äƒŠP™…¥±¥¹œƒ
œ€ÈØÌ…ÍÍ•ÉÑ¥½¸Ñ¡…Ğ„ÍÑ…¹‘¥¹œ‰Õ¥±‘¥¹œµ…ä¹½Ğ…ÁÁ•…È½¸Ñ¡…Ğ±¥ÍĞ¸Q¡”(€Í•Ñ¥½¸­••ÁÌÑ¡”Á±…¥¸¥Ñ…Ñ¥½¸°•Ù¥‘•¹”è™…±Í•€Í…åÌÍ¼…ĞÑ¡”…±°Í¥Ñ”°…¹„¹•Ü(€…ÍÍ•ÉÑ¥½¸Á¥¹Ì¥ĞÍ¼Ñ¡”½ÁÑ¥½¸…¹¹½Ğ™±¥À‰…¬¸(´€¨©5…É­ÕÀ¥¹Í¥‘”„±¥ÍĞ¥Ñ•´µ…­•Ì½Õ¹Ñ¥¹œÍ•±•Ñ½ÉÌİÉ½¹œ¸¨¨¹•ÍÑ•€ñÕ°ù€‰É½­”Ñİ¼(€Õ¹É•±…Ñ•…ÍÍ•ÉÑ¥½¹Ì•¹Õµ•É…Ñ¥¹œ€¹¥Ñ•Ì±¥€ìÑ¡•ä…É”€¹¥Ñ•Ì€ø±¥€¹½Ü¸M•½¹½ÕÉÉ•¹”½˜(€Ñ¡¥ÌÍ¡…Á”¸((¨©½¹”€ÈÀÈØ´Àà´ÄÄƒŠPÑ¡”½Ñ¡•ÈÑ¡É•”‘•É¥Ù•‘½Õµ•¹ÑÌ…É”…¸¥¹Ñ•É™…”Ñ½¼°…¹‰½Ñ Í•¹Ñ•¹•Ì)Ñ¡•äİ•É”¡¥‘¥¹œİ•É”İÉ¥ÑÑ•¸™½È„Ù¥Í¥Ñ½È¸¨¨Q¡”•¹ÑÉä…‰½Ù”±½Í•ÌÑ¡”Í½ÕÉ”µÉ•½É)‘¥É•Ñ¥½¸¸]¡…Ğ¥Ğ‘½•Ì¹½Ğ±½Í”¥ÌÑ¡”€©‘½Õµ•¹Ğ¨èÍ¥‘•…É}Í¡…Á•€Í…åÌ¥¸¥ÑÌ½İ¸‘½ÍÑÉ¥¹œ)Ñ¡…Ğ¥Ğ½Ù•ÉÌÑ¡”Á•ÈµÍÑÉÕÑÕÉ”Í¥‘•…È…¹¹½Ğ•á±ÕÍ¥½¹Ì¹©Í½¹€½ÈÑ•ÉÉ…¥¸¹©Í½¹€°‰•…ÕÍ”)Ñ¡½Í”€‰¡…Ù”Ñ¡•¥È½İ¸É•…‘•ÉÌ…¹Ñ¡•¥È½İ¸Í¡…Á•ÌˆƒŠPÍ¼Ñ¡”¥¹Ñ•É™…”İ¡•É”ƒ
œ€Èà°ƒ
œ€Èä…¹ƒ
œ€ÌÀ)•… ™½Õ¹„™…Õ±Ğİ…ÌÕ…É‘•™½È½¹”‘½Õµ•¹Ğ½ÕĞ½˜™½ÕÈ¸¡•­}‘•É¥Ù•‘}½¹ÑÉ…Ñ€½Ù•ÉÌÑ¡”)½Ñ¡•ÈÑ¡É•”°‰½Ñ ‘¥É•Ñ¥½¹Ì°…¹™½Õ¹Ñİ¼½¸¥ÑÌ™¥ÉÍĞÉÕ¸¸()Q¡”É½Õ¹¹½ÜÍ…åÌ€¨©İ¡¥ É½Õ¹¨¨¥ÑÌÑİ•¹Ñä±…¥µÌ…É”…‰½ÕĞƒŠPÑ¡”ÍÁ•ŒÌ½İ¸Í•¹Ñ•¹”…‰½ÕĞ)Ñ¡”™½É­ÌÅÕ…‘É…¹Ğ°½µÁ¥±•¥¹Ñ¼•Ù•ÉäÑ•ÉÉ…¥¸Í¥‘•…ÈÍ¥¹”Ñ¡”Ñ•ÉÉ…¥¸±…¹‘•…¹…Í­•™½È‰ä)¹½‰½‘ä°İ¡¥ ¥ÌÑ¡”™¥ÉÍĞÅÕ•ÍÑ¥½¸„Ù¥Í¥Ñ½È¡…Ì…™Ñ•Èİ…Ñ¡¥¹œÑ¡”É½Õ¹•¹™É½´Ñ¡”…¥È¸¹)Ñ¡”±¥‰•ÉÑ¥•Ì±¥ÍĞÍ…åÌİ¡…Ğ„±¥‰•ÉÑä¥Ì€¨©¥¸Ñ¡”‘½Õµ•¹ĞÌİ½É‘Ì¨¨è±¥‰•ÉÑ¥•Ì¹©Í½¹€…ÉÉ¥•Ì)Ñ¡…ĞÍ•¹Ñ•¹”°¥¹‘•à¹¡Ñµ±€…ÉÉ¥•„¡…¹µÑåÁ•Á…É…Á¡É…Í”½˜¥Ğİ¥Ñ ¹½Ñ¡¥¹œ¡½±‘¥¹œÑ¡”Ñİ¼)Ñ½•Ñ¡•È°…¹Ñ¡”Á…É…Á¡É…Í”¥Ì½¹”¸()Q¡É•”Ñ¡¥¹Ìİ½ÉÑ …ÉÉå¥¹œè((´€¨©Q¡”‰¥¹‘¥¹œ¥Ì‘•±…É•°¹½Ğ¥¹™•ÉÉ•°…¹Ñ¡…Ğ¥ÌÑ¡”‘•Í¥¸¸¨¨Í¥‘•…È¹…µ•Ì¥ÑÍ•±˜ì(€Ñ¡•Í”…É”™•Ñ¡•¥¹Ñ¼‘½€…¹¡…¹‘••¹ÑÉä‰ä•¹ÑÉäÑ¼„É•¹‘•É•È°Í¼Ñ¡”™¥•±¹…µ”¥Ì(€¡½Í•¸……¥¹ÍĞ„™Õ¹Ñ¥½¸Á…É…µ•Ñ•ÈƒŠPƒ
œ€ÈäÌÍÑ…Ñ•±¥µ¥Ğ¸I%Y}=U59QM€İÉ¥Ñ•ÌÑ¡”(€‰¥¹‘¥¹œ‘½İ¸…¹Ñ¡”…Ñ”¡½±‘ÌÑ¡”µ½‘Õ±”Ñ¼¥Ğ‰½Ñ İ…åÌ°¥¹±Õ‘¥¹œ„É½½Ğ‰½Õ¹İ¡•É”Ñ¡”(€‘½Õµ•¹Ğ¡…Ì¹½Ñ¡¥¹œ¸(´€¨©¥¹Ñ•É¹…±€¥Ìƒ
œ€ĞàÌÁ…ÉÑ¥Ñ¥½¸½¸„Í•½¹™…µ¥±ä¨¨°½Ù•Èİ¡…ĞÑ¡”½µÁ¥±•È•µ¥ÑÌÉ…Ñ¡•ÈÑ¡…¸(€½Ù•È„Í¡•µ„°¡•­•¥¸‰½Ñ ‘¥É•Ñ¥½¹ÌÍ¼„‘•±…É…Ñ¥½¸…¹¹½Ğ½ÕÑ±¥Ù”¥ÑÌ™¥•±½È‰”İÉ½¹œ(€…‰½ÕĞÑ¡”Ù¥Í¥Ñ½È¸¥Ñ…Ñ¥½¸±•…Ù•ÌÍÑ…äİ¥Ñ ¡•­}Í½ÕÉ•}ÍÕÉ™…•€è½¹”™¥•±°½¹”½İ¹•È¸(´ùø¨©É•…¥Ì„¹…µ”°¹½Ğ„É•¹‘•ÈƒŠP…¹½¹”¥ÌÍÑ¥±°½ÕÑÍÑ…¹‘¥¹œ¸¨©ùø€¨©=9€ÈÀÈØ´Àà´ÄÄ¨¨(€€¡MQQULƒ
œ€ÔÀ¤¸•á±ÕÍ¥½¹Ì¹©Í½¹€ÌÍÑ…¹‘…É‘€…¹Õ¹•ÉÑ…¥¹}ÍÑ…¹‘…É‘€İ•É”É•…¥¹Ñ¼(€µ½Õ¹Ñá±ÕÍ¥½¹Í€ÌÉ•ÑÕÉ¸Ù…±Õ”°É•¹‘•É•‰ä¹½‰½‘ä°…¹É•ÍÑ…Ñ•‰ä¡…¹¥¸¥¹‘•à¹¡Ñµ±€ì(€‰½Ñ …É”µ½Õ¹Ñ•Ù•É‰…Ñ¥´¹½Ü…¹Ñ¡”Á…É…Á¡É…Í•Ì…É”‘•±•Ñ•¸%Ğİ…ÌÑ¡”•ÍÑ¥µ…Ñ•Í¥é”ƒŠP„(€ÍÑ…¹‘…É‘5½Õ¹Ñ€…¹Ñİ¼Á…É…É…Á¡ÌƒŠP…¹¥Ğ™½Õ¹½¹”Ñ¡¥¹œÑ¡”•ÍÑ¥µ…Ñ”‘¥¹½ĞèÑ¡”(€½Á•¸µÅÕ•ÍÑ¥½¹ÌÁ…É…Á¡É…Í”¡…‘É¥™Ñ•¥¹Ñ¼„€¨©¡…¹µÑåÁ•½Õ¹Ğ¨¨½˜Ñ¡”İ…Ñ ±¥ÍĞ€ ‰Ñ¡É•”½˜(€Ñ¡•Í”ƒŠ˜…¹Ñ¡”™½ÕÉÑ ˆ¤°İ¡¥ ½•ÌİÉ½¹œÑ¡”‘…ä„™¥™Ñ ÅÕ•ÍÑ¥½¸¥ÌÉ•½É‘•…¹İ¡¥ ¹¼(€…Ñ”¥¸Ñ¡¥ÌÁÉ½©•Ğ½Õ±¡…Ù”¡•±¸Q¡”Íµ½­”…ÍÍ•ÉÑÌÑ¡”½µÁ¥±•Í•¹Ñ•¹”Ù•É‰…Ñ¥´°½¹”°(€…¹Ñ¡…ĞÑ¡”½Õ¹Ğ¥Ì½¹”¸€¨©Q¡”…Ñ”Ì±¥µ¥Ğ¥ÌÕ¹¡…¹•…¹İ…Ì¹½Ğİ¥‘•¹•¨¨è„É•…¥Ì(€ÍÑ¥±°„¹…µ”°Ñ¡”Í…¸ÍÑ¥±°…¹¹½Ğ™½±±½Ü„Ù…±Õ”¥¹Ñ¼„™Õ¹Ñ¥½¸°…¹Ñ¡”¹•áĞÍÕ ™¥•±(€İ¥±°‰”™½Õ¹‰ä„Á•ÉÍ½¸É•…‘¥¹œ„µ½‘Õ±”¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”ÍÑ…±•¹•ÍÌ…Ñ”¥Ì„¡•¬¹½Ü°¹½Ğ„Í•¹Ñ•¹”¸¨¨Ù•ÉäÉÕ±”…‰½Ù”)…ÍÍÕµ•ÌÑ¡”Í¡¥ÁÁ•µ•Í ¥ÌÑ¡”½¹”Ñ¡”É•½É‘•ÍÉ¥‰•Ì°…¹¹½Ñ¡¥¹œİ…ÌÑ•ÍÑ¥¹œÑ¡…ĞèÑ¡”)µ…¹¥™•ÍĞ¡……ÉÉ¥•…¸¥¹ÁÕÑÍ}Í¡„ÈÔÙ€Á•È…ÍÍ•ĞÍ¥¹”Ñ¡”™¥ÉÍĞ‰…­”…¹¹¼½‘”•Ù•È)É•½µÁÕÑ•¥Ğ¸%Ğ‘½•Ì¹½Ü°™½È‰Õ¥±‘¥¹Ì…¹Ñ•ÉÉ…¥¸…±¥­”°İ¥Ñ Ñ¡”É•¥Á”±¥Ù¥¹œ‰•Í¥‘”Ñ¡”)•¹•É…Ñ½ÉÌÍ¼Ñ¡”İÉ¥Ñ•È…¹Ñ¡”¡•­•È…¹¹½Ğ‘É¥™Ğ¸()QÕÉ¹¥¹œ¥Ğ½¸µ•…¹ĞÉ•İÉ¥Ñ¥¹œİ¡…ĞÑ¡”¡…Í ¥Ì½Ù•È°‰•…ÕÍ”Ñ¡”½±½¹”É•Á½ÉÑ•…±°Í¥à)‰Õ¥±‘¥¹ÌÍÑ…±”™½ÈÉ•…Í½¹ÌÑ¡…Ğ…¹¹½Ğµ½Ù”„Ù•ÉÑ•àƒŠPÉ•½ÉÁÉ½Í”°…¹„½¹ÍÑ…¹Ğ…‘‘•Ñ¼„)Í¥‰±¥¹œ…É¡•ÑåÁ”ÌÁ…É…µ•Ñ•Èµ½‘Õ±”¸%Ğ¹½Ü¡…Í¡•ÌÑ¡”€©É•Í½±Ù•¨Á…É…µ•Ñ•ÉÌ°Ñ¡”‘•É¥Ù•)ÁÉ½Á•ÉÑ¥•Ì°Ñ¡”½¹™¥‘•¹”™±½…ÑÌ…¹Ñ¡”‰Õ¥±‘•ÈÌ‰åÑ•ÌìÁ…É…µ•Ñ•Èµµ½‘Õ±”Í½ÕÉ”¥Ì½ÕĞ°)‰•…ÕÍ”¥ÑÌ•¹Ñ¥É”•™™•Ğ½¸Ñ¡”µ•Í ¥ÌÑ¡”½‰©•Ğ¥ĞÉ•ÑÕÉ¹Ì¸Q¡”•¥¡Ğ½µµ¥ÑÑ•¡…Í¡•Ìİ•É”)É”µÍÑ…µÁ•İ¥Ñ¡½ÕĞ„‰…­”…¹Ñ¡”É”µÍÑ…µÀ¥ÌÁÉ½Ù•É…Ñ¡•ÈÑ¡…¸…ÍÍ•ÉÑ•èÉÕ¸Ñ¡”¹•ÜÉ•¥Á”)¥¹Í¥‘”„İ½É­ÑÉ•”½˜Ñ¡”±…ÍĞ‰…­”½µµ¥Ğ…¹Ñ¡”¥¹ÁÕĞ‘½Õµ•¹ÑÌ½µ”½ÕĞ¥‘•¹Ñ¥…°°‰Õ¥±¹Áå€)•á•ÁÑ•°İ¡½Í”½¹±ä¡…¹”¥Ì‘•±•…Ñ¥¹œÑ¡”¡…Í ¸M•”MQQULƒ
œ€ÄÔ™½ÈÑ¡”™Õ±°…½Õ¹Ğ…¹Ñ¡”)±¥µ¥ĞƒŠPÑ¡¥Ì½µÁ…É•Ì¥¹ÁÕÑÌ°¹½Ğ½ÕÑÁÕĞ°Í¼„¡…¹µ•‘¥Ñ•1ÍÑ¥±°Á…ÍÍ•Ì¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠP„ÍÑÉÕÑÕÉ”¡…ÌÑ¼É•… Ñ¡”É½Õ¹°…¹½¹”‘½•Ì¹½Ğ¸¨¨Q¡”Ñ¡¥É)¡½¹•ÍÑä…Ñ”¥¸Ñ¡”™…µ¥±äÑ¡…Ğ‰•…¸İ¥Ñ ±¥‰•ÉÑ¥•Ì½Ù•É…”¸Q¡”½¹™¥‘•¹”µ½‘•°É…‘•Ìİ¡…Ğ)„Ù…±Õ”±…¥µÌ…¹Ñ¡”•½µ•ÑÉä‘•±…É…Ñ¥½¹ÌÉ…‘”İ¡•Ñ¡•È¥Ğİ…Ì‰Õ¥±Ğì¹•¥Ñ¡•È…¸Í•”„)ÍÑÉÕÑÕÉ”…ÍÍ•µ‰±•™…¥Ñ¡™Õ±±ä½¹Ñ¼É½Õ¹Ñ¡…Ğ¥Ì¹½ĞÕ¹‘•È¥Ğ°‰•…ÕÍ”•Ù•Éä¹…µ”É•Í½±Ù•Ì…¹)•Ù•ÉäÙ…±Õ”É•…¡•Ì„Ù•ÉÑ•à¸… …É¡•ÑåÁ”¹½Ü‘•±…É•Ìİ¡•É”¥ĞÑ½Õ¡•ÌÑ¡”Ñ•ÉÉ…¥¸ƒŠP)Á•É¥µ•Ñ•É€…ĞÑ¡”‰…Í”½˜Ñ¡”İ…±±Ì°•¹‘Í€…Ğ‘•¬¡•¥¡Ğ™½È„É½ÍÍ¥¹œƒŠP…¹Ù…±¥‘…Ñ”¹Áå€)µ•…ÍÕÉ•ÌÑ¡…Ğ½ÕÑ±¥¹”……¥¹ÍĞÑ¡”½µµ¥ÑÑ•¡•¥¡Ñ™¥•±¸Q¡”Ñ½±•É…¹”¥ÌÑ¡”İ…±­•ÈÌ€À¸ÌÔ´)ÍÑ•ÀµÕÀÉÕ±”É…Ñ¡•ÈÑ¡…¸„™É•Í ¹Õµ‰•È°‰•…ÕÍ”Ñ¡”…Ñ”¥Ì…Í­¥¹œÑ¡”İ…±­•ÈÌÅÕ•ÍÑ¥½¸¸()Q¡”Í¥à‰Õ¥±‘¥¹Ì±…¹°İ½ÉÍĞ½É¹•È€À¸ÄØ´¸€¨©Q¡”9½ÉÑ 	É…¹ ‰É¥‘”ÍÑ…¹‘Ì€È¸ĞÈ´±•…È½˜)Ñ¡”É½Õ¹…Ğ‰½Ñ ±…¹‘¥¹Ì…¹¹¼±…¹¥¸Ñ¡”€ØĞÀ´‰½àÉ¥Í•ÌÑ¼¥ÑÌ‘•¬¨¨°Í¼Ñ¡”É½ÍÍ¥¹œ)Ñ½Õ¡•Ì¹•¥Ñ¡•È‰…¹¬¸Q¡”É•½É‘•±…É•ÌÉ½Õ¹‘}½¹Ñ…Ğè…ÁÁÉ½…¡}¹½Ñ}µ½‘•±±•‘€°0ÌÀ…‘µ¥ÑÌ)¥Ğ°…¹Ñ¡”¡¥ÀÉ•…¡•ÌÑ¡”Ù¥Í¥Ñ½ÈÑ¡É½Õ Ñ¡”ÁÉ½Ù•¹…¹”Á½ÁÕÀ¸Qİ¼™½±±½Üµ½¹ÌÑ¡¥Ì±•…Ù•Ì)½¸Ñ¡”Ñ…‰±”°‰½Ñ É•…°…¹‰½Ñ ‰¥•ÈÑ¡…¸„Í±¥”è((´€¨©Q¡”…ÁÁÉ½… ¥ÑÍ•±˜¥ÌÕ¹…ÑÑ•ÍÑ•¸¨¨9½Ñ¡¥¹œ‘•ÍÉ¥‰•Ì¡½Ü„Á•ÉÍ½¸½Ğ™É½´Ñ¡”‰…¹¬½¹Ñ¼(€Ñ¡”‘•¬°Í¼Ñ¡”™¥à¥ÌÉ•Í•…É ‰•™½É”¥Ğ¥Ì•½µ•ÑÉäƒŠPÑ¡”€ÄàÌĞ¼ÄàÌÔ]…‰…¹Í¥„…¹-¥¹é¥”Ì(€‘‘¥Ñ¥½¸Á±…Ğ¥ÌÑ¡”‰•ÍĞ…¹‘¥‘…Ñ”°…¹„Í½ÕÉ•±•…É…¹”İ½Õ±¹…ÉÉ½Ü¥ĞÑ½¼°Í¥¹”„(€±½İ•È‘•¬¹••‘Ì±•ÍÌ…ÁÁÉ½… ¸(´€¨©]…±­¥¹œÑ¡”‘•¬¨¨€¡MQQULƒ
œ€ÈÄ¤¥Ì¹½Üµ•…ÍÕÉ…‰±ä‰±½­•É…Ñ¡•ÈÑ¡…¸µ•É•±äÕ¹‰Õ¥±Ğè•Ù•¸(€İ¥Ñ ÍÕÉ™…•Ìµ…‰½Ù”µÑ¡”µÉ½Õ¹¥¸Ñ¡”İ…±­•È°Ñ¡•É”¥Ì¹½Ñ¡¥¹œÑ¼ÍÑ•À™É½´¸Q¡”Ñİ¼…É”½¹”(€Á¥•”½˜İ½É¬°¥¸Ñ¡…Ğ½É‘•È¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”É½Õ¹ÍÑ…Ñ•Ì¥ÑÌ½İ¸±…¥µÌ°…¹ÍÑ…Ñ¥¹œÑ¡•´™½Õ¹Ñ¡”Í•½¹™¥±”)İ¡•É”ÉÕ±”½¹”İ…Ì¹•Ù•È¡•­•¸¨¨Ù•Éä¡½¹•ÍÑäÍÕÉ™…”…‰½Ù”‰•±½¹ÌÑ¼„‰Õ¥±‘¥¹œ¸Q¡”)Ñ•ÉÉ…¥¸É…‘•Ì¥ÑÍ•±˜…Ì…É•™Õ±±ä…Ì…¹äÉ•½ÉƒŠP‘½Õµ•¹Ñ•‘€İ…Ñ•È°¥¹™•ÉÉ•‘€‘¥Ù¥Í¥½¸)±•Ù•±Ì½™˜Á•É¥½¹…ÉÉ…Ñ¥Ù”™••Ğ°„½¹©•ÑÕÉ…±€‰…¹¬™…”°„¡…¹¹•°Í•Ñ¥½¸İ¡½Í”¹½Ñ”Í…åÌ)¥Ğ…ÉÉ¥•Ì¹¼•Ù¥‘•¹”…Ğ…±°ƒŠP…¹Í…¥¹½¹”½˜¥ĞÑ¼„Ù¥Í¥Ñ½È°İ¡¥±”‘¥Ñ¡•É¥¹œÕ¹‘•ÈÑ¡”)½¹™¥‘•¹”Ù¥•Ü±¥­”•Ù•ÉåÑ¡¥¹œ•±Í”°İ¡¥ Í¡½İÌÑ¡…Ğ„©Õ‘•µ•¹Ğ•á¥ÍÑÌ…¹¹½Ñ¡¥¹œ…‰½ÕĞ)İ¡…Ğİ…Ì©Õ‘•¸Q¡”Ù¥‘•¹”Á…¹•°¹½Ü…ÉÉ¥•Ì€©Q¡”É½Õ¹å½Ô…É”ÍÑ…¹‘¥¹œ½¸¨è€ÈÀ±…¥µÌ)İ¥Ñ Ñ¡”ÍÁ•ŒÌ½İ¸™¥ÕÉ•Ì°¥ÑÌÉ•…Í½¹¥¹œÙ•É‰…Ñ¥´…¹¥ÑÌ¥Ñ…Ñ¥½¹Ì©½¥¹•°‘•É¥Ù•‰ä)½µÁ¥±•}Í•¹”¹Áå€…¹É”µ‘•É¥Ù•‰ä¡•¬¹Í¡€¸¡•­}Ñ•ÉÉ…¥¹}±…¥µÍ€¡½±‘ÌÑ¡•´Ñ¼Ñ¡”)É•½ÉÌÉÕ±•ÌƒŠPÍ½ÕÉ•ÌÉ•Í½±Ù”°‘½Õµ•¹Ñ•‘€½İ•Ì•Ù¥‘•¹”°¹¼±…¹•±•Ù…Ñ¥½¸µ…ä±…¥´Ñ¼‰”)‘½Õµ•¹Ñ•ƒŠP½™˜Ñ¡”Í…µ”•¹Õµ•É…Ñ¥½¸Ñ¡”Á…¹•°É•¹‘•ÉÌ°Í¼Ñ¡”¡•­•Í•Ğ…¹¹½ĞÍÑ½À‰•¥¹œ)Ñ¡”‘¥ÍÁ±…å•Í•Ğ¸0ÌÈ…¹0ÌÌ…‘µ¥ĞÑ¡”‰…¹¬™…”…¹Ñ¡”¡…¹¹•°ÁÉ½™¥±”°İ¡¥ ¡…Ù”‰••¸)½¹©•ÑÕÉ…°¥¸Ñ¡”‘…Ñ„Í¥¹”Ñ¡”Ñ•ÉÉ…¥¸±…¹‘•…¹İ•É”…‘µ¥ÑÑ•¹½İ¡•É”¸()Qİ¼™½±±½Üµ½¹Ì°‰½Ñ É•…°°‰½Ñ ÍÑ…Ñ•¥¸MQQULƒ
œ€ÌÈÉ…Ñ¡•ÈÑ¡…¸ÅÕ¥•Ñ±ä‘É½ÁÁ•è((´€¨©Q¡É•”±…¥µÌ…É”¥¹™•ÉÉ•‘€İ¥Ñ ¹¼É•…Í½¹¥¹œ…Ğ…±°¨¨ƒŠPÑ¡”¹½ÉÑ …¹İ•ÍĞ‘¥Ù¥Í¥½¸Í½¥±Ì(€…¹Ñ¡”¡…¹¹•°Ì¸=¸„É•½ÉÑ¡…Ğ¥Ì…¸•ÉÉ½Èì¡•É”¥Ğ¥Ì„İ…É¹¥¹œ°‰•…ÕÍ”Ñ¡”¹½Ñ”¡…ÌÑ¼(€¼¥¸Ñ•ÉÉ…¥¹}ÍÁ•Œ¹©Í½¹€°İ¡½Í”€©‰åÑ•Ì¨…É”Ñ¡”Ñ•ÉÉ…¥¸ÌÍÑ…±•¹•ÍÌ¡…Í °Í¼„Í•¹Ñ•¹”Ñ¡…Ğ(€…¹¹½Ğµ½Ù”„Ù•ÉÑ•àÉ”µÍÑ…±•ÌÑ¡”É½Õ¹…¹¹••‘Ì„‰…­”¸€¨©Q¡”Í±¥”Ñ¡…ĞİÉ¥Ñ•ÌÑ¡½Í”Ñ¡É•”(€¹½Ñ•Ì±…¹‘ÌÑ¡”‰…­”İ¥Ñ Ñ¡•´…¹ÑÕÉ¹ÌÑ¡”ÉÕ±”¥¹Ñ¼…¸•ÉÉ½È¸¨¨]½ÉÑ ‘½¥¹œ…ĞÑ¡”Í…µ”Ñ¥µ”è(€Ñ•ÉÉ…¥¹}¥¹ÁÕÑÍ}Í¡…€ÍÑ¥±°¡…Í¡•Ìİ¡½±”™¥±•Ì°İ¡¥ ¥ÌÑ¡”™…±Í”Á½Í¥Ñ¥Ù”MQQULƒ
œ€ÄÔÉ•µ½Ù•(€™É½´Ñ¡”‰Õ¥±‘¥¹œ¡…Í …ÉÉ¥Ù¥¹œ½¸Ñ¡”Ñ•ÉÉ…¥¸Í¥‘”¸(´ùø¨©Q¡”±¥‰•ÉÑ¥•Ì½Ù•É…”…Ñ”…¹¹½ĞÍ•”Ñ¡”Ñ•ÉÉ…¥¸ÍÁ•Œ¸¨©ùø€¨©=9€ÈÀÈØ´Àà´ÄÀ¨¨ƒŠPÍ•”Ñ¡”(€•¹ÑÉä‰•±½Ü¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”É½Õ¹…¹Íİ•ÉÌÑ¼Ñ¡”½Ù•É…”…Ñ”°…¹Ñ¡”™¥ÉÍĞÑ¡¥¹œ¥Ğ…Í­•™½È)İ…Ì…¸¥¹Ù•¹Ñ¥½¸¹½‰½‘ä¡…¹½Ñ¥•¸¨¨Q¡”•¹ÑÉä…‰½Ù”¹…µ•Ì¥ÑÌ½İ¸±¥µ¥ĞèÑ¡”Ñ•ÉÉ…¥¸Ì)¥¹Ù•¹Ñ¥½¹ÌÉ•…¡•Ñ¡”Ù¥‘•¹”Á…¹•°…¹ÍÑ…å•½ÕÑÍ¥‘”Ñ¡”…Ñ”°Í¼0ÌÈ…¹0ÌÌ•á¥ÍÑ•)‰•…ÕÍ”„Á•ÉÍ½¸¹½Ñ¥•¸½Ù•ÉÌé€¹½Ü¡…Ì„Í•½¹¹…µ•ÍÁ…”°Ñ•ÉÉ…¥¸¸ñ•Á½ ø¸ñ±…¥´ù€°)•¹Õµ•É…Ñ•‰äÑ¡”Í…µ”½µÁ¥±•}Í•¹”¹É½Õ¹‘}±…¥µÍ€Ñ¡”Á…¹•°É•¹‘•ÉÌ™É½´…¹µ…Ñ¡•¥¸‰½Ñ )‘¥É•Ñ¥½¹ÌƒŠP…¸Õ¹±…¥µ•½¹©•ÑÕÉ…°É½Õ¹Ù…±Õ”™…¥±Ì°…¹Í¼‘½•Ì„±…¥´½¸„‰±½¬Ñ¡…Ğ¥Ì)¹½Ğ½¹©•ÑÕÉ…°°½¸…¸•Á½ Ñ¡…Ğ¥Ì¹½Ğ½µµ¥ÑÑ•°½È½¸„±…¥´¥Ñ¡”ÍÁ•Œ‘½•Ì¹½ĞÉ…‘”¸()M¥à½¹©•ÑÕÉ…°É½Õ¹±…¥µÌì™¥Ù”¡…ÁÉ½Í”‰•¡¥¹Ñ¡•´€¡0ÄĞµ¥É¼µÉ•±¥•˜°0ÄÔÑ¡”Ñİ¼Íİ…±•Ì°)0ÌÈÑ¡”‰…¹¬™…”°0ÌÌÑ¡”¡…¹¹•°Í•Ñ¥½¸¤…¹…‘‘¥¹œÑ¡•¥È½Ù•ÉÌé€™¥•±‘Ìİ…Ì‰½½­­••Á¥¹œ¸(¨©Q¡”Í¥áÑ ¡…¹½Ñ¡¥¹œ¸¨¨Q¡”¹½ÉÑ µÍ¥‘”Í±½Õ Ì•á¥ÍÑ•¹”…¹½ÕÉÍ”…É”]É¥¡Ğ€ÄàÌĞÌì¥ÑÌ)½¹”µ™½½Ğ‰•…¹€Ä¸È´”µ™½±…É”¥¸Ñ¡”µ½‘•°‰•…ÕÍ”„Í¡…±±½İ•È¡…¹¹•°ÍÑ½ÁÌÉ•…‘¥¹œ…Ì)İ…Ñ•È°…¹¹¼±¥ÍĞµ•¹Ñ¥½¹•Ñ¡•´¸€¨©0ÌĞ¨¨¥Ì¹•Ü¸Q¡¥É¡•¬¥¸Ñ¡¥Ì™…µ¥±äÑ¼™¥¹Í½µ•Ñ¡¥¹œ)½¸¥ÑÌ™¥ÉÍĞÉÕ¸¸()Qİ¼‘•¥Í¥½¹Ì…É”…ÍÍ•ÉÑ•É…Ñ¡•ÈÑ¡…¸…ÍÍÕµ•°…¹‰½Ñ …É”…‰½ÕĞ¹…µ¥¹œ¸Q¡”•Á½ ¥Ì¥¸Ñ¡”)Ñ½­•¸‰•…ÕÍ”‘½Ì½A=!L¹µ‘€Ù•ÉÍ¥½¹ÌÑ¡”É½Õ¹°Í¼„±…Ñ•ÈÍ¡½É•±¥¹”Ì¥¹Ù•¹Ñ¥½¹ÌµÕÍĞ¹½Ğ‰”)‘¥Í¡…É•‰äÑ¡¥Ì½¹”Ì…‘µ¥ÍÍ¥½¸ƒŠPÑ¡”Í•±˜µÑ•ÍĞÁ¥¹ÌÑ¡…Ğ¸¹Ñ¡”Ñ•ÉÉ…¥¸¥Ì¹½Ğµ½‘•±±•…Ì)„ÍÑÉÕÑÕÉ”É•½É…±±•Ñ•ÉÉ…¥¹€èÑ¡”‘½µ…¥¹Ì…É”Í•Á…É…Ñ”½‰±¥…Ñ¥½¹Ì°¹•¥Ñ¡•È‘¥Í¡…É•ÌÑ¡”)½Ñ¡•È°…¹Ñ¡”±…¥´…ÉÉ¥•Ì¥ÑÌ‘½µ…¥¹€É…Ñ¡•ÈÑ¡…¸±•…Ù¥¹œ„É•…‘•ÈÑ¼¥¹™•È¥Ğ™É½´„Ñ½­•¸Ì)Í¡…Á”¸ùù]¡…Ğ¥ÌÍÑ¥±°½ÕÑÍ¥‘”Ñ¡”ÉÕ±”¥ÌÑ¡”É½Õ¹Ì€¨©½µ¥ÍÍ¥½¹Ì¨¨ƒŠPÑ¡•É”¥Ì¹¼Ñ•ÉÉ…¥¸)=9MU5ùøƒŠP€¨©=9€ÈÀÈØ´Àà´ÄÀ°Í•”Ñ¡”•¹ÑÉä‰•±½Ü¨¨ìÑ¡”É…‘•ÌÍÑ…ä‰±½¬µ±•Ù•°°Í¼0ÌĞ)…‘µ¥ÑÌµ½É”Ñ¡…¸Ñ¡”‘…Ñ„‘½•Ì¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”É½Õ¹¡…ÌÑ¼Í…äİ¡…Ğ¥Ğ‘½•Ì¹½Ğ‰Õ¥±°…¹¥Ğ¥Ì¹½Ğµ…‘”½˜İ¡…Ğ¥Ğ)Í…åÌ¥Ğ¥Ìµ…‘”½˜¸¨¨Q¡”•¹ÑÉä…‰½Ù”¹…µ•Ì¥ÑÌ½İ¸±¥µ¥ĞèÑ¡”½Ù•É…”ÉÕ±”™¥É•Ì½¸„)½¹©•ÑÕÉ…±€Ñ…œ°Í¼…¸¥¹Ù•¹Ñ¥½¸İ…Ì‘•µ…¹‘•…¹…¸½µ¥ÍÍ¥½¸±•™Ğ¹¼ÑÉ…”¸Q¡”Ñ•ÉÉ…¥¸¡…Ì„)=9MU5€¹½ÜƒŠPÑ¡”ÍÁ•Œ™¥ÕÉ•ÌÑ•ÉÉ…¥¹}•¸¹‰Õ¥±‘}™¥•±‘€…ÑÕ…±±äÉ•…‘ÌƒŠP…¹)¡•­}É½Õ¹‘}•½µ•ÑÉå€¡½±‘Ì•Ù•Éä½Ñ¡•È™¥ÕÉ”Ñ¡”Ù¥‘•¹”Á…¹•°Í¡½İÌÑ¼„µ•Í é€)‘•±…É…Ñ¥½¸½¸¥ÑÌ‰±½¬°¥¸‰½Ñ ‘¥É•Ñ¥½¹Ì°İ¥Ñ …‰Í•¹Ñ€…¹Í¥µÁ±¥™¥•‘€½İ¥¹œ„½Ù•ÉÌé€)Ñ½­•¸•á…Ñ±ä…ÌÑ¡•ä‘¼½¸„É•½É¸((¨©¥Ù”ÍÕÉ™…”µ…Ñ•É¥…±Ì°Ñİ¼½˜Ñ¡•´‘½Õµ•¹Ñ•‘€°‘•ÍÉ¥‰”„Í½¥°¹¼ÍÕÉ™…”¥¸Ñ¡¥Ìµ½‘•°¥Ì)µ…‘”½˜¸¨¨Q¡”É½Õ¹µ•Í ¥Ì½¹”•…ÉÑ ½±½ÕÈ•‘”Ñ¼•‘”ìÑ•ÉÉ…¥¹}•¸¹Áå€‰Õ¥±‘Ì•±•Ù…Ñ¥½¸)…¹¹½Ñ¡¥¹œ•±Í”¸Q¡…Ğ¥ÌÑ¡”]½±˜A½¥¹Ğİ½±˜Í¥¸½¹”‘½µ…¥¸½Ù•ÈƒŠPÑ¡”ÁÉ½©•ĞÌÍÑÉ½¹•ÍĞ)¡¥À½Ù•ÈÍ½µ•Ñ¡¥¹œ„Ù¥Í¥Ñ½È¥Ì•µÁ¡…Ñ¥…±±ä¹½Ğ±½½­¥¹œ…ĞƒŠP…¹0ÌÔ¥Ìİ¡•É”¥Ğ¥Ì…‘µ¥ÑÑ•¸)Q¡”É½İÌÍ…ä€©¹½Ğµ½‘•±±•™É½´Ñ¡¥Ì¨°¥¸Ñ¡”ÁÉ½Ù•¹…¹”…ÉÌİ½É‘Ì°½ÕĞ½˜Ñ¡”ÁÉ½Ù•¹…¹”)…ÉÌµ½‘Õ±”€¡É•¹‘•É•ÉÌ½İ•ˆ½©Ì½•½µ•ÑÉä¹©Í€°¹½ÜÍ¡…É•‰ä‰½Ñ ÍÕÉ™…•Ì¤¸½±½ÕÉ¥¹œÉ½Õ¹‰ä)é½¹”¥Ì€¨©LØ¨¨…¹Ñ¡”‘•±…É…Ñ¥½¸½µ•Ì½™˜Ñ¡”‘…äÑ¡”•¹•É…Ñ½ÈÉ•…‘ÌÑ¡”Ù…±Õ”¸()Q¡É•”Ñ¡¥¹Ìİ½ÉÑ …ÉÉå¥¹œ°…±°½˜Ñ¡•´…‰½ÕĞİ¡•É”„‘•±…É…Ñ¥½¸µ…ä±¥Ù”è((´€¨©Ñ•ÉÉ…¥¹}¥¹ÁÕÑÌ¹=9MU5€°¹½ĞÑ•ÉÉ…¥¹}•¸¹=9MU5€¸¨¨¸…É¡•ÑåÁ”‘•±…É•Ì¥ÑÌ½¹ÍÕµ•(€Í•Ğ‰•Í¥‘”Ñ¡”½‘”Ñ¡…ĞÉ•…‘Ì¥Ğ°…¹Ñ¡…Ğ½¹±äİ½É­Ì‰•…ÕÍ”„Á…É…µÌµ½‘Õ±”Ì‰åÑ•Ì…É”½ÕĞ(€½˜Ñ¡”‰Õ¥±‘¥¹œ¡…Í ¸Ñ•ÉÉ…¥¹}•¸¹Áå€½•Ì¥¹Ñ¼Ñ¡”É½Õ¹Ì¡…Í İ¡½±”°Í¼Ñ¡”µ…ÀÉ”µÍÑ…±•(€Ñ¡”Ñ•ÉÉ…¥¸½¸Í¥¡Ğ…¹…Í­•™½È„	±•¹‘•È‰…­”Ñ¼±…¹„½¹ÍÑ…¹Ğ¸%ĞÍ¥ÑÌ‰•Í¥‘”Ñ¡”(€‘•¹å±¥ÍĞ¥¹ÍÑ•…ƒŠPÍ…µ”™¥±”°Í…µ”ÍÕ‰©•ĞƒŠP…¹Ñ•ÍÑ}‘•±…É•‘}Ñ•ÉÉ…¥¹}É•…‘Í}…É•}É•…±}É•…‘Í€(€Í…¹ÌÑ¡”•¹•É…Ñ½È™½È„É•…½˜•Ù•Éä‘•±…É•­•ä°İ¡¥ ¥Ìİ¡…Ğ¼µ±½…Ñ¥½¸İ½Õ±¡…Ù”(€‰½Õ¡Ğ¸(´€¨©Q¡”­•ä¥Ìµ•Í¡€‰•…ÕÍ”•½µ•ÑÉå€¥ÌÑ…­•¸¸¨¨%¸„•½)M=8Ñ¡…Ğİ½É¥ÌÑ¡”½½É‘¥¹…Ñ•Ìì(€ÍÑÉ¥ÁÁ¥¹œ¥Ğ™É½´Ñ¡”¡…Í İ½Õ±¡…Ù”Ñ…­•¸•Ù•ÉäÑÉ…•‰…¹¬±¥¹”½ÕĞ½˜Ñ¡”É½Õ¹Ì(€ÍÑ…±•¹•ÍÌ¸Ñ•ÍĞİÉ¥ÑÑ•¸™½Èƒ
œ€ÌĞÌÁÕÉÁ½Í”É•™ÕÍ•¥Ğ½¸Ñ¡”™¥ÉÍĞÉÕ¸¸(´€¨©É•ÍÑ…Ñ•‘}¥¹}½‘•€¥Ì„™½ÕÉÑ ÍÑ…Ñ”…¹½¹±äÑ¡”É½Õ¹¹••‘Ì¥Ğ¸¨¨Q¡”İ…Ñ•ÈÁ±…¹”Ìé•É¼(€…¹Ñ¡”‰…¹¬Ì•…Í”µ½ÕĞ…É”İÉ¥ÑÑ•¸¥¸Ñ¡”ÍÁ•Œ…¹Í•Á…É…Ñ•±äİÉ¥ÑÑ•¸¥¸AåÑ¡½¸¸Q¡”µ•Í (€…É••Ìİ¥Ñ Ñ¡•´…¹‘½•Ì¹½ĞÉ•…Ñ¡•´ìÑ¡…Ğ¥Ì„İ…É¹¥¹œÑ¼İ¡½•Ù•È•‘¥ÑÌÑ¡”•¹•É…Ñ½ÈÉ…Ñ¡•È(€Ñ¡…¸„…Ù•…ĞÑ¼„Ù¥Í¥Ñ½È°Í¼¥Ğ…ÉÉ¥•Ì¹¼µ…É­•È¸€¨©]¡…Ğ¡•±Ñ¡”Ñİ¼¡…±Ù•ÌÑ½•Ñ¡•Èİ…Ì(€¹½Ñ¡¥¹œ°…¹Í¥¹”€ÈÀÈØ´Àà´ÄÀ€¡MQQULƒ
œ€ÌØ¤¥Ğ¥ÌÑ•ÉÉ…¥¹}¥¹ÁÕÑÌ¹IMQQM€¨¨è•… É•ÍÑ…Ñ•µ•¹Ğ(€¹…µ•ÌÑ¡”¡…±˜¥Ğ…É••Ìİ¥Ñ ƒŠP„™¥ÕÉ”¥¸Ñ¡”¡•¥¡Ñ™¥•±Ñ¡”‰…­”İÉ½Ñ”°…¹½Ñ¡•È™¥ÕÉ”¥¸(€Ñ¡”Í…µ”‰±½¬°½È„±¥¹”½˜Ñ•ÉÉ…¥¹}•¸¹Áå€ƒŠP…¹¡•­}É•ÍÑ…Ñ•‘}…É••µ•¹Ñ€½µÁ…É•ÌÑ¡•´¸(€Mİ¥Ñ¡¥¹œ¥Ğ½¸™½Õ¹Ñ¡É•”™¥ÕÉ•Ìµ…­¥¹œÑ¡”ÁÉ½µ¥Í”Õ¹‘•ÈÑ¡”İÉ½¹œÍÑ…Ñ”è•Ù•Éä‘¥Ù¥Í¥½¸Ì(€‰…¹­}É•ÍÑ}™Ñ€É•ÍÑ…Ñ•Ì¹•…É}™Ñ€…¹İ…Ì‘•±…É•É•½É‘}½¹±å€°İ¡¥ ½İ•Ì¹½Ñ¡¥¹œ…¹…Í­Ì(€¹½Ñ¡¥¹œ¸±°Í•Ù•¸…É•”Ñ½‘…äìÑ¡”Ù…±Õ”¥ÌÑ¡…ĞÑ¡”¹•áĞ•‘¥ĞÑ¼„‘¥Ù¥Í¥½¸±•Ù•°…¹¹½Ğ±•…Ù”(€Ñ¡”Á…¹•°Í¡½İ¥¹œÑ¡”½±É•ÍĞ¸((¨©½¹”€ÈÀÈØ´Àà´ÄÀƒŠPÑ¡”ÍÕ´Õ¹‘•È™¥Ù”‰Õ¥±‘¥¹Ì¥Ì‘…Ñ„¹½Ü°…¹¥Ğİ…Ì™¥Ù”Á…É…É…Á¡Ì¸¨¨Ù•Éä)…Ñ”…‰½Ù”…Í­Ìİ¡•Ñ¡•È„±…¥´¥Ì¡½¹•ÍĞìÑ¡¥Ì½¹”…Í­Ìİ¡•Ñ¡•ÈÑ¡”…É¥Ñ¡µ•Ñ¥Œ‰•¹•…Ñ „)½½É‘¥¹…Ñ”İ…Ì•Ù•ÈÉ•‘½¹”¸¥Ù”Á±…•µ•¹ÑÌ…É”Ñ¡”Í…µ”½¹ÍÑÉÕÑ¥½¸ƒŠP„µ½‘•É¸¥¹Ñ•ÉÍ•Ñ¥½¸)•¹ÑÉ”½™˜=Á•¹MÑÉ••Ñ5…À°¡…±˜…¸€àÀ™ĞÁ±…ÑÑ•ÍÑÉ••ĞÑ¼Ñ¡”­•Éˆ°„¹…µ•™…”½¸¥ĞƒŠPİÉ¥ÑÑ•¸)½ÕĞ½¹”Á•ÈÉ•½É°İ¥Ñ Ñ¡”¹Õµ‰•È€ÄÈ¸È…ÁÁ•…É¥¹œ¥¸™¥Ù”Á…É…É…Á¡Ì…¹¹¼™¥±”¸)‘…Ñ„½ÑÉ…•Ì½ÍÑÉ••Ñ}½¹ÑÉ½°¹©Í½¹€¡½±‘ÌÑ¡”µ½‘Õ±”…¹Ñ¡”½¹ÑÉ½°½¹”ì)¡•­}Á½Í¥Ñ¥½¹}‘•É¥Ù…Ñ¥½¹Í€É•‰Õ¥±‘Ì•Ù•ÉäÁ±…•µ•¹Ğ™É½´Ñ¡•´…¹¡½±‘ÌÑ¡”É•ÍĞÑ¼„)‘•±…É…Ñ¥½¸ì…¹Ñ¡”ÍÕµÌİ•É”…±°½ÉÉ•Ğ°İ¡¥ ¥ÌÑ¡”±•…ÍĞ¥¹Ñ•É•ÍÑ¥¹œÁ…ÉĞ¸()Q¡É•”Ñ¡¥¹Ìİ½ÉÑ …ÉÉå¥¹œè((´€¨©Í¬Ñ¡”Á±…•Í¡…Á”°¹½ĞÑ¡”½½É‘¥¹…Ñ”¸¨¨É•½ÉÌÁ½Í¥Ñ¥½¸¥ÌÑ¡”™½½ÑÁÉ¥¹ĞÁ½±å½¸Ì½İ¸(€½É¥¥¸°Í¼„™……‘”‰•…É¥¹œÑÕÉ¹Ì¥Ğ½™˜Ñ¡”½É¹•ÈÑ¡”±…¥´¥Ì…‰½ÕĞƒŠPÑ¡”É••¸QÉ•”Ì(€•…ÍÑ¥¹œÍ¥ÑÌ€ÈĞ¸Ğ´™É½´¥ÑÌ¥¹Ñ•ÉÍ•Ñ¥½¸İ¡•É”Ñ¡”±…¥´Í…åÌ€ÄÈ¸È¸¡•¬½µÁ…É¥¹œ(€½½É‘¥¹…Ñ•ÌÑ¼­•É‰ÌÁ…ÍÍ•Ì„½ÉÉ•Ñ±äÁ±…•‰Õ¥±‘¥¹œ…¹„É½Ñ…Ñ•µ½ÕĞµ½˜µ¥ÑÌµ±½Ğ‰Õ¥±‘¥¹œ(€İ¥Ñ •ÅÕ…°½¹™¥‘•¹”°Í¼Ñ¡”Í•±˜µÑ•ÍĞÌ‘¥ÍÉ¥µ¥¹…Ñ¥¹œ…Í”¥Ì½¹”‰Õ¥±‘¥¹œ…ÁÁ•…É¥¹œÑİ¥”¸(´€¨©‘¥Í…É••µ•¹Ğå½Ô…¹¹½Ğ…Ğ½¸•ÑÌÉ•½É‘•…¹±•™Ğ¸¨¨Q¡”€àÀ™Ğ€¼€ØØ™ĞÍÑÉ••Ğİ¥‘Ñ (€€¡‘½Ì½IMI ½¡½…¹}ÍÑ½É”¹µ‘€ƒ
œ€Ô¤Í…Ğ‰•…ÕÍ”Í•ÑÑ±¥¹œ¥Ğµ•…¹Ğ™¥Ù”¡…¹µÉ•‘½¹”ÍÕµÌ¸%Ğ¥Ì(€¹½Ü½¹”•‘¥Ğ…¹„ÁÉ¥¹Ñ•±¥ÍĞ½˜İ¡¥ ‰Õ¥±‘¥¹Ìµ½Ù•°€È¸ÄÌ´•… ¸(´€¨©]É¥Ñ¥¹œÑ¡”½¹ÑÉ½°‘½İ¸™½Õ¹Ñİ¼½½É‘¥¹…Ñ•Ì™½È½¹”©Õ¹Ñ¥½¸¨¨ƒŠP…¹…°…¹-¥¹é¥”°…Ù•É…•(€½Ù•È™¥Ù”=M4¹½‘•Ì™½ÈÑ¡”•½É•™•É•¹”…¹Ñ¡É•”™½ÈÑ¡”‰É¥‘”°€Ì¸à´…Á…ÉĞ¸Q¡”‰É¥‘”¥Ì(€¹½Ğµ½Ù•è¥ÑÌÍÁ…¸¥ÌÑ¡”‘¥ÍÑ…¹”‰•Ñİ••¸Ñ¡”ÑÉ…•‰…¹­Ì…±½¹œ¥ÑÌ•¹ÑÉ•±¥¹”°Ñ¡…Ğ‘¥ÍÑ…¹”(€¥Ì„µ•Í Á…É…µ•Ñ•È°…¹É”µ‘•É¥Ù¥¹œ¥Ğ…Í­Ì™½È„‰…­”¸Q¡”Ù…É¥…¹”¥Ì‘•±…É•…¹¡•­•(€¥¹ÍÑ•…¸M•”‘½Ì½IMI ½ÍÑÉ••Ñ}µ½‘Õ±•|ÄàÌÀ¹µ‘€¸(´€¨©Q¡”½¹ÑÉ½°Á½¥¹ĞÑ¡”İ¡½±”İ•ÍĞ‘¥Ù¥Í¥½¸¥Ìµ•…ÍÕÉ•™É½´¥Ì¥¹Í¥‘”„‰±½¬¨¨€ ÈÀÈØ´Àà´ÄÀ°(€MQQULƒ
œ€ĞÈ¤è!…Ñ¡…İ…ä!¥Ì€ÔÈ¸Ğ´İ•ÍĞ½˜Ñ¡”…¹…°MÑÉ••Ğ½ÉÉ¥‘½È…¹]É¥¡ĞÔ€ÈÀ¸È´İ•ÍĞ°(€‰½Ñ İ¥Ñ ‰±½¬€ÈàÌ¹Õµ‰•ÈÁÉ¥¹Ñ•…É½ÍÌÑ¡•´¸Ô¥Ì„‘…ÑÕ´@°Í¼Ñ¡”•áÁ½ÍÕÉ”¥ÌÁÉ¥•(€€ ÄÔ¸À´½˜½É¥¥¸µ½Ù•µ•¹Ğ°I5LÕ¹¡…¹•¤…¹ÅÕ•Õ•É…Ñ¡•ÈÑ¡…¸Ñ…­•¸ƒŠP…‘½ÁÑ¥¹œ¥ĞÉ”µ‘•É¥Ù•Ì(€•Ù•Éä½½É‘¥¹…Ñ”…¹ÍÑ…±•Ì•Ù•Éäµ•Í ¸¡•­}ÍÑÉ••Ñ}µ½‘Õ±•€™…¥±ÌÑ¡”‘…ä•¥Ñ¡•È½ÉÉ•Ñ¥½¸(€±…¹‘Ì°‰•…ÕÍ”Ñ¡”™¥¹‘¥¹œÌ¥¹ÁÕÑÌİ½Õ±¡…Ù”µ½Ù•¸(´€¨©¹É”µ™•Ñ¡¥¹œÑ¡”½¹ÑÉ½°Ñ¡”¹•áĞ‘…äÍ…¥İ¡¥ ½˜Ñ¡”Ñİ¼İ…ÌÉ¥¡Ğ¨¨€ ÈÀÈØ´Àà´ÄÀ°(€MQQULƒ
œ€Ìä¤¸©Õ¹Ñ¥½¸¥ÌÑ¡”¹½‘•ÌÍ¡…É•‰äÑ¡”Ñİ¼¹…µ•€©ÍÕÉ™…”É½…‘İ…åÌ¨ìÑİ¼½˜-¥¹é¥”(€…¹…¹…°Ì™¥Ù”½µµ¥ÑÑ•¹½‘•Ì…É”‰¥­•İ…äÉ½ÍÍ¥¹Ì°…¹Ñ¡”½Ñ¡•ÈÑ¡É•”…É”Ñ¡”‰É¥‘”Ì(€É•…‘¥¹œÑ¼„•¹Ñ¥µ•ÑÉ”¸Q¡”Í…µ”¥¹±ÕÍ¥½¸¡…ÁÕĞI…¹‘½±Á …¹…¹…°€Ğ¸ĞĞ´½ÕĞ°İ¡¥ µ½Ù•(€Ñ¡”]•ÍÑ•É¸!½Ñ•°¸Ñ½½±Ì½É•™•Ñ¡}½¹ÑÉ½°¹Áå€É”µ‘•É¥Ù•Ì„©Õ¹Ñ¥½¸™É½´Ñ¡”ÍÑÉ••Ğ¹…µ•Ì…¹(€É”µ™•Ñ¡•ÌÑ¡”É•½É‘•¹½‘”¥‘Ìì¥Ğ¹••‘ÌÑ¡”¹•Ñİ½É¬°Í¼¥Ğ¥Ì½¸µ‘•µ…¹…¹¹½Ğ¥¸(€Ñ½½±Ì½¡•¬¹Í¡€¸((ŒŒLÄÀƒŠP½µÁ±•Ñ”)Õ±ä€ÄàÌÔ‰Õ¥±‘¥¹œ¥¹Ù•¹Ñ½Éäƒ
Ü€¨©I=9%1€ÈÀÈØ´Àà´ÄĞ¨¨()Q¡”½İ¹•ÈµÍÕÁÁ±¥•É•½¹ÍÑÉÕÑ¥½¸ÍÁ•¥™¥…Ñ¥½¸•ÍÑ…‰±¥Í¡•Ì„ÁÉ½‘ÕÑ¥½¸Ñ…É•Ğ½˜€¨¨ØØÔÉ½½™Ì¨¨è(ÔÄÄÁÉ¥¹¥Á…°½™Õ¹Ñ¥½¹…°…¹€ÄÔĞ…¹¥±±…Éä°‘¥ÍÑÉ¥‰ÕÑ•M½ÕÑ €ÌÜÀ€¼]•ÍĞ€ÄÌÔ€¼9½ÉÑ €ÄÔÀ€¼½ÉĞ(ÄÀ¸Q¡”‘ÕÉ…‰±”µ…ÍÑ•È±•‘•È¥Ì‘…Ñ„½É•½¹ÍÑÉÕÑ¥½¸¼ÄàÌÕ}‰Õ¥±‘¥¹}¥¹Ù•¹Ñ½Éä¹©Í½¹€ì¥ĞÁÉ•Í•ÉÙ•Ì)Ñ¡”¥¹‘•Á•¹‘•¹Ñ±äÉ•½¹¥±…‰±”™…µ¥±ä…¹‘¥ÍÑÉ¥Ğµ…ÑÉ¥•Ì…¹•áÁ±¥¥Ñ±äÍ•Á…É…Ñ•Ì…É•…Ñ”)µ½‘•É…Ñ”½¹™¥‘•¹”™É½´¥¹Ñ•ÉÁÉ•Ñ¥Ù”Á•Èµ¥¹ÍÑ…¹”Á±…•µ•¹Ğ¸€¨©Q¡…Ğ™¥±”¥ÌÑ¡”QIP…¹‘½•Ì)¹½Ğµ½Ù”¸¨¨]¡…Ğ¡…Ì‰••¸‰Õ¥±Ğ……¥¹ÍĞ¥Ğ°İ¡…Ğ¥Ì±•™Ğ…¹İ¡•É”¥Ğ…¸¼…É”‘•É¥Ù•ƒŠP)Ñ½½±Ì½É•½¹¥±•|ØØÔ¹Áå€ƒŠH‘…Ñ„½É•½¹ÍÑÉÕÑ¥½¸¼ÄàÌÕ|ØØÕ}É½½™}ÁÉ½É…µµ”¹©Í½¹€°É”µ‘•É¥Ù•‰ä)Ñ½½±Ì½¡•¬¹Í¡€½¸•Ù•Éä½µµ¥Ğ€¡PµÄ¤¸((¨©MÑ…¹‘¥¹œ€ÈÀÈØ´Àà´ÄĞè€ÈÌÈÁ¡åÍ¥…°É½½™Ì™É½´€ÈĞÈÉ•½É‘Ì¸I•µ…¥¹¥¹œè€ĞÌÌ¨¨ƒŠPM½ÕÑ €ÈÜÀ°)]•ÍĞ€äĞ°9½ÉÑ €Øä°½ÉĞ€À¸=˜Ñ¡½Í”€ĞÌÌ°€¨¨ÄÀÔ¡…Ù”µ½‘•±±•°Á±…ÑÑ•É½Õ¹Ñ¼ÍÑ…¹½¸¨¨…¹(ÌÈà‘¼¹½Ğè€ÈÀ¥¸Ñ¡”Ñİ¼‰±½­ÌÑ¡”Á±…Ğµ½‘Õ±”É•™ÕÍ•Ì™½Èİ…¹Ğ½˜M½ÕÑ ]…Ñ•ÈÍÑÉ••Ğ½¹ÑÉ½°°(ÌÔ¡•±‰äÑ¡”]•ÍĞÉ•¥Á”Ì½İ¸•áÑ•¹Í¥½¸…Ñ”°…¹€ÈÜÌ¥¸É½Õ¹İ¥Ñ ¹¼½µµ¥ÑÑ•ÍÑÉ••Ğ)½¹ÑÉ½°…Ğ…±°ƒŠP•…ÍĞ½˜MÑ…Ñ”°Í½ÕÑ ½˜]…Í¡¥¹Ñ½¸°İ•ÍĞ½˜±¥¹Ñ½¸°…¹Ñ¡”İ¡½±”9½ÉÑ )¥Ù¥Í¥½¸°İ¡¥ Ñ¡”É¥½Ù•ÉÌ‰ä¹½Ğ½¹”‰±½¬¸Q¡”€ØØÔµÉ½½˜ÁÉ½É…µµ”¥Ì€¨©½Ù•É…”µ‰½Õ¹°)¹½ĞÉ•¥Á”µ‰½Õ¹¨¨ìƒ
œLä¥Ìİ¡…ĞÍÑ…¹‘Ì‰•Ñİ••¸¥Ğ…¹Ñ¡”¹•áĞÑİ¼¡Õ¹‘É•É½½™Ì¸()M¥à™…µ¥±äÑ…É•ÑÌ…É”…±É•…‘ä•á••‘•‰ä•Ù¥‘•¹”ƒŠPÄ°$È°PÈ°\Ä°\Ğ…¹\Ô°¹¥¹”É½½™ÌƒŠP)İ¡¥ Ñ¡”±•‘•ÈÉ•Á½ÉÑÌÉ…Ñ¡•ÈÑ¡…¸¡¥‘•Ì¸‘½Õµ•¹Ñ•É½½˜¥Ì¹•Ù•ÈÉ•µ½Ù•Ñ¼ÁÉ½Ñ•Ğ„)™…µ¥±ä…À°Í¼Ñ¡”¹¥¹”½µ”½ÕĞ½˜Ñ¡”¥¹Ù•¹Ñ•™…µ¥±äİ¥Ñ Ñ¡”µ½ÍĞÍ±…¬¸((´€¨©A¡…Í”€Ä‘½¹”è¨¨€ĞàÙ¥Í¥‰±äÑ…•…¹½¹åµ½ÕÌM½ÕÑ ¥Ù¥Í¥½¸É½½™Ì¥¸™¥Ù”µ¥á•‰±½­ÏŠPĞÀ(€ÁÉ¥¹¥Á…°½™Õ¹Ñ¥½¹…°…¹•¥¡Ğ…¹¥±±…Éä¸I•ÁÉ½‘Õ¥‰±”É•½É‘Ì…¹™±…•É•Ù¥•Ü1	Ì…É”(€‘•É¥Ù•™É½´Ñ¡”Á…É•°É•¥Á”İ¥Ñ¡½ÕĞ	±•¹‘•È…¹¡•­•½¸•Ù•Éä½µµ¥Ğ¸(´€¨©A¡…Í”€ÈÁ±…¹¹¥¹œ…‘Ù…¹•¥¸Á…É…±±•°è¨¨É•Ù¥•İ•°¹½¸µÉ•¹‘•É•É•¥Á•Ì¹½ÜÉ•Í•ÉÙ”…¹½Ñ¡•È(€€àĞM½ÕÑ É½½™Ì°€ÔÔ]•ÍĞÉ½½™Ì…¹€ØÀ9½ÉÑ É½½™Ìİ¥Ñ¡½ÕĞ½Ù•É‘É…İ¥¹œ…¹ä™…µ¥±äÑ…É•Ğ¸Q¡”(€M½ÕÑ É•¥Á”¥Ì½±±¥Í¥½¸µ¡•­•……¥¹ÍĞÁÉ½Ñ•Ñ•¹…µ•Í¥Ñ•ÌìÑ¡”9½ÉÑ Í•ĞÌ€ØÀ™½½ÑÁÉ¥¹ÑÌ(€ÍÑ…ä½¸Ñ¡”ÕÉÉ•¹Ğ‘ÉäÑ•ÉÉ…¥¸¸Q¡”]•ÍĞÉ•¥Á”‘•±¥‰•É…Ñ•±ä…Ñ•Ì€ÌÔÉ½½™ÌÕ¹Ñ¥°Ñ¡”İ½É±(€•áÑ•¹‘ÌÑ¼±½…°€´ÜÀÀ´°…¹Ñ¡”É•µ…¥¹¥¹œ€äÀµÉ½½˜9½ÉÑ Á…ÍÌİ…¥ÑÌ™½ÈÕ¹¥™¥•Ñ•ÉÉ…¥¸°(€¡å‘É½±½ä°½±±¥Í¥½¸°™±½É„°ÍÑÉ••ÑÌ…¹µ…À½Ù•É…”Ñ¼8€¬ÜØÀ´¸Q¡•Í”…É”ÁÉ½‘ÕÑ¥½¸Á±…¹Ì°(€¹½Ğ…‘‘•Í•¹”½Õ¹Ğì•á¥ÍÑ¥¹œµÉ½½˜É•½¹¥±¥…Ñ¥½¸½µ•Ì™¥ÉÍĞ¸(´€¨©½¹”€ÈÀÈØ´Àà´ÄÈè¨¨…±°€ÜØÁÉ”µ•á¥ÍÑ¥¹œÉ•½É‘Ì…É”É•½¹¥±•Ñ¼Á¡åÍ¥…°É½½˜Õ¹¥ÑÌì‰É¥‘•Ì°(€å…É‘Ì°Á…±¥Í…‘•Ì°½¹ÍÑÉÕÑ¥½¸Í¥Ñ•Ì…¹½µÁ½Õ¹‘Ì¹¼±½¹•Èµ…­”É•½É½Õ¹Ğ„ÁÉ½áä¸(´€¨©½¹”€ÈÀÈØ´Àà´ÄÈè¨¨Ñ¡”Ñ•ÉÉ…¥¸µÍ…™”€ØÀµÉ½½˜9½ÉÑ ¥¹¥Ñ¥…°Á…É•°¥ÌÙ¥Í¥‰±”…¹¡•­•¸(´Y•É¥™äÑ¡”½ÕÁ¥•İ•ÍĞ½¹½ÉÑ Í•ÑÑ±•µ•¹Ğ•áÑ•¹Ğ‰•™½É”•áÑ•¹‘¥¹œÑ•ÉÉ…¥¸¸Q¡”•¹±…É•Á±…Ğ(€¥Ì¹½ĞÑ¡”Í…µ”Ñ¡¥¹œ…Ì‰Õ¥±Ğ™½½ÑÁÉ¥¹Ğ°…¹…Ğ±•…ÍĞ€ĞÔ”½˜¥ĞÉ•µ…¥¹ÌÍÁ…ÉÍ”½½Á•¸¸(´%µÁ±•µ•¹ĞÑ¡”€ÌÔ™…µ¥±ä…É¡•ÑåÁ•Ì…¹€ÈÔÀ¬Ù¥Í¥‰±”½µ‰¥¹…Ñ¥½¹Ì°É•Á±…¥¹ŸŠQ¹½ĞÍ¥±•¹Ñ±ä(€ÁÉ½µ½Ñ¥¹ŸŠQÑ¡”É•Ù¥•Üµ…ÍÍ¥¹Ì¸(´A½ÁÕ±…Ñ”É•µ…¥¹¥¹œ‘¥ÍÑÉ¥ĞÁ…É•±ÌÑ¼Ñ¡”É•½¹¥±•Ñ…É•Ğ°Ñ¡•¸…‘Ñ•ÉÉ…¥¸µÍ…µÁ±•(€™½Õ¹‘…Ñ¥½¹Ì°å…É‘Ì…¹ÁÉ½ÁÌ¸9¼Í•Á…É…Ñ”½±±¥Í¥½¸Á±…¹”¸()M•”‘½Ì½IMI ½É•½µµ•¹‘•‘}¥¹™¥±±|ÄàÌÔ¹µ‘€°)‘½Ì½IMI ¼ÄàÌÕ}•á¥ÍÑ¥¹}É½½™}É•½¹¥±¥…Ñ¥½¸¹µ‘€°)‘½Ì½IMI ¼ÄàÌÕ}™…µ¥±å}…É¡•ÑåÁ•}É½ÍÍİ…±¬¹µ‘€°)‘½Ì½IMI ½Á¡…Í”É}Í½ÕÑ¡}½É•}…¹‘}µ¥á•¹µ‘€°)‘½Ì½IMI ½İ•ÍÑ}‘¥Ù¥Í¥½¹}¥¹™¥±±|ÄàÌÔ¹µ‘€°…¹1¥‰•ÉÑä0àÄ¸)Q¡”9½ÉÑ …¹…±åÍ¥Ì¥Ì‘½Ì½IMI ¼ÄàÌÕ}¹½ÉÑ¡}‘¥Ù¥Í¥½¹}•áÑ•¹Ñ}…¹‘}¥¹™¥±°¹µ‘€¸((ŒŒLàƒŠP5¥±•ÍÑ½¹”€Ä()]½±˜A½¥¹Ğ±ÕÍÑ•È€¬M½ÕÑ ]…Ñ•È‰±½¬€¡1…M…±±—ŠM±…É¬¤¸Q¡”™¥ÉÍĞÑ•ÍĞ½˜İ¡•Ñ¡•ÈÑ¡”)…É¡•ÑåÁ”…ÁÁÉ½… …ÑÕ…±±äÁ…åÌ™½È¥ÑÍ•±˜¸((ŒŒ1…Ñ•ÈƒŠPÑ¡”€ÑÁÉ½½˜()Í•½¹Í•¹”€ ÄàÌÌ½È€ÄàÌÀ¤•á•É¥Í¥¹œÑ¡”•Á½ µ…¡¥¹•Éä°Ñ¡”ÁÉ•}™¥É•}ØÅ€É½ÍÍİ…±¬°…¹)„5…¹…•ÈÉ½Üİ¥Ñ Ñ¡”¡…¹•±½œ…‘•¹”ÉÕ¹¹¥¹œ¸((´´´((ŒŒ]½É­¥¹œ¹½Ñ•Ì((´Ñ½½±Ì½¡•¬¹Í¡€‰•™½É”•Ù•Éä½µµ¥Ğ¸%ĞÑ…­•ÌÕ¹‘•È„Í•½¹¸(´=¹”½¡•É•¹ĞÕ¹¥Ğ½˜İ½É¬Á•ÈÉÕ¸¸(´]É¥Ñ¥¹œÍÕ‰…•¹ÑÌ•… •ĞÑ¡•¥È½İ¸¥Ğİ½É­ÑÉ•”¸(´UÁ‘…Ñ”MQQUL¹µ‘€¥¸Ñ¡”Í…µ”½µµ¥Ğ…ÌÑ¡”İ½É¬°…¹­••À¥ĞÕ¹™±…ÑÑ•É¥¹œ¸(´9¼µ½‘•°¥‘•¹Ñ¥™¥•ÉÌ¥¸É•Á¼…ÉÑ¥™…ÑÌ¸(