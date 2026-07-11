# Sandstone Filament Transparency Test Coupons

Small, fast, support-free test pieces for checking how much light a given
filament lets through **before** committing to a full 180 mm sandstone lamp
shade. Each coupon reproduces the *exact* wall the real lamp uses — the true
**2 mm wall thickness** and the true strata texture at the 180 mm lamp's
vertical scale — just cropped to a short section so it prints in minutes.

Generated from the real lamp geometry by
[`../../main/generate_coupon.py`](../../main/generate_coupon.py).

## Files

| File | Shape | Footprint | Height | Wall | Use |
|------|-------|-----------|--------|------|-----|
| `sandstone-transparency-coupon-ring-30mm.stl` | Full ring (mini lamp bottom) | ⌀~100 mm | 30 mm | 2 mm | Set it **over** your light — walls glow all around, exactly like the real lamp. Most representative. |
| `sandstone-transparency-coupon-arc120-30mm.stl` | 120° curved panel | 78 × 27 mm | 30 mm | 2 mm | Even less filament. Stand it **next to** the light as a little glowing tile. |

Both are watertight/manifold and print with **no supports**.

## How to use

1. Slice and print the coupon **in the actual filament you want to test.**
2. Put your light source inside/under the ring (or beside the arc). No need to
   attach anything — the piece can just sit on, next to, or over the light.
3. Judge the glow: how evenly the light diffuses, whether the strata lines read
   nicely when backlit, and whether the color is what you want. If a filament
   looks good on the coupon, it'll look good on the full shade.

## Slicer tips for a meaningful test

- **Match the real print settings.** The whole point is that the 2 mm coupon
  wall transmits light the same way the finished lamp will, so use the wall
  count / line width / layer height you'd use for the real shade.
- **Vase / spiralize mode** works well for the ring (single continuous 2 mm
  wall, no seams, fastest). For the arc, print it upright on its curved edge.
- **Fewer top layers = brighter.** If you're testing pure wall transmission,
  0–2 top layers lets more light through.
- Test more than one filament by printing a coupon of each — they're cheap.

## Regenerating / customizing

```bash
cd ../../main

# Default 30 mm full ring
python3 generate_coupon.py -o ../files/coupon/sandstone-transparency-coupon-ring-30mm

# Taller section, or a thinner wall to preview a brighter glow
python3 generate_coupon.py --coupon-height 40 --wall 1.2

# Curved panel instead of a full ring
python3 generate_coupon.py --arc 120 -o ../files/coupon/sandstone-transparency-coupon-arc120-30mm
```

| Flag | Description | Default |
|------|-------------|---------|
| `--coupon-height` | Height of the coupon (mm) | 30 |
| `--wall` | Wall thickness (mm) | 2.0 (matches the lamp) |
| `--arc` | Make a curved panel spanning N degrees instead of a full ring | *(full ring)* |
| `-o` | Output basename | *(auto-generated)* |
