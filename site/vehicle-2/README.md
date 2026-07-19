# Corsair Finder (`site/vehicle-2/`)

A published, ranked shortlist of **2026 Lincoln Corsair** vehicles matching a
specific buyer wishlist, built from a nationwide Lincoln-dealer search. Live at
`https://kevinrhaas.github.io/custom/vehicle-2/` (published by the repo's
`site/` GitHub Pages deploy).

## The wishlist (priority order)

1. **Red Carpet Metallic Tinted Clearcoat** exterior — utmost
2. **Light seats** — *Light Smoked Truffle* ideal (utmost); light grey / other
   light faux-leather also welcome; *Medium Smoked Truffle* as a backup; darker
   (Eternal Red, Ebony) only reluctantly
3. **Reserve or Premiere** trim — never Grand Touring (PHEV, excluded)
4. **AWD** preferred (FWD tolerated)
5. Panoramic Vista Roof + nicer packages preferred
6. New, or essentially new (lightly-used)

Match tiers weight the two utmost preferences (exterior + a light interior) most
heavily, then trim, drivetrain, roof, condition, and — as a tiebreaker —
distance to Crystal Lake, IL.

## Files

```
index.html        The app (static, no build step, no deps)
css/app.css       Luxury Lincoln skin (aurora backdrop, light/dark toggle)
js/data.js        FACTS ONLY — the vehicle listings (auto-generated; do not hand-edit)
js/app.js         Rendering + match-scoring + filtering/sorting (all logic)
raw.json          Raw merged listings from the search (the compiler's input)
build_data.mjs    Compiler: dedupe by VIN, VIN-decode drivetrain, compute distance → js/data.js
```

## Regenerating the data

The listings are a point-in-time snapshot (searched 2026-07-19). Inventory
changes daily. To refresh: update `raw.json` with new/verified listings, then:

```
node build_data.mjs        # writes js/data.js (distances + VIN decode applied)
```

VIN decode used (2026 Corsair `5LMCJ{trim}{drive}A…`): `1`=Premiere, `2`=Reserve;
`C`=FWD, `D`=AWD.

## Data caveats

Every VIN, dealer, and price is from a real listing (dealer VDP, Cars.com card,
or the dealer's own page). Many franchise dealer pages block automated reads, so
some prices / panoramic-roof flags are left blank and marked "confirm by phone"
rather than guessed. **Confirm availability, price, and exact spec with the
dealer before acting.** Distances are straight-line estimates to Crystal Lake,
IL (60014).
