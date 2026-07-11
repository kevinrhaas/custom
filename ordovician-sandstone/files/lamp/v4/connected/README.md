# Connected Illinois Sandstone Lamp v4

V4 fixes the two mesh defects in the earlier connected release:

- The sandstone body and 80 mm threaded connector are now combined by an
  exact Boolean union into **one watertight indexed solid**.
- Overlapping connector/floor triangles are removed, leaving a continuous
  smooth interior floor at the 9.46 mm base height. This removes the dashed
  internal-rim artifacts seen in the slicer.

The original 120 mm model's 111 sandstone control rings are all preserved.
The 150 and 180 mm variants add interpolated rings without discarding source
detail. The gentle 1 mm-radius inward return at the top is also retained.

## Release sizes

| Height | Rings | Wall | Base | Opening | Connector |
|---:|---:|---:|---:|---:|---:|
| 120 mm | 111 | 2 mm | 9.46 mm | 66 mm | 80 mm |
| 150 mm | 139 | 2 mm | 9.46 mm | 66 mm | 80 mm |
| 180 mm | 166 | 2 mm | 9.46 mm | 66 mm | 80 mm |

Use the `.3mf` file in Bambu Studio or OrcaSlicer. Each 3MF contains one mesh
object and one printable build item—there are no overlapping multipart shells.
The STL and OpenSCAD polyhedron are provided as alternate formats, and each
JSON report records the edge/manifold validation.

These lamps mate with:

```text
files/base/sandstonelayers-base-v4-smooth-drilled.3mf
```

## Regenerate

From `ordovician-sandstone/main`:

```bash
python3 -m pip install -r requirements-v4.txt
python3 generate_sandstone_v4.py --height 120
python3 generate_sandstone_v4.py --height 150
python3 generate_sandstone_v4.py --height 180
```

The prepared connector is stored at
`files/connect/80mm-lamp-attach-base-manifold-v4.stl`. To rebuild it from the
legacy multipart STL, run `python3 repair_connector_v4.py` first.
