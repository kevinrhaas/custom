# The temporal architecture

The mistake this document exists to prevent: building "Chicago 1835" as a thing, then
discovering that "Chicago 1848" means starting over.

## Three layers, three speeds

| layer | changes | modeled as |
|---|---|---|
| **Land** — elevation, shoreline, river channel, sloughs, ponds | slowly, in punctuated jumps (a harbor cut, a lakefront fill, the grade raising) | **terrain epochs** |
| **Structures** — buildings, bridges, piers, palisades | constantly | **records with dated phases** |
| **Living cover** — flora, fauna | seasonally and with settlement | **zones tied to an epoch, with ranges** |

A **scene** (`data/scenes/1835.json`) names a date and a terrain epoch. Everything resolves
against that date. Adding a year is a new scene file plus, if the ground moved, a new epoch.

## Terrain epochs

`data/terrain/epochs.json` is a registry of non-overlapping intervals. Each epoch owns a bundle
of vector layers and a heightfield spec.

```jsonc
{ "id": "e1834_harbor_cut", "from": "1833-07-01", "to": "1848-12-31",
  "note": "The cut through the bar is open; the old southward channel is decaying behind the spit.",
  "status": "active" }
```

Rules:

- Intervals must not overlap, and a scene's date must fall inside its epoch's interval.
- An epoch is a *state of the ground*, not a year. `e1834_harbor_cut` covers well over a decade
  because the ground did not meaningfully move again until the canal era.
- Only one epoch may be `active` at a time until the first milestone ships. Others sit as
  `planned` stubs so the shape is visible without inviting scope creep.

Planned epochs, in the order they matter:

| epoch | what changed |
|---|---|
| `e1830_natural` | pre-cut: the baymouth bar deflects the river south nearly half a mile; natural mouth near present Madison St |
| `e1834_harbor_cut` | **active** — piers and the cut through the bar; the old channel silting behind the sand tongue |
| `e1849_canal_era` | the I&M canal, wharfing, early fills |
| `e1856_grade_raise` | the city lifts itself out of the mud; the original ground surface is buried |
| `e1871_postfire` | the burnt district and the fills that followed |

## Why fast-changing works are structures, not terrain

The north pier grew from roughly 700 ft at the end of 1834 to 1,260 ft by the close of the 1835
season. If the pier were terrain, every few months of pier construction would need its own
epoch, and the epoch registry would become a calendar.

So: **terrain is the slow layer; anything that changes on a human project schedule is a
structure with phases.** Piers, bridges, wharves, and the palisade are structures. The sandbar,
the shoreline, and the slough are terrain.

## Structure phases

One identity, several forms over time. The Sauganash is the reference case:

| phase | range | what it is |
|---|---|---|
| `log_1829` | 1829 → 1831 | the one-story log Eagle Exchange, including its documented **move** after the 1830 plat put it in the middle of a platted street |
| `frame_1831` | 1831 → 1851 | the two-story white frame block with blue shutters, built onto the log core at Lake & Market |

Phases carry their own `position`, so a relocated building is native to the model rather than a
special case. Early Chicago moved buildings routinely — the Methodist meeting house was floated
across the river and rolled on logs to Washington & Clark in 1838.

Resolution rule, shared by the validator, the scene compiler, and the renderer: for scene date
`T`, exactly one phase must cover `T`. Zero phases means the structure is not in that scene.
Two means the data is wrong.

## Vertical datum

Internal working datum is **Z = 0.0 at the summer-1835 lake/river water surface**, in feet,
converted to meters at export. Export offset: `ASL = Z + 580.0`.

This is deliberate. The Chicago City Datum was established in 1847 against a low-water mark and
sits on an obsolete "mean tide New York" reference; mixing it with modern NAVD88 figures
introduces a systematic error of most of a foot in a landscape whose *entire* natural relief is
under fifteen feet. Pick one internal datum, convert once, and record the conversion.

Total relief across the whole modeled area is less than 15 ft. Flatness is the story — the
lakeshore sand ridge stands about 9–10 ft above the lake while the plain west of State Street
sits 2–3 ft above the river. A vertical-exaggeration toggle may exist in the renderer for
legibility, but it defaults **off**, and no zone is invented to make the terrain interesting.

## Horizontal datum

Working CRS **EPSG:26916** (UTM 16N, NAD83, meters); scene frame is local East-North-Up meters
from a fixed origin at the Chicago River forks at Wolf Point.

`data/datum.json` carries `verified: false` until the origin has been derived from the
georeferenced 1834 Wright and Hathaway maps, and **the generators and the bake refuse to run
while it is false.** Fixing the origin after geometry exists means regenerating everything, so
the build is designed to make that impossible rather than merely discouraged.
