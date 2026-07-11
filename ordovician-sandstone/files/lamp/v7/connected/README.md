# Connected Illinois Sandstone Lamp v7

V7 gives the open top a gentle, natural shoulder instead of ending in a nearly
vertical wall. Over the upper 8 mm, a raised-cosine curve gradually moves the
wall inward by 1.50 mm. It then flows into the existing 1 mm half-round inward
lip, for a 9 mm total transition to the crest.

The curve has zero slope where it starts and where it meets the rounded lip, so
there is no visible kink. Its maximum added angle is 16.41 degrees from
vertical—about 0.047 mm of added inward movement per 0.16 mm layer. V7 also
reserves the lip's 1 mm height before scaling the organic rings, preventing the
last sandstone interval from being compressed into a tiny step. The 120 mm
model's worst combined movement in that final interval is 0.071 mm per 0.16 mm
layer (82.3% line overlap at 0.4 mm), so it remains support-free. The radius
changes by only 1.50 mm (3 mm on diameter), leaving an approximately 71 mm
minimum inner opening.

V7 preserves all validated v6 features:

- every source sandstone ring and the original surface detail;
- 2 mm radial wall thickness through the tapered region;
- the gentle 1 mm-radius rounded inward-return lip;
- 1.50 mm smooth cylindrical lead-in at the 66 mm base opening;
- 7.96 mm of lower threaded connector engagement;
- one Boolean-unified, watertight solid with no boundary, non-manifold,
  degenerate, or duplicate faces;
- a continuous interior floor and no dashed inner-rim geometry.

## Release sizes

| Height | Rings | Wall | Base opening | Upper taper | Radial inset |
|---:|---:|---:|---:|---:|---:|
| 120 mm | 111 | 2 mm | 66 mm | 8 mm | 1.50 mm |
| 150 mm | 139 | 2 mm | 66 mm | 8 mm | 1.50 mm |
| 180 mm | 166 | 2 mm | 66 mm | 8 mm | 1.50 mm |

The `.3mf` files contain geometry only: one mesh object and no Flash Studio,
OrcaSlicer, printer, filament, process, or plate settings. Import them as
geometry and apply your own Flash Studio profile. STL, SCAD, and detailed JSON
validation reports are also included.

## Regenerate

From `ordovician-sandstone/main`:

```bash
python3 -m pip install -r requirements-v4.txt
python3 generate_sandstone_v7.py --height 120
python3 generate_sandstone_v7.py --height 150
python3 generate_sandstone_v7.py --height 180
```

The validated release values are adjustable with `--top-taper-height` and
`--top-taper-inset`.
