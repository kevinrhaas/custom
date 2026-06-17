// ===========================================================================
// PLEXI CORNER CLIP — variations of the PLAIN BASELINE (#1, the winner)
// Keeps #1's look exactly: sharp corner, smooth faces, slot = t + 0.50 = 2.00mm.
// This set varies only the practical dimensions so you can pick the proportions
// you like: HEIGHT (grip up the panel), ARM (footprint along each panel), and
// WALL/LIP (sturdiness vs. daintiness). STL exports clean; render with
// -D show_num=true for a number map.
// ===========================================================================

t = 1.5;
fit = 0.25;          // chosen clearance (slot = 1.75 mm)
show_num = true;     // -D show_num=false to export without numbers
$fn = 48;

module clip(arm=4, ht=4, wall=1, lip=0.9, toph=1, label="") {
  slot  = t + fit;
  cross = wall + slot + lip;
  difference() {
    union() {
      difference() {
        union() {
          translate([-wall,-wall,0]) cube([arm+wall, cross, ht]);
          translate([-wall,-wall,0]) cube([cross, arm+wall, ht]);
        }
        translate([0,0,-0.01]) cube([arm+1, slot, ht-toph+0.01]);
        translate([0,0,-0.01]) cube([slot, arm+1, ht-toph+0.01]);
      }
      translate([-wall,-wall,ht-toph]) cube([arm+wall, arm+wall, toph]);
    }
    if (label != "" && show_num)
      translate([(arm-wall)/2, (arm-wall)/2, ht-0.4]) linear_extrude(0.6)
        text(label, size=2.2, halign="center", valign="center",
             font="Liberation Sans:style=Bold");
  }
}

cx = 10; ry = 13;
// Row 1 — height (grip) ladder, baseline footprint
translate([0*cx,0])  clip(ht=3.0, label="1");          // low profile
translate([1*cx,0])  clip(ht=4.0, label="2");          // the winner (#1) as-is
translate([2*cx,0])  clip(ht=5.0, label="3");          // taller
translate([3*cx,0])  clip(ht=6.0, label="4");          // tallest grip
// Row 2 — footprint length + sturdiness
translate([0*cx,ry]) clip(arm=3.2, label="5");                 // shorter arms (smaller)
translate([1*cx,ry]) clip(arm=5.0, label="6");                 // longer arms (more hold)
translate([2*cx,ry]) clip(wall=1.2, lip=1.2, label="7");       // beefier (stronger grip)
translate([3*cx,ry]) clip(wall=0.8, lip=0.7, label="8");       // daintier (slimmer/lighter)
