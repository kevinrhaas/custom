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

Band photos used to be the one exception, hotlinking the festival's S3 bucket.
They are local now (see below) and still degrade to the band's initials if they
don't load.

## Band photos are local

`python3 fetch-photos.py` downloads each photo once and writes a card-sized
thumbnail to `../site/porchfest/app/img/<id>.jpg`. Needs `Pillow` and
`pillow-heif`. It skips anything already fetched; `--force` re-fetches.

The originals are full-resolution camera JPEGs — around 5000px wide and several
megabytes each, one of them 24 MB. Browsing the lineup pulled **304 MB** off
someone else's bucket, over the same saturated cell tower this app exists to
avoid needing. The thumbnails come to **2.8 MB total, 0.9% of that**.

Three photos are HEIC straight off an iPhone. Those never displayed at all
outside Safari, since Chrome and Firefox cannot decode HEIC — converting them
here fixes them rather than merely relocating them.

They stay as files rather than base64 inlined into the page. Routing already
works with zero requests because the street graph and every set time are in the
payload; photos are decoration that loads lazily as you scroll the browser.
Inlining ~2 MB would slow the thing that matters to speed up the thing that
doesn't.

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
node build-draw.mjs     # 4. profiles -> draw.json (how big a name each act is)
python3 fetch-photos.py # 5. band photos -> local thumbnails + photos.json
node build-data.mjs     # 6. merge lineup + profiles + geo + draw + photos -> data.json
node build-app.mjs      # 7. inject data into the template -> ../site/porchfest/app/index.html
node smoke-test.mjs     # 8. the ship gate
```

Editing `app.template.html` only needs step 5.

The lineup is scraped from the festival's JS bundle, where the full band list is
embedded as a `JSON.parse('…')` literal — no HTML scraping, so it survives a
restyle but not a data-layer change (`scrape.mjs` fails loudly if the shape moves).

Band profiles (`profiles.merged.json`) are the one step no script reproduces:
they came from research agents following `SPEC.md`. Re-run that only when the
lineup changes.

## Draw — "how big a name is this act?"

`build-draw.mjs` scores every band 0–100 for footprint and writes `draw.json`,
which becomes each band's `dw`. There is no attendance or streaming data for a
porchfest, so this is an **evidence score, not a measurement**: the rooms an act
has played (First Avenue outranks a coffee shop), who they have opened for,
releases, press and curation, and how much the researchers could actually
verify. It is normalised against the strongest act in this lineup, so it reads
as "relative to this festival" rather than as a false absolute.

A naive keyword sweep gets this wrong in ways that misrepresent real musicians,
so the scorer defends against its own failure modes and the smoke test holds it
to them. Three guards, each earned from a real false positive:

- **Negation.** "rather than a road-hardened *touring* act" is not a touring
  credit. A negation cue in the run-up to a match voids it.
- **Confidence gating.** A `low` confidence profile means the research found
  nothing to verify the text against, so text-derived credit is scaled to 0.35.
  Without this, "no footprint to verify — this profile rests on their own
  *festival* bio" scored as a festival booking.
- **Precise patterns.** "the *current* lineup" is not the radio station; "aimed
  at the *headlines*" is not a headline slot; an act that *runs* the We Love
  Fiesta label is not signed to one; "RADIO BABY" is an album title.

Only the top two tiers are labelled in the UI (≥60 "Big draw", ≥42 "Known
name") and each badge shows the evidence behind it. Nothing is labelled
negatively — an act with no footprint simply gets no badge.

**The tier must be carried by shape, not hue.** In the schedule it is `★★` for
a big draw and `★` for a known name (`TIERMARK`). The two tiers were once told
apart only by colour and both colours are orange (`--brand` / `--brand-2`) —
at 10px that is a coin flip for anyone, and no distinction at all with
red-green colour blindness. Colour still rides along as a second cue; it must
never be the only one. The star is also a button: tapping it toasts the tier
and its evidence, because the only explanation before was a `title` tooltip
and a phone has no hover.

If you re-run the research, re-run this too: it reads `profiles.merged.json`.
`node build-draw.mjs --report` prints the full ranking with the evidence per
act, which is the fastest way to sanity-check a change to the patterns.

## Who's walking (the group presets)

`CREW` in `app.template.html` holds four life-stage profiles — *With kids*,
*Twenties*, *Easy does it*, *All ages*. A preset sets taste dimensions by name
and may add `__tags` (genres to seek, replacing the current chips), `__pop`
(draw), `__pace` and `__max` (band cap).

Those last two are the reason this row exists at all and isn't just more vibe
presets: **stamina is a real constraint, and only these can express it.** A
stroller or a pair of eighty-year-old knees changes how far the route should
reach, not just what it should sound like. *Easy does it* drops the pace to
3 km/h and caps the route at four stops, which lands around 1.4 km for the
whole afternoon. Reset restores pace and cap along with everything else,
otherwise a slow pace silently outlives the preset that set it.

The row sits at the TOP of the plan pane on purpose: picking a profile
overwrites the pace and band cap shown below it, so it has to come first.

*With kids* absorbed the old *Family stroll* vibe preset — same taste, plus the
pace and the shorter loop a family actually needs. Don't reintroduce it.

Keep these labels demographic, never personal names: this is a public page that
strangers at the festival will open, and a name means nothing to them.

## Desktop panels

Above 1080px the three views are resizable cards. Widths live in the
`--col-tune` / `--col-route` custom properties, so dragging only ever writes
two numbers, and a collapsed panel is simply width 0 — no separate state to
keep in sync. The handle deliberately stays put when a panel collapses, because
it is the way to pull it back. Sizes persist at `pf.layout`; the header button
on the map resets them.

Below 1080px the map moves under the other two, so there is no third column to
drag against and the handles are hidden rather than resizing into nothing.
Phones get the tab bar instead: no cards, no headers, no handles.

**Watch the specificity.** The card rules set `overflow-x` on `#tune` / `#route`,
which are ID selectors — the mobile override that returns the panes to
`overflow:visible` has to match that specificity or the pane becomes its own
scrollport and the sticky CTA silently breaks. That is a real regression the
suite caught; the comment is in the CSS.

## Units

Distances read in **miles and feet**, pace in **mph** — this is a street
festival in Minneapolis and the people walking it think in blocks and miles.
Everything underneath stays metric: the street graph is in metres, `S.pace` is
still km/h, and the share payload is unchanged, so links cut before the switch
still decode correctly. Only `km()` and `mph()` convert, at the display layer.
Under a tenth of a mile shows as feet.

If you ever add a metric toggle, change those two functions and nothing else.

## Swap

Each stop has a Swap button. It drops that band and refills the slot, holding
the rest of the schedule in place — `plan(64, {hold})` pins the other stops for
the re-solve, so swapping the 3pm act does not quietly rearrange the other
nine. Swapping something you had pinned as a must-see also unpins it, since you
have changed your mind about it.

Swapped bands go into `S.rejected` and leave the pool, so they do not creep
back on the next re-plan — which is the whole point, but it means there has to
be a visible way back. The schedule shows "N bands swapped out — bring them
back" whenever the list is non-empty. Don't remove that: without it a few taps
silently shrink the lineup with no explanation.

If nothing else fits the freed slot, the swap is **undone** rather than leaving
you a band short, and it says so.

`S.rejected` rides in the share payload as `rj`, so a shared plan re-plans the
same way rather than pulling back a band the sender had deliberately dropped.

## Shuffle

Shuffle has to produce a *different* good afternoon, not the same one again.
The search is randomised but the objective is not, so 64 restarts all converge
on one optimum — the button re-derived the identical winner and looked broken.

`shuffledPlan()` penalises repeating bands from the recent routes (`cfg.avoid`
as a Map of id → weight, `cfg.avoidW` the multiplier), escalating the weight
until the route actually changes, and gives up honestly — saying so — when the
constraints admit only one answer. It remembers the last three routes, not just
the current one: avoiding only what is on screen makes it ping-pong between two
answers forever. Must-sees are exempt; you pinned them so they'd stay.

The stored `score` is deliberately the unpenalised one, or a later
"only replace if better" pass would compare two different yardsticks.

## Back and Forward

The four views are the app's navigation, so they are what the browser buttons
move through. The URL is `#s=<state>&v=<view>`.

The rule that makes this usable: **only a view change pushes a history entry.
Tuning replaces the current one.** A slider fires a burst of input events, and
an afternoon of tuning would otherwise bury the entry you actually wanted under
a hundred near-identical ones — Back would need fifty presses to leave a tab.
So Back walks where you have *been*, never every value a dial passed through.

- `setView(v)` pushes when the view actually changes; pass `false` as the
  second argument to switch without touching history (boot, and popstate).
- `applyPlan` replaces, guarded by `navLock` so a restore doesn't rewrite the
  entry it just landed on.
- `popstate` re-decodes the state as well as the view, so Back also undoes
  tuning done after that entry was made — and only re-solves when the entry
  carried no usable plan, or stepping back would hand you a freshly randomised
  route instead of the one you had.
- `S.crew` rides in the payload as `cw`. It is UI-only, but without it Back
  leaves a group chip highlighted that no longer matches the dials.

`v` is optional and appended, so links shared before it existed still open.
`shareUrl()` deliberately omits it: a shared plan should open where the app
thinks best, not on whichever tab the sender happened to be looking at.

## Smoke before ship

`node smoke-test.mjs` — Chromium **and** WebKit, 390×780 and desktop, zero
pageerrors, zero console errors. It asserts the things that actually break: a
route exists on load with nothing clicked, moving a dial re-plans on its own,
"exactly 6" / "3–5" / "at most 4" are obeyed, avoiding a genre drops it from the
route live, every stop sits inside its set window, the schedule is
chronological, every stop is pinned on the map, **no two pins overlap**, share
links round-trip, the toast doesn't stretch, and the primary action clears the
mobile tab bar. Mobile is a release gate.

For draw it checks behaviour rather than specific bands, since the planner is
randomised: asking for big names must *raise* the mean draw of the routed acts
and hidden gems must *lower* it, the preset must drive the slider, Reset must
clear it, the browser sort must be descending, every badge must carry its
evidence, and a share link cut before the slider existed must still open.

For the group presets it asserts the one that does the most work: *Easy does
it* must
ease the pace *and* the band cap and seek her genres, Reset must put all three
back, and "Full profile" on a scheduled stop must land on that band's card.

If an engine is missing locally the suite says so loudly and keeps going; under
`CI=1` a missing engine fails the run.

## Attribution

Lineup, set times, porch addresses and photos: [uptownporchfest.com](https://uptownporchfest.com/bands).
Geocoding: [Nominatim](https://nominatim.openstreetmap.org).
Street network, corners and walking distances: [OpenStreetMap](https://www.openstreetmap.org/copyright)
contributors (ODbL), via Overpass and OSRM.

An unofficial fan project, not affiliated with the festival.
