// Overview of the askew ("hand-stacked") box-pyramids: rows = square1, square2,
// mixed1, mixed2; columns = 40 / 60 / 80 mm.  Seeds match the parts.
use <wallrows.scad>
$fn = 28;
module row(yc, mixed, s) {
  translate([  0, yc, 0]) box_pyramids(40, mixed, s, true);
  translate([ 52, yc, 0]) box_pyramids(60, mixed, s, true);
  translate([124, yc, 0]) box_pyramids(80, mixed, s, true);
}
row(   0, false, 11);
row( -42, false, 27);
row( -90, true,  41);
row(-138, true,  63);
