// ===========================================================================
// PLEXI CORNER CLIP — STYLE VARIATIONS of the chosen fit (clear +0.50)
// All 8 share the winning slot (t + 0.50 = 2.00 mm). They differ only in
// look / size: sharp vs rounded corner, smooth vs corrugated face, compact,
// tall grip, chamfered top. STL exports clean; render with -D show_num=true
// for a number map.  Same press-fit U-channel design.
// ===========================================================================

t = 1.5;
fit = 0.50;          // the chosen clearance (slot = t + fit = 2.00 mm)
show_num = true;     // -D show_num=false to export without numbers
$fn = 56;

// round  : outer vertical-corner radius (0 = sharp)
// corr   : corrugated outer faces (vertical ribs)
// tchamf : chamfer on the top edges (0 = flat slab)
module clip(arm=4, ht=4, wall=1, lip=0.9, toph=1, round=0, corr=false,
            tchamf=0, label="") {
  slot  = t + fit;
  cross = wall + slot + lip;
  difference() {
    union() {
      // slotted arms
      difference() {
        union() {
          translate([-wall,-wall,0]) cube([arm+wall, cross, ht]);
          translate([-wall,-wall,0]) cube([cross, arm+wall, ht]);
        }
        translate([0,0,-0.01]) cube([arm+1, slot, ht-toph+0.01]);
        translate([0,0,-0.01]) cube([slot, arm+1, ht-toph+0.01]);
      }
      // top: flat slab, or chamfered (frustum) top
      if (tchamf > 0)
        hull() {
          translate([-wall,-wall,ht-toph]) cube([arm+wall, arm+wall, 0.01]);
          translate([-wall+tchamf,-wall+tchamf,ht-0.01])
            cube([arm+wall-2*tchamf, arm+wall-2*tchamf, 0.01]);
        }
      else
        translate([-wall,-wall,ht-toph]) cube([arm+wall, arm+wall, toph]);
      // corrugated outer faces
      if (corr) {
        cr=0.45; p=1.1;
        for (x=[0.5:p:arm-0.2]) translate([x,-wall,0]) cylinder(r=cr,h=ht);
        for (y=[0.5:p:arm-0.2]) translate([-wall,y,0]) cylinder(r=cr,h=ht);
      }
    }
    // round the outer vertical corner
    if (round > 0)
      translate([-wall,-wall,-1]) linear_extrude(ht+2)
        difference() { square([round,round]); translate([round,round]) circle(r=round); }
    // number map (recessed) — off in the exported STL
    if (label != "" && show_num)
      translate([(arm-wall)/2, (arm-wall)/2, ht-0.4]) linear_extrude(0.6)
        text(label, size=2.2, halign="center", valign="center",
             font="Liberation Sans:style=Bold");
  }
}

cx = 10; ry = 13;
// Row 1
translate([0*cx,0])  clip(label="1");                          // baseline (the winner)
translate([1*cx,0])  clip(round=1.2, label="2");               // rounded corner
translate([2*cx,0])  clip(corr=true, label="3");               // corrugated face
translate([3*cx,0])  clip(round=1.0, corr=true, label="4");    // rounded + corrugated
// Row 2
translate([0*cx,ry]) clip(arm=3.2, ht=3.5, label="5");                 // compact
translate([1*cx,ry]) clip(arm=3.2, ht=3.5, round=1.0, label="6");      // compact + rounded
translate([2*cx,ry]) clip(ht=5.5, label="7");                          // tall grip
translate([3*cx,ry]) clip(tchamf=0.8, label="8");                      // chamfered top
