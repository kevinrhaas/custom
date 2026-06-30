// ===========================================================================
// 1:64 GARAGE -- WALL-LINING CLUTTER ROWS
// Companion to setdressing.scad: longer multi-item clusters that sit
// against a wall, like stuff that piled up over the years.
//   - Each "cluster" is one printable unit (~30-40mm long, ~10-18mm deep).
//   - Everything upright, flat on the bed -- NO leaners, NO overhangs.
//   - Random-ish via seeded rands(); change `seed` for a different roll.
//   - Each plate_*() packs 4 straight variations + 1 corner piece.
//
// Render one plate:        -D 'part="barrels"'   (also tires|boxes|mixed)
// Overview (all 4):        -D 'part="all"'   (default)
//
// Wall budget at 1:64 = ~100 mm per wall arm. A typical plate piece is
// 30-40 mm long, so plan on 2-3 pieces per wall plus the corner.
// ===========================================================================

use <setdressing.scad>

// QUALITY = "high" (default, smooth) or "low" (slicer-friendly).
// Override on CLI:  -D 'QUALITY="low"'
QUALITY = "high";
$fn       = QUALITY == "high" ? 48 : 24;
fn_tire   = QUALITY == "high" ? 72 : 36;
n_tread   = QUALITY == "high" ? 18 : 12;
fn_rim    = QUALITY == "high" ? 48 : 24;
EPS = 0.01;

// BONDED = true adds an invisible 0.4mm raft under each cluster so the
// whole cluster prints as one piece (items merged by a slim base).
// Override on CLI:  -D 'BONDED=true'
BONDED = false;
BOND_GROW = 0.4;   // outward expansion of the raft (bridges gaps between items)
BOND_H    = 0.4;   // raft thickness (2 layers @ 0.2mm = barely visible)

// Apply the bonded raft if BONDED is on, else pass through.
module bond(grow=BOND_GROW, h=BOND_H) {
  union() {
    children();
    linear_extrude(h) offset(r=grow) projection(cut=false) children();
  }
}

module maybe_bond() {
  if (BONDED) bond() children();
  else        children();
}

drum_d  = 9.0;   drum_h  = 13.7;
tire_od = 10.0;  tire_w  = 3.2;  tire_id = 4.4;

// stable pseudo-random in [lo,hi) from (seed, i)
function r(seed, i, lo=0, hi=1) = rands(lo, hi, 1, seed*97 + i*7 + 13)[0];

// Tire size presets [od, w, id]  (mm at 1:64)
TIRE_CAR   = [10.0, 3.2, 4.4];   // 25" car
TIRE_SUV   = [11.5, 3.8, 4.8];   // 30" light-truck/SUV
TIRE_TRUCK = [13.0, 4.4, 5.4];   // 33" truck
TIRE_SEMI  = [16.0, 5.0, 6.5];   // 40" semi/heavy

// Biased random tire size: mostly car, occasional larger.
function pick_tire(seed, i) =
  let(p = r(seed, i))
  p < 0.55 ? TIRE_CAR
  : p < 0.80 ? TIRE_SUV
  : p < 0.94 ? TIRE_TRUCK
  : TIRE_SEMI;

// Sum of first n elements of a numeric list (used to pack varying ODs)
function sum_first(list, n, i=0, acc=0) =
  i >= n ? acc : sum_first(list, n, i+1, acc + list[i]);

// ---------------------------------------------------------------------------
// BARRELS / DRUMS -- rows
// ---------------------------------------------------------------------------
// FRONT-ROW RANDOMNESS:
//   - ~14% chance to drop a drum entirely (gap)
//   - height varies 88-100% normally; ~12% chance of a stubby 55-75% drum
// Back row already had random skips.
module barrel_row(n=5, seed=1, depth=1) {
  s = drum_d * 1.02;
  for (i=[0:n-1]) {
    if (r(seed+3, i) > 0.14) {       // 86% kept
      stubby = r(seed+4, i) > 0.88;
      h_mult = stubby ? r(seed+5, i, 0.55, 0.78)
                      : r(seed+6, i, 0.88, 1.00);
      translate([drum_d/2 + i*s, drum_d/2, 0])
        rotate([0,0, r(seed, i, 0, 360)])
          drum(d=drum_d, h=drum_h*h_mult);
    }
  }
  if (depth >= 2) {
    for (j=[0:n-2])
      if (r(seed+1, j) > 0.30) {
        h_mult = r(seed+7, j, 0.85, 1.00);
        translate([drum_d + j*s, drum_d/2 + s*0.87, 0])
          rotate([0,0, r(seed+2, j, 0, 360)])
            drum(d=drum_d, h=drum_h*h_mult);
      }
  }
}

module barrel_corner(arm=4, seed=10) {
  s = drum_d * 1.02;
  // arm along +X (corner drum at i=0)
  for (i=[0:arm-1])
    translate([drum_d/2 + i*s, drum_d/2, 0])
      rotate([0,0, r(seed, i, 0, 360)]) drum();
  // arm along +Y (skip i=0, shared)
  for (j=[1:arm-1])
    translate([drum_d/2, drum_d/2 + j*s, 0])
      rotate([0,0, r(seed+1, j, 0, 360)]) drum();
}

// ---------------------------------------------------------------------------
// TIRES -- stacked rows
// ---------------------------------------------------------------------------
// tire2: bulged D-profile sidewall + radial tread slots + rim recess top/bot
// (replaces setdressing's plain rounded-square cross-section for a more
// tire-like silhouette at 1:64.)
module tire2(od=tire_od, w=tire_w, id=tire_id) {
  difference() {
    rotate_extrude($fn=fn_tire) {
      offset(r=0.30) offset(r=-0.30)
        polygon([
          [id/2,        0.0    ],
          [id/2,        w      ],
          [od/2 - 0.35, w      ],
          [od/2,        w*0.78 ],
          [od/2,        w*0.22 ],
          [od/2 - 0.35, 0.0    ]
        ]);
    }
    // tread blocks: radial slots in the OD band
    for (a=[0:360/n_tread:359])
      rotate([0,0, a]) translate([od/2 - 0.10, 0, w/2])
        cube([0.80, 0.45, w*0.58], center=true);
    // rim recess ring on top + bottom (shows the wheel hub area)
    for (zz=[-EPS, w-0.32+EPS])
      translate([0, 0, zz])
        difference() {
          cylinder(d=id*1.62, h=0.40, $fn=fn_rim);
          cylinder(d=id*1.12, h=0.50, $fn=fn_rim);
        }
  }
}

module tire_stack(n=4, seed=1, od=tire_od, w=tire_w, id=tire_id) {
  for (i=[0:n-1])
    translate([0, 0, i*w])
      rotate([0,0, r(seed, i, 0, 360)]) tire2(od=od, w=w, id=id);
}

// Row of stacks with mixed tire sizes; back face of each stack at y=0 (wall).
module tires_row(heights=[5,3,6,4], seed=1) {
  n = len(heights);
  sizes = [for (i=[0:n-1]) pick_tire(seed+100, i)];
  ods   = [for (sz=sizes) sz[0]];
  for (i=[0:n-1]) {
    od_i = ods[i];
    x_off = sum_first(ods, i) + i*0.25 + od_i/2;
    translate([x_off, od_i/2, 0])
      tire_stack(heights[i], seed+i,
                 od=sizes[i][0], w=sizes[i][1], id=sizes[i][2]);
  }
}

// Tires + small box pile beside (boxes positioned after the tire row's actual length)
module tires_and_boxes(seed=1) {
  n = 3;
  sizes = [for (i=[0:n-1]) pick_tire(seed+100, i)];
  ods   = [for (sz=sizes) sz[0]];
  hs    = [5, 3, 6];
  for (i=[0:n-1]) {
    od_i = ods[i];
    x_off = sum_first(ods, i) + i*0.25 + od_i/2;
    translate([x_off, od_i/2, 0])
      tire_stack(hs[i], seed+i,
                 od=sizes[i][0], w=sizes[i][1], id=sizes[i][2]);
  }
  total_x = sum_first(ods, n) + (n-1)*0.25 + 1.2;
  translate([total_x,     3, 0])    box(6, 5, 4.5);
  translate([total_x,     3, 4.55]) rotate([0,0, 8]) box(5, 4.2, 3.2);
  translate([total_x + 6, 3, 0])    box(5, 4.5, 4);
}

// Corner: 1 shared corner stack + 2 more in +X arm + 2 more in +Y arm.
module tires_corner(seed=11) {
  corner_sz = pick_tire(seed+200, 0);
  szs_x = [pick_tire(seed+200, 1), pick_tire(seed+200, 2)];
  szs_y = [pick_tire(seed+300, 0), pick_tire(seed+300, 1)];
  hxs = [4, 6, 3];
  hys = [5, 4];
  // corner stack (i=0 for +X arm, also acts as the +Y arm's corner stack)
  translate([corner_sz[0]/2, corner_sz[0]/2, 0])
    tire_stack(hxs[0], seed,
               od=corner_sz[0], w=corner_sz[1], id=corner_sz[2]);
  // +X arm (2 more stacks past the corner)
  for (i=[0:len(szs_x)-1]) {
    od_i = szs_x[i][0];
    prev = corner_sz[0] + sum_first([for (j=[0:i-1]) szs_x[j][0]], i);
    x_off = prev + (i+1)*0.25 + od_i/2;
    translate([x_off, od_i/2, 0])
      tire_stack(hxs[i+1], seed+5+i,
                 od=szs_x[i][0], w=szs_x[i][1], id=szs_x[i][2]);
  }
  // +Y arm (2 more stacks past the corner)
  for (j=[0:len(szs_y)-1]) {
    od_j = szs_y[j][0];
    prev = corner_sz[0] + sum_first([for (k=[0:j-1]) szs_y[k][0]], j);
    y_off = prev + (j+1)*0.25 + od_j/2;
    translate([od_j/2, y_off, 0])
      tire_stack(hys[j], seed+10+j,
                 od=szs_y[j][0], w=szs_y[j][1], id=szs_y[j][2]);
  }
}

// ---------------------------------------------------------------------------
// BOXES -- cardboard pile against a wall
// ---------------------------------------------------------------------------
// Base row of varying-size boxes; some get a smaller box stacked on top.
module box_row(seed=1, len=4) {
  // [x_start, w, d, h]
  base = [ [0,    7.0, 5.0, 4.5],
           [7.5,  7.0, 5.5, 4.0],
           [15.0, 6.5, 6.0, 5.2],
           [22.5, 7.0, 5.0, 4.8],
           [30.0, 6.5, 5.5, 4.0] ];
  m = min(len, len(base));
  for (i=[0:m-1]) {
    b = base[i];
    translate([b[0] + b[1]/2, b[2]/2, 0]) box(b[1], b[2], b[3]);
    if (r(seed, i) > 0.4) {
      sx = b[1]*0.70;  sy = b[2]*0.75;  sz = b[3]*0.60;
      tx = r(seed+1, i, -0.3, 0.3);
      ty = r(seed+2, i, -0.3, 0.3);
      rz = r(seed+3, i, -8, 8);
      translate([b[0] + b[1]/2 + tx, b[2]/2 + ty, b[3] + 0.05])
        rotate([0,0, rz]) box(sx, sy, sz);
    }
  }
}

module box_corner(seed=12) {
  // 3 boxes along +X
  for (i=[0:2]) {
    w = 6.5 + r(seed,   i, 0, 1.5);
    d = 5.0 + r(seed+1, i, 0, 1.2);
    h = 4.0 + r(seed+2, i, 0, 1.5);
    translate([w/2 + i*7.5, d/2, 0]) box(w, d, h);
  }
  // 3 boxes along +Y
  for (j=[1:3]) {
    w = 5.0 + r(seed+5, j, 0, 1.2);
    d = 6.5 + r(seed+6, j, 0, 1.5);
    h = 4.0 + r(seed+7, j, 0, 1.5);
    translate([w/2, d/2 + j*7.5, 0]) box(w, d, h);
  }
  // small box on top of the corner box (small enough to clear, no cantilever)
  translate([3.5, 3.5, 4.7]) rotate([0,0, r(seed,20,-10,10)]) box(4.0, 3.5, 2.8);
}

// ---------------------------------------------------------------------------
// MIXED -- drums + tires + boxes + crates -- garage hoarder vibes
// ---------------------------------------------------------------------------
module mixed_A(seed=1) {
  s = drum_d * 1.02;
  // two drums
  translate([drum_d/2,     drum_d/2, 0]) rotate([0,0, r(seed,0,0,360)]) drum();
  translate([drum_d/2 + s, drum_d/2, 0]) rotate([0,0, r(seed,1,0,360)]) drum();
  // tire stack
  tx = 2*s + tire_od/2;
  translate([tx, tire_od/2, 0]) tire_stack(5, seed+10);
  // box pile
  bx = tx + tire_od/2 + 3.5;
  translate([bx, 3,    0])   box(6, 5, 4.5);
  translate([bx, 3, 4.55])   rotate([0,0, 7]) box(4.5, 4, 3);
  // last drum
  translate([bx + 5, drum_d/2, 0])
    rotate([0,0, r(seed,5,0,360)]) drum();
}

module mixed_B(seed=2) {
  // tire stack | 3 drums | crate | small box
  s = drum_d * 1.02;
  translate([tire_od/2, tire_od/2, 0]) tire_stack(4, seed);
  x0 = tire_od + 0.5;
  for (i=[0:2])
    translate([x0 + drum_d/2 + i*s, drum_d/2, 0])
      rotate([0,0, r(seed,i+5,0,360)]) drum();
  cx = x0 + 3*s + 4.0;
  translate([cx,        3.5, 0]) crate(7);
  translate([cx + 7.5,  2.5, 0]) box(5, 4.5, 3.5);
}

module mixed_C(seed=3) {
  // 4 drums | 2 crates stacked | 2-box stack
  s = drum_d * 1.02;
  for (i=[0:3])
    translate([drum_d/2 + i*s, drum_d/2, 0])
      rotate([0,0, r(seed,i,0,360)]) drum();
  cx = 4*s + 3.5;
  translate([cx, 3.5, 0])      crate(7);
  translate([cx, 3.5, 7.05])   crate(5.5);   // smaller crate on top, centered
  bx = cx + 7.5;
  translate([bx, 3, 0])        box(7, 5.5, 4);
  translate([bx, 3, 4.05])     rotate([0,0, 6]) box(5.5, 4.5, 3.2);
}

module mixed_corner(seed=20) {
  s = drum_d * 1.02;
  // arm along +X: drum, drum, tire stack
  translate([drum_d/2,        drum_d/2, 0]) rotate([0,0, r(seed,0,0,360)]) drum();
  translate([drum_d/2 + s,    drum_d/2, 0]) rotate([0,0, r(seed,1,0,360)]) drum();
  tx = 2*s + tire_od/2;
  translate([tx, tire_od/2, 0]) tire_stack(5, seed+5);
  // arm along +Y: crate, box pile, drum
  translate([3.5, drum_d + 4,           0]) crate(7);
  translate([3,   drum_d + 4 + 8,       0]) box(6, 5, 4.5);
  translate([3,   drum_d + 4 + 8,    4.55]) rotate([0,0, 8]) box(4.5, 4, 3);
  translate([drum_d/2, drum_d + 4 + 8 + 5 + drum_d/2, 0])
    rotate([0,0, r(seed,10,0,360)]) drum();
}

// ---------------------------------------------------------------------------
// MIXED-2  -- jerry cans, buckets, pallets-with-crates
// ---------------------------------------------------------------------------
module mixed_D(seed=4) {
  // 3 jerry cans + 2 drums
  jw=5.2; jd=2.6;
  for (i=[0:2])
    translate([jw/2 + i*(jw+0.2), jd/2, 0])
      rotate([0,0, r(seed,i,-10,10)]) jerrycan();
  s = drum_d * 1.02;
  dx0 = 3*(jw+0.2) + drum_d/2 + 0.6;
  translate([dx0,     drum_d/2, 0]) rotate([0,0, r(seed,5,0,360)]) drum();
  translate([dx0 + s, drum_d/2, 0]) rotate([0,0, r(seed,6,0,360)]) drum();
}

module mixed_E(seed=5) {
  // small pallet w/ crates on top + drum row alongside
  pal_x = 14; pal_y = 9;
  translate([pal_x/2, pal_y/2, 0]) pallet(x=pal_x, y=pal_y, h=2.2);
  // 2 crates on the pallet
  translate([3.5,  pal_y/2 - 0.5, 2.25]) crate(5);
  translate([9.0,  pal_y/2 - 0.3, 2.25]) crate(4.6);
  // a smaller crate on top of the first
  translate([3.5,  pal_y/2 - 0.5, 2.25 + 5 + 0.05]) crate(3.5);
  // drums after the pallet
  s = drum_d * 1.02;
  translate([pal_x + 0.8 + drum_d/2,     drum_d/2, 0])
    rotate([0,0, r(seed,0,0,360)]) drum();
  translate([pal_x + 0.8 + drum_d/2 + s, drum_d/2, 0])
    rotate([0,0, r(seed,1,0,360)]) drum();
}

module mixed_F(seed=6) {
  // bucket cluster + drums + a small box
  bd = 4.8;
  // bucket nested-pair (stacked-inside style)
  translate([bd/2 + 0.4, bd/2 + 0.6, 0])      bucket();
  translate([bd/2 + 0.4, bd/2 + 0.6, 1.6])    bucket();
  // single bucket beside
  translate([bd + bd/2 + 1.0, bd/2 + 0.6, 0]) bucket();
  // drums
  s = drum_d * 1.02;
  dx = 2*bd + 1.6 + drum_d/2;
  translate([dx,     drum_d/2, 0]) rotate([0,0, r(seed,0,0,360)]) drum();
  translate([dx + s, drum_d/2, 0]) rotate([0,0, r(seed,1,0,360)]) drum();
  // small box on the end
  translate([dx + 2*s + 1.0, 2.5, 0]) box(5, 4.5, 3.5);
}

module mixed_G(seed=7) {
  // drum, drum, box stack, jerry can, drum
  s = drum_d * 1.02;
  jw=5.2; jd=2.6;
  translate([drum_d/2,     drum_d/2, 0]) rotate([0,0, r(seed,0,0,360)]) drum();
  translate([drum_d/2 + s, drum_d/2, 0]) rotate([0,0, r(seed,1,0,360)]) drum();
  // box stack
  bx = 2*s + 3.0;
  translate([bx, 3,    0])    box(6, 5, 4.5);
  translate([bx, 3, 4.55])    rotate([0,0, 7]) box(4.5, 4, 3);
  // jerry can
  translate([bx + 5.5, jd/2, 0]) jerrycan(w=4.2, d=2.2, h=4.8);
  // drum on the end
  translate([bx + 5.5 + 4.2 + 0.8, drum_d/2, 0])
    rotate([0,0, r(seed,5,0,360)]) drum();
}

module mixed_corner2(seed=21) {
  jw=5.2; jd=2.6;
  bd=4.8;
  // +X arm: 3 jerry cans, drum
  for (i=[0:2])
    translate([jw/2 + i*(jw+0.2), jd/2, 0])
      rotate([0,0, r(seed,i,-10,10)]) jerrycan();
  s = drum_d * 1.02;
  translate([3*(jw+0.2) + drum_d/2, drum_d/2, 0])
    rotate([0,0, r(seed,3,0,360)]) drum();
  // +Y arm: bucket-pair, crate, drum
  translate([bd/2 + 0.5,           jd + 0.5 + bd/2,            0])      bucket();
  translate([bd/2 + 0.5,           jd + 0.5 + bd/2,            1.6])    bucket();
  translate([3.5,                  jd + 0.5 + bd + 3.5 + 0.4,  0])      crate(7);
  translate([drum_d/2,             jd + 0.5 + bd + 7.4 + drum_d/2, 0])
    rotate([0,0, r(seed,10,0,360)]) drum();
}

// ---------------------------------------------------------------------------
// MIXED-3  -- pallets, crate piles, tire/box combos
// ---------------------------------------------------------------------------
module mixed_H(seed=8) {
  // crate stack + box stack + drums
  translate([3.5, 3.5, 0])       crate(7);
  translate([3.5, 3.5, 7.05])    crate(5.5);
  translate([8.0, 3.0, 0])       box(7, 5.5, 4.5);
  translate([8.0, 3.0, 4.55])    rotate([0,0, 6]) box(5.5, 4.5, 3.2);
  s = drum_d * 1.02;
  dx = 13.0 + drum_d/2;
  translate([dx,         drum_d/2, 0]) rotate([0,0, r(seed,0,0,360)]) drum();
  translate([dx + s,     drum_d/2, 0]) rotate([0,0, r(seed,1,0,360)]) drum();
  translate([dx + 2*s,   drum_d/2, 0]) rotate([0,0, r(seed,2,0,360)]) drum();
}

module mixed_I(seed=9) {
  // small pallet (no load) + box stacks beside
  pal_x = 12; pal_y = 8;
  translate([pal_x/2, pal_y/2, 0]) pallet(x=pal_x, y=pal_y, h=2.2);
  // boxes resting ON the pallet
  translate([3.0, pal_y/2, 2.25])     box(5, 5, 4);
  translate([8.0, pal_y/2, 2.25])     box(4.5, 5, 3.5);
  translate([3.0, pal_y/2, 2.25+4.05]) rotate([0,0,7]) box(4, 4, 2.6);
  // box pile beside the pallet
  translate([pal_x + 3.5, 3.0, 0])      box(6, 5, 4.5);
  translate([pal_x + 3.5, 3.0, 4.55])   rotate([0,0, -6]) box(4.5, 4, 3.0);
  // drum on the end
  translate([pal_x + 6.5 + drum_d/2, drum_d/2, 0])
    rotate([0,0, r(seed,0,0,360)]) drum();
}

module mixed_J(seed=10) {
  // tire stack + bucket + crate + jerry can + drum
  translate([tire_od/2, tire_od/2, 0]) tire_stack(4, seed);
  bd = 4.8;
  translate([tire_od + 0.6 + bd/2, bd/2 + 0.5, 0]) bucket();
  translate([tire_od + 0.6 + bd/2, bd/2 + 0.5, 1.6]) bucket();
  cx = tire_od + 0.6 + bd + 1.0 + 3.5;
  translate([cx, 3.5, 0]) crate(7);
  translate([cx + 5.0, 1.3, 0]) jerrycan(w=4.2, d=2.2, h=4.8);
  translate([cx + 5.0 + 4.2 + 0.6 + drum_d/2, drum_d/2, 0])
    rotate([0,0, r(seed,5,0,360)]) drum();
}

module mixed_K(seed=11) {
  // box stack + drums + crate + tire trio
  translate([3.5, 3.0, 0])          box(7, 5.5, 4);
  translate([3.5, 3.0, 4.05])       rotate([0,0, 5]) box(5, 4.5, 3.0);
  s = drum_d * 1.02;
  dx = 7.5 + drum_d/2;
  translate([dx,     drum_d/2, 0]) rotate([0,0, r(seed,0,0,360)]) drum();
  translate([dx + s, drum_d/2, 0]) rotate([0,0, r(seed,1,0,360)]) drum();
  cx = dx + 2*s + 3.0;
  translate([cx, 3.0, 0]) crate(6);
  // tire trio
  tx = cx + 6.5 + tire_od/2;
  translate([tx,                     tire_od/2, 0]) tire_stack(3, seed+5);
  translate([tx + tire_od*1.01,      tire_od/2, 0]) tire_stack(4, seed+6);
}

module mixed_corner3(seed=22) {
  // pallet anchors the corner; stuff flows out both arms
  pal_x = 13; pal_y = 11;
  translate([pal_x/2, pal_y/2, 0]) pallet(x=pal_x, y=pal_y, h=2.2);
  // 3 crates on the pallet
  translate([3.5, 3.5, 2.25])         crate(5);
  translate([9.0, 3.5, 2.25])         crate(4.5);
  translate([3.5, 8.0, 2.25])         crate(4.5);
  // +X arm past pallet: drums then tire stack
  s = drum_d * 1.02;
  translate([pal_x + 0.5 + drum_d/2,      drum_d/2, 0])
    rotate([0,0, r(seed,0,0,360)]) drum();
  translate([pal_x + 0.5 + drum_d/2 + s,  drum_d/2, 0])
    rotate([0,0, r(seed,1,0,360)]) drum();
  translate([pal_x + 0.5 + 2*s + tire_od/2, tire_od/2, 0])
    tire_stack(4, seed+5);
  // +Y arm past pallet: box pile + drum
  translate([3.0, pal_y + 2.5,     0])    box(6, 5, 4.5);
  translate([3.0, pal_y + 2.5,  4.55])    rotate([0,0, 8]) box(4.5, 4, 3.0);
  translate([drum_d/2, pal_y + 5.5 + drum_d/2, 0])
    rotate([0,0, r(seed,10,0,360)]) drum();
}

// ===========================================================================
// BARRELS-BIG -- dense, deep, irregular corner-fill barrels
// ===========================================================================
// Hex-packed back rows (k%2 offsets X by s/2); random skips + height variation.
module barrels_big_corner(arm_x=5, arm_y=5, max_d=3, seed=30) {
  s = drum_d * 1.02;
  s_back = drum_d * 0.92;
  for (i=[0:arm_x-1]) {
    d_here = max(1, floor(r(seed, i, 1, max_d+0.99)));
    for (k=[0:d_here-1])
      if (r(seed+50, i*10+k) > 0.09) {
        h_mult = (r(seed+60, i*10+k) > 0.86)
          ? r(seed+61, i*10+k, 0.55, 0.78)
          : r(seed+62, i*10+k, 0.88, 1.00);
        translate([drum_d/2 + i*s + (k%2)*s/2, drum_d/2 + k*s_back, 0])
          rotate([0,0, r(seed+i, k, 0, 360)])
            drum(d=drum_d, h=drum_h*h_mult);
      }
  }
  for (j=[1:arm_y-1]) {
    d_here = max(1, floor(r(seed+100, j, 1, max_d+0.99)));
    for (k=[0:d_here-1])
      if (r(seed+150, j*10+k) > 0.09) {
        h_mult = (r(seed+160, j*10+k) > 0.86)
          ? r(seed+161, j*10+k, 0.55, 0.78)
          : r(seed+162, j*10+k, 0.88, 1.00);
        translate([drum_d/2 + k*s_back, drum_d/2 + j*s + (k%2)*s/2, 0])
          rotate([0,0, r(seed+j+200, k, 0, 360)])
            drum(d=drum_d, h=drum_h*h_mult);
      }
  }
}

module barrels_big_row(n=10, max_d=3, seed=31) {
  s = drum_d * 1.02;
  s_back = drum_d * 0.92;
  for (i=[0:n-1]) {
    d_here = max(1, floor(r(seed, i, 1, max_d+0.99)));
    for (k=[0:d_here-1])
      if (r(seed+50, i*10+k) > 0.09) {
        h_mult = (r(seed+60, i*10+k) > 0.86)
          ? r(seed+61, i*10+k, 0.55, 0.78)
          : r(seed+62, i*10+k, 0.88, 1.00);
        translate([drum_d/2 + i*s + (k%2)*s/2, drum_d/2 + k*s_back, 0])
          rotate([0,0, r(seed+i, k, 0, 360)])
            drum(d=drum_d, h=drum_h*h_mult);
      }
  }
}

module barrels_big_pile(w=6, d=4, seed=32) {
  s = drum_d * 1.02;
  s_back = drum_d * 0.92;
  for (i=[0:w-1])
    for (j=[0:d-1])
      if (r(seed+50, i*10+j) > 0.05) {
        h_mult = (r(seed+60, i*10+j) > 0.86)
          ? r(seed+61, i*10+j, 0.55, 0.78)
          : r(seed+62, i*10+j, 0.88, 1.00);
        translate([drum_d/2 + i*s + (j%2)*s/2, drum_d/2 + j*s_back, 0])
          rotate([0,0, r(seed+i, j, 0, 360)])
            drum(d=drum_d, h=drum_h*h_mult);
      }
}

// ===========================================================================
// TIRES-BIG -- big multi-deep tire piles, mixed sizes & heights
// ===========================================================================
// Each column has a single tire size; depth varies per column; height per stack.
module tires_big_cluster(across=7, max_deep=4, seed=40) {
  sizes_x = [for (i=[0:across-1]) pick_tire(seed+100, i)];
  ods_x   = [for (sz=sizes_x) sz[0]];
  for (i=[0:across-1]) {
    sz = sizes_x[i];
    d_here = max(1, floor(r(seed+200, i, 1, max_deep+0.99)));
    x_off = sum_first(ods_x, i) + i*0.30 + sz[0]/2;
    for (k=[0:d_here-1])
      if (r(seed+300, i*10+k) > 0.08) {
        h = max(2, floor(r(seed+500, i*10+k, 2, 7)));
        y_off = sz[0]/2 + k*(sz[0] + 0.30);
        translate([x_off, y_off, 0])
          tire_stack(h, seed+i*10+k,
                     od=sz[0], w=sz[1], id=sz[2]);
      }
  }
}

// ===========================================================================
// SQUARES-BIG -- long box/crate/bin/milk-crate clusters
// ===========================================================================
// Open-top rectangular bin
module bin(w=6, d=5, h=4, wall=0.5) {
  difference() {
    rbox(w, d, h, 0.3);
    translate([0, 0, wall])
      rbox(w-2*wall, d-2*wall, h, 0.2);
  }
}

// Slatted milk crate
module milk_crate(s=5) {
  difference() {
    rbox(s, s, s*0.85, 0.2);
    translate([0, 0, 0.5])
      rbox(s-1.0, s-1.0, s*0.85, 0.15);
    for (zz=[s*0.30, s*0.55])
      for (rot=[0, 90, 180, 270])
        rotate([0,0, rot])
          translate([0, s/2, zz])
            cube([s-1.6, 1.5, s*0.12], center=true);
  }
}

module squares_big_long(seed=50) {
  translate([3,    2.5, 0])    box(6, 5, 4.5);
  translate([3,    2.5, 4.55]) box(4.5, 4, 3);
  translate([9,    3.5, 0])    crate(7);
  translate([9,    3.5, 7.05]) crate(5.5);
  translate([15,   3.0, 0])    bin(6, 5, 5);
  translate([21,   3.0, 0])    box(7, 5.5, 4);
  translate([21,   3.0, 4.05]) box(5.5, 4.5, 3.2);
  translate([28,   3.0, 0])    milk_crate(6);
  translate([34,   3.5, 0])    crate(6.5);
  translate([34,   3.5, 6.55]) box(5, 4, 3);
  translate([40,   2.5, 0])    box(5, 4.5, 4);
  translate([3,    8.0, 0])    box(4.5, 4, 3.5);
  translate([15,   8.0, 0])    crate(5);
  translate([28,   8.5, 0])    bin(5.5, 4.5, 4);
}

module squares_big_pile(seed=51) {
  translate([3,   2.5, 0])    box(7, 5, 4.5);
  translate([3,   2.5, 4.55]) box(5.5, 4.5, 3.2);
  translate([10,  3.5, 0])    crate(7);
  translate([10,  3.5, 7.05]) crate(5.5);
  translate([17,  2.5, 0])    box(6, 5, 4);
  translate([17,  2.5, 4.05]) milk_crate(4.5);
  translate([24,  3.0, 0])    bin(6, 5, 5);
  translate([3,   8.0, 0])    crate(6);
  translate([10,  8.5, 0])    box(5.5, 4.5, 4);
  translate([10,  8.5, 4.05]) box(4, 3.5, 2.8);
  translate([17,  8.0, 0])    milk_crate(5);
  translate([24,  8.0, 0])    box(5, 4, 3.5);
  translate([3,   13.5, 0])   box(4, 3.5, 3);
  translate([17,  13.0, 0])   crate(5);
}

module squares_big_corner(seed=52) {
  translate([3.5,  3.0, 0])    box(6, 5, 4.5);
  translate([3.5,  3.0, 4.55]) box(4.5, 4, 3);
  translate([10,   3.5, 0])    crate(7);
  translate([10,   3.5, 7.05]) crate(5);
  translate([17,   3.0, 0])    bin(6, 5, 5);
  translate([23,   3.0, 0])    milk_crate(6);
  translate([29,   2.5, 0])    box(5, 4.5, 4);
  translate([3.5,  10,   0])   crate(7);
  translate([3.0,  17,   0])   box(6, 5, 4.5);
  translate([3.0,  17, 4.55])  box(4.5, 4, 3);
  translate([3.0,  23.5, 0])   bin(6, 5, 5);
  translate([10,   8.0, 0])    box(5, 4, 3.5);
  translate([17,   8.0, 0])    box(4.5, 4, 3.0);
  translate([8.5,  10,   0])   milk_crate(5);
  translate([8.0,  17.5, 0])   crate(5);
}

// ===========================================================================
// MIXED-BIG -- big multi-type clusters with depth
// ===========================================================================
module mixed_big_wide(seed=60) {
  s = drum_d * 1.02;
  for (i=[0:2])
    translate([drum_d/2 + i*s, drum_d/2, 0])
      rotate([0,0, r(seed,i,0,360)]) drum();
  tx = 3*s + tire_od/2;
  translate([tx, tire_od/2, 0]) tire_stack(5, seed+10);
  cx = tx + tire_od/2 + 4;
  translate([cx, 3.5, 0])    crate(7);
  translate([cx, 3.5, 7.05]) crate(5.5);
  bx = cx + 7.5;
  translate([bx, 3, 0])      box(6, 5, 4.5);
  translate([bx, 3, 4.55])   rotate([0,0, 7]) box(4.5, 4, 3);
  dx = bx + 6 + drum_d/2;
  translate([dx,       drum_d/2, 0]) rotate([0,0, r(seed,5,0,360)]) drum();
  translate([dx + s,   drum_d/2, 0]) rotate([0,0, r(seed,6,0,360)]) drum();
  translate([dx + 2*s + 3, 3, 0]) bin(6, 5, 5);
  // back row partials
  translate([drum_d/2, drum_d/2 + s*0.87, 0])
    rotate([0,0, r(seed,20,0,360)]) drum(d=drum_d, h=drum_h*0.7);
  translate([cx, 3.5+8, 0]) crate(5);
}

module mixed_big_pallet(seed=61) {
  pal_x = 18; pal_y = 13;
  translate([pal_x/2, pal_y/2, 0]) pallet(x=pal_x, y=pal_y, h=2.2);
  translate([4,  3.5, 2.25]) crate(6);
  translate([11, 3.5, 2.25]) crate(6);
  translate([4,  3.5, 8.25]) crate(4.5);
  translate([11, 9,   2.25]) box(6, 5, 4);
  translate([4,  9,   2.25]) box(5, 5, 3.5);
  translate([4,  9,   5.8])  box(4.0, 4.0, 2.8);
  s = drum_d * 1.02;
  for (i=[0:2])
    translate([pal_x + 1 + drum_d/2 + i*s, drum_d/2, 0])
      rotate([0,0, r(seed,i,0,360)]) drum();
  translate([pal_x + 1 + 3*s + tire_od/2, tire_od/2, 0])
    tire_stack(5, seed+5);
  translate([pal_x + 1 + drum_d/2, drum_d/2 + s*0.87, 0])
    rotate([0,0, r(seed,10,0,360)]) drum();
}

module mixed_big_jerry(seed=62) {
  jw=5.2; jd=2.6;
  for (i=[0:3])
    translate([jw/2 + i*(jw+0.2), jd/2, 0])
      rotate([0,0, r(seed,i,-10,10)]) jerrycan();
  bd = 4.8;
  translate([2*jw, jd + 0.6 + bd/2, 0])      bucket();
  translate([2*jw, jd + 0.6 + bd/2, 1.6])    bucket();
  s = drum_d * 1.02;
  dx = 4*(jw+0.2) + 0.5;
  for (i=[0:2])
    translate([dx + drum_d/2 + i*s, drum_d/2, 0])
      rotate([0,0, r(seed,5+i,0,360)]) drum();
  bx = dx + 3*s + 4;
  translate([bx, 3, 0])    box(6, 5, 4.5);
  translate([bx, 3, 4.55]) rotate([0,0, 7]) box(4.5, 4, 3);
  translate([bx + 6.5, 3.5, 0]) crate(6.5);
}

module mixed_big_corner(seed=63) {
  pal_x = 13; pal_y = 13;
  translate([pal_x/2, pal_y/2, 0]) pallet(x=pal_x, y=pal_y, h=2.2);
  translate([3.5, 3.5, 2.25]) crate(5);
  translate([9.0, 3.5, 2.25]) crate(4.5);
  translate([3.5, 9.0, 2.25]) crate(4.5);
  translate([9.0, 9.0, 2.25]) box(5, 4.5, 4);
  s = drum_d * 1.02;
  for (i=[0:2])
    translate([pal_x + 0.5 + drum_d/2 + i*s, drum_d/2, 0])
      rotate([0,0, r(seed,i,0,360)]) drum();
  translate([pal_x + 0.5 + 3*s + tire_od/2, tire_od/2, 0])
    tire_stack(5, seed+5);
  translate([pal_x + 0.5 + drum_d/2, drum_d/2 + drum_d*0.87, 0])
    rotate([0,0, r(seed,10,0,360)]) drum();
  translate([3.0, pal_y + 2.5, 0])    box(6, 5, 4.5);
  translate([3.0, pal_y + 2.5, 4.55]) rotate([0,0, 8]) box(4.5, 4, 3);
  translate([3.5, pal_y + 8.5, 0])    crate(6.5);
  jw=5.2; jd=2.6;
  translate([jw/2,            pal_y + 14, 0]) rotate([0,0, r(seed,15,-10,10)]) jerrycan();
  translate([jw/2 + jw + 0.2, pal_y + 14, 0]) rotate([0,0, r(seed,16,-10,10)]) jerrycan();
}

// ===========================================================================
// WORKSHOP -- iconic shop items (designed for upright print, no bridges >5mm)
// ===========================================================================
module workbench(w=22, d=8, h=12) {
  end_th = 1.0; top_th = 1.2;
  // solid end-walls (not corner legs -- top slab gets full-span support)
  for (sx=[-1,1])
    translate([sx*(w/2 - end_th/2), 0, 0])
      rbox(end_th, d, h - top_th, 0.2);
  // top
  translate([0, 0, h - top_th])
    rbox(w, d, top_th, 0.3);
  // ground stretcher (visual)
  translate([0, 0, 0.5])
    cube([w - 2*end_th - 0.4, d*0.55, 1.0], center=true);
  // vise on top, +X end
  translate([w/2 - 3.5, -d/2 + 2.5, h]) {
    rbox(3, 2.5, 1.8, 0.25);
    translate([0, -1.6, 0.7])
      cube([2.5, 0.6, 1.2], center=true);
  }
  // parts tray on top, -X end
  translate([-w/2 + 4, d/2 - 2, h])
    rbox(4, 2.5, 0.7, 0.2);
}

module compressor(d=8, h=22) {
  cylinder(d=d, h=h*0.75);
  translate([0, 0, h*0.75])
    cylinder(d1=d, d2=d*0.7, h=h*0.08);
  translate([0, 0, h*0.83])
    rbox(d*0.62, d*0.62, h*0.12, 0.3);
  translate([0, 0, h*0.95])
    cylinder(d=d*0.32, h=h*0.05);
}

module floor_jack(L=18, W=6, H=4) {
  rbox(L, W, H, 0.4);
  // saddle near front
  translate([L*0.25, 0, H])
    cylinder(d=2.8, h=0.5);
  translate([L*0.25, 0, H + 0.5])
    cylinder(d=1.7, h=0.3);
  // vertical handle stub at rear
  translate([-L/2 + 0.7, 0, H])
    cylinder(d=0.9, h=H*1.4);
}

module jack_stand(base=4, h=11) {
  // 3 legs sloping inward (taper-up -- prints fine, no overhang accumulation)
  for (a=[0, 120, 240])
    rotate([0,0,a])
      hull() {
        translate([base/2, 0, 0])
          cube([1.0, 1.4, 0.5], center=true);
        translate([0.1, 0, h*0.5])
          cube([0.8, 0.8, 0.5], center=true);
      }
  translate([0, 0, h*0.5])
    cylinder(d=1.0, h=h*0.45);
  translate([0, 0, h*0.95]) {
    rbox(1.8, 1.8, 0.5, 0.2);
    difference() {
      translate([0, 0, 0.5])
        cylinder(d=1.6, h=0.5);
      translate([0, 0, 0.8])
        cube([2, 0.6, 1], center=true);
    }
  }
}

// Combos for the workshop plate
module shop_combo_A(seed=70) {
  workbench(w=22, d=8, h=12);
  translate([-2, 11, 0]) jack_stand(base=3.5, h=10);
  translate([ 3, 11, 0]) jack_stand(base=3.5, h=10);
}

module shop_combo_B(seed=71) {
  compressor(d=8, h=22);
  translate([13, 0, 0]) toolchest();
}

module shop_combo_C(seed=72) {
  floor_jack(L=16, W=5, H=3.5);
  translate([-6, 8, 0]) jack_stand(base=3.5, h=10);
  translate([ 0, 8, 0]) jack_stand(base=3.5, h=10);
  translate([16, 4, 0]) tire_stack(4, seed,   od=11.5, w=3.8, id=4.8);
  translate([16, -5, 0]) tire_stack(3, seed+1, od=11.5, w=3.8, id=4.8);
}

module shop_combo_D(seed=73) {
  workbench(w=18, d=8, h=12);
  translate([16, 0, 0]) compressor(d=8, h=22);
}

// ===========================================================================
// PLATES -- 4 straight variations + 1 corner per type
// ===========================================================================
module plate_barrels() {
  translate([0,    0, 0]) maybe_bond() barrel_row(n=4, seed=1, depth=1);
  translate([0, -22, 0]) maybe_bond() barrel_row(n=5, seed=2, depth=1);
  translate([0, -44, 0]) maybe_bond() barrel_row(n=6, seed=3, depth=2);
  translate([0, -76, 0]) maybe_bond() barrel_row(n=7, seed=4, depth=2);
  translate([0,-115, 0]) maybe_bond() barrel_corner(arm=4, seed=10);
}

module plate_tires() {
  translate([0,    0, 0]) maybe_bond() tires_row([5,3,6,4],   seed=1);
  translate([0, -25, 0]) maybe_bond() tires_row([4,6,3,5,4], seed=2);
  translate([0, -50, 0]) maybe_bond() tires_row([3,4,5,3],   seed=3);
  translate([0, -75, 0]) maybe_bond() tires_and_boxes(seed=4);
  translate([0,-110, 0]) maybe_bond() tires_corner(seed=11);
}

module plate_boxes() {
  translate([0,    0, 0]) maybe_bond() box_row(seed=1, len=4);
  translate([0, -18, 0]) maybe_bond() box_row(seed=2, len=5);
  translate([0, -36, 0]) maybe_bond() box_row(seed=3, len=4);
  translate([0, -54, 0]) maybe_bond() box_row(seed=4, len=5);
  translate([0, -82, 0]) maybe_bond() box_corner(seed=12);
}

module plate_mixed() {
  translate([0,    0, 0]) maybe_bond() mixed_A(seed=1);
  translate([0, -22, 0]) maybe_bond() mixed_B(seed=2);
  translate([0, -44, 0]) maybe_bond() mixed_C(seed=3);
  translate([0, -68, 0]) maybe_bond() mixed_A(seed=4);
  translate([0,-100, 0]) maybe_bond() mixed_corner(seed=20);
}

module plate_mixed2() {
  translate([0,    0, 0]) maybe_bond() mixed_D(seed=4);
  translate([0, -16, 0]) maybe_bond() mixed_E(seed=5);
  translate([0, -34, 0]) maybe_bond() mixed_F(seed=6);
  translate([0, -52, 0]) maybe_bond() mixed_G(seed=7);
  translate([0, -78, 0]) maybe_bond() mixed_corner2(seed=21);
}

module plate_mixed3() {
  translate([0,    0, 0]) maybe_bond() mixed_H(seed=8);
  translate([0, -16, 0]) maybe_bond() mixed_I(seed=9);
  translate([0, -36, 0]) maybe_bond() mixed_J(seed=10);
  translate([0, -56, 0]) maybe_bond() mixed_K(seed=11);
  translate([0, -82, 0]) maybe_bond() mixed_corner3(seed=22);
}

// ---- BIG / WORKSHOP PLATES ------------------------------------------------
module plate_barrels_big() {
  translate([0,    0, 0]) maybe_bond() barrels_big_row(n=10, max_d=3, seed=31);
  translate([0, -42, 0]) maybe_bond() barrels_big_row(n=8,  max_d=2, seed=33);
  translate([0, -72, 0]) maybe_bond() barrels_big_pile(w=6, d=4, seed=32);
  translate([0,-118, 0]) maybe_bond() barrels_big_corner(arm_x=5, arm_y=5, max_d=3, seed=30);
}

module plate_tires_big() {
  translate([0,    0, 0]) maybe_bond() tires_big_cluster(across=7, max_deep=3, seed=40);
  translate([0, -55, 0]) maybe_bond() tires_big_cluster(across=6, max_deep=4, seed=42);
  translate([0,-125, 0]) maybe_bond() tires_big_cluster(across=8, max_deep=2, seed=44);
}

module plate_squares_big() {
  translate([0,    0, 0]) maybe_bond() squares_big_long(seed=50);
  translate([0, -28, 0]) maybe_bond() squares_big_pile(seed=51);
  translate([0, -72, 0]) maybe_bond() squares_big_corner(seed=52);
}

module plate_mixed_big() {
  translate([0,    0, 0]) maybe_bond() mixed_big_wide(seed=60);
  translate([0, -32, 0]) maybe_bond() mixed_big_pallet(seed=61);
  translate([0, -65, 0]) maybe_bond() mixed_big_jerry(seed=62);
  translate([0,-105, 0]) maybe_bond() mixed_big_corner(seed=63);
}

module plate_workshop() {
  translate([0,    0, 0]) maybe_bond() shop_combo_A(seed=70);
  translate([0, -32, 0]) maybe_bond() shop_combo_B(seed=71);
  translate([0, -62, 0]) maybe_bond() shop_combo_C(seed=72);
  translate([0, -92, 0]) maybe_bond() shop_combo_D(seed=73);
}

// ===========================================================================
// DISPATCH
// ===========================================================================
part = "all";

if      (part == "barrels")      plate_barrels();
else if (part == "tires")        plate_tires();
else if (part == "boxes")        plate_boxes();
else if (part == "mixed")        plate_mixed();
else if (part == "mixed2")       plate_mixed2();
else if (part == "mixed3")       plate_mixed3();
else if (part == "barrels-big")  plate_barrels_big();
else if (part == "tires-big")    plate_tires_big();
else if (part == "squares-big")  plate_squares_big();
else if (part == "mixed-big")    plate_mixed_big();
else if (part == "workshop")     plate_workshop();
else if (part == "all") {
  translate([  0, 0, 0]) plate_barrels();
  translate([ 60, 0, 0]) plate_tires();
  translate([130, 0, 0]) plate_boxes();
  translate([200, 0, 0]) plate_mixed();
  translate([270, 0, 0]) plate_mixed2();
  translate([340, 0, 0]) plate_mixed3();
}
