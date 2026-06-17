include <awning.scad>
color([0.80,0.66,0.10]) projection(cut=true) translate([0,0,-5]) straight_raw(40, 0);
color([0.55,0.27,0.07,0.9]) translate([0,-20]) square([wall_thk,20]);
led_ceiling = -oh_under + led_d;
color([0.1,0.6,0.2]) translate([xin+lip_t+1, led_ceiling-1.4]) square([8,1.4]);
