# Connected Illinois Sandstone Lamp v6

V6 removes the repeated dashed divots at the top inner edge by changing the
connector geometry below that edge—not merely by retriangulating the floor.

The 66 mm opening now has a smooth 1.50 mm-deep cylindrical lead-in. Connector
thread geometry is cleared 0.05 mm behind this bore throughout the lead-in, so
the periodic upper thread fragments cannot project onto the visible rim. The
functional lower 7.96 mm of connector engagement remains intact.

V6 also retains the v5 safeguards:

- connector cap recessed 0.20 mm below the horizontal finish plane;
- exactly 240 large, flat finish-plane triangles;
- one watertight Boolean-unified solid;
- no boundary, non-manifold, degenerate, or duplicate faces;
- original sandstone rings and gentle rounded top lip preserved.

## Release sizes

| Height | Rings | Wall | Opening | Smooth lead-in | Thread engagement |
|---:|---:|---:|---:|---:|---:|
| 120 mm | 111 | 2 mm | 66 mm | 1.50 mm | 7.96 mm |
| 150 mm | 139 | 2 mm | 66 mm | 1.50 mm | 7.96 mm |
| 180 mm | 166 | 2 mm | 66 mm | 1.50 mm | 7.96 mm |

Use the `.3mf` files in Flash Studio, Bambu Studio, or OrcaSlicer. STL, SCAD,
and detailed JSON validation reports are included.

## Regenerate

From `ordovician-sandstone/main`:

```bash
python3 -m pip install -r requirements-v4.txt
python3 generate_sandstone_v6.py --height 120
python3 generate_sandstone_v6.py --height 150
python3 generate_sandstone_v6.py --height 180
```

The lead-in depth is adjustable with `--smooth-lead-in-depth`; 1.50 mm is the
validated release value.
