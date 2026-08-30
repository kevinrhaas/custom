# The renderer gate's budget — what it costs here, and what covers what

**T-0235.** Three tickets — T-0170, T-0173 and T-0181 — reason about the desktop
legs' margin against a **30-minute** cap. That cap is not this machine's. The
steward runner has no GPU: chromium launches with `--enable-unsafe-swiftshader`
and rasterises on the CPU, and the whole gate was measured at **55 m 10 s**
unfiltered there on 2026-08-27, nearly twice the figure those three margins are
taken against.

And a steward run's single foreground command is capped at **600 s**, so no run
can take the gate whole. It takes the parts that cover what it touched — and
until this page, nothing said which those were. A run either spent more than its
entire budget on all fifteen staged commands, or picked by feel.

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
taken against the 30-minute cap) · ROADMAP § THE RUN BUDGET.
