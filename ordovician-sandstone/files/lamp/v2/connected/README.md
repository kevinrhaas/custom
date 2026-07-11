# Connected Illinois Sandstone Lamp v2

These releases include the complete `80mm-lamp-attach-base` assembly in the
bottom 9.46 mm of the lamp. The connector is centered without scaling or
remeshing, preserving the existing twist-lock/thread geometry that mates with:

```text
files/base/base-115mm-v3.stl
```

The 115 mm screw base remains a separate printed part so the shade can be
installed and removed normally.

## Release sizes

| Height | Source-preserving rings | Connector | Recommended file |
|---:|---:|---|---|
| 120 mm | 111 | 80 mm × 9.46 mm | `illinois_sandstone_v2_120mm_111L_wall2_base9.46_hole66_connector80.3mf` |
| 150 mm | 139 | 80 mm × 9.46 mm | `illinois_sandstone_v2_150mm_139L_wall2_base9.46_hole66_connector80.3mf` |
| 180 mm | 166 | 80 mm × 9.46 mm | `illinois_sandstone_v2_180mm_166L_wall2_base9.46_hole66_connector80.3mf` |

Use the 3MF files in Bambu Studio or OrcaSlicer. Each contains one printable
assembly with two components:

1. the watertight sandstone lamp body;
2. the unchanged 80 mm threaded connector, overlapping the lamp floor exactly
   as it does in the earlier non-parametric project.

The corresponding STL is provided for slicers that do not accept 3MF. It is
an overlapping multipart STL by design; the slicer should union the volumes.

`bambulampconnect-80mmwide-frompv_twisted_puck.stl` is the bare puck component.
The releases use `80mm-lamp-attach-base.stl`, which includes that functional
geometry plus the reinforcing outer ring.

## Regenerate

From `ordovician-sandstone/main`:

```bash
python3 generate_sandstone_v2.py --height 120
python3 generate_sandstone_v2.py --height 150
python3 generate_sandstone_v2.py --height 180
```

Layer counts default proportionally to 111, 139, and 166. Add
`--no-connector` to generate only the standalone lamp body.
