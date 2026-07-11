# Sandstone lamp screw bases

## Recommended base: v4 smooth drilled

`sandstonelayers-base-v4-smooth-drilled.3mf` is the current base for the
80 mm connector used by the connected 120, 150, and 180 mm lamp releases.

V4 preserves the complete functional geometry from
`sandstonelayers-base-v3-final.3mf`:

- screw/locking interface;
- central core and upper ring;
- rectangular openings and internal features;
- the positioned drill/cord object.

Only the disconnected 115 mm outer body is replaced. Its new profile has:

- a 115 mm outside diameter;
- a 15 mm-high outer body;
- a 2 mm bottom fillet;
- a quarter-ellipse upper shoulder;
- a 94 mm-diameter flat top area.

The upper shoulder reaches the flat top with a horizontal tangent, avoiding a
visible rise, dip, or crease at the transition.

The drill object remains a Bambu Studio `negative_part` with the exact source
geometry and transform. It is automatically subtracted when the 3MF is sliced.
For that reason, use the 3MF rather than exporting the unsliced positive body
as an STL.

## Regenerate and test

From `ordovician-sandstone/main`:

```bash
python3 generate_base_v4.py
python3 -m unittest -v test_generate_base_v4.py
```

The adjacent JSON report records the preserved/replaced triangle counts,
curve parameters, negative-part status, and output dimensions.
