include <awning.scad>
difference() {
  mirror([1,0,-1]) intersection() {
    mirror([1,0,0]) translate([0,0,-corner_back]) straight_raw(corner_leg+corner_back,0);
    keep_ZX();
  }
  if (wire_hole) wire_tunnel();
}
