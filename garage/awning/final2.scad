// ===========================================================================
// FINAL ASSEMBLY v2 — pin holes on EVERY joint, located in the OVERHANG zone
// (the only region solid through BOTH straights and the raised-cap centers).
// 2 pins per joint. Reuses awning.scad's validated modules.
//
// Run with -D 'part="none"' -D 'piece="..."'.  a1/b1 also need -D glue_seat=100.
//
// Pin map (sx = straight overhang side -X; cx = corner overhang side +X):
//   a1 inner | a2 both ends | a3 both ends | corner legA+legB | b3 both | b2 both | b1 inner
// The overhang sides mate piece-to-piece, so sx on the straights and cx (mirror)
// on the corner line up once the pieces are set overhang-toward-the-cars.
// ===========================================================================
include <awning.scad>

piece = "none";

/* [ Pin alignment ] */
pin_d     = 4.2;          // hole diameter
pin_clear = 0.30;         // pin is this much under the hole
pin_depth = 6;            // hole depth into each face
pin_y     = 6;            // height in the overhang roof (above the LED cove)
sx        = [-11, -4];    // straight pins: overhang side (-X)
cx        = [ 11,  4];    // corner pins: overhang side (+X) = mirror of sx
pin_fn    = 32;

module hZ0(xs)   for (px=xs) translate([px,pin_y,-0.5])         cylinder(d=pin_d,h=pin_depth+0.5,$fn=pin_fn);
module hZL(L,xs) for (px=xs) translate([px,pin_y,L-pin_depth])  cylinder(d=pin_d,h=pin_depth+0.6,$fn=pin_fn);

module center_v2() difference() { straight_raw(100,cap_h); hZ0(sx); hZL(100,sx); } // a2 / b2
module a3_v2()     difference() { straight_raw(45,0);      hZ0(sx); hZL(45,sx);  }
module b3_v2()     difference() { straight_raw(55,0);      hZ0(sx); hZL(55,sx);  }

// center with a SMOOTH (flat, no-corrugation) fascia band of length `flat_len` added
// at the end-straight-facing end (toward a1/b1). The band is plain base_solid (cross-
// section, no roof/fascia ribs) -> a clean flat trim strip + extra length. Pins move
// to the new end face.  flat_len passed via -D.
flat_len  = 0;   // smooth band on the a1/b1-facing end
flat_len2 = 0;   // smooth band on the a3/b3-facing end (0 = corrugated)
module hZface(zf,xs) for (px=xs) translate([px,pin_y,zf-0.5]) cylinder(d=pin_d,h=pin_depth+0.5,$fn=pin_fn);
module center_flat() difference() {
  union() {
    straight_raw(100, cap_h);                                    // corrugated, z 0..100
    translate([0,0,-flat_len])  base_solid(flat_len + 0.01,  cap_h); // band -> a1/b1 end
    translate([0,0,100 - 0.01]) base_solid(flat_len2 + 0.01, cap_h); // band -> a3/b3 end
  }
  hZface(-flat_len, sx);        // pins at the a1/b1 end face
  hZL(100 + flat_len2, sx);     // pins at the a3/b3 end face
}

// integrated end-straight (endcap with glue_seat=100). Pins on the INNER end only;
// cut before the L-mirror so they follow the hand.
module endstraight_R() difference() { endcap(); hZ0(sx); }
module endstraight_v2(hnd) { if (hnd=="L") mirror([0,0,1]) endstraight_R(); else endstraight_R(); }

// b1 with the cap-end interior HOLLOWED up to the ROOF: clears the channel structure
// AND the inner roof body between the front fascia and back skirt for the last ~12mm,
// cutting UP to y = plexi_rise+clearance (+9.6, the plexi-slot depth / just under the
// roof). Removes the inner-wall stub too. Leaves a thin roof skin (visible corrugation
// untouched), the front fascia, the back skirt, and the plexi slot.
// Cavern: full height ~24.6mm (bottom -15 -> +9.6), usable inside ~16.6mm (floor -7 -> +9.6).
cap_hollow_z   = 7;                      // how far into the straight part (Z)
cap_hollow_top = plexi_rise + plexi_cl;  // +9.6 ceiling (= plexi slot top)
module b1_hollow() difference() {
  endstraight_v2("R");
  translate([xin + lip_t, -back_skirt - 1, glue_seat - cap_hollow_z])
    cube([ci - (xin + lip_t), cap_hollow_top - (-back_skirt - 1), cap_hollow_z + 0.01]);
}

// a1 = the L-hand piece, which is just the Z-mirror of the R piece -> mirror the
// whole hollowed R piece and the cavern follows to a1's cap end automatically.
module a1_hollow() mirror([0,0,1]) b1_hollow();

// corner: validated corner() (drill + filled L) + pins at both leg ends
module corner_v2() difference() {
  corner();
  for (px=cx) translate([px,pin_y,corner_leg-pin_depth]) cylinder(d=pin_d,h=pin_depth+0.6,$fn=pin_fn);           // leg A
  for (pz=cx) translate([corner_leg+0.5,pin_y,pz]) rotate([0,-90,0]) cylinder(d=pin_d,h=pin_depth+0.6,$fn=pin_fn);// leg B
}

// printable chamfered pin + a plate of 14 (12 needed for 6 joints, +2 spare)
module pin1() {
  r=(pin_d-pin_clear)/2; L=2*pin_depth-1.5; ch=0.7;
  hull() {
    translate([0,0,ch])     cylinder(r=r,    h=L-2*ch, $fn=pin_fn);
    cylinder(r=r-ch, h=0.01, $fn=pin_fn);
    translate([0,0,L-0.01]) cylinder(r=r-ch, h=0.01,   $fn=pin_fn);
  }
}
module pins_plate() for (i=[0:13]) translate([(i%7)*7, floor(i/7)*14, 0]) pin1();

if      (piece=="center")     center_v2();
else if (piece=="centerflat") center_flat();   // -D flat_len=0.5 (a2) / 1.0 (b2)
else if (piece=="a3")     a3_v2();
else if (piece=="b3")     b3_v2();
else if (piece=="a1")     endstraight_v2("L");
else if (piece=="b1")     endstraight_v2("R");
else if (piece=="a1hollow") a1_hollow();
else if (piece=="b1hollow") b1_hollow();
else if (piece=="corner") corner_v2();
else if (piece=="pins")   pins_plate();
