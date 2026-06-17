include <awning.scad>
// flip the cross-section in X so the overhang faces the INSIDE of the corner
module legA2() intersection() { mirror([1,0,0]) straight_raw(corner_leg,0); keep_ZX(); }
legA2();
translate([miter_nudge,0,miter_nudge]) mirror([1,0,-1]) legA2();
