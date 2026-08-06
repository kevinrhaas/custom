#!/usr/bin/env python3
"""The reference photograph, reduced to numbers.

The target is a product shot of a faceted olive knight, 1232x1232, lit from
above, shown at the yaw and elevation solved into CAMERA below. Everything below
was read off that image and normalised against the piece's own bounding box,
so it can be compared against a render at any size:

    u = (px - 298) / 628      0 = leftmost point (the muzzle), 1 = rightmost
    v = (py - 130) / 1038     0 = crown, 1 = the bottom of the plinth

``SILHOUETTE`` is the outline: left and right edge at twenty heights.
``LANDMARKS`` are the features that have to land in the right place.
``TOLERANCE`` is what counts as a match — 2.5% of the piece height, about
1.5 mm on the real object.
"""

# The camera the reference was shot from. Solved from the outline: the piece's
# width-to-height ratio pins the yaw once the plinth diameter is fixed, and the
# squash of the plinth ellipse pins the elevation.
CAMERA = {"yaw": 45.0, "elev": 5.0, "dist": 420.0, "fov": 13.5}
ASPECT = 628 / 1038          # bounding box width / height

# Absolute scale. The normalised outline table above cannot see a uniform error
# — a muzzle that is too long just rescales u and every row still agrees — so
# these are checked separately, in millimetres, PROJECTED at CAMERA (not in
# object space: at 45 deg of yaw the muzzle is foreshortened by cos 45).
HEIGHT_MM = 60.0                            # the piece, crown to plinth
SPAN_MM = 34.2 * 628 / 592                  # 36.30: outline width at that height
REACH_IN_PLINTH_RADII = 1.12                # muzzle tip / plinth radius, projected

# v, u_left, u_right — read band by band off the photograph
SILHOUETTE = [
    (0.019, 0.417, 0.672),
    (0.067, 0.290, 0.783),
    (0.116, 0.154, 0.847),
    (0.164, 0.043, 0.871),
    (0.212, 0.003, 0.882),
    (0.260, 0.322, 0.905),
    (0.308, 0.274, 0.914),
    (0.356, 0.242, 0.920),
    (0.405, 0.221, 0.927),
    (0.453, 0.205, 0.933),
    (0.501, 0.193, 0.939),
    (0.549, 0.182, 0.946),
    (0.597, 0.172, 0.952),
    (0.645, 0.162, 0.955),
    (0.694, 0.153, 0.959),
    (0.742, 0.123, 0.971),
    (0.790, 0.091, 0.982),
    (0.838, 0.075, 0.989),
    (0.886, 0.064, 0.995),
    (0.934, 0.057, 0.998),
]

# name -> (u, v) of the feature's defining corner in the reference
LANDMARKS = {
    "muzzle_tip": (0.003, 0.226),        # leftmost point, the lower lip
    "muzzle_underside": (0.010, 0.245),  # where the muzzle outline turns back
    "nose_top": (0.043, 0.164),          # top of the nose's front facet
    "crown": (0.560, 0.000),             # highest point of the skull
    "ear_notch": (0.700, 0.058),         # the step behind the ear
    "jaw_notch": (0.322, 0.262),         # where the jaw meets the throat
    "mane_tooth_1": (0.828, 0.098),
    "mane_tooth_2": (0.887, 0.199),
    "mane_tooth_3": (0.924, 0.310),
    "mane_tooth_4": (0.951, 0.419),
    "mane_tooth_5": (0.967, 0.525),
    "plinth_top": (0.500, 0.742),        # where the figure leaves the plinth
    "plinth_step": (0.500, 0.895),       # the flange step near the bottom
}

TOLERANCE = 0.025

# Qualities the outline numbers cannot capture, checked by eye against the
# photograph. Kept here so the critic and the generator argue about one list.
FEATURE_CHECKLIST = [
    "five mane teeth, each a wedge with a sloping top face and a sharp notch",
    "a long straight top plane running nose to brow with one nostril break",
    "the lower lip leads the nose: the chin is the most forward point",
    "a thin lip-line crease along the muzzle, not a gaping slot",
    "a triangular eye recess sunk under a hard brow ridge",
    "a hard step where the narrow head meets the wider neck (the jowl)",
    "an angular panel crease on the chest",
    "a 16-sided plinth with a vertical bottom flange, a stepped drum and a "
    "collar, every step facing up",
    "every surface planar, every crease a hard edge, no smoothing anywhere",
]
