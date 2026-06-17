include <awning.scad>
wh = 16; vy = 4; L=290;
rt = roof_front_y + (5 - xin)*tan(pitch_deg);
scale([1,vy,1]) {
  // wall: 0-100 coping, 100-200 raised cap, 200-290 coping
  color([0.62,0.30,0.10]) polygon([[0,-wh],[0,0],[100,0],[100,cap_h],[200,cap_h],[200,0],[L,0],[L,-wh]]);
  // awning section: bottom bears on wall/cap, top straight roofline
  color([0.85,0.70,0.12,0.85]) polygon([[0,0],[100,0],[100,cap_h],[200,cap_h],[200,0],[L,0],[L,rt],[0,rt]]);
}
// joint markers at the cap steps (z=100, 200)
color("red") { translate([100,-wh*vy]) square([0.6,(rt+wh)*vy]); translate([200,-wh*vy]) square([0.6,(rt+wh)*vy]); }
color("black") {
  translate([30,rt*vy+5]) text("corner leg 100",size=8);
  translate([128,rt*vy+5]) text("center 100",size=8);
  translate([228,rt*vy+5]) text("main 90",size=8);
  translate([60,-wh*vy-14]) text("joints (red) hide on the cap steps",size=7);
}
