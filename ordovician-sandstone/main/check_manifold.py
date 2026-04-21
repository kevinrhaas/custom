#!/usr/bin/env python3
import struct, collections, sys

path = sys.argv[1] if len(sys.argv) > 1 else "vase_sandstone_78mmx176mm_wall3_base3_163L.stl"
with open(path, 'rb') as f:
    f.read(80)
    n = struct.unpack('<I', f.read(4))[0]
    edges = collections.Counter()
    for _ in range(n):
        f.read(12)
        verts = [struct.unpack('<3f', f.read(12)) for _ in range(3)]
        f.read(2)
        for i in range(3):
            v0, v1 = verts[i], verts[(i+1)%3]
            edges[tuple(sorted([v0, v1]))] += 1

bad = [(e, c) for e, c in edges.items() if c != 2]
print(f"Triangles: {n}  |  Unique edges: {len(edges)}  |  Non-manifold: {len(bad)}")
if not bad:
    print("✓ Fully manifold!")
else:
    counts = {}
    for _, c in bad:
        counts[c] = counts.get(c, 0) + 1
    print(f"Bad edge count distribution: {counts}")
    print(f"Sample bad edge: {bad[0]}")
