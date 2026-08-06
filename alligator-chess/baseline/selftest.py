#!/usr/bin/env python3
"""Prove the invariants are load-bearing, not decorative.

An invariant that passes on a broken piece is worse than no invariant: it turns
a false claim into a false measurement. Each test here deliberately breaks one
thing and asserts that the gate notices. If a gate ever stops noticing, this
fails long before a bad STL ships.

    python3 selftest.py
"""

from __future__ import annotations

import sys

import numpy as np
import trimesh

import chesskit as ck
import knight


def expect_failure(label: str, mesh, needle: str) -> bool:
    try:
        knight.assert_invariants(mesh)
    except AssertionError as exc:
        if needle in str(exc):
            print(f"  PASS  {label}\n          caught: "
                  f"{[l.strip('- ') for l in str(exc).splitlines() if needle in l][0]}")
            return True
        print(f"  FAIL  {label}\n          raised, but not about {needle!r}: {exc}")
        return False
    print(f"  FAIL  {label}\n          invariants passed a mesh that is broken")
    return False


def main() -> int:
    ok = True
    print("baseline knight — invariant self-test\n")

    piece = knight.build()
    try:
        knight.assert_invariants(piece)
        print("  PASS  the shipped piece satisfies every invariant")
    except AssertionError as exc:
        print(f"  FAIL  the shipped piece does not: {exc}")
        ok = False

    # 1. The jowl step. This is THE regression that hid for a full revision:
    #    a draft plane wide enough to reach the muzzle also reached the neck
    #    and clipped both slabs to one width, leaving a smooth ramp where the
    #    step should be — while the old two-sample measurement still reported
    #    a healthy 1.5 mm, because two samples on a ramp always differ.
    print("\n  breaking the two-slab construction (HEAD_W := BODY_W):")
    original = knight.HEAD_W
    try:
        knight.HEAD_W = knight.BODY_W
        flat = knight.build()
        ok &= expect_failure("jowl step gate notices the step is gone",
                             flat, "jowl step")
    finally:
        knight.HEAD_W = original

    # 2. A ramp must never read as a step, at any slope.
    print("\n  a pure linear ramp must not read as a step:")
    ramp = trimesh.creation.box((40.0, 16.0, 60.0))
    ramp.apply_translation((10.0, 0.0, 30.0))
    ramp.apply_transform(trimesh.transformations.compose_matrix(scale=[1, 1, 1]))
    measured = knight.jowl_step(ramp)
    if measured < 0.05:
        print(f"  PASS  flat-sided box reads {measured:.3f} mm of step")
    else:
        print(f"  FAIL  flat-sided box reads {measured:.3f} mm of step")
        ok = False

    # 3. A needle triangle must be caught.
    print("\n  a needle triangle must be caught:")
    needled = piece.copy()
    verts = needled.vertices.copy()
    verts = np.vstack([verts, verts[0] + [1e-4, 0, 0], verts[0] + [1e-4, 1e-4, 0]])
    faces = np.vstack([needled.faces, [0, len(verts) - 2, len(verts) - 1]])
    needled = trimesh.Trimesh(vertices=verts, faces=faces, process=False)
    alt = ck.triangle_altitude(needled)
    if (alt < ck.NEEDLE_LIMIT).any():
        print(f"  PASS  triangle_altitude flags it ({alt.min():.2e} mm)")
    else:
        print("  FAIL  triangle_altitude missed a needle")
        ok = False

    # 4. A floating island must be caught.
    print("\n  a floating island must be caught:")
    report = ck.layer_report(trimesh.util.concatenate(
        [piece, trimesh.creation.box(
            (4, 4, 4), trimesh.transformations.translation_matrix((40, 0, 30)))]))
    if report["layers_with_islands"]:
        print(f"  PASS  layer_report flags "
              f"{len(report['layers_with_islands'])} layers with islands")
    else:
        print("  FAIL  layer_report missed a detached block")
        ok = False

    print("\n" + ("all self-tests passed" if ok else "SELF-TEST FAILURES"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
