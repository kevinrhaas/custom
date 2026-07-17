# Lurvey hosta data — spec & re-pull guide

This is the **base plant data** behind the Gangway Hosta Garden app: every hosta
variety Lurvey listed, with the fields the app needs to filter, price, and place
them. It lives in [`lurvey-hostas.json`](./lurvey-hostas.json) and can be
**exported, edited, and re-imported** from the app's *Plant finder → Base data*
panel.

When you want fresh numbers (Lurvey changes prices and stock), hand this spec to a
research/cowork session, let it re-pull, and import the resulting JSON back into the
app. Nothing else in the app has to change — the finder, the render kit, and the
per-design shopping math all read from these records.

---

## Source

- **Retailer:** Lurvey Home & Garden Supply
- **Catalog URL:** <https://lurveys.com/shop/?_sf_s=Hosta>
- **Prices:** standard-pot list, **pre-tax**, in USD.
- **Stock:** as-of the pull date (volatile — expect it to drift).

## File shape

```jsonc
{
  "$schema": "lurvey-hostas/v1",
  "source":  "https://lurveys.com/shop/?_sf_s=Hosta",
  "retailer":"Lurvey Home & Garden Supply",
  "pulledAt":"2026-07-16",        // ISO date of the pull
  "count":    74,
  "records": [ /* one object per variety, schema below */ ]
}
```

## Record schema (`records[]`)

| Field | Type | Meaning |
|-------|------|---------|
| `category` | int 1–13 | Which of the 13 design categories it belongs to (see list below). |
| `categoryLabel` | string | Human label, e.g. `"4. Large Blue Mounds"`. |
| `name` | string | Variety name as sold, e.g. `"Abiqua Drinking Gourd"`. |
| `url` | string | Link to the product / search on lurveys.com. |
| `image` | string | Product thumbnail URL (Lurvey CDN) — used in the finder. |
| `star` | bool | `true` = a standout/recommended pick. |
| `note` | string | One-line description (leaf, habit, use). |
| `color` | string | Foliage colour story, e.g. `"Blue"`, `"Gold center / blue edge"`. |
| `leafSize` | string | Leaf & clump size as listed, e.g. `18-22" × 3-3.5 ft`. |
| `spacing` | string | Recommended planting spacing (center-to-center). |
| `light` | string | Light preference, e.g. `"Part shade"`. |
| `spreadFt` | number | **Mature spread in feet** (numeric — drives fit & plan drawings). |
| `heightIn` | int | Mature leaf-mound height in inches. |
| `fit` | enum | Does it fit the 3-ft bed? `yes` \| `vase` \| `tight` \| `no`. |
| `fitLabel` | string | Display text, e.g. `"Fits"`, `"Too wide"`, `"Vase"`, `"Tight"`. |
| `fitClass` | enum | Badge colour key: `y` (fits) \| `v` (vase) \| `t` (tight) \| `n` (no). |
| `zone` | enum | Best zone: `street` \| `slot` \| `either`. |
| `zoneLabel` | string | Display text, e.g. `"The slot"`, `"Street end"`, `"Either"`. |
| `zoneClass` | enum | Badge colour key: `e` (street/edge) \| `s` (slot) \| `a` (any/either). |
| `price` | number | Standard-pot price, USD, pre-tax. |
| `inStock` | bool | In stock on the pull date. |
| `stockLabel` | string | `"In stock"` / `"Sold out"`. |
| `sizes` | array | Pot options: `[{ "label": "Std", "text": "Std $11.99", "inStock": true }]`. |
| `plansUsed` | int | How many of the 6 designs use it (0 if none). Recompute from the designs, or leave as-is on a plain price refresh. |
| `search` | string | Lowercased haystack for the finder's text box (name + category + colour + note …). Regenerate as `"{name} {category words} {color} {light} {note} {stock}"`. |

### Category list (the 13)

1. Giant Blue Specimens · 2. Giant & Large Gold / Chartreuse · 3. Upright, Vase-Shaped
& Cream/Gold-Margined · 4. Large Blue Mounds · 5. Large Green & Fragrant-Flowered ·
6. Green with White Margin · 7. Green / Blue with Gold or Yellow Margin · 8. Gold-Centered,
Two-Tone · 9. Medium Blue Mounds · 10. Frosted / Misted & Two-Tone Medium · 11. Small Gold
& Red-Petioled Accents · 12. Small Green & Variegated Edgers · 13. Miniatures — Mouse Ears & Tiny

### Fit rule (how `fit` is decided)

The bed is **3 ft deep**. Judge against mature spread:
`spreadFt ≤ 3` → `yes`; a distinctly **upright/vase** habit that reads narrow despite a
listed wide spread → `vase`; `3 < spreadFt ≤ ~3.5` (just squeezes) → `tight`;
`spreadFt > 3.5` and mounding → `no`.

---

## Re-pull prompt (paste into a research/cowork session)

> Pull the current hosta catalog from Lurvey Home & Garden Supply
> (https://lurveys.com/shop/?_sf_s=Hosta — page through all results). For **every**
> hosta variety, produce one JSON record following the `lurvey-hostas/v1` schema in
> this spec: `category` (1–13 per the category list), `categoryLabel`, `name`, `url`,
> `image`, `star`, `note`, `color`, `leafSize`, `spacing`, `light`, `spreadFt`
> (numeric feet), `heightIn`, `fit`/`fitLabel`/`fitClass` (using the 3-ft-bed fit
> rule), `zone`/`zoneLabel`/`zoneClass`, `price` (standard pot, pre-tax), `inStock`,
> `stockLabel`, `sizes[]`, and a lowercased `search` string. Set `plansUsed` to 0 for
> new varieties (I'll recompute). Wrap them as
> `{ "$schema":"lurvey-hostas/v1", "source":…, "retailer":…, "pulledAt":"<today>",
> "count":<n>, "records":[…] }`. Output valid JSON only.

Then in the app: **Plant finder → Base data → Import**, choose the file, done. Use
**Export** first if you want the current file as a starting point, and **Reset** to
return to the shipped data.
