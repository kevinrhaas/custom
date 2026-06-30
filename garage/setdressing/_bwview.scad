// Overview of the box-wall collection: rows = square1, square2, mixed1, mixed2;
// columns = 40 / 60 / 80 mm wide.  Seeds match the exported parts.
// (preview only -- not a print plate)
use <wallrows.scad>
$fn = 28;
module row(yc, mixed, s) {
  translate([  0, yc, 0]) box_wall(40, mixed, s);
  translate([ 50, yc, 0]) box_wall(60, mixed, s);
  translate([120, yc, 0]) box_wall(80, mixed, s);
}
row(   0, false, 11);   // square1
row( -34, false, 27);   // square2
row( -78, true,  41);   // mixed1
row(-112, true,  63);   // mixed2
