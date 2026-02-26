//
// Wavy-Layer Bowl (parametric) — CLOSED MANIFOLD VERSION
// OpenSCAD trig is DEGREES.
//

// NEW: floor control (guarantees a real bottom)
// floor_radius=0 makes it close to a point; larger makes a flatter bigger floor.
floor_radius      = 0;     // mm (try 8–18)
floor_blend_height= 6;      // mm (how quickly the inner wall blends into the floor)


///////////////////////
// MAIN PARAMETERS
///////////////////////
base_radius      = 35;     // mm  (radius at bottom outside)
height           = 40;     // mm  (overall bowl height)
pitch_deg        = 40;     // degrees (side flare)
wall_thickness   = 2.2;    // mm

// Solid bottom thickness (actual bowl floor thickness)
bottom_thickness = 2.0;    // mm (1.6–3.0 typical)

// Radial scallops (around circumference)
rim_waves        = 16;     // top rim radial scallops count
outer_rim_waves  = 12;     // middle band radial scallops count
inner_rim_waves  = 8;      // lower band radial scallops count

// Radial amplitudes (mm)
rim_amp          = 2.0;
outer_rim_amp    = 2.0;
inner_rim_amp    = 2.0;

// Band placement (fractions of height)
rim_band_center   = 0.95;  rim_band_width   = 0.50;
outer_band_center = 0.55;  outer_band_width = 0.50;
inner_band_center = 0.25;  inner_band_width = 0.50;

// Phases (degrees)
rim_phase_deg        = 0;
outer_rim_phase_deg  = 360/(max(outer_rim_waves,1)*2);
inner_rim_phase_deg  = 360/(max(inner_rim_waves,1)*3);

// NEW: top rim HEIGHT waviness (vertical ruffle)
rim_z_waves         = 10;    // bumps around rim
rim_z_amp           = 3.0;   // mm vertical variation
rim_z_irregular     = 0.45;  // 0..1 (more organic)
rim_z_phase_deg     = 0;     // degrees
rim_z_falloff_width = 0.18;  // fraction of height where it fades in near top

// Interior base dish (optional)
inner_base_dish_depth = 1.5;      // mm (0=flat)
inner_base_dish_radius_frac = 0.75;

// Outside shimmer (micro radial irregularity)
shimmer_amp       = 0.0;   // mm (0 = smooth)
shimmer_waves     = 35;
shimmer_z_waves   = 3;
shimmer_irregular = 0.55;  // 0..1
shimmer_phase_deg = 17;

// Mesh resolution
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

// vertical ruffle applied near the very top
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
        // regular inner wall radius based on outside - thickness
        ri_wall = max(0.5, r_outer(theta_deg, z) - wall_thickness),

        // blend factor: 0 at bottom_thickness, ->1 by bottom_thickness+floor_blend_height
        t = clamp((z - bottom_thickness)/max(floor_blend_height, 0.001), 0, 1),

        // smooth blend so it doesn't kink
        w = t*t*(3-2*t)
    )
    // at the very bottom, force inner radius to floor_radius, then blend to wall
    (1-w)*max(0.0, floor_radius) + w*ri_wall;

function inner_dish(z) =
    (inner_base_dish_depth <= 0 ? 0 :
        inner_base_dish_depth * (1 - smoothstep(0.0, 0.18, z/height)));

///////////////////////
// MESH GENERATION (CLOSED)
///////////////////////
module wavy_bowl_closed(){
    nT = fn_theta;
    nZ = fn_z;

    function vid_outer(iT,iZ) = iZ*nT + iT;
    function vid_inner(iT,iZ) = (nZ+1)*nT + iZ*nT + iT;

    // counts
    outer_count = (nZ+1)*nT;
    inner_count = (nZ+1)*nT;

    // center vertices indices (added at the end)
    outer_center_idx = outer_count + inner_count;       // z=0 underside center
    inner_center_idx = outer_center_idx + 1;            // z=bottom_thickness inner floor center

    z_out_bottom = 0;
    z_in_bottom  = bottom_thickness;

    // dish shaping reference
    rin0  = r_inner(0, z_in_bottom);
    dishR = rin0 * inner_base_dish_radius_frac;

    // points
    points =
        concat(
            // OUTER surface vertices (z=0..height)
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

            // INNER surface vertices (z=bottom_thickness..height)
            [ for (iZ=[0:nZ])
              for (iT=[0:nT-1])
                let(
                    z_lin = z_in_bottom + (height - z_in_bottom)*iZ/nZ,
                    th    = 360*iT/nT,
                    ri    = r_inner(th, z_lin),
                    dish  = inner_dish(z_lin),
                    f     = clamp(ri/(max(dishR,0.01)), 0, 1),
                    dish_z= dish * smoothstep(1.0, 0.0, f),
                    zz = (iZ==0) ? z_in_bottom : (z_lin + dish_z + rim_z(th, z_lin))
                )
                [ ri*cos(th), ri*sin(th), zz ]
            ],

            // two center points for bottom closures
            [[0,0,z_out_bottom], [0,0,z_in_bottom]]
        );

    faces =
        concat(
            // OUTER side wall
            [ for (iZ=[0:nZ-1], iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_outer(iT,  iZ),
                    b=vid_outer(iT2, iZ),
                    c=vid_outer(iT2, iZ+1),
                    d=vid_outer(iT,  iZ+1))
                each [[a,b,c],[a,c,d]]
            ],

            // INNER side wall (reverse winding)
            [ for (iZ=[0:nZ-1], iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_inner(iT,  iZ),
                    b=vid_inner(iT,  iZ+1),
                    c=vid_inner(iT2, iZ+1),
                    d=vid_inner(iT2, iZ))
                each [[a,b,c],[a,c,d]]
            ],

            // TOP rim bridge (outer top ring to inner top ring)
            [ for (iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_outer(iT,  nZ),
                    b=vid_outer(iT2, nZ),
                    c=vid_inner(iT2, nZ),
                    d=vid_inner(iT,  nZ))
                each [[a,b,c],[a,c,d]]
            ],

            // BOTTOM THICKNESS WALL: connect outer bottom ring (z=0) to inner bottom ring (z=bottom_thickness)
            [ for (iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_outer(iT,  0),
                    b=vid_outer(iT2, 0),
                    c=vid_inner(iT2, 0),
                    d=vid_inner(iT,  0))
                each [[a,b,c],[a,c,d]]
            ],

// OUTER UNDERSIDE DISK (cap bottom outside at z=0)
[ for (iT=[0:nT-1])
    let(iT2=(iT+1)%nT,
        a=vid_outer(iT,  0),
        b=vid_outer(iT2, 0),
        c=outer_center_idx)
    [b,a,c]
],

// INNER FLOOR DISK (cap interior at z=bottom_thickness)
[ for (iT=[0:nT-1])
    let(iT2=(iT+1)%nT,
        a=vid_inner(iT,  0),
        b=vid_inner(iT2, 0),
        c=inner_center_idx)
    [a,b,c]
]
        );

    polyhedron(points=points, faces=faces, convexity=10);
}

wavy_bowl_closed();