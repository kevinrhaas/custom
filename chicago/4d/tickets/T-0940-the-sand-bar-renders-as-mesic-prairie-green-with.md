---
id: T-0940
title: The sand bar renders as mesic-prairie green with scrub on it, though z08_lakeshore and z09_sand_prairie cover it and declare sand at 55 and 18 per cent bare soil
state: open
epic: GROUND
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

**OWNER-REPORTED from the walkthrough, 2026-09-07** — a second screenshot of the sand bar,
looking E at 088° from 631 ft, after the ground itself was confirmed present. The bar is
plainly there and plainly WRONG: it is the same green as the mainland prairie behind it, and
it carries scattered scrub across its whole length. His standing instruction from the first
report was **"a low lying sandy stretch with little to no vegetation on it"**.

## The data already says sand. The screen says prairie.

`data/flora/index.json` covers the bar twice over, and both zones declare a sand surface:

| zone | box `e` | `ground_rgb` | `bare_soil_fraction` |
|---|---|---|---|
| `z09_sand_prairie` | 840 .. 1400 | `168, 158, 124` | 0.18 |
| `z08_lakeshore` | 1400 .. 1700 | `198, 190, 166` | **0.55** |
| `z02_mesic_prairie` (for contrast) | the plain | `86, 92, 56` | 0.02 |

The bar's traced edges run **e 1306 .. 1497**, so `z09` holds its landward two-thirds and
`z08` its seaward third. Both use the `july_lake_sand` palette. **Nothing in the flora data
asks for the green that is on screen**, and `z08` asks for the surface to be more than half
bare.

The terrain spec says the same thing in its own words, `vegetation_note`:

> "The eastward extension puts the sand-ridge belt and the bar inside the box for the first
> time — **sand prairie and beach, not the wet-prairie communities the forks carries.**"

## This exact fault was diagnosed and fixed once already

`z08_lakeshore`'s own extent note, dated **2026-08-11**:

> "PRIORITY RAISED 12 -> 45. Planting this zone did nothing until now: at 12 it lost
> everywhere to z02_mesic_prairie (22) and z01_wet_prairie (20), which are ELEVATION BANDS
> matching the general plain, **so the beach and the foredune were being rendered as mesic
> prairie.** A zone defined by a specific geography and a specific SUBSTRATE has to outrank a
> band defined by height alone."

`z09` carries the matching note (11 -> 40). So the priority order is already correct and
already argued. **The question this ticket exists to answer is why the screen does not show
it**, and there is a strong candidate that must be checked FIRST:

**The priority raise governs which zone PLANTS. The green is the terrain mesh's own colour,
and the mesh may not be reading zones at all.** Every entry in the spec's
`surface_materials` carries `"mesh": { "material": "simplified", "dossier_zone":
"record_only" }` — the material record is explicitly RECORD-ONLY for the mesh. If the baked
ground is one simplified material across the whole box, then no flora priority can ever
change the bar's colour, the 2026-08-11 fix could only ever have moved the scatter, and the
fix has looked applied for a month while the ground stayed green.

Establish which of the two it is before changing any number:

1. **The mesh is single-material** — then this is not a regression at all, and the work is to
   carry zone `ground_rgb` into the baked terrain, or to give the bar its own material.
2. **The mesh does read zones and z02 is winning again** — then it IS a regression of the
   2026-08-11 fix, and the thing to find is what re-ordered them.

Say which, with the evidence, in the PR. They are different repairs and only one of them is
a priority question.

## The scrub is the second half

Whatever is planting woody growth across the bar is not what `july_lake_sand` describes. A
lake sand bar carries beach grass, sedge and low scrub in pockets — not the even scatter of
bushes now covering its whole length. `renderers/web/js/trees.js` already states the
governing principle where `north_division_timber` stops at **e ~ +820**: *"roughly 300 m
short of the 1835 shore, because the sandy hills near the lake are the stated exception."*
That exception is written for the far timber and needs to reach the bar's planting too.

## Acceptance

1. The bar reads as sand from the air — its surface takes `z08`/`z09`'s declared colour
   rather than the mesic-prairie green, and `z08`'s 0.55 bare-soil fraction is visible as
   bare ground on the seaward third.
2. **The cause is named**, per the two candidates above, and the fix matches the cause. A
   priority nudge that happens to change the picture without explaining the month of green
   is not accepted.
3. The bar's vegetation is beach grass and low scrub in pockets — **no even scatter of woody
   growth**, and the "sandy hills near the lake" exception is carried onto it explicitly
   rather than by hand-placed exclusions.
4. Nothing on the mainland changes colour. Report what moved outside the bar's footprint;
   the answer should be nothing.
5. `tools/check.sh` green. If the ground mesh changes, bake in the same PR.

**Scope note:** this is the bar's SURFACE. Its southern tip having no ground at all is
**T-0939**, its height is **T-0800**, and re-tracing it off the full sheet is **T-0799**.
This ticket changes no elevation and moves no edge.
