# Zion + Bryce Canyon Field Guide

An offline-ready field companion for a Chicago → Las Vegas → Zion → Bryce → St. George loop, September 5–13, 2026.

Live app: `https://kevinrhaas.github.io/custom/zion-bryce/`

## What it does

- turns the source itinerary into exact daily run sheets with realistic buffers;
- lets Sept 7–9 swap between Scout Lookout, the Narrows and a Zion flex day;
- uses an Open-Meteo forecast as a planning signal for those swaps while keeping official NPS conditions authoritative;
- explains the Nevada/Utah time-zone shift in both directions;
- includes route links, official conditions, trail comparisons, a comprehensive categorized packing checklist, calendar export, print layout and an installable offline shell;
- adds a saved “carry today” kit and tactical field tips to every day, automatically changing the kit when a flexible Zion day is swapped;
- stores confirmations and notes only in browser `localStorage` and keeps all reservation numbers out of the public repository.

The implementation is static HTML, CSS and ES modules—no framework, dependency install, account, analytics or build-time network request.

## Build and verify

```sh
node zion-bryce/build.mjs
node zion-bryce/check.mjs
node zion-bryce/browser-check.mjs
```

`src/` is canonical. The build script creates the deploy mirror in `site/zion-bryce/`, which GitHub Pages publishes with the rest of `site/`.

## Research decisions

- The trip is nine days and eight nights, despite the original “10-Day” heading.
- Zion’s 2026 canyon shuttle begins at 7:00 AM for these dates; private cars cannot use Zion Canyon Scenic Drive while shuttle service is operating.
- Bryce sunrise on September 11 is 7:07 AM, before the 8:00 AM shuttle start. Lodge guests should walk or drive.
- Scout Lookout is presented at the official roughly 4.2-mile, strenuous scale. The permit boundary is beyond Scout Lookout at Angels Landing.
- A bottom-up Narrows outing requires no permit to Big Spring, but flash-flood potential, water flow and park closures override the plan.
- Red Canyon’s roadside tunnels sit naturally on the September 10 drive into Bryce, not the southbound September 12 route.
- Snow Canyon’s Scout Cave route is roughly six miles and does not fit before a fixed 7:00 PM dinner. Jenny’s Canyon is the short-stop recommendation.
- Confirmed AA1497 flight times are shown for both directions; booking codes and passenger details remain private.

Primary sources are linked in the app and include NPS Zion and Bryce operations, USGS river data, NWS flash-flood potential, Nevada State Parks and Utah State Parks. Operations were last researched August 30, 2026 and must be rechecked during the trip.
