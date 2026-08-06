# Baseline knight — the reference form for the set

`stl/knight_baseline.stl` is the piece every other piece in this set will be
built from. It is not a sketch: the plinth, the chamfer language, the
construction method and the printability rules established here are the ones
the pawn, bishop, rook, queen and king inherit. Get this one exactly right and
the rest are head swaps.

![the baseline knight](preview/hero.png)

## The piece

|                     |                                            |
| ------------------- | ------------------------------------------ |
| Height              | 60.0 mm                                     |
| Plinth              | 34.2 mm across the flats, 16-sided          |
| Volume              | 28.0 cm³                                    |
| Triangles           | ~1,250                                      |
| Mesh                | watertight, genus 0, consistent winding     |
| Thinnest triangle   | 5.7 µm (no needles)                         |
| Units               | millimetres, Z up, sits on Z = 0            |

Everything is planar. There is not one smoothed surface, one filleted edge or
one tessellated curve in the model — every face is flat and every transition
is a real edge, because that is what the reference is.

## How it is built

Three primitives, in `chesskit.py`:

1. **`chamfered_extrude`** — a closed side-view outline extruded at ONE
   half-width, with a bevel running from the flank to the silhouette edge. One
   width per slab is the whole trick: it guarantees the flank is a single flat
   plane instead of a dome, which is what makes the low-poly read honest. The
   knight is two of these — a narrow head slab unioned onto a wider body slab,
   and the step between them is the jowl.
2. **`polygon_base`** — the stacked 16-gon plinth. Shared, unchanged, by every
   piece in the set.
3. **Boolean cuts** — `slice_block_z` and `plane_block` (flat blocks that shave
   a mass along an exactly planar face: the muzzle taper, the jaw draft, the
   neck, crest and mane drafts), `groove_along` (V-creases: the jowl line, the
   chest panel) and `pocket` (the eye).

Taper is never modelled by varying the extrusion width — always by subtracting
a flat block. That is deliberate: varying the width produces a curved flank
and a fan of triangles where the side cap has to close over it. Cutting with a
plane produces a plane.

Two details worth knowing before building the next piece on this:

- **The neck drafts must stop below `JOWL_Z`.** A draft plane that runs past it
  clips the head slab and the body slab to the same width, and the jowl step —
  the whole reason there are two slabs — silently disappears. It is measured
  and asserted, not trusted.
- **Detail cuts are placed with `flank_at`, which asks the solid.** After nine
  chained booleans the flank is not something a formula predicts, and a pocket
  placed on a prediction punches through the silhouette. `flank_at` slices the
  solid and interpolates the outline. (Sampling *vertices* does not work: the
  middle of a large flat facet contains none.)

## Invariants

`knight.py` asserts these at build time and raises rather than writing an STL.
They exist because a docstring cannot fail — an earlier revision claimed a jowl
step it did not have and a draft angle twice its real value, and nothing
noticed:

| check | value |
| --- | --- |
| watertight, genus 0, consistent winding | yes / 2 / yes |
| empty layers, layer islands | 0, 0 |
| needle triangles (< 5 µm thick) | 0 |
| jowl step (want ≥ 1.29 mm = 0.15 × neck) | **1.96 mm** |
| muzzle reach (want ≤ 25.5 mm) | 24.6 mm |
| unsupported area (want ≤ 3%) | **2.42%** |
| ceilings outside the jaw band (want 0) | **0 mm²** |
| jaw draft angle (want ≤ 45°) | 32.1° |
| dead-level shelves above the plinth (want 0) | **0 mm²** |
| height | 60.00 mm |

The muzzle-underside exemption is measured too, not just excused: 156 mm² at a
worst of 86.5°, printed on every build so it cannot quietly grow. The band it
sits in is *derived* from the outline knots that make the jaw, not fitted around
wherever the steep faces landed — an earlier version had `x_min = 7.0` against
faces starting at 7.03 mm, which describes nothing.

`python3 selftest.py` proves these gates are load-bearing rather than
decorative: it breaks the two-slab construction, feeds in a linear ramp, a
needle triangle and a floating island, and asserts each gate notices. The ramp
test sweeps real wedges from 0.1 to 4.0 mm of width-drop per mm; its first
version applied an identity transform to a box and so asserted nothing, which
is the same species of empty check it exists to prevent. That test exists
because the jowl-step check previously *passed* a piece with no step —
it sampled two points on a smooth ramp and subtracted, so it reported 1.5 mm on
a form whose width was a featureless gradient. A false claim had been upgraded
to a false measurement, which is worse than having no check at all.

## Printability

Printed upright on the plinth, no raft needed.

- **The plinth has no overhang above its first millimetre.** All four steps
  are upward-facing shelves and the radius only ever decreases going up. The
  one exception is deliberate and is *not* zero: the bottom edge is lifted
  0.75 mm so the first layer cannot flare, and that relief chamfer is itself a
  43° flare over the first 0.8 mm — inside the support-free window, but it is a
  flare, and calling the plinth "zero overhang" was wrong.
- **Bevels sit at 39° from vertical** (`BEVEL_RATIO = 0.80`), inside the
  support-free window for any printer.
- **The mane teeth self-support.** Each tooth's underside runs 28° from
  vertical.
- **The muzzle flank is drafted to 30° from vertical**, measured off the plane
  `jaw_draft` actually cuts, not asserted. It narrows the jaw to a 4.8 mm keel,
  which is also what gives the muzzle its triangular horse section rather than
  a flat bill, and puts the lip line where the reference has it — one facet
  doing three jobs.

**No layer contains an island.** This is the number that actually decides
whether a print succeeds, and it is checked rather than assumed: `layer_report`
slices the piece and walks every layer. Every one is a single closed loop — the
nozzle never starts extruding into air, and the piece grows continuously from
the plate to the crown. Verified at 0.4 mm and again at 0.1 mm, four times
finer than any layer height you would print at.

The thinnest section is the tip of the crown, and how thin depends on where you
sample: 0.64 mm at 0.4 mm layers, 0.17 mm at 0.1 mm, 0.08 mm at 0.05 mm. That last sliver is the
top ~0.2 mm of the crown and no printer will reproduce it — the piece will come
out with a 0.2 mm flat instead of a point. Worth knowing, not worth fixing.

**The one honest caveat**: the knight's muzzle projects ~15 mm forward of the
throat, and that projection grows faster than 45° per layer, so part of its
underside is a steep overhang no matter how the section is drafted. This is
inherent to the shape of a knight, not a modelling shortcut. It measures
**154 mm², 2.3% of the surface**, all of it in the band z = 43–50 mm, all of it
tucked under the jaw where nobody looks. Because it is an overhang on connected
material and not an island, it prints — the surface will show some droop on an
unsupported FDM run.

Recommended: print upright with supports enabled at a 50° threshold and
`everywhere`, not `on build plate only` — the latter will not catch it. The
contact patch is a few mm². On resin, print upright and let the slicer support
the jaw. Alternatively tilt the model 20° nose-up, which brings the whole
underside inside 45° at the cost of supporting the plinth rim.

Run the numbers yourself:

```
python3 knight.py          # builds, asserts, writes the STL, prints the report
```

Overhangs are judged in two classes, because they fail differently. 45–60° is
what the upper wall of a 1.3 mm detail pocket looks like — the brow over the
eye, the top of the jowl crease — and bridges cleanly anywhere. Over 60° is a
real ceiling, and the build refuses one anywhere except under the jaw.

## Fidelity to the reference

The target photograph is written down twice: as prose in `REFERENCE.md` and as
numbers in `reference.py` — a 20-row outline table, a landmark list and the
solved camera. `compare.py` renders the STL at that camera, extracts the
silhouette, normalises it against its own bounding box and reports the error
at every row:

```
python3 compare.py
```

It also writes `preview/overlay.png` — the render greyed out with the
reference outline's target points marked in red, so a miss is visible rather
than argued about.

Current: **19 of 20 outline heights within tolerance, worst error 3.3%**, and
**5 of 5 mane-tooth landmarks** within tolerance. The landmark table used to be
dead code — nothing read it, so the mane could drift out of pitch while every
outline row still passed, because the rows are sampled at fixed heights and
simply miss where the tips land. `compare.py` now finds each tip as a local
maximum of the silhouette's right edge and checks it. The normalised table has a blind spot — it scales u against the
render's own bounding box, so a uniformly over-long muzzle would rescale the
axis and every row would still agree — so absolute scale is checked separately,
in millimetres, projected at the reference camera:

| | model | reference |
| --- | --- | --- |
| outline span | 36.19 mm | 36.28 mm |
| height | 60.00 mm | 60.00 mm |
| muzzle reach | 1.115 plinth-radii | 1.120 |

The camera itself was solved, not guessed: the width-to-height ratio of the
outline pins the yaw once the plinth diameter is fixed, and the squash of the
plinth ellipse pins the elevation.

## Files

```
chesskit.py     the geometry kernel + the fleet plinth — shared by the set
knight.py       this piece: outlines, cuts, assembly
reference.py    the photograph as numbers (camera, outline, landmarks)
REFERENCE.md    the photograph as prose
compare.py      render-vs-reference measurement + landmarks + overlay
selftest.py     proves the invariants catch the regressions they name
render.py       headless software rasteriser (no GPU, no display)
stl/            the deliverable
preview/        renders
```

Rebuild everything:

```
python3 knight.py          # writes stl/knight_baseline.stl + the print report
python3 compare.py         # measures it against the reference
```

Dependencies: `numpy`, `trimesh`, `manifold3d`, `scipy`, `pillow`.
