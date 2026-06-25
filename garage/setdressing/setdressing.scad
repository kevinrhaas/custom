// ===========================================================================
// 1:64 GARAGE SET DRESSING  --  shop clutter for the baby-garage diorama
// Parametric. Units = mm. Z is UP; every piece sits ON the bed at z=0.
//
// Each "piece" is a pre-combined little GROUPING (a stack / cluster), not a
// single object, so you scatter them around the garage and butt them together
// into bigger piles. Footprints are kept compact for that.
//
// Build one piece:        -D 'part="drumtrio"'
// Build a print plate:     -D 'part="plateA"'   (also plateB, plateC)
// Whole-collection view:   part="all"   (default; for rendering, not printing)
//
// Scale check @ 1:64:  55gal drum 23x34.5in -> 9.0 x 13.7 mm
//                      car tire 25in OD     -> 9.9 mm OD
//                      pallet 48x40in       -> 19 x 16 mm
// ===========================================================================

part = "all";

$fn = 48;
EPS = 0.01;

// ---- shared palette of dims (mm @ 1:64) ----------------------------------
drum_d  = 9.0;   drum_h  = 13.7;
tire_od = 10.0;  tire_w  = 3.2;  tire_id = 4.4;
gap     = 0.0;   // touching clusters

// ---------------------------------------------------------------------------
// HELPERS
// ---------------------------------------------------------------------------

// rounded box, flat top/bottom, rounded vertical edges, base at z=0
module rbox(x,y,z,r=0.6){
  hull() for(sx=[-1,1],sy=[-1,1])
    translate([sx*(x/2-r), sy*(y/2-r), 0])
      cylinder(r=r, h=z);
}

// fully rounded box (soft on all edges) via offset on a profile
module softbox(x,y,z,r=0.8){
  hull() for(sx=[-1,1],sy=[-1,1],sz=[-1,1])
    translate([sx*(x/2-r), sy*(y/2-r), z/2 + sz*(z/2-r)])
      sphere(r=r,$fn=24);
}

// horizontal rolling hoop ring at height zz on a cylinder of radius rr
module hoop(rr, zz, t=0.7){
  translate([0,0,zz]) rotate_extrude($fn=$fn)
    translate([rr,0]) circle(d=t,$fn=12);
}

// ---------------------------------------------------------------------------
// 1. OIL DRUM  (single, reused)
// ---------------------------------------------------------------------------
module drum(d=drum_d, h=drum_h){
  rr=d/2;
  cylinder(d=d, h=h);
  hoop(rr, h*0.30); hoop(rr, h*0.52); hoop(rr, h*0.74);   // rolling hoops
  // top + bottom chimes
  hoop(rr-0.25, h-0.4, 0.9);  hoop(rr-0.25, 0.4, 0.9);
  // bungs on the lid
  translate([rr*0.45,0,h-EPS]) cylinder(d=1.3,h=0.5,$fn=16);
  translate([-rr*0.45,0,h-EPS]) cylinder(d=0.9,h=0.4,$fn=12);
}

module drumtrio(){
  s = drum_d/2 + 0.05;                 // triangle pack radius
  for(a=[90,210,330]) rotate(a) translate([s*2/sqrt(3),0,0]) drum();
}

module drum_roller(){
  // two upright + one tipped on its side, with a little chock
  translate([-drum_d/2-0.1, 0,0]) drum();
  translate([ drum_d/2+0.1, 0,0]) drum();
  // tipped drum lying along +Y in front
  translate([0, drum_d/2+drum_h/2+0.2, drum_d/2])
    rotate([-90,0,0]) drum();
}

// ---------------------------------------------------------------------------
// 2. WOODEN CRATE  (slatted)
// ---------------------------------------------------------------------------
module crate(s=7){
  // SOLID block with shallow incised slat lines (not openings)
  difference(){
    rbox(s,s,s,0.4);
    // horizontal slat grooves on the 4 walls (shallow, do not pass through)
    for(zz=[s*0.28, s*0.5, s*0.72])
      for(rot=[0,90,180,270])
        rotate([0,0,rot]) translate([0, s/2, zz])
          cube([s-1.4, 0.5, 0.22], center=true);
    // corner-post relief: a vertical groove near each vertical edge
    for(sx=[-1,1],sy=[-1,1])
      translate([sx*(s/2-1.0), sy*(s/2-1.0), s/2])
        cube([0.45,0.45,s+1], center=true);
    // lid seam: thin recessed border near the top edge
    translate([0,0,s-0.11]) difference(){
      cube([s-1.2, s-1.2, 0.25], center=true);
      cube([s-2.4, s-2.4, 0.5], center=true);
    }
  }
}

module cratestack(){
  s=7;
  translate([-s/2-0.1,-s/2-0.1,0]) crate(s);
  translate([ s/2+0.1,-s/2-0.1,0]) crate(s);
  translate([0, s/2+0.1, 0]) crate(s);
  translate([0,0,s+0.1]) crate(s*0.86);     // one on top
}

// ---------------------------------------------------------------------------
// 3. CARDBOARD BOXES (offset stack)
// ---------------------------------------------------------------------------
module box(x,y,z){
  difference(){
    rbox(x,y,z,0.35);
    // tape / flap seam down the top
    translate([0,0,z-0.15]) cube([0.4, y+1, 0.5], center=true);
    translate([0,0,z-0.15]) cube([x+1, 0.4, 0.5], center=true);
  }
}
module boxstack(){
  box(8,6.5,5);
  translate([0.8,-0.6,5+0.05]) rotate([0,0,8]) box(7,6,4.2);
  translate([-0.6,0.7,5+4.2+0.1]) rotate([0,0,-6]) box(6,5,3.6);
  translate([6,1,0]) rotate([0,0,18]) box(5,4.5,4);   // a loose one beside
}

// ---------------------------------------------------------------------------
// 4. TIRES
// ---------------------------------------------------------------------------
module tire(od=tire_od, w=tire_w, id=tire_id){
  th=(od-id)/2;
  rotate_extrude($fn=64)
    translate([id/2,0])
      offset(r=0.55) offset(r=-0.55) square([th, w]);
}
module tirestack(){
  n=5;
  for(i=[0:n-1]) translate([0,0,i*(tire_w+0.05)]) rotate([0,0,i*22]) tire();
  // one leaning against the stack
  translate([tire_od*0.55, 0, tire_od/2]) rotate([0,72,0]) tire();
}

// ---------------------------------------------------------------------------
// 5. PALLET + LOAD
// ---------------------------------------------------------------------------
module pallet(x=19, y=16, h=2.2){
  deck=0.7; foot=h-2*deck;
  // bottom deck boards (along x)
  for(yy=[-y/2+1, 0, y/2-1]) translate([0,yy,0]) cube([x, 2, deck], center=true);
  // feet/stringers
  for(xx=[-x/2+1.2,0,x/2-1.2]) translate([xx,0,h/2]) cube([1.6, y, foot], center=true);
  // top deck boards (along y)
  for(i=[-3:3]) translate([i*(x/7),0,h-deck/2]) cube([1.6, y, deck], center=true);
}
module palletload(){
  pallet();
  // shrink-wrapped box block
  translate([0,0,2.2]) softbox(17,14,9,1.2);
  // a sack flopped on top
  translate([2,-1,2.2+9]) rotate([0,0,20]) softbox(9,6,3.2,1.4);
}

// ---------------------------------------------------------------------------
// 6. JERRY CANS
// ---------------------------------------------------------------------------
module jerrycan(w=5.2,d=2.6,h=7.1){
  difference(){
    rbox(w,d,h,0.6);
    // shallow rectangular X-brace recess on each broad face (NATO can look)
    for(sy=[-1,1]) translate([0,sy*(d/2+0.08),h*0.5])
      rbox(w-1.6, 0.5, h-2.0, 0.3);
  }
  // top handle (3 ridges, the classic can grip)
  for(xx=[-w*0.28,0,w*0.28]) translate([xx,0,h]) rbox(0.9, d-0.6, 1.4, 0.35);
  // spout cap on the corner
  translate([w*0.30,0,h+0.4]) cylinder(d=1.3,h=1.0,$fn=12);
}
module jerrycans(){
  translate([-3.2,0,0]) jerrycan();
  translate([ 3.2,0.3,0]) rotate([0,0,12]) jerrycan();
  translate([0, 3.5,0]) jerrycan(4.2,2.2,4.8);   // short one in front
}

// ---------------------------------------------------------------------------
// 7. ROLLER TOOL CHEST  (cabinet + top box on casters)
// ---------------------------------------------------------------------------
module toolchest(){
  w=16.3; d=7.1; cab=10.0; topb=4.5; cz=1.2;
  // casters
  for(sx=[-1,1],sy=[-1,1]) translate([sx*(w/2-1.2), sy*(d/2-1.2), cz/2])
    cylinder(d=cz+0.4, h=cz, center=true,$fn=16);
  // cabinet body
  translate([0,0,cz]) difference(){
    rbox(w,d,cab,0.5);
    // drawer lines (front face at +Y? use -Y as front)
    for(zz=[cab*0.22, cab*0.45, cab*0.68])
      translate([0,-d/2,zz+cz-cz]) translate([0,0,0])
        translate([0,-0.0,zz]) cube([w-1.2,0.5,0.5],center=true);
  }
  // drawer handles
  for(zz=[cab*0.22, cab*0.45, cab*0.68])
    translate([0,-d/2-0.1,cz+zz+0.6]) cube([w-3,0.6,0.5],center=true);
  // top tool box
  translate([0,0,cz+cab+0.05]) difference(){
    rbox(w-0.8,d,topb,0.5);
    translate([0,-d/2,topb*0.5]) cube([w-3,0.5,0.5],center=true);
  }
  // top handle
  translate([0,0,cz+cab+topb]) rbox(w-6,d-1.5,0.8,0.4);
}

// ---------------------------------------------------------------------------
// 8. GAS / WELDING CYLINDER CART
// ---------------------------------------------------------------------------
module gascyl(d=3.6,h=20){
  cylinder(d=d,h=h*0.9);
  translate([0,0,h*0.9]) sphere(d=d);                  // domed shoulder
  translate([0,0,h*0.9]) cylinder(d=d*0.35,h=h*0.12);  // valve neck
  difference(){                                        // valve cap ring
    translate([0,0,h*0.9]) cylinder(d=d*0.7,h=h*0.1);
    translate([0,0,h*0.9-EPS]) cylinder(d=d*0.5,h=h*0.1+0.1);
  }
}
module gascart(){
  // hand-truck base
  translate([0,0,0]) rbox(10,7,0.6,0.4);
  // axle wheels
  for(sx=[-1,1]) translate([sx*5, 3.2, 1.4]) rotate([0,90,0]) cylinder(d=2.8,h=0.8,center=true,$fn=20);
  // upright frame
  for(sx=[-1,1]) translate([sx*3.5,-3,0]) cube([0.8,0.8,18]);
  // two cylinders
  translate([-2.2,0,0.6]) gascyl();
  translate([ 2.2,0,0.6]) gascyl();
  // chain strap across
  translate([0,2.2,12]) cube([9,0.6,0.8],center=true);
}

// ---------------------------------------------------------------------------
// 9. SHELF RACK (3-tier, loaded)
// ---------------------------------------------------------------------------
module shelfrack(){
  w=14.3; d=7.1; h=22; post=0.9; shelf=0.6;
  // posts
  for(sx=[-1,1],sy=[-1,1]) translate([sx*(w/2-post/2),sy*(d/2-post/2),0])
    cube([post,post,h]);
  // shelves
  zz=[0.6, h*0.34, h*0.67, h-0.6];
  for(z=zz) translate([0,0,z]) rbox(w,d,shelf,0.3);
  // clutter on shelves
  translate([-3, 0, zz[1]+shelf]) box(4,4,3.5);
  translate([2.5,-1, zz[1]+shelf]) box(5,4.5,3);
  translate([-2, 1, zz[2]+shelf]) drum(3.5,5);
  translate([3,  0, zz[2]+shelf]) drum(3.5,5);
  translate([0,0, zz[3]+shelf]) box(7,5.5,3.5);
}

// ---------------------------------------------------------------------------
// 10. BUCKETS (5-gal, nested + tipped)
// ---------------------------------------------------------------------------
module bucket(d=4.8,h=5.75){
  difference(){
    cylinder(d1=d*0.82,d2=d,h=h);
    translate([0,0,0.6]) cylinder(d1=d*0.7,d2=d-0.8,h=h);
  }
  translate([0,0,h]) rotate_extrude($fn=$fn) translate([d/2-0.2,0]) circle(d=0.9,$fn=12); // rim
  // bail handle
  rotate([0,0,90]) translate([0,0,h]) rotate([90,0,0])
    difference(){ cylinder(d=d*0.9,h=0.4,center=true,$fn=24); cylinder(d=d*0.9-0.8,h=1,center=true,$fn=24); }
}
module buckets(){
  bucket();                                   // base bucket
  translate([0,0,1.6]) bucket();              // nested in it
  translate([5.5,0,4.8*0.5]) rotate([90,0,30]) bucket();   // tipped beside
}

// ---------------------------------------------------------------------------
// 11. CABLE SPOOL + carton
// ---------------------------------------------------------------------------
module spool(d=14.3, w=11.9){
  flange=1.0; hub=d*0.42;
  for(zz=[0, w-flange]) translate([0,0,zz]) cylinder(d=d,h=flange);
  translate([0,0,flange-EPS]) cylinder(d=hub,h=w-2*flange+2*EPS);
  // center bore
}
module cablespool(){
  // spool lying on its side so it reads as a spool standing on the floor
  translate([0,0,14.3/2]) rotate([90,0,0]) translate([0,0,-11.9/2]) spool();
  translate([10,0,0]) box(6,6,5);             // a carton next to it
}

// ---------------------------------------------------------------------------
// 12. SACK PILE (stacked bags)
// ---------------------------------------------------------------------------
module sack(x=9.5,y=6.3,z=2.0){ softbox(x,y,z,1.6); }
module sackpile(){
  sack();                          translate([0.4,0,0]) sack();
  translate([0,0,2.0]) rotate([0,0,90]) sack();
  translate([0,0,4.0]) rotate([0,0,15]) sack(8.5,5.6,1.8);
  translate([0,0,4.0]) rotate([0,0,95]) translate([1,0,0]) sack(8,5,1.7);
  translate([0,0,5.8]) rotate([0,0,45]) sack(8,5.4,1.7);
}

// ---------------------------------------------------------------------------
// 13. TRAFFIC CONES + PARKING BLOCK
// ---------------------------------------------------------------------------
module cone(h=6){
  base=h*0.7;
  rbox(base,base,0.6,0.8);
  translate([0,0,0.5]) cylinder(d1=base*0.7,d2=1.0,h=h-0.5);
}
module conesblock(){
  translate([-3,0,0]) cone();
  translate([3,1.2,0]) cone(5.2);
  // parking block / wheel stop
  translate([0,-6,0]) difference(){
    rotate([90,0,0]) rotate([0,0,90])
      linear_extrude(11) polygon([[0,0],[3.2,0],[2.4,2.2],[0.8,2.2]]);
    translate([0,0,1.2]) for(sx=[-1,1]) translate([sx*3.5,0,0]) cylinder(d=1.2,h=3,center=true);
  }
}

// ===========================================================================
// PIECE DISPATCH
// ===========================================================================
module piece(name){
  if(name=="drumtrio")    drumtrio();
  else if(name=="drumroller") drum_roller();
  else if(name=="cratestack") cratestack();
  else if(name=="boxstack")   boxstack();
  else if(name=="tirestack")  tirestack();
  else if(name=="palletload") palletload();
  else if(name=="jerrycans")  jerrycans();
  else if(name=="toolchest")  toolchest();
  else if(name=="gascart")    gascart();
  else if(name=="shelfrack")  shelfrack();
  else if(name=="buckets")    buckets();
  else if(name=="cablespool") cablespool();
  else if(name=="sackpile")   sackpile();
  else if(name=="conesblock") conesblock();
}

NAMES = ["drumtrio","drumroller","cratestack","boxstack","tirestack",
         "palletload","jerrycans","toolchest","gascart","shelfrack",
         "buckets","cablespool","sackpile","conesblock"];

// ---- layout for the "all" overview + print plates -------------------------
module gridlayout(names, cols=4, pitch=26){
  for(i=[0:len(names)-1])
    translate([(i%cols)*pitch, -floor(i/cols)*pitch, 0]) piece(names[i]);
}

if(part=="all")          gridlayout(NAMES, 4, 26);
else if(part=="plateA")  gridlayout(["drumtrio","drumroller","cratestack","boxstack","tirestack"],3,26);
else if(part=="plateB")  gridlayout(["palletload","jerrycans","toolchest","gascart","shelfrack"],3,26);
else if(part=="plateC")  gridlayout(["buckets","cablespool","sackpile","conesblock"],2,26);
else piece(part);
