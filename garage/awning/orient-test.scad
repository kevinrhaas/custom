// ===========================================================================
// PRINT-ORIENTATION TEST SLICE for the corrugated straight piece.
// A short slice of straight_raw, rotated into each candidate print orientation
// so it rests on the bed (Z-up = the printer's up). Generate one per -D orient,
// drop into the slicer ("place on face" if needed), and compare surface quality.
//
// Does NOT change any final pieces. Reuses awning.scad's modules.
// ===========================================================================
include <awning.scad>

slice_len = 40;            // length of the test slice
orient    = "roof_up";     // roof_up | roof_down | on_back | on_end

module slc() straight_raw(slice_len, 0);

// rest-on-bed helper: drop the lowest point to z=0
module bed(m) {
  // crude but works: large negative offset then the part is positioned by the slicer.
  // here we just rotate; slicer auto-drops to the plate.
  children();
}

if (orient == "roof_up")
  // baseline: corrugation faces UP at the roof pitch, channel skirts on the bed.
  // Rough because the rounded rib tops are near-horizontal -> layer stair-stepping.
  rotate([90,0,0]) slc();

else if (orient == "roof_down")
  // corrugation faces DOWN onto the glass bed -> rib tops print glassy-smooth.
  // Channel opening faces up (no support). Valleys become short overhangs.
  rotate([-90,0,0]) slc();

else if (orient == "on_back")
  // back/outer wall on the bed -> the roof slope stands VERTICAL, ribs run vertical
  // -> smoothest corrugation (printed as in-plane arcs). Overhang needs support.
  rotate([0,90,0]) slc();

else if (orient == "on_end")
  // stand on the end -> length vertical. The corrugation wave becomes stacked
  // layers (stair-steps on the wave) + tall/thin/slow. Shown for comparison.
  slc();
