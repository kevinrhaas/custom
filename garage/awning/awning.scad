// ===========================================================================
// Garage baby-diorama AWNING / coping cap with under-mount LED channel
// Parametric. Units = mm. Print upside-down (roof face on plate).
//
// Cross-section lives in X-Y; the run length goes along Z.
//   X  = across the wall.  X<0 = OVERHANG side (over the cars / inner face).
//                          X>0 = OUTER / back side (wall's outer face).
//   Y  = vertical. Y=0 is the top of the wall.
//   Z  = along the length of the wall.
//
// Build one part at a time with:  -D 'part="straight"'  ("corner" / "endcap")
// ===========================================================================

part          = "straight";   // "straight"(main) | "center"(over cap) | "corner" | "endcap"
hand          = "R";          // for endcap only: "R" or "L" (the two ends of the L)

/* [ Wall fit -- from your measurements ] */
wall_thk      = 10.0;  // wall top thickness the cap slides over
chan_clear    = 0.4;   // slip clearance added to the channel slot
chan_wall     = 2.0;   // thickness of the skirts that grip each wall face
chan_depth    = 7.0;   // how far the INNER (car-side) skirt hangs down
back_skirt    = 15.0;  // how far the REAR skirt wraps down the back to grip the wall

/* [ Raised center cap (the "top notch") ] */
cap_h         = 10.0;  // how far the center cap rises above the main coping
cap_w         = 100.0; // length of the raised cap along the wall
cap_clear     = 1.0;   // gap left above the cap inside the roof cavity

/* [ Awning geometry ] */
overhang      = 15.0;  // roof projection inward over the cars
oh_under      = 2.0;   // overhang underside drop below the wall top
fascia_drop   = 4.0;   // front lip total drop below wall top (the LED shield)
lip_t         = 1.5;   // thickness of the front shield lip
roof_t        = 2.0;   // roof thickness above the highest point (the cap)
pitch_deg     = 7;     // roof pitch (slopes down toward the front)

/* [ LED cove (front edge, opens DOWN, hidden behind the fascia lip) ] */
led_w         = 10.0;  // groove width  (8 mm strip + slack)
led_d         = 3.0;   // recess depth (up into the overhang)

/* [ Roof panel look ] */
roof_style    = "corr"; // "seam" | "corr" | "flat"  -- corr is the printed/chosen look
rib_pitch     = 10.0;  // standing-seam rib spacing ALONG the wall length
seam_w        = 1.6;   // standing-seam rib width
seam_h        = 1.4;   // standing-seam rib height
corr_r        = 1.6;   // corrugation ridge radius
corr_pitch    = 4.0;   // corrugation ridge spacing ALONG the wall length
corr_sink     = 0.4;   // how far the ridge centre sits below the roof surface
panel_break   = 0;     // transverse panel line every N mm (0=off)

/* [ Segments ] */
seg_len       = 100;   // length of a main straight piece (multiple of rib_pitch)
center_len    = 100;   // length of the center piece (= cap_w)

/* [ Corner (inside 90 deg) ] */
corner_leg    = 45;    // length of each leg past the corner

/* [ Plexi end cap -- wraps the open end, captures the SIDE plexiglass ] */
glue_seat        = 8.0;   // length seated on the wall end (channel grips + glue here)
plexi_thk        = 2.0;   // SIDE plexiglass thickness            (measured ~1.8-2)
plexi_cl         = 0.6;   // slot clearance around the plexi
plexi_rise       = 9.0;   // how far the plexi stands ABOVE the wall top (measured ~9)
plexi_seat       = 4.0;   // (legacy) -- groove now clears plexi_rise instead
side_fascia_t    = 3.0;   // thickness of the outboard side-fascia wall
side_fascia_drop = 15.0;  // side wall hangs the SAME depth as the back wall (= back_skirt)
endcap_t      = 2.0;   // (legacy flat closeout thickness, unused by plexi cap)

/* [ Front plexi relief -- OFF: no plexi along the front runs, only at the end caps ] */
front_relief  = false; // straight + center have NO relief (locked, do not change)
fr_x0         = -2.5;  // (unused while front_relief=false)
fr_x1         =  3.0;

/* [ render ] */
$fn = 48;
eps = 0.02;
BIG = 1000;

// --- derived ----------------------------------------------------------------
cw   = chan_wall;
ci   = wall_thk + chan_clear;          // channel slot inner width
xin  = -overhang;                      // front lip X (over the cars)
xout =  ci + cw;                       // back-most X (outer skirt)
run  =  xout - xin;
// roof top is pinned at the inner wall face (x=0) just high enough to clear the
// raised cap, then pitched down to the front. This keeps a straight, level
// roofline that runs ABOVE the 10 mm center cap along the whole length.
roof_at_x0  = cap_h + cap_clear + roof_t;
roof_back_y = roof_at_x0 + xout*tan(pitch_deg);
roof_front_y = roof_at_x0 - overhang*tan(pitch_deg);

// ============================================================================
// 2D cross-section of the cap (no LED groove; that is cut in 3D)
// rest_y = height of the pocket ceiling that bears on the wall:
//   0      -> main pieces (sit on the normal coping)
//   cap_h  -> center piece (sits on top of the raised cap)
module cross_section(rest_y=0) {
  polygon(points=[
    [xout,        roof_back_y],   // top outer (high)
    [xin,         roof_front_y],  // top front (low)  -- roof slope
    [xin,        -fascia_drop],   // down the front fascia (shield)
    [xin+lip_t,  -fascia_drop],   // bottom of the shield lip
    [xin+lip_t,  -oh_under],      // up to the overhang underside
    [-cw,        -oh_under],      // underside back to inner skirt
    [-cw,        -chan_depth],    // inner skirt down
    [0,          -chan_depth],    // across
    [0,           rest_y],        // up channel inner wall to the bearing ceiling
    [ci,          rest_y],        // pocket ceiling (bears on wall / cap top)
    [ci,         -back_skirt],    // down channel outer wall (deep rear grip)
    [xout,       -back_skirt],    // rear skirt bottom -> wraps the wall like a cap
  ]);
}

module base_solid(len, rest_y=0) { linear_extrude(height=len) cross_section(rest_y); }

module led_groove(len) {
  // downward-opening pocket just behind the front shield lip
  gx0 = xin + lip_t;
  translate([gx0, -oh_under - eps, -eps]) cube([led_w, led_d + eps, len + 2*eps]);
}

// ribs sit ON the sloped roof plane -----------------------------------------
module rib_bar(len) {
  if (roof_style == "seam")
    rotate([90,0,0]) linear_extrude(height=seam_w, center=true)
      polygon([[0,0],[len,0],[len,seam_h*0.6],[len-seam_h,seam_h],
               [seam_h,seam_h],[0,seam_h*0.6]]);
  else if (roof_style == "corr")
    rotate([0,90,0]) cylinder(h=len, r=corr_r);
}

module roof_texture(len) {
  if (roof_style != "flat")
    translate([xin, roof_front_y, 0]) rotate([0,0,pitch_deg]) {
      slope_len = run/cos(pitch_deg);          // overshoot; clipped flush later
      sp = (roof_style=="corr") ? corr_pitch : rib_pitch;
      off = (roof_style=="corr") ? -corr_sink : 0;
      n = floor(len/sp);
      for (i=[0:n]) {
        z = i*sp + sp/2;
        if (z < len)
          translate([0, off, z]) rib_bar(slope_len + corr_r*2);
      }
    }
}

// the same panel style continues DOWN the front fascia (toward the cars),
// aligned with the roof ribs so the sheet looks folded over the front edge
module fascia_rib(h) {
  if (roof_style == "corr")
    translate([xin+corr_sink, -fascia_drop, 0]) rotate([-90,0,0]) cylinder(h=h, r=corr_r);
  else if (roof_style == "seam")
    translate([xin-seam_h, -fascia_drop, -seam_w/2]) cube([seam_h+0.6, h, seam_w]);
}
module fascia_texture(len) {
  if (roof_style != "flat") {
    h  = roof_front_y + fascia_drop;          // fascia face height
    sp = (roof_style=="corr") ? corr_pitch : rib_pitch;
    n  = floor(len/sp);
    for (i=[0:n]) { z = i*sp + sp/2; if (z < len) translate([0,0,z]) fascia_rib(h); }
  }
}

// full-length relief so the awning clears the proud front plexi (runs along Z)
module front_plexi_relief(len) {
  translate([fr_x0, -oh_under - eps, -eps])
    cube([fr_x1 - fr_x0, (plexi_rise + plexi_cl) + oh_under + eps, len + 2*eps]);
}

module straight_raw(len, rest_y=0) {
  difference() {
    union() {
      base_solid(len, rest_y);
      // clip the ribs to the roof footprint so their ends finish flush
      // with the front fascia / back face (no protruding round "log ends")
      intersection() {
        roof_texture(len);
        translate([xin, -chan_depth-50, -1]) cube([run, 200, len+2]);
      }
      fascia_texture(len);   // continue the panel style down the front face
    }
    led_groove(len);
    if (front_relief) front_plexi_relief(len);
  }
}

module straight() { straight_raw(seg_len, 0); }       // main piece, sits on coping
module center()   { straight_raw(center_len, cap_h); } // center piece, sits on cap top

// --- inside 90-degree corner -----------------------------------------------
// keep the half-space Z >= X (plane Z=X through origin, 45 deg about Y).
// `over` extends it slightly past the miter so the mirrored leg overlaps
// instead of sharing a coincident plane (keeps the union manifold).
miter_over = 0.6;
// z>=0 half-space rotated so its boundary becomes the plane Z=X (normal (-1,0,1)).
// Extended by miter_over so the mirrored leg overlaps -> manifold union.
module keep_ZX()
  rotate([0,-45,0]) translate([-BIG/2,-BIG/2,-miter_over]) cube([BIG,BIG,BIG]);

// INSIDE corner: the awning roof must slope DOWN toward the concave corner, so
// the overhang/front lip faces INWARD (over the cars in the L). Each leg's
// cross-section is therefore flipped in X (mirror) so the overhang points +X.
// keep_ZX's miter_over makes the two legs overlap a hair at the X=Z seam, so the
// union is manifold without any off-plane nudge (survives reflection cleanly).
// Each leg also reaches `corner_back` mm PAST the corner so the two legs overlap
// and fill the outer/back corner square (the wall junction) -- no open notch, the
// corrugated roof carries continuously across the whole corner.
corner_back = 16;

/* [ Wire pass-through -- corner only: 10 mm round drill, FRONT-to-REAR through Wall B ] */
wire_hole = true;
wire_d    = 10.0;   // 10 mm round drill hole (see-through)
wire_pos  = 12.0;   // position along the Wall B leg from the corner (near the corner).
                    // Bit edge = wire_pos-5 = 7; must stay > the drill's max z (6) so
                    // it never reaches leg A (leg A exists only where z>=x).
wire_cy   = 0.0;    // center height (at the wall top, opening into the channel)

// 10 mm round CORD hole for the rear LED/power assembly. Enters the REAR of Wall B
// (the exterior/back skirt), passes through the channel AND the inner/middle wall,
// and opens into the LED COVE (z~3.5..13.5) so the wire reaches the strip. STOPS at
// z=6 -> well before the front fascia (z=15), which stays solid/covered on BOTH legs,
// and the 10 mm bit clears Wall A's overhang entirely (no stray notch at the corner).
module wire_tunnel()
  translate([wire_pos, wire_cy, -25]) cylinder(d=wire_d, h=31, $fn=64);  // z: -25 .. 6

module corner() {
  difference() {
    union() {
      legA();                                // wall along +Z, overhang toward +X (inside)
      mirror([1,0,-1]) legA();               // wall along +X, overhang toward +Z (inside)
    }
    if (wire_hole) wire_tunnel();
  }
  module legA() intersection() {
    mirror([1,0,0]) translate([0,0,-corner_back]) straight_raw(corner_leg + corner_back, 0);
    keep_ZX();
  }
}

// --- plexi end cap: wraps the open end of a run in corrugated metal ---------
// Length runs along Z:
//   [0 .. glue_seat]      : full channel profile, seats on the wall end (glue here)
//   [glue_seat .. ec_len] : solid roof cantilever past the wall, over the side plexi
//   far end (side_fascia_t): the SIDE FASCIA wall, hangs down to cover the plexi
//   a groove just inboard of the fascia receives the plexi top edge.
slot   = plexi_thk + plexi_cl;            // Z-width of the plexi groove
ec_len = glue_seat + slot + side_fascia_t;

// solid roof slab. Front underside at -oh_under; the BACK carries a full-depth
// back wall (down to -back_skirt) so the rear wall is CONTINUOUS the whole length.
module roof_body(len)
  linear_extrude(height=len)
    polygon([[xout,roof_back_y],[xin,roof_front_y],[xin,-oh_under],
             [ci,-oh_under],[ci,-back_skirt],[xout,-back_skirt]]);

// the side fascia continues that slab DOWN to cover the side plexi
module fascia_drop(len)
  linear_extrude(height=len)
    polygon([[xout,-oh_under],[xin,-oh_under],[xin,-side_fascia_drop],[xout,-side_fascia_drop]]);

// vertical corrugation ribs on the outboard end face (so the side reads as metal)
module side_fascia_ribs() {
  if (roof_style != "flat") {
    yb = -side_fascia_drop; yt = roof_front_y;
    sp = (roof_style=="corr") ? corr_pitch : rib_pitch;
    n  = floor((xout - xin)/sp);
    for (i=[0:n]) {
      x = xin + i*sp + sp/2;
      if (x < xout)
        translate([x, yb, ec_len - corr_sink]) rotate([-90,0,0]) {
          if (roof_style=="corr") cylinder(h=yt-yb, r=corr_r);
          else translate([-seam_w/2,0,0]) cube([seam_w, yt-yb, seam_h]);
        }
    }
  }
}

module endcap() {
  difference() {
    union() {
      // A: seat on the wall (full channel) with the LED cove
      difference() { base_solid(glue_seat,0); led_groove(glue_seat); }
      // B: roof cantilever out over the plexi
      translate([0,0,glue_seat]) roof_body(ec_len - glue_seat);
      // C: side fascia wall hanging down at the far end
      translate([0,0,ec_len - side_fascia_t]) fascia_drop(side_fascia_t);
      // corrugated skin on the top + front, full length, clipped flush
      intersection() {
        roof_texture(ec_len);
        translate([xin, -side_fascia_drop-1, -1]) cube([run, 200, ec_len+2]);
      }
      fascia_texture(ec_len);
      side_fascia_ribs();
    }
    // plexi clearance RECESS -- a pocket cut up into the underside (NOT through the
    // roof, so the roof top stays continuous). Stops at x=ci so the rear wall is solid.
    gz0 = ec_len - side_fascia_t - slot;
    relief_top = plexi_rise + plexi_cl;                 // recess ceiling, below the roof top
    translate([xin-1, -oh_under - eps, gz0])
      cube([ci - xin + 1, relief_top + oh_under + eps, slot]);
  }
}

// ============================================================================
if (part == "straight") straight();
else if (part == "center") center();
else if (part == "corner") corner();
else if (part == "endcap") {
  if (hand == "L") mirror([0,0,1]) endcap();   // opposite end of the L
  else endcap();
}
