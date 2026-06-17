include <awning.scad>
// overhang flipped to +X, keep the OTHER half (x>=z) via the complementary wedge
intersection() {
  mirror([1,0,0]) straight_raw(corner_leg,0);
  rotate([0,-45,0]) translate([-BIG/2,-BIG/2, miter_over-BIG]) cube([BIG,BIG,BIG]); // z<=x side
}
