//
// Wavy-Layer Bowl (parametric) — CLOSED MANIFOLD + GUARANTEED SOLID BASE
// OpenSCAD trig is DEGREES.
//
// Fixes included:
// - Prevents degenerate bottom when floor_radius=0 (enforces a tiny minimum inner radius).
// - Makes inner_base_dish_* apply to the floor (no special-case disabling at iZ==0).
// - Treats inner_base_dish_radius_frac as 0..1 fraction.
// - Caps dish so it can’t punch through underside.
// - NEW: Removes center “dimple” shading artifact by capping the inner floor with a small center ring
//        (no single-vertex triangle fan).
//

///////////////////////
// FLOOR / BASE CONTROL
///////////////////////

// Inner radius at the *inside* bottom (at z = bottom_thickness).
// Typical: 8–18mm for a flatter floor. 0 allowed (we still keep a tiny safety radius internally).
floor_radius         = 0;   // mm

// How quickly the inner wall transitions from floor_radius to normal wall.
floor_blend_height   = 0;    // mm

// Solid floor thickness (underside z=0 to inside floor z=bottom_thickness).
bottom_thickness     = 0;  // mm

// Minimum material thickness left at the very center when using concave dish.
min_center_thickness = 0.8;  // mm (>=0.6 recommended)

///////////////////////
// CENTER CAP (VISUAL FLATNESS) 
///////////////////////

// NEW: Inner floor is capped with an annulus + small center ring instead of a single center vertex.
// This removes the “dimple” shading artifact in OpenSCAD and improves triangulation.
cap_center_radius = 0.0;   // mm (0 disables ring and reverts to center-point fan)
cap_center_verts  = 0;    // (12–48 typical)

///////////////////////
// MAIN SHAPE PARAMETERS
///////////////////////
base_radius     = 60;   // mm (outer radius at underside edge)
height          = 20;   // mm
pitch_deg       = 40;   // degrees
wall_thickness  = 5;  // mm

///////////////////////
// RADIAL SCALLOPS
///////////////////////
rim_waves       = 12;
outer_rim_waves = 12;
inner_rim_waves = 12;

rim_amp         = 3.0;
outer_rim_amp   = 4.0;
inner_rim_amp   = 2.0;

// Band placement along height (0..1). Width is fraction of height (0..1).
rim_band_center   = 0.88;  rim_band_width   = 0.0;
outer_band_center = 0.55;  outer_band_width = 0.0;
inner_band_center = 0.25;  inner_band_width = 0.0;

rim_phase_deg       = 45;
outer_rim_phase_deg = 360/(max(outer_rim_waves,1)*2);
inner_rim_phase_deg = 360/(max(inner_rim_waves,1)*3);

///////////////////////
// TOP RIM HEIGHT WAVINESS
///////////////////////
rim_z_waves         = 3;
rim_z_amp           = 9.0;
rim_z_irregular     = 0.45;
rim_z_phase_deg     = 0;
rim_z_falloff_width = 0.99;

///////////////////////
// INTERIOR BASE DISH (CONCAVE)
///////////////////////
inner_base_dish_depth       = 5.0;   // mm (0 disables)
inner_base_dish_radius_frac = 0.85;  // 0..1

///////////////////////
// OUTSIDE SHIMMER
///////////////////////
shimmer_amp       = 0;
shimmer_waves     = 0;
shimmer_z_waves   = 0;
shimmer_irregular = 0;
shimmer_phase_deg = 0;

///////////////////////
// MESH RESOLUTION
///////////////////////
fn_theta = 220;
fn_z     = 90;

///////////////////////
// HELPERS
///////////////////////
function clamp(x,a,b) = x<a ? a : (x>b ? b : x);

function smoothstep(e0,e1,x) =
    let(t = clamp((x-e0)/(e1-e0),0,1))
    t*t*(3-2*t);

function band(zf, center, width) =
    let(a = center - width/2, b = center + width/2)
    smoothstep(a, center, zf) * (1 - smoothstep(center, b, zf));

function flare(z) = z * tan(pitch_deg);

function wave(theta_deg, n, amp, phase_deg) =
    (n <= 0 ? 0 : amp * sin(n*theta_deg + phase_deg));

function shimmer(theta_deg, z) =
    (shimmer_amp <= 0 ? 0 :
        let(
            zf = z/height,
            n  = max(shimmer_waves, 1),
            n2 = n + 7,
            n3 = max(1, n - 5),
            ph = shimmer_phase_deg,
            hz = sin(360*shimmer_z_waves*zf + ph),
            k  = clamp(shimmer_irregular, 0, 1),
            base = sin(n*theta_deg + ph),
            mix1 = 0.6*sin(n2*theta_deg + 1.7*ph) + 0.4*sin(n3*theta_deg - 1.3*ph),
            mixed = (1-k)*base + k*mix1
        )
        shimmer_amp * mixed * (0.65 + 0.35*hz)
    );

function rim_z(theta_deg, z) =
    (rim_z_amp <= 0 || rim_z_waves <= 0) ? 0 :
    let(
        zf = z/height,
        w  = smoothstep(1 - rim_z_falloff_width, 1.0, zf),
        n  = max(rim_z_waves,1),
        ph = rim_z_phase_deg,
        k  = clamp(rim_z_irregular, 0, 1),
        base = sin(n*theta_deg + ph),
        mix1 = 0.6*sin((n+3)*theta_deg + 1.3*ph) + 0.4*sin(max(1,n-2)*theta_deg - 0.9*ph),
        mixed = (1-k)*base + k*mix1
    )
    rim_z_amp * mixed * w;

function r_outer(theta_deg, z) =
    let(
        zf = z/height,
        A_rim   = rim_amp       * band(zf, rim_band_center,   rim_band_width),
        A_outer = outer_rim_amp * band(zf, outer_band_center, outer_band_width),
        A_inner = inner_rim_amp * band(zf, inner_band_center, inner_band_width)
    )
    base_radius
    + flare(z)
    + wave(theta_deg, rim_waves,       A_rim,   rim_phase_deg)
    + wave(theta_deg, outer_rim_waves, A_outer, outer_rim_phase_deg)
    + wave(theta_deg, inner_rim_waves, A_inner, inner_rim_phase_deg)
    + shimmer(theta_deg, z);

function r_inner(theta_deg, z) =
    let(
        ri_wall = max(0.5, r_outer(theta_deg, z) - wall_thickness),
        t = clamp((z - bottom_thickness)/max(floor_blend_height, 0.001), 0, 1),
        w = t*t*(3-2*t),
        floor_r_safe = max(0.8, floor_radius)   // prevents collapse to a point
    )
    (1-w)*floor_r_safe + w*ri_wall;

function dish_depth() =
    max(0, min(inner_base_dish_depth, bottom_thickness - min_center_thickness));

///////////////////////
// MESH GENERATION (CLOSED)
///////////////////////
module wavy_bowl_closed(){
    nT = fn_theta;
    nZ = fn_z;

    function vid_outer(iT,iZ) = iZ*nT + iT;
    function vid_inner(iT,iZ) = (nZ+1)*nT + iZ*nT + iT;

    outer_count = (nZ+1)*nT;
    inner_count = (nZ+1)*nT;

    // Two “true” centers (underside and interior cap fallback)
    outer_center_idx = outer_count + inner_count; // [0,0,0]
    inner_center_idx = outer_center_idx + 1;      // [0,0,bottom_thickness]

    // Optional inner cap ring indices (added after the two centers)
    capN = max(3, cap_center_verts);
    capRing_start_idx = inner_center_idx + 1;     // first vertex of ring (if enabled)

    z_out_bottom = 0;
    z_in_bottom  = bottom_thickness;

    rin0  = r_inner(0, z_in_bottom);
    dishR = rin0 * clamp(inner_base_dish_radius_frac, 0.05, 1.0);
    dishD = dish_depth();

    // Cap ring radius must be <= the inner bottom ring radius
    floor_r_safe = max(0.8, floor_radius);
    capR = clamp(cap_center_radius, 0, floor_r_safe);

    points =
        concat(
            // OUTER surface vertices
            [ for (iZ=[0:nZ])
              for (iT=[0:nT-1])
                let(
                    z  = height*iZ/nZ,
                    th = 360*iT/nT,
                    ro = r_outer(th, z),
                    zz = z + rim_z(th, z)
                )
                [ ro*cos(th), ro*sin(th), zz ]
            ],

            // INNER surface vertices (dish is concave: subtract dish_z)
            [ for (iZ=[0:nZ])
              for (iT=[0:nT-1])
                let(
                    z_lin  = z_in_bottom + (height - z_in_bottom)*iZ/nZ,
                    th     = 360*iT/nT,
                    ri     = r_inner(th, z_lin),
                    f      = clamp(ri/max(dishR,0.01), 0, 1),
                    dish_z = (dishD <= 0) ? 0 : dishD * (1 - smoothstep(0.0, 1.0, f)),
                    zz     = (z_lin - dish_z) + rim_z(th, z_lin)
                )
                [ ri*cos(th), ri*sin(th), zz ]
            ],

            // Two center points
            [[0,0,z_out_bottom], [0,0,z_in_bottom]],

            // OPTIONAL: inner cap ring points at z=bottom_thickness (eliminates center fan artifact)
            (capR > 0 ? [ for(i=[0:capN-1])
                let(th = 360*i/capN)
                [ capR*cos(th), capR*sin(th), z_in_bottom ]
            ] : [])
        );

    // Helper: cap ring vertex id
    function vid_cap(i) = capRing_start_idx + i;

    faces =
        concat(
            // OUTER wall
            [ for (iZ=[0:nZ-1], iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_outer(iT,  iZ),
                    b=vid_outer(iT2, iZ),
                    c=vid_outer(iT2, iZ+1),
                    d=vid_outer(iT,  iZ+1))
                each [[a,b,c],[a,c,d]]
            ],

            // INNER wall (reverse winding)
            [ for (iZ=[0:nZ-1], iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_inner(iT,  iZ),
                    b=vid_inner(iT,  iZ+1),
                    c=vid_inner(iT2, iZ+1),
                    d=vid_inner(iT2, iZ))
                each [[a,b,c],[a,c,d]]
            ],

            // TOP bridge
            [ for (iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_outer(iT,  nZ),
                    b=vid_outer(iT2, nZ),
                    c=vid_inner(iT2, nZ),
                    d=vid_inner(iT,  nZ))
                each [[a,b,c],[a,c,d]]
            ],

            // BOTTOM thickness wall (outer z=0 ring to inner z=bottom_thickness ring)
            [ for (iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_outer(iT,  0),
                    b=vid_outer(iT2, 0),
                    c=vid_inner(iT2, 0),
                    d=vid_inner(iT,  0))
                each [[a,b,c],[a,c,d]]
            ],

            // OUTER underside disk (z=0)
            [ for (iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_outer(iT,  0),
                    b=vid_outer(iT2, 0),
                    c=outer_center_idx)
                [b,a,c]
            ],

            // INNER floor closure (z=bottom_thickness)
            // If capR==0 -> original center fan
            (capR <= 0 ?
                [ for (iT=[0:nT-1])
                    let(iT2=(iT+1)%nT,
                        a=vid_inner(iT,  0),
                        b=vid_inner(iT2, 0),
                        c=inner_center_idx)
                    [a,b,c]
                ]
            :
                concat(
                    // Annulus: connect inner bottom ring to cap ring
                    [ for (iT=[0:nT-1])
                        let(
                            iT2=(iT+1)%nT,
                            // map inner ring index iT to cap ring index proportionally
                            j  = floor(capN*iT/nT),
                            j2 = floor(capN*iT2/nT),
                            a=vid_inner(iT,  0),
                            b=vid_inner(iT2, 0),
                            c=vid_cap(j2),
                            d=vid_cap(j)
                        )
                        each [[a,b,c],[a,c,d]]
                    ],

                    // Cap ring to center (small fan, much less artifact)
                    [ for (j=[0:capN-1])
                        let(j2=(j+1)%capN,
                            a=vid_cap(j),
                            b=vid_cap(j2),
                            c=inner_center_idx)
                        [a,b,c]
                    ]
                )
            )
        );

    polyhedron(points=points, faces=faces, convexity=10);
}

wavy_bowl_closed();