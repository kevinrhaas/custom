// top-view plan of the L (schematic, mm). y is "down the page".
W = 26;                 // awning footprint width (schematic)
capcol = [0.80,0.45,0.10];
wallcol= [0.62,0.62,0.66];
// Wall A: horizontal, plexi(front) at left x=0, corner at right x=290
translate([0,0]) {
  color(wallcol) square([290,W]);
  color(capcol)  translate([100,0]) square([100,W]);   // cap 100-200 from front
}
// Wall B: vertical, corner at top, plexi(front) at bottom; offset so corner overlaps
translate([290-W,W]) {
  color(wallcol) square([W,300]);
  color(capcol)  translate([0,100]) square([W,100]);    // cap 100-200 from front(corner side)
}
// corner marker
color([0.85,0.1,0.1]) translate([290-W,W]) square([W,W]);
// labels
color("black") {
  translate([20,W+8])   text("PLEXI end",size=9);
  translate([120,W+8])  text("CAP",size=9);
  translate([225,W+8])  text("90->corner",size=8);
  translate([300,8])    text("<- CORNER (cord out back)",size=8);
  translate([300,150])  text("Wall B 100/100/100",size=9);
  translate([300,295])  text("PLEXI end",size=9);
  translate([60,-14])   text("Wall A  290 = 100 + 100(cap) + 90",size=9);
}
