# Illinois Sandstone Lamp v2

This folder contains the recommended 180 mm lamp shell and the outputs from
`main/generate_sandstone_v2.py`.

The `connected/` subfolder contains the current print releases at 120, 150,
and 180 mm. They include the original 80 mm threaded lamp connector and mate
with `files/base/base-115mm-v3.stl`.

V2 improves the earlier parametric model in three ways:

- preserves all 111 rings from the original 120 mm sandstone source, then
  inserts intermediate rings to reach the requested 166-layer mesh;
- constructs the outer wall, inner wall, 9.46 mm base, 66 mm hole, and top
  rim as one connected watertight mesh;
- finishes the top with an eight-segment half-round inward return, giving the
  shade a gentle wrapped lip instead of an abrupt flat edge.

## Default 180 mm preset

From `ordovician-sandstone/main`:

```bash
python3 generate_sandstone_v2.py
```

This is equivalent to:

```bash
python3 generate_sandstone_v2.py \
  --height 180 \
  --layers 166 \
  --wall 2 \
  --base 9.46 \
  --hole 66 \
  --top-lip-segments 8
```

The generator writes a print-ready STL, a mesh-only 3MF, a generated SCAD
polyhedron, and a JSON validation report. It uses only Python's standard
library.

Connector output is enabled by default. Use `--no-connector` when a standalone
shell is needed. Connected releases are named with the `_connector80` suffix.

## Why the base artifact is gone

The previous 180 mm project contained an open-bottom shell and a separate
overlapping base. Their circumferential boundaries were not shared topology,
which produced the dashed interior seam and left 240 open shell edges.

V2 uses the same indexed point loops for the inner wall, flat floor, center
hole tube, and bottom surface. The validation report must show:

```text
Boundary edges:     0
Non-manifold edges: 0
Components:         1
Watertight:         true
```

## Tests

```bash
cd ordovician-sandstone/main
python3 -m unittest -v test_generate_sandstone_v2.py
```
