// ═══════════════════════════════════════════════════════════════════════════
// Geometric Sandstone Lamp  —  native parametric model
// ═══════════════════════════════════════════════════════════════════════════
//
// A faceted, jagged cousin of the Ordovician sandstone lamp.  Straight flat
// walls and sharp corners, following a procedural "sandstone motion" of strata
// that swell and pinch up the height.  Everything below is live-tunable in the
// OpenSCAD Customizer (Window ▸ Customizer) — drag a slider, hit F5.
//
// Jaggedness = rotate (twist) the polygon per layer  +  per-corner radial
// jitter that drifts up the height.  Both on by default.
//
// Fits the standard 80mm lamp-connect base: hollow shade, solid base, and a
// centre hole for the hardware/cord.  All fit dimensions are parameters.
//
// For a baked, print-ready STL with identical math (and round high-res caps),
// use:  python3 generate_geometric_sandstone.py
// ═══════════════════════════════════════════════════════════════════════════

/* [Form] */
height      = 150;   // [50:300]
facets      = 7;     // [3:24]    number of flat sides
mean_r      = 45;    // [20:80]   mean exterior radius (mm)
layers      = 120;   // [12:240]  strata resolution up the height
taper       = 0.0;   // [0:0.005:0.4]  top narrowing over full height

/* [Strata Bands] */
strata_bands = 22;   // [2:60]          number of stacked sediment shelves
band_amp     = 0.07; // [0:0.005:0.25]  shelf depth, fraction of radius
band_blend   = 0.4;  // [0.02:0.02:1]   0=hard ledges, 1=fully merged layers

/* [Jaggedness] */
strata_amp  = 0.05;  // [0:0.005:0.30]  smooth swell over the bands
jitter_amp  = 0.05;  // [0:0.005:0.20]  per-corner jaggedness, fraction of radius
twist_deg   = 12;    // [-90:90]        total facet rotation over the height
seed        = 42;    // [0:200]         which procedural rock

/* [Lamp Base Fit] */
hollow      = true;
wall        = 2.0;   // [0.8:0.1:6]
base_h      = 9.46;  // [0:0.01:20]   solid base height (mm)
hole_d      = 66;    // [0:0.5:90]    centre hole diameter (mm)
hole_fn     = 64;    // [12:128]      roundness of the centre hole

// ── Derived ────────────────────────────────────────────────────────────────
P = facets;
N = layers;

// Seed-stable random tables (deterministic in OpenSCAD).
ph   = rands(0, 360, 3, seed);                 // strata band phases
cph  = rands(0, 360, facets, seed * 3 + 1);    // per-corner phases
cfrq = rands(1.0, 4.0, facets, seed * 7 + 2);  // per-corner drift frequencies

// ── Stacked strata bands (the sedimentary shelves that merge/blend) ──
B     = max(2, strata_bands);
rthk  = rands(0, 1, B, seed * 17 + 2);             // band thickness noise
boff  = rands(-1, 1, B, seed * 29 + 4);            // per-band shelf radius
thk   = [ for (i = [0 : B - 1]) 1 + 0.6 * (rthk[i] * 2 - 1) ];
function _sum(v, i = 0) = i >= len(v) ? 0 : v[i] + _sum(v, i + 1);
total = _sum(thk);
function edge(i) = i <= 0 ? 0 : edge(i - 1) + thk[i - 1] / total;  // 0..1
function ctr(i)  = (edge(i) + edge(i + 1)) / 2;
function findi(t, i = 0) =
    (i >= B - 2) ? B - 2 : (t <= ctr(i + 1) ? i : findi(t, i + 1));
function band(t) =
    let (c0 = ctr(0), cL = ctr(B - 1))
    t <= c0 ? boff[0] :
    t >= cL ? boff[B - 1] :
    let (i = findi(t), a = ctr(i), b = ctr(i + 1),
         u = (t - a) / (b - a), h = band_blend * 0.5,
         w = max(0, min(1, (u - (0.5 - h)) / (2 * h))),
         s = w * w * (3 - 2 * w))
    boff[i] + (boff[i + 1] - boff[i]) * s;

// Smooth swell layered over the bands, in ~[-1,1].
function strata(t) =
      0.55 * sin(360 * 3.5 * t + ph[0])
    + 0.30 * sin(360 * 7.0 * t + ph[1])
    + 0.15 * sin(360 * 13.0 * t + ph[2]);

// Per-corner jitter that drifts slowly up the height.
function jit(f, t) = sin(360 * cfrq[f] * t + cph[f]);

// Exterior radius of corner f at height fraction t, optionally shrunk inward.
function rcorner(f, t, shrink) =
    (mean_r * (1 + band_amp * band(t)
                 + strata_amp * strata(t)
                 + jitter_amp * jit(f, t)))
        * (1 - taper * t) - shrink;

// Points: layer rings of facet corners, then bottom + top centres.
function tower_points(shrink) = concat(
    [ for (k = [0 : N - 1], f = [0 : P - 1])
        let (t = k / (N - 1),
             ang = 360 * f / P + twist_deg * t,
             r = rcorner(f, t, shrink))
        [ r * cos(ang), r * sin(ang), t * height ] ],
    [ [0, 0, 0], [0, 0, height] ]
);

// Faces: side quads (two tris) + bottom fan + top fan, outward-facing.
function tower_faces() = concat(
    [ for (k = [0 : N - 2], f = [0 : P - 1])
        let (f1 = (f + 1) % P) each [
            [ k*P + f, k*P + f1, (k+1)*P + f1 ],
            [ k*P + f, (k+1)*P + f1, (k+1)*P + f ] ] ],
    [ for (f = [0 : P - 1]) let (f1 = (f + 1) % P)
        [ N*P, f1, f ] ],                                  // bottom fan
    [ for (f = [0 : P - 1]) let (f1 = (f + 1) % P)
        [ N*P + 1, (N-1)*P + f, (N-1)*P + f1 ] ]           // top fan
);

module tower(shrink = 0) {
    polyhedron(points = tower_points(shrink),
               faces  = tower_faces(), convexity = 10);
}

// ── Assembly ────────────────────────────────────────────────────────────────
if (!hollow) {
    tower(0);
} else {
    difference() {
        tower(0);
        // Hollow the inside, but only above the solid base.
        intersection() {
            tower(wall);
            translate([0, 0, base_h]) cylinder(h = height, r = 1000);
        }
        // Centre hole through the solid base.
        if (hole_d > 0)
            translate([0, 0, -1])
                cylinder(h = base_h + 2, d = hole_d, $fn = hole_fn);
    }
}
