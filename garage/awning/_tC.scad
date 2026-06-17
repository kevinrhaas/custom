include <awning.scad>
mirror([1,0,-1]) intersection(){ straight_raw(corner_leg,0); keep_ZX(); }
