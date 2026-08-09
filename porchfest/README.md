# Porchfest Planner

A walking-route planner for **Uptown Porchfest** (Lowry Hill East / The Wedge,
Minneapolis) — Saturday 15 August 2026. 91 bands play overlapping sets across 33
porches in about six blocks; this works out where you should actually stand, and
when.

This folder is the **source and build pipeline**. The published output lives in
the deployed `site/` tree (same split as `hosta/`):

- `../site/porchfest/index.html` — marketing page (hand-maintained)
- `../site/porchfest/app/index.html` — **the whole app, one self-contained file** (~262 KB), generated
- `app.template.html` — the app source; everything but the data
- `data.json` — the baked payload injected at build time

## The app is one file, on purpose

The app inlines its CSS, its JavaScript and its entire dataset. Once the
page loads it makes **zero network requests** — no tile server, no CDN, no fonts,
no API. That buys three things that matter at a street festival:

- it works on a saturated cell tower, or with no signal at all;
- a shared plan is just a URL — no backend, no account, nothing to keep running;
- there is no third-party rate limit or API key to expire between now and August.

Band photos are the one deliberate exception: they hotlink the festival's own S3
bucket and degrade to the band's initials if they don't load.

## How it plans

Picking a route is an **orienteering problem with time windows** — choose a
subset of sets and an order that maximises taste-match, subject to walking times,
each band's set window, your finish time, and an optional band count. The solver
is randomised greedy insertion plus a swap local search, best of N runs.

**It re-plans as you touch anything** — no build button. Input is debounced to
the moment you pause, then two passes run: a fast one (14 restarts, ~25 ms) for
immediate feedback, and a thorough one (56 restarts) a beat later that only
replaces the route if it genuinely scored better, so the map doesn't churn for
nothing. The button shuffles to a different good answer at full effort.

**Band count** is a hard "at most" and a soft "at least": exceeding the cap is
impossible, while falling short of the floor costs 400 points per missing band,
so any route that makes the number outranks every route that doesn't — and when
the clock genuinely can't fit them, you get the best short route plus a warning
rather than nothing.

Walking distances come from a **pedestrian graph of the real street network**
baked into the page (511 nodes, 594 edges), with Dijkstra for both distance and
the drawn path. Porches snap to the nearest point on the nearest street segment,
so a porch sits on the road out front rather than at the corner. Distances were
validated against an OSRM foot matrix: median error 3.1%, and biased slightly
long because the graph deliberately omits alley cut-throughs.

The map is hand-drawn SVG from the same baked street data — which is why it needs
no tiles, themes correctly in light and dark, and can cluster its own pins.

## Ten dimensions

Every band is rated 1–5 on: **energy, loudness, tempo, electronic, vocals,
danceability, experimental, brightness, grit, kid-friendly**, plus 2–5 genre tags
from a controlled vocabulary. Each dimension is one slider centred on "don't
care", so you nudge only what you have an opinion about.

Ratings and profiles were produced by research agents working from the band's own
Bandcamp/Spotify/press presence against `build/SPEC.md`, then validated for range
and vocabulary. Confidence is recorded per band — 37 high, 39 medium, 15 low —
because plenty of these acts have almost no web footprint, and an honest thin
profile beats an invented rich one. **They are generated summaries, not
journalism.**

## Rebuilding

Each step is independent; run only what changed. Requires network for 1–4.

All paths are relative to this folder.

```
node scrape.mjs         # 0. lineup from the festival bundle -> lineup.json
node geocode.mjs        # 1. porch addresses -> lat/lon (Nominatim)
node build-matrix.mjs   # 2. street corners (Overpass) + an OSRM foot matrix to validate against
node build-streets.mjs  # 3. street network -> streets.json
node build-data.mjs     # 4. merge lineup + profiles + geo -> data.json
node build-app.mjs      # 5. inject data into the template -> ../site/porchfest/app/index.html
node smoke-test.mjs     # 6. the ship gate
```

Editing `app.template.html` only needs step 5.

The lineup is scraped from the festival's JS bundle, where the full band list is
embedded as a `JSON.parse('…')` literal — no HTML scraping, so it survives a
restyle but not a data-layer change (`scrape.mjs` fails loudly if the shape moves).

Band profiles (`profiles.merged.json`) are the one step no script reproduces:
they came from research agents following `SPEC.md`. Re-run that only when the
lineup changes.

## Smoke before ship

`node smoke-test.mjs` — Chromium **and** WebKit, 390×780 and desktop, zero
pageerrors, zero console errors. It asserts the things that actually break: a
route exists on load with nothing clicked, moving a dial re-plans on its own,
"exactly 6" / "3–5" / "at most 4" are obeyed, avoiding a genre drops it from the
route live, every stop sits inside its set window, the schedule is
chronological, every stop is pinned on the map, **no two pins overlap**, share
links round-trip, the toast doesn't stretch, and the primary action clears the
mobile tab bar. Mobile is a release gate.

If an engine is missing locally the suite says so loudly and keeps going; under
`CI=1` a missing engine fails the run.

## Attribution

Lineup, set times, porch addresses and photos: [uptownporchfest.com](https://uptownporchfest.com/bands).
Geocoding: [Nominatim](https://nominatim.openstreetmap.org).
Street network, corners and walking distances: [OpenStreetMap](https://www.openstreetmap.org/copyright)
contributors (ODbL), via Overpass and OSRM.

An unofficial fan project, not affiliated with the festival.
