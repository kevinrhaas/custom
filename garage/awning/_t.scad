include <awning.scad>
module leg() intersection(){ straight_raw(corner_leg,0); keep_ZX(); }
union(){ leg(); translate([1.0,0,1.0]) mirror([1,0,-1]) leg(); }
