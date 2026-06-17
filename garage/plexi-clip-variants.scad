// ===========================================================================
// PLEXI CORNER CLIP — VARIANT TEST PLATE
// 10 versions of the 1.5 mm-panel outside-corner clip on one STL so you can
// print once and pick the winner. Each is numbered (recessed on the top cap);
// see the legend in chat for what each number is. Same press-fit U-channel
// idea as the awning. Units = mm.  Outside corner at each clip's local origin.
// ===========================================================================

t = 1.5;        // plexi panel thickness (all variants)
show_num = true;   // recess the ID number on each top cap (-D show_num=false to hide)
$fn = 48;
function lbl(n) = show_num ? n : "";

// --- one clip ---------------------------------------------------------------
// clear : slot clearance (+ looser / - tighter)
// arm   : run along each panel ; ht: height ; wall/lip/toph: shell/lip/top
// round : outer vertical-corner radius (0 = sharp)
// corr  : true = corrugated outer faces (vertical half-round ribs)
// label : number recessed into the top cap
module clip(clear=0, arm=4, ht=4, wall=1, lip=0.9, toph=1,
            round=0, corr=false, label="") {
  slot  = t + clear;
  cross = wall + slot + lip;          // full width of each arm
  difference() {
    union() {
      // slotted arms: solid bars with the 1.5 mm panel slot cut in
      difference() {
        union() {
          translate([-wall,-wall,0]) cube([arm+wall, cross, ht]);
          translate([-wall,-wall,0]) cube([cross, arm+wall, ht]);
        }
        translate([0,0,-0.01]) cube([arm+1, slot, ht-toph+0.01]);   // slot A
        translate([0,0,-0.01]) cube([slot, arm+1, ht-toph+0.01]);   // slot B
      }
      // square top slab: caps panel tops + ties it together
      translate([-wall,-wall,ht-toph]) cube([arm+wall, arm+wall, toph]);
      // corrugated outer faces (vertical ribs along each arm)
      if (corr) {
        cr = 0.45; p = 1.1;
        for (x=[0.5 : p : arm-0.2]) translate([x,-wall,0]) cylinder(r=cr,h=ht);
        for (y=[0.5 : p : arm-0.2]) translate([-wall,y,0]) cylinder(r=cr,h=ht);
      }
    }
    // round the outer vertical corner
    if (round > 0)
      translate([-wall,-wall,-1]) linear_extrude(ht+2)
        difference() { square([round,round]); translate([round,round]) circle(r=round); }
    // recessed number on the top cap
    if (label != "")
      translate([(arm-wall)/2, (arm-wall)/2, ht-0.4]) linear_extrude(0.6)
        text(label, size=2.3, halign="center", valign="center",
             font="Liberation Sans:style=Bold");
  }
}

// --- 10 variants on a 5x2 grid ---------------------------------------------
cx = 10;   // column pitch
ry = 13;   // row pitch

// Row 1 — clearance ladder (same size) + tall
translate([0*cx, 0]) clip(clear=-0.10, label=lbl("1"));                 // tight
translate([1*cx, 0]) clip(clear= 0.00, label=lbl("2"));                 // snug
translate([2*cx, 0]) clip(clear= 0.10, label=lbl("3"));                 // nominal
translate([3*cx, 0]) clip(clear= 0.20, label=lbl("4"));                 // loose
translate([4*cx, 0]) clip(clear= 0.10, ht=5.5, label=lbl("5"));         // tall grip

// Row 2 — sizes + styled faces
translate([0*cx, ry]) clip(clear=0.10, arm=3.2, ht=3.5, label=lbl("6"));            // small
translate([1*cx, ry]) clip(clear=0.10, arm=2.6, ht=3.0, lip=0.8, label=lbl("7"));   // smallest
translate([2*cx, ry]) clip(clear=0.10, round=1.2, label=lbl("8"));                  // rounded corner
translate([3*cx, ry]) clip(clear=0.10, corr=true, label=lbl("9"));                  // corrugated
translate([4*cx, ry]) clip(clear=0.10, round=1.0, corr=true, label=lbl("10"));      // rounded + corrugated
