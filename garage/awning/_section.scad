include <awning.scad>
wh = 18; vy = 4;   // vy = vertical exaggeration for readability
rt = roof_front_y + (5 - xin)*tan(pitch_deg);
scale([1,vy,1]) {
  color([0.62,0.30,0.10]) polygon([
    [0,-wh],[0,0],[100,0],[100,cap_h],[200,cap_h],[200,0],[300,0],[300,-wh] ]);
  color([0.85,0.70,0.12,0.85]) polygon([
    [0,0],[100,0],[100,cap_h],[200,cap_h],[200,0],[300,0],[300,rt],[0,rt] ]);
}
// labels (drawn at true scale, positioned in the exaggerated frame)
color("black") {
  translate([110,cap_h*vy+6])   text("10mm cap, hidden under straight roofline", size=7);
  translate([20,-wh*vy-14])     text("main 100", size=8);
  translate([120,-wh*vy-14])    text("cap 100",  size=8);
  translate([225,-wh*vy-14])    text("main 100", size=8);
  translate([2, rt*vy+4])       text("straight, level roofline ->", size=7);
}
