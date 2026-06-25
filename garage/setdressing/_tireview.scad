// Tire close-up: single tire + a stack of 4 next to it.
use <wallrows.scad>
$fn = 96;
tire2();
translate([14, 0, 0]) for (i=[0:3]) translate([0,0,i*3.2]) rotate([0,0,i*22]) tire2();
