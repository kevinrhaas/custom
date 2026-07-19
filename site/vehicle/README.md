# Vehicle Finder (`site/vehicle/`)

Ranked, nationwide vehicle searches centered on **Crystal Lake, IL**, published
at `https://kevinrhaas.github.io/custom/vehicle/`. One app, multiple searches:

- **`#corsair`** — Pat's 2026 Lincoln Corsair: Red Carpet Metallic + light
  Smoked Truffle seats, Reserve/Premiere (never the Grand Touring PHEV), AWD
  preferred, panoramic roof preferred, new or essentially new.
- **`#forester`** — 2026 Subaru Forester Touring Hybrid per the build sheet:
  Crimson Red Pearl + Touring Brown leather, $42,995 as configured.

`site/vehicle-2/` is a redirect stub kept for old links (the Corsair search
lived there first).

## Files

```
index.html         The app (static, no build step, no deps; search switcher)
css/app.css        Lincoln-inspired skin (aurora backdrop, light/dark)
js/data.js         FACTS ONLY — both searches' listings (auto-generated)
js/app.js          Rendering + per-search match scoring + filters + value ratings
raw-corsair.json   Raw merged Corsair listings (compiler input)
raw-forester.json  Raw merged Forester listings (compiler input)
build_data.mjs     Compiler: dedupe by VIN, VIN-decode, distances, asset links
stickers/<vin>.pdf Hosted Monroney window stickers (fetched from FordDirect,
                   link-verified; Lincoln VINs only — Subaru has no public API)
photos/<vin>.jpg   Real listing photos (scraped og:image); cards fall back to a
                   color-accurate SVG illustration when no photo could be saved
```

## Regenerating

Update the raw JSON files, then `node build_data.mjs` (writes `js/data.js`,
attaches sticker/photo paths for files that exist, computes distances, dedupes
by VIN). Window stickers: `curl "https://www.windowsticker.forddirect.com/windowsticker.pdf?vin=<VIN>"`.

## Ranking & value ratings

Match tiers weight each search's top preferences (target exterior + interior)
most heavily, then trim, drivetrain, roof, condition, and distance to Crystal
Lake as a tiebreaker. Value ratings compare the asking price to a fair-price
estimate: for the Corsair (final model year) fair ≈ 7% under MSRP for clean new
cars and ≈ 13% under for demos/used, anchored to verified discounts in this
dataset ($4k–$9.3k off); for the Forester hybrid (in demand) fair ≈ 4.5–6%
under MSRP, floor-checked against verified market lows. MSRPs come from the
actual window stickers where hosted. Estimates, not appraisals — verify with
dealers.
