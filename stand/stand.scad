// Parametric three-rail adjustable display stand
// Units: millimetres
//
// Open in OpenSCAD and select a value for `part`, or use build.py to render
// every print-ready STL. The same rail is printed three times.

/* [Output] */
part = "assembly"; // [assembly,rail,axle,cap,spacer,stop_pin,fit_test,rails_plate,hardware_plate]
show_object_envelope = true;

/* [Object envelope] */
object_length = 150;
object_width = 120;
object_height = 70;

/* [Rail geometry] */
rail_length = 180;
rail_thickness = 18;       // depth in the rail's working plane
rail_width = 26;           // width along the common axle
pivot_boss_d = 22;
end_round_d = 18;

/* [Angle adjustment] */
stop_hole_start = 16;      // first hole centre from the axle
stop_hole_pitch = 10;
stop_hole_count = 6;
stop_pin_d = 8;
stop_pin_hole_clearance = 0.50; // diametral
stop_pin_reach = 10;       // engagement into the neighbouring rail lane
stop_pin_head_d = 15;
stop_pin_head_h = 4;

/* [Axle and spacing] */
axle_d = 12;
pivot_hole_clearance = 0.60; // diametral
spacer_thickness = 4;
spacer_d = 20;
axial_play = 0.60;
axle_head_d = 22;
axle_head_h = 4;
axle_tip_d = 10;
axle_tip_length = 5;
cap_d = 22;
cap_h = 7.5;
cap_floor = 2;
cap_fit_clearance = 0.35;   // diametral; tune after printing fit_test
cap_relief_slot = 1.2;

/* [Preview] */
assembly_angle = 54;        // relative angle between centre and outer rails
assembly_stop_index = 0;    // 0 is the closest/steepest stop position

/* [Quality] */
$fn = 96;
eps = 0.02;
entry_chamfer = 0.5;

pivot_hole_d = axle_d + pivot_hole_clearance;
stop_pin_hole_d = stop_pin_d + stop_pin_hole_clearance;
stop_offsets = [for (i = [0 : stop_hole_count - 1])
    stop_hole_start + i * stop_hole_pitch];
axle_bearing_length = 3 * rail_width + 4 * spacer_thickness + axial_play;
stop_pin_shaft_length = rail_width + spacer_thickness + stop_pin_reach;

assert(stop_hole_start > pivot_boss_d / 2 + stop_pin_d / 2,
    "First stop pin must clear the neighbouring pivot boss");
assert(stop_hole_start > pivot_hole_d / 2 + stop_pin_hole_d / 2 + 2,
    "Not enough material between pivot and first stop hole");
assert(stop_offsets[len(stop_offsets) - 1] + stop_pin_hole_d / 2
       < rail_length / 2 - end_round_d / 4,
    "Last stop hole is too close to a rail end");
assert(cap_floor < cap_h && axle_tip_length <= cap_h - cap_floor + 0.5,
    "Cap socket is too shallow for the axle tip");

module capsule_2d(length, diameter) {
    hull() {
        translate([-(length - diameter) / 2, 0]) circle(d = diameter);
        translate([ (length - diameter) / 2, 0]) circle(d = diameter);
    }
}

module chamfered_bore(d, height) {
    translate([0, 0, -eps]) cylinder(d = d, h = height + 2 * eps);
    translate([0, 0, -eps])
        cylinder(d1 = d + 2 * entry_chamfer, d2 = d,
                 h = entry_chamfer + eps);
    translate([0, 0, height - entry_chamfer])
        cylinder(d1 = d, d2 = d + 2 * entry_chamfer,
                 h = entry_chamfer + eps);
}

module rail() {
    difference() {
        linear_extrude(height = rail_width)
            union() {
                capsule_2d(rail_length, end_round_d);
                circle(d = pivot_boss_d);
            }

        chamfered_bore(pivot_hole_d, rail_width);

        for (side = [-1, 1], offset = stop_offsets)
            translate([side * offset, 0, 0])
                chamfered_bore(stop_pin_hole_d, rail_width);
    }
}

module axle() {
    union() {
        // Broad first-layer foot doubles as the permanent retaining head.
        cylinder(d1 = axle_head_d - 1, d2 = axle_head_d,
                 h = entry_chamfer);
        translate([0, 0, entry_chamfer])
            cylinder(d = axle_head_d, h = axle_head_h - entry_chamfer);

        translate([0, 0, axle_head_h - eps])
            cylinder(d = axle_d, h = axle_bearing_length + 2 * eps);

        translate([0, 0, axle_head_h + axle_bearing_length])
            cylinder(d = axle_tip_d,
                     h = axle_tip_length - entry_chamfer);
        translate([0, 0,
                   axle_head_h + axle_bearing_length
                   + axle_tip_length - entry_chamfer])
            cylinder(d1 = axle_tip_d, d2 = axle_tip_d - 1,
                     h = entry_chamfer);
    }
}

module cap() {
    difference() {
        union() {
            cylinder(d1 = cap_d - 1, d2 = cap_d, h = entry_chamfer);
            translate([0, 0, entry_chamfer])
                cylinder(d = cap_d, h = cap_h - entry_chamfer);
        }

        // Blind, slightly compliant push-fit socket.
        translate([0, 0, cap_floor])
            cylinder(d = axle_tip_d + cap_fit_clearance,
                     h = cap_h - cap_floor + eps);

        // A single split lets the socket flex and remain removable.
        translate([0, -cap_relief_slot / 2, cap_floor])
            cube([cap_d / 2 + eps, cap_relief_slot,
                  cap_h - cap_floor + eps]);
    }
}

module spacer() {
    difference() {
        cylinder(d = spacer_d, h = spacer_thickness);
        translate([0, 0, -eps])
            cylinder(d = pivot_hole_d, h = spacer_thickness + 2 * eps);
    }
}

module stop_pin() {
    union() {
        cylinder(d1 = stop_pin_head_d - 1, d2 = stop_pin_head_d,
                 h = entry_chamfer);
        translate([0, 0, entry_chamfer])
            cylinder(d = stop_pin_head_d,
                     h = stop_pin_head_h - entry_chamfer);
        translate([0, 0, stop_pin_head_h - eps])
            cylinder(d = stop_pin_d,
                     h = stop_pin_shaft_length - 1.5 + eps);
        translate([0, 0,
                   stop_pin_head_h + stop_pin_shaft_length - 1.5])
            cylinder(d1 = stop_pin_d, d2 = stop_pin_d - 1.2, h = 1.5);
    }
}

module fit_test() {
    // One small plate tests both functional clearances before the full print.
    difference() {
        translate([-20, -10, 0]) cube([40, 20, 7]);
        translate([-10, 0, -eps])
            cylinder(d = pivot_hole_d, h = 7 + 2 * eps);
        translate([10, 0, -eps])
            cylinder(d = stop_pin_hole_d, h = 7 + 2 * eps);
    }

    translate([-10, 17, 0]) cylinder(d = axle_d, h = 10);
    translate([ 10, 17, 0]) cylinder(d = stop_pin_d, h = 10);
    translate([ 27, 17, 0]) cylinder(d = axle_tip_d, h = 8);
    translate([ 27, -25, 0]) cap();
}

module rails_plate() {
    for (y = [-28, 0, 28]) translate([0, y, 0]) rail();
}

module hardware_plate() {
    translate([-48, 0, 0]) axle();
    for (x = [-20, 0, 20, 40]) translate([x, 0, 0]) stop_pin();
    translate([-22, 28, 0]) cap();
    for (x = [0, 23, 46]) translate([x, 28, 0]) spacer();
    translate([11.5, 51, 0]) spacer();
}

module placed_pin(x_offset, rail_angle, z_base, reverse = false) {
    translate([0, 0, z_base])
        rotate([0, 0, rail_angle])
            translate([x_offset, 0, 0])
                if (reverse)
                    mirror([0, 0, 1]) stop_pin();
                else
                    stop_pin();
}

module assembly_horizontal_axis() {
    half_angle = assembly_angle / 2;
    selected_offset = stop_offsets[assembly_stop_index];

    // Stack from the permanent axle head toward the removable cap.
    translate([0, 0, -axle_head_h]) color("silver") axle();

    translate([0, 0, 0]) color("lightgray") spacer();
    translate([0, 0, spacer_thickness])
        rotate([0, 0, half_angle]) color("cornflowerblue") rail();

    translate([0, 0, spacer_thickness + rail_width])
        color("lightgray") spacer();
    translate([0, 0, 2 * spacer_thickness + rail_width])
        rotate([0, 0, -half_angle]) color("gainsboro") rail();

    translate([0, 0, 2 * spacer_thickness + 2 * rail_width])
        color("lightgray") spacer();
    translate([0, 0, 3 * spacer_thickness + 2 * rail_width])
        rotate([0, 0, half_angle]) color("cornflowerblue") rail();

    translate([0, 0, 3 * spacer_thickness + 3 * rail_width])
        color("lightgray") spacer();

    translate([0, 0, axle_bearing_length + cap_h])
        mirror([0, 0, 1]) color("silver") cap();

    // Two opposing pins per interface bracket the angle in both directions.
    for (x_offset = [-selected_offset, selected_offset]) {
        placed_pin(x_offset, half_angle, 0, false);
        placed_pin(x_offset, half_angle,
                   4 * spacer_thickness + 3 * rail_width, true);
    }
}

module assembly() {
    half_angle = assembly_angle / 2;
    // Exact vertical extent of the rounded rail end at this angle.
    lift = (rail_length - end_round_d) / 2 * sin(half_angle)
         + end_round_d / 2;

    // Rotate the CAD stack so the axle is horizontal and the rail ends stand.
    translate([0, 0, lift]) rotate([90, 0, 0])
        assembly_horizontal_axis();

    if (show_object_envelope)
        color([0.35, 0.22, 0.12, 0.35])
            translate([0, -axle_bearing_length / 2,
                       lift + object_height * 0.58])
                scale([object_length / 2,
                       object_width / 2,
                       object_height / 2]) sphere(r = 1, $fn = 64);
}

if (part == "assembly") assembly();
else if (part == "rail") rail();
else if (part == "axle") axle();
else if (part == "cap") cap();
else if (part == "spacer") spacer();
else if (part == "stop_pin") stop_pin();
else if (part == "fit_test") fit_test();
else if (part == "rails_plate") rails_plate();
else if (part == "hardware_plate") hardware_plate();
else assert(false, str("Unknown part: ", part));
