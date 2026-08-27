---
id: T-0209
title: The 'full' and 'balanced' ceilings are both breached on dev, with no parcel in flight that spends them
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-27
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The `full` and `balanced` scene-detail ceilings are both breached at T-0135's worst stand, and
no branch in flight is spending them.

## Measured 2026-08-27, published mirror, desktop 1280 x 800, Lake Street at Canal, east

`tools/measure_detail_ceilings.mjs`, which runs T-0135's five-stand sweep on its own and
reproduces bake run 32761900576's figures to the triangle.

| tier | ceiling | dev @ `e2056e97` (T-0117) | dev @ `29eebdef` + T-0126 | verdict today |
|---|---:|---:|---:|---|
| `full` | 1,400,000 | 1,390,060 @ 203c | **1,412,120 @ 204c** | **12,120 OVER** |
| `balanced` | 1,210,000 | **1,244,766 @ 201c** | **1,252,802 @ 202c** | **42,802 OVER** |
| `light` | 1,050,000 | 803,316 @ 70c | 838,742 @ 71c | passes, 20 % under |

Draw calls are inside the 215 budget at every tier and every stand; this is a triangle
problem alone.

## Nothing in flight caused it, and that is the finding

T-0126's whole branch was swept against its own base: **all fifteen readings — five stands x
three tiers — identical to the triangle and to the draw call**, and 487,837 triangles in
`assets/web/` on both trees. A materials parcel spends no geometry, so the breach it was
charged with was already standing on the commit it was cut from. The bake charged it anyway,
because the sweep only runs in a nightly and the last nightly ran against that branch.

The spend is traceable and it is content that has already merged:

- **T-0098's branch read `balanced` at 1,209,926 of 1,210,000** — seventy-four triangles of
  headroom — at this stand, on dev @ `059aaf26`.
- **T-0095, T-0109, T-0106 and T-0117** merged next and cost **34,840** there. That is the
  breach.
- **T-0188** then added six re-placed South Water buildings, +66.8 m of plank walk and three
  street-fence meshes, and took the ground-hugging boards out of the shadow map. Net at
  `balanced`: **+8,036**. The `light` reading is the clean measure of the content, because that
  tier already cast no furniture shadows: **+35,426**.
- `full` has **never been over before today**.

## What this ticket is NOT

It is not a request to raise the constants. T-0135 set both figures on 2026-08-22 with about
6 % of headroom over the measured worst; four days of content ate it, and a ceiling that is
raised every time the town grows measures nothing. AGENTS.md's re-budget ruling is available —
"just raise it", never silently, `light` stays the floor, measure then move — but it wants a
parcel that needs the room. **There is no such parcel here.** The last four raises were each
argued at the definition site and the town has outgrown all four.

It is also not a duplicate of T-0190, which owns whether a second street tier can be afforded.
This ticket owns the plainer fact underneath it: the town is over its own ceilings with nothing
added at all, at two tiers, and every branch that touches the renderer from now on inherits a
red gate it did not cause.

## Acceptance

(state it before working — the definition of done, never weakened to pass)

`full` and `balanced` are inside their ceilings at the WORST of T-0135's five stands on the
published mirror, at both release viewports, with the reading taken by
`tools/measure_detail_ceilings.mjs` and written where the number is defined. Either

1. **a trim** — T-0146 (merge far chunks), a furniture reach at `balanced` the way T-0150 gave
   one to `light`, or the street-fence half of T-0188's shadow lever (measured at **44,110**
   triangles and 3 calls with Randolph in) — with the frame-signature cost measured, not
   assumed, the way T-0150 measured its own; or
2. **a conscious re-budget**, argued at `DETAIL` in `renderers/web/js/main.js` with what the old
   figure came from and what supports the new one, `light` untouched as the floor, and a stated
   answer to "what stops this being the sixth raise".

Whichever is taken, say which one it is. **Never weaken the assertion in
`tools/smoke_renderer.mjs` to make the red go away** — the gate is not the problem.

**Links:** T-0135 (the five stands and the instrument) - T-0190 (the street tier the ceiling
refuses, and its 1,205,762 / 4,238 reading) - T-0147 and T-0149 (win the axial frame back, then
let the ceilings follow) - T-0089 (the same shape at `light`, 2026-08-18, and the first time a
branch was charged for a breach it did not open) - T-0056 - T-0115's ledger -
`docs/STATUS.md`, the T-0126 entry.
