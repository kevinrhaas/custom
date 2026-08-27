# ROADMAP

The build order and the work parcels. `docs/PLAN.md` carries the full reasoning; this is the
operational view — what to pick up next, and what it depends on.

```
S0 scaffold ─┬─► S1 georeference + datum ──► S2 terrain e1834 ──► S3 M0 Sauganash walkable
   [DONE]     │        [DONE]
              ├─► R1 renderer shell (synthetic geometry) ────────┘
              ├─► P1 research dossiers (read-only) ──► S5 structure records ──► S8 M1
              └─► S4 archetype generators (golden params) ──────► S5 bakes
S2 ──► S6 flora + fauna ──► S7 polish, audio, perf ──► release sweep
```

**Critical path: S1 → S2 → S3.** The datum gates every coordinate in the project. Work that does
not need coordinates is deliberately structured to proceed in parallel.

---

## THE OVERNIGHT LANES — 2026-08-14 · **START HERE**

Two lanes, opened on the owner's instruction of 2026-08-14 alongside the activation of
`docs/RENDERING.md` and the `dev` → `main` pipeline. Everything below:

- **targets `dev`.** Branch `steward/<topic>` off `dev`, PR into `dev`, merge when the dev
  gate is green. Production moves only when the owner dispatches
  `chicago-4d-promote-to-prod.yml`. See `docs/PIPELINE.md`.
- **is ONE parcel per run.** Claim it first (the K16-style heading below), check `git log`
  and open PRs, then work only inside your parcel's file list.
- **is disjoint by construction.** Lane 1 touches renderer and tool files; lane 2 touches
  data and docs. **They cannot collide**, so one of each may run at the same time. Two
  parcels from the SAME lane may not.
- **stays vocabulary-agnostic on confidence names while K16 is in flight.** Name the three
  levels by function — source-attested, reasoned-from-specific-evidence,
  invented-to-fill-a-need — and read `docs/PROVENANCE.md` at your arrival date for the
  current strings.
- **never installs Blender.** Geometry arrives via the nightly `chicago-4d-bake.yml`, which
  now branches off `dev` and PRs into `dev`. A parcel needing new geometry ships the
  data/archetype half and says so.

### THE RUN BUDGET IS 150 MINUTES, AND THE SMOKE COSTS 26 OF THEM

Set 2026-08-14 on the owner's instruction — *"if it's too long we will want to break it into
pieces"* — after a run was cancelled at exactly 150 minutes having committed nothing.

**The arithmetic, measured rather than estimated.** `steward-improve` allows 150 minutes
(raised from 90 that day, because runs of 95, 81 and 70 minutes were real work being destroyed
at the ceiling). One `tools/smoke_renderer.mjs` pass costs **~26 minutes** at both viewports.
`tools/critic_shots.mjs --metrics` costs ~12 minutes for the full station set, ~3 with
`--stations`. So a parcel gets **roughly four smoke-equivalents in total**, and it also has to
read, think, write, publish and open a PR inside that.

**The rule: a parcel whose acceptance needs more than TWO full smoke passes must be split
before it is claimed.** Measure-then-fix parcels are the ones that breach this, and they split
along a seam they already have:

- **(a) land the failing gate** — build the measurement, prove it fails on the current build,
  commit it red with the numbers quoted. One smoke.
- **(b) fix it green** — take (a)'s committed numbers as the baseline. One smoke.

This is better than a time-saving trick: it forces the measurement to be committed *before*
anyone knows which candidate cause is guilty, so the fix cannot quietly redefine success. It
is exactly how R-BUG2 succeeded — *"measure before choosing"* refuted its own prime suspect.

**Use `--stations` and `SMOKE_VIEWPORT`.** `critic_shots.mjs --stations a,b,c` runs in about
2 minutes instead of 13; the smoke takes `SMOKE_VIEWPORT=desktop` for a single viewport while
iterating. Full runs belong at the end, not in the loop. (**Corrected 2026-08-15 by R-W4a**:
this paragraph promised a `--stations` flag that did not exist and a `--only` flag the smoke
does not have, so every run that took the advice ran the full set. `--stations` exists now and
was measured at 2 min 03 s for three desktop stations. The full both-viewport `--metrics` run
now costs 13 min with R-W4a's second capture.)
**Updated 2026-08-15 by R-W4c(a), which added a THIRD capture (flower heads hidden).** Measured
on the same three desktop stations: **3 min 45 s**, against R-W4a's 2 min 58 s for two captures
and the original 2 min 03 s for one. The full both-viewport run was **not** re-measured — 13 min
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
0 failed. `SMOKE_VIEWPORT=desktop` was killed at 10 m 00 s having passed 151 with 0 failed** — an
estimated ~13 minutes end to end, so it fails by about three. Both halves in one command is ~18
minutes and never fits. The trailing `page.click: Target page … has been closed` in such a log is
the kill, not a failure.

**So a parcel whose acceptance needs the desktop half cannot self-verify it here, and should say so
in its PR rather than quietly merging on the mobile half.** `tools/check.sh` — which is the actual
dev gate (`.github/workflows/chicago-4d-check.yml` runs it and nothing else) — is unaffected at
~90 s. The durable fix is for the smoke to take a test-name or section filter the way it takes
`SMOKE_VIEWPORT`, so the desktop half can be run as two commands that each fit; until then, the
desktop half belongs to a runner without the per-command ceiling.

**RESOLVED 2026-08-20 by T-0060: the smoke takes `SMOKE_STAGE=1..4`, and each stage fits the
ten-minute command.** The body of each viewport is cut at three section boundaries verified for
crossing bindings (two crossed — `terrainLoad`, `streetLayer` — and both are now read before the
split; the scans that missed them are written up in the ticket). Measured on the improve runner,
mobile against the published mirror: **stage 1 — 1 m 54 s, 74 staged checks · stage 2 — 3 m 00 s,
91 · stage 3 — 3 m 17 s, 33 · stage 4 — 7 m 30 s, 143**, plus 9 always-on checks (boot, loader
problems, run-to-completion, page errors, vendor) taken in EVERY invocation — the run prints that
split so the halves can be audited to add up to an unfiltered pass: 341 staged + 9 = 350. The
page-error assertion is no longer the tail of an unrunnable body: a mid-suite throw is caught,
recorded as its own FAIL, and the tail still runs. The unfiltered single-process reference lives
in `.github/workflows/chicago-4d-smoke.yml` (push-to-its-own-path or dispatch on main) — that is
the "runner without the per-command ceiling" this section asked for. Desktop stage timings are
not yet measured; stage 4 is the one to watch (its mobile 7 m 30 s includes the shared
street-layer reading), and if it overruns on desktop the fifth cut goes in then, the same way.

**RE-CUT 2026-08-24 by T-0166 (piece 1 of T-0121): the four stages are EIGHT parts, and
`SMOKE_STAGE` takes a range.** The four had eroded exactly as the paragraph above feared, and
faster: by 2026-08-23 three of the four DESKTOP quarters ran past the ten-minute ceiling and the
fourth cleared it by two minutes, so the desktop half a steward run could reach was stage 1
alone. Each quarter is now halved at a section boundary re-verified for crossing bindings, so
**part 2k-1 plus part 2k is exactly T-0060's stage k** — the cheap viewport is still four
commands (`SMOKE_STAGE=1-2`, `3-4`, `5-6`, `7-8`) and nothing about the audit changes.

Three of the four new second halves inherited page state rather than a binding, which the
scope-aware scan cannot see and only a part run alone from a fresh boot will show: part 6 and
part 8 boot at the GATE SCREEN (`enterTown()`, T-0060's inline accommodation, now one function
called at the head of four parts), part 8 also needs the PANEL open because its first statement
clicks a tab inside it, and part 4 needs the Sauganash framed because its first check picks
whatever is down the crosshair. All three prologues are guarded on the state they establish, so
an unfiltered run runs them as no-ops.

**The mobile fit, measured on the improve runner against the published mirror** — part 1
**1 m 41 s**, 66 staged checks · part 2 **1 m 17 s**, 66 · part 3 **0 m 52 s**, 65 · part 4
**3 m 17 s**, 38 · part 5 **2 m 52 s**, 19 · part 6 **0 m 44 s**, 14 · part 7 **3 m 48 s**, 36 ·
part 8 **4 m 19 s**, 107 — 411 staged checks plus the 9 always-on ones every invocation takes,
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
1 m 53 s at desktop — so the desktop cost of a part is NOT a fixed multiple of its mobile cost,
the camera-heavy parts scale several times harder than the DOM-heavy ones, and an eight-way cut
sized on the mobile profile could not be assumed to fit.

**THE DESKTOP PROFILE, MEASURED 2026-08-24 by T-0167** — eight foreground commands at 1280x800
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
that read the roads — 5 and 7 — will have moved a little since, and part 5's reading was taken
with T-0114's road-legibility check still failing. The re-cut readings below, and the audit,
were re-taken on top of T-0114.

**NOTHING OVERRAN, AND THAT IS NOT THE SAME AS FITTING.** Two readings have to be held together:
part 7 measured 7 m 43 s here and was KILLED at 10 m 00 s on T-0166's runner three days earlier,
on a body that had not grown in between. **These desktop numbers move by minutes between runs**
— SwiftShader is a software renderer and its cost tracks whatever else the machine is doing — so
a part is not sized by whether one reading cleared the ceiling but by how much margin it has when
it does. A 74-second margin is not a margin.

**RE-CUT 2026-08-24 by T-0167 (piece 2 of T-0121): part 8 is halved and there are NINE parts.**
Part 8 was both the thinnest margin on the profile and the most check-dense part of the suite by
a factor of three, which is the combination worth cutting. It is also the TAIL, so the new part
is APPENDED and parts 1-7 keep their numbers: the pairing rule survives as 1+2, 3+4, 5+6, **7+8+9**,
and the mobile recipe's last command widens from `7-8` to `7-9` — still four commands. The
boundary is the Evidence panel: the profile put 6 m 05 s of the old part 8 above it and 2 m 41 s
below, and the scope-aware scan found three names crossing it (`eye`, `toggles`, `typed`) of which
all three are prose or a different local (`typedE.typed`), so nothing crosses in fact. Part 9's
prologue is `enterTown()` alone — the liberties reading already carries its own guarded panel-open
and clicks its own tab, so unlike part 8 it needs no panel guard bolted on.

**Measured after the cut, at desktop: part 8 — 6 m 10 s, 28 staged · part 9 — 3 m 09 s, 79
staged.** 28 + 79 = 107, exactly the old part 8's count, which is how "never dropping a check" is
demonstrated rather than asserted. Both were taken twice, once at `ac1abb80` (6 m 08 s / 3 m 08 s)
and again on top of T-0114 — the same counts and within two seconds either way, which is also a
reading on how much of the desktop variance is the scene and how much is the machine. The worst
desktop margin is now **part 7 at 2 m 17 s**, and it is the next one to go — T-0170, which also
records why it was not taken in the same run: part 7 has no section headers to cut at, it holds
one half of the `anyStage(5, 7)` street-layer reading, and it is not the tail, so cutting it
renumbers everything after it. The audit was taken at mobile too: old `SMOKE_STAGE=7-8` gives 143
staged / 9 always-on / 152 passed and new `7-9` gives **143 / 9 / 152**, in 5 m 53 s against
5 m 49 s.

**AND THE HEADING OF THIS SECTION IS OUT OF DATE BY A FACTOR OF TWO.** "The smoke costs 26 of
them" was measured on 2026-08-14. T-0167's profile puts the staged gate at **39 m 58 s of desktop
across nine commands plus 13 m 26 s of mobile across four** — call it **53 minutes**, better than a
third of the 150-minute run budget, and that is before a part is re-run after a fix. The two-full-
passes rule above should be read as ONE full pass and a re-run of the parts a change touches; a
parcel whose acceptance needs the whole gate twice has already outgrown a run.

**`SMOKE_TIMING=1` stamps every check line with the elapsed clock**, and T-0167 added it because
the profile could not have been taken without it. A part that BREACHES the ceiling is killed
*before* it prints its wall clock, so the parts actually worth cutting were the only ones a plain
run reported nothing about — T-0166's part 7 reading is literally ">10 m", and nothing else. With
the stamp on, a killed run is still a profile of everything it reached, which is what places the
next cut. It is off by default so the gate's own output stays comparable between runs.

### NEXT UP — every row says whether a visitor can SEE it

**Rewritten 2026-08-15 on the owner's report that the loop does research and organisation rather
than work on the app. Measured: 15 of the last 30 changelog entries say nothing you can see
changed, and v124–v137 is fourteen invisible runs in a row.** Two causes, both fixed here. The
first is the rule — see AGENTS.md § THE VISIBLE-PROGRESS RULE, which caps invisible runs at one in
four. The second is this table: it had grown ~20 completed rows above the live picks, so the
visible parcels were the hardest ones to find. Completed work now lives in its own section below,
not at the top of the queue.

> ## ⛔ THIS TABLE IS FROZEN AS OF 2026-08-17 — THE LIVE QUEUE IS `tickets/QUEUE.md`
>
> On the owner's direct request the operational backlog moved to **`tickets/`**: one file
> per ticket, `QUEUE.md` holding the priority order (the owner orders it; agents only append
> and remove), `BOARD.md` generated, and `tools/ticket.mjs check` gating it all in check.sh.
> His requests were untraceable in this file — the K-series he asked for in August was
> sitting below line 9,300 with no status tags while the loop picked from this table — and
> he could not reorder priorities without editing prose. Every open parcel below became a
> ticket carrying its old id in `legacy_id`; the deep boxes in this file remain the
> reasoning archive and tickets link into them. **Do not add rows here. Do not pick from
> here. Read AGENTS.md § THE QUEUE.**

| # | lane | parcel | why first |
|---|---|---|---|
| — | RENDERING | ~~R-BUG7~~ | **SEEN** | **DONE 2026-08-17 — the stalk was aimed at the stem and then TURNED to a random bearing, and now the flower is hung by its foot.** `maybeHead` computes `tiltAz` so the stalk leans back to the stem and passes a random `yaw` beside it; `push`'s Euler is `YXZ`, so the yaw spins the whole tilted head and the azimuth with it — and `push`'s own docstring says *"Pass `yaw` 0 alongside a tilt"*. **Four repairs computed that bearing correctly and not one reached the geometry.** The repair is not a fifth aim: the archetype's origin moved to the FOOT of its own stalk, so the offset from the stem is generated by the rotation and `foot <= plantH` makes attachment an invariant at every fade rather than a number. **38 of 11,752 drawn heads over 32 poses → 0**, all 38 `corymb`, worst foot **58 cm** from any stem; foot-to-stem median **21 mm → 0**. Read its box before adding a per-instance rotation to any set |
| — | RENDERING | ~~R-BUG5b~~ | **SEEN** | **DONE 2026-08-16 — it was the PLANTER after all, and the whole near-field wood was drawn mirrored.** The loop asks every question in ENU (`isWater`, `communityAt`, `surfaceHeight`, `blocked`, `noteStation`) and hands its ENU north straight to `addTree`, which takes a three world **z** — and `enuToWorld` is `(e, y, -n)`. So every tree was TESTED at `(px, pz)` and DRAWN at `(px, -pz)`: **391 stations, 0 wet, 64 of the same 391 wet at their mirror, 10,734 vertices of timber over open water and the worst 48 m from dry ground.** Three green gates all walk `stations`, which is the point that was TESTED — **nothing had ever read the geometry back**. Read its box before trusting any placement gate in this file |
| — | RENDERING | ~~R-BUG5~~ | **DONE 2026-08-16 · a real second fault, but NOT the owner's picture (see R-BUG5b)** — it was the SKYLINE, not the planter. Both of the owner's populations are ONE body of far timber authored **between the two banks** of the main stem, 39 of 39 samples over water and **3.347 m** under its surface; the scatter is the horizon solver's own gap modulation breaking the same run into crowns. Both existing gates were green because both count the near-field planter's 632 m square, and **nothing had ever asked the five `FAR_TIMBER` polylines where they stand**. Read its box before quoting any horizon-timber number |
| **1** | RENDERING | **R-BUG5(b)** | **NOT A PICK WITHOUT THE OWNER.** `main_stem_belt_east` now draws nothing, because none of it was on land. Where the South Water Street belt's near edge actually ran is a placement claim no source here settles — three routes are written up in R-BUG5's box for the owner to choose between |
| — | RENDERING | ~~R-BUG3c~~ | **DONE 2026-08-15** — neither surface moved: the publish step quantises the ground onto a **306 mm** vertical lattice AFTER the only gate that measures it, burying the road and the flora by up to **228 mm**. The heights are read back off the field at load, and two gates now hold the file that SHIPS. Read the box before quoting any ground number |
| — | RENDERING | ~~R-W4c(a)~~ | **DONE 2026-08-15** — the flower-load recipe's hue cut at 50° runs through the middle of a July prairie's bloom, so `0.0012` is not a count of flowers. (a) landed the honest measurement; **(b) is the tuning half and must take (a)'s committed numbers as its baseline** |
| — | RENDERING | ~~R-W4c(b1)~~ | **DONE 2026-08-15** — **there is no 4–6 % target.** Its remnant half cites no photograph this repository holds; its planting half does not reproduce (**5.54 %**, and 12.91 % is not on that frame under either ordering); and the repair R-W4c(a)'s diagnosis implies **fails** — reordering the tests takes precision **0.998 → 0.062**, so the flower test cannot see a flower either. Read its box before quoting any flower number |
| — | RENDERING | **R-W4c(b2)** | **NOT A PICK — it is blocked on the owner.** "Raise the bloom" has no bar left to raise it against, and R-W4c(b1) measured that the bloom is planted from sourced `density_per_ha`, so moving it is a DATA change needing source support rather than a renderer tune. Three routes are written up in (b1)'s box for the owner to choose between; an agent picking one would be inventing the target this parcel just removed |
| — | RENDERING | ~~R-W6~~ | **DONE 2026-08-16** — **yes, at 16 bits**, and the artefact was not invisible: the 14-bit ground stands up to **46.3 mm** above the field, past the 22 mm road lift at 87 sample points, **one of them 1.9 m from South Water Street's centreline**. 16 bits costs **1,116 bytes** and takes the worst error to 12.9 mm, under the lift everywhere; the uncompressed 5.8 MB would buy 12.9 → 7.7 mm, and 7.7 is DECIMATION the master carries too. Read its box before quoting any payload or lattice number. **Its 12.9 mm no longer describes the tree** — re-measured 2026-08-23 on the terrain as extended east, the same 16-bit ground is **77.1 mm** worst with **56** samples past the lift, on 60–90 % slopes that did not exist in the box R-W6 measured. T-0152 |
| — | RENDERING | ~~R-BUG4~~ | **DONE 2026-08-15** — the wet-corner rule deleted the dry half of a road panel with the wet half. Clipped at the waterline now: **28 panels / 62.7 m** of roadway recovered, and the gate asserts the invariant rather than the number |
| — | RENDERING | ~~R-W4a~~ | **DONE 2026-08-15** — the horizon figure counted the town's roofs as timber (62 % of it at `prairie_south`), the G−B discriminator this project named was measured and **refuted**, and the replacement cannot move when a block lands. Read its box before quoting any horizon number |
| 2 | RENDERING | **R-BUG4** | XS, owner-reported. A wet CORNER deletes a whole road panel, dry half included: **28 panels / 62.7 m** of roadway removed where the centreline is dry land |
| 3 | RENDERING | **R-W4a** | the horizon-timber metric counts gable ends as trees, so W4's headline number is unmeasurable and a town parcel already banked a false pass. Prior to every other W4 half · *promoted 2026-08-15: R-M1b, which was #1, is blocked on the owner* |
| — | RENDERING | ~~R-M1~~ | **R-M1a DONE 2026-08-15** — the two scales are measured and their baseline is committed. **R-M1b is NOT a pick: it is blocked on a threshold source, because the photograph R-M1 named to derive from contains no dirt track.** Read R-M1b's box before touching it |
| — | RENDERING | ~~R-M1c~~ | **SEEN** | **DONE 2026-08-16 — the road score divided by probes SEEN, so an occluder RAISED it.** One band, three builds, one evening: **seen 157 → 177 → 163** and the old score **62 % → 54 % → 59 %**, while the number of readable stretches never moved off **96** and `nBare` was **182 in all three**. The build with the whole wood on the wrong side of the river scored HIGHEST; K45(b2) would have gone green by planting more timber in front of the road. **The instrument was already built and already printing** — `shotMF`'s own comment says the marked-only denominator "drops instead of failing" — and nothing had ever divided by it. Scored on `nBare`: **53.3 / 52.7 / 52.7 %**, under the 0.55 bar in all three. Read its box before quoting any road-contrast percentage taken before this date |
| — | RENDERING | ~~R-W1~~ | **SEEN** | **LANDED ON `dev` 2026-08-16 — the light was wrong by 1.9× and 2.9× red against its own sky, and the honest sky costs the roads.** Literal black pixels 12,063 → 0 at three stations; `south_water` 250–600 m falls **71 % → 16 %**. **NOT FOR PROMOTION** until the owner walks `/dev/` or R-W2 buys the contrast back — read its release-condition box before any promotion. Its third finding is R-M1d: the suite reported **229/2 before and after**, because a station already red on another band hides a 55-point collapse |
| — | RENDERING | ~~R-W2a~~ | **DONE 2026-08-16** — the material sheet, measured out of the shipped GLBs: **1,353 material slots, 32 names, 41 colours, 18 roughness values, zero textures**. Five findings, and two of them block texturing outright: **the chimney is not a material here** (219 stacks painted `roof`) and **no record states a roof covering** (315 roof types, 0 coverings). Read `docs/RESEARCH/materials.md` §4 before quoting any material number |
| — | TOWN | ~~T-A15~~ | **DONE 2026-08-15** — `blk_randolph_clark`, the block opposite the courthouse: the first with a store on it, the face rule EXTENDED to rank one (**K32**), the end rule measured at **1.02× / 7.5 m** and declared exhausted (**K31**), and **two of T-A14's three adoption candidacies refuted** — the laundress and teamster arguments never claim a floor, so they fail rule 6's test 1. Read finding 3 before quoting any adoption test |
| — | TOWN | ~~T-A16~~ | **DONE 2026-08-15** — `blk_randolph_lasalle` is **the public square** and is not a building site. It was withdrawn rather than built: no lots, no roofs, a gate, and **two documented buildings moved off it**. The block parcel's own gates all passed on the old placement, because not one of them asks whether the ground was for sale. Read its box before scheduling anything anywhere |
| — | TOWN | ~~T-A3h~~ | **DONE 2026-08-15** — the last open block entry, and the two adoptions it predicted are the two it made: `blk_randolph_dearborn`'s D3 to the carpenters and its D1 to the labourers, measured with `tools/measure_adoption_tests.py` rather than recalled. **Its finding is about the other two**: the D4 and the D2 that pass as a "second roof" are pairs this layer has NEVER housed — the D4 evidence is one household in the NORTH, the D2's is four in the NORTH and WEST — so every second-roof refusal K28 has collected is a candidacy built from two projections of one table. Read its box and K28's before quoting any adoption test |
| — | TOWN | ~~T-V1(a)~~ | **DONE 2026-08-15** — the stamp is **not** at `south_water`: every twin in the town is in the North Division parcel, **36 of its 60 roofs**, and the census found something bigger — **40 eaves outside the band their own note cites**, 18 of them in a parcel that samples its footprints and says so. (b) is written, measured and **blocked by a circular dependency in the pipeline** — read its box before touching any dimension on a baked record |
| 2 | TOWN | **T-V1(b)** | the sixty North records: **NEEDS ONE BAKE**, and cannot go green on the improve runner. A policy question for the owner, not an engineering one |
| — | TOWN | ~~T-I3(a)~~ | **DONE 2026-08-16** — the town's public buildings are **three roofs** and this project already had all three, so the refusal is now absolute rather than argued. The finding is the fourth building: **the court-house was not built yet** — Andreas fixes the season, the month AND the corner the record said nothing fixed, and the citation it had was a **picture caption** — so a record is taken OUT of a scene on evidence for the first time. Read its box before quoting any civic number |
| 3 | TOWN | **T-I3(b)** | **NOT A PICK WITHOUT THE OWNER.** Three of the six I3 slots are a count of nothing; the inventory's arithmetic is closed, so removing them is either "the town had 662 roofs" or "three roofs were not civic". Two different claims about the town, and the research settles neither |
| — | TOWN | ~~K30(a)~~ | **DONE 2026-08-16** — it is **29 buildings on eight streets**, not three on one, and every one of them is a record a PERSON placed: **zero** generated roofs lap a corridor, across 332 placed phases. The depths are bimodal with an empty gap at 1.98–3.48 m, and **13 of the 17 deep ones are South Water**. T-A7's "fourteen" does not reproduce **at its own commit** (16 there, the same 16 today), and the anchor-convention suspect is **refuted** — recentring makes 10 of the 29 worse. Read its box before quoting any intrusion number |
| — | TOWN | ~~K30(b)~~ | **DONE 2026-08-16 · ITS CAUSE IS REFUTED 2026-08-22 — read K30(d) before quoting any of this row.** The anchors it compares with the half-width are BACK corners, so the comparison could not see the displacement it looked for; the real cause is the committed `south_water` centreline standing 4.3–8.8 m south of the control the placements were offset from. Its own text follows: the cause is the **drawing**, and the Wacker made-ground suspect is **refuted** by arithmetic: the anchors sit 11.64–15.30 m from the centreline against a 12.192 m half-width, with both signs, so no displacement of 4.51–8.17 m is there. The records are derived to their FRONTAGE and drawn with the body growing north from it (331 of 333 footprints grow from the minimum corner), so each stands in the road by its own depth — **all 17** deep records, and reflection takes 12 of them under 1 m. **The residual law** settles the shallow tail without moving anything: what survives correct drawing IS the point's own penetration, to 0.10 m. Read its box before quoting any intrusion cause |
| — | TOWN | ~~K20~~ | **DONE 2026-08-16** — the invented-name allocator, measured properly for the first time: **73 of 113 renamed by ONE new household**, not the 17–25 the eleven by-product measurements reported, and never zero in the two big buckets. It is **10** now, and the report prints each bucket's **pool pressure** so the residual cannot be misread — at 0.14× it renames **one**, at 2.03× it renames ten, and that is the pool being too small. Unwelding the given name from the surname exposed **two identical residents**. Read its box before quoting any churn number |
| — | TOWN | ~~K28~~ | **DONE 2026-08-16** — three questions, three clauses, **two gates, and not one record moved**. The table is **projections** (the pair reading is refused because it refuses T-A4's fourteenth labouring household, one of the four rule 6 says its third test recovers); there **is** a cap, one adoption per trade per block, which is what makes the projections safe; and test 1 means the trade's **own committed text**, so the laundresses' D2 and the teamsters' D4 are refused with the remedy named. All **21** standing block adoptions already obeyed it. Read its box before quoting any adoption rule |
| — | TOWN | ~~K25a~~ | **DONE 2026-08-15** — it is **98 values on 80 of 249 records**, not 54 on 193, and **24 causes, not 98**: seven metre values hold all 54 eaves and six degree constants hold all 38 pitches, because the generator authors the archetype's constant and the note cites the family's band. **Roof pitch had never been measured by anything.** The sub-1-ft question is decided — they are failures, and nearness is the diagnosis. Read its box before quoting any band number |
| — | TOWN | ~~K33~~ | **DONE 2026-08-15** — it is **623 values on 227 of 249 records**, not 581, and the extra 42 are the finding: `roof_pitch_deg` cites a band on five families whose roof line is **"gable or shed"**, a form with no slope, and K25(a) could not see them because **a value with no band is never tested against one**. Route 2 (split the note), and route 3 is measured as unavailable — the confidence floats are in the mesh hash and prose is not. The assertion is **absolute, not a ratchet**. Read its box before quoting any citation number |
| — | GROUND | ~~T-E2~~ | **DONE 2026-08-15** — 26.5 % of the modelled land above the water surface is the reservation or the bar, and every gate this project had would have built on it. Nothing moved: **zero** anonymous roofs were there. Read its box before quoting any buildable-ground figure |

**Every row is tagged. `SEEN` means a screenshot from the same spot looks different when it
merges. `UNSEEN` means it does not — those are real work and this project needs them, but they are
rationed.**

| # | lane | parcel | seen? | why |
|---|---|---|---|---|
| — | RENDERING | ~~K49(f)~~ | **SEEN** | **DONE 2026-08-16 — 2 species absent → 0, and the block's own phase pays for itself twice.** The even deal dealt the SAME 64 values of `u` in every block of the world, so a band narrower than 1/64 fell between two of them EVERYWHERE: **45 matrix bands, exactly 2 under one step, and exactly those 2 were the species drawn nowhere.** Matrix deviation **282.90 → 219.19**. Its finding is not the repair: **K49(e)'s leading explanation is refuted for the bigger of the two rows it was written about** — the settled town recovers 23.66 of its 24.87 regression on a change that touches no filter. Read its box before quoting K49(d) on a regressed row |
| — | RENDERING | ~~R-A1~~ | **SEEN** | **DONE 2026-08-16 — the Road visibility slider, off by default, and the first parcel taken by PULLING A SEEN ROW UP when every numbered one was blocked.** Its finding is about gates, not roads: **an inertness assertion needs a liveness assertion beside it**, because "the default is unchanged" passes identically whether a control is wired correctly or wired to nothing — R-BUG1's dead `--no-sun-shadow` one parcel earlier. And the instrument was measured before its threshold was set: the 12² frame signature scores the aid at **worst 2 against a residual of 0**, the same difference at 48² is **worst 6**, and nothing about the scene changed between the two runs. Read its box before adding any preference to Settings |
| — | RENDERING | ~~K24~~ | **SEEN** | **DONE 2026-08-17 — the Brightness slider, off by default, and the SECOND parcel taken by pulling a SEEN row up when every numbered one was blocked.** Owner-requested on 2026-08-14 and deferred behind PR #125 by a sequencing note that turned out to be a claim about a diff nobody had checked: the aid is one constant and one method, not a `world.js` rewrite. **Its finding is about R-A1's gate rather than about light** — `Object.assign` copies what a getter returns, so `get roadAid()` had been a frozen `0` since it shipped, and both of R-A1's readback assertions expect `0`. The control was live; its report of itself was not. Read its box before adding any reading to `window.__chicago4d` |
| — | RENDERING | ~~K51~~ | **SEEN** | **DONE 2026-08-17 — 139 researched animals reached no browser at all, and the whole layer is now a card in the Evidence panel.** Fauna figures reaching a visitor **0 of 30 → 30 of 30**; the dataset's unread population **58 of 100 → 28**. Its findings are about instruments, not animals: K42's assertion 3a **fired exactly as designed** the moment the directory was opened, and **two of that gate's own controls had been written against the repository's state** — one became a copy of the measurement and the other printed SILENT rather than failing. And `docs/LIBERTIES.md` **L2 said "ambient wildlife is rendered sparsely" for eight days while nothing was rendered at all**. Read its box before quoting any layer-read number |
| — | RENDERING | ~~R-BUG6(a)~~ | **SEEN in motion** | **DONE 2026-08-17 — the shadow box was re-centred on the visitor's exact position, so its texel lattice slid under every step and re-quantised every shadow edge in the town.** It moves in whole texels now: with the camera held still and the box slid half a texel, `from_above` **2,023 changed pixels → 0** and `descend_main_stem` **5,650 → 0**. Three findings, and two of them are about instruments: **the control that "cleared the shadow map" was inert** (a compile-time flag is not a runtime handle — it moves 5,439 px now), and **a sub-pixel nudge cannot measure a shadow box at all** — scaled up to a half texel it changes 29,138 px with the fix and 28,784 without, sign included. The answer to the parcel's title: **the shadow map is 14–16 % of the town's flicker**, not the cause of it. Read its box before quoting any flicker number |
| — | RENDERING | ~~R-BUG6(b)~~ | — | **DONE 2026-08-17 — the premise was wrong and two tests say so. The residual is NOT co-planar ties: switching the depth test from `LessEqual` to `Less` moves 36,187 px of the frame and only 13 of the 1,108 flickering ones (1.2 %), and 5× the depth precision leaves 604 of 607 surviving.** It is the town's own edges being resampled, which is antialiasing and not a defect — R-BUG1's near plane had already taken the real one. Three findings: **an exact tie is STABLE and a near tie is what flickers** (which is why 3.5 % of this frame is co-planar and none of it shimmers); the ownership instrument (`tools/measure_tie_class.mjs`, 0 unattributed, buildings + trees own 94.5 % of the flicker on 7.7 % of the frame); and **`measure_river_edge.mjs`'s bank mask counts the SKY as water** — rows 0–200 are 1,280 of 1,280 "waterish", so no bank-line pixel count from it is a statement about the river. Read its box before quoting any flicker or bank number |
| — | TOWN | ~~K52~~ | **SEEN** | **DONE 2026-08-17 — the layer that already had a reader was hiding seventeen households, and the reader is the reason nobody looked.** A household reaches a visitor only through a building it `lives_at` or `works_at`, so the 17 whose residence AND workplace are both unattested on 1 July 1835 attached to no building and appeared **on no card anywhere** — 20 person entries, one of them the **Mark Beaubien** household, dropped for exactly the thin evidence that makes its record interesting. And the join carried a third of each record it did reach: arrival, origin, reason for coming, presence, a person's age, sex, name basis and sources, and all ten `researched_not_resident` findings reached nothing. **K42's assertion 3a did not fire** — the census tool names `flora` and `fauna` only, which is K52(b). The third parcel taken by pulling a SEEN row up when every numbered one was bake-blocked. Read its box before assuming a layer with a reader is a layer that is read |
| **1** | RENDERING | **R-BUG6(c)** | UNSEEN | **NEEDS ONE BAKE.** The 36,187 co-planar pixels above are steady but arbitrary: two surfaces of different colours at one depth, with draw order picking the winner. A question about the models, opened by (b) |
| — | RENDERING | ~~K53~~ | **SEEN** | **DONE 2026-08-17 — twenty-one shrub records were drawn with the forb archetype, and the clamp that made that survivable was hiding the recorded width.** Shrubs 0 → **14** drawn over 32 poses, clump width **0.40 m clamped → 1.80 m median**, and the census is identical plant for plant (2,201 forb-layer plants before, 2,187 + 14 after, every zone conserved). Its finding is the reason the number is 14 and not 140 — **the forb lottery deals by HEAD COUNT, so a hazel covering 7 m² competes as one plant against 40 wild leeks per m²**, and the wet woods' attested dominant shrub gets 0.2 % of the slots. Opened as **K54**. Read its box before quoting a shrub count |
| — | RENDERING | ~~K54~~ | **SEEN** | **DONE 2026-08-17 — the two strata were sharing one lattice, and where the herb layer saturates it the deal is a subsample by head count. 4 bushes standing over the eight stations → 181.** The shrubs are dealt from their own pass at their own recorded clump density: `z06_dense_forest` **2 → 156** drawn and **40.1 %** of its recorded 94.9 % cover, the riverbank dogwood belt **20.1 % against a recorded 19.5 %**, matrix deviation unmoved to the second decimal and **0 of 98** pairs drawn nowhere. Two findings: **the slot count still mixed units** and planted the riverbank understory **8.8×** too thickly (K55), and **the instrument this parcel named cannot answer its question** — "deviation from the recorded cover" has measured the lattice against its own target since K49(c2). Read its box before quoting 89.11 or any deviation sum across two builds |
| — | RENDERING | ~~K56~~ | **SEEN** | **DONE 2026-08-17 — 16 sprays → 32, shell fill 17.7 % → 30.9 %, and the lowest band arches down over the stems.** The size did NOT move: a spray is a leaf MASS, not a leaf, so shrinking it would have bought a smaller plate with more sky round it. Follow-up **K57** |
| — | RENDERING | ~~K57~~ | **SEEN** | **DONE 2026-08-17 — the question cannot be asked at a fixed plate area, because the plates are what carries the RECORDED clump width.** 64 sprays at the shipped total area buy 8.5 points of cover and pay **reach 0.990 → 0.890** of the recorded half-width for them, plate 37 → 26 cm. So the grain trades against TRIANGLES: at the shipped plate size, 32 → 48 → 64 sprays cover **36.9 % → 46.9 % → 51.3 %** of the outline for 72 → 104 → 136 triangles, and **48 is where the return halves**. Stem cover 40.9 % → 51.3 %, 38.8 % of the frame changed. Two findings: **K56's 17.7 %/30.9 % were taken by a script nobody committed** — the instrument is `tools/measure_spray_grain.mjs` now, reproducing K56's plate area to the digit off `renderers/web/js/shrub-grain.js`, which imports nothing; and the wet woods' ring is **167 shrubs, not the 156 K54 and K56 quote**. Opened **K59**, which is now DONE and spent the 4.4 points: read K59's box before timing anything in a browser here. Read this one before shrinking any archetype plate |
| — | RENDERING | ~~K55~~ | **SEEN, and only just** | **DONE 2026-08-17 — the same fault runs BOTH WAYS, and for the herbs it ran the other one.** A cover fraction read as a count over-planted the 2.25 m dogwood by 8.8× and UNDER-planted the riverbank's 10 cm ground layer by **96×**: `z05` 0.025 → 2.407 plants/m², `z03` 0.123 → 1.254, forb slots **781 → 923** over the eight stations, `z03`'s own layer **31 → 84**, matrix and shrub unchanged to the second decimal. Three findings: the sign of the fault is decided by whether one plant covers more or less than a square metre, so the queue inherited "over-planting" from the case measured first; **three of the parcel's six named rows were never faults** — the `basis` column was printing `subsetOn`'s default argument and the matrix slot count comes off `cover.matrix_fraction`; and the count moved a fifth while the frame moved **0.15 %**, with `z10_settled_town` — the parcel's predicted visible half — not moving at all, because its share was clamped before and after. Opened **K58**. Read its box before quoting a forb count or calling a mixed list a defect |
| **1** | RENDERING | **K58** | **SEEN** | **six forb layers of ten now ask for more plants than the lattice can carry**, so their drawn cover is bounded by `TUNE.forb` and not by any research figure — `z06_dense_forest` draws 40.1 % of a recorded 94.9 % for that reason and not for want of data. Opened 2026-08-17 by K55, which took the clamped count from four to six |
| — | TOWN | ~~K30(c)~~ | **SEEN** | **REFUTED 2026-08-22 (T-0009, K30(d)) — DO NOT RUN THIS REPAIR.** The 29 buildings are still drawn standing in the roadway, but not for this reason: `--anchors` finds the record's point at the BACK corner on **all 17** of the deep records and on the kerb face on **none** of them, so the street-facing FACE is what was placed on the frontage and reflection would take twelve documented buildings a full depth behind their own frontage. The cause is the committed `south_water` centreline, deliberately shifted 4.3–8.8 m south of the control the placements were offset from. **What to do about it is the owner's, and T-0009 is blocked on him** |
| **2** | RENDERING | **R-W2b** | **SEEN** | wire R-W2a's committed material sheet into the params and records — 1,353 materials measured out of the shipped GLBs and currently reaching nothing. **This is what repaints the town**, and R-W2 owns the worst-scored axis on R-G1's whole table (texture, **1.4**) |
| — | RENDERING | ~~R-W2c~~ | **SEEN** | **DONE 2026-08-22 (T-0008) — the stack is not the roof.** 157 stacks on 143 buildings now carry a masonry material of their own: **brick on 112 framed buildings**, off `frame_tavern`'s committed Petford value moved into the sheet, and a **cat-and-clay daub on 31 log cabins** at the midpoint of the two committed values that bound it. `docs/RESEARCH/chimneys.md` is the fabric argument; L168 records the invention. **Three findings.** It was NOT a one-file fix and it was not palette-only: the two dispositions the archetypes had already argued in prose are two materials, and the fabric had to be researched before either could be chosen. **It cost NO draw call** — `buildings.js::materialKey` batches on maps and flags, never on colour or roughness, both of which ride per vertex, so 113 calls before and 113 after at `south_water`. And R-W2a's *219 stacks on 199 buildings* does not reproduce: the resolved parameters of the committed masters give **157 on 143** across four archetypes. Left standing: the fort (**T-0137**) and the placeholders' second brick (**T-0138**) |
| — | TOWN | ~~T-V2~~ | **DONE 2026-08-16** — the anchor named South Water Street stood 101 m from it, in a field. Now in the street at Wells, both coordinates read from committed data. **It sat on `hold` two days on a number other parcels had already fixed**: the far band it was parked for reads **2.1 L\* / 71 %** today, not 0.5 / 30 %. Its real finding is R-M1c's, from a second direction — the field stand scored **100 % on six probes of 510** and the street stand shows **93 perceptible stretches against 31** and scores lower. T-V2b folded into R-M1c; baseline re-shoot is T-V2c |
| **5** | GROUND | **T-E3** | **SEEN** | the heightfield east (= `S2e`). Ground a visitor can walk onto that is not there today |
| 6 | TOWN | **T-V1(b)** | SEEN | the sixty North records — but **NEEDS ONE BAKE** and cannot go green on the improve runner. Claim only with the bake available |
| **1** | RENDERING | **R-W2** | **SEEN** | **PROMOTED 2026-08-16 — R-W1 landed on `dev` and cannot leave it until this parcel runs.** Textured coverage is the only thing that buys back the contrast the honest sky costs: R-W1 takes `south_water` 250–600 m from **71 % to 16 %**, and the near band's opaque *ceiling* is 3.4–4.3 L\* whatever the light does. Every road band in the suite is now under or near its bar, and no amount of relighting fixes a surface with no texture on it. Read R-W2a's material sheet first — its findings 1 and 2 (the chimney is not a material; no record states a roof covering) bound what can be textured today |
| — | RENDERING | ~~R-W3b(a)~~ | **SEEN** | **DONE 2026-08-17 — the sun threw a shadow within 60 m of the visitor and nowhere else: 5 to 8 of 331 structures and 0 to 41 of 730 stems, measured at all eight anchors.** It is ±120 m now, at the SAME texel size (the map doubles with the box), and `green_tree` goes 8 → 27 structures, `south_water` 8 → 26 and 12 → 54 stems. **Its finding is the ceiling: the reach is DRAW-CALL-bound, not fill-bound** — every batch entering the box is another call in the shadow pass, and the worst anchor reads 70 calls at 60 m, 74 at 120, 78 at 150 and **exactly 80 at 180, which is the budget**, with the town still two thirds outside the box. Read its box before raising the number |
| — | RENDERING | ~~R-W5a2 + R-W3b(a2)~~ | **SEEN** | **DONE 2026-08-17 — 16 batches → 1, and the reach went straight from ±120 m to ±240 m on the calls it freed.** Roughness is the last thing that was splitting the town, and it is per-vertex now; the worst anchor reads **50 draw calls of 80 where it read 74 this morning**, at the SAME 11.7 cm texel. `green_tree` 27 → **49** of 331 structures and 0 → **70** of 730 stems; `south_water` 26 → **91** and 54 → **239**. **Its finding is that the batch merge is not neutral after all** — 942 pixels of 7,168,000 move across seven poses, all of them depth ties between co-planar surfaces of different materials, which is R-BUG6's own class one draw call in. Read its box before quoting a draw-call figure taken before this date |
| — | RENDERING | ~~R-W4c(b2)~~ | — | **NOT A PICK — blocked on the owner.** "Raise the bloom" has no bar left to raise it to |
| — | TOWN | ~~T-I3(b)~~ | — | **NOT A PICK — blocked on the owner.** Three of the six I3 slots are a count of nothing |
| — | GROUND | **T-E5(b)** | UNSEEN | how much of the public square was wet — research, opened by T-E5(a) |
| — | RENDERING | ~~K45(b) change one~~ | **SEEN** | **DONE 2026-08-17 as K45(b4) — 88 poplars stand on 4.30 ha of lakeshore sand that had never been offered a stem, and the placement rule is the SWARD'S.** The dune is a substrate and the heightfield does not carry substrate, so `communityAt` asks `flora.js` which zone a point is in rather than carrying a second copy of the beach. Two findings: the 40.2 ha refused east of the limits is **4.30 ha of plantable lakeshore and 33.6 ha of sand prairie whose own record carries no tree at all**, so most of it was never a woody omission; and **`SPECIES` is keyed by species id, which breaks the first time a species is recorded twice** — `populus_deltoides` is a 22–30 m gallery emergent AND a 5–15 m dune leaner, and the beach was one line from being planted with the wrong one. Read its box before adding a species to a second zone |
| — | RENDERING | ~~K45(b3)~~ | **SEEN on `light`** | **DONE 2026-08-17 — the control was inert for the wood and was quietly halving the one thing that must not thin.** Measured before the repair: the three levels planted **472 / 470 / 437 trees** — one wood planted three times, exactly as K45(b2) predicted — while the point-bar willow screen went **258 / 190 / 133 stools**, because the thicket roll is a fixed per-cell chance and a coarser grid visits fewer bar cells. **So the only thing scene detail did was break the screen its own comment says must not be broken.** `keep` is now a fraction on the tree acceptance roll (1 / 0.80 / 0.60, the levels' own triangle ceilings read as a ratio — L121) and the thicket roll scales with its cell instead: **`light` 437 → 257 trees and 133 → 182 stools**, scene triangles **416,222 → 370,738**, `full` unchanged to the stem, and the wood reaches N +391.8 m at `light` against `full`'s +397.7. Read its box before quoting a stem count at any level but `full` |
| — | RENDERING | ~~K45(b2)~~ | **SEEN** | **DONE 2026-08-16** — the planter sweeps the field (reach 27.05 % → 98.37 %), the timber gets the east end Andreas gives it, and `z05`'s own note had Wells Street 440 m from where the committed centreline puts it. Read its box before quoting a reach number or moving a woody east limit |
| — | RENDERING | ~~K48~~ | **SEEN** | **DONE 2026-08-16 — and it refuted its own premise. 0 sycamores became 2.** Both repairs it named are impossible: rescaling to the bands is an unsolvable system in two of four communities (`wet_woods` floors sum to 100/ha under a stand ceiling of 84), and deriving `perHa` from the mix sum contradicts the same dossier's own canopy sentence. The share is not the defect; the **draw** was. Read its box before proposing a change to any weight, density or band |
| — | RENDERING | ~~K49(d)~~ | **SEEN** | **DONE 2026-08-16 — the block permutation works and `prairie_west` does not stripe: matrix deviation 368.80 → 282.89, and the 31.47-slot row is now 3.67.** Its finding is not the repair: **the stratum size is a U-curve**, and K49(b) finding 3's rule is only its left half — a block also has a CEILING, because exactness over the block is read through a sub-window. Measured at five sizes, and the smallest is 7.4× WORSE than doing nothing. Read its box before setting a stratum size anywhere |
| — | RENDERING | ~~R-BUG1~~ | **SEEN** | **DONE 2026-08-16 — the owner's flickering river edge was the NEAR PLANE, and 15.6 % of the drawn bank line is now 3.3 %.** A fixed 0.1 m near against a 3,000 m far leaves two surfaces 350 m away needing 10 cm of separation before the depth buffer can order them, and the waterline is co-planar BY DESIGN. The instrument is the finding: **move the camera 2 mm and photograph the same view twice** — the control is 0 px, so anything that changes is a tie. **Most of what flickers is not the bank (R-BUG6), and its suspect is UNTESTED because the flag written to test it changes nothing.** Read its box before biasing any surface to settle a tie |
| — | RENDERING | ~~K49(e)~~ | UNSEEN | **DONE 2026-08-23 (T-0018) — REFUTED, and in the opposite direction.** The filters do not eat the stratification: over 7,844 dealt slots the survivors sit at **0.65** of what a rank-BLIND filter of the same size departs by, and the riverbank row the parcel was left on refuses **0.0 %** of its slots. The instrument was shown red before it was believed — a width-selective control on the same vectors reads 3.9–5.0. Read its box before blaming a filter for a census row |
| — | RENDERING | ~~K49(b)~~ | **SEEN** | **DONE 2026-08-16 — all six species are standing, 6 absent → 0 over 6,795 slots.** And the screenshot the parcel asked for vetoed half its own repair: on the dense matrix layers the same construction rows the prairie. Read its box before proposing a low-discrepancy draw anywhere else — the answer is layer-dependent, and the census would have merged the striped version |
| — | RENDERING | ~~K49(c1)~~ | — | **DONE 2026-08-16 — the 25 footprints are in, `unconvertible` 25 → 0, and the conversion is measured and NOT shipped.** It moves the shares by up to 3× (June grass 8.1 % → 24.0 %, wood nettle 1.1 % → 6.3 %) and improves both deviations (matrix 219.19 → 197.46, forb 107.18 → 89.11), and it puts *Scirpus atrovirens* at **1.10 slots owed, 0 drawn** — K49(f)'s absolute gate. Read its box before dealing a sward slot off any number |
| — | RENDERING | ~~K49(c2)~~ | **SEEN** | **DONE 2026-08-16 — the conversion is SHIPPED and the tail gate is green on the mirror: matrix deviation 219.19 → 154.19, forb 107.18 → 89.11, worst shortfall 15.21 → 8.50.** Route 1 was built and is **refuted at frame scale** (the sweep alone leaves *S. cyperinus* drawn nowhere at 1.11 owed, because a frame does not hold whole blocks — K49(e)'s question); route 3, which K49(c1) said was "not a route to green", **is** what got there. Read its box before proposing a construction to fix a tail |
| — | RENDERING | ~~K49(a)~~ | — | **DONE 2026-08-16.** The drawn census of the sward, in every community, + the abundance-unit audit. **And the lesson that is not about flora: the gate's own station reports 0 species absent, because it stands in one community of ten.** Read its box before quoting a flora share or a per-frame figure the smoke prints |
| — | RENDERING | ~~K49~~ | **SEEN** | **opened 2026-08-16 by K48.** Every other weighted draw in this project is the same shape and none has been asked what its tail does — the 63 inferred households, the roof coverings, the massing-variety picker. K48's own finding is that a small weighted sample loses its rare end permanently when the seed is fixed. Pick one, census what it actually draws, and it is visible wherever the answer is a building |
| — | RENDERING | ~~K47~~ | — | **DONE 2026-08-16 — and it inverted: claimed SEEN, delivered UNSEEN.** The sycamore's archetype is built and `drawn_as_another_species` is empty; the tree is **0 of 163 stems**. Read its box before quoting v139 or K45(b1) on what stands by the river |
| — | RENDERING | ~~K46~~ | **SEEN** | **DONE 2026-08-16** — the written weight plants the stem, and route 3 was refuted by the DATASET: ZONE 6a and 6b are one record, so a zone-keyed density cannot hold the elm at 60 in the thicket and 12 in the pocket. 23 of 26 weights sit inside their own cited band, 3 below, **none above**. Read its box before quoting a mix weight or a species share |

**If you are about to claim an UNSEEN parcel, stop and read the rule.** It needs one of three
written exemptions: an owner-reported bug, the second half of a measure-then-fix split, or a gate
that is blocking a named SEEN parcel. "It would be good to have" is not one of them.

**And if the SEEN rows above are all blocked, that is the finding** — say so in the PR and pull a
SEEN parcel up from the sections below rather than defaulting to another gate.

**AND THAT IS WHAT HAPPENED — 2026-08-16, R-A1, the first run to take this paragraph rather than
the table.** Every numbered SEEN pick was blocked (K30(c), T-E3, R-W2c, T-V1(b) need a bake; T-V2
and R-W1 were parked on `hold` — **both landed 2026-08-16 when the whole `hold` queue was worked
down; see R-M1c for why three of the four holds were one instrument fault**; R-W2b is a 315-record
schema change with no source stating a roof
covering), and the only unblocked NEXT UP row was **K49(e)**, which is UNSEEN — and the visible-
progress cap forbade it: v148 is already the one invisible run in the last four, so a second would
have made it two in four. So a SEEN parcel was pulled up from the sections below and shipped. **It
took ~25 minutes of budget to establish that, which is what the box below exists to save** — but
the pull-up route is now proven, and `R-A1`'s own section is the model: a parcel deferred for a
reason, whose stated precondition another parcel has since met, is a SEEN pick hiding in the file.
Search for *"deferred"* and *"unblocked"* the way T-E5(a) searched for `not_modelled`.

**THE TABLE ABOVE IS NEARLY OUT OF PICKS THIS RUNNER CAN CLOSE — counted 2026-08-16 by K28, and
stated here because the next run will otherwise spend a third of its budget rediscovering it.**
Of the numbered picks left standing, **T-V1(b), K30(c), T-E3 and R-W2c all say NEEDS A BAKE** and
cannot go green on the improve runner; **T-V2 landed 2026-08-16 (its `hold` was withdrawn — the
number it was parked on had been fixed by other parcels), and R-W1 is still on `hold` PR #125**;
**R-W4c(b2), T-I3(b) and R-M1b are blocked on the owner**; and **R-W5a2's own box says to take it
only when the lane has nothing sharper**. That leaves **R-W2b** — whose R-W2a finding 2 makes it a
schema change across 315 records with no source yet stating a roof covering, so it is larger than
"unblocked" reads — and **T-E5**, whose ground half also needs a bake though its research and
`docs/LIBERTIES.md` half does not. **The lane needs new parcels opened more than it needs the next
one picked**, and the bake-shaped backlog is the reason: four parcels are waiting on a nightly.

**AND THE COUNT IS BETTER THAN IT WAS — 2026-08-16, K45(b2).** The box above says the lane needs
new parcels more than it needs the next pick, and this run left **two runner-closable SEEN ones**
where it took one: **K45(b) change one** (the dune community, whose hard question K45(b2) removed
rather than answered) and **K45(b3)** (the detail control, which K45(b2) measured as doing nothing
at all). Both are rows 1a and 1b in the table above. Neither needs a bake.

**T-E5 WAS THE LAST OF THOSE TWO AND IT IS TAKEN — 2026-08-16, T-E5(a).** The count above was
right and the paragraph's own advice is now the binding one: **the lane needs new parcels opened
more than it needs the next one picked.** T-E5's bake-free half is spent, its successor T-E5(b)
needs a bake, and every other numbered pick still sits behind a bake, a `hold` PR or the owner. So
the next runner-closable unit here is most likely **a parcel this file does not yet contain**, and
the honest way to find one is the way T-E5(a) found its own: read a deferral, a `not_modelled`
entry or a "deferred to parcel (c)" phrase and ask **what question it was never asked**. That is
where four of the last six findings came from.

**AND IT PAID A THIRD TIME, ONE LINK FURTHER IN — 2026-08-16, K36(b).** The successor to the
paragraph below took its own advice literally: K36(a) had gated a transformation and named its
output a fault about NAMES, so K36(b) asked what else that transformation changes. The answer
was the town's draw-call budget, breached at half its scene anchors, on a flag whose
documentation says it does the opposite. **The generalisation: when a tool's own justification
for a step is a number, measure the number in YOUR system.** `--palette` merges materials
inside one file; this renderer batches across files; those are not the same currency and
nothing had ever converted between them. The lane is full of steps justified by a
tool's README — `--simplify`, `--compress`, `meshopt`'s bit depths, the AO bake's own nightly
(B-A1 asks exactly this question of it, and is still unclaimed).
**And it opened TWO runner-closable parcels, K37 and R-W6(b)**, which is the count the box
above says the lane needs more than it needs the next pick.
**K37 IS SPENT — 2026-08-16 — and it opened two more of the same shape.** Its own finding was
that the parcel's question ("are these 90 special?") had the wrong subject: the discriminator was
not the asset's kind but a number nobody had taken, and taking it convicted three assets the
parcel never suspected. The two it leaves open are both *writers of `assets/web/` that nothing
decided*: `generators/inferred_placeholder.py`, which seeds the tree from the master on every
run, and `tools/publish.sh`, which copies a master through on an **mtime** comparison. Three
scripts write that directory and only one of them is the step. **The generalisation, and it is
the K36(a) seam one turn further: when a directory has more than one writer, the gate on its
contents is a gate on the last writer only.**

**AND THAT SENTENCE WAS WORTH A PARCEL ON ITS OWN — 2026-08-16, K38.** It took K37's
declined paragraph verbatim and the answer was worse than the paragraph guessed: the count
is not three writers but **four passthrough branches across three scripts**, three of them
silent, and the fault is reachable in one command. Two masters `touch`ed and
`tools/publish.sh` run put **1,212,760 uncompressed bytes into the payload** and drew
**CHECK PASS** from the entire dev gate — because a master copied over its own derivative
satisfies assertions 1 through 7 *by construction*. **The generalisation one turn further:
a gate written against a transformation is not a gate on its output directory**, and the
difference is invisible for as long as only the transformation writes there. Two of this
project's directories now have more writers than gates, and `assets/gltf/` — written by
`generators/build.py`, by the nightly, and by whatever a parcel does with `--only` — has
never been asked the question at all. K38's own successor K39 is the narrower half: the
step knows which master it compressed and writes it down nowhere, so staleness is still a
timestamp.

**AND THE NARROW HALF WAS THE ONE THAT PAID — 2026-08-16, K39.** The record itself is
exactly what K38 predicted and took an afternoon. The finding came from trying to VERIFY
it: a seeded hash wants a reproduction control, this repository claims one in as many
words (*"it reproduces 331 of 334"*), and **the claim is false** — 6 of 20, with the other
14 reproducing byte-for-byte under a flag K36(b) turned off two parcels ago. **The
generalisation, and it is the K36(b) seam turned on ourselves: when a repair regenerates
SOME of a set, the remainder becomes the output of a step that no longer exists.** K36(b)
regenerated 38 of 241 and said so honestly; nothing asked what the other 203 were. This
project has done partial regenerations at least three times — K36(b)'s 38, K37's 3, and
R-W6's terrain that never reached the file at all — and each one left a cohort behind.
K40 is this instance. The question is worth asking of `assets/gltf/` too, where the
nightly, a `--only` run and `generators/build.py` all write.

**THE SEAM IS STILL OPEN, AND IT PAID AGAIN — 2026-08-16, K36(a).** Same move as K34, one link
further out: instead of a rule about a record, take a rule about a FILE — *"a stale committed GLB
is a check failure, not a warning"*, *"the bytes a visitor downloads have to be the bytes
something tested"* — and ask which of the steps between the data and the browser anything
actually measures. Two of three, it turned out, and the ungated one had been shipping 75
textures out of a repository that contains none. **The generalisation worth carrying forward:
this project gates its ARTEFACTS at their ends and not at their transformations**, and every
transformation here is a script with a flag in it. `publish.sh`, `compile_scene.py` and the dev
preview assembler are the same shape of thing; two of them now have a gate and the question is
worth asking of anything that rewrites a file on its way out.

**THE ADVICE WORKS, AND THE RICHEST SEAM IS NOT THE DEFERRALS — 2026-08-16, K34.** It took the
paragraph above and widened it one step: instead of a deferral, read a **rule this project states
about itself** and ask what enforces it. AGENTS.md's standing constraint on the removal is the
most important sentence in this repository and nothing had ever measured what it covers; the
answer was "the buildings, and not the people", plus one record that claimed the flag in prose
and never carried it. **`docs/` and `AGENTS.md` are full of sentences of that shape** — a rule
stated, a mechanism named, and nothing that runs. K35 is the successor this one opened, and the
seam is not exhausted.

**R-W5a is DONE (2026-08-15) — the town was paying one draw call per COLOUR OF PAINT, and the
growth term is now zero.** All 47 building batches were the same `MeshStandardMaterial` in every
respect a renderer distinguishes — metalness 0, no map of any kind, `DoubleSide`, opaque, no alpha
test, smooth-shaded. The only fields that differed were `color` (39 distinct values) and
`roughness` (16). Base colour moved to a per-vertex attribute and left the key, so **47 batches
became 16** and **11 of 22 station-viewports over the ≤ 80 budget became 0**. Full table and the
identity proof under R-W5a below. Three things came out of it that are not the number:

- **R-G1's "+11 draw calls per 19 roofs" was 11 new MATERIAL GROUPS, not 11 objects** — which is
  why it was uniform at bearings 150° apart: it counts paints in frame, not buildings. That term
  is now **zero by construction**: a new roof of any colour joins an existing batch. T-A8 and the
  399 roofs behind it are unblocked, and no future block parcel needs to think about this.
- **Triangles are identical to the triangle at all 22 station-viewports**, which is the proof that
  nothing was dropped to buy the calls.
- **The frame is not byte-identical and the difference is quantified rather than waved at**:
  2 of 22 shots hash the same, the rest differ on ~0.013 % of pixels in scattered 7–56 px specks
  at building silhouettes — depth ties resolving the other way under a changed draw order — for a
  whole-frame mean |Δ| of **0.003–0.005 of one 8-bit count**. No surface is repainted; the albedo
  arithmetic is the same product in a different order.

**R-BUG3 is REOPENED (2026-08-15) — the owner reproduced it WITH the fix in.** What it fixed is
real and stays; what it claimed is not. See **R-BUG3c** and **R-BUG4** below, and read them before
quoting any road number. The original write-up follows, corrected:

**R-BUG3's near-field contrast half is done (2026-08-15)** — the owner-reported invisible-at-your-feet road was **the alpha,
and NOT the grass**: the near band scored **1.5 L\* / 30 %** and now scores **3.1 of a measured
ceiling of 3.4 with 80 % perceptible on mobile, 3.2 of 4.3 with 60 % on desktop**, and the alpha
half of the fix fades to nothing by 40 m, so every band past it is unchanged to the decimal. (Those
figures are re-measured on the merge of 2026-08-15; an earlier draft of this line quoted *2.8 of
3.7 / 60 %*, which was one iteration stale and matched neither viewport. The gate prints the bands
— quote it, do not paraphrase it.) Two things were found
that are not the fix and matter more. **The near band was empty at both gated stations, because
neither one stands on a road** — `south_water` is 101 m from its own centreline (T-V2) and
`from_above` is in the air — so the parcel's own first move, adding `[2, 40]`, measured nothing
until a station stood on the roadway. And **a band gated on probes SEEN gates itself out exactly
when the road goes invisible**; the bands are now gated on probes PROJECTED, so that failure is
loud. Full findings under R-BUG3 below — read them before pointing any gate at anything.

**R-BUG2 is DONE (2026-08-14)** — the owner-reported vanishing roads were **two** faults, not one,
and the parcel's prime suspect was **refuted by measurement**. The gate could not see any of it and
now can: `roadContrast()` scores the fault at **0.3 L\* / 14 %** on foot at range and **1.1 L\* /
0 %** from the air, against **4.0 / 92 %** and **2.9 / 91 %** with the fix. Full findings under
R-BUG2 below — read the refutation before reaching for a mip-filter fix anywhere else.

**K21 is DONE (2026-08-15)** — the four trades whose adoption test was silent are silent no longer:
every roof this layer raises now carries the family band its own prose has always named, **29 of 29
census trades resolve across 44 trade-family pairs**, and a gate fails if a household is ever housed
on a roof that names no family. No liberty was owed — the value was already committed twice over —
and rule 6 gains no clause. The parcel's own Watch note was **refuted**: the two sawyer roofs differ
because they were dealt different families. The real archetype split, and the finding underneath it
— **54 of 193 roofs sit outside the band their note cites** — are **K25**. Full findings under K21
below; read the refutation before massing anything off an archetype.

**T-A7 is DONE (2026-08-15)** — a lot was known to be free by the *absence of a centroid*, and a
building standing proud of its own frontage has its centroid in the road, so four documented
buildings — the Temple Building, Harmon & Loomis's store, the Chicago Democrat's office and the
Cook County courthouse — stood on lots the schedule was offering to anonymous roofs. Occupancy is
now measured by area, in ONE module both halves import. **266 stand and 399 remain, 61 of them on
covered ground** (was 66). Full findings under T-A7 below; read them before claiming a block.

**T-A6 is DONE (2026-08-15)** — the schedule was dealing five of the ten open blocks roofs their
own lots could not hold, and the deal now derives lot occupancy the same way the block generator
does. **266 stand and 399 remain, 66 of them on covered ground** (was 71 — five roofs never had
anywhere to stand; **re-derived to 61 by T-A7**). Full findings under T-A6 below.

**T-A5 is DONE (2026-08-14)** — `blk_randolph_market` carries eight roofs, so **266 stand and 399
remain**, 71 of them on covered ground (**re-derived to 66 by T-A6**). It is the first block whose standing roofs this project's
*own inferred-residents layer* had put there, and it **settles the division question T-A4 left
open**: rule 6 takes three tests, the third being the roof's division, and the written test recovers
all four adoption decisions made before it. It also found what the tests cannot answer — four trades
are housed only in family-less bespoke records, so test 2 is silent rather than negative for them
(**K21**). Full findings under T-A5 below.

**T-A4 is DONE (2026-08-14)** — `blk_randolph_clinton`, the first West Division block, carries
seven roofs and one adopted household, so **258 stand and 407 remain**, 79 of them on covered
ground. It is the first block parcel to arrive at ground that was already partly built, and the
gates that assumed an empty block are what it fixed. Full findings under T-A4 below.

**T-E1 is DONE (2026-08-14)** — the 1830 sheet is registered and read, and it is a **land-title
map, not a settlement map**: a name on a tract is who took title between 1828 and **1836**, not
who lived there and not that anything was built. A named tract may never license an anonymous
roof. Full findings under T-E1 below; read them before T-E2 or T-E4.

**T-A2h is DONE (2026-08-14)** — two of `blk_randolph_wells`'s ten roofs carry an argued
household and eight stay anonymous, under a **two-test rule now written into the household
programme's own `method` list**: a block roof may be adopted only where the trade's committed
argument calls its count a floor rather than a bound, AND the roof's family is one this layer
already houses that trade in. **The adoption is no longer a parcel of its own.** The generator
carries the gate in both directions, so T-A4 onward applies the rule in the same run as the
block — `T-A3h` was the one outstanding backfill because its block landed first, and it is **DONE (2026-08-15)**: every block this lane has placed has now been asked the question, and what the backfill found about the tests themselves is in its box and in K28.

**LANE 3 (ground) is a THIRD lane, opened 2026-08-14** — it touches terrain, sources and the
infill generator's eligibility rule. It is **disjoint from lane 1** (renderer) but **overlaps
lane 2** at `tools/generate_block_infill.py` and the inventory, so **a lane-2 block parcel and
a lane-3 parcel may not run at the same time.** Lane 1 may always run alongside either.

**Why it matters now:** only 86 of the 414 remaining roofs sit on covered ground. Lane 2
exhausts them in roughly a day and a half and then has nowhere to build. Lane 3 is what keeps
the town growing after that — and the owner's condition on opening it is that the geography be
real, not convenient.

**R-G0 is DONE (2026-08-14)** — the harness and the baseline are in, so every parcel below
opens with `node tools/critic_shots.mjs --metrics` and closes with the same command, and
quotes the two tables rather than an adjective.

**R-G1 is DONE (2026-08-14) — the baseline scores 4.18 of 10, every axis below 7.** Texture
**1.4** is the floor, historical accuracy **6.8** the ceiling, and the five-point gap between
them is the shape of this project. Full tables and per-axis justification in `docs/STATUS.md`
§ "The baseline scored". **Three findings came out of it that are not scores**, and each is
written into the parcel that owns it below:

- **§1 item 7's mechanism does not survive.** 94–100 % of the literal-black pixels lie in
  components entirely above the land/sky row — they are the shaded near canopy, not a shadow —
  and the darkest-decile figure reaches the same surface a second way, because the metric's
  per-column "ground" starts at the top of a crown. **R-W1** owns it; raising a shadow floor
  will not move either number.
- **The horizon-timber metric counts a gable as a tree.** `prairie_south` gained 20 % on that
  metric between two runs with no renderer change, from 19 new roofs. **R-W4** owns the target
  and needs a discriminator before its ≥ 90 % acceptance number means anything.
- **19 roofs cost +11 draw calls at seven of eleven stations**, taking the over-budget count
  from 4 to 6 desktop. Extrapolated over the 414 remaining roofs that is about +240 against a
  budget of 80. **R-W5** owns it and should treat batching as its first question.

**T-A3 is DONE (2026-08-14)** — `blk_randolph_dearborn` carries **nine of the ten roofs the
schedule dealt it**, so **251 stand and 414 remain**, 86 of them on covered ground. The tenth was
a civic roof and is deferred with its reasoning: the parcel shape repeated exactly as T-A2
predicted, and what it found was that one family cannot be massed at all. See T-I3.

**T-A2 is DONE (2026-08-14)** — `blk_randolph_wells` carries ten roofs, so **242 stand and 423
remain**, 95 of them on covered ground. The parcel authors no coordinates: block parcels are now
a recipe entry read against the committed lot polygons, which is what makes T-A3 onward cheap.

**T-A1 is DONE (2026-08-14)** — 232 roofs stood, 433 remained, and
`data/reconstruction/1835_665_roof_programme.json` schedules them per block. Only **105 of
the 433** have modelled ground to stand on, so lane 2 has about ten block parcels of work in
it and then it is blocked on S9 street control and the terrain extensions, not on recipes.

---

## LANE 1 — RENDERING · phases from `docs/RENDERING.md`

Acceptance numbers are copied from RENDERING §5 so a builder does not have to hold two
documents open. Where a phase has a bake-dependent half, it is marked — ship the half you
can and say so.

### R-BUG5b — the trees are still in the river · **DONE 2026-08-16 · the whole wood was drawn mirrored**

**THE WOOD WAS TESTED IN ENU AND DRAWN IN WORLD SPACE, AND THE TWO POINT OPPOSITE WAYS.** The
near-field planter in `renderers/web/js/trees.js` walks a 4 m grid and asks every question in local
ENU metres — `terrain.isWater(e, n)`, `communityAt(e, n)`, `terrain.surfaceHeight(e, n)`,
`cellAt(e, n)`, `blocked(e, n)`, `noteStation(e, n, y)`. Then it called
`addTree(buf, spec, px, gy, pz, rnd)`, and `addTree`'s fifth argument is a **three world z**.
`terrain.js`'s own `enuToWorld` is `(e, y, -n)`. The sign was never taken. **Every tree in the wood
was tested at `(px, pz)` and drawn at `(px, -pz)` — the entire near-field woodland mirrored across
the datum's east–west line through the forks.**

**The numbers, measured on `dev` as it stood (the build in the owner's screenshot):**

| | |
|---|---|
| stations recorded | **391** |
| stations wet at the point that was TESTED | **0** — which is why every gate was green |
| stations wet at the point that was DRAWN | **64** (16.4 %) |
| drawn vertices over the water mask | **12,285 of 77,688** (15.8 %) |
| …more than 4 m from the nearest dry ground | **10,734** |
| worst distance from dry ground | **48 m** — at E 160.1, N 47.8, 0.61 m above the water |
| nearest station to a vertex, read as ENU `n = -z` | **∞** (no station anywhere near the geometry) |
| nearest station to a vertex, read as ENU `n = +z` | **13.1 m** — one crown radius. That is the proof |

**THE FINDING IS NOT THE SIGN. It is that three gates agreed with each other and all three were
measuring the same wrong thing.** `wetTreeStations`, `drownedTreeStations` and
`tools/measure_far_timber.py` all walk `stations` — the list the planter writes at the moment it
DECIDES to plant. That list is correct and always was; not one entry of it is in the water. **No
check anywhere read the merged geometry back and asked where a tree was DRAWN**, so a fault that
separates the decision from the drawing was invisible to all of them simultaneously. This is the
generalisation, and it is the sixth green-gate-versus-window disagreement on this project: **a gate
on a placement is not a gate on a picture. If a layer decides in one coordinate system and draws in
another, only a gate that reads the drawn buffers back can see the step between them.**
`renderers/web/js/flora.js` had it right the whole time — `_m.setPosition(e, y, -n2)` — which is
exactly why the sward has never been in the channel and the wood always was.

**R-BUG5 (#196) IS NOT RETRACTED, AND SAYING SO PRECISELY MATTERS.** `main_stem_belt_east` really
is authored between the two banks, really is 39 of 39 samples over water, and really should not be
drawn; that clip stands and its gate stands. What #196 got wrong is the ATTRIBUTION: it explained
the owner's photograph with the horizon band, shipped, and told the owner it was fixed. The band
was a second, genuine fault that happens to sit in the same direction from the same viewpoint. The
lesson it paid for is the one its own box asked for and did not get — **reproduce the frame before
choosing a cause.** This parcel's first commit was a screenshot, not a diagnosis.

**How the frame was reproduced, so the next person does not have to find it again.** The owner's
pose is `local_e -100, local_n -40, yaw_deg 76, altitude_m 1.22` — the south bank west of the
forks, 4 ft up, ENE 076°, which is what the HUD reads in his screenshot. The line of crowns is
at 130–190 m, over the main stem. `tools/shoot.mjs` puts the camera there in one command.

**The repair** is one named function, `worldZ(n) => -n`, applied at the two `addTree` call sites,
plus the comment block that says why it is named rather than inlined. Nothing about which trees
grow where, how many stand, or the evidence behind any of it moved: `perHa`, `edgeFade`,
`clearedFactor`, the waterline gate, the species draw and the seed are all untouched. **Every tree
simply moved to the side of the river it was already recorded as standing on** — so the North
Division's body of timber is now on the North Side, and the south bank of the main stem opens out,
which is what the sources describe and what the town's own `blocked()` footprints were being tested
against all along.

**The two new gates, in `tools/smoke_renderer.mjs`, and both were demonstrated RED on the unfixed
published mirror before the fix went in:**

- *every tree drawn stands at its own station* — every vertex of the merged timber within 24 m of
  some entry in `stations`. **This is the one that could never have passed through the bug**: under
  the mirror the nearest station is twice the vertex's own northing away. Structural, not a
  threshold.
- *no timber is drawn out in the channel* — no vertex over the water mask further than 12 m from
  dry ground, which is a bank willow's lean (see `TREE_DRY_MARGIN_M`'s box and `lean` in `SPECIES`)
  and no more. This is the owner's report in the owner's terms.

**Neither may ever be relaxed into a test of the placement. That is the test that was already
green.**

**LANDED WITH ONE GATE KNOWINGLY RED, AND THE `hold` IT WAS FIRST PARKED UNDER WAS WITHDRAWN ON
MEASUREMENT.** With the wood repaired, `the roads reach the screen from the air, at the aerial
anchor` fails — the FLYING station; **both on-foot road stations are green**, so nothing a walker
sees regressed. It is not a regression in the streets either: not one street vertex moved, and every
street gate — drape, wet vertices, the R-BUG4 panel invariant — is still green.

This parcel was first parked on `hold` asking the owner to accept that red. **The premise of the
question was measurable, and measuring it reversed the answer.** Both columns below were taken the
same evening on the same runner, mobile 390×780, published mirror, with nothing but `trees.js`
between them — `dev` at 3ea4e00 and this branch rebased onto it. The earlier figures in this box
were taken against the pre-R-BUG1 base and are superseded by these:

| aerial anchor, gated bands | `dev` (wood mirrored) | wood repaired |
|---|---|---|
| 100–250 m — seen of 63 projected | 46 | **60** |
| 100–250 m — perceptible | 80 % → **37 probes** | 85 % → **51 probes** |
| 250–600 m — seen of 186 projected | 157 | **177** |
| 250–600 m — median ΔL\* | 2.7 of 6.1 opaque | 2.3 of 4.8 opaque |
| 250–600 m — perceptible | 62 % → **~97 probes** | 54 % → **~96 probes** |
| 250–600 m — weber / ground L\* | 0.1104 / 53.9 | 0.0951 / 52.8 |
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
still divides by `seen`. Score the same band on `nProjected` — fixed at 186 whatever stands in the
way — and **`dev` reads 52 % and this branch reads 52 %.** `dev` is under the 0.55 bar too, and has
been; it reports 62 % only because twenty-nine of its probes stand behind trees that were never
supposed to be there. **The band did not regress today. It stopped being flattered.**

**`ROAD_MIN_PERCEPTIBLE` is NOT lowered** — AGENTS.md § "never weaken an assertion to pass", and
cutting a bar to admit the probes an occluder was hiding is the exact shape of that mistake. Note
too that the honest denominator would not have let this branch through either, which is what makes
it a finding rather than a route: it fails both builds. The band's real fix is **R-W2**'s textured
coverage — its ceiling is 4.8 L\* opaque, so the contrast is there to be spent — and the denominator
is **R-M1c**, opened below by this parcel. **R-W1** (`hold` PR #125) and **R-M1b** (no threshold
source) remain the owner's.

**Why it merged rather than waiting.** Holding a correct, visible, owner-reported fix behind a gate
that was passing on an artefact of the very bug being fixed inverts what the gate is for. Merging to
dev is stage, not ship: it publishes the `/dev/` preview only, and production moves solely on owner
dispatch. Recorded here so no later run reads the red as fresh breakage — it is red on merit, red on
`dev` as much as here, and it belongs to R-W2 and R-M1c.

**What this leaves open, and it is a real question rather than a courtesy.** Every other layer that
decides in ENU and draws in world space should be asked the same question by the same method —
reading its buffers back rather than its intentions. `flora.js` is measured and clean.
`streets.js`, `buildings.js` and `ground.js` have not been asked, and the ROADMAP entry for it is
**K50** below.

<details>
<summary>The parcel as it was written when it was claimed (2026-08-16)</summary>

**The owner reshot the river at 3:14 PM CT, standing 4 ft up on the south bank looking ENE 076°, on
the build whose What's-New panel says — in the same screenshot — "The trees standing in the river
are gone · Fixed · Aug 16, 2026, 1:31 PM CT". A straight line of crowns still runs across the
channel, with scattered ones beside it. The two sights #196 said were "one thing seen twice" are
both still there.**

**#196 is not to be trusted as a starting point, and this is the point of the parcel.** It shipped
`trees.js` (+74), `tools/measure_far_timber.py` (+484), a committed baseline and a new smoke
assertion — and the thing a visitor sees did not change. **Three instruments agreed with each other
and disagreed with the window.** That is now the FIFTH time on this project that a green gate and
the owner's screen have disagreed, after R-BUG2, R-BUG3, R-BUG3c and R-BUG4.

**The first job is NOT the trees. It is to reproduce the owner's frame and see them in it.** Until a
harness stands at that pose and photographs the trees over the water, nothing measured about timber
means anything, and any further fix is aimed at a target nobody has sighted.

**Do this in order and do not skip to the third:**

1. **Stand where the owner stood** — south bank of the main stem, 4 ft eye height, bearing 076°.
   Screenshot it. **If the trees are not in your frame, your pose is wrong, not his screenshot.**
2. **Make the gate FAIL on the current build.** #196's assertion passes today with the defect on
   screen, so it is measuring something else — find out what, and say so, before changing it. A
   check that passed through this bug is evidence about the check.
3. **Only then** work out why the crowns are over water, and fix it.

**One reading of #196 worth testing first, because it is cheap.** #196 changed `trees.js` and the
tools — **it changed no data.** Its own account says the South Water timber belt is *written*
between the two banks, every point over the channel, the worst 3.33 m under the surface. If the
committed line still runs across the river and the fix only taught the renderer to cull crowns over
water, then the cull is either not reaching this band, not reaching this viewpoint, or being applied
in a space where the water test does not answer — the ENU-vs-world swap and the single `y = 0`
water quad are both still live candidates from R-BUG5. **Fixing the record so the belt runs beside
the street it is named after may be the honest repair, not culling the symptom.**

**Acceptance, and it is stricter than #196's because #196 met its own and shipped a defect:**
a screenshot from the owner's pose with no crown over water, posted in the PR **beside the "before"
from the same pose**; the gate demonstrated FAILING on `dev` as it stands today and passing after;
and the What's-New entry does not say "fixed" unless that pair of screenshots is in the PR.

</details>

### K51 — the fauna layer reaches a visitor · **DONE 2026-08-17 — 139 animal records were read by nothing, and the gate that was supposed to notice had been told to expect it**

**Read this box before quoting any layer-read number taken before today.** The census line printed
by `tools/measure_layer_reads.py --gate` ended in the words *"which no renderer opens"* until this
parcel, and by then that clause was a claim rather than a measurement: it was true when K42 wrote
it and the gate had no way to keep it true. It is gone, and the line now separates a figure that
moves a vertex from one a visitor reads on a card, because rolling the two together is how a layer
with no geometry starts sounding drawn.

**What shipped.** The Evidence panel's *What was living here* section: ten habitats in the
manifest's own order, and inside each one every species researched into it — **139 records**, each
with its July status, its presence mode, its abundance, what it would be doing, what it would look
like, its voice, the sign it leaves, and the sources behind the three graded claims. The citations
are the joined records `citations.js` renders everywhere else, not bare ids.

**Numbers, measured rather than promised.** Fauna figures reaching a visitor: **0 of 30 → 30 of
30**. Whole-dataset: **58 of 100 figures reached nothing → 28**, and `data/fauna`'s share of that
is **30 → 0**. Habitats on the card **10 of 10**, species **139 of 139**, citations rendered **54**,
zero page errors at 390×780.

**FINDING 1 — the gate did exactly what it was built for, and that is the part worth carrying.**
K42 wrote assertion 3a to fail *the moment* a layer with no declared reads gains a reader —
*"because the whole of this layer's unread bank rests on nobody opening it"* — and it fired on the
first commit that opened the directory. Thirty figures had to be classified in the same commit
instead of riding on a sentence that had quietly expired. **A gate written against an absence has
to name the event that ends the absence**, or the absence becomes permanent by default.

**FINDING 2 — two of that gate's own controls were written against the repository's state, and
both went silent when the state moved.** Its self-test asserted `not layer_is_opened(src, "fauna")`
and constructed its 3a case by setting `opened["fauna"] = True`. Opening the layer turned the first
into a second copy of the measurement and the second into a case that could not be built at all —
it printed **SILENT** rather than failing, which is the quieter of the two ways a control dies.
Both are synthetic now: a scanner that cannot say *no* about a directory nothing names is broken
whatever this repository happens to contain today. **This is the sixth time on this project that a
green reading came from an instrument pointed at nothing**, and the first where the instrument was
a self-test rather than a flag.

**FINDING 3 — `docs/LIBERTIES.md` L2 has said "ambient wildlife is rendered sparsely" since
2026-08-09, and nothing was rendered at all.** Not sparsely: none. The entry's own revision of
2026-08-11 added a paragraph of measured detail about a dataset no renderer had opened, which is
how a liberty about the scene becomes a liberty about a file. L2 now states what the renderer does
— nothing is drawn, heard or traced — and keeps the decision as the standing intent for whenever
animals *are* drawn.

**What it does NOT do.** No animal is in the 3-D scene, no animal geometry is proposed, and the
standing constraint on depicting people is untouched. Every one of the thirty read declarations is
`shown` and none is `mesh`, deliberately: a state that said otherwise would be the read map making
a claim about the town. K42's route 1 — *"leave it and say so"*, which needs `data/scenes/1835.json`
and L2 to stop implying a reader — is **half discharged**: L2 is corrected here, and the `layers`
list is now honest for a different reason, because the layer does reach the browser.

**Files:** `renderers/web/js/fauna.js` (new) · `renderers/web/index.html` ·
`renderers/web/js/main.js` · `renderers/web/css/walk.css` · `tools/publish.sh` ·
`tools/check_published.mjs` (the copy rule) · `tools/compile_scene.py` (the citation join only) ·
`tools/measure_layer_reads.py` + `tools/layer_reads_baseline.json` · `tools/smoke_renderer.mjs` ·
`docs/LIBERTIES.md` L2.

**Not claimed:** the desktop half of the smoke — ~13 min against this runner's 10-minute
per-command ceiling; see the run-budget box at the top of this file. The section was photographed
at 1280×800 by hand and reads correctly there.

**What it opens.** K42's third route, *give it a reader in the scene*, is untouched and is a much
larger parcel behind a bake. The narrower successor is **K52**: the same question asked of
`data/residents/` — that layer IS published and IS read by the building card, and nothing has ever
censused which of its figures reach a visitor. The read map covers flora and fauna and the two
generators declare their own `CONSUMED`; the population layer is declared by nothing, which is the
state `data/fauna` was in this morning.

### K52 — nobody has censused what the residents' figures reach · **DONE 2026-08-17 — the layer with a reader was hiding seventeen households, and the reader is why nobody looked**

**The census answer, and it is worse than the fauna one it was written to be safer than.**
`data/residents/` had exactly one reader: `tools/compile_scene.py`'s `compile_residents()`
attaches a household to a building's sidecar and `popup.js` names it on the building card.
That join reaches a building through `lives_at` or `works_at` — so **a household whose
residence AND workplace are both unattested at the scene date attaches to nothing and
appeared on no card anywhere in this project.**

| | households | person entries |
|---|---|---|
| in `data/residents/` | 173 | 209 |
| reachable through a building card | 156 | 189 |
| **reachable nowhere, before today** | **17** | **20** |

**One of the seventeen is the Mark Beaubien household** — the man who built the Sauganash,
whose house held the incorporation election of 10 August 1833, and whose own record calls
itself *"the most famous household in the town and one of the thinnest records in this
parcel."* He is unreachable for exactly the reason his record is interesting: he had left
the Sauganash by 1834 and the Exchange by August 1834, so where he slept on 1 July 1835 is
not in the record, `lives_at` is `null`, and the join drops him. **The layer was dropping
records for being poorly evidenced, which is the opposite of what the confidence model is
for.**

**Finding 2 — a reader is not a read map, and this one carried a third of each record it
did reach.** `compile_residents()` copies id, name, division, the relation, its note, and a
person's name, relationship, grade and occupation *word*. Everything else stopped at the
repository: `arrival`, `origin`, `reason_for_coming`, `party_size_on_arrival`,
`present_on_scene_date`, `touches_removal`, a person's `sex`, `age_on_scene_date`,
`birth_year`, `name_basis` and their own `sources`, the occupation's grade and reasoning,
and the ten `researched_not_resident` findings whose own manifest doc calls them *"as
load-bearing as the households"*. **This is what K52's box predicted in as many words** — *"a
layer with one reader is exactly where an unread figure hides, because 'the browser has it'
reads as 'somebody looks at it'."* It was right, and the hiding place was bigger than the
fauna layer's, which at least had the decency to have no reader at all.

**Finding 3 — K42's assertion 3a did NOT fire here, and that is a hole rather than a pass.**
`tools/measure_layer_reads.py` scans `flora` and `fauna` and nothing else, so giving
`residents` a reader tripped no gate. The fauna parcel was caught by its own instrument; this
one was caught by reading the join. **Extending the census tool to `data/residents/` is not
done and is opened as K52(b)** — the tool is built around flora/fauna figure kinds and the
extension is its own parcel, not a line in this one.

**What shipped.** `renderers/web/js/residents.js`, the Evidence panel's people section: the
manifest in one fetch, all 173 households listed with their division, their people and their
grade tallies, the 17 marked on their own rows in the conjectural colour, and each household's
full record fetched the first time its row is opened. Every graded claim shows its value, its
confidence swatch, its reasoning and its joined citations; the ten researched non-residents
are published with theirs. **Nothing is drawn** — L1 and the standing constraint on depicting
people are untouched, and nothing in `docs/LIBERTIES.md` needed a line because nothing was
invented: this parcel published records that already existed.

**Files:** `renderers/web/js/residents.js` (new) · `renderers/web/index.html` ·
`renderers/web/js/main.js` · `renderers/web/css/walk.css` ·
`tools/compile_scene.py` (`compile_residents_sources`, the citation join, 11 sources) ·
`tools/smoke_renderer.mjs` (ten assertions) · `data/sidecars/1835/residents_sources.json`.

**Not verified here:** the desktop half of the smoke does not fit the runner's ten-minute
per-command ceiling (§ THE RUN BUDGET). The mobile half ran on the published mirror: **263
passed, 2 failed**, and both failures are the road-contrast bands `dev` already carries red —
see `docs/STATUS.md` § *Landed with two bands red*. This parcel changes no 3-D rendering.

### K52(b) — extend the read census to `data/residents/` · **UNCLAIMED · UNSEEN · opened 2026-08-17 by K52 · Effort: S–M**

`tools/measure_layer_reads.py` covers `flora` and `fauna` by name — its kinds, its baseline
and its self-test's negative control are all written around those two — so `residents` gaining
a reader today fired nothing. K52 answered the question by hand (finding 1 and finding 2
above, both measured off the join); what it did not do is put the answer under a gate, so the
next figure this layer adds can go unread exactly as the last 20 did.

**It is UNSEEN and carries no exemption of its own.** Take it the way K52 was taken, or behind
a parcel that ends in something visible.

### K53 — every shrub in the town is drawn as a giant forb · **DONE 2026-08-17 — the archetype is in, the recorded width is drawn, and the reason only fourteen of them stand is measured**

**The whole shrub layer is drawn with `forbGeometry()`** — one 12-triangle herbaceous stalk with
four broad leaves, scaled to the record's height. Twenty-one records across eight zones carry
`form: 'shrub_low'`, and `FORB_FORMS` contains that string, so a 3 m American hazel, a 2.5 m
elderberry, a multi-stemmed black-oak grub and a *sprawling mat* of sand cherry are all the same
wand of leaves at four different sizes. `placeForb`'s own comment names the damage and treats the
symptom: *"a riverbank shrub recorded at two metres across therefore grew sixty-centimetre leaves"*
— so the recorded clump width is CLAMPED to 0.40 m of spread, which is the shrub layer being made
narrow enough to look like a forb rather than being drawn as a shrub.

**It is SEEN and needs no exemption.** `corylus_americana` is the wet woods' *attested* dominant
shrub at 20–50 % cover — the dossier's own headline finding, with *"under-rendering hazel is the
specific mistake this record exists to prevent"* written beside it — and it is a wand. So is the
elder at the gallery edge, the dogwood on the river bank, the currant in the fenced dooryards and
the willow scrub on the lakeshore back slope, which is the population K45(b4) recorded as *"still
not planted"* in as many words.

**What it is NOT:** it is not a new record, not a new density and not a bake. Every number this
draws with — height, clump width, foliage greens, the July head — is committed and already read;
the archetype that consumes them is what is missing. The shrub form itself is a **reconstruction**
and gets a `docs/LIBERTIES.md` entry, exactly as the nine flower archetypes did.

**Files:** `renderers/web/js/flora.js` (a `shrubGeometry` archetype, a set beside `rosetteSet`, a
`placeShrub`) · `data/liberties.json` + `docs/LIBERTIES.md` · the flora gates' baselines if a read
moves · `renderers/web/js/changelog.js` · `site/chicago/4d/` · `docs/STATUS.md`.

**WHAT SHIPPED.** `shrubGeometry()` — four woody stems from one root, sixteen leaf sprays over
them, 40 triangles against the forb's 12 — on its own instanced set `flora-shrub`, dealt from the
forb lattice so it takes slots the forb archetype used to take rather than adding any. `placeShrub`
reads `width_m` as what it is on a shrub: the clump diameter. **Measured on the published mirror, at
all eight anchors and four bearings each:**

| | before | after |
|---|---|---|
| plants drawn with the shrub archetype | **0** | **14** |
| clump width | 0.40 m, the forb clamp | **1.80 m median, 2.00 m worst** |
| forb-layer plants, all archetypes | 2,201 | 2,187 + 14 = **2,201** |
| flora triangles, worst view | 41,754 | 41,772 |

**The census is identical plant for plant**, per zone as well as in total (`z08_lakeshore` 131 →
122 + 9, `z05_riverbank_timber` 61 → 57 + 4, `z06_dense_forest` 222 → 221 + 1). Nothing was redealt,
no density moved, and no record changed: this parcel changes what a plant is DRAWN as and nothing
else, which is why the sward census gate reads the same 6,809 slots and the same 154.19 / 89.11
deviations K49(c2) banked.

**FINDING 1 — the wands were only survivable because the width was clamped away.** `placeForb`
clamps spread to 0.40 m, and its own comment says why: *"a riverbank shrub recorded at two metres
across therefore grew sixty-centimetre leaves"*. That is the leaf archetype being protected from a
number that was never a leaf. `prunus_pumila`'s committed appearance is *"low sprawling mats 1-3 m
across"* and it was drawn 0.7 m wide and vertical. **A clamp that exists to protect one archetype
from another's data is a missing archetype, stated as a bound.**

**FINDING 2 — and it is why this is fourteen plants and not a hundred and forty: the forb lottery
deals by HEAD COUNT, so it under-draws exactly the plants that are big.** K49(c2) moved the lottery
onto `stems` — plants per m² — to fix the opposite fault, a species recorded as covering 25 % of the
ground being dealt as 0.25 plants/m². The conversion for a cover-recorded species is
`cover / (π · (width/2)²)`, so a hazel that covers 7 m² of ground converts to 0.088 plants/m² and
competes for slots against `allium_tricoccum` at **40 plants/m²**. Measured over each zone's forb
list, the shrubs' share of the lottery is:

| zone | shrub share of the forb list | the species that takes the rest |
|---|---|---|
| `z10_settled_town` | **0.1 %** | four weeds at 0.4–1.1 plants/m² |
| `z06_dense_forest` | **1.0 %** | `allium_tricoccum`, 99.0 % |
| `z08_lakeshore` | 2.6 % | `artemisia_campestris`, `campanula_rotundifolia` |
| `z05_riverbank_timber` | 3.0 % | `allium_canadense`, 97.0 % |
| `z09_sand_prairie` | 7.6 % | `allium_cernuum`, `monarda_punctata` |

So `corylus_americana`, **attested** at 20–50 % ground cover and named in its own note as the
specific under-rendering this record exists to prevent, is drawn as **1 plant of 221** in the wet
woods. The count is not wrong — one hazel IS one plant — but the layer is a SAMPLE of ~220 slots
against a population of tens of thousands, and a sample drawn by count reproduces the population's
head count while reproducing none of its ground cover. **Both readings are defensible and this
parcel changes neither**; the numbers are banked and the question is opened as **K54** rather than
retuned here, because K49(c2) moved this lottery deliberately and moving it back is a decision, not
a repair.

**FINDING 3 — the first cut of the archetype was the wand at a larger size.** Four stems each
carrying one 60 cm paddle reads as a candelabra, not a bush; the shot showed it and the fix was
sixteen small sprays over two heights rather than four big ones. **A silhouette is made by its
outer shell**, which is the same thing `trees.js` says about a crown in its own comment — and it is
worth writing down that the archetype had to be LOOKED at, twice, after it measured correct.

**Verified:** `tools/check.sh` — CHECK PASS (the dev gate; `chicago-4d-check.yml` runs it and
nothing else), after `tools/publish.sh` in the same commit. `tools/measure_sward_draw.mjs --gate` —
PASS, 0 of 98 (list, species) pairs drawn nowhere, 6,809 slots, deviations unmoved. The before/after
readings above are `flora-shrub`/`flora-forb`/`flora-rosette` instance counts and their `aFlora`
attributes read back off the published mirror at 1280×800, against a worktree of `origin/dev` for
the before column. Evidence: `docs/evidence/k53-{before,after}.png`, the river-bank stand at
E −288 / N +368 facing SSE. **Zero page errors** in every run.

**NOT verified here:** neither half of `tools/smoke_renderer.mjs`. The desktop half has never fitted
this runner's ten-minute per-command ceiling and K45(b4) recorded the mobile half outgrowing it too;
the three gates in it that read the flora sets by NAME were extended to `flora-shrub` in this commit
(rooted-plant anchoring, the pop-in walk, head support) plus `tools/measure_head_support.mjs`, so
the new set is inside them rather than invisible to them — but that extension is unexecuted here and
is the first thing to run on a runner without the ceiling.

### K54 — the forb lottery deals by head count, and the shrub layer is the population it loses · **DONE 2026-08-17 — route 2, and neither reading of the sample was the fault: the two strata were sharing one lattice**

**The answer to "which quantity should a sample reproduce" is that this sample did not have to
choose.** A lattice slot is 2.89 m² of ground and carries one plant, so where the herb layer's own
recorded density SATURATES the lattice — five of the ten communities — the deal stops being a
population draw and becomes a count-proportional subsample. A subsample by head count thins the
shrubs by the whole saturation ratio, and in the wet woods that ratio is **117**. But a hazel clump
stands OVER the leeks rather than instead of them, and the records state the two separately: nine
`shrub_low` records in `z06_dense_forest` summing to **94.9 %** ground cover, above a herb layer
recorded at **40 plants/m²**. So the shrub stratum is dealt from **its own lattice pass over the same
ring**, at its own recorded clump density, with a different salt so the two draws are independent.
**Nothing is taken from the herb layer to pay for it, and no share, cap or tuning number was
authored.**

| `tools/measure_sward_draw.mjs`, published mirror, 8 communities stood in | before | after |
|---|---|---|
| shrub instances standing, summed over the 8 stations | **4** | **181** |
| shrubs drawn standing in `z06_dense_forest` | 2 | **156** |
| drawn shrub cover there, against a recorded 94.9 % | ~0 | **40.1 %** |
| drawn shrub cover, `z05_riverbank_timber`, recorded 19.5 % | 2.0 % *(the whole forb list)* | **20.1 %** |
| deviation per 100 slots — matrix | 2.58 over 5,965 | **2.58 over 5,965** |
| deviation per 100 slots — forb | 10.56 over 844 | **10.40 over 781** |
| deviation per 100 slots — shrub | — | **10.41 over 181** |
| (list, species) pairs owed a whole slot and drawn nowhere | 0 of 98 | **0 of 98** |

**The gain K54 required is kept, and the raw sums cannot show it** — `forb 89.11` became
`forb 81.22 + shrub 18.84` because the deviation is an absolute sum over slots and this parcel split
one list into two. Per 100 slots the herb list IMPROVED and the new shrub list draws at the same
fidelity. Hence the tool's new per-slot column: **a discrepancy sum cannot compare two draws of
different sizes**, and every previous parcel that quoted 89.11 against another build was comparing
lists of the same length by luck.

**FINDING 1 — the slot count still mixed units, and it planted the riverbank understory 8.8× too
thickly.** K49(c2) moved the LOTTERY onto `stems` and its own comment says the slot count was left
on the recorded sum. That sum adds cover fractions to plants per m², and sixteen of the twenty-one
shrub records state an area: `z05_riverbank_timber`'s forb share was **0.636 where its herb records
give 0.072**, and `z07_bur_oak_savanna`'s hazel — its only forb-list species — was planted at **4×**
its own recorded clump density. So the riverbank swap is not only more shrubs: it is **11 dogwood,
elder and ninebark clumps carrying 20.1 % cover in place of 33 herbs carrying 2.0 %**, and the herbs
that left were never in the record. Dealing the shrub stratum off `stems` closes it for that
stratum; **four herb lists still carry it (`z03`, `z05`, `z06`, `z10`), and the tool now names them
with a `basis` column. Opened as K55.**

**FINDING 2 — the instrument K54's own box named cannot answer K54's question, and had been
mislabelled since K49(c2).** `expected` is `share × slots` and `share` is the species' share of the
LOTTERY, so *"deviation from the recorded cover"* — the line this box quoted as *"the very quantity
in question"* — measures the lattice's disagreement with its own target distribution and never
touches a record. It is the right figure for comparing two draws and the wrong one for judging
fidelity to the data. The tool prints a real `cover` column now, and **its first denominator was
wrong in R-M1c's exact way**: dividing a community's drawn plants by the whole ring reported 17.9 %
where that community holds a fifth of the ring. It divides by the community's own MEASURED plantable
ground inside the ring — 1 m² samples through `zoneAt` and `plantableAt`, the placer's own rules.

**What it costs and what is NOT verified.** One extra lattice pass over the forb ring per rebuild;
`flora-shrub` was already a committed set and a committed draw call, so the frame gains instances and
no batch. Neither half of `tools/smoke_renderer.mjs` ran — the desktop half has never fitted this
runner's ten-minute per-command ceiling and the mobile half has outgrown it (K45(b4), K53) — and the
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
shrubs would take **30–100 %** of the forb list's slots in seven of ten communities, because the herb
forbs' own summed cover is under 1 % of the ground in most of them — the ground cover in a prairie
belongs to the MATRIX list, which is dealt separately. Route 3 (say it on the card) was available and
is now unnecessary.

**FINDING 3 — and it came from LOOKING, which is K53's finding 3 one parcel later: the archetype
was designed and photographed at fourteen instances in the whole scene, and the wet woods now
carries 158 in one ring.** `docs/evidence/k54-{before,after}.png`, the same station (E −54 / N +314,
bearing 135°) at 1280×800 on the published mirror: the before frame is an open field with a log
building 15 m away and ONE shrub in the corner; the after frame is a thicket the building shows
through. That is what the record asks for — `z06_dense_forest` reads_as *"a hazel shrub layer
through all of it"* and its nine shrub records sum to 94.9 % cover — and it is also the first time
anyone has seen this archetype repeated. **At that density its leaf sprays read as ~0.4 m paddles**,
which is the shell L122 bounded to 0.30–0.55 of the recorded half-width and is defensible on a
2.25 m hazel; whether it should scale that way is now a question a visitor can answer, and it is
opened as **K56**. Flora triangles at the station **46,904 → 58,868**; the herb layer is untouched
(forb 194 → 195, rosette 35 → 31) which is the arithmetic proof that nothing was taken to pay for
it; zero page errors.

### K54 — original statement, for the record · **superseded by the box above**

**The arithmetic is banked in K53 finding 2 and is not in dispute.** The forb layer deals ~220
slots over the ring; each slot is one plant; species compete for slots on `stems`, plants per m².
A hazel covering 7 m² of ground is 0.088 plants/m² and a wild leek is 40, so the wet woods are
drawn as leeks with one shrub in them, and the shrub layer their own dossier calls the dominant
one takes **1.0 %** of the deal.

**The question is which quantity a SAMPLE should reproduce.** By head count the current deal is
exactly right and the frame is wrong; by ground cover the frame would be right and the head count
wrong. Three routes, none of them free:

1. **Deal a fixed share of the slots to the shrub sub-list**, off the recorded `cover_fraction` —
   the field the shrubs mostly carry — and deal the rest by count as today. Honest, cheap, and it
   makes the layer's slot mix a second authored quantity that no record states.
2. **Give the shrubs their own lattice**, the way `trees.js` has one: a sparse layer dealt on
   plants per hectare over a wider radius, which is what a shrub layer physically is. The most
   faithful and the largest.
3. **Leave it and say so on the card.** The layer is a count-faithful sample; the Evidence panel
   could say that a drawn plant is one plant and that ground cover is not what the sward reproduces.

**Do not take this as a tuning.** K49(c2) moved this lottery onto counts deliberately and measured
the improvement; whatever lands here has to keep that gain (matrix 154.19 / forb 89.11 deviation,
0 species drawn nowhere) and say which quantity it is now faithful to. **`tools/measure_sward_draw.mjs`
already prints everything needed to judge it** — it reports the deviation from recorded cover, which
is the very quantity in question.

**Files:** `renderers/web/js/flora.js` (`compileZones`, `dealt`) · `tools/measure_sward_draw.mjs`
(a cover-share column) · `docs/LIBERTIES.md` if a share is authored.

### K55 — four herb lists still deal their SLOT COUNT off a sum of areas and counts · **DONE 2026-08-17 — the same fault runs BOTH WAYS, and for the herbs it ran the other one: the riverbank's ground layer was planted 96× too THINLY**

**The repair.** `SLOT_BASIS` is one object naming which sum each stratum's slot count is dealt off,
and both lattice strata now read `stems`. The forb half is what moved; the arithmetic is K54's and
was not re-derived.

| forb layer | density before | after | ratio | forbShare before → after |
|---|---|---|---|---|
| `z05_riverbank_timber` | 0.025 /m² | **2.407** | **96×** | 0.072 → **1.0 (clamped)** |
| `z10_settled_town` | 0.395 | **7.760** | 19.6× | 1.0 → **1.0, no slot moves** |
| `z03_sedge_meadow` | 0.123 | **1.254** | 10.2× | 0.354 → **1.0 (clamped)** |
| `z06_dense_forest` | 40.615 | **44.545** | 1.10× | 1.0 → 1.0 |
| the other six | unchanged to the digit | | 1× | unchanged |

Drawn, on the published mirror over the census's eight stations: **forb slots 781 → 923**,
`z03_sedge_meadow`'s own layer **31 → 84** (cover 1.0 % → 2.8 % of a recorded 11.0 %),
`z05_riverbank_timber`'s **1 → 16** at its own station and **4 → 50** standing in the wet woods, with
a row at `z03` that did not exist before (**0 → 14**). Forb deviation per 100 slots **10.40 → 9.33**.
**Matrix and shrub are unchanged to the second decimal** — 154.19 and 18.84, the same figures K54
banked — and `0 of 98` pairs are drawn nowhere.

### Finding 1 — a cover fraction read as a count is wrong in whichever direction the plant's own size points

K54 measured this fault OVERSTATING by 8.8× and fixed it downward. The herb lists have it
understating by up to 96×, and the two are the same division: `stems = cover ÷ π(width/2)²`, so the
sign is decided by whether one plant covers more or less than a square metre. A 2.25 m dogwood
clump covers ~4 m², so its cover fraction is a bigger number than its count; a 10 cm forb covers
~0.008 m², so its cover fraction is ~125× smaller. **"Adding an area to a count" was banked here as
over-planting because that is the case that was measured first**, and the queue inherited the
direction along with the diagnosis.

### Finding 2 — the report was naming three refusals as work, because it printed a default argument

The parcel's own box suspected the matrix half was a refusal and it is: `matrixShare` comes off
`cover.matrix_fraction` directly, and `subsetOn`'s `density` was **computed for the matrix and read
by nobody**. The `basis` column that named `z03.matrix`, `z08.matrix` and `z09.matrix` as K55 work
was printing `subsetOn`'s default parameter, not a fact about the renderer — so three of the parcel's
six named rows were never faults at all. Both the renderer and the report read `SLOT_BASIS` now, and
the matrix's entry is `null` rather than a label, so there is no number left to misread.

### Finding 3 — it is SEEN, and only just: the count moved a fifth and the picture moved 0.15 %

`docs/evidence/k55-{before,after}.png`, `z05_riverbank_timber` at E −300 / N +398 bearing 090°,
1280×800 on the published mirror: **1,586 changed pixels of 1,024,000 (0.15 %)** — a scatter of white
flower heads through the near grass. At the `z03_sedge_meadow` station the same comparison is **24
pixels at 135° and nothing at 315°**, because the added plants are small and stand under a dense
matrix layer. **The parcel's own prediction that `z10_settled_town`'s weeds were "the visible half"
is refused by the table above**: that share was over the lattice ceiling before and after, so the
one community a visitor spends the walk in is the one community that does not move. Quote the
counts for this parcel, not a screenshot.

### Successor — K58, the forb lattice's ceiling now binds six communities of ten

`forbShare` clamps at one plant per slot, and K55 takes the clamped count from four communities to
six (`z05` and `z03` join `z04`, `z08`, `z10`, `z06`). A clamped share means the record is asking for
more plants than the lattice can carry, so the drawn cover is bounded by `TUNE.forb` rather than by
any research figure — `z06_dense_forest` reaching 40.1 % of a recorded 94.9 % is that ceiling, not a
data gap. Opened below.

### K55 — original statement, for the record · **superseded by the box above**

**The arithmetic is banked in K54 finding 1 and is not in dispute.** `subsetOn`'s `density` sums
`s.recorded` — the abundance in whatever unit the record used — and `forbShareOf` reads that sum as
plants per m². Where a list mixes the two, the slot count is a cover fraction added to a count.
K49(c2) left it there deliberately and said so; K54 fixed the shrub stratum's half of it by dealing
that list off `stems`. **What is left, printed every run by `tools/measure_sward_draw.mjs` under
`slot count off 'recorded'`:** `z03_sedge_meadow.matrix`, `z03_sedge_meadow.forb`,
`z06_dense_forest.forb`, `z08_lakeshore.matrix`, `z09_sand_prairie.matrix` — and `z05`'s and `z10`'s
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

**Files:** `renderers/web/js/flora.js` (`subsetOn`, `forbShareOf`) · `tools/measure_sward_draw.mjs`
baselines · `docs/STATUS.md`.

### K56 — the shrub's leaf spray is scaled off the clump width, and 158 of them in one ring is the first look anyone has had at that · **DONE 2026-08-17 — the spray is a leaf MASS, so the size was never the number: sixteen of them covered 17.7 % of the shell and you could see straight through every clump**

`shrubGeometry`'s sprays are a fraction of the recorded half-width (L122), so a `corylus_americana`
recorded 2.25 m across carries sprays about 0.4 m long. At fourteen instances scattered over the
whole scene that was invisible; at **158 in the wet woods' ring** it is the near-field texture of a
whole community — `docs/evidence/k54-after.png`.

**The question is not whether 0.4 m is right, it is what the spray STANDS FOR.** A grass tuft in
this renderer is a bundle of shoots and says so; if a spray is a bundle of leaves then its size is a
rendering choice bounded by the plant's shell and the answer may be "unchanged". If it is meant to
read as a leaf, a hazel leaf is ~10 cm and no scaling off the clump width can produce one at 40
triangles. **Decide which, write it into L122 or a new liberty, and only then change a number.**

Cheap and visible: one archetype function, one before/after pair at the station K54 used, and
`tools/measure_sward_draw.mjs` is unaffected because no count moves.

**Files:** `renderers/web/js/flora.js` (`shrubGeometry`) · `docs/LIBERTIES.md` · `docs/evidence/`.

**THE ANSWER TO THE QUESTION THE PARCEL ASKED, because it decides which number moves.** A spray
stands for **a mass of leaves on one shoot**, not a leaf. That is the same abstraction the tree
canopy's plates and the near tuft's bundle of shoots already use in this renderer, and it is the
only one two triangles can carry: a hazel leaf is ~10 cm and no scaling off the clump width
produces one. So the honest reading of the 0.4 m spray is **not wrong**, and shrinking it would
have bought a smaller plate with more sky around it. Written into `docs/LIBERTIES.md` as **L124**
before any number changed, which is the order the parcel asked for.

**WHAT THE LOOKING FOUND, and it is the count.** Summed over the archetype's own loop, the sixteen
sprays' plates cover **17.7 %** of the shell they are spread over — a clump a visitor sees straight
through, which is why an isolated plate reads as one enormous leaf: nothing overlaps it. **32
sprays cover 30.9 %.** `docs/evidence/k56-{before,after}.png`, the same station K54 used (E −54 /
N +314, bearing 135°) at 1280×800 on the published mirror.

| | before | after |
|---|---|---|
| leaf sprays per shrub | 16 | **32** |
| spray bands | 2 | **3, the lowest arching DOWN** |
| plate area, archetype units² | 1.399 | **2.698** |
| shell fill | 17.7 % | **30.9 %** |
| triangles per shrub | 40 | **72** (+5,056 in the wet woods' ring, of a 1,000,000 ceiling) |
| spray length on a 2.25 m clump | 0.26–0.44 m | **0.26–0.44 m — unchanged** |
| drawn reach, as a fraction of the recorded half-width | 0.91 | **0.98** |

**FINDING — nothing in the first cut hung below its own attachment.** All sixteen sprays rose, so
the shell stayed open exactly where the four stems are most exposed, and `k0 = shade(0.16)` makes
those stems a black stick wherever foliage does not cover them — which the archetype's own comment
had feared in the abstract and the before frame shows happening. The lowest of the three bands now
arches down over them, bounded so no tip is pushed below the plant's base.

**No census moved.** Same species in the same places, plant for plant; `spread`, `height` and the
lattice are untouched. The gate `tools/measure_sward_draw.mjs` is unaffected, as the parcel
predicted, because no count moves.

### K57 — the spray's GRAIN, which trades triangles against the size of a leaf mass · **DONE 2026-08-17 — asked at a fixed plate area it cannot be asked at all, because the plates carry the recorded clump width; 48 sprays ship at K56's plate size and 48 is where the return halves**

K56 answered *what a spray stands for* and moved the count. It did **not** answer the finer
question underneath: at a fixed total plate area, is the shell better read as 32 masses of 0.4 m or
64 of 0.2 m? That is a grain question and it costs triangles — 32 sprays is 72 triangles a shrub,
64 would be 136 — so it needs a **frame-time and triangle budget measured in the wet woods**, where
158 of them stand in one ring and the matrix layer is densest, rather than a preference.

**What bounds the answer.** The plate may not shrink below the size at which it reads as a single
leaf against its neighbours, which is the fault K56 diagnosed and would rebuild at a smaller scale
if the count did not rise with it. So grain and count move together or not at all.

Cheap and visible: one archetype function, one before/after pair at the same station, and the
triangle line printed by the smoke at both viewports is the budget half.

**Files:** `renderers/web/js/flora.js` (`shrubGeometry`) · `docs/LIBERTIES.md` · `docs/evidence/`.

**What it measured, banked so nothing re-derives it.** 24 bearings, orthographic, on the archetype the
scene draws — foliage cover is the UNION of the projected plates over the convex hull of them, because
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
archetype here — the tree canopy, the near tuft, the forb head.

### K59 — the last 4.4 points of the shrub's shell, and whether a frame can afford them · **DONE 2026-08-23 (T-0020) — the frame was read and the points are spent: 64 sprays ship, for +3.0 % of a frame on desktop and +2.1 % on mobile against a 0.2 % A/B/A control**

K57 shipped 48 sprays at the knee and left 64 measured and unspent: **cover 46.9 % → 51.3 %, worst
bearing 43.0 % → 47.3 %, stem cover 51.3 % → 54.2 %, for 104 → 136 triangles a shrub** and 17,368 →
22,712 in the wet woods' ring of 167, of a 1,000,000 ceiling. Reach is unaffected (0.998 → 0.997), so
this is a pure budget question and the numbers are already banked — nothing needs re-measuring.

**What is NOT known, and it is the whole parcel:** no frame-time figure has been taken anywhere in this
archetype's history. K57 justified 104 on a triangle count and a draw-call count, which is not a frame.
The batch does not split — one instanced set, one draw call, K56 and K57 both — so the cost is fill and
vertex work, and neither has been read. **Take this parcel only with a frame-time measurement in
hand**, in the wet woods where 167 of them stand; without one it is a preference wearing a table, which
is exactly what K57 refused.

**Files:** `renderers/web/js/shrub-grain.js` (`SHRUB_GRAIN.fill`) · `tools/measure_spray_grain.mjs`
· `docs/LIBERTIES.md` · `docs/STATUS.md`.

**THE ANSWER, 2026-08-23 (T-0020). The parcel's own condition was met before anything moved:
`tools/measure_shrub_frame_cost.mjs` is the frame-time instrument this box refused to be claimed
without.** It stands the walker in `z06_dense_forest` — 158 shrubs drawn in one ring, the densest
of the ten communities — sweeps eight bearings and fixes the camera at the most expensive of them
(1,343,341 triangles at 135°), holds the clock, drives frames one at a time rather than letting the
browser pace them, and fences each frame with a one-pixel readback.

| | 48 sprays | 64 sprays | |
|---|---|---|---|
| desktop 1280×800 | 4282.30 ms | 4410.30 ms | **+3.0 %** |
| mobile 390×780 | 2739.60 ms | 2795.80 ms | **+2.1 %** |
| desktop, shipped grain measured AGAIN | **4292.90 ms** | | **+0.2 %** — the control |

**Finding 1 — three points of a frame for 4.4 points of shell, and the control is what makes that
readable.** The A/B/A third row is the identical scene measured after the candidate: the runner's
own drift is two tenths of a point, so the candidate's three are fifteen times it. Cover 46.9 % →
51.3 %, worst bearing 43.0 % → 47.3 %, stem cover 51.3 % → 54.2 %, reach unmoved at 0.997, 17,368 →
22,712 triangles in the ring of a 1,000,000 ceiling. **64 ships** (L175).

**Finding 2, and it is the durable one — `gl.finish()` IS NOT A FENCE HERE, and a measurement built
on it was wrong by a factor of a thousand.** The first cut of this instrument timed `step()` +
`gl.finish()` and reported **2.90 ms** a frame while the process spent about **four seconds** of
wall clock on each one. ANGLE's SwiftShader backend rasterises in another process, so a finish
returns having synchronised nothing a caller can observe; what was being timed was how fast three.js
can TALK, which is the one quantity that does not move when a shrub grows 32 triangles. It even
produced a plausible-looking answer — **+31 %**, which would have refused this parcel. A one-pixel
`readPixels` is a real fence, because the caller cannot be handed a pixel that has not been drawn,
and it is what the renderer's own `capture()` has always used. **Read this before timing anything in
a browser here, and prefer a readback to a finish.**

**Finding 3 — a Playwright route handler is not free.** The grain was first injected by intercepting
`shrub-grain.js` with `page.route`. Registering ANY route turns network interception on for EVERY
request in that context, and this page pulls several hundred GLB and JSON files through it: one page
load went from about eight seconds to over four minutes. The instrument patches the byte at the
static server it already runs instead.

**What this parcel does NOT settle.** Every figure above is a headless software rasteriser on a
shared CI machine — the absolute milliseconds are that machine's, and a frame there is four seconds.
The ratio is the answer, and it argues in the safe direction: a software rasteriser is the most
fill-sensitive renderer available, so it is the harshest witness for the one risk here (overdraw
1.33 → 1.56). The reading L121, L156 and L174 all still want — a real low-end machine — is not this.

### K58 — six forb layers of ten now ask for more plants than the lattice can carry · **UNCLAIMED · SEEN · opened 2026-08-17 by K55 · Effort: M**

`forbShareOf` is `min(1, density × cell² / perCell)`, and the clamp is a lattice ceiling of one
plant per slot. K55 took the number of communities sitting ON that clamp from four to six — `z05`
(2.407 plants/m² asked) and `z03` (1.254) join `z04` (14.5), `z06` (44.545), `z08` and `z10` (7.760).

**What the clamp costs, stated plainly: those six layers are drawn at a density `TUNE.forb` chose
and not at one any record states.** `z06_dense_forest` drawing 40.1 % of its recorded 94.9 % cover is
that ceiling and not a research gap, and K54's box already flagged it as the one community whose
shrub density reached it — the forb stratum has now joined it in five more.

**It is not a free tune, which is why it is its own parcel.** The lattice's cell and `perCell` were
fitted against the reference photographs on a closed prairie sward (L32), so raising either changes
every community and costs geometry in exactly the two — `z06`, `z10` — that already carry the most.
Candidate routes, none of them chosen here: a per-stratum cell; more than one plant per slot where
the record asks for it; or accepting the ceiling and **printing the shortfall per community**, which
is at least honest and is nearly free.

**The measurement to land first**, and it fits in one census run: `tools/measure_sward_draw.mjs`
already knows both numbers, so print `forbShare` beside the drawn cover per community and the size
of the debt is visible without a single plant moving. `flora.communities()` exposes `forbShare`,
`forbShareWet`, `shrubShare` and both densities as of K55, so nothing new needs wiring.

**Files:** `renderers/web/js/flora.js` (`forbShareOf`, `TUNE.forb`) · `tools/measure_sward_draw.mjs`
· `docs/STATUS.md` · `docs/evidence/`.

### K52 — nobody has censused what the residents' figures reach · **UNCLAIMED · UNSEEN · opened 2026-08-17 by K51 · Effort: S–M**

`tools/measure_layer_reads.py` covers `data/flora` and `data/fauna`; `generators/archetypes/*_params.py`
and `generators/terrain_inputs.py` declare their own `CONSUMED`. **`data/residents/` is declared by
nothing.** It is published (`tools/publish.sh` copies it) and the building card names the households
attached to a structure, so unlike this morning's fauna the layer certainly has *a* reader — which
makes it the harder question, not the easier one: a layer with one reader is exactly where an
unread figure hides, because "the browser has it" reads as "somebody looks at it". 96 researched
people, 113 invented names, and no answer to which of their figures a visitor ever sees.

**It is UNSEEN and carries no exemption**, so it is not a pick while the visible queue has picks in
it. Take it the way K51's own gate was taken: as the second half of a parcel that ends in a card.

K42 finding 2, taken: **`data/fauna` has no reader, and three separate documents imply it does.**
139 animal records across ten habitat zones, 90 citations, every one of them researched to the
July gate — and no file under `renderers/` names the directory, `tools/publish.sh` does not copy
it, so a browser has never been offered the layer. K42 wrote three routes and this is route 2,
*"give it a reader"*, which its own box says is a renderer parcel of real size and **no bake**.

**It is a CARD, not a herd.** Nothing is drawn in the 3-D scene: the standing constraint on
depicting people is untouched, and no animal geometry is proposed here. What a visitor gets is
the Evidence panel section this dataset was always for — the ten habitats, what each reads as on
1 July, and every species with its July status, presence mode, abundance, behaviour, voice and
its sources. The visible-progress rule's own definition of SEEN is *"in the 3-D scene or on a
card a visitor opens"*, and this is the second of those.

**The gate it must pass through is the one K42 built.** `tools/measure_layer_reads.py` assertion
3a fails the moment a layer with no declared reads gains a reader — deliberately, *"because the
whole of this layer's unread bank rests on nobody opening it"*. So the parcel owes a read map for
all 30 fauna figures, in the same commit, and the self-test's negative control has to move off
`fauna` onto a synthetic source rather than the repository's own state.

**Files:** `renderers/web/js/fauna.js` (new) · `renderers/web/index.html` · `renderers/web/js/main.js`
· `renderers/web/css/*` · `tools/publish.sh` · `tools/compile_scene.py` (the citation join only)
· `tools/measure_layer_reads.py` + its baseline · `tools/smoke_renderer.mjs`.

### K50 — ask every other layer the question that caught R-BUG5b · **DONE 2026-08-17 — both layers draw where they decided, and the instrument that caught R-BUG5b does not transfer whole**

**The answer is: nothing is mirrored.** 331 structures unioned out of 1,310 drawn instances,
**533,346 vertices read back** through the instance matrices the renderer hands the GPU, and
**19,372 road vertices** read back off the ribbon:

| layer | population read back | anchors outside their own drawn footprint | nearer to their MIRROR |
|---|---|---|---|
| `buildings.js` | 331 structures · 533,346 vertices | **0**, worst **0.00 m** | **0** |
| `streets.js` | 19,372 vertices · 3 meshes · 17 centrelines | **0** off every centreline, worst **0.00 m** | not a discriminator — see finding 2 |

Measured on the **published mirror** at 1280×800, against the DATA rather than against another
renderer number: a structure's `placement.local_e/local_n` in its sidecar and a street's
`path_local_enu_m`. The ground half was not redone — `smoke_renderer.mjs` already reads the drawn
surface back against `heightfield.bin` at every field sample and `tools/measure_terrain_horizontal.mjs`
holds its two horizontal axes — and `flora.js` was measured clean by R-BUG5b itself. **All four
layers named in this parcel are now answered.**

**Finding 1 — a per-INSTANCE box is not a building, and the first reading of this census said 279
of 1,310 bodies were misplaced.** A structure joins one batch per material it uses, so it holds
several instances and any one of them is walls, or roof, or trim. Judging a building by one of its
materials produced a **21 % false-positive rate** on a town that is entirely correct — worst
"stray" 24.45 m on `fort_dearborn_palisade`. `buildings.js` `instanceBounds()` warns about exactly
this in its own comment, for exactly the reason a size gate once passed a town of collapsed boxes:
*"a building is walls plus roof plus trim, and any one of those alone is not the building."*
**A new gate on this layer that does not union per structure id is measuring a material.**

**Finding 2 — the mirror test does not discriminate on a street grid, and R-BUG5b's instrument
therefore does not transfer.** Asking whether a drawn road vertex is nearer to a street at its
mirrored northing answered *yes* for **3,975 of 19,372** vertices on a build where every single
vertex is inside its own track. Two causes, both structural: reflect a point across an east-west
line in a **grid** town and it lands on another east-west street; and a vertex at the EDGE of its
own track scores worse than a mirror landing mid-track, by construction. So the streets gate is the
**half-width test alone** — which a mirrored ribbon cannot pass, because a reflected road runs
where no centreline is recorded — and the mirror figure is printed as a diagnostic that gates
nothing. What transferred from R-BUG5b was the QUESTION, not the instrument.

**Finding 3 — the gate was proved RED before it was believed.** `--refute` injects R-BUG5b's exact
fault into the live scene (the sign of each instance matrix's z translation; the sign of every
drawn road vertex's z) and re-runs the same census:

| | clean | fault injected |
|---|---|---|
| buildings outside their footprint | 0 of 331 | **329 of 331**, worst **1,238.89 m** |
| buildings nearer their mirror | 0 | **324** |
| road vertices off every centreline | 0 of 19,372 | **15,397**, worst 222.30 m, **5,010** off the grid altogether |

The two buildings that survive the mirror are the two standing on the datum's own east-west line,
which is arithmetic rather than a hole. This is R-A1's finding taken seriously one parcel on: *an
assertion that can only ever see one value is not an assertion*, and a placement gate that has only
run on a correct build has demonstrated nothing.

**What it unblocks, named as the visible-progress rule requires: `K30(c)`** — the queue's #1 SEEN
pick, *"29 buildings on eight streets are drawn standing in the roadway… redraw the bodies onto the
correct side of their own frontage."* K30(c) changes where 331 bodies are drawn relative to their
records, and until today **no gate in this project read the buildings layer's geometry back at
all**. The census is its acceptance instrument and its before-picture: worst anchor-outside-footprint
**0.00 m**, worst anchor-to-nearest-corner **47.11 m**.

**Files:** `tools/drawn_placement_census.mjs` (new — the census, shared) ·
`tools/measure_drawn_placement.mjs` (new — the instrument, ~1 min at one viewport) ·
`tools/smoke_renderer.mjs` (two gates, both viewports). The census lives in ONE module that both
import, because R-BUG5's own box records `measure_far_timber.py` and the browser disagreeing until
they were made to agree sample for sample.

R-BUG5b was invisible to three gates because all three asked where a layer DECIDED to put something
and none read back where it was DRAWN. Four layers decide in ENU and draw in three's world space:
`flora.js` (measured clean — `_m.setPosition(e, y, -n2)`), `streets.js`, `buildings.js` and
`ground.js`. The method is committed and cheap: transform each layer's drawn vertices to ENU with
`worldToEnu`'s own convention and compare them against the layer's own record of where it meant to
put them. **UNSEEN if it finds nothing and SEEN the moment it does**, which is the honest way to
scope it; it qualifies under the visible-progress rule's third exemption either way, as a gate on
nothing less than trust in every other placement gate in the renderer.

### R-BUG5 — trees stand in the river · **DONE 2026-08-16 · a real second fault, not the owner's picture**

**The owner's two populations are ONE cause, and neither of them is a planted stem.** The report was
a screenshot from 31 ft up, bearing 044°, north-east across the main stem: a straight LINE of woody
plants running out across the channel, and scattered ones over the open water beside it. The line is
`FAR_TIMBER.main_stem_belt_east`, a three-point polyline in `renderers/web/js/trees.js`, and the
scatter is the horizon solver's own gap modulation breaking the rest of the same run into separate
crowns.

**Measured, from the reported viewpoint with the far bank loaded, and the population is reported so
the denominator is visible** — the trap this box warned about is real and the probe below does not
fall into it:

| population | counted | over water |
|---|---|---|
| planted woody stations (`noteStation`) | **391** | **0** |
| flora instances, every set in the group | **1,024** | **0** |
| far-timber polyline samples at 2 m | **6,527 in-box of 6,664** | **47** |

Counted in the browser, on the published mirror, from the reported viewpoint. The two woody gates
were telling the truth about the 391 and the 1,024; the 47 is a population neither of them has a
reader for. **The Python census and the browser census agree sample for sample and to the
millimetre on every body** — which is the R-BUG3c-class assumption (the mask in `data/` and the mask
the page loads being the same mask) asserted rather than assumed, for the first time on this
layer.

**So nothing the two existing gates measure was ever wrong.** They were measuring the wrong
population. `"woody vegetation never occupies the river mask"` walks
`trees.group.userData.stations`, which `noteStation()` writes inside the near-field planter's 632 m
square; `"emergent flora stays within eight metres of a riverbank"` walks the flora instance
matrices, a lattice re-centred on the camera. `FAR_TIMBER` is neither: five bodies of timber the
sources put beyond the modelled town, authored as polylines and drawn as a horizon silhouette. **No
gate in this project had ever asked those polylines where they stand.** Fifth time a green gate and
the owner's screen have disagreed, and the fifth time the gate was pointed at something other than
what ships.

**The census, `tools/measure_far_timber.py`, RED on the build in the screenshot:**

| body | samples | over water | wet run | worst depth |
|---|---|---|---|---|
| `main_stem_belt_east` | 39 | **39** | **73.4 m of 73.4 m** | **3.347 m** |
| `north_branch_belt` | 2,513 | 8 | 16.0 m of 5,016.1 m | 1.380 m |
| `south_branch_belt` | 2,308 | 0 | — | — |
| `north_division_timber` | 459 | 0 | — | — |
| `south_branch_grove` | 1,345 | 0 | — | — |

`main_stem_belt_east` runs (326, 46) → (396, 68). The committed `south_water` centreline is at
n ≈ +7 across that reach and `north_water` at n ≈ +66, so **a belt whose own note says it follows
South Water Street was authored between the two banks.** It is not a survey error at the margin: it
is on the far side of the river from the street it is named after, along its whole length.

**Three of the four candidates this box listed are REFUTED, and the fourth is not what happened.**
The row emitter does consult the mask — `communityAt()` refuses `terrain.isWater` outright and the
planting loop tests the exact stem point before the ecology. The space is right: everything on that
path is ENU throughout. The mask and the drawn water do not disagree here. And nothing streams past
a placement gate. **The bug was in a population nobody had listed as a suspect**, which is the
finding worth keeping: the candidate list was written from the near-field planter, because that is
where a search for "what plants things" leads, and the thing that drew these trees does not plant
anything at all.

**The fix, and it is an invariant rather than a coordinate.** `solveHorizon()` now asks
`terrain.isWater(pe, pn)` at every emitted sample and skips it. The near-field planter has refused
that mask since it was written; a stand drawn at four hundred metres makes the same claim about the
same water. It is sampled at the EMITTED point, not at the body's vertices, because a belt can cross
a channel between two dry ends — which is exactly what the North Branch belt does. Outside the
modelled heightfield the mask returns its fallback and answers "dry", and that is the honest answer:
this project has no survey of that ground and a clip that claimed one would be inventing it.

**What is NOT fixed, deliberately: `main_stem_belt_east` now draws NOTHING, because none of it was
on land.** Repairing it means choosing where the belt's near edge actually ran, and no source here
settles that — the note that produced the fault is itself this project's best current reading of
Andreas ("the South Side timber extend[ed] east as far as Wells Street"). Picking a new line to make
the census green would be inventing the very thing the measurement just showed nobody knows. So the
two offenders are **banked by name in `tools/far_timber_baseline.json`**: the fault may shrink and
may not grow, a new offender fails, and a repair that forgets to re-bank fails too. **The renderer
half is absolute and needs no baseline.**

**R-BUG5(b) — where the South Water Street belt stood · NOT A PICK WITHOUT THE OWNER.** Three routes,
and they are different claims about the town rather than different code:
1. **Re-derive it from the committed `south_water` centreline**, south of the corridor. Mechanical,
   and the same move `south_branch_belt` already makes off the river's modern course — but it
   asserts which side of the street the timber stood on, which Andreas does not say.
2. **Leave it drawing nothing** and record the body as researched-but-unplaceable. Honest, and it
   loses a documented body of timber from the skyline.
3. **Withdraw the record** the way T-A16 withdrew the public square, on the grounds that a belt
   whose position cannot be derived is not a body this scene can carry.

**Files:** `renderers/web/js/trees.js` · `tools/measure_far_timber.py` ·
`tools/far_timber_baseline.json` · `tools/smoke_renderer.mjs` · `tools/check.sh`

**Gates:** `tools/check.sh` runs the census and its self-test (five broken-assertion cases plus the
three ratchet directions). `smoke_renderer.mjs` asserts the browser's own census matches the banked
numbers AND that `horizonWetSkipped > 0` from a stand where the belt clears `MIN_FAR_M` — from the
spawn point it is **329.2 m** away against a 330 m cut-off — 0.8 m inside it — so a gate that solved
only at spawn would have exercised nothing. Measured on the shipped build from that stand:
**7 samples clipped**.


### R-G0 — the critic harness · **DONE 2026-08-14 (G0.1 + the numeric half of G0.2)**

**Phase:** RENDERING §4 G0 · **Runner:** improve-runner (no Blender) · **Effort:** S

Everything later measures through this, which is why it was first. One reproducible loop so a
phase proves its delta in numbers rather than adjectives.

**Shipped:** `tools/critic_shots.mjs` — eleven stations (the eight scene anchors, driven by
`goTo` so they cannot drift from what a visitor is offered, plus three re-established
prairie-sweep stands), both release viewports at device scale 1, the clock held from before
the render loop's second tick, the DOM chrome hidden, pitch printed and asserted per station.
`tools/critic_metrics.mjs` — a dependency-free PNG reader and the six Appendix B recipes, so
the SAME code can measure a reference photograph and one of our frames, which has never been
true here before. Baseline for both viewports in `docs/STATUS.md` § "The critic baseline".

**Two things came out of it that are not the harness**, both recorded rather than fixed:

- **Draw calls exceed the ≤ 80 budget at four of the eleven stations** — `prairie_west` 97
  desktop / 94 mobile, `green_tree` 91/88, `forks` 87/82, `south_water` 85/83. The budget was
  only ever measured at the spawn station, where it passes at 65/62. Not a regression; a
  measurement nobody had taken. R-W5 owns the draw-call work and should take it.
- **Captures are byte-identical within a browser process and near-identical across
  processes.** Both baseline runs came out 11/11 byte-identical at both viewports, but an
  earlier pair of rounds had four desktop stations alternating between two variants differing
  in 1, 2, 11 and 43 pixels of 1,024,000 — on the horizon row and on alpha-blended surfaces.
  So the acceptance line "byte-stable" is now a stated stability CONTRACT in the harness
  (≤ 0.05 % of pixels may differ AND every reported metric must repeat within 1 %), it is
  checked by `--stability`, and the byte-identical count is reported alongside it. See
  RENDERING §4 G0 for the amendment.

**Still open from G0.2:** the baseline **8-axis rubric score**. The protocol requires a critic
that did not write the code under review, and the same run cannot both build the harness and
be that critic. It is a parcel of its own — **R-G1** below.

**Trap (kept for the record):** the harness must use the existing `window.__chicago4d` API
(`goTo`, `setAnimationHold(true)`, `capture`) and must not add a second way to drive the
scene. It does not: non-anchor stands use the same `walker.teleport` `tools/shoot.mjs`
already uses, and nothing in `renderers/` changed.

### R-G1 — the baseline scored pass · **DONE 2026-08-14 · mean 4.18 of 10**

**Phase:** RENDERING §4 G0.2 · **Runner:** improve-runner · **Effort:** S · **After:** R-G0

Scored at five named stations — `sauganash`, `first_post_office`, `south_water`, `prairie_west`,
`river_bank` — desktop 1280×800, against the §0 reference set and never against a commercial
game frame. **Mean 4.18; no axis reaches 7**, against a pass bar of mean ≥ 8.0 with no axis
below 7. Axis means: texture **1.4**, lighting **3.2**, material **3.6**, post **3.8**,
atmosphere **4.2**, geometry **4.6**, composition **5.8**, historical accuracy **6.8**.

**The independence condition held**: this parcel changed no code — three documents and a
changelog entry — and the run that wrote the harness was a different one. The mobile set was
captured and measured in the same run and deliberately **not** scored; six of the eleven
stations were read for context and not scored. Both facts are on the record in STATUS rather
than left to be inferred.

**Where the fixes went** — R-W1 (lighting, and the corrected mechanism for §1 item 7), R-W2
(material and texture, both halves), R-W3 (openings and the AO cage that has to carry form the
sun angle does not), R-W4 (atmosphere, the flower load, and a horizon-timber metric that cannot
tell a gable from an oak), R-W5 (post-processing and the draw-call growth), and two new lane-2
parcels, **T-V1** and **T-V2**, for the two failures that are data rather than rendering.

**Files:** `docs/STATUS.md` · `docs/ROADMAP.md` · `renderers/web/js/changelog.js` (no code)

**What it did not do:** re-anchor the §5 targets by measuring a reference plate through
`tools/critic_metrics.mjs`. That is still a one-line job and still not done.

### R-W1 — calibrated light and environment · **SHIPPED TO PRODUCTION 2026-08-17 ON THE OWNER'S RULING**

> ## ✅ RELEASE CONDITION — DISCHARGED BY THE OWNER, 2026-08-17
>
> **The condition below was put to Kevin before the promotion that carried this parcel, with the
> cost stated and three options offered — ship it, re-measure first, or promote without it. He
> chose to ship it.** The parcel went to production in the same promotion as K24's brightness
> slider, which is the accommodation he asked for on 2026-08-14 when he was first told this scene
> would be ~16 % dimmer.
>
> **The cost is real and is not retracted.** `south_water` 250–600 m fell from **71 % of probes
> perceptible to 16 %** when this landed on `dev`, and the far road down a street is a complaint
> he has raised twice. **R-W2**'s textured coverage is still the parcel that buys it back, and it
> stays #1 on the rendering lane for that reason. If a later run finds that band still dead, the
> answer is R-W2 — not a smaller bar, and not a revert of the light.
>
> **The figure is also older than the build it shipped in.** It was taken on `dev` at 836fa84;
> K24, the doubled shadow reach (R-W3b/R-W5a2) and R-BUG6(a)/(b) all landed after it and none was
> re-measured against this band. **Do not quote 16 % as this build's number** — it is the number
> this parcel cost on the day it landed. Re-read it before using it to argue anything.
>
> *Original condition, kept because the reasoning is the record:* R-W1 was not to be promoted
> until the owner had walked the `/dev/` preview and approved the look, or R-W2 had bought the
> contrast back. It was held on `dev` for exactly that purpose, and released by the first route.

**The light was wrong and this parcel is right about it.** Measured on an upward-facing white
Lambertian card, sun excluded, on the rebased branch: the old `HemisphereLight` rig put out
**1.9× the luminance and ~2.9× the red of the sky it was standing under**. Every calibration this
project has made — the sward's density, the wall colours, the crown contrast — was taken under a
fill that contradicted its own backdrop.

**And it is expensive, in the place that is already sore.** The scene is ~16 % dimmer, so road
contrast falls almost everywhere. Mobile, published mirror, honest denominator (R-M1c), against
`dev` at 836fa84:

| station · band | `dev` | R-W1 | |
|---|---|---|---|
| `south_water` 2–40 m | 90 % | 90 % | — |
| `south_water` 40–100 m | 87 % | 80 % | −7 |
| `south_water` 100–250 m | 52 % ✗ | 33 % ✗ | −19 |
| **`south_water` 250–600 m** | **71 % ✓** | **16 % ✗** | **−55** |
| `from_above` 100–250 m | 85 % | 78 % | −7 |
| `from_above` 250–600 m | 53 % ✗ | 50 % ✗ | −3 |
| `lake_market` 40–100 m | 100 % | 93 % | −7 |
| `lake_market` 250–600 m | 98 % | 100 % | +2 |

**THE SUITE REPORTS 229 / 2 BEFORE AND 229 / 2 AFTER, AND THAT IS A THIRD INSTRUMENT FINDING.**
The count is identical because `south_water` was *already* red on its 100–250 m band, so a band
collapsing from 71 % to 16 % **changed no verdict and appears nowhere in the summary**. A
station-level check hides a band-level regression, and a reader comparing tallies would conclude
this parcel cost nothing. Opened as **R-M1d**: the suite should report a band that moves against
its own last figure, not only a station that crosses a bar.

**What it buys, and this is real too.** Literal black pixels go to zero at all three metric
stations — `river_bank` **12,063 → 0**, `first_post_office` **11,015 → 0**, `prairie_south`
**2,315 → 0** — and the decile L\* rises everywhere, nearly doubling at `river_bank` (0.93 → 1.78).
§1 item 11 is retired and item 7's "no literal (0,0,0)" half with it.

**The sequencing conclusion, stated because it is the actual answer:** R-W1 is **correct and
premature**. It belongs *with or after* **R-W2**'s textured coverage, which is the parcel that buys
the contrast back. Landing it before R-W2 trades a documented, owner-reported defect for a
less-visible correctness win. It is on `dev` and not in production precisely so that trade is
visible to the person entitled to make it.

Everything below is the parcel as written on 2026-08-14, kept because it records the reasoning;
the branch has been rebased onto `dev` and its figures re-measured above.

**What shipped on the branch.** `scene.environment` is a PMREM of the calibrated sky **with
a ground half in it**, and the ground half is the finding: an analytic sky model is defined
over the whole sphere, so a sky-only environment paints the ground blue and lights every
downward-facing surface in the town with sky from below. That is what "swamped albedo" in
the 2026-08 attempt this file records. The ground half's radiance is DERIVED —
`reflectance x E_horizontal / PI`, with the reflectance the dun the hemisphere light already
carried as its ground colour, read as what its numbers already are (a 15 % reflector). No
new constant, and the bounce is finally tied to how much light is falling on the ground it
is bouncing off. The hemisphere lights are gone.

**THE FINDING, and it outlives the parcel: the old fill was not the sky.** Measured with the
new instrument, the `HemisphereLight(0xa8c4e0, 0x7a6b4e, 2.4)` rig delivered **1.86x the
luminance and 2.85x the red** of the very sky this project calibrated against a verified
photograph. The town was lit by a sky that does not exist, at an exposure set for one that
does, and every calibration since — the sward's density, the wall colours, the crown
contrast — was measured under it.

**Measured, desktop, at the three worst stations** (`node tools/critic_shots.mjs --metrics
--stations river_bank,first_post_office,prairie_south`):

| station | literal black px | decile L\* | crown G−B |
|---|---|---|---|
| `river_bank` | 12,063 → **0** | 0.93 → 1.78 | 47.8 → 33.7 |
| `first_post_office` | 11,015 → **0** | 5.35 → 6.20 | 12.2 → 15.7 |
| `prairie_south` | 2,315 → **0** | 7.09 → 7.97 | 19.9 → 10.7 |

So **§1 item 11 is retired** (an environment is installed and it does not override albedo),
**item 7's "no literal (0,0,0)" half is retired**, and **item 8 holds** — every station stays
over the ≥ +10 crown target. Fill on downward-facing surfaces is up 30 %.

**What did NOT clear, with the arithmetic rather than an excuse.** The decile target of
L\* ≥ 14 is not reachable by lighting and the numbers say why. An interior crown vertex
carries `CROWN_SHADE_FLOOR = 0.060` folded into its own vertex colour, so its albedo is the
record's foliage green times 0.06 — **0.24 % reflectance, darker than charcoal**. Even at a
floor of 1.0, i.e. no self-shadowing at all, that surface reaches only L\* ≈ 12 under this
rig. R-G1 was right that the metric reads canopy rather than shadow; what this parcel adds is
that the canopy is dark in the ALBEDO, where no environment can reach it. **The next lever is
`CROWN_SHADE_FLOOR` in `trees.js`, and it is a separate calibration** — the constant's own
committed check is the Weber contrast the reference photograph's tree mass holds (0.625,
against 0.655 here), so raising it has to be paid for there and not smuggled through a
lighting parcel.

**WHY IT IS PARKED — one real regression, named.** `tools/smoke_renderer.mjs` reports **403
passed, 4 failed**; three were an unstamped changelog and are fixed. The fourth is
**`the roads reach the screen from the air, at the aerial anchor`** — R-BUG2's own gate,
added yesterday, which requires ΔL\* ≥ 1.8 and ≥ 55 % of probes perceptible. `south_water`
still passes; only the aerial band fails. **Do not weaken it.** Two candidates worth
separating before touching anything: the scene is 16 % dimmer overall, and the environment
adds an indirect specular term to the terrain that is near-uniform across road and grass and
therefore compresses their ratio. The second would be the more interesting fault and is
testable on its own — the roads were tuned yesterday under the brighter rig, so a re-tune may
be owed, but it belongs to whichever parcel proves which cause it is.

**A note on the plan this deviates from.** RENDERING §4 W1 asks for `tools/gen_sky_env.py`
and a committed `.hdr` loaded through a vendored `RGBELoader`. That was not built, on purpose:
the sky in this renderer is already fitted to a verified photograph inside its own shader
(SKY_EXPOSURE, HORIZON_RESTORE), so a Python re-implementation would be a SECOND sky that must
be kept in step with the first, and RENDERING's own acceptance asks the environment and the
backdrop to agree in hue at the horizon. A PMREM of the shader agrees by construction. No
binary asset, no vendor change, no licence entry. **This is a proposal, not a settled
amendment** — RENDERING §4 W1 still reads as written and the owner may prefer the .hdr.

**Files on the branch:** `renderers/web/js/world.js` · `renderers/web/js/flora.js` (reads the
fill from `scene.userData.chiSkyFill`, because a Lambert material cannot see
`scene.environment` and the sward would otherwise have kept a fill the town no longer has) ·
`tools/light_probe.mjs` (new) · `tools/critic_shots.mjs` (`--stations`) ·
`renderers/web/js/changelog.js` · `site/chicago/4d/` · `docs/`

**Phase:** RENDERING §4 W1 · **Runner:** improve-runner · **Effort:** M · **After:** R-G0

Retires RENDERING §1 items 7, 8 and 11.

**Files:** `tools/gen_sky_env.py` (new) · `assets/env/` (new, with `assets/LICENSES.md`) ·
`renderers/web/js/world.js` · `renderers/web/vendor/MANIFEST` (+ `RGBELoader`) ·
`tools/smoke_renderer.mjs`

**Acceptance (RENDERING §5):** shadowed darkest decile **L ≥ 14**, no literal `(0,0,0)`;
sunlit crown **G−B ≥ +10**; a documented white wall reads white and a brown log wall keeps
**R/B ≈ 1.75** (measured 1.08 at the failure). Sun disc EXCLUDED from the HDRI — the direct
sun stays on the directional light; `world.js` documents why a five-figure-radiance disc
destroys the PMREM.

**Trap:** this is the change that failed before. Tune environment intensity until materials
keep their hue, THEN rebalance the hemisphere fill and ground bounce DOWN — otherwise total
illuminance doubles instead of being redistributed.

**From R-G1 (scored 3.2, the second-worst axis) — the acceptance number needs re-reading before
you start.** "No literal `(0,0,0)`" and "darkest decile L ≥ 14" were both written believing they
measured shadow. They do not, at any station measured: 94–100 % of the literal-black pixels lie
in connected components entirely above the median land/sky row, on the shaded side of the near
canopy, and the darkest-decile metric reaches the same pixels because its per-column "ground"
begins at the top of a crown. **Raising a shadow floor moves neither number.** What lights a leaf
facing away from the sun is the environment term this parcel installs — so the two numbers are
still W1's to earn, by the IBL rather than by the shadow path, plus a floor on the crown's
darkest albedo if the IBL alone does not clear it. Verify by locating the dark pixels — connected
components and their bounding boxes against the land/sky row — and not by the aggregate alone: an
aggregate that moves for the wrong reason is how this got mis-stated once already. Second, the
sun stands **70.5°** up at the scene's 12:30 and a
shadow is 0.354 × the height of what casts it, so the frame carries almost no shadow information
and form must come from the IBL and from W3's AO — the hour is a recorded, reasoned choice and
this is not an argument to move it, but W1 should not expect the shadow map to help it.

### R-W4 — atmosphere and the mid-field · **SPLIT FOUR WAYS — claim ONE**

> **R-W4a is DONE 2026-08-15** — the metric counted the town's roofs as timber, the
> discriminator this entry named was measured and REFUTED, and the figure it was replaced with
> cannot move when a block lands. Findings and the corrected table under R-W4a below.
> R-W4b/c/d are free and now have a number they can trust.

**Phase:** RENDERING §4 W4 · **Runner:** improve-runner · **After:** R-G0

The largest single visual gap: RENDERING §1 items 1–6. **It was tagged L and that is why it is
split** — the run budget is 150 minutes and one smoke pass is 26 of them (see the budget section
at the top). Each half below is one coherent change with one smoke.

| | parcel | why it stands alone |
|---|---|---|
| ~~**R-W4a**~~ | ~~fix the horizon-timber metric~~ · **DONE 2026-08-15** | The headline figure counted gable ends as trees and the acceptance number was unmeasurable. It is measurable now, and it is much worse than it read. Findings below. |
| ~~**R-W4b**~~ | ~~the ring seam~~ · **ALREADY SHIPPED 2026-08-13 (PR #95) — NOT A PICK.** Noticed 2026-08-17 by R-BUG6(a) while choosing a parcel: every lattice slot has carried its own outer radius since that commit (`fringeOf`, `LOBE_M`, `TUNE.mid.fringe = 3.0`), the spread went **1.4 px → 5.9 px** at 1280×800 and 17.4 px at 390×780, and a gate holds it. **This row stayed pickable for four days and cost this run part of its budget** — see `docs/STATUS.md` § *the sward ended on a straight line*. | 
| ~~**R-W4c**~~ | ~~flower load~~ · **(a) and (b1) DONE 2026-08-15, (b2) IS THE TUNING HALF** | `0.0012` was not a count of flowers: the recipe's hue cut at 50° runs through the middle of a July prairie's bloom and misses **94.5 %** of it. The render's true bloom at `prairie_west` is **2.19 %**, not 0.12 %. **And there is no 4–6 % target to tune to** — R-W4c(b1) found it unsourced on one half and unreproducible on the other. Findings under R-W4c(a) and R-W4c(b1) below — **read both before quoting any flower number, and before tuning anything**. |
| **R-W4d** | **the mid-field itself** | Vegetated pixels to the fog-90 % distance, crown fine-detail ≥ 0.6, depth-band high-pass RMS. The bulk, and the part that genuinely needs the others' numbers to be trustworthy first. |

**R-W4a is not bookkeeping.** A town parcel has already handed W4 a pass it did not earn, and
the same thing will happen again on every block that lands. Fixing the metric before chasing the
number is the difference between improving the scene and improving the score.

**Files:** `renderers/web/js/flora.js` · `renderers/web/js/trees.js` ·
`renderers/web/js/world.js` (horizon band) · `data/flora/` (tuning only) ·
`tools/smoke_renderer.mjs`

**Acceptance (RENDERING §5):** vegetated pixels present to the fog-90 % distance; horizon
timber column coverage **≥ 90 %** — quoted from `horizonTimber.timberOnly.coverageAll` and
never from `coverageAll`, which counts roofs (R-W4a); crown fine-detail ratio **≥ 0.6**; depth-band high-pass
RMS non-collapsing, far band **≥ 0.75×** reference; flower load **4–6 %** — quoted from
`flower.bloom` and never from `flower.load`, which counts a yellow coneflower as grass
(R-W4c(a)), and against a target R-W4c(b) must re-derive before it compares the two; the ring seam gone
(no constant screen row across all columns). Fog still total by 1500 m (**L17**), and
`HAZE_MAX = 0.82` on the horizon band is **L35** — a technique that changes what either
claims gets an appended **Revised** line in `docs/LIBERTIES.md` in the same PR.

**Trap:** the ring seam is a circle of constant radius drawn on flat ground, which is why it
lands on one screen row. Varying the radius per patch is the fix that worked for the sward;
the same shape of fix is wanted here, not a bigger radius.

**From R-G1 (scored 4.2) — the ≥ 90 % horizon-timber target does not currently measure timber.**
The recipe counts a column as timbered if any pixel in the band above the land/sky line falls
3 luma below, or 3 G−B above, the sky extrapolated from the 20 rows over it. A gable end breaking
the skyline satisfies that as surely as an oak, and it has already happened: with **no renderer
change** between two runs (`git diff --stat 282dd9a..HEAD -- renderers/` is `changelog.js` and
nothing else), `prairie_south` moved **0.364 → 0.436** all and **0.340 → 0.441** centre on the
strength of 19 new anonymous roofs, whose grey gable ends occupy the left third of that station's
skyline. **A town-completion parcel can therefore hand W4 a pass it did not earn.** Before the
acceptance number is quoted again, either the metric excludes columns carrying a structure
silhouette or a second figure reports timber-only coverage; the crown-hue channel the recipe
already computes (G−B) is the obvious discriminator, since a whitewashed gable is not green.
Two further reads from the scored pass: the sky is a single cloudless gradient at all five
stations, and the flower load at `prairie_west` is **0.0012** against the honest 4–6 % target —
the largest single accuracy deduction on the historical axis outside the town itself.

#### R-W4a — DONE 2026-08-15 · the horizon metric was scoring the town, and the discriminator this entry named does not work

**What it was.** `critic_metrics.mjs` counted a horizon column as timbered if anything broke the
skyline in the band above the land/sky line. A gable end does that as surely as an oak, so the
figure rose when the town grew — R-G1 measured `prairie_south` moving 0.364 → 0.436 on nineteen
new roofs with no renderer change — and 399 roofs were still to come.

**The named discriminator was refuted before anything was built.** This entry proposed the G−B
channel, "since a whitewashed gable is not green". Measured on the 2026-08-15 `dev` build,
desktop, at the first hit pixel of every broken column: the grey gables at `prairie_south` sit at
**ΔG−B +22.4** and hazed timber at `prairie_west` ranges **+0.1 to +17.5**. The populations
overlap completely, because the sky near the horizon is strongly blue-dominant and *every*
non-sky pixel clears a +3 G−B test by a wide margin — the channel is a not-sky detector, and
`coverageAll` was reading the same thing twice. **No colour test can work here in principle**:
L17 makes extinction total by 1500 m, so distant timber and a distant wall converge on the fog
colour. The atmosphere destroys the evidence the discriminator needs, correctly.

**What was done instead — subtraction, not a heuristic.** `critic_shots.mjs` photographs each
station twice from the identical pose: once as the visitor sees it, and once with the
`structures` group's `visible` flag down. `measure()` runs the same recipe on both. The second
frame's coverage is timber by construction — no threshold, no hue, nothing to tune — and it
**cannot move when a block lands**. The old number is kept, unchanged in value and computed
exactly as before, under a name that says what it counts (skyline breaks), so the 2026-08-14
baseline stays comparable.

**The corrected table — source tree, 2026-08-15 `dev`, both viewports, 11 stations.** `breaks` is
the old figure; `timber` is the honest one; `town` is the share of the old figure that was roofs.

| station | dsk breaks | dsk **timber** | dsk town | mob breaks | mob **timber** | mob town |
|---|---|---|---|---|---|---|
| `sauganash` | 0.638 | **0.477** | 29 % | 0.756 | **0.574** | 33 % |
| `sauganash_wing` | 0.518 | **0.492** | 20 % | 0.636 | **0.636** | 16 % |
| `lake_market` | 0.532 | **0.534** | 16 % | 0.697 | **0.597** | 24 % |
| `first_post_office` | 0.847 | **0.751** | 12 % | 0.919 | **0.698** | 24 % |
| `forks` | 0.738 | **0.651** | 25 % | 0.749 | **0.818** | 16 % |
| `green_tree` | 0.737 | **0.745** | 9 % | 0.762 | **0.797** | 3 % |
| `south_water` | 0.889 | **0.706** | 25 % | 0.836 | **0.362** | 58 % |
| `from_above` | 0.212 | **0.212** | 0 % | 0.156 | **0.156** | 0 % |
| `prairie_south` | 0.632 | **0.295** | **62 %** | 0.682 | **0.403** | 49 % |
| `prairie_west` | 0.830 | **0.894** | 5 % | 0.669 | **0.639** | 21 % |
| `river_bank` | 0.641 | **0.651** | 1 % | 0.713 | **0.713** | 0 % |

**Three things in that table are worth reading before quoting it:**

- **The worst overstatement is `prairie_south`, where 62 % of the "timber" was the town** — 409
  of 1053 measured columns broke the skyline on a roof and on nothing else. The station R-G1 used
  to demonstrate the fault is the station the fault was worst at, which is the fault being
  self-consistent rather than a coincidence.
- **The correction runs the OTHER way at six of the twenty-two station-viewports** (`green_tree`,
  `lake_market`, `prairie_west` desktop, `forks` mobile, `river_bank`), because a building can
  stand in front of timber and hide it. This is the figure answering "is the horizon timbered",
  not "can the visitor see timber past the town" — the right question for a target derived from
  photographs of a treeline, and it is stated here so nobody reads a rise as an improvement.
- **Nought of twenty-two station-viewports meet the ≥ 90 % target on the honest figure**, against
  one on the old one. Mean 0.582 against 0.672. **R-W4d inherits a bigger gap than it was
  promised**, and `from_above` (0.212 / 0.156, town share 0 %) is an aerial pose whose band is
  not a horizon at all — do not average it in without saying so.

**Cost, measured.** The full 11-station both-viewport `--metrics` run took **13 min 12 s** with
the second capture, against the ~12 min the budget section quotes without it; on a 3-station
desktop A/B it went 2 min 03 s → 2 min 58 s, most of the fixed cost being the page load the two
share. `--no-mask` opts out and says so in the header.

**Putting the town back leaves the frame alone, measured rather than assumed.** The visitor's
screenshot is taken BEFORE the toggle, so a station's own frame cannot be affected by it; the
question is whether the NEXT station's is. Same three stations before and after the change, in
separate browser processes: **5, 9 and 51 differing pixels of 1,024,000** (≤ 0.005 %), inside the
harness's own documented cross-process residual of 1–43 px and far under its 0.05 % ceiling. The
`--stability` contract passes with the second capture in it, byte-identical at both stations
tested, worst metric drift **0**.

**And a doc claim was found false while using it.** The budget section has told every run since
2026-08-14 to use `critic_shots.mjs --stations a,b,c` for a 3-minute run instead of 12. **That
flag did not exist**, so every run that followed the advice ran the full set. It exists now.

#### R-W4c(a) — DONE 2026-08-15 · the flower metric cannot see most of a flower, and the gap it reported is 18× too big

**What it was.** R-G1 measured a flower load of `0.0012` at `prairie_west` against a 4–6 %
target and this file called it "an under-representation of a July prairie by two orders of
magnitude". The recipe sorts every ground pixel into *plant* or *flower*, and it applies the
plant test first: `hue ∈ [50°, 180°)` with any chroma at all is plant. **No yellow-through-cyan
pixel can therefore ever be a flower, however brilliant it is** — and the headline colour of a
July prairie is the yellow composite.

**The cut runs through the bloom it is sorting, and this project's own records straddle it.**
Measured on the committed `data/flora/zones/` inflorescence colours:

| record | rgb | hue | counted as |
|---|---|---|---|
| `silphium_laciniatum` | 228, 200, 62 | **49.880** | flower |
| `ratibida_pinnata` | 232, 206, 72 | **50.250** | **the grass it is compared against** |
| `opuntia_humifusa` | 236, 208, 72 | 49.756 | flower |
| `nuphar_advena` | 230, 206, 80 | 50.400 | **plant** |

Two yellow composites 0.37° apart land on opposite sides, and nobody looking at the frame could
tell the pair apart. Of the **97** inflorescence colours in the zone records, **52 are called
plant, 26 are called neither** — dropped from *both* sides of the ratio, which is where the
saturated dark purples go (`liatris_pycnostachya`, `vernonia_fasciculata`, `dalea_purpurea`,
`pontederia_cordata`) — and only **19 are called flower**.

**So the harness was made to take the flowers away, the same subtraction R-W4a used for the
town.** `critic_shots.mjs` photographs each station a third time with the nine `flora-head-*`
instanced sets hidden; every ground pixel that moved is a pixel a flower head painted, by
construction — no hue, no colour threshold, nothing that moves when the palette is re-tuned.
The heads cast no shadow (`flora.js` sets `castShadow = false` on every set), so hiding them
cannot change a pixel they did not cover. Both frames are read over the **visitor frame's**
ground line, so a scape breaking the skyline cannot move the boundary and count its own removal.

**The measurement — source tree, 2026-08-15 `dev`, desktop, the three prairie stations.**

| station | recipe `load` | **true bloom** (of hued ground) | of ground | bloom px | recipe **recall** | recipe **precision** |
|---|---|---|---|---|---|---|
| `prairie_west` | 0.0012 | **0.0219** | 0.0202 | 10,843 | **0.055** | 0.998 |
| `prairie_south` | 0.0024 | **0.0187** | 0.0107 | 9,137 | **0.128** | 0.996 |
| `river_bank` | 0.0022 | **0.0076** | 0.0057 | 4,131 | **0.284** | 1.000 |

**Where the missing bloom goes, in-frame — this is the whole finding.** Of the 10,843 pixels a
flower actually painted at `prairie_west`: **5.5 % are called flower, 69.7 % are called PLANT,
24.9 % are called neither.** The recipe does not merely miss them — a bloom pixel called plant
is subtracted from the numerator **and added to the denominator**, so the ratio is pushed down
twice by the same pixel. Precision runs the other way and is near-perfect (0.998): almost
everything it *does* call a flower is one. It is not over-counting. It is blind.

**Three things follow, and two of them are corrections to this project's own claims.**

- **"Two orders of magnitude" is wrong and is corrected wherever it appears.** The render's
  bloom at `prairie_west` is **2.19 %**, not 0.12 %. Against a 4–6 % target that is a factor of
  about two to three — a real gap, worth R-W4c(b), and **eighteen times smaller than the one
  this file has been quoting**. A parcel sized against the old figure would have been sized
  against a measurement error.
- **NEITHER COMPARISON WITH THE 4–6 % TARGET IS SOUND YET, AND R-W4c(b) MUST NOT BE ACCEPTED ON
  ONE.** That target was derived by running *this same recipe* on the reference photographs
  (STATUS §00: planting 12.91 %, virgin remnant 1.79–5.54 %). So `0.0012` vs 4–6 % is
  recipe-against-recipe, which is at least consistent in method but reads a number that is
  94.5 % blind on our side and blind by an unmeasured amount on the photograph's; and 2.19 % vs
  4–6 % compares a true count against a blind one. A photograph has no second frame, so its
  bloom **cannot** be measured by subtraction. **Re-deriving the target with a method of known
  recall is R-W4c(b)'s first job, before it tunes anything** — otherwise the tuning half will
  chase a bar that was never on this scale.
- **What (a) does give (b) is an exact baseline.** Whatever `data/flora/` or `flora.js` is
  changed to, the bloom it paints is now countable to the pixel and the count cannot be gamed by
  a palette shift. That is the point of landing the measurement before the fix, and it is why
  the parcel was split.

**The one limit of the figure, checked rather than waved at.** It counts head pixels **over
ground only**, because that is `load`'s denominator. A head silhouetted against the sky is
therefore outside it. Measured whole-frame against ground-only: `prairie_west` 10,873 vs 10,843
(**30 px**, 0.3 %), `prairie_south` 9,137 vs 9,137 (**0**), `river_bank` 4,240 vs 4,131
(**109 px**). The restriction costs essentially nothing at these stations and the figure is a
floor, not an estimate.

**Cost, measured.** Three desktop stations with all three captures: **3 min 45 s**, against the
2 min 58 s R-W4a measured for the same three with two captures. The third capture is frames, not
a page load, and `--no-mask` still opts out of both.

**`flower.load` is unchanged in name and in value**, exactly as `coverageAll` was kept by R-W4a,
so the 2026-08-14 baseline and the photograph-derived target stay comparable to themselves. The
new reading is `flower.bloom`, and it is `null` for a reference photograph the same way
`timberOnly` is.

#### R-W4c(b1) — DONE 2026-08-15 · there is no 4–6 % target: half of it is unsourced, half does not reproduce, and the instrument cannot be repaired

**What it was.** R-W4c(a) ruled that the tuning half's *first* job is to re-derive the 4–6 %
flower-load target "with a method of known recall, before it tunes anything — otherwise the
tuning half will chase a bar that was never on this scale". That is a whole parcel, so it was
split off as (b1). **The answer is that the target cannot be re-derived from anything in this
repository, and the instrument that produced it cannot be fixed by the repair its own diagnosis
implies.** Every figure below comes out of `node tools/measure_bloom_target.mjs`, which is
committed; `--assert` holds the inputs to the numbers quoted here.

The target's stated derivation (STATUS §00, from the 2026-08-10 prairie sweep) has two clauses:
the recipe read **12.91 %** on a restoration planting and **1.79–5.54 %** on a never-plowed
remnant, so the honest bar for unmanaged 1835 prairie is 4–6 %. Both clauses were checked.

**1 · THE REMNANT HALF IS UNSOURCED.** There is **no never-plowed remnant photograph in this
repository and no source record describing one.** Three photographs are committed: the DuPage
restoration planting, a September 2017 Kansas trail, and the owner's sagebrush two-track. The
phrase "never-plowed remnant" occurs exactly **once** in `data/sources/` — inside the record of
the DuPage planting, the photograph that is *not* the remnant, and the same record that forbids
quoting that photograph for this number. It cites nothing. So the entire lower reference of the
target, and therefore the "4–6 %" that was set below the planting's reading on the strength of
it, rests on a measurement no reader can check. **That is precisely the failure `AGENTS.md` rule
1 exists to prevent**, reached not by inventing a citation but by carrying a number forward until
its source was forgotten.

**2 · THE PLANTING HALF DOES NOT REPRODUCE.** The committed recipe on the committed photograph:

| what was measured | flower load |
|---|---|
| the full frame, 4032×3024 | **5.54 %** |
| the nearest quarter | 7.02 % |
| the nearer half | 6.69 % |
| the full frame, flower test first (the §3 repair) | 25.82 % |

**12.91 % is not there** — not on the full frame, not on a nearer crop, and not under either
ordering of the recipe's two tests. The one candidate cause with a motive was tested and
**refuted**: the render reads 12.93 % under the reversed ordering, a hair from the missing
12.91 %, so the obvious explanation is that the sweep's uncommitted harness ordered its tests the
other way — but that ordering reads 25.82 % on the photograph, not 12.91 %. The near-match at
12.9 % is between two different images and means nothing.

**And 5.54 % is, to the digit, the figure this project attributes to the never-plowed remnant it
has no photograph of.** That coincidence is recorded and not explained. It is not built on
anywhere below.

**3 · THE INSTRUMENT CANNOT BE REPAIRED BY THE OBVIOUS FIX, and R-W4c(a)'s precision finding
needs a correction.** R-W4c(a) diagnosed the bug exactly — the plant test runs first and swallows
every yellow-through-cyan pixel — and the repair that diagnosis implies is to run the flower test
first. Scored against the same subtraction ground truth, on the same frames:

| station | instrument | load | recall | precision | bloom / ground |
|---|---|---|---|---|---|
| `prairie_west` | committed | 0.12 % | 0.055 | **0.998** | 2.02 % |
| `prairie_west` | flower test first | 12.93 % | 0.367 | **0.062** | |
| `prairie_south` | committed | 0.30 % | 0.128 | 0.801 | 1.07 % |
| `prairie_south` | flower test first | 3.60 % | 0.305 | 0.159 | |
| `river_bank` | committed | 0.22 % | 0.284 | 1.000 | 0.57 % |
| `river_bank` | flower test first | 27.65 % | 0.525 | 0.014 | |

Recall roughly sextuples and **precision collapses by sixteen times**. Reordered, the recipe calls
**12.93 %** of `prairie_west`'s ground a flower where a flower painted **2.02 %** of it.

So R-W4c(a)'s reading of the precision figure — *"almost everything it does call a flower is one.
It is not over-counting. It is blind"* — was true of the recipe as a whole and **wrong about
which half of it was working**. The near-perfect 0.998 was the plant test's pre-filter, not the
flower test's discrimination: the flower test is "saturated and light, or white and light", which
in a July prairie is *sunlit grass*. It cannot see a flower either. Ordering is not the whole bug,
and there is no repair here that a re-read of the photograph could be trusted to.

(The last column is `bloom.shareOfGround`. R-W4c(a)'s headline **2.19 %** is `shareOfHued`, over
the smaller denominator `load` uses. Both are in the metrics and they are not the same number —
quote which one you mean.)

**4 · THE BAR THAT DOES EXIST, and it needs neither a classifier nor a photograph.** Every
flowering forb in `data/flora/zones/` carries a sourced `density_per_ha` and a sourced
inflorescence `size_m`. Heads as discs of diameter `size_m`, that is a bloom fraction **in plan**,
by arithmetic, from committed records:

| zone | bloom in plan | species with a density / stated by cover instead |
|---|---|---|
| `z01_wet_prairie` | **0.097 – 1.064 %** | 9 / 2 |
| `z02_mesic_prairie` | **0.027 – 0.219 %** | 11 / 0 |
| `z09_sand_prairie` | 0.004 – 0.044 % | 5 / 0 |
| `z03_sedge_meadow` | 0.016 – 0.140 % | 2 / 6 |

**This is not a target and must not be quoted as one.** It is a *plan* fraction and `load`,
`bloom` and the photograph are all *screen-space* readings at an oblique pose — a head is seen
frontally from an eye at 1.6 m while the ground it stands on is foreshortened to nothing, so the
screen figure is expected to be much the larger. The conversion is not attempted here.

What it does settle is **where a bloom change lives**. `flora.js` plants the forb layer at "the
zone's OWN summed `density_per_ha`" (`flora.js:644`, weight at `:1089`), subject to a lattice cap.
So the bloom a visitor sees is generated from sourced record fields, and **raising it is a DATA
change requiring source support — not a renderer knob and not a palette tune.** Whether the
realised density matches the specified one is *not* measured here and is named as open work below.

**WHAT R-W4c(b2) MUST NOT DO.** It must not tune against 4–6 % (unsourced and unreproducible), it
must not tune against `flower.load` (recall 0.055), and it must not "fix" the recipe by reordering
it (precision 0.062). The honest reading is `bloom.shareOfHued` / `bloom.shareOfGround`, which has
no classifier on either side — and **it has no target**. Three routes out, for the owner to choose
between rather than an agent to pick:

- **commit a never-plowed July remnant photograph** with rights cleared the way
  `saari_2018_dupage_tallgrass` and `samstone_2017_tallgrass_trail` were on 2026-08-15 (Commons
  API, SHA-1 checked against the file page), and derive a bar from it by a *stated* method. Note
  that a photograph has no second frame, so its bloom cannot be measured by subtraction and any
  method used on it will have unmeasured recall — this route buys a source, not an instrument.
- **derive the bar from the flora records** by building the plan→screen conversion the table
  above deliberately skips. This is the only route that ends in a number the project can
  re-derive by command, and it is a real parcel, not a line of arithmetic.
- **decide the bloom is not gated on a number at all** and retire the 4–6 % figure from STATUS,
  RENDERING §4 and this file rather than leaving it to be quoted again. It has been quoted five
  times in three documents while resting on the two clauses above.

**Cost, measured.** The whole parcel: one 3-station desktop capture at **4 min 02 s**, and 19 s
for `measure_bloom_target.mjs` (of which §2 is 4032×3024 pixels twice). No renderer file changed,
so no bake and no new geometry.

### R-W5 — water, post-lite, dynamic resolution · **SPLIT TWO WAYS — claim ONE**

> **R-W5a is DONE 2026-08-15** (PR on `steward/r-w5a-batch-albedo`). **R-W5b is free**, and so is
> its successor **R-W5a2** below. Read the R-W5a findings before touching `buildings.js`.

**Phase:** RENDERING §4 W5 · **Runner:** improve-runner · **After:** R-W5a nothing; R-W5b after R-W1

| | parcel | why it stands alone |
|---|---|---|
| **R-W5a** | **the draw-call budget and batching** | **The more urgent half, and it is not really about water at all.** R-G1 measured lane 2 adding **exactly +11 draw calls per 19 structure records**; the straight-line over the 414 roofs still to come is **+240 against a budget of 80**. This is being spent right now, every time a block lands. Independent of the water surface. |
| **R-W5b** | **the water surface, post-lite, dynamic resolution** | RENDERING §1 item 13, EffectComposer/SMAA. It no longer carries **R-BUG1** — the flickering river edge was closed on its own 2026-08-16, and it was the camera's near plane rather than the water material. Still owns `terrain.js`'s water material. |

**R-W5a is the whole queue's first parcel as of 2026-08-15, and it has NO dependency on R-W1.**
The `After: R-W1` this section carried was inherited from the unsplit parcel and is true only of
**R-W5b**, which shares tonemapping and exposure with W1's post chain. Batching touches neither.
Nothing is gained by holding it behind a parked PR, and the TOWN lane is the reason: **T-A8 and
every block after it is blocked on this budget**, and each block that lands while it is unmet
spends more of what is left. A budget met by tuning after 414 roofs have landed is a rewrite; met
now, it is a design choice. The two leads R-G1 left are in the finding below and neither has been
explained — start there rather than reaching for a batching library.

**Files:** `renderers/web/js/terrain.js` (water material) · `renderers/web/js/world.js` ·
`renderers/web/vendor/MANIFEST` (+ EffectComposer/SMAA) · `tools/smoke_renderer.mjs`

**Acceptance:** RENDERING §1 item 13 retired; draw calls still **≤ 80** in the main pass with
extra passes accounted separately; triangles within the per-tier ceilings; zero page errors
at both viewports. **R-BUG1 is DONE and was not this parcel's** — the flickering river edge was
the depth buffer's precision, closed 2026-08-16 with no change to the water material at all. Read
its box before reaching for a `polygonOffset` here.

**From R-G1 (scored 3.8) — the draw-call budget is moving away from you, and lane 2 is what
moves it.** Re-measured on the same renderer with 19 more structure records (242 → 261):
**exactly +11 draw calls at seven of eleven desktop stations, exactly 0 at the other four**,
triangles up by only 244–562, so this is per-object cost and not geometry. Stations over the
≤ 80 budget go **4 → 6** desktop and **4 → 5** mobile; the worst goes 97 → 108. Straight-line
over the 414 roofs still to come is roughly **+240 draw calls against a budget of 80**. That is
not an argument for slowing lane 2 — the roofs are the product — it means **batching is this
parcel's first question, not its last**, and that a budget met by tuning after the fact will not
stay met overnight. Two leads: `from_above`, which sees the whole town, gained **0**, so
something already drops these objects at distance; and the +11 is suspiciously uniform across
bearings 150° apart, which no one has explained.

#### R-W5a — DONE 2026-08-15 · the town was paying a draw call per colour of paint

**What it was.** `buildings.js` groups the town into one `BatchedMesh` per distinct material, and
the grouping key included the material's base colour. Every one of the 47 batches in the
2026-08-15 `dev` scene was the same `MeshStandardMaterial` — metalness 0, **no map of any kind**,
`DoubleSide`, opaque, `alphaTest` 0, smooth-shaded. The only fields that differed were `color`
(39 distinct values across 47 batches) and `roughness` (16 values). The town was spending 47 draw
calls to render two numbers.

**What was done.** Base colour moved OUT of the key and INTO the geometry, as a per-vertex `color`
attribute filled from `material.color`, with the shared batch material left white and
`vertexColors` on. This is not an approximation: `material.color` is already in the renderer's
linear working space, three's `<color_fragment>` multiplies `diffuseColor.rgb` by the attribute
with no colour-space conversion of its own, and the confidence view's tint was **already** applied
after `<color_fragment>` — so the shader does the identical product in a different order. A
documented white wall still renders at the value its record claims, to the bit. Roughness and
metalness are additionally compared at three decimals, which merged two more pairs: the bespoke
masters carry `0.8999999761581421` (a float32) and the generated infill writes `0.9`, and
comparing them exactly had split the 0.90 and 0.88 buckets for no reason a visitor could see.

**The result — `tools/critic_shots.mjs`, source tree, both viewports, before and after on the same
`dev` at 276 structure records:**

| draw calls | `sauganash` | `s'nash_wing` | `lake_market` | `f_post_office` | `forks` | `green_tree` | `south_water` | `from_above` | `prairie_south` | `prairie_west` | `river_bank` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| desktop before | 75 | 78 | 90 | 66 | 98 | 103 | 96 | 72 | 95 | **109** | 56 |
| desktop after | 56 | 58 | 60 | 57 | 68 | 70 | 66 | 59 | 62 | **75** | 52 |
| mobile before | 72 | 74 | 78 | 60 | 82 | 99 | 94 | 72 | 93 | **106** | 49 |
| mobile after | 54 | 55 | 58 | 51 | 64 | 68 | 64 | 59 | 61 | **73** | 47 |

**Batches 47 → 16. Station-viewports over the ≤ 80 budget: 11 of 22 → 0 of 22.** The worst station
falls 109 → 75 desktop and 106 → 73 mobile.

**The growth term is zero, and that is the point.** R-G1's "+11 draw calls per 19 roofs" was
**11 new material GROUPS** — new paints, not new objects — which is exactly why it was uniform at
bearings 150° apart: the cost counts paints in frame, not buildings. A new roof of any colour now
joins an existing batch, so **T-A8 and the 399 roofs behind it cost nothing in draw calls**, and
the ~+240 extrapolation is retired rather than deferred. The one residual growth path is a NEW
ROUGHNESS from a future bespoke bake, which adds one batch and is bounded by the material palette,
not by the roof count. (`from_above` gaining 0 in R-G1 is consistent with none of those 11 paints
having an instance in that frame; it is not worth chasing now that the term is zero.)

**Two acceptance facts, measured rather than asserted:**

- **Triangles are identical to the triangle at all 22 station-viewports.** Nothing was dropped,
  culled or simplified to buy the draw calls.
- **The frames are not byte-identical, and here is exactly how far apart they are.** 2 of 22 shots
  hash the same; the rest differ on **0.013 % of pixels** — 15 to 487 pixels per frame, in 7 to
  195 scattered components whose largest is 56 px, lying on building silhouettes. That is depth
  ties at coincident surfaces resolving the other way under a changed draw order. Worst single
  pixel 93/255; **whole-frame mean |Δ| 0.003–0.005 of one 8-bit count**. No surface is repainted.

### R-W5a2 + R-W3b(a2) — the last 16 batches → 1, and the reach it buys spent · **DONE 2026-08-17 — ±120 m became ±240 m at the same texel, and the batch merge is not the pixel-identical operation it was written up as**

**Phase:** RENDERING §4 W5 + §4 W3 · **Runner:** improve-runner · **Files:**
`renderers/web/js/buildings.js` (`roughnessAttribute`, `perVertexRoughness`, `materialKey`) ·
`renderers/web/js/world.js` (`SHADOW_REACH_M`, the shadow block) · `tools/smoke_renderer.mjs`
(four new assertions) · `docs/evidence/r-w5a2-{before,after}.png` · `site/chicago/4d/**`.

**It was taken as ONE parcel on purpose.** R-W5a2 alone is UNSEEN by its own row and the visible-
progress cap forbade a second invisible run in four (v161 is the one). But R-W3b(a), six hours
earlier, had measured the shadow reach as **draw-call-bound** and named this parcel as what unbinds
it — so the batch merge is the enabler and the reach is the payoff, and shipping the enabler alone
would have been an invisible run whose whole point was the visible one it declined to take.

**Finding 1 — the shadow pass is where the batch count was actually being spent.** R-W5a2's box
priced the merge at "about 15 draw calls at every station", which is the COLOUR pass alone. Every
batch that enters the sun's ortho box is a second call in the shadow pass, so the true saving grows
with the reach and the town's batch count was setting how far the sun could see. Measured on the
published mirror at 1280×800, at the eight scene anchors:

| anchor | dev, ±120 m, 16 batches | this, ±240 m, 1 batch |
|---|---|---|
| `green_tree` | **74** of 80 | **50** |
| `forks` | 73 | 47 |
| `south_water` | 69 | 41 |
| `from_above` | 69 | 44 |
| `lake_market` | 65 | 37 |
| `sauganash_wing` | 64 | 36 |
| `first_post_office` | 62 | 39 |
| `sauganash` | 61 | 34 |

**What the reach buys, counted off the DATA** the way R-W3b(a) counted it — each structure's
`placement.local_e/local_n`, each planted stem's own station, against the shadow camera's matrices:

| anchor | structures inside, ±120 m | at ±240 m | stems, ±120 m | at ±240 m |
|---|---|---|---|---|
| `green_tree` | 27 of 331 | **49** | 0 of 730 | **70** |
| `south_water` | 26 | **91** | 54 | **239** |
| `forks` | 16 | **46** | 17 | **151** |

**±240 and not more, and this time the ceiling is resolution rather than calls.** 4096² over a
480 m box is **11.7 cm per texel** — the same figure this rig has resolved since R-W3b(a), and the
2048² phone map holds **23.4 cm**, likewise unchanged. ±360 m would need 6144² to hold that, or it
buys reach by blurring the eave shadow a visitor is standing under, which is the trade R-W3b(a)
refused. The route past here is **R-W3b(b)**, true cascades, and it is now a resolution parcel
rather than a budget one: at ±240 m the worst anchor sits **30 calls under budget**, where before
this it sat 6.

**FINDING 2, AND IT IS THE ONE TO CARRY FORWARD — a batch merge is not pixel-identical, and
R-W5a's acceptance could not have seen why.** The acceptance both halves of R-W5a inherit is
"whole-frame mean |Δ| under 0.01 of an 8-bit count", and this passes it four times over at
**0.0024**. But the mean is the wrong statistic for this operation: shot at seven poses, 1280×800,
**942 pixels of 7,168,000 changed, and the worst of them by 90 counts** — a whole surface, not a
rounding. They are scattered singletons over roofs and wall junctions, and the cause is that
merging sixteen batches into one **reorders the submission of co-planar triangles that were tying
in the depth buffer**, so the tie resolves the other way. That is **R-BUG6's** exact class of defect
(*"something in the frame is decided by a tie, and the tie is not stable"*), reached from a
direction R-BUG6 did not consider: a batching change can move a tie without touching a material, a
bias or a near plane. **The generalisation: an acceptance stated as a frame MEAN cannot distinguish
"nothing changed" from "a few hundred pixels changed completely", and the second is what a
reordering does.** A merge parcel owes a changed-pixel COUNT and a worst-pixel figure beside the
mean, which is what this box quotes and what R-W5a's does not.

**Why the per-vertex substitution is exact where it is exact, and it is not an argument, it is
6,999,058 pixels.** Roughness is written once per vertex from the source material, so all three
vertices of any triangle carry the identical float — a triangle never spans two source meshes — and
the interpolation of three equal values is that value. `perVertexRoughness` replaces
`#include <roughnessmap_fragment>` with `float roughnessFactor = vChiRough;`, which is that chunk
verbatim minus a `USE_ROUGHNESSMAP` branch no asset in this dataset takes (R-W2a: 1,353 material
slots, **zero** textures). If the substitution had silently failed, the whole town would have
rendered at ONE roughness and millions of pixels would have moved; 6,999,058 of 7,168,000 are
identical to the byte, which is a stronger proof than any assertion.

**The gate, and it is R-A1's shape.** Four assertions, of which the first two would pass identically
on a town that merged its batches by throwing roughness away — one batch, one sheen, every wall the
same — so the third is the one that does the work: the town is **1** batch; the merged batch still
carries **16** distinct roughness values spanning **0.25–0.98**; driving every vertex to 0.02 moves
the worst 48² cell by **13** (floor 4, a third of the reading, measured before it was set); and
restoring the channel returns the frame with residual **0**. `STRUCTURE_BATCHES = 1` is asserted as
an equality rather than a ceiling deliberately: a textured asset would legitimately raise it, and
raising it should be an edit with a reach measurement beside it, because the reach is standing on
this number.

**Verification.** `tools/check.sh` **CHECK PASS**. `SMOKE_VIEWPORT=mobile` on the published mirror:
**250 passed, 2 failed** against `origin/dev`'s **246 passed, 2 failed** on the same runner and the
same command — the same two road assertions `dev` already carries (R-BUG5b/#201 and T-V2/#135), and
the +4 is exactly this parcel's four new gates. No threshold, band or station was weakened. **The
desktop half of the smoke does not fit the runner's ten-minute per-command ceiling and did not run**
(ROADMAP § THE RUN BUDGET); the desktop figures above are `measure_shadow_reach.mjs` and
`measure_shipped_batches.mjs` at 1280×800 on the published mirror.

**Superseded numbers.** Any draw-call figure in this file taken before 2026-08-17 is a 16-batch
figure — including R-W5a's own 16, K36(b)'s 56-vs-16 and R-W3b(a)'s 70/74/78/80 ladder. The town
is one batch now and the ladder must be re-measured before it is quoted.

#### R-W5a2 — the parcel as written, kept for the record

**Phase:** RENDERING §4 W5 · **Runner:** improve-runner · **After:** R-W5a (done)

The 16 remaining building batches are one per distinct `roughness` in the town. Carrying roughness
per-vertex the way R-W5a carried colour would make it **1**, worth about 15 draw calls at every
station — measured, not estimated: R-W5a's own instrumented run counted 18 structure draw calls
before the three-decimal merge and 16 after, at every station.

**It needs a shader patch, which is why it was not done in the same run.** `vertexColors` is a
stock three feature; per-vertex roughness is not, and wants a `_roughness` attribute plus a
replacement of `#include <roughnessmap_fragment>`, chained onto `confidence.patch`'s
`onBeforeCompile` the way that patch already chains onto whatever came before it. The `_confidence`
channel is the proof the pattern works inside a `BatchedMesh` here.

**Take it only when the lane has nothing sharper.** The budget is met with 5 calls of headroom at
the worst station and the growth term is already zero, so this buys margin, not a fix.
*(Overtaken 2026-08-17: the margin WAS the fix — see finding 1 above. The paragraph priced the
colour pass and the shadow pass was where the count was being spent.)*

**Files:** `renderers/web/js/buildings.js` · `renderers/web/js/confidence.js` (chaining only)

**Acceptance:** 1 structure batch; draw calls ≤ 80 at all 11 stations, both viewports; triangles
unchanged to the triangle; the same frame-difference budget R-W5a measured itself against
(whole-frame mean |Δ| under 0.01 of an 8-bit count); zero page errors.

### R-W2 — texture the town · **UNCLAIMED · SPLIT**

**Phase:** RENDERING §4 W2 · **Effort:** L · **After:** R-W1

**The no-Blender half is itself TWO parcels — claim ONE:**

| | parcel | scope |
|---|---|---|
| **R-W2a** | ~~**the material sheet**~~ · **DONE 2026-08-16 — `docs/RESEARCH/materials.md`. Read its §4 before texturing anything: the chimney is not a material here, no record states a roof covering, and 27 % of the town is painted by a generator that shares no colour with the other 73 %** | Research and write it: which surfaces exist, what each is made of, its **roughness** (not only colour and tiling rate — see the R-G1 finding below), tiling rates, and which archetype parameter selects it. **Files:** `docs/RESEARCH/materials.md` (new) only. No code, no records, so no smoke — it is a document, and it is the input everything downstream needs. |
| **R-W2b** | ~~**wire the sheet in**~~ · **LANDED 2026-08-21 as T-0007** — `generators/common/materials.py` is the sheet as code and 207 of 243 committed GLBs were repainted from it. **The records needed no new material field:** `finish_key` (222 records) and `roof_condition` (218) were already committed in the `reconstruction` block, one level ABOVE the phase, which is exactly why no archetype could read them — so the wiring is `from_phase(phase, record)` rather than a 315-record schema change. Triangle delta 0 and material-count delta 0 (K36(a)'s five-material threshold binds hard). Findings 2 and 5 discharged; **finding 2's covering half stands untouched** — no `shingle` row exists and roofs are graded by weathering CONDITION. `docs/LIBERTIES.md` L155; materials.md §6; STATUS.md. | Take R-W2a's committed sheet and make the params and records name its surfaces. **Files:** `generators/archetypes/*_params.py` · `data/structures/*.json` (material fields only). Re-derives through the generators' `--check`. |

**R-W2a costs almost nothing to run and unblocks the rest** — it is reading and writing, not
rendering. Do not merge the two: a sheet argued and a sheet applied are different reviews.

**The bake half (nightly bake, arrives as a dev-targeted PR):** UV layout, atlas generation
and the actual textured GLBs. The `ktx` binary is installed on the bake runner as of
2026-08-14 (RENDERING §8 decision 5), so `--texture-compress ktx2` can finally run.

**Do not** attempt the bake half on the improve runner.

**From R-G1 — this parcel owns the two worst axes on the board**, texture **1.4** and material
**3.6**, and nothing else can move them. The scored reading: every surface in the town is one
flat colour, so a roof, a whitewashed clapboard wall, a hewn log, its chinking and a chimney
differ only in hue; there is no roughness variation anywhere, so nothing reads as painted,
weathered or wet; and the Wau-Bun blue shutters at `sauganash` sit at the same value as the
glazing beside them. The material sheet should name a roughness per surface, not only a colour
and a tiling rate.

### R-W2a — the material sheet · **DONE 2026-08-16 · `docs/RESEARCH/materials.md`**

**Phase:** RENDERING §4 W2.1 · **Runner:** improve-runner · **Effort:** S (a document) ·
**Files:** `docs/RESEARCH/materials.md` (new) · `docs/ROADMAP.md` · `docs/STATUS.md` ·
`renderers/web/js/changelog.js`. No code, no parameter, no record — so no smoke, by the
parcel's own definition.

**The sheet is measured out of the shipped GLBs, not read off the source**, because this
project has shipped a bug in that gap twice (B-BUG2). **334 assets carry 1,353 material
slots** resolving to **32 names, 41 base colours and 18 roughness values**; every one is
`metallicFactor 0`, `doubleSided`, `OPAQUE` and carries no map of any kind. It sizes every
tile to a whole number of the surface's own committed module (32 clapboard courses of 0.14 m
→ 4.48 m at 1024² → 228.6 px/m; 12 log courses of 0.34 m → 4.08 m → 251.0 px/m) so the tiles
land inside §4 W2's 128–256 px/m band without a chosen-to-look-right number anywhere.

**Five findings, none of them patched — this parcel ships a document:**

1. **The chimney is not a material in this project.** `frame_dwelling`, `frame_storefront`
   and `log_dwelling` build their stacks with `M_ROOF`: **219 stacks on 199 buildings are
   painted with the roof's colour.** The 90 inferred placeholders ship a real
   `placeholder_chimney_brick`. So the town *has* a brick chimney material and the archetype
   buildings do not use it — and `log_dwelling`'s own docstring argues at length that a
   frontier stack is stick-and-clay or fieldstone, a different object from a framed house's
   brick stack, which renders identically to it. Opened as **R-W2c**.
2. **No record anywhere states a roof covering.** 315 records state a roof *type* and 309 a
   pitch; **zero** state what the roof is made of. All 234 `roof` slots are one colour, and
   the board roof `outbuilding` argues for is separated from a shingle field by **0.03 of
   roughness and nothing else**. The repository's one direct attestation — the North Side
   school's "sheeted and shingled roof" — is read by nothing. Roofs cannot be textured until
   an attribute exists to select the covering, and that is a schema change across 315 records.
3. **A `documented` material fact is committed, correct, and rendered by nothing.**
   `cobweb_castle` carries `cladding: clapboard_part_way_up`, **attested**, sourced to
   `andreas_1884_v1` — and it is a `log_dwelling`, which does not read `cladding`, and the
   value is not in `CLADDINGS`. `cladding` is stated on 27 records and read on 22.
4. **27 % of the town is painted by a generator with no shared palette.** The 90 placeholders
   share not one colour and not one roughness with the 244 archetype assets (their walls are
   all 0.86, a value that appears nowhere else). They also read `roof_condition` — stated on
   **218 records** — and `finish_key`, and **no archetype reads either**, so on 244 buildings
   a weathered roof and a fresh one are the same pixel. An atlas that textures one path and
   not the other splits the town visibly in half.
5. **R-G1's "there is no roughness variation anywhere" is right about what matters and wrong
   as written, and the difference decides what W2 builds.** *Between* surfaces there are 18
   argued values spanning 0.15–1.00. What is absent is variation *within* a surface — every
   square metre of every wall has one roughness, which is why nothing reads as weathered.
   **The deliverable is a roughness map, not better constants.** Do not spend a round
   re-tuning the 18 numbers.

Two smaller ones on the record: `timber` is one name over two materials **3.2× apart in
linear red** (only the outbuilding's ships — no record turns `framing_exposed` on), and one
log wall in Chicago is a different timber from the other 52 (`frame_tavern` alone still
imports `LOG_RGBA`, and the affected asset is the Sauganash's log wing, in front of the
station named after it).

**It also decides the licensing question W2.1 has to answer: generate the atlas, do not
photograph it.** 38 of the project's 65 sources are `check_required`; the one full-resolution
photograph committed is CC BY-SA 4.0 cleared for measurement and **explicitly not for any
derived asset**; and the owner's twelve-view reference set says in its own README that it may
drive materials as `inferred` — while being the same `chicagology_*` material
`assets/LICENSES.md` gates. Procedural tiles built from the dimensional constants in the sheet
need no new clearance and keep the property this project actually cares about.

### R-W2c — the chimney is roof-coloured on 199 buildings · **DONE 2026-08-22 as ticket T-0008 — brick on the framed town, cat-and-clay on the log cabins**

219 stacks painted `roof` (finding 1 above). **It is not a palette fix, and picking the
placeholder's brick would be the wrong half of it**: `log_dwelling` argues a stick-and-clay or
fieldstone stack against the gable, `frame_dwelling` an interior brick stack at the gable end,
and those are two materials, not one. So the parcel **opens with the research question** —
what a Chicago chimney of 1835 was built of, by building type — and only then touches a
palette. `docs/LIBERTIES.md` L26 already owns every chimney's *position*; whatever this lands
owes the same treatment for its *fabric*.

**Files:** `docs/RESEARCH/` (a dossier) · `generators/archetypes/*.py` (material index only) ·
`generators/common/mesh.py` if a shared value is wanted. **NEEDS ONE BAKE** — it changes
material assignment on committed geometry, so it cannot go green on the improve runner and
should ship the research + palette half and say so.

**HOW IT LANDED, 2026-08-22 (T-0008), and the bake half came with it** — Blender has been on the
improve runner since 2026-08-19, so the parcel shipped whole rather than in halves: 245 generated
masters rebuilt, derivatives and publish in the same commit.

**The research is `docs/RESEARCH/chimneys.md`** and its answer is the one this box predicted —
two materials, not one — arrived at from what the repository already held rather than from a
palette. The framed town gets **brick**, `inferred`: the Petford watercolour of the Sauganash is
the one coloured witness here to any Chicago chimney and it says brick; Blodgett's brick-yard
opened on the North Side in the spring of 1833 (`brickyard_north_side`, Andreas p. 1161) and the
Lake House went up in brick in 1835; and an interior flue through a timber roof has to be masonry.
The log cabins get a **cat-and-clay daub**, `reconstructed` and bounded rather than picked — no
paler than the CHINKING it is daubed with, no darker than the palest ROOF CONDITION, and at the
midpoint of the two because nothing states where between them it sits. Fieldstone is the other
half of `log_dwelling`'s own sentence and is deliberately not built.

**The tone is not a new number.** `frame_tavern`'s `BRICK_RGBA` moved into
`generators/common/materials.py` verbatim — the same convergence T-0007 made for the hewn log —
so the Sauganash's masters come out byte-for-byte unchanged, which is the proof the value did not
move.

**Three findings.**

1. **It was not a one-file fix.** Four archetype modules and the sheet, because a material index
   is only the last step: `M_CHIMNEY` is appended CONDITIONALLY in each archetype, on the
   discipline `log_dwelling` already held itself to for `M_PAINT` — an unreferenced slot still
   reaches the glTF, so an unconditional append would rewrite every chimneyless master for a
   colour it does not use. Two `frame_storefront` masters keep their six-material list for
   exactly that reason.
2. **It cost NO draw call, and the reason is worth banking.** `buildings.js::materialKey` batches
   on type, emissive, metalness, the four maps, side, transparency and flat-shading — never on
   base colour and never on roughness, both of which ride per vertex since R-W5a2. So two new
   material colours merge into the buckets that already exist: **113 draw calls before and 113
   after** at `south_water`, 1280×800. A parcel that adds a COLOUR to this town is free; one that
   adds a MAP is not.
3. **R-W2a's own count does not reproduce.** This box says 219 stacks on 199 buildings; the
   resolved parameters of the committed masters give **157 stacks on 143 buildings** across the
   three archetypes plus `frame_tavern` (frame_dwelling 71/69, frame_storefront 33/33,
   log_dwelling 34/31, frame_tavern 19/10). The 2026-08-16 figure is not re-derivable from
   anything committed, so it is left as written and this is the measurement that replaces it.

**Left standing, in writing rather than by omission:** the fort's ten garrison buildings keep
roof-coloured stacks — 1816, federal ground, four constructions, and neither answer above reaches
them without inventing a third (**T-0137**); and the 90 inferred placeholders keep their own
`#89503F` brick, about 20 % apart in linear red from the archetypes' (**T-0138**), because
converging it moves 90 masters and the banked passthrough set. A third trap surfaced on the way:
the bake cannot reach `cook_county_courthouse_1835` at all, so any `generators/common/` edit
leaves it stale with no committed route to heal it (**T-0139**).

### R-W3b(a) — the shadow reach · **DONE 2026-08-17 — the sun lit the town and shadowed 8 buildings of 331, and the ceiling is draw calls rather than fill**

**The answer is 60 m, and it was costing the whole mid-field.** `world.js` gives the sun ONE
orthographic shadow camera, a box that follows the visitor, and everything outside it is clipped
out of the depth map before it is drawn — so it casts no shadow on anything. Counted off the DATA
(each structure's `placement.local_e/local_n`, each planted stem's own station) against the shadow
camera's own matrices, on the published mirror at 1280×800:

| anchor | structures inside, ±60 m | inside at ±120 m | stems, ±60 m | at ±120 m |
|---|---|---|---|---|
| `south_water` | **8** of 331 | **26** | **12** of 730 | **54** |
| `green_tree` | 8 | 27 | 0 | 0 |
| `sauganash` | 5 | 16 | 34 | 76 |
| `lake_market` | 5 | 13 | 33 | 73 |
| `forks` | 5 | 16 | 0 | 17 |
| `from_above` | **1** | 8 | 41 | 55 |

**Shipped: ±120 m, and the map doubles with it — 2048² desktop, 1024² phone — so the texel size is
UNCHANGED at 11.7 cm and 23.4 cm.** That is the whole reason the number is 120 and not 150: nothing
a visitor stands next to got softer to buy the distance. The before/after pair in
`docs/evidence/r-w3b-{before,after}.png` is shot at `green_tree` at both rigs AS THEY SHIP — the
first pair taken for this parcel compared ±60 m at 2048² against ±120 m at 2048², which is a
comparison of two texel sizes and made the near wall look like the change.

**THE FINDING — the reach is DRAW-CALL-bound, not fill-bound, and that is the opposite of what a
shadow map is usually limited by.** Every batch that enters the box is another draw call in the
shadow pass (three renders it inside `render()`, after `info.reset()`, so `renderer.info` counts
it). Measured at the worst anchor, `green_tree`:

| reach | draw calls | triangles | structures inside |
|---|---|---|---|
| ±60 m (shipped before) | 70 | 742,256 | 8 |
| ±120 m (**shipped now**) | **74** | 772,268 | 27 |
| ±150 m | 78 | 825,146 | 33 |
| ±180 m | **80 — the budget exactly** | 830,690 | 38 |

The budget is 80 (`main.js` `BUDGET.drawCalls`) and the smoke asserts it. So **±180 m fails the
gate at the first station that adds a batch**, with two thirds of the town still outside the box,
and the route past ±120 m is fewer batches — **R-W5a2**, "the last 16 batches → 1", which this
parcel therefore promotes from "not needed for the budget" to the thing that unblocks the reach —
or true cascades, **R-W3b(b)**. Raising the constant alone will not get there.

**AND R-W5a2 TOOK THAT ROUTE THE SAME DAY — the ladder above is a 16-batch ladder and is
superseded.** With the town merged to one batch the same worst anchor reads **48 calls at ±120 m
and 50 at ±240**, so the shipped reach is **±240 m at 4096²/2048², still 11.7 / 23.4 cm per
texel**. Read R-W5a2's box for the new table; do not quote 70/74/78/80 for anything but the
16-batch scene they were taken on.

**The gate, and the liveness assertion R-A1 says it owes.** `tools/smoke_renderer.mjs` asserts at
`lake_market` that the rig carries ±120 m over the right map for its tier, AND that winding the
reach back to ±60 m CHANGES the frame — because a reach wired to nothing passes the first
assertion identically. The threshold was measured before it was set: winding back moves 104 of
2,304 cells with a worst cell of 8 at 1280×800 and 86 with a worst of 8 at 390×780, and the gate
asks for 4. `world.setShadowReach()` exists for that assertion and nothing else.

**Files:** `renderers/web/js/world.js` (`SHADOW_REACH_M`, the shadow block, `shadowRig`,
`setShadowReach`) · `tools/measure_shadow_reach.mjs` (new — the instrument) ·
`tools/smoke_renderer.mjs` (two assertions) · `docs/evidence/r-w3b-{before,after}.png`.

**Not verified here:** the desktop half of the smoke does not fit the runner's ten-minute
per-command ceiling (ROADMAP § THE RUN BUDGET), so the desktop assertions were run through
`measure_shadow_reach.mjs` at 1280×800 rather than through the gate itself. The draw-call figures
above are that measurement, at every anchor.

### R-W3 — ambient occlusion and cascaded shadows · **UNCLAIMED · SPLIT**

**Phase:** RENDERING §4 W3 · **Effort:** M · **After:** R-W2

**The no-Blender work is THREE parcels — claim ONE. They are genuinely unrelated jobs that were
filed together only because RENDERING §4 groups them:**

| | parcel | scope |
|---|---|---|
| **R-W3a** | **the AO cage rule** | §1 item 10: the bake works end to end and fails because clapboard courses and window reveals a centimetre off the wall occlude each other (mean 0.265, 69 % of texels below half). It needs a **low-poly cage**, not tuning. **Files:** `docs/RESEARCH/ao-cage.md` (new) · `generators/archetypes/*.py` (cage emission). |
| **R-W3b** | **cascaded shadows** | `renderers/web/js/world.js` only — today one 1024² map on a ±60 m follow ortho, nothing beyond 60 m. **Touches no generator and no record**, so it shares nothing with 3a and can run beside it. **SPLIT 2026-08-17 into R-W3b(a) — the reach of the one map, DONE — and R-W3b(b) — true cascades, which (a)'s measurement says is now the only route past ±120 m that does not start by cutting batches.** |
| **R-W3c** | **openings** | The silhouette failure R-G1 names: no reveal, no sill, no sash, no muntin anywhere in the set, so the 6-over-6 rhythm the Green Tree plate documents does not exist. Archetype geometry. |

**The bake half (nightly bake):** re-bake with the cage and flip `baked_ao` on the 244 assets.
**After R-W3a**, and see `B-A1` before assuming the nightly should be the thing that runs it.

**3a and 3c are the same conversation about the same few centimetres of wall** (R-G1 says so),
so whoever takes one should read the other — but they ship separately.

**From R-G1 (geometry scored 4.6) — AO is carrying more than it looks like it is.** At the
scene's 70.5° sun a shadow is 0.354 × the height that casts it, so the only cast shadow legible
in the five scored frames is each chimney's on the roof beside it. Form in this scene therefore
has to come from the environment term (W1) and from this parcel's AO, and both are currently
off. Separately, the silhouette failure the score names is **openings**: no reveal, no sill, no
sash and no muntin anywhere in the set, so the 6-over-6 rhythm the Green Tree plate documents
does not exist. The cage rule and the opening geometry are the same conversation about the same
few centimetres of wall.

---

## LANE 2 — TOWN COMPLETION · data only, no renderer files

Carries the town toward its documented late-1835 density — the **665-roof programme** —
through the existing generators. **This lane touches no file lane 1 touches**, which is what
makes the two safe to run at once.

**Where the count stands after T-A5 (2026-08-14): 266 roofs · 156 households · 192 persons**
(76 source-attested, 20 reasoned-from-evidence, 96 invented-to-fill-a-need). 399 roofs remain of
the 665-roof programme, **71 of them on ground the project has coverage for** — the binding
constraint is coverage, not recipes, which is what lane 3 exists to move.

**The rules, every parcel:**
- Recipe → structure records + household records via the existing generators
  (`tools/generate_*_infill.py`, `tools/generate_inferred_households.py`,
  `tools/generate_inferred_names.py`), then `tools/compile_scene.py --all`.
- Placeholder massing from `generators/inferred_placeholder.py`. **No Blender.**
- **Every invention grades at the invented-to-fill-a-need tier with its reasoning note.**
  `tools/audit_confidence.py --strict` enforces the rule that nothing on an invented
  structure may outrank the invention that put it there.
- **Liberties appended** where a recipe embodies a compression — `docs/LIBERTIES.md` is
  append-only, and L91 shows the class-token form for a whole programme.
- `review_required: true` is honoured, not cleared. It blocks a scene from `released`.
- **Residents are RECORDS and Evidence/popup content only.** The no-human-figures constraint
  (AGENTS.md standing constraint, L1) is untouched by this lane and is not negotiable.

### T-A1 — refresh the 665-roof recipe · **DONE 2026-08-14**

Every later block parcel reads this, so it went first. The programme is now
`data/reconstruction/1835_665_roof_programme.json`, **derived** by `tools/reconcile_665.py`
and re-derived by `tools/check.sh` — a ledger about a town that grows most nights cannot be
an authored number, which is exactly how the crosswalk came to call 617 roofs remaining
while 232 were standing.

**232 physical roofs stand** (242 records: 12 of them are bridges, piers, a palisade, a
parade ground, a garden and a construction site that the reconciliation credits with no
roof, and one record is two cabins). **433 remain.** By district: South 270, West 94,
North 69, Fort 0 — the fort is complete.

**The finding that matters is not the count, it is where the count can go.** The plat module
reaches 19 blocks holding 152 lots. At the phase-1 parcel's own density — one principal roof
per lot, ancillary at the programme's 154:511 — those blocks have **105 roofs of headroom**.
The other **328 of the 433 have nowhere to stand**: 20 in the two blocks the module refuses
for want of South Water street control, 35 in the West recipe's own extension-gated set, and
273 in ground with no committed street control at all (east of State, south of Washington,
west of Clinton, and the whole North Division, which the grid does not cover by a single
block). **The binding constraint on the 665-roof programme is coverage, not recipes** — S9
street control and the terrain extensions are now what the town is waiting on, and T-A2
onward can only work the 105.

Six families are already **over** their target — C1, I2, T2, W1, W4, W5, nine roofs in all,
every one of them evidence the research placed after the target was written. A documented
roof is never removed to protect a family cap, so the excess is reported and taken out of
the invented family with the most slack (D4, the two-storey frame dwellings).

**Files:** `tools/reconcile_665.py` (new) · `data/reconstruction/1835_665_roof_programme.json`
(new, derived) · `tools/check.sh` (one step) · `1835_building_inventory.json` and
`1835_family_archetype_crosswalk.json` (stale statuses corrected) · `docs/ROADMAP.md` (S10) ·
`docs/STATUS.md`

### T-A2 — the first refreshed block · **DONE 2026-08-14 (`blk_randolph_wells`)**

Ten anonymous roofs on the block bounded by Randolph, LaSalle, Washington and Wells: seven
principal buildings on seven of its eight lots and three yard buildings off the alley, to the
family mix the schedule apportioned it (A1 A3 A4 D1 D2 D3 D4 D5 H1 H2). Standing roofs
**232 → 242**; remaining **433 → 423**, of which **95** still have modelled ground.

**The parcel shape that repeats, and it is not the one T-A2 was written expecting.** The three
earlier parcels authored their own coordinates — a row northing and a list of eastings, or a
centre per slot — because the plat module did not exist when they were written. This one
authors **no coordinates at all**: the recipe says which family stands on which lot, whether it
fronts the street or the alley, and how far back, and `tools/generate_block_infill.py` reads
every metre off the committed lot polygons. That is what makes T-A3…T-An a recipe entry rather
than a new geometry argument each time, and it retires by construction the defect class K7 found
(seven buildings in the middle of the road, from a recipe that never asked where the road was).

**Two findings came out of it that are not the block.**

- **`family_bands_ft` in the building inventory has no H1, H2, H3, C4, T1-T3, W5, F3, F4, I1-I3
  or M1 band** — 14 of the programme's 35 families — so the earlier generators could only build
  the families somebody had retyped into Python, and the schedule was apportioning H1 and H2 to
  this very block. **The crosswalk had them all along**: `1835_family_archetype_crosswalk.json`
  carries the footprint band, the storey count, the eave height and the placeholder archetype for
  every family, and agrees with `family_bands_ft` on all 21 both of them hold. This generator
  reads the crosswalk, so every family the programme can name is now buildable and no band is
  retyped anywhere. **H1 and H2 stand for the first time.**
- **The A3 privy's authored eave band (6-7 ft) dips below what the outbuilding archetype needs**
  to carry its own man door plus a header — refused by name at 1.891 m. The sample is now drawn
  from the part of the authored band the archetype can build (2.07 m here, beside phase one's
  privies at 2.05), and a family whose whole band sits under that floor fails loudly rather than
  being quietly raised out of its typology. Recorded in L92.

**Deferred, deliberately, and it is the one part of the parcel as written that did not ship:**
the **household layer**. Adopting these ten roofs as dwellings means restating
`1835_inferred_household_programme.json`'s occupation census — the generator gates the census and
the households against each other in both directions — and that is the K1 programme's own
argument about who the town's tradesmen were, not something a block parcel should re-decide as a
side effect. **T-A2h below owns it.**

**Files:** `tools/generate_block_infill.py` (new) ·
`data/reconstruction/1835_platted_block_parcels.json` (new, authored) ·
`data/structures/recon_1835_blk_randolph_wells_*.json` (10, derived) ·
`data/structures.schema.json` (four lot-provenance fields) · `data/sidecars/1835/` ·
`assets/…` placeholder massing · `docs/LIBERTIES.md` (L92) · `tools/check.sh` (one step)

### T-A2h — the ten roofs' households · **DONE 2026-08-14 (two adopted, eight refused)**

**Two of the ten roofs are adopted and the other eight are not, and the ratio is the finding.**
The parcel was written expecting an argument about the town's trade mix. The argument it actually
produced is about who is allowed to start one: a block parcel appends ten dwellings to the plat in
the time it takes to write a recipe entry, and an occupation census that grows to match is a
census driven by what has been drawn rather than by the town. The 3,265-people-in-398-dwellings
calibration is a claim about Chicago; letting a drawn cottage raise it is fitting the evidence to
the model.

**So the rule, now written into the household programme's own `method` list where the next parcel
reads it.** A block roof may be adopted only where BOTH tests pass: the trade's own committed
argument states in its text that its count is a **floor rather than a bound**, and the roof's
family is one this layer **already houses that trade in**.

- **Test one passes for exactly two of twenty-nine trades.** The carpenter — *"the shop count is a
  floor under the trade, not a measure of it"* — and the labourer — *"still a small fraction of
  what 3,265 people implies"*. Every other entry states a ceiling (the plasterer's and the
  drover's say *"and no more"* outright) or is bounded by a workshop or store family's roof target
  under method rule 2. Two apparent third and fourth matches are a false positive worth naming:
  the laundress and the boarding-house keeper entries contain the word *floor* only inside the
  Andreas quotation *"with the floor covered besides"*.
- **Test two, measured against the layer as it stood, picks the same two families.** All 8 of the
  layer's adopted labouring households live in a D1 and 9 of its 10 carpenters in a D3 — and a D1
  and a D3 are two of the seven dwellings this block deals. The tests were derived independently
  and agreed on the first block they were applied to, which is the only reason to trust either.
- **The result:** `hh_inf_labourer_south_13` in the D1 log cabin and `hh_inf_carpenter_south_11`
  in the D3 cottage. Households **152 → 154**, persons **188 → 190**, adopted anonymous roofs
  **83 → 85**. Standing roofs unchanged at **251** — this parcel built nothing.

**Three kinds of refusal, and only one of them is the rule.** The stable, privy and woodshed are
refused because a yard building has no occupant to argue about, and the generator now says so by
name. D2, D4 and D5 are refused by the rule: this layer houses laundresses, boatmen, masons,
clerks and shoemakers in those families and every one of those counts was argued to a number.
**H1 and H2 are refused for the strongest reason** — 18 larger houses and 14 merchant or
professional houses in the whole town, whose occupants are the most likely people here to be
nameable, so inventing an anonymous merchant into one would break the programme's own rule never
to infer a person where a documented one is available. They want T-I3's treatment, not a census
draw.

**The adoption is data, in one place, gated in both directions.** `tools/generate_block_infill.py`
now reads `tools/inferred_occupancy.py` exactly as the three earlier anonymous parcels do, so the
adoption is authored once in the household ledger and handed to whichever generator owns the roof
— hand-editing a generated record would have failed the drift check that makes these parcels
trustworthy. The new gate refuses an adoption that lands on an ancillary roof, and refuses a roof
the ledger names that no recipe builds. Both verified by doing each: the privy adoption fails by
name, and a household pointed at a non-existent block roof fails by name.

**One thing this parcel churned and did not fix — see K20.** Adding two people renamed **25 of the
94** reconstructed residents, because the invented-name allocator deals names round each pool by
index within a bucket, so an insertion shifts everyone after it. No grade moved and every name
re-derives, but the file's own docstring claims the assignment is a function of a person's id, and
it is a function of the whole population.

**Files:** `data/reconstruction/1835_inferred_household_programme.json` (census, two households,
method rule 6) · `tools/generate_block_infill.py` (occupancy + the adoption gate) ·
`data/residents/households/*.json` · `data/residents/index.json` ·
`data/structures/recon_*.json` (occupancy only, via the generators) · `data/sidecars/1835/` ·
`assets/manifest.json` · `docs/LIBERTIES.md` (L94) · `docs/ROADMAP.md` · `docs/STATUS.md`

### T-A3h — the second block's households · **DONE 2026-08-15 (two adopted, three refused, and the refusals traced)**

**The prediction held and the reason it held was not the one this box gave.** `blk_randolph_dearborn`
landed on 2026-08-14, a day before rule 6 took its third test, and its five dwellings had never been
asked the adoption question. Run rather than recalled — `tools/measure_adoption_tests.py <family>
south`, five times — the block's D3 on lot 0 is adoptable by the **carpenters** and nobody else, its
D1 on lot 3 by the **labourers** and nobody else, and its D5 by no trade at all. Both are adopted:
carpenter households **19 → 20**, labouring **22 → 23**, inferred households **99 → 101**, inferred
persons **111 → 113**, adopted anonymous roofs **102 → 104**. **Standing roofs unchanged at 322 and
remaining unchanged at 343** — this parcel raises no building, invents no position and moves no
record. Recorded in L109.

**THE OTHER TWO DWELLINGS ALSO PASS ALL THREE TESTS, AND WHAT THEY PASS ON IS THIS PARCEL'S
FINDING.** The D4 on lot 6 prints ADOPTABLE for the carpenters and the D2 on lot 5 for the
labourers, exactly as the "second roof" at eight blocks before this one did. Nobody had asked where
those verdicts come from:

- this layer houses **one** carpenter in a D4 — `hh_inf_carpenter_north_10`, in the **North**
  Division — and all thirteen carpenters it houses in the **South** Division are in a D3;
- it houses **four** labourers in a D2 — the shanties north_a, north_b, west_a, west_b — and all
  eleven labourers it houses in the **South** Division are in a D1.

**So neither candidacy is a pair this layer has ever housed.** Rule 6 says in its own committed text
that *the three tests are independent*, so test 2 reads the set of families and test 3 the set of
divisions, and a roof passes on a family taken out of one division and a division taken out of
another family. `tools/measure_adoption_tests.py --pairs` (new here) prints the whole table: **20
(family, division) pairs across 8 trades are admitted by the projections and housed by nothing**, and
test 1 narrows the ones that can actually be adopted to exactly **two** — the carpenters' D4/south and
the labourers' D2/south. Those two are the entire content of the second-roof question. Every refusal
K28 has collected — nine for the labourers, seven for the carpenters — refused a candidacy assembled
out of evidence that is never about the same roof twice.

**THE STRICTER READING IS NOT OBVIOUSLY RIGHT AND THIS PARCEL DOES NOT TAKE IT.** Requiring the PAIR
would refuse the **fourteenth labouring household**: T-A4 adopted a D1 in the WEST Division when this
layer housed labourers west of the river only in D2 shanties, and argued it in exactly the projected
form — the family from one division, the division from another family. Rule 6 names that adoption as
one of the four decisions its third test *recovers*, so a pair reading breaks the calibration the
rule rests on. Both facts are now committed and K28 decides with them in front of it; the tool
reports the column and gates nothing, because a gate would freeze the question shut.

**The two refused roofs are refused on T-A9's reading, unchanged**, for the ninth and seventh time,
as a choice rather than a rule. **Nothing was built on the block's three open lots**: they are named
open in T-A3's committed recipe with a reason each — one for the refused I3 civic slot, two on the
programme's alternating-vacancy assumption — and filling one to house a household would be the
fitting-the-model-to-the-drawing rule 6 exists to stop.

**The eleventh K20 measurement is 67 of 111** carried-over invented persons renamed — the highest
since T-A14's 61-of-108, and for the structural reason K20 predicts: two insertions landed in the
middle of the two largest buckets this layer has. No grade moved, every `name_basis` kept its pool
citation, and `check.sh` re-derives all 113.

**Files:** `data/reconstruction/1835_inferred_household_programme.json` (two households, two census
counts, two arguments) · `tools/measure_adoption_tests.py` (the `pair housed` column and `--pairs`) ·
`data/residents/households/*.json` · `data/residents/index.json` · `data/structures/recon_1835_blk_randolph_dearborn_{d1_04,d3_01}.json`
(occupancy only, via the generators) · `data/sidecars/1835/` · `assets/manifest.json` ·
`docs/LIBERTIES.md` (L109) · `docs/ROADMAP.md` · `docs/STATUS.md` ·
`renderers/web/js/changelog.js` · `site/chicago/4d/` (publish mirror)

### K20 — the invented-name allocator is not stable under insertion · **DONE 2026-08-16**

> **DONE — and the twelve anecdotes understated it. One new household renamed up to 73 of the
> 113 invented residents, 64.6 % of the layer, and in the two largest buckets it never renamed
> nobody. It is 10 now, the pools are the reason it is not 0, and the instrument is committed.**
>
> **The eleven measurements were all real and all low.** T-A2h read 25 of 94, T-A5 17 of 33
> touched, T-A9 19 of 98, T-A14 61 of 108, and L101 — the worst before this — 72 of 100. Every
> one was a by-product of a parcel doing something else, which means every one measured a
> single arbitrary insertion at a single arbitrary point in the hash order. Sampled properly,
> with 240 synthetic single-household insertions across all six trades this layer populates,
> the distribution is not centred anywhere near 25: mean **40.4** for a carpenter, worst
> **73 of 113**, and **1 of 40** probes in that bucket renamed nobody. The parcels that read
> 17 and 19 were lucky, and the argument that "a fifth of the layer" was the cost was built on
> the low half of a distribution nobody had drawn.
>
> **The cause is exactly what the parcel predicted, and the fix is the shape it proposed with
> one change.** Dealing by index makes a name a function of *how many people sort ahead of you*.
> It is now a function of *who you collide with*: each person has their own deterministic
> ordering of the pool, and taking them in the same stable hash order, each claims the
> least-used name they are permitted. The change to the proposal is that **a given name and a
> surname are not the same problem** and the old code welded them to one index. A repeated
> given name is what a town looks like — five Johns among 73 men in 1835 is unremarkable and
> claims nothing about anybody — so a given name is now simply each person's first preference,
> with no ledger at all, which is the most insertion-local rule available. A repeated *surname*
> reads as kinship, which this layer asserts of nobody, so that one keeps the ledger and the
> floor rule that holds every count within one of every other.
>
> **Measured after, on the same 240 probes: worst 10 of 113, mean 4.6.** Splitting the two
> halves is a third of that improvement on its own — the floor rule on both halves gives 17.
>
> **The residual is the POOL, not the allocator, and the report proves it rather than asserting
> it.** `tools/measure_name_churn.py` prints each bucket's pressure — its size over its surname
> pool. The two buckets with room to spare (**0.14×**) rename **at most one** person, which is
> the literal acceptance criterion: only the person actually collided with. The four dealing 36
> surnames to 73 men (**2.03×**) rename up to ten, because at that pressure there is no spare
> name at the floor, so the newcomer must displace somebody and that person displaces the next.
> **8 renames at pressure 2.03× is a pool that is too small; 8 at 0.14× would be an allocator
> that is still not local.** The gate reads the second as a failure and the first as arithmetic.
>
> **A bug the fix exposed, which the index deal had been hiding.** Unwelding the given name from
> the surname allows two people to draw the same pair, and the first run of it shipped **two
> Alvah Hastings** — two invented residents who were the same person. The allocator now carries
> that as its one absolute constraint; all 113 full names are distinct.
>
> **The one-time cost is the whole layer: 113 of 113 renamed, 101 household files.** That is
> what K20 said it would be, it is recorded as **L111**, and it invents nothing new — the pools,
> the grading, the `name_basis` citation and the note are untouched, and a different invented
> name is the same claim about the same nobody.
>
> **The durable half is a gate**, in `check.sh` at ~2 s: `measure_name_churn.py --gate` fails if
> one insertion rewrites more than **16** names. Sixteen rather than ten because what it must
> catch is the class — an allocation that depends on how many people precede you — and every
> measurement of that class has been above it. If growth ever fires it, the answer is a wider
> pool, not a higher number.
>
> **What this does NOT fix, and what to open if the diffs go noisy again:** the surname pools
> are 2.03× oversubscribed and are seeded from the 76 attested residents this project holds, so
> widening them is **evidence work** — more named 1835 Chicagoans out of Andreas and the census
> rolls — and not a tuning knob. At 3× pressure the residual will climb again. That is the
> parcel to open, and it buys a better-attested pool as well as a quieter diff.
>
> **Files:** `tools/generate_inferred_names.py` · `tools/measure_name_churn.py` (new) ·
> `tools/check.sh` · `data/residents/households/*.json` (101) · `data/sidecars/1835/*.json` ·
> `docs/LIBERTIES.md` · `docs/ROADMAP.md` · `docs/STATUS.md` · `renderers/web/js/changelog.js`
> and the published mirror. `data/residents/index.json` is deliberately untouched: it carries
> person ids, not names, which is the point the naming tool's own closing comment makes.

`tools/generate_inferred_names.py` said of itself, before this parcel: *"Assignment is DETERMINISTIC, from a hash of
the person's id. Re-running produces the same town… nobody has to wonder whether a name drifted."*
The first clause is what the code was built for and the second is not what it does. Pass two deals
each `(community, sex)` bucket round its pool **by index** — deliberately, to stop four unrelated
households sharing a surname — so a person inserted into a bucket shifts every name after them.
Measured on T-A2h: **two new people renamed 25 of the 94** reconstructed residents.

Nothing about that is a provenance failure — every name is invented, graded `reconstructed`, and
re-derives under `--check`. It is a churn and a documentation defect, and it compounds: every
future block parcel will rewrite a quarter of the town's invented names as a side effect, which
buries the parcel's real diff and makes a genuine drift harder to see.

**The likely fix** is to keep the anti-collision property while making it insertion-local: give
each person a deterministic permutation of the pool from their own id and, walking people in
stable hash order, take the first pair not already claimed. An insertion then only bumps the
people it actually collides with. That is a **one-time rename of the whole layer** in the PR that
does it, which is why it belongs in its own parcel with its own liberty note rather than riding
along with a block.

**Files:** `tools/generate_inferred_names.py` · `data/residents/households/*.json` ·
`data/residents/index.json` · `docs/ROADMAP.md`

**Acceptance:** adding one household to the programme renames only the people who collide with it,
demonstrated by measurement in the PR; `tools/check.sh` green; no grade moves and no `name_basis`
loses its pool citation.

**Measured a second time by T-A5 (2026-08-14):** a **one**-household insertion renamed **17 of the
33** carried-over invented persons in the household files it touched, and dragged 24 files into a
diff whose real content is one addition. Two independent measurements at the same rate; the "buries
the parcel's real diff" paragraph above is now demonstrated rather than predicted.

### K21 — the adoption tests are silent, not negative, for four trades · **DONE 2026-08-15**

**The answer was the first of the two the parcel offered, and it was not close.** Every one of the
31 buildings this layer raises was dealt a crosswalk family by the programme, and every one has
always *said* so in prose: the footprint note reads "a 16 x 22 ft rectangle from the **D3** family
band", and each form value cites the same band. What no record carried was the band as a **value**.
So there was nothing to decide — the assignment is a transcription of a string committed in two
other places, which is why **it owes `docs/LIBERTIES.md` nothing**: a liberty is an invention, and
writing down what was already committed invents nothing. The second branch (records deliberately
outside the typology, rule 6 gaining a fourth clause) was never reached, and rule 6 gains **no new
clause** — a trade whose families are now readable can still fail the test.

**What it measured, before and after.** Of 29 census trades, **four resolved nothing**
(`brickmaker`, `packer`, `sawyer`, `wheelwright`) and **eight resolved partly** — 17 households
stood on 31 roofs that named no family. After: **29 of 29 trades resolve, across 44 trade-family
pairs**, and the two sawyer households T-A5 refused now read D3 and D2 — facts a parcel can check
rather than a question it could not ask.

**The gate is the durable half.** `tools/generate_inferred_households.py` now fails if any roof a
household *lives or works in* names no family in the crosswalk, over both links rather than the
dwelling alone — a shop's family is as much a claim about the town as a cottage's. A test cannot go
silent again without a gate saying so, which is the same medicine T-A4's `deferred` gate applied
one level down.

**The suspicion in the parcel's own Watch note is refuted, and the refutation is the useful part.**
`inf_sawyer_dwelling_b` masses as an `outbuilding` while `_a` masses as a `frame_dwelling` because
**they were dealt different families** — D3 and D2 — and each resolves through its own family's
committed placeholder archetype. The programme says so in the record's own existence note: the
second sawyer's roof is "a plank dwelling of the schedule's D2 shanty family, which is what the
meanest end of the building trade lived in". Two dwellings of one trade massed as different kinds
of thing is the deliberate claim, not a defect. **The real archetype split is elsewhere and the
Watch note pointed at the wrong record:** five W4 shops, one family, are massed two ways —
`inf_shoemaker_shop`, `inf_tailor_shop` and `inf_barber_shop` as `frame_storefront` at a 3.25 m
eave, `inf_gunsmith_shop` and `inf_harness_shop` as `outbuilding` at 2.05 m. All five are
one-storey, so W4's own licence for the storefront massing ("acceptable only for one-storey
massing; two-storey shop-house variants need dwelling/storefront openings") does not explain it.
That is **K25**, with the larger finding it opened.

**Two side effects, both caught by gates rather than by reading.** `tools/reconcile_665.py`
classified a record by whether it carried a reconstruction block at all, so all 31 moved from
`inferred_household_programme` into `generated` — totals unchanged, attribution wrong, which is
precisely the kind of thing a total hides; it keys on the status now. And `compile_scene.py` sent
every reconstruction-block record to the anonymous-infill dossier, which would have put a visitor
who clicked a building raised for one argued household in front of a write-up about aggregate
count-units; the household layer has its own dossier and now points at it. That link is dead on the
live site for every building on the site — see **K26**.

**Files:** `tools/generate_inferred_households.py`, `tools/compile_scene.py`,
`tools/reconcile_665.py`, `data/structures.schema.json` (the block gains an `inferred_household`
status and an `occupation`; `sequence` and `inventory_class` are required of the anonymous status
only, because a bespoke roof has no parcel slot and inventing one would be a claim),
`data/reconstruction/1835_inferred_household_programme.json` (rule 6 records the resolution),
31 structure records + their sidecars.

<details>
<summary>The parcel as it was written</summary>

**Phase:** lane 2, data only · **Runner:** improve-runner (no Blender)

Rule 6 of the household programme's `method` list now has three tests, and the second asks whether
the roof's family is one this layer already houses that trade in. **For four trades that question
has no answer.** `brickmaker`, `packer`, `sawyer` and `wheelwright` are housed exclusively in
bespoke `inf_*_dwelling_*` records raised by the inferred-residents parcel, which carry no
`reconstruction.family` field at all — they were built to order against the census rather than
dealt off the roof programme. Eight further trades (blacksmith, boatman, carpenter, cooper, grocer,
labourer, mason, teamster) are partly so, and for those the test can still be answered from the
households that do stand on a family-bearing roof.

**Why it is not merely tidiness.** T-A5 met the case head on: the two sawyer households stand on
`blk_randolph_market` itself, and the sawyer argument's *"the smallest number that answers the
demand"* passes test 1 cleanly. The trade was refused adoption because test 2 could not be
evaluated, not because it was evaluated and failed. **A refusal this project cannot distinguish
from an unanswerable question is the same defect T-A4's `deferred` gate was written to close**, one
level up.

**What is owed.** Decide which of two things is true and say so: either each bespoke inferred
dwelling can be assigned the crosswalk family its committed footprint and form already sit inside —
in which case assign them and the test answers itself — or those records are deliberately outside
the family typology, in which case rule 6 needs a fourth clause naming the silent case and stating
what happens in it. **Do not simply grant the silent trades a pass**: that would let a census grow
on the strength of a missing field.

**Watch:** `inf_sawyer_dwelling_b` resolves through the `outbuilding` archetype while `_a` resolves
through `frame_dwelling` — two dwellings of one trade massed as different kinds of thing. Worth
looking at while in the file; it may be the same root cause and it may be a second finding.

**Files:** `data/reconstruction/1835_inferred_household_programme.json` ·
`tools/generate_inferred_households.py` · `data/structures/inf_*_dwelling_*.json` ·
`docs/LIBERTIES.md` · `docs/ROADMAP.md` · `docs/STATUS.md`

**Acceptance:** every trade in the occupation census either resolves test 2 or is named as a case
rule 6 explicitly handles; `tools/check.sh` green; `tools/audit_confidence.py --strict` green; no
household is added by this parcel.

</details>

### K25 — the invention is not bounded by the specification it cites · **(a) DONE 2026-08-15 · from K21 · (b) NEEDS THE BAKE**

**Phase:** lane 2 for (a), and (b) NEEDS THE BAKE · **Effort:** M

**(a) DONE 2026-08-15 — it is 98 values, not 54, and 24 causes, not 98.** The parcel was
scoped from an eave count taken on 193 records. Measured properly — every reconstructed
record in the dataset, and every form value the crosswalk authors a testable band for —
**1135 values were tested against a band and 98 are outside it, on 80 of 249 records**:

| field | tested | outside | near the edge |
|---|---:|---:|---:|
| eave (`wall_height_m` vs `eave_ft`) | 249 | **54** | 46 |
| roof pitch (vs the `roof` rise:run) | 207 | **38** | 38 |
| storeys + loft (vs `levels`) | 181 | **4** | 1 |
| footprint (vs `footprint_ft`) | 249 | **2** | 0 |
| roof form (vs the `roof` prose) | 249 | **0** | — |

The eave figure of 54 survived the widening by coincidence; T-V1(a)'s 40 is its
anonymous-layer half (40 + 14 household). **Roof pitch had never been measured by
anything**, and it is the second-largest fault in the dataset's provenance.

**The 98 are 24 causes.** Every offender is one of a handful of archetype constants
landing on a family whose band nobody checked it against — 13 distinct (family, value)
pairs hold all 54 eaves and **six values hold all 38 pitches**:

| | value | band | records |
|---|---|---|---:|
| eave | 2.78 m = 9.12 ft | D3 8–9 ft | 20 |
| eave | 2.05 m = 6.73 ft | D2 7–8 ft | 10 |
| eave | 2.05 m = 6.73 ft | W4 9–18 ft — **the worst, +2.27 ft** | 3 |
| pitch | 18.0° = 3.90:12 | D2 4:12–8:12 | 21 |
| pitch | 32.0° = 7.50:12 | A2 8:12–12:12 | 9 |
| pitch | 38.0° = 9.38:12 | H2/H3 6:12–9:12 | 4 |

**Seven metre values account for all 54 eaves** — 2.05, 2.75, 2.78, 3.25, 5.05, 5.20,
5.35 — which is the archetype table, not a measurement of anything.

**Pitch has its own mechanism, and it is a unit mismatch.** The crosswalk authors
rise:run; the generator authors whole degrees. 4:12 is 18.435°, and the shed constant is
18.0°, so **21 D2 sheds are 0.10 of a 1:12 step under a floor they would have cleared if
the value had been authored in the band's own units**. All 38 pitch offenders are within
one step. That is the diagnosis, not a defence — and it tells (b) exactly what to do:
author the pitch from the band's rise:run rather than from a degree constant.

**The sub-1-ft decision, which (a) owed: they are failures.** 46 of the 54 eaves are
within a foot and every pitch is within a step, and nearness is exactly what a retyped
constant looks like — 2.78 m clears D3's 9 ft ceiling by 37 mm because the frame-dwelling
archetype builds 2.78 m walls, not because anyone measured a cottage. A tolerance wide
enough to forgive that is wide enough to forgive a third of a D3 band, and it would
forgive the fault the parcel exists to name. The only slack in the tool is 1.5 mm for the
metre round-trip; five footprints sat half a millimetre over an edge and are exact whole
feet in the source, so they are not counted.

**And a second fault the parcel did not know it had.** The same sentence is attached to
values the crosswalk says nothing about at all: **`paint` on 227 records, 220 of them
against a family that never mentions paint; `board_gap_m` on 99 against a specification
that names no board gap anywhere; `chimneys` on 150, 93 of them silent.** A note citing a
band that does not speak to the value is a different fault from a value outside its band —
worse in kind, since there is no band to be inside — and the instrument that finds it is a
keyword over the family's authored strings, so it is **reported and not gated**. It wants
its own parcel; see **K33** below.

**What shipped.** `tools/measure_band_claims.py` — census, `--strict` (the assertion (b)
must turn green; it exits 1 today) and `--gate` (a ratchet against the committed census in
`tools/band_claims_baseline.json`, on every `check.sh`). Both halves of the ratchet were
broken on purpose and proved to fail before being trusted: planting a 4.9 m D1 wall is
caught as NEW, and repairing `recon_1835_north_d3_002` without re-writing the baseline is
caught as an unrecorded repair. **The fault may shrink and may not grow.** No dimension
moved; the strict assertion is red on purpose and `check.sh` runs the ratchet, because a
permanently red dev gate would block every unrelated parcel behind it.

**(b) is blocked exactly where T-V1(b) is blocked.** Every offender is on a parcel whose
meshes are canonical Blender bakes; changing a dimension stales the GLB, `validate.py
--all` fails a stale GLB, that validator is the dev gate, there is no Blender on the
improve runner, and `chicago-4d-bake.yml` bakes from `dev`. The repair cannot pass the
gate it must pass to reach the branch the bake reads. T-V1(b)'s three routes are (b)'s
routes; choosing one is the owner's.

---

*The original parcel description follows, with its 193-record numbers left as written.*

Every reconstructed roof carries the same sentence on every form value: *"Type-level choice within
the D3 band in the reconstruction specification."* For **54 of 193** records the value is not in
that band. Measured against `key_geometry_parameters` in
`data/reconstruction/1835_family_archetype_crosswalk.json`, reading `wall_height_m` as the eave the
placeholder massing builds it as:

| layer | records | outside | worst |
|---|---:|---:|---|
| anonymous infill (`recon_1835_*`) | 162 | **39** | F2 at 17.6 ft against 19–23 |
| inferred-household (K21's 31) | 31 | **15** | W4 at 6.7 ft against **9–18** |

**The root cause is one line, and it is not a typo.** `inferred_form()` in
`tools/generate_inferred_households.py` — and its counterparts in the anonymous generators — choose
every form value from the **archetype**, consulting the family only for a handful of special cases.
So `outbuilding` hands out a 2.05 m wall whether the family band asks for 7–8 ft (D2, near enough)
or 9–18 ft (W4, out by a third of the band's floor), and the note attached to that value cites the
band regardless. **Fifteen of the 54 are within 1 ft and read as rounding** (D3 at 9.1 ft against a
band ending at 9.0). The other end is not rounding: `inf_laundry_north` is 280 sq ft against an A5
band of 48–192, and `inf_sawpit_shed` is 720 against W5's 792–2160.

**Why it outranks a tidy-up.** A note that cites a band is a provenance claim — it says the
invention is *bounded by the specification*, which is the whole defence for inventing it. Where the
value is outside the band the note is not merely imprecise, it is **wrong about its own source**,
and it is wrong on 54 buildings at once.

**(a) land the failing measurement.** A gate that reads each form value against its family's
committed band and fails, committed RED with the numbers above quoted, plus the decision about the
sub-1-ft cases (widen the tolerance and say why, or accept them as failures). Data and tools only;
no geometry moves. **(b) turn it green** takes (a)'s numbers as the baseline. Some fixes are a
number in a table; any that changes a wall height changes the massing and **needs the bake**, so
(b) ships the data half and says so.

**Do not fix this by widening a band.** The bands are the specification's, not this project's, and
a band widened to admit the value it was supposed to bound stops being evidence. Where a value
genuinely belongs outside its band, the record's note must say so in its own words instead of
citing a band it does not sit in.

**The W4 split rides along.** Five W4 shops, one family, two massings (three `frame_storefront` at
3.25 m, two `outbuilding` at 2.05 m) and all five one-storey, so the family's own licence for the
storefront does not explain it. Decide which is right for a one-storey artisan shop and make the
five agree, or record why a barber's shop and a gunsmith's are different kinds of building.

### K33 — the note cites a band for values the specification does not bound · **DONE 2026-08-15 · 623 values, and 42 of them nothing could have found**

**Phase:** lane 2 · **Effort:** S to decide, M to apply · data and tools only, no bake

**DONE 2026-08-15 — it is 623 values on 227 of 249 records, and the decision is route 2:
split the note.** The box below scoped it from the prose census (581). The true figure is
**623**, because the census could only ask its question of the fields it had classified as
prose, and **42 `roof_pitch_deg` values cite a band on five families whose roof line is
"gable or shed"** — a form with no slope in it. Those were invisible to K25(a) for a
structural reason worth keeping: **a value with no band is never tested against one**, so
the banded half of the tool walked straight past the very records where the fault is total
rather than partial. The generous keyword instrument was not the only floor in the census;
the classification itself was.

| field | repaired | field | repaired |
|---|---:|---|---:|
| `paint` | 220 | `door` / `door_side` | 37 each |
| `chimneys` | 93 | `bays` | 35 |
| `board_gap_m` | 69 | `porch` | 23 |
| `plan` | 46 | `goods_door` / `goods_door_side` | 8 each |
| **`roof_pitch_deg`** | **42** | `gallery` / `shopfront` | 4 / 1 |

**The decision, and why route 2 rather than route 3.** Route 1 (extend the crosswalk) would
author evidence rather than record it and is refused. **Route 3 — grade these a level lower
— is not available at this project's price, and the reason is mechanical: the confidence
FLOATS are hashed into `generators/mesh_inputs.py`'s input recipe.** Regrading 623 values
would stale 249 committed GLBs, and that is the identical wall T-V1(b) and K25(b) are stuck
behind. **Prose is not hashed.** So route 2 is both the honest repair and the only one that
lands without a bake — and that coincidence is worth naming, because next time it will not
be a coincidence and somebody will be tempted by the cheap one anyway.

**What the note says now.** It negates the paragraph above it rather than quietly dropping
a citation. Every one of these values is prefixed by a generator-level lede reading *"the
spec is cited because the invention is bounded by it"* — the exact claim that is untrue
here — so dropping the trailing citation alone would have left the false impression intact
and made the repair invisible. The replacement opens `NOT BOUNDED BY THE SPECIFICATION,
and the sentence above about the invention being bounded does not hold for this value`,
names the family and the field, and says what the value actually is: the reconstruction
generator's type default. Each parcel's own closing clause ("it is not evidence for this
anonymous North Division instance") is preserved verbatim.

**What shipped.** `tools/band_notes.py` — the single predicate for *may this value cite the
band*, imported by all five generators that author the sentence and by
`tools/measure_band_claims.py` that audits it. One file, because `family_bands.py` exists
for exactly this reason and its docstring says so: the same arithmetic in two files, and
only one of them ran. The assertion is now in `--gate` and `--strict` and is **absolute —
no baseline, no allowance**, in deliberate contrast to K25's ratchet beside it, because
this repair costs prose and cannot block anything. Proven in three directions before being
trusted: **red at 623 against the pre-repair data**, **green at 0 after**, and a planted
fresh offender caught. It also fails on a citation attached to a field neither table has
classified, so the next invented fitting cannot inherit a citation by default.

**What did NOT change, and the residual.** No value moved and no geometry moved; 623 note
strings and nothing else. Two things are left open on purpose:

- **`sources` still lists the spec on these values.** The note now says the spec does not
  bound them, while the machine-readable `sources` array still cites it. The spec IS the
  source of the family assignment that produced the archetype default, so it is not simply
  wrong — but the two fields no longer say the same thing, and that is a smaller version of
  this same parcel's subject. It wants a decision, not a sweep.
- **The prose tier keeps its citation.** Where the crosswalk speaks without bounding —
  `construction` as "hewn or round logs with chinking", `variants` as "2/3 bays; external
  chimney" — the citation stands. K25(a) drew that line when it separated the prose fields
  from the banded ones and K33 does not reopen it. A parcel that wants to argue the middle
  tier down is a new one, and it should read `PROSE_KEYWORDS` first: the instrument is a
  keyword and generous by design.

---

*The original parcel description follows, with its 581-value prose census left as written.*

K25(a) measured the values the crosswalk *does* bound. This is the other half, and it is
worse in kind: **`paint` on 227 records carries "Type-level choice within the D3 band",
and 220 of those families never mention paint at all.** There is no band to be inside.
The census, printed by `tools/measure_band_claims.py` on every run:

| field | records citing a band | of which the family's authored geometry says nothing |
|---|---:|---:|
| `paint` | 227 | **220** |
| `chimneys` | 150 | 93 |
| `board_gap_m` | 99 | **69 — and the specification names no board gap anywhere** |
| `plan` | 103 | 46 |
| `door` / `door_side` | 99 | 37 each |
| `bays` | 103 | 35 |
| `porch` | 35 | 23 |
| `gallery` | 4 | 4 |
| `construction`, `cladding`, `gable_front` | 249 / 21 / 21 | 0 |

**The instrument is a keyword** over the family's `key_geometry_parameters` strings, and
it is deliberately generous — a hit means the specification *mentions* the thing, not that
it bounds it. So the true count is a floor, and the field is reported rather than gated
until the decision below is made.

**It is a decision before it is a fix.** These values are not wrong; a board gap of 12 mm
on an unpainted plank shed is a perfectly ordinary invention. What is wrong is the
*citation*: the note says the value is bounded by a specification that does not speak to
it. Three candidates, and the second is the honest cheap one: extend the crosswalk so the
specification actually authors these (large, and it would be authoring evidence rather
than recording it); **or split the note — cite the band only where a band exists, and say
plainly "the specification does not speak to this; the value is the archetype's default"
where it does not**; or grade these values a level lower than the ones the band covers.

**Whatever is chosen, `tools/measure_band_claims.py` gains the assertion** — a value may
cite a band only if the family authors one for it. Until then the census prints and does
not fail, and this box says why.

### K34 — what `review_required` actually blocks · **DONE 2026-08-16 · one record claimed the flag in prose and never carried it, and the block read buildings only**

**Phase:** lane 2 · **Effort:** S to measure, S to gate · data, tools and docs only, no bake

AGENTS.md puts one constraint above the work — *the final removal of the Potawatomi from
Chicago occurred in August 1835, inside this project's first target year* — and gives it one
mechanism: **`review_required: true` on any record blocks a scene from being marked
`released`.** Nothing had ever measured what that sentence covers. It covers **9 structures
of 332**; it did **not** cover the **7 households of 173** that carry the same flag, nor the
person layer that carries the same two fields.

**FINDING 1 — `hh_caldwell_billy` says it carries the flag and never has.** Its
`research_note` has read *"It carries review_required so that no scene containing it can be
marked released before the consultation the project has committed to"* since the record was
written, and `git log -S` finds no commit in which the field was ever `true`. The sentence is
the same one `hh_robinson_alexander` carries, where both fields ARE set. Billy Caldwell —
Sauganash, the agency's interpreter, the namesake of the town's best-known tavern — is the
one household in this dataset whose own text quotes Andreas putting its subject at the head
of the march to the Missouri. **Both flags are set now, on the record's own committed text
and on nothing new**, and the note records that they were false and that the paragraph above
them said otherwise. `touches_removal ⇒ review_required` could not catch it because
`touches_removal` was false too.

**FINDING 2 — the release block was `data/structures/` alone, and the households were safe by
coincidence.** `validate.py`'s scene gate built its `blocked` list out of structures while
its own household-side error promised that *"any record touching it blocks a scene from being
marked released"* — a consequence that did not follow. The seven flagged households were
covered anyway because **all 11 of their `lives_at`/`works_at` links land on a structure that
is flagged too**. Nothing required that. A flagged household with a null `lives_at` and an
unflagged workplace — or with no links at all — passed clean, and the self-test that proves
it is committed.

**FINDING 3 — the same sentence read the other way is a deliberate, honest NO.**
`chappel_infant_school`, `walker_meeting_house` and `watkins_school_house` each say
*"review_required is set false … but the call is worth a second opinion"*, and each is false.
That is the reason assertion 1 tests **both directions** rather than "prose mentions the
constraint ⇒ set the flag": three settler buildings that reasoned their way to `false` in
writing are not defects, and a gate that could not tell them from finding 1 would have been
a gate arguing for its own conclusion. **Three of the nine flagged structures — `beaubien_barn`,
`clybourn_slaughterhouse`, `robert_kinzie_store` — state no reason at all**, which is the
open end of this parcel and is left open rather than guessed at: see K35.

**WHAT SHIPPED.** `tools/measure_review_constraint.py`, in `check.sh`, with **four absolute
assertions and no ratchet** — a ratchet is the instrument for a fault being paid down, and
this is a commitment. (1) a record whose prose claims the flag carries it, and one whose prose
declines it does not; (2) `touches_removal ⇒ review_required` at household AND person level,
the person half never having been asked; (3) the flag reaches the building a constrained
household lives or works in, 11 of 11; (4) **behavioural** — `validate_scene` is run against
the real dataset with `released` forced true and the blocked set it names must equal the union
of flagged ids across every layer, so a gate that restated the rule cannot pass while the
validator disagrees with it. Plus `tools/review_constraint_baseline.json`: adding a flag is
free, **clearing one fails** and names what clearing it would mean.

**All four were broken deliberately before the gate was trusted** — the Caldwell flag cleared
again, `cobweb_castle` unflagged under three households, a person given `touches_removal`
without `review_required`, and the validator reverted to reading structures only. Each exits
1 with the divergence named; the restored tree passes.

**WHAT IT DID NOT DO.** It moved no building, no household and no coordinate, invented
nothing, and upgraded no confidence. No liberty is owed: `docs/LIBERTIES.md` records
inventions, and nothing here was invented.

**Verified:** `tools/check.sh` green. `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs`
green against the published mirror. The desktop half was not run and is not claimed — it
needs ~13 minutes against this harness's 10-minute per-command ceiling (see the run-budget
box at the top of this file). This parcel changes no renderer file and no geometry.

### K35 — three records carry the standing constraint and say why nowhere · **UNCLAIMED · opened 2026-08-16 by K34 · Effort: S — a research question, then possibly a field**

`beaubien_barn`, `clybourn_slaughterhouse` and `robert_kinzie_store` carry
`review_required: true` and no text anywhere in the record says what for. Six of the nine
flagged structures do explain themselves in prose, and three settler buildings explain in
prose why they are deliberately NOT flagged (K34 finding 3) — so the reason is *usually*
written down, by convention rather than by rule.

**The question is not "why are these three flagged".** It is whether a bare boolean is the
right carrier for a commitment this project puts above the work. Households have
`touches_removal` beside `review_required` and structures have nothing equivalent, so on the
building side there is no field in which a reason could live even if somebody wrote one.

Three routes, and the choice belongs with the owner rather than with a gate:

1. **Prose convention, asserted.** Require every flagged record to say something — K34's
   assertion 1 already reads prose, so this is a small extension. Cheapest; also the weakest,
   because "says something" is not "says why".
2. **A `review_reason` string on the structure schema.** Explicit, greppable, and a schema
   change across 9 records. Bake-free: a top-level structure field is not in
   `generators/mesh_inputs.py`'s resolved-params recipe, so it stales no GLB — **but confirm
   that against the placeholder records, whose `inputs_sha256` is the sha of the whole file.**
   None of the nine is a `recon_*` placeholder today.
3. **Leave it.** The flag is conservative in the direction that matters — it blocks — and an
   unexplained block is not a hazard the way an unexplained claim is.

### K36(a) — nothing compared a shipped derivative to the master it came from · **DONE 2026-08-16 · the site has 75 textures and the repository has none**

**Phase:** kernel (lane 1 side) · **Effort:** S to measure, S to gate · tools and docs only —
no data record, no renderer file, no geometry, no bake

The geometry a visitor downloads reaches them along four links:

    data/  ->  assets/gltf/  ->  assets/web/  ->  site/chicago/4d/assets/web/

Link 1 is gated — `validate.py --stale` recomputes every master's input hash. Link 3 is gated —
`check_published.mjs` asserts the mirror is byte-identical to its source, and exists because
R-BUG3c-b cost three parcels discovering that *"nothing else in this project measures a
published artefact against its own source"*. **Link 2 was gated by nothing at all**, and it is
the link with the moving parts: two `gltf-transform` passes whose own comments in `tools/bake.sh`
record what has already come out of them — *"a bug that collapsed every building to a two-metre
box shipped past a fully green gate — twice"*, and a `--texture-compress ktx2` flag that
*"silently turned every derivative into an uncompressed copy of its master, in every
environment, since this step was written"*. Both were found by a person reading the script.
This reads the bytes.

**FINDING 1 — the town on the site is textured; the town in this repository is not.**
`optimize`'s palette pass folds the named materials of **38 of 334 assets** into one
`PaletteMaterial001` carrying generated PNGs. **75 textures exist in `assets/web/` that exist in
no master**, and the material NAMES they replace — `log`, `chinking`, `board`, `roof`, `dark`,
`interior` — do not reach the browser at all on those 38.

**FINDING 1b — the split is a COUNT and it is exact.** Every master carrying **five or six**
materials is faulted (31 `log_dwelling`, 6 `outbuilding`, 1 `frame_tavern`); every master
carrying **four or fewer** is clean, 296 of 296. Nothing about logs: that is the palette pass's
own documented minimum of five materials, and its output is named `PaletteMaterial001` by the
tool. The consequence is the reason this is a ratchet rather than a curiosity — **275 assets sit
exactly one material short of the threshold**, so an archetype that gains a fifth surface moves
every asset it paints across it. That is what R-W2b does.

**FINDING 2 — R-W2a's material sheet inventories the masters under the words "the shipped
GLBs".** `docs/RESEARCH/materials.md` reasons in its own preamble that *"the source and the
shipped bytes have disagreed in this project before … a sheet that inventories intentions is
worth nothing to a bake"* — and then measures `assets/gltf/**/*.glb`, which is the source side
of exactly that disagreement. Its **"nothing in the town carries a texture of any kind"** is
true of what is baked and false of what is served. Corrected in place, with a §0 note and a
pointer here; **none of its five findings moves**, because all five are about what the
generators paint and that is unaffected. What DOES move is R-W2b's plan: it wires an atlas onto
material names that the publish path deletes on 38 assets, and it now knows that before it
starts rather than after a bake.

**FINDING 3 — 90 assets ship uncompressed, and the only instrument that could notice is a
25 MB budget.** They are exactly the 90 pure-Python placeholders, which
`generators/inferred_placeholder.py` writes byte-identically into both trees; the 244
Blender-baked assets compress **5.29×**. It is 508 KB and **11.4 % of the payload** — not a
problem today, and it is now a printed census line rather than a warning in a nightly log.

**WHAT DOES NOT MOVE, MEASURED RATHER THAN ASSUMED.** Triangle counts are identical across all
334 pairs, so `--simplify false` has held in fact and not only in the script. Node names, the
`structure_id`/`phase_id` extras and mesh names all survive, so the sidecar join key is intact.
`_CONFIDENCE` — how a visitor is told which parts we made up — reaches the site on every asset
carrying it. The world bounding box agrees to at worst **2.63 rungs** of an asset's own extent
(0.107 mm on a 2.7 m shed); the terrain's 82.8 mm is **1.08 rungs** of its 5,020 m box, the same
quantity R-W6 committed as a 76.6 mm lattice, which is the cross-check that the two
measurements are of the same thing.

**WHAT SHIPPED.** `tools/measure_web_derivatives.py`, in `check.sh` at **0.2 s and with no
decoder** — the shipped positions are `EXT_meshopt_compression` payloads this project cannot
decode here, and every claim above is answerable from the glTF JSON chunk instead, because the
spec requires POSITION accessors to carry `min`/`max` and a quantised file carries its
dequantisation in the node's own TRS. **Five absolute assertions** — bijection both ways,
triangle count, node/mesh identity, the attributes `docs/GLB-CONTRACT.md` names, and a bounding
box within **four rungs** (`extent / 65535`) of the master's. The bound is a lattice rather than
a millimetre count because the assets differ in size by three orders of magnitude, and a
building collapsed to a two-metre box is thousands of rungs, not four. **One ratchet** —
`tools/web_derivative_baseline.json`, the 38 — which fails on a new offender, on a banked one
whose loss has grown, AND on a banked one that is now clean and has not been banked as repaired.
TEXCOORD_0 is dropped from 204 masters on the way and that is reported, not gated: the UVs are
unused on an untextured asset and the prune pass is right to drop them.

**All eight failure modes were broken deliberately before the gate was trusted**
(`--self-test`, in memory, against the real tree): a derivative with no master, a master with no
derivative, a simplified mesh, a lost `structure_id`, a lost `_CONFIDENCE`, a collapsed
bounding box, a new material fault, and a repaired one left in the baseline. Each fires; the
clean tree passes.

**WHAT IT DID NOT DO.** It moved no record, no coordinate and no byte of geometry, invented
nothing and upgraded no confidence. No liberty is owed — `docs/LIBERTIES.md` records inventions,
and this parcel measures.

**Verified:** `tools/check.sh` green (with the new step). `SMOKE_VIEWPORT=mobile node
tools/smoke_renderer.mjs --published` green. The desktop half was not run and is not claimed —
it needs ~13 minutes against this harness's 10-minute per-command ceiling (see the run-budget
box at the top of this file). This parcel changes no renderer file and no geometry, so the
scene it would exercise is byte-for-byte the one the last run smoked.

### K36(b) — give the site back the material names it was baked with · **DONE 2026-08-16 · the palette pass was not buying draw calls, it was spending them, and four of the eight anchors were over budget**

**Phase:** kernel (lane 1 side) · **Effort:** S–M · tools, docs and 38 derivative files —
no data record, no renderer file, no master, no bake

**FINDING 1 — the flag's own justification is false here, and it is false by 40 batches.**
The palette pass merges materials *inside one file*, which is a saving when the renderer
batches per file. This one does not. `materialKey()` in `renderers/web/js/buildings.js`
includes `m.map?.uuid`, and a GLTFLoader mints a fresh uuid per loaded texture — so an asset
arriving with its own generated palette map **cannot join any batch, not even another palette
asset's**. Measured on the mirror: the 38 faulted assets shipped as **40 single-building
batches** on top of the town's 16 (40 rather than 38 because `sauganash_hotel` came out with
three `PaletteMaterial`s, its glass and shutters refusing the merge), and the published town
drew **56 batches where R-W5a's committed number is 16**. With the pass off: **56 → 16**, every
one of the 40 folded back into the roughness buckets, `textures` in memory 55 → 41, shader
programs 15 → 12.

**FINDING 2 — the answer to K36(b)'s own "second question" is: R-W5a's numbers were taken on
the SOURCE tree.** Its *"no map of any kind"* is true of what is baked and was never true of
what is served, exactly as K36(a)'s finding 2 was of R-W2a's sheet. That is the same mistake
twice in three days, from two different parcels, and the reason is the same both times — the
instrument was pointed at `assets/gltf/`. `tools/measure_shipped_batches.mjs` is pointed at
the mirror by default and prints which tree it read, so the next parcel cannot make it a third
time. **R-W5a's finding stands** — the collapse from 47 to 16 is real and is what the 40 now
fold back into — but its "16 batches" was never a statement about the site.

**FINDING 3 — and this is the one that matters to a visitor: four of the eight scene anchors
were OVER the 80-call budget on the published site.** A batch holding one building is culled
with that building, so the cost is paid per pose and it is worst where the town is densest.
Measured at 1280×800 through the renderer's own `goTo`, before → after:

| anchor | before | after |
|---|---|---|
| green_tree | **102** | 70 |
| forks | **96** | 68 |
| from_above | **84** | 63 |
| south_water | **82** | 69 |
| lake_market | 71 | 63 |
| sauganash_wing | 68 | 61 |
| first_post_office | 66 | 60 |
| sauganash | 62 | 59 |

**None is over budget now, and the worst falls 102 → 70.** Nothing had ever measured this,
because the smoke reads the counter at the pose it happens to be standing in and
`critic_shots.mjs` reports draw calls per station without asserting on them.

**WHAT IT COST.** The 38 derivatives go **318,540 → 505,932 bytes (+187,392, +58.8 %)** — 197
named materials take more room than 75 generated PNGs — which is **+4.1 %** on a 4.5 MB tree
against a 25 MB budget. `material identity: 334 of 334` now, and the K36(a) ratchet is rebanked
empty; it will fail loudly on the 39th.

**WHAT SHIPPED.** `tools/web_derivatives.sh` — the web-derivative step lifted out of
`tools/bake.sh` **whole and unchanged apart from the flag**, so a Blender-free runner can
regenerate derivatives from the committed masters and MEASURE them. That was the structural
problem behind this parcel: link 2 could be *found* broken by K36(a) but not *repaired* without
a nightly. `BAKE_PALETTE=1` restores the old behaviour for re-measurement; nothing sets it.
Plus `tools/measure_shipped_batches.mjs` (one page load, seconds, no captures) and the
`docs/GLB-CONTRACT.md` bullet that recommended the pass, now struck through with the numbers.

**THE CONTROL, and it is what makes the 38 changes attributable.** Regenerating all 334
derivatives under `BAKE_PALETTE=1` reproduces **243 of 334 byte-for-byte**, md5 for md5,
including **all 38** faulted ones. So the difference in the shipped files is `--palette false`
and not a change of tools. **The other 91 are two findings this parcel did NOT fix and did not
hide** — see K37 and R-W6(b) below; both are real, both are outside a parcel about materials,
and neither is safe to "tidy" without a gate looking at it.

**WHAT IT DID NOT GATE, deliberately and worth someone's parcel.** Finding 3 is measured and
not asserted: nothing fails if an anchor goes back over 80. `measure_shipped_batches.mjs` costs
a page load (~40 s), which is too much for `check.sh` at 14 s, so the right home is the smoke —
it already has a page open and already reads `stats().drawCalls` at whatever pose it is
standing in. **Walking the eight anchors and asserting each is the missing gate**, and it is a
few lines rather than a parcel's worth of work.

**WHAT IT DID NOT DO.** It moved no record, no coordinate, no master and no triangle —
triangle counts are asserted identical across all 334 pairs by the K36(a) gate, which passes.
It invented nothing and upgraded no confidence. No liberty is owed.

**Verified:** `tools/check.sh` green. `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs
--published` green. The desktop half was not run and is not claimed — ~13 minutes against this
harness's 10-minute per-command ceiling (see the run-budget box at the top of this file) — but
the desktop draw-call numbers in finding 3 ARE measured at 1280×800, by
`tools/measure_shipped_batches.mjs`, which is the quantity the desktop half would have been
run for.

### K37 — 90 derivatives were never put through the step that produces them · **DONE 2026-08-16 · the passthrough is right, the rule is not "placeholder", and three assets were going the other way**

**Phase:** kernel · tools, docs and three derivative files — no data record, no renderer
file, no master, no bake, no record moved, no confidence touched.

**FINDING 1 — the answer is the passthrough, and the margin is not close.** The step was
run over all 90 flagged placeholders, which is the measurement the parcel asked for:
**520,700 → 628,028 bytes, +107,328 (+20.6 %)**, and **88 of the 90 grow**. `meshopt`
writes a compression header, a buffer-view table and an index buffer, and on a
sixteen-to-sixty-triangle shed those cost more than the compression saves. K36(a) read
the 90 as an anomaly; K36(b)'s control read them as a non-reproduction; both were true
and **neither was a rule**. Committing them squeezed would have grown the payload to buy
nothing.

**FINDING 2 — and this is the one the parcel did not expect: the class predicate is wrong
in BOTH directions.** "Placeholder ⇒ master copy" fits the tree exactly today —
`kind: placeholder` is 90 of 90 uncompressed, `kind: generated` was 244 of 244
compressed — and it is a coincidence of write order, not a rule:

| | bytes | Δ |
|---|---|---|
| `fort_dearborn_root_house__cellar_1816` | 4,488 → 4,812 | **+324 (+7.2 %)** |
| `lake_house_construction__shell_1835` | 5,620 → 5,860 | **+240 (+4.3 %)** |
| `fort_dearborn_magazine__brick_1816` | 6,236 → 6,460 | **+224 (+3.6 %)** |
| `fort_dearborn_parade__parade_1816` | 5,504 → 4,156 | −1,348 (−24.5 %) |
| `recon_1835_blk_randolph_wells_h2_01` (placeholder) | 8,728 → 7,912 | −816 (−9.3 %) |
| `recon_1835_blk_randolph_clark_h2_02` (placeholder) | 8,712 → 7,904 | −808 (−9.3 %) |

**Three assets that have been through this step on every bake since it was written have
been shipping LARGER than the masters they came from**, and two of the ninety
placeholders compress smaller. Byte size does not predict it either — `parade` is 5,504
bytes and wins, `lake_house_construction` is 5,620 and loses; the discriminator is
triangle count against header overhead, and the honest way to know is to run it. So the
rule is **keep whichever file is smaller, measured per asset**, and it is in
`tools/web_derivatives.sh` rather than in a list of names.

**WHAT MOVED.** Three derivatives, replaced by their masters: **−788 bytes**, and they
now carry exact float positions rather than a quantised lattice. Nothing else. The 90
placeholders are byte-identical to what they were — the parcel's own *"do not fix this by
regenerating them"* held, and the measurement is why.

**THE GATE.** `tools/measure_web_derivatives.py` assertion 6, **absolute, bound zero**: no
derivative may be larger than the master it came from. Its `--self-test` grows a
derivative by one byte and confirms it fires, **and grows an epoch mesh by one byte and
confirms it does not** — an exclusion nobody has watched hold is an exclusion nobody has
watched.

**THE ONE EXCLUSION, by name and with its number.** `water__e1834_harbor_cut.glb` is
1,352 → 2,096 bytes (**+744, +55.0 %**) and the rule would pass it through. It is not
passed through and it is not banked as a fault: the epoch meshes' bit depth is a
*geometric* decision (R-W6 set `EPOCH_QUANT_BITS` against measured drawn-surface error,
and the ground and waterline are what R-BUG3c, R-BUG4, R-M1a and the road-contrast bands
all measure against), and **R-W6(b) is holding both files** pending the owner's word on
regenerating geometry outside a bake. A payload rule does not get to move the water while
that is open. R-W6(b) inherits the question with the number already taken.

**THE OPEN END, stated rather than tidied.** The two placeholders that compress 9.3 %
smaller are left as master copies, because `generators/inferred_placeholder.py` rewrites
**every** non-superseded placeholder into both trees on every run and would silently undo
them — the same write-order coupling that produced this parcel. Fixing it means deciding
whether that generator may seed a provisional derivative at all, which is a generator
change and a separate question. Cost of leaving it: **1,624 bytes**. With the size rule
in place and these three repairs applied, `tools/web_derivatives.sh` reproduces **331 of
334** committed derivatives; the three are those two and `terrain__` (14 bits committed,
16 asked for — R-W6(b)).

**A THIRD WRITER OF `assets/web/`, noticed and not chased.** `tools/publish.sh` copies a
master through whenever it is **newer by mtime** than its derivative. That is a
passthrough nothing decided either, it is invisible to this gate (a copy is never larger
than its master), and on a fresh clone mtimes come from checkout order. Worth a parcel's
attention; it is not this one's.

**AND THE GATE'S OWN SELF-TEST HAD BEEN RED SINCE THE DAY BEFORE.**
`measure_web_derivatives.py --self-test` reported **SELF-TEST FAIL** on a clean `dev` from
K36(b) onward: K36(b) repaired all 38 material faults and rebanked the ratchet empty, so
the mutation *"a banked asset was repaired and not banked"* had nothing to mutate and
printed MISSED. Nothing caught it because `check.sh` ran `--gate` and never `--self-test`.
Both are fixed: an inapplicable mutation now prints `skipped`, and `check.sh` runs the
self-test as its own step. The docstring's *"38 of 334 assets fail this today"* was also
a day stale and now says 334 of 334.

**Verified:** `tools/check.sh` green (including the two new steps).
`SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs --published` green. The desktop half
was not run and is not claimed — ~13 minutes against this harness's 10-minute per-command
ceiling; see the run-budget box at the top of this file. Nothing in this parcel moves a
vertex, a material or a pose, and the three files it does move become *more* geometrically
exact, so the desktop half has no quantity of its own to measure here.

### K37 — the parcel as written, kept for the record

K36(a) reported *"90 assets ship uncompressed, and the only instrument that could notice is a
25 MB budget"*, and attributed it to `generators/inferred_placeholder.py` writing the same
bytes into both trees. K36(b)'s control adds the other half: **running the pipeline's own
web-derivative step over those 90 masters does not reproduce their committed derivatives** —
it produces different, and *larger*, files. On the sample measured, `4,968 → 6,000 bytes`
(**+20.8 %**), because `meshopt` adds a compression header and index buffer to a file too small
to earn either back.

So the count is exact in both directions and the two halves disagree about which is right:
`tools/web_derivatives.sh` says those 90 should be meshopt-compressed and 21 % bigger; the
committed tree says they should be master copies. **Nothing measures the disagreement**, which
is the same shape of gap K36(a) opened — a transformation with a flag in it and no gate.

The decision is small and needs a number, not a preference:

1. measure the payload both ways across all 90 (the sample says the passthrough wins on bytes);
2. decide whether a placeholder derivative is *supposed* to be a master copy — if it is, say so
   in `tools/web_derivatives.sh` and skip them there deliberately, rather than by the accident
   of write order;
3. either way, make `tools/measure_web_derivatives.py` assert the rule, so the 91st cannot
   appear silently.

Watch: **do not "fix" this by regenerating them.** It grows the payload and moves 90 files for
no visitor-visible reason. The fault is that nothing states which behaviour is intended.

### K38 — `assets/web/` has three writers and the gate on it watched one · **DONE 2026-08-16 · two masters copied into the payload, +1,212,760 bytes, and the whole gate printed CHECK PASS**

**Phase:** kernel · `tools/publish.sh`, `tools/web_derivatives.sh`,
`tools/measure_web_derivatives.py`, `tools/check.sh`, docs. No data record, no renderer
file, no master, no GLB moved, no confidence touched.

**FINDING 1 — the fault is real, it was reachable in one command, and every gate this
project owns passed it.** Two compressed masters were `touch`ed and `tools/publish.sh`
run, which is the state the tree reaches whenever `generators/build.py` is run on its
own — the exact case the script's own comment says the passthrough exists for:

| | master | derivative before | shipped after |
|---|---|---|---|
| `fort_dearborn_palisade__picket_1816.glb` | 841,836 | 114,768 | **841,836** |
| `dearborn_street_drawbridge__draw_1834.glb` | 557,196 | 71,504 | **557,196** |

**+1,212,760 bytes into the payload**, written into the *tracked* `assets/web/` and
mirrored to `site/`. Then, on that tree: `measure_web_derivatives.py --gate` **exit 0**,
`check_published.mjs` **exit 0**, and the full `tools/check.sh` printed **CHECK PASS**.

**FINDING 2 — and it could not have been otherwise, which is the general point.** A
master copied over its own derivative carries the master's triangles (assertion 2), node
names and `extras` (3), contract attributes (4), bounding box to **zero** rungs (5) and
material table (7), and a byte count that is *equal* rather than larger (6). K36(a) wrote
those assertions to watch the transformation `assets/gltf/ → assets/web/`. **They watch
the transformation. They cannot see a file that skipped it** — and the whole point of a
gate on a directory is that it holds whatever put the bytes there.

**FINDING 3 — it is not three writers, it is three scripts and FOUR passthrough
branches**, three of which are silent:

| writer | branch | decided? |
|---|---|---|
| `tools/web_derivatives.sh` | the size rule — compressed file is bigger, keep the master (K37) | **yes**, 93 assets |
| `tools/web_derivatives.sh` | `optimize` failed → `cp "$f" "$out"` | no — warns, gated by nothing |
| `tools/web_derivatives.sh` | `gltf-transform` unavailable → copy **all 334** | no — warns, gated by nothing |
| `tools/publish.sh` | master newer by mtime → `cp` | no — announced, gated by nothing |
| `generators/inferred_placeholder.py` | seeds both trees from the master every run (K37) | no — and 90 of the 93 are its output |

The no-tool branch is the widest of them: it takes the payload from **4.54 MB to
20.96 MB**, a 4.6× against a 25 MB budget, and the only instrument that would have
noticed is that budget.

**FINDING 4 — mtime was answering a content question, and it is wrong in BOTH
directions.** On a fresh clone of this repository, **334 of 334 masters are OLDER than
their derivatives** — not because anything is fresh, but because `git checkout` writes in
index order and `assets/gltf/` sorts before `assets/web/`. So the rule fires on any
rebuild that rewrites a master (true positive, wrong response) and is blind on a clean
clone (false negative, no response). It has never once compared a byte.

**WHAT MOVED.** No asset. **Assertion 8**, absolute in both directions against a set
banked by name in `tools/web_derivative_baseline.json`: 93 decided passthroughs, and a
94th fails whichever writer produced it; a banked one that comes back compressed fails
too, and says to re-bank. Its two `--self-test` mutations both fire. **And
`tools/publish.sh` is no longer a writer of `assets/web/`** — it keeps the mtime scan,
moves it above the first write, and **refuses**, naming each stale file and the
`tools/web_derivatives.sh --only <name>` that fixes it. Verified end to end: the same two
`touch`es now stop the publish at exit 1 with the working tree clean.

**THE COST, STATED.** A new placeholder now needs
`measure_web_derivatives.py --write-baseline` in the commit that adds it. That is the
assertion working, not a wart: `generators/inferred_placeholder.py` is the writer of 90
of the 93, and "the generator added one" and "something copied a master through" are the
same bytes. One of them is a decision and it is now written down.

**THE RESIDUAL, and it is K39.** Refusing on mtime is strictly better than copying on
mtime, but it is still mtime: on a fresh clone it will not fire, so a derivative that is
genuinely stale in CONTENT — a master rebuilt with different `_CONFIDENCE` values and the
same geometry, which is the debugging round `publish.sh`'s original comment cites — passes
assertion 2 through 7 and this scan alike. **The honest fix is for the step to record the
master it compressed**, so staleness is a hash comparison and not a timestamp. That is a
change to what a bake commits, so it is a parcel and not a footnote.

**Verified:** `tools/check.sh` green including the self-test step.
`SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs --published` green. The desktop half
was not run and is not claimed — ~13 minutes against this harness's 10-minute per-command
ceiling; see the run-budget box at the top of this file. No vertex, material or pose moves
in this parcel and no committed asset changed a byte, so the desktop half has no quantity
of its own to measure here.

### K38 — the parcel as written, kept for the record

**Phase:** kernel · `tools/publish.sh`, `tools/measure_web_derivatives.py`, docs. No data
record, no renderer file, no master, no confidence.

K37 closed with a paragraph it declined to chase: *"A THIRD WRITER OF `assets/web/`, noticed
and not chased. `tools/publish.sh` copies a master through whenever it is newer by mtime.
That is a passthrough nothing decided either, it is invisible to this gate (a copy is never
larger than its master), and on a fresh clone mtimes come from checkout order."* Its
generalisation is the parcel: **when a directory has more than one writer, the gate on its
contents is a gate on the last writer only.**

The questions, in order:

1. **Can the mtime rule fire, and what does it do when it does?** Not "is it firing today" —
   whether the tree can reach a state where `publish.sh` replaces a compressed derivative
   with an uncompressed master copy, in the *tracked* source tree and in the mirror.
2. **Which of the eight assertions in `tools/measure_web_derivatives.py` sees it?** A master
   copied over its own derivative has the master's triangles, node identity, attributes,
   bounding box, materials and byte count. Answer it by measurement, not by reading.
3. **What does the passthrough cost if it fires everywhere?** The census already prints the
   payload both ways; put the number in the parcel rather than leaving it as a ratio.
4. **Then decide the writer, not only the gate.** `publish.sh`'s copy exists for a real
   failure (run `generators/build.py` alone and `assets/web/` is stale), but this project's
   own rule for that case is *"a stale committed GLB is a check failure, not a warning"*
   (AGENTS.md), and `measure_web_derivatives.py --gate` already answers staleness from
   CONTENT. A silent `cp` and a content gate cannot both be the answer.

Watch: the 93 legitimate passthroughs K37 decided are legitimate — the gate must tell a
decided passthrough from an accidental one, and a bound of zero would be wrong.

### K39 — the derivative does not record the master it was made from · **DONE 2026-08-16 — it does now, and the control that was supposed to verify it does not exist: 14 of 20 shipped derivatives cannot be produced by this repository's own step**

**Phase:** kernel · `tools/web_derivatives.sh`, `tools/measure_web_derivatives.py`,
`tools/publish.sh`, `assets/manifest.web.json` (new), `assets/LICENSES.md`, docs. No data
record, no renderer file, no master, no confidence, and **no committed asset changed a
byte**.

**THE COUPLING, DECIDED BEFORE THE FILE WAS WRITTEN** — which is what the parcel asked
for, because it is the part that can turn a nightly into a red dev gate for everyone
else. **The STEP writes the record, on every run, and a bake carries the diff.**

- The record's lifecycle is the derivative's: same producer, same run, same commit.
  `tools/bake.sh`'s only web-derivative call is `tools/web_derivatives.sh`, and the bake
  workflow commits `chicago/4d` whole — so a nightly that regenerates geometry rewrites
  the record in the same breath, and **no workflow change is needed** (which matters:
  workflow files are outside a steward run's scope).
- Hand-banking was the alternative and it is the failure this project has now measured
  twice — `build.json`, written once by hand and two days stale on the site; the
  665-roof crosswalk, authored and wrong by a third of the programme. A record a person
  maintains describes the tree as it was when they last remembered.
- **It is not in `tools/web_derivative_baseline.json`**, which is K39's own Watch. That
  file is a record of FAULTS a person banks deliberately with `--write-baseline`; a map
  that changes on every bake has the opposite lifecycle and would train everyone to run
  `--write-baseline` without reading it. It went beside **`assets/manifest.json`**
  instead, because the two are the two links of one chain: the manifest records
  data → master and is written by the Blender build, `manifest.web.json` records
  master → derivative and is written by the step after it.

**FINDING 1 — one hash, and the assertion is absolute in both directions.** 334 of 334
derivatives now record the master they were made from. A derivative whose recorded hash
is not its master's hash today fails; a derivative with no entry fails (that is a file no
step here claims to have produced); an entry naming a derivative that is not there fails.
**Exercised against the real tree rather than only in memory**: appending one byte to
`cobweb_castle__log_1820.glb`'s master makes `--gate` fail by name — *"made from a master
with sha256 275bab93cbe7… and the master in the tree today is d6e5c694decd…"* — and makes
`tools/publish.sh` **refuse before it writes anything**, working tree clean afterwards.
Two new `--self-test` mutations, both caught, and they are the mutations assertions 1-8
survive: a master rebuilt into the same geometry moves no triangle, no node, no
attribute, no bounding box, no material and no byte count.

**There is deliberately no way to rewrite the record without regenerating the bytes.** No
`--write-record` on the gate, no reseed flag on the step. The remedy for every failure
assertion 9 can produce is `tools/web_derivatives.sh --only <name>`. A hash map you can
rewrite to make a gate green is a hash map that says nothing, and this project already
keeps one file whose whole discipline is that it may only be rewritten to record a
repair.

**FINDING 2, AND IT IS THE ONE WORTH READING — the record's own verification control
does not exist.** The obvious way to prove a seeded hash is to regenerate the derivative
and compare bytes, and `tools/web_derivatives.sh`'s header says that works: *"it
reproduces 331 of 334."* **It does not.** Measured on a 20-asset spread sample of the
compressed derivatives:

| | reproduced by `tools/web_derivatives.sh` | did not |
|---|---|---|
| 20-asset spread sample | **6** | **14** |

And the 14 are not noise — **every one of them reproduces BYTE FOR BYTE under
`BAKE_PALETTE=1`** (checked on three: `bates_auction_room`, `jh_kinzie_forwarding_store`,
`recon_1835_west_022`). The cause is a side effect nobody had measured: **`optimize`'s
palette pass welds**, and K36(b) turned that pass off for draw-call reasons that stand,
then regenerated only the **38** assets that carried the material fault. The other
derivatives still carry palette-era bytes.

The size of it needs no `npx` at all — a welded derivative carries fewer vertices than
its master, and that is readable from the glTF JSON:

| compressed derivatives (334 − 93 passthroughs) | 241 |
|---|---|
| **fewer vertices than their master** — only the palette-era step produces this | **195** |
| exactly the master's vertex count — today's step, or nothing to weld | 46 |
| vertices the welded set drops in total | 10,513 |

195 is a **lower bound**: an asset with no duplicate vertices to weld looks identical
under both steps, which is exactly why 6 of the sample reproduced.

**Nothing is wrong with the bytes on the site.** A weld is lossless, the triangles are
equal, and assertions 1-9 are green on all 195. What is wrong is the claim: the sentence
the whole no-Blender repair strategy rests on — *this runner can regenerate what the
nightly ships* — is true for 46 of 241 and false for 195. And the consequence is
scheduled: **the next nightly bake rewrites all 195 as unwelded files**, +2,756 bytes
across the 14 sampled (+197 each), arriving in a bake PR as binary noise nothing
predicted.

**FINDING 3 — and it is why assertion 9 stops where it does.** The hash names the
MASTER, not the STEP. All 195 palette-era derivatives record the right master and are
correctly green, because their master *is* the master beside them. Answering "which step
made this" is a second field with a 195-file repair behind it, and it is K40's, not this
parcel's — K39's own effort line says one field.

**THE SEED, STATED PLAINLY.** The record was seeded in this commit rather than produced
by a full run of the step, because a full run regenerates all 334 derivatives and 195 of
them would change bytes — that is K40's repair and it needs a smoke half this runner
cannot finish. One entry (`cobweb_castle__log_1820.glb`) was written by the step itself,
and its derivative came back **md5-identical**; the other 333 were hashed from the
masters in the tree and merged into the same structure. **What the seed rests on** is
assertions 1-8: each derivative carries this master's triangles, node identity and
`extras`, contract attributes, bounding box to under 2.63 rungs, and material table, and
93 of them are byte-identical to it. **What it does not claim** is that the shipped bytes
were produced by today's step — finding 2 measured that at least 195 of them were not.

**Verified:** `tools/check.sh` green, including the self-test step and the licence check
(`assets/manifest.web.json` is accounted for in `assets/LICENSES.md`, beside
`manifest.json`, as a build record rather than an asset).
`SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs --published` green. The desktop half
was not run and is not claimed — ~13 minutes against this harness's 10-minute
per-command ceiling; see the run-budget box at the top of this file. No vertex, material
or pose moves in this parcel and no committed asset changed a byte.

### K40 — 195 shipped derivatives were made by a step this repository no longer has · **DONE 2026-08-16 — it is 189, this runner reproduces the nightly's bytes on every one of them, and the rewrite is not scheduled: it is sitting in an open bake PR**

**Read `docs/RESEARCH/web-reproduction.md` before quoting any reproduction number, and stop
quoting 195.** Four questions were asked and all four are answered from a control that runs
`tools/web_derivatives.sh` itself over all 334 masters — chunked into four 3 min 21 s passes
to fit the harness's ten-minute per-command ceiling, which is why the loop is now a tool
(`tools/measure_web_reproduction.py`) rather than something each parcel reinvents.

**FINDING 1 — the exact count, and the failures decompose with nothing left over.**
**142 of 334** reproduce. Of the 192 that do not, **189 come back BYTE FOR BYTE under
`BAKE_PALETTE=1`** — the palette-era set, counted rather than inferred — and the remaining
**three were already owned by name**: the two K37 placeholders that compress smaller
(`recon_1835_blk_randolph_clark_h2_02`, `…_wells_h2_01`) and `terrain__e1834_harbor_cut.glb`,
committed at 14 bits against a 16-bit ask, which is R-W6(b) in one file.

**FINDING 2, AND IT IS THE ONE THAT MOVES THE PARCEL — the rewrite is not scheduled, it is
OPEN, and this runner's control produces the nightly's exact bytes.** Bake PR **#175**
(opened 07:34 UTC, 2026-08-16) rewrites **280 derivatives**, and all 192 non-reproducing
files are in it. On the 189 the nightly's bytes and this runner's are **md5-identical, 189 of
189**. So the claim the whole no-Blender repair strategy rests on — *this runner can
regenerate what the nightly ships* — is **true**, with a control behind it for the first
time. What was wrong was never the extraction; it was that a step change had been carried
through 38 files and not 334. The bake's 280 decompose exactly: **189** palette-era + **90**
placeholder masters upgraded to canonical archetype bakes (5 KB boxes → 25–83 KB buildings)
+ **1** terrain at 16 bits. A binary diff nobody could review now has an arithmetic.

**FINDING 3 — K39's vertex signature is REFUTED as an identifier.** It counted 195 files
carrying fewer vertices than their masters and reasoned that only the palette-era step
produces that. Against the exact set it is wrong in **both** directions: 189 shared, **six
welded files that today's step reproduces exactly** (2–4 vertices each — `optimize` dedups
without the palette pass) and three failures with no weld. The tool prints the proxy beside
the exact answer so it cannot be rounded off again, and **no gate is built on the vertex
count**.

**THE PRICE.** +48,836 bytes over the 189 (mean **+258**, and **all 189 grow**; worst
`fort_dearborn_garrison_garden__fence_1816` at +7,240), **+48,328** net across the tree once
K37's two placeholders' −1,624 is counted. That is +1.01 % of 4,764,664 bytes and **0.18 % of
the 25 MB budget**. K39's sample said +197 from 14 files and 30 % reproduction; the true
figures are +258 and 42.5 %. **10,491** vertices are merged across the set.

**DECISION 1 — who moves the 189: nobody here.** The parcel expected a choice between
regenerating 195 binary files on a runner that cannot finish the desktop smoke, and letting a
nightly land them unreviewable. Measuring first dissolved the first option — an open PR
already holds those exact bytes — and answered the second with the decomposition above. This
parcel therefore **moves no asset and merges no bake**: #175 and #164 carry **no status checks
at all**, because a bot-opened PR does not trigger the dev gate, and running that gate against
them is the janitor's job and the owner's call.

**DECISION 2 — should the record name the STEP as well as the master? NO,** and the
measurement is the reason. A flag-set string is prose, and prose can be edited to turn a red
gate green — the one property K39 deliberately denied the record. A hash of the script is not
editable and is wrong measurably: the four commits that have changed
`tools/web_derivatives.sh` since it was extracted moved **38, 3, 0 and 0** derivatives, so a
script hash would have invalidated all 334 entries four times, **twice on a commit that moved
no byte**, and the file is mostly comment — every parcel writing down what it learned would go
red. What the failure needed was a rule, and it is in the step's header now: **a change here
that moves any derivative's bytes regenerates all 334, not the ones that visibly broke.** It
is deliberately not a gate — the only exact test is the 13-minute control, `tools/check.sh` is
90 seconds on purpose, and the one cheap candidate is the signature finding 3 refutes.

**Verified:** `tools/check.sh` green; `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs
--published` green. The desktop half was not run and is not claimed — ~13 minutes against a
10-minute per-command ceiling; see the run-budget box at the top of this file. **No asset,
record, parameter or renderer file changed in this parcel** — it is a measurement, two
decisions, a tool and the documents.

**Open, and named rather than left implicit:** #175 rewrites `assets/web/` and this parcel did
not gate it. When it or a successor lands, `tools/measure_web_reproduction.py --report` should
read **334 of 334**, and the two K37 placeholders are the ones to watch — today's step
compresses them, so `tools/web_derivative_baseline.json`'s passthrough list moves 93 → 91 and
assertion 8 asks to be re-banked. That is a repair to record deliberately, not a surprise.

### K40 — the parcel as written, kept for the record

K39 needed a reproduction control and could not get one. `tools/web_derivatives.sh` does
not produce the bytes on the site: **6 of 20 sampled derivatives reproduce, 14 do not,
and all 14 come back byte-for-byte with `BAKE_PALETTE=1`.** K36(b) turned the palette
pass off — correctly, it was costing draw calls at four of eight scene anchors — and
regenerated only the 38 assets whose material identity it had broken. The pass was also
**welding**, which nothing had measured, so **195 of the 241 compressed derivatives carry
fewer vertices than their masters** (10,513 vertices in total) and are the output of a
step that no longer exists here.

Nothing on the site is wrong today. The problem is that the repair is *scheduled without
a decision*: the next nightly bake regenerates all 195 unwelded, and that lands as a
195-file binary diff in a bake PR with no number attached to it.

The questions, in order:

1. **Count it exactly.** The 195 is a lower bound from the vertex signature; a full
   `tools/web_derivatives.sh --out <tmp>` control over 334 masters gives the exact set.
   It costs about 17 minutes of `npx` at ~3 s per asset, so it must be **chunked** under
   this harness's 10-minute per-command ceiling — that constraint is the parcel's shape,
   not an aside.
2. **Price it.** +197 bytes per asset on the 14 sampled, against a 4.5 MB payload and a
   25 MB budget. Take the real total, both ways, and quote it.
3. **Decide who moves them, and say why.** Regenerating them here is one command and no
   Blender, but it moves 195 binary files and the acceptance is the *desktop* smoke half
   — which this harness cannot finish (see the run-budget box). Letting the nightly do it
   costs nothing and buys a bake PR nobody can review. Both are defensible; picking
   silently is not.
4. **Then ask whether the record should name the STEP.** K39 deliberately recorded the
   master and not the step, and finding 3 says why: the 195 record the right master and
   are correctly green. A second field — the tool version and the flag set — would have
   caught this on the day K36(b) landed. It would also go stale on every flag change, so
   it is a lifecycle question, not a hashing one.

Watch: **do not "fix" this by turning the palette pass back on.** K36(b) measured what it
costs — 56 draw calls against R-W5a's 16, four of eight anchors over the 80 budget, worst
102 at the Green Tree — and that measurement stands. If the weld is worth having, it is
worth having *on its own*: `gltf-transform` ships a `weld` command, and a pass this
project adds deliberately is a pass it can measure. Do not add one without a number.

### K39 — the parcel as written, kept for the record

K38 took `tools/publish.sh` out of the business of writing `assets/web/` and left its
detector in place, refusing instead of copying. **The detector is still an mtime
comparison, and K38 measured that mtime cannot answer this question**: on a fresh clone
334 of 334 masters are older than their derivatives by `git checkout`'s own write order,
so the scan is silent on exactly the tree a steward run starts from.

The gap that survives is narrow and named. `measure_web_derivatives.py` asserts triangles,
node identity, contract attributes, a bounding box within four rungs and material
identity — so a master rebuilt into a *different building* fails. A master rebuilt into
the **same** geometry with different `_CONFIDENCE` values does not, and that is the
failure `publish.sh`'s original comment was written about: *"a rebuilt building kept
rendering with its old confidence values."* `_CONFIDENCE` is how a visitor is told which
parts we made up, so a stale one is a provenance fault wearing a rendering fault's
clothes.

The fix is one hash. `tools/web_derivatives.sh` knows exactly which master it compressed;
nothing writes that down.

1. Have the step record `name → sha256(master)` as it produces each derivative — as a
   committed sidecar it writes itself, so the record travels with the artefact and the
   step stays the only thing that authors it.
2. Assert it: a derivative whose recorded master hash is not the master's hash today is
   stale, absolutely, whatever the timestamps say. That subsumes K38's mtime scan and
   `publish.sh` can then simply run the gate.
3. **Decide the coupling first, because it is the real question.** The record changes on
   every bake, so a nightly that regenerates geometry and does not rewrite it turns the
   dev gate red for everything else. Either the step rewrites it (and the bake PR carries
   the diff, which is honest) or it is banked by hand (and it will go stale). Pick, and
   say why, before writing the file.

Watch: do **not** fold this into `tools/web_derivative_baseline.json`. That file is a
record of FAULTS and repairs, deliberately rewritten only by a person banking a decision;
a hash map that changes on every bake has the opposite lifecycle and would train everyone
to run `--write-baseline` without reading it.

### K42 — the read-set for the flora and fauna layers · **DONE 2026-08-16 — 58 of the two layers' 100 figures reach nothing, and one whole layer has no reader at all: no file under `renderers/` opens `data/fauna`, and `publish.sh` never puts it on the site**

**Read this box before quoting any flora or fauna read number.** K41's residual, taken at
face value: the buildings and the ground each declare which of their figures reaches a
vertex, `tools/validate.py` turns each declaration into a rule, and the two layers with 293
records between them had never been asked the question.

**FINDING 1 — the count, and it is nearly evenly split.** **100 figures** across five record
kinds (flora zone / manifest / palette, fauna zone / manifest), after identity, file routing,
provenance and prose keys are stripped the way `compile_scene.ground_fields` strips them on
the ground side. **38 reach a vertex or a pixel**, 2 are read only to be shown as text, 2 are
read only into a diagnostic or a gate accessor, and **58 reach nothing at all**. One of the
38 is worth naming because it is provenance everywhere else in this project and a colour
here: `species[].confidence`, which the confidence view tints each plant by.

**FINDING 2 — `data/fauna` has no reader, and three separate documents imply it does.** **139
species records across 10 habitat zones**, 30 figures, **zero reads** — and the strong form of
that is not a field scan but a directory one: **no file under `renderers/` names the layer**,
and `tools/publish.sh` does not copy it, so `site/chicago/4d/data/` has no `fauna/` in it and a
browser has never been offered the layer. Against that: `data/scenes/1835.json` lists `fauna`
in its `layers`; `docs/LIBERTIES.md` L2 describes the July soundscape as shipped; and
`tools/validate.py` demanded eight vocabulary blocks on the ground that *"a renderer reads this
block"*. **This is not an argument for deleting anything** — AGENTS.md says the dataset is the
durable artefact and renderers are disposable, so a sourced July soundscape nothing draws is
banked work. The fault is that nothing said so, and a reader of any of those three documents
would conclude the town has animals in it.

**FINDING 3 — four unread things in the flora, one of which is a false sentence in the data.**
(a) `data/flora/index.json`'s own `_doc` said the `ground_*` and `bare_soil_fraction` copies
were denormalised into the manifest *"so the ground shader can work from one fetch"* — and
**`terrain.js` never opens `data/flora`**; the sward's `bare_soil_fraction` is read off the
zone record, by the smoke's cover gate, not by the ground. That sentence is rewritten to what
is true. (b) `plantable_in_scene` is read by nothing in either place it is written: zones 7–9
match nothing because their extents do not meet the modelled ground, not because of the flag.
(c) **The palettes are 12 unread figures each, 108 in all** — `wind.{speed_mps,sway_deg,gust,
wave_m}`, `lod.{near_m,mid_m,far_m}`, `budget.instances_{near,mid}` and `ground.{rgb,dry_rgb,
wet_rgb}` — because `flora.js` tuned its own `TUNE` constants and reads only `greens` and
`dry_accent`. (d) **31 flowering species record a July `fruit` nothing draws**, plus
`cover.standing_water_fraction` on all ten zones and `cover.litter_fraction` on one.

**FINDING 4 — K41's residual, answered, and the plants are on the wrong side of it.** All
**202** unresolved-source citations in `data/flora` sit on a record node carrying at least one
figure that reaches a vertex (a node's own figures stop at the next node that cites its own
sources, so a zone does not inherit its species' geometry). All **30** in `data/fauna` sit on
a layer nothing draws. Under K41's wide reading the flora layer is the worst-affected
population in the project — worse proportionally than the 49 building attributes — and under
the narrow reading it is untouched. **Same reading, same owner, same three routes as K41.**

**WHAT SHIPPED.** `tools/measure_layer_reads.py` — census, `--gate`, `--self-test`,
`--update` — and `tools/layer_reads_baseline.json`, 58 entries banked by layer, record kind
and field path with the record count on each. Five assertions: **1** every figure present is
classified; **2** every read declaration names an expression still in the renderer; **3**
absolute in two halves — a layer with no declared reads may not be opened by any renderer
source and a layer with them must be, then per figure a reverse property scan; **4** a new
unread figure fails; **5** absolute, a banked entry that has left the data fails until it is
un-banked in the commit that wired it up. All exercised in memory by `--self-test`, which
`tools/check.sh` runs.

**THE TWO METHOD NOTES worth carrying to the next parcel of this shape.** (a) **The map is
Python and the reader is JavaScript**, which is `terrain_inputs.py`'s problem in a new
costume — there the reason not to co-locate was the ground's hash, here it is a 26-minute
smoke behind every renderer edit. Both buy the same thing the same way: **the declaration is
scanned against the source it describes**. (b) **Strip the comments before scanning.**
`flora.js` discusses `bare_soil_fraction: 0.45` in a comment three lines above the line that
reads it, and `check_sidecar_contract` reported *itself* on its first run for exactly this.
The stripper is exercised in the self-test in both directions, including a string that looks
like a comment.

**THE LIMIT, stated rather than discovered later.** A text scan cannot attribute a property
access to one of two record kinds that both carry that field name — `bare_soil_fraction` is
read off a zone and copied into the manifest — so **2 entries are exempted from the per-field
scan and listed by name in the census** as stated rather than proven. The fauna half needs no
exemption because the layer rule is absolute. The durable fix is the same one this project
keeps arriving at from other directions: a renderer that declares its own read-set in a form
the gate can import.

**WHAT THIS PARCEL DOES NOT DECIDE, and the routes.** Whether an unread figure should be
deleted, wired up or declared is three different answers. *The fauna layer*: (1) leave it and
say so — the honest option, and it needs `data/scenes/1835.json`'s `layers` list and
`docs/LIBERTIES.md` L2 to stop implying otherwise, which is a claim about the scene and the
owner's; (2) give it a reader, which is a renderer parcel of real size and no bake; (3) do
nothing, which is where the last three days left it. *The palettes*: their unread blocks are
render tuning the renderer has re-tuned, so either the palette record stops carrying them or
`flora.js` reads them — a `TUNE`-versus-record question with no evidence in it, and cheap.
*The `fruit` on 31 species*: it is the one entry here with a research half, because a July
fruit is a visible thing this scene omits and `docs/LIBERTIES.md` does not record the
omission.

**Verified:** `tools/check.sh` green with the two new steps; `SMOKE_VIEWPORT=mobile node
tools/smoke_renderer.mjs --published` green. The desktop half was not run and is not claimed —
~13 minutes against a 10-minute per-command ceiling; see the run-budget box at the top of this
file. **No record moved and no asset changed**: the only data edit is one `_doc` sentence in
`data/flora/index.json` that was false, and two `tools/validate.py` error messages that said
a renderer reads a block no renderer reads.

### K45(a) — the repair K44 named draws nothing, because `TIMBER_ZONES` is a species table and the placer picks from a hand-written list · **DONE 2026-08-16 — one line of prescribed repair refuted three ways, and the American sycamore has been standing in the same hole all along**

**Read this box before quoting any planting-reach number.** K44 found four researched
lakeshore trees handed to no reader and wrote the repair down in `docs/LIBERTIES.md`
**L113** and in this file: *"Add `z08_lakeshore` to `TIMBER_ZONES` and the four dune
records are drawn by the archetypes that already exist."* This parcel is the run-budget
box's rule applied to that sentence — **land the measurement before spending a smoke on
the fix** — and the measurement refuses the fix.

**FINDING 1 — `TIMBER_ZONES` places nothing; it is a SPECIES table, and the proof is
already committed.** `trees.js` opens those four zone files to build one render spec per
species — height, crown width, July foliage, density, confidence — and then throws the
zone away. A zone's `extent` is read by `flora.js` and **never** by `trees.js`. Placement
is `COMMUNITIES`: four hand-written mixes chosen by heightfield rules (distance to water,
which land division, a generated relief field), and a stem's species is
`pick(mix, rnd())`. Nobody has to take that on argument, because the repo contains the
control: **`z07_bur_oak_savanna`'s declared extent box is E −2600..−600, N −6400..−4400** —
4.4 km outside the modelled field in the nearest direction, so no point in the scene is
ever in that zone — **and its two oaks are drawn anyway**, out of the `ridge_oak` mix. A
zone in the list is a zone whose species parameters are read. It is not a zone that is
planted.

**FINDING 2 — so the prescribed repair draws exactly zero stems, and the gate now says so
in memory.** Applied to the real tree by `--self-test`, adding `z08_lakeshore` to
`TIMBER_ZONES` does this and nothing else: `populus_deltoides` and `salix_interior`
**already** have a spec from `z05_riverbank_timber`, and `loadTimberZones` is first-zone-
wins (`if (specs[sp.id]) continue`) with the new zone appended last, so z05's gallery
cottonwood keeps the entry and the dune form never lands — which is the right outcome and
also not a repair. The other two, **`populus_tremuloides` and `populus_balsamifera`, are in
no community mix**, so `pick()` can never return them: they gain a `specs` entry nothing
can select. Four records in, zero stems out. The count is asserted rather than described —
the self-test prints the two species the repair adds to the unselectable bank.

**FINDING 3 — and the hole was already occupied.** Ask the question of the town as it
stands and one species falls into it: **`platanus_occidentalis`, the American sycamore** —
routed by `z05_riverbank_timber`, role `tree`, form `tree_gallery` which has an archetype,
`density_per_ha` **[1, 3]** written down, graded `inferred` off McBride & Bowles, its July
appearance recorded as *"Rare, at its northern edge; white mottled bark flashing on the
upper limbs"* — **and in none of the four mixes.** It is drawn nowhere and always has
been. **K44 counted it as reached**, correctly by its own definition: the record is handed
to `trees.js`. It is the same loss one level in, and invisible from K44 for the same reason
K44 was invisible from K42 — *"this record is received"* and *"this record can be selected"*
are different sentences, and only the first one had a gate.

**FINDING 4 — the timber layer has never visited three quarters of the modelled ground.**
The woody planting loop sweeps a fixed square, `half = 320 - step`, so **E/N −316..+316 m**
at full detail. S2e carried the heightfield east to **E −320..+1700, N −400..+400**.
Measured against the planter's own dry floor (`water_surface_m + TREE_DRY_MARGIN_M`, 0.20 m):
**192,844 heightfield nodes stand above it, 52,163 of them inside the square — 27.05 % —
and 140,681 outside, which is 87.9 ha.** `flora.js`'s lattice is built around `camE`/`camN`
and follows the visitor over all of it, so the sward reaches ground the timber cannot. And
`z08_lakeshore`'s own box starts at E +1400, **1,084 m east of the planter's east edge**:
even a repair that fixed the mix would still plant nothing there.

**WHAT THIS MEANS FOR THE PARCEL, stated as a plan rather than left implied.** K45's first
repair is not one line, it is two changes and one research question: a **dune community**
in `COMMUNITIES` with a placement rule (what selects it — substrate? distance to the lake?
the zone extent, which would make `trees.js` read an extent for the first time) and the
sourced densities the records already carry (3–15, 2–8, 2–8 per ha), **and** the planting
loop's square carried east over the ground that community stands on. Both carry the smoke,
and the second one changes how much ground the loop sweeps, which is a cost question this
box does not answer. That is **K45(b)**.

**WHAT SHIPPED.** `tools/measure_planting_reach.py` — census, `--gate`, `--self-test`,
`--update` — and `tools/planting_reach_baseline.json`. Four assertions: **1** the
declarations are still in the renderer, and `trees.js` still has exactly the **2**
`addTree` call sites this gate accounts for, so a third selection path is a failure rather
than a species wrongly called unselectable; **2** the planter's domain, banked exactly and
allowed to GROW and not shrink — the number K45(b) has to move; **3** the routed,
archetyped, unselectable species, exact both ways, which is the assertion that refuses
L113's repair; **4** every `TIMBER_ZONE` that declares an extent box with whether that box
meets the planter, so routing-is-not-placement is held in a file instead of a paragraph.
Every declaration is **scanned out of the renderer**, and a scanner that cannot find its
own is a raise rather than an empty set.

**THE SCANNER BUG THIS FILE FOUND IN ITSELF, recorded because it is the failure mode the
house style exists to prevent.** The first version read a community's mix with
`\[(.*?)\],` and the mixes are written several lines long with a `],` closing each species
pair, so the non-greedy match stopped two entries in — and the census confidently reported
**nine** unselectable species, six of which are drawn in every frame. A bracket-balanced
reader replaced it and a self-test check now asserts that a multi-line mix is read to its
END. **A scan that under-reads looks exactly like a finding**, which is why every scanner
here has to be able to say no as well as yes.

**THE LIMIT.** `standsDry` is one of several tests a stem must pass — the traced water
mask, the buildings, the community classifier (which returns null over most of the box)
and the per-hectare roll all remove more. The land census is therefore an **upper bound on
ground the loop could visit**, not a count of stems; the stems actually built are
`trees.stats` and belong to the smoke. The tool's docstring says so.

**Verified:** `tools/check.sh` green with the two new steps; `SMOKE_VIEWPORT=mobile node
tools/smoke_renderer.mjs --published` green. The desktop half was not run and is not
claimed — ~13 minutes against a 10-minute per-command ceiling; see the run-budget box at
the top of this file. **No record, asset, parameter or renderer file changed** — this
parcel is a measurement, a bank, two gate steps, a correction to L113 and a changelog
entry. Nothing a visitor sees moved, which is the honest outcome when the repair on the
table would have moved nothing either.

### K45(b) — the lakeshore repair as it actually is · **SPENT 2026-08-17 — all three changes have landed · opened 2026-08-16 by K45(a)**

> **NOT A PICK — there is nothing left in it.** Change three (the sycamore) landed as K45(b1),
> change two (the planter's square) as K45(b2), and change one (the dune community) as
> K45(b4) below. Its successors are **K45(b3)**, the detail control, and the willow scrub
> K45(b4) leaves unplanted.

K45(a) refuted the one-line version. What is left is two changes and one research question, and
its numbers are all measured and committed — take them, do not re-derive them.

**Change one: a community that can stand on dune sand.** `COMMUNITIES` has four mixes and the
classifier that chooses between them (`communityAt`) asks distance-to-water, which land division,
and a generated relief field. On the beach the lake IS water, so bank distance is small and the
classifier would return `gallery` — silver maple and elm on open sand, which is worse than nothing.
A `dune` mix needs its own branch and the branch needs a rule: the honest candidates are
**substrate** (the zone record's own `cover`/`ground`), **the zone extent** (which would make
`trees.js` read an extent for the first time in its life, and is a real design change, not a
line), or **distance to the lake specifically** rather than to any water. The densities are
already sourced — `populus_deltoides` [3, 15]/ha in the dune form, `populus_tremuloides` and
`populus_balsamifera` [2, 8] each, all three graded `attested` off the MNFI open-dune survey and
Cowles 1901. **Do not invent a fourth species to round the mix out.**

**Change two: the planting loop's square carried east.** `const half = 320 - step` sweeps
E/N −316..+316 while the field runs E −320..+1700, N −400..+400 — **87.9 ha, 72.95 % of the ground
above the loop's own dry floor, is outside it**. The cost is the open question this parcel has to
answer with a number rather than a guess: the loop is O(cells) and the field is 4× the square, so
the sweep gets ~4× longer at the same step, on top of whatever the new stems cost in triangles and
draw calls. `stats.drawCalls` and the ≤ 80-per-station budget R-W5a and K36(b) both measure are
the gate. **Measure it before widening it**: a `SMOKE_VIEWPORT=desktop` run cannot self-verify on
this runner, so if the widened sweep needs the desktop half, split again and say so.

**And the third thing, which is separable and much smaller.** The **American sycamore** is one mix
entry — `['platanus_occidentalis', 1]` in `gallery`, weighted at the [1, 3]/ha its own record
carries — and it is drawn nowhere today. It has nothing to do with the lakeshore and could ship on
its own, ahead of either change above, as the cheapest way to move `tools/measure_planting_reach.py`'s
unselectable bank from one to zero. It changes the frame, so it carries the smoke; that is the whole
of its cost.

**The gate will demand the bank move.** `tools/measure_planting_reach.py` holds the planter's reach
(may grow, may not shrink) and the unselectable population (exact both ways), so each of the three
has to `--update` in the commit that makes it. `docs/LIBERTIES.md` **L114** is the entry to move to
**Resolved**, in halves, as they land.

**THE THIRD THING IS SPENT — 2026-08-16, K45(b1) — and the line above got its weight wrong twice.**
See K45(b1) below before writing any mix entry. Changes one and two stand exactly as written.

**CHANGE TWO IS SPENT — 2026-08-16, K45(b2) — and it answered change one's hardest question on the
way.** The planter sweeps the field; the cost is measured; and the classifier's beach problem is
solved for now by an east limit rather than by a dune mix. **Change one is what is left of K45(b)
and it is now the only thing standing between `z08_lakeshore`'s three dune poplars and the
ground** — read K45(b2) below before writing its placement rule, because the branch it needs is
narrower than this box says: `communityAt` already refuses everything east of State Street, so a
`dune` mix does not have to out-argue the bank-distance test, it has to be reached at all.

### K45(b2) — the planter sweeps the field, and the timber gets the east end its own source gives it · **DONE 2026-08-16 — the square was 13 m from right on one bank and 510 m from right on the other**

**SEEN.** 147 stems stand east of the old square's edge where **one** did; a screenshot taken
looking east from anywhere on the north bank differs. It also holds no exemption and needs none.

**Read this box before quoting a planting-reach number or moving a woody east limit.**

**WHAT SHIPPED, one: the loop.** `const half = 320 - step` is gone. The planting loop sweeps the
heightfield's own extent inset by one planting step — **E −316..+1696, N −396..+396** — so the
reach goes from **52,163 to 189,700 of the field's 192,844 dry nodes, 27.05 % → 98.37 %**, and the
87.9 ha it had never offered a stem to is **2.0 ha of one-step rim**. The bounds are derived from
the heightfield rather than written down, which is the stronger form: a square written as a number
can be right by accident, and this one was.

**WHAT SHIPPED, two: the east end, which the square used to supply by accident.** Ground the loop
reaches is not ground a wood may stand on, and the classifier had no eastern answer at all —
`bank <= width` would have read the lake as a river and planted silver maple on the beach.
Andreas ends both divisions in the sentence `z05_riverbank_timber` is already built from: the
South Side belt runs *"east as far as Wells Street"*, and the North Side's timber excepts *"the
sandy hills near the lake"*. `communityAt` now carries one limit per division, **read at load out
of `data/streets/1835.json`** — Wells at **E +329.3**, State at **E +825.8** — so a limit and the
street it cites cannot drift apart. **64,385 nodes, 40.2 ha, are swept and refused**, which is a
stated omission where an unstated one stood.

**FINDING 1 — `z05_riverbank_timber`'s own note put Wells Street 440 m east of where it is, and
the error was load-bearing.** The note read *"Wells Street is about 440 m east of this box's east
edge, so the whole South Division frontage inside the box is inside that belt."* The committed
centreline runs **E +328.1 to +330.5**. That is **nine metres** east of the 640 m box's edge, not
440. The conclusion survived — but on nine metres of margin, not four hundred, and a belt read as
running 440 m past the box would have licensed a gallery over the beach ridges the moment the
planter was widened. Corrected in the record and in `data/flora/index.json`, both quoting the
committed street. **The generalisation: a note that states a distance is a measurement somebody
took once, and this repository holds the coordinates to re-take it.** Three flora zone notes state
distances of this shape (z03's *"480 to 840 m EAST"*, z07's *"5.6 km SSW"*, z08's *"1,084 m"*) and
only this one has been checked.

**FINDING 2 — the timber's detail control has never done anything, and widening the sweep turned
that from harmless into a defect.** `STEMS` caps the stems at 820/520/300 trees by detail level,
and `step` is **count-neutral by construction**: the acceptance roll is `perHa * step² / 10000`,
so a coarser step visits proportionally fewer cells and accepts proportionally more at each. The
caps are therefore the whole of the control — and at 163 trees they had never bound, so `light`
and `full` have always planted the same wood in slightly different places. Widened, the wood plants
**387 trees at `light`**, and the cap **bound at exactly 300**: measured, not predicted. That is
not a thinning. The loop runs south to north, so a bound cap **deletes the north end of the wood
and leaves a straight edge across the town** — on phones, which start at `light`. Every cap is
raised by 3.70×, the ratio of the ground now swept, and **a bound cap is now a `problems` entry**,
which the release smoke reads as a failure. Making the detail control mean something is a uniform
thinning rather than a cap, and it is its own parcel — see K45(b3).

**THE COST, measured on this runner at 1280×800 rather than estimated.** The loop is O(cells) and
the field is 4× the square. Load **1.98 s → 2.13 s**. Stems **377 → 640** (163 trees + 214 thickets
→ 376 + 264). Timber triangles **108,804 → 175,136**; whole scene **~393k → 459k** against a
1,000,000 budget. **Draw calls unchanged at 59** against the ≤ 80 budget: the timber merges into
four quadrant buffers keyed on the sign of e and n, and widening the field does not add a bucket.
**The limit that buys**: those buckets are now 2 km wide, so a frame in town still submits the
eastern wood's geometry to be culled per-object at four objects. It costs nothing today at 175k
triangles and it is the wrong shape at 500k — a tiled chunker is the fix and it trades draw calls
for it, which is a budget question and not this parcel's.

**WHAT THE GATE HOLDS NOW.** `tools/measure_planting_reach.py` assertion 2 was a banked square and
is a banked domain: the swept bounds (may grow, may not shrink), the field they sit in, the reach
census, **the hectares swept and refused east of the limits**, and **both east limits with the
street each is read from, banked EXACTLY in both directions** — a wood that reaches further east is
an argument about a source, not a re-bank. Three new scans refuse the ways this could go quiet: a
loop that stopped sweeping the field, a renderer that stopped reading the street data, and a
`communityAt` that loads the limits and never consults them — which is precisely the loss K45(a)
measured one level out. All 38 self-test cases fire.

**WHAT DID NOT CHANGE, and one thing that did that a reader deserves.** No mix, no weight, no
density, no confidence and no archetype moved. But the wood is dealt from one seeded stream in
sweep order, so a wider sweep **redeals every stem in the town**: same rules, same expected counts,
different individuals. Nothing was tuned to make that look better.

**Verified:** `tools/check.sh` green; `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs
--published` green. The desktop half was not run and is not claimed — ~13 minutes against the
10-minute per-command ceiling; see the run-budget box at the top of this file. The draw-call and
triangle figures above are from a 1280×800 page load, which is the desktop geometry even though
the desktop smoke did not run.

### K45(b4) — the dune community, and the classifier that had to come from somewhere else · **DONE 2026-08-17 — 88 poplars on 4.30 ha of sand, and the beach's own record was never asked where it stood**

**SEEN.** Walk east to the lake and there are trees where there were none. It holds no exemption
and needs none.

**Read this box before adding a species to a second zone, or before quoting a refused-hectares
number.**

**WHAT SHIPPED, one: the community.** `COMMUNITIES.dune` — `populus_deltoides` in its dune form at
**9**/ha, `populus_tremuloides` and `populus_balsamifera` at **5** each, every one of them the
midpoint of its own `z08_lakeshore` band under K45(b1)'s rule, over `perHa` **[7, 31]**. That stand
density is **derived and not quoted**, which is a first here: ZONE 8 gives no canopy figure because
a dune has no canopy, and on open sand three isolated-tree densities ADD rather than competing for
one. The arithmetic is checkable in one line — at the middle of [7, 31] the draw plants 9 + 5 + 5
per hectare, each record's own midpoint reproduced exactly — and that is why it is written that way
rather than normalised to a hundred. Measured: **88 stems, 42 / 23 / 23**, against 41.7 / 23.2 /
23.2 expected.

**WHAT SHIPPED, two: the placement rule, and it is the interesting half.** K45(b) left three
candidates — substrate, the zone extent, or distance to the lake. All three are the same question
asked badly: **the heightfield does not carry substrate**, and the extent alone is not the
classifier, because ten zones overlap and a priority order decides between them. `flora.js` already
resolves exactly that, for the sward under the visitor's feet. So `communityAt` asks it —
`zoneAt(e, n) === 'z08_lakeshore'` — and the wood stands on the sand that is DRAWN, not on a second
copy of the beach that could drift from it. `trees.js` still reads no extent. A dead sward answers
null and plants no dune, which is the safe direction.

**FINDING 1 — the 40.2 ha K45(b2) banked as swept-and-refused was never 40.2 ha of woody
omission.** Measured on the committed heightfield through the sward's own classifier: the ground
east of the timber limits is **4.30 ha the lakeshore claims (2,687 dry nodes) and 33.6 ha of
`z09_sand_prairie`** (20,991 nodes), the relict beach ridges. **z09's record carries no tree.** Its
only woody entry is `quercus_velutina_grubs`, a `shrub_low` — a role no woody reader takes and
`flora.js`'s business, not this layer's. So five sixths of the refused ground is refused by the
dataset rather than by the renderer, and the parcel that reads "plant the 40.2 ha" was reading a
number that had never been broken down. **The generalisation: a refused population is only a defect
where something wanted to stand there, and nothing had asked WHICH records wanted to.**

**FINDING 2 — `SPECIES` is keyed by species id, and that breaks the first time a species is
recorded twice.** `populus_deltoides` is `z05_riverbank_timber`'s `tree_gallery`, 22–30 m tall with
a 14–22 m crown, and `z08_lakeshore`'s `tree_leaning`, 5–15 m with a 6–14 m crown and a note that
says *"isolated, half-buried and leaning"*. `loadTimberZones` keyed its spec map by species id and
took the first zone to name one, so the dune was one line from being planted with twenty-five-metre
floodplain cottonwoods — **the record read, routed, banded, gated, and drawn as another zone's
tree**, which is L116's fault one level in and would have passed every gate this project had. The
repair is narrow on purpose: `ARCHETYPE_BY_ZONE` lets a ZONE declare archetypes and a community name
the zone it plants from (`specsFrom`), and only the lakeshore has an entry. **The general form —
a spec map keyed by (zone, species) for every community — would redeal the whole town's specs**,
because `ulmus_americana` and four others are named by two zones too, and it is its own parcel.

**FINDING 3 — a gate that scans one table reports a false finding when a second table appears.**
`measure_planting_reach.py` assertion 3b reports a placed species drawn with the fallback's bole
and bark by scanning `SPECIES` alone, so it convicted both new poplars the moment they were
planted **with their own archetypes committed three hundred lines above**. It reads
`ARCHETYPE_BY_ZONE` now, per community rather than globally, and the bank is **0**. The scanner
raises on an absent table rather than returning an empty set, which is this file's own rule and the
reason the false finding was caught in one run rather than banked.

**AND ONE SELF-TEST CASE WAS ASSERTING THE REPOSITORY RATHER THAN THE MECHANISM.**
`measure_flora_reach.py` tested *"a woody record outside TIMBER_ZONES reaches nothing"* by naming
`z08_lakeshore` — so this parcel turned it red by repairing the thing it was written about. It is
asked of `z09_sand_prairie` now, with a note saying to move it again rather than delete it. That is
the third instance of this shape in four days (R-A1's inertness assertion, K51's two controls), and
the pattern is worth naming: **a case whose fixture is a defect dies when the defect is fixed.**

**WHAT IT COSTS.** Trees **373 → 472** (88 dune stems and a redeal of the rest), timber triangles
**167,830 → 186,442** against a 1,000,000-triangle scene budget, load 2.19 s. Timber draw calls
**4 → 5**, against the ≤ 80-per-station budget R-W5a and K36(b) hold. The wood is dealt from one
seeded stream in sweep order, so a new community **redeals every stem in the town**: same rules,
same expected counts, different individuals. Nothing was tuned to make that look better.

**WHAT IT REFUSES.** The river's point-bar branch is refused on the dune outright. It tests only
height and distance to water, so on the lakeshore it would read the beach as a point bar and hang a
willow screen along the open lake — which ZONE 8a refuses in as many words: 85–98 % bare sand, *"do
not vegetate this"*. Measured, it changes nothing today — **0 of the dune's 2,687 dry nodes qualify,
the nearest is 9.66 m from water against the branch's 9 m** — and it is written because 0.66 m is
the whole of that margin.

**WHAT IS STILL NOT PLANTED, stated rather than left to be discovered.** ZONE 8c's willow scrub —
`salix_cordata` 15–50 clumps/ha, red-osier, juniper, sand cherry — is `shrub_low`, a role no woody
reader has a cohort for, and `flora.js` plants it as ground cover rather than as scrub. Six records
reaching no reader became **two**; 301 unreached (record, figure) pairs became **261**. The
remaining two are the two vines whose `vine_drape` form nothing implements.

**Verified:** `tools/check.sh` — CHECK PASS, before AND after merging `dev`, with every moved bank
in this commit (`planting_reach_baseline.json`: 0 unselectable, 5 timber zones, 29 mix entries;
`flora_reach_baseline.json`: 2 records, 14 figures) plus all three gates' self-tests. That is the
dev gate: `chicago-4d-check.yml` runs it and nothing else, and it passed in CI on the PR too.

**AND THE MOBILE SMOKE HAS NOW OUTGROWN THE PER-COMMAND CEILING, WHICH IS WORTH RECORDING BECAUSE
THE RUN-BUDGET BOX AT THE TOP OF THIS FILE SAYS ONLY THE DESKTOP HALF HAD.** On this parcel's own
tree, `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs --published` finished at **237 passed /
2 failed** — the two road-contrast checks — and a run of the same command against a clean
`origin/dev` worktree returned **237 / 2, the same two checks, with the walker's-eye numbers
identical to the digit**. So the failures are the queue's, not this parcel's; R-M1c's box already
records that those bands sit honestly under the bar. Nothing gated moved, and in the reported-only
600–4000 m aerial band the readable share moves 75 % → 70 % on an unchanged `nBare` of 151 — a
redealt wood standing in front of more road, which is exactly what R-M1c's repaired denominator
exists to show rather than hide.

**After merging `dev` — which brought R-W1's lighting — the same command was killed by the
ten-minute ceiling at 230 passes**, the same two road failures and no page error, with the last
seven checks (free-fly return, three inspect paths, zero-page-errors, two vendor meshopt) unreached.
They are interaction and vendor assertions this parcel does not touch and all seven passed on its
pre-merge tree. **The mobile half now costs more than one command here**, so the durable fix named
in the run-budget box — a test-name or section filter beside `SMOKE_VIEWPORT` — is no longer only
the desktop half's problem.

### K45(b3) — the timber's detail control is a cap that never binds, and a cap is the wrong instrument · **DONE 2026-08-17 — the control did nothing to the wood and was halving the one population that must not thin**

K45(b2) finding 2 predicted half of this: `step` is count-neutral, so `light`, `balanced` and `full`
plant the same wood, and the only thing that could differentiate them — the `STEMS` caps —
truncates the north of the wood rather than thinning it when it binds. K45(b2) raised the caps so
they do not bind and made a bound one loud, which is a backstop and not a control. The repair is a
keep fraction per detail level applied to the acceptance roll, so a phone gets the same wood at
lower density instead of three quarters of one, and the caps stay what they now are.

**THE MEASUREMENT CAME FIRST AND IT FOUND A SECOND FAULT THE PARCEL WAS NOT WRITTEN ABOUT.** The
new instrument is `tools/measure_timber_detail.mjs`, which walks the visitor's own `setDetail`
through all three levels on the PUBLISHED mirror and asks two questions of each — how many stems,
and *how far north do they reach and in what shape*. Run against `dev` before a line was changed:

| level | trees | stools | stems | timber tris | scene tris | northernmost stem |
|---|---|---|---|---|---|---|
| `full` | 472 | 258 | 730 | 186,442 | 511,919 | N +397.7 m |
| `balanced` | 470 | 190 | 660 | 161,674 | 466,814 | N +396.3 m |
| `light` | 437 | 133 | 570 | 136,382 | 416,222 | N +391.7 m |

**FINDING 1 — the tree count confirms K45(b2): 472 / 470 / 437 is one wood planted three times.**
The spread is a draw's, not a control's — the acceptance roll is `perHa · step² / 10000` over
~190,000 cells, so the count is near-Poisson and 437 sits 1.6 σ under 472. Nothing in the detail
control had ever moved the timber.

**FINDING 2, AND IT IS THE ONE NOBODY WAS LOOKING FOR — the only thing scene detail DID do was
halve the sandbar-willow screen, which is the one population in this file that must not be
thinned.** The point-bar branch rolls a **fixed** per-cell chance (0.84), so unlike the tree roll it
is not count-neutral in `step`: a coarser grid visits fewer bar cells and accepts the same fraction
of each. **258 → 190 → 133 stools, 52 % of the screen gone at `light`, purely as a by-product of a
grid spacing, on the level phones start at.** The branch's own comment records exactly why that is
wrong — *"a screen needs its clumps to touch … thinning these to half was what left them standing
as separate cushions on open sand"* — and the code four lines below it was doing the thinning. **A
comment that states an invariant is not a gate**, and this one had been true and unenforced since
the branch was written.

**THE REPAIR, both halves.** `keep` is a fraction on the tree acceptance roll — 1 / 0.80 / 0.60,
the levels' OWN triangle ceilings in `main.js` read as a ratio, recorded as **L121** because the
ratio is invented and the ceilings are what bound it. The pre-K45(b2) caps' ratio (1 / 0.634 /
0.366) was the obvious alternative and is rejected in writing: those caps never bound, so they are
an intent nothing ever executed. The thicket roll now scales with the cell it is offered and
saturates at 1 — `THICKET_ACCEPT = min(1, 0.84 · cellArea / 16)` — and does **not** take `keep`.

| level | trees | stools | stems | timber tris | scene tris | northernmost stem |
|---|---|---|---|---|---|---|
| `full` | 472 (=) | 258 (=) | 730 (=) | 186,442 (=) | 511,919 (=) | N +397.7 m |
| `balanced` | **373** | **232** | 605 | 156,358 | 453,026 | N +396.4 m |
| `light` | **257** | **182** | 439 | 115,234 | **370,738** | N +391.8 m |

`full` is unchanged to the stem, which is the invariant that matters: every banked figure in this
repository is `full`'s. `light` loses 180 trees and gains 49 stools, and its scene comes down
45,484 triangles (−10.9 %).

**FINDING 3 — the screen cannot be fully recovered at a coarse step, and the residual is stated
rather than tuned away.** A probability cannot exceed 1: at 0.84 in a 4 m cell, both coarser steps
clamp, so the screen accepts every bar cell the grid offers and no more. The bar is a 6–9 m strip,
so a 5.6 m grid simply has fewer points on it than the screen wants stools — `light` recovers to
182 of 258 (70.5 %) and stops. That is a limit of what a coarse grid can resolve, which is honest;
0.84 was not. Closing the rest means sub-cell sampling on the bar, and it is not this parcel's.

**WHAT THE GATE HOLDS.** `tools/measure_timber_detail.mjs --gate`, against
`tools/timber_detail_baseline.json`, 17 assertions green: each level declares the keep fraction the
baseline banks and plants that share of `full`'s trees; **the wood still reaches the north end of
the field at every level and its northernmost tenth keeps its share of the stems** — the pair that
tells a thinning from a truncation, and the pair a stem count alone cannot; the screen holds ≥ 65 %
of `full`'s stools; and no level reports a bound budget. The tolerance on the tree share is 0.09
rather than 0.06 **because the sampling step moves the count on its own** — 472/470/437 before any
keep existed — so the tolerance has to carry the grid's drift as well as the draw's, and a tighter
number would have been a gate tuned to one seed.

**READ THIS BEFORE QUOTING A STEM COUNT.** Every figure this project publishes is `full`'s. A
screenshot or a census taken at `light` is now a different wood by construction, and that is new
since 2026-08-17: before it, the levels were interchangeable and nothing said so either way.

**FOR THE NEXT PARCEL.** `step` is now a pure sampling resolution — it costs planting-loop CPU at
load and buys no geometry — and `keep` is the whole of the density control. The two are orthogonal
for the first time, which is what makes a per-level frame-time measurement worth taking: it would
replace L121's borrowed ratio with a measured one. `flora.js` was read first as the parcel asked,
and its instrument does not transfer: the sward's LOW is a *shallower field* (smaller rings), which
works because the sward is planted into a ring that follows the visitor. The wood has no ring — it
is planted over the whole field once — so density is the only lever it has.

### K45(b1) — the sycamore, and the weight beside it that nothing uses · **DONE 2026-08-16 — 17 of the 26 mix entries are written to one number and plant stems at another**

**SEEN, weakly, and the honest sentence is in the changelog rather than hidden here:** a handful of
stems along the river are now a different species, at their own recorded height, crown and foliage
colour — so a screenshot from the same spot differs — but **finding 3 below is that they cannot be
identified as sycamores**, because the archetype they borrow is the elm's. It also holds
AGENTS.md's exemption 2 outright: K45(a) was the measurement half of this split and this is the
fix half.

**Read this box before quoting any mix weight.** K45(b)'s separable third change was *"one mix
entry — `['platanus_occidentalis', 1]` … weighted at the [1, 3]/ha its own record carries"*, and
`docs/LIBERTIES.md` L114 says the same in prose. The entry is in and the population it moves is
banked. The weight in it is not the one that was prescribed, for two independent reasons, and the
second one is the parcel.

**FINDING 1 — the prescribed 1 is the BOTTOM of the band, and the file's rule is the midpoint.**
Measured across all 25 entries standing before this parcel: **18 sit exactly on their record's
band midpoint or on its floor** (`fraxinus_pennsylvanica` 22 against 22.5, `celtis_occidentalis` 8
against 8.5, `juglans_nigra` 2 against 2.5, `salix_nigra` 42 against 42.5). Of the seven that do
not, three are a species carrying its full band in one list and a deliberately reduced presence in
another (`salix_amygdaloides` 8 in the gallery against 17 at the edge; `acer_saccharinum` the
other way about; `ulmus_americana` 60 in the thicket against 12 in the pocket), two are
`ridge_oak`, whose dossier merges **ZONE 6c + ZONE 7** so no single band applies, and two are
residue: `fraxinus_pennsylvanica` at 32 against 30, and `fraxinus_nigra` at **14 against 15** in
the only community it appears in, from the only zone that carries it. `[1, 3]` has a midpoint of
**2**, so the entry shipped is `['platanus_occidentalis', 2]`.

**FINDING 2, and it makes finding 1 moot — the literal beside a species id is a FALLBACK, and it
loses.** `loadTimberZones` builds `density[sp.id] = (perHa[0] + perHa[1]) / 2` for the first
`TIMBER_ZONES` entry that names a species, and `mixes` is then rebuilt as
**`records.density[id] ?? fallback`**. So the number that places a stem is *one global figure per
species for the whole town*, and the per-community weighting this file writes by hand — the thing
its own comment says the weights ARE — does not survive the load. **17 of the 26 entries differ**,
and three of them differ in a way a reader would call an error if they saw the frame:

| entry | written | plants at | from |
|---|---|---|---|
| `wet_woods.ulmus_americana` | 60 (39.2 % of the mix) | **25** (25.6 %) | z05, not z06 |
| `mesic_pocket.ulmus_americana` | 12 (12.2 %) | **25** (22.4 %) | z05, not z06 |
| `gallery.edgeMix.acer_saccharinum` | 8 (11.9 %) | **25** (29.4 %) | z05 |
| `gallery.mix.salix_amygdaloides` | 8 (7.0 %) | **17.5** (14.0 %) | z05 |
| `wet_woods.quercus_bicolor` | 17 (11.1 %) | **10** (10.3 %) | z05, not z06 |

The elm is written 60 where it is meant to dominate and 12 where it is meant to be incidental, and
is planted at 25 in both. The edge mix's own comment says *"at the water's edge the mix goes to
willow"* and the maple it cuts to 8 to say so is planted there at **25**, taking the edge from a
ninth silver maple to nearly a third of it. **All five species written into more than one list**
— `acer_saccharinum`, `ulmus_americana`, `fraxinus_pennsylvanica`, `quercus_bicolor`,
`salix_amygdaloides` — take **z05's** band in every community, because z05 is first in
`TIMBER_ZONES`: the same first-zone-wins rule K45(a) found deciding the SPEC, one field along and
with nothing anywhere saying so.

**WHAT DID NOT MOVE, and why that is the honest outcome.** No weight was corrected. Which of the
two numbers ought to win is a claim about the ecology — a per-community weight asserts *this
species is commoner here than there*, and the per-species midpoint is what the record actually
states — and answering it moves stems in three of the four communities at once. That is **K46**,
and it carries the full smoke and the critic shots. Correcting it here, inside a parcel whose
subject is one rare tree, would have been a frame-wide ecological change smuggled in under a
one-line repair.

**FINDING 3 — and the tree that got planted cannot be identified in the frame.** The sycamore is
the **only** placed species with no `SPECIES` archetype of its own, so
`SPECIES[sp.id] ?? SPECIES.ulmus_americana` hands it the elm's bole, taper, dbh band, puff count
and **bark colour**; its height, crown width and July foliage are its record's. The one thing the
record singles the species out for is *"white mottled bark flashing on the upper limbs"*, which is
how a sycamore is identified across a floodplain. **No flora record in this project carries a bark
colour at all**, so choosing a hex is a plain invention and a conspicuous one — the palest trunk
on that riverbank. Recorded as `docs/LIBERTIES.md` **L116** rather than invented inside a parcel
about a mix entry, and banked by name in `drawn_as_another_species`, exact both ways.

**WHAT SHIPPED.** `['platanus_occidentalis', 2]`; assertion **5** in
`tools/measure_planting_reach.py` — every entry's literal beside the weight that runs and the zone
it came from, banked exactly both ways — and the derivation itself scanned, so a renderer that
stops overriding the literal, or stops taking the band's midpoint, **raises** rather than
comparing a number with itself. A mix entry weighted **0** is a failure now: it would sit in the
file looking planted, be unpickable, and be invisible to assertion 3, which asks about species not
in a mix. Assertion **3b** banks every placed species drawn with another's archetype — one today,
and the substitution named in both directions. The self-test fires K45(b)'s own prescribed `['platanus_occidentalis', 1]` in memory on
every run, the way K45(a) fires L113's repair. The `unselectable` bank is **0 of 20**, and its old
negative control — *"a species in no mix is not selectable"*, which was this very sycamore — is
synthetic now: a gate whose proof that its scanner can say no is a species somebody is about to
plant stops proving it the day the repair lands.

**Verified:** `tools/check.sh` green; `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs
--published` green. The desktop half was not run and is not claimed — ~13 minutes against a
10-minute per-command ceiling; see the run-budget box at the top of this file.

### K46 — the hand-written community weight, or the record's global one? · **DONE 2026-08-16 — the written weight wins, because the dataset cannot hold what it says**

**SEEN. Read this box before quoting any mix weight or any species share.** The literal in
`COMMUNITIES` is now the number that plants the stem, and the record's band is the CONSTRAINT on
it. All 26 entries changed standing; 17 of them changed value.

**THE FINDING, and it refutes route 3 without needing the owner.** K46 offered three routes and
called route 3 — key `density` by (zone, species), each community reading the band from the zone
its own `dossier` cites — "the one that says what the file's comment claims". **It cannot be
built.** `wet_woods` cites **ZONE 6a** and `mesic_pocket` cites **ZONE 6b** and both resolve to the
single record **`z06_dense_forest`**, whose elm band `[40, 80]` is the swamp thicket's reading. A
zone-keyed density plants the elm at 60 in BOTH communities, and the **12** that makes it
incidental in the fire-protected pocket has nowhere in `data/` to live. Route 3 destroys the exact
reading it was proposed to restore. Route 1 (delete the weights) loses it too, by its own
admission. So route 2 is not a preference — it is the only one of the three that can express the
file, and the reason is the shape of the dataset rather than an argument about ecology.

**THE MEASUREMENT THAT MADE IT SAFE, and it is the one nobody had taken.** Each literal was scored
against the band of the zone its own community cites:

| | count | of 26 |
|---|---|---|
| inside its own cited band | **23** | 88 % |
| below one | **3** | 12 % |
| **above one** | **0** | — |

**Not one hand weight is an inflation.** That is what licensed handing them the scene: where the
file departs from a record it thins a species, never claims more of one than the evidence carries.
The three that depart are the three the file's own prose already explained — the peachleaf willow
held out of the gallery interior, the silver maple cut at the water's edge, the elm made incidental
in the pocket — and they are `docs/LIBERTIES.md` **L117** now, declared in each community's new
`departures` field, with the renderer refusing to load an undeclared one.

**WHAT MOVED IN THE FRAME.** No stem count changed — `perHa`, the stand density, was never
overridden and is untouched — so no tree appeared, vanished, or moved ground. What changed is
species share, in three of the four communities:

| list · species | was | now | Δ |
|---|---|---|---|
| `gallery.edgeMix` · `acer_saccharinum` | 29.4 % | **11.9 %** | −17.5 pp |
| `gallery.edgeMix` · `salix_nigra` | 50.0 % | **62.7 %** | +12.7 pp |
| `wet_woods` · `ulmus_americana` | 25.6 % | **39.2 %** | +13.6 pp |
| `mesic_pocket` · `ulmus_americana` | 22.4 % | **12.2 %** | −10.2 pp |
| `gallery.mix` · `salix_amygdaloides` | 13.8 % | **6.9 %** | −6.9 pp |
| `wet_woods` · `fraxinus_nigra` | 15.4 % | **9.2 %** | −6.2 pp |
| `ridge_oak` · `quercus_macrocarpa` | 36.8 % | **40.5 %** | +3.8 pp |

**THE RESIDUE K45(b1) LEFT IS RESOLVED, AND SO IS ITS OPEN OWNER QUESTION.** `fraxinus_nigra` at
**14** against a midpoint of 15 needs no explanation: the rule was never "the midpoint" — that was
a regularity 18 of 25 entries happened to follow — and 14 sits inside z06's `[10, 20]`. And
`ridge_oak`'s merged **ZONE 6c + ZONE 7**, which K45(b1) sent to the owner, **does not need
answering**: the record is a constraint, not a source, so the question is not *which band does it
mean* but *is the weight admissible in one of them*, and all four oak weights are. A question
dissolved by a rule change is worth more than a question answered.

**WHAT SHIPPED.** `zones: [...]` per community, held equal to the `ZONE n` numbers in its own
`dossier` prose by the gate, so the citation a reader sees and the bands the loader checks against
cannot drift. `departures: {...}` with the reason per entry, exact BOTH ways — a departure repaired
without dropping its note is `stale-departure` and fails. Assertion 5 in
`tools/measure_planting_reach.py` rebuilt: it banks each weight, the bands its community cites and
its verdict, and four faults are fired against synthetic bands on every run so the failing branches
are not theoretical. The renderer's own rule is scanned four ways — a loader that goes back to
`records.density[id] ?? fallback`, that collapses the per-zone band, that stops comparing, or that
stops reading `departures` all RAISE.

**THE FRAME, MEASURED BEFORE AND AFTER ON THE SAME THREE STATIONS** (`critic_shots.mjs
--metrics --stations river_bank,prairie_south,prairie_west`, source tree, desktop / mobile).
`CRITIC SHOTS OK` both times — no budget breached — and the **after-set was run twice in separate
processes and reproduced to every decimal below**, so these deltas are the change and not the
rasteriser's last bit:

| metric | station | before | after |
|---|---|---|---|
| high-pass RMS far | `river_bank` | 21.85 / 13.24 | **6.74 / 5.56** |
| high-pass RMS near | `river_bank` | 5.98 / 29.86 | **16.64 / 29.11** |
| crown fine-detail ratio | `river_bank` | 0.817 / 0.747 | 0.889 / 0.814 |
| horizon TIMBER (all) | `river_bank` | 0.7128 / 0.6485 | 0.7077 / 0.6685 |
| high-pass RMS far | `prairie_west` | 20.79 / 14.45 | **20.78 / 14.57** |
| high-pass RMS near | `prairie_west` | 19.61 / 27.80 | **19.61 / 27.73** |
| horizon TIMBER (all) | `prairie_west` | 0.7026 / 0.8719 | 0.5308 / 0.8625 |
| horizon TIMBER (all) | `prairie_south` | 0.3359 / 0.2727 | 0.3282 / 0.2250 |

**The control is the finding.** `prairie_west` is the station Andreas calls *"an open prairie,
entirely free from timber"*, and its texture metrics do not move — 20.79 → 20.78 far, 19.61 →
19.61 near. `river_bank` stands in the gallery, the community that changed most, and it moves
hardest and in the direction the weights predict: far-field detail falls by two thirds as the
interior loses peachleaf-willow share to elm and maple, and near-field detail more than doubles as
the water's edge goes to black willow at the camera. A frame-wide ecological change that left the
open-prairie control still is the evidence that it changed the timber and nothing else.

**One swing not chased, and it is stated rather than buried:** `prairie_west`'s horizon-timber
fraction falls 0.7026 → 0.5308 on desktop while barely moving on mobile (0.8719 → 0.8625). A
one-viewport swing of that size on a metric **R-W4a owns** deserves its own look; this parcel did
not take it, and no gate reads that figure today.

**Verified:** `tools/check.sh` green; `python3 tools/measure_planting_reach.py --self-test` PASS
(all 15 fire cases fire, all 27 scanner checks ok); `SMOKE_VIEWPORT=mobile node
tools/smoke_renderer.mjs --published` green; critic shots re-measured. The desktop half was not run
and is not claimed — ~13 minutes against a 10-minute per-command ceiling; see the run-budget box at
the top of this file.

### K47 — the sycamore is drawn as an elm from the bark outwards · **DONE 2026-08-16 — the archetype is built, and the tree it was built for is not in the town: 0 sycamores of 163 stems**

**UNSEEN, and the parcel was claimed SEEN. That inversion is the finding, so it goes first.** The
archetype landed exactly as specified — `SPECIES.platanus_occidentalis`, its own bole, taper,
diameter band, puff count and a two-tone bark — and a screenshot from any spot in this town is
byte-identical, because **the species the archetype draws is not planted anywhere in the scene.**

**THE MEASUREMENT.** Read out of `api.trees.stats.species` in the **published** build at 1280×800,
which is what a visitor loads:

| | |
|---|---|
| woody stems planted | **163** (plus 214 sandbar-willow thicket clumps) |
| of them in the `gallery` | **115** |
| **American sycamores** | **0** |
| the mix weight | 2 of the gallery's 116 |
| expected at that share | 115 × 2/116 = **1.98** |
| P(zero), independent draws | (1 − 2/116)^115 = **13.5 %** |

Three other species stand as a **single** stem (`celtis_occidentalis`, `quercus_velutina`,
`ostrya_virginiana`) and one as two, so the sycamore is the tail of a distribution rather than a
special case: **a 115-draw sample cannot carry a 26-entry ecology, and the rare end of it rounds
to nothing.**

**AND THE RULE UNDERNEATH IT, which no gate has ever checked.** `COMMUNITIES.gallery.mix` sums to
**116** while the community's stand density `perHa` is **[34, 62]** south of the river and
**[50, 78]** north. The weights are therefore *shares*: every species is planted at
**29–67 % of the density written beside it**. K46 made the literal the number that plants the
stem and made the record's band the constraint on that literal — and the literal is not the
density. The sycamore's 2 sits at the midpoint of its recorded **[1, 3]/ha** and passes the gate;
the scene plants it at **0.59–1.34/ha**, at or under the band's floor. That is **K48**, opened
below, and it is frame-wide: correcting it moves every species in every community, exactly as K46
did.

**SO WHAT DID CHANGE.** `docs/LIBERTIES.md` **L116** is resolved — nothing in this scene is drawn
with another species' archetype now, and `drawn_as_another_species` is empty where it held one.
The two invented bark tones are **L118**, with their bounds written down. `renderers/web/js/trees.js`
gained one optional field, `barkUpper`, used by the upper bole and the limbs; every other species
omits it and is unchanged. Assertion 3b's negative control was **re-pointed rather than left**: it
synthesised an empty bank against a state that carried the substitution, and with the substitution
repaired it was comparing nothing with nothing — a control that stops controlling on the day its
subject is fixed. It now synthesises the bank side.

**AND THE RECORD IT CORRECTS.** K45(b1)'s box and changelog **v139** both say a handful of stems
along the river are now sycamores and that a screenshot from the same spot differs. **Neither is
true**: the species became *selectable* — which is what that parcel's gate measures, and it
measured it correctly — and selectable is not planted. Nothing was overstated on purpose; the
instrument answered the question it was asked. `tools/measure_planting_reach.py` banks whether a
record can be **chosen**; nothing banks whether it is **drawn**, and the drawn census exists only
inside a running renderer. That gap is the other half of K48.

**Verified:** `tools/check.sh` green; `python3 tools/measure_planting_reach.py --self-test` PASS
(all 16 fire cases fire, all 27 scanner checks ok); `SMOKE_VIEWPORT=mobile node
tools/smoke_renderer.mjs --published` green. The desktop half was not run and is not claimed —
~13 minutes against a 10-minute per-command ceiling; see the run-budget box at the top of this
file. The two-tone bark was **proved to draw** before it was shipped: with the mix weight
temporarily at 400 the pale trunks and limbs are unmistakable at 70 m against the near-black
boles beside them, and that experiment was reverted before the commit.

### K49(a) — census the sward's draw · **DONE 2026-08-16 — the tail loss is REAL here too (6 species, 6,780 slots), and it sits on top of a second fault: 6 of 20 lists deal their slots off an area compared against a count**

**Read this box before quoting a flora share, and before proposing any change to a
`cover_fraction`, a `density_per_ha` or a `stems_per_m2`.**

K49 was opened by K48 on the reading that every weighted draw in this project loses its rare
end the way the woody mix did. The sward is the biggest of them — **118 of this project's 154
plant records**, against the 36 `trees.js` draws — and it had never been counted at all.

**Measured on the published mirror by `tools/measure_sward_draw.mjs`, standing the placer in
every community in turn: 8 communities, 16 populated lists, 6,780 slots dealt. Six species that
their own list owes a whole plant to are drawn NOWHERE, and the worst shortfall is 31.47 slots.**

| species | owed | its list | recorded as |
|---|---|---|---|
| **prairie dock** `silphium_terebinthinaceum` | **3.23** | `z01_wet_prairie.forb` | `density_per_ha` |
| water hemlock `cicuta_maculata` | 2.62 | `z01_wet_prairie.forb` | `density_per_ha` |
| wood nettle `laportea_canadensis` | 1.74 | `z06_dense_forest.forb` | `cover_fraction` |
| ninebark `physocarpus_opulifolius` | 1.45 | `z05_riverbank_timber.forb` | `cover_fraction` |
| compass plant `silphium_laciniatum` | 1.14 | `z02_mesic_prairie.forb` | `density_per_ha` |
| wild garlic `allium_canadense` | 1.02 | `z05_riverbank_timber.forb` | `cover_fraction` |

**Prairie dock is the one to look at**: a 2–3 m plant with a basal rosette 0.6–1.0 m across,
which is to say a landmark, owed three of them in the wet prairie and standing none.

**AND THE GATE'S OWN STATION CANNOT SEE ANY OF IT, which is the second finding and the more
transferable one.** The release smoke reads the same census, but it reads it where the gate
happens to be standing — the settled town, **68 slots, one community of ten** — and from there
the honest answer is "0 species absent". A first draft of this box quoted that figure and
concluded the sward's tail was clean. It is not; the sample was. **A census taken wherever the
harness already stood is a census of that place**, and every per-frame measurement this project
takes through the smoke has the same shape: `stats.sets`, `stats.instances`, the flower share.
`tools/measure_sward_draw.mjs` exists because the fix was to change where the instrument stands,
not what it counts.

**And underneath the tail there is a second fault, in the arithmetic that makes the share.**
`pick()` deals SLOTS, and a slot is one drawn plant. A record may state its abundance in three
fields, and they are not three spellings of one number: `stems_per_m2` and `density_per_ha`
are COUNTS of plants, `cover_fraction` is the AREA of ground the species holds. `buildSpecies`
normalises all three into one share, which reads *"covers 25 % of the ground"* as *"0.25 plants
per square metre"* — the same sentence about a two-metre dogwood and about a wild garlic, made
identical by a division.

**Measured, published mirror, mobile 390×780 — and dataset-wide, so it does not move with the
camera:**

| list | slots dealt off a count, against species recorded as an area |
|---|---|
| **`z06_dense_forest.forb`** | **96.5 %** |
| `z08_lakeshore.matrix` | 14.0 % |
| `z03_sedge_meadow.forb` | 10.2 % |
| `z03_sedge_meadow.matrix` | 3.8 % |
| `z09_sand_prairie.matrix` | 0.7 % |
| `z10_settled_town.forb` | 0.6 % |

**Six of twenty lists. The forest understory is the extreme**: ramps at 2.5 stems/m² take 96 %
of that list against nine shrubs recorded as cover, so what a visitor walks through in the
timber is decided by a comparison with no unit in it.

**And the repair is blocked on data, which is why this is (a) and not the whole parcel.**
Converting an area into a count needs the plant's own footprint, and **25 records state a
cover fraction and carry no `width_m`** — including `poa_pratensis`, which holds 60 % of the
town's lawn, and every one of the three cover-recorded forbs in the sedge meadow. The placer's
existing fallback (`min(0.35, height × 0.16)`) is a WALKER-CLEARANCE radius, and putting it at
the centre of the arithmetic that decides what the sward is made of would be an invented number
driving the answer: measured offline, the fallback moves `poa_pratensis` from a 0.60 share to
0.99 while a recorded width moves `trifolium_repens` from 0.16 to 0.003. **The conversion's
outcome is dominated by exactly the records that do not carry the number it needs**, which is
the definition of a gap that must be recorded rather than filled (AGENTS.md rule 2).

**Reported and NOT gated**, on the R-M1 split: a bar set today would either fail the build over
unresearched data or be satisfied by an invention. Both figures print every smoke run —
`6 of 20 lists`, `25 records` — and `stats.draws` carries the drawn census beside them.

**WHY THE TAIL WAS NOT FIXED IN THE SAME RUN, and it is not the same shape as K48.** K48's
repair is a picker that keeps accounts: it carries `share × drawn − placed` and hands the next
stem to whoever is owed most. That is legitimate for the wood, which is dealt ONCE at load. The
sward is dealt again every time the lattice re-centres, over a WORLD-ANCHORED grid whose whole
contract is that re-centring puts every plant back exactly where it was (`hash3`, and the comment
above it). A picker with running state makes a slot's species depend on which slots were visited
before it — so the plant at your feet would change species as you walked toward it. **The sward
needs a stateless equivalent** — a low-discrepancy assignment keyed on the slot's own world
coordinates, which is equidistributed over any window without carrying state between slots — and
that is a placement change that has to be looked at in a screenshot for lattice striping before
it ships. It is K49(b)'s second half, and it is why this parcel split.

**Nothing a visitor can see changed, and the changelog says so.** This is the measurement half
of a measure-then-fix split under AGENTS.md § THE VISIBLE-PROGRESS RULE exemption 2; **K49(b)
is the fix and is SEEN.** The three merged entries before it (v140, v141, v142) are all visible,
so the one-in-four cap is not touched.

**Files:** `renderers/web/js/flora.js` (the census, the count reading, `auditAbundance`) ·
`tools/measure_sward_draw.mjs` (new — the census read in every community, ~1 min, no frame it
does not need) · `tools/smoke_renderer.mjs` (one gated assertion that the instrument attributes
every slot, three reported figures) · ROADMAP + STATUS + the changelog + the published mirror.
No `data/` change, so no bake.

**Verified:** `tools/check.sh` green · `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs
--published` green, 222 passed / 0 failed · `node tools/measure_sward_draw.mjs` on the published
mirror, which is where every number above comes from. The desktop half of the smoke was not run
and is not claimed — ~13 minutes against this runner's 10-minute per-command ceiling.

### K49(b) — stand the six absent species up · **DONE 2026-08-16 — all six are standing, and the screenshot the parcel asked for vetoed half the repair: the dense layer cannot take a lattice**

**Read this box before proposing a low-discrepancy draw anywhere else in this project — the
answer is layer-dependent, and the deciding evidence is a frame, not a number.**

**The six are up.** `tools/measure_sward_draw.mjs`, standing the placer in all eight
communities, **6,780 slots → 6,795, and 6 species owed a whole plant and drawn nowhere → 0.**
Prairie dock stands in the wet prairie it was owed 3.23 of; water hemlock beside it; wood
nettle in the dense forest; ninebark and wild garlic on the riverbank; compass plant on the
mesic prairie. The settled town, where the gate's own station stands, still reports 0 absent —
the repair did not move the fault to the one place that could see it.

**The repair, as the parcel prescribed it.** A slot's draw is `frac(c·α + r·β + k·γ + shift)` on
its own world lattice coordinates — the R3 generators, 1/g, 1/g², 1/g³ for g⁴ = g + 1 — walked
against the CDF `pick()` already walks. Stateless, so re-centring puts the same plant back; K48's
account-keeping picker was NOT ported, for the reason K49(a) gave.

**Finding 1 — the thinning has to be part of the same draw, or the equidistribution is spent.**
A slot is asked two questions: does the recorded cover put a plant here (`share`), and which
species. Left as two independent numbers, the surviving slots are a *random subsample* of a
low-discrepancy set, and a random subsample is back to Poisson in its tail — the exact fault
being repaired. `dealt()` asks both of one draw: `u < share` carries the plant, and `u`'s
position inside `[0, share)` walks the CDF. Same marginals, one stratified draw.

**Finding 2 — and it is the one to carry away — THE DENSE LAYER CANNOT TAKE THIS, and a
screenshot is why.** Run on the near and mid tufts as well, the same construction grew the west
prairie **in visible ROWS with bare ground between them**. A lattice band is a family of
near-diagonal lines through the index grid: invisible where two slots in a hundred are planted,
unmissable where sixty are. Two frames at `prairie_west`, before and after, settled it in one
look after the census had already reported the change an improvement — *the census would have
merged it.* The matrix lists lost **no** species to the tail (their column read 0 absent both
ways), so the cost was entirely visible and the benefit entirely in a number that was already
zero. **The forb layer keeps the stratified draw; the near and mid layers are untouched.**
Consequence, stated rather than buried: the matrix layers' worst shortfall stays at 31.47 slots.

**Finding 3 — the block size is set by PLANTED slots, not by cells.** The Cranley–Patterson
rotation that breaks the lattice's diagonals is keyed on a world block. At 4×4 cells (64 slots)
the forb layer plants one or two per block, so the rotation was all that survived — an
independent draw in a costume — and the census still found **3** species standing nowhere
(`silphium_laciniatum`, `sambucus_canadensis`, `allium_canadense`). At 16×16 (1,024 slots, ~54 m,
about the width of the forb ring itself) it found none. Measured, both numbers, before choosing.

**Files:** `renderers/web/js/flora.js` (`LD_A/B/C`, the per-block rotation, `dealt`, the forb
emit) · ROADMAP + STATUS + the changelog + the published mirror. No `data/` change, no bake.

**Verified:** `tools/check.sh` green · `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs
--published` green · `node tools/measure_sward_draw.mjs` on the published mirror, 0 absent ·
`tools/critic_shots.mjs --stations prairie_west,river_bank` before and after, no striping and no
change to the grass. The desktop half of the smoke was not run and is not claimed — ~13 minutes
against this runner's 10-minute per-command ceiling.

### K49(d) — a stratification the dense layer can take · **DONE 2026-08-16 — the bijection works, and the block size is a U-curve nobody had a floor OR a ceiling for. Matrix deviation 368.80 → 282.89, and `prairie_west` does not stripe**

**Read this box before setting a stratum size anywhere in this project, and before quoting any
matrix shortfall number.**

**The construction, as the parcel prescribed it.** Every slot in a block of the world lattice is
dealt a distinct rank by a four-round Feistel network keyed on the block — a bijection by
construction, so `u` takes each of the n equally spaced values in `[0, 1)` exactly once and a CDF
band of width w gets `round(w·n)` slots rather than a Poisson draw around it. It is a pure
function of the slot's world coordinates, so re-centring puts the same plant back. Verified as a
permutation before it was measured as a repair: 1,024 distinct ranks of 1,024 at three keys, and
a 0.05-wide CDF band inside `share = 0.6` gets exactly 31 of 614.

**Finding 1 — the headline, and it is the row the parcel was opened on.** `z02_mesic_prairie`
deals 793 slots between four grasses and one came up **31.47** short of its own recorded cover.
It is now **3.67**. Across the seventeen matrix rows: **eleven improve, five cannot move** (they
are single-species lists, and a list of one has nothing to stratify) **and two get worse** —
finding 3. Worst shortfall **31.47 → 19.59**; total deviation **368.80 → 282.89**, −23 %.

**Finding 2 — THE BLOCK SIZE IS A U-CURVE, and K49(b) finding 3's rule is only its left half.**
That rule — *the block size is set by PLANTED slots, not by cells* — is a FLOOR: the block must
hold enough planted slots to resolve the finest CDF band. It has a CEILING too, and nothing had
named it: exactness holds over the block, the census reads a sub-window, so the error is whatever
the window's partial blocks cut. A near ring is 15.2 m across; a 16-cell block is 11.8 m, so the
window contained about **one** whole block and almost every slot read was in a partial one.
Measured, all five, on the matrix deviation:

| block | m (near) | slots | matrix deviation | vs. independent draw |
|---|---|---|---|---|
| independent draw | — | — | 368.80 | — |
| 1 cell | 0.74 | 4 | **2,725.88** | 7.4× worse |
| 2 cells | 1.48 | 16 | 602.95 | 1.6× worse |
| **4 cells** | **2.96** | **64** | **282.89** | **−23 %** |
| 8 cells | 5.92 | 256 | 303.30 | −18 % |
| 16 cells | 11.84 | 1,024 | 340.47 | −8 % |

The floor is not a soft one. At four slots per block `u ∈ {0.125, 0.375, 0.625, 0.875}`, so at
`share ≈ 0.6` exactly two are planted and `u/share` takes **two** values — the whole CDF collapses
onto two species and the deviation is seven times the fault being repaired. **The forb layer sits
at the floor** (it plants ~1 % and needed 1,024 slots); **the matrix layer is bound by the
ceiling** (it plants ~60 %, so 64 slots already carry ~38 plants). Same rule, opposite ends,
which is why one number could never have served both layers.

**Finding 3 — the two rows that got WORSE are both rows where a spatial filter runs after the
deal, and that is the sub-window weakness one turn further in.** `z10_settled_town` in its own
community went 14.31 → **39.18** and `z05_riverbank_timber` reading the wet-prairie list went
6.37 → 8.87. A permutation makes rank a deterministic function of position inside the block, so
anything that removes slots *on a spatial rule* — the town's building footprints through
`station()`, the waterline through the same — selects a **biased** set of ranks, where an
independent draw would have been filtered without bias. That is the leading explanation and it is
consistent with both rows being the two most heavily filtered; it is **not proven**, and
`z03_sedge_meadow` reading the marsh list improved despite crossing water. **K49(e)** is the
parcel that measures it.

**CORRECTED 2026-08-16 by K49(f): this explanation is refuted for the bigger of the two rows.**
Giving the block's grid a phase — a change that touches no filter — takes `z10_settled_town` from
39.18 back to **15.52**, within 1.21 of its pre-K49(d) 14.31, and `z05_riverbank_timber` from 8.87
to **7.67**. The town's regression was the fixed grid's own bias, not `station()`. What is left for
K49(e) is the riverbank's residual 1.30. Do not quote the paragraph above without this one.

**AND FULLY REFUTED 2026-08-23 by K49(e)/T-0018, which is what that parcel was opened to settle:
the mechanism is not merely unproven, it runs the OTHER WAY.** Measured over 7,844 dealt slots in
29 rows, the survivors of `station()` and `crowdsTheWalker()` are **less** unevenly spread across
species than a rank-blind subsample of the same size — pooled 0.65 of the rank-blind figure, worst
row 1.11 — and the riverbank row this paragraph is about has **0.0 % of its slots refused**, so no
filter can be carrying any part of its residual. Finding 3 above is wrong in its direction and is
kept only as the reasoning it was. Do not quote either paragraph without K49(e)'s box.

**The screenshot, which is the acceptance test K49(b) set.** `prairie_west` desktop, published
mirror, before and after: **no rows, no diagonal banding, 74 draw calls both ways.** The mix in
frame changes visibly — the under-drawn grass now has its recorded share — which is the point.
The veto is cleared.

**Finding 4 — the measurement this needed did not exist.** `worstShortfall` is a max of a max: it
moves on one species in one list and it ranked these five candidates in a different order from the
robust statistic (16 cells wins on `worst` at 15.98 and is nearly the worst option on deviation).
It named the fault and it cannot choose a repair. `tools/measure_sward_draw.mjs` now also prints
**`deviation`** — the whole list's disagreement with its own record, summed over every species and
both signs — per row and per layer, and that is the figure the table above ranks on.

**Files:** `renderers/web/js/flora.js` (`STRAT_SALT`, `STRAT_BLOCK_SHIFT`, `feistel`, `stratum`,
`stratumHalf`, `scatter`'s `draw` mode, the near + mid emits) · `tools/measure_sward_draw.mjs` ·
ROADMAP + STATUS + the changelog + the published mirror. No `data/` change, no bake.

**Verified:** `tools/check.sh` **CHECK PASS** · `SMOKE_VIEWPORT=mobile node
tools/smoke_renderer.mjs --published` green · `node tools/measure_sward_draw.mjs` on the published
mirror, five block sizes, table above · `tools/critic_shots.mjs --published --viewport desktop
--stations prairie_west` before and after. **The desktop half of the smoke was not run and is not
claimed** — ~13 minutes against this runner's 10-minute per-command ceiling.

### K49(e) — does a spatial filter eat the stratification? · **DONE 2026-08-23 (T-0018, TWO PARALLEL RUNS, TWO INSTRUMENTS, ONE ANSWER — NO, AND IT IS THE OTHER WAY ROUND). PR #337 refuted the mechanism in principle on 400 synthetic layer keys and banked its control pair into `tools/check.sh`; PR #338 measured the placer's own filters where they actually run — pooled 0.65 of the rank-blind figure, worst row 1.11, and the riverbank residual this parcel was left on has 0.0 % of its slots filtered**

**K49(c2) found a second symptom of the same suspect, and it is a stronger one than the census rows
this parcel was opened on.** Its route-1 sweep makes the union of the blocks in a frame an exact
stratification of the CDF at `1/(n·B)` — on paper. Measured, a species owed **1.11** slots was
still drawn nowhere, which cannot happen if the union is exact. The ring and the view cone cut most
blocks partially, so the rank a narrow band lands on is often a rank that was never dealt. Whoever
takes this: the question is not only whether the filter biases the SET of ranks, it is what
fraction of a block survives it, because that fraction is the ceiling on any tail guarantee this
placer can offer.

**It is UNSEEN and it has the written exemption: it is a gate-shaped measurement blocking a named
SEEN parcel** — every future use of `stratum` in a filtered layer, and K49(c) is one.

K49(d) finding 3's explanation is stated and not proven. The claim: because a permutation makes
rank a deterministic function of position within the block, any filter applied AFTER the deal that
is itself a spatial rule selects a biased set of ranks, and an independent draw would not have
been biased that way. The two rows that regressed are the two most heavily filtered
(`z10_settled_town`'s building footprints, `z05_riverbank_timber`'s waterline); one row that
crosses water improved anyway, which the explanation does not cover.

**How to settle it without guessing.** `station()` and `crowdsTheWalker()` are the filters. Count,
per row, what fraction of DEALT slots they reject and correlate it against the change in
`deviation` — the tool already stands the placer in every community, so this is a column, not a
harness. If the correlation is there, the remedy is not a different permutation: it is to deal
AFTER the filter, or to accept it and say so in `stratum`'s doc block. If it is not there, the
regression has another cause and K49(d) finding 3 must be corrected in this file.

**MOSTLY ANSWERED ALREADY, AS A BY-PRODUCT — 2026-08-16, K49(f), and the answer is the LAST clause
above.** K49(f) gave the block's grid a phase. It touches no filter, `station()` and
`crowdsTheWalker()` run exactly as before, and both regressed rows recover: **`z10_settled_town`
39.18 → 15.52**, which is 23.66 of its 24.87 regression and lands within 1.21 of its
pre-K49(d) 14.31; **`z05_riverbank_timber` reading the wet prairie 8.87 → 7.67**, 1.20 of 2.50.
So the town's regression was **not** the filter — it was the fixed grid's own bias, and the
explanation K49(d) finding 3 offered is refuted for the row it was mostly measured on. What
survives is the riverbank's residual **1.30**, which is what this parcel is now for: a small term,
possibly the filter, possibly nothing. **Re-scope it before claiming it** — the correlation column
is still the right instrument and the population it has to explain is now half the size.

**THE ANSWER — 2026-08-23, T-0018, and it was answered TWICE, by two runs that took the ticket in
parallel and could not see each other.** Read both; they are different constructions and the pair is
stronger than either. **PR #337** attacks it analytically: the position→rank map is `feistel(idx,
half, blockHash)` and `blockHash` is re-keyed per block, so a rule that reads only position cannot
lean — demonstrated over 400 synthetic layer keys with χ² against uniform, three modelled filter
shapes indistinguishable from a rank-blind control, and a rank-reading arm four orders of magnitude
red; its control pair now runs in `tools/check.sh`. **PR #338 — this section — measures the real
thing**: not a `halfplane` standing for a waterline but `station()` and `crowdsTheWalker()`
themselves, over the actual town, at ten stations, in the census the project already keeps. What
follows is that half.

**The instrument, and why it is not the correlation column this box asked for.** `deviation` is a
functional of the SURVIVORS' ranks alone, so the claim can be put exactly instead of correlated
across sixteen noisy rows. `flora.js` now counts each species' slots at the moment of the deal
(`dealt`) as well as after the filters (`drawn`) — the same census one step earlier — and
`tools/measure_sward_draw.mjs` splits the survivors' disagreement with the deal in two:

| term | what it is |
|---|---|
| `dealtDev` | `Σ|dealt_i − share_i·N|` — the discrepancy the DEAL has before any filter |
| `B` | `Σ|drawn_i − q·dealt_i|`, `q = m/N` — how far the survivors are from the filter having taken the same fraction of every species. Zero for a perfectly even filter |
| `Bnull` | what `B` reads when the mechanism is ABSENT: `Σ √(2/π)·√(m·p_i(1−p_i)·(N−m)/(N−1))`, the mean absolute deviation of the hypergeometric a rank-blind filter would produce |

**`B/Bnull ≈ 1` refutes the mechanism for a row; `B/Bnull ≫ 1` proves it, and by how much.** The
figure `deviation` moves on is `dealtDev` scaled by `q` plus `B`, so this is a decomposition and
not a proxy.

**Finding 1 — the mechanism is refuted, and refuted in the opposite direction.** Over **7,844
slots dealt in 29 rows, of which the two filters refuse 23.4 %**, the pooled `B/Bnull` is
**0.65**; the median row is 0.65 and the worst row in the scene is **1.11**. Not one row is
meaningfully above the rank-blind figure. A filter that selected a biased set of ranks would sit
ABOVE 1; these sit below it, which says the survivors are spread across the species list MORE
evenly than an independent subsample of the same size would be. The stratification is not eaten by
the filter. It partly survives it.

**Finding 2 — the riverbank residual this parcel was left on cannot be the filter at all, because
nothing is filtered there.** `z05_riverbank_timber` standing in its own community reading the
wet-prairie matrix list: **44 slots dealt, 44 drawn, 0.0 % refused**, `dev/100` identical before
and after the filters at 11.91. The residual K49(f) left to this parcel is entirely the DEAL's own
discrepancy at a 44-slot population — the stratification's granularity, not `station()`. That is
the alternative this box was required to name if the correlation was not there.

**Finding 3 — the explanation for the sub-1 reading, stated as reasoning and not measured here.**
`station()` refuses ground in contiguous patches — a building footprint, the far side of a
waterline, a road — and the block permutation that finding 3 of K49(d) called the danger is what
makes that safe: a contiguous patch is close to whole blocks, and a whole block is a COMPLETE
stratum, one slot of every rank. Removing complete strata leaves the remainder exactly stratified,
which is why `B` lands below the i.i.d. null rather than on it. **The negative is what is proven;
this paragraph is the reading of it.**

**Finding 4 — the instrument was shown red before it was believed.** Both controls run on the real
dealt vectors, in `tools/measure_sward_draw.mjs`, 200 trials each: a genuinely uniform subsample of
the same size reads **0.96–1.03** (so `Bnull` is calibrated, not merely plausible), and one of the
same size that rejects wide clumps preferentially — which is the rule `crowdsTheWalker()` actually
applies — reads **3.92–5.00**. The instrument can see the mechanism. It is not there.

**What this licenses, which is the reason the parcel carried the exemption.** `stratum` may be used
in a heavily filtered layer: the filtering costs the layer its SIZE, and a smaller population has a
larger per-slot discrepancy for that reason alone (`z09_sand_prairie` reading the mesic list, 51.8 %
refused, `dev/100` 1.08 → 2.63 — below what rank-blind filtering of that size predicts). It does not
cost the layer its stratification. A census row that got worse behind a filter should be blamed on
the deal or on the row's size, and this tool now prints both columns to say which.

**What #337 left, and this closes.** A synthetic model answers whether a filter of a given SHAPE can
bias the deal; it cannot answer whether the filters the placer really runs are those shapes. They
are: measured in place, every real row sits at or below the rank-blind figure, and the row the
parcel was left on turns out to refuse nothing at all — which is a stronger statement than #337's
"5.24 is below the mean deviation at that sample size", because there is no filter there to be
below anything.

**Files:** `renderers/web/js/flora.js` (`countDealt`, `countDraw` reached through the zone rather
than a rebuilt Map key, the `rejStation`/`rejWalker` counters on the four censused emits,
`closeCensus`) · `tools/measure_sward_draw.mjs` · this box · STATUS + the changelog + the mirror.
No `data/` change, no bake, nothing drawn moves.

**Verified:** `tools/check.sh` **CHECK PASS** · `node tools/measure_sward_draw.mjs` on the source
tree and on the published mirror · both viewports, which read identically — and that is itself a
finding, filed as its own ticket: `SWARD_VIEWPORT=mobile` changes the browser page size but not
`lowSpec`, so the ring sizes the tool's own header says the viewport decides are in fact the same
at both.

### K49(f) — the same 64 numbers in every block · **DONE 2026-08-16 — 2 species absent → 0, matrix deviation 282.90 → 219.19**

**Read this box before reaching for `stratum` anywhere, and before quoting K49(d) on a regressed
row.**

**The fault.** `stratum()` returned `(rank + 0.5) / n`. The Feistel permutation decides which slot
gets which rank; it does **not** change the SET of `u` a block deals, which was the same n equally
spaced numbers in every block of the world. A species owns a CDF band of width `share × weight`, so
a band narrower than `1/n` may contain none of those numbers — and if it contains none of them in
one block it contains none of them in **all** of them. The species is then not thinly drawn. It is
absent from the scene, deterministically, at every station, for ever. The forb layer never had this
because its lattice `u` already carried the block's `shift`; the matrix layer acquired it the day
K49(d) handed it a fixed grid.

**Finding 1 — the predicted population and the measured one are the SAME TWO RECORDS.** At
`STRAT_BLOCK_SHIFT = 2` the step is `1/64 = 0.015625`. Across the ten communities there are **45**
matrix bands, and exactly **two** are narrower than one step: `z04_marsh.zizania_aquatica` at
**0.007137** (0.457 of a step) and `z09_sand_prairie.opuntia_humifusa` at **0.004412** (0.282).
Those two, and only those two, were the species `tools/measure_sward_draw.mjs` found owed a whole
slot and drawn nowhere — wild rice at all three stations that read the marsh list. That is an exact
correspondence between a population predicted from the construction and a population measured in
the shipped build, which is what makes this a cause rather than a correlation. **A band narrower
than a step is not certain to be missed** — it is missed unless it happens to contain one of the n
values — but because the grid is identical everywhere, that coin is tossed **once for the whole
world**. Both of these lost it.

**The repair, and why it is the textbook one.** `u = frac((rank + 0.5) / n + phase)`, where `phase`
is the block's own offset — the `shift` the lattice path has always taken, now taken by both. This
is a systematic sample with a random start, and the reason that is the standard form is exactly the
reason it is needed here: the n values stay equally spaced, so the block is still an exact
stratification and K49(d)'s construction is untouched, but a band of width w now falls on a dealt
value in about `w · n` of the blocks instead of in all of them or none. The estimator becomes
unbiased. One line, in `stratum` and its call site.

**Finding 2 — it is not a trade, it pays on the statistic K49(d) chose too.** Published mirror,
`tools/measure_sward_draw.mjs`, 17 matrix rows:

| | K49(d) | K49(f) |
|---|---|---|
| species owed a whole slot and drawn nowhere | **4 rows / 2 species** | **0** |
| total matrix deviation | 282.90 | **219.19** |
| worst matrix shortfall | 19.59 | **15.21** |
| matrix rows improved / unchanged / worse | — | **8 / 5 / 4** |
| forb deviation | 107.18 | **107.18** |

The five unchanged rows are single-species lists. The forb figure is identical **to the decimal**,
which is the control: the lattice path was not touched. **Four rows do get worse** — `z02` 12.67 →
18.13, `z04` 7.06 → 12.48 (and it is the row that gains wild rice), `z03` 36.69 → 42.20, `z09`
25.88 → 26.35 — and that is the honest cost of an unbiased draw: a band of width w takes `floor` or
`ceil` of `w·n` per block instead of one fixed count, so a block is noisier and the long run is
right. Net **−22.5 %**.

**Finding 3 — the by-product is the bigger result, and it belongs to K49(e).** See that box: the
two rows K49(d) regressed and attributed to a post-deal spatial filter recover on a change that
touches no filter. The town recovers 95 % of its regression. **The generalisation worth carrying:
when a construction is changed and two numbers move, the explanation offered for the one that got
worse is a hypothesis about the CONSTRUCTION, and the cheapest test of it is another change to the
construction — not a harness around the suspect.** K49(e) was scoped as a filter measurement and
its subject was never the filter.

**Finding 4 — the gate that missed it is the gate K49(a) already described, and it is fixed here
rather than described again.** `smoke_renderer.mjs` read the sward census at whichever community it
was standing in — the settled town, one of ten — and printed "0 absent" throughout. It now stands
the placer in **every** community, the way `tools/measure_sward_draw.mjs` does, and the assertion is
on the SCENE rather than on a station: a species counts as absent only where **no** station drew it
while some station's list owed it a whole slot. A station missing a plant its own ring owes 1.2 of
is a sample; a plant that is nowhere is the fault. The camera is restored afterwards so nothing
downstream reads a sward dealt at the last station visited.

**And finding 4 has a second half that the first version of this gate got wrong, which is worth
more than the gate.** It was written as "viewport-safe by construction" on the reasoning that a
smaller ring lowers what is owed. **That is false, and the gate failed on its own first run
proving it.** The census's resolution is the number of slots dealt, and that is set by SCENE DETAIL,
not by the viewport: measured at 390×780, `full` deals **6,848** slots, `balanced` **3,791** and
`light` **2,670** — and the smoke's own run had left the renderer at `light`, where the wet
prairie's prairie dock, owed **1.09**, can take none of them from a perfectly correct draw. Gating
that reads a fault out of a small sample. So the census now runs at **all three** detail levels, the
**richest** one is the gate, and the other two are printed every run:

| detail | slots dealt | drawn nowhere |
|---|---|---|
| **full** | **6,848** | **0** — gated |
| balanced | 3,791 | 1 — `z01_wet_prairie.forb.cicuta_maculata`, owed 1.37 |
| light | 2,670 | 1 — `z01_wet_prairie.forb.silphium_terebinthinaceum`, owed 1.09 |

**Those two are named rather than gated away, and they are not this parcel's fault**: both are in
the FORB list, which K49(f) does not touch, and both are one plant either side of an expectation
just over 1. But the row is real — *a visitor on `light` may not find the prairie dock* — and the
honest place for it is a line the smoke prints every run rather than a sentence in a doc. **The
generalisation: a census gate's bar belongs to its SAMPLE SIZE, and the sample size here is a
setting the visitor controls.**

`tools/measure_sward_draw.mjs --gate` is the same scene-wide assertion as a one-command check
(**7 s**, at the default detail); `tools/check.sh` runs neither, because the dev gate's runner has
no Playwright by design.

**Files:** `renderers/web/js/flora.js` (`stratum`, its call site in `scatter`) ·
`tools/smoke_renderer.mjs` (the all-community census) · `tools/measure_sward_draw.mjs` (`--gate`) ·
ROADMAP + STATUS + the changelog + the published mirror. No `data/` change, no bake, no liberty.

**Verified:** the gate landed RED on the old construction first — `--gate` reports **FAIL, 4
species** with the phase forced to zero and **PASS, 0** with it in, which is the only way to know an
assertion catches the thing it was written for. `tools/check.sh` **CHECK PASS** ·
`SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs --published` green · **the desktop half of the
smoke was not run and is not claimed** (~13 min against this runner's 10-minute per-command
ceiling); the desktop evidence is `measure_sward_draw.mjs`, which measures at 1280×800 and reports
0 absent.

### K49(c1) — the twenty-five footprints, and what the conversion does · **DONE 2026-08-16 — `unconvertible` 25 → 0, and the conversion is MEASURED AND NOT SHIPPED because it puts a species at the edge of K49(f)'s gate**

**Read this box before dealing a sward slot off any number.** K49(c) was written as one parcel and
split on the run-budget rule the lane already carries: it is a measure-then-fix, its measurement
half is the twenty-five records, and the fix half now has a committed baseline it cannot redefine.

**The research half, and it is closed.** Every sward record that measured an AREA and carried no
footprint has one: **25 records across 8 communities**, each graded in its own
`width_provenance` — **11 inferred**, reasoned from a footprint this dataset already commits for
a plant standing beside it in the same list, and **14 reconstructed**, bounded by the record's own
`height_m` and its dossier row's stated habit and recorded in `docs/LIBERTIES.md` **L119**. Not one
is attested, because **no source this project holds states a footprint for any of the twenty-five**;
the one measured graminoid footprint in the whole dossier is *Carex stricta*'s (§ ZONE 3,
*"tussocks 0.3–0.5 m tall × 0.3 m wide"*), which this dataset already committed.

**Why the grade sits on the figure rather than on the record.** A record's `confidence` grades what
its sources say about the PLANT, and eight of the twenty-five are `attested` records. Writing an
argued width under that grade would have promoted an argument into an attestation — the one thing
AGENTS.md rule 1 forbids — so `width_provenance` is a sibling block of the `{confidence, sources,
note}` shape this project already uses on every structure attribute, and `tools/validate.py`
refuses a width_provenance that outranks the record it sits in.

**And the gap is closed for good, which the measurement alone would not do.** `tools/validate.py`
now fails any flora record whose abundance is a `cover_fraction` and whose role is one the sward
placer deals (`matrix`, `forb`, `emergent`, `shrub_low`, `ground`) unless it carries a `width_m`.
A new cover record without one silently re-opens a list that is measurable today.

**THE FIX HALF, MEASURED ON THE PUBLISHED MIRROR AND COMMITTED HERE SO K49(c2) CANNOT MOVE THE
BAR.** The conversion — `weight` dealt off `stems` (plants per m²) instead of off whichever field
the record carried, with `forbShare` held on the recorded-cover sum so the number of slots does not
move — was built, published and censused with `tools/measure_sward_draw.mjs`:

| | before | after the conversion |
|---|---|---|
| records giving a cover with no `width_m` | 25 | **0** |
| deviation from the recorded cover, matrix | 219.19 | **197.46** slots |
| deviation from the recorded cover, forb | 107.18 | **89.11** slots |
| worst shortfall, any row | 15.21 | **12.29** slots |
| species owed a whole slot and drawn nowhere | 0 | **1** |

**The shares it moves, which is why the parcel is SEEN:** the forest understory's ramps
**96.5 % → 89.3 %** of its lottery and the wood nettle **1.1 % → 6.3 %**; the sand prairie's June
grass **8.1 % → 24.0 %**; the lakeshore's little bluestem **11.6 % → 30.1 %**; the settled town's
broadleaf plantain **25.2 % → 53.6 %**; the sedge meadow's cordgrass **14.2 % → 3.2 %**.

**AND THE ONE THING THAT STOPS IT MERGING, stated as a number rather than as a worry.** The two
bulrushes of the sedge meadow — *Scirpus atrovirens* and *S. cyperinus*, **identical records at
200/ha** — are dealt **1.90 % → 0.16 %** of that list's slots, which over the census's 645-slot
frame is **1.10 slots owed each**. One takes its slot and the other takes none, and K49(f)'s gate
is ABSOLUTE on exactly that: a species owed a whole slot and drawn nowhere fails the smoke. It is
not a band narrower than one step — the fault K49(f) repaired — it is **the tail of an unbiased
deal at expectation 1.1**, and the two identical species landing on opposite sides of it is the
proof. Weakening the assertion to pass is refused; the gate is right and the deal needs to reach
it. **K49(c2) is the fix half.**

**A second finding, and it is about what `width_m` MEANS.** The conversion is
`cover / (π·(w/2)²)`, which is exact for non-overlapping cover — so it only converts honestly if
the width is the same thing the cover measures. It is not, everywhere: § ZONE 3 gives the tussock
sedge **40–60 % cover** and, in the same sentence, tussocks **0.3 m wide standing 0.5–1.0 m
apart** — which is **1–4 plants/m²**, against the **6.62/m²** the conversion derives from that
record's committed 0.31 m width. The width is a BASE width and the cover is FOLIAGE cover. This
project's `width_m` is a crown width on a tree and a clump width on a sedge, and nothing had ever
asked whether those are the same field. Where a dossier states a SPACING it states a density
directly, and that is better evidence than any width — K49(c2) owns it.

### K49(c2) — deal the sward on plants per m² · **DONE 2026-08-16 — the conversion is SHIPPED, and the route that was written off as "not a route to green" is the one that got there**

**Read this box before proposing a construction to fix a tail.** The sward is dealt on plants per
m² in every list, at K49(c1)'s committed baseline, and the tail gate is green on the published
mirror. Measured with `tools/measure_sward_draw.mjs` against the mirror, at both viewports:

| | dev (before) | K49(c1)'s conversion | shipped here |
|---|---|---|---|
| deviation from the record, matrix | 219.19 | 197.46 | **154.19** slots |
| deviation from the record, forb | 107.18 | 89.11 | **89.11** slots |
| worst shortfall, any row | 15.21 | 12.29 | **8.50** slots |
| species owed a whole slot, drawn nowhere | 0 | 1 | **0** |

**Finding 1 — ROUTE 1 WAS BUILT AND IT DOES NOT CLEAR THE TAIL.** The block phase is stratified
across blocks now (`blockPhase`: a van der Corput sweep of the step `1/n`, indexed by the block's
Morton code on one random start for the layer, so neighbouring blocks sit a quarter and a sixteenth
of the step apart by construction rather than by luck). Measured on the conversion alone it takes
the matrix deviation **197.46 → 156.51** and the worst shortfall to 8.50 — and *S. cyperinus* is
**still drawn nowhere at 1.11 owed**. The promise in K49(c1)'s route 1 — "a species owed one slot
in the frame would take one" — is **refuted at frame scale**, and the reason is K49(e)'s question:
a frame does not hold whole blocks. The union of block grids is an exact stratification only if
every block is fully realised, and the ring and the view cone cut most of them, so the rank a
narrow band lands on is often a rank that was never dealt. **At an expectation of 1.1 slots no
world-anchored construction can guarantee the draw**; the sweep buys variance, not a guarantee.
It is kept because 197.46 → 156.51 on its own is the largest single move in this table.

**Finding 2 — ROUTE 3 IS WHAT MADE IT GREEN, and K49(c1) said it would not.** Its exact words:
"That does not on its own lift the bulrushes over the gate (measured: 0.24 %, 1.57 slots owed)".
Measured here, it does — **with the sweep (154.19) and, tested separately, without it (191.48)**.
The prediction was made on the share and not on the draw, which is the same mistake as reading a
cover as a count: 1.57 owed is not 1.10 owed, and the extra half slot is the difference between
a coin toss and a plant. `data/flora/zones/z03_sedge_meadow.json`'s *Carex stricta* now records
`stems_per_m2: [1, 4]` — 1/s² for the **0.5–1.0 m apart** its own dossier row states — with an
`abundance_provenance` block grading it `inferred` (the source states a spacing, not a count; the
even-spacing arithmetic is ours) and `tools/validate.py` holds that block to the same rule
`width_provenance` carries. It replaces a derived **6.62/m²**, and the cover figure is not lost:
how much ground the matrix holds is the zone's own `cover.matrix_fraction`, which is what deals
the slots. `z03_sedge_meadow.matrix` falls from **42.20 to 19.87** deviation and its worst
shortfall from 15.21 to 6.18.

**Finding 3 — THE SLOT COUNT DID NOT MOVE, and it is held by construction rather than by care.**
`forbShare` is computed from a subset's `recorded` sum — the abundance exactly as written, in
whatever unit — and the lottery from `stems`. The two numbers are now separate fields with
separate jobs, so a future change to the lottery cannot thin the sward by accident.

**What this does NOT do.** It does not touch `matrixShare` or `forbShare`'s tuning (a separate
question, against the reference photographs), and it does not raise a confidence anywhere: the
one figure that moved carries its own grade and no liberty was owed, because nothing was invented.
The desktop half of the smoke was not run — the runner's ten-minute per-command ceiling does not
fit it (see THE RUN BUDGET above); the mobile half is green at 224/0 and the census was run at
both viewports.

**Route 2 (a designated tail slot) was NOT built and is not needed** — the tail is green without a
new construction in a filtered layer. Finding 1 is the argument against reaching for it later:
the filter is what breaks the guarantee, so a construction inside the filter would inherit the
same problem. K49(e) owns the measurement.

The original parcel text follows.

The fix half. The conversion is built and measured (the table above is its baseline and may not be
re-derived to something kinder); what is missing is the tail. Three routes, none of them a change
to the assertion:

1. **Stratify the phase across BLOCKS, not just within one.** K49(f) gave each block its own
   offset, which makes a narrow band land in about `w·n` of the blocks — unbiased, and still a coin
   flip over the two or three blocks a frame holds. A phase that sweeps the step across
   neighbouring blocks would make a species owed one slot in the frame take one. Watch K49(d)'s
   U-curve and K49(e)'s filter question before touching it.
2. **A tail slot.** One designated slot per block dealt from the species whose bands are narrower
   than one step. Guarantees the rare end by construction; it is a new construction in a filtered
   layer, so it needs its own census.
3. **Take the density where a dossier states a SPACING** — § ZONE 3's *"0.5–1.0 m apart"* is a
   count of 1–4/m², attested, and it moves *Carex stricta* from the 6.62/m² the width implies. That
   does not on its own lift the bulrushes over the gate (measured: 0.24 %, 1.57 slots owed), so it
   is a correction to make and not a route to green.

Whatever route: publish, re-census, and the smoke's sward tail assertion must be green on the
PUBLISHED mirror before it merges.

The other fault K49(a) measured and refused to guess at. **It starts with the 25 records**,
because nothing else can be derived until they carry a footprint: find a clump width for each
from its own dossier, or state in the record that none is attested and grade what follows
accordingly. `tools/smoke_renderer.mjs` prints the list every run.

Then convert every list to plants per m² and deal the slots on that basis. **Two things it must
not do.** It must not change how many slots a list gets — `forbShare` and `matrixShare` are
tuned against the reference photographs and are a separate question again. And it must not raise
a confidence: a width read off a dossier is attested, a width argued from a related species is
reasoned, and a width chosen to make the sward look right is invented and belongs in
`docs/LIBERTIES.md`.

**Why it is SEEN:** the forest understory is 96 % ramps today and the eleven species recorded
beside them as an area hold 3.5 % of the slots between them. Any honest conversion moves that,
and the riverbank, the sedge meadow and the lakeshore dune with it.

### K48 — the share was not the defect · **DONE 2026-08-16 — both repairs it named are impossible, and the sycamore was lost by the DRAW. 0 sycamores became 2**

**Read this box before proposing a change to a mix weight, a `perHa`, or a recorded density.**
K48 was opened on the reading that every species is planted too thin. That reading is wrong, and
the arithmetic that refutes it is in the record rather than in an opinion. Neither of the two
repairs the parcel named can be built:

- **(a) rescale each community's literals so the realised density lands inside the record's band
  — ARITHMETICALLY IMPOSSIBLE in two of the four communities.** The realised densities of a
  community's species sum to its stand density, so putting every species at or above its own
  recorded floor requires the floors to fit under the stand ceiling. **`wet_woods`: the floors sum
  to 100/ha against a stand ceiling of 84.** **`gallery`: 75 against 62** in the South Division
  belt (the North Division's [50, 78] clears it by three). No assignment of weights exists. This
  is not a preference between two ecologies; it is a system with no solution.
- **(b) derive `perHa` from the mix sum — REFUTED by the same dossier row the weights come from.**
  It puts the gallery at **116 trees/ha** against § ZONE 5's *"canopy 30–80 trees/ha"* and
  `wet_woods` at **153** against § ZONE 6's *"overall canopy target 50–110 trees/ha"*. Both
  contradict an attested structural sentence to satisfy a column in the table beneath it.

**So the record's density column is not a stand density and never was.** ZONE 6 says so in its own
words — *"overall canopy target 50–110/ha with local >100/ha pockets and >30 % of area at savanna
density"* — and 6a's four species sum to 100–205 on their own. The figures are microsite
abundances that legitimately sum above the stand they sit in, which is exactly what the mix comment
in `trees.js` already said and what K48 read as a defect. **The file was right and the parcel that
doubted it was wrong.** K46's gate is checking the literal against the band, which is the right
check on the right number after all.

**What WAS broken is one line further down, and it is what K47 actually found.** Every stem was an
**independent** draw on its community's shares. An independent draw loses the rare end of a
distribution: the sycamore is 2 of the gallery's 116 over 115 gallery stems — 1.98 expected — and
the seeded shuffle dealt none. Because the scene is seeded that was not luck that would come out
next time; it was permanent. Three more species stood as a single stem, so it was the tail of a
distribution and not one species' bad day.

**The repair: the draw is corrected against what it already owes.** Each species carries
`share × drawn − placed` and the draw is proportional to that shortfall, except that a species
already owed a whole stem takes the next one outright. Two bounds follow by construction —
nothing overshoots by a stem, and nothing owed a whole stem gets none — and both are what the
smoke now asserts. Stress-tested over **35,880** (mix, stand size, seed) cases at stand sizes 4 to
900: worst overshoot **0.99** stems, worst shortfall **1.21**, zero species owed a stem and given
none. Without the outright rule the worst shortfall is **2.32** and 17 of those cases lose a
species the stand owed a stem to. **No weight, density, band or departure moved.**

**Measured on the published mirror, mobile 390×780 and desktop 1280×800, identical at both:**

| | before | after |
|---|---|---|
| American sycamores standing | **0** | **2** (for 1.52 owed) |
| of the 26 weighted entries, standing nowhere | 1 | **0** |
| worst overshoot / shortfall against share | — | **0.51 / 0.86** stems |
| stems / thicket stools | 163 / 214 | 178 / 213 |

**The wood is re-dealt and the PR says so rather than claiming otherwise.** `addTree` draws a
tree's own bole, taper and puffs from the same stream and takes a different number of draws per
species, so changing which species stands at one stem shifts every draw after it. Nothing that
decides how many stems a hectare holds changed — `perHa`, `edgeFade`, `clearedFactor` and the
waterline gate are untouched — so 163 → 178 is the same Bernoulli placement re-dealt, not a
denser wood.

**The drawn census now exists**, which was the parcel's cheaper half and the gap K47 named:
`tools/measure_planting_reach.py` proves a record can be **chosen**, and
`stats.draws` + the two smoke assertions prove it is **drawn**. A renderer that went back to an
independent draw fails both — it overshoots freely (the gallery elm's 25/116 over 115 stems has a
standard deviation of 4.4 stems) and it loses the tail.

**The generalisation, and it is the K36(b) seam pointed at a distribution: when a parcel says a
population is the wrong SIZE, check first whether it is the wrong SHAPE.** Three parcels in a row
here — K45(b1), K46, K48 — read a species that was not in the frame as a fault in the number
beside it. Twice it was, once it was not, and the once was the one where the number was small.
Every weighted rare thing in this project is drawn the same way: **the 63 households in
`generators/inferred_households.py`, the roof coverings, the massing variety picker.** Each one is
a weighted draw over a small sample, and none of them has ever been asked what its tail does.

**Files:** `renderers/web/js/trees.js` · `tools/smoke_renderer.mjs` (the drawn census) ·
ROADMAP + STATUS + the changelog. No `data/` change, so no bake.

### K47 — the parcel as it was claimed, kept for the record

K45(b1) planted the American sycamore and its own box says the tree **cannot be identified in the
frame**: it is the only placed species with no `SPECIES` archetype, so
`SPECIES[sp.id] ?? SPECIES.ulmus_americana` hands it the elm's bole, taper, dbh band, puff count
and **bark colour**, and `docs/LIBERTIES.md` **L116** records the substitution rather than
inventing past it. The one thing `z05_riverbank_timber` singles the species out for is the
sentence *"white mottled bark flashing on the upper limbs"* — the reason a sycamore is
identifiable across a floodplain — and this scene draws it in the elm's dark brown.

**Why this parcel and why now.** The owner, 2026-08-15: *"you are still being hesitant and
refusing to build because you are being too cautious about being perfect. It's ok to create
things that have some justification and they can be inferred or even reconstructed based on your
analysis"* — with **the tree colours as his own example**. L116's stated reason for not
building is that no flora record carries a bark colour, so a hex is an invention. That is what
`docs/LIBERTIES.md` is for: bound the invention, write it down, and build.

**Files:** `renderers/web/js/trees.js` (one `SPECIES` entry, and the one change that lets a
species carry a second bark tone) · `tools/measure_planting_reach.py` (assertion 3b's bank leaves
with `--update`, and its negative control has to be re-pointed, because a control whose subject is
the thing being repaired stops controlling anything) · `docs/LIBERTIES.md` L116 → resolved, plus
the new entry the invention owes · `docs/STATUS.md` · the changelog. **No `data/` change, so no
bake.** It changes the frame, so it carries the smoke.

### K46 — the parcel as it was opened · **superseded by the box above**

K45(b1) measured the divergence and refused to resolve it. The question is one sentence: **when a
community's mix says a species is commoner in it than the species' own record does, which number
plants the stem?** Today the record wins by accident — `records.density[id] ?? fallback` was
written to let a record supply a weight the file did not have, and it also overwrites every weight
the file does have. Nothing in the repository states that as a decision.

**Take K45(b1)'s numbers; they are banked.** 17 of 26 entries differ, and the five sharpest are in
its table. Do not re-derive them: `python3 tools/measure_planting_reach.py` prints the pairs.

**The three routes, and none of them is free.**

1. **The record wins, deliberately** — delete the per-community weights and write the mixes as bare
   species lists. Honest about what runs today, and it *discards* real information: the swamp
   thicket's elm at 60 and the mesic pocket's at 12 are a reading of the dossier that nothing else
   in this project records. Cheapest, and it loses the most.
2. **The community wins** — the fallback becomes the value and `records.density` supplies only
   species the mix does not weight. Restores the edge mix's "goes to willow" and the elm's two
   readings; moves stems in three of the four communities, so it is the route that has to prove
   itself in the frame.
3. **Both, keyed properly** — `density` becomes per (zone, species) rather than global, and each
   community reads the band from the zone its own `dossier` line cites. This is the one that says
   what the file's comment claims: the weights ARE the dossier's per-species densities, from the
   right dossier. It needs `ridge_oak`'s merged **ZONE 6c + ZONE 7** answered first — it cites two
   zones and would have to say which band it means, or how it combines them.

**What it must not do.** Route 2 or 3 without the frame is not acceptable: this changes the
species composition of most of the timber in the scene, and R-W4a's horizon metric and R-G1's
axes are the evidence that it did not make the town worse. `tools/critic_shots.mjs --metrics
--stations …` and the mobile smoke are the minimum; the desktop half does not fit this runner's
per-command ceiling, so say so rather than merging on the mobile half alone.

**One residue for whoever takes it.** `fraxinus_nigra` is written **14** against a band whose
midpoint is **15**, in the only community it appears in, from the only zone that carries it — the
one departure K45(b1) could not explain by a species in two lists or a community merging two
zones. It is invisible today (the 15 runs), and route 2 would make it visible.

### K44 — a figure can be read and still reach nothing, because every reader takes a cohort · **DONE 2026-08-16 — 339 of 1,880 (record, figure) pairs, six records handed to no reader at all, and the July fruit K43 was opened to record as missing is drawn on 29 of the 31 records that carry it**

**Read this box before quoting any flora read number.** K42 built the read-set and asked
the question a read-set can ask: does any file under `renderers/web/js/` contain an
expression that touches this figure? One does, so `species[].july.inflorescence.shape` is
`mesh` and the map is finished with it — **for all 154 species records at once, and no
reader in this project has ever received all 154.**

**FINDING 1 — the arithmetic, and the map reports zero of it.** Every reader takes a
COHORT, declared in the renderer as three different kinds of literal: `flora.js` draws
five of the manifest's seven roles and fifteen of its forms over **all ten** zones;
`trees.js` draws the other two roles, five forms, and **four of the ten zones**
(`TIMBER_ZONES`). Multiply K42's 18 declared species reads by that routing and **339 of
the 1,880 (record, figure) pairs it calls read reach nothing** — 18 %, across **17 of the
18** figures. The two widest are not the flowers: `species[].common` and
`species[].july.appearance` are read by `trees.js` alone, so **30 of 154** plant records
can be named to a visitor and **124 cannot**. `july.phenology` is read by `flora.js`
alone, so the woody layer has **no July gate at all** — 36 records whose season is
recorded and never tested.

**FINDING 2 — six records reach no reader, and four of them are a promise the zone makes
in its own prose.** `z08_lakeshore` carries **eastern cottonwood, quaking aspen, balsam
poplar and sandbar willow** — three graded `attested` off the MNFI open-dune survey and
Cowles 1901 — and `TIMBER_ZONES` does not name that zone, so `trees.js` never opens it.
The zone's `reads_as` says *"a scrub of sand cherry and leaning cottonwood"*: the sand
cherry is a `shrub_low` and is drawn, the cottonwood is a `tree` and is not. **The fault is
independent of the ground question and survives its repair** — whatever K42's finding 4b
settles about the eastern zones' extents, and whatever T-E3 does to the heightfield under
them, these four records are still handed to nothing, because the list they are missing
from is in a renderer and not in the terrain. The other
two are the riverbank's vines, whose `vine_drape` form the manifest itself publishes in
`forms_unimplemented`: a stated gap, and stated to a programmer rather than to a visitor.

**FINDING 3 — K42's fruit sentence is refuted, and K43's research half is not owed.**
*"31 flowering plants record the fruit they carry in July, which nothing draws"* is wrong
in the direction that matters: **29 of the 31 are drawn**, in the fruit's own recorded
colour, shape, size and height on the plant, because `headOf()` draws a fruiting head from
`july.inflorescence` exactly as it draws a flowering one — the cattail's brown spadix
`[92, 62, 40]`, the dogwood's white berry cluster `[214, 216, 206]`, the iris's green
capsule. What no renderer reads is the **boolean** `inflorescence.fruit`, which
`tools/validate.py` requires whenever `phenology` is `fruiting`, and which is therefore the
one part of the record another field already implies. **The flower that IS missing is a
different one**: `trees.js` has no head archetype at all, so the **American basswood in
bloom** — *"pale flower clusters on their strap bracts, heavily bee-worked"*, colour and
size both written down — draws plain foliage, as does the ironwood in fruit. Three recorded
July inflorescences draw no flower; two are woody and one is the grape.

**WHY THE FIELD-LEVEL MAP COULD NOT SEE ANY OF THIS, and it is the generalisation worth
carrying.** *"This figure is read"* and *"this record is read"* are different sentences,
and only the first one had a gate. A read-set keyed on a field path is a statement about a
FILE; the population it is silently quantified over is the records that reach that file,
and nothing had ever written that population down. The same shape is waiting anywhere a
project declares a read against a reader that receives a subset: the archetypes' `CONSUMED`
lists are per-archetype and every building is dispatched to one of them, and
`terrain_inputs.py` declares its reads against a generator that runs on one epoch.

**WHAT SHIPPED.** `tools/measure_flora_reach.py` — census, `--gate`, `--self-test`,
`--update` — and `tools/flora_reach_baseline.json`, banking all three populations by name:
6 records, 17 partly-reached figures with their counts, 3 headless inflorescences with a
reason each. Five assertions: **1** the manifest's `forms_flora` / `forms_trees` /
`forms_unimplemented` vocabularies against the readers' own dispatch tables, both
directions; **2** the two cohorts are disjoint and every role is a published one; **3**
the unrouted records, exact both ways and by reason; **4** every declared read whose
carriers are not all reached, banked with its counts, so a moved population is a failure
rather than a discovery; **5** the recorded flowers that draw no head. Every cohort is
**scanned out of the renderer**, never restated — a Set, an array and an object literal,
and a scanner that cannot find its declaration raises rather than returning an empty set,
because an empty cohort would route the whole town to `none` and bank it. K42's
`FLORA_ZONE_READS` is imported rather than copied, so the two gates cannot drift.
`docs/LIBERTIES.md` **L113** records the omission, with the three repairs that resolve it.

**THE METHOD NOTE, because one scan alone is wrong in both directions.** Attributing a
figure to a reader needs the declared expression AND the leaf scan, unioned. The
expression alone undercounts — `sp.height_m` is destructured in `flora.js` and
type-checked in `trees.js`, and K42's map names one of those. The leaf scan alone misses
the renamed local: `flora.js` reads `inflor.rgb` off a variable, and `rgb` is the one leaf
K42 has to scan parent-qualified. Both directions are exercised in `--self-test`.

**THE LIMIT, stated rather than discovered later.** This measures **routing** — which
reader is handed the record. Whether a routed record then has modelled ground to stand on
is a different question with a different answer (K42's finding 4b, zone extents), and this
tool does not ask it: a record it calls reached is one its reader receives, not a plant a
visitor is guaranteed to be standing in front of. The tool's docstring and its census
footer both say so.

**Verified:** `tools/check.sh` green with the two new steps; `SMOKE_VIEWPORT=mobile node
tools/smoke_renderer.mjs --published` green. The desktop half was not run and is not
claimed — ~13 minutes against a 10-minute per-command ceiling; see the run-budget box at
the top of this file. **No record moved, no renderer file changed and no asset changed**:
this parcel is a measurement, a bank, a liberty and two gate steps.

### K41 — the rights rule tests a label, and the label is on the other side of the question · **DONE 2026-08-16 — the gate could only ever fire on a violation an author had already written down, and 49 geometry-bearing attributes on 21 records are built from sources nobody has checked**

**Read this box before quoting any rights number.** AGENTS.md hard rule 6 and
`docs/PROVENANCE.md` both say a `check_required` source *"may be cited in text but must not
have assets derived from it"*, and PROVENANCE.md added four words: **"The validator enforces
this."** The parcel took K34's move — *read a rule this project states about itself and ask
what enforces it* — and pointed it at rule 6.

**FINDING 1 — the enforcement compares two fields of the SAME source record, and the pair it
looks for has never existed.** `run_license_check` fails a source whose `rights_status` is
`check_required` or `restricted` **and** whose `asset_use` is `geometry`. `asset_use` is the
source's own declaration of intent, so the assertion fires only once an author has written the
violation into the record. Measured: **38 of 64 sources have unresolved rights and every one
of them declares `cross_check` or `text_only`**; the **three** that declare `geometry` are
`wright_1834`, `harrison_1830_river_mouth` and `hathaway_1834` — a survey and two maps, all
clear. The intersection is empty and always has been. Note what this is *not*: the labels are
not dishonest. `asset_use: geometry` means *this work is traced*, and nothing traced is
unresolved. The fault is that the rule is about a **derivation** and the mechanism is about a
**declaration**, so the one population it exists to watch is invisible to it.

**FINDING 2 — the derivation is real, and this project already had a definition of it.** No
reviewer has to decide what "derived" means here: `generators/archetypes/*_params.py` declares
`CONSUMED`, the set of form attributes the generator reads, and `generators/terrain_inputs.py`
declares the same map for the ground. That is the same definition `tools/validate.py` uses to
demand a `geometry:` declaration on everything *outside* it — an attribute inside it reaches a
vertex by construction. Footprints are in by the same argument: `from_phase` reads the polygon
for the massing. Against that definition, **49 geometry-bearing attributes on 21 records cite
a source whose rights are unresolved** — 43 on buildings, 6 on the terrain spec's blocks — and
**19 of the 20 buildings have a baked master in `assets/gltf/` today**.

**FINDING 3 — the sharp population is the sole-support one, and it is most of it.** **35 of
the 49** have no source outside the blocked set at all, so striking the unresolved citation
would leave the value standing on nothing. **16 of those 35 are graded `attested`** — this
project's strongest grade, resting entirely on a work nobody has checked the rights on. They
are not marginal buildings: the **Sauganash Hotel**'s storeys and construction, the **Wolf
Point Tavern**'s frame addition and its painted sign, the **Green Tree Tavern**'s footprint,
roof and paint, **St Mary's Church**'s footprint, the **Western Hotel**, **Miller House**,
and on the ground the west and south division levels and the old south channel.

**WHAT THIS PARCEL DELIBERATELY DOES NOT DECIDE.** Whether reading *"two storeys, frame"* out
of a copyrighted page and building a box from it **is** deriving an asset from that page is a
question about rights, and the project's own documents do not agree. `docs/PLAN.md` reads it
narrowly — *"blocks derived assets, e.g. Conley/Stelzer, but not textual citation … Stanford
renewal check before any derivative texture"*, which is about **images** — while AGENTS.md and
PROVENANCE.md read it broadly enough to cover a dimension. The two readings give opposite
answers for all 49. **A gate cannot settle that and this one does not try**: it holds the
population where it is and hands the reading to the owner.

**THE THREE ROUTES, for the owner.** (1) *Narrow the rule to expression* — say in AGENTS.md
and PROVENANCE.md that `check_required` blocks traced geometry and derived textures, not facts
read out of a text; then the 49 are legitimate and the bank becomes a watch-list for the day
someone traces one. (2) *Do the checks* — 13 distinct sources carry all 49, mostly
`chicagology.com` and `drloih`; resolving those to `cleared` empties the bank by data rather
than by definition, and assertion 3 makes each resolution a visible commit. (3) *Hold the wide
reading and re-grade* — the 16 `attested` sole-support values would have to fall back to
`inferred` with the reasoning stated, which is a change to what the town claims about itself
and needs the owner's word.

**WHAT SHIPPED.** `tools/measure_rights_derivation.py` — census, `--gate`, `--self-test`,
`--update` — and `tools/rights_derivation_baseline.json`, 49 entries banked by record, phase
and attribute. Four assertions: **1** absolute, the old label test kept and restated where the
real measurement lives; **2** a new geometry-bearing citation of an unresolved source fails;
**3** absolute, a banked entry that has left the data fails until it is un-banked in the
commit that repaired it, so a repair is recorded rather than absorbed; **4** a banked entry
may improve and may not worsen — its blocked set may not grow and corroboration may not be
lost. All five failure modes are exercised in memory against the real tree by `--self-test`,
which `tools/check.sh` runs, because K37's lesson was that a gate nobody has watched fail is a
gate nobody knows fires.

**THE RESIDUAL, named rather than left silent.** The gate stops at the buildings and the
ground because those are the only two layers with a declared read-set. **`data/flora` carries
202 citations of an unresolved source and `data/fauna` 30**, both rendered, and neither has a
`CONSUMED` map — so "which of a zone's figures reaches a vertex" has no answer to gate on yet.
The census prints both counts on every run so the hole cannot be forgotten. That map is the
successor parcel, and it is worth more than the citations: it is the same question
`check_geometry_declarations` asks of every building and has never asked of a plant.

**Verified:** `tools/check.sh` green (with the two new steps); `SMOKE_VIEWPORT=mobile node
tools/smoke_renderer.mjs --published` green. The desktop half was not run and is not claimed —
~13 minutes against a 10-minute per-command ceiling; see the run-budget box at the top of this
file. **No record, asset, parameter or renderer file changed** — this is a measurement, a
gate, the documents and a changelog entry.

### R-W6(b) — the 16-bit ground is in the script and not in the file a visitor downloads · **CLOSED 2026-08-23 by T-0151 — the file caught up on its own, and that was the second half of the fault**

> **The finding below describes a state the tree has left.** Measured 2026-08-23 with this box's
> own control: `terrain__e1834_harbor_cut.glb` regenerated from the committed master at **16**
> bits reproduces the committed derivative md5 for md5
> (`5b8446876a425fceace5c7dd7c59688a`, 704,004 bytes); at 14 bits it does not
> (`4b9fb0765a9b5669dd547b32ef156825`, 702,896). A nightly bake shipped the 16-bit ground when it
> rebuilt the terrain, and **nothing in this repository could say so** — which is the same silence
> this box was written about, running the other way. Both ends are shut now:
> `tools/measure_terrain_fit.mjs --gate` recovers the shipped POSITION bit depth from the mesh's own
> rungs (`extent / (2**bits − 1)`, inverted) and FAILS when it is coarser than
> `tools/web_derivatives.sh` asks for, demonstrated firing on the 14-bit file.
> The water mesh reproduces at both depths (`61b38d4bc36964db450b59ac7b646b77`), exactly as R-W6
> predicted: four vertices at y = 0 land on every lattice.
>
> **The numbers below are superseded** — 671/672 KB was a smaller terrain. What is NOT closed is
> the surface error: on the ground that ships today the worst drawn-surface departure is **77.1 mm**
> with **56** samples past the 22 mm road lift, because the epoch box grew east into 60–90 % slopes.
> That is R-W6's own stated reopen condition for the skirt split and it is **T-0152**.


R-W6 is marked DONE 2026-08-16: the terrain's quantisation was raised from 14 to 16 bits,
taking the ground's lattice from 306 mm to 76.6 mm and its worst drawn-surface error from
46.3 mm to 12.9 mm, under the 22 mm road lift everywhere. **The change is in
`EPOCH_QUANT_BITS`. It is not in `assets/web/terrain__e1834_harbor_cut.glb`.**

Measured, not inferred. Regenerating the committed terrain master at **14** bits reproduces the
committed derivative **md5 for md5** (`8fb489c25b3b1237b0a95565d8a9e9e6`, 687,232 bytes); at 16
bits it comes out 688,348 bytes, and **1,116 bytes is exactly the cost R-W6 quoted for 16 bits**.
So the ground a visitor is standing on today is still on the **306 mm lattice R-BUG3c found
buries the road**, and R-W6's numbers describe a file that has never been published.

Nothing caught it because the K36(a) gate compares master to derivative on material identity,
triangle count, node identity and a bounding box within four rungs — and a bit-depth change
moves none of those. R-W6's own gates measure the *field*, not the shipped bytes.

**Why this is not K36(b)'s to fix.** It moves the ground, which is the surface R-BUG3c,
R-BUG4, R-M1a and the road-contrast bands all measure against, so it needs those gates run and
not a materials parcel's. It is one `tools/web_derivatives.sh --only terrain__e1834_harbor_cut.glb`
plus the same for `water__`, so a runner *can* do it — but regenerating geometry outside a bake
is a policy question this project has not answered (see T-V1(b), which is parked on the same
one). **Take the measurement above as committed; do not re-derive it.**

### K36(b) — the parcel as written, kept for the record

The 38 assets in `tools/web_derivative_baseline.json` reached the browser as one
`PaletteMaterial001` plus two generated PNGs. **This repair needs no Blender**: `assets/web/` is
produced from the committed masters by `gltf-transform` alone, so a run with `npx` reachable can
regenerate all 334 derivatives from the tree as it stands.

**The likely fix is one flag** — turning the palette pass off in `tools/bake.sh`'s `optimize`
invocation — but the parcel is not "add the flag", it is **measure what the flag costs**. The
palette pass exists to reduce draw calls by merging materials, which is the same currency R-W5a
spent its parcel on (47 batches → 16, budget ≤ 80 per station-viewport). So:

1. regenerate the derivatives with the palette pass disabled, and diff the payload;
2. re-run the smoke and R-W5a's batch counts against the *published* mirror, at the stations
   where those 38 buildings are in frame, and quote both numbers;
3. **if the palette genuinely buys draw calls**, the answer is not to keep it silently — it is
   to say so in `docs/GLB-CONTRACT.md`, which is a bilateral contract, and to record that the
   shipped material identity is deliberately different from the baked one;
4. either way, bank the outcome with `tools/measure_web_derivatives.py --write-baseline`.

**Read K36(a)'s finding 1b first.** The fault is a function of a material count with 275 assets
one step below the threshold, so "it is only 38 buildings" is a statement with a short shelf
life — and R-W2b is the parcel that would end it.

**A SECOND QUESTION THIS PARCEL SHOULD ASK RATHER THAN ASSUME.** R-W5a measured that all
building batches share one `MeshStandardMaterial` with *"no map of any kind"*. On 38 shipped
assets there IS a map. Whether R-W5a's numbers were taken against the source tree or the
published mirror decides whether that finding is unaffected or partly measured on files that no
longer exist in that form — ask it before quoting either.

### K26 — every building card links to a dossier that is not published · **DONE 2026-08-16 · 332 links, 332 of them 404, and 30 that should never have been links**

**Phase:** lane 1 (renderer or publish) · **Effort:** S

**The 404 is measured rather than reasoned about**, because the whole fault is that it can only
be seen from outside the repository:

```
200  https://github.com/kevinrhaas/custom/blob/main/chicago/4d/docs/RESEARCH/sauganash_hotel.md
404  https://kevinrhaas.github.io/custom/chicago/4d/docs/RESEARCH/sauganash_hotel.md
```

The second URL is what the card offered. **332 cards, not 276** — the parcel was written when the
town was smaller — and every one of them broken on the deployed site for as long as the site has
had cards on it.

**Route 2 was taken, as the parcel expected: the link is absolute and goes to GitHub**
(`popup.js` `DOSSIER_BASE`), which renders the markdown with its tables and images rather than
downloading it. `main` and not `dev`, deliberately — that is the branch a visitor's copy was
promoted from, so a dossier written on `dev` links to a page that appears when the promotion
lands, carrying the tier's existing lag rather than a second one. **Measured at 0 today:** all 55
distinct dossier paths the cards currently link are already on `main`.

**What the parcel did not predict is the 30, and they are the better half of the finding.** The
compiler asserted the path by convention — `docs/RESEARCH/<id>.md` for any record with no
reconstruction block — and never asked whether the file was there. It is right about 302 records
and wrong about 30, all of them **documented** buildings whose write-up nobody has done: the
courthouse, the log jail, the estray pen, St Mary's, the Temple Building, the Presbyterian church,
Kinzie & Hunter's warehouse. So the convention generated a link that looked exactly like the 302
working ones and led nowhere. `compile_scene.research_doc()` now resolves the path against the
repository and emits `""` where nothing is written, and the card says *no dossier written for this
building yet* instead of offering a link that breaks. That is route 3 applied to the 30 records
route 3 was actually right about, and it is not a competing answer to route 2 — the two questions
are "where is a dossier read" and "is there one".

**Both halves are gated, structurally and offline** — `tools/check_dossier_links.py`, run by
`check.sh`. Every non-empty `research_doc` must be a file here (absolute, not a ratchet: a card
either links to something that exists or does not link), and `DOSSIER_BASE` must be an absolute
GitHub blob URL ending in this app's own location inside the repository, with nothing handing the
card a relative base back. **Proved in four directions before being trusted:** a planted dead
path, a `DOSSIER_BASE` reverted to `'../../'`, an app prefix moved to `chicago/5d/`, and a
`docBase: '../'` override restored in `main.js` — each red, and green again after.

**The smoke assertion it replaces is the reason this survived**, and it is worth stating as a
lesson rather than a fix. `popup links the research dossier` tested the card's TEXT for the path,
and the text was right on every run for months while every link was a 404. It now reads the
`href` and asserts it **leaves this origin** — a property nothing served from the payload can
satisfy — plus the discriminating case beside it: `temple_building`, one of the 30, must offer no
dossier anchor at all.

**Precedent that was already here.** `validate.py` has asserted since it was written that an open
question's `dossier.file` "is not a committed file" is an error, and that its anchor exists in
that file. The building card's pointer — 332 of them, the ones a visitor actually sees — was
never asked either question.

**The 30 stay a research debt and are named by the gate on every run**, so the number is loud
rather than absent. Writing them is research, not this parcel.

**Contract:** `research_doc`'s empty case is documented in `docs/GLB-CONTRACT.md`; the field is
unchanged in name, shape and reader, so this is an extension of the sidecar's stated meaning
rather than a change to it.

Each sidecar carries `research_doc`, and `popup.js` renders it as a link — `docBase +
s.research_doc`, so `docs/RESEARCH/<id>.md` relative to the walkthrough. **`tools/publish.sh`
deliberately does not publish `docs/`** ("the uncompressed GLB masters, the research dossiers and
the raw dataset all stay in the repo and out of the payload"). So on the deployed site **all 276
cards link to a 404**, and the card that says the least — an invented building whose whole defence
is the write-up behind it — is the one whose link is worth the most.

In the repo it is worse than a blanket 404 and better than nothing: **215 of 276** dossier paths
exist, 61 do not. Thirty of those 61 are documented buildings with no dossier written yet (a
research debt, not this parcel); the other 31 were K21's, and now point at the dossier that
actually covers them.

**It is a decision before it is a fix, which is why it is not folded into either.** Three
candidates: publish `docs/RESEARCH/` (it is markdown a browser will not render, so it wants a
viewer); link to the file on GitHub (leaves the site, works today, one line); or have the card show
nothing where the dossier is unreachable rather than offering a link that breaks. The middle one is
cheapest and honest. **Whatever is chosen, a gate should assert that a card's dossier link
resolves** — a link nobody clicks in the dev tree is exactly how this survived.

### K28 — may one block raise a trade's count twice? · **DONE 2026-08-16 — three questions, three clauses, two gates, and not one record moved**

**The settlement, and it deliberately does not run conservative three times.** The three
questions this box had accumulated are one question — *how fast may a drawing move a claim about
the town* — so they were settled together, and the answer is **permissive on the table and strict
on the rate**:

| | question | answer |
|---|---|---|
| **(i)** | are tests 2 and 3 a set of PAIRS or two projections of one table? | **projections** — the pair reading is **refused** |
| **(ii)** | may one block raise a trade's count twice? | **no** — one adoption per trade per block parcel |
| **(iii)** | does test 1 mean the trade's own text, or method rule 3's list? | **its own committed text** |

**(i) is refused on rule 6's own standard, not on a preference.** Requiring the pair refuses the
**fourteenth labouring household** — T-A4's D1 log cabin in the WEST Division, adopted when this
layer housed labourers west of the river only in D2 shanties, which is exactly the projected form
— and rule 6 names that adoption as one of the **four decisions its third test recovers**. The
same paragraph says a test which has to be told the answers is a preference and one that recovers
them is a rule. The pair reading has to be told one of the four. What the projections admit is
measured rather than waved at: `tools/measure_adoption_tests.py --pairs` prints **20 (family,
division) pairs across 8 trades** that the projections admit and this layer houses none of.

**(ii) is what makes (i) safe, and the objection to it is the reason for it.** A block is an
artefact of the drawing rather than a unit of the town — the same two roofs dealt to two blocks
would both have been adopted without anybody pausing — which is precisely why the rate has to be
capped there: without a cap, the **granularity of the plat** sets the rate at which this census
grows, and that is the fitting-the-model-to-the-drawing rule 6's first sentence exists to stop.
The projections widen WHICH roofs are eligible; the cap bounds HOW FAST any of them may move a
count.

**(iii) separates two things nine parcels had been reading as one.** Method rule 3 names four
trades whose count is argued from the building rate because no roof family bounds it; that says
where a number came from, not that the number is too low. Test 1 asks the second thing. Only the
**carpenters and the labourers** state it (`--floors`), so the laundresses' D2 and the teamsters'
D4 — T-A14's two extra candidacies, which T-A15 could not reproduce — are refused. **The remedy
is named so the refusal is not read as a closed door**: if either count really is a floor, the
place to say so is that trade's own argument, argued from the town. What is refused is a trade
acquiring a floor as a side effect of a block being dealt a D2.

**Two gates, and both bite on the exact roofs nine parcels refused by hand.** They live in
`tools/generate_inferred_households.py` and were proven against mutated copies of the programme
before merge:

- a second carpenter on `blk_south_water_wells`'s D4 → *"blk_south_water_wells adopts 2 carpenter
  households … rule 6 caps a block parcel at ONE adoption per trade (K28 clause ii)"*;
- a laundress on `blk_randolph_franklin`'s D2 → *"the laundress argument never states in its own
  committed text that its count is a floor, so rule 6 test 1 fails (K28 clause iii)"*.

The floor predicate is **imported** from `tools/measure_adoption_tests.py` rather than restated,
because a second copy of the rule in the gate path is how the report and the gate would come to
disagree about what a floor is.

**NOTHING MOVED, AND THAT IS THE RESULT RATHER THAN AN ANTICLIMAX.** All **21 block adoptions**
standing on 2026-08-16 are already one per trade per block, so nine parcels' habit became a rule
without a household, roof or coordinate changing. The four T-A9 candidates re-decide identically
— its D3 and D1 stay adopted, its D4 and D2 stay refused, now under clause (ii) rather than under
a reading — and T-A4's fourteenth labouring household stays adopted, under clause (i). What
changed is that the next block cannot drift: the refusal is code.

**Files:** `data/reconstruction/1835_inferred_household_programme.json` (rule 6) ·
`tools/generate_inferred_households.py` (the gates) · `tools/measure_adoption_tests.py` (it no
longer tells its reader the question is open) · `docs/LIBERTIES.md` L112 · `docs/STATUS.md`.

**The parcel as written follows.**

### K28 (spec) — may one block raise a trade's count twice? · **from T-A9 · Effort: S — a decision, then a `method` clause and a gate**

> **THE ID IS USED TWICE AND THIS IS THE ROADMAP ONE.** The published-mirror gate that landed as
> PR #147 ("gate the published mirror against its own source", recorded at the top of
> `docs/STATUS.md`) also shipped under the name K28 and has no ROADMAP entry of its own. Every
> `K28` citation in `docs/LIBERTIES.md` (L100, L101) and in the census arguments of
> `1835_inferred_household_programme.json` means **this** parcel — the rule-6 question below.
> Noted by T-A10, which met the collision while citing it; renumbering landed work is not a block
> parcel's call.

**Phase:** lane 2, data and tools · **Runner:** improve-runner (no Blender)

Rule 6 (the household programme's `method` list) admits an anonymous block roof into the
inferred-household census where three tests pass: the trade's committed argument calls its own
count a floor, the roof's family is one this layer already houses that trade in, and the roof's
division is one it already houses that trade in. **It says nothing about how many roofs of one
block a single trade may take**, because until T-A9 no block had offered the case.

`blk_south_water_wells` offered it twice over. Four of its six dwellings pass for one trade or
the other: the **D3 and the D4** for carpenters (this layer houses one carpenter household in a
D4, in the North Division) and the **D1 and the D2** for labourers (it houses four labourers in
D2s). T-A9 adopted one per trade and refused the other two, on the reading that rule 6's own
opening sentence — *the mix is a claim about the TOWN rather than about what has been drawn* —
forbids a block's deal from raising a trade's count twice. That is written into both census
arguments and into `docs/LIBERTIES.md` L100 **as a choice**, so the next parcel can read it back
and disagree with it.

**Why it is not obvious.** Against the cap: the census argues the trade's count from the town's
building rate and its documented volumes, so letting the drawing move it is fitting the model to
the evidence — and the tests are per-ROOF, so a block dealt three D1s would take three labouring
households on a rule that never meant to grant them. For the cap being wrong: method rule 5 says
house every household, and a household this layer has already argued for and cannot house is a
worse outcome than two adoptions on one block; a block's family deal comes from a schedule that
knows nothing whatever about this census, so two passes on one block is a coincidence rather than
a bias; and the eight roofs of a block are not a meaningful unit — the same two roofs dealt to
two blocks would both have been adopted without anybody pausing.

**THE QUESTION IS BIGGER THAN THIS ENTRY SAYS — T-A14, 2026-08-15, and read this before
claiming.** Six blocks have written their refused D4 and D2 up as *second* roofs for the carpenters
and the labourers. They are also the **first** roofs of the **teamsters** (D4) and the
**laundresses** (D2) — the other two of method rule 2's four unbounded trades, each housed in that
one family and in no other, each already placed in the South Division, and so each passing all three
of rule 6's tests on those very roofs. No parcel had ever named them. **Sixteen anonymous D2 and D4
roofs stand in the South Division under exactly that description**, and every one of the six
"conservative refusals" was therefore a refusal of four candidacies while recording two. So the cap
question is only half of it: the other half is **whether rule 6 may hand a roof to a trade whose own
argument never asked for one**, which is the thing that would actually grow the census as a side
effect of a drawing. A decision that settles the cap and leaves this open settles nothing.

**AND THERE MAY BE NOTHING TO CAP — T-A3h, 2026-08-15, and read this before claiming.** Every
second-roof candidacy this lane has recorded is the carpenters' **D4** or the labourers' **D2**, in
the **South** Division, and **neither is a pair this layer has ever housed**. It houses one carpenter
in a D4 and that household stands in the NORTH Division; it houses four labourers in a D2 and all
four stand in the NORTH or the WEST; every carpenter and labourer it houses in the SOUTH is in a D3
or a D1. The verdicts hold only because rule 6 says *the three tests are independent*, so test 2
reads the set of families and test 3 the set of divisions and a roof passes on a family from one
division and a division from another family. `tools/measure_adoption_tests.py --pairs` prints it:
**20 pairs across 8 trades are admitted by the projections and housed by nothing**, and test 1 leaves
exactly **two** of them adoptable — which are precisely the two roofs sixteen refusals have been
about. So the cap question may be a question about a set of candidacies that a pair reading would
empty.

**It does not follow that the pair reading is right, and the counter-evidence is in the census
already.** Requiring the pair refuses the **fourteenth labouring household** — T-A4's D1 in the WEST
Division, adopted when this layer housed labourers west of the river only in D2 shanties, and argued
in exactly the projected form. Rule 6 names that adoption as one of the four its third test
*recovers*. A reading that breaks the rule's own calibration set needs an argument, not a
preference. **This parcel must therefore settle THREE things and not two**: whether the table is
pairs or projections; whether there is a cap (and it may be moot); and whether a trade that never
asked for a roof may be handed one. Neither T-A3h nor any block parcel decides it — measuring is
what a block parcel may do.

**Acceptance:** rule 6 gains a fourth clause **or an explicit statement that there is no cap**,
in the programme's own `method` list; **it also states whether a roof may be adopted by a trade
that has not asked for one, because T-A14 showed the two questions are the same question**, and
**whether tests 2 and 3 are read as a pair or as two projections, because T-A3h showed the cap
question may be empty without it**; `tools/generate_inferred_households.py` gates whichever is
chosen, so the answer is code rather than a habit; the four T-A9 candidates are re-decided under it
and the two refusals either stand with a reason or are adopted; **T-A4's fourteenth labouring
household is re-decided too, because a pair reading refuses it**; `tools/check.sh` green.

### K29 — the schedule deals log cabins to the town's commercial frontage · **UNCLAIMED · from T-A8 (L99) and T-A9 (L100)**

**Phase:** lane 2, data only · **Runner:** improve-runner (no Blender) · **Effort:** M

**L99 said this had been opened as a ROADMAP parcel and it had not.** The ID that entry names
was already carrying the confidence-band parcel, so the question has been sitting in a liberty
with no work item behind it since 2026-08-15. This box is that work item; L100 carries the
corrected pointer.

The 665-roof programme apportions families **by district**. It has no notion of what a street was
for, so every time this lane reaches a South Water block the schedule deals it ordinary
dwellings — `blk_south_water_franklin` got five including a D2 plank shanty, and
`blk_south_water_wells` got six including a D1 log cabin and a D2 shanty. South Water Street was
where the town's stores, forwarding houses and warehouses stood in 1835; every documented roof on
or beside both blocks is one of those. Three South Water blocks remain open and the same thing
will happen on each.

**This is a re-apportionment, not a block parcel**, which is why neither T-A8 nor T-A9 did it:
T-A6 and T-A7 both started as blocks and finished as schedule changes, and the two cannot share a
run. The shape is a frontage term in `tools/reconcile_665.py` — a block face's street decides the
family mix it may be dealt, with the commercial families (C, F, W) weighted onto the business
front and the meanest dwelling families weighted off it — argued from the reconstruction
specification's own street hierarchy and from the documented commercial roofs already standing
there, not invented as a preference.

**It does not license moving anything already standing.** The blocks T-A8 and T-A9 built keep
their roofs; a re-apportionment changes what the schedule DEALS, and L99 and L100 stay on the
record as admissions about the two blocks that were filled before the term existed.

**Acceptance:** the frontage term is derived from a committed source rather than authored as a
constant; `tools/reconcile_665.py --check` re-derives; the family totals of the 665-roof
programme are unchanged in aggregate (this moves families between schedule units, it does not
raise or lower the target); the three open South Water blocks visibly change deal; `check.sh`
green.

### K30(a) — the distribution, measured · **DONE 2026-08-16**

**It is 29 buildings, not three and not five, and every one of them is documented.** The
question is a command now — `tools/measure_corridor_intrusion.py` — and `tools/check.sh`
carries it, so the figure cannot silently grow.

**The headline table.** 29 of the town's 332 placed phases lap one of the 13 platted
corridors; 16 have their **centroid** in one, which is T-A7's test; 9 have their authored
**position point** in one.

| street | records | deepest | shallowest |
|---|---|---|---|
| south_water | 14 | **12.10 m** | 0.03 m |
| randolph | 2 | 11.45 m | 3.48 m |
| clark | 2 | 4.54 m | 1.92 m |
| state | 2 | 3.97 m | 1.98 m |
| lake | 4 | 1.63 m | 0.19 m |
| dearborn | 2 | 1.75 m | 0.97 m |
| wells | 1 | 1.44 m | — |
| canal | 2 | 0.85 m | 0.56 m |

**Finding 1 — the fault is entirely in the hand-placed layer, and the placement gate holds
absolutely.** All 29 are `research`-layer records. **Zero** of the anonymous reconstruction
roofs and **zero** of the inferred-household roofs lap any corridor, across 332 placed
phases. Every generator has asked `plat_corridors.intrusion()` before placing anything since
K7, and the assertion this parcel commits is therefore **absolute, not a ratchet**: a
generated roof in a roadway is a regression, never a debt. Both halves of the gate were
broken deliberately before being trusted — a documented building moved 6 m (caught,
`0.19 → 6.19 m`) and a generated roof moved into the Washington corridor (caught, `must be 0`).

**Finding 2 — T-A9's and T-A12's "all five are on South Water" does not survive the full
set, and the depth distribution replaces it with something sharper.** The 29 are on **eight**
streets, so a centreline-or-width error on one stretch cannot be the whole story. But the
depths are **bimodal, with a clean empty gap between 1.98 m and 3.48 m**: 17 records deep,
12 shallow, nothing in between. **13 of the 17 deep ones are South Water.** The shallow tail
— ≤ 1.98 m, on Lake, Dearborn, Canal, Wells, Clark and State — is exactly the "metre or two
proud of its own frontage" T-A7 described, which is inside the tolerance a derived corridor
and a traced centreline can honestly disagree by. The deep cluster is not.

**And the gap is very nearly the centroid test.** Every record deeper than 3.48 m has its
centroid in the corridor and every record shallower than 1.98 m does not, with **exactly one
exception**: St Mary's church, 3.97 m deep with its centroid clear. So T-A7's fourteen and
this parcel's depth distribution are two views of one population, not two findings.

**Finding 3 — T-A7's "fourteen" does not reproduce, at its own commit.** Re-run at
`52641c46`, the commit that states it, the centroid test gives **16**, and the same 16 it
gives today. The set has not grown by a single record since — as designed, because every
block parcel since is generated and gated — so the discrepancy is not the town growing. It
is a hand-derived number that was never a command, the same failure T-A14 found in T-A13's
frontage counts and for the same reason. Two of the four buildings T-A7 names are also
quoted against the wrong street in the write-ups (the courthouse as Randolph, the Newberry &
Dole warehouse as South Water): a centroid at an intersection is inside **two** corridors,
and nothing said which one to print. The tool records every corridor a point is in.

**Finding 4 — the one systematic cause that could be tested without new sources was tested,
and it is REFUTED.** `docs/GLB-CONTRACT.md` fixes the record's position at the footprint
polygon's own origin — *"NOT the centroid and NOT the bbox corner"* — and 332 of the 333
committed footprints put local `(0, 0)` at a **vertex**. So a building derived to "the
south-west corner of South Water and LaSalle" is drawn with a *corner* on that point and its
whole body extending in whatever direction the polygon and its rotation send it. That is a
plausible enough mechanism to look like the answer, and **20 of the 29 have an anchor point
standing on perfectly legal ground while the body reaches into the street.**

It is still not the cause. Re-measured with every footprint **centred** on its own anchor
instead of cornered at it, the fault does not go away: 5 records clear entirely, 14 get
shallower — and **10 get WORSE**, the Tremont House by +7.59 m and the Exchange Coffee House
by +6.97 m. Recentring is not the fix, and the anchor convention is not the fault. K30(b)
inherits a refuted suspect rather than an untested one, and the refutation is a command —
`--recentre` — rather than a paragraph, for the reason finding 3 gives.

**What is NOT concluded.** Nothing here says whether the corridor, the position, or 1835
itself is wrong, and no building was moved — the deep cluster is on the street whose modern
equivalence (`osm_streets_2026`, cited by 19 of the 29) is Wacker Drive, a boulevard built on
filled river frontage, and testing that is source work. **One record is deliberately left in
the table and is not a defect**: `slough_log_bridge`, 0.03 m into South Water. A bridge
carrying a street belongs in that street's corridor, and a category rule for street furniture
is K30(b)'s to write, not a number to quietly exclude.

**Files:** `tools/measure_corridor_intrusion.py` (new) ·
`tools/corridor_intrusion_baseline.json` (new, derived) · `tools/check.sh` ·
`docs/ROADMAP.md` · `docs/STATUS.md` · `renderers/web/js/changelog.js`. **No data record,
coordinate, dimension or confidence moved.**

### K30(b) — attribute the deep cluster to a cause, and decide what moves · **DONE 2026-08-16**

**THE CAUSE IS THE DRAWING, NOT THE GEOREFERENCE, AND IT IS A COMMAND —
`tools/measure_corridor_intrusion.py --reflect`.** The suspect this entry named is refuted;
the one that survives explains **all 17** records in the deep mode, and the residual it
leaves is measured rather than argued. **No coordinate, dimension, footprint or confidence
moved in this parcel.** Nothing was invented, so `docs/LIBERTIES.md` gains no entry.

**Finding 1 — the Wacker made-ground hypothesis is REFUTED, and the refutation is
arithmetic.** If the committed 1835 centreline were displaced from the modern control the
placements were derived from, every South Water record would be displaced by that amount.
It is not: the anchors of the 13 deep South Water records stand **11.64–15.30 m** from the
committed centreline against a platted half-width of **12.192 m**, so the corridor and the
placements agree to about a metre, and the disagreement has **both signs**. A displacement
large enough to explain a 4.51–8.17 m intrusion would have to be 4.51–8.17 m. It is not
there, and made ground is not the answer.

**Finding 2 — the cause is that the body is drawn across the frontage its own point was
derived to, and it is universal.** Two conventions that were never reconciled with each
other:

- The **derivation** convention puts the record's point on its FRONTAGE. The position notes
  say so in as many words — *"the modern intersection centre was read from OpenStreetMap and
  the footprint offset 12.2 m, half an 80 ft platted street"* — and the measured offsets
  above are that half-width.
- The **drawing** convention puts local `(0, 0)` at the polygon's minimum corner, so a body
  grows NORTH and EAST from that point. **331 of the 333 committed footprints do this.**

A south-side building whose point is on the south kerb, drawn with its body growing north,
is therefore drawn **into the roadway by its own full depth**. All 13 deep South Water
records declare themselves on the south side of the street, and all 13 are drawn northward
from a point at the kerb. Across the whole table, **all 17 records in the deep mode have
their body drawn toward the street from their own anchor.**

**The counterfactual that tests it is a REFLECTION, not K30(a)'s recentring** — the same
record with its body on the other side of the frontage it was derived to, rather than moved
half its own depth. `--reflect` is that command:

| | as drawn | reflected |
|---|---|---|
| `jh_kinzie_forwarding_store` | 6.87 m | **0.00** |
| `frederick_thomas_shop` | 6.25 m | **0.00** |
| `pruyne_kimball_drugstore` | 5.55 m | **0.00** |
| `log_jail` | 3.48 m | **0.00** |
| `newberry_dole_slaughterhouse_south_branch` | 11.45 m | **0.00** |
| `h_jones_store` | 8.17 m | 0.65 |
| `chicago_american_office` | 6.91 m | 0.12 |
| `carpenter_south_water_store` | 6.62 m | 0.59 |
| `madore_beaubien_house` | 5.98 m | 0.35 |
| `harmon_loomis_store` | 5.31 m | 0.30 |
| `chicago_democrat_office` | 5.11 m | 0.05 |
| `peck_store` | 4.51 m | 0.24 |

**12 of the 17 deep records fall under 1 m**, and 11 of the 28 buildings clear the corridor
outright. K30(a)'s recentring was the wrong operation on the right suspect: it moves a body
half its depth, which cannot clear a fault whose size IS its depth, and that is why 10
records got worse under it.

**Finding 3 — THE RESIDUAL LAW, which is the shallow tail's answer (item 3) and settles it
without moving anything.** Once the body is drawn on the correct side of its own point, the
depth still left in the roadway **IS how far that point stands inside the corridor**, to
within **0.10 m** across the six records the law applies to. The two terms are separable and
they are different sizes:

- **The drawing term** is metres — a building's own depth, 4.51 to 8.17 m on South Water.
- **The point term** is **0.35–1.69 m**, and that is exactly what a corridor derived from a
  module and a centreline traced by hand disagree by.

So the shallow tail is **not to be fixed**, as this entry suspected, and now for a measured
reason rather than a guess: `tremont_house_1` (1.75 m drawn / 1.69 m point), and
`exchange_coffee_house` (1.44 / 1.39) and `western_hotel` (0.85 / 0.85) are their point's
penetration and nothing else. **Their bodies are already drawn correctly** — reflecting them
is the wrong operation and sends them 12 m into the road, which is the check that the law is
about the point and not about the drawing. Eight further shallow records are corner clips at
intersections, where two corridor rings overlap and a polygon corner reaches into the one it
does not front. **Twelve nudged buildings would have bought nothing.**

**Finding 4 — three deep records are NOT the frontage fault and are named rather than
averaged in.** `newberry_dole_warehouse` (12.10 m, reflects to 11.97) has its point **7.00 m
inside the corridor**, in the INNER half — it is not a frontage placement at all, and its own
note says its bank is disputed between two readings this project has not settled.
`hogan_store` (10.06 → 7.95) is derived to the Lake/Market junction at the wedge where Lake
and South Water converge, so it laps a street it was not placed against. `temple_building`
(5.49 → 2.38), `cook_county_courthouse_1835` (4.54 → 3.69) and `st_marys_church` (3.97 →
3.00) improve but do not clear. Each is its own question and none is answered here.

**Item 2 — the street-furniture rule, written and gated.** A bridge in a street corridor is
the bridge doing its job. `slough_log_bridge` (0.03 m into South Water) is now
**categorised, not deleted**: the row stays in the table, stays in the baseline and stays
ratcheted, and is reported as furniture rather than counted among the 28 buildings drawn
standing in a street. The rule is derived from the record's own `archetype` **and**
`function` — a carrying-way archetype with a crossing function — and **never from a list of
ids**, because an id list is an allowance a later parcel can quietly extend. The obvious
abuse is to make a store into a bridge, so **the gate now refuses any category change**:
re-labelling `peck_store` as `bridge_timber` + `street_crossing` was tried before the rule
was trusted and the gate caught it (`changed category building -> furniture`).

**What K30(b) deliberately does NOT do: it moves nothing.** The repair is a footprint change
on 13+ records — it changes every affected mesh, so it needs a bake this runner cannot run —
and "the reflection clears the corridor" is evidence about the cause, not authority to
redraw a documented building. That is **K30(c)**, below. The standing prohibition held: a
position with a source still outranks a corridor this project derived.

**Files:** `tools/measure_corridor_intrusion.py` (`--reflect`, the furniture rule, the
category assertion, `centreline_frame`) · `tools/corridor_intrusion_baseline.json`
(additive only — **no depth changed**) · `docs/ROADMAP.md` · `docs/STATUS.md` ·
`renderers/web/js/changelog.js`.

### K30(c) — redraw the bodies onto the correct side of their own frontage · **REFUTED 2026-08-22 by K30(d) · do not run this repair · from K30(b)**

**Phase:** lane 2, data + geometry · **Runner:** NOT the improve runner — needs `bake.sh`

K30(b) attributed the deep cluster and committed the counterfactual as a command. This is
the repair, and it is a **footprint** change, not a position change: the records' points are
right and their sources are untouched. For each record `--reflect` clears, the polygon's
local origin moves from the corner nearest the street to the corner away from it, so the
body grows away from the frontage instead of across it. Every affected mesh regenerates, so
this parcel cannot go green on the improve runner.

**Three things it must not do.** It must not move a point — the intrusion that survives is
the residual law's term and belongs to the corridor, not to the record. It must not touch
the five records finding 4 names; they are separate questions. And it must not treat
`--reflect`'s output as the answer to copy: the reflection is a test of the cause, while the
repair is authoring the correct anchor corner for each polygon, which is a per-record
reading of what that record fronts.

**Acceptance:** the affected footprints re-authored and baked; `--reflect` and the baseline
re-run and the repair banked with `--write-baseline`; the residual on each repaired record
equals its point's penetration to the tolerance finding 3 measured; `tools/check.sh` and
`tools/smoke_renderer.mjs` green; nothing in `docs/LIBERTIES.md` unless something is invented.

### K30(d) — the deep cluster is the corridor moving, not the bodies · **DONE 2026-08-22 (T-0009)**

**K30(b)'s CAUSE IS REFUTED, AND K30(c)'S REPAIR IS THE WRONG OPERATION ON EVERY RECORD IT
NAMES.** The refutation is arithmetic and it is a command —
`tools/measure_corridor_intrusion.py --anchors`. **Nothing was moved, nothing was baked, and
no confidence changed**, which is the whole point: T-0009 would have redrawn twelve documented
buildings off the frontages their own committed control was offset to.

**Finding 1 — the flag K30(b) read cannot tell the two arrangements apart.** `body_toward_street`
is true when the footprint's centroid is on the street side of the record's anchor. Two
completely different drawings make it true:

- the **anchor at the KERB**, with the body growing across the frontage into the roadway by its
  own full depth — the fault K30(b) described; and
- the **anchor at the BACK corner**, set back from the frontage by the footprint's own depth so
  that the body grows forward and its street-facing **face** lands on the frontage — a correct
  drawing.

**Finding 2 — it is the back corner on all 17, and `--anchors` is the test.** Measure how far the
anchor stands from the corridor centreline against how far the footprint's two faces stand from
it: if the anchor coincides with the NEAR face the point is at the kerb, if with the FAR face the
point is the back corner. **0 of the 17 records in the deep mode have the point on the kerb
face.** The only three that do are `tremont_house_1`, `exchange_coffee_house` and `western_hotel`
— which are exactly the three K30(b) finding 3 named as *already drawn correctly and ruined by
reflection*. So both conventions are in the dataset, and K30(b) had them the wrong way round.

**Finding 3 — the dataset says so in its own words, and a gate already checks it.** The
machine-checkable `position.derivation` blocks constrain a FACE to a kerb, never the anchor:
`sauganash_hotel`'s reads *"the 8 m the note describes as 'the footprint's own depth' is not a
term here — the depth is in the polygon, so the constraint is on the face"*, and
`tools/validate.py::check_position_derivations` recomputes five placements from
`data/traces/street_control.json` on every commit. The prose notes of the twelve agree, and
their sums reproduce to the centimetre:

| record | what its note says | check |
|---|---|---|
| `peck_store` | *"12.2 m west and 12.2 m south of it less the building's own width and depth"* | origin N 4637388.28 committed 4637388.3; north face = LaSalle centre − 12.2 |
| `chicago_american_office` | *"12.2 m south less the depth so its north face is on the South Water frontage"* | face = Dearborn centre − 12.2, exact |
| `madore_beaubien_house`, `harmon_loomis_store`, `chicago_democrat_office` | the same sentence | exact |
| `h_jones_store`, `jh_kinzie_forwarding_store`, `carpenter_south_water_store`, `pruyne_kimball_drugstore` | *"the south kerb taken 12.2 m south of it"*, the kerb interpolated between two intersection centres | face on the interpolated kerb to **0.01 m** in all four |
| `frederick_thomas_shop` | 33.5 m east of the American office's origin, *"on the same frontage"* | inherits a back corner; its shallower depth leaves the face 1.5 m behind the line |
| `log_jail` | the square's NW inside corner, *"offset 12.2 m into the block on each axis"* | north face = 4637130.78, the corner itself, exact |

**Finding 4 — the real cause is committed, and the street record states it.**
`data/streets/1835.json`, `south_water`: *"east of Franklin the line follows the modern Wacker
control used by the structure placements **but is shifted into the dry half of the platted
riverfront corridor**."* `plat_corridors` derives the legal corridor by offsetting that committed
centreline, so shifting the centreline silently re-plats the street. Measured against the
intersection centres the ten placements were offset from, the committed line stands **4.3–8.8 m
south** of them — Franklin −8.56, Wells −8.80, LaSalle −4.30, Clark −4.90, Dearborn −6.20 m — and
that displacement, not any drawing, is the 4.51–8.17 m the ten records lap. K30(b)'s finding 1
looked for a displacement of that size and concluded it "is not there" because it compared the
anchors with the half-width; the anchors are back corners, so that comparison could not see it.

**And the shift is not a mistake either, which is what makes this the owner's decision.**
`chicago_american_office`'s own note records the corroboration from the other side: the traced
1834 south bank runs **18.7 m north of its north face**, so a corridor centred on the modern
Wacker control puts its northern half in the river. The street was pulled south onto dry ground;
the buildings were placed against the unshifted control; nobody reconciled them. Three
resolutions exist and the research settles none of them:

1. **The buildings follow the street** — ten documented positions move 4–9 m south. A position
   change on sourced records, which is exactly what AGENTS.md forbids an agent to do alone.
2. **The corridor stops following the drawn line** — the platted corridor is a legal line off the
   plat and arguably cannot be moved to dodge water; only the travelled TRACK should have shifted.
   `plat_corridors` would then take its centreline from the control rather than from the street's
   drawn path.
3. **Neither** — 1835 South Water genuinely had its north half over the water as wharf, the
   frontage is where the records put it, and the intrusion table is measuring a corridor the town
   never had on that reach.

**Files:** `tools/measure_corridor_intrusion.py` (`--anchors`; `--reflect` re-labelled a
counterfactual) · `docs/ROADMAP.md` · `chicago/4d/tickets/T-0009-*.md` (blocked on the owner) ·
`renderers/web/js/changelog.js`. **No structure record, footprint, coordinate, confidence or
baseline was touched, and `docs/LIBERTIES.md` gains no entry — nothing was invented.**

#### K30(d) RESOLUTION 1 IS TAKEN FOR SIX OF THE ELEVEN — 2026-08-24, T-0127 → T-0188

**The owner answered it, in a ticket, in his own ask.** K30(d) left three resolutions and said
resolution 1 — *"the buildings follow the street"* — is *"a position change on sourced records,
which is exactly what AGENTS.md forbids an agent to do alone"*, and T-0009 has sat `blocked-owner`
on it since. **T-0127** (`requested_by: owner`, `seen: true`) is that decision: *"ten documented
buildings on that side were placed against the MODERN kerb, read off OpenStreetMap, rather than
against this project's own platted line… **Reconciling them with the committed plat closes those
gaps and is worth doing on its own terms** — the disagreement is a finding about the dataset, not
about the sidewalk."*

**What T-0188 did with it.** Measuring the walk band found **eleven**, not ten — `temple_building`
is the eleventh and no earlier count had it. **Six were reconciled**: `harmon_loomis_store`,
`madore_beaubien_house`, `peck_store`, `chicago_democrat_office`, `temple_building` and
`jh_kinzie_forwarding_store`, each translated along its block face's inward normal until its north
wall stands 1.50 m back from the committed frontage line — the margin
`generate_block_infill.py` already gives every reconstructed unit on those faces. **No along-street
position moved and no confidence grade moved**: this is each record's OWN stated method
(*"the south kerb taken 12.2 m south of it… so the north face sits on the South Water frontage"*)
re-run against this project's committed centreline instead of the modern OpenStreetMap one, which
is the reference frame K30(d) finding 4 identified as the whole cause. Town-wide corridor laps go
**29 → 26**, and the six drop from 4.51–7.48 m to 0.16–0.21 m, on a cross street.

**Five could NOT be, and the blocker is not the owner's this time.** `h_jones_store`,
`carpenter_south_water_store`, `pruyne_kimball_drugstore`, `chicago_american_office` and
`frederick_thomas_shop` each seat, once reconciled, on a platted lot the 665-roof schedule has
already dealt to the anonymous South Water frontage run, and `generate_block_infill.py` refuses to
deal a roof to a lot that already carries one. Each was tried alone to prove it was its own
blocker. They are refused **in writing, per store**, in their own `position.note` and in
`data/frontage/town_street_edge.json`'s `refused`. **T-0189** owns the untangling.

**T-0009 is untouched here** — it is a `needs_bake` ticket about 29 bodies on eight streets and its
`blocked_on` text is wider than these eleven — but its decision is now answered for the South Water
cluster, and whoever picks it up should read this heading first.



**Phase:** lane 2, data only · **Runner:** improve-runner (no Blender)

T-A7 established that a record placed from typed coordinates before the plat module existed can
stand "a metre or two proud" of its own street frontage, and measured what that does to
**occupancy**. Nobody had measured the intrusion itself. On `blk_south_water_wells`, T-A9 did:
**H. Jones's grocery stands 4.5 m, Philo Carpenter's South Water Street store 6.6 m and P. F. W.
Peck's store 8.2 m inside the platted South Water corridor.** Jones's and Carpenter's lap no lot
of that block at all — they are wholly in the roadway; Peck's laps only lot 6, which Rufus
Brown's boarding house already holds.

**It is not a block parcel's business and it did not cost T-A9 anything** (the nearest invented
roof to any of the three is 7.99 m, against a 3 m gate), but it is a claim about the town that
nothing in the dataset states: three named, documented commercial buildings are drawn standing in
a street. Either the street's committed centreline or width is wrong on that stretch, or the
three positions are, or 1835 South Water Street genuinely had stores encroaching on it — which is
entirely possible on a frontage street of a boom town and would be a **finding**, not a defect,
if a source said so.

**FIVE CASES NOW, AND ALL FIVE ARE ON SOUTH WATER STREET (T-A12, 2026-08-15).** The last block of
the row added two: the **Chicago American office** stands **6.91 m** inside the corridor and
**Frederick Thomas's shop 6.25 m**, so **both** of that block's documented South Water buildings —
**148.6 m²** of roof between them — stand on ground the plat calls street. The five intrusions span
**4.5 m to 8.2 m** and none of them is on any other street, which is the shape a *centreline or
width error on one stretch* would make and not the shape of a uniform grid bias. It cost T-A12
nothing either (the nearest invented roof is 6.79 m against a 3 m gate), and it is still not a block
parcel's business — but the distribution this entry asked for is now half-measured, on the street
that matters, and it is pointing at one answer.

**Start by measuring all fourteen**, not these three: T-A7 counted fourteen committed records
whose centroid lands in a roadway and named four of them. The distribution is the finding — a
handful of deep intrusions on one street is a different problem from a uniform half-metre bias
across the grid, and the fix differs accordingly.

**Acceptance:** every documented structure's intrusion into every platted corridor is measured
and committed as a derived table; the three cases above are attributed to a cause with reasoning
recorded; anything invented in the resolution goes to `docs/LIBERTIES.md`; a gate reports the
figure so it cannot silently grow. **Do not move a documented building to make a number look
better** — a position with a source outranks a corridor this project derived.

### T-A3 — the second refreshed block · **DONE 2026-08-14 (`blk_randolph_dearborn`)**

**The parcel shape did repeat, and that is the finding.** Appending a block to
`data/reconstruction/1835_platted_block_parcels.json` and running the generator is the whole of
the geometry work — no coordinate is authored, no family band is retyped, and the recipe entry
took minutes. Two things came out of the repeat that a single block could not have shown, and
both are worth more than the nine roofs.

**One roof of the ten was refused, and the generator now refuses its whole family by name.** The
schedule dealt this block an I3 — civic or public-service. (The parcel as written expected H3;
the schedule is derived from what stands, so T-A2 re-apportioned it. Read the schedule, never
this entry's memory of it.) I3 resolves through the `fort_structure` placeholder, whose entire
vocabulary of building kinds is garrison words — quarters, barracks, blockhouse, magazine, store,
guard, sutler, artillery — with nothing in it for the adapted office or engine house the
crosswalk says the family spans. Massing it would have stood a garrison building in the platted
town, 750 m from the fort. The crosswalk had already written the precondition on its own entry:
the six-roof aggregate *"spans unlike functions; they must reconcile to named public records
before selecting construction"*. So `REFUSED_FAMILIES` in `tools/generate_block_infill.py` now
refuses I1, I2 and I3 by name with the committed sentence each refusal enforces, instead of the
generic *"add a form rule before a recipe uses it"* — which was an instruction to step over the
precondition. **The deferral is gated in both directions**: a roof the schedule dealt and the
parcel did not build must be named in the recipe's `deferred` list with its reasoning, and a slot
may only be deferred for a refusal the code states. A family cannot be dropped for being awkward,
and a deferral cannot be used to hide one. Both directions verified by reintroducing them.

**The lot frame was being chosen by a two-centimetre margin, and on this block it chose wrong.**
`lot_frame()` identified a lot's alley edge as the edge nearest the alley's CENTROID — and a
block's alley centroid sits at the block's own centre, so for an END lot the side lot line
running back toward that centre is nearly as close as the alley edge. On `blk_randolph_dearborn`
the two came out **38.93 m against 38.95 m**, and two of the four end lots picked the side lot
line: a building framed broadside to its own street, hanging over the neighbour. What reported it
was the lot-margin gate, at **1.44 m against a 1.5 m bound** — a millimetre-scale complaint about
a ninety-degree error, which is the shape of this defect worth remembering. Measuring to the
alley STRIP instead separates the same two edges by 0.2 m and 26.3 m. A structural check rides
with it: a lot's front and rear are its two block-face-parallel edges and are the same length to
within the plat's skew, so a 20 % disagreement means one of them is a side line and fails loudly.
**`blk_randolph_wells` cleared the old tie by 1.3 m in 37 — a 3 % margin — so nothing T-A2
committed moves**, and it was never more than the block's proportions away from the same failure.
Verified by framing this block's lots under the old rule against the new check: 2 of 8 rejected,
the two that were wrong.

**Standing roofs 242 → 251; remaining 423 → 414, 86 of them on covered ground.** Five dwellings
on five of eight lots and four yard buildings off the alley; three lots open, two on the
programme's alternating-vacancy assumption and one because the parcel refused its roof. Recorded
in L93.

**Files:** `data/reconstruction/1835_platted_block_parcels.json` (one block appended) ·
`tools/generate_block_infill.py` (`REFUSED_FAMILIES`, the deferral gate, `lot_frame`) ·
`data/structures/recon_1835_blk_randolph_dearborn_*.json` (9, derived) · `data/sidecars/1835/` ·
`assets/…` placeholder massing · `docs/LIBERTIES.md` (L93) · `docs/ROADMAP.md` · `docs/STATUS.md`

### T-V1 — the anonymous town reads as one gable stamped a dozen times · **(a) DONE 2026-08-15 · (b) NEXT UP, AND IT NEEDS ONE BAKE**

**(a) is the measurement and the rule; (b) is the sixty records, and (b) cannot go green on the
improve runner.** Read the box before quoting any uniformity number.

#### T-V1(a) — the census, the shared rule, and the door bug it found · **DONE 2026-08-15**

**The parcel is not where R-G1 said it was.** T-V1 named `south_water` — the South Division
business street — and by the time it was claimed that row had already been fixed twice over: the
phase-one South parcel samples its footprints, and every one of the twelve `phase3` platted-block
parcels samples footprint AND eave. Measured across all 218 anonymous roofs, **every twin is in
one parcel**: `phase2_north_division_initial`. Sixty roofs, twenty-three families, **24 distinct
massings — 36 of the 60 share a footprint AND an eave with another roof of their own family**.
The West approaches parcel does not sample either, and has no twins only because its twenty roofs
are spread thin across families.

**`tools/measure_massing_variety.py --gate` is the census, and it runs on every `check.sh`.** It
gates a sentence the data itself makes: 138 records say in their own footprint note that the
rectangle was `sampled deterministically` inside the family's authored band, and the gate holds
them to it — inside the band, and unique within family and parcel. Both clauses were **broken on
purpose and proved to fail** before being trusted (a 9.90 m A1 against a band topping at 6.10 m;
a duplicated phase-one D3 rectangle). Everything else it **reports and does not fail**, for the
reason in T-V1(b) below.

**The census found something bigger than the twins, and it is K25's subject rather than R-G1's.**
Every invented dimension carries the note *"Type-level choice within the &lt;family&gt; band"*, and that
sentence is the whole defence for the invention — the building is made up, but made up inside the
specification. **40 of the 218 eaves are outside the band their own note cites**: 18 in
`phase1_south`, 17 in `phase2_north`, 5 in `phase2_west`. The phase-one parcel is the sharp case,
because it samples its FOOTPRINT and carries the sentence saying so while its eave is still one
constant per family — so a record can carry a true sentence about its plan and a false one about
its wall, in the same note style, and nothing distinguished them until now. **(a) fixes none of
the 40.** It counts them, names them by id, and prints them on every build.

**One real bug, found by the arithmetic and fixed.** `DOOR_HEADROOM_M` is 2.05 m, the phase-one
privies' height, and it was applied as the eave floor for **every** door-carrying family —
including the wagon doors on W1, W2, W5, F1 and A2. A wagon door is **3.00 m in the clear** and
`outbuilding_params` refuses a wall that cannot header it. It never bit, because those families
stood at a retyped 3.42 m that happened to clear it; the moment the North parcel sampled its own
band, `recon_1835_north_w1_*` failed by name at 2.821 m. `eave_floor(family, door)` now asks
`generators/archetypes/outbuilding_params.DOOR_SIZE_M` how much room the door needs instead of
carrying a constant copied out by hand — **which is the same fault this parcel is about, in
miniature**. The block parcels' 90 records are **byte-identical** across the change: their wagon
and stable families (A1, A2) have band floors already above the new requirement.

**And the rule now lives in one place.** `tools/family_bands.py` holds `families()`,
`dimensions_m()`, `wall_height_m()`, `storeys()`, `stable_fraction()` and `eave_floor()`, lifted
verbatim out of `tools/generate_block_infill.py`, which now imports them. The block generator's
own docstring already said family geometry comes from the crosswalk and not from a generator
file; this makes that true of the second generator that needs it.

**Files:** `tools/family_bands.py` (new) · `tools/measure_massing_variety.py` (new) ·
`tools/generate_block_infill.py` · `tools/check.sh` · `docs/ROADMAP.md` · `docs/STATUS.md`

#### T-V1(b) — the sixty North records · **LANDED 2026-08-22 (T-0144), and the wall it was stuck behind is gone**

**THE CIRCULAR DEPENDENCY BELOW IS RESOLVED, and not by any of the three routes it offered.** Blender
arrived on the improve runner on 2026-08-19, so the fourth route — the one the box could not see
because it did not exist — is that the run that changes the data also bakes it. The sixty stale GLBs
were rebuilt in the same commit as the records that staled them, `tools/validate.py --stale` never
went red on `dev`, and no policy question had to be decided. Sixty `--only` bakes cost 39 seconds;
the web derivatives, which are the slow half, cost three minutes for the sixty.

Measured on the landed change, against the box's own table: duplicate instances **36 → 0**, distinct
massings **24 → 60**, eaves outside their own family band **17 → 0**. Every placement gate passed on
the sampled footprints, exactly as (a) recorded. `tools/measure_massing_variety.py --gate` now reads
the North parcel as claiming its sampling and honouring it; the dooryard planting layer re-dealt its
stems onto the new footprints in the same commit; `docs/LIBERTIES.md` **L170** records the sampling
rule's fourth parcel; `tools/audit_confidence.py --strict` is green.

**What is still owed, and it is now its own ticket (T-0145):** the roof-pitch half, deferred here for
the reason given below and unchanged by this — eleven North records carry a pitch outside their cited
band, all within half a 1:12 step of its edge, and the ridge band has to be gated in the same pass or
the fault simply moves one field over. `recon_1835_north_w5_040`'s unauthored loft rides with it.
**K25(b) and the west parcel are still owed the same repair** — 18 south and 5 west eaves outside
their cited bands — and the wall is gone for them too.

**The record below is kept verbatim**, because the reasoning was right when it was written and the
thing that changed was the runner, not the argument.

#### T-V1(b), as it stood — **the original block, kept verbatim · Effort: S to write, and it NEEDS ONE BAKE**

**The work is done and measured; what it cannot do is land here.** Wiring
`generate_north_infill.py` to `family_bands` — deriving width, depth and eave per record from the
family band instead of from a retyped constant and from `width_ft`/`depth_ft` columns in
`1835_north_division_initial_parcel.json` — was implemented and run during (a). Every one of the
North generator's placement gates passed on the sampled footprints: **no collision, no platted-
corridor intrusion, no roof off the modelled terrain, no perimeter over the 0.35 m relief
contract, and every archetype accepted its parameters.** The result, measured:

| | before | after |
|---|---:|---:|
| duplicate (footprint + eave) instances of 60 | **36** | **0** |
| distinct massings | 24 | **60** |
| eaves outside their own family band | **17** | **0** |

**IT WAS REVERTED, AND THE REASON IS A CIRCULAR DEPENDENCY THE PIPELINE HAS, NOT A DOUBT ABOUT
THE WORK.** The sixty North roofs' GLBs are canonical Blender bakes (`kind: "generated"`), not
placeholders. Changing a dimension changes the resolved archetype parameters, which is exactly
what `generators/mesh_inputs.py` hashes, so **all 60 committed meshes go stale at once** and
`tools/validate.py --all` fails — which is the dev gate, so the PR cannot merge. There is no
Blender on the improve runner and installing one is forbidden. And
`.github/workflows/chicago-4d-bake.yml` **bakes from `dev`**: it can only rebuild what has
already landed. So the change cannot reach `dev` through a gate it turns red on the way, and the
thing that would turn it green only runs after it lands.

**Do not "fix" this by re-stamping `assets/manifest.json`.** That would leave sixty meshes showing
the old building under a hash claiming freshness, which is the precise failure the staleness gate
was built for (`run_stale_check`, and the note above it). **Do not** run
`generators/inferred_placeholder.py` over them either: it stands aside for a canonical bake by
design, and the one time it did not it silently replaced 113 KB archetypes with 4.9 KB flagged
boxes and every gate stayed green.

**Three routes, for the owner to pick:**
1. **Dispatch `chicago-4d-bake.yml` against the branch** — needs the workflow's "bake from dev"
   step to accept a ref, which is a workflow edit and therefore an owner-visible change.
2. **Let the gate merge red once**, on an explicitly labelled PR, and let the nightly bake green
   `dev` the same night. Cheapest, and it costs the invariant that `dev` is always green.
3. **Pair the parcel with a bake PR** — land (b)'s data and the rebuilt GLBs in one commit,
   produced by a dispatched bake off a branch that already carries the data.

Route 2 is what the bake workflow's own note (*"a change to data is picked up by the nightly"*)
appears to assume, and nothing in `docs/PIPELINE.md` says a red merge is permitted. **It is a
policy question, not an engineering one, so it is not being decided by an overnight run.**

**The same wall stands in front of K25(b) and every other parcel that would move a dimension on
the 128 canonically-baked anonymous roofs**, which is why it is written here at length rather than
in a commit message.

**(b) still owes**, when it lands: the roof-pitch half (deferred deliberately — the crosswalk
authors pitch as `7:12-10:12` **coupled to a committed `ridge_ft` band**, so sampling pitch without
gating the ridge would put ridges outside a band their own note cites, which is the fault this
parcel is fixing); a `docs/LIBERTIES.md` entry for extending the sampling rule to a fourth parcel;
`tools/audit_confidence.py --strict` green (it was, on the reverted implementation); and the
`south_water`, `prairie_west` and `prairie_south` critic frames re-shot **after** the bake, since
before it they cannot show a difference.

#### T-V1 (spec) — the original parcel definition


**Phase:** lane 2, data only · **Runner:** improve-runner (no Blender) · **Effort:** M

R-G1's lowest station is `south_water` at **3.38**, and the reason is not the renderer. The
business street's horizon row is one gable form, at one width, one pitch and one eave height,
repeated at even spacing along the block — while the research behind those records knows a store,
an auction room, two newspaper offices and a warehouse. It cost points on **geometry (3)** and,
more seriously, on **historical accuracy (5)**: uniformity is itself a claim, and no source makes
it. The same stamp is visible on the horizon at `prairie_west` and `prairie_south`.

**The fix is a sampling question, not a modelling one.** Each anonymous record already carries a
family, and `1835_family_archetype_crosswalk.json` already carries that family's footprint band,
storey count and eave height — the same table T-A2 taught the generators to read. The placeholder
massing takes one value per family where the committed band is a **range**. Draw each record's
footprint, eave height and roof pitch from within its own authored band, deterministically from
the record id so a re-run reproduces it, and the row stops being a stamp without a single new
claim being made. **This must not widen any band, and must not invent a band for a family that
has none** — the A3 privy precedent (T-A2) stands: a family whose authored band cannot carry its
archetype fails loudly rather than being quietly raised out of its typology.

**Do not** vary orientation off the lot frame — T-A3 found what happens when a building's facing
is chosen by anything other than the lot line.

**Files:** `generators/inferred_placeholder.py` and/or `tools/generate_block_infill.py` ·
`data/structures/inf_*.json` (dimension fields only) · `docs/LIBERTIES.md` (the sampling rule is
a compression and gets its own entry) · `docs/STATUS.md`

**Acceptance:** no two anonymous roofs of the same family share a footprint and eave height
unless their bands are degenerate; every emitted value inside its committed band; the confidence
tier of every dimension unchanged (this adds variety, not knowledge); `tools/audit_confidence.py
--strict` green; and the `south_water`, `prairie_west` and `prairie_south` critic frames re-shot
and quoted. **Needs the bake for the massing to reach the site** — ship the data half and say so.

### T-V2 — the `south_water` anchor points at a field · **DONE 2026-08-16 · and the far band it was held for does not reproduce**

**Phase:** lane 2, data only · **Effort:** XS — one record, no code

R-G1 scored composition **4** at `south_water`: about 60 % of the frame is foreground grass and
the business street the anchor is named for is a 40-pixel band on the horizon. The anchor moved
from **(260, −95)** to **(329.8, 7.0)** — into the street at the Wells corner, looking east, pitch
0. **Neither half is new evidence**: the easting is the Wells junction the sixteen South Water
records are themselves offset from (quoted in their own position notes) and the northing is
`data/streets/1835.json`'s South Water centreline at that easting. **This moves a camera, not a
building.**

**IT SAT ON `hold` FOR TWO DAYS ON A NUMBER THAT OTHER WORK HAD ALREADY FIXED.** The park said the
250–600 m band **collapsed to 0.5 L\* / 30 % perceptible** from the street, and asked whether a
threshold set against an oblique view should assert that band at all — opened as T-V2b. Re-measured
on `dev` at c701833, after R-BUG3's near lift, R-BUG5b's wood and R-A1: **that band reads 2.1 L\*
and 71 %.** The question was answered by other parcels while this one waited.

**What the move is worth, and it is R-M1c again from a second direction.** Mobile, published
mirror, same runner. `nProjected` is the road in the frame; `n` is what the marker pass can see:

| `south_water` band | old stand, in the field | new stand, in the street |
|---|---|---|
| 2–40 m | **not gated** — 1 probe projects | ΔL\* 4.1, **90 %**, n 10 of 10 |
| 40–100 m | ΔL\* 4.1, 100 %, n 28 of 34 | ΔL\* 3.5, 87 %, n 15 of 15 |
| 100–250 m | ΔL\* 3.7, 100 %, n 25 of **96** | ΔL\* 2.2, **52 %**, n 42 of **67** |
| 250–600 m | ΔL\* 15.8, 100 %, n **6 of 510** | ΔL\* 2.1, 71 %, n 100 of **423** |
| **gated probes PERCEPTIBLE** | **31** | **93** |

**The old stand scored 100 % on six probes of five hundred and ten** — it could not see 98.8 % of
the band it was grading. The new stand shows **seventy-one** perceptible stretches of that band and
scores 71 %. Three times the readable road in front of a visitor, recorded as a regression. On
`nProjected`: **5.1 % → 19.0 %**. **T-V2b is therefore folded into R-M1c** — "a threshold set
against an oblique view" is the same fault as "a score divided by what an occluder left", seen from
the other end.

**Landed with two bands red.** `walker's eye` fails on 100–250 m at 52 % against 55 %; `aerial
anchor` fails and is **inherited from `dev` unchanged to the digit** (85 % / 54 %) — R-BUG5b's
knowingly-red band. No threshold moved, no band widened, no station dropped.

**Before and after are committed** at `docs/evidence/t-v2-{before,after}.png` — desktop 1280×800,
published mirror, salvaged from PR #205.

> ### The 100–250 m band may belong to K30(c), not to the light — salvaged from PR #205
>
> **The loop reached this parcel independently on 2026-08-17 (PR #205, closed as superseded) and
> found the same anchor and the same healed far band.** Two of its observations are not in the
> merged parcel and are worth more than the duplication cost:
>
> **It is this stretch of street, not the middle distance in general.** On the same run
> `lake_market` — the other station standing on a roadway — reads **3.3 L\* and 100 %** in the very
> band `south_water` fails at 52 %. So a threshold that is wrong for on-street poses is *not* the
> explanation; something about this stretch is.
>
> **And here is the candidate: 13 of the 17 deep corridor intrusions K30(a) measured are South
> Water records.** The stretch this band covers is also the stretch with buildings drawn standing
> *in the roadway* — and **25 of the 67 projected probes in that band are not seen at all**.
> A building standing on the road is a building standing on the probes. **K30(c) is the repair, it
> needs a bake, and it is #1 in NEXT UP** — so this band should be re-read after K30(c) lands
> before anyone treats it as a lighting or threshold problem.

### T-V2c — the `south_water` baseline row measures a different place now · **UNCLAIMED · UNSEEN · from T-V2 · Effort: XS**

`tools/critic_shots.mjs` drives the scene anchors through `goTo`, so T-V2 moved a **baseline
station**. Every `south_water` row in the STATUS baseline table was shot from the field stand and
the next round will be shot from the street: **two incomparable numbers under one name**, which is
precisely what the harness exists to prevent.

Re-shoot the full desktop and mobile sets and **restate** the row rather than letting the next
comparison silently straddle a camera move. Note in passing what the parked PR already measured at
the old commit — moving the anchor took **flower load 0.0575 → 0.0002** and **draw calls 109 → 94
desktop, 104 → 79 mobile**, because looking east down the street culls the prairie the old stand
faced across — so the new row should be cheaper as well as different, and a round that does not show
that has measured something else.

### T-I3(a) — the civic roofs, reconciled to named records · **DONE 2026-08-16**

**The town's public buildings with a roof on 1835-07-01 are THREE, and this project already had
all three of them** — `log_jail`, `council_house`, `chicago_lighthouse_1832`. `estray_pen` is
public and roofless. The enumeration is
`docs/RESEARCH/civic_public_buildings_1835.md`; every citation in it is Andreas, a source this
project has held since the scaffold, so **no new source record was needed and none was invented**.

**THE FINDING IS THE FOURTH BUILDING: the court-house was not built yet, and it is now out of the
scene.** 332 structures resolved into 1835 and 331 do. The record modelled it as complete on 1
July under a note saying, correctly, that nothing it had reached fixed a month. Three passages
fix it and none is earlier than the fall: the town-period narrative — *"During the fall of the
year (1835,) a one-story and basement brick court-house was erected on the northeast corner of the
square, on Clark and Randolph streets"* (Andreas I scan p. 369); the chronology, under 1835 at
**November** (scan p. 1317); and the county Recorder *"removed his office toward the end of
October to the new building recently erected by the county on the public square"* (scan p. 305).
**The dataset had said it already, in another file, for four days**: the physical-roof reconciliation gives this record `roof_count: 0` because *"Production chronology places construction in fall 1835"*, committed 2026-08-12, one day after the record that stood the building on the square — and the walkthrough's release notes carried that reading to visitors while the walkthrough drew the building. Nothing reads the two files together. The one that was right is the one with **no citation at all**.
**The citation the record had was a picture** — the scan p. 373 it cited for "a section headed
'THE FIRST COURT-HOUSE.'" is a PLATE, and those words are an engraving's caption. The narrative is
four scan pages earlier. This is the second time in this project a citation has resolved to a
heading instead of to a sentence.

**Two of the record's own hedges are settled and BOTH say it was better than it knew.** Its
position note warned that Andreas's north-east siting "is the 1837 BUILDING" and might be
contaminating an 1835 record; Andreas gives that corner to THIS building, in the sentence that
dates it, so the invented placement is where the source puts it. Its construction note ruled out
brick because "the first brick building in Chicago is 1837"; that fact is about the first brick
HOUSE (`peck_brick_house`, already excluded) and Andreas calls this court-house brick. **Neither
is applied**: a changed form value stales the placeholder mesh, geometry belongs to the nightly
bake, and a promotion made in the same commit that took the building off screen is a promotion
nobody can see. Both are recorded on the record as amendments and are the bake parcel's to apply.

**The refusal is now the research, and it is ASSERTED rather than argued.**
`tools/measure_institutional_claims.py` runs in `check.sh` and asks every committed record, not
only the ones a generator is about to write: **absolute zero** for I1 and I3 — the families are
enumerable, so zero is enforceable — and a **ratchet at one** for I2, naming
`recon_1835_north_i2_015`, the liberty L93 records rather than deletes. All three halves were
broken deliberately before the gate was trusted. `generate_block_infill.py` refused these families
on the ARCHETYPE's vocabulary; that argument stands and is no longer the load-bearing one.

**What a slot would have been spent on, and why none of it is a building.** The crosswalk says the
family spans *"jail/blockhouse; engine/service; adapted offices"*, and in July 1835 every adapted
office in Chicago was a room in a private building. The **United States Land Office** is the sharp
case: open since May 1835, transacting Beaubien's pre-emption four weeks before the scene date
(certificate 28 May, recorded 26 June) — and *"on the east side of Lake Street, between Clark and
Dearborn streets"*, where *"the office of the Registers and Receivers were usually at their
private offices"* (scan p. 313). The post office was a counter in Hogan's store, which this
project already shows. The county's own officers were private until late October. Three guards
added to `data/exclusions.json` — `us_land_office_1835`, `custom_house_chicago`,
`chicago_town_hall` — and `first_fire_engine_house` **amended**, because it dated the ENGINE and
the HOUSE is later still (contracted to Levi Blake 30 December 1835, unfinished in February 1836).

**A citation correction on the way past, worth its line because nothing visible depends on it.**
`estray_pen` dated the pen to March **1833** and cited Andreas for the year. Andreas gives 1832
twice — the narrative (*"seen in March, 1832 ... there arose upon the southwest corner of the
square, the so-called 'estray-pen' ... quite roofless"*, scan p. 365) and the chronology, where
the entry stands under the heading **1832** (scan p. 1315) — and 1833 nowhere. The month was read
off that index correctly and the year off the wrong heading. The pen stands, roofless, either way.
Its phase id stays `pen_1833`: a phase id is half of a baked asset's filename and a cosmetic
rename is not worth a bake.

**Files:** `docs/RESEARCH/civic_public_buildings_1835.md` (new) ·
`tools/measure_institutional_claims.py` (new) · `tools/check.sh` ·
`tools/generate_block_infill.py` (the I3 refusal's reason) ·
`data/structures/cook_county_courthouse_1835.json` · `data/structures/estray_pen.json` ·
`data/exclusions.json` · `data/sidecars/1835/*` · `docs/LIBERTIES.md` (L110) · `docs/STATUS.md`

### T-I3(b) — the six-roof target, which is a claim about the town and not about its public buildings · **BLOCKED ON THE OWNER · opened 2026-08-16 by T-I3(a)**

**Three of the six I3 slots are a count of nothing.** That much is settled. What is not settled is
what to do with them, and the reason an agent should not choose is the R-W4c(b2) reason: the
inventory's arithmetic is closed — every family target sums into a district-group row, every row
into a district target, every district into `roof_total: 665`, and `tools/reconcile_665.py`
asserts all three — so three slots cannot simply be deleted. There are exactly two exits and they
are **two different claims about the town**:

1. **The town had three fewer roofs than 665.** `roof_total` → 662, inside the spec's own
   `defensible_range` of [565, 765]; `institutional_public` 12 → 9; the south district 370 → 367.
   This says the authored total was over by the three phantom civic roofs.
2. **The three roofs existed and were not civic.** They go back into the pool the 665 apportions
   and are re-typed by weight into the ordinary families. This says the total is right and the
   family split was wrong.

Route 1 also makes the filename `1835_665_roof_programme.json`, the tool name `reconcile_665.py`
and a great deal of committed prose say a number the data no longer holds — not a reason to
prefer route 2, but a cost to price in. **Until the owner picks, the target stays at six and the
programme keeps scheduling I3 slots that every generator and now every gate refuses.** That is
visible, gated and honest, and it is a better failure than a number quietly changed.

### T-I3 — the parcel as written, kept for the record

**Research, not massing, and it is the parcel T-A3 refused to do by hand.** The programme
schedules six I3 roofs — civic or public-service — across the town, and the generator now refuses
every one of them until this parcel runs. What is owed is what the crosswalk asks for: which
civic and public-service buildings Chicago actually had in July 1835, where they stood, and what
they were built of. The estray pen, the jail, an engine house, an adapted office are the kinds of
thing at stake, and each is nameable or is not there.

**The rule that makes this different from a block parcel:** a named record substitutes for a
compatible anonymous roof and never increases the total, so this parcel can only ever move roofs
from the anonymous column into the named one. **Never invent a source.** A civic building for
which no source record resolves does not become `conjectural` here — it stays absent, and the
absence is recorded in `data/exclusions.json` with its citation the way every other
researched-and-excluded structure is.

**Whether an anonymous I3 may ever stand is itself part of the parcel.** If the research shows
the town's public buildings are enumerable, then the family's six-roof target is the thing that
is wrong and the programme should be corrected rather than filled. Say which, with the reasoning.

**Files:** `data/sources/*` (new, with Wayback snapshots) · `docs/RESEARCH/<id>.md` ·
`data/structures/*` or `data/exclusions.json` · `data/reconstruction/1835_building_inventory.json`
(only if the target is what moves) · `tools/generate_block_infill.py` (`REFUSED_FAMILIES`, only
once a named record exists) · `docs/LIBERTIES.md`

**Acceptance:** `tools/check.sh` green; every new attribute graded `documented` resolves to a
source record; nothing anonymous gains a civic function; L93's *How to resolve* answered in
whichever direction the evidence points.

### T-A4 — the first West Division block · **DONE 2026-08-14 (`blk_randolph_clinton`)**

**Standing roofs 251 → 258; remaining 414 → 407, 79 of them on covered ground.** Four dwellings
on four lots and three yard buildings off the alley, on the block bounded by Randolph, Canal,
Washington and Clinton. One labouring household adopted under the T-A2h rule; households
**154 → 155**, persons **190 → 191**. Recorded in L95.

**The block was not empty, and every gate here assumed it would be.** Both blocks before this one
stood vacant, so a parcel could treat all eight lots as free and be right. Three roofs of the
phase-two West parcel already stand inside this one — placed from typed coordinates before the
plat module existed, so **no record of theirs names a lot**. The generator's one-principal-per-lot
check reads only the records the parcel builds, and the three-metre separation gate does not close
the difference: **two principal roofs can stand twelve metres apart on one twenty-five-metre lot
and pass every test in the file.** Occupancy is now DERIVED from the committed footprints — a
recipe that had to be told which lots were taken would be the second opinion about the same ground
that the plat module exists to retire — and a principal slot on an occupied lot is refused by name.
Two gates ride with it: an ancillary roof must stand on a lot this parcel gave a principal roof
(a yard building behind somebody else's house is a claim about their yard), and **every lot must
be built on, already occupied, or named open with its reasoning** — the three classes were counted
in three places and nothing made them meet, so a lot could be called open in the recipe with a
house standing on it. All five refusals verified by doing each.

**Two smaller defects the first non-South block exposed.** The record's visitor-facing location
line said *"South Division"* as a literal — correct on every record that had ever existed, and
wrong on all seven of these. And `reconcile_665.py` attributed **every anonymous West Division
roof to the Wolf Point recipe**, which was the same set until this parcel: the ledger read seven
new roofs as seven of that recipe's own placements emitted out of order and refused to derive
(*"28 placements left to emit but 35 standing beyond its instantiation block"*). It counts by the
programme phase each record names now — the recipe's `id` IS that phase string — so the West
recipe's remainder holds at 35 with seven West roofs added beside it.

**The adoption, and the one it refused.** The block deals a D1 and a D3, which are exactly the two
families T-A2h's rule admits. The D1 is adopted: the labourer's count is a floor by its own text,
D1 is the family this layer houses nine of its eleven housed labourers in, and **this layer
already places two labouring households in the West Division**, so nothing crosses a division line
the programme had not already argued. **The D3 carpenter is refused, and the reason is a gap in
the rule rather than in the roof.** Rule 6's two tests are silent on division, and all eleven
carpenter households stand north or south — a twelfth placed west of the river would be a new
claim about where the town's carpenters lived, arriving as a side effect of a block parcel, which
is the exact failure mode rule 6 was written to prevent. **T-A5 should settle whether rule 6 takes
a division test rather than each parcel deciding it again.**

**Files:** `data/reconstruction/1835_platted_block_parcels.json` (one block appended) ·
`tools/generate_block_infill.py` (lot occupancy, the ancillary and partition gates, the district
string) · `tools/reconcile_665.py` (counting by programme phase) ·
`data/reconstruction/1835_inferred_household_programme.json` (census, one household) ·
`data/structures/recon_1835_blk_randolph_clinton_*.json` (7, derived) · `data/residents/` ·
`data/sidecars/1835/` · `assets/…` placeholder massing · `docs/LIBERTIES.md` (L95) ·
`docs/ROADMAP.md` · `docs/STATUS.md`

### T-A5 — `blk_randolph_market`, and the division test · **DONE 2026-08-14**

**Standing roofs 258 → 266; remaining 407 → 399, 71 of them on covered ground.** Four dwellings on
four of the six free lots and four yard buildings off the alley, on the block bounded by Randolph,
Franklin, Washington and Market. One carpenter household adopted; households **155 → 156**, persons
**191 → 192**. Recorded in L97. **The recipe cleared every placement gate on its first run** — no
lot-line, separation, corridor, relief or occupancy failure to iterate against, which is what the
gates T-A2 through T-A4 accumulated were for. **No tool changed**: the parcel is a recipe entry and
a census edit, which is the shape T-A2 said these would settle into.

**The block was already built on, by this project's OTHER layer.** T-A4 met a block occupied by the
pre-plat West density recipe; this one is occupied by `inf_sawyer_dwelling_a` and `_b`, the
dwellings of the occupation census's own two sawyer households, placed from typed coordinates
before the plat module existed. The layer that argues who the town held and the layer that fills its
blocks have met on the same ground, and T-A4's derived-occupancy machinery absorbed it unchanged.

**The vacancy's position is arithmetic, not argument, and the parcel says so.** Both standing roofs
are on the Randolph face, so the two lots free there are exactly the two the frontage-value typology
wants, and the programme's alternating vacancy has nowhere to fall but Washington. Had the schedule
dealt one roof fewer it would have looked deliberate.

**THE DIVISION QUESTION IS SETTLED: rule 6 takes three tests, and the third is the division.** It is
the family test made about the other axis of the same table — where a trade lived is as much a claim
about the town as what it lived in — and T-A4 had already applied it by hand when it refused a D3
carpenter west of the river. Written into the household programme's `method` list rather than
re-argued per parcel, **it recovers all four adoption decisions taken before it**: T-A2h's carpenter
and labourer adopted, T-A4's labourer adopted, T-A4's carpenter refused. A test that has to be told
those answers is a preference; one that recovers them is a rule. This block's D3 passes all three.

**What it could not decide, and did not fudge: K21 (above).** The sawyers standing on this very
block pass test 1 — *"the smallest number that answers the demand"* — and fail test 2 because their
bespoke dwellings carry no `reconstruction.family` for it to read. Four trades of twenty-nine are
housed that way and only that way. The test is **silent, not negative**, for them; silence is being
read as refusal, which is the cautious answer and not the same answer.

**Files:** `data/reconstruction/1835_platted_block_parcels.json` (one block appended) ·
`data/reconstruction/1835_inferred_household_programme.json` (rule 6, the carpenter census, one
household) · `data/structures/recon_1835_blk_randolph_market_*.json` (8, derived) ·
`data/residents/` · `data/sidecars/1835/` · `assets/…` placeholder massing · `docs/LIBERTIES.md`
(L97) · `docs/ROADMAP.md` · `docs/STATUS.md`

### T-A6 — the schedule learns what a lot is · **DONE 2026-08-15**

**Claimed as `blk_randolph_franklin` and finished as something else, because the block could not
be built honestly.** Re-deriving the schedule on arrival showed the parcel had been dealt seven
principal roofs onto seven free lots — every lot filled, no vacancy — and checking the other nine
open blocks found the same blindness in four more. Full measurement and the three failure shapes
in `docs/STATUS.md` § "half the open blocks were scheduled roofs their own lots could not hold".

**The one-line version:** a block's room was counted in ROOFS and a principal roof needs a free
LOT, so `standing_roofs` could not tell two roofs on one lot from two roofs on two.
`blk_south_water_clark` and `blk_lake_market` were dealt seven principal roofs against six free
lots — unwritable. `blk_south_water_wells`, `blk_randolph_franklin` and `blk_randolph_clark` were
dealt exactly their free-lot count, which is writable and worse, because it spends the alternating
vacancy the recipe's own placement rule promises without anybody deciding to. And
`blk_randolph_dearborn` (the T-A3h backfill) was dealt one yard building and no principal roof to
put it behind.

**A rule a parcel can be dealt out of is not a rule.** The vacancy was a promise each parcel kept
by hand — T-A2 left one lot open, T-A5 two — and a block dealt its exact free-lot count could not
keep it. It is now a property of the deal: `principal = min(free lots − 1, roof headroom)`,
`ancillary` bounded by the 154:511 ratio AND by the principals the parcel builds, lot occupancy
derived by the same footprint-centroid rule `tools/generate_block_infill.py` already uses so the
two halves cannot disagree again, a token a unit cannot take offered to the next unit rather than
dropped, and a new assertion that fails the build if a unit is ever dealt past its room.

**Cost: schedulable-on-covered-ground 71 → 66, gated 328 → 333.** Five roofs that never had
anywhere to stand went back to waiting on coverage. That is the honest number and it is smaller
than the one this lane had been quoting.

**All ten open blocks are buildable now, and each keeps a lot open.** `blk_randolph_franklin`
returns to the queue with the corrected mix below. This parcel changed no structure record, no
resident, no sidecar and no mesh: `tools/reconcile_665.py`, the derived programme, two documents
and a changelog entry.

**Files:** `tools/reconcile_665.py` · `data/reconstruction/1835_665_roof_programme.json` (derived)
· `docs/STATUS.md` · `docs/ROADMAP.md` · `renderers/web/js/changelog.js`

**What it did not do:** ask whether ONE open lot per block is the right vacancy. The rule now
guarantees a floor of one, which is what the phase-one parcel assumes and what every parcel so far
has done or bettered; whether a block of eight lots in 1835 Chicago carried six roofs rather than
seven is a question for the evidence, not for the apportionment, and nothing here answers it.

### T-A7 — a building stands on the lot it stands on · **DONE 2026-08-15**

**Claimed as `blk_south_water_franklin` and finished as something else, the way T-A6 was, and
for the neighbouring reason.** T-A6 made a block's room a function of its FREE LOTS. This is
about how a lot is known to be free at all — and the answer was *the building's centroid is not
in it*, which is a proxy that fails on precisely the records the plat grid was built to correct.

**The one-line version:** a building placed from typed coordinates before the plat module
existed can stand a metre or two proud of its own street frontage, so its centroid lands in the
ROADWAY — and a building whose centroid is in the roadway stands, as far as the schedule can
tell, on no lot of any block. Fourteen committed records were in that position. Four of them
are named, documented buildings sitting on lots the schedule was offering to anonymous roofs:
the **Temple Building** (27 % of it on `blk_south_water_franklin` lot 0), **Harmon & Loomis's
store** (31 % on `blk_south_water_clark` lot 0), the **Chicago Democrat's office** (34 % on
`blk_south_water_lasalle` lot 6) and the **Cook County courthouse** (13 % on
`blk_randolph_lasalle` lot 6). The claimed block was dealt six principal roofs for seven free
lots when one of those lots has the Temple Building on it.

**The rule now has two tests, in `tools/plat_occupancy.py`, and each answers a different way of
being wrong.**

1. **A building stands on the lot most of it is on**, measured. This is the same claim the
   centroid was making, made by area instead of by a point. It is purely additive on the
   committed dataset: *no record changes lot*, five lots that read free are now known to be
   taken, and none that read taken became free.
2. **It occupies that lot only where it reaches the lot's buildable part** — the lot inset by
   `LOT_MARGIN_M`, the same 1.5 m the generator makes every new roof keep from its own lot
   lines. A neighbour lapping only into that strip has taken nothing a roof could have used.
   **J. H. Kinzie's store is the case that earns this test**: 9.7 m² of it lies on
   `blk_south_water_franklin` lot 2 and none of it inside the buildable inset, so the lot is
   free and the schedule may still deal it a roof. Without test two the town loses roofs it can
   honestly have.

**And the second half of the same defect, in the ledger:** a roof was attributed to a block by
its position POINT, so the same buildings were counted as standing in no block at all — their
roofs never subtracted from the headroom of the block they physically stand in. The **Exchange
Coffee House** holds nine tenths of a lot of the claimed block and counted nowhere; so did
**Harmon & Loomis's store** and the **Tremont House**. A roof standing on a block's lot stands
in that block, and the ledger now says so.

**One implementation, imported by both halves.** T-A6 required the schedule and the generator to
derive occupancy the same way and they did — by each carrying its own copy of the rule, which is
how two copies of one rule drift. `tools/plat_occupancy.py` is now the only implementation;
`reconcile_665.py` and `generate_block_infill.py` both call it, and `LOT_MARGIN_M` is authored
there too because the occupancy test reads the same number from the other side.

**Cost: schedulable-on-covered-ground 66 → 61, gated 333 → 338.** Occupied lots 79 → 84. Standing
roofs are unchanged at 266 and remaining at 399 — nothing was built or removed, five roofs went
back to waiting on coverage because the ground they were promised is already built on. Four
blocks lose a lot each: `blk_south_water_franklin` 7 free lots → 6 and 8 roofs → 7,
`blk_south_water_lasalle` 8 → 7, `blk_south_water_clark` 7 → 5 (it also gains two standing
roofs), `blk_randolph_lasalle` 5 → 4.

**What it measured and deliberately did NOT call occupancy.** `recon_1835_west_018` laps 11.9 m²
onto `blk_randolph_clinton` lot 2, where T-A4 stands a principal roof. Test one seats that
building on lot 4, where 82 % of it is, so lot 2 remains the roof T-A4 put there. A rule that
called every lap an occupation would have condemned a committed, gated placement on a corner of
a building — and whether two roofs may stand three metres apart across a conjectural side lot
line is the separation gate's question, which it passed at the time. The number is recorded here
so that nobody reads the silence as nobody having looked.

**What it did not do: build the block.** `blk_south_water_franklin` returns to the queue below
with its corrected deal — 7 roofs, 5 principal and 2 ancillary, on six free lots.

**Files:** `tools/plat_occupancy.py` (new) · `tools/reconcile_665.py` ·
`tools/generate_block_infill.py` · `data/reconstruction/1835_665_roof_programme.json` (derived)
· `docs/ROADMAP.md` · `docs/STATUS.md` · `renderers/web/js/changelog.js`. No structure record,
no resident, no sidecar, no mesh and no renderer file.

### T-A9 — `blk_south_water_wells` · **DONE 2026-08-15**

The second block of the South Water row — bounded by South Water, LaSalle, Lake and Wells —
carries **eight roofs, six principal and two ancillary**, on six of its seven free lots.
`brown_boarding_house` holds lot 6 and the Lake-and-Wells corner is left open. **281 stand and
384 remain, 46 of them on covered ground.** The recipe cleared every placement gate on its first
run and **no tool changed**, which under T-A8's own text is what a block parcel is supposed to
look like now. Two adoptions under rule 6: the D3 one-room cottage on lot 7 becomes the
fourteenth inferred carpenter household, the D1 log cabin on lot 5 the sixteenth labouring one.
Full admission in `docs/LIBERTIES.md` **L100**.

**Three findings came out of it that are not the block.**

1. **Both adoptable trades were offered a SECOND roof here, and refusing them was a choice
   rather than a rule.** Read literally, four of the six dwellings pass rule 6's three tests for
   one trade or the other — the D3 *and the D4* for carpenters (one carpenter household stands in
   a D4, in the North Division), the D1 *and the D2* for labourers (four stand in D2s). The rule
   says nothing about how many roofs of one block a single trade may take, because no parcel
   before this one was offered the case. One per trade was adopted, on the reading that rule 6's
   own opening sentence — the mix is a claim about the town, not about what has been drawn —
   forbids a block's deal from raising a trade's count twice. **That reading is written into both
   census arguments and into L100 as a choice, not smuggled in as a rule**, and **K28** is raised
   to settle it.
2. **Three documented stores on this block stand INSIDE the platted South Water corridor** —
   Jones's grocery by 4.5 m, Philo Carpenter's store by 6.6 m and Peck's store by 8.2 m. T-A7
   established that a pre-plat record can stand "a metre or two proud" of its frontage and
   measured the consequence for *occupancy*; nobody had measured the intrusion itself. Two of the
   three lap no lot of this block at all. It cost this parcel nothing — the nearest any roof here
   comes to any of them is 7.99 m against a 3 m gate — so it is recorded and opened as **K30**
   rather than fixed inside a block parcel.
3. **L99 said it had opened the commercial-frontage question as a ROADMAP parcel and it had
   not** — the ID it names was already in use for the confidence-band parcel. The question is
   real and this block is the second instance of it: the programme apportions families by
   district and has no notion of what a street was for, so it dealt a log cabin and a plank
   shanty to the town's busiest commercial frontage for the second time running. Opened properly
   as **K29**.

**Files:** `data/reconstruction/1835_platted_block_parcels.json` ·
`data/reconstruction/1835_inferred_household_programme.json` · `data/structures/` (8 new) ·
`data/residents/` (2 new households, 2 new persons, K20 churn) ·
`data/reconstruction/1835_665_roof_programme.json` (derived) · `assets/generated/` (8 flagged
placeholder GLBs, no Blender) · sidecars · `docs/LIBERTIES.md` L100 · `docs/STATUS.md` ·
`docs/ROADMAP.md` · `renderers/web/js/changelog.js` · the published mirror. **No tool file.**

### T-A10 — `blk_south_water_lasalle` · **DONE 2026-08-15**

The third block of the South Water row — bounded by South Water, Clark, Lake and LaSalle — carries
**seven roofs, five principal and two ancillary**, on five of its six free lots. Lot 1 (the
Lake-and-LaSalle corner) is left open; lot 6 is held by the Chicago Democrat's office and lot 5 by
Thomas Church's store, both derived by `tools/plat_occupancy.py` rather than authored. **288 stand
and 377 remain, 39 of them on covered ground.** The recipe cleared every placement gate on its
first run and **no tool changed** — the third block in a row, which under T-A8's own text is what a
block parcel should look like now. Two adoptions under rule 6: the D3 one-room cottage on lot 0
becomes the fifteenth inferred carpenter household, the D1 log cabin on lot 7 the seventeenth
labouring one. Full admission in `docs/LIBERTIES.md` **L101**.

**Four findings came out of it that are not the block.**

1. **The first block of the row that arrived with a documented roof on BOTH faces**, which is the
   first real test of the frontage argument rather than a repeat of it. T-A8 and T-A9 could send
   their meanest roofs to an empty back street; Church's store already stands on this one's Lake
   frontage. The arrangement was applied anyway — a log cabin and a plank shanty on a frontage that
   already carries a documented store — and L101 records that it is the same invention made with
   less room rather than a new one.
2. **T-A7's lap case has a third instance and it is the largest by a factor of two.** Church's
   store is seated on lot 5 by test one (59.3 m² of 92.9 m² against 33.6 m² on lot 3), but
   **22.1 m² of the lot 3 lap falls inside lot 3's buildable inset** — where Kinzie's 9.7 m² fell
   entirely outside it and `recon_1835_west_018`'s 11.9 m² was ruled a lap on a corner. It cost the
   parcel nothing (the shanty was offset west and clears the store by **7.56 m** against a 3 m
   gate, the closest approach in the whole parcel) so nothing was moved, but the case now has three
   measured points and the largest of them is inside the strip test two was written to protect.
3. **K28 is not a one-off, and that is the argument for settling it.** This block offered the
   identical pair of double candidacies T-A9 met — the D3 and the D4 for carpenters, the D1 and the
   D2 for labourers. Two consecutive blocks dealing both floor trades both of their families is
   what a five-or-six-dwelling South Division block looks like, not a coincidence. One per trade
   was adopted again, on T-A9's reading, recorded as a choice in both census arguments and L101.
4. **The `K28` id is used twice in this repository** — for the rule-6 question below, and for the
   published-mirror gate that landed as PR #147 with no ROADMAP entry of its own. Both are real and
   neither is wrong; the collision is in the label. A disambiguation line is added at K28's heading
   so existing citations resolve. Renumbering landed work is not a block parcel's call, which is
   why this is a note rather than an edit.

**And one number about this project rather than about the town: the fifth K20 measurement is
72 of 100**, against 19-of-98 at T-A9. Inserting two households renamed nearly three quarters of the
layer's invented names. No grade moved and `check.sh` re-derives all 102, so it is churn — but the
"a fifth of the layer" description every earlier entry used is now wrong, and the mechanism is
visible rather than mysterious: `tools/generate_inferred_names.py` deals names round-robin through
each community-and-sex pool in a stable hash order of person id, so one new person landing early in
a large bucket renames everything after it. K20's fix still belongs in its own parcel.

**Files:** `data/reconstruction/1835_platted_block_parcels.json` ·
`data/reconstruction/1835_inferred_household_programme.json` · `data/structures/` (7 new) ·
`data/residents/` (2 new households, 2 new persons, K20 churn) ·
`data/reconstruction/1835_665_roof_programme.json` (derived) · `assets/gltf/` + `assets/web/`
(7 flagged placeholder GLBs, no Blender) · sidecars · `docs/LIBERTIES.md` L101 · `docs/STATUS.md` ·
`docs/ROADMAP.md` · `renderers/web/js/changelog.js` · the published mirror. **No tool file.**

### T-A11 — `blk_south_water_clark` · **DONE 2026-08-15**

The fourth block of the South Water row — bounded by South Water, Dearborn, Lake and Clark —
carries **five roofs, four principal and one ancillary**, on four of its five free lots. Lot 1
(the Lake-and-Clark corner) is left open; lots 0, 6 and 7 are held by Harmon & Loomis's store,
John Bates Jr.'s auction room and the first Tremont House, all three derived by
`tools/plat_occupancy.py` rather than authored. **293 stand and 372 remain, 34 of them on covered
ground.** The recipe cleared every placement gate on its first run and **no tool changed** — the
fourth block in a row. Two adoptions under rule 6: the D3 one-room cottage on lot 5 becomes the
sixteenth inferred carpenter household, the D1 log cabin on lot 3 the eighteenth labouring one.
Full admission in `docs/LIBERTIES.md` **L102**.

**Five findings came out of it that are not the block.**

1. **The end rule has been asserted as a direction three times and is measured here for the first
   time.** T-A8, T-A9 and T-A10 each put the better roof nearer "the town-centre end". This
   block's east end is Dearborn Street, and the **Dearborn Street drawbridge** — the only crossing
   of the main stem in July 1835, already a committed structure record, its south abutment at the
   foot of Dearborn on South Water — is **35.6 m** from lot 6's frontage and **101.7 m** from
   lot 0's, with lots 4 and 2 at 55.5 m and 78.1 m between them; the back street runs 126.3 m at
   lot 7 to **158.2 m at lot 1**. The arrangement is still invented — no source says a better
   house stood nearer the bridge — but it now has a re-derivable criterion instead of a compass
   direction, and the open lot is the one farthest of the eight from the only bridge in town.
2. **The frontage half of the same rule meets its first counter-example, and it is kept anyway.**
   The largest documented footprint on this block stands on the BACK street: the first Tremont
   House at **139.3 m²**, against 92.9 m² for the auction room, 92.9 m² for Harmon & Loomis's
   store and 46.5 m² for the drug store. A hotel choosing Lake and Dearborn is evidence about
   1835; the face rule is a typology for where anonymous dwellings of different tiers go, and L102
   says so rather than letting three parcels of repetition harden into a claim about the street.
3. **T-A7's lap case has a fourth instance and it is the first that costs the lot nothing.**
   Pruyne & Kimball's drug store laps lot 2 by **4.66 m²** with **0.00 m² inside the buildable
   inset** — the whole lap is in the 1.5 m margin strip. Two of its corners are 0.70 m and 0.65 m
   inside the platted lot line; the other two stand 5.4 m out in the road, a **5.55 m** intrusion
   into the South Water corridor. Four measured points now span the case from "entirely in the
   strip" to L100's 22.1 m² of buildable area.
4. **The west offset T-A10 used to clear a documented store was measured here and refused.** On
   lot 2 it buys **0.03 m at 1.5 m and 0.33 m at 3.0 m**, the 3 m version costing 1.26 m of
   lot-line margin, where half a metre of extra setback buys **0.50 m**. Church's store stood deep
   in its lot; this one stands in the roadway, so only the setback moves the distance. The cottage
   clears it by **6.83 m** against a 3 m gate — the closest approach in the parcel — and the
   remaining offsets are called jitter rather than clearance.
5. **Five South Division households live in a D5, this block was dealt one, and no parcel had ever
   written down why none of them takes it.** Rule 6's family and division tests pass for the
   baker, the butcher, the blacksmith and both clerks; every one of them fails test one, and two
   fail it emphatically — the baker's argument infers one baker "and only one, because a bakehouse
   serves a great many people and nothing attests a second". Three blocks running have been dealt
   a D5 in silence. The silence is now a recorded refusal.

**And K28 gets its third piece of evidence rather than its second.** The D4 on lot 2 passes all
three tests for the carpenters as literally as T-A9's and T-A10's did, and was refused again on
the same conservative reading. Three for three means the case is the ordinary shape of a South
Division block, not a recurring edge — settle it rather than collect a fourth precedent. The
labourers were dealt no D2 here, the first block since T-A8 where their second-roof question did
not arise.

**The sixth K20 measurement is the smallest ever recorded: 7 of 102** carried-over invented
persons renamed, against 72-of-100 at T-A10, 19-of-98 at T-A9 and 32-of-96 at T-A8. Nothing was
fixed in between; it is the hash-position mechanism L101 described, and this is the confirmation
rather than an improvement. K20 still owns the fix.

**Files:** `data/reconstruction/1835_platted_block_parcels.json` ·
`data/reconstruction/1835_inferred_household_programme.json` · `data/structures/` (5 new) ·
`data/residents/` (2 new households, 2 new persons, K20 churn) ·
`data/reconstruction/1835_665_roof_programme.json` (derived) · `assets/gltf/` + `assets/web/`
(5 flagged placeholder GLBs, no Blender) · sidecars · `docs/LIBERTIES.md` L112 · `docs/STATUS.md` ·
`docs/ROADMAP.md` · `renderers/web/js/changelog.js` · the published mirror. **No tool file.**

### T-A12 — `blk_south_water_dearborn` · **DONE 2026-08-15**

The fifth and **last** block of the South Water row — bounded by South Water, State, Lake and
Dearborn — carries **six roofs, five principal and one ancillary**, on five of its six free lots.
Lot 7 (the Lake-and-State corner) is left open; lots 1 and 6 are held by the Mansion House and the
Chappel infant school, both derived by `tools/plat_occupancy.py` rather than authored. **299 stand
and 366 remain, 28 of them on covered ground.** The recipe cleared every placement gate on its first
run and **no tool changed** — the fifth block in a row. Two adoptions under rule 6: the D3 one-room
cottage on lot 4 becomes the seventeenth inferred carpenter household, the D1 log cabin on lot 5 the
nineteenth labouring one. Full admission in `docs/LIBERTIES.md` **L103**. **State Street is the
platted town's eastern limit, so the business front is now built end to end and the row is closed.**

**Five findings came out of it that are not the block.**

1. **The two readings of the end rule point in opposite directions here, and this is the block that
   separates them.** T-A11 replaced "nearer the town-centre end" with a measurement — the distance
   to the Dearborn Street drawbridge — and on the four blocks before this one the bridge lay east,
   so the compass and the criterion agreed and nothing distinguished them. On this block the bridge
   is at the **west** end: lot 0 is **36.4 m** from it, lots 2 and 4 are **57.7 m** and **81.7 m**,
   and lot 6 — the compass reading's better end — is **106.6 m**, with the back street running
   **126.4 m** at lot 1 to **161.1 m** at lot 7. The parcel follows the committed criterion, so the
   row's arrangement reverses direction for the first and last time, and the open lot is again the
   farthest of the eight from the only bridge in town.
2. **A third criterion was tried and is recorded as UNDECIDABLE rather than quietly dropped.** The
   bridge is one landmark, so the parcel asked a question with no landmark and no radius in it:
   where is the mass of documented building? The footprint-weighted centroid of all **83 documented
   roofs (19,145 m²)** lands at local **E 939, N 123** — east of this block — making lot 6 nearest at
   **189.9 m** against lot 0's **250.8 m**. Excluding the fort's 13 roofs and **10,460 m²** moves it
   to **E 737, N 88** and reverses the answer: lot 0 at **95.0 m**, lot 6 at **115.9 m**. Whether a
   military reservation is part of the town is a judgment, not a measurement, and the criterion's
   whole spread without it is **20.9 m** against the bridge's **70.2 m**.
3. **K30 gains two more cases and every one of the five is on the same street.** Both of this
   block's documented South Water buildings stand in the platted roadway: the **Chicago American
   office** intrudes **6.91 m** and **Frederick Thomas's shop 6.25 m**, which is **148.6 m² of
   documented building on this block's north frontage standing on ground the plat calls street**.
   With T-A9's three (4.5 m, 6.6 m, 8.2 m) that is five documented buildings, all on South Water,
   all between 4.5 and 8.2 m in — the distribution K30 asked for, and it points at one street rather
   than a uniform bias across the grid. Nothing was moved.
4. **T-A7's lap case has a fifth instance and it is the largest that costs a lot nothing.** The
   American office laps lot 0 by **10.74 m²** with **0.00 m² inside the buildable inset**; two of its
   corners sit 0.78 m and 0.70 m inside the platted lot line and the other two stand 6.92 m and
   6.84 m out in the road. **T-A11's refusal of the lateral offset is confirmed independently and
   more cleanly**: from the committed placement, 1.5 m further west buys **0.01 m** of clearance for
   0.76 m of margin and 3.0 m buys **0.22 m** for 2.26 m, where half a metre of extra setback buys
   **0.50 m** and costs neither. The cottage clears the office by **6.79 m**; the parcel's closest
   approach is the D4 on lot 2 at **7.01 m** from Frederick Thomas's shop.
5. **The row closes with K28 still open, and it is now four blocks of five.** The D4 on lot 2 and the
   D2 on lot 3 both pass rule 6's three tests read literally and both are refused on the same
   conservative reading. T-A11 asked that a fourth precedent not be collected but that the rule be
   settled; of the five blocks of this row, one dealt neither floor trade a second roof, one dealt it
   to the carpenters alone and **three dealt it to both**. The D5 was dealt and refused again, on
   T-A11's written reasoning rather than a fresh argument — which is what writing it down bought.

**The seventh K20 measurement is 59 of 104** carried-over invented persons renamed, against 7-of-102
at T-A11, 72-of-100 at T-A10, 19-of-98 at T-A9 and 32-of-96 at T-A8. Five measurements now span 7 %
to 72 % with nothing fixed or broken between them, which is what a stable hash order looks like when
two new ids are inserted at a random position. K20 still owns the fix.

**Files:** `data/reconstruction/1835_platted_block_parcels.json` ·
`data/reconstruction/1835_inferred_household_programme.json` · `data/structures/` (6 new) ·
`data/residents/` (2 new households, 2 new persons, K20 churn) ·
`data/reconstruction/1835_665_roof_programme.json` (derived) · `assets/gltf/` + `assets/web/`
(6 flagged placeholder GLBs, no Blender) · sidecars · `docs/LIBERTIES.md` L103 · `docs/STATUS.md` ·
`docs/ROADMAP.md` · `renderers/web/js/changelog.js` · the published mirror. **No tool file.**

### T-A13 — `blk_lake_market` · **DONE 2026-08-15**

The **first block of this parcel shape that is not on South Water Street** — bounded by Lake,
Franklin, Randolph and Market, at the western limit of the platted South Division against the south
branch — carries **seven roofs, five principal and two ancillary**, on five of its six free lots.
Lot 3 is left open; lots 0 and 1 are held by the Sauganash Hotel with Philo Carpenter's log drug
store, and by the packer's dwelling, all derived by `tools/plat_occupancy.py` rather than authored.
**306 stand and 359 remain, 21 of them on covered ground.** The recipe cleared every placement gate
on its first run and **no tool changed** — the sixth block in a row. Two adoptions under rule 6: the
D3 one-room cottage on lot 2 becomes the eighteenth inferred carpenter household, the D1 log cabin
on lot 5 the twentieth labouring one. Full admission in `docs/LIBERTIES.md` **L104**.

**Five findings came out of it that are not the block.**

1. **The face rule was asserted five times and is measured here, because neither of this block's
   faces is South Water.** T-A8 through T-A12 named the front by the street's documented use, which
   says nothing about a block bounded by Lake and Randolph. Counting every documented or inferred
   structure whose footprint centroid stands within 25 m of a street's committed centreline,
   **Lake carries 12 and Randolph carries 2** (South Water carries 9). Lake's twelve include the
   Sauganash, the Green Tree, the Exchange Coffee House, the Tremont, the Mansion House, both
   churches and Dole's south warehouse; Randolph's two are the log jail and the Western Hotel. The
   rule is now inherited on a measurement rather than a habit — **and is still the invention it
   always was**: no source says a better dwelling stood on the better street.
2. **The end rule's ORDER survives and its MEANING does not.** T-A11's criterion — distance to the
   Dearborn Street drawbridge — runs **532.2 m** at lot 6 to **600.4 m** at lot 0 on the Lake
   frontage and **576.3 m** at lot 7 to **640.0 m** at lot 1 behind, so it orders the lots exactly as
   it has on every block. But on T-A12's block the far end stood **2.93×** as far from the bridge as
   the near end and here it stands **1.13×**; the absolute spread of the front face is **68.2 m**
   against T-A12's 70.2 m — the same block, moved half a kilometre. The criterion is separating two
   lots that are, in any terms a resident would have used, the same distance from the bridge. It is
   followed anyway, because swapping criteria on the block where the first stops flattering the
   answer is how an invention starts to look like a finding — **but at this distance the arrangement
   is closer to arbitrary than on any block of the row**, and L104 says so rather than defending it.
3. **K30 gets its first control measurement off South Water, and it is a factor of twenty to forty.**
   The **Sauganash Hotel** intrudes **0.19 m** into the platted Lake corridor and **Philo Carpenter's
   log drug store 0.22 m**, against 4.5–8.2 m for all five South Water cases — near enough to the
   kerb line to be inside the plat's own precision. Two cases are not a survey, but they are the
   control K30 asked for and they point **away** from a uniform grid bias. Nothing was moved.
4. **The block's two documented roofs share one lot and the occupancy map names the smaller of
   them.** The Sauganash puts **94.33 m²** of its 96.0 m² on lot 0 (67.66 m² inside the buildable
   inset) and the log shop **28.58 m²** of its 29.7 m² (19.43 m² inside it); the source says the shop
   stood against the Sauganash's public bar and the two footprints touch at **0.00 m**, so the record
   is agreeing with itself. `plat_occupancy` names the first holder by id — the log shop — so the
   town's most-documented building is not the one the derived table credits with its own corner. It
   costs this parcel nothing, and it will mislead anyone reading that table for what stands where.
   **T-A7's lap case also gains a sixth instance**: the packer's dwelling laps lot 3 by **9.57 m²**
   with **0.00 m² inside the buildable inset**, and lot 3 is the lot left open.
5. **A sixth block offered both floor trades a second roof, and it is the first that is not on South
   Water.** The D4 on lot 4 and the D2 on lot 7 pass rule 6's three tests read literally and are both
   refused on the same conservative reading. T-A11 read three consecutive cases as the ordinary shape
   of a South WATER block; this one shows it is the ordinary shape of **a South Division block of
   five dwellings, wherever it stands**, so the sample K28 has to settle is larger than the row that
   produced it.

**The eighth K20 measurement is 67 of 106** carried-over invented persons renamed, against 59-of-104
at T-A12, 7-of-102 at T-A11, 72-of-100 at T-A10, 19-of-98 at T-A9 and 32-of-96 at T-A8. Six
measurements now span 7 % to 72 % with nothing fixed or broken between them. K20 still owns the fix.

**A note for the next block parcel, which cost this one twenty minutes.**
`tools/generate_inferred_households.py` **strips every invented resident name and its `name_basis`**;
`tools/generate_inferred_names.py` puts them back. Running the first without the second leaves 106
persons named "A baker (reconstructed resident, unnamed)" and reads, in a diff, exactly like a K20
churn measurement of 100 %. Run them in that order, and measure K20 after the second.

**Files:** `data/reconstruction/1835_platted_block_parcels.json` ·
`data/reconstruction/1835_inferred_household_programme.json` · `data/structures/` (7 new) ·
`data/residents/` (2 new households, 2 new persons, K20 churn) ·
`data/reconstruction/1835_665_roof_programme.json` (derived) · `assets/gltf/` + `assets/web/`
(7 flagged placeholder GLBs, no Blender) · sidecars · `docs/LIBERTIES.md` L104 · `docs/STATUS.md` ·
`docs/ROADMAP.md` · `renderers/web/js/changelog.js` · the published mirror. **No tool file.**

### T-A15 — `blk_randolph_clark` · **DONE 2026-08-15**

The block bounded by Randolph, Dearborn, Washington and Clark — across Clark Street from the public
square with the county courthouse on it, and with Dearborn Street, the bridge street, for its east
face — carries **eight roofs, six principal and two ancillary**, on six of its seven free lots. Lot
0 is held by the inferred gunsmith's shop, derived by `tools/plat_occupancy.py`; lot 1 is left open.
**322 stand and 343 remain, 5 of them on covered ground.** The recipe cleared every placement gate
on its first run — the eighth block in a row. It is the first block parcel dealt **both** larger
house families at once (`H1` + `H2`) and the first to stand a **`C2` store-residence**, though
`blk_randolph_wells` built an H1 and an H2 at T-A2 and four C2 roofs already stand elsewhere: what
is new is the combination. One adoption under rule 6: the `D1` log cabin on lot 3 becomes the
twenty-second inferred labouring household. Full admission in `docs/LIBERTIES.md` **L106**. It is
the **second block parcel of this shape to commit a tool**, `tools/measure_adoption_tests.py`, for
the reason in finding 3.

**Four findings came out of it that are not the block.**

1. **The face rule reproduces exactly, which is what T-A14's tool was for.** `tools/
   measure_street_frontage.py randolph washington` returns Randolph 7 research / 7
   inferred-household and Washington 1 / 0 — the same 14 against 1 T-A14 measured on the same pair,
   from a command rather than from a memory. The third layer (this programme's own output) read 18
   and 12 and is excluded, not merged. **This is the first block parcel whose face measurement was
   inherited rather than re-argued**, which is the whole return on committing the tool.
2. **The face rule ranks DWELLINGS and this block had a STORE, so the rule was extended.** The
   extension: a store-residence's claim on the better frontage is functional rather than social —
   it is the only one of six roofs whose purpose requires that a stranger can find it — so the `C2`
   takes Randolph's third free lot and the `D6` that would have had it goes to the head of the back
   street. Opened as **K32** rather than left as a private decision: the next block dealt a
   commercial family follows it or refutes it.
3. **Two of T-A14's three adoption candidacies do not reproduce, and the fix is a command.** T-A14
   recorded that its `D2` passes all three of rule 6's tests for the **laundresses** and its `D4`
   for the **teamsters**. Tests 2 and 3 hold. Test 1 does not: rule 6 asks whether the trade's OWN
   ARGUMENT states in its committed text that its count is a floor, and neither argument contains
   any such statement — the only occurrence of the word in the laundress argument is Andreas's "with
   the floor covered besides", a plank floor in a boarding house. Only the carpenters and the
   labourers state it. `tools/measure_adoption_tests.py` is committed here so the tests are RUN, and
   it prints the sentence each verdict rests on. **K28's question narrows**: not "may a trade that
   has not asked for a roof be given one" but "does test 1 mean the trade's own text or method rule
   3's list of unbounded trades". The two readings disagree for exactly two trades. Measured by the
   command, this block's `D2` admits exactly one claimant — the labourers, taking a second roof —
   and it is refused for the eighth time on the same conservative reading.
4. **The end rule is exhausted, and the reason is geometry rather than this block.** Distance to the
   Dearborn Street drawbridge runs **318.3 / 321.1 / 325.8 m** across the Randolph frontage and
   376.4 → 388.2 m behind. Far/near on the front face is **1.02×**, against T-A14's 1.11, T-A13's
   1.13 and T-A12's 2.93, and the absolute spread is **7.5 m** — under a third of one lot's 24.6 m
   frontage. The bridge bears **10.4° east of north** from the block centre while the face runs
   east–west, so the criterion sees sin(10.4°) = **18 %** of any along-street displacement: 49.3 m
   between the lot 2 and lot 6 centroids projects to 8.9 m, and 7.5 m survives. Followed anyway on
   T-A13's reasoning; the successor question is **K31**. On this block a stronger criterion agrees
   — lot 6 is the corner on Dearborn Street, the street that carries the bridge — which is why
   following the exhausted rule cost nothing here and is exactly what K31 must not assume elsewhere.

**The tenth K20 measurement is 12 of 110** carried-over invented persons renamed, against 61-of-108
at T-A14, 67-of-106 at T-A13, 59-of-104 at T-A12, 7-of-102 at T-A11, 72-of-100 at T-A10, 19-of-98 at
T-A9 and 32-of-96 at T-A8. Eight measurements span 7 % to 72 % with nothing fixed or broken between
them; this is the second-lowest. K20 still owns the fix.

**Files:** `data/reconstruction/1835_platted_block_parcels.json` ·
`data/reconstruction/1835_inferred_household_programme.json` · `data/structures/` (8 new) ·
`data/residents/` (1 new household, 1 new person, K20 churn) ·
`data/reconstruction/1835_665_roof_programme.json` (derived) · `assets/gltf/` + `assets/web/`
(8 flagged placeholder GLBs, no Blender) · sidecars · `docs/LIBERTIES.md` L106 · `docs/STATUS.md` ·
`docs/ROADMAP.md` · `renderers/web/js/changelog.js` · the published mirror. **One tool file:
`tools/measure_adoption_tests.py`, new, standalone, not wired into `check.sh`.**

### K31 — the end rule is exhausted on the Randolph–Washington row · **UNCLAIMED · from T-A15 · Effort: S to decide, S to apply**

T-A11's criterion — the better roof goes to the free lot nearest the Dearborn Street drawbridge —
has thinned on every block since it was written: **2.93× at T-A12, 1.13× at T-A13, 1.11× at T-A14,
1.02× at T-A15**, where it separated three lots by **7.5 m across a 74 m block face**. T-A15
measured the cause and it is not the town: the bridge bears **10.4° east of north** from that block
while the face runs east–west, so the criterion can only see **sin(10.4°) = 18 %** of a displacement
along the street. Every remaining block on this row is in the same position or worse, and the two
`platted_block_awaiting_street_control` entries on South Water are not.

**The question is not whether to keep it — it is what replaces it, and the answer must not be
chosen on a block where it agrees with the old rule.** T-A15's own lot 6 is the trap: it wins under
distance-as-measured AND under frontage on the bridge street, so that block cannot discriminate
between the two. Candidates worth measuring, on a block where they disagree:

- **distance along the street network** to the bridge rather than straight-line — restores the
  discrimination the projection destroys, and is what a resident actually walked;
- **frontage on a named through street** (Dearborn to the bridge, Lake and South Water to the
  business front) — a claim about the street rather than about the corner;
- **nothing at all**: declare the within-face order arbitrary on blocks under some measured
  threshold and say so per block, rather than dressing rounding up as reasoning. **This is a
  legitimate answer** and probably the honest one for a 7.5 m spread.

Whatever lands, the deliverable is the same shape as `tools/measure_street_frontage.py`: a command
that prints the number, so the next block inherits it. Do NOT retro-fit the answer to blocks
already built — L102 onward record what was done and why, and this document is append-only.

### K32 — may the face rule rank a store? · **UNCLAIMED · from T-A15 · Effort: S — a decision, then a clause**

The face rule as committed at T-A13 and T-A14 ranks **dwellings**: the best take the better street,
the meanest take the back one. `blk_randolph_clark` was the first block dealt a **`C2`
store-residence** and the rule said nothing about it. T-A15 extended it — a store's claim on the
better frontage is functional rather than social, being the only roof whose purpose requires a
stranger can find it — and put the `C2` on Randolph, displacing a `D6` to the back street.

**That extension is an invention about 1835 commerce made by an agent, and it needs settling before
it repeats.** The schedule still holds `C1`…`C4`, `F1`…`F4`, `H3`, `I3`, `T1`, `W1`…`W5` for blocks
not yet built, so the same question arrives again the moment a `W` workshop or an `F` warehouse is
dealt — and a warehouse's answer is plainly the opposite of a store's, because a warehouse wants the
river and not the crowd. Three readings to choose between:

1. **rank by claim on frontage** (T-A15's): commerce > better dwelling > meaner dwelling, with the
   ranking authored per inventory group in `1835_building_inventory.json` rather than per parcel;
2. **rank dwellings only** and place non-dwellings by their own function — the store to the busiest
   frontage, the warehouse to the water, the workshop to the alley — which is more honest about
   there being two rules and not one;
3. **refuse the question**: leave non-dwelling placement to the arrangement note of whichever parcel
   meets it, as T-A15 in effect did, and accept that it will not reproduce.

Reading 2 is the likeliest and is the one K29 ("the schedule deals log cabins to the town's
commercial frontage") is already circling from the other side; the two should probably be settled
together. Whatever lands belongs in the recipe's `placement_rule`, where the generator can be made
to check it, rather than in prose a later parcel has to remember.

### T-A14 — `blk_randolph_franklin` · **DONE 2026-08-15**

The first block of the row **two streets back** from the business front — bounded by Randolph,
Wells, Washington and Franklin — carries **eight roofs, six principal and two ancillary**, on six of
its seven free lots. Lot 1 is left open; lot 2 is held by Harmon's log cabin, derived by
`tools/plat_occupancy.py` rather than authored. **314 stand and 351 remain, 13 of them on covered
ground.** The recipe cleared every placement gate on its first run — the seventh block in a row —
and it is the **first block parcel of this shape to commit a tool**, `tools/measure_street_frontage.py`,
for the reason in finding 1. Two adoptions under rule 6: the D3 one-room cottage on lot 7 becomes
the nineteenth inferred carpenter household, the D1 log cabin on lot 3 the twenty-first labouring
one. Full admission in `docs/LIBERTIES.md` **L105**.

**Four findings came out of it that are not the block.**

1. **T-A13's face-rule measurement does not reproduce, and the fix is a command rather than a
   correction.** T-A13 reported Lake 12, Randolph 2, South Water 9 "counting every documented or
   inferred structure whose footprint centroid stands within 25 m of a street's committed
   centreline". No filter recoverable from the repository produces those three numbers: the stated
   one gives **Lake 17 / Randolph 7 / South Water 14** on the research layer alone. The finding it
   supported survives every filter tried — Lake is the better face by a wide margin — so what failed
   was not the judgement but the **reproducibility**, and on a project whose product is provenance
   that is the more serious failure. `tools/measure_street_frontage.py` is committed here so the
   next block runs the measurement instead of remembering it. L104 is left verbatim: LIBERTIES.md is
   append-only and the method is what is corrected.
2. **The count must report its three evidence layers separately, and this block is the
   demonstration.** The reconstruction layer — the anonymous roofs the block parcels themselves
   place — stood at **15 on Randolph and 9 on Washington** when this arrangement was chosen and read
   **18 and 12** the moment the parcel built. A face rule counting that layer reads the programme's
   own output back as evidence and drifts a little further from the town's record with every block.
   Excluded, the answer here is **14 against 1**: Randolph carries 7 research-layer records and 7
   inferred-household buildings, and **Washington Street's entire documented 1835 frontage is the
   estray pen**, the town's pound for stray animals.
3. **The end rule thins for a second block running.** Distance to the Dearborn Street drawbridge
   runs **527.8 m** at lot 6 to **584.0 m** at lot 0 on the Randolph frontage and **568.5 m** at lot
   7 to **621.0 m** at lot 1 behind; the far end of the front face stands **1.11×** as far from the
   bridge as the near end, against T-A13's 1.13 and T-A12's 2.93, and the front face's absolute
   spread is **56.2 m** against T-A13's 68.2 m. Followed anyway on T-A13's reasoning; recorded as
   closer to arbitrary than ordered.
4. **The "second roof" question has been the wrong question for six blocks, and this is the finding
   that matters most.** Every block since T-A9 has recorded its D4 and its D2 as *second* roofs for
   the carpenters and the labourers and refused them conservatively. Both were dealt here and both
   are refused again — but the D4 is also the **first** roof of the **teamsters** and the D2 the
   first roof of the **laundresses**, the other two of method rule 2's four unbounded trades, each
   housed in that one family and in no other and each already placed in the South Division. Both
   pass all three of rule 6's tests and no parcel has ever named them. **Sixteen anonymous D2 and D4
   roofs stand in the South Division today under exactly that description.** **K28** is therefore
   settling a larger question than the one it was opened on: not whether a trade may take a second
   roof, but whether rule 6 admits a roof for a trade that has not asked for one.

**The ninth K20 measurement is 61 of 108** carried-over invented persons renamed, against 67-of-106
at T-A13, 59-of-104 at T-A12, 7-of-102 at T-A11, 72-of-100 at T-A10, 19-of-98 at T-A9 and 32-of-96
at T-A8. Seven measurements now span 7 % to 72 % with nothing fixed or broken between them. K20
still owns the fix.

**Files:** `data/reconstruction/1835_platted_block_parcels.json` ·
`data/reconstruction/1835_inferred_household_programme.json` · `data/structures/` (8 new) ·
`data/residents/` (2 new households, 2 new persons, K20 churn) ·
`data/reconstruction/1835_665_roof_programme.json` (derived) · `assets/gltf/` + `assets/web/`
(8 flagged placeholder GLBs, no Blender) · sidecars · `docs/LIBERTIES.md` L105 · `docs/STATUS.md` ·
`docs/ROADMAP.md` · `renderers/web/js/changelog.js` · the published mirror. **One tool file:
`tools/measure_street_frontage.py`, new, standalone, not wired into `check.sh`.**

### T-A16 — `blk_randolph_lasalle` is the public square · **DONE 2026-08-15 · the block was WITHDRAWN, not built**

The thirteenth block parcel claimed the last open entry on the Randolph–Washington row and
**could not build it**. `blk_randolph_lasalle` — Randolph, Clark, Washington, LaSalle — is
**the public square**: Andreas calls it *the square* and *the court-house square*, this
project's own ground control names its corners *NW / SE corner of the Public Square block*,
and it carries three of the county's own buildings — the estray pen on its south-west corner
(March 1833, Chicago's first public building), the log jail on its north-west (fall 1833) and
the first Cook County court-house (1835). The 665-roof programme was dealing it an `A1`, a
`D3`, a `D4` and a `D5`.

So the parcel reserved it instead. `data/reconstruction/1835_reserved_ground.json` is the
authored reservation; the plat module emits the block **with no lots**; `reconcile_665.py`
reports it `platted_block_reserved` / `state: reserved` and deals it nothing;
`generate_block_infill.py` refuses a recipe that names it, by name and before it builds
anything; and `tools/measure_reserved_ground.py --gate` is a step of `check.sh`. Full
admission in `docs/LIBERTIES.md` **L107**. It is the first parcel of this shape to commit no
structure record at all, and the third to commit a tool.

**Four findings came out of it that are not the block.**

1. **Every placement gate this project has passed the two buildings that were standing on the
   square.** `wright_building_to_let_a` and `_b` — John Wright's two documented cottages to
   let — were placed in *"the South Division band the recipes use for ordinary dwellings"*,
   and that band ran across the square. The placement was tested for clearance from other
   buildings, for its own lot lines, for the platted roadway and for buildable ground. **Not
   one of those questions is whether the ground was for sale**, which is why a documented
   private building could stand on the county's square through every gate the project owns.
   The new gate is the one that asks it.
2. **The defect is upstream of the schedule, in the plat module.** `generate_plat_lots.py`
   subdivides every block it can build into four lots to a face, because that is what the
   Thompson module says a block is. Drawing eight lot lines across the square asserted a
   subdivision that this project has never read on any sheet, and everything downstream
   believed it. The reservation therefore withdraws the **lots**, not merely the schedule's
   permission to use them: the grid drops 152 → **144 lots**, and `lots_per_face_withheld`
   records what the module would have drawn.
3. **The reservation is `inferred` and is not promoted.** No source this project holds says in
   terms that the square was reserved from sale. What it holds is the block's name, the
   county's three buildings on it, the dossier's own reading of the rest of it — *"open,
   unimproved, fenced or unfenced prairie block"* — and one period description of the ground
   itself: *"Our public Square was then a pond, where the Indians had trapped the muskrat, and
   where the first settlers hunted ducks"* (`chicagology_prefire273`, rung 2). Three readings
   from three directions, none of them a house, and the grade stays in the middle tier where
   the evidence puts it.
4. **The pond is documented and is not modelled** — the terrain carries no standing water here
   and the marsh flora zone is a buffer of the mapped water, so the square renders as dry
   prairie. A second false statement about the same ground, smaller than the one fixed and not
   fixed here. Opened as **T-E5**.

**Where the two cottages went.** Each takes the nearest free platted lot **that no committed
block recipe has already spoken for** — the recipes name their open lots and say why, and
taking one would rewrite a parcel that has landed. Building *a* moves **83 m** to lot 7 of
`blk_lake_wells`, building *b* **69 m** to lot 7 of `blk_lake_lasalle`, both on the Randolph
frontage facing the square. The pair is **split**, and that is stated rather than hidden: the
only ground that would have kept them on one block was 200 m further off and faced two
different streets, and one advertisement offering two buildings was never a statement that
they shared a holding.

**The eleventh K20 measurement is 0 of 111** carried-over invented persons renamed, against
12-of-110 at T-A15, 61-of-108 at T-A14, 67-of-106 at T-A13, 59-of-104 at T-A12, 7-of-102 at
T-A11, 72-of-100 at T-A10, 19-of-98 at T-A9 and 32-of-96 at T-A8. Zero for a structural reason
and not a lucky one — **this parcel inserts and removes no person, so the allocator has nothing
to shift.** Nine measurements in, that is the first evidence about *what* perturbs it, and K20
should start there.

**Ledger:** standing roofs unchanged at **322**; **343 remain, 1 of them on ground the project
has coverage for** (was 5 — the square held four of the five). Lane 2 is now one block entry
from having nowhere to build, which is what LANE 3 exists for.

**Files:** `data/reconstruction/1835_reserved_ground.json` (new) ·
`data/reconstruction/1835_inferred_household_programme.json` ·
`data/reconstruction/1835_665_roof_programme.json` (derived) ·
`data/traces/vectors/thompson_lots.json` (derived) · `data/structures/` (2 moved, 0 new) ·
sidecars · `docs/LIBERTIES.md` L107 · `docs/STATUS.md` · `docs/ROADMAP.md` ·
`renderers/web/js/changelog.js` · the published mirror. **Four tool files:
`tools/measure_reserved_ground.py` (new, and wired into `check.sh`),
`tools/generate_plat_lots.py`, `tools/reconcile_665.py`, `tools/generate_block_infill.py`** —
the ROADMAP asks a parcel that edits the block generator to say what was genuinely new, and
this is it: **the generator had no concept of ground that is not for sale.**

### T-A13…T-An — the remaining blocks · **UNCLAIMED**

One block per run, same shape, until the schedule is exhausted. Each names its own block
prefix in its claim heading so two runs cannot take the same one. **Read the schedule at your own
arrival date** — it is derived from what stands, so every block parcel that lands re-apportions
the families of every block that has not. A parcel that meets an institutional family defers it
per T-A3 rather than reaching for a shape, and a block that is already partly built has its taken
lots derived rather than authored per T-A4.

**The rules are now complete enough that a block parcel should need no argument of its own beyond
its arrangement note.** Deferral (T-A3), derived occupancy with its five refusals (T-A4) and the
three-test adoption rule (T-A2h + T-A5) all live in code or in the programme's `method` list, and
T-A5 changed no tool at all. A run that finds itself editing `tools/generate_block_infill.py` has
met something genuinely new and should say what it was in its ROADMAP entry.

**Open after T-A16, re-derived from the programme that parcel committed — 1 roof across ONE
entry:** `blk_randolph_dearborn` 1 (a `D3`). **`blk_randolph_lasalle` is gone from this list for
good**: T-A16 found it was the public square and reserved it, so the four roofs it held went back
to the district balance. The row is closed.
`blk_randolph_lasalle` is **the public square block** — it already carries the Cook County
courthouse, the estray pen and both Wright buildings to let, so it arrives with four of eight lots
taken and is the first open entry whose standing roofs are all research-layer records rather than
this programme's own. `blk_randolph_dearborn` is still not a block parcel for the same reason it was
not one after T-A14: one dealt roof that can only be deferred with its reason, so T-A3h's "backfill,
now a D3" stays stale. **The South Water row is closed, Lake and Market with it, and Randolph at
Franklin and at Clark now too**; both open entries are on the Randolph–Washington row.
**This list is a convenience and goes stale the moment the next parcel lands** — the schedule
re-apportions every open block each time one closes. Re-derive it, do not trust it. What T-A6
guarantees, and what the list itself does not, is that whatever you re-derive will FIT: no block
is dealt more principal roofs than it has free lots less one, and no block is dealt a yard
building without a roof to stand it behind.

---

## LANE 3 — THE EASTERN AND SOUTHERN GROUND · opened 2026-08-14 on the owner's instruction

> *"If you need to extend the town east to add population that is fine … but you must make
> sure that the extension of the city matches the real geographic maps of the city, like where
> the peninsula comes down with the sand bars should be accurate. But I don't think houses are
> in much of it because of Fort Dearborn. You should be able to define further south from
> accurate maps."* — Kevin, 2026-08-14, supplying two scans of **Map of Chicago in 1830**.

**Why this lane exists.** The roof programme is out of room. 251 roofs stand and 414 remain,
but only **86 sit on ground the heightfield currently covers**; the other **328 have nowhere
to go**. Lane 2 hits that wall in about a day and a half. This lane makes the ground, and it
is the owner's instruction that making it is licensed *provided the geography is real*.

### THE TRAP, and it will catch a runner who skims

**The supplied sheet is dated 1830. The scene is 1835-07-01, and the harbour was cut in
between.** `data/terrain/epochs/e1834_harbor_cut/` exists precisely because that cut moved the
river's mouth: before it, the Chicago River turned south behind a sand bar and entered the lake
well below the fort; after it, a straight channel and piers went through the bar. A runner who
traces the 1830 outlet into the 1835 scene will have moved the river's mouth by several hundred
metres and will have done it confidently, from a real map.

Worse, the sheet carries a label reading **"present outlet of river"**. *Present* means the
publication's present, not 1830 and certainly not 1835. It is a retrospective annotation on a
retrospective map. The same goes for its 1812 markings (the camp, the surrender, the massacre
site): those are memorial labels placed by a later hand, not features standing in 1835, and
nothing in this lane may render them as such.

**So the division of labour is fixed, and is not a runner's choice:**

| element | driver | the 1830 sheet's role |
|---|---|---|
| lake shore, sand bar, harbour cut, piers, the old southward channel | **Wright 1834** (already S2e's driver) | corroboration only |
| land claims, owners, and where settlement actually reached | **the 1830 sheet** | primary |
| street and block geometry | **Thompson plat 1830** + **Hathaway 1834** | corroboration only |
| the fort's reservation extent | **the 1830 sheet** + Andreas prose | primary |

The bar's *form* comes from Wright because Wright is a survey five years closer to the target
date and is already the master warping raster. The 1830 sheet says who held which ground — the
thing Wright does not say, and the thing this lane actually needs.

### T-E1 — register the 1830 sheet as a source · **DONE 2026-08-14**

`data/sources/andreas_1884_chicago_1830_map.json` + `docs/RESEARCH/chicago_1830_claims.md`.

**Identified by opening the page, not by inference:** Andreas vol. 1 (1884), fold-out inset
facing pp. 112–113 = Internet Archive leaf **`n240`**. Cross-fixed because leaf `n242` is p. 113
carrying the Harrison harbour map already registered here, which pins the leaf-to-page offset.
Rights were already settled — the volume is `andreas_1884_v1`, public domain.

**What the parcel found, and it changes lane 3's shape:**

1. **It is a land-title map. A name is not a house.** The plate's own printed note says the
   names are "primary patentees, or persons by whom entry was made, entered or patented". So a
   named tract may **never** license an anonymous roof, and T-E4's eligibility rule must not
   read "named ⇒ buildable". The handful of structures the plate actually draws is a far better
   guide to where building had happened than the wall of names is — which supports the owner's
   instinct that houses were not spread across this ground.
2. **The entry window is 1828–1836 — past the scene date.** Some names belong to people who had
   not entered the land on 1835-07-01, and the sheet does not date individual entries.
3. **It is an 1884 compilation that labels its anachronisms "present."** `PRESENT CANAL` is the
   Illinois & Michigan Canal, **not completed until 1848**. Also `Present Court House Square`,
   `present outlet of river`, and a street grid the note itself disclaims as post-1830. Every
   "present" on this plate is a fifty-four-year anachronism.
4. **Two plates in the volume share the name** — a map (inset, pp. 112–113) and a pictorial view
   (p. 164). Cite the leaf, never the name.
5. **The owner's two scans are not the same document.** The line-art issue is a different
   rendering, unidentified, and **may not be cited** until it is.
6. **T-E2 may need no new evidence for the bar.** `harrison_1830_river_mouth` — already held —
   draws the sand bar, the "Sand and Gravel" ground and the old southward channel in plan.
   Check it before going looking.

### T-E1 (spec) — the original parcel definition

Nothing else in this lane may cite the map until it resolves in `data/sources/`. **Never invent
a source** — that rule is not relaxed because the owner supplied the image.

The identification is expected to be cheap: `andreas_1884_v1` is already registered
(public domain, tier 3, `archive.org/details/historyofchicago01andr`) and
`harrison_1830_river_mouth` already cites p. `n242` of that same volume. The plate is very
likely in it. **Verify that; do not assume it.** If it is, this is a plate citation within a
source already held, and rights are settled. If it is not, find the actual publication and
record it with a Wayback snapshot like any other.

Two editions are in hand and they are not the same document: a plain line-art version and a
coloured version carrying substantially more detail (timber stipple, the Canal Land and School
Section blocks, the 1812 annotations, additional claim names). Record **which** is cited for
each reading, because they do not agree on everything.

**Files:** `data/sources/<id>.json` (new) · `docs/RESEARCH/chicago_1830_claims.md` (new)
**Acceptance:** `tools/check.sh` green; the record states plate, page and edition; a
`what_it_does_not_supply` list that names the 1830-vs-1835 problem and the "present outlet"
label explicitly.

### T-E2 — the ground that must stay empty · **DONE 2026-08-15**

Two grounds outside the plat are withdrawn from the buildable town: the **United States
Reservation** east of State Street and the **sand bar across the river mouth**. The refusal is
authored in `data/reconstruction/1835_no_build_ground.json`, enforced in
`tools/generate_block_infill.py` before any placement test that could mask it, and gated by
`tools/measure_no_build_ground.py --gate` as a step of `tools/check.sh`. Full admission in
`docs/LIBERTIES.md` **L108**.

**The measurement is the parcel.** Of the **121.18 ha** of modelled land standing above the water
surface, **32.10 ha — 26.5 %** is one of the two: the reservation **22.57 ha**, the bar **9.53 ha**.
Every gate this project had asked whether a placement cleared its neighbours, its lot lines, the
platted roadway, the modelled terrain and the relief; **none of them asked whether the ground was
ever for sale.** L107 found that hole inside the plat at T-A16. This is the same hole, four times
larger, outside it.

**Four findings that are not the polygons.**

1. **Nothing had to move, and that is an accident rather than a rule.** Seventeen structure records
   stand on the two grounds — the fort's stockade, parade and eleven buildings, the garrison garden,
   the 1832 lighthouse, Beaubien's homestead and barn, and the south pier, which touches both
   because that is what a pier run out through a bar does — and **zero anonymous roofs**. Every
   recipe to date was keyed to a platted block and the reservation was never platted. T-A16 was not
   so lucky: two documented cottages had been standing on the public square for five days.
2. **The refusal is `documented` and the boundary is `inferred`, and grading them together would
   have been the error.** Andreas gives 75.69 acres, the southwest fractional quarter of Section 10,
   unplatted, outside the town's eastern boundary, under Beaubien's pre-emption claim filed five
   weeks before the scene date. The polygon is a different claim: **no vertex of it is authored.**
   Its west and south sides are the quarter's two survey lines resolved from one committed control
   point — G1, State & Madison, whose own note has said since the datum work that *Madison's line
   continues east as the reservation's south boundary* — carried on the plat's east-west bearing,
   which Lake, Randolph and Washington agree on to the sixth decimal. Its third side is the
   committed waterline the trace itself calls *the Fort Dearborn reservation's lake shore*.
3. **The derived polygon is 13.2 % short of the documented acreage and is NOT tuned to close it:
   65.70 acres against 75.69.** Three candidates, none measured — a fractional quarter is surveyed
   to the lake's meander line, which lies east of the 1834 waterline and encloses the old southward
   channel's water; the traced shore carries +/-20 m; the shore trace's own note says it leaves its
   window south of Madison. **So the polygon is a FLOOR**, and the floor is asserted rather than
   hoped: the gate re-counts every cell of modelled land above the water surface that stands east of
   the west line, north of Madison, south of the main stem and inside neither polygon. **It is zero
   today**, and it is what will fail when **T-E3** extends the terrain past the traced shore.
4. **562 cells looked like a hole and were not one.** The first pass flagged that many unclassified
   dry cells between the reservation's east bank and the bar; measured, every one of them lies
   between **-0.10 m and 0.00 m** — the waterline tolerance band the buildable test carries, not
   ground. Above the water surface the count is zero, which is why the gate is written against the
   water surface rather than against the tolerance.

**Both assertions were proved to fail before either was trusted**, the standard K27 and K28 were
held to: removing one permitted entry fails the gate by name, and shrinking the bar polygon to a
sliver fails the under-coverage count with **11,100** cells.

**The four open questions this parcel did not close, and did not pretend to.** The 1830 plate draws
**Mark Beaubien's**, **Elijah Wentworth's cabin**, **La Framboise's cabin and store** and
**Porter's log cabin**; none has a record, an exclusion, or a tested survival to 1835-07-01. The
new disposition table at the foot of `docs/RESEARCH/chicago_1830_claims.md` accounts for every
structure the plate draws and lists these four as open, which is the disposition T-E2's acceptance
allows and the only honest one available from an 1884 land-title compilation. **Mark Beaubien's is
the one inside the modelled area and is the one worth taking first.** T-E2 made no new structure
record and no new exclusion.

**What it costs the roof programme: nothing that was owed.** The 177 roofs in
`south_plat_beyond_committed_control` wait on street control reaching east of State and south of
Washington. This parcel removes an answer that was never available — the ground immediately east of
State is not coming, at any date, because it is the reservation.

**Files:** `data/reconstruction/1835_no_build_ground.json` (new) ·
`tools/measure_no_build_ground.py` (new) · `tools/generate_block_infill.py` · `tools/check.sh` ·
`docs/RESEARCH/chicago_1830_claims.md` · `docs/LIBERTIES.md` L108 + `data/liberties.json` ·
`docs/STATUS.md` · `docs/ROADMAP.md` · `renderers/web/js/changelog.js` · the published mirror.
**No structure record changed, and no geometry was baked.**

### T-E2 (spec) — the original parcel definition

The owner's read — *"I don't think houses are in much of it because of Fort Dearborn"* — is
the substance of this parcel, and it is a claim to be evidenced, not assumed.

The **military reservation** east of the town is not ordinary building ground, and the **sand
bar** is not building ground at all. Both must become polygons the infill generator refuses,
in the same way `REFUSED_FAMILIES` already refuses civic roofs: an anonymous roof placed on the
reservation or on the bar is not a plausible inference, it is an error the schedule made
because nothing stopped it.

**This parcel may not simply shrink the buildable area and call it done.** Where a named
structure genuinely stood on or near the reservation, the 1830 sheet names several — the Kinzie
house, Beaubien's store, the Baptiste Beaubien field, the Crafts house — and those are
*records*, not anonymous infill. Whether each was still standing on 1835-07-01 is a per-record
question with an answer or an exclusion, never a guess.

**Files:** `data/terrain/…/no_build.json` (new) · `tools/generate_block_infill.py` ·
`data/exclusions.json` · `docs/LIBERTIES.md`
**Acceptance:** `tools/check.sh` green; the generator refuses the reservation and the bar and
says why; every named claim from the sheet is either a structure record, an exclusion with a
citation, or listed as an open question — nothing silently dropped.

### T-E3 — finish the heightfield east · **UNCLAIMED · after T-E1 · NEEDS THE BAKE**

**This is `S2e` below, not a new parcel — read it before starting.** Parcel (a) is done and it
already measured the answer off Wright: the box must reach about **E +1700**, roughly
2.0 km × 0.7 km, ~224k samples at the current 2.5 m cell. Use a coarser cell east of the built
blocks, where the evidence does not support 2.5 m detail anyway.

New geometry arrives via `chicago-4d-bake.yml` as a PR into `dev`. The data half ships here and
says so.

### T-E4 — the southern buildable ground, and the re-apportioned schedule · **UNCLAIMED · after T-E2**

The owner is right that south is where the room is: the sheet shows the town's platted blocks,
then Canal Land and the School Section below Madison, with named claims scattered through. That
is a real, mapped distinction between ground that was subdivided and ground that was not, and it
should govern where the remaining 328 roofs may go.

**The schedule is derived, not authored** — `tools/reconcile_665.py` recomputes the remainder
from what stands — so this parcel's job is to widen the *eligible ground*, then let the
apportionment fall out. A roof may be placed only where the ground is **covered by the
heightfield AND historically plausible**. Widening the first without the second is exactly the
failure this lane was opened to prevent.

**Files:** `data/reconstruction/1835_building_inventory.json` ·
`tools/generate_block_infill.py` · `docs/RESEARCH/chicago_1830_claims.md`
**Acceptance:** `tools/check.sh` green; the eligible-ground rule is stated in the programme and
enforced by the generator; the reconciliation still balances; no roof stands on the bar, the
reservation, water, or unmodelled ground.

---

### T-E5(a) — date the in-town water before anything models it · **DONE 2026-08-16**

**The deferral asked about a place and was read as though it answered about a scene.** The
terrain spec defers **four** in-town water features under one shared phrase — *"existence
documented, geometry conjectural"* — and not one of them had ever been asked where it stands on
**1835-07-01**. They do not answer alike, which is the whole finding:

| dossier zone | feature | at 1835-07-01 | what dates it |
|---|---|---|---|
| 14 | The slough | **present** (inferred) | a structure this project already stands in the scene |
| 15 | **The public-square pond** | **not established** (inferred) | nothing — and one document argues both ways |
| 16 | The Frog Pond, Lake & LaSalle | present (inferred) | a newspaper, one year late to the day |
| 17 | The Wells Street marsh | present (inferred) | the sentence that gives the slough gives what it drains |

**The sharpest thing in it is not the pond: the scene draws a BRIDGE over a watercourse the
scene does not contain.** `slough_log_bridge` is a committed structure standing on 1835-07-01 and
the source runs that crossing *"until after 1840"*, so a visitor walks onto a timber crossing laid
over open prairie. That is not an argument for cutting a conjectural channel — depth and width are
still unsourced and parcel (c) still owns them — it is the proof that the four were never on one
footing, which one shared phrase implied they were.

**Since, 2026-08-24 (T-0109).** Zone 14 came off the deferral list: **T-0005** carved it on
2026-08-20 and **T-0118** ran its last reach square under the crossing the same day, at the
reconstructed tier with depth and width declared invented in **L149**. So the bridge over nothing is
gone, and the reading is now taken rather than argued — `tools/measure_slough_crossing.py`, on the
committed heightfield: **3.30 m of open water in an 8.00 m span, 0.53 m deep, 2.35 m of dry abutment
seat at each end, the reach to the river unbroken, nothing else rooted in the cut.** The other three
zones stand exactly as this box left them, and the correspondence gate above still holds them: 15,
16 and 17 remain deferred and dated, and zone 14 no longer appears in the dating record because the
spec no longer defers it.

**On the pond itself the answer is `not_established`, and deliberately not "it was not there".**
One document, `chicagology_prefire273`, carries both sides. FOR: its slough sentence has the stream
draining *"the pond and the marsh extending up Wells Street"* as a live feature of a drainage
system whose bridge outlives the scene by five years. AGAINST, and the deferral weighed none of
these three — the quotation dates nothing (*"was then"*, past tense against an **1857** present, in
a document this project's own source record identifies as built on **Hubbard's Chicago of 1818**
and **Davis's 1832** drawing); the dossier's own row calls the pond **seasonal** with water
*"0.5–2 ft deep in spring"* against a scene dated **1 July**; and this project already stands the
**estray pen** on the square's south-west corner from **March 1832** and the **log jail** on its
north-west corner from the **fall of 1833**. A pound is not built in a pond.

**The buildings do not refute a pond — they BOUND one, and that is why the date and the extent are
one question.** A whole-block pond is refused by this project's own committed records; a partial
one is untouched by them and is exactly T-E5's third question, which no source reached can answer.
So the phrase's second half was never a detail to fill in later: the conjectural geometry is the
thing that decides whether water stands under Chicago's first public building.

**T-E5's fallback is discharged and NO LIBERTY IS OWED.** Its instruction was *"if it cannot be
made honestly, the honest answer is a `docs/LIBERTIES.md` entry saying the square is drawn dry and
why."* Nothing was invented, no confidence moved up, and the square was **already** drawn dry and
already recorded as such in text a visitor can read. What was missing was the reason, and the
reason is now in that same visitor-facing text — the four `why` strings `ground.js` renders. Prose
in the spec is stripped from the terrain's staleness hash, so it cost no bake.

**And it cost something downstream nobody would have gone looking for.**
`data/fauna/zones/f04_marsh.json` rested **three claims** on the pond quotation as in-scene
evidence, one of them saying so in as many words — muskrat `presence` and mallard `presence` were
`attested` on **that quotation alone**, noted as *"direct evidence of animals present in numbers at
a named location inside the scene box"*. **No grade moved**, and that is measured rather than
convenient: what carries `attested` is Andreas's *"ducks and muskrats in the marshes"*, and the
marshes he names **are** the habitat this zone plants — `z04_marsh`'s extent is a buffer of the
mapped water, the river-shore strip, and has never reached the square. The animal is attested in
the habitat the scene draws and is no longer attested at a named block the scene draws dry, and
the notes now say which of the two they mean.

**Shipped:** `data/terrain/1835_intown_water_dating.json` (authored, no coordinates, no geometry);
`tools/measure_intown_water.py` + a `tools/check.sh` step holding the correspondence **in both
directions**, so a fifth feature cannot be deferred undated and a dating entry cannot outlive the
deferral it grades; the four visitor-facing `why` strings; the three fauna corrections;
`docs/RESEARCH/public_square_pond.md`. **The gate was verified to fail** on four separate
injections — an undated deferral, an `inferred` grade with its reasoning blanked, a zone number
nothing defers, and a source that does not resolve — and to pass restored. A check that has never
failed is not a check.

**What it did NOT do:** it modelled, moved and sized nothing. All four features remain deferred to
parcel (c), and no research dossier was edited — those are committed verbatim, which is why the
disagreement lives in `docs/RESEARCH/`.

### T-E5(b) — how much of the square was wet · **UNCLAIMED · opened 2026-08-16 by T-E5(a) · Effort: M · NEEDS A BAKE**

What (a) deliberately did not answer. Its first question is not how to model an extent but
**whether any source states one at all** — (a) found none, and the two corners this project has
already built on are the only hard constraint anywhere in the evidence. Read
`docs/RESEARCH/public_square_pond.md` § 3 before touching it: a partial pond fitted to clear the
buildings is a number chosen to look right, which is the failure mode R-M1b is parked on and the
one this project has been handed twice. If the honest answer is that no extent is recoverable,
that is a finding and it belongs in `docs/LIBERTIES.md` — but (a) is not it, because (a) invented
nothing. Ground geometry means a bake either way.

<details>
<summary><b>The original T-E5 brief, as opened by T-A16 on 2026-08-15</b></summary>

`data/fauna/zones/f04_marsh.json` carries the finding in its own note: *"The Public Square —
Randolph to Washington, Clark to LaSalle — 'was then a pond, where the Indians had trapped the
muskrat, and where the first settlers hunted ducks'"*, from `chicagology_prefire273` at rung 2, and
`docs/research/08-fauna.md` line 44 and `docs/research/02-flora.md` line 40 carry the same water and
the slough draining it past the Tremont House site to the river at the foot of State Street. The
terrain carries none of it: there is no standing water on this block in any committed epoch, the
marsh flora zone's extent is a **buffer of the mapped water** so it plants nothing here, and the
square therefore renders as dry prairie with a pound, a jail and a court-house standing on it.

**Three things to settle before any ground moves**, and the third is the one that will bite.

1. **How much of the block, and when.** The quotation is a recollection published in 1857 of a
   period the writer dates loosely; *"was then"* is not July 1835. `data/exclusions.json` is the
   place for a researched-and-excluded reading if the pond turns out to predate the scene date —
   the estray pen went up on this block in March 1833 and a pound is not built in a pond.
2. **The slough is the same feature and is already half-recorded** — `docs/research/01-terrain-
   hydrology.md` row 14 gives its route documented and its depth and width conjectural. Whatever
   lands here should land with it rather than modelling a pond that drains nowhere.
3. **Three committed structures stand on this block**, two of them on corners Andreas gives. Water
   under a documented building is a worse error than no water at all, so the deliverable is
   probably a wet **part** of the square with the three public buildings clear of it — which is a
   claim about extent that no source reached supports. If it cannot be made honestly, the honest
   answer is a `docs/LIBERTIES.md` entry saying the square is drawn dry and why.

**Not urgent, and not a blocker for anything** — no roof is scheduled here now that T-A16 has
reserved the block.

</details>

## Bugs found and not yet fixed

### B-BUG1 — the nightly bake died at the finish line · **FIXED 2026-08-14**

Recorded because the shape of it will recur, not because it is still open.

The published-mirror smoke was added to the end of `tools/bake.sh` on 2026-08-13 21:00 UTC
(commit `7645be6`), and it was the right thing to add: the source tree and the published
tree do not load the same geometry, and a bug that flattened every building to a two-metre
box had already shipped past a green gate twice because nothing had ever loaded the
compressed derivatives.

`chicago-4d-bake.yml` does not install Playwright. So from that commit onward the nightly
did all of it — fetched Blender, generated, baked AO, compressed, published, gated **green**
— and then died on `Cannot find module …/playwright/index.js`, one step short of the step
that pushes the bake branch and opens the PR. Every night's output was discarded. Runs
`31761814117` (01:49Z) and `31771193146` (04:52Z) both read as a failed content build with
no clue in the summary that everything of substance had succeeded.

**Fixed** by installing `playwright@1.56.1` globally plus the matching Chromium in the bake
workflow. Nothing was skipped and no assertion was weakened — `SKIP_SMOKE=1` exists and was
deliberately not used, because a nightly that publishes without loading what it published is
the exact hole this smoke was added to close.

**The general lesson, for whoever adds the next gate:** `bake.sh` runs in two places with
different toolchains — a dev container that has Playwright and a runner that does not — and
a step added to the script is only really added once the runner can execute it. Check the
workflow in the same commit as the script.

### B-BUG2 — installing `ktx` turned on textures the renderer cannot read · **FIXED 2026-08-14**

The immediate sequel to B-BUG1, and the reason that fix was worth making: the moment the
bake could run its smoke again, the smoke found something.

`tools/bake.sh` asked for `--texture-compress ktx2` whenever a `ktx` binary was on PATH. That
is the wrong precondition. Whether the TOOL can write KTX2 says nothing about whether the
RENDERER can read it — and it cannot. The vendored `GLTFLoader` handles `KHR_texture_basisu`
only after `setKTX2Loader()` is called, nothing calls it, and no Basis transcoder is vendored
(it would have to be: `renderers/web/` takes no CDN).

So when the KTX-Software install landed on the runner, three derivatives came back with KTX2
textures — `blacksmith_shop_state_st__log_1823`, `brown_boarding_house__documented_1835`,
`beaubien_barn__converted_1817` — and each threw `THREE.GLTFLoader: setKTX2Loader must be
called before loading KTX2 textures`.

**All eleven failures in bake run `31773216178` are that one cause.** An asset that throws in
the loader is an asset that is not in the scene, so the count guard on the ground-contact
check (`n > 200`) saw 198 and tripped, and the raycast, click-to-inspect and inspect-from-the-air
checks had less town to hit. Nothing floated — the worst corner was 0.077 m, well inside the
0.15 m tolerance. Reading the failure list as eleven problems would have sent someone a long
way in the wrong direction.

**None of it left the runner.** The bake fails before its push step, so no branch, no PR, and
production was never touched: the published mirror as shipped carries zero KTX2 textures and
runs `403 passed, 0 failed`.

**Fixed** by gating the flag on an explicit `BAKE_KTX2=1` instead of on the binary's presence.
The `ktx` install stays — W2 needs it and it costs nothing idle.

**Turning it on is part of W2, in this order:** wire `KTX2Loader` plus a vendored transcoder
into the renderer, prove it loads a textured asset at both viewports, and only then set
`BAKE_KTX2=1`.

### B-BUG3 — the revived bake fired on every merge and piled up PRs · **FIXED 2026-08-14**

The third and last consequence of the bake never having worked: nobody had ever seen what it
does when it *succeeds* in a repo whose loop is running.

`chicago-4d-bake.yml` triggered on pushes touching `chicago/4d/data/**`, and carried no
`concurrency` group (both `deploy.yml` and the promotion have one). That was sound when data
changed rarely. It is not sound now — the steward loop's entire job this week is adding
structures, so nearly every merge into `dev` touches `data/**`. Between 06:42 and 12:19 the
bake opened **seven** PRs — #107, #110, #111, #113, #114, #116, #117 — each a full
regeneration of the same binary assets, each ~20 minutes of Blender, all mutually conflicting,
and all but the newest already stale against a `dev` that had moved on. Two pairs
(`31786785408`/`31786796289`, `31793910650`/`31793926909`) were racing runs seconds apart.

The workflow's own header said "never on every commit". The trigger list quietly stopped
honouring it once the loop changed what a typical commit looks like.

**Fixed** by dropping `data/**` from the push trigger — a change to a GENERATOR or to
`bake.sh` alters how everything is built and earns an immediate rebake, while a data change is
exactly what the nightly is for — and by adding `concurrency: { group: chicago-4d-bake,
cancel-in-progress: true }`. A superseded bake has nothing to offer: its output is measured
against a `dev` that has already moved, so cancelling it is the correct outcome rather than a
lost result.

**Left for the owner:** the seven open PRs. They hold real baked geometry and only the newest
(#117, based on the current `dev`) is current; the rest are stale and conflict with it. Closing
six and merging one is a judgement call about content, not a workflow defect, so it has not
been made here.

### R-REF1 — commit the reference photograph · **DONE 2026-08-15**

`bar/dupage_tallgrass_2018-07-24.jpg` — the verified July Illinois-prairie photograph this
project calibrates its sky against and reasons about tree-mass contrast from — **is not in the
repo.** Confirmed 2026-08-14: `git ls-files` returns nothing for it.

**It is now blocking two things, not one.** R-W1 named it *"the single thing most in the way of
judging these numbers"* — RENDERING §5's note 1 asks the targets to be re-anchored by measuring
a reference through this code, and that cannot be done against a file nobody has. And **`R-M1`
below needs it** to derive its thresholds from what a real dirt track holds against real prairie,
rather than from numbers picked to fit today's build.

**The whole parcel is: establish the rights, commit the file, register it as a source.** It is a
photograph like any other input — `data/sources/<id>.json` with its licence, provenance and a
`what_it_does_not_supply` list, exactly as every map in this dataset carries. If the rights do
not permit committing it, **say so in the source record and name a substitute** that does; an
uncitable calibration reference is a calibration nobody can check.

**Files:** the image · `data/sources/<id>.json` · `assets/LICENSES.md` · `docs/RENDERING.md`
**Acceptance:** `tools/check.sh` green; the file resolves; the rights are recorded, not assumed.

**DONE 2026-08-15.** The file is
`data/sources/assets/saari_2018_dupage_tallgrass/dupage_tallgrass_2018-07-24.jpg`, source
record `saari_2018_dupage_tallgrass`, licence row in `assets/LICENSES.md`, and both R-W1 and
R-M1 are unblocked. Full findings in `docs/STATUS.md` § "the photograph the sky is calibrated
against". Four things the next parcel should take from it rather than rediscover:

- **It is the right photograph and the numbers prove it.** `python3 tools/measure_reference.py`
  (new, Pillow-optional, deliberately outside `check.sh`) reproduces all four sky readings
  `world.js` quotes to within a few units, with nothing in the renderer touched. Identification
  never rested on the filename: the Commons description carries the same
  restoration-not-remnant finding the 2026-08-10 sweep made about this photograph, and the
  EXIF says 2018-07-24 09:32:25.
- **The frame is solved: `elevation(row) = (820 − row) / 57.0` degrees**, 14.4° above the
  horizon to 38.7° below, camera pitch −12.1° — which is the ~12° down-tilt the prairie sweep
  found independently. **Quote the elevation of any reading.** Both of this project's
  reference disagreements were two people measuring different heights in one photograph.
- **The rights are CC BY-SA 4.0 and they bite.** Verbatim redistribution and measurement are
  cleared; **any crop, resample, texture or LUT is an adaptation** and would put a ShareAlike
  obligation on this repository. R-M1 may measure it freely — it must not cut a tile out of it.
- **R-M1's fallback is not needed.** It was written to freeze provisional Weber figures "if the
  rights forbid committing it". They do not. ~~Derive the thresholds from the photograph.~~
- **CORRECTED 2026-08-15 by R-M1a: the photograph cannot supply R-M1's thresholds, and this
  bullet was wrong to promise it could.** It contains no bare-earth surface — widest contiguous
  bare run **8.2 % of the frame width, at −38.2°**, at the photographer's feet — so there is no
  dirt track in it to measure a road contrast against. `python3 tools/measure_reference.py`
  prints the survey. **Nothing else on this list is affected**: the sky, horizon and canopy
  readings R-REF1 landed all still reproduce, and they are what `world.js` and `trees.js`
  actually quote. R-REF1 unblocked R-W1's target re-anchoring, which was the other half of what
  it was for. See R-M1b for what a threshold source would now have to be.

### R-M1a — the two scales, measured and not gated · **DONE 2026-08-15**

**The parcel was split before it was claimed, under the lane's own run-budget rule.** R-M1's
acceptance names three builds to smoke — the pre-R-BUG2 build, current `dev`, and R-W1's
branch — and the rule above is that *a parcel whose acceptance needs more than TWO full smoke
passes must be split before it is claimed*. The seam that rule prescribes is
**(a) land the measurement and commit its numbers**, **(b) set the bars against them**, and it
earns more here than the time it saves: the baseline has to exist before anyone knows which
threshold it will justify, so (b) cannot quietly pick a bar and call it derived.

**What landed.** `weberContrast` and `relativeLuminance` are exported from
`tools/critic_metrics.mjs` — the first thing in `tools/` to compute Weber, which `trees.js` and
`LIBERTIES.md` have been quoting by hand — and every road band in `smoke_renderer.mjs` now also
reports **`weber`** (exposure-invariant road-against-ground contrast, magnitude, median over the
same probes) and **`groundL`** (median CIE L\* of the ground at those probes, the floor reading).
**Neither is gated.** Nothing this change touches can alter a pass or a fail, which is the whole
reason it is safe to land in one smoke: a gate that moves at the same moment as its own baseline
has no baseline.

**THE BASELINE, `dev@b287b31` + this branch, one full smoke, both viewports.** Gated bands only;
`weber` is the median magnitude, `n` the probes it is taken over.

| station | band | mobile 390×780 | desktop 1280×800 |
|---|---|---|---|
| `south_water` | 40–100 m | 0.1461 (n 34) · L\* 52.7 | 0.1570 (n 33) · L\* 53.5 |
| `south_water` | 100–250 m | 0.1482 (n 24) · L\* 53.1 | 0.1606 (n 36) · L\* 54.6 |
| `south_water` | 250–600 m | **0.5217 (n 15)** · L\* 52.0 | 0.1646 (n 11) · L\* 54.7 |
| `from_above` | 100–250 m | 0.1169 (n 40) · L\* 51.2 | **0.1217 (n 11)** · L\* 51.9 |
| `from_above` | 250–600 m | 0.1105 (n 150) · L\* 53.5 | 0.0999 (n 327) · L\* 53.9 |
| `lake_market` | 2–40 m | 0.1190 (n 10) · L\* 51.0 | 0.1326 (n 10) · L\* 51.5 |
| `lake_market` | 40–100 m | 0.1491 (n 15) · L\* 52.7 | 0.1288 (n 15) · L\* 52.7 |
| `lake_market` | 100–250 m | 0.1339 (n 43) · L\* 53.5 | **8.8023 (n 23) · L\* 3.0** |
| `lake_market` | 250–600 m | 0.1274 (n 122) · L\* 56.3 | **0.3965 (n 18)** · L\* 54.4 |

**The implementation is verified against a number this project committed before it existed, and
did not compute.** R-W1's parked measurement recorded Weber **0.1217** at `from_above`,
desktop, 100–250 m, `dev@d762a19`, taken by hand at the point of use. This helper reads
**0.1217 at n 11** against R-W1's **n=11**, on a `dev` that has moved eleven commits since.
That is a reproduction, not an agreement of adjectives, and it is the evidence that the two
halves of R-M1 are measuring one quantity. The 250–600 m band is the one that moved —
0.0940 → 0.0999 (+6.3 %), with ΔL\* 2.36 → 2.4 in step — which is R-BUG3's opaque-and-alpha
work showing up where R-BUG3 said it would not reach and is worth one line of R-M1b's attention.

**Three things (b) must not walk past, and the first of them is why this half was worth landing
on its own.**

- **WEBER IS UNBOUNDED BELOW, AND ONE BAND ALREADY PROVES IT. `lake_market`, desktop,
  100–250 m reads `weber 8.8023` over a ground of `L* 3.0`.** The denominator is the light the
  ground is carrying, and at that station-band, on that viewport, the road's projected probes
  land against something almost black — so a ratio that reads 0.13 on the same band at mobile
  reads **eight point eight** on desktop. Nothing is wrong with the road there; ΔL\* reads 18.0
  and 100 % perceptible. It is the scale that has no ceiling as its background goes dark.
  **A median Weber over a band can therefore be set by its darkest probes rather than by its
  roads**, which is the exact failure the owner's ruling anticipated when it paired the ratio
  with a floor rather than replacing one bar with the other. (b) has to say what it does about
  it — exclude probes below the floor, gate the two bars per-probe rather than per-median, or
  something better — and it must not simply threshold this column. **Had the bars been set in
  the same PR as the baseline, this is the number they would have been set against.**
- **`south_water` at 250–600 m is not a band, it is fifteen pixels.** Mobile reads **0.5217**
  against every other band's 0.10–0.17, on **15 probes seen of 510 projected**, and desktop
  reads 0.1646 on **11 of 637**. A threshold fitted to that station-band is fitted to whatever
  those few surviving probes happen to sit against. `ROAD_MIN_PROBES` is 8 and this clears it;
  the number that should worry a threshold-setter is the seen-to-projected ratio, not the count.
- **The floor is remarkably flat and that is a finding about the floor, not about the roads.**
  Every gated band on both viewports reads ground L\* **51–58**. A floor bar anywhere below ~50
  would never fire on any build this project has shipped, which makes it untestable rather than
  safe. R-W1's build is the one that moves it — 14–17 % darker — so the floor's value has to be
  derived against *that* branch or it is decoration.

### R-M1b — set the two bars · **UNCLAIMED · NEXT UP · from R-M1a · Effort: M · BLOCKED ON A THRESHOLD SOURCE**

Take R-M1a's table as the baseline. What is left is R-M1's original acceptance: the new bars
**fail on the pre-R-BUG2 build** and **pass on current `dev`**, R-W1's branch is re-run against
them **without re-tuning the streets**, every existing band still reports, and each threshold
carries its derivation in a comment beside it.

> ### THE DERIVATION SOURCE R-M1 NAMED DOES NOT EXIST. DO NOT SUBSTITUTE A GUESS FOR IT.
>
> R-M1 says to derive the thresholds by measuring "what contrast a real dirt track holds
> against real prairie" in the R-REF1 photograph. **It does not contain a dirt track.**
> `python3 tools/measure_reference.py` now surveys the land region of the frame and prints it:
> the widest contiguous bare-earth run anywhere below the horizon is **332 px, 8.2 % of the
> frame width, at −38.2°** — the bottom edge, at the photographer's own feet, and it is litter
> and dry stems between plants rather than a surface. The widest run with no green excess at
> all is **11.1 % at −0.4°**, which is the hazed treeline and is not ground. A track crossing
> that frame would put a contiguous bare run across a large fraction of the width at some
> elevation. Nothing in it does. The soil-like *fraction* is 3 % overall and rises to 18.5 %
> in the bottom 5° — which is exactly why the fraction cannot decide this and the run length
> can.
>
> This is the same shape of error the 2026-08-10 sweep recorded against itself: a brief handed
> a builder a target — *"Weber 0.036–0.067"* — that **"does not exist in the reference at any
> threshold"**, and STATUS.md says of it *"that error was the brief's, not the builder's"*.
> R-M1's threshold clause is the second instance. The sky, horizon and canopy readings the
> photograph *does* support are untouched by this and still reproduce.
>
> **So (b) needs a source, and picking one is above this lane's pay grade.** The honest options,
> for the owner rather than for a runner:
>
> 1. **A second reference photograph** — a documented dirt track through grass, CC-licensed,
>    committed the way R-REF1 committed this one, measured by the same code. It is R-REF1 again
>    in full: identification, rights, EXIF, a frame solved so a reading can state its elevation.
>    Call it **R-REF2**. It is the only option that makes "derived" literally true.
> 2. **A published detection threshold**, cited as such — Weber contrast at photopic levels for
>    a large suprathreshold target — with the bar set at a stated multiple of it and the
>    multiple argued in the comment. Honest, and it is a claim about *eyes*, not about *roads*,
>    which is a different bar than the parcel asked for and must be labelled as one.
> 3. **Freeze R-M1a's own baseline as a no-regression bar**, explicitly labelled provisional in
>    the code the way R-M1's struck-out fallback would have been. It is the weakest: it says
>    only "no worse than 2026-08-15" and it cannot fail the pre-R-BUG2 build unless the margin
>    is chosen, which is picking a number with extra steps.
>
> **Do not quietly take option 3 and describe it as derived.** If (b) arrives before the owner
> has ruled, land option 3 *labelled as option 3* and say so in the PR — or leave the bars
> ungated and say why.

#### R-M1 (spec) — the original parcel definition, kept verbatim

Unchanged except for the threshold-source paragraph, which is struck through below for the
reason R-M1b states. (a) discharged the helper, the two measurements and the baseline; (b) owns
everything else in it.

**The decision, made by the owner after R-W1 broke the gate by legitimately changing exposure:
score exposure-invariant contrast AND keep an absolute floor. Both bars, not a replacement.**

**Why the old metric was not wrong, only unguarded.** CIE `L*` is a perceptual scale — equal
steps are roughly equal perceived difference *under a fixed adaptation state*. That precondition
held for as long as exposure was fixed, and R-W1 is the first parcel to break it. ΔL\* did not
fail; its assumption did. Measured: R-W1 preserved the road/ground ratio to within **0.4 %** and
still lost the gate, because the scene got 14–17 % darker.

**Why a ratio alone is not the answer either.** Contrast sensitivity genuinely collapses at low
luminance, so a pure ratio metric would pass a scene too dark to see anything in. That is the
failure mode being traded into, and the floor is what prevents it.

**So: a contrast bar for "is the road distinguishable from the ground", and a luminance floor for
"is there enough light to distinguish anything at all".** Each catches what the other cannot, and
together they are strictly stronger than the single bar in place today. This is not a relaxation
and must not become one — the metric still has to FAIL on the pre-R-BUG2 build.

**Weber is a documented standard here, not a shared helper.** `trees.js:856` reasons in Weber
contrast against the bar photograph and `STATUS.md` / `LIBERTIES.md` quote it, but nothing in
`tools/` computes it. Expect to write the function. — **DISCHARGED by R-M1a**:
`weberContrast` and `relativeLuminance` are exported from `tools/critic_metrics.mjs`, and the
first thing they were used for reproduced R-W1's hand-taken 0.1217 exactly.

~~**Derive the thresholds; do not pick them.** Today's `ROAD_MIN_DELTA_L = 1.8` and
`ROAD_MIN_PERCEPTIBLE = 0.55` were set under one exposure and are now unanchored. The honest
source is the reference photograph — what contrast does a real dirt track hold against real
prairie? Hence **R-REF1 first.** ~~If the rights forbid committing it, freeze the measured Weber
figures from the last agreed-good build (**0.094 at 250–600 m, 0.118 at 100–250 m**, desktop,
`dev@d762a19`) as a provisional floor and **label them provisional in the code**.~~

**R-REF1 landed 2026-08-15, so the fallback is off.** The photograph is committed at
`data/sources/assets/saari_2018_dupage_tallgrass/dupage_tallgrass_2018-07-24.jpg` and its
readings reproduce (`python3 tools/measure_reference.py`). **Derive the thresholds from it.**
Two conditions come with it: quote the **elevation** of every reading — `elevation(row) =
(820 − row) / 57.0` degrees, the frame runs 14.4° above the horizon to 38.7° below — and
**measure it, never cut it up**. It is CC BY-SA 4.0: measurement and verbatim redistribution
are cleared, a crop or a resample is an adaptation that would put ShareAlike on this
repository (`assets/LICENSES.md`). The Weber figures above stay useful as the last
agreed-good build's numbers to sanity-check a derived threshold against, which is a different
job from being the threshold.~~

**STRUCK 2026-08-15 by R-M1a: the photograph contains no dirt track, so it cannot be the
source.** Measured, printed and reproducible — `python3 tools/measure_reference.py`. See
R-M1b's box above for what the options now are; the two conditions on *reading* the photograph
(quote the elevation, never cut it up) stand and apply to anything that measures it.

**Not a user setting, and the reasoning is worth keeping.** The gate runs headless in CI; there
is no user in the room. Its thresholds are already tunable in the right way — named constants at
the top of `smoke_renderer.mjs` with the reasoning beside them, so a change appears in a diff and
gets argued. Moving them to a config file would make them easier to change *without* review,
which is backwards for a gate.

**Files:** `tools/smoke_renderer.mjs` · `tools/critic_metrics.mjs` (the Weber helper) ·
`tools/measure_reference.py` (R-M1a, the survey that struck the threshold source)
**Acceptance:** the new bars fail on the pre-R-BUG2 build and pass on current `dev`; R-W1's
branch is re-run against them **without re-tuning the streets**; every existing road band still
reports; thresholds carry their derivation in a comment. — **all of it R-M1b's**, except
"every existing road band still reports", which R-M1a holds green by not gating anything.

### R-M1d — a band can collapse without the suite saying anything · **UNCLAIMED · UNSEEN · from R-W1 · Effort: S**

**The gate is per STATION and the measurement is per BAND, so a band that falls off a cliff under a
station that is already red is invisible.** R-W1 took `south_water` 250–600 m from **71 % of probes
perceptible to 16 %** — a 55-point collapse in the far road down a street — and the suite reported
**229 passed / 2 failed** before and **229 passed / 2 failed** after. Identical. Nothing in the
summary moved, because that station was already failing on its *100–250 m* band, and `bad.length
=== 0` cannot distinguish one bad band from two.

**A reader comparing tallies would have concluded the parcel cost nothing.** That is the same shape
of blindness as R-M1c one step up: there, an occluder could raise a score without anyone seeing;
here, a regression can happen without anyone seeing. Both are the suite reporting a verdict where a
figure was needed.

**Scope.** Bank each gated band's last figure and REPORT any band that moves against its own bank
by more than a stated margin, whatever the station's verdict. It is a report, not a new bar — the
thresholds stay exactly where they are — but it must be loud enough that a run cannot land a
55-point drop and describe the suite as unchanged. `roadContrast()` already returns everything
needed; nothing new has to be measured.

**Watch the direction.** This must not become a ratchet that forbids a band from ever falling —
R-W1 shows a band can fall for an honest reason. The requirement is that the fall is *stated in the
PR*, not that it is forbidden.

**Files:** `tools/smoke_renderer.mjs` (the `ROAD_STATIONS` loop), plus a banked figures file
**Acceptance:** replay R-W1's branch against `dev` and show the tool naming `south_water` 250–600 m
71 % → 16 % without being told where to look; no threshold moves; a band that rises is reported too.

### R-M1c — the road score divides by a number an occluder can shrink · **DONE 2026-08-16 (#207) — the denominator is `nBare`; this header was stale until 2026-08-17**

**A gate whose score IMPROVES when something hides the thing it measures is dividing by the wrong
number.** `roadContrast()` computes `perceptible` as `ds.filter(d >= 2).length / ds.length`, where
`ds` runs over the probes **SEEN**. Anything standing between the camera and a faint stretch of road
removes that stretch from the denominator, and the band scores higher for it.

**This is R-BUG3's own lesson surviving one level below where R-BUG3 fixed it.** R-BUG3 already
moved the decision of WHETHER to gate a band from "enough probes SEEN" to "enough PROJECTED", and
its comment says why: *"a band nobody can see reports n=0 and gates itself out, which is
indistinguishable from a band with no road in it."* The same argument applies to the score and was
not applied to it.

**THE INSTRUMENT WAS ALREADY BUILT AND ALREADY PRINTING.** The `shotMF` marker pass photographs the
same probes with the sward and the trees hidden, and its own comment states this parcel's finding in
full: *"A probe marked here but not in `shotM` is a road that is ON SCREEN and COVERED BY
VEGETATION, **which the marked-only denominator drops instead of failing**."* It was written as a
diagnostic, it has been reported in every band line for two parcels, and nothing ever divided by it.

**`nBare` is the denominator, NOT `nProjected` — and the difference is a claim about what a visitor
is owed.** A road behind a store is a road a visitor legitimately cannot see, and scoring against
`nProjected` would demand X-ray vision through the town's own buildings. Vegetation is different:
it is ours, it moves when we change it, and it must not be able to launder a faint road out of the
sample. `seen ⊆ bare` always, so the change can only ever LOWER a score.

**Measured on one band across three builds the same evening, and the case is the stability rather
than any single number.** Aerial anchor, 250–600 m, mobile, published mirror, same runner. The only
difference between the columns is what the near-field wood is doing:

| aerial, 250–600 m | wood mirrored (`dev` 3ea4e00) | wood repaired (R-BUG5b) | wood widened (K45(b2)) |
|---|---|---|---|
| probes **seen** | 157 | 177 | 163 |
| probes **bare** | **182** | **182** | **182** |
| perceptible probes | ~97 | ~96 | ~96 |
| score over **seen** (the old one) | **62 %** — passes | **54 %** — fails | **59 %** — passes |
| score over **bare** (this parcel) | **53.3 %** | **52.7 %** | **52.7 %** |

**The old score swung eight points three times while the number of readable stretches of road never
moved off ninety-six.** The build with a bug that stood the whole wood on the wrong side of the
river scored HIGHEST of the three; K45(b2) would have gone green by planting more timber in front of
the same road. The honest score is flat to half a point, and it is **under the 0.55 bar in all
three** — which is the real state of that band and always was.

**Scope.** Change `perceptible`'s denominator from `ds.length` to `nBare`; keep `n`, `nBare` and
`nProjected` all printing so occlusion stays legible as occlusion. Then re-read every band at every
station and write down what moves — this WILL turn bands red that read green today, and that is the
parcel, not a side effect.

**The thing this parcel must not do.** It must not arrive with `ROAD_MIN_PERCEPTIBLE` lowered to
absorb what it uncovers. If honest scoring puts a band under the bar, the band is under the bar, and
the fix is **R-W2**'s textured coverage or **R-W1**'s light — not a smaller number. Note that this
change makes scores strictly WORSE, never better, so it cannot be mistaken for a route through a
gate.

**Files:** `tools/smoke_renderer.mjs` (`roadContrast`, ~line 497)
**Acceptance:** the denominator is `nBare`; `n`, `nBare` and `nProjected` all still print; the
aerial 250–600 m band is shown reading the same on a mirrored-wood build and a repaired one; every band's new figure
is recorded in the PR; no threshold moves.

### R-A1 — a road-legibility accessibility aid · **DONE 2026-08-16 — shipped OFF by default, and the gate that proves it reaches the render had to be measured before it could be set**

**Read this box before adding any other preference to Settings.**

**What shipped.** A **Road visibility** slider, `roadAid` 0 → 1, default **0**. It scales the
street ribbons' alpha last in `streets.js`'s fragment patch — after the thin-ribbon floor and
R-BUG3's near lift — so it can never change which surface is fainter than which. `AID_GAIN` is
`1 / 0.24`: 0.24 is the faintest body alpha any surface authors (light worn earth at its crown),
so full aid takes that one surface to opaque, which is the ceiling R-BUG3 measured by forcing the
near probes opaque. At `uRoadAid == 0` the two added lines reduce to `min(a * 1.0, MAX_ALPHA)` —
the statement that was already there — so the default frame is the frame that shipped before the
control existed.

**Finding 1 — a "the default is unchanged" assertion is not enough, and R-BUG1 is why.** The
obvious gate for a preference is that it is inert at its default. That assertion passes
identically whether the control is wired correctly or **wired to nothing**, which is exactly the
failure R-BUG1 banked one parcel ago: `--no-sun-shadow` cleared a suspect it never reached and
reported "not the cause" for the same reason a broken thermometer reports a steady temperature.
So the aid is gated three ways, not one — **off at boot**, **raising it changes the frame**,
**dropping it restores the frame** — and the middle one is the load-bearing one. **The
generalisation: an inertness assertion needs a liveness assertion beside it, or it is a test that
a control exists rather than a test that it works.**

**Finding 2 — the instrument had to be measured before the threshold could be set, and the
default instrument was the wrong one.** The 12² frame signature the confidence view is graded on
averages the aid away: at `lake_market` the roadway is about a tenth of the frame, and the first
run scored **worst 2 counts against a restored residual of 0** — a real signal with no headroom to
gate on. At **48²** the same difference is **worst 6, mean 0.26**, residual still **0.00 / 0**.
Gated at worst ≥ 4 / mean ≥ 0.15, a third under the measurement. Both grids are printed.
**Nothing about the scene changed between those two runs** — only how finely the frame was
divided before it was compared, which is worth remembering the next time a delta gate reads
"barely".

**Why it was allowed to ship at all.** It was deferred 2026-08-14 because a contrast preference
converts a defect into a preference. R-BUG3 made the default correct on 2026-08-15 (near band
1.5 L\* / 30 % → **3.1 of a ceiling of 3.4 / 80 %** on mobile), which is the precondition the
deferral itself named. **It does not discharge R-W2**: the near band's *ceiling* is still the
lowest of any band and textured coverage is the honest fix for that.

**Files:** `renderers/web/js/streets.js` (the uniform, `setLegibilityAid`) ·
`renderers/web/js/hud.js` (`roadAid`, the range) · `renderers/web/js/main.js` (boot + `onSetting`
+ the harness handle) · `renderers/web/index.html` (the control and its note) ·
`tools/smoke_renderer.mjs` (three assertions).

**Not claimed:** the desktop half of the smoke — ~13 min against this runner's 10-minute
per-command ceiling. Mobile 390×780 is green, 229 passed / 0 failed on the published mirror. No
accessibility standard is claimed to be met, and `docs/LIBERTIES.md` is untouched: the default
rendering is unchanged to the digit.

**The original box, for the reasoning that gated it:**

Considered and deliberately deferred, 2026-08-14, because the reasoning matters more than the

Considered and deliberately deferred, 2026-08-14, because the reasoning matters more than the
feature. A user control that boosts road contrast **converts a defect into a preference** and
takes the pressure off fixing the default. `K24`'s lighting setting is defensible because both
positions are legitimate and the default is the evidence-anchored one; *"roads you cannot see
while standing on them"* is not a position worth offering.

**But the accessibility case is real** — contrast sensitivity varies, and a phone screen in
sunlight is brutal, which is the exact condition R-BUG3 was reported from. So this ships as an
aid layered on a correct default — **R-BUG3 made the default correct on 2026-08-15, so the
precondition is met** — and it inherits `K24`'s constraint: the harness measures the default
regardless of stored preference. Note what R-BUG3 left standing: the near band's *ceiling* is
3.4–4.3 L\*, the lowest of any band, and a fifth of near probes cannot clear the threshold even
fully opaque. The honest fix for that is **R-W2**'s textured coverage, not this aid; shipping
this one must not be allowed to retire that.

### R-BUG3 — the road is invisible AT YOUR FEET · **PARTLY DONE 2026-08-15 · REOPENED as R-BUG3c**

**What it took, and what it refuted.** The near band was added, it failed exactly as this parcel
predicted — **1.5 L\* with 30 % of probes perceptible at 2–40 m, against 3.4 / 87 % in the very
next band out** — and it is now **3.1 of a measured ceiling of 3.4, with 80 % perceptible** on
mobile (3.2 of 4.3 with 60 % on desktop), on the published mirror. Three
findings came out of it, and only the third is the one this parcel expected:

1. **The near band was EMPTY, and no threshold would have caught this bug.** `[2, 40]` on its own
   changes nothing, because **neither gated station stands on a road**: `south_water` sits **101 m
   from the centreline it is named after** (that is T-V2, measured from the committed path) and
   17 m from the nearest one, and `from_above` is 175 m up. The near band collected **one probe**
   at the first station and **none** at the second. The parcel's own first move was necessary and
   nowhere near sufficient — the window was wrong in TWO dimensions, distance and pose, and only
   the distance one was visible from the failing gate. There is now a third station,
   `lake_market`, which arrives the way a visitor does — by clicking a verified street-control
   intersection in the Go to tab — and then turns to look along the centreline it is standing on,
   a bearing read off the committed path rather than authored here. The arrival pose alone was
   not enough either: the shipped jump faces a fixed bearing, which at a crossing points
   diagonally into the block and put **zero** road probes inside 100 m.
2. **THE PRIME SUSPECT IS REFUTED — no grass is hiding this road.** The harness now re-shoots its
   road markers with the sward and the trees hidden, so an occluded probe is distinguishable from
   an absent one, and in the near band **all ten probes are marked either way**. Sward occlusion
   and the clearing-corridor width are both out, this parcel's non-licence never had to be tested,
   and `flora.js` is untouched. The gate reports the discrimination on every band from now on
   (`seen N of M projected (K clear of flora)`) because it is the distinction three gates in a row
   have failed to draw.
3. **The fault is candidate 3, and the mechanism is sharper than "alpha".** An alpha here is a
   **coverage fraction**, and a coverage fraction is only the right picture of a mixture where one
   pixel spans many patches of it. Up close one pixel spans one patch, which is either earth or
   grass, and the blend paints a uniform wash instead. The harness measures both ends: the same
   near probes forced fully **opaque** score **3.4 L\***, so the contrast was in the ribbon's own
   colour and the shipped alpha was spending under half of it. The near field also has less to spend — the
   ground underfoot is genuinely darker than at range, **L\* 51.0 against 52.7–56.3** — which is
   why spending it matters here and not at 250 m. The fix scales alpha by 2.4 inside 15 m, fading
   to nothing by 40 m; every band past the fade is unchanged to the decimal, which is the
   arithmetic guarantee and also the measurement. Recorded as **L98**.

**And one lesson for the gates, which is the durable part.** A band gated on *how many probes were
SEEN* gates itself out at exactly the moment the thing it measures goes wrong: a road nobody can
see reports n=0 and is indistinguishable from a road that is not there. The bands are now gated on
how many probes were **PROJECTED** — on screen and therefore owed a picture. That is the third
time this bug has been a question of what the gate was pointed at, and it is the first fix that
makes the gate fail loudly rather than quietly abstain.

**One more thing the opaque pass taught, and it is a gate lesson too.** Its first form dropped the
ribbon into the opaque queue without letting it write depth, so the terrain painted back over it
and the pass reported a **0.0 ceiling under a perfectly healthy road**. It writes depth now, like
the marker pass it should always have mirrored. A diagnostic that lies quietly is worse than none,
and this one lied in the direction of "nothing to see here" — the same direction as everything else
in this bug's history.

**And a second fault, found by the new station and fixed with it.** At desktop, 100–250 m from the
crossing, the ribbon scored **0.0 L\*** with the marker pass frontmost: R-BUG2's fault 1 again, its
polygon offset having been tuned until the bands *at the two stations then gated* passed. Deepened
to the marker's own values, that band reads **18.0 L\* at 100 % perceptible**. The number was never
wrong; the sample it was tuned against was.

**Not done here, and deliberately:** the near band has the least headroom of any band a walker
actually stands in — its opaque ceiling is **3.4 L\* on mobile and 4.3 on desktop**, against
5.9–6.9 at the same station's 40–100 m and at both aerial bands — and **20 % of near probes on
mobile, 40 % on desktop, cannot clear the perceptibility threshold even fully opaque**. Say it
that way rather than "the lowest of any band": at `lake_market` the 600–4000 m band's ceiling is
lower still (3.2 mobile), which is a road at a kilometre and not the thing this parcel is about.
L98 names the honest fix — a textured coverage, earth and grass resolved as patches at the scale a
near pixel can show, so the eye integrates the recorded fraction instead of the blender pre-mixing
it. That belongs to **R-W2** (texture the town), which is where the 1.4 texture score lives.

<details>
<summary>The parcel as opened, 2026-08-14</summary>


Reported by the owner 2026-08-14, on mobile, on the **dev preview** — so **with the R-BUG2 fix
already in**: standing on Franklin Street approaching Randolph, the wheel ruts read clearly in
the mid-distance and **the road is simply not there in the near field**. *"It should not be
invisible when I am standing on it."*

**R-BUG2 is working. This is the band it never measured.** Its gate is
`ROAD_BANDS = [[40, 100], [100, 250], [250, 600], [600, 4000]]` — **the nearest band starts at
40 metres.** Everything from the walker's feet out to 40 m was outside the sample, so the road
could be perfectly invisible underfoot while every gated band passed at 3.6–14.3 ΔL\*. The
measurement was sound and the fix was real; the window was wrong.

**That is the lesson worth taking, and it is the second time on this same bug:** the first gate
measured the geometry and never asked whether the road reached the screen; the second asked, but
only past 40 m. A gate answers exactly the question it was pointed at.

**SPLIT IN TWO — see "the run budget is 150 minutes" above. Claim ONE.**

**R-BUG3a — land the near-field band, red.** Extend `ROAD_BANDS` with a `[2, 40]` band (below
~2 m the surface is under the camera and degenerate). `roadContrast()` already has the
machinery: the opaque-marker denominator **M** works identically here, and a road occluded by
grass stays in the sample and scores as *a road that covers a pixel and does not change it* —
exactly the signature wanted. **Commit it FAILING, with the measured numbers quoted**, and stop.
One smoke pass. That failure is this half's acceptance, and committing it before anyone knows
which cause is guilty is what stops the fix redefining success.

**R-BUG3b — turn it green.** Takes R-BUG3a's committed numbers as the baseline and works the
candidates below. One smoke pass. **Do not start until 3a has landed.**

**Candidate mechanisms — measure before choosing.** That instruction is what saved R-BUG2 from
a fix that would have made things worse, and it applies again:

1. **Near-field sward occlusion, and this is the prime suspect.** At eye height the grass
   nearest the camera is enormous in screen space and stacks, so the road can be completely
   hidden within a few metres even at a *correct* planting density. The existing check —
   `street clearing removes travel-track plants but preserves the block` — is a boolean on one
   street and one block. It cannot see this.
2. **The clearing corridor is narrower than the drawn track**, so the ribbon's edges are
   planted over even where the centre is clear.
3. **Alpha under magnification.** R-BUG2 raised the baselines to 0.54/0.38/0.28 and added a
   sub-pixel floor that *scales alpha up* below 2 px — which by design does nothing up close,
   where the ribbon is widest. A worn track at 0.38 seen through near-field grass may simply
   not be enough.

**The non-licence, and it is a real constraint.** Do **not** fix this by clearing grass around
every road. Each community's ground cover is a dataset claim with its own gate — *"the sward is
planted at each community's own recorded cover"* — and widening a clearing corridor to win a
contrast score would be falsifying a recorded figure to pass a test. If the corridor genuinely
should be wider, that is a change to the record with its reasoning, not a tuning constant.

**Files:** `tools/smoke_renderer.mjs` (the near band) · `renderers/web/js/flora.js` (clearing) ·
`renderers/web/js/streets.js` (alpha) · `docs/LIBERTIES.md` if a recorded cover or corridor moves

**Acceptance:** the near band gated and green at both viewports, with the fault put back to prove
the check names it; every existing road band still green; the per-community sward cover check
untouched and still passing. **Mobile is the report and mobile is the gate** — 390×780 is where
it was seen.

</details>

### R-BUG3c — the near ground is missing, and it is NOT the streets · **DONE 2026-08-15**

**R-BUG3c-b is DONE (2026-08-15) — NEITHER surface moved. The publish step moves the mesh
AFTER the only gate that measures it.**

(a) asked which of the two was wrong and refused to guess. The answer is neither: the drawn
ground and the sampler are both faithful to the terrain spec, and the disagreement is
introduced between the generator and the browser, by `gltf-transform optimize` in
`tools/bake.sh`.

**Measured on the committed bytes** — `tools/measure_terrain_fit.mjs`, a third reader of this
geometry, which decodes `EXT_meshopt_compression` and `KHR_mesh_quantization` the way the
renderer does and compares vertex heights against the same `heightfield.bin` the walker samples:

| mesh | lattice | mean | rms | max \|Δ\| |
|---|---|---|---|---|
| `assets/gltf/` **master** — what the generator gates | float | −0.0 mm | 1.4 mm | **2.5 mm** |
| `assets/web/` **shipped** — what a browser loads | **306.4 mm** | 5.0 mm | 85.1 mm | **227.6 mm** |

The master honours `MESH_FIT_TOLERANCE_M` to **2.5 mm**, which is the heightfield's own
quantisation error — it is as exact as the field it is built from. The derivative published
beside it is off by up to **228 mm**.

**Why, precisely.** `gltf-transform` quantises POSITION to a **bit depth — 14 by default** —
under ONE UNIFORM node scale, and stores the result in the next integer type up, so the low
two bits are always zero. The uniform scale is set by the widest axis. This mesh is
**5,020 m wide** (a 2,020 m box plus `SKIRT_MARGIN_M` = 1.5 km of apron on each side) and
**8.6 m tall**, an aspect ratio of 580:1, so the vertical rung spacing is
`5020 / 16383` = **306 mm**. The skirt — whose entire job is to carry the channel past the
box edge — is what sets the precision of the ground the town stands on.

**And no setting fixes it, which is the part that decides the shape of the fix.** Measured, not
argued: `--quantize-position 16`, the maximum the format offers, lands on a **76.6 mm** lattice
(rms 22.0 mm, max 54.4 mm) — still over the 30 mm the generator refuses to export past.
`--meshopt-level medium` quantises identically and costs 166 KB more. Only `--compress false`
meets the tolerance, at **6.45 MB against 688 KB**.

**So the renderer reads the heights back off the field at load** —
`conformGroundToField()` in `js/terrain.js`. Not a correction factor and explicitly not the
`LIFT_M` fudge (a) forbade: the heightfield is *already* the authority for collision, building
anchoring, flora roots and street drape, so this makes the surface a visitor SEES the same
surface as the one the town is placed on, by construction rather than by tolerance. The GLB
keeps the jobs the field cannot do — the decimated topology, the normals, the `_CONFIDENCE`
channel. All **124,141** vertices move, by up to **227.6 mm**, and the residual afterwards is
**0.24 µm**, which is float32 storage and nothing else.

The skirt is carried rather than flattened: it lies outside the box, where `sample()` returns
its **fallback of 0** instead of clamping, so snapping it naively would have dropped 1.5 km of
apron onto the water plane. Sampling at the clamped position reproduces the generator's own
rule for the skirt — "carry each boundary vertex outward, keeping its own height" — and the
seam at the box edge closes exactly.

**Three gates missed this, and the reason they all missed it is the same.** The normals gate,
the road-contrast gate and the horizon gate each compare the render to another render. A
quantised ground is a *correct-looking* ground; it is only wrong relative to a measurement
none of them held. Two new gates hold it:

- **`tools/check.sh`** — asserts the committed MASTER still meets `MESH_FIT_TOLERANCE_M` and
  REPORTS the derivative's drift. Nothing re-checked the master after the bake, because the
  generator's own refusal happens inside a Blender run this gate cannot make; a hand-edited GLB
  would have sailed through every check in this repo. The derivative is reported and **not**
  asserted, because it cannot pass and saying so would only assert that a compressor is a
  compressor.
- **`tools/smoke_renderer.mjs`** — asserts the surface actually DRAWN, at the tiles' own
  vertices after every load step, against the sampler the town is placed with. That is the
  comparison none of the three made. Green at **both** viewports.

**What is NOT repaired, and is a question rather than a defect.** The same quantiser moves E and
N by up to **153 mm**, which is invisible on a decimated prairie and is why only Y is read back.
Whether the terrain should ship quantised at all — 688 KB with a lattice, against 6.45 MB
exact — is a payload decision with an owner-facing cost, so it is **R-W6** below rather than
something this parcel settled on its own. The fix here makes that answer stop mattering for the
ground a visitor stands on.

**The gate lesson, for the fourth time on this bug: do not measure the file you built. Measure
the file you ship.**

**The owner reproduced R-BUG3 on the branch that fixes it**, on mobile, on Lake Street approaching
Franklin — the same complaint, after the parcel below declared it solved. Reproduced here at that
exact pose (`walker.teleport` to the committed Lake x Franklin intersection, 52.4 m back, facing
Lake's own centreline bearing, 390x780). Findings, all measured, none inferred:

1. **It is not the alpha, and no alpha can reach it.** With the streets forced fully OPAQUE,
   depth-writing, at the marker pass's own polygon offset — nothing able to hide them — the ribbon
   still reaches only **row 937 of 1560**. The bottom **40 % of the frame contains no roadway at
   any opacity**. R-BUG3's `NEAR_GAIN` is scaling the alpha of fragments that are not drawn.
2. **It is not a streets bug.** Per-row high-frequency energy across the same frame collapses from
   **1.0-2.4 above row 1000 to 0.2 below row 1120** — a 5-10x drop. Below that line there is no
   road, **no grass tufts and no ground texture at all**: a smooth green wash. Everything that
   sits on the ground vanishes together, at one radius, which is why the edge is a clean
   horizontal line — a constant distance from the camera.
3. **The geometry exists.** `STEP_M = 2.25`, `LIFT_M = 0.022`, and **32 street vertices lie within
   10 m of the camera** at this pose. Something is burying them; they are not absent.
   (A first probe reported "no vertex within 1.5 m of the centreline" — that was the PROBE's
   error, not a finding: a ribbon quad's four corners are all at +/- half the track width, so
   there are never vertices ON the centreline. Do not repeat it.)

**SUPERSEDED ON MECHANISM by #145, 2026-08-15 — read that first.** The measurements below stand and
reproduce; the CONCLUSION drawn from them, that the two are 'different data', was wrong about why.
#145 found the cause: **the publish step quantises the mesh after the only gate that measures it**, so
neither ground moved. Both measurements here were taken against the PUBLISHED mirror — which is the
right target for a visitor-facing bug and the wrong one for asking which source surface is
authoritative, because the published copy is not the surface either generator emitted. The spread of
±3 m is the quantisation grid, not a disagreement between the GLB and `heightfield.bin`.

**THE HYPOTHESIS IS CONFIRMED, AND IT IS WORSE THAN STATED — measured 2026-08-15.**

The ground that is DRAWN is not the ground that things are PLACED on, and the gap is an order of
magnitude larger than the road's own lift. Measured at the owner's pose by finding, for each sample
point, the actual triangle of the ground mesh above it and interpolating its height — no raycaster,
no assumption about how the mesh is built:

| d (m) | `surfaceHeight()` | drawn ground | drawn − sampled | road placed at | buried |
|---|---|---|---|---|---|
| 2 | 0.775 | **0.906** | **+0.131** | 0.797 | yes |
| 10 | 0.781 | 0.906 | +0.125 | 0.803 | yes |
| 25 | 0.790 | 0.906 | +0.116 | 0.812 | yes |
| 50 | 0.805 | 0.906 | +0.101 | 0.827 | yes |
| 100 | 0.810 | 0.906 | +0.096 | 0.832 | yes |

**The drawn ground sits 9.6–13.1 cm ABOVE the sampler, over the whole hundred metres.** `LIFT_M` is
**22 mm**. The road is under the visible ground along its entire length here and never had a chance;
so is every plant rooted by the same sampler, which is why the grass tufts vanish with it.

**Then why is the road visible beyond ~7 m at all?** Because the polygon offset wins at range and
loses up close: depth-buffer resolution is finest near the camera, so a fixed ~12 cm burial is
decisively resolvable at 5 m and swamped by the offset at 50 m. The crossover depends on distance
alone — which is exactly why the edge is a clean horizontal line at a constant radius, the one
feature of the screenshots no other explanation accounted for.

**The walker is inside the hill.** Eye is at 2.455 with the sampler at 0.775 — 1.68 m of eye height,
as recorded — but the drawn ground under that same point is 0.906, so a visitor stands **13 cm sunk
into the terrain they can see**. Collision, building anchoring, flora roots and street drape all use
the sampler, so this is not only a road bug: **everything in the town is anchored to a surface that
is not the one on screen.**

**What has NOT been established, and must be before anything is changed.** Which of the two is
wrong. The drawn mesh is a baked GLB; the sampler reads `heightfield.bin`; both descend from the
same terrain spec, and this measurement says only that they disagree, not which one moved. Do not
"fix" this by raising `LIFT_M` — that hides a 13 cm datum disagreement behind a fudge and leaves
buildings and collision still wrong. Find out why the two disagree.

**The original hypothesis, as written before the measurement:**

**The hypothesis to test FIRST, and it is only a hypothesis.** Roads and flora are both PLACED
with `terrain.surfaceHeight()`. If the terrain that is DRAWN sits above that sampler near the
camera, both are buried by the same few centimetres at the same radius — which is the symptom
exactly. It would also fit **R-BUG1** (the river edge flickering when flying). Measure the drawn
terrain surface against `surfaceHeight()` before changing anything.

**And the gate lesson, for the third time on this one bug.** R-BUG3 added a station that stands
*at* the Lake/Market crossing — one of the few places the near ground is intact — and it went
green. The owner was 172 ft short of an intersection. A station AT a crossing cannot speak for the
block between crossings. Add a mid-block station on foot before claiming this closed.

**Do not re-declare this done from a passing gate.** Shoot the frame and look at it.

### R-W6 — should the terrain ship quantised at all? · **DONE 2026-08-16 · opened by R-BUG3c**

**YES, AT 16 BITS — and the artefact was NOT invisible, which is the finding.** This parcel was
written expecting to confirm that the horizontal displacement cannot be seen and to raise the bit
depth because it is free. The second half stands; the first is wrong. Measured on the bytes that
ship, the 14-bit ground stands **up to 46.3 mm above the field the town is placed on**, past the
**22 mm** road lift at **87** of the field's 259,689 sample points, 44 of them on dry ground —
**and the closest of those stands 1.9 m from the centreline of South Water Street**, inside a
10.5 m travelled track, 30.2 mm over a road that is lifted 22 mm. That is R-BUG3c's own failure
mode, on the street the owner reported it from, surviving the fix at 1/5 the size and 0.03 % of
the town. `tools/measure_terrain_horizontal.mjs` is the new reader; `--mesh f.glb=label` prices
any candidate derivative against the same columns.

**The trade is not the one the box below describes, because 16 bits is nearly free and nearly
exact.** Every row measured with the same `gltf-transform` the bake runs, on the committed
master, and the 14-bit rebuild came back **byte-for-byte identical to the file in
`assets/web/`** — so these are the shipping numbers, not a simulation of them:

| encoding | KB | vertical lattice | \|Δy\| handed to the browser | plan displacement | **drawn surface vs the field, after conforming** | past the 22 mm lift |
|---|---|---|---|---|---|---|
| master (`assets/gltf/`) | 6296 | float | 2.5 mm | — | 1.3 rms / 3.8 p99 / **7.7 max** | — |
| **shipped today, 14-bit** | **671** | 306.4 mm | 227.6 mm | **273.1 mm** | 2.1 / 7.9 / **46.3** | **87** (44 dry) |
| 15-bit | 677 | 153.2 mm | 107.0 mm | 131.0 mm | 1.5 / 4.5 / **22.4** | 1 |
| **16-bit — TAKEN** | **672** | 76.6 mm | 54.4 mm | 52.0 mm | 1.4 / 3.8 / **12.9** | **0** |
| no compression | 6296 | float | 2.5 mm | 0.0 mm | 1.3 / 3.8 / **7.7** | 0 |

Four things in that table are worth more than the decision:

- **The last column is measured at all 259,689 of the field's own sample points, after
  `conformGroundToField()`** — the surface a visitor is actually shown, read by interpolating
  the containing triangle in plan the way a rasteriser does. Not at three camera anchors: an
  anchor set cannot answer a question about 1.6 km² of ground, and R-BUG3's own gate went green
  standing 172 ft from the fault.
- **The master's 1.3 mm rms / 7.7 mm max is DECIMATION, and every row carries it.** So the
  uncompressed file buys 12.9 mm → 7.7 mm for **5.8 MB**, and what is left after that is not the
  compressor's to give back. That is the whole answer to "should it ship quantised at all".
- **The mechanism is slope, not size.** A vertex conformed at a displaced position holds the
  field's height for the wrong place, so the cost is (slope × displacement): the 87 over-budget
  samples sit at a **median slope of 18 %** — bank faces, the sand ridges, the harbour cut —
  and flat platted prairie cannot show this artefact at any bit depth.
- **R-BUG3c's "E and N move by up to 153 mm" was arithmetic — half of the 306.4 mm rung — and
  the measured figure is larger**: 203.6 mm east, 182.0 mm north, **273.1 mm in plan**. Quote the
  measured one. (Its 16-bit row reproduces exactly: 54.4 mm.)

**Precision is per-mesh, and only two meshes in this town are big enough to care.**
`gltf-transform` quantises POSITION under one uniform node scale set by the mesh's OWN bounding
box, so an asset's lattice is its widest axis over 2^bits — nothing to do with how fine its
details are. Across the 244 derivatives that ship quantised: `water__e1834_harbor_cut` 330.8 mm,
`terrain__e1834_harbor_cut` 306.4 mm, `north_pier` 16.8 mm, and **every other asset ≤ 4.8 mm,
median 0.5 mm**. So the bit depth is raised on the epoch meshes and left alone everywhere else:
**+1,116 bytes**, against **+105.7 KB (+2.4 %)** measured for 16 bits across the whole payload to
buy nothing anything can see. `EPOCH_QUANT_BITS` / `ASSET_QUANT_BITS` in `tools/bake.sh`.

**Two smaller measured facts, recorded so nobody re-derives them:** 15 bits is BIGGER than 16
(693.4 KB against 688.3) — do not "optimise" to it; and the water mesh is four vertices at
exactly y = 0, which lands on the lattice at every bit depth, so its 330.8 mm rung never had
anything to spoil and its derivative is byte-identical either way.

**The skirt split is NOT taken, and that is now a measurement rather than a deferral.** The idea
below is sound — 1.5 km of apron on each side is what sets the quantisation volume — but at 16
bits every one of the 259,689 samples is already inside the tightest budget this town has, so
splitting the skirt would buy precision nothing is waiting on, at the cost of a generator change,
a `docs/GLB-CONTRACT.md` amendment and a bake. Reopen it if a future epoch's box grows or the
ground gets a tighter consumer than the road lift.

**What is NOT verified here:** the desktop half of `tools/smoke_renderer.mjs` (the ten-minute
per-command ceiling — see "the run budget" above). The **mobile** half was run against a
published mirror carrying the 16-bit ground: **218 passed, 0 failed, zero page errors**,
including the drawn-surface-against-the-sampler assertion R-BUG3c added. **No GLB is committed by
this parcel** — `assets/web/` is the bake's to write, and the ground reaches the site with the
next nightly `chicago-4d-bake.yml`. Until it does, the shipped ground is the 14-bit one this box
measures.

**Files:** `tools/bake.sh` (the two-stage optimize + meshopt pass, and the per-mesh bit depth) ·
`tools/measure_terrain_horizontal.mjs` (new) · `tools/measure_terrain_fit.mjs` (exports its
reader rather than growing a fourth one) · `docs/RENDERING.md` · `docs/STATUS.md`

---

**The parcel as written, for the record:**

R-BUG3c found that the published ground mesh lands on a **306 mm** vertical lattice and fixed
the consequence rather than the cause: the renderer reads the heights back off the heightfield,
so the ground a visitor stands on is correct whatever the compressor does. This parcel asks
whether the cause is worth removing.

**The numbers are already measured** — see R-BUG3c's table and
`tools/measure_terrain_fit.mjs`:

| encoding | size | vertical lattice | max \|Δ\| vs the field |
|---|---|---|---|
| shipped today (meshopt, 14-bit) | **688 KB** | 306.4 mm | 227.6 mm |
| meshopt, 16-bit (the format's max) | 688 KB | 76.6 mm | 54.4 mm |
| meshopt, `--level medium`, 16-bit | 854 KB | 76.6 mm | 54.4 mm |
| no compression | **6.45 MB** | float | 2.5 mm |

**What is still open, and it is genuinely a decision rather than a measurement.** 5.8 MB is a
real cost on the phone this project was reported from twice, and the conforming pass has made
the height error harmless. What remains wrong is the **horizontal** displacement — E and N move
by up to **153 mm** — which nothing corrects and which nobody has yet shown a visitor can see.

**So the honest order is: measure the horizontal artefact BEFORE trading 5.8 MB for it.**
`tools/critic_shots.mjs --metrics` exists for exactly this kind of "can you see it" question.
If it is invisible at the anchors a visitor is offered, the answer is to keep the 688 KB, raise
the bit depth to 16 because it is free, and write the reasoning down. Do not answer this by
preference, and do not answer it by reaching for the uncompressed file because exactness feels
safer — page weight is a user-facing cost the same way a buried road is.

**One thing to check first, because it may make the whole trade cheap:** the 5,020 m width that
sets the lattice is mostly `SKIRT_MARGIN_M` — 1.5 km of apron on each side of a 2,020 m box. A
skirt emitted as its own mesh would shrink the ground's quantisation volume by 2.5×
(`--quantization-volume mesh` is already the default), which at 16 bits would put the lattice
near 31 mm for nothing but a generator change. That needs a bake, so it is a proposal to
`docs/GLB-CONTRACT.md` and `generators/terrain_gen.py`, not a unilateral edit.

**Files:** `tools/bake.sh` · `generators/terrain_gen.py` (skirt split, if taken) ·
`docs/RENDERING.md` · `docs/GLB-CONTRACT.md` (propose). Measurement first.

### R-BUG4 — a wet corner deletes the whole road quad, dry half included · **DONE 2026-08-15**

**DONE 2026-08-15.** The edge test clips at the waterline now instead of deleting the panel. Each
end is trimmed on each side INDEPENDENTLY by bisection out from the dry centreline — asymmetric on
purpose, because a bank road is wet on one side only and shrinking it symmetrically would throw the
dry verge away too. The centreline test is untouched: a road whose centre is in the river is a
crossing, and that is a bridge's job.

**Measured on the built geometry, not on a replay of the rule:** 4,843 panels have a dry
centreline, **all 4,843 now reach the ribbon**, **28 of them clipped at the waterline**, **0**
dropped as sub-metre slivers, and **62.7 m of roadway recovered**. The `13 quads / ~30 m` first
recorded here was read off a truncated probe listing and was **half the true figure** — a reminder
that a sorted table read from its tail is not a total.

The gate asserts the INVARIANT rather than the number: every panel with a dry centreline reaches
the ribbon, the only permitted absences being sub-metre slivers, which are counted and printed. It
also asserts that clipping actually happens, so a later simplification back to deleting the panel
fails in CI rather than in a screenshot. The existing "no street vertex stands on water" assertion
is unchanged and still passes — the clip stops at dry ground by construction.


Owner-reported 2026-08-15 from South Water Street: a clean-edged green quadrilateral punched
through the roadway ahead. Straight edges mean geometry, and it is the size of one road quad.

`streets.js addRecord` drops a quad when the centreline OR **any of its four corners** is water:

    if (terrain.isWater(a) || terrain.isWater(b) || corners.some(isWater)) { continue; }

The comment says the edge test exists to "keep a bank road from painting over water just because
its legal corridor reaches it" — a fair aim, and the wrong instrument. **The remedy for "do not
paint over water" is to CLIP the quad at the waterline, not to delete it**, because deleting takes
the dry half with it. On a bank road the corridor's outer corner grazes the mask constantly.

Replayed against the shipped mask, per street:

| street | quads | dropped: wet CENTRE | dropped: wet EDGE ONLY | metres deleted | % |
|---|---|---|---|---|---|
| Kinzie | 632 | 84 | **6** | 202 | **14.2 %** |
| Lake | 543 | 34 | 1 | 79 | 6.5 % |
| Washington | 543 | 20 | 1 | 47 | 3.9 % |
| Canal | 357 | 13 | 2 | 33 | 4.2 % |
| Randolph | 544 | 22 | 0 | 49 | 4.0 % |
| South Water | 341 | 4 | **3** | 16 | 2.1 % |

The **edge-only** column is the indefensible part. **The table above understates it**: it was read
off a truncated listing, and the whole-town figure measured from the built geometry is **28 panels
and 62.7 m of roadway deleted while the centreline was dry land a visitor can stand on** — twice
what was first written down here. Quote the measured figure, not the table. The wet-centre drops are defensible in principle
(a road genuinely crossing the river) but should be checked against the bridge records rather than
assumed — 34 quads on Lake is 79 m, and it is worth knowing whether that is one crossing or a
mask that is too generous.

**Files:** `renderers/web/js/streets.js` (clip, do not drop) · `tools/smoke_renderer.mjs` (a check
that no street loses a quad whose centreline is dry)
**Acceptance:** the edge-only deletions go to **zero**; the wet-centre deletions are unchanged or
justified per street; the South Water hole is gone in a shot at the owner's pose; no road paints
over water — prove it, do not assert it.

### B-A1 — does the AO bake earn its nightly? · **UNCLAIMED · NEXT UP (lane 1 or standalone)**

Opened 2026-08-14 after nine bake PRs (#107, #110, #111, #113, #114, #116, #117, #118, #120)
were closed unmerged in a batch. **B-BUG3 stopped them accumulating; this parcel asks whether
they should be produced at all.**

**What closing them revealed.** Every GLB in the newest PR was **modified, none added** — 57
modified, 0 new — against a `dev` that already carried all 270, including the nine
`randolph_dearborn` roofs from that morning's block. A block parcel lands complete: the infill
generators emit placeholder geometry deterministically without Blender
(`generators/inferred_placeholder.py`, gated by `check.sh`), so the nightly is **re-baking what
already exists rather than supplying anything missing**. And a re-bake rewrites bytes even when
nothing changed, because `tools/bake.sh` says so on its own face: determinism is defined on
INPUTS, "because Cycles AO is not bit-reproducible across hardware".

So a bake PR is, byte for byte, mostly churn — and it goes stale within hours. #120 would have
**deleted eleven lines from the published changelog** and rewritten `walk/index.html`, because
it branched five commits back and re-published a mirror that predated the work since, including
the R-BUG2 fix.

**The question, and it is answerable rather than a matter of taste:** what does the AO bake
visibly buy over the placeholder geometry? `R-G0` merged that morning precisely so "did this
change how it looks" stops being an adjective. Use it.

**Method.** Take one block that has both forms available, shoot it through
`tools/critic_shots.mjs --metrics` as placeholder-only and as baked, and quote the two tables.
Then say which of these the evidence supports:

- **It earns the nightly** — the difference is visible at the anchors a visitor is offered.
  Keep the cadence; the fix is that the bake should close its own superseded PRs when it opens
  a new one, so exactly one is open and it is always current.
- **It earns a cadence, but not a nightly** — visible but slow-moving. Move to weekly or to
  dispatch, and say what the trigger should be.
- **It does not earn either** — the placeholders are what ships and the bake is refining
  something nobody sees at the distances the app is walked at. Then the honest outcome is to
  stop running it on a schedule, keep it on dispatch for when geometry genuinely changes, and
  record that in `docs/RENDERING.md`.

**Do not answer this by preference.** Nine PRs a day of runner time is a real cost and so is
throwing away a refinement that matters; the tables decide it.

**Files:** `docs/RENDERING.md` · `.github/workflows/chicago-4d-bake.yml` (cadence and/or the
supersede step) · `docs/ROADMAP.md`. Measurement only — no data record changes.

**Note:** the bake PRs' gate runs also sit in `action_required` (GitHub holding
bot-branch workflows for manual approval), so they could never have gone green unattended
anyway. If the outcome keeps PRs in the picture, that needs solving too, or every bake PR
arrives permanently ungated.

### R-BUG2 — the town's roads vanish in places, and from the air · **DONE 2026-08-14 · two faults, and the third suspect refuted**

**Shipped:** the gate first, then the fix, in that order and for that reason.

**The gate — `roadContrast()` in `tools/smoke_renderer.mjs`.** Three frames of one held scene at
each of two anchors, at both viewports: the real render **R**, the same geometry as an opaque
marker with a deliberately DEEPER polygon offset **M**, and the scene with the street group
hidden **O**. **M is the denominator and it is what makes this work** — a probe counts only where
the marker reached the screen, so a road behind a building, a tree or a rise drops out of the
sample instead of being scored as a fault, while a road that loses the depth fight to the terrain
stays in it and shows up as a road that covers a pixel and does not change it. The number is
`|L*(R) − L*(O)|` at each surviving probe, on `critic_metrics.mjs`'s own `labL` — the same scale
the critic harness measures reference photographs with. Bars: median **ΔL\* ≥ 1.8** and **≥ 55 %**
of probes at ΔL\* ≥ 2, per distance band, bands needing ≥ 8 probes, gated to ≤ 600 m and reported
beyond.

**What it measured with the fault in — both bars failed, which is the acceptance:**

| station | band | median ΔL\* | perceptible |
|---|---|---|---|
| `south_water` (eye) | 250–600 m | **0.3** | **14 %** |
| `from_above` (aerial) | 100–250 m | **1.1** | **0 %** |

**And with the fix in, desktop:**

| station | 40–100 m | 100–250 m | 250–600 m | 600 m+ (ungated) |
|---|---|---|---|---|
| `south_water` | 4.2 / 70 % | 3.9 / 89 % | 4.0 / 92 % | — |
| `from_above` | — | 2.9 / 91 % | 2.4 / 63 % | 3.3 / 100 % |

**FAULT 1 — the depth fight, and it is the "in places".** `polygonOffsetFactor: -1,
polygonOffsetUnits: -1` against a coplanar terrain is a fraction of a depth unit, and depth
precision degrades with distance, so past ~250 m the terrain won in patches. Deepening the offset
to **−4 / −8** ALONE took `south_water` 250–600 m from 0.3 / 14 % to **3.3 / 71 %**. No vertex
moved and `worstDrape` still gates at 1e-5 m.

**FAULT 2 — the road was 4 % opaque, and it is the "from the air".** At the aerial anchor the
ribbon is wide, unoccluded and wins depth, and it STILL scored 1.1 / 0 %: neither the offset nor
the thin-ribbon rule moved that band at all. The cause was the authored alpha — a lightly worn
track was `0.08 + ruts*0.54 − crown*0.04`, so 8 % earth over 92 % prairie away from the ruts and
4 % at the crown. Baselines raised to **0.54 / 0.38 / 0.28** (graded / worn / light), modulation
shape and class ordering untouched. Recorded as **L96** in `docs/LIBERTIES.md` as an amendment to
L79, which already recorded these numbers as invention.

**REFUTED — mip-averaged alpha falling under `alphaTest`, the parcel's own prime suspect.** It is
the right shape and it is the v74 treeline family, and it is not what is happening: turning
mipmaps OFF made every band WORSE (`south_water` 250–600 m, share of probes reaching the screen:
**22 % with mips, 6 % without**). The mip chain is holding a sub-pixel ribbon together, not
erasing it. `minFilter` is unchanged. **Measure before choosing was the right instruction and it
saved a fix that would have made this worse.**

**Also shipped, and it is not what fixed either fault:** a sub-pixel floor in the street shader.
`u` runs 0→1 exactly across the track, so `1/fwidth(vMapUv.x)` IS the ribbon's width in screen
pixels — no uniform, no viewport to keep in sync. Under 2 px the alpha scales up in proportion,
capped at 6× and 0.92. Same principle as `MIN_SILHOUETTE_PX` in `trees.js`. It binds only at the
thin end, which is why it did nothing from the air.

**Third suspect, NOT acted on.** `transparent: true` with `alphaTest` does put a town-wide mesh in
the back-to-front pass sorted on a meaningless bounding-sphere centre. Moving it to the opaque
queue measured as a small, consistent improvement — and it makes every road SOLID, because an
unblended alpha-tested fragment draws at full strength. That would delete the graded/worn/light
distinction the dataset carries. Left as it is, deliberately; if the sort ever bites, the fix is a
per-record renderOrder, not opacity.

**One thing the gate had to learn about itself:** `from_above` is an aerial anchor, and leaving
the camera there broke the horizon-timber check further down the file, which reads the band the
tree solver builds around the camera and found nought of nought covered bearings. A measurement
that moves the camera owes the next one its pose back. It does now.

Reported by the owner 2026-08-14: *"the town roads seem to disappear in places and when you
fly over them you lose them, they should be on the surface and be seen."*

**The gate cannot see this, and that is the first thing to fix.** `tools/smoke_renderer.mjs`
asserts the streets are *populated and draped* — record count, vertex count, drape error,
no wet vertices — and every one of those passes while the roads are invisible. Draped is not
seen. There is no assertion anywhere that a road reaches the screen.

**Three candidate mechanisms, all in `renderers/web/js/streets.js`, and they compound.
Measure before choosing — do not fix all three blind.**

**1. Mip-averaged alpha falling under `alphaTest`. The most likely, and this project has
already been bitten by it once.** The road texture's alpha is built as
`255 * edge * body`, where `edge` ramps to zero across the outer 12 % of the width and `body`
for an unimproved track is `0.08 + ruts*0.54 - crown*0.04` — so away from the wheel ruts the
alpha is about **20/255**. With `minFilter: LinearMipmapLinearFilter`, climbing away averages
that thin, low-alpha ribbon against its own transparent edges; once the averaged alpha drops
under `alphaTest: 0.025` the fragments are **discarded outright**. That is the same failure
family as changelog **v74** — *"The distant treeline had holes in it that were not sky"*, where
crown modulation cut a one-pixel silhouette out of existence. The fix pattern that worked there
is the one to reach for: never let a modulation take a feature below one pixel of the viewer's
own screen. `trees.js` carries the precedent.

**2. Insufficient polygon offset at altitude.** The material sets
`polygonOffsetFactor: -1, polygonOffsetUnits: -1` against a coplanar terrain. One unit is
tiny, and depth-buffer resolution degrades sharply with distance, so from the air the terrain
can win the depth test in patches — which is exactly the reported *"in places"*, rather than a
clean all-or-nothing fade. Note the mesh is `depthWrite: false` but still depth-**tests**.

**3. The transparent queue is sorting a town-wide mesh by one centre point.**
`transparent: true` puts the streets in the back-to-front pass, where a merged
mesh-per-surface sorts on its bounding-sphere centre — a meaningless point for a road network
spanning the whole town. `alphaTest` with `transparent: true` is a smell in itself: an
alpha-tested surface usually belongs in the opaque queue, writing depth, where the sort is
per-fragment and free.

**Files:** `renderers/web/js/streets.js` · `tools/smoke_renderer.mjs`

**Acceptance:** a new gate that would FAIL today — sample the rendered frame along known street
centrelines from the walker's eye AND from the aerial anchor, at both viewports, and assert the
road is distinguishable from the ground beside it. Quote the measured numbers, and put the
fault back to prove the check names it. RENDERING §5's method applies: measure, do not assert an
adjective. The roads must read *on the surface* — this is not licence to lift them off the
terrain, which would break the drape assertion that already passes and is correct.

**Runner:** lane 1. It touches no data and no generator, so it may run beside any town parcel.

### T-BUG2 — 79 ground vertices face downward · **DONE 2026-08-23 (T-0014) — the classifier had no threshold in it**

**Closed by `generators/terrain_gen.py` § `_face_the_sky()`, and the count is 0.** The
defect decomposed exactly on the shipped master, with nothing left over: **33 triangles
wound backwards** (plan area −3.125 to −25.0 m², ordinary full-size ground faces whose
winding the n-gon triangulation reversed) and **197 standing edge-on** (plan area exactly
0.0 — slivers in a plane of constant E, constant N, or three points collinear in plan;
the necks of keyholes the planar dissolve leaves in its n-gons, and the source of the
mesh's 15 one-triangle vertices). The generator now re-winds the first set and deletes
the second, then refuses to export if either survives.

**What makes it a repair and not a mask: the classifier is the invariant, and it has no
tuned number in it.** Both surfaces this module emits are single-valued functions of
(E, N), so seen from above every triangle must cover positive plan area and wind
counter-clockwise. The 2.5 m lattice quantises plan area to multiples of half a cell, so
the histogram has a clean gap either side of nothing: 197 faces at exactly 0.0 m², then
the smallest honest triangle at 3.125 m². No third population, no judgement call.
Deleting an edge-on face cannot open a hole for the same reason it is deleted — it covers
no plan area — and `mesh_vs_field()` says so out loud: **0 misses of 28,890 rays, max
6 mm, before and after.**

**The obvious fix was tried first and is worse.** `ngon_method="CLIP"` (ear clipping,
robust on concave n-gons where BEAUTY is not) gives **42** backwards faces instead of 33
and **9,483** sub-mm² slivers instead of 188, measured on this same mesh. The
triangulation Blender picks is not the thing to argue with.

Master: 249,826 → 249,629 triangles, 125,180 → 125,174 vertices, −2,532 bytes; the six
lost vertices are keyhole tips and every surviving vertex keeps its `_CONFIDENCE` value
to the bit. Worst shipped ground normal now points **0.737** up, against a gate at 0.1.
`tools/smoke_renderer.mjs` assertion (b) is `=== 0` and must stay there.

---

**The original box, as it stood:**

Found 2026-08-14 while gating the black-wedge fix. **79 of the terrain's 742,581 vertices
(0.011 %) come out of the generator with normals facing DOWN** — scattered isolated points
inside the town at ordinary elevations (e 90 n −310, e 213 n −135, e 228 n 133), not a
contiguous patch and not at the box edge, which is why they produce no visible artefact.

Distinct from the wedge that prompted the search: that was 33 of ONE tile's 99 vertices — a
third of it — caused by `gltf-transform optimize` simplifying the ground, and it is fixed.
These 79 are in the master and predate it. Most likely degenerate triangles or a
normal-averaging artefact in the decimator.

**Pinned, not ignored.** `tools/smoke_renderer.mjs` asserts the count cannot exceed 79, so
the number can only go down. Fixing this lowers the constant in the same PR.

**Files:** `generators/terrain_gen.py` · a terrain rebake (nightly bake lane) ·
`tools/smoke_renderer.mjs` (lower the constant)

**Runner:** the no-Blender half is diagnosis — find the 79 in the generator's own output and
say what makes them. The rebake arrives via `chicago-4d-bake.yml`.

### R-BUG1 — the river edge flickers when flying · **DONE 2026-08-16 — it was the NEAR PLANE, and the fix moves no edge**

**Read this box before biasing any surface to settle a depth tie.** The owner's flickering bank
line is the depth buffer running out of numbers at range, and the cause is a camera setting
rather than anything about the water: `main.js` carried a **fixed 0.1 m near plane** with a
3,000 m far plane. A perspective depth buffer resolves about `z² / (near · 2^bits)` at distance
`z`, so at the 0.1 m near, two surfaces **350 m away had to be ~10 cm apart in depth** before the
buffer could order them — and the waterline is the one place in this scene where two surfaces are
**co-planar by design** (`terrain.js`: the bank line IS where the ground crosses `y = 0`). Inside
that band the winner is decided by rounding, and any camera movement re-rolls it.

**The instrument, and it is the part worth carrying forward: MOVE THE CAMERA TWO MILLIMETRES.**
`tools/measure_river_edge.mjs` stands at three aerial poses along the owner's own reproduction,
photographs each, nudges the camera 2 mm — about a five-hundredth of a pixel at these ranges, so
no edge can honestly move — and photographs it again. The clock is held, the HUD is hidden, and
**the same pose photographed twice with no nudge differs by 0 pixels at every station**, which is
the control that makes the rest of it mean anything. A pixel that changes under the nudge changed
because a depth tie resolved the other way. Flicker is motion, and this is how a still frame
answers a question about motion.

| station | altitude | bank line, px | **bank flicker, before** | **after** |
|---|---|---|---|---|
| `from_above` (the scene anchor) | 175 m | 21,457 | 672 · **3.1 %** | 583 · **2.7 %** |
| `descend_main_stem` | 90 m | 16,994 | 2,648 · **15.6 %** | 560 · **3.3 %** |
| `over_the_forks` | 45 m | 19,794 | 1,469 · **7.4 %** | 471 · **2.4 %** |

Measured on the PUBLISHED mirror at 1280×800. The gate is `--gate`, at **5 % of the bank line**:
red at two of the three stations before, green at all three after with 1.7 points to spare. It is
a SHARE and not a count on purpose — a count is a number about the pose.

**The fix is precision, not a tie-break, and that distinction is the parcel's argument.** The near
plane now opens with altitude (`NEAR` in `main.js`: a twenty-fifth of the eye's height above the
ground, quantised, clamped to 0.1–8 m). On foot `altitude` is 0, so **a walker's camera is the
camera they had before, to the digit**. The obvious alternative — a `polygonOffset` on the water
material — was rejected on the acceptance this box was written with: it settles the tie by biasing
the water toward the camera, and at 350 m one depth step is ~10 cm of ground, so the drawn
waterline would climb the bank by up to that much. **That breaks the invariant the design exists
to guarantee.** Precision costs nothing and moves no edge; a bias buys the same picture by
lying about where the river is.

**Finding — MOST OF WHAT FLICKERS IS NOT THE BANK, and it is now R-BUG6.** The whole-frame count
under the same nudge is 1,690 / 5,901 / 3,886 px before and 1,568 / 1,883 / 1,173 after: the
continuous magenta line along the bank in the before-mask is gone, and what is left is **speckle
on roofs, walls and canopies** at every station. That is a second population with a different
cause, and this parcel did not chase it. The residual 2.4–3.3 % at the bank is the same speckle
falling within two pixels of a waterline, which is why the gate is not tighter.

**And the suspect for it is UNTESTED rather than refuted, because the instrument was inert.**
`--no-sun-shadow` was written to test the obvious candidate — the shadow camera follows the
walker, so a moved camera re-rasterises the shadow map onto a shifted texel grid. It reported the
numbers **unchanged to the pixel**, which read as a refutation. It is not: the flag's own control
(put the shadow back, photograph again) changes **0 pixels**, so dropping `castShadow` after boot
never reaches the render at all. The flag now **exits 2** on that control rather than printing a
finding. *A diagnostic that changes nothing reports "not the cause" for the same reason a broken
thermometer reports a steady temperature* — the sixth time on this project that a green reading
came from an instrument pointed at nothing.

**Files:** `renderers/web/js/main.js` (the `NEAR` block, `setNearFor`, `stats().cameraNear`) ·
`tools/measure_river_edge.mjs` (new) · `tools/smoke_renderer.mjs` (two structural assertions on
the near plane; the pixel gate stays in the tool, at three frames a station).

**Not claimed:** the desktop half of the smoke — ~13 min against this runner's 10-minute
per-command ceiling. The measurement itself was run at 1280×800, which is the harder viewport for
this defect: more pixels of bank line to disagree about.

### R-BUG7 — flower heads hang in the sky with nothing under them · **DONE 2026-08-17 · SEEN · OWNER-REPORTED 2026-08-16**

**THE OWNER'S REPORT, and it is the fifth time this symptom has been fixed.** Standing on South
Water Street on the `/dev/` preview at **bearing NNE 025°**, looking north across the main stem: two
yellow flower heads float **above the horizon line**, each on a short stalk that **stops in mid-air**
and reaches no plant. His words: *"yellow floating objects, I guess they are supposed to be flowers
but it does not connect."* Both sit well above eye level with clear sky beneath them; the near one is
the larger, so they are at different depths and this is not one stray instance.

**FOUR PRIOR REPAIRS ARE WRITTEN INTO `renderers/web/js/flora.js` FOR THIS EXACT SYMPTOM, AND THE
SYMPTOM IS IN PRODUCTION.** Read them before touching anything — each closed a real mechanism and
none of them closed this:

| where | what it fixed | its own words |
|---|---|---|
| ~line 666 | head and plant drew heights from independent draws of one range | *"the pair of flower heads the critic found floating unattached in the open sky"* |
| ~line 2398 | every head archetype gained a **peduncle** below it | *"a flower that ends where its stalk should begin is the floating sprite the critic caught in the sky"* |
| ~line 2409 | `PEDUNCLE` bounds how far a branched head may sit off the stem | *"lollipops hanging in the air beside the scape"* |
| ~line 2532 | `rayGeometry` went from 9 rays to 14 so a disc is not a spider | *"at nine centimetres on a prairie-dock scape it was **a yellow star in the sky**"* |

**THE FINDING IS ALREADY AVAILABLE AND IT IS R-BUG5b's: four fixes to the DRAWING, and not one gate
that reads the drawing back.** `tools/smoke_renderer.mjs` has no assertion anywhere that a drawn
flower head has plant geometry beneath it. The two things that sound like it are not it — the
`floating` check near line 2057 is about **buildings** hovering over their ground, and
`floatingDry/floatingWet` near line 2846 asks whether a water-lily *record* is **placed** on dry
land, which is a placement test of exactly the kind R-BUG5b proved cannot see a drawing fault. **So
this symptom has been repaired four times by eye and asserted zero times.**

**TWO SUSPECTS ARE ALREADY REFUTED — do not spend the run on them again.**

1. **It is NOT R-BUG5b's sign fault.** `flora.js`'s `push()` (~line 1968) takes ENU `n2` and does
   `_m.setPosition(e, y, -n2)` **itself**, so every caller — heads included — is negated once and
   only once. `maybeHead` passing `n + Math.cos(a) * r` is correct.
2. **It is NOT a head surviving a dropped stem.** `placeForb` and `placeGraminoid` both end
   `return set.push(...) ? h : 0`, and both call sites guard `if (h > 0)` before calling
   `maybeHead`. The comment beside it already states the rule: *"a zero says the cap was reached and
   nothing was drawn here, so nothing may be hung off it either."*

**THE LIVE SUSPECTS, in the order worth testing.**

1. **THE RING FADE LOWERS THE HEAD AND THE PLANT SEPARATELY.** `maybeHead` passes `rise` to the
   shader as well as adding it to `y`, and the reason is written down: *"the shader has to bring the
   head DOWN with the plant as the ring fades it: a head left at the height the CPU put it would
   hang in the air over a shrinking stem."* The head and the plant are in **different instanced
   sets with different ring parameters** (`near.head` / `ringAt(f.head, …)` against the plant's own
   `f.fade`), and the only thing tying them together is a radius comparison at the call site
   (`r <= f.head[0] + off + step`). **A radius comparison is not the same statement as "the stem
   under this head is at full height".** If the plant's fade reaches zero before the head's does,
   the documented failure mode is exactly the owner's photograph.
2. **The ground the head is hung off may not be the ground the stem stands on.** `y = station(e, n,
   zone, sp, wet)` is sampled once and used for both, but the shot is taken **across water**, and
   the emergent/wet path is the least-travelled one in that function.
3. **Scale.** A head is sized from the record's `inflorescence.size_m` through a nominal unit box;
   a record with a bad `size_m` gives a head far too large for its plant, which reads as floating
   even when it is attached. Cheap to rule in or out — print the drawn head size against its
   plant's height and look at the tail.

**THE ACCEPTANCE, and it is not negotiable, because four eyeball fixes is enough.** The repair ships
with a gate that **reads the merged head geometry back and requires plant geometry beneath every
head** — the same shape as R-BUG5b's *every tree drawn stands at its own station*, which is the one
gate that could not have passed through that bug. Concretely: for every drawn flower-head instance,
some plant instance of the same species within its own spread, whose drawn top reaches the head's
stalk. **Demonstrate it RED on today's build before the fix goes in.** A gate on the placement is
the gate that has been green through all four repairs.

**Reproduce first, diagnose second** — R-BUG5b's rule, and the one #196 skipped. The pose is on
South Water Street at NNE 025°; `tools/shoot.mjs` puts the camera there. **The first commit of this
parcel should be a screenshot.**

**THE ANSWER, 2026-08-17: THE BEARING WAS RIGHT AND THE MATRIX TURNED IT.** `maybeHead` computes
`tiltAz` so the stalk leans back to the stem, and then passes a **random `yaw`** into the same
`push` call. `push` builds the instance rotation as an Euler in **`YXZ` order**, so that yaw is a
`Ry` applied OUTSIDE the tilt: it spins the whole leaning head, and the azimuth with it, to a
uniformly random bearing. **`push`'s own docstring says *"Pass `yaw` 0 alongside a tilt — the matrix
carries the whole rotation"*, and the caller does not** — and the yaw is not even needed there,
because the vertex program already spins the head about its own axis off `aFlora.w`. It was applied
twice, and the second application was the bug. That is why four repairs to the DRAWING each closed a
real mechanism and none of them closed this: **every one of them computed a number that a later line
threw away.** The live suspects in the box above were all wrong — the ring fade is monotone (head
fade is provably ≤ plant fade at every distance), and the fault reproduces down a dry street.

**THE RED, LANDED FIRST, ON THE UNMODIFIED `dev` BUILD.** `tools/measure_head_support.mjs` reads the
instance buffers back — every head set and every rooted set — reproduces the vertex program's ring
fade and head descent in JS, and asks whether the foot of each drawn head's stalk lands inside a
drawn plant's body, under its drawn top. Published mirror, desktop, all eight scene anchors at four
bearings:

| | before | after |
|---|---|---|
| drawn heads with nothing under them | **38 of 11,752** | **0 of 11,735** |
| poses carrying a fault | **8 of 32** | 0 |
| stalk foot → nearest stem, median | **21 mm** | **0** |
| ...p99 / worst | **234 mm / 582 mm** | **0 / 0** |
| by shape | **38 of 1,407 `corymb`**, 0 of the other eight | — |

**It is all `corymb`, and that is the arithmetic rather than a coincidence:** `corymb_flat` is the
one architecture with both a large tilt band (0.44–0.74 rad) and up to twenty heads per plant, and
the head's offset is capped at `reach × size × sin(lean)` — 0.53 m on a 24 cm umbel. A random
bearing on that cap is a half-metre miss. Every other shape is small enough, or upright enough, that
the miss stays inside the plant it came from.

**THE REPAIR IS NOT A FIFTH AIM, and that is deliberate.** The head archetypes are now built with
their origin at the **foot of their own stalk** (`peduncle` lifts the whole archetype by its own
drop, and it is the last call in all nine builders). The instance is then pushed **on the stem**, at
the height the branch leaves it, and the tilt rotates the head out about that point — so the offset
from the stem is *generated by* the stalk instead of being a second number that has to agree with
it. Three things follow, and the third is the one that matters:

1. `r`, `spread` and the `0.94` fudge are gone from `maybeHead`. There is nothing left to disagree.
2. `chiFade` scales the head about its foot, so a head slides DOWN its own stalk as its plant
   shrinks. Before, the lateral offset was baked into the translation and did not shrink at all —
   a second, quieter detachment that the first cut of the repair left behind at 1 of 11,735.
3. `foot = min(plantH, rise − reach·size·cos(lean))`, and the shader scales both the foot's rise and
   the plant's height by the same ramp, so **`foot × fade ≤ height × fade` at every fade**. The gate
   is an invariant that holds by construction, not a number measured at the pose someone chose.

**THE GATE.** `tools/smoke_renderer.mjs` carries it at both viewports — *every drawn flower head has
a plant under its own stalk* — over the same eight anchors at four bearings. It takes the stalk foot
from **the archetype's own lowest vertex** rather than from a constant, which is why the before and
after numbers above are comparable across a repair that moved the anchor: the same measurement reads
`minY = −PEDUNCLE[kind]` on the old build and `minY = 0` on the new one and reports the same point.
A mid clump card is excluded from the plants that may support a head — no head is hung from one, and
counting them is exactly how the first cut of this measurement read **0 unsupported** on a build the
committed evidence frame shows to be broken.

**THE LESSON, and it is for every set in this file, not for flowers.** A per-instance rotation that
is composed from two sources — one the caller computed and one it passed along out of habit — has no
error mode that looks like an error. It renders. It renders plausibly. **Four separate agents fixed
this symptom by eye and the geometry never once did what any of their comments say it does.** Before
adding a rotation term to an instanced set, ask what else is already rotating it.

**Before and after** at `docs/evidence/r-bug7-{before,after}.png` — the same white umbel by the
storefronts on South Water Street at bearing 090°, published mirror, desktop 1280×800, cropped from
the frame `docs/evidence/t-v2-after.png` recorded the fault in.

**A SECOND INSTANCE IS ALREADY COMMITTED, AT A DIFFERENT STATION, IN AN IMAGE SHOT FOR ANOTHER
PARCEL.** `docs/evidence/t-v2-after.png` — the on-street South Water view, **bearing 090°, desktop
1280×800**, taken to show T-V2's anchor move — carries a **pale flower head at roof height at the
right-hand edge of the frame**, beside the storefront row, with clear sky behind it. Different
bearing, different viewport, different day, same symptom. Two things follow:

1. **The repro is cheap and does not need the owner's exact pose.** Two of the three committed
   South Water frames show it. Start with the ones already in the tree.
2. **It is not confined to looking across water**, which weakens live suspect 2 (`station()` on the
   emergent path over the river) before anyone spends a run on it — this frame looks *down a dry
   street* with the river off to the left. Suspect 1, the ring fade, survives that; check it first.

### T-0035 — the flowers grow up out of the ground as you approach · **DONE 2026-08-18 · OWNER-REPORTED 2026-08-17**

**THE OWNER'S REPORT:** *"the flowers still seem like they grow out of the ground as you approach
them, they do not fade in as you walk towards, they grow up."* **"Still" is the whole finding** —
this is his SECOND report on the same ring, and the first one was answered without answering it.

**WHAT THE FIRST ANSWER DID.** His 2026-08-14 report — *"grass and flowers appear out of the ground
as you walk towards them"* — was diagnosed as a RATE problem and it really was one: the ramp was
baked into the height on the CPU and could only change when the lattice was rebuilt, so a plant
arrived at 55 % of its height between one frame and the next. The repair moved the ramp into the
vertex program (continuous, per frame) and inset the fade ring inside its own lattice by the rebuild
step, so nothing is ever drawn before it is placed. The `popIn` gate in the smoke holds both halves
and is still green — measured on this branch, **53 arrivals over a 3 m walk, worst arrival 0.0 % of
the ramp**, which is the inset doing exactly what it was built for.

**AND IT LEFT THE RAMP DRIVING SCALE.** `transformed *= chiFade` — the whole plant, uniformly, about
its own base, with a matching world-space descent (`chiDrop = aChiRise * (1 - chiFade)`) that slid a
flower head down its own stalk so it stayed on the shrinking stem. **A plant that goes from nothing
to full size about its base is growing, however finely you subdivide the growth.** The first repair
made the growth SMOOTH, which is not what he asked for either time.

**THE FIX: THE RAMP IS COVERAGE, NOT HEIGHT.** `flora.js` § `plantMaterial` hands `chiFade` to the
fragment shader as a varying and resolves it with the ordered 4×4 Bayer screen-door dither this
project already uses to draw an unevidenced wall (`confidence.js`) — chosen over real translucency
because a sward is eight thousand double-sided instances that would have to be depth-sorted every
frame, and over a per-instance stochastic cut because that is a pop, which is the defect the ring
was built to remove. Three consequences:

* **Height is 0 or 1 and nothing between** (`heightOf`). A drawn plant is drawn at the height its
  record gives it, at every distance it is drawn at at all.
* **The head descent is gone with the scale it chased.** R-BUG7's invariant survives intact and gets
  simpler: `maybeHead`'s clamp gives `foot <= plantH`, and nothing scales either side of it now.
* **Contouring is broken by a per-instance phase.** Sixteen dither levels against a ramp in DISTANCE
  would be sixteen concentric rings about the walker — § S6a item 3's "constant world radius is a
  constant screen row" all over again — so each plant offsets its threshold by a hash of its own
  world position. `fract(bayer + phase)` is still uniform on [0,1), so coverage is unchanged.

**THE GATE, and it is a new one rather than a re-run.** The smoke's popIn walk now also reads the
drawn HEIGHT of every plant over the same twenty paces: *a plant is drawn at its own height, faint,
never short* — no plant that is drawn at all is drawn short, and nothing already on screen gains
height between two frames a pace apart. **Measured: shortest drawn plant 100.0 % of its own height,
worst gain 0.0 % per 0.15 m pace. The same reading of the OLD height term over the same walk is
0.02 %** — a plant drawn at a five-thousandth of its height, which is what growing out of the ground
looks like written down.

It is deliberately not asked of ARRIVALS alone. The inset means a plant arrives at coverage zero, so
an arrival-only reading asks the question of a plant that is not yet drawn and passes on anything;
the gate reads every drawn plant in every frame of the walk. `tools/measure_head_support.mjs` and
the smoke's R-BUG7 gate lose their `* fade` terms in the same commit, because both reproduce the
vertex program and a mirror that drifts stops reading the drawing.

**COST.** Draw calls 41 and 611,823 triangles, unchanged: the instances were always in the buffer,
the ramp only ever changed their size. What the band pays instead is fill — plants inside it are
rasterised whole rather than shrunken — and what it saves is the annulus outside the fade ring,
which now collapses to a point instead of rasterising a full-size plant to discard every fragment.


### R-BUG6(a) — the shadow grid slid under every step, and the control that cleared it was inert · **DONE 2026-08-17 · SEEN in motion · opened 2026-08-16 by R-BUG1**

**Phase:** lane 1, renderer only · **Runner:** improve-runner · **Files:**
`renderers/web/js/world.js` (`centreFor`, `follow`, `setShadowSnap`, `shadowRig.snapped`) ·
`tools/measure_river_edge.mjs` (the repaired control, `--box-drift`, `--snap-off`,
`RIVER_NUDGE_M`) · `tools/smoke_renderer.mjs` (three assertions) · `site/chicago/4d/**`.

**THE SHIPPED FIX: the shadow box moves in whole texels.** It follows the visitor, and it was
re-centred on their exact position every frame — so the map's sample lattice slid a fraction of a
texel with every step and re-quantised every shadow edge in the scene while nothing in the world
moved. The centre is now rounded onto a world-anchored lattice of the box's own texel size, in the
light's own plane. **Measured with the camera held perfectly still and the box slid half a texel
(58.6 mm): `from_above` 2,023 changed pixels → 0, `descend_main_stem` 5,650 → 0.**

The correction is at most half a texel — 5.9 cm desktop, 11.7 cm phone — and it is **only ever
across the map, never along the sun**, so the reach, the map size, the 11.7 cm texel and the `bias`
/ `normalBias` calibrated to it are all untouched.

**FINDING 1 — THE CONTROL THAT "CLEARED THE SHADOW MAP" COULD NOT HAVE CLEARED ANYTHING, AND NOW
IT MOVES 5,439 PIXELS.** `--no-sun-shadow` dropped `sun.castShadow` after boot and changed 0
pixels of the frame, which this box read as "the flag never reached the render". The mechanism is
compilation: `castShadow` is read when a material's program is built, so flipping it later leaves
every shader still sampling `directionalShadowMap[0]` — and the map itself is still hanging in the
texture unit from the last frame that had one. The repaired handle switches `renderer.shadowMap`
off **and marks every material `needsUpdate`**, which rebuilds each program against the new
`NUM_DIR_LIGHT_SHADOWS`. **The generalisation: a renderer flag read at compile time is not a
runtime handle, and a diagnostic that flips one is measuring the scene it meant to exclude.**

**FINDING 2 — THE ANSWER TO THIS PARCEL'S TITLE, AND IT IS MOSTLY NOT THE SUN.** With the repaired
control, the whole-frame flicker under the 2 mm nudge on `dev` falls from **1,284 → 1,108** at
`from_above` and **2,383 → 2,008** at `descend_main_stem` when the shadow map is taken out
entirely: **the shadow map carries 14–16 % of it.** The snap banks about half of that (1,284 →
1,184 and 2,383 → 2,195, and the gated bank share 2.9 % → 2.6 % and 3.4 % → 3.1 %); the other
~84 % is **NOT** co-planar depth ties — R-BUG6(b) refuted that on 2026-08-17 with the depth-function
switch (13 of 1,108) and 5× the near plane (604 of 607 survive); it is the town's own edges being
resampled. The sentence below stood for one day and is kept because the box it sits in is quoted.
Do not quote
the shadow map as the cause of the town's flicker.

**FINDING 3 — THE NUDGE INSTRUMENT CANNOT MEASURE THE SHADOW BOX, AND THE ATTEMPT IS ON THE
RECORD.** 2 mm slides the lattice by 1.7 % of a texel, so the nudge sees 1.7 % of a defect a
walking visitor meets twelve texels of per second. Nudging by a half texel instead to scale it up
**fails**: at `from_above` a 58.6 mm nudge changes **29,138** pixels with the snap on and **28,784**
with it off — the camera move resamples the whole frame and swamps the box, sign included. **A
sub-pixel nudge is an instrument for depth ties only.** The right instrument moves the BOX and not
the camera, which is what `--box-drift` does: it freezes `follow`, places the box twice half a
texel apart, and photographs one identical pose. That is where the 2,023 → 0 above comes from.

**FINDING 4 — THE INSTRUMENT COULD NOT RUN ON THIS RUNNER AT ALL, AND THE REASON IS A WAIT.**
Every capture in `measure_river_edge.mjs` timed out: `elementHandle.screenshot()` waits for the
element to be *stable* — two consecutive animation frames with an unchanged box — and one frame of
this scene under SwiftShader takes about ten seconds, so two do not fit Playwright's 30 s action
timeout. Measured: element capture fails at 12 s where `page.screenshot()` returns in 10.2 s from
the same page. The tool photographs the page now, with an assertion that the canvas fills the
viewport so the substitution is proven rather than assumed. **A stability wait is the wrong wait in
a harness that holds the clock on purpose.**

**The gate.** Three assertions, and the middle one is R-A1's: the box holds still across a
sub-texel step (**2.4 × 10⁻¹⁵ m** across the map, float noise); with `setShadowSnap(false)` the
same millimetre moves it **0.994 mm**, so the snap reaches the box rather than being asserted into
existence; and a 1 m walk moves it **5 times at the phone's 23.4 cm texel and 11 at the desktop's
11.7 cm, every jump exactly 1.000 texel**, which is the lattice pitch measured from outside. **The first version of that first assertion demanded the box
hold still ABSOLUTELY and failed a correct rig at 0.107 mm** — the centre keeps the walker's
component along the sun, where an orthographic camera rasterises every world point to the same
texel and the written and compared depths shift together. The invariant is *across the map*, and
`world.direction` is what the assertion projects onto.

**Verification.** `tools/check.sh` **CHECK PASS**. `SMOKE_VIEWPORT=mobile` on the published
mirror: **253 passed, 2 failed** — the same two road assertions `dev` already carries
(R-BUG5b/#201 and T-V2/#135), and the +3 is exactly this parcel's three gates. The desktop half
does not fit the runner's ten-minute per-command ceiling (ROADMAP § THE RUN BUDGET) and did not
run; every figure above is `measure_river_edge.mjs` at 1280×800 on the published mirror.

### R-BUG6(b) — the other 84 % is NOT co-planar ties · **DONE 2026-08-17 — the premise is refuted by the two tests that can settle it, and the residual is the town's own edges**

**Phase:** lane 1, renderer only, no bake · **Runner:** improve-runner · **Files:**
`tools/measure_tie_class.mjs` (new) · `docs/ROADMAP.md` · `docs/STATUS.md` ·
`renderers/web/js/changelog.js` · `site/chicago/4d/**`. **No renderer file was changed, because
nothing was found to change.**

**THE ANSWER: 13 pixels of 1,108.** Three boxes of this file — R-BUG1's successor note,
R-BUG6(a) finding 2 and the row in NEXT UP — said the residual flicker was "co-planar depth
ties", by analogy with R-W5a2's batch merge. It is not. Two independent tests say so, and
neither had been run:

| test | what it can see | result |
|---|---|---|
| **the depth function** — `LessEqual` → `Less`, all 11 materials | changes a pixel **only** where two surfaces have exactly the same depth. It is the definition of co-planar, asked of the renderer | **36,187 px of the frame move — and only 13 of them are flickering pixels (1.2 %)** |
| **the near plane** — 7 m → 35 m, 5× the depth precision | heals any tie decided by rounding rather than by geometry | **604 of 607 interior ties survive**; the whole frame goes 1,108 → 1,115 |

So the remainder is neither co-planar nor precision-limited. **It is the scene's own geometric
edges being resampled by a camera that moved** — which is what antialiasing is, is present in
every correct renderer, and is not a defect. R-BUG1's near plane had already taken the real
one.

**FINDING 1 — AN EXACT TIE IS STABLE, AND THAT IS WHY THIS SCENE GOT AWAY WITH 36,187 PIXELS OF
IT.** The depth-function switch moves **3.5 % of the whole frame**, so co-planar surfaces are
everywhere in this town — and not one of them shimmers. The reason is the arithmetic nobody had
written down: two surfaces at *exactly* the same depth quantise to the same value from every
camera position, so the tie is broken by DRAW ORDER, which is deterministic and does not move
when the visitor does. **It is the NEAR tie — a gap smaller than one depth quantum — that
flickers, because the quantum boundary is what the camera moves.** The two look identical in a
still frame and behave oppositely in motion, and this project had been reasoning about the
first while measuring the second.

**FINDING 2 — THE INSTRUMENT: A LAYER'S FOOTPRINT IS THE SET OF PIXELS THAT CHANGE WHEN YOU HIDE
IT.** `tools/measure_tie_class.mjs` partitions the flicker by what is actually drawn there —
exact ownership, decided by occlusion, the same way the depth buffer decides it. At
`from_above`, with the shadow map off by R-BUG6(a)'s repaired control:

| layer | footprint px | its flicker | share | interior | silhouette |
|---|---|---|---|---|---|
| structures | 22,175 | 556 | 50.2 % | 383 | 173 |
| trees | 56,565 | 491 | 44.3 % | 211 | 280 |
| ground | 721,346 | 35 | 3.2 % | 12 | 23 |
| water | 178,210 | 22 | 2.0 % | 1 | 21 |
| streets | 47,918 | 4 | 0.4 % | 0 | 4 |
| flora | 0 | 0 | 0.0 % | 0 | 0 |
| **unattributed** | — | **0** | — | — | — |

Zero unattributed and zero control drift, so it is a partition of the whole set rather than a
sample of it. **The buildings and the trees own 94.5 % of the flicker on 7.7 % of the frame** —
which is the shape of "edges", not the shape of "surfaces".

**FINDING 3 — AND THE TRAP IN MY OWN FIRST INSTRUMENT, WHICH IS WHY FINDING 1 NEEDED THE DEPTH
FUNCTION.** The `interior` column above was built to separate ties from edges: a pixel whose
owner's footprint surrounds it on all eight sides has nothing else drawn there, so a change
looked like the layer fighting itself. **It is not sound, and the frames say so** — a roof
against its own wall, a chimney against its own roof, one building in front of another and a
shingle course against the course below are all *interior to the `structures` footprint* and
all ordinary silhouettes. 607 "interior ties" survive at 5× precision precisely because 604 of
them were never ties. **A footprint tells you WHO owns a pixel and cannot tell you WHY it
moved**, and the column is kept, with this caveat printed beside it, because the ownership half
is exact and useful.

**FINDING 4 — `measure_river_edge.mjs`'s BANK MASK COUNTS THE SKY AS WATER.** Its water test is
`b > r + 6 && g > r`, and July sky passes it: measured on the same frame, **rows 0–200 are 1,280
of 1,280 "waterish"**, so `bank_px` = 33,328 is mostly the horizon and every roof and canopy
silhouette against it. The gate is a *share*, so both halves are inflated and it has not been
reading falsely — but **"784 of the bank line flickers" is not a statement about the river**, and
the number should not be quoted as one. The layer footprints in the tool above are what a real
bank mask would be built from: the boundary where the `water` footprint meets the `ground` one.
Not fixed here — it is R-BUG1's gate and changing its denominator changes a shipped threshold,
which is its own parcel.

**Verification.** `tools/check.sh` **CHECK PASS**. `SMOKE_VIEWPORT=mobile` on the published
mirror. The desktop half does not fit the runner's ten-minute per-command ceiling (§ THE RUN
BUDGET) and did not run; every figure above is `measure_tie_class.mjs` at 1280×800 on the
published mirror, control 0 px and return-to-pose 0 px on every run.

**What is left of R-BUG6, and it is not a renderer parcel.** The 36,187 co-planar pixels are
stable, but they are two surfaces of possibly different colours drawn at the same depth, with
draw order picking the winner — so *which* surface a visitor sees there is arbitrary even though
it is steady. Whether that is 3.5 % of the frame painted the wrong colour is a question about
the GEOMETRY, needs a bake, and is **R-BUG6(c)** below.

### R-BUG6(c) — 3.5 % of the frame is two surfaces at one depth · **UNCLAIMED · opened 2026-08-17 by R-BUG6(b) · NEEDS ONE BAKE · Effort: M**

The depth-function switch moves **36,187 pixels of a 1,024,000-pixel frame**. Every one of them
is a place where two surfaces sit at exactly the same depth *and are not the same colour* — if
they matched, the switch could not have moved the pixel. Draw order decides which one the
visitor sees, and draw order is a property of the batch, not of the building.

It is stable, so it is not flicker and not this parcel. It is a question about the models: which
pairs of surfaces are coincident, is it the same pair on every archetype, and is the surface
that currently wins the one the record intends? Start by attributing those pixels the way
`measure_tie_class.mjs` attributes flicker, then look at the generator that emits the pair.
**Needs a bake if the answer is to move a face**, which is why it is not folded into (b).

### R-BUG6(c2) — what fights INSIDE a layer · **ANSWERED 2026-08-23 by T-0013 · nothing there is a defect**

`measure_tie_class.mjs` splits each layer's flicker into a SILHOUETTE share (the boundary
against everything else, which any camera resamples) and an INTERIOR share, where the layer's
own footprint surrounds the moving pixel on all eight sides. The interior share was read as *a
layer fighting itself* and T-0013 was re-aimed at it: 370 px on `structures`, 257 on `trees`.

`tools/diagnose_interior_flicker.mjs` asks what the DEPTH FIELD does at each of those pixels,
by photographing a packed-depth pass at the base pose and at the nudged pose. Three answers are
possible and they are told apart without any per-surface threshold:

- an **internal edge** — a depth BREAK inside the layer's own footprint. A break is a second
  difference (`|d(-1) + d(+1) - 2·d(0)|`), which is ~0 on any plane however steeply it is seen
  and large where the surface changes, so a grazing roof cannot be mistaken for an edge.
- a **depth reorder** — locally smooth depth, and the front-most surface 0.3 m nearer or further
  after a 2 mm nudge. Two surfaces swapped. This is the fight the parcel was opened for.
- **neither** — same distance, same shape, a different colour: shading, not geometry. A
  near-coplanar z-fight also lands here, because a pair 1 mm apart swaps without moving the
  depth, so this class is where such a fight would have to appear.

Read at `from_above`, 1280×800, 2 mm nudge, shadow map off by R-BUG6(a)'s repaired control,
control 0 px and return 0 px:

```
layer        interior   internal edge   depth reorder   same surface   no depth
structures      370      349  (94%)        0   (0%)       0   (0%)         21
trees           257      252  (98%)        0   (0%)       0   (0%)          5
ground           78       75  (96%)        0   (0%)       0   (0%)          3
```

**Not one pixel in either layer is a depth reorder, and not one is shading.** Two controlled
toggles confirm it from the other side. Supersampling (device pixel ratio 1 → 2: four times the
samples, the same geometry and the same shading) leaves 63 of 370 structures px and 18 of 257
trees px moving — 83–93 % healed, which is what a coverage-bound edge does and what a depth
reorder cannot do, since every extra sample gets the same wrong answer. Going matte (18
materials at roughness 1, metalness 0 — the specular lobe gone, every vertex where it was)
changes 164,572 px of the picture and heals **nothing**: 370 → 370 and 257 → 256.

The `no depth` column is the same finding again rather than a gap in it. Those pixels read the
far plane where their layer is drawn, because a packed depth photographed through MSAA is a
BLEND of the samples' bytes, and the packing is not linear across its four channels. A pixel
whose depth cannot be decoded is a pixel with more than one surface in it.

**So the interior/silhouette discriminator does not mean what its name says.** `interiorOf`
knows one layer's outline against the rest of the scene; it cannot see the boundary between two
surfaces OF that layer — one crown behind another, a chimney against its own roof, a house
against the house behind it. Those are silhouettes too, and 94–98 % of the "interior" count is
made of them. What is left of R-BUG6 at `from_above` is: 21 px exactly coplanar (b), 0 px of
self-fight (here), and the rest is the town's own edges being resampled.

### R-BUG6(b) — the parcel as written, kept for the record

**The suspect list is one shorter and the remainder is measured**: with the shadow map switched
off by the repaired control, `from_above` still flickers **1,108** pixels and
`descend_main_stem` **2,008** under the 2 mm nudge. Those are ties, and R-W5a2 has already
characterised the class from the other direction — merging sixteen batches into one moved 942
pixels, *"all of them depth ties between co-planar surfaces of different materials"*.

**Start where R-W5a2 ended, not where R-BUG1 did.** The candidates left are the buildings'
`DoubleSide` faces meeting at a coplanar seam, the canopies' alpha-tested cards ordering
differently, and the confidence-view attribute path; the shadow map is spent. `--box-drift` is
the shape of instrument that works here — hold the camera still and move the one thing under
suspicion — and `--no-sun-shadow` is now a control that reaches the render, so a run can
subtract the shadow's share honestly rather than assuming it.

### R-BUG6 — the parcel as written, kept for the record

**Under the 2 mm nudge, with the bank line fixed, 1,173–1,883 pixels of every aerial frame still
change** — scattered over roofs, walls and tree canopies, not over the ground between them. The
control is 0, so it is not noise. It is the same class of defect R-BUG1 just closed at the
waterline: something in the frame is decided by a tie, and the tie is not stable.

**Start by proving your instrument.** R-BUG1's shadow-map suspect is untested, not refuted:
`measure_river_edge.mjs --no-sun-shadow` drops `sun.castShadow` after boot and changes **0 pixels
of the drawn frame**, so the run that "cleared" the shadow map cleared nothing. A test that
reaches the render has to rebuild the shadow state — or the scene — rather than flipping a flag on
a light whose materials are already compiled. **Land that control green before quoting any
number**, and the parcel's first commit is that control, not a fix.

**Candidates, none of them measured:** the shadow map's texel grid moving with the camera; the
buildings' `DoubleSide` faces meeting at a coplanar seam; the tree canopies' alpha-tested cards
ordering differently; the confidence-view attribute path. `tools/measure_river_edge.mjs` takes
`RIVER_STATIONS` and writes a magenta flicker mask with `--out`, which is how the bank line was
separated from the rest by eye in the first place.

**Runner:** lane 1, renderer only, no bake. It may run beside any town parcel.

Reported by the owner 2026-08-14: flying over the river, its edges flicker. Almost certainly
**z-fighting between the water plane at the datum (y = 0) and the terrain crossing it** — the
waterline is drawn by the depth buffer rather than by a traced outline, which is deliberate
(`terrain.js` header: the bank line IS where the ground crosses y = 0, so the waterline can
never drift out of step with the trace) and is exactly the configuration that co-planar
surfaces fight in at depth-buffer precision, worse the further the camera is from the
surface — hence "when flying".

**Owned by R-W5**, which is the parcel that touches the water surface. Do not fix it in a
lane-2 parcel or in passing.

**Candidate fixes, in the order worth trying:** a small `polygonOffset` on the water material;
raising the camera's `near` plane (a large near/far ratio is what starves depth precision at
altitude); or a logarithmic depth buffer. Whichever is chosen, the acceptance is that **the
waterline stays exactly where the ground crosses the datum** — a fix that moves the
waterline has broken the thing the current design exists to guarantee, and would need a
liberty entry.

**Reproduce:** fly to the `from_above` anchor, then descend slowly toward the forks; the
edges shimmer along the bank line.

---

## K — Kevin's punch list of 2026-08-13 · **THE PRIORITY QUEUE — steward, work these first**

Thirteen directions from the project owner, written up as parcels an agent can pick up cold.
Each names its files, its evidence, its gate and its trap. Standing policy for all of them:
**build liberally, grade honestly** — `conjectural` is a legitimate answer and the confidence
view paints it; the two absolute rules (never invent a source, never silently fill a gap) do
not relax. *Avoid circling on historical perfection: do the reasonable best, mark the rest,
move on.* One parcel per run; leave the others for the next tick or for interactive sessions —
check `git log` first so you do not duplicate a parcel already landed.

**Claims — how two runs avoid building the same thing.** `git log` only shows work already
LANDED, which is no help against work in flight: the scheduled steward and an interactive
session can both start the same parcel and neither can see the other until one of them pushes.
So a run taking a parcel big enough to be worth protecting marks its heading
**`· CLAIMED <date> — DO NOT PICK UP`**, writes one line saying who holds it and what to take
instead, and **pushes that to `main` before starting the work** — a claim that sits unpushed on
a branch protects nothing. Respect any claim you find. Claims carry an expiry, and an expired
one is void without ceremony: an abandoned claim must not become a permanent lock on a parcel.
Small parcels do not need this — the cost of claiming exceeds the cost of a collision.

### K24 — Let the visitor choose the light · **DONE 2026-08-17 · owner-requested 2026-08-14**

> **SHIPPED: a Brightness slider, 0 stops (the calibrated grade) to +1 stop, default off.** The
> design question the box left open is decided — **a slider, and the readout names the calibrated
> position** rather than showing a bare zero, on the eye-height precedent. The ceiling is **one
> photographic stop** because a stop is the unit a correction like this is bounded in, not because
> one stop looked right; past it ACES rolls the roofs and the sky into one flat highlight.
>
> **It did NOT have to wait for #125.** The sequencing note below was right that `world.js` is
> what #125 rewrites and wrong that this needed the file: the aid is one constant (`BASE_EXPOSURE`)
> and one method on the returned world, so #125 conflicts with two additions rather than a
> rewritten file. **A sequencing note is a claim about a DIFF, and it should be checked against the
> diff before it defers a parcel for three days.**
>
> **THE FINDING IS ABOUT R-A1'S READBACK, NOT ABOUT LIGHT.** `exposure` is the first reading on
> `window.__chicago4d` whose expected value MOVES, and it reported `0.95` on a frame that had just
> changed by 45 counts. `Object.assign` **invokes a getter and copies the value**, so
> `get roadAid()` — written inside the `Object.assign(api, {…})` literal by R-A1 one day earlier —
> **has been a constant 0 since it shipped**. Both of R-A1's readback gates assert `=== 0`, so a
> frozen 0 passed both; the liveness gate reads a frame signature and never touched it. The control
> was always live and the REPORT of its position was the dead thing. Fixed, plus a gate that the
> road aid reads back **1** when raised. **Read this before adding any reading to the harness:
> anything whose answer changes after boot goes in `Object.defineProperties`, and an assertion that
> can only ever see one value is not an assertion.**
>
> Measured, mobile 390×780, published mirror: off at boot `brightness 0 / exposure 0.95`; +1 stop
> moves the 12² signature **mean 49.40, worst 51**; `setBrightness(9)` clamps to **1**; restored
> residual **0.00 / 0**. Full write-up in `docs/STATUS.md`.

### K24 — the parcel as written, kept for the record

Owner, on being told R-W1 makes the scene 16 % dimmer and that holding the old brightness would
collapse albedo retention to 62 %: *"Can you make this an option in settings?"*

**It dissolves the trade-off rather than picking a side.** R-W1's argument for its own magnitude
is sound — a real sky is blue, and scaling it to carry a warm lamp's luminance destroys the wall
colours the dataset documents. But "correct and dim" and "bright and wrong" is a false choice
when the visitor can be handed the dial.

**Settings already has the shape for this.** `hud.js` `wireRange(id, label, key, fmt)` drives
`speed`, `eyeHeight` and `fov`; `s-units` is the select pattern; everything persists additively
into `chicago4d.settings`. Nothing new is needed structurally.

**The precedent to copy is the eye-height slider**, and it is exactly the right one. It prints
`— period eye level` when it sits on the researched default, *"so moving off it is a visible
choice instead of a silent drift"* (`hud.js`). A light control needs the same treatment: the
default position is the one calibrated against a verified July prairie photograph, and it should
say so on its face.

**The thing this must not become.** This project grades every claim by evidence. A brightness
control must read as a **viewing accommodation, like the units toggle** — the same scene, easier
to see — and never as a claim about how bright 1835 was. Label it so that no reading of the UI
suggests the brighter setting is an alternative reconstruction. The risk is concrete: a visitor
who moves the dial and then forms a judgement about the town's colours is judging under a light
this project has just measured as **1.86× the luminance and 2.85× the red** of its own sky.

**The non-negotiable: calibration stays anchored to the DEFAULT.** `tools/critic_shots.mjs`,
`tools/light_probe.mjs` and every gate in `smoke_renderer.mjs` measure the default setting and
must keep doing so. If a gate can be made to pass by moving this control, the control has become
a way to launder a failure — add an assertion that the default rendering is unchanged by the
setting's existence, and that the harness reads the default regardless of stored preference.

**AND THAT PAIR IS NOT ENOUGH — copy R-A1's THIRD assertion (2026-08-16).** R-A1 shipped this
exact shape of control for the roads and found that "off at boot" plus "the default is unchanged"
both pass identically when a control is **wired to nothing**. It gates three ways: off at boot,
**raising it changes the frame**, dropping it restores the frame. R-A1's box has the code, the
grid it had to be measured at, and the numbers.

**Open design question, worth deciding rather than defaulting:** a two-way choice between named
rigs, or a continuous exposure slider with the calibrated point marked? The slider matches the
eye-height precedent and is friendlier; the toggle is harder to misread as "accuracy dial".
Recommendation: **slider, with the calibrated default named in the readout** — but say which was
chosen and why.

**Sequencing:** this touches `world.js`, which **PR #125 rewrites substantially**. It must land
**after** #125 resolves or it will conflict badly. It also does **not** unblock #125 — that PR's
road-gate failure occurs at the *default* setting, and a preference control does not change it.

**Files:** `renderers/web/js/world.js` · `renderers/web/js/hud.js` · `renderers/web/index.html`
(the control) · `tools/smoke_renderer.mjs` (default-unchanged assertion) · `docs/index.html` (Help)

**Acceptance:** `tools/check.sh` green; the setting persists across reload and does not break an
existing stored `chicago4d.settings`; the default rendering is byte-comparable to before the
setting existed; every critic and smoke measurement still reads the default; the readout names
the calibrated position; **mobile 390×780 is a release gate** and the control must be reachable
and legible there.

### K23 — The invented buildings are still NAMED "Inferred", and the card never says what we made up · **K23a DONE 2026-08-15 · K23b DONE 2026-08-15 · owner-reported 2026-08-14**

> **BOTH HALVES ARE DONE.** K23a made the prose agree with the grade (193 names); K23b put the
> per-level summary on the card. Findings under "K23a — what the sweep actually found" and
> "K23b — what the summary had to decide" below.

Owner, from a card on the dev preview: *"these are recreated structures, recreations, not
inferred right? Like if it was totally invented based on our population household program it was
probably recreated not inferred. Can you check those description cards. And when you say what we
made up, say what we included in the recreation, or what we included in the inferred building, or
what we included in the attested building."*

**They are right, and the card contradicts itself on screen.** The title reads
**"Inferred A2 barn or carriage shed #08"** while the chip directly beneath it reads
**RECONSTRUCTED**, and so does every other chip on the card.

**Verified, not assumed.** `data/structures/recon_1835_blk_randolph_market_a1_07.json` contains
the string `"reconstructed"` **thirteen times** and `"inferred"` **zero** times — and its `name`
is `"Inferred A1 stable #07"`. **193 structure records** are named this way.

**Why it happened, and it is the residue of a fix that worked.** Changelog **v76** moved 9,076
values onto the current three levels and re-graded 1,694 that had claimed to be reasoning when
they were invention. It moved the DATA. It did not move the generated PROSE, which is hardcoded:

```
tools/generate_block_infill.py:522    "name": f"Inferred {family} {function} #{seq:02d}"
tools/generate_block_infill.py:543    "change_note": "Inferred anonymous July 1835 block infill…"
tools/generate_inferred_infill.py:229 "name": f"Inferred {family} {function} #{seq:03d}"
tools/generate_inferred_infill.py:251 "change_note": "Inferred anonymous July 1835 infill…"
```

Under the OLD vocabulary `inferred` was the BOTTOM tier and those names were honest. Under the
current one it is the MIDDLE tier — *reasoned from evidence about this particular thing* — which
is exactly what an anonymous roof dealt by the household programme is **not**. So every one of
the 193 names now claims a grade **better than its own record**, in the largest text on the card.
This is the v76 fault surviving in the most visible place in the app.

**SPLIT — claim ONE. A and B are a mechanical sweep and a design question, and bundling them
means the sweep waits on the design.**

- **K23a — make the prose agree with the grade.** Part A below. Deterministic, re-derives
  through the generators' `--check`, and it stops the app contradicting itself on screen. Ship
  it on its own.
- **K23b — say what we actually did, per level.** Part B below. This one needs a wording
  decision and a card layout, and it should not hold up 193 names that are currently wrong.

**Part A — make the prose agree with the grade.** Fix it in the GENERATORS, not the records:
they are `--check` gated, so the records must re-derive rather than be hand-edited. Sweep the
`name`, `change_note` and `research_note` prose, and `data/residents/` too. Then check whether
any OTHER user-visible string still uses a level-word in its old sense.

**Part B — say what we actually did, per level.** This is the substantive half, and the owner's
own framing is the specification: for each building the card should say **what was included and
where it came from** —

- **attested** — which attributes the source states, and which source;
- **inferred** — what was reasoned, and *from what specific evidence about this thing*;
- **reconstructed** — what we invented, and what bounded the invention (the archetype table,
  the household programme, the 665-roof schedule).

The card already carries per-attribute chips and `why` disclosures, so the parts exist; what is
missing is the plain summary a visitor reads first. *"A yard building off the block alley"* does
not tell them the footprint, the height, the roof form and the position were all invented and
only the block was reasoned.

**The trap.** `K16` below is **STALE and must not be followed** — it describes a rename to
`documented/derived/inferred` that was superseded by what actually shipped in v76
(`attested/inferred/reconstructed`). Whoever takes this should close K16 out with a line saying
so. The standing instruction to stay vocabulary-agnostic while K16 was in flight is spent: the
vocabulary landed, and this parcel is about making the words on screen match it.

**Files:** `tools/generate_block_infill.py` · `tools/generate_inferred_infill.py` ·
`tools/generate_inferred_households.py` · `renderers/web/js/popup.js` · regenerated
`data/structures/*` · `docs/PROVENANCE.md` · `docs/ROADMAP.md` (close K16)

**Acceptance:** `tools/check.sh` green with every generator's `--check` re-deriving; **no
user-visible string names a level it is not**; a smoke assertion that a record's displayed name
never contradicts its own existence grade — put the fault back and it must name it; the card
states what was included at each level for one attested, one inferred and one reconstructed
building. Mobile is where it was reported.

#### K23b — what the summary had to decide · **DONE 2026-08-15**

**Shipped:** a section at the TOP of every provenance card — `What did we include, and where did
it come from?` — that partitions every graded claim below it into the three levels, names the
claims at each, and says where they came from. `renderers/web/js/popup.js` (`basisSection`),
`renderers/web/css/walk.css`, four assertions in `tools/smoke_renderer.mjs`, and the changelog.
No data changed and no generator ran: this is entirely a reading of records that already existed.

**Making it a PARTITION is what made it gateable, and that was the design decision.** A summary
can be written as a highlight reel — *"attested: its size, its position"* — and nothing can then
check it, because there is no arithmetic to disagree with. Every claim the card renders lands in
exactly one row instead, so the gate is a RECOUNT: pick every building, tally the confidence chips
off the rendered card, and require the section's own three numbers to be those numbers.
**All 276 loaded buildings agree, at both viewports.** The recount deliberately uses the SAME
selector as the older chip-coverage assertion (`.pop-meta .conf, .pop-sec table.attrs .conf`) —
two definitions of "a claim on this card" is exactly how a summary would come to disagree with
the card it summarises while both gates stayed green.

**A citation means a different thing at each level, and one label over all three would have been
the same category error this card's history is made of.** On an `attested` claim a source is
where the value came FROM. On a `reconstructed` one it is what BOUNDED an invention — the
records say so themselves (*"the spec is cited because the invention is bounded by it, which is
what makes it defensible rather than arbitrary"*) — and 193 anonymous roofs cite
`owner_chicago_1835_reconstruction_spec_2026` and `andreas_1884_v1` on every attribute they have.
A single `sources:` line over the summary would have printed a nineteenth-century history as
attribution for a building nobody claims stood there. The three leads are **From**, **Reasoned
from** and **Bounded by**.

**Attested is not the same as built, and a summary of what was INCLUDED is exactly where that
gap does damage.** The Western Hotel's stables are `attested` — a pre-fire account describes the
wagon yard — and there is nothing of them in the model. **14 records carry an attribute in that
state.** The rows below have marked it since the `geometry` declaration existed; the summary
repeats it (`Not in the model: stables`) rather than averaging it into a count of things we
included. Gated on the discriminating pair: the Western Hotel shows the line, the Sauganash has
no such attribute and shows nothing.

**An empty level says so in words, and that is the common case rather than the edge case.**
Across the dataset's 279 records and **3,675 graded claims — 199 attested, 509 inferred, 2,967
invented — 204 records have no attested claim at all.** A row that rendered only when non-empty
would go silent on three quarters of the town, at the one moment a visitor most needs telling.
So the attested row on an anonymous roof reads *"Nothing about this building is attested by a
source."*

**The finding this parcel did not go looking for: 69 buildings have inventions that nothing is
recorded as bounding.** `reconstructed` requires a note, not a source — deliberately, and K23a
argued why the old "a bottom-tier value citing sources is suspicious" rule died with the rename.
The consequence had never been counted: of the 270 records carrying at least one invented claim,
**69 cite nothing at all on any of them**, so their `Bounded by` line reads *"Nothing is cited as
bounding these."* The Sauganash Hotel is one of them — its footprint is the placeholder its own
note calls a placeholder, and no typology is named beside it. That is honest and it is now
VISIBLE, which is the point; whether those 69 should acquire a bound is a research question for
a successor and not something to paper over on the card.

**Two things deliberately not done.** The section does not claim to cover the LIBERTIES — a
liberty belongs to no attribute, which is why it has its own section — so the lead points at
"What we made up here" rather than implying three rows of claim labels are the whole of what was
invented. And the three definitions are the Evidence panel's own words, literally: each is a
substring of the legend in `index.html`, asserted as such, because two surfaces quietly
disagreeing about what `inferred` means is the fault K23a spent a run cleaning up.

#### K23a — what the sweep actually found · **DONE 2026-08-15**

**The parcel named two generators. There were five, plus a sixth stage nobody had listed.**
`generate_block_infill.py` and `generate_inferred_infill.py` were the two written down;
`generate_north_infill.py`, `generate_west_infill.py` and `generate_inferred_households.py`
carry the same four strings, and `generate_inferred_names.py` is a **second pass that runs after
the household programme and rewrites the household's own label**. Regenerating the households
without it silently deleted every invented resident's name and `name_basis` block — the whole of
K18 — and the diff was the only thing that said so. **`generate_inferred_households.py` then
`generate_inferred_names.py`, in that order**, or you lose the naming layer; the household
programme's `--check` hides this by overlaying the naming pass before it compares, so `--check`
is green either way.

**Four strings per generator, not one.** `name`, `change_note`, `research_note` — and
`symbolic_location`, which the parcel did not list and which said "Anonymous inferred roof in
the …" on 162 records. All four now say `reconstructed`.

**"NOT A DOCUMENTED NAMED BUILDING" was wrong twice in one line.** Every `research_note` ended
by contrasting itself with a tier called `documented`, which has not existed since v76. It reads
`NOT AN ATTESTED NAMED BUILDING` now.

**The counts, so the next sweep can tell drift from a fresh fault.** 193 names, all on records
graded `reconstructed` at existence — and the three `research_note` openers partition them
exactly: 142 `RECOMMENDED / GENERATED`, 31 `INFERRED BUILDING`, 20 `INFERRED / GENERATED`. There
is no fourth group and no record was missed. `recommended` is the word this project renamed away
from **by name** on 2026-08-13 and then kept printing on 142 cards for a fortnight.

**Three things outside the app were saying it too, and two of them are worse than the cards:**

- **`docs/PROVENANCE.md` documented a vocabulary the build rejects.** It still defined
  `documented / inferred / conjectural`. It is the page you send someone to when they ask what
  the grades mean, so anyone following it would have written a record `validate.py` refuses.
  Swapped, with a dated note recording the rename and pointing at `CONFIDENCE` as the
  enforcement. Its `reconstructed` row also had to change MEANING, not just spelling: the old
  bottom tier meant "no evidence, filled for visual completeness", the new one means "invented
  within a bound and owing a note", and the rule that a bottom-tier value citing sources is
  suspicious **died with the rename** — the source that bounds an invention is what makes it
  defensible. `documented_range` keeps its name; it is a field, not a level.
- **`validate.py`'s own error messages named the wrong tier.** A missing source on an `attested`
  value reported *"documented requires at least one source_id"*; a `reconstructed` value with no
  note reported *"inferred requires a note"*. An error that names a grade the project does not
  have sends the reader to fix the wrong field.
- **The smoke's own household assertion required the bug.** It asserted the household label
  matched `/inferred/` — so the release gate was *holding the fault in place*. It is pinned to
  the head's own `grade` now rather than to a literal, which is the form that cannot rot.

**What was deliberately NOT changed, and why.**

- **`reconstruction.status: "inferred_anonymous"`, the `inferred_1835` phase id, the
  `hh_inf_*`/`1835_inferred_household_programme.json` filenames, and the generator filenames.**
  These are machine identifiers: never printed, and `inferred_anonymous` names the GLB files.
  The last time this value was renamed, `popup.js` was left testing the old string and **the
  reconstruction flag silently vanished from 108 cards** — a test on a value nothing carries is
  always false. Prose moved; keys did not. The card's wording and its key are now decoupled on
  purpose, with the reason written at the test.
- **`renderers/web/js/changelog.js` entries v87 and earlier.** They are the historical record and
  describe what shipped *at the time*, when "recommended reconstruction" was the word actually on
  the cards. Rewriting a shipped release note to look better is the kind of tidying this project
  exists not to do.

**Left for a successor, stated rather than quietly skipped.** `docs/PROVENANCE.md`'s *arguments*
were only re-read where the word-swap made a sentence flatly false. Its § "They may, however,
carry a position to `inferred`" still glosses the bottom tier as asserting *no evidence exists*,
which was true of `conjectural` and is only half true of `reconstructed`. That is prose about
reasoning rather than a mislabelled grade, so it is a separate read against `validate.py` and
not a line to change in passing.

### K1 — The inferred-residents programme *(the big one; multi-session; carve into districts)*
Chicago went from ~350 people (1833) to ~3,265 (late 1835). Build the POPULATION as a dataset,
then build the buildings it implies. New directory `data/residents/`: one file per HOUSEHOLD,
grouping persons, with per-person fields — name, arrival date (month if knowable), party size,
origin, why they came, period-correct occupation, where they lived, where they worked — and an
accuracy grade using EXACTLY this vocabulary: **`documented`** (named in a source: Andreas is
dense with them — officials, ministers, traders, tavern keepers, the *Democrat*'s advertisers),
**`derived`** (a real person whose details are partly reconstructed), **`inferred`** (a
hypothesised resident filling the town's demonstrable needs — the first barber, the second
blacksmith, the cooper the packing trade requires). NEVER "recommended" — the words are
**inferred residents** and **inferred structures**. Natives who remained belong in the
population where sourced; depiction of people stays out of scope (L1) — this is a DATASET layer
feeding structures. Cross-reference each household to `data/structures/` ids (`lives_at`,
`works_at`); businesses cluster toward the river/streets, residences spread outward as the town
crowds (use the Thompson plat lots, K7). Extend `tools/validate.py` so a resident's source_ids
must resolve and grades are enforced. **The primary goal is buildings**: every inferred
household that needs a dwelling gets an `inferred structure` record on the plat, archetyped,
baked, confidence-graded — this is how the town reaches its true 1835 density. Start with
DOCUMENTED people (mayors-to-be, Ogden, Hubbard, the clergy, every advertiser already in
`chicago_democrat_1833_11_26`), then derive, then infer to fill the count by occupation census.

**Phase one DONE 2026-08-13** — the documented and derived layer: 72 households, 96 persons,
`tools/validate.py check_residents()`, and the rename that retired "recommended" from the
vocabulary and from the code. **Phase two DONE 2026-08-13** — 80 inferred households and 92
person entries (152 / 188 in all: 76 documented, 20 derived, 92 inferred), **38 new structures**
(7 documented buildings the sources describe and the model lacked, 31 inferred workplaces and
dwellings), and **83 of the 108 anonymous roofs adopted** into argued occupancy. 222 structures;
162 name a household on the card. `docs/LIBERTIES.md` L84 admits the lot; the recipe and its
re-runnable gates are `data/reconstruction/1835_inferred_household_programme.json` +
`tools/generate_inferred_households.py --check`; reasoning in
`docs/RESEARCH/residents_1835_inferred.md`.

**Phase three (a) DONE 2026-08-13 — the buildings are out of the road, and the gate can see the
road now.** The placement gate in `tools/generate_inferred_households.py` tested overlap, water
and modelled ground and had never tested for the street. It does now, through
`tools/plat_corridors.py` — the same module `tools/generate_plat_lots.py --report` reads, so the
check and the generator that must satisfy it cannot answer differently — and it refuses **any**
generated footprint that reaches inside a platted corridor. **23 of the 38 recipe centres moved**
(median 12.0 m, worst 21.9 m); in-corridor centres across the whole scene fell 22 → 10 and not
one of the ten is a generated placement. The centre test had understated the problem by more than
half: the recipe read the 80 ft frontage bands as lines to sit ON rather than edges to sit
BEHIND, so a row of Lake Street shops stood with its front half in the street and its centre a
metre outside the corridor, invisible to a point test. Footprints inside a corridor across the
scene: **56 → 33**. Positions stay `conjectural`: clearing the roadway is not standing on a
recovered lot. Detail in `docs/RESEARCH/thompson_plat_grid.md` § 7a.

**What phase three inherits.** (a) No inferred person is named and none should be — an inferred
resident is a claim about a ratio. (b) **No period trade table for a comparable western town is
in `data/sources/`**; every ratio is derived from five in-dataset calibrations and the arithmetic
is written out per trade. Finding a real trade table is the single highest-value research errand
left in this programme, because it would move the occupation census off derived arithmetic.
(c) 25 anonymous roofs are deliberately unadopted (privies, sheds, stables, the schoolhouse).
(d) The 55 reserved West-Division slots and 84 South phase-2 slots are untouched and the
placement gate now actively avoids them. (e) Two households arrive at `year` precision straddling
1835-07-01 (`hh_davis_john`, `hh_haddock_edward`) and are still warnings.

### K2 — Image-accuracy loops on the landmark buildings
Reference set: `data/sources/assets/prefire_views_kevin_2026_08/` (12 plates; READ ITS README —
the Doric-portico courthouse plate is the 1837+ building and is a NEGATIVE reference). Also
https://chicagology.com/prefire/prefire275/ (source record exists). Loop per building:
render the model's building from the plate's viewpoint, compare, improve, repeat until massing,
roof, fenestration rhythm, chimneys and signboard match. Tier-5 pictorial rule holds: views
drive FORM as `inferred`, never a coordinate or footprint. **Green Tree first** (plate 11 —
two-storey clapboard, end chimneys both gables, even 6/6 bays, hanging corner SIGNBOARD, rear
ell), then the fort group (palisade on rising ground), then Sauganash/Wolf Point.

**Two cautions this parcel has now paid for, both from the fort pass (T-0044 → T-0094).**

1. **"Whitewashed palisade" is the reference set's README talking, not a source.** The plate paints
   the fort's one continuous north curtain across a **1.85×** range of tone in a single view —
   luminance 191 east of the gate work, 103 west of it — with the surface this project ships
   (`hewn_log`, luminance 143) sitting between the two. Fergus's white-washed board fence is the
   enclosure of **1850**, after the pickets came down. Neither licenses a tone.
2. **This loop compares two pictures BY EYE, and that is how it produced a wrong ticket.** T-0044's
   row 3 said the model's pickets were flat-topped and the plate's pointed; the model has carried
   0.312 m of sharpened head on all 768 posts since the archetype was written, and the plate rules
   its cap straight to 0.45 px rms while resolving pickets at a 10 px pitch. Both readings were
   available to anyone who measured, and nobody had. **Where a row of this pass asserts a shape or a
   tone, measure it before it becomes a ticket** — `tools/measure_picket_plate.py` is the shape of
   instrument that costs a minute and settles it. T-0094 is the write-up; **T-0184** is the one
   finding of that measurement that survived.

### K3 — Flora pop-in and coverage · **POP-IN DONE 2026-08-13; COVERAGE STILL OPEN**
Grass and flowers "appear out of the ground as you walk towards them."

**The pop-in half is fixed, and the diagnosis is the part worth keeping.** The transition was
not missing — `ringFade`/`innerFade` had been scaling every plant down over the outer band of
its ring since the layer was written. It was *frozen*: the fade was baked into the instance's
height at lattice-rebuild time, and the lattice is rebuilt only every `TUNE.step.near` metres
walked. So the ramp was sampled once per stride and held. With a 1.2 m step against the near
ring's 2.2 m band, a plant went from nothing to **55 % of full height between one frame and the
next** — a fade function producing a step, which is why the code looked like it already did
what the owner was asking for.

The ramp now runs per FRAME in the vertex shader against `cameraPosition` (`aChiRing` carries
`[outer, band, inner, innerBand]` per instance; the scale is uniform, about the plant's base).
Three things came with it:

- **Flower heads have to descend, not just shrink.** A head's origin is partway up a stem, so
  scaling it in place leaves it hanging over a plant that is no longer under it. `aChiRise`
  carries the height of the head over its own plant's base and the shader lowers it by
  `rise × (1 − fade)`, applied after the instance transform because the instance matrix carries
  a real rotation for the tilted heads.
- **The `fade < 0.35` head gate was a step in the middle of a ramp** — and the most conspicuous
  pop in the field, because a flower is the brightest thing in it. Heads have their own ring now,
  reaching zero exactly where the plant's ramp passes 0.35, so the same heads are drawn and the
  head cap sees the same pressure.
- **The lattice is now inset from the fade ring by the rebuild step** (`ringsFor`), which is what
  makes arriving-already-grown impossible rather than merely rare: a plant is always already
  placed, at zero height, before it is near enough to be worth any. The outer edge is bought by
  moving the *fade* in (growing the lattice would cost a 34 % wider near annulus against 6 % of
  triangle headroom — see K14); the inner edge by moving the *lattice* out, which costs 1.3 % of
  the mid ring and keeps the near/mid crossover exactly where it is. `step` is halved to 0.6 m,
  since its job is now the width of that margin rather than the frequency of the ramp.
- **The bound is one frame, not zero**, and it is stated rather than hidden: the rebuild fires on
  the frame that carries the walker past the step, so it can overshoot by however far that one
  frame moved — 0.024 m at 60 fps, about 1 % of a plant's height. The gate walks twenty 0.15 m
  paces at both viewports and requires every plant arriving in front of the walker to be under
  10 % of full; measured 0.0 %.

**Coverage, part one, DONE 2026-08-13: the sward reads each community's own recorded cover.**
The zone records author `cover.matrix_fraction` per community and a `bare_soil_fraction` beside
it; `tools/validate.py` gates both and `index.json` denormalises the second so the ground shader
can fetch it once. **`flora.js` had never asked for either.** All ten communities were planted at
the one lattice density L32 tuned on closed wet prairie, so the settled town (0.45 matrix, 0.45
bare by its own record), the shaded riverbank understory (0.45), the lakeshore sand (0.35) and
the forest floor (0.35) were drawn as densely as prairie that covers the ground completely. The
fraction is now the probability a matrix lattice slot carries a plant, in the near layer and the
mid cards alike — the rule the forb layer has always applied to its own recorded densities.
Measured across the eight communities with a clean sampling station: planted density spans
**2.21–6.90 per m²** where it was one number, and the implied full-cover density agrees at
**6.31–8.15** against a lattice that carries 7.30. **Wet prairie is untouched** (it records 1.00),
so nothing the prairie sweep tuned moved, and the change can only ever remove instances: measured
against `main` at 1280×800, wet prairie is 360 979 tris against 360 863 (the reshuffled draw), the
settled town 429 281 against 441 683 and the marsh edge 299 161 against 308 235. L32 carries a Revised line: the density RATIO between two
communities is the record's now; the absolute figure and the saturation anchor stay liberties.

**Still open: COVERAGE, part two.** The mid-field targets from the prairie sweep stand in § S6a,
and the near ring's *visible* radius is 0.6 m shorter than it was — that is the pop-in inset, and
it is a coverage question for this half of the parcel to weigh.

**The middle-distance ring seam is out, 2026-08-13 — S6a item 3.** The outer edge of the sward
was a circle about the walker, and on ground with 4.30 ft of relief across the whole box a
constant world radius is a constant screen ROW: measured at **1.4 px** of variation across the
view before the change, which is the sweep's "razor straight across all 1280 columns" as a
number. Every lattice slot now carries its own outer radius, offset by a world-anchored fringe of
±3 m at full detail, and the boundary spans **5.9 px** at 1280×800 and **17.4 px** at 390×780.
It costs nothing — triangles are paid for by the lattice and a slot pushed out of reach is
dropped rather than drawn at zero height — and it takes nothing off the ring's mean reach, so it
is not a coverage loss dressed as a fix. Full note and the traps in § S6a item 3.

**Two findings that slice measured and did not fix — BOTH RESOLVED 2026-08-13.** (a) **S6a item 9
named the wrong zone.** It read the `river_bank` shot against zone 1's cordgrass at 40–55 %, but
ground within eight metres of water is the MARSH zone by extent (`z04`, priority 70) — measured at
the shot's own bank, the sward there is 100 % z04 and z10, and none of it is z01. The marsh's own
record says 0.75 matrix and 0.0 bare, which is what it is now planted at. Item 9 says so now.
(b) **Two floating-leaved aquatics were rooted on dry land — FIXED, and it was a data field.**
`nuphar_advena` and `nymphaea_odorata` are `role: emergent`, `form: mat_prostrate`, 0.01–0.10 m
tall, and their own `appearance` says "floating pads in open water" — but that is prose, and
nothing machine-readable distinguished a water lily from a cattail, so both were planted on the
dry marsh edge like any other emergent: **6.5 % of the tufts** on that bank, pads at ankle height
standing on soil, which is a better explanation of the "~25 cm sprigs" in item 9 than any density
is.

`data/flora/index.json` now publishes a **`substrates`** vocabulary — `soil` (rooted ground above
the water, the default when the field is absent), `saturated_soil` (the emergent habit: wet ground
OR standing water, foliage above the surface) and `open_water` (rooted below the surface, leaves
floating ON it) — every `role: emergent` record must state one, and `validate.py` refuses an
`open_water` species in a zone whose extent never reaches water, because a record that can never
be drawn is a claim the walkthrough does not make. `flora.js` splits each community into the
subset legal on each side of its waterline and picks from THAT, with the weights renormalised
over the subset: the recorded `matrix_fraction` still decides how many slots carry a plant, so
clearing the lilies off the bank does not thin it. Refusing the slot instead would have removed
6.5 % of that sward, and 0.75 does not stop meaning 0.75 because two of its species float.

**Measured, both viewports.** An 8 m sweep of the modelled box finds **299 dry marsh-edge
stations** (289 the placer will plant at all) and **286 over water**; the two lilies were legal at
every one of the 289 and are now legal at **none**, while the cattail still stands on both sides
(289 dry / 273 wet). At the marsh-edge station nearest the forks the sward is the same density it
was — **2 483 → 2 481 rooted instances, 47 551 → 47 435 triangles** — and the two `head_ray`
flowers that stood on that dry bank, which are the water-lily blooms, are gone. A wet-prairie
control station is identical to the byte. New gate: three assertions in `smoke_renderer.mjs` that
ask the placer itself (`flora.stationOf`) rather than re-deriving its rules, including the
anti-vacuity half — a placer that refused everything on that bank would otherwise read as a pass.

### K4 — Facades: weathered wood, not painted clones
The buildings read as freshly painted and identical. Research first, then implement: most 1835
Chicago frame buildings were UNPAINTED weatherboard or whitewashed — paint was expensive; keep
the documented exceptions exactly as documented (Wau-Bun's white Sauganash with bright-blue
shutters). Add material variation per building — board tone jitter, weathering by age of the
phase, board-width irregularity — so no two share a face (extends L22/L23 rather than
repeating them). Log buildings: hewn vs round logs per record. Cite what you can; grade the
rest `inferred` with the economics argument in the note.

### K5 — The town's furniture: fences, yards, wagons, signs, porches, docks
The scene is buildings on bare ground; a working town has STUFF. In order: (a) the
**`enclosure` archetype** — fence line, gateway count, gate width, fence type (picket/rail/
worm) — already the single biggest structural gap: it discharges the estray pen (currently a
roofed shed, wrongly), the Western Hotel wagon yard (L10), Clybourn's stockyard, garden fences
(the Kinzie-view plate shows picket-fenced garden plots and Lombardy poplars — reference for
TREATMENT, the house itself stays excluded); (b) **signboards** on businesses — attested
(the Green Tree plate's hanging sign; the wolf sign documented) — parameter exists in
`frame_storefront`, switch it on per record, lettering stays undrawn (L25); (c) **yard
objects**: wagons/drays (documented mired on Lake St), woodpiles and lumber stacks (Ordinance 9
documents timber, stone, brick, boxes, barrels IN the streets), crates and barrels at the
stores, kitchen gardens (fort garden documented; dooryard gardens inferred), stove pipes on
every frame building (Ordinance 6 — documented, none modelled); (d) **porches** ONLY where
attested or typologically argued — the Kinzie piazza is the attested exemplar; do not blanket
the town; (e) **docks/wharves** at the forwarding houses (attested "with its dock along the
river front"; needs a river-wharf mode of `pier_crib`). Everything invented gets its liberty.

**(b) is shipped on a SIGNAGE layer, and it struck one of its own citations.** **T-0039**:
`data/signage/`, `renderers/web/js/signage.js`, generated by
`tools/generate_business_signboards.py` and re-derived by `tools/check.sh` — 24 blank boards on
business frontages chosen by a rule (named record · public trade · trade attested or inferred ·
standing · no sign already), 4 refused in writing, every vertex graded `reconstructed` (L130),
lettering undrawn per L25. Two corrections to this box's own line above. **The Green Tree plate's
hanging sign is not evidence this project holds**: `data/sources/chm_green_tree_1859.json` records
that the image has never been retrieved and `verified` is false, so it underwrites nothing and is
struck from the argument. **And "switch the `frame_storefront` parameter on per record" cannot be
done here** — that parameter is Blender's, so the archetype route waits on a bake; the layer above
is the renderer-side half and needs none. What (b) still owes: the GENERATOR half, so a baked town
carries its own boards; and any source that gives a WORDING, which is the only thing that could
ever put lettering on one.

**And that last sentence was overtaken by the owner — T-0066, 2026-08-21.** *"you can and should
put the name of the location on the sign board. the sign boards should have variation in color and
style and signage font and color, some signs may hang from an awning and others may be on the
building or painted on the face of the building. you need to add more signage and be period
correct and it is fine if they are reconstructions."* So the layer now carries the NAME of every
business it selects — the name the record already gives it, so the sign and the card agree — in
one of ten colourways and four letterforms, on one of five mountings (bracket, awning hood, board
on the wall, post at the street edge, and the name painted straight onto the building), dealt so
that no two signs within 40 m share a style or a ground colour. The count is 23 → **33**: the
trade rule gains a WORKS AND WAREHOUSE class that paints its firm on its front and hangs nothing.
**L25 is untouched** — no board carries an image or a trade device, and the wolf is still a wolf
with no words on it. Everything T-0066 adds is `reconstructed` and claimed at **L158**. What (b)
still owes is unchanged and now shorter: the GENERATOR half, and a source that gives a wording, a
colour or a mounting for a named house.

**And the wording itself was corrected the next day — T-0130, 2026-08-22, so the paragraph above
is now the argument that was available before the owner read a board.** T-0066 painted THE
RECORD'S OWN NAME, which is this project's label for a BUILDING and not what a signwriter
lettered. The owner, of the Carpenter board: *"philo would not have referred to his own place as
log drug store … that may be different than the name of the building for us, the sign may read
differently historically"*; of the next: *"same with hogan's store"*; and then *"i guess do a pass
on all those signs and make sure they feel right for the era."* All 33 are re-lettered in the
register the town's own newspaper advertising uses — proprietor or firm first and largest, the
trade beneath, the place last and smallest — with the wording as its OWN field, free to differ
from the `name` and tied to it only by a declared `sign_identity` that must appear in both.
**14 carry a firm's own advertised line (`inferred`)**, 19 are `reconstructed` from the trade
vocabulary those pages evidence, and **none is `attested`**, because the seven newspaper pages
behind them are images supplied in conversation and are not committed to `data/sources/assets/`.
Every one of those notes says what would upgrade it and the recipe is in ticket **T-0130**, so
what (b) still owes has changed shape: not "a source that gives a wording" — the wordings are here
— but **the seven pages committed as source records**, which would take fourteen of them off
`inferred` in an afternoon. **L25 is STILL untouched**, and T-0130 is the case that shows why it is
about IMAGES rather than about signs: Carpenter's own 1835 notice heads itself *"AT THE SIGN OF THE
GOLDEN MORTAR"*, so his board carries a painted mortar — a device its owner described in print —
while the wolf, which nobody described, is L165's and rests on a sentence saying a wolf was on it.
No other board gets a device, and the smoke pins that count at one. **L166.**

**(c) is shipped IN PART, on a YARD layer, and its evidence is the strongest on this box.**
**T-0040**: `data/yard/`, `renderers/web/js/yard.js`, generated by `tools/generate_yard_goods.py`
and re-derived by `tools/check.sh` — **149 objects at 26 trading frontages** (102 upright casks,
46 packing cases, an empty laid on its side outside the public houses) and **one wagon**, every
vertex graded `reconstructed` (L131), no brand, name, stencil or label on any of them. Unlike (b),
this clause does not rest on a treatment argument: **Ordinance 9 of 7 November 1833 is a tier-1
contemporary statement that this town's streets had timber, stone, brick, boxes and barrels
standing in them** (`data/sources/chicago_democrat_1833_11_26.json`), and a corporation does not
legislate against a thing nobody does. What it gives is no address at all, so which frontage is a
rule — a named record, a goods-keeping trade, that trade attested or inferred, on the TOWN's
ground (the fort's provision store and the sutler's are refused: federal ground, no corporation
street in front of the door). **One correction to this box's own line.** *"wagons/drays
(documented mired on Lake St)"* — **this project holds no source record for that claim**, so it
underwrites nothing and is struck. The wagon that IS drawn rests on `chicagology_prefire278` and
the Western Hotel's yard, the one place in the town named for wagons, at a stand derived rather
than picked. What (c) still owes: **the timber, stone and brick half of Ordinance 9**, which is
building material on a lot under construction rather than a merchant's stock and is filed as its
own ticket; goods standing in a ROADWAY, which is the ordinance's own stronger reading and is
deliberately not drawn here; stove pipes on every frame building (Ordinance 6); and the generator
half, so a baked town carries its own yards.

**(e) is shipped on a WHARF layer, and it is the clause on this box that had been owed longest.**
**T-0041**: `data/wharves/`, `renderers/web/js/wharves.js`, generated by
`tools/generate_river_wharves.py` and re-derived by `tools/check.sh` — **two docks, 26 crib bents,
every vertex graded `reconstructed` (L132)**. **This box's own line said it "needs a river-wharf
mode of `pier_crib`", and that is a BAKE reason**: the renderer-side half needs no Blender, the
same argument that already carries (a), (b) and (c). Which frontage is a rule and it reads the
records rather than a trade table — a sidecar standing on the scene date whose own `dock`
attribute is true and graded `attested` or `inferred`, which selects exactly the two warehouses
this line cites and refuses every other river frontage in the dataset. The outline is derived
(the committed footprint's max-`v` edge, the traced 1834 bank's own tangent at the nearest point,
the committed heightfield for the depth at the face) and the SIZE is invented within stated bounds;
the deck's height is the terrain's, sampled at load, which is T-0001's finding applied to a layer
that has no walk surface to catch it twice. Both `dock` attributes move from `geometry: "absent"`
to `"simplified"`, which is the half of **L66** this discharges — the bank each warehouse stands on
is untouched and still open. What (e) still owes: a deck a visitor can walk out along (its own
ticket); anything lying at either wharf, which no source here describes; and the GENERATOR half, so
a baked town carries its own docks.

**(e) grew a third shore on 2026-08-24, and the reason the first two were the only two is worth
recording. T-0062** stated five reconstructed docks on the owner's *"you can add more docks!"* — and
it stated them on **South Water merchants**, so the town's other shores were never asked. The North
Division shore had a landing only because Kinzie & Hunter's dock is attested; the west bank at Wolf
Point, five buildings all fronting the water, had none. **T-0107** asks the trade test of every river
frontage in the town, and on the west bank it selects exactly one record: **Robert A. Kinzie's
storehouse**, "dealing in groceries and Indian goods", whose committed position note of 2026-08-11
had already reasoned that *"a storehouse trading goods off canoes has a positive reason to face the
landing"*. Five landings now stand where four did (L179). The row's other four state no dock and get
none — lodging, dwelling and worship take nothing off a canoe. It also shipped **clause 6**: the
deck is one standard rectangle set on the bank's own tangent, **the bank bends at Wolf Point**, and
a face that would stand on dry ground (PR #258 measured −0.34 m at Hogan's store) is refused with
the measured rise on the record rather than given a bespoke outline. The clause refuses nothing in
the town as it stands and is proved by `generate_river_wharves.py --selftest`, which `--check` runs.

**(a) is shipped in three pieces, all on the enclosure layer** (`data/enclosures/`,
`renderers/web/js/enclosures.js`) — the renderer-side half of the archetype this box asked for,
which needs no bake. **T-0050** built the layer and the Western Hotel's wagon yard (L127);
**T-0051** moved the estray pen onto it and retired its roof (L128, L60 resolved); **T-0052**
added the `picket` fence type and the **dooryard garden plots** this line cites the Kinzie-view
plate for — 18 of them, on platted house lots chosen by a rule and generated by
`tools/generate_dooryard_pickets.py` rather than placed (L129). What (a) still owes: Clybourn's
stockyard, the pig pens the November 1833 town code implies, the fenced-or-unfenced state of the
public square, and the GENERATOR half — `palisade` still builds no enclosure form, so nothing here
is baked with the town.

### K6 — The river bulge at Clark Street · **DONE 2026-08-13**
Not paper stretch and not a mis-traced stream: the traced south bank had been walked round
the **outline capital G of "CHICAGO RIVER"**, which Wright letters across the channel, joined
to the drawn bank by a brown foxing stain. `tools/trace_shoreline.py` gained a declared
`LETTERING` window that reads the map's own type as type, spliced into the uncorrected ring
so the declared box is the blast radius. Heightfield regenerated: **0 cells changed outside
the corridor E +505 … +660, max |delta| 0.000000 m, 0 waterline crossings**; inside it 1 719
cells, max 3.605 m, 620 crossings, all land → water. Gradient audit unchanged and passing
(`plain_block_max` 0.468 ft / 300 ft). Memo:
`docs/RESEARCH/clark_reach_bulge_1834.md`. The 78–80 m vs 15–19 m South Water discrepancy
this item cited was this defect, so **`docs/RESEARCH/chicago_american_office.md` § 3 now
overstates the Clark residual** and should be re-measured against the corrected trace.


### K7 — Thompson plat lot lines · **PHASE ONE DONE 2026-08-13**
Generate block/lot geometry analytically from the plat module (80-ft streets, documented lot
widths), snapped to the datum — the S1 carry-forward note already prescribes exactly this.
Commit as `data/traces/vectors/thompson_lots.json`. It becomes the placement grid for K1's
inferred structures and the check on every "corner of X and Y" position in the dataset.

**Shipped**: 19 blocks, 152 lots, generated from the module and this project's committed street
lines by `tools/generate_plat_lots.py`, re-derived byte for byte in `tools/check.sh`. Block edges
are `inferred` (arithmetic on inferred street lines and an inferred module width); the lot lines
and the alley POSITION are `conjectural` and say so — four lots to a face is a reading of one
block, block 18 on the owner's Clark-reach crop. No lot or block is numbered: this project has
never read Thompson's numbering off a sheet. Five candidate blocks are refused with their
reasons, three of them because a block there would span the South Branch. Memo:
`docs/RESEARCH/thompson_plat_grid.md`.

**What phase two inherits.** (a) ~~Seven structures stand 6.5–12.1 m inside a platted street
corridor~~ — **DONE 2026-08-13 under K1 phase three (a)**: the gate exists
(`tools/plat_corridors.py`, shared with `--report`), 23 recipe centres moved clear, and the
report now measures FOOTPRINTS as well as centres, which is what showed the seven to be the loud
end of a set of 23. ~~What is left in the roadway is not the generator's: **four anonymous roofs**
from the two infill generators (worst `recon_1835_south_a5_044`, 4.3 m — that gate is added when
that parcel next runs, because moving an anonymous roof re-derives the occupancy ledger those
generators own)~~ — **DONE 2026-08-13 as phase two (b)**: both infill generators carry the gate,
through the same `tools/plat_corridors.py`, and **no generated placement anywhere in this dataset
stands in a platted corridor** (footprints in a corridor 33 → 29). The four were one row's
spacing, not four numbers: the parcel's eight ancillary buildings were laid on a 123 m pitch —
the block pitch — which put one at the eastern edge of every block, and the four that passed
passed by being privies rather than by being placed (1.4–2.1 m clear against a ±20 m
georeference). All eight now stand behind the easternmost principal roof of their own block,
which is what a rear yard is; 17–32 m of movement, nothing regraded, and the household ledger
keys on id so the adoptions survived. Detail in `docs/RESEARCH/thompson_plat_grid.md` § 7b. What
is left is **29 hand-placed records whose positions carry a frontage argument**. Of
those, thirteen are on South Water Street and they are a finding rather than a queue: from South
Water's committed centreline the traced 1834 waterline is **10.75 m away at E +180 against a
12.19 m half-corridor**, so the platted street there runs 1.4 m into the river and a building on
its north side cannot be both clear of the corridor and on dry land. That is the plat module and
the drawn bank disagreeing, and it wants a reading of the travelled way (L79), not a nudge to
thirteen records. The Sauganash's first cabin remains the reminder that a building in the street
is sometimes a fact, and `slough_log_bridge` in the South Water corridor is the reminder that
sometimes it is the point. (b) The grid
covers 19 of the plat's 58 blocks; the North Division is absent because its street control is
what § S9 still records as owed, and `blk_south_water_market` — one of the most built-up blocks
in town — is refused only because the street layer does not carry South Water west of E +100.
(c) Two pitches disagree with the 1834 traverses (Dearborn→State 128.0 m, Lake→Randolph 142.8 m)
and are recorded rather than averaged. (d) No source in `data/sources/` gives a Thompson LOT
DEPTH; the depths here are residuals of the block, and finding a stated one is what would move
the lot lines off conjecture. (e) Nothing draws the grid — when the lot lines reach the screen
they need a liberty and a confidence treatment with them.

### K8 — River bank heights *(research first, then terrain)* · **DONE 2026-08-20 (T-0004)**
The owner: banks look too low against the fort views (10–20 ft with graduated slopes). The
dossier gives +2–4 ft banks at the forks (documented) but the FORT stood on distinctly rising
ground — "the flattened mound", the 1830 Harrison plan's bank, Swearingen's 18-ft pool at the
fort bend. Parcel: re-read `01-terrain-hydrology.md` and the primary accounts; raise and
GRADUATE the fort-reach south bank as the evidence supports; record the disagreement between
the tier-5 lithographs and the dossier rather than averaging it; keep the forks banks at their
documented height. Gradient audit re-run; exemption itemised like the others.

**Shipped**: the mound raised from the zone's mid-range to its stated apex —
`fort_dearborn_mound.rise_ft` 2.8 → 3.8, flat top +11.0 → +12.0 ft, the north face carrying
the full rise to the waterline at 1:6.8 (inside the bank block's 1:6–1:10 band). The
disagreement is three-cornered, not two, and is recorded rather than averaged in
`docs/RESEARCH/fort_reach_bank_heights.md`: the witnesses (Swearingen 1803 tier-1 ~8 ft;
Hubbard 1881 "not over eight feet", a correction pushing DOWN) keep the BANK, zone 6's
+10–12/apex +12 takes the mound, and the plates' 10–20 ft is refused as a build input.
Hubbard-vs-zone-6 stands unresolved on the record — if the owner rules the witnesses outrank
the dossier's reconciliation, the mound drops to ~+8; that is a ruling, not a research gap.
Measured: 2,169 changed cells, max +0.305 m, zero outside the mound's 75 m radius — the forks
byte-identical. Gradient audit PASS (plain max 0.468), mound band itemised as before. The
bank now standing is what unblocks T-0099's track from the north gate down to the water.

### K9 — Navigation and settings UI · **DONE 2026-08-13**
(a) A **"Go to" tab** — buildings and street intersections, DOCUMENTED entries only for now
(inferred locations join later once K1 lands); it replaces the overlapping Viewpoints list and
sits as its own tab after Controls. (b) The panel opener becomes a **hamburger menu** (it is
more than settings); reassess the "?" icon. Mobile 390×780 gate; smoke tests updated with the
UI, never weakened.

**Shipped**: one list — 8 authored viewpoints, 4 verified junctions and all 222 loaded
structures — in a `goto` tab second in the strip, opened by <kbd>G</kbd> (which focuses the
search on a keyboard and deliberately does not on a phone, where it would raise the on-screen
keyboard over the list). The Settings copies are gone: the viewpoint chips and the duplicate
search are both retired to it. `#btn-help` is a hamburger with `aria-label="Menu"`.

**The one departure from the parcel as written, and why.** It does NOT list documented entries
only. K1 has landed since this was written, and the honest reading of "inferred locations join
later" is now the second one: **no structure position in this dataset is `documented`** — 54 are
`inferred` and 168 `conjectural` — so a documented-only menu would have held four junctions and
nothing else. Every structure instead carries its own `placement.position_confidence` as a chip,
in the popup's three words and three colours, and the gate compares every chip against the
record it jumps to. Viewpoints and junctions carry none: neither is a claim about the town.

**What it inherits.** (a) The tally in the tab is counted from the list, so it moves when the
dataset does — nothing to restate here when a position is regraded. (b) Five tabs fit with about
20 px of slack at both viewports (desktop panel widened 360 → 380 px, tab padding 9 → 6 px,
mobile type 12.5 → 11.5 px); a **sixth tab does not fit** and the gate will say so rather than
shipping a two-row strip. (c) The gate's own desktop half had not been running: see § the smoke
budget in STATUS.

### K10 — Bridge approaches
"How would a wagon cross that?" Every bridge currently floats over its banks
(`approach_not_modelled`). Build abutment earthworks/ramps that meet the deck at grade on both
ends — evidence: the 1883 settlers' statement (log abutments IN the shallow water near the
banks), deck heights already documented. Walkable end to end, wagon-plausible gradients;
regrade `ground_contact` as each bridge actually lands; move the relevant liberty text.

### K11 — Trees standing in the river · **DONE 2026-08-13**
The river mask (`isWater`) begins 100 mm BELOW the water plane, so a stem could root in that
band, pass the mask and render standing in open water — 36 of 618 stations were doing it.
`trees.js` now requires every tree and thicket to stand `TREE_DRY_MARGIN_M` = 0.20 m clear of
the epoch's own `water_surface_m` (0.15 m of sunk bole + the 0.03 m ground-mesh tolerance,
plus 20 mm). 197 candidates rejected; lowest surviving station +0.201 m. New smoke assertion
**"no tree stands below the waterline"**, alongside — not replacing — the river-mask check.


### K12 — Loop hygiene *(standing instruction to every steward run)*
Every run that adds anything user-visible writes its changelog entry (v: null, ts: '') IN THE
SAME RUN — the overnight push of 2026-08-11 landed ~50 buildings with no changelog entry and
the owner noticed before we did. Publish (`tools/publish.sh`) and merge to main so the deploy
actually ships; main is the only branch Pages publishes.

**2026-08-13 — the changelog was corrupted by a MERGE, and the gate now runs in `check.sh`.**
`main` carried a `renderers/web/js/changelog.js` that did not parse, and had done since merge
`65c8de1`. One missing `] },` swallowed 64 entries into one; a duplicate `v: 64` rode along. The
What's-new tab was dead on the live site and this project reported no releases to Manager or the
launcher. **Both parents of that merge parse; the merge does not** — `.gitattributes` merges this
file `merge=union`, and the union driver runs during the merge, so a green PR can still produce a
red `main`. Repaired, and `tools/check.sh` now runs `tools/check-changelog.mjs` as a step
(previously a hand-run instruction in AGENTS.md, which is precisely what a merge-time corruption
evades). The contract check now reads the literal's shape as TEXT before executing it, and names
the entry that lost its terminator and the entry that got swallowed. Detail in STATUS.

**What is still open, and it is not this parcel's to fix.** Nothing runs on a merge commit
itself. The repository's CI lives outside `chicago/4d` and outside this lane's scope, so a merge
performed on GitHub can still publish a union-corrupted changelog with no gate between it and
Pages. Two candidate fixes, both needing a decision rather than a slice: run the subtree's gate
from the repo's own workflow on pushes to `main`, or replace `merge=union` on this path with a
merge driver that understands the literal. **The standing instruction until then: any agent that
performs a merge affecting `changelog.js` re-runs `tools/check-changelog.mjs` AFTER the merge,
not only before it.**


### K13 — The La Salle Street re-entrant, and the other Main Branch sloughs
Wright draws a narrow watercourse dropping south off the main stem between plat blocks 19 and
18, at local E +462 … +469 — La Salle Street. The waterline trace carries its mouth (that is
as far as Wright washes it) and nothing beyond. The dossier records that the 1830 Thompson
plat shows **three sloughs off the Main Branch**, and ROADMAP § S2e makes Conley/Stelzer 1833
the primary guide for where the streams come in and where they terminate. Parcel: identify
the three, and carry the ones that are attested as `hydrology.geojson` CENTRELINES in the
form the north-side slough already takes — never as traced boundaries, because the bank wash
is not there to trace. Cross-check the State Street slough mouth the trace already carries at
E +850 … +856 against dossier zone 14.

### K14 — The terrain decimator’s tolerance cliff · **DONE 2026-08-13**
`generators/terrain_gen.py --decimate-deg` behaves as a cliff, not a dial, against
`MESH_FIT_TOLERANCE_M`: after the K6 correction, 0.040 and 0.038 both land at 30 mm and are
refused, while 0.030 lands at 3.1 mm — and costs 247 527 triangles / 6.4 MB against the
previous 135 249 / 3.5 MB. The GLB now committed is the 0.030 one. Worth a look at whether
the planar decimate is the right operator here, or whether the fit should be enforced by a
quadric-error budget instead of a dihedral angle; the payload is inside the 25 MB budget
(`tools/publish.sh` reports 19.16 MB) but the ground is now the largest single asset by a
wide margin. **The rendered-triangle budget is the tighter constraint**: the smoke measures
**564 681 tris at 1280×800 against a 600 000 budget** — 6 % of headroom, where before this
change there was roughly 25 %. The terrain is `frustumCulled = false`, so all 247 527 of its
triangles are in every frame. The next parcel that adds geometry will hit this ceiling
before it hits the payload one.

**RESOLVED 2026-08-13, and not where this item was looking.** The decimator was never the
problem worth solving: the ground was ONE mesh with `frustumCulled = false`, so its whole
247 527 triangles were drawn every frame no matter which way the walker faced. Cut into a
**12 × 3 grid by triangle centroid** (`renderers/web/js/terrain.js tileGround()`), each tile
carries its own bounding sphere and the ones behind you are skipped. Desktop went **550 513 →
461 112 triangles** at 71 of 80 draw calls; headroom is now **138 888** where it was 49 487.
Grid picked by measurement — 8×4 gives the same draw calls for 27 000 MORE triangles, 12×6
saves another 26 000 but leaves ONE draw call spare, which is not headroom.
**Two things still on the table**, neither taken: (a) 12×6 or finer, if the draw-call budget is
ever deliberately revisited — the terrain tiles are cheap calls sharing one material, but the
budget is a gate and moving it is a decision, not a side effect; (b) the decimator question as
originally written, which is now about PAYLOAD rather than frame cost and is much less urgent
since the published tree fell to 10.78 MB (see the meshopt fix of the same day).
**The payload figure quoted above is stale** — 19.16 MB was measured when the anonymous roofs
were placeholder massing and every web derivative was an uncompressed copy of its master.
### K18 — The invented residents have names · **DONE 2026-08-14**

Every reconstructed resident used to read "A baker (inferred resident, unnamed)", and the record
argued for it: an invented surname would make the entry indistinguishable at a glance from the
documented layer beside it. That is sound about the DATA and wrong about the TOWN — a place
where most households are called "an inferred cooper's household" reads as a spreadsheet, not a
town. The owner asked for names.

**What bounds the invention.** The pools in `data/reconstruction/1835_invented_name_pools.json`
are seeded from the **76 ATTESTED residents this project already holds** — real people, named
from cited sources — so an invented cooper is named the way this town's real coopers were named
rather than the way a novel would name one. Three communities, each with the evidence that puts
it here: New England and New York (the documented origins run Vermont, Connecticut, New York),
French colonial and metis of the Detroit and Milwaukee country (Beaubien appears three times
among the named residents), and Irish (one attested origin in County Kerry; Egan and Casey).

**Where a weighting is itself a guess, it says so.** Boatmen draw French colonial ON EVIDENCE —
the carrying trade of this river was worked by that community. Labourers draw EVENLY, and the
note explains why: the Irish labouring Chicago of popular memory arrives with the canal
contracts of **1836**, after this scene, so weighting 1835 labourers Irish would be importing a
later decade into this one.

**What stops it becoming a laundering route.** A name looks like a fact in a way "wall height
3.25 m" does not, which makes it the easiest way for an invention to be mistaken for a finding.
So: every reconstructed person carries a `name_basis` block, graded `reconstructed`, whose note
opens "THE NAME IS INVENTED"; `validate.py` **errors** if a reconstructed person lacks one, if
its grade is anything better, or if an attested person carries one at all (their name comes from
a source and marking it invented would understate what is known about a real person). Three
self-tests hold all three directions. Assignment is deterministic from the person's id and
`check.sh` re-derives it, so a name that moved without the pools moving is a finding.

Names are **dealt** round each pool rather than drawn independently: independent draws put four
unrelated households under "Lyman" and four under "Gilbert", and a shared surname reads as
kinship this layer claims nothing about. 61 distinct surnames across 92 people.

### K17 — Hiding a level, folded into the confidence control · **DONE 2026-08-14**

The confidence chip coloured the town by evidence. It now also has a caret, and behind it three
checkboxes: **Attested 11 · Inferred 69 · Reconstructed 162**, counted from the loaded registry
rather than written down. Turning one off removes it from the view outright.

**Hiding is deliberately independent of the colouring.** They are two questions and the second
is the more searching one: colouring asks how sure we are, hiding asks *what is left if you keep
only what somebody wrote down*. Tying it to the colour mode would mean you could only ask it
while the whole town was amber and dithered, and the answer reads far better in daylight. Turn
off `reconstructed` and most of the town vanishes. That is the honest picture of how much of
1835 Chicago is recoverable, it is not a comfortable thing for this project to show, and it is
now one click away.

Implemented as one `uHideLevel` uniform banded from the same thresholds as `levelOf()`, so the
shader and the labels cannot disagree about which level a fragment is in. The choice persists,
is applied before the first frame (a returning visitor should not watch the hidden town flash
in), and the caret carries a dot while anything is hidden — a control that quietly removes two
thirds of the buildings has to say so while its panel is shut.

### K19 — The town shipped as 242 two-metre boxes, and the gate was green · **DONE 2026-08-13**

> **DONE.** Fixed in `buildings.js` + `terrain.js`; new gates in `smoke_renderer.mjs`; the trap
> is written up in `docs/GLB-CONTRACT.md` § *Quantised geometry: float before you transform*.

**What the visitor saw.** Every building at roughly a sixth of its size. At South Water and
Lake — the busiest corner in the town — two knee-high boxes and some very large trees. Live for
several days, through two attempted fixes.

**The defect, exactly.** Under `KHR_mesh_quantization` a POSITION is a *normalized* `Int16Array`
— stored integer over 32767, so the attribute can only represent `[-1, 1]` — and the metres come
from a dequantisation scale on the node (6.25 on the Sauganash).
`BufferAttribute.applyMatrix4` reads denormalised floats, transforms them, and writes the result
**back into that same normalized `Int16Array`**. Applying the dequantisation therefore clamped
every coordinate over a metre to exactly one metre. Both scale regressions were this one
write-back: discarding the node transform gave two-metre buildings, applying it gave two-metre
buildings *in pieces*, because the clamp is per-axis and a building is not centred on its
origin. The fix is to float first and transform second, in both modules.

**Why three rounds of diagnosis missed it.** Every reading was taken from a tree that does not
have the bug. A sidecar's `gltf/<name>.glb` resolves against `assets/` in the source tree — the
uncompressed masters — and against `data/` on the site, which `publish.sh` fills from
`assets/web/`. The smoke had never once loaded a compressed asset. Local captures rendered
correctly, measured buildings came out at sensible sizes, and all of it was true and irrelevant.

**Three gates now exist that would have caught it on day one:**

1. `smoke_renderer.mjs --published` serves the mirror and enters at `/walk/` — the visitor's
   exact bytes and layout. `bake.sh` runs it after publish. This also covers the other failure
   this project keeps hitting: a file that exists in the source tree, is never copied, and 404s
   only when live.
2. Per-structure size assertions. The old check took the **tallest** building in the scene and
   asked whether it was between 3 and 30 m — which passes with one correct building and 241
   broken ones, and that is the scene that shipped. Every structure is now measured against its
   own record, including its documented `wall_height_m`. Reintroducing the fault fails the new
   checks by name on all 242 and quotes the heights they should have had.
3. `tools/measure_glbs.py` measures assets against records with no browser at all, and
   `tools/shoot.mjs` takes pictures rather than assertions — because the assertions were green
   and the town was not.

**The lesson worth keeping:** a gate that cannot reach the bytes that ship is not a gate, and an
aggregate assertion (`max`, `any`, `the tallest`) hides exactly the failure mode where almost
everything is broken. Neither of those is specific to quantisation.

### K15 — The two reserved anonymous parcels · **WEST PART DONE 2026-08-13 · SOUTH STILL CLAIMED**

> **WEST: DONE.** `tools/generate_west_infill.py` emits **20 of the 55** and is re-derived by
> `tools/check.sh`. The other **35 are held by the recipe's own terrain gate** — their centres lie
> west of local E -300 m and the committed ground stops at E -320 m. They are not lost: ids and
> family allocation are kept, and extending the terrain box west releases them without
> re-authoring. Admission: `docs/LIBERTIES.md` **L90**. **Eight of the twenty stood inside a
> platted street** by 2.2–11.7 m and were set back (largest move 12.5 m, inside the recipe's own
> ±20 m); the recipe predates K7's plat grid, so nothing could have caught it before. Frozen
> constants in the generator, not a search at generation time.
>
> **SOUTH: still claimed, and it is the harder half** — the recipe has `clusters` and a
> `placement_schema` but NO `placements`, so its 84 slots must be AUTHORED against the cluster
> overlap-controls (reserve envelopes around every named South Water and Lake Street record, keep
> out of the Public Square, respect the estray-pen envelope) and then generated the same way.
>
> **CLAIM — steward, skip the South half.** Taken by the interactive session on 2026-08-13 after
> K14 freed the triangle headroom it needs. It is a large, single, indivisible unit (two
> generators, ~139 records, one liberties block) and two runs building it concurrently would
> collide on `data/structures/` and on the 665-roof ledger, which is exactly the kind of
> conflict that is expensive rather than merely annoying. Take **K2, K4, K5, K8 or K10**
> instead. This claim is void if no commit touching it lands by **2026-08-15** — a claim that
> outlives the work is a lock, and nobody should be blocked by an abandoned one.

Two recipes have been sitting fully specified and uninstantiated, and together they are the
largest remaining block of buildings in the project:

- **`data/reconstruction/1835_phase2_west_wolf_point_approaches.json`** (`status:
  research_recipe_not_instantiated`) — **55 roofs**, 44 principal + 11 ancillary, 40.7 % of the
  135-roof West Division target. Group mix and per-family counts (D1–D7, H1–H2, C1–C2, W1–W5,
  F1, A1–A5) are already written. Memo: `docs/RESEARCH/west_division_infill_1835.md`.
- **`data/reconstruction/1835_phase2_south_core_and_mixed_recipe.json`** (`status:
  proposed_not_generated`) — **84 roofs**, 66 principal + 18 ancillary, against a 370-roof South
  Division target. Carries a `placement_schema` and a `coordinate_system` block with the UTM
  conversion spelled out. Memo: `docs/RESEARCH/phase2_south_core_and_mixed.md`.

**The pattern to follow already exists twice**: `tools/generate_inferred_infill.py` (South
phase 1, 48) and `tools/generate_north_infill.py` (North, 60), both re-derived byte-for-byte by
a `--check` step in `tools/check.sh`. A third and fourth generator in that shape is the job —
NOT hand-written records, because 139 hand-placed buildings cannot be re-derived and the
placement gate would have nothing to check against.

**The traps, all of them already paid for once.** (a) The counting rule is in the South recipe's
own words: *a better-evidenced roof SUBSTITUTES for a slot; it never increases the 665 target* —
so these 139 do not stack on top of K1's 38. (b) `tools/generate_inferred_households.py` placed
K1 phase two while actively avoiding these slots, so they are still clear — keep it that way, and
re-run its `--check` after. (c) Every conjectural existence, position and footprint owes a
`docs/LIBERTIES.md` entry with `Covers:` tokens, in both directions. (d) Placement must pass the
existing gates: no footprint within 3 m of any other, terrain covered, dry, ≤0.30 m perimeter
relief — and `Heightfield.covers()` exists because a structure once landed 832 m adrift and
reported a perfect fit. (e) Triangle budget: 139 roofs at the ~723 tris the K1 bake averaged is
~100 000, against 574 440 of headroom at Full detail. It fits now; it did not before K14.

### K16 — The confidence vocabulary is wrong, and the owner named the fix · **CLOSED 2026-08-15 — SUPERSEDED, DO NOT FOLLOW**

> **CLOSED by K23a.** The rename happened, but **not to the words written below**. This parcel
> proposed `documented / derived / inferred`; what actually shipped in the v76 merge of
> 2026-08-13 is **`attested / inferred / reconstructed`**, and `tools/validate.py`'s `CONFIDENCE`
> tuple is the enforcement. Everything from "The rename, which is a rename and not a new tier"
> onward describes a vocabulary this project does not use — **a record written to the table below
> fails the build.** `docs/PROVENANCE.md` is the current authority and now carries a dated note
> saying so.
>
> The parcel is kept rather than deleted because its *reasoning* is the reasoning behind the
> words that did ship, and because it is the origin of the fault K23a swept up: it left the
> standing instruction to stay "vocabulary-agnostic while K16 is in flight", and under that
> instruction 193 generated names went on saying `Inferred` for three weeks after `inferred`
> stopped meaning invented. **That instruction is spent.** Read the strings off
> `docs/PROVENANCE.md`, not off this section.

The owner's correction, 2026-08-13, in their words: *"I don't want to use inferred in those kind
of cases where there was some solid research behind it… the government blacksmith shop seems
fairly good in location and you labeled it inferred. Inferred is the name for when you make your
research combination and invent a person based on likely needs of the city and population."*

They are right, and the fault is that two very different acts share one word. Placing the agency
blacksmith shop from Andreas's description is RESEARCH; inventing a cooper because a town packing
two thousand hogs needs one is INVENTION. Both currently read `inferred`.

**The rename, which is a rename and not a new tier** — the three existing levels keep their
meanings and their paint, and two of them get honest names:

| now | becomes | paint | means |
|---|---|---|---|
| `documented` | `documented` | white / unmarked | a source attests this at the scene date |
| `inferred` | **`derived`** | gold | reasoned from specific evidence ABOUT THIS THING — a described location, a measured lot, an adjacent record. Researched and likely. |
| `conjectural` | **`inferred`** | dithered | invented to fill a demonstrable need of the town. No evidence for this particular thing. **Not a "guess"** — the owner asked for that word to go. |

This also UNIFIES the two axes: `data/residents/` already grades people
`documented` / `derived` / `inferred` with almost exactly these meanings (docs/PROVENANCE.md and
`data/residents/index.json`). After the rename one vocabulary covers both.

**Order matters, because the words collide mid-flight.** `conjectural`→`inferred` cannot run
before `inferred`→`derived`, or every old `inferred` is swallowed. Do it as ONE scripted pass
with a two-phase substitution through a sentinel, re-derive every generated record, and diff the
count of each level before and after: the totals must move as a permutation, not change.

**What must move with it:** `schemas/*.json` enums · `tools/validate.py` (including
`check_liberties_coverage`, which keys on `conjectural` — after the rename the liberties trigger
is `inferred`) · the three infill generators and the household generator, whose literal strings
are re-derived byte for byte · `renderers/web/js/confidence.js` · the Evidence legend in
`index.html` · `popup.js` · `docs/PROVENANCE.md`, `AGENTS.md`, `docs/LIBERTIES.md` prose.
**Do not rewrite the historical prose in `docs/STATUS.md` or shipped changelog entries** — they
are a record of what was said at the time.

### K17 (spec) — Confidence view: dither the roofs, and let a level be switched off · **DISCHARGED 2026-08-14**

> Built. The roof half landed with K20b, which made the whole of a reconstructed building
> dither together — walls, roof, trim and chimney — rather than leaving a ghost with a solid
> chimney on it. The switch-a-level-off half is the K17 entry above. The original spec is kept
> below because it is what was asked for and the entry above is what was built.


Depends on K16's vocabulary. Three things the owner asked for on 2026-08-13:

1. **The roofs do not dither.** In the confidence view the walls take the dithered treatment and
   the roof planes do not, so a building that is entirely invented still reads as half-solid.
   Find out whether the roof material misses the `_confidence` attribute or the patch, and either
   dither it or — the owner's own suggestion — give the roof a distinct treatment so a dithered
   wall and a dithered roof stay legible against each other.
2. **A hide mode.** *"I would like to be able to toggle that view to make the buildings objects
   items disappear altogether based on those levels."* So the confidence view gains a mode: COLOUR
   (today's behaviour) or HIDE, where a level's geometry is removed from the scene rather than
   tinted — walk a town of only what is documented, then only what is documented and derived.
   The owner suggests consolidating it into the confidence control rather than adding a second
   one, which is right: it is the same question asked two ways.
3. Per-level toggles, so the three levels can be shown or hidden independently.

**The honest trap:** hiding by level must hide whole OBJECTS by their record's grade, not
individual attributes — a building whose position is derived but whose roof pitch is inferred is
one building, and it has to be somewhere. Decide and write down which attribute governs an
object's visibility (existence, surely) before building the control.

### K18 (spec) — Invent period-appropriate names for inferred residents · **DISCHARGED 2026-08-14**

> Built — see the K18 entry above for the pools, the weighting and the validator rule that
> keeps an invented name from ever grading above the invention. Spec kept for the record.


The owner, 2026-08-13: *"for inferred people you can invent/create period appropriate names for
them… of course it's one of the inferences so I'm sure it will be clear… use whatever historical
research is reasonable for names like doctors might have some names and laborers would have
others."*

This REVERSES the standing rule in `docs/LIBERTIES.md` L84 and `data/residents/index.json`, which
say no inferred person is named. That reversal is the owner's call and it is made — but the
reason for the old rule has to be answered rather than forgotten: a named invented person must
never be mistakable for a documented one. So the name is an attribute like any other and carries
the `inferred` grade the person already has; the card must show the name and the grade together.

**Do the research rather than picking pleasant names.** 1835 Chicago's inferred population should
draw on the documented one's own composition — the 1833 trade roster and the residents already in
`data/residents/` are the sample: New England and New York Yankees, New York Dutch, Irish and
German arrivals on the canal works, French-Canadian and Métis families at the forks. Trade
correlates with origin in ways the sources support (canal labour heavily Irish; merchants and
professionals disproportionately Yankee), and that correlation — not a random draw — is what
makes an invented name defensible. Surnames and given names should come from period-attested
lists, and the memo must say which and why, per the standing rule that a source_id resolves.

Add `name_basis` (or equivalent) to the person record so the card can say WHY this name and not
another, and extend `tools/validate.py` so an inferred person's name cannot be graded above
`inferred`.

---

## S1 — Georeference and verify the datum · **DONE 2026-08-09**

Origin: E 447072.7, N 4637395.8 (EPSG:26916) = 41.886721, -87.637951 — the Wright-drawn forks,
eight-GCP fit RMS 17.5 m, cross-checked against an independent Hathaway georeference (57.9 m)
and the modern OSM junction (39.4 m). The published Allmaps 3-point transform was measured
(RMS 25.9 m against independent control) and superseded; no annotation existed for the LOC
Hathaway, so that georeference is new work. Memo: `docs/RESEARCH/datum_derivation.md`;
enforcement: `tools/rederive_datum.py` in `check.sh`. Carry-forward: ±20 m working uncertainty
for anything traced from the 1834 sheets; generate street geometry analytically from plat
dimensions (Hathaway annotates them) and snap to control rather than tracing pixels.

## S2 — Terrain, epoch `e1834_harbor_cut`

### S2e — extend the ground EAST to the lake · **IN PROGRESS — parcel (a) DONE 2026-08-10**

Promoted above the rest of S2 because the free-fly camera made the gap impossible to
miss from the air: **the modelled ground stops 800 m short of Fort Dearborn and about a
kilometre short of Lake Michigan.**

The numbers, measured against `data/datum.json` rather than estimated:

| | local E | inside the box? |
|---|---|---|
| current terrain box | −320 … **+320** | — |
| Lake St & State St | +842 | no |
| **Fort Dearborn site** (Michigan Ave bridge) | **+1127** | no, 3.5× beyond the edge |
| modern lakefront at the river mouth | +2155 | no |

(Landmark positions are modern-successor scoping figures, not dataset claims — they say
how far the box falls short, nothing about 1835.)

**The 1835 lake edge is nowhere near the modern one** — everything east of roughly Michigan
Avenue is later landfill, much of it fire debris after 1871 — so drawing today's coast
would be the single largest false claim in the dataset. It comes off Wright 1834. This is
precisely the case the year-parameterized architecture exists for: `docs/EPOCHS.md` treats
terrain as versioned per epoch, so a later year gets its own shoreline rather than editing
this one.

**Which source drives which element** (set 2026-08-10 by Kevin, who is right that the
earlier reading of these sources was over-cautious — see `docs/PROVENANCE.md` § tier 5):

| element | source | confidence it supports |
|---|---|---|
| lake shore, harbour cut, piers, sand tongue, the old southward channel | **Wright 1834** — a survey, and the master warping raster | `inferred`, ±20 m; a fair estimate is expected rather than avoided |
| the river through the central blocks; street and block geometry | **Thompson plat 1830** — 80-ft streets, 18-ft alleys, generated analytically from the module, not traced | `documented` for the module, `inferred` for the fit |
| the streams coming in, and where each one terminates | **Conley/Stelzer 1833** as primary guide, Wright as the check | `inferred`, named in the note |
| **bridge positions** | **Conley/Stelzer 1833** — it draws them in place | `inferred` |
| general cross-check on all of the above | an 1836 map — **not yet in `data/sources/`; find and record one first** | — |

The standing rule still holds where it earns its keep: nothing traced from a pictorial
sheet becomes an *outline*. A reconstruction tells you a bridge was here; it does not tell
you its plan. Position `inferred` with a note, geometry from the archetype.

**Do not let ±20 m stop the work.** The uncertainty is recorded per structure and shown in
the popup; that is the mechanism for handling it. Leaving the east half of the town empty
because the shore cannot be fixed to the metre is the more misleading of the two options.

**Scope, now measured off the sheet rather than guessed.** First readings are committed in
`data/traces/vectors/wright_1834_east.json`, derived by `tools/wright_px.py` from the same
fitted affine the datum is checked against:

| feature, from Wright 1834 | local E | local N |
|---|---|---|
| Fort Dearborn (label centre) | **+1152** | +221 |
| river mouth, south bank | +1180 | +272 |
| lake shore north of the harbour | **+1331 … +1365** | +330 … +735 |
| north pier, outer end | **+1544** | +178 |

So the box must reach about **E +1700**, not the +1500 I first estimated — the harbour
works run further out than the shore does. That gives a ~2.0 km × 0.7 km field; at the
current 2.5 m cell, ~224k samples (~450 KB int16) against today's 66k (132 KB). Well inside
the 25 MB publish budget, but worth a coarser cell east of the built blocks, where the
evidence does not support 2.5 m detail anyway.

Two things the first pass settled, and one it did not:

- **The Fort Dearborn position is cross-checked.** Wright puts it at E +1152, N +221; the
  modern successor landmark (Michigan Avenue bridge) independently gives E +1127, N +195.
  35 m apart, from methods sharing no input. That is what licenses `inferred`.
- **Wright labels the reservation, not the fort.** There is no palisade plan on this sheet,
  so the footprint has to come from elsewhere — Andreas, or the fort's own published plans.
  Do not trace an outline off the banner.
- **The sand bar and the old southward channel are now read** (second pass, same day). Three
  ink lines, nested west to east: the mainland bank of the decaying old channel, the bar's
  channel side, and the bar's lake-facing side. Checked for coherence rather than eyeballed
  — at every sampled northing the three nest in order and the bar comes out 71–171 m wide,
  narrowing to its southern hook, which is what a littoral spit should do. Uncertainty is
  recorded at 30 m rather than the shore's 25: these are ink lines over a wash, and the
  southern hook is the least certain shape in this quadrant.

**The coastline gate is therefore cleared.** Shore, harbour piers, sand bar and old channel
are all in `data/traces/vectors/wright_1834_east.json` in local ENU. What S2e still needs is
the *heightfield* work — extending the zone table east over ~2.0 km × 0.7 km, with the bar
as sand and the old channel as water — not more tracing.

Unblocks the **Fort Dearborn** and **Harbor works** parcels in S5, which cannot be placed
onto ground that does not exist. It also retires the aerial view's worst artefact: from
150 m up you currently see the ground simply end.

Parcels (parallel once S1 lands):

- **(a) Shoreline + river vectors** — **DONE 2026-08-10.** `tools/trace_shoreline.py` →
  `data/terrain/epochs/e1834_harbor_cut/shoreline.geojson`: the main stem from the box edge
  east, the 1834 cut between its piers, the old southward channel, the **sand bar as an
  island** (the water polygon's interior ring), and the mainland lake shore — 2 466 m of south
  shore, 1 568 m of north shore, a 1.5 km bar perimeter, all off the same Wright 1834 sheet
  through the same affine, ±20 m. Memo: `docs/RESEARCH/shoreline_harbor_1834.md`. Two boundary
  runs were found and dropped on purpose: the outer edge of the lake wash is where the
  draughtsman stopped washing, not a coast. **Measured, which changes the box:** the mainland
  shore reaches E +1257 and the bar's east edge E +1497, so the proposed +1500 clips the bar by
  3 m — **use E +1560**, inside the traced window's +1570. The two windows overlap by 80 m and
  agree there to 0.1–5.7 m, which is the check that the segmentation is reading the map rather
  than its own parameters. Not yet consumed by `terrain_gen.py`; it is the evidence, not the
  ground.
- **(b) Heightfield** — the 30-zone table in `docs/research/01-terrain-hydrology.md`, quantized ≤0.25 ft at 5–10 ft cells. One thing this parcel no longer has to budget for (2026-08-10, STATUS § 34): **prose in `terrain_spec.json` is out of the terrain's staleness hash**, so a zone's reasoning, caveat or citation can be written, argued and rewritten without a bake — and it must be, because an `inferred` ground claim with no stated reasoning is now an error rather than a warning. A number, an id or a confidence still stales the ground, so the spec's figures and the bake are still one slice. Z=0 at the 1835 lake surface. **Next slice**, and it needs a bake for the ground GLB, so record + mesh land together. Two things parcel (a) hands it: the bar is *land inside water*, so the signed-distance rule that builds the forks ground has to understand islands, not only banks; and no elevation for the bar exists in any source, so its height is a spec argument to be made in the open, not a number to pick.
- **(c) Hydrology** — the slough (public-square pond → past Lake & Dearborn → river at the foot of State), Frog Pond at Lake & LaSalle, the Wells Street marsh, the marshy river-shore strip.
- **(d) `terrain_gen.py`** — spec + vectors → terrain mesh + `heightfield.bin` for collision.

Reminder: piers and bridges are **structures with phases**, not terrain (see `docs/EPOCHS.md`).

## R1 — Renderer shell · *can start now, needs no datum*

Parcels: (a) shell + input-intent layer + walker; (b) confidence shader + provenance popup
against a hand-written test sidecar; (c) `tools/smoke.mjs`.

Build against synthetic geometry and flat ground. Contract in `docs/PLAN.md`. Mobile
(390×780) is a release gate from the first walkable commit — retrofitting touch into a 3D
walkthrough later is the expensive way to do it.

## R2 — Rendering program · **ACTIVE — owner reviewed and merged 2026-08-14 (PR #106)**

The phased plan for higher-fidelity rendering — Track 1 (`walk/` improved in place: light,
textures, AO, cascades, atmosphere, water, content), Track 2 (a second high-fidelity web
renderer at `walk-hd/`), Track 3 (a native-engine renderer) — lives in `docs/RENDERING.md`,
with per-phase gates, acceptance numbers and runner routing.

**The W track and G0 are buildable now. H and N stay gated** behind the `OWNER DECISION`
items in RENDERING §8, as do the open budget and distribution questions. The claimable
parcels are the **RENDERING lane** below; each one names its RENDERING phase, its file list,
its acceptance numbers and its runner.

**Everything lands on `dev`** (`docs/PIPELINE.md`). Production moves only when the owner
dispatches `chicago-4d-promote-to-prod.yml`.

## S3 — Milestone 0: the Sauganash, end to end

Definition of done in `docs/PLAN.md`. The record, the sources, and the dossier are already
written; what remains is the `frame_tavern` archetype, the first bake, and the walkable page
with a working confidence toggle.

Success is not "a building appears". Success is that a viewer can toggle the confidence view
and see exactly which parts of the Sauganash we can defend — the white two-story block and the
blue shutters solid, the invented footprint and the disputed gallery dithered.

## S9 — Streets, roads and paths · **VISIBLE EARTH LAYER + LIVE NAMES DONE 2026-08-11**

Asked for as "streets, roads, paths in accurate surface and elevations", then expanded to a
toggleable 1835/current-name readout. The first dated visible layer is now in: seventeen earth
travelways compiled into the scene index, draped on the heightfield, cut at water, cleared only
through the narrow travelled strip, drawn on the overview map and queried live for the street
underfoot or the next cross street ahead. The remaining work is to extend control on North Water
and the north-side grid, research any dated plank footwalks separately, and replace L79's visual
wear widths wherever a specification or depiction survives.

**Half of that sentence is committed data as of 2026-08-10.** `data/traces/street_control.json`
holds the module (80 ft streets, `inferred`, with the 66 ft dissent recorded beside it) and the
control table this project actually snaps to, each street carrying its axis and its modern
equivalent — and, since 2026-08-10, the rule that makes a control point re-derivable rather than
merely re-fetchable (`node_rule`: the nodes shared by the two named surface roadways, averaged,
with bikeways and stacked lower-level streets excluded). What is still missing for this parcel is
the plat's **block dimensions and extent** — that file holds only what the existing placements
used. See `docs/RESEARCH/street_module_1830.md`.

**And the module is measured rather than annotated, 2026-08-10** (STATUS § 42,
`docs/RESEARCH/street_module_1830.md` § 8, `data/traces/vectors/street_corridors_1834.json`).
Eight platted corridors read off BOTH 1834 sheets, 75.7-92.8 ft, none within 9 ft of 66: the
dissent is excluded and so is the reconciliation that it might be about different streets. Two
things this parcel inherits. First, a **measured block pitch** — seven consecutive corridor
spacings of 116.6-123.2 m, the 300 ft block plus one street — which is the beginning of the block
dimensions this section asks for, though not yet the plat's extent. Second, a **method problem to
solve before the E-W streets can be measured**: the N-S traverse reads Wright's lot lines, whose
depths are a platted street's width and whose lines run as far as a block face does, so a corridor
here has to be identified by something other than its width. Lake, Randolph, South Water and
Market are unmeasured until that exists.

**SOLVED 2026-08-11** (STATUS § 52, memo § 10). The three tests that failed are all readings
taken *across* a candidate at one place; the one that works turns ninety degrees and asks how far
a candidate is open ground **down its own centreline**, which a street is for a whole block and a
strip of lots never is. The threshold is derived from the module band (95 − 30 = 65 m) rather
than tuned. **Lake reads 79.4 ft and Randolph 81.5 ft** on Wright — both named by their committed
modern junctions to 0.9 m, not by counting — with one unnamed corridor a block further south at
86.5 ft; ten lot strips were rejected and none of the eight already-committed corridors was.
Three things this parcel inherits from it. **The E-W pitch is 134-136 m against 116.6-123.2 m the
other way**, so the blocks are NOT square and the 300 ft block that fits the N-S streets does not
describe them — that is the rest of the block dimensions this section asks for, and it comes off
two spacings on one sheet, so measure more before generating a grid from it. **The E-W widths
rest on one sheet**: Hathaway's N-S traverse commits nothing, so they have no cross-check. And
**South Water and Market are still unmeasured** — Market falls outside both traverses, and every
candidate north of Lake is bounded by a line that stops after 24-32 m. Both need a traverse
placed for them, not a looser filter.

**A caution for the generator, from the same slice.** The corridors drawn on these sheets run
about 5 ft wider than 80 ft on both, and that is paper stretch plus pen placement, not evidence
of a wider street. Generate the grid from the platted module (§ above) and snap it to control —
do not fit it to the traced corridor widths, which would bake 4% of paper distortion into the
town.

**Geometry comes from the Thompson module, generated, not traced.** The 1830 plat gives
80-ft streets and 18-ft alleys over the original 0.375 sq mi; Wright 1834 shows the same
grid extended, and both sheets carry ±20 m of georeferencing slop that tracing would bake
in as wobble. Generate the grid analytically from the module and snap it to control. A
street that is straight because the surveyor made it straight should not arrive bent
because we traced a folded sheet.

**"Accurate surface" in 1835 means earth, not gravel.** The first instinct — a crowned,
kerbed, gravelled or paved roadway — is wrong for the date, but the earlier wording here was
too broad in the opposite direction. The official 1891 municipal chronology records South
Water ordered pitched by April 1834 and graded for drainage that July, and calls South Water
and Lake the two principal early turnpiked and graded streets. It separately dates Canal,
Lake west to Desplaines and Randolph turnpiking to fall 1836; street planking begins in 1844,
general planking in 1849, limestone block in 1855, and macadam/cobble in 1856. On 1 July 1835
the defensible visual vocabulary is therefore **graded or thrown-up earth on the principal
routes, worn native soil on lesser streets, grassy margins, no gravel or hard paving**. Dated
plank footwalks remain a separate research parcel and are not silently supplied by the road.

**"Accurate elevations" means modest early grading is not the later Raising of Chicago.**
South Water's documented drainage order means "nothing had been graded" was false. What no
source supplies is the amount, cross-section, crown or fill profile, so this first layer does
not edit the heightfield or invent one: its vertices sample the existing ground exactly and sit
22 mm above it only to avoid depth fighting. The walk camera now locks to that same bilinear
surface each frame instead of easing behind it on rises and falls. Where a street reaches water,
the ribbon stops; a crossing is content to research, not a rendering artefact to flatten away.

## S5a — Fort Dearborn · **DONE 2026-08-11**

Kevin's call, and the dependency he named is satisfied: the coastline, the sand bar and the
harbour works are read, so there is ground to put it on once S2e builds the heightfield.

- **Position is settled and cross-checked**: local E +1152, N +221, two independent methods
  35 m apart (see S2e).
- **What it *was* on 1835-07-01 is SETTLED, 2026-08-10** — `docs/RESEARCH/fort_dearborn.md`.
  An **occupied United States Army post, commanded by Major John Greene**, who held it from
  18 December 1833 until 16 September 1835. Three separately written accounts agree the fort
  was garrisoned through 1835 and the post surgeon's prescription book has an entry dated
  15 March 1835. The soldiers left on 29 December 1836 and the post was not given up until
  June or July 1837 — which is how Andreas manages to give 1836 in one chapter and
  10 May 1837 in another. Nothing here goes to `data/exclusions.json`; the fort was here.
- **The footprint is still NOT sourced, but the search is narrowed to three candidates.**
  Wright *labels* the reservation and draws no plan; neither does Hathaway. The best lead is
  a survey, not a picture: the War Department's agent, reporting on 21 November 1840, names
  the platted lots of the **Fort-Dearborn Addition (1839)** that were withheld from sale
  because they covered "the fortress of Fort Dearborn *within the pickets*". Find that plat,
  fit it (its streets survive in the modern grid) and read the withheld lots. Second: **Henry
  Hart's 1853 survey of the fort**, named but not yet located. Third: a War Department plan
  of the rebuilt fort, never looked for. Ruled out with reasons in the memo § 7 — do not
  re-run them. Still: do not infer a stockade outline from a banner.
- **Four constraints exist now that did not.** Gurdon S. Hubbard, correcting the *Wau-Bun*
  view in 1881, states that the enclosure ran "nearly north and south, east and west"; that
  the north picket line stood nowhere more than 80 ft from the water and 50-60 ft opposite
  the north gate; that the ground at the fort was "not over eight feet above the River at its
  lowest stage"; and that the north and south gates were on one sight line. The first two are
  usable against the traced 1834 bank. **The third is a finding about the terrain**: an 8 ft
  platform is taller than any landform in the modelled box (total relief 4.30 ft), so it
  belongs to S2e parcel (b) as much as to this parcel.
- It is a **complex, not a building**: S5's Fort Dearborn parcel already itemises palisade,
  blockhouse, bastion, magazine, quarters, barracks, sutler, hospital, parade and gardens.
  Expect several records and several bakes, not one. The interior arrangement is now attested
  element by element (memo § 5) and the one open disagreement is whether there were two
  bastions or one.
- **A caution the memo pays for.** Three enclosures get confused in this literature and only
  one is the 1835 fort: the 1816 stockade, the post-army compound of 1850 (pickets gone, a
  whitewashed board fence, "say 400 feet"), and the 53¼-acre reservation. The 400 ft figure
  is the middle one and must not be read as a palisade.

**How both gates were cleared, and what it cost.**

- **The plan source exists and it is a survey.** *Map of the Mouth of Chicago River*, F. Harrison
  Jr., Ass't U.S. Civil Engineer, for the proposed harbour improvements, approved by William
  Howard 24 February 1830 — reproduced in **Andreas vol. 1 p. 113** and listed in that volume's
  own table of maps as "Fort Dearborn in 1830-32". It draws the fort in plan and names the ground
  round it (Garden for the Garrison, Cultivated Field, Big Barn with Cupola, Wash house, Well,
  Shop, Fort Cemetery, the Ferry). Recorded as `harrison_1830_river_mouth`, `asset_use: geometry`,
  tier 2 — because the plate says on its face that it carries "additions and changes … suggested
  by the Memory of Early Settlers", so it is a period survey plus fifty-year-old recollection
  mixed on one plate. **Nothing taken from it is graded `documented`.**
- **The plate has no scale bar, and that is the whole difficulty.** The scale is derived by
  setting the drawn north range equal to the commandant's quarters at "about 25 x 50 ft" from the
  1855 photograph key — 1.10 ft/px — and checked twice on the same plate (drawn aspect 1.9:1
  against a stated 2.0:1; parade width 71 ft against a stated 80 ft). **±20 %** on every derived
  dimension, on top of the datum's ±20 m. The stockade comes out about **53 m (174 ft) square**.
  **No dimension of the 1816 fort exists in the literature**: Quaife's monograph prints
  Whistler's measured 1808 draught of the FIRST fort and states none for the second anywhere.
- **The arrangement is much better evidence than the scale**, and it is what licenses `inferred`
  rather than `conjectural` for the positions: an 1830 engineer's plan and Gurdon Hubbard's 1827
  walk round the inside agree building by building, on the same sides of the same two gates.
- **The garrison is settled.** Held continuously **June 1832 → 29 December 1836**; Andreas
  brackets the scene date and the drloihjournal chronology fills the bracket with **Maj. John
  Greene, 5th Infantry**. Two companies in 1833; **no strength figure for mid-1835 was found and
  none is claimed**. The fort is modelled maintained, with its gates shut.
- **Fourteen records, two new archetypes, fourteen bakes, ~17,000 triangles.** `palisade`
  (picket stockade with named gates and corner works; worm rail fence for the garden) and
  `fort_structure` (eleven kinds — quarters, barracks, blockhouse, magazine, store, guard,
  sutler, artillery, parade, root house, tower). The lighthouse of 1832 came with them.
- **Five exclusions, four of them wrong-fort findings**: the first fort itself, the sally-port,
  the three artillery pieces and the fifty invalids, the 1850s board fence and turnstile — plus
  **there is no hospital building**, only the fort *becoming* a general hospital in the 1832
  cholera. Three corrections to `docs/research/04-structures-south.md` are recorded in
  `docs/RESEARCH/fort_dearborn.md` § 6, and one to § 2 in
  `docs/RESEARCH/chicago_lighthouse_1832.md`.
- **It stood on nothing for about four hours.** The complex is 832 m east of where the
  heightfield used to stop, and while it was there it exposed a real blind spot in the
  ground-contact gate — the clamped edge made a fort in the void report a perfect landing. See
  STATUS § "Known weaknesses" 0a. **S2e parcel (b) then landed the same day**: the field reaches
  E +1700, twelve of the fourteen structures land, and the lighthouse and the root house — both
  `conjectural` in position — moved off the channel and onto the bank top now that there is a
  surface to be wrong about. The two that remain off the ground are the stockade and the
  commandant's quarters, whose north sides cross the top of the river bank by 1.40 m and 0.46 m,
  because **no cut, fill, revetment or foundation is modelled anywhere in this project**. L46.

**The gates were open, and `p4_0` never drew the corner works it was said to (T-0095,
2026-08-24).** Two findings, one measured off the sheet and one off the shipped mesh —
`docs/RESEARCH/fort_dearborn_gate_and_corner_works.md`, held by
`tools/measure_fort_works_plate.py` and `tools/measure_fort_gates.py`.

- **The plate raises no work at either angle it draws.** It raises exactly two roofed,
  lanterned, log-faced works and both stand over the MIDDLE of the wall, at **0.435 and
  0.521** of the drawn run; a corner work stands at 0.000 or 1.000. The one angle it shows
  unoccluded is the north-east and it is drawn plain — which is what the record says of that
  angle. The north-west angle, the one the record does put a work at, is behind the tree
  outside the walls. **Nothing was massed at the angles**, and the log-faced work over the
  gate was not built either: the sheet already carries a certified FIRST-fort feature (the
  flagstaff, `data/exclusions.json`) and two roofed lanterned log towers is that fort's own
  signature in everything but position. Same failure as T-0094, one day apart, on the same
  sheet: the plate read by eye.
- **Both documented gates stood a quarter open.** One leaf of each pair was placed from a
  midpoint that collapsed onto its own jamb, so **0.90 m of the 3.6 m gateway was daylight
  straight through the wall** and 0.90 m of leaf lay across the pickets outside the frame —
  in the committed GLB, so in the bytes a visitor downloaded. Four lines in `palisade.py`,
  one asset rebaked (`fort_dearborn_palisade__picket_1816`). The gate that holds it reads the
  shipped mesh rather than re-deriving the placement, because the derivation was the fault.
- **The south-west blockhouse already read above the curtain** and now has a number: 9.48 m
  of building over a 3.80 m curtain, from its own instance bounds in the scene.

**Still open in this quadrant, in the order the evidence supports:** the named ground on the 1830
plan that is drawn as a symbol and a label and nothing else (Big Barn with Cupola, Wash house,
Well, Shop, Out Buildings, U.S. Factor's House, Cultivated Field, the Ferry — the Fort Cemetery
deliberately left alone); the drill ground south of the pickets, which Kinzie attests and does not
measure; the garden's planting, which is documented and needs a **cultivated flora zone** rather
than a structure; and a keeper's dwelling beside the lighthouse, which is plausible and
unattested.


## S4 — Archetype generators

One parcel per archetype, each with a golden-parameter GLB and a reference shot:

`frame_tavern` · `frame_storefront` · `frame_dwelling` · `log_dwelling` · `institutional` ·
`fort_structure` · `outbuilding` · `plank_walk` · `bridge_timber` · `pier_crib` · `palisade`

Balloon-frame logic (stud spacing, sheathing, proportions) is a first-class requirement, not a
detail: 1833–35 Chicago is where balloon framing was invented, and it is the first thing a
knowledgeable viewer checks.

**`frame_dwelling` DONE 2026-08-11** — and it is the one that unblocks houses. Until it existed
every frame record had to be a two-storey public house or a log cabin, so the dataset held
taverns, stores and a bridge and not one dwelling. It takes `stories` 1, 1.5 or 2 (default the
story-and-a-half, knee wall and gable-end attic window, which is the form of these years); reads
the rear **ell off the footprint polygon** rather than off invented dimensions, so an L-shaped
plan is built as an L and `GROUND_CONTACT: perimeter` is literally true of the mesh; builds a
stoop or a small roofed porch, never the tavern's gallery; and makes `construction` the first
attribute in this project that MOVES A VERTEX rather than sitting unread in the sidecar — the
stud module (16 in balloon, 24 in braced) places every opening, the clapboard butt joints fall on
stud lines, and a braced frame gets the girt band at its upper floor that a balloon frame has no
line for. `plan` + `bays` are **L23's own stated resolution** — a bay count derived from frontage
and a rhythm that comes from the room arrangement — so the default front is asymmetric and
unevenly spaced rather than the Sauganash's five bays worn by every building.

Still open on it, and worth a record's attention before the first house lands: no dormer (the
half storey is lit only from the gable ends), no foundation or cellar, no muntins in the sash,
and the stoop projects outside the recorded footprint. All four are in the report attached to
the parcel and belong in docs/LIBERTIES.md the day a `frame_dwelling` record does.

**`outbuilding` DONE 2026-08-11** — stables, sheds, cribs, smokehouses, privies. Built as a
FAMILY rather than a shape, because a single set of proportions that flatters the middle of the
range breaks both ends: five golden variants span a 1.25 m privy to a 13 m hotel stable, and
`GROUND_CONTACT: perimeter` is verified on all five rather than on one. Deliberate absences carry
as much of the design as the parameters — `stories` is NOT consumed, because two storeys of wall on
a secondary building is a claim and `wall_height_m` is the honest way to make it; `construction`
names log/plank/light_frame rather than balloon/braced, because nothing behind the boards of a shed
is visible at this LOD and no source describes the framing of any outbuilding here, so the
vocabulary names only what a viewer can see.

Two things it hands upward. **L10 should be NARROWED, not resolved**: this archetype can build the
Western Hotel's stable but not its wagon yard, and a yard is an enclosure — a fence line, two
gateways, trodden ground — so building it out of an outbuilding would be calling a fence a
building. The same gap swallows the estray pen and Clybourn's stockyard, and an `enclosure`
archetype is now a named want. And **registering any archetype restales every committed GLB**:
`mesh_inputs._code_shas` hashes `build.py`'s bytes for every archetype, and `build.py` carries the
`ARCHETYPES` registration table, so adding a row to it changes the hash of buildings it never
touched. Two parcels hit this independently and both verified the re-bake is byte-identical. The
fix is to split the export path out of `build.py` so the registration table stops being a mesh
input; until then one batched re-bake clears it.

**`frame_storefront` DONE 2026-08-11** — 23 consumed attributes, all 13 live storefront records
resolving with no `geometry:` declaration owed. It is the archetype where `construction` finally
separates from `frame_tavern`: balloon frame gets a thin 4 in corner board, no girt and a 16 in
module; braced frame gets a 6 in corner post and a girt line at the second floor. `cladding` is
read rather than ignored, which is the L22 defect not repeated. And the unfinished state is
buildable — open studwork over 9 in board sheathing on the loading gable, attested in kind by
Andreas for the *Chicago Democrat*'s own building at South Water and Clark, "unfinished at the
time" in November 1833. Never a default.

### Three bugs it found in neighbouring code — NOT fixed, and the third is a gate hole

1. **`MeshBuilder.add_gable_roof` fills each gable end with a solid triangle 0.25 m OUTBOARD of
   the wall.** So anything drawn on a gable at the wall plane is *inside* the roof and invisible.
   `log_dwelling._loft_opening` does exactly this: its loft openings are not in the committed
   reference image and never were. A generator that silently swallows its own output is the worst
   kind of bug here, because the reference render is what a reviewer checks.
2. **`log_dwelling`'s baked GLB has `y_min = -0.065`** while declaring `GROUND_CONTACT:
   perimeter` — an opening surround below grade. The same bug was found and clamped inside
   `frame_storefront`; this one is live in the committed asset, so a record is making a false
   ground-contact claim right now.
3. **`frame_tavern` declares `construction` and `gallery` in CONSUMED and builds neither** —
   and `test_consumed_attributes_actually_reach_the_parameters` PASSES, because it only requires
   the resolved *parameters* to move, not the geometry. Today every record says `gallery: false`,
   so the falsy rule hides it; **the first record that says `true` gets excused from a
   `geometry:` declaration for a gallery that is never built.** That is the exact failure the
   CONSUMED contract exists to prevent, sitting inside the test that is supposed to enforce it.
   Fixing it means the test has to compare vertices, not parameters.

## S5 — Structure records

**Queued first, and it is a regrade rather than an addition: 21 `documented` values rest on
later scholarship alone** (2026-08-10, STATUS § 43). The evidence ladder has a gate now, and its
fourth rule is a counted warning rather than an error: a `documented` value with no source at
tier 3 or better — no period document, no eyewitness recollection, no compilation from pioneer
testimony — is either an over-graded value or an under-tiered source, and only reading the page
settles which.

**The source half is DONE 2026-08-10 and it was fifteen of the twenty-one** (STATUS § 44,
`docs/RESEARCH/evidence_tiers_chicagology.md`). `prefire127`, `prefire273` and `prefire278` were
fetched and read in full; all three transcribe near-primary recollection — the *Inter Ocean*
old-settler interviews of 1 and 22 July 1883, and the *Chicago Magazine* of 15 May 1857 built on
Hubbard's own account — and all three were graded 4. They are 2, no value moved, no mesh went
stale, and the count reads **six**. The judgement is also a declaration now rather than a typed
number: a record dating its own retrieval and claiming a testimony rung must declare
`transcribes`, and its tier is the best rung it declares.

**The four sharp ones are what is left, and they are the expensive half**: `sauganash_hotel`
`form.stories` and `form.construction`, `miller_house` `form.frame_addition_stories` and
`wolf_point_tavern` `form.sign` are supported by nothing but the two `drloih` blog compilations,
whose own source records say *never as sole evidence*. Re-tiering cannot touch them — the pages
are unfootnoted, mutually contradictory and unarchived — so this is a regrade of the VALUE, and
a confidence is a mesh input: the slice stales those GLBs and lands with a bake. Behind it, the
machine-readable half — a `never_sole_evidence` flag on a source record, which turns those four
into errors — stays deliberately behind the regrade, because a gate that fails the committed
dataset on the day it lands is a gate that gets switched off.

**The other two are outside the buildings**: ground `surface_materials.south_division`
(`chicago_architecture_history_115`) and ground `water` (`wikipedia_chicago_river`). ~~The first
of those has not been opened.~~ **Both are read and both are over-graded VALUES** — `water` on
2026-08-11 (§ 46, `docs/RESEARCH/swearingen_1803.md`) and the soil profile the same day
(STATUS § 51, `docs/RESEARCH/surface_materials_south_division.md`). The soil page is a 2022 essay
that is its own document, correctly at rung 4, and it prints **no footnote, endnote or reference
anywhere in it**; the one witness on it — John Mills Van Osdel, block-quoted with no publication,
date or page, and unmentioned by this project's own dossier — attests the ORDER of the strata and
the drainage failure and gives **no black loam and not one thickness**, so the three figures in
the claim have nobody behind them. `documented` → `inferred`, and it lands with the bake.

**The three pages that looked like the same case were opened 2026-08-11** (STATUS § 45,
`docs/RESEARCH/evidence_tiers_round_two.md`), and two of them were. `prefire062` reprints
**Andreas**, who quotes the *Chicago American* of 9 July **1836** (not 1835) for the Lake and
La Salle frog pond — tier 3, on Andreas and deliberately not on the newspaper nobody here has
opened. `prefire276` reprints the *Chicago Magazine* of 15 May 1857, the same document and the
same reading as `prefire273` — tier 2, with the 1856 *Tribune* notice beside it left undeclared
because no claim here rests on it. Neither page is cited by anything today, so the ladder count
stays at six; both are queued research (S2 parcel (c)'s pond, and the fort) that can now be
graded honestly when it is written.

**`wikipedia_chicago_river` was NOT the case, and that is the finding with a consequence.** It
reprints nothing — one sentence of encyclopedia prose paraphrasing Swearingen with a footnote to
**Quaife 1913, pp. 373-377**, which is the primary printing the record has asked for since it was
written. Two things come off it:

| queued | what it costs |
|---|---|
| ~~Fetch Quaife 1913 pp. 373-377 and record Swearingen's 1803 soundings at their own rung~~ | **DONE 2026-08-11** — `quaife_1913_swearingen`, the dataset's first tier-1 written eyewitness document; memo `docs/RESEARCH/swearingen_1803.md`. And **the price above was wrong**: `generators/terrain_inputs.py` strips `sources` from the terrain hash along with the prose, so citing it from `terrain_spec.json` cost nothing and was done in the same slice. A `confidence` is the mesh input, not a citation |
| **ground `water`: `documented` → `inferred`** — the flat surface rests on an unfootnoted encyclopedia sentence about sluggish flow, not on Swearingen, who gives no gradient and measures 1.2 miles downstream | a confidence is a mesh input: it stales the ground and lands with its Blender bake, exactly like the four `drloih` values. **Better argued as of 2026-08-11 and unchanged in direction**: reading Swearingen made the case stronger rather than rescuing it, because his 'dead water' is attributed in the same clause to a mouth stopped by sand — the `e1830_natural` condition the 1834 cut removed. He is deliberately NOT cited on the water plane; the block's note says so where a visitor reads it |

That is the **first of the six warnings settled in the over-graded direction** — the source is
correctly tiered and the value is not.

**And the primary printing arrived 2026-08-11, which cost the encyclopedia one of its two bank
figures** (STATUS § 46, `docs/RESEARCH/swearingen_1803.md`). Quaife's Appendix I is now
`quaife_1913_swearingen` at tier 1, read from two Internet Archive scans that agree character
for character. Wikipedia's *"6 ft on the north"* is nowhere in the journal: Swearingen gives no
north-bank height, only a bounded difference flagged as made *by appearances*, and 6 is what a
later writer got by subtracting the maximum from 8. What the paraphrase dropped matters more —
*"the banks above are quite low"* is the only sentence in the passage about the reach this
project models, and it is attached to the spec's `bank` block now, which cited nothing before.
Fourth citation found misdescribing its own page, and the first found by opening the document
rather than the host. ~~Six pages at tier 4 or weaker still declare nothing
(`chicago_temple_history`, `chicagology_first_post_office`, `chicagology_lastwardance`,
`chicagology_prefire274`, `drloih_hotels`, `drloih_wolf_point`), counted by the validator every
run, and the two `drloih` pages are not solvable this way.~~

**The four that could be opened were opened 2026-08-11, and the count reads two** (STATUS § 47,
`docs/RESEARCH/evidence_tiers_round_three.md`). `chicagology_lastwardance` is the *Chicago
Tribune* of 14 August 1910 printing **John Dean Caton's own written recollection** — an
identified eyewitness, not the "later compilation of recollections" the record claimed — and is
rung 2. `chicagology_prefire274` is *Chicago Magazine*, March 1857, the installment before
`prefire276`, and is the first source here graded **by which part of it you stand on**: rung 2
for the landform this project cites, no better than 3 for its 1803-1812 fort narrative, which
nothing cites. `chicagology_first_post_office` was read and **left at 4** — Currey 1922 naming
no authority for the post-office facts — which is what this section meant by *unread rather than
wrong*. `chicago_temple_history` reprints nothing and says so in `carries_no_document`; its
missing `archived_url` is filled from a 2026-06-05 snapshot verified against both quotations,
one standing warning gone.

**The finding is on the post-office page and it touches S9.** The 66 ft street module — the
dissent against the 80 ft every platted placement is offset from — is *not part of Currey's
article*: it interrupts his chronology, its subject is a survey in an article about buildings,
and it is the one paragraph naming no authority while writing "downstate Randolph County". It is
undeclared, off the ladder, and `data/traces/street_control.json` no longer says "Currey states".
No number moves — the figure was already excluded by measurement — but the dissent is now a
sourceless website sentence rather than a named historian, which is a different thing for the
streets parcel to weigh.

**What is left of this thread is not research, and as of 2026-08-11 that is true of all six.**
Only `drloih_hotels` and `drloih_wolf_point` still declare nothing, and this method does not reach
them: the pages are unfootnoted, mutually contradictory and unarchived, and their four values need
the VALUE regraded, which is a mesh input. **That slice, ground `water` and ground
`surface_materials.south_division` are one bake** — five values, six warnings, take them together
on a runner with Blender. Every page behind the six has now been opened and the verdict on every
one of them is the same: the source is tiered correctly and the value is graded too high.


**The repair queue that came before it, all of it DONE — three attributes that were recorded
and unbuilt.** Found by the omission gate on 2026-08-10 and admitted meanwhile by L20 and L21.

| record | attribute | what the archetype reads | effect |
|---|---|---|---|
| ~~`wolf_point_tavern`~~ | ~~`frame_extension`~~ | `frame_addition` | **DONE 2026-08-10** — renamed, dimensioned and re-baked in one slice |
| ~~`wolf_point_tavern`~~ | ~~`signage`~~ | `sign` | **DONE 2026-08-10** — the board hangs on the river front; the wolf is not drawn (L25) |
| ~~`miller_house`~~ | ~~`chimneys: 2`~~ | `chimney` (a boolean) | **DONE 2026-08-10** — the count is a parameter of both archetypes; the second stack stands on the frame range |

**The one repair found by reading rather than by a gate is DONE** (2026-08-10, STATUS § 23 → § 24):

| record | attribute | what the evidence says | effect |
|---|---|---|---|
| ~~`north_branch_bridge`~~ | ~~`pier_spacing_m`~~ (15 cribs at the archetype default) | **two "bents" of four heavy logs resting on the bottom** | **DONE** — `pier_count: 2` replaces the spacing in record and archetype; L29 resolved, L31 new |
| ~~`north_branch_bridge`~~ | ~~`pier_kind: crib`~~ | the settlers' own word is **bents** — and Cleaver signed it | **DONE** — `bent` beside `crib` and `pile`; four heavy logs under a cap |
| ~~`north_branch_bridge`~~ | ~~`clearance_m`~~ (`inferred`, page not found) | **"about six feet above the water, so that teams passed under them on the ice freely"** | **DONE** — `documented` on `old_settlers_bridges_1883`; the deck and stringers come out of dithering |
| ~~`north_branch_bridge`~~ | ~~deck~~ (archetype's, unstated) | **"puncheons or split logs were laid for a floor"** | **DONE** — `deck_kind: puncheon`, a value the generator reads |

All four were mesh inputs, so the record, the archetype change and the bake landed as one slice —
the same coupling the note below describes, arriving from a new direction. The evidence is a
signed 1883 statement by four men who used the bridge, printed as a footnote at Andreas
pp. 631-632 and missed by the full-text index; see `docs/RESEARCH/north_branch_bridge.md` § 6.

**The lesson is about the parameter, not the number.** `bridge_timber` divided a span by a
spacing, so it could only ever produce a colonnade; no source will ever state a spacing, and what
a witness remembers is a count and a form. Setting 4.5 m to 23.94 m would have fixed this bridge
and left the next one to be found by the same accident. Worth asking of any archetype whose
defaults are about to be overridden: is it asking for the kind of number a source could contain?
What the repair could not settle is where along the span the two bents stood — the letter locates
them by depth, in a river whose bed this project does not model — so they sit at the third points
and **L31** admits it, together with the splices in three 23.9 m stringer runs that no source
places.

Each of the earlier repairs was a small data edit plus a re-bake, so **record and geometry landed in one slice** — the
same coupling the note below describes. All three are done.

**The list refills itself, which is the point of the gate.** Making the chimney count real
required placing Miller's second stack, and placing it exposed the next repair of exactly the
same kind:

| record | attribute | what the archetype does | effect |
|---|---|---|---|
| ~~`miller_house`~~ | ~~`frame_addition` (documented, undimensioned)~~ | picks side, width, depth and storey count from its defaults | **DONE 2026-08-10** — the record states all five, the two invented ones are L27, re-baked in the slice |

That was L24's defect one building over, and it came with a second one underneath it that was
not on any list. **`stories: 2, documented` was the frame range's and `log_dwelling` reads it as
the log core's**, so the documented claim was spent on the cabin, the range took a 4.7 m default,
and the model stood a two-storey log cabin behind a shorter frame block — the composition
inverted. The record now separates them: `frame_addition_stories: 2` documented, `stories: 1`
inferred for the cabin, `frame_addition_height_m: 5.2` and `wall_height_m: 2.6`. Two of the four
queued attributes turned out to be attested rather than invented — the side, because the source
says *fronting the river*, and the storey count — and only the width and depth are guesses, taken
off the record's own footprint limb (9 × 6 m) rather than picked afresh. L13 moves to Resolved,
L27 is new. **The repair queue is empty and nothing refilled it: S5 is additions again.**

The lesson worth carrying past this table: the omission gate found three misspellings and the
fourth fault was not one. `stories` was a name the archetype *found* and read as being about the
other half of a two-part building — which is invisible to a spelling check and to
`test_consumed_attributes_actually_reach_the_parameters`, since the value does move geometry,
just the wrong geometry. Any archetype attribute that means different things to different
elements of a composite building is the same trap; `wall_height_m` was the second one in this
record.

**The Wolf Point pair landed together, which is the shape** (2026-08-10). Both renames, the four
attributes the frame bay needed, the re-bake, the publish and the liberties moved in one PR. Two
things are worth carrying forward. First, a rename is never only a rename: `frame_addition: true`
alone would have let the archetype choose the bay's side, width, depth and storey count from its
defaults, so a documented feature would have arrived at an invented size with nothing admitting
it — the record now states all four and L24 admits the three that are conjectural. Second, the
staleness gate did exactly what it was written for: the record edit turned the tavern's GLB STALE
on the spot and the commit could not go green until the bake landed with it.

**And the count of a thing is not the thing** (2026-08-10). `chimneys` was stated by every record
and read by neither archetype: `frame_tavern` built two stacks and `log_dwelling` built one,
whatever the number said. Both take the count now, and the frame pair keeps its exact positions so
that parameterising a number did not move a building whose count was already right. The
`log_dwelling` half was the `frame_extension`/`signage` failure a third time — the parameter was
`chimney` and no record has ever contained that word — so the class has a check now rather than
another discoverer: `test_consumed_attributes_actually_reach_the_parameters` perturbs every stated
value an archetype declares it consumes and requires the resolved parameters to change. What the
count still does not carry is where a stack stood, how big it was or what it was made of; nothing
in the dataset records that for any building, and L26 is where it is admitted.

**You cannot land half of one any more** (2026-08-10). `check.sh` recomputes each committed GLB's
inputs and fails when the record and the mesh disagree. The working shape: prepare the record on
a branch, let the bake workflow run against that branch (it triggers on any push under
`chicago/4d/data/**` or `generators/**`), take its baked assets onto the same branch, and merge
one PR carrying both. See `generators/mesh_inputs.py` for what counts as an input and what
deliberately does not.

**The first bridge landed 2026-08-10, and it is the first record whose size is evidence.** The
North Branch crossing at Kinzie Street — Chicago's first bridge, 1832-1839 — is a record, a bake
and a published mesh on the `bridge_timber` archetype, which had been written and never used.
Three things worth carrying into the rest of S5:

- **A crossing can be measured where a building cannot.** Its 71.83 m span is the distance
  between the two traced 1834 waterlines along the Kinzie alignment, read off `river.geojson`,
  and its 3.048 m width is Cleaver's "ten feet wide" — so the footprint is derived rather than a
  placeholder. Anything that meets the traced water (the piers, the wharves, the raft bridge) can
  be dimensioned the same way. Anything that does not still gets a placeholder.
- **The invention moved from the outline to the interior.** A building's placeholder is its
  footprint; this bridge's is the fifteen cribs the archetype puts under a span nobody described
  the middle of (L29). Same class of fault, different place to look for it.
- **The contract's water anchor is implemented now** — `VERTICAL_ANCHOR` on the archetype,
  `placement.vertical_anchor` in the sidecar, a literal `y = 0` in the renderer, and a smoke
  assertion written as the difference between the two anchors. The next structure over water
  needs no renderer work. **What is still missing is walking on it**: the walker follows the
  terrain, so the deck is scenery. That is its own unit and it is recorded in STATUS, not faked.

**The first building whose footprint is evidence landed 2026-08-10**, and it is an ADDITION
rather than a repair — the first since the queue emptied. `hogan_store`, the log store at the
west end of the Lake Street block where the United States opened a post office at Chicago on
31 March 1831, carries a `documented` footprint: Andreas states its size twice, twenty by
forty-five feet, both times as an aside about how little room the town's mail needed. Three
things worth carrying into the rest of S5:

- **A building can be measured after all, when the source is describing something else.** The
  bridge's numbers came from a witness describing the bridge. This one's came from a writer
  making a point about the *post office's* cramped quarters. Dimensions in this literature hide
  inside arguments about something other than the building, so search the prose around an
  institution rather than the entry for a structure.
- **Reading a page corrected the dossier's chronology by twenty months.** `docs/research/`
  § 4 dated the post office's move to Franklin and South Water from the day Hogan became
  postmaster (2 Nov 1832); Andreas says twice it moved about July 1834. The dossier's summary
  tables are finding aids, and a table row is not the page. See `docs/RESEARCH/hogan_store.md`
  § 3.
- **The first record with nothing conjectural in it.** Its gaps are gaps in the sources'
  precision rather than filled holes, so it needs no liberty — which finally exercises the
  provenance popup's empty "What we made up here" state that STATUS § 11 recorded as unexercised
  by real data. Its weak point is instead its **survival**: attested to about July 1834 and
  placed in a scene eleven months later on a continuity argument, stated as such on the record.

Per-cluster parcels, each one file per structure so parallel agents never collide:

| parcel | contents |
|---|---|
| Wolf Point west bank | Wolf Tavern (painted wolf sign), Green Tree, Western Hotel, James Kinzie house, R. A. Kinzie store |
| North bank | Miller House, Miller tannery, Cobweb Castle, Walker's meeting house, Steamboat Hotel, Lake House (under construction) |
| South Water blocks A–G | the block-by-block sketch in `docs/research/04-structures-south.md` is the work order. ~~Hogan's store / the first post office, Lake at South Water~~ **DONE 2026-08-10**. Next on this block: Philo Carpenter's log drug store, "immediately adjacent to the Sauganash's public bar", which has no dimensions at all; and the **Franklin Street post office**, the building actually holding the mail on the scene date, of which nothing but a street junction is attested — see `docs/RESEARCH/hogan_store.md` § 4 before building it |
| Lake Street | Tremont House I, Mansion House, Exchange Coffee House, St. Mary's, First Presbyterian, Thomas Church store |
| Civic square | estray pen, log jail, courthouse (under construction, month unfixed) |
| Fort Dearborn | palisade, blockhouse, bastion, magazine, quarters, barracks, sutler, hospital, parade, gardens |
| Harbor works | north pier, south pier, the cut, the lighthouse, wharves |
| Crossings | ~~North Branch bridge~~ **DONE 2026-08-10** · South Branch raft bridge (floating — needs its own archetype, see `bridge_timber_params`) · Dearborn Street drawbridge (200 ft with a 60-ft draw, a different animal and outside the current terrain box) |

## S6 — Flora and fauna

**And the ground's surface, which is now a declared omission rather than an unstated one**
(2026-08-10, L35): the terrain spec grades five surface materials — the divisions' loam over
quicksand over blue clay, the marsh strip's peat and sedge, the channel's silt — and the mesh is
one earth colour. A per-zone surface treatment driven by those entries retires L35; the palette
has to be argued from the sources rather than picked, which is the same trap the street surface
is (§ S9).

Per-zone parcels from the dossiers: 10 flora zones, 7 fauna zones. Honor the July phenology
rules — big bluestem is vegetative in July, cordgrass is the tall flowering element, ramps are
leafless scapes. Negative findings (no ring-billed gulls, no beaver, no periodical cicadas) go
into the data as `absent` entries with citations, so nobody re-adds them later.

### S6a — the eye-height sward · **ROUND 1 IN 2026-08-10**

`renderers/web/js/flora.js` draws the graminoid matrix, the forb layer, the emergents and the
low shrubs from `data/flora/`, mounted in `main.js` beside `trees.js`. Blade geometry runs within
about 7.6 m and camera-facing clump cards to 27 m; beyond them the actual terrain's procedural
prairie texture carries unresolved colour. Placement is a deterministic world lattice
re-centred on the walker and culled to a 62° cone, so nothing swims underfoot and nothing is
paid for behind your head. Heights, greens, cover, phenology and per-plant confidence all come
from the records; the tuft density and far-texture compression are liberties (L32, L80).

**Corrected after the 2026-08-11 real-device review:** the former L33 far-field canopy was a
solid surface at plant-top height. It looked like a second terrain layer, hid foundations and
roots, and could be walked underneath. It was removed rather than making the walker and every
building stand on false plant-top topography. Terrain is now the sole physical and visible
surface; all detailed flora and structures share its sampler. L80 records the replacement.

**Judged against `WORK/bar`** — two verified photographs of surviving Illinois tallgrass in
mid-July (a Chicago-region remnant, 29 July 2021; a DuPage restoration, 24 July 2018) and an
October negative control. Where round 1 stands, measured on the primary shot rather than
asserted:

| tell | reference | round 1 |
|---|---|---|
| the ground is hidden at eye height | invisible | hidden past ~3 m, patchy in the nearest 2 m |
| several heights, several greens | 4-5 layers | 5 species heights, two greens each, per record |
| July hue (green, not tawny) | R/G 0.76-0.93 | **0.73-0.80** |
| local contrast (p90 − p10 luminance) | **141-212** | **101 near, 83 mid, 46 far** |
| no flowering bluestem/Indian grass/switchgrass | none | none, structurally |

### S6a next — the open work, in the order it is worth doing

**Reordered 2026-08-10 after a three-critic blind round on one identical shot set.** Every item
below carries a measured target and the definition it is measured with, because two rounds of
this work were spent chasing numbers that either did not reproduce or did not exist in the
reference. See STATUS.md § "Known weaknesses" 00 for the full measurements. The old list's
items 1–3 were not wrong; they were aimed at the near field, and the blind test is being lost
in the **mid** field.

1. **Restore distant vegetation without restoring a second surface.** The removed L33 sheet
   cannot return: any impostor or sparse far geometry must be rooted on the heightfield, remain
   visibly porous, and pass the same root/building/walker surface checks as the detailed field.
   The terrain texture is the honest current fallback beyond 27 m.
2. **Give the far terrain texture grain at fragment scale.** Keep it on the physical terrain,
   with enough irregular contrast to suggest unresolved vegetation without asserting a second
   height or species silhouette. Re-measure the old high-pass target against the corrected
   renderer before reusing it; the prior 14.6 figure measured the removed sheet.
3. **Kill the middle-distance ring seam.** · **DONE 2026-08-13.** `TUNE.mid.radius = 27.0` did
   map to a constant screen row on flat ground, and the measurement that says so is now in the
   gate: bin the view by bearing, ask each bin how far its own sward reaches, convert to the row
   it lands on. On the ring as it stood those rows spanned **1.4 px** — the finding's "razor
   straight across all 1280 columns", in one number. Fixed the second way the item offers, not
   the first: every lattice slot carries its own outer radius, `fade[0]` plus a world-anchored
   offset of up to **±3 m** (±1.6 m on a phone — about an eighth of the ring at every detail
   setting), from smooth 4 m value-noise lobes with a per-slot dither on top. Measured after:
   **5.9 px** of spread at 1280×800 and **17.4 px** at 390×780, reaching 25.0–28.4 m about a
   nominal 26.4. Every card is still rooted on the terrain and nothing moved vertically.
   - **Widening the fade was the wrong half of the choice.** The band is already 7 m, which is
     18 px of the frame at that distance; the line is not the ramp, it is where the ramp reaches
     zero, and a wider ramp still reaches zero everywhere at once.
   - **It is nearly free, and that is a property of the design rather than luck.** Triangles are
     paid for by the LATTICE, not by the fade, so a slot the fringe pushes beyond reach is
     dropped at rebuild instead of drawn at zero height; the lattice grew by the amplitude to
     carry the ones it pushes in, and with a symmetric offset the mean cost is
     `radius² + variance` rather than `(radius + amplitude)²`. Measured A/B at 1280×800 at three
     fixed stations: open prairie **174 363 → 176 656** triangles (+1.3 %, 3 742 → 3 850 flora
     instances), settled town **389 369 → 389 253** (−0.03 %), river bank **350 109 → 350 105**.
     Draw calls unchanged at 37 / 66 / 72. Paying for the whole annulus instead — drawing the
     pushed-out slots at zero height — would have been the amplitude twice over.
   - **The offset is a function of world position only**, so the ragged edge is anchored to the
     ground: it does not swim as the walker moves, and it is the same edge whichever way they
     face. The gate asks the placer (`flora.fringeAt`) for it rather than re-deriving the noise,
     and checks nine points answer identically from two cameras 40 m apart.
   - **The forb ring ends within a metre of the mid ring**, so the flowers would have gone on
     drawing the line the grass no longer does; it carries the same fringe. It is gated on its
     RINGS rather than on its drawn edge — at 3.4 m cells a 3.75° bin holds one or two forbs, so
     "the furthest one drawn" is a sampling statistic, and measured that way it reported a nine
     metre hole in ground that has none.
   - **The pop-in gate had to be made instance-aware to stay honest.** It asked the layer's
     nominal ring how faded an arriving plant was, and the nominal ring answers *zero* — a free
     pass — for exactly the plants the fringe pushes furthest out. It reads each instance's own
     `aChiRing` now. Same bound, same measured 0.0 % arrival height.
3b. **The NEAR/MID handover is a density handover.** · **DONE 2026-08-24, T-0093.** The sibling of
   item 3: that one was about where the sward STOPS, this one is about where its two
   representations swap over. Read this box before quoting a near-ring band or before assuming a
   ring named in a ticket is the ring drawing the artefact.
   - **The instrument first**, because there was none: `tools/measure_near_verge.mjs` classes every
     flora instance the way the fragment shader's own guard does — `whole` (coverage 1, the Bayer
     branch is skipped), `partial` (0 < coverage < 1, **every fragment thresholded — the dots**),
     `absent` — off the `aChiRing` that went to the GPU, then projects each drawn plant's recorded
     height and spread to screen and sums the footprints. Instance counts are the wrong unit: a
     hundred plants at forty metres are four pixels. Mobile runs at `deviceScaleFactor: 1.5`, not
     the smoke's 2, so one measured pixel is one drawing-buffer pixel — the screen door is locked
     to `gl_FragCoord` and a 4/3 resample smears the grain.
   - **THE TICKET'S PRIME SUSPECT IS HALF THE AUTHOR, AND AT ITS OWN TWO STANDS IT IS NONE OF IT.**
     T-0086's two stands are in a roadway and `station()` clears the travel track — 10.5 m on South
     Water, 7 m on Wells — so at *South Water approaching Wells* the near ring places **0 tufts at
     `light`, 1 at `full`**. At *Wells approaching Lake* on a phone the near set is empty and the
     whole screen-doored verge (1.729 % of the frame) is written by the **mid ring's inner ramp
     fading IN across 4.5–7.5 m**. Only in open prairie does the near ring dominate: 5.90 % against
     the mid's 3.65 % exposed at `light`. So both boundaries were converted, not the named one.
   - **The band is not where the ticket says either.** `ringsFor` insets every fade ring inside its
     lattice by the 0.6 m rebuild step, so the ramp runs **4.80–7.00 m** at `full` (measured as the
     `d` range of the partial instances), not 5.4–7.6; and at `light` the ring is 4.6 m, so the ramp
     is **1.80–4.00 m** — under the walker's feet, which is why the phone frame is the dramatic one
     (53.654 % of it screen-doored in open prairie, against 45.173 % on the desktop).
   - **The fix is T-0086's answer on a ring that still has an edge in it.** `TUNE`
     `near.spreadOuter` / `mid.spreadInner` move the band out of the ramp and into a per-slot
     spread of the boundary: `fade[0] − band × handoverRank(e, n)`, world-anchored and quantised to
     ⅛ m as `farRank` is, with the shader's ring left as a step (`HARD`). The fraction of slots
     drawn at `d` is `clamp((fade[0] − d) / band)` — **the same number the alpha used to write** —
     so expected cover is unchanged to the arithmetic and no tuning figure means anything new.
   - **Placement is untouched on purpose.** The mid ring's `return` for slots the fringe pushes out
     of reach is deliberately NOT copied to the near pass: every slot is still dealt a species and
     still counted, so no community's population or cover figure moves. It costs nothing — the
     vertex program already collapsed an out-of-ring plant to a point — and it saves fill, because
     half the band's fragments are no longer rasterised only to be discarded.
   - **Two knock-ons.** Heads ride their PLANT's ring now, not the layer's: on a spread boundary the
     layer's ring answers for no particular tuft, and a head hung on it is R-BUG7 from the other
     end. And `flora.fadeAt`/`heightAt` take all four ring numbers, because a reader carrying only
     the outer radius would be told every mid card past 4.5 m is drawn.
   - **The residue, held rather than closed.** The mid and forb rings' own OUTER ramps are still
     coverage ramps, and at `light` they reach in to **5.4 m** and **7.4 m** — inside the verge on a
     phone. That is the mid→far handover, which T-0086 answered by standing the far band over it;
     the gate holds it against `tools/near_verge_baseline.json` so it cannot grow, and it is filed.
     **Closed 2026-08-27 by item 3c below, and NOT the way this box expected.**
3c. **The outer ramps' WIDTH, not their kind.** · **DONE 2026-08-27, T-0187.** The residue item 3b
   banked: at `light` the mid and forb rings' outer coverage ramps began 5.4 m and 7.4 m ahead of
   the walker and 15.4 % of the phone's frame inside nine metres was written through the screen
   door. Read this box before proposing a density handover on any OUTER edge.
   - **The cause is one line that was never scaled.** `LOW` and `MID` cut `radius` and scaled
     `fringe` with it — "about an eighth of the radius at every setting", its own comment — and left
     `band` at TUNE's 7.0 m and 5.0 m. A ramp sized for 18–27 m therefore sat on a 13 m ring and
     came out across the middle of the phone's field. `balanced` had it too: the mid ramp began at
     **8.2 m** there, also inside the verge. Nothing about the phone was special; the number simply
     was not carried down.
   - **THE OBVIOUS FIX WAS PRICED AND REFUSED, and the number is the reason.** Handing these edges
     over by density — `spreadOuter`, T-0093's own answer — was simulated slot by slot on the
     published mirror against every mid instance's own `aChiRing` and the gate's own 16 bearing
     bins. It takes the mean drawn reach from **26.81 m to 25.42 m at `full`**, which the boundary
     check survives (bar 24.90), and from **11.89 m to 9.64 m at `light`**, where the bar stands at
     **11.60 m and only 0.29 m of it was unspent**. Even a one-metre spread lands at 11.48 m. The
     loss is not a tuning artefact: the drawn edge of a stochastic thinning is the depth at which
     the thinning still leaves a plant standing in a given bearing, and the mid lattice deals about
     one slot per metre per bin at 12 m against two and a third at 26 m.
   - **The bar it fails is resting on plants nobody can see, and that is now its own ticket.** The
     reach admits any plant at `fadeAt > 0.02` — two per cent coverage, one pixel in fifty through
     the Bayer matrix. On a coverage ramp that is every placed slot, so the statistic reports where
     the placer stopped placing rather than where the field ends, and it can only ever be met by
     drawing ghosts. **T-0209.** The bars were left exactly where they stood.
   - **So the ramp is cut to the ring instead.** The rule: an outer band may not BEGIN inside the
     verge — `radius − step − fringe − 9.0`, the nine metres `tools/measure_near_verge.mjs` calls
     the ground a walker looks at. `light` takes **1.6 m** on both rings (the clearance binds at
     1.8; it lands equal to the fringe, so the edge thins over no more ground than it is ragged
     by); `balanced` takes the proportionate **4.7 m** and **3.4 m**, which already clear it; `full`
     is unchanged at 7.0 m and 5.0 m, clearing by 16.4 m and 17.4 m.
   - **What it costs and what it buys.** Placement is untouched, so triangles, instances and draw
     calls are unchanged — the ramp's own comment in item 3 already says the lattice pays for the
     geometry and the fade pays for nothing. What changes is fill: the ground the ramp used to
     thin is drawn solid, and the phone's sward stops opening up five metres ahead of the walker.
     The flower heads reach further out with it, because `headRingOf` hangs the head ring off the
     band (`fade[0] − 0.35 × band`): at `light` the forb heads run to 11.8 m where they stopped at
     10.0 m.
4. **Re-baseline the crown metrics.** The previous crown fine-detail, darkness and hue targets
   measured a surface that no longer exists. Establish new near/mid and far-terrain bands before
   tuning colour or contrast; never improve the score by closing the far field into a sheet.
5. **Horizon continuity.** Columns carrying timber **31 % → ≥ 90 %** (reference 100 % in every
   band). Band *height* stays 1–4 px — that arithmetic is honest. Two mechanisms: drop
   `hazeDisplayLinear()`'s ACES step so the band stops being aimed 16 R / 12 G past the ground
   it touches, and suppress the crown/gap modulation `k` whenever a crown subtends under ~2 px,
   where it deletes the silhouette rather than texturing it.
   **BOTH MECHANISMS DONE 2026-08-13. The photographic column count is NOT re-measured, and
   that half of the item stays open** — the shot harness the 31 % came from is not in the gate,
   and quoting a number this slice did not measure would be exactly the failure § S6a was
   reordered to stop.
   - **The colour is one line and it was arithmetic answering the wrong question.**
     `hazeDisplayLinear()` ran `HORIZON_HAZE` through ACES to reach the band's display colour.
     The band is `toneMapped: false, fog: false`, so its fragment goes `opaque → colorspace`
     and a linear vertex colour displays as the hex it decodes from; the fogged ground goes
     `opaque → tonemapping → colorspace → fog` with `fogColor` uploaded in the OUTPUT colour
     space, so it converges on that same literal hex. One decode each. The tone curve was
     applied to one end and to nothing it had to match, which is the 16 R / 12 G — and the 69
     in blue at `prairie_west` — of L35. Both ends now report **#88a3c0** and the gate compares
     the band's own hazed end against `scene.fog.color` rather than against a hex in either
     file. A second consequence, unstated in the item: the band's far end was displaying at
     **L 170 against a horizon sky of L 162** — a *pale* band, brighter than the sky behind it,
     which is the one thing a treeline never is. It is L 159 now, three below its sky.
   - **The modulation is floored in PIXELS, which is why the band is now solved against the
     viewport.** `MIN_SILHOUETTE_PX = 1.0`: the crown/gap term may cut a bearing to one pixel
     and no further, and where the raw crown is itself sub-pixel it is suppressed outright
     (`kFloor` reaches 1). A floor on the RESULT rather than a cap on `k` binds only where
     pixels are scarce — a 400 m treeline is 40 px tall and keeps its gaps to the last per
     cent. `main.js` passes `pixelsPerRadian` from the live renderer size and camera field, so
     a phone (475 px/rad at its 94° clamp) and a desktop (833 px/rad at 55°) get their own
     answer instead of one hard-coded field; a viewport change re-solves the band exactly as
     walking does.
   - **Measured at the spawn station, with the floor removed and then in place.** 281 of 900
     bearings carry a body. Without the floor the modulation drew **251 of 280** resolvable
     bearings at a pixel or more on the phone and **267 of 281** on the desktop, worst
     silhouette **0.18 px** and **0.31 px**. With it, **280/280 and 281/281**, worst
     **1.00 px**, and the horizon band's triangle count is unchanged at 562 — the floor moves
     vertices, never their number.
   - **The gate is every resolvable bearing, not a percentage**, because 90 % would have passed
     the desktop half of the defect (267/281 is 95 %). It carries both anti-vacuity guards — a
     solver that stopped putting timber up would otherwise report a perfect fraction of nothing
     — and a third assertion that the band was solved against THIS viewport, since a floor
     measured in pixels is meaningless against a hard-coded field.
6. **Close the near field with rooted geometry.** Detail-free area (5×5 luminance sigma <
   2/255, below-horizon, resampled to 1280 wide) was **13.7 %** in the nearest quarter against
   references at 0.3–1.5 %; re-measure it after the one-surface correction. Add a **broad-leaf**
   element — in both references the visual mass at every distance is dicot leaf, not grass
   blade — and deepen the shade without dimming the flecks. Every new instance must begin on
   `terrain.surfaceHeight()` rather than borrowing visual closure from an elevated sheet.
7. **Flower load, against the corrected bar.** ~~Whole-sward chroma flower **1.49 % → 4–6 %**
   (*not* 13.89 %) · nearest quarter **0.07 % → 3.0 %**, which *is* right — it is what a
   never-plowed remnant shows at a matched look-angle.~~ **EVERY FLOWER FIGURE IN THIS ITEM IS
   WITHDRAWN, 2026-08-15 by R-W4c(b1).** There is no 4–6 % bar: no remnant photograph is
   committed, 12.91 % does not reproduce on the planting that is, and the recipe all four numbers
   were read with has recall 0.055. Read R-W4c(b1)'s box before restating any of them.
   Colour variety: effN-after-median at equal N
   **144 → ≥ 300**, green hue IQR **5.6° → ≥ 8.5°**, green chroma p25 **32.3 → ≤ 26** (what is
   missing is the grey-green and glaucous foliage, not the saturated flowers).
8. **Fix the shot set before trusting any of the above.** `prairie_south` sits inside the
   gallery timber (23.4 % open sky), so there is exactly one open-prairie view and
   `prairie_west` has been tuned against itself with no control. Move it, and add a shot
   standing in **z02 mesic prairie** — the camera at `prairie_west` stands 5 cm below the z02
   elevation threshold, which is why wild bergamot, yellow coneflower, rattlesnake master and
   pale purple coneflower render zero pixels in every frame. That threshold is admittedly ours
   (the zone's own note: "a reading of the terrain, not evidence"). **Do not move species
   between zones to satisfy a camera.**
9. **`river_bank` is not honouring its own dataset.** Zone 1 specifies cordgrass at 1.2–2.0 m
   and 40–55 % cover with `bare_soil_fraction: 0.0`; the frame shows ~25 cm sprigs on bare
   soil in near-rows. The data is right; the renderer is not reading it.
   **The general half is DONE 2026-08-13** — see K3: every community is now planted at its own
   recorded `cover.matrix_fraction`, which nothing had read. **The item's own reading is wrong
   in two ways, both measured rather than argued.** The bank is not zone 1: within eight metres
   of water the extent is the marsh (`z04`, priority 70), and the shot's sward is entirely z04
   and z10. And the sprigs were not a density problem — `nuphar_advena` and `nymphaea_odorata`,
   floating-leaved aquatics recorded 0.01–0.10 m tall, were 6.5 % of the tufts planted on that
   dry bank, because `role: emergent` was all the renderer could see and nothing in the
   vocabulary said a lily floats. **DONE 2026-08-13** — the published vocabulary gained
   `substrate` and the placer reads it; see K3. What remains of this item is the mid-field
   coverage question in items 1–7, not the lilies and not zone 1.
10. **Adaptive budget.** Thin the sward automatically when measured frame time exceeds a
    threshold, so a slow device degrades instead of stuttering. Mobile is a release gate and
    the low-spec field is currently a fixed, hand-tuned reduction.
11. **Wind.** One travelling wave and a gust; the references show combing at several scales.

Deferred, with the reason: an **understory below 3 m** would fix a real and measured inversion
(our treeline base is *brighter* than its crowns — base/crown 1.84 against the photograph's
0.74, worth ~60 L) but it is invisible until the crowns stop reading as boulders. Fixing it
first puts a dark skirt under a pile of slate.

## S7 — Polish

Performance against the budgets, licensed ambience audio, provenance-popup UX, `LIBERTIES.md`
completeness pass, mobile release gate.

**Done 2026-08-11 — navigation that grows with the dataset.** A live compass shows the
walker's sixteen-point heading and numeric bearing. A north-up overview draws land and water
from the loaded heightfield, every structure from its compiled footprint, and the moving visitor
marker from the walker state; both overlays are independently persistent settings. The old
anchor buttons remain as authored viewpoints, while the searchable jump index now enumerates
all 76 loaded structures and all four verified street-control intersections. Intersections are
compiled into `sidecars/<scene>/index.json` from `street_control.json` and the datum, so the
renderer still consumes derived scene data and no control coordinate is copied into the UI.

**Done 2026-08-10 — free-fly, and the town seen whole.** `F` (or the ▲ chip) lifts the visitor
off the prairie; `Space`/`Q` and a touch pad rise and descend; the `from_above` anchor arrives
already in the air. Forward follows the look direction and strafe stays level; horizontal speed
scales with altitude, capped, because at 300 m a walking pace reads as not moving. Terrain
remains a floor — the step-up rule and the footprint capsule are deliberately *not* applied,
since they are exactly what you asked to leave. Leaving free-fly snaps to the ground rather
than descending: the walk path's ground-smoothing is exponential at 14/s, which from 175 m is a
150 m/s plummet followed by a crawl.

Worth knowing for whoever takes the next slice: **the aerial view is the most honest picture of
how little is built.** Six structures across a 640 m box, and the edge of the modelled ground is
visible from about 150 m up. That is L17 working as intended, not a bug to hide — but it makes
S5 (more structures) the obvious next unit, and it argues for an eventual haze/extent treatment
rather than a bigger skirt.

**Done 2026-08-10 — the liberties are in the walkthrough.** `docs/LIBERTIES.md` stays the
append-only source of truth; `tools/compile_liberties.py` derives `data/liberties.json`,
`check.sh` re-derives it and fails on drift, and the Evidence panel lists all eighteen with
their reasoning.

**Done 2026-08-10 — and attached to their buildings.** The provenance popup reads `subjects`
and shows the liberties taken with the building being inspected, under "What we made up here",
between the attribute table and the citations. Panel and card share one entry renderer
(`libertyEntryHtml`) so they cannot drift; the smoke asserts per-building filtering rather than
a count, which is the assertion a popup dumping all eighteen would still have passed.

**Done 2026-08-10 — the document is checked for gaps.** The inverse check runs in
`validate.py` (`check_liberties_coverage`) and therefore in `check.sh`: every phase whose
`footprint` or `position` is `conjectural` must be named by a liberty that is *about that
aspect*, matched against the entry's own prose. Naming the building is deliberately not
sufficient, and the self-test asserts exactly that case. Six inventions in the committed data,
six covered. The Evidence panel states the guarantee, because a promise a visitor cannot read
is not one.

**Done 2026-08-10 — coverage is now asserted, not inferred.** Entries carry a `**Covers:**`
field of `structure_id[.phase_id].aspect` tokens; `compile_liberties.py` parses it, and
`check_liberties_coverage` matches the claims against the records **in both directions** — an
invention with no admission fails, and so does an admission whose value is not conjectural
(exempt under **Resolved**, so evidence is allowed to arrive without breaking the gate). The
keyword match over prose is gone, and the self-test's discriminating case is now an entry that
talks about footprints and placement while claiming nothing. Writing the claims down immediately
found a drift the heuristic was indifferent to: L12 described the Walker meeting house position
as `inferred` months after the record was downgraded to `conjectural`. The chips are in the
Evidence panel and on the provenance card, because a guarantee enforced only in the repository
is the filed confession this whole line of work exists to stop being.

**Done 2026-08-10 — the rule now covers what a building *is*, not only where it stands.** The
`Covers:` vocabulary was `footprint`/`position`; it is now every attested value in a record —
those two, `documented_range`, the structure-level `function` and `occupants`, and `form.<attr>`
for anything under a phase's form, enumerated from the data rather than from a list so a new
archetype attribute is inside the rule the day it appears. The argument is that a conjectural
`roof_type` is not an absence in the model: a gable gets built and the visitor sees a gable, and
a conjectural `gallery: false` is the same claim in the negative — a plain front rendered because
nobody found evidence either way, which reads as the finding. Four inventions were owed an
admission and had none: the Sauganash's 1829 cabin height and roof (L18) and the Green Tree's and
the Western's galleries (L19). Ten conjectural values, ten declarations. The chips read as
attributes — "Sauganash Hotel roof type" — while the token the gate matches keeps its `form.`
prefix.

**Done 2026-08-10 — the hard half: omissions and simplifications are enforced.** The missing
claim turned out to belong to the *generator*, not to the record or the document. Each
`generators/archetypes/*_params.py` now declares `CONSUMED`, the form attributes its `from_phase`
actually reads, and `validate.py` holds every attribute outside that set to a `geometry:`
declaration on the record — `absent` (nothing of it is built), `simplified` (a fixed default
stands in its place) or `record_only` (a rejected reading, which owes nothing). `absent` and
`simplified` need a `Covers:` token exactly as an invention does, checked both ways, and the
popup marks those rows *not built* / *not modelled from this* so the admission reaches a visitor
and not only a reviewer. Twenty-one attributes across six buildings reach no vertex; L9 and L10
now claim theirs, and L20–L23 are new.

Switching it on found a real defect, which is the argument for the rule in one line: **the Wolf
Point Tavern's frame extension and its painted wolf sign are both `documented` and neither is
modelled.** The record spells them `frame_extension` and `signage`; `log_dwelling` reads
`frame_addition` and `sign`; the absent attributes resolved to defaults and nothing complained.
Both were fixed the same day, in one slice with the re-bake — see S5. The standing limit is
unchanged and worth repeating: nothing can catch a liberty taken that nobody noticed taking — but
an attribute recorded and never built is no longer in that category.

**Done 2026-08-10 — and the defect it found is repaired: the wolf sign hangs.** The rule's whole
argument was one building, so here is that building finished. The record's `frame_extension` and
`signage` are now `frame_addition` and `sign`, the names `log_dwelling` reads; the frame bay and
the signboard are baked, published and visible; and the popup's `documented` chips over both now
describe something a visitor can walk up to. The rename alone would have been the smaller half of
the fix. A frame addition with no dimensions recorded takes the archetype's defaults — a two-storey
block across the river front, on a tavern the sources describe as low — so the record states the
bay's side, width, depth and storey count, and L24 admits the three of those that are invented.
The board is deliberately blank: the sign is documented and the painting on it is not (L25).

**Done 2026-08-10 — what is not here, and the file that said so reaching a visitor.** Every
gate above asks whether what we *built* is honest. None of them could reach the structures
this project researched and deliberately did not build: `data/exclusions.json` has held
fourteen of them, with the evidence that dates each one, since the scaffold — and it shipped
nowhere a visitor could read it. The Evidence panel now carries them under **What is not
here**, derived per scene by `compile_scene.py` with citations joined, in the same entry the
liberties use. The panel states, and the smoke asserts, that this is **not** a list of
everything missing: eight of roughly forty researched structures stand, and the aerial view
remains the honest picture of the rest.

Switching it on found the one file where rule 1 was never enforced. Every `source_id` in this
project must resolve in `data/sources/`; nothing read the exclusions file's, so a citation
there could have named a source that never existed. `check_exclusions` now requires a slug id,
a name, a stated reason and a citation that resolves — the committed file passes unchanged,
and the next entry cannot skip it. The date gate also runs backwards now: an entry dating a
building to 1837 is a correct exclusion from 1835 and a wrong one from 1837, which no
comparison against the records can catch, because an excluded structure has no record.

And the sidecars are re-derived on every commit (`compile_scene.py --all --check`, in
`check.sh`). They are committed so the site needs no build step, which only keeps the
walkthrough and the archive together if a record edited without a recompile is a gate failure
rather than a discovery on the deployed site. All eight were byte-identical on the first run.

**Done 2026-08-10 — the third category, and the promise inside it.** The entry above ends by
saying the watch list is deliberately not shown and that its uncertainty belongs on the records
and in the popup. That was right about the one of the four that is STANDING and wrong about the
three that are not: an empty lot cannot say *researched, and still open* any more than it could
say *researched and ruled out*. The four are structured data now — what is open, what settling it
would change, a dossier pointer that must resolve to a committed file and to a line inside it,
and citations that resolve or a sentence saying why there are none — and they render under **What
is still an open question**, with the standing one chipped *standing here* rather than listed
among absences. `check_watch_list` enforces the file's own sentence, which had never been
enforced: an entry naming a committed record must name the claim carrying the doubt, and that
claim may not be `documented`, so the day the evidence arrives the gate fails instead of the list
quietly going out of date. Nothing in the committed four was wrong — the value is the next entry
— and the near miss it did surface is `western_hotel`, whose line still read as though its
build-date question were open a day after the record settled it. See STATUS § 37.

**Done 2026-08-10 — the card answers "was it here?", which it never had.** Every gate and every
panel above asks how sure we are of something we built. None of them was asking the question a
visitor asks first, and the card could not answer it: `popup.js` has read
`sidecar.documented_range` since the card was written and `compile_scene.py` never emitted the
field, so the line rendered as nothing on every building for the life of the project. The phase's
claim about itself now travels to the card in the attribute shape — the dated span with its
confidence, sources and reasoning; the phase's `change_note` in the record's own words; and the
position's argument behind a `why` on the line that already showed its chip. Dates print as
recorded, because seven of the eight spans end on 31 December of a year and that is a bound, not
a day anybody wrote down.

The failure class is worth carrying rather than the fix: **two halves each correct about their
own side of an interface neither states**. The compiler was consistent with itself, which is all
`--check` proves; the record validated clean; the markup was right. So the test opens the actual
card and reads what a visitor would see, and asserts the discriminating pair — the Sauganash
`documented`, Hogan's store `inferred` — because a card stamping one grade on all eight would
have passed any check for "there is a chip". Any other sidecar field the renderer reads is in the
same category; `test_the_card_is_fed_the_claims_it_renders` is where the next one goes.
One gate came with it: a `documented` date span now owes a resolving source, like every other
`documented` value. Still not on the card: the footprint's reasoning, because the footprint has
no display value that is not itself a derivation — see STATUS § 28.

**Done 2026-08-10 — the sidecar interface is stated, and stating it found the second field
falling through it.** The entry above ends with a sentence where a mechanism belongs — *any
other sidecar field the renderer reads is in the same category* — and one of them was already
broken. The provenance card asks the sidecar `asset_is_placeholder`, a field `compile_scene.py`
has never written and, compiling from `data/` alone, cannot: so the note telling a visitor *this
shape is a stand-in, not a bake from the record* has never rendered on any building.

`check_sidecar_contract` derives the interface from both halves rather than asking either to
declare it — what is emitted comes off the committed sidecars, which `--check` already proves
are what the dataset compiles to, and what is read is scanned out of the renderer's own modules.
27 reads across six modules; one resolved to nothing. The fix moves the fact instead of inventing
a field: a placeholder is something the GLB says about itself, `scene-loader` has read it at load
time all along, and it now reaches the card on the registry entry. The scan sees a read that
names a field while the sidecar is in hand and not one made through a function parameter — which
is the direction both faults came from, since that is where the field name is chosen. The
reverse direction is a note, not an error, and it has one finding in it: `research_note` is
compiled into every sidecar and shown nowhere. That is an unshipped claim rather than dead
weight, and it belongs to whoever next works on the card.

**Done 2026-08-10 — and that claim is shipped: the record's own account is on the card.** The
last entry ends by handing `research_note` to whoever next worked here, and this is that slice.
It is a different fault from the two above it and the difference is the point: nothing was
broken. The card asked for nothing it was not given, the compiler wrote what it should, every
gate was right — **the field simply had no surface**, which is how a claim goes unshipped when
there is no fault for a check to find. Every structure record carries one, written for a reader:
what it actually asserts, which sources disagree, which was believed and why, and where the
record is weakest.

Shown **verbatim**, and the smoke pins that with an exact string comparison against the sidecar
rather than a substring match — a note whose subject is the limit of the evidence is the last
text on this card that a program should trim or summarise, and a first sentence with an ellipsis
would pass any looser check. The discriminating case is asserted as everywhere else on this
card: a second building gets its own account, so one fixed block of prose fails. Collapsed by
default for the liberties' reason — several hundred words open would push the citations off a
62vh panel on a phone. The unread-field note is down to `archetype`, `scene` and `target_date`,
which are machinery a visitor has no reason to see, so the list is empty of unshipped claims.
Untested and stated: the empty state, since all eight records carry a note.

**Done 2026-08-10 — the outline says how much of itself is evidence, and the silence is countable
now.** The card graded a roof pitch and said nothing whatever about the largest claim a visitor is
standing in front of: `compile_scene.py` carried `footprint.confidence` and dropped
`footprint.sources` and `footprint.note`, so six placeholders that say PLACEHOLDER in their own
first line reached nobody, and neither did the two footprints that are evidence. **Was it this
shape?** is a section of its own, rendered by the same claim renderer as the presence line so the
two cannot be qualified differently.

The card prints **no dimension**, and STATUS § 28's argument for that is unchanged — the only
printable value is the polygon, reducing it to a box is a measurement the record does not make, and
the shape is already in front of the visitor at full size. `claimRow` renders no value cell for a
`null` value and the smoke pins that across all eight buildings.

Two things worth carrying. **The compensating disclosure was a sentence, not a build**: the massing
rule was narrowed to stop dithering a documented building over an unknown SIZE, on the recorded
understanding that the size would be carried on the card, and nothing carried it. **And this is the
second graded-and-silent claim found by reading a file** (`documented_range` was the first), so it
has a count rather than a third discoverer: the smoke matches each record's graded claims against
the chips its card draws, for every building, and reports all eight one chip short when run against
the previous commit. What it cannot see is a chip whose reasoning is wrong, and it cannot reach a
field the compiler never writes — `check_sidecar_contract`'s unread report is top-level only, and
widening it to leaves was refused because the scan cannot follow a value into a function.

**Done 2026-08-10 — the open question reaches the building it is about, and the panel's promise
about the card is a gate.** § 26 said the watch list's uncertainty belongs on the records and in the
provenance popup and left it unqueued; the panel half shipped and its entry for the one STANDING
structure tells a visitor, in rendered text, that *the provenance card shows it*. The card showed
the dated claim with an `inferred` chip and never that the claim is a tracked open question — not
the dispute behind it (the builder's own statement against a hotel chronology), not that the later
date would make the Western Hotel brand new on the scene date, not that the grade is held down on
purpose. The card now carries the panel's own entry through the panel's own renderer with an
`onCard` flag, filtered by `openQuestionsFor` exactly as the liberties are, so one uncertainty
cannot be described two ways. The other seven buildings render nothing rather than a reassurance,
because "no open questions recorded" would read as settled and the list cannot promise that.
And `check_watch_list` now holds `carried_by` to a claim the card really renders — the path is read
out of `popup.js` by § 29's scanner — which is the third instance of a sentence in this project
describing a surface it could not see. Data and meshes untouched; nothing was re-baked. STATUS § 41.

**Done 2026-08-11 — a rung is a judgement about a document, and the document had never reached
the card.** Four slices (§ 44-47) established which page carries which document and what each
one cannot supply; all of it landed in `data/sources/*.json` and none of it left the repository.
So a visitor following a citation reached a present-day blog stamped *tier 2 · near-primary
recollection* with nothing saying it reprints the *Chicago Tribune* of 14 August 1910 carrying
John Dean Caton's own account — the ladder made to look like an over-grade by the one field that
would have explained it. Every citation now carries the document it reprints with that
document's date, or the finding that the page reprints none, and the source's own
`what_it_supplies` / `what_it_does_not_supply` behind a `<details>`.

The fault is a third kind and it is why the gate is shaped the way it is. § 28 was a field read
and never emitted; § 30 was a field emitted and never read. This one **never entered the
interface**, which neither direction of `check_sidecar_contract` can see — a shape unioned over
what is emitted cannot report what was never offered. The bounded set is the schema, so
`compile_scene.SOURCE_FIELD_SURFACE` partitions all 22 properties and `check_source_surface`
fails on a property in neither half, on a visitor-facing field no compiled citation carries, and
on one `citations.js` never reads. Adding a field to a source record now costs one line saying
whether a visitor sees it.

Three things worth carrying:

- **A partition inside a field is legitimate and has to be argued.** The card gets the document
  and the limits; it does not get the `note` on a `transcribes` entry or the reading in
  `carries_no_document`, because both quote rung numbers, name files in `data/` and record HTTP
  statuses — they are addressed to whoever re-grades the source. Stated in `citations.js` and in
  STATUS § 48 rather than left looking like an oversight.
- **One renderer for every context stopped being right, and a test said so first.** The reprints
  line arrived under "What is not here" and named *"The Old Western Hotel"* — a building standing
  200 m away — failing § 26's assertion that a standing building may not appear on that list. The
  section keeps the plain citation, `evidence: false` says so at the call site, and a new
  assertion pins it so the option cannot flip back.
- **Markup inside a list item makes counting selectors wrong.** A nested `<ul>` broke two
  unrelated assertions enumerating `.cites li`; they are `.cites > li` now. Second occurrence of
  this shape.

**Done 2026-08-11 — the other three derived documents are an interface too, and both sentences
they were hiding were written for a visitor.** The entry above closes the source-record
direction. What it does not close is the *document*: `sidecar_shape` says in its own docstring
that it covers the per-structure sidecar and not `exclusions.json` or `terrain.json`, because
those "have their own readers and their own shapes" — so the interface where § 28, § 29 and § 30
each found a fault was guarded for one document out of four. `check_derived_contract` covers the
other three, both directions, and found two on its first run.

The ground now says **which ground** its twenty claims are about — the spec's own sentence about
the forks quadrant, compiled into every terrain sidecar since the terrain landed and asked for by
nobody, which is the first question a visitor has after watching the ground end from the air. And
the liberties list says what a liberty is **in the document's words**: `liberties.json` carries
that sentence, `index.html` carried a hand-typed paraphrase of it with nothing holding the two
together, and the paraphrase is gone.

Three things worth carrying:

- **The binding is declared, not inferred, and that is the design.** A sidecar names itself;
  these are fetched into `doc` and handed entry by entry to a renderer, so the field name is
  chosen against a function parameter — § 29's stated limit. `DERIVED_DOCUMENTS` writes the
  binding down and the gate holds the module to it both ways, including a root bound where the
  document has nothing.
- **`internal` is § 48's partition on a second family**, over what the compiler emits rather than
  over a schema, checked in both directions so a declaration cannot outlive its field or be wrong
  about the visitor. Citation leaves stay with `check_source_surface`: one field, one owner.
- ~~**A read is a name, not a render — and one is still outstanding.**~~ **DONE 2026-08-11**
  (STATUS § 50). `exclusions.json`'s `standard` and `uncertain_standard` were read into
  `mountExclusions`'s return value, rendered by nobody, and restated by hand in `index.html`;
  both are mounted verbatim now and the paraphrases are deleted. It was the estimated size — a
  `standardMount` and two paragraphs — and it found one thing the estimate did not: the
  open-questions paraphrase had drifted into a **hand-typed count** of the watch list ("three of
  these … and the fourth"), which goes wrong the day a fifth question is recorded and which no
  gate in this project could have held. The smoke asserts the compiled sentence verbatim, once,
  and that the count is gone. **The gate's limit is unchanged and was not widened**: a read is
  still a name, the scan still cannot follow a value into a function, and the next such field
  will be found by a person reading a module.

**Done 2026-08-10 — the staleness gate is a check now, not a sentence.** Every rule above
assumes the shipped mesh is the one the record describes, and nothing was testing that: the
manifest had carried an `inputs_sha256` per asset since the first bake and no code ever
recomputed it. It does now, for buildings and terrain alike, with the recipe living beside the
generators so the writer and the checker cannot drift.

Turning it on meant rewriting what the hash is over, because the old one reported all six
buildings stale for reasons that cannot move a vertex — record prose, and a constant added to a
sibling archetype's parameter module. It now hashes the *resolved* parameters, the derived
properties, the confidence floats and the builder's bytes; parameter-module source is out,
because its entire effect on the mesh is the object it returns. The eight committed hashes were
re-stamped without a bake and the re-stamp is proved rather than asserted: run the new recipe
inside a worktree of the last bake commit and the input documents come out identical, `build.py`
excepted, whose only change is delegating the hash. See STATUS § 15 for the full account and the
limit — this compares inputs, not output, so a hand-edited GLB still passes.

**Done 2026-08-10 — a structure has to reach the ground, and one does not.** The third
honesty gate in the family that began with liberties coverage. The confidence model grades what
a value claims and the geometry declarations grade whether it was built; neither can see a
structure assembled faithfully onto ground that is not under it, because every name resolves and
every value reaches a vertex. Each archetype now declares where it touches the terrain —
`perimeter` at the base of the walls, `ends` at deck height for a crossing — and `validate.py`
measures that outline against the committed heightfield. The tolerance is the walker's 0.35 m
step-up rule rather than a fresh number, because the gate is asking the walker's question.

The six buildings land, worst corner 0.16 m. **The North Branch bridge stands 2.42 m clear of
the ground at both landings and no land in the 640 m box rises to its deck**, so the crossing
touches neither bank. The record declares `ground_contact: approach_not_modelled`, L30 admits
it, and the chip reaches the visitor through the provenance popup. Two follow-ons this leaves
on the table, both real and both bigger than a slice:

- **The approach itself is unattested.** Nothing describes how a person got from the bank onto
  the deck, so the fix is research before it is geometry — the 1834/1835 Wabansia and Kinzie's
  Addition plat is the best candidate, and a sourced clearance would narrow it too, since a
  lower deck needs less approach.
- **Walking the deck** (STATUS § 21) is now measurably blocked rather than merely unbuilt: even
  with surfaces-above-the-ground in the walker, there is nothing to step from. The two are one
  piece of work, in that order.

**Done 2026-08-10 — the ground states its own claims, and stating them found the second file
where rule one was never checked.** Every honesty surface above belongs to a building. The
terrain grades itself as carefully as any record — `documented` water, `inferred` division
levels off period narrative feet, a `conjectural` bank face, a channel section whose note says
it carries no evidence at all — and said none of it to a visitor, while dithering under the
confidence view like everything else, which shows that a judgement exists and nothing about
what was judged. The Evidence panel now carries *The ground you are standing on*: 20 claims
with the spec's own figures, its reasoning verbatim and its citations joined, derived by
`compile_scene.py` and re-derived by `check.sh`. `check_terrain_claims` holds them to the
record's rules — sources resolve, `documented` owes evidence, no land elevation may claim to be
documented — off the same enumeration the panel renders, so the checked set cannot stop being
the displayed set. L32 and L33 admit the bank face and the channel profile, which have been
conjectural in the data since the terrain landed and were admitted nowhere.

Two follow-ons, both real, both stated in STATUS § 32 rather than quietly dropped:

- **Three claims are `inferred` with no reasoning at all** — the north and west division soils
  and the channel's. On a record that is an error; here it is a warning, because the note has to
  go in `terrain_spec.json`, whose *bytes* are the terrain's staleness hash, so a sentence that
  cannot move a vertex re-stales the ground and needs a bake. **The slice that writes those three
  notes lands the bake with them and turns the rule into an error.** Worth doing at the same time:
  `terrain_inputs_sha` still hashes whole files, which is the false positive STATUS § 15 removed
  from the building hash arriving on the terrain side.
- ~~**The liberties coverage gate cannot see the terrain spec.**~~ **DONE 2026-08-10** — see the
  entry below.

**Done 2026-08-10 — the ground answers to the coverage gate, and the first thing it asked for
was an invention nobody had noticed.** The entry above names its own limit: the terrain's
inventions reached the Evidence panel and stayed outside the gate, so L32 and L33 existed
because a person noticed. `Covers:` now has a second namespace, `terrain.<epoch>.<claim>`,
enumerated by the same `compile_scene.ground_claims` the panel renders from and matched in both
directions — an unclaimed conjectural ground value fails, and so does a claim on a block that is
not conjectural, on an epoch that is not committed, or on a claim id the spec does not grade.

Six conjectural ground claims; five had prose behind them (L14 micro-relief, L15 the two swales,
L32 the bank face, L33 the channel section) and adding their `Covers:` fields was bookkeeping.
**The sixth had nothing.** The north-side slough's existence and course are Wright 1834's; its
one-foot bed and 1.2 m e-fold are in the model because a shallower channel stops reading as
water, and no list mentioned them. **L34** is new. Third check in this family to find something
on its first run.

Two decisions are asserted rather than assumed, and both are about naming. The epoch is in the
token because `docs/EPOCHS.md` versions the ground, so a later shoreline's inventions must not be
discharged by this one's admission — the self-test pins that. And the terrain is not modelled as
a structure record called `terrain`: the domains are separate obligations, neither discharges the
other, and the claim carries its `domain` rather than leaving a reader to infer it from a token's
shape. ~~What is still outside the rule is the ground's **omissions** — there is no terrain
`CONSUMED`~~ — **DONE 2026-08-10, see the entry below**; the grades stay block-level, so L34
admits more than the data does.

**Done 2026-08-10 — the ground has to say what it does not build, and it is not made of what it
says it is made of.** The entry above names its own limit: the coverage rule fires on a
`conjectural` tag, so an invention was demanded and an omission left no trace. The terrain has a
`CONSUMED` now — the spec figures `terrain_gen.build_field` actually reads — and
`check_ground_geometry` holds every other figure the Evidence panel shows to a `mesh:`
declaration on its block, in both directions, with `absent` and `simplified` owing a `Covers:`
token exactly as they do on a record.

**Five surface materials, two of them `documented`, describe a soil no surface in this model is
made of.** The ground mesh is one earth colour edge to edge; `terrain_gen.py` builds elevation
and nothing else. That is the Wolf Point wolf sign one domain over — the project's strongest
chip over something a visitor is emphatically not looking at — and L35 is where it is admitted.
The rows say *not modelled from this*, in the provenance card's words, out of the provenance
card's module (`renderers/web/js/geometry.js`, now shared by both surfaces). Colouring ground by
zone is **S6** and the declaration comes off the day the generator reads the value.

Three things worth carrying, all of them about where a declaration may live:

- **`terrain_inputs.CONSUMED`, not `terrain_gen.CONSUMED`.** An archetype declares its consumed
  set beside the code that reads it, and that only works because a params module's bytes are out
  of the building hash. `terrain_gen.py` goes into the ground's hash whole, so the map re-staled
  the terrain on sight and asked for a Blender bake to land a constant. It sits beside the
  denylist instead — same file, same subject — and `test_declared_terrain_reads_are_real_reads`
  scans the generator for a read of every declared key, which is what co-location would have
  bought.
- **The key is `mesh` because `geometry` is taken.** In a GeoJSON that word is the coordinates;
  stripping it from the hash would have taken every traced bank line out of the ground's
  staleness. A test written for § 34's purpose refused it on the first run.
- **`restated_in_code` is a fourth state and only the ground needs it.** The water plane's zero
  and the bank's ease-out are written in the spec and separately written in Python. The mesh
  agrees with them and does not read them; that is a warning to whoever edits the generator rather
  than a caveat to a visitor, so it carries no marker. **What held the two halves together was
  nothing, and since 2026-08-10 (STATUS § 36) it is `terrain_inputs.RESTATES`**: each restatement
  names the half it agrees with — a figure in the heightfield the bake wrote, another figure in
  the same block, or a line of `terrain_gen.py` — and `check_restated_agreement` compares them.
  Switching it on found three figures making the promise under the wrong state: every division's
  `bank_crest_ft` restates `near_ft` and was declared `record_only`, which owes nothing and asks
  nothing. All seven agree today; the value is that the next edit to a division level cannot leave
  the panel showing the old crest.

**Done 2026-08-10 — the sum under five buildings is data now, and it was five paragraphs.** Every
gate above asks whether a claim is honest; this one asks whether the arithmetic beneath a
coordinate was ever redone. Five placements are the same construction — a modern intersection
centre off OpenStreetMap, half an 80 ft platted street to the kerb, a named face on it — written
out once per record, with the number 12.2 appearing in five paragraphs and no file.
`data/traces/street_control.json` holds the module and the control once;
`check_position_derivations` rebuilds every placement from them and holds the rest to a
declaration; and the sums were all correct, which is the least interesting part.

Three things worth carrying:

- **Ask the placed shape, not the coordinate.** A record's position is the footprint polygon's own
  origin, so a facade bearing turns it off the corner the claim is about — the Green Tree's
  easting sits 24.4 m from its intersection where the claim says 12.2. A check comparing
  coordinates to kerbs passes a correctly placed building and a rotated-out-of-its-lot building
  with equal confidence, so the self-test's discriminating case is one building appearing twice.
- **A disagreement you cannot act on gets recorded and left.** The 80 ft / 66 ft street width
  (`docs/RESEARCH/hogan_store.md` § 5) sat because settling it meant five hand-redone sums. It is
  now one edit and a printed list of which buildings moved, 2.13 m each.
- **Writing the control down found two coordinates for one junction** — Canal and Kinzie, averaged
  over five OSM nodes for the georeference and three for the bridge, 3.8 m apart. The bridge is
  not moved: its span is the distance between the traced banks along its centreline, that distance
  is a mesh parameter, and re-deriving it asks for a bake. The variance is declared and checked
  instead. See `docs/RESEARCH/street_module_1830.md`.
- **The control point the whole west division is measured from is inside a block** (2026-08-10,
  STATUS § 42): Hathaway HA is 52.4 m west of the Canal Street corridor and Wright G5 20.2 m west,
  both with block 28's number printed across them. G5 is a datum GCP, so the exposure is priced
  (15.0 m of origin movement, RMS unchanged) and queued rather than taken — adopting it re-derives
  every coordinate and stales every mesh. `check_street_module` fails the day either correction
  lands, because the finding's inputs would have moved.
- **And re-fetching the control the next day said which of the two was right** (2026-08-10,
  STATUS § 39). A junction is the nodes shared by the two named *surface roadways*; two of Kinzie
  and Canal's five committed nodes are bikeway crossings, and the other three are the bridge's
  reading to a centimetre. The same inclusion had put Randolph and Canal 4.44 m out, which moved
  the Western Hotel. `tools/refetch_control.py` re-derives a junction from the street names and
  re-fetches the recorded node ids; it needs the network, so it is on-demand and not in
  `tools/check.sh`.

## S10 — Complete July 1835 building inventory · **RECONCILED 2026-08-14**

The owner-supplied reconstruction specification establishes a production target of **665 roofs**:
511 principal/functional and 154 ancillary, distributed South 370 / West 135 / North 150 / Fort
10. The durable master ledger is `data/reconstruction/1835_building_inventory.json`; it preserves
the independently reconcilable family and district matrices and explicitly separates aggregate
moderate confidence from interpretive per-instance placement. **That file is the TARGET and does
not move.** What has been built against it, what is left and where it can go are derived —
`tools/reconcile_665.py` → `data/reconstruction/1835_665_roof_programme.json`, re-derived by
`tools/check.sh` on every commit (T-A1).

**Standing 2026-08-14: 232 physical roofs from 242 records. Remaining: 433** — South 270,
West 94, North 69, Fort 0. Of those 433, **105 have modelled, platted ground to stand on** and
328 do not: 20 in the two blocks the plat module refuses for want of South Water street control,
35 held by the West recipe's own extension gate, and 273 in ground with no committed street
control at all — east of State, south of Washington, west of Clinton, and the whole North
Division, which the grid covers by not one block. The 665-roof programme is **coverage-bound,
not recipe-bound**; § S9 is what stands between it and the next two hundred roofs.

Six family targets are already exceeded by evidence — C1, I2, T2, W1, W4 and W5, nine roofs —
which the ledger reports rather than hides. A documented roof is never removed to protect a
family cap, so the nine come out of the invented family with the most slack.

- **Phase 1 done:** 48 visibly tagged anonymous South Division roofs in five mixed blocks—40
  principal/functional and eight ancillary. Reproducible records and flagged review GLBs are
  derived from the parcel recipe without Blender and checked on every commit.
- **Phase 2 planning advanced in parallel:** reviewed, non-rendered recipes now reserve another
  84 South roofs, 55 West roofs and 60 North roofs without overdrawing any family target. The
  South recipe is collision-checked against protected named sites; the North set's 60 footprints
  stay on the current dry terrain. The West recipe deliberately gates 35 roofs until the world
  extends to local E -700 m, and the remaining 90-roof North pass waits for unified terrain,
  hydrology, collision, flora, streets and map coverage to N +760 m. These are production plans,
  not added scene count; existing-roof reconciliation comes first.
- **Done 2026-08-12:** all 76 pre-existing records are reconciled to physical roof units; bridges,
  yards, palisades, construction sites and compounds no longer make record count a proxy.
- **Done 2026-08-12:** the terrain-safe 60-roof North initial parcel is visible and checked.
- Verify the occupied west/north settlement extent before extending terrain. The enlarged plat
  is not the same thing as built footprint, and at least 45% of it remains sparse/open.
- Implement the 35 family archetypes and 250+ visible combinations, replacing—not silently
  promoting—the review massings.
- Populate remaining district parcels to the reconciled target, then add terrain-sampled
  foundations, yards and props. No separate collision plane.

See `docs/RESEARCH/recommended_infill_1835.md`,
`docs/RESEARCH/1835_existing_roof_reconciliation.md`,
`docs/RESEARCH/1835_family_archetype_crosswalk.md`,
`docs/RESEARCH/phase2_south_core_and_mixed.md`,
`docs/RESEARCH/west_division_infill_1835.md`, and Liberty L81.
The North analysis is `docs/RESEARCH/1835_north_division_extent_and_infill.md`.

## S8 — Milestone 1

Wolf Point cluster + South Water block D (LaSalle–Clark). The first test of whether the
archetype approach actually pays for itself.

## Later — the 4D proof

A second scene (1833 or 1830) exercising the epoch machinery, the `pre_fire_v1` crosswalk, and
a Manager row with the changelog cadence running.

---

## Working notes

- `tools/check.sh` before every commit. It takes under a second.
- One coherent unit of work per run.
- Writing subagents each get their own git worktree.
- Update `STATUS.md` in the same commit as the work, and keep it unflattering.
- No model identifiers in repo artifacts.
