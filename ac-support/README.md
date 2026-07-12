# AC screen support insert

This folder contains an ASA-CF production insert and three quick fit gauges for
nominal 20 × 20 × 1 mm square aluminum tube (18 mm nominal inside width).

## Start here

1. Print the three fit gauges in ASA-CF using the same printer/profile as the final part.
2. Test them in an actual cut end of the aluminum tube. Use the largest size that
   seats fully by firm hand pressure without hammering or splitting the tube seam.
3. The production STL is 17.7 mm. If a different gauge wins, change
   `make_insert(17.7)` near the bottom of the generator and rerun it.

Do not assume the nominal 18 mm opening is exact. Powder coat, extrusion tolerance,
internal corner radii, flow calibration, and ASA-CF shrinkage all affect fit.

## Production part dimensions

- Stem: 17.7 × 17.7 mm rounded square
- Stem corner radius: 1.5 mm
- Insertion depth: 40.0 mm
- Flange: 23 × 23 × 3 mm
- Tip lead-in: 1 mm at approximately 45°
- M5 insert pilot: 6.4 mm diameter
- Pocket depth: 10.5 mm from the outside flange face
- Pocket entry chamfer: 0.5 mm at 45°
- Intended insert: M5 × 0.8, 7.1 mm maximum OD × 9.5 mm long, double-knurled brass
- Intended joint screw: M5 × 30 mm flanged button-head hex screw
- Mating-tube clearance hole: 5.5 mm through both walls, centered
- Optional washer: M5, approximately 14.7–15 mm OD × 1–1.5 mm thick

The insert pocket is axial: the screw passes through the full 20 mm width of the
mating square tube and then threads 8.5–9 mm into the heat-set insert when the
optional washer is used.

## Print and installation notes

- Material: black ASA-CF for outdoor UV/heat resistance and added rigidity.
- Use a hardened nozzle because carbon fiber fill is abrasive.
- Orientation: flange flat on the build plate, stem upward.
- Suggested profile: 0.20 mm layers, 6 walls, 6 top/bottom layers, 75–100% infill.
- Use a 5–8 mm brim if needed for ASA bed adhesion.
- Print the insert region solid; wall count matters more than the infill label.
- Install the heat-set insert square and about 0–0.2 mm below the flange face.
- Verify the insert's actual OD with calipers. Generic M5 inserts vary; adjust the
  6.4 mm pilot if the manufacturer recommends a different hole.
- Drill the 5.5 mm mating-tube clearance hole through both walls as one operation
  so the screw remains coaxial with the insert.
- Do not use an M5 × 35 mm screw with this 20 mm tube and 9.5 mm insert; it is
  likely to bottom out before clamping.
- The 17.7 mm stem leaves 5.65 mm of plastic around the 6.4 mm pocket at its
  narrowest section and 32.5 mm behind the 10.5 mm-deep pocket.
- For serviceable retention of the plug inside its tube, add a separate M3
  cross-screw through the aluminum and the solid portion of the stem, well behind
  the 10.5 mm insert pocket.

## Files

- `ac_support_insert_17.7mm_ASA-CF.stl` — production part
- `fit_gauge_17.5mm.stl` — 10 mm-deep fit gauge
- `fit_gauge_17.7mm.stl` — 10 mm-deep fit gauge
- `fit_gauge_17.9mm.stl` — 10 mm-deep fit gauge
- `generate_ac_support_insert.py` — dependency-free (except NumPy) parametric generator

The generator validates closed-manifold topology, positive signed volume, and
overall bounds before writing portable ASCII STL files.
