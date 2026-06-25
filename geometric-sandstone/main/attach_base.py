#!/usr/bin/env python3
"""
Fuse the existing twisted-puck twist-lock receiver onto the bottom of a
geometric-sandstone shade — the same multi-body approach as the original
`sandstonelayers-to80mmtwistedpuck` files.

The shade is generated with a 9.46 mm solid base and a 66 mm centre bore; the
puck (⌀66 body / ⌀80 flange / ⌀63 twist-lock bore, 9.46 mm tall) nests exactly
into that bore at z0 with no transform.  The two meshes are written as a single
multi-body binary STL; the slicer unions the overlapping solids into one print,
and the Bambu LED module twist-locks into the puck's bore from below.

  python3 attach_base.py shade.stl -o shade_with_base.stl

Default connector is the project's proven twisted puck; override with
--connector.  Use --dz / --rotate only if a different puck needs aligning.
"""
import argparse
import math
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PUCK = os.path.normpath(os.path.join(
    HERE, "..", "..", "ordovician-sandstone", "files", "connect",
    "bambulampconnect-80mmwide-frompv_twisted_puck.stl"))


def read_stl(path):
    """Return list of triangles, each ((nx,ny,nz),(v0,v1,v2))."""
    with open(path, "rb") as f:
        f.read(80)
        n = struct.unpack("<I", f.read(4))[0]
        tris = []
        for _ in range(n):
            nx, ny, nz = struct.unpack("<3f", f.read(12))
            vs = [struct.unpack("<3f", f.read(12)) for _ in range(3)]
            f.read(2)
            tris.append(((nx, ny, nz), vs))
    return tris


def transform(tris, dz=0.0, rot_deg=0.0):
    """Translate in z and rotate about the z-axis (degrees)."""
    if dz == 0.0 and rot_deg == 0.0:
        return tris
    c, s = math.cos(math.radians(rot_deg)), math.sin(math.radians(rot_deg))

    def t(p):
        x, y, z = p
        return (x * c - y * s, x * s + y * c, z + dz)

    out = []
    for (nx, ny, nz), vs in tris:
        out.append(((nx * c - ny * s, nx * s + ny * c, nz),
                    [t(v) for v in vs]))
    return out


def write_stl(path, tris):
    with open(path, "wb") as f:
        f.write(b"\0" * 80)
        f.write(struct.pack("<I", len(tris)))
        for (nx, ny, nz), vs in tris:
            f.write(struct.pack("<3f", nx, ny, nz))
            for v in vs:
                f.write(struct.pack("<3f", *v))
            f.write(b"\0\0")


def bbox(tris):
    mn = [1e9] * 3
    mx = [-1e9] * 3
    for _, vs in tris:
        for v in vs:
            for i in range(3):
                mn[i] = min(mn[i], v[i])
                mx[i] = max(mx[i], v[i])
    return mn, mx


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("shade", help="Generated shade STL")
    ap.add_argument("--connector", default=DEFAULT_PUCK,
                    help="Twist-lock connector STL (default: project twisted puck)")
    ap.add_argument("--dz", type=float, default=0.0,
                    help="Shift connector up/down in mm (default 0 — aligned)")
    ap.add_argument("--rotate", type=float, default=0.0,
                    help="Rotate connector about z, degrees (default 0)")
    ap.add_argument("-o", "--output", help="Output STL (default: <shade>_with_base.stl)")
    a = ap.parse_args()

    shade = read_stl(a.shade)
    puck = transform(read_stl(a.connector), a.dz, a.rotate)
    combined = shade + puck

    out = a.output or os.path.splitext(a.shade)[0] + "_with_base.stl"
    write_stl(out, combined)

    smn, smx = bbox(shade)
    pmn, pmx = bbox(puck)
    cmn, cmx = bbox(combined)
    print("Fuse shade + twist-lock puck")
    print(f"  shade : {len(shade):,} tris   Z[{smn[2]:.2f},{smx[2]:.2f}]")
    print(f"  puck  : {len(puck):,} tris   Z[{pmn[2]:.2f},{pmx[2]:.2f}]  "
          f"⌀flange {2*max(pmx[0],pmx[1]):.0f}")
    print(f"  ----")
    print(f"  combined: {len(combined):,} tris   "
          f"Z[{cmn[2]:.2f},{cmx[2]:.2f}]   bodies=2 (slicer unions)")
    print(f"  ✓ {out}")
    if abs(pmn[2] - smn[2]) > 0.5:
        print(f"  ⚠ connector base z={pmn[2]:.2f} not flush with shade z="
              f"{smn[2]:.2f}; adjust --dz")


if __name__ == "__main__":
    main()
