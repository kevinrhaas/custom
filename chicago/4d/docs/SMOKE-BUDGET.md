# The renderer gate's budget — what it costs here, and what covers what

**T-0235**, corrected by **T-0435**. A steward run's single foreground command is
capped at **600 s**, so no run can take the gate whole. It takes the parts that
cover what it touched — and until this page, nothing said which those were. A run
either spent more than its entire budget on all fifteen staged commands, or
picked by feel.

## Three caps, and they are three different quantities (T-0435)

This page opened by reading a 55-minute unfiltered pass against a 30-minute cap
and concluding the cap "is not this machine's". Both halves of that were wrong,
and the correction is measured rather than argued.

| cap | what it bounds | value | where |
|---|---|---|---|
| the foreground-command ceiling | ONE `node tools/smoke_renderer.mjs …` a run blocks on | **600 s** | the agent harness |
| the **leg** cap | ONE matrix job of the nightly gate — one viewport, one range of parts, **eight legs in parallel** | **30 min** | `chicago-4d-bake.yml` § `smoke`, `timeout-minutes` |
| the reference pass | both viewports, unfiltered, one process | **90 min** | `chicago-4d-smoke.yml`, `timeout-minutes` |

The 55 m 10 s measured on 2026-08-27 is **all eight legs' work in one process**.
The 30 minutes governs **one leg**. Neither figure bounds the other, and "nearly
twice the figure those margins are taken against" compared a whole to a part.
T-0170, T-0173 and T-0181 are reasoning about the leg cap, correctly.

**And it is the same machine.** `steward-improve.yml`, `chicago-4d-bake.yml`
§ `smoke` and `chicago-4d-smoke.yml` are all `runs-on: ubuntu-latest` — 4 × AMD
EPYC 7763, 15 GiB, **no GPU**, so chromium rasterises on SwiftShader in all
three. The A/B, on `dev` at `415909cf`, same leg against the same bytes:

| mobile `SMOKE_STAGE=1-2 --published` | |
|---|---|
| bake runner — run 33290607360, `Smoke the published mirror` step | **4 m 40 s** |
| improve runner — T-0435 | **4 m 44 s** |

1.4 per cent apart. The control is real rather than incidental: that bake
produced no changes (`open-pr` skipped), so the mirror it smoked out of its own
artifact is `dev`'s committed mirror byte for byte. **So the desktop figures in
T-0167, T-0170, T-0173 and T-0181 do describe the machine the gate runs on**, and
none of them needs re-measuring on that account.

**What moves a reading is LOAD, not hardware.** T-0215 measured the same tree
twenty times slower on a busy box than a quiet one; part 10 took **2 m 53 s** at
desktop on 2026-08-30 against T-0167's **6 m 10 s** for the same 28 checks six
days earlier. That is why `dev-smoke-state.json` stamps cpu count and load
average on every record, why `smoke_budget.mjs` reports a median, and why a part
must never be re-cut off a single reading.

## What the eight legs cost, measured (T-0435)

`smoke_budget.mjs` reads per-PART readings out of the standing record and names
the six desktop parts that have none. The **legs** — the four ranges
`1-2 3-6 7-8 9-11` the nightly gate actually runs — have no gaps at all, because
every one of them runs every night. From run 33290607360 (2026-08-30), the
`Smoke the published mirror` step alone, not the job:

| leg | mobile | desktop |
|---|---|---|
| `1-2` | 4 m 40 s | 8 m 36 s |
| `3-6` | 7 m 02 s | 12 m 23 s |
| `7-8` | 6 m 39 s | 12 m 04 s |
| `9-11` | 9 m 14 s | 17 m 28 s |
| **total** | **27 m 35 s** | **50 m 31 s** |

Three readings follow. The whole **mobile** half is four commands and every one
fits the 600 s ceiling — a run that changed something mobile-wide can take that
half entire. Three of the four **desktop** legs are over the ceiling, so desktop
is taken part by part, which is what the map above is for. And the whole staged
gate is **78 m 06 s** of compute against the 55-minute unfiltered pass, because
it pays eight boots where that pays two: the price of the cut, not a regression.
The worst leg, desktop `9-11`, has 12 m 32 s of margin under the 30-minute leg
cap.

Two things follow, and both are tools rather than prose, because a table of part
numbers rots the first time the parts are re-cut — which has happened four times
in 2026 (T-0060, T-0121, T-0167, T-0346).

```
node tools/smoke_budget.mjs                    # what the gate costs on this machine
node tools/smoke_budget.mjs --for <path>…      # the parts that cover those files
node tools/smoke_budget.mjs --for-diff         # the same, off your own diff vs origin/dev
node tools/smoke_budget.mjs --self-test        # the map has not rotted (runs in check.sh)
```

## Where the seconds come from

Every figure is READ out of `tools/dev-smoke-state.json` — the standing record
T-0216 built — filtered to readings taken on `host.kind: steward-runner` against
the published mirror, and reported as the median of the readings for that part.
Nothing on this page is asserted, nothing is a bar, and a part with no reading is
named as having none rather than given a plausible number. As readings
accumulate the figures move on their own; file the smoke you ran anyway:

```
node tools/dev-smoke-state.mjs record /tmp/smoke-desktop4.log
```

**The numbering changed on 2026-08-30** (T-0346 cut old part 4 into 4 + 5 + 6 and
renumbered old 5-9 to 7-11). Readings filed before that merge are labelled in the
old numbering and the tool RENUMBERS them rather than discarding them: the
content of old part 5 is the content of new part 7, so the reading is a reading
of new part 7. Old part 4 is the one case that cannot be renumbered to a single
part — it is a reading of 4 + 5 + 6 together and is reported as the group.

## The recipe is conservative by construction

The map in `tools/smoke_budget.mjs` can only ever ADD parts:

- a path the map does **not** know maps to **the whole gate**, so a module nobody
  wrote a row for makes the recipe bigger, never quietly smaller;
- a path the map knows reads **no** part of the body — the gate's own tooling,
  the backlog, prose — says `NO PART` explicitly, which is a different statement
  from "unmapped", and still earns one cheap staged pass per viewport, because
  boot, the page-error check and the vendor checks are taken in **every**
  invocation whichever stage is asked for;
- `--self-test` fails if a mapped path has vanished from the tree, if any part
  1..11 is covered by no row, if `PARTS` in `smoke_renderer.mjs` has moved out
  from under the map, if the renumbering arithmetic breaks, or if an unmapped
  path ever stops meaning the whole gate. `check.sh` runs it.

**One limitation, stated rather than worked around.** `tools/publish.sh` restamps
the build id into `site/chicago/4d/walk/index.html` on every publish, and that
file is the page itself — every part clicks its markup — so it maps to the whole
gate. A published change will therefore always be told "the whole gate", even
when the only edit to that file is the one stamp line. The map is path-based and
cannot tell a stamp from a markup change, and making it guess would be a way to
shrink a gate quietly. **Read the diff.** If `walk/index.html` differs only in
its `gate-build` line, the parts your other paths name are the recipe, and say so
in the PR.

**A staged run is not the gate**, and it says so on its own first line. The gate
is both viewports, every part. What this page buys is the ability to spend ten
minutes on the parts that could possibly have moved, instead of spending nothing
because the whole thing did not fit.

## What each part covers

The map's rows are justified by the parts' own section headings in
`tools/smoke_renderer.mjs`. In outline:

| part | what it takes |
|---|---|
| 1 | the town count, water anchoring, the enclosure layer, the pound, the dooryard pickets, the lot-line fences, the plantings, the fort stockade, the business signs and what they say |
| 2 | the yard goods, the wagons, the building material, the frontage layer, the plank walk, the street edge, the wharves and walking one, the boats, the confidence view |
| 3 | the ground faces the sky, the ground the town stands on, the residents' names, the level prose, pick → provenance, the dossier link, the liberties on the card, who was here |
| 4 | the raycast pick, walking, standing, the bridge decks, the touch backend, the budgets, life size, nothing hovers |
| 5 | the scene-detail ladder, and nothing else (T-0346 cut it out on its own) |
| 6 | the gate and the chrome, and the confidence menu's own clicks |
| 7 | navigation and its readouts, the road-legibility aid, the batch merge |
| 8 | the facade tones, the shadow reach, the shadow box, the brightness aid |
| 9 | the flora census, the sward, the horizon timber, the streets a visitor reads |
| 10 | eye height, typing is not driving, the Go-to tab, What's-new |
| 11 | the Evidence panel — liberties, people, wildlife, what grows, what is not here, researched-and-open, what the ground claims — free-fly, and inspecting from the air |

## The zero-byte log, which is why a green run got killed

`node` block-buffers stdout **to a pipe**. A smoke redirected through a pipe
therefore writes nothing at all until the process exits, so a long staged run
looks identical to a hung one for its entire life. On 2026-08-27 a run watching
41 minutes of zero-byte log killed the smoke **one minute from its finish**, as
the flushed fragment showed afterwards.

**Redirect to a real file and tail it.** Never pipe a smoke you intend to watch.

```
SMOKE_VIEWPORT=desktop SMOKE_STAGE=5 node tools/smoke_renderer.mjs --published > /tmp/smoke-d5.log 2>&1
```

`SMOKE_TIMING=1` stamps every check line with the elapsed clock. Turn it on when
you are profiling a part rather than gating one: a part that BREACHES the ceiling
is killed before it prints its wall clock, so the parts most worth cutting are
exactly the ones a plain run learns nothing about.

## Related

`docs/PIPELINE.md` (where a green gate sends the work) · `AGENTS.md` § How work
ships · T-0216 `tools/dev-smoke-state.mjs` (the record these figures are read
from) · T-0346 (the last re-cut) · T-0170, T-0173, T-0181 (the three margins
taken against the 30-minute LEG cap — which is the right cap for them to take)
· T-0435 (the three caps, and the two-runner A/B) · ROADMAP § THE RUN BUDGET.
