include <awning.scad>
wall_h = 35;
// --- the stepped wall (main coping + raised center cap) ---
color([0.62,0.30,0.10]) {
  translate([0,-wall_h,0]) cube([wall_thk, wall_h, 300]);       // wall body
  translate([0,0,cap_w_pos()]) cube([wall_thk, cap_h, cap_w]);  // raised cap
}
function cap_w_pos() = (300-cap_w)/2;   // 100
// --- the awning: main | center | main ---
color([0.85,0.70,0.12,0.92]) {
  translate([0,0,0])   straight_raw(100, 0);
  translate([0,0,100]) straight_raw(cap_w, cap_h);
  translate([0,0,200]) straight_raw(100, 0);
}
