include <awning.scad>
// single inside-corner leg: overhang faces +X (interior), wall along +Z, mitered to z>=x
intersection() { mirror([1,0,0]) straight_raw(corner_leg,0); keep_ZX(); }
