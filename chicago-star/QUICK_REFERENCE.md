# Parametric Coaster Generator - Quick Reference

## One-Liner Commands

### Default Configuration
```bash
python coaster_star_parametric.py
```
Generates: 100mm width, 4mm height, 4mm rim, 2mm strut, 8-point star

### Popular Presets

#### Modern/Elegant (Wide Rim, Thin Strut)
```bash
python coaster_star_parametric.py --rim-width 8 --strut-width 0.5
```

#### Bold/Sturdy (Narrow Rim, Thick Strut)
```bash
python coaster_star_parametric.py --rim-width 2.5 --strut-width 3
```

#### Larger Coaster
```bash
python coaster_star_parametric.py --width 120 --height 5
```

#### 5-Point Star
```bash
python coaster_star_parametric.py --points 5
```

#### 6-Point Star
```bash
python coaster_star_parametric.py --points 6
```

### Custom Combinations
```bash
python coaster_star_parametric.py --width 110 --height 3.5 --rim-width 5 --strut-width 1.5 --points 8
```

### Save with Custom Name
```bash
python coaster_star_parametric.py --output my_coaster.stl
```

## Parameter Ranges

| Parameter | Min | Recommended | Default | Max |
|-----------|-----|-------------|---------|-----|
| width | 50 | 90-120 | 100 | 200 |
| height | 2 | 3-5 | 4 | 10 |
| rim-width | 1 | 4-6 | 4 | 20 |
| strut-width | 0.5 | 1-3 | 2 | 10 |
| points | 5 | 8 | 8 | 8 |

## Batch Generation

Generate multiple variations at once:
```bash
python batch_generate_examples.py
```
Creates 6 different styles in `generated_variants/` directory:
- slim-modern (elegant)
- balanced-classic (original)
- bold-substantial (sturdy)
- large-deluxe (spacious)
- pentagram (5-point)
- hexagon-star (6-point)

## Common Use Cases

### Drinking Glass Coasters
```bash
python coaster_star_parametric.py --width 100 --height 4 --rim-width 4 --strut-width 2
```

### Mug Coasters (Larger)
```bash
python coaster_star_parametric.py --width 110 --height 4 --rim-width 5 --strut-width 1.5
```

### Coffee Cup Coasters (Smaller)
```bash
python coaster_star_parametric.py --width 85 --height 3 --rim-width 3 --strut-width 1.5
```

### Decorative (Thin, Elegant)
```bash
python coaster_star_parametric.py --width 120 --height 2 --rim-width 8 --strut-width 0.5
```

### Industrial (Thick, Bold)
```bash
python coaster_star_parametric.py --width 100 --height 6 --rim-width 3 --strut-width 4
```

## File Naming Convention

Generated files follow this pattern:
```
coaster-star-{POINTS}pt-{RIM}mmrim-{STRUT}mmstrut-{WIDTH}w{HEIGHT}h.stl
```

Example: `coaster-star-8pt-4.0mmrim-2.0mmstrut-100w4.0h.stl`
- 8-point star
- 4mm rim
- 2mm strut
- 100mm width
- 4mm height

## Tips & Tricks

### For 3D Printing
- **Minimum strut width**: 0.8mm (below this may fail)
- **Optimal layer height**: 0.1-0.2mm
- **Support**: Usually not needed for coasters
- **Infill**: 100% recommended for structural integrity

### Design Tips
- Wider rim = more structural integrity
- Thinner strut = more delicate, modern look
- 5-point star = bold geometric style
- 8-point star = classic, balanced look

### Customization
Edit `coaster_star_parametric.py` to:
- Add custom shapes (octagon, circle, etc.)
- Add embedded patterns or text
- Change star geometry (points depth, etc.)
- Add beveled edges

## Troubleshooting

**Q: My slicer says "non-manifold edges"**
A: Re-import the STL file. If issue persists, increase `--rim-width` to > 1.5mm

**Q: Model looks too thin**
A: This is normal - coasters are thin by design. Increase `--height` to 5-6mm for more material

**Q: Can't generate with very small parameters**
A: Keep `--strut-width` > 0.5mm and `--rim-width` > 1mm for reliable results

**Q: Want different star shape**
A: Modify `coaster_star_parametric.py` - change `create_star_polygon()` function

## Next Steps

1. **Test Print**: Generate with default settings and test print
2. **Iterate**: Adjust rim-width and strut-width based on results
3. **Batch Produce**: Use `batch_generate_examples.py` to create variants
4. **Customize**: Modify script for your specific needs

---

**Version**: 1.0 | **Last Updated**: May 2026
