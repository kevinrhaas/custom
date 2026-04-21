////////////////////////////////////////////////////////////
// Illinois Sandstone Cylinder – FAST polyhedron with LAYERS
////////////////////////////////////////////////////////////

height = 120;
radius = 40;

// Detail controls (start lower if you want it faster)
layers = 220;     // vertical sampling for mesh (not number of beds)
slices = 160;     // circumferential sampling

// Strata controls (this is what creates visible beds)
beds = 70;            // number of sandstone beds
bed_amp = 2.0;        // how “steppy” the bedding is (mm-ish)
bed_sharp = 0.22;     // smaller = crisper beds (0.18–0.35 good)
bed_warp = 0.55;      // waviness of bed boundaries (merge/split feel)

// Silhouette controls (overall not-round cylinder)
silhouette_amp = 5.2;   // big in/out
micro_amp      = 1.1;   // small in/out (keep modest)

// Secondary texture that does NOT destroy bedding
cross_amp = 0.35;       // subtle diagonal vibe

$fn = 64; // irrelevant for polyhedron, but kept harmless

// --- helpers ---
function clamp(x,a,b)= min(max(x,a),b);
function smoothstep(a,b,x)=
    let(t=clamp((x-a)/(b-a),0,1))
    t*t*(3-2*t);

// smooth periodic-ish “noise” (all sines, no jaggies)
function n1(x)= sin(x)*0.5 + sin(2.17*x+11)*0.3 + sin(3.73*x+3)*0.2;

// varying bed thickness by warping z->z'
function z_warp(z,t)= z + bed_warp * n1(z*0.09 + t*0.7);

// silhouette
function silhouette(t)=
    silhouette_amp*(0.62*sin(3*t)+0.38*sin(5*t+25));

function micro(t)=
    micro_amp*(0.55*sin(11*t+40)+0.45*sin(17*t));

// --- LAYERING CORE ---
// Map z into a bed index that varies with theta (merge/split vibe)
function bed_phase(z,t)=
    beds * ( z_warp(z,t) / height )
    + 0.65*sin(t*1.0 + z*0.03)     // makes boundaries drift around
    + 0.35*sin(t*2.0 - z*0.02);

// Create a “rounded step” per bed using fractional part
function frac(x)= x - floor(x);

// A smooth saw/step that creates ledges but avoids harsh overhangs
function bed_step(z,t)=
    let(p = bed_phase(z,t),
        f = frac(p)) // 0..1 inside bed
    // make each bed have a gentle “lip” near one side:
    // f near 0 = boundary. We create a small bulge that fades within bed.
    (1.0 - smoothstep(0.0, 0.55, f))   // high at boundary, fades by mid-bed
    - (1.0 - smoothstep(0.0, 0.55, 1.0-f))*0.35; // slight counter-shape

// subtle diagonal/cross texture that won’t erase horizontal beds
function cross_tex(z,t)= cross_amp * sin(z*0.22 + t*1.3);

// final radius
function R(z,t)=
    radius
    + silhouette(t)
    + micro(t)
    + bed_amp * bed_step(z,t)
    + cross_tex(z,t);

// Index helper
function idx(i,j)= i*slices + j;

module sandstone_poly() {
    pts =
        [ for (i=[0:layers])
            let(z = height*i/layers)
            for (j=[0:slices-1])
                let(t = 360*j/slices,
                    r = R(z,t))
                [ r*cos(t), r*sin(t), z ]
        ];

    side_faces =
        [ for (i=[0:layers-1])
            for (j=[0:slices-1])
                let(jn=(j+1)%slices,
                    a=idx(i,j), b=idx(i,jn),
                    c=idx(i+1,jn), d=idx(i+1,j))
                each [[a,b,c],[a,c,d]]
        ];

    bottom_center = len(pts);
    top_center    = len(pts) + 1;
    pts2 = concat(pts, [[0,0,0],[0,0,height]]);

    bottom_faces =
        [ for (j=[0:slices-1])
            let(jn=(j+1)%slices)
            [bottom_center, idx(0,jn), idx(0,j)]
        ];

    top_faces =
        [ for (j=[0:slices-1])
            let(jn=(j+1)%slices)
            [top_center, idx(layers,j), idx(layers,jn)]
        ];

    polyhedron(
        points=pts2,
        faces=concat(side_faces,bottom_faces,top_faces),
        convexity=10
    );
}

// Flat top (already flat by cap), but this shaves any numerical fuzz:
difference() {
    sandstone_poly();
    translate([-300,-300,height]) cube([600,600,20]);
}