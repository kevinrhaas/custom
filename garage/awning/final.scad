// ===========================================================================
// FINAL ASSEMBLY pieces for the garage awning. Reuses the validated modules in
// awning.scad (included below). Run with -D 'part="none"' so awning.scad's own
// dispatch stays silent, then select a piece with -D 'piece="a3"' etc.
//
// Tiling (outer/plexi end -> corner):
//   Wall A 290 = a1(100, end cap built in) + a2 center 100 + a3 45 + corner-leg 45
//   Wall B 300 = b1(100, end cap built in) + b2 center 100 + b3 55 + corner-leg 45
//   a1/b1 are generated from awning.scad's endcap() with glue_seat=100 (L/R hand).
//
// Alignment: PIN HOLES on the flat butt joints (a3<->corner, b3<->corner).
// Pins are a separate printable part ("pins"). Holes are symmetric about x=0 so
// they line up regardless of which way a piece is flipped on the wall.
// ===========================================================================
include <awning.scad>

piece = "a3";   // a2 | b2 | a3 | b3 | corner | pins   (a1/b1 -> see header)

/* [ Pin alignment ] */
pin_d     = 4.2;     // hole diameter
pin_clear = 0.30;    // pin is this much under the hole
pin_depth = 6;       // hole depth into each mating face
pin_y     = 5;       // height of the pins in the solid roof body
pin_xs    = [-3, 3]; // symmetric about x=0 -> flip-proof
pin_fn    = 32;

// pin holes drilled into the +Z mating face of a straight piece of length L
module pin_holes_pZ(L)
  for (px = pin_xs)
    translate([px, pin_y, L - pin_depth])
      cylinder(d=pin_d, h=pin_depth + 1, $fn=pin_fn);

// a3 / b3: straight on the coping, pin holes at the corner (+Z) end
module straight_pinned(L) difference() { straight_raw(L, 0); pin_holes_pZ(L); }

// corner: the validated corner() (filled L + mitered valley + 10 mm wire drill)
// plus pin holes at BOTH leg ends to receive a3 / b3.
module corner_final() {
  difference() {
    corner();
    // leg A end (z = corner_leg), holes into -Z
    for (px = pin_xs)
      translate([px, pin_y, corner_leg - pin_depth])
        cylinder(d=pin_d, h=pin_depth + 1, $fn=pin_fn);
    // leg B end (x = corner_leg), holes into -X  (z mirrors x by symmetry)
    for (pz = pin_xs)
      translate([corner_leg + 0.5, pin_y, pz])
        rotate([0,-90,0]) cylinder(d=pin_d, h=pin_depth + 1, $fn=pin_fn);
  }
}

// the printable alignment pin (chamfered both ends for easy insertion)
module pin1() {
  r  = (pin_d - pin_clear)/2;
  L  = 2*pin_depth - 1.5;
  ch = 0.7;
  hull() {
    translate([0,0,ch])     cylinder(r=r,    h=L-2*ch, $fn=pin_fn);
    translate([0,0,0])      cylinder(r=r-ch, h=0.01,   $fn=pin_fn);
    translate([0,0,L-0.01]) cylinder(r=r-ch, h=0.01,   $fn=pin_fn);
  }
}
module pins_plate() for (i=[0:5]) translate([i*7, 0, 0]) pin1();   // 6 pins (4 needed)

// --- dispatch (only fires when run as the top file) ------------------------
if      (piece == "a2")     straight_raw(100, cap_h);   // center, sits on the cap
else if (piece == "b2")     straight_raw(100, cap_h);
else if (piece == "a3")     straight_pinned(45);
else if (piece == "b3")     straight_pinned(55);
else if (piece == "corner") corner_final();
else if (piece == "pins")   pins_plate();
