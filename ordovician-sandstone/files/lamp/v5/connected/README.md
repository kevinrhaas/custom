# Connected Illinois Sandstone Lamp v5

V5 specifically removes the dashed arcs that remained on the visible interior
floor in v4. Those marks came from thousands of microscopic connector Boolean
fragments lying at essentially the same Z height as the lamp's 9.46 mm floor.

The connector is now clipped 0.20 mm below the finish plane before the Boolean
union. This leaves the original generated interior floor completely untouched:

- exactly 240 large, flat, upward-facing triangles;
- no connector faces on the finish plane;
- no micro-triangles, overlaps, or dashed sliver geometry;
- one watertight connected solid.

The functional connector below that narrow top clearance, all original
sandstone control rings, and the gentle rounded inward top lip are preserved.

## Release sizes

| Height | Rings | Wall | Floor | Opening | Connector clearance |
|---:|---:|---:|---:|---:|---:|
| 120 mm | 111 | 2 mm | 9.46 mm | 66 mm | 0.20 mm |
| 150 mm | 139 | 2 mm | 9.46 mm | 66 mm | 0.20 mm |
| 180 mm | 166 | 2 mm | 9.46 mm | 66 mm | 0.20 mm |

Use the `.3mf` files for Bambu Studio or OrcaSlicer. STL, SCAD, and detailed
JSON validation reports are included alongside them.

## Regenerate

From `ordovician-sandstone/main`:

```bash
python3 -m pip install -r requirements-v4.txt
python3 generate_sandstone_v5.py --height 120
python3 generate_sandstone_v5.py --height 150
python3 generate_sandstone_v5.py --height 180
```

The clearance can be adjusted with `--connector-top-clearance`, but 0.20 mm is
the validated release value.
