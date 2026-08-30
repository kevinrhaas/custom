#!/usr/bin/env python3
"""How far every stack in the town stands above the roof it passes through.

**T-0333.** The Trustees of the Town of Chicago passed an ordinance on 5 August 1835
whose section 18 regulates roof geometry directly, under a penalty of five dollars for
each and every offence:

    every stove pipe or chimney passing through the roof of any building shall extend
    and be carried at least eighteen inches above the roof

— `chicago_democrat_1835_08_19#c005`, read under T-0335. It is not the first printing
of that number. The corporation's own fire ordinance of 26 November 1833, twenty months
BEFORE the scene date and therefore the one in force on 1835-07-01, carries the same
eighteen inches (`chicago_democrat_1833_11_26#c028`), and its column is the
worst-damaged in that issue, so the two printings corroborate each other.

**This is the first documented DIMENSIONAL constraint this project holds on anything
above a roof line**, and it points the other way from the sentence the town's memoirist
gives it: Andreas has a Chicago with "not a single steeple nor a chimney four feet above
any roof". Four feet is a maximum somebody noticed; eighteen inches is a minimum the
town enforced. Both can be true, and together they BRACKET every stack in the scene —
which is what this instrument measures against.

    0.4572 m  <=  a stack's projection above its own roof  <=  1.2192 m

## What it measures, and why it is per-STACK and not per-building

`tools/measure_stack_fabric.py` reads accessor bounds alone and asks a per-BUILDING
question — is anything at all above the roof, and what colour is it. That is too coarse
for a dimensional rule in two ways. Every stack on a building shares one primitive, so
the bounds report the TALLEST of them; and the roof material's bound is the MAIN ridge,
so a stack standing on a kitchen ell's lower ridge would be measured against a roof it
does not pass through. Either error hides a short stack.

So this decodes the mesh. For each phase whose record counts a chimney:

1. the stack primitive's vertices are read and split into as many stacks as the record
   counts, by horizontal single-linkage at 1.05 m — wider than the diagonal of one
   stack's own shaft-and-corbel head, narrower than the gap between any two stacks any
   archetype builds. **The split is checked against the record's count** and the run
   fails if they disagree, so the clustering cannot quietly merge two stacks into one;
2. the roof it passes through is taken as the HIGHEST roof surface the stack has to
   clear: the roof triangles interpolated under the stack's own axis where the stack
   breaks the roof, and the roof geometry within 1.0 m of the stack's footprint where
   it does not. The second rule is what an exterior gable stack needs —
   `log_dwelling` builds its stacks OUTSIDE the wall, against the gable, so there is no
   roof over the flue at all and what it must clear is the rake beside it.

Taking the highest nearby roof is deliberately the harsh reading: it can only ever
understate a stack's projection, never overstate it.

## The scope, and what this gate does NOT know

Section 18 binds only "within the limits of the Corporation". Section 22 of the same
sitting walks that boundary street by street, and deriving it from committed street
control is **T-0334**, not this ticket. Until it exists this gate holds the WHOLE town
to the rule — a superset of the ordinance's reach. That costs nothing today, because
nothing in the town is short and so nothing is conformed to a rule that does not bind
it; if a structure outside the line ever does fail here, the answer is to derive the
boundary, not to weaken the bar.

    python3 tools/measure_stove_pipe_ordinance.py            # the whole town
    python3 tools/measure_stove_pipe_ordinance.py --by-archetype
    python3 tools/measure_stove_pipe_ordinance.py --gate --quiet   # check.sh's line
    python3 tools/measure_stove_pipe_ordinance.py --self-test      # the assertions

Exit 1 if any stack stands under eighteen inches above its roof, or over Andreas's four
feet, or if the geometry cannot be read the way this instrument claims to read it.
"""
import argparse
import json
import math
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from measure_glbs import read_glb  # noqa: E402

#: The exporter runs `export_yup=True`, so glTF +Y is Blender +Z is up, and the two
#: horizontal axes are X and Z.
UP, H0, H1 = 1, 0, 2

INCH = 0.0254
#: Section 18's minimum, in metres. Eighteen inches.
FLOOR_M = 18 * INCH
#: Andreas's maximum, in metres. Four feet — "not a single steeple nor a chimney four
#: feet above any roof". A memoirist's observation, not an ordinance, so a stack over it
#: is a contradiction of a source rather than an offence against a by-law; it is gated
#: here because the two numbers are only worth anything as a pair.
CEILING_M = 4 * 12 * INCH

#: Which material each archetype paints its stacks. This module is deliberately NOT
#: archetype-blind — `measure_stack_fabric.py` is, because there the generator is the
#: thing under test; here the stack has to be FOUND before it can be measured, and the
#: only honest way to find it is to ask the archetype that built it. An archetype
#: missing from this table is a hard failure rather than a silent skip: a new one whose
#: stacks nothing measures is exactly the miss T-0137 recorded.
STACK_MATERIAL = {
    "log_dwelling": "chimney",
    "frame_dwelling": "chimney",
    "frame_storefront": "chimney",
    "fort_structure": "chimney",
    "frame_tavern": "brick",
}

#: Horizontal single-linkage distance that makes one stack out of its shaft and its
#: corbelled head. The widest head any archetype builds is 0.98 m across, so its own
#: adjacent corners are 0.98 m apart; the closest two stacks any archetype puts on one
#: building are metres apart. 1.05 m sits between, with the whole gap either side.
LINK_M = 1.05
#: How far from a stack's footprint roof geometry still counts as the roof it clears.
NEAR_M = 1.0


def chimney_count(phase):
    v = (phase.get("form") or {}).get("chimneys")
    if isinstance(v, dict):
        v = v.get("value")
    return v if isinstance(v, int) else 0


# ------------------------------------------------------------------ reading the mesh

_COMPONENT = {5120: "b", 5121: "B", 5122: "h", 5123: "H", 5125: "I", 5126: "f"}
_COUNT = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


def accessor(js, bins, index):
    """One accessor as a list of tuples. Uncompressed, unstrided — which is what this
    project's exporter writes, and anything else is refused rather than guessed at."""
    acc = js["accessors"][index]
    n = _COUNT[acc["type"]]
    fmt = _COMPONENT[acc["componentType"]]
    size = struct.calcsize("<" + fmt)
    bv = js["bufferViews"][acc["bufferView"]]
    stride = bv.get("byteStride")
    if stride not in (None, n * size):
        raise ValueError("interleaved buffer view: this reader decodes tight ones only")
    blob = bins[0]
    base = bv.get("byteOffset", 0) + acc.get("byteOffset", 0)
    out = struct.unpack_from("<" + fmt * n * acc["count"], blob, base)
    return [out[i * n:(i + 1) * n] for i in range(acc["count"])]


def primitive_of(js, material_name):
    """The one primitive painted `material_name`, or None. Every archetype here emits
    exactly one primitive per material; two would mean the export rule changed."""
    want = [i for i, m in enumerate(js.get("materials", []))
            if m.get("name") == material_name]
    if not want:
        return None
    found = [p for mesh in js.get("meshes", []) for p in mesh.get("primitives", [])
             if p.get("material") in want]
    if len(found) > 1:
        raise ValueError(f"{material_name}: {len(found)} primitives, expected one")
    return found[0] if found else None


# ------------------------------------------------------------------ the stacks

def split_stacks(points):
    """Horizontal single-linkage at LINK_M. Returns a list of vertex-index lists."""
    n = len(points)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(n):
        for j in range(i + 1, n):
            if (math.hypot(points[i][H0] - points[j][H0],
                           points[i][H1] - points[j][H1]) <= LINK_M):
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[ri] = rj
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return sorted(groups.values(), key=lambda g: -len(g))


def closest_on_triangle(tri, h0, h1):
    """(horizontal distance from (h0,h1) to this triangle's plan, height there).

    Inside the plan the distance is zero and the height is the interpolated roof
    surface; outside it, the closest point on the nearest edge and the height there.
    That single rule covers both stacks this project builds: an interior stack breaking
    the roof reads distance zero, and an exterior gable stack reads the rake beside it.
    """
    a, b, c = tri
    p0 = [(v[H0], v[H1]) for v in (a, b, c)]
    z = [v[UP] for v in (a, b, c)]
    (x1, y1), (x2, y2), (x3, y3) = p0
    den = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    if abs(den) > 1e-12:
        l1 = ((y2 - y3) * (h0 - x3) + (x3 - x2) * (h1 - y3)) / den
        l2 = ((y3 - y1) * (h0 - x3) + (x1 - x3) * (h1 - y3)) / den
        l3 = 1.0 - l1 - l2
        if min(l1, l2, l3) >= -1e-9:
            return 0.0, l1 * z[0] + l2 * z[1] + l3 * z[2]

    # Off the plan — or on a triangle with no plan at all, which is what a gable-end
    # fill is: vertical, so it projects to a line and every point of it is the same
    # distance away. Ties go to the HIGHEST point, because the question is what the
    # flue has to clear and the apex of a gable end is exactly that. Taking the first
    # tie instead read the eave of every log cabin's gable and reported its stack
    # standing three metres proud of a roof it stands 0.72 m proud of.
    best = None
    for i, j in ((0, 1), (1, 2), (2, 0)):
        ex, ey = p0[j][0] - p0[i][0], p0[j][1] - p0[i][1]
        span = ex * ex + ey * ey
        t = 0.0 if span < 1e-18 else max(0.0, min(1.0, (
            (h0 - p0[i][0]) * ex + (h1 - p0[i][1]) * ey) / span))
        cx, cy = p0[i][0] + t * ex, p0[i][1] + t * ey
        d = math.hypot(h0 - cx, h1 - cy)
        h = z[i] + t * (z[j] - z[i])
        if best is None or d < best[0] - 1e-9 or (abs(d - best[0]) <= 1e-9
                                                 and h > best[1]):
            best = (d, h)
    return best


def roof_shells(tris):
    """The roof's connected components, welded by position.

    A building's roof is one shell; a house with a kitchen ell has two, at two
    different ridge heights. The distinction matters because a stack built OUTSIDE a
    wall never passes through anything, so what it has to clear is the ridge of the
    roof it stands against — and measuring it against the wrong element's ridge is the
    per-building error this instrument exists to avoid.
    """
    weld, parent = {}, list(range(len(tris)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for t, tri in enumerate(tris):
        for v in tri:
            key = (round(v[0], 4), round(v[1], 4), round(v[2], 4))
            if key in weld:
                ra, rb = find(weld[key]), find(t)
                if ra != rb:
                    parent[ra] = rb
            else:
                weld[key] = t
    shells = {}
    for t in range(len(tris)):
        shells.setdefault(find(t), []).append(t)
    return list(shells.values())


def roof_reference(tris, shells, stack_pts):
    """The highest roof this stack has to clear, and which rule found it.

    `through` — the stack's axis stands over the roof, so the reference is the roof
    surface interpolated directly under it. That is what section 18 measures: a pipe
    "passing through the roof" is eighteen inches above the roof AT THE PENETRATION,
    not above the ridge it happens to sit near.

    `beside` — nothing is over the axis. `log_dwelling` builds its stacks OUTSIDE the
    wall, against the building, precisely so a stick-and-clay flue can be pulled down
    when it catches fire, and such a flue passes through no roof at all. Section 18's
    first clause does not reach it (its second clause, forbidding a stove pipe through
    the SIDE or END of a building, is the one that speaks to this arrangement and it
    speaks about stove pipes rather than chimneys). What is measurable is the ridge it
    is carried past, so the reference is the highest point of the roof shell it stands
    against — not the eave it happens to be nearest, which would report a cabin's stack
    three metres proud of a roof it stands 0.72 m proud of.
    """
    lo0 = min(p[H0] for p in stack_pts)
    hi0 = max(p[H0] for p in stack_pts)
    lo1 = min(p[H1] for p in stack_pts)
    hi1 = max(p[H1] for p in stack_pts)
    axis = ((lo0 + hi0) / 2.0, (lo1 + hi1) / 2.0)

    hits = [closest_on_triangle(t, *axis) for t in tris]
    if not hits:
        return None, "none"
    through = max((z for d, z in hits if d <= 1e-9), default=None)
    if through is not None:
        return through, "through"
    nearest = min(range(len(hits)), key=lambda i: hits[i][0])
    shell = next(sh for sh in shells if nearest in sh)
    return max(v[UP] for t in shell for v in tris[t]), "beside"


def stacks_of(path, archetype, count):
    """Every stack on one building: its projection above the roof it passes through."""
    mat = STACK_MATERIAL.get(archetype)
    if mat is None:
        raise ValueError(f"archetype '{archetype}' counts chimneys and this gate does "
                         f"not know which material it paints its stacks — add it to "
                         f"STACK_MATERIAL rather than letting its stacks go unmeasured")
    js, bins = read_glb(path)
    stack_prim = primitive_of(js, mat)
    roof_prim = primitive_of(js, "roof")
    if stack_prim is None:
        raise ValueError(f"no '{mat}' primitive, but the record counts {count} stack(s)")
    if roof_prim is None:
        raise ValueError("no 'roof' primitive to measure a stack against")

    stack_pts = accessor(js, bins, stack_prim["attributes"]["POSITION"])
    roof_pts = accessor(js, bins, roof_prim["attributes"]["POSITION"])
    idx = [i[0] for i in accessor(js, bins, roof_prim["indices"])]
    roof_tris = [(roof_pts[idx[i]], roof_pts[idx[i + 1]], roof_pts[idx[i + 2]])
                 for i in range(0, len(idx) - 2, 3)]

    shells = roof_shells(roof_tris)
    groups = split_stacks(stack_pts)
    if len(groups) != count:
        raise ValueError(f"the record counts {count} stack(s) and the mesh splits into "
                         f"{len(groups)} at {LINK_M} m — one of the two is wrong, and "
                         f"a merged pair would hide a short stack")

    out = []
    for g in groups:
        pts = [stack_pts[i] for i in g]
        top = max(p[UP] for p in pts)
        ref, rule = roof_reference(roof_tris, shells, pts)
        if ref is None:
            raise ValueError("no roof geometry at all to measure a stack against")
        out.append({"top": top, "roof": ref, "clear": top - ref, "rule": rule})
    return sorted(out, key=lambda s: s["clear"])


def readings():
    manifest = json.loads((ROOT / "assets" / "manifest.json").read_text())["assets"]
    by_key = {(a["structure_id"], a.get("phase_id")): (name, a.get("archetype"))
              for name, a in manifest.items() if "structure_id" in a}
    rows, problems = [], []
    for path in sorted((ROOT / "data" / "structures").glob("*.json")):
        rec = json.loads(path.read_text())
        for phase in rec.get("phases", []):
            n = chimney_count(phase)
            if n <= 0:
                continue
            key = (rec["id"], phase.get("id"))
            if key not in by_key:
                problems.append(f"{rec['id']}: counts {n} stack(s) and has no built asset")
                continue
            name, arch = by_key[key]
            try:
                stacks = stacks_of(ROOT / "assets" / "gltf" / name, arch, n)
            except ValueError as exc:
                problems.append(f"{rec['id']}: {exc}")
                continue
            for s in stacks:
                rows.append({"id": rec["id"], "archetype": arch, **s})
    return rows, problems


# ------------------------------------------------------------------ the self-test

def self_test():
    """Every way this instrument could report a compliant town that is not one.

    The gate is only worth what its ability to fail is worth, and each case below is a
    reading that WOULD have been reported as compliant before it was written. Two of
    them are not hypothetical: taking the first tie on a vertical gable-end fill read
    every log cabin's stack against the eave rather than the apex, and measuring a
    building's stacks as one primitive hid a stack on a lower ell entirely.
    """
    cases = []

    def case(label, ok):
        cases.append((label, bool(ok)))

    # 1-2. the clustering separates the closest pair any archetype builds and joins the
    #      widest corbelled head any archetype builds
    case("the closest pair an archetype builds stays two stacks",
         len(split_stacks([(0, 0, 0), (2.8, 0, 0)])) == 2)
    case("the widest head an archetype builds stays one stack",
         len(split_stacks([(0, 0, 0), (0.98, 0, 0), (0.98, 0, 0.98),
                           (0, 0, 0.98)])) == 1)

    # 3. an archetype this gate was never taught about is refused, not skipped
    try:
        stacks_of(ROOT / "assets" / "manifest.json", "brick_kiln", 1)
        case("an archetype with no stack material is refused", False)
    except ValueError:
        case("an archetype with no stack material is refused", True)

    # 4-5. the roof surface is interpolated where the stack breaks it, and a point off
    #      the roof is not reported as standing over it
    slope = ((0.0, 0.0, 0.0), (4.0, 2.0, 0.0), (0.0, 0.0, 4.0))
    d, z = closest_on_triangle(slope, 2.0, 1.0)
    case("a slope is interpolated, not rounded to a vertex", d == 0.0 and abs(z - 1.0) < 1e-9)
    case("a point off the roof reads a distance", closest_on_triangle(slope, 9.0, 9.0)[0] > 0)

    # 6. THE GABLE-END TIE. A gable end is vertical, so it projects to a LINE and every
    #    point on it is the same distance away. Taking the first tie takes the eave.
    gable = ((0.0, 2.6, 0.0), (6.0, 2.6, 0.0), (3.0, 4.9, 0.0))
    case("a vertical gable end reads its apex, not its eave",
         abs(closest_on_triangle(gable, 3.0, -0.1)[1] - 4.9) < 1e-9)

    # 7. THE ELL. Two roof shells at two ridge heights are two shells, so a stack on the
    #    lower one is not measured against the higher one's ridge.
    main = [((0.0, 3.0, 0.0), (4.0, 3.0, 0.0), (2.0, 6.0, 2.0)),
            ((0.0, 3.0, 0.0), (2.0, 6.0, 2.0), (0.0, 3.0, 4.0))]
    ell = [((9.0, 2.0, 0.0), (11.0, 2.0, 0.0), (10.0, 4.0, 0.0))]
    case("a kitchen ell's roof is its own shell", len(roof_shells(main + ell)) == 2)

    # 8. and a stack standing beside that ell clears the ELL's ridge
    beside_ell = [(9.4, 0.0, -0.6), (10.6, 0.0, -0.6), (9.4, 4.6, -0.6), (10.6, 4.6, -0.6)]
    ref, rule = roof_reference(main + ell, roof_shells(main + ell), beside_ell)
    case("a stack beside the ell clears the ell's ridge, not the main one",
         rule == "beside" and abs(ref - 4.0) < 1e-9)

    # 9-10. the bracket is the two documented numbers and nothing else
    case("eighteen inches is 0.4572 m", abs(FLOOR_M - 0.4572) < 1e-12)
    case("four feet is 1.2192 m", abs(CEILING_M - 1.2192) < 1e-12)

    for label, ok in cases:
        print(f"  {'ok    ' if ok else 'MISSED'}  {label}")
    bad = [c for c in cases if not c[1]]
    print(f"SELF-TEST {'PASS' if not bad else 'FAIL'} — "
          f"{len(cases) - len(bad)}/{len(cases)} assertions hold")
    return 1 if bad else 0


# ------------------------------------------------------------------ the report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true", help="pass/fail only")
    ap.add_argument("--quiet", action="store_true", help="suppress the per-stack table")
    ap.add_argument("--by-archetype", action="store_true",
                    help="the census grouped by the archetype that built the stack")
    ap.add_argument("--self-test", action="store_true",
                    help="prove the instrument's own assertions fire")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    rows, problems = readings()
    short = [r for r in rows if r["clear"] < FLOOR_M]
    tall = [r for r in rows if r["clear"] > CEILING_M]

    if not (args.gate or args.quiet):
        width = max((len(r["id"]) for r in rows), default=10)
        print(f"{'structure':<{width}}  {'archetype':<17} {'above its roof':>14}  "
              f"{'in inches':>9}  read")
        for r in sorted(rows, key=lambda r: (r["clear"], r["id"])):
            flag = ("  <- UNDER EIGHTEEN INCHES" if r["clear"] < FLOOR_M
                    else "  <- OVER FOUR FEET" if r["clear"] > CEILING_M else "")
            print(f"{r['id']:<{width}}  {(r['archetype'] or '?'):<17} "
                  f"{r['clear']:>12.3f} m  {r['clear'] / INCH:>8.1f}\"  "
                  f"{r['rule']}{flag}")
        print()

    if args.by_archetype and not args.gate:
        fam = {}
        for r in rows:
            fam.setdefault(r["archetype"], []).append(r["clear"])
        print("by archetype, the projection above the roof each one builds:")
        for arch in sorted(fam, key=str):
            v = fam[arch]
            print(f"  {(arch or '?'):<17} {len(v):>4} stacks   "
                  f"{min(v):.3f}–{max(v):.3f} m   "
                  f"({min(v) / INCH:.1f}–{max(v) / INCH:.1f} in)")
        print()

    if problems:
        for p in problems:
            print(f"FAIL: {p}")
        return 1

    if not args.quiet:
        lo = min(r["clear"] for r in rows) if rows else 0.0
        hi = max(r["clear"] for r in rows) if rows else 0.0
        print(f"{len(rows)} stacks on "
              f"{len({r['id'] for r in rows})} buildings, projecting "
              f"{lo:.3f}–{hi:.3f} m ({lo / INCH:.1f}–{hi / INCH:.1f} in) above the roof "
              f"each passes through.")

    if short:
        print(f"FAIL: {len(short)} stack(s) stand under eighteen inches above their own "
              f"roof, which the ordinance of 5 August 1835 forbids under a five-dollar "
              f"penalty (chicago_democrat_1835_08_19#c005, and the same figure in the "
              f"fire ordinance of 26 November 1833 that was in force at the scene date): "
              f"{', '.join(sorted({r['id'] for r in short}))}. Raise the stack — do not "
              f"lower the bar. If one of these stands OUTSIDE the limits of the "
              f"Corporation the ordinance does not bind it, and the answer is to derive "
              f"that boundary (T-0334), not to weaken this gate.")
        return 1
    if tall:
        print(f"FAIL: {len(tall)} stack(s) stand over four feet above their own roof, "
              f"which contradicts Andreas's description of a town with 'not a single "
              f"steeple nor a chimney four feet above any roof': "
              f"{', '.join(sorted({r['id'] for r in tall}))}")
        return 1
    if not args.quiet:
        print(f"OK: all {len(rows)} stacks in the town stand inside the bracket the "
              f"ordinance's eighteen inches and Andreas's four feet make "
              f"({FLOOR_M:.4f}–{CEILING_M:.4f} m).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
