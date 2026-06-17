// ===========================================================================
// PLEXI CORNER CLIP — joins two 1.5 mm plexiglass panels at a 90° butt corner.
// A small corner CAP. Built the clean way: one solid L-block wraps the outside
// corner, then a 1.5 mm slot is CUT down each arm. What's left is a proper
// U-channel on each panel (outer wall + inner lip, equal and regular) joined
// solidly through the corner, with a top that caps the panel top edges and ties
// it all together. Push it down onto the top corner; friction holds it.
// Same parametric press-fit idea as the awning channels. Units = mm.
//
// Plan (looking down the corner): outside corner at the origin.
//   Panel A runs +X, outer face on y=0   (slot y: 0..t)
//   Panel B runs +Y, outer face on x=0   (slot x: 0..t)
//   Clip body wraps the -X,-Y outside.   Inside (cars) = +X,+Y.
// ===========================================================================

/* [ Fit ] */
t      = 1.5;    // plexi panel thickness
clear  = 0.00;   // slot clearance: 0 = snug press, +0.1 looser, -0.1 tighter
slot   = t + clear;

/* [ Size ] */
arm    = 4.0;    // how far the clip runs along each panel
ht     = 4.0;    // overall height (along the corner)
wall   = 1.0;    // outer shell wall thickness
lip    = 0.9;    // inner lip thickness (grips the panel's inner face)
toph   = 1.0;    // top thickness (caps the panel tops + ties it together)

cross  = wall + slot + lip;   // full width of each arm = outer wall + slot + lip
$fn    = 32;

module clip() {
  union() {
    // --- two slotted arms: solid bar with the 1.5 mm panel slot cut in ---
    difference() {
      union() {
        translate([-wall, -wall, 0]) cube([arm + wall, cross, ht]);   // arm A (+X)
        translate([-wall, -wall, 0]) cube([cross, arm + wall, ht]);   // arm B (+Y)
      }
      translate([0, 0, -0.01]) cube([arm + 1, slot, ht - toph + 0.01]); // slot A
      translate([0, 0, -0.01]) cube([slot, arm + 1, ht - toph + 0.01]); // slot B
    }
    // --- square top slab: caps the panel top edges + ties it all together -
    translate([-wall, -wall, ht - toph]) cube([arm + wall, arm + wall, toph]);
  }
}

clip();
