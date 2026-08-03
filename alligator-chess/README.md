# Tomorrowland Alligators Chess Set

A six-piece chess family built around one complete faceted alligator-bust
archetype: upright torso, long wedge muzzle, heavy angular brow, separate jaw
line, planar chest, sculpted forelimbs, and a row of dorsal plates. The low-poly
geometry follows a retrofuturistic 1960s Tomorrowland design language while the
cranial and back silhouettes preserve each piece's chess identity.

![The complete alligator chess family](preview/alligator_chess_family.png)

## Files

| Piece | STL | Size (X × Y × Z) | Design cue |
| --- | --- | --- | --- |
| Pawn | `stl/alligator_pawn.stl` | 26.1 × 26.1 × 43 mm | Compact hatchling bust and low dorsal crown |
| Rook | `stl/alligator_rook.stl` | 29.8 × 29.8 × 58.2 mm | Squared back plates and four cranial battlements |
| Knight | `stl/alligator_knight.stl` | 29.9 × 30 × 60.2 mm | Pure rearing alligator silhouette closest to the core concept |
| Bishop | `stl/alligator_bishop.stl` | 29.4 × 29.4 × 71 mm | Twin tapered planes form an open mitre |
| Queen | `stl/alligator_queen.stl` | 31.3 × 31.3 × 74.5 mm | Five rising crown plates integrated behind the brow |
| King | `stl/alligator_king.stl` | 32.5 × 32.5 × 76 mm | Tall dorsal post and diamond-section crossbar |

All dimensions are millimetres. Each STL contains one piece, upright on the
build plate at Z=0.

## Print guidance

These pieces were designed to print upright without supports on a normally
tuned FDM printer.

- Layer height: 0.16–0.24 mm
- Walls: 3 perimeters
- Top/bottom: 4 layers
- Infill: 10–15% gyroid or grid
- Brim: usually unnecessary; use 3–5 mm for the knight if bed adhesion is marginal
- Supports: off
- Scale: 100%; all bases are sized for a conventional tournament-scale board
- Material: PLA recommended; PETG also works with adequate cooling

The long snouts use narrow lower keels instead of broad horizontal undersides.
Forelimbs descend toward the torso, dorsal elements are vertical or tapered,
the king's crossbar has a self-supporting diamond section, and every base has a
broad flat underside. The geometry is intentionally coarse and planar so the
faceting survives ordinary FDM layer heights.

The source generator represents each design as overlapping closed solids. PrusaSlicer,
OrcaSlicer, Bambu Studio, Cura, and other current slicers merge these volumes at
slice time. If a slicer offers an option such as “union overlapping volumes” or
“remove mesh intersection,” leave it enabled.

## Verification

`mesh_report.csv` is regenerated with the models. Every constituent shell is
closed, each edge is shared by exactly two triangles, there are no degenerate
triangles, and every model begins at Z=0. Triangle counts and exact bounding-box
dimensions are recorded in that report.

To regenerate the STLs and previews using Python 3 plus Pillow:

```sh
python3 generate_models.py
python3 render_previews.py
```

`generate_models.py` itself uses only the Python standard library; Pillow is
needed only for the preview images.
