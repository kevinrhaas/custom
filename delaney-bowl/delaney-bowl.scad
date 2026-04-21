//
// Wavy Bowl — Simplified & Manifold-Safe
// Uses CSG difference() of two closed polyhedron solids.
// OpenSCAD's CGAL engine guarantees watertight output.
//

///////////////////////
// PARAMETERS
///////////////////////
base_radius      = 60;     // mm — outer radius at base
height           = 20;     // mm — nominal bowl height
pitch_deg        = 40;     // degrees — wall flare angle
wall_thickness   = 5;      // mm
bottom_thickness = 2.0;    // mm — solid flat floor

// Rim height waviness
rim_z_waves         = 3;
rim_z_amp           = 9.0;    // mm
rim_z_irregular     = 0.45;   // 0 = pure sine, 1 = fully irregular
rim_z_phase_deg     = 0;
rim_z_falloff_width = 0.99;   // fraction of height affected (0..1)

// Resolution (lower = faster render, higher = smoother)
fn_theta = 180;    // angular steps
fn_z     = 60;     // vertical steps

///////////////////////
// HELPERS
///////////////////////
function clamp(x, a, b) = x < a ? a : (x > b ? b : x);

function smoothstep(e0, e1, x) =
    let(t = clamp((x - e0) / (e1 - e0), 0, 1))
    t * t * (3 - 2 * t);

// Height-dependent rim waviness offset
function rim_z_offset(theta_deg, zfrac) =
    (rim_z_amp <= 0 || rim_z_waves <= 0) ? 0 :
    let(
        n  = max(rim_z_waves, 1),
        ph = rim_z_phase_deg,
        k  = clamp(rim_z_irregular, 0, 1),
        w  = smoothstep(1 - rim_z_falloff_width, 1.0, zfrac),
        base_val = sin(n * theta_deg + ph),
        mix1 = 0.6 * sin((n + 3) * theta_deg + 1.3 * ph)
             + 0.4 * sin(max(1, n - 2) * theta_deg - 0.9 * ph),
        mixed = (1 - k) * base_val + k * mix1
    )
    rim_z_amp * mixed * w;

// Outer radius at a given height z
function r_at_z(z) = base_radius + z * tan(pitch_deg);

///////////////////////
// CLOSED SOLID
///////////////////////
// Builds a watertight polyhedron solid.
//   inset:   radial shrink (0 = outer shell, wall_thickness = inner cavity)
//   z_floor: bottom z of this solid
//   z_cap:   z of the top center point (must be above all top-ring vertices)
module solid_body(inset, z_floor, z_cap) {
    nT = fn_theta;
    nZ = fn_z;

    total_ring_verts = (nZ + 1) * nT;
    bot_idx = total_ring_verts;        // bottom center
    top_idx = total_ring_verts + 1;    // top center

    z_span = height - z_floor;

    points = concat(
        // Ring vertices from bottom to top
        [ for (iZ = [0:nZ])
          for (iT = [0:nT-1])
            let(
                frac = iZ / nZ,
                z    = z_floor + z_span * frac,
                th   = 360 * iT / nT,
                r    = max(0.5, r_at_z(z) - inset),
                dz   = rim_z_offset(th, frac),
                zz   = z + dz
            )
            [r * cos(th), r * sin(th), zz]
        ],
        // Center points
        [ [0, 0, z_floor],
          [0, 0, z_cap] ]
    );

    faces = concat(
        // Wall quads (split into triangles)
        [ for (iZ = [0:nZ-1], iT = [0:nT-1])
            let(
                iT2 = (iT + 1) % nT,
                a = iZ * nT + iT,
                b = iZ * nT + iT2,
                c = (iZ + 1) * nT + iT2,
                d = (iZ + 1) * nT + iT
            )
            each [[a, b, c], [a, c, d]]
        ],
        // Bottom disk (fan, facing downward)
        [ for (iT = [0:nT-1])
            let(iT2 = (iT + 1) % nT)
            [iT2, iT, bot_idx]
        ],
        // Top cap (fan, facing upward)
        [ for (iT = [0:nT-1])
            let(
                iT2 = (iT + 1) % nT,
                a = nZ * nT + iT,
                b = nZ * nT + iT2
            )
            [a, b, top_idx]
        ]
    );

    polyhedron(points = points, faces = faces, convexity = 10);
}

///////////////////////
// BOWL = OUTER minus INNER
///////////////////////
difference() {
    // Outer solid: flat bottom at z=0, cap barely above highest rim
    solid_body(
        inset   = 0,
        z_floor = 0,
        z_cap   = height + rim_z_amp + 0.5
    );
    // Inner cutout: starts at floor thickness, cap well above for full subtraction
    solid_body(
        inset   = wall_thickness,
        z_floor = bottom_thickness,
        z_cap   = height + rim_z_amp + 40
    );
}
