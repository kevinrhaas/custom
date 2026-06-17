include <awning.scad>
rotate([-90,0,0]) {
  color([0.62,0.30,0.10]) {
    translate([0,-30,0]) cube([wall_thk, 30, 300]);
    translate([0,0,100]) cube([wall_thk, cap_h, 100]);
  }
  color([0.86,0.71,0.13]) {
    translate([0,0,0])   straight_raw(100, 0);
    translate([0,0,100]) straight_raw(100, cap_h);
    translate([0,0,200]) straight_raw(100, 0);
  }
}
