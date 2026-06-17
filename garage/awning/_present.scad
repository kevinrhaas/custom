include <awning.scad>
// --- the cap profile ---
color([0.80,0.66,0.10]) projection(cut=true) translate([0,0,-5]) straight_raw(seg_len);
// --- reference: the WALL it slides over (top at y=0) ---
color([0.55,0.27,0.07,0.9]) translate([0,-14]) square([wall_thk,14]);
// --- reference: the 8mm LED strip seated in the cove, facing DOWN ---
led_ceiling = -oh_under + led_d;            // +1
color([0.1,0.6,0.2]) translate([xin+lip_t+1, led_ceiling-1.4]) square([8,1.4]);
