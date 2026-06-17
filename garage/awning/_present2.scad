include <awning.scad>
// center-piece profile (rest_y = cap_h) at the steeper pitch
color([0.80,0.66,0.10]) projection(cut=true) translate([0,0,-5]) straight_raw(center_len, cap_h);
// wall + raised cap seated in the slot
color([0.55,0.27,0.07,0.95]) translate([0,-15]) square([wall_thk,25]);   // body+cap up to +10
// 8mm LED strip in the front cove
led_ceiling = -oh_under + led_d;
color([0.1,0.6,0.2]) translate([xin+lip_t+1, led_ceiling-1.4]) square([8,1.4]);
