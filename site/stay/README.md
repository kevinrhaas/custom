# Stay Finder (`site/stay/`)

A ranked, mapped shortlist of **6–8 bedroom houses for December 19–27, 2026**
across the Tampa Bay region — published at
`https://kevinrhaas.github.io/custom/stay/`.

The brief: somewhere for a multi-generational group of 12–18 to be under one
roof at Christmas, six to eight bedrooms, **king beds in as many of them as
possible**, anywhere from Cedar Key down to Siesta Key and inland to Crystal
Springs. "A house or other cool accommodations" — so estates, ranch compounds
and whole-inn buyouts count alongside plain beach houses.

**87 properties across five areas**, found by five research passes run in
parallel:

| Area | Found | What it's good for |
|------|-------|--------------------|
| Tampa / St. Pete / Clearwater metro | 23 | The deepest 6–8BR inventory, and the only listings with real quoted prices for these dates |
| Gulf beaches & barrier islands | 20 | The big king-bed beach houses — Anna Maria and Siesta Key dominate |
| Cedar Key, Crystal River, Homosassa | 14 | Old-Florida character and December manatee season; thin at this size |
| Crystal Springs, Dade City, Lakeland, Ocala | 17 | Acreage, ranches and space per dollar |
| Estates, inn buyouts and compounds | 13 | The unusual: whole-inn buyouts, island inns, historic mansions |

## Files

```
index.html          The app (static, no build step, no dependencies)
css/app.css         Gulf Coast skin (aurora backdrop, light/dark, sticky map column)
js/data.js          FACTS ONLY — the 88 listings (auto-generated)
js/geo.js           Map geometry: coastline, bays, lakes, rivers (auto-generated)
js/app.js           Rendering + fit scoring + filters + the map
raw-<region>.json   Raw research output, one file per area (compiler input)
build_data.mjs      Compiler: validate, dedupe, attach local photos, write js/data.js
tools/build_geo.py  Map geometry builder — clips and simplifies US Census TIGERweb
tools/fetch_photos.py  Saves one hero photo per listing into photos/
photos/<id>.jpg     Local listing photos, downscaled (53 of 87 had a usable image URL)
```

## Regenerating

```
node build_data.mjs          # raw-*.json  -> js/data.js
python3 tools/fetch_photos.py   # refresh photos/ from the listing image URLs
python3 tools/build_geo.py      # only if the map frame changes (needs the TIGERweb downloads)
```

## The map

Plain SVG with no tile server and no map library, the same approach as the
Porchfest route map. Geometry comes from **US Census TIGERweb** (public domain)
and is baked into `js/geo.js` at build time:

- **land** from `USLandmass` — the shoreline-clipped state polygon
- **water** from `Hydro` areal hydrography — bays, sounds and coastal water
- **lakes** and **named rivers** from the same service

Paint order carries the whole thing: the frame fills with water, land paints on
top, then bays and passes carve back out. That order is not cosmetic — TIGER's
coastal water stops at the 3-mile county limit, so the open Gulf can only come
from the frame fill, and painting water last is what puts Boca Ciega Bay behind
the barrier islands instead of drowning them. Each feature paints as its own
even-odd path, so islands survive as holes and neighbouring county polygons
never cancel each other into phantom land.

Checked against unsimplified TIGER on a dense grid through the most intricate
stretch of coast (Treasure Island / Boca Ciega Bay): **96.9% agreement**, with
disagreements confined to about a kilometre of boundary wobble. Anna Maria,
Siesta Key, Clearwater Beach and Treasure Island all resolve correctly as land.
Islands under roughly a square kilometre — Cabbage Key, Useppa — are below the
source's resolution and are not drawn; their pins sit on the sound, which for
boat-only islands is honest enough.

## Ranking

`js/data.js` holds facts only; every judgement lives in `js/app.js`. The fit
score weights bedroom count in the 6–8 band first, then the **king ratio**
(kings ÷ bedrooms), then sleeping capacity, a *heated* pool (an unheated one is
decor in December), water frontage, an elevator (multi-generational groups and
stairs), and evidence that the dates are actually open. Compounds are penalised
slightly — several keys means several conversations.

Tiers: **Best fit** (6–8BR with kings in 60%+ of rooms) · **Strong** (right
size, kings partial or unpublished) · **Worth a look** (right size, not king
beds) · **Stretch** (outside the band, or several keys).

A listing that never published its bed layout is scored as *unknown*, never as
zero kings — 28 of the 87 are in that position and their cards say so.

## What is and isn't verified

**No live calendar was read.** Every rental platform blocks automated checks, so
availability is reported as exactly what was seen and nothing more:

- **20 listings** — "came back in a Dec 19–27 search". Airbnb's dated search
  pages were reachable with a browser user agent, and the embedded state carried
  real 8-night totals, coordinates and per-bedroom bed configurations **for the
  actual trip dates**. These prices are genuine quotes for Dec 19–27, 2026.
- **67 listings** — "unknown". Found and read, dates not checkable.
- Prices elsewhere are whatever the source published — often a shoulder-season
  nightly rate or a published range, **not** a Christmas-week quote, which will
  usually be higher.

Nothing here is a booking. Confirm dates, bed layout and the real holiday rate
with the host or manager before counting on any of it.

## Findings worth keeping

Three results from the search that are as useful as the listings themselves:

- **Crystal Springs itself has essentially nothing.** It is a roughly one-square-mile
  hamlet wrapped around the privately held Crystal Springs Preserve, which does
  not rent nightly. Every platform's "Crystal Springs" page re-serves Zephyrhills
  and Dade City inventory. The two genuine 6BR options in Dade City proper are
  both in this list.
- **Cedar Key has no 6-bedroom houses.** Both dominant island agencies were
  enumerated: the ceiling is 4BR sleeping 10–12. Cedar Key works for a group of
  this size only as a multi-unit block through one manager, or via the one
  private-island compound in the list.
- **The northern Pinellas beaches and the luxury Tampa/St. Pete peninsulas are
  dead zones at this size.** Clearwater Beach through Pass-a-Grille is condos and
  3–4BR houses; Davis Islands, Snell Isle, Old Northeast and Tierra Verde are
  owner-occupied with almost no large short-term rental stock. Not worth more
  hunting.
