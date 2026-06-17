// ===========================================================================
// PLEXI CORNER CLIP — FIT LADDER (wider channel)
// 4 clips on one plate, the plexi slot stepped WIDER in 0.25 mm increments,
// for when the first piece read too tight. slot = t + clear.
//   #1 clear +0.25  -> slot 1.75      #3 clear +0.75 -> slot 2.25
//   #2 clear +0.50  -> slot 2.00      #4 clear +1.00 -> slot 2.50
// Number is recessed on each top cap. Same press-fit U-channel design.
// ===========================================================================

t = 1.5;            // nominal plexi thickness
show_num = true;    // -D show_num=false to print without the numbers
$fn = 48;

module clip(clear=0, arm=4, ht=4, wall=1, lip=0.9, toph=1, label="") {
  slot  = t + clear;
  cross = wall + slot + lip;
  difference() {
    union() {
      difference() {
        union() {
          translate([-wall,-wall,0]) cube([arm+wall, cross, ht]);
          translate([-wall,-wall,0]) cube([cross, arm+wall, ht]);
        }
        translate([0,0,-0.01]) cube([arm+1, slot, ht-toph+0.01]);   // slot A
        translate([0,0,-0.01]) cube([slot, arm+1, ht-toph+0.01]);   // slot B
      }
      translate([-wall,-wall,ht-toph]) cube([arm+wall, arm+wall, toph]);
    }
    if (label != "" && show_num)
      translate([(arm-wall)/2, (arm-wall)/2, ht-0.4]) linear_extrude(0.6)
        text(label, size=2.3, halign="center", valign="center",
             font="Liberation Sans:style=Bold");
  }
}

cx = 10;
translate([0*cx, 0]) clip(clear=0.25, label="1");
translate([1*cx, 0]) clip(clear=0.50, label="2");
translate([2*cx, 0]) clip(clear=0.75, label="3");
translate([3*cx, 0]) clip(clear=1.00, label="4");
