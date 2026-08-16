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

### NEXT UP — the unambiguous picks

| # | lane | parcel | why first |
|---|---|---|---|
| — | RENDERING | ~~R-BUG3c~~ | **DONE 2026-08-15** — neither surface moved: the publish step quantises the ground onto a **306 mm** vertical lattice AFTER the only gate that measures it, burying the road and the flora by up to **228 mm**. The heights are read back off the field at load, and two gates now hold the file that SHIPS. Read the box before quoting any ground number |
| — | RENDERING | ~~R-W4c(a)~~ | **DONE 2026-08-15** — the flower-load recipe's hue cut at 50° runs through the middle of a July prairie's bloom, so `0.0012` is not a count of flowers. (a) landed the honest measurement; **(b) is the tuning half and must take (a)'s committed numbers as its baseline** |
| — | RENDERING | ~~R-W4c(b1)~~ | **DONE 2026-08-15** — **there is no 4–6 % target.** Its remnant half cites no photograph this repository holds; its planting half does not reproduce (**5.54 %**, and 12.91 % is not on that frame under either ordering); and the repair R-W4c(a)'s diagnosis implies **fails** — reordering the tests takes precision **0.998 → 0.062**, so the flower test cannot see a flower either. Read its box before quoting any flower number |
| — | RENDERING | **R-W4c(b2)** | **NOT A PICK — it is blocked on the owner.** "Raise the bloom" has no bar left to raise it against, and R-W4c(b1) measured that the bloom is planted from sourced `density_per_ha`, so moving it is a DATA change needing source support rather than a renderer tune. Three routes are written up in (b1)'s box for the owner to choose between; an agent picking one would be inventing the target this parcel just removed |
| — | RENDERING | ~~R-W6~~ | **DONE 2026-08-16** — **yes, at 16 bits**, and the artefact was not invisible: the 14-bit ground stands up to **46.3 mm** above the field, past the 22 mm road lift at 87 sample points, **one of them 1.9 m from South Water Street's centreline**. 16 bits costs **1,116 bytes** and takes the worst error to 12.9 mm, under the lift everywhere; the uncompressed 5.8 MB would buy 12.9 → 7.7 mm, and 7.7 is DECIMATION the master carries too. Read its box before quoting any payload or lattice number |
| — | RENDERING | ~~R-BUG4~~ | **DONE 2026-08-15** — the wet-corner rule deleted the dry half of a road panel with the wet half. Clipped at the waterline now: **28 panels / 62.7 m** of roadway recovered, and the gate asserts the invariant rather than the number |
| — | RENDERING | ~~R-W4a~~ | **DONE 2026-08-15** — the horizon figure counted the town's roofs as timber (62 % of it at `prairie_south`), the G−B discriminator this project named was measured and **refuted**, and the replacement cannot move when a block lands. Read its box before quoting any horizon number |
| 2 | RENDERING | **R-BUG4** | XS, owner-reported. A wet CORNER deletes a whole road panel, dry half included: **28 panels / 62.7 m** of roadway removed where the centreline is dry land |
| 3 | RENDERING | **R-W4a** | the horizon-timber metric counts gable ends as trees, so W4's headline number is unmeasurable and a town parcel already banked a false pass. Prior to every other W4 half · *promoted 2026-08-15: R-M1b, which was #1, is blocked on the owner* |
| — | RENDERING | ~~R-M1~~ | **R-M1a DONE 2026-08-15** — the two scales are measured and their baseline is committed. **R-M1b is NOT a pick: it is blocked on a threshold source, because the photograph R-M1 named to derive from contains no dirt track.** Read R-M1b's box before touching it |
| 4 | RENDERING | **R-W1** | RENDERING §4: "W1+W4 alone retire most of §1" — and R-G1 scored lighting **3.2**, the second-worst axis · *parked on PR #125 with `hold`* |
| — | RENDERING | ~~R-W2a~~ | **DONE 2026-08-16** — the material sheet, measured out of the shipped GLBs: **1,353 material slots, 32 names, 41 colours, 18 roughness values, zero textures**. Five findings, and two of them block texturing outright: **the chimney is not a material here** (219 stacks painted `roof`) and **no record states a roof covering** (315 roof types, 0 coverings). Read `docs/RESEARCH/materials.md` §4 before quoting any material number |
| 2 | RENDERING | **R-W2b** | wire R-W2a's committed sheet into the params and records. **Unblocked as of 2026-08-16** — the sheet exists, and it says which surfaces are real, what selects each one, and which two tiles cannot be sized until a source arrives |
| 3 | RENDERING | **R-W2c** | opened by R-W2a: 219 chimney stacks on 199 buildings are painted with the roof's colour, while the 90 placeholders ship a real brick. Opens with a research question, not a palette. **NEEDS ONE BAKE** |
| 5 | RENDERING | **R-W5a2** | the last 16 batches → 1, opened by R-W5a with its numbers already measured. **Not needed for the budget** — take it only when the lane has nothing sharper |
| — | TOWN | ~~T-A15~~ | **DONE 2026-08-15** — `blk_randolph_clark`, the block opposite the courthouse: the first with a store on it, the face rule EXTENDED to rank one (**K32**), the end rule measured at **1.02× / 7.5 m** and declared exhausted (**K31**), and **two of T-A14's three adoption candidacies refuted** — the laundress and teamster arguments never claim a floor, so they fail rule 6's test 1. Read finding 3 before quoting any adoption test |
| — | TOWN | ~~T-A16~~ | **DONE 2026-08-15** — `blk_randolph_lasalle` is **the public square** and is not a building site. It was withdrawn rather than built: no lots, no roofs, a gate, and **two documented buildings moved off it**. The block parcel's own gates all passed on the old placement, because not one of them asks whether the ground was for sale. Read its box before scheduling anything anywhere |
| — | TOWN | ~~T-A3h~~ | **DONE 2026-08-15** — the last open block entry, and the two adoptions it predicted are the two it made: `blk_randolph_dearborn`'s D3 to the carpenters and its D1 to the labourers, measured with `tools/measure_adoption_tests.py` rather than recalled. **Its finding is about the other two**: the D4 and the D2 that pass as a "second roof" are pairs this layer has NEVER housed — the D4 evidence is one household in the NORTH, the D2's is four in the NORTH and WEST — so every second-roof refusal K28 has collected is a candidacy built from two projections of one table. Read its box and K28's before quoting any adoption test |
| 1 | TOWN | **T-V2** | XS, one record: the `south_water` anchor points at a field, not at the street it is named for — **R-BUG3 measured it at 101 m from its own centreline**, and 17 m from the nearest one |
| — | TOWN | ~~T-V1(a)~~ | **DONE 2026-08-15** — the stamp is **not** at `south_water`: every twin in the town is in the North Division parcel, **36 of its 60 roofs**, and the census found something bigger — **40 eaves outside the band their own note cites**, 18 of them in a parcel that samples its footprints and says so. (b) is written, measured and **blocked by a circular dependency in the pipeline** — read its box before touching any dimension on a baked record |
| 2 | TOWN | **T-V1(b)** | the sixty North records: **NEEDS ONE BAKE**, and cannot go green on the improve runner. A policy question for the owner, not an engineering one |
| — | TOWN | ~~T-I3(a)~~ | **DONE 2026-08-16** — the town's public buildings are **three roofs** and this project already had all three, so the refusal is now absolute rather than argued. The finding is the fourth building: **the court-house was not built yet** — Andreas fixes the season, the month AND the corner the record said nothing fixed, and the citation it had was a **picture caption** — so a record is taken OUT of a scene on evidence for the first time. Read its box before quoting any civic number |
| 3 | TOWN | **T-I3(b)** | **NOT A PICK WITHOUT THE OWNER.** Three of the six I3 slots are a count of nothing; the inventory's arithmetic is closed, so removing them is either "the town had 662 roofs" or "three roofs were not civic". Two different claims about the town, and the research settles neither |
| — | TOWN | ~~K30(a)~~ | **DONE 2026-08-16** — it is **29 buildings on eight streets**, not three on one, and every one of them is a record a PERSON placed: **zero** generated roofs lap a corridor, across 332 placed phases. The depths are bimodal with an empty gap at 1.98–3.48 m, and **13 of the 17 deep ones are South Water**. T-A7's "fourteen" does not reproduce **at its own commit** (16 there, the same 16 today), and the anchor-convention suspect is **refuted** — recentring makes 10 of the 29 worse. Read its box before quoting any intrusion number |
| — | TOWN | ~~K30(b)~~ | **DONE 2026-08-16** — the cause is the **drawing**, and the Wacker made-ground suspect is **refuted** by arithmetic: the anchors sit 11.64–15.30 m from the centreline against a 12.192 m half-width, with both signs, so no displacement of 4.51–8.17 m is there. The records are derived to their FRONTAGE and drawn with the body growing north from it (331 of 333 footprints grow from the minimum corner), so each stands in the road by its own depth — **all 17** deep records, and reflection takes 12 of them under 1 m. **The residual law** settles the shallow tail without moving anything: what survives correct drawing IS the point's own penetration, to 0.10 m. Read its box before quoting any intrusion cause |
| — | TOWN | ~~K20~~ | **DONE 2026-08-16** — the invented-name allocator, measured properly for the first time: **73 of 113 renamed by ONE new household**, not the 17–25 the eleven by-product measurements reported, and never zero in the two big buckets. It is **10** now, and the report prints each bucket's **pool pressure** so the residual cannot be misread — at 0.14× it renames **one**, at 2.03× it renames ten, and that is the pool being too small. Unwelding the given name from the surname exposed **two identical residents**. Read its box before quoting any churn number |
| — | TOWN | ~~K28~~ | **DONE 2026-08-16** — three questions, three clauses, **two gates, and not one record moved**. The table is **projections** (the pair reading is refused because it refuses T-A4's fourteenth labouring household, one of the four rule 6 says its third test recovers); there **is** a cap, one adoption per trade per block, which is what makes the projections safe; and test 1 means the trade's **own committed text**, so the laundresses' D2 and the teamsters' D4 are refused with the remedy named. All **21** standing block adoptions already obeyed it. Read its box before quoting any adoption rule |
| 4 | TOWN | **K30(c)** | the repair K30(b) attributed: redraw the bodies onto the correct side of their own frontage. **NEEDS ONE BAKE** — it changes footprints, so it cannot go green on the improve runner |
| — | TOWN | ~~K25a~~ | **DONE 2026-08-15** — it is **98 values on 80 of 249 records**, not 54 on 193, and **24 causes, not 98**: seven metre values hold all 54 eaves and six degree constants hold all 38 pitches, because the generator authors the archetype's constant and the note cites the family's band. **Roof pitch had never been measured by anything.** The sub-1-ft question is decided — they are failures, and nearness is the diagnosis. Read its box before quoting any band number |
| — | TOWN | ~~K33~~ | **DONE 2026-08-15** — it is **623 values on 227 of 249 records**, not 581, and the extra 42 are the finding: `roof_pitch_deg` cites a band on five families whose roof line is **"gable or shed"**, a form with no slope, and K25(a) could not see them because **a value with no band is never tested against one**. Route 2 (split the note), and route 3 is measured as unavailable — the confidence floats are in the mesh hash and prose is not. The assertion is **absolute, not a ratchet**. Read its box before quoting any citation number |
| — | GROUND | ~~T-E2~~ | **DONE 2026-08-15** — 26.5 % of the modelled land above the water surface is the reservation or the bar, and every gate this project had would have built on it. Nothing moved: **zero** anonymous roofs were there. Read its box before quoting any buildable-ground figure |
| 1 | GROUND | **T-E3** | the heightfield east (= `S2e`, whose first pass already measured the box) · **it is now also the parcel T-E2's under-coverage assertion is waiting for** |

| — | GROUND | ~~T-E5(a)~~ | **DONE 2026-08-16** — the four in-town waters were deferred under one phrase and **three of the four are datable at the scene; the pond is not**. The sharpest finding is not the pond: **the scene draws the BRIDGE over the slough and not the slough**. On the square, date and extent are one question — a whole-block pond is refused by this project's own estray pen (**March 1832**) and log jail (**fall 1833**), and a partial one has no source. **No liberty owed, no grade moved.** Read its box before quoting any in-town water number |
| 2 | GROUND | **T-E5(b)** | how much of the square was wet — opened by T-E5(a), and its first question is whether any source states an extent at all. **NEEDS A BAKE** |

**THE TABLE ABOVE IS NEARLY OUT OF PICKS THIS RUNNER CAN CLOSE — counted 2026-08-16 by K28, and
stated here because the next run will otherwise spend a third of its budget rediscovering it.**
Of the numbered picks left standing, **T-V1(b), K30(c), T-E3 and R-W2c all say NEEDS A BAKE** and
cannot go green on the improve runner; **T-V2 and R-W1 are parked on `hold` PRs #135 and #125**;
**R-W4c(b2), T-I3(b) and R-M1b are blocked on the owner**; and **R-W5a2's own box says to take it
only when the lane has nothing sharper**. That leaves **R-W2b** — whose R-W2a finding 2 makes it a
schema change across 315 records with no source yet stating a roof covering, so it is larger than
"unblocked" reads — and **T-E5**, whose ground half also needs a bake though its research and
`docs/LIBERTIES.md` half does not. **The lane needs new parcels opened more than it needs the next
one picked**, and the bake-shaped backlog is the reason: four parcels are waiting on a nightly.

**T-E5 WAS THE LAST OF THOSE TWO AND IT IS TAKEN — 2026-08-16, T-E5(a).** The count above was
right and the paragraph's own advice is now the binding one: **the lane needs new parcels opened
more than it needs the next one picked.** T-E5's bake-free half is spent, its successor T-E5(b)
needs a bake, and every other numbered pick still sits behind a bake, a `hold` PR or the owner. So
the next runner-closable unit here is most likely **a parcel this file does not yet contain**, and
the honest way to find one is the way T-E5(a) found its own: read a deferral, a `not_modelled`
entry or a "deferred to parcel (c)" phrase and ask **what question it was never asked**. That is
where four of the last six findings came from.

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

### R-W1 — calibrated light and environment · **PARKED on PR #125 (`hold`) — DO NOT REDO**

**The work is done and measured; it is one assertion short of green.** Take the branch
`steward/r-w1-calibrated-light`, not a blank sheet.

> ### THE BLOCKER IS SETTLED. DO NOT RE-DERIVE IT.
>
> **A run burned its entire 150-minute budget on 2026-08-14 (`31848983349`) re-deriving this
> and was cancelled mid-smoke with nothing committed.** The answer below was obtained in one
> targeted measurement. Start from it.
>
> The PR named two candidate causes. **Cause 1 (the scene is 16 % dimmer) is CONFIRMED.
> Cause 2 (a near-uniform indirect specular term compressing road against grass) is REFUTED.**
>
> Measured with the gate's own probe construction at `from_above`, desktop 1280×800, source
> tree, `dev@d762a19` vs branch `9c69a93` — but recording **linear luminance** alongside ΔL\*,
> because the two causes have opposite signatures there: dimming is multiplicative and
> preserves the road/ground ratio; a specular pedestal is additive and collapses it.
>
> | band | Weber contrast dev → branch | ΔL\* | perceptible |
> |---|---|---|---|
> | 100–250 m (n=11) | 0.1217 → 0.1176 (**−3.4 %**) | 2.87 → 2.60 | 91 % → 91 % |
> | 250–600 m (n=326) | 0.0940 → 0.0904 (**−3.8 %**) | 2.36 → 2.12 | 63 % → **52 %** |
>
> Ground scales ×0.862, road ×0.866. **The ratio moved 0.4 %** — the road is physically as
> distinguishable as it was; the scene is darker and ΔL\* is compressive.
>
> **What actually fails is narrower than "the aerial band":** the median 2.12 clears the 1.8
> bar. It is the *fraction* bar in the farthest gated band only — **52 % perceptible against
> 55 % required**, a three-point miss. 100–250 m never moved.
>
> **Do not re-tune the street alpha.** It tunes content to a metric artefact, makes roads more
> contrasty than the sky lighting them warrants, and guarantees another re-tune at every
> lighting change — the streets were tuned under the rig this PR proved was 1.86× too bright.
>
> **The owner has ruled: the gate scores contrast plus a floor. See `R-M1`.** Once R-M1 lands,
> re-run this branch's gate against the new metric — do not re-tune the streets to satisfy the
> old one. Full working: `kevinrhaas/custom#125` (issue comment, 2026-08-14).

Everything else it needs is in the PR and in `docs/STATUS.md` § "the town was lit by a sky that
does not exist". Everything else in lane 1 (R-W4, R-W5, R-W2, R-W3) is untouched and free. Lane 1's other parcels
(R-W4, R-W5, R-W2, R-W3) are untouched by it and R-W4 is the one to take instead; any
lane-2 or lane-3 parcel may run alongside it, since this one touches only
`renderers/web/js/world.js`, `tools/smoke_renderer.mjs` and the vendor manifest.

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
| **R-W4b** | **the ring seam** | Self-contained, and the fix shape is already known from the sward (vary the radius per patch). `flora.js`. |
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
| **R-W5b** | **the water surface, post-lite, dynamic resolution** | RENDERING §1 item 13, EffectComposer/SMAA, and **R-BUG1** — the river edge that flickers when flying, which the owner reported. Owns `terrain.js`'s water material. |

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
at both viewports. **Carries R-BUG1 below** — the river edge flickers when flying, and this
is the parcel that owns the water surface.

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

### R-W5a2 — the last 16 batches → 1 · **UNCLAIMED · from R-W5a · Effort: S**

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
| **R-W2b** | **wire the sheet in** | Take R-W2a's committed sheet and make the params and records name its surfaces. **Files:** `generators/archetypes/*_params.py` · `data/structures/*.json` (material fields only). Re-derives through the generators' `--check`. |

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

### R-W2c — the chimney is roof-coloured on 199 buildings · **UNCLAIMED · opened 2026-08-16 by R-W2a · Effort: S–M**

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

### R-W3 — ambient occlusion and cascaded shadows · **UNCLAIMED · SPLIT**

**Phase:** RENDERING §4 W3 · **Effort:** M · **After:** R-W2

**The no-Blender work is THREE parcels — claim ONE. They are genuinely unrelated jobs that were
filed together only because RENDERING §4 groups them:**

| | parcel | scope |
|---|---|---|
| **R-W3a** | **the AO cage rule** | §1 item 10: the bake works end to end and fails because clapboard courses and window reveals a centimetre off the wall occlude each other (mean 0.265, 69 % of texels below half). It needs a **low-poly cage**, not tuning. **Files:** `docs/RESEARCH/ao-cage.md` (new) · `generators/archetypes/*.py` (cage emission). |
| **R-W3b** | **cascaded shadows** | `renderers/web/js/world.js` only — today one 1024² map on a ±60 m follow ortho, nothing beyond 60 m. **Touches no generator and no record**, so it shares nothing with 3a and can run beside it. |
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

### K30(c) — redraw the bodies onto the correct side of their own frontage · **UNCLAIMED · from K30(b) · NEEDS ONE BAKE · Effort: M**

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

#### T-V1(b) — the sixty North records · **NEXT UP · Effort: S to write, and it NEEDS ONE BAKE**

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

### T-V2 — the `south_water` anchor points at a field · **UNCLAIMED · NEXT UP · from R-G1**

**Phase:** lane 2, data only · **Effort:** XS — one record, no code

R-G1 scored composition **4** at `south_water`: about 60 % of the frame is foreground grass and
the business street the anchor is named for is a 40-pixel band on the horizon. An anchor a
visitor is offered from the navigation menu should show the thing it is named after. Move the
anchor in `data/scenes/1835.json` onto the street — the surveyed corners the sixteen South Water
records already carry are the coordinates to use — keep the pitch at 0, and re-shoot. **This
moves a camera, not a building**, and it is the cheapest point on R-G1's whole table.

**Watch:** `tools/critic_shots.mjs` drives the eight scene anchors through `goTo`, so moving this
one moves a baseline station. Re-shoot the full desktop and mobile sets and restate the
`south_water` row in the STATUS baseline table rather than leaving two incomparable numbers
under one name — the whole point of the harness is that two rounds can be compared.

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

### R-A1 — a road-legibility accessibility aid · **UNCLAIMED · UNBLOCKED 2026-08-15 by R-BUG3 — never instead of it**

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

### T-BUG2 — 79 ground vertices face downward · **UNCLAIMED**

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

### R-BUG1 — the river edge flickers when flying · **UNCLAIMED**

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

### K24 — Let the visitor choose the light · **UNCLAIMED · owner-requested 2026-08-14 · AFTER #125**

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
ell), then the fort group (whitewashed palisade on rising ground), then Sauganash/Wolf Point.

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

### K8 — River bank heights *(research first, then terrain)*
The owner: banks look too low against the fort views (10–20 ft with graduated slopes). The
dossier gives +2–4 ft banks at the forks (documented) but the FORT stood on distinctly rising
ground — "the flattened mound", the 1830 Harrison plan's bank, Swearingen's 18-ft pool at the
fort bend. Parcel: re-read `01-terrain-hydrology.md` and the primary accounts; raise and
GRADUATE the fort-reach south bank as the evidence supports; record the disagreement between
the tier-5 lithographs and the dossier rather than averaging it; keep the forks banks at their
documented height. Gradient audit re-run; exemption itemised like the others.

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
