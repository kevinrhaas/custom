include <awning.scad>
projection(cut=true) rotate([0,90,0]) translate([-5.5,0,0])
  difference() {
    mirror([1,0,-1]) intersection() {
      mirror([1,0,0]) translate([0,0,-corner_back]) straight_raw(corner_leg+corner_back,0);
      keep_ZX();
    }
    wire_tunnel();
  }
