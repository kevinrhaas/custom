# Stay Finder (`stay/`)

A ranked, mapped shortlist of **5–6 bedroom houses for December 19–27, 2026**
across the Tampa Bay region. The app is in [`site/stay/`](../site/stay/) and
publishes to `https://kevinrhaas.github.io/custom/stay/`.

The brief: somewhere for **nine people** to be under one roof at Christmas —
three couples plus three adult children in their twenties. Five or six
bedrooms, **exactly three kings, one per couple**, anywhere from Cedar Key down
to Siesta Key and inland to Crystal Springs. "A house or other cool
accommodations", so estates, ranch compounds and whole-inn buyouts count
alongside plain beach houses.

Three kings is a target, not a maximum. A seven-king house is not a better
answer than a three-king house — the twenty-somethings want a decent queen,
not another master — and a house built for eighteen is the wrong house even
when its bedroom count fits. Both of those are encoded in the ranking.

**168 properties across five areas**, found by two rounds of five parallel
research passes — the first at 6–8 bedrooms, the second re-run at 5–6 after the
group turned out to be nine rather than sixteen:

| Area | Found | What it's good for |
|------|-------|--------------------|
| Tampa / St. Pete / Clearwater metro | 40 | Deepest inventory, and North Pinellas is the best value anywhere — 5BR houses with docks and fireplaces at $3.6–8k for the week |
| Gulf beaches & barrier islands | 39 | Indian Rocks Beach is the strongest single market at this size; Anna Maria and Siesta Key cost roughly double for the same shape |
| Cedar Key, Crystal River, Homosassa | 28 | Old-Florida character and December manatee season at Kings Bay |
| Crystal Springs, Dade City, Lakeland, Ocala | 36 | Acreage and space per dollar, but cold pools in December |
| Estates, inn buyouts and compounds | 25 | Five-room inn buyouts — often three kings already, because inn rooms are kings far more often than house bedrooms are |

**114** are inside the 5–6 bedroom brief and **62** of those are right-sized for
nine (sleeping 9–12 rather than 16–20). **89** carry a real eight-night price
quoted by the platform for Dec 19–27 specifically. Eight-night totals run
$2,495 to $24,815, median $7,680 — the spread at identical bedroom counts is
enormous, which is most of the value in having the list at all.

## Layout

Source, research and tooling live here in `stay/`; only the published app is
under `site/`, the same split `porchfest/` uses.

```
stay/
  README.md              This file
  raw-<region>.json      Round-one research (6-8 bedroom brief), one file per area
  raw-<region>-nine.json Round-two research (5-6 bedrooms, nine people)
  build-data.mjs         Validate, dedupe, attach photos -> site/stay/js/data.js
  build-geo.py           Download + clip US Census TIGERweb -> site/stay/js/geo.js
  fetch-photos.py        Save one hero photo per listing -> site/stay/photos/
  build-artifact.py      Bundle the app into one self-contained page
  geo-cache/             Cached TIGERweb downloads (gitignored, ~20 MB)

site/stay/               The published app — static, no build step, no dependencies
  index.html
  css/app.css            Gulf Coast skin (aurora backdrop, light/dark, sticky map column)
  js/data.js             FACTS ONLY — the 87 listings (generated)
  js/geo.js              Map geometry: coastline, bays, lakes, rivers (generated)
  js/app.js              Rendering + fit scoring + filters + the map
  photos/<id>.jpg        Local listing photos, downscaled (132 of 168 had a usable image URL)
```

## Regenerating

Every generated file is reproducible from what's in this folder:

```
node build-data.mjs        # raw-*.json           -> site/stay/js/data.js
python3 build-geo.py       # TIGERweb (cached)    -> site/stay/js/geo.js
python3 fetch-photos.py    # listing image URLs   -> site/stay/photos/
python3 build-artifact.py  # the app              -> site/stay/artifact.html
```

`build-geo.py` downloads about 20 MB from TIGERweb on first run and caches it in
`geo-cache/`; delete that folder to force a refetch. It reproduces `geo.js`
byte-for-byte.

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

`site/stay/js/data.js` holds facts only; every judgement lives in
`site/stay/js/app.js`.

The fit score weights the 5–6 bedroom band first, then **kings toward three and
no further** — `min(kings, 3)`, so a fourth king earns nothing — then capacity
scored *against the group rather than maximised*: sleeping 9–12 gains, sleeping
16+ loses, and so does an eighth bedroom. Bunk rooms lose points, because these
are nine adults. After that: a *heated* pool (an unheated one is decor in
December), a fireplace, water frontage, an elevator, and evidence the dates are
actually open. Compounds are penalised slightly — several keys means several
conversations.

Tiers: **Best fit** (5–6BR with three or more kings) · **Strong** (right size,
kings partial or unpublished) · **Worth a look** (right size, no kings listed) ·
**Stretch** (outside the band, or several keys).

A listing that never published its bed layout is scored as *unknown*, never as
zero kings — 38 of the 168 are in that position and their cards say so.

## What is and isn't verified

**No live calendar was read**, and nothing here is a booking. Availability is
reported as exactly what was seen:

- **89 listings — "Priced for Dec 19–27".** Airbnb's dated search pages are
  reachable with a browser user agent, and the embedded state carries a costed
  **eight-night total for these exact dates**, plus coordinates and room-by-room
  bed configurations. The platform's own engine costed the stay, which is the
  strongest evidence obtainable without booking — but someone else can still
  take the house tomorrow.
- **79 listings — "unknown".** Found and read; the calendar was not reachable.
  Prices on these are whatever the source published, often a shoulder-season
  rate, **not** a Christmas-week quote, which will usually be higher.

One trap worth naming: **a house missing from a dated search is not proof it is
booked.** A holiday minimum-stay rule can exclude an empty house from an
eight-night December search. Several Cedar Key houses appear in a November
dated search but not the December one, and that ambiguity is a phone call, not
a write-off.

## Findings worth keeping

Results from the search that are as useful as the listings themselves:

- **Three kings is scarce.** Of 171 listings checked in the Tampa metro alone,
  roughly eight had three kings *and* sensible capacity. The ideal configuration
  is genuinely rare, which is worth knowing before holding out for it.
- **Cedar Key does work — the earlier "no 6-bedroom houses" finding was an
  artifact of searching at the wrong size.** Searching the island at 5–6
  bedrooms turns up three genuine 5BR houses plus three 4BRs that really sleep
  10–12. Five is the true ceiling: one agency has ~90 properties with exactly
  one at 4BR+.
- **Indian Rocks Beach is the best beach market at this size**, and was a dead
  zone at 6–8. Mid-size elevated pool homes on the Intracoastal, mostly capped
  at 10 guests, at $8–14k for the eight nights against $17–28k for equivalent
  Siesta Key stock. North Pinellas — Palm Harbor, Dunedin, Safety Harbor, Lake
  Tarpon — is the best value in the whole search at $3.6–8k.
- **Crystal Springs itself has nothing.** A roughly one-square-mile hamlet
  wrapped around a privately held preserve that does not rent nightly; every
  platform's "Crystal Springs" page re-serves Zephyrhills and Dade City. The
  closest bookable house is four miles away in Zephyrhills — the only 5BR in
  that town.
- **The prestige neighbourhoods are empty at any size.** Twelve extra searches
  across Davis Islands, Snell Isle, Old Northeast, Shore Acres, Tierra Verde and
  Bayshore added exactly one listing between them. Owner-occupied streets, not a
  rental market.
- **Heated pools need confirming, especially inland.** Platform amenity data
  states "heated" for only a minority; elsewhere the listing title claims it and
  the structured data does not back it. Inland, exactly one house checked stated
  a year-round heated pool in writing.
