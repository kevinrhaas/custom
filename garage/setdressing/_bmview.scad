// Overview of the deep box-mound collection: rows = square1, square2,
// mixed1, mixed2; columns = 40 / 60 / 80 mm wide.  Seeds match the parts.
// (preview only -- not a print plate)
use <wallrows.scad>
$fn = 28;
module row(yc, mixed, s) {
  translate([  0, yc, 0]) box_mound(40, mixed, s);
  translate([ 52, yc, 0]) box_mound(60, mixed, s);
  translate([124, yc, 0]) box_mound(80, mixed, s);
}
row(   0, false, 11);   // square1
row( -58, false, 27);   // square2
row(-116, true,  41);   // mixed1
row(-178, true,  63);   // mixed2
