// Bonded preview: one barrel row + one tire row side-by-side, low angle
// so the raft is visible under the items.
use <wallrows.scad>
$fn = 24;
BONDED = true;
// (modules pulled from wallrows.scad)
bond() barrel_row(n=5, seed=2, depth=1);
translate([0, -22, 0]) bond() tires_row([5,3,6,4], seed=1);
