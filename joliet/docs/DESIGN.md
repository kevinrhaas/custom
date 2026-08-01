# Design

## The spine

Greg has a drawing from Boyington's office, 1858, showing a vaulted void
beneath the east cell house. It is labelled only as a cistern. It appears on no
survey after 1910 — not the state plans, not the 2002 decommissioning documents,
not the museum's stabilisation report. Something was sealed, and then quietly
erased from the record.

The crew's stated goal is the tower at dawn. The real goal, the one that keeps
escalating, is finding out what is under the east block.

The answer is **institutional, never paranormal**: a sealed punishment level
from the era when inmates hand-quarried the limestone that built the walls they
were kept behind — with their names cut into the stone by their own tools. The
building was made by the people it consumed, and someone bricked over the proof.
Every ambiguous beat has a mundane explanation available. The horror is the
record-keeping.

*(The void itself is fiction. The convict-quarried limestone is not. See
`HISTORICAL-LIBERTIES.md` §3 — the game tells the player which is which.)*

## Roles are data, not four campaigns

One level geometry. `RoleConfig` objects drive ability flags, stamina curves,
highlight filters, dialogue barks and **starting spawn point within the same
first level**. There is no second content pipeline.

| Role | Wants | Flaw | Wrong about | Mechanic |
|---|---|---|---|---|
| **Greg** — the Director | The void confirmed and documented so the history can't be sanitised again | Treats the building as an artifact and the people in it as footnotes; will push the crew into real danger for a photograph | That documentation is the same thing as accountability | **Architectural Insight** — overlays period blueprints on the live world, ghosting structural weak points, sealed openings, original vs. later construction |
| **Mike** — the Veteran Guard | To walk out having proven to himself the place is just a building now | He already suspects what's down there and doesn't say until forced | That he can visit without it costing him | **Institutional Knowledge** — bypasses mechanical locks, calls patrol and camera geometry from memory, and his commentary lowers crew stress |
| **Jsn** — the Documentarian | The shot nobody else has | Frames risk as content; the camera is how he avoids feeling anything | That the footage will mean the same thing to viewers as it does to him | **Tech & Optics** — thermal and low-light, LIDAR-style scan that reveals cavities behind masonry, and a battery economy forcing a choice between seeing and recording |
| **Lonnie** — the First-Timer | To not be the reason something goes wrong | Defers to whoever sounds most certain | That he's the least useful person there — he's the only one who reacts to it as a place where people suffered | **Adrenaline** — stamina recovers faster under stress; improvised solutions surface to him that others can't see |

## The crew is always with you

You play one. The other three are live on radio for the entire run. This solves
"where did the other three go", makes the role choice a *perspective* rather
than a fork, and lets the scenes teach history through argument instead of
monologue.

Banked bark categories: collectible proximity · puzzle stall (escalating toward
a hint) · near-miss · first-time-in-a-room reaction · inter-character friction
that shifts with what the player has found.

Radio degrades with depth and stone. Dropouts and static are a **diegetic**
signal that you're going too far — not a compression artefact.

## "Fun and not too hard" is a spec

Operationalised, and testable:

- Checkpoints every **60–90 s**.
- **No instant-fail, anywhere.** A missed water-balance check costs stamina and
  makes noise; it does not kill.
- Detection is a **2-stage warn-then-reset**. Never restart-from-scratch.
- A contextual hint surfaces after **3 failures or 90 s of no progress**.
- Traversal and climbing use forgiving hitboxes and assist snapping.
- Exhaustion **slows** you, it never stops you.
- The headlamp browns out and flickers at low battery; it never cuts to black.
- Every scene logs **time-to-first-frustration** in playtest.

## Suspense without combat

There are no weapons and no enemies. Tension comes from darkness, sound,
structural instability, wildlife, and battery/light management. Nothing in this
game shoots back, and nothing ever will.

## Collectibles

~25 historical documents, photographs and audio logs. Each is tied to a **cited
fact** in `RESEARCH.md`. They are the reward loop and the vehicle for the real
history.

## Scene list

| Scene | Status | Note |
|---|---|---|
| 1.1 Perimeter Approach | look-dev lock | Three entries: drainage trench (wet/fast/loud), wall breach at the quarry cut (exposed, needs a climb), maintenance gate (Mike's knowledge or a lockpick). Teaches the whole movement vocabulary under zero pressure. |
| 1.2 The Siphon | planned | Chest-deep water, shifting cinder blocks, a rising-water timer driven by an audible storm above. Pressure without a fail state. First collectible: a 1970s work order referencing "the east cistern — do not open." |
| 2.1 The Powerhouse | planned · **never cut** | Two conduits, both plausible, one mislabelled by a period sign that was accurate in 1901 and isn't now. The wrong turn is the *player's misread*, not a cutscene. Sequence the boiler valves and relay board and **lights come on across the map, permanently.** Earn the lighting. |
| 2.2 Armory Spiral | stretch | Where Mike goes quiet, and where Jsn's scan first picks up a cavity behind the stone at the wrong depth. |
| 3.1 The Cellblocks | planned · **never cut** | The showpiece. Five tiers, hollow acoustics, every footfall carrying. Greg's overlay and Jsn's scan **disagree**; reconciling them is the puzzle. |
| 3.1b The Void | planned · **never cut** | The climax. Tight, silent, hand-cut stone, names and dates. No jump scares. Let the player read the walls. The critic loop protects this scene first. |
| 3.2 Maintenance Ladder | stretch | Ascent as release after the Void — sky, wind, air. About relief, not tension. |
| 4.1 The Guard Tower | planned · **never cut** | Choose what to do with what you found: publish, hand it to the museum quietly, or take nothing out. Mike argues one way, Greg another, Jsn a third; Lonnie asks the question that actually matters. No option is punished — they resolve differently. |
| 4.2 Exit | planned · **never cut** | Epilogue keyed to that choice plus collectibles found, with real end cards about the site's history and preservation status. |

**Cut order if time runs out:** 2.2 → 3.2 → alternate 1.1 entries → roles 3 and 4.
**Never cut:** 1.1, 2.1, 3.1, 3.1b, 4.1, 4.2.

## Accessibility — ship requirement, not stretch goal

- Subtitles **on by default**, with speaker names, scalable.
- Remappable keys; full gamepad parity.
- Head-bob and motion blur independently adjustable to zero; `prefers-reduced-motion` respected on first run.
- High-contrast interaction prompts.
- **No pure-audio-only puzzle gates** — every audio cue has a visual channel.
- Colourblind modes (protan/deutan/tritan).
