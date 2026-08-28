#!/usr/bin/env python3
"""Derive North Water Street's platted line from the committed north bank.

T-0226. North Water Street's committed line ran 477.4 m of its 843.3 m INSIDE the
terrain's water mask, in one unbroken run from [200.2, 55] to [675.4, 95.7], and
`renderers/web/js/streets.js` therefore drew no roadway at all across that reach:
R-BUG4 drops any panel whose centreline endpoint is wet, because a crossing is a
bridge's job and a ford is not something a ribbon may paint. Three of the street's
six authored bends stood in the river.

WHICH RECORD WAS WRONG, and this tool is the answer to that question rather than a
nudge to close the gap. The two candidates were the traced north bank and the street
line, and only one of them is a reading of a source:

  * The BANK is a trace. `data/terrain/epochs/e1834_harbor_cut/river.geojson` carries
    `traced_from: wright_1834`, the segmentation method, the IIIF region and its
    sha256, `affine_rms_m: 17.5` and a stated `uncertainty_m: 20`.
  * The STREET LINE was not. Its own note said so in its own words -- "a schematic
    bank-following path used for orientation and readout ... the committed street
    module does not yet carry enough control to claim this curve as a trace" -- it
    graded its geometry `reconstructed`, the bottom tier, and it has no entry in
    `data/traces/street_control.json`, which is where a street's control lives.
  * The project had ALREADY adjudicated the conflict, in the bank's favour and in
    writing. `data/reconstruction/1835_north_division_initial_parcel.json` places the
    North Division's roofs under the constraint "Reject any footprint whose sampled
    terrain cell is water; PROXIMITY TO NORTH WATER STREET NEVER OVERRIDES THE
    AUTHORITATIVE WATER MASK", and its occupied envelope's south edge is N +105 --
    north of every point the old street line held west of E +700.
  * And the disagreement was far too big to be tracing wobble: the old line ran from
    1 m to 86 m south of the bank along that reach, up to 4.3x the trace's own stated
    +/-20 m.

So the street line is the record that was wrong, the bank is left exactly as it is,
and the line is re-derived here FROM the bank rather than drawn beside it.

THE DERIVATION. North Water Street fronted the main stem on its north side, so its
platted corridor is laid with its SOUTH line on the committed bank and the centreline
falls half a platted street north of it -- 12.192 m, the `thompson_module_1830`
half-width committed in `data/traces/street_control.json` and applied town-wide. At
each 5 m station the north bank of the main stem is read off the committed
heightfield exactly as the renderer reads it (`terrain.isWater` is
`heightfield.sample(e, n) < -0.10`), and the required centreline is that bank plus the
half-width. The polyline is then the fewest straight runs that stay north of every
station's requirement and never wander more than MAX_ABOVE_M beyond it, so the drawn
6 m track sits between 9.2 m and 15.2 m clear of the water along the whole reach and
no panel is trimmed.

THE SLOUGH IS CROSSED, NOT STOPPED AT -- T-0254, and it is why this tool derives TWO
reaches with a structure between them. The attested "Unnamed slough, north side"
(`hydrology.geojson`, confidence `attested`, Wright 1834 draws it running north out of
the main stem across Kinzie Street) meets the river in a funnel between E +170 and
E +270 reaching N +145; north of that funnel the channel settles to a steady 5-7 m.
A ribbon may not paint over a watercourse -- the town's other two slough crossings are
modelled STRUCTURES, `slough_log_bridge` and the La Salle Slough Crossing -- so the
street goes ROUND THE HEAD OF THE BAY and crosses the narrow reach above it on a third
one, `north_water_slough_crossing`, whose deck runs E +183 .. +195 at N +157.5.

  * the EAST reach runs from the deck's east end to E +830, as before;
  * the WEST reach runs from the deck's west end to the North Branch at E -30, laid on
    the same bank with the same setback;
  * ONE BEND STANDS IN THE WATER, at the deck's midpoint. That is deliberate and it is
    the thing R-BUG4 is for: `renderers/web/js/streets.js` drops a panel whose
    centreline endpoint is wet, so the two panels either side of that bend are dropped
    and the deck carries the crossing. Carrying the line across with dry bends at each
    shoulder would have drawn a 6.65 m ford in silence -- the fault T-0254 was filed to
    avoid, not a shortcut past it.

Each reach's smoothing window is clamped INSIDE its own reach. The running maximum
exists to clear metre-scale notches in a trace, and looking across the crossing is not
that: at E +190 the funnel and the slough are one water run reaching N +165, and a
window that saw it would push the street 20 m up the slough instead of over it.

    tools/derive_north_water.py            print the derivation
    tools/derive_north_water.py --write    write it into data/streets/1835.json
    tools/derive_north_water.py --gate     exit 1 if the committed line is not this one
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPOCH = ROOT / "data" / "terrain" / "epochs" / "e1834_harbor_cut"
STREETS = ROOT / "data" / "streets" / "1835.json"

# The renderer's own waterline (renderers/web/js/terrain.js SHORE_Y). Read it here
# rather than restating a number: a mask the ribbon disagrees with is the whole fault.
SHORE_Y = -0.10

SETBACK_M = 12.192          # half the 80 ft platted street module, thompson_module_1830
STATION_M = 5.0             # how finely the bank is read
MAX_ABOVE_M = 8.0           # how far a straight run may stand north of what it needs
SMOOTH_M = 15.0             # a bank notch this short is cleared, not followed
BELOW_M = 0.5               # how far a run may fall short of the setback (see fit)
E_EAST = 830.0              # where the street leaves the bank and climbs to Kinzie
TAIL = [[920.0, 190.0], [970.0, 270.0]]   # unchanged: dry, drawn, and not in question

# THE CROSSING (T-0254). These three numbers are the deck's, and they are read off
# `data/structures/north_water_slough_crossing.json` rather than restated -- the
# structure record is the one that decides where the crossing is, and a deck that moves
# has to move the street with it or the two disagree in silence.
CROSSING = "north_water_slough_crossing"
# The North Branch. West of E -35 the widest water run at an easting is no longer the
# main stem: the branch merges into it and its north edge jumps from N +33 to N +216 in
# one 5 m step, so the setback rule has nothing to read. The street ends where the
# street ended -- at the branch.
E_WEST_END = -30.0


def load_field():
    spec = json.loads((EPOCH / "heightfield.json").read_text())
    cols, rows = spec["cols"], spec["rows"]
    raw = (EPOCH / "heightfield.bin").read_bytes()
    grid = struct.unpack("<%dh" % (cols * rows), raw)
    cell, scale = spec["cell_m"], spec["scale"]
    oe, on = spec["origin_e"], spec["origin_n"]

    def sample(e, n):
        x = (e - oe) / cell
        y = (n - on) / cell
        if x < 0 or y < 0 or x > cols - 1 or y > rows - 1:
            return None
        x0, y0 = int(x), int(y)
        x1, y1 = min(x0 + 1, cols - 1), min(y0 + 1, rows - 1)
        fx, fy = x - x0, y - y0
        g = lambda c, r: grid[r * cols + c] * scale
        lo = g(x0, y0) * (1 - fx) + g(x1, y0) * fx
        hi = g(x0, y1) * (1 - fx) + g(x1, y1) * fx
        return lo * (1 - fy) + hi * fy

    def is_water(e, n):
        v = sample(e, n)
        return v is not None and v < SHORE_Y

    return is_water


def north_bank(is_water, e, step=0.25):
    """North edge of the MAIN STEM at this easting.

    Not "the first dry northing above the first water": the two committed slough
    cuts (`slough_log_bridge` at E 805-813 and the La Salle Slough Crossing at
    E 461-473) put a narrow south-side channel in the way, and a walk that starts
    below them answers with the drain's own north lip. The main stem is by a wide
    margin the widest water run on any of these eastings, so the widest run is the
    one that is asked, and its north end is the bank.
    """
    runs = []
    n = -80.0
    start = None
    while n < 260.0:
        wet = is_water(e, n)
        if wet and start is None:
            start = n
        elif not wet and start is not None:
            runs.append((start, n))
            start = None
        n += step
    if start is not None:
        runs.append((start, n))
    if not runs:
        return None
    return max(runs, key=lambda r: r[1] - r[0])[1]


def deck():
    """The crossing's deck, read out of the structure record.

    Returns (west_end_e, east_end_e, centreline_n). The record's footprint polygon IS
    the deck -- u along the span, v across the width -- laid at the placement, exactly
    as tools/measure_slough_crossing.py reads it. Read rather than restated so a deck
    that is re-sized or re-sited moves this street with it instead of leaving the two
    records disagreeing about where the town crosses its own slough.
    """
    rec = json.loads((ROOT / "data" / "structures" / (CROSSING + ".json")).read_text())
    phase = rec["phases"][0]
    poly = [(float(u), float(v)) for u, v in phase["footprint"]["polygon"]]
    if float(phase["position"].get("rotation_deg", 0.0)) != 0.0:
        raise SystemExit("%s is no longer laid square; this tool reads an east-west "
                         "deck and would have to be taught the rotation" % CROSSING)
    e0 = float(phase["position"]["utm_e"])
    n0 = float(phase["position"]["utm_n"])
    datum = json.loads((ROOT / "data" / "datum.json").read_text())
    e0 -= float(datum["origin_utm_e"])
    n0 -= float(datum["origin_utm_n"])
    us = [u for u, _ in poly]
    vs = [v for _, v in poly]
    return e0 + min(us), e0 + max(us), n0 + 0.5 * (min(vs) + max(vs))


def stations(is_water, e_from, e_to, anchor=None):
    """Bank and required centreline at every station of ONE reach.

    The requirement is a running MAXIMUM of the bank over +/-SMOOTH_M rather than the
    bank at the station itself, because a 2.5 m heightfield cell reading a trace with
    +/-20 m of paper stretch in it produces metre-scale notches, and a line that
    followed those would be a street with a bend every 5 m. Clearing them is the
    honest reading: the bank is where it is, and the street stands north of all of it.

    THE WINDOW IS CLAMPED TO THE REACH. It used to reach SMOOTH_M past both ends, which
    was harmless while the reach ended in open bank; it is not harmless now that a reach
    ends AT THE CROSSING, because the water on the far side of the deck is the slough
    and the running maximum would read its far bank as this street's.

    `anchor` is (easting, northing) -- the deck's own abutment, imposed at the reach's
    crossing end: the
    street has to arrive AT the abutment, not at where the setback rule would have put
    it. The two differ by 7.6 m at the west abutment -- the bay's edge is still climbing
    there -- and that difference is the crossing's approach, carried by the fit's
    ordinary MAX_ABOVE_M slack rather than by a special case.
    """
    raw = []
    e = e_from
    while e <= e_to + 1e-9:
        bank = north_bank(is_water, e)
        if bank is None:
            raise SystemExit("no north bank at E %.1f" % e)
        raw.append((e, bank))
        e += STATION_M
    if abs(raw[-1][0] - e_to) > 1e-9:
        bank = north_bank(is_water, e_to)
        if bank is None:
            raise SystemExit("no north bank at E %.1f" % e_to)
        raw.append((e_to, bank))
    out = []
    for e, bank in raw:
        window = [b for f, b in raw if abs(f - e) <= SMOOTH_M + 1e-9]
        out.append((e, bank, max(window) + SETBACK_M))
    if anchor is not None:
        ae, an = anchor
        for i, (e, bank, _) in enumerate(out):
            if abs(e - ae) < 1e-9:
                out[i] = (e, bank, an)
                break
        else:
            raise SystemExit("the deck's abutment at E %.1f is not a station of the "
                             "reach E %.1f .. %.1f" % (ae, e_from, e_to))
    return out


def clears(st, pts, i0, i1, slack):
    """Does the straight run pts[i0]->pts[i1] clear every station beneath it?"""
    e0, n0 = pts[i0]
    e1, n1 = pts[i1]
    for e, _, need in st:
        if e < min(e0, e1) - 1e-9 or e > max(e0, e1) + 1e-9:
            continue
        t = (e - e0) / (e1 - e0) if e1 != e0 else 0.0
        n = n0 + (n1 - n0) * t
        if n < need - BELOW_M or n > need + slack:
            return False
    return True


def fit(st):
    """Fewest straight runs that clear every station and stay within MAX_ABOVE_M.

    BELOW_M is the reason this is four runs and not ten. Held to the setback exactly,
    the fit has to break every time the bank rises a decimetre, and the town gets a
    street that changes bearing by a degree every 30 m -- which the joint probe reads
    as slivers of uncovered ground at bends too shallow to be bends. Half a metre of
    give is 2.5 % of the bank trace's own stated +/-20 m: immaterial to the claim, and
    the difference between a street and a jitter.
    """
    pts = [[st[0][0], st[0][2]]]
    i = 0
    while i < len(st) - 1:
        j = len(st) - 1
        while j > i + 1 and not clears(st, pts + [[st[j][0], st[j][2]]], len(pts) - 1, len(pts), MAX_ABOVE_M):
            j -= 1
        pts.append([st[j][0], st[j][2]])
        i = j
    # The greedy run has to stop the moment it cannot reach any further, which leaves
    # short stubs at every place the bank turns. Drop a bend whose neighbours can see
    # each other across it: fewer, longer runs, the same clearance guarantee.
    changed = True
    while changed and len(pts) > 2:
        changed = False
        for k in range(1, len(pts) - 1):
            if clears(st, pts, k - 1, k + 1, MAX_ABOVE_M):
                del pts[k]
                changed = True
                break
    return pts


def reach(is_water, e_from, e_to, anchor):
    st = stations(is_water, e_from, e_to, anchor)
    pts = [[round(e, 1), round(n, 1)] for e, n in fit(st)]
    # Rounding to a decimetre can only move a vertex 5 cm; lift any that fell short.
    for pt in pts:
        need = next(s for s in st if abs(s[0] - pt[0]) < 1e-6)[2]
        if pt[1] < need:
            pt[1] = round(need + 0.05, 1)
    return pts, st


def derive():
    is_water = load_field()
    w_end, e_end, n_deck = deck()
    west, st_w = reach(is_water, E_WEST_END, w_end, (w_end, n_deck))
    east, st_e = reach(is_water, e_end, E_EAST, (e_end, n_deck))
    # THE BEND IN THE WATER. One vertex at the deck's midpoint, and it is wet on
    # purpose: R-BUG4 drops a panel whose centreline endpoint is wet, so the two panels
    # that reach the abutments go with it and the deck is what a visitor crosses on.
    mid = [round(0.5 * (w_end + e_end), 1), round(n_deck, 1)]
    return west + [mid] + east + [list(t) for t in TAIL], st_w + st_e, is_water


def report(path, st, is_water):
    print("North Water Street, derived from the committed north bank")
    print("  setback %.3f m north of the bank (half the 80 ft platted module)" % SETBACK_M)
    print("  %d authored bends, %s" % (len(path), " ".join("[%g, %g]" % (e, n) for e, n in path)))
    worst_low, worst_high = 99.0, 0.0
    wet = 0.0
    total = 0.0
    w_end, e_end, _n_deck = deck()
    for i in range(len(path) - 1):
        e0, n0 = path[i]
        e1, n1 = path[i + 1]
        length = ((e1 - e0) ** 2 + (n1 - n0) ** 2) ** 0.5
        total += length
        steps = max(1, int(length / 0.5))
        for k in range(steps + 1):
            t = k / steps
            e, n = e0 + (e1 - e0) * t, n0 + (n1 - n0) * t
            if is_water(e, n):
                wet += 0.5
    for e, bank, need in st:
        if w_end - 1e-9 <= e <= e_end + 1e-9:
            continue          # the deck's own span: measured by measure_slough_crossing
        n = at(path, e)
        worst_low = min(worst_low, n - bank)
        worst_high = max(worst_high, n - bank)
    print("  length %.1f m, of which wet centreline: %.1f m" % (total, wet))
    print("  clearance from the waterline, northward: %.2f m .. %.2f m"
          % (worst_low, worst_high))
    # THE NORTHWARD FIGURE IS NOT THE CLEARANCE A WALKER SEES, and on the west reach the
    # two part company. The setback is applied northward and the running maximum is
    # taken over +/-SMOOTH_M, both of which were written for the east reach's roughly
    # east-west bank. West of the slough the bank runs at 30-60 degrees as it comes
    # round Wolf Point into the forks, so a northward offset buys only its cosine in
    # perpendicular clearance while the running maximum, lagging a steadily rising
    # bank, adds it back and more. Neither is wrong -- the street stands north of every
    # bank point within 15 m of it, which is what the rule says -- but the honest
    # statement of how far the road is from the water is this one.
    print("  clearance from the waterline, perpendicular: %.2f m .. %.2f m"
          % perpendicular_clearance(path, is_water, w_end, e_end))
    _w, _e, n_deck = w_end, e_end, deck()[2]
    dry_edges = [q for q in edge_probes(path)
                 if not (w_end - 4.0 <= q[0] <= e_end + 4.0) and is_water(*q)]
    print("  the drawn 6 m track's own edges, off the deck: %s"
          % ("all dry" if not dry_edges else "%d WET" % len(dry_edges)))
    print("  bends standing in water: %s"
          % (" ".join("[%g, %g]" % (e, n) for e, n in path if is_water(e, n)) or "none"))
    print("  the crossing: %s, deck E %g .. %g at N %g" % (CROSSING, w_end, e_end, n_deck))


def perpendicular_clearance(path, is_water, w_end, e_end, step=2.0):
    """Shortest distance from the drawn centreline to water, off the deck's own span.

    Walked rather than solved: at every station along the path a ray is pushed out
    square to the chord, on both sides, until it finds water or gives up at 80 m. The
    minimum and maximum of those are the two numbers -- how close the road comes to the
    river anywhere, and how far it stands off it at its worst.
    """
    lo, hi = 999.0, 0.0
    for i in range(len(path) - 1):
        e0, n0 = path[i]
        e1, n1 = path[i + 1]
        length = ((e1 - e0) ** 2 + (n1 - n0) ** 2) ** 0.5
        if length < 1e-9:
            continue
        ue, un = -(n1 - n0) / length, (e1 - e0) / length
        for k in range(int(length / step) + 1):
            t = k * step / length
            e, n = e0 + (e1 - e0) * t, n0 + (n1 - n0) * t
            if w_end - 4.0 <= e <= e_end + 4.0:
                continue          # the deck's own reach; the crossing owns that water
            d = 80.0
            for side in (1, -1):
                r = 0.0
                while r < d:
                    r += 0.5
                    if is_water(e + ue * side * r, n + un * side * r):
                        d = r
                        break
            lo, hi = min(lo, d), max(hi, d)
    return lo, hi


def at(path, e):
    for i in range(len(path) - 1):
        e0, n0 = path[i]
        e1, n1 = path[i + 1]
        if min(e0, e1) <= e <= max(e0, e1):
            t = (e - e0) / (e1 - e0) if e1 != e0 else 0.0
            return n0 + (n1 - n0) * t
    return path[-1][1]


def edge_probes(path, half=3.0, step=1.0):
    out = []
    for i in range(len(path) - 1):
        e0, n0 = path[i]
        e1, n1 = path[i + 1]
        length = ((e1 - e0) ** 2 + (n1 - n0) ** 2) ** 0.5
        ue, un = -(n1 - n0) / length, (e1 - e0) / length
        for k in range(int(length / step) + 1):
            t = k * step / length
            e, n = e0 + (e1 - e0) * t, n0 + (n1 - n0) * t
            out.append((e + ue * half, n + un * half))
            out.append((e - ue * half, n - un * half))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args()

    path, st, is_water = derive()
    doc = json.loads(STREETS.read_text())
    street = next(s for s in doc["streets"] if s["id"] == "north_water")

    if args.gate:
        committed = [[float(e), float(n)] for e, n in street["path_local_enu_m"]]
        if committed != [[float(e), float(n)] for e, n in path]:
            print("north_water's committed line is not the one this tool derives:")
            print("  committed %s" % committed)
            print("  derived   %s" % path)
            return 1
        # ONE bend may stand in water and exactly one: the crossing's, at the deck's
        # midpoint. Every other wet bend is the fault T-0226 found -- three of the old
        # line's six bends stood in the river and the roadway simply vanished.
        w_end, e_end, n_deck = deck()
        wet = [p for p in committed if is_water(*p)]
        expect = [round(0.5 * (w_end + e_end), 1), round(n_deck, 1)]
        if wet != [expect]:
            print("north_water's bends in water are %s; the only one allowed is the "
                  "crossing's, at %s" % (wet, expect))
            return 1
        print("north_water: derived line committed, %d bends, one in water and it is "
              "%s's deck midpoint" % (len(committed), CROSSING))
        return 0

    report(path, st, is_water)
    if args.write:
        # A surgical replacement, not a re-dump: the file is hand-formatted with
        # compact inline coordinate arrays and re-serialising it would rewrite every
        # street to make one line move.
        text = STREETS.read_text()
        anchor = '"id": "north_water"'
        i = text.index(anchor)
        key = text.index('"path_local_enu_m": [', i)
        end = text.index("\n", key)
        literal = "[" + ", ".join("[%g, %g]" % (e, n) for e, n in path) + "]"
        text = text[:key] + '"path_local_enu_m": ' + literal + "," + text[end:]
        STREETS.write_text(text)
        print("  written to %s" % STREETS.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
