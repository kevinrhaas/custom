//
// Wavy-Layer Bowl (parametric) — OpenSCAD (DEGREE-CORRECT)
// OpenSCAD sin/cos use DEGREES. This version is consistent.
//

///////////////////////
// MAIN PARAMETERS
///////////////////////
base_radius      = 35;     // mm  (radius at bottom outside)
height           = 40;     // mm  (overall bowl height)
pitch_deg        = 40;     // degrees (side flare: bigger = wider faster)
wall_thickness   = 2.2;    // mm

// Wave counts (scallops around circumference)
rim_waves        = 16;      // top rim scallops
outer_rim_waves  = 12;      // middle band scallops
inner_rim_waves  = 8;      // lower band scallops

// Wave amplitudes
rim_amp          = 2.0;    // mm
outer_rim_amp    = 2;    // mm
inner_rim_amp    = 2.0;    // mm

// Band placement (fractions of height)
rim_band_center   = 0.95;  rim_band_width   = 0.5;
outer_band_center = 0.55;  outer_band_width = 0.5;
inner_band_center = 0.25;  inner_band_width = 0.5;

// Phase offsets (degrees) to keep bands from aligning perfectly
rim_phase_deg        = 0;
outer_rim_phase_deg  = 360/(max(outer_rim_waves,1)*2);
inner_rim_phase_deg  = 360/(max(inner_rim_waves,1)*3);

// Interior base: smooth + optional shallow dish
inner_base_dish_depth = 1.5;      // mm (0 = flat)
inner_base_dish_radius_frac = 0.75;

// Outside shimmer (micro irregularity). 0 = smooth
shimmer_amp       = 0.0;   // mm (try 0.4 to 1.2)
shimmer_waves     = 35;    // around circumference
shimmer_z_waves   = 3;     // along height
shimmer_irregular = 0.55;  // 0..1
shimmer_phase_deg = 17;    // degrees

// Mesh resolution
fn_theta = 220;  // around
fn_z     = 90;   // vertical

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

function flare(z) = z * tan(pitch_deg); // tan() expects degrees in OpenSCAD

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
    max(0.5, r_outer(theta_deg, z) - wall_thickness);

function inner_dish(z) =
    (inner_base_dish_depth <= 0 ? 0 :
        inner_base_dish_depth * (1 - smoothstep(0.0, 0.18, z/height)));

///////////////////////
// MESH GENERATION
///////////////////////
module wavy_bowl(){
    nT = fn_theta;
    nZ = fn_z;

    function vid_outer(iT,iZ) = iZ*nT + iT;
    function vid_inner(iT,iZ) = (nZ+1)*nT + iZ*nT + iT;

    rin0  = r_inner(0, 0);
    dishR = rin0 * inner_base_dish_radius_frac;

    vertices =
        concat(
            // OUTER vertices
            [ for (iZ=[0:nZ])
              for (iT=[0:nT-1])
                let(
                    z = height*iZ/nZ,
                    th = 360*iT/nT,
                    ro = r_outer(th, z)
                )
                [ ro*cos(th), ro*sin(th), z ]
            ],
            // INNER vertices (smooth wall, optional dish near bottom)
            [ for (iZ=[0:nZ])
              for (iT=[0:nT-1])
                let(
                    z = height*iZ/nZ,
                    th = 360*iT/nT,
                    ri = r_inner(th, z),
                    dish = inner_dish(z),
                    f = clamp(ri/(max(dishR,0.01)), 0, 1),
                    dish_z = dish * smoothstep(1.0, 0.0, f)
                )
                [ ri*cos(th), ri*sin(th), z + dish_z ]
            ]
        );

    faces =
        concat(
            // OUTER surface
            [ for (iZ=[0:nZ-1], iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_outer(iT,  iZ),
                    b=vid_outer(iT2, iZ),
                    c=vid_outer(iT2, iZ+1),
                    d=vid_outer(iT,  iZ+1))
                each [[a,b,c],[a,c,d]]
            ],

            // INNER surface (reverse winding)
            [ for (iZ=[0:nZ-1], iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_inner(iT,  iZ),
                    b=vid_inner(iT,  iZ+1),
                    c=vid_inner(iT2, iZ+1),
                    d=vid_inner(iT2, iZ))
                each [[a,b,c],[a,c,d]]
            ],

            // TOP rim connection
            [ for (iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_outer(iT,  nZ),
                    b=vid_outer(iT2, nZ),
                    c=vid_inner(iT2, nZ),
                    d=vid_inner(iT,  nZ))
                each [[a,b,c],[a,c,d]]
            ],

            // BOTTOM cap ring
            [ for (iT=[0:nT-1])
                let(iT2=(iT+1)%nT,
                    a=vid_outer(iT,  0),
                    b=vid_inner(iT,  0),
                    c=vid_inner(iT2, 0),
                    d=vid_outer(iT2, 0))
                each [[a,b,c],[a,c,d]]
            ]
        );

    polyhedron(points=vertices, faces=faces, convexity=10);
}

wavy_bowl();