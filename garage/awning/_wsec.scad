include <awning.scad>
// section through the wire hole (X=5.5): horizontal axis = Z (length of leg B), vertical = Y
projection(cut=true) rotate([0,90,0]) translate([-5.5,0,0]) corner();
