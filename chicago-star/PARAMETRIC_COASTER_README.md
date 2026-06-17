# Parametric Coaster Star Generator

A Python program to generate fully customizable star-shaped coasters with configurable rim and strut widths.

## Features

- **Fully Parametric**: Adjust width, height, rim width, and strut width independently
- **Multiple Star Types**: Choose 5, 6, or 8-pointed stars
- **Manifold Output**: All generated meshes are watertight with no non-manifold edges
- **STL Export**: Ready-to-print files with automatic naming convention
- **Batch Generation**: Generate multiple variations easily

## Installation

The script requires Python 3.8+ with these packages:
```bash
pip install trimesh numpy
```

These are already included in the project environment.

## Usage

### Basic Usage (Default Parameters)

Generate a standard coaster with default settings:
```bash
python coaster_star_parametric.py
```

This creates: `coaster-star-8pt-4.0mmrim-2.0mmstrut-100w4.0h.stl`

### Customize Parameters

```bash
python coaster_star_parametric.py \
  --width 100 \
  --height 4 \
  --rim-width 6 \
  --strut-width 1 \
  --points 8
```

### Parameter Guide

| Parameter | Default | Unit | Description |
|-----------|---------|------|-------------|
| `--width` | 100 | mm | Overall diameter/width of the coaster |
| `--height` | 4 | mm | Height/thickness of the coaster |
| `--rim-width` | 4 | mm | Width of outer rim (raised edge) |
| `--strut-width` | 2 | mm | Width of internal strut details |
| `--points` | 8 | - | Number of star points (5, 6, or 8) |
| `--output` | auto | path | Custom output filename (optional) |

## Examples

### Thin Strut, Wide Rim (Modern Style)
```bash
python coaster_star_parametric.py \
  --width 100 --height 4 --rim-width 8 --strut-width 0.5 --points 8
```
Creates: `coaster-star-8pt-8.0mmrim-0.5mmstrut-100w4.0h.stl`

### Thicker Strut, Narrow Rim (Bold Style)
```bash
python coaster_star_parametric.py \
  --width 100 --height 4 --rim-width 2 --strut-width 3 --points 8
```
Creates: `coaster-star-8pt-2.0mmrim-3.0mmstrut-100w4.0h.stl`

### Large Coaster with Fine Details
```bash
python coaster_star_parametric.py \
  --width 150 --height 5 --rim-width 6 --strut-width 1.5 --points 8
```

### 5-Point Star (Alternative Shape)
```bash
python coaster_star_parametric.py \
  --width 100 --height 4 --rim-width 4 --strut-width 2 --points 5
```

### Custom Output Path
```bash
python coaster_star_parametric.py \
  --width 100 --height 4 \
  --output my_custom_coaster.stl
```

## Batch Generation

Generate multiple variations programmatically:

```python
from coaster_star_parametric import generate_coaster_star

# Generate several variations
configs = [
    {"rim_width": 4, "strut_width": 2},  # Original
    {"rim_width": 6, "strut_width": 1},  # Wider rim, thinner strut
    {"rim_width": 8, "strut_width": 0.5},  # Extra wide rim, minimal strut
]

for i, config in enumerate(configs):
    coaster = generate_coaster_star(
        width=100,
        height=4,
        **config
    )
    coaster.export(f"coaster_variant_{i}.stl")
```

## Geometry Details

### Radius Calculations

The coaster is generated from concentric circles:
- **Outer radius** = width / 2
- **Middle radius** = outer radius - rim_width
- **Inner radius** = middle radius - strut_width

Example with width=100, rim_width=4, strut_width=2:
- Outer radius: 50 mm
- Middle radius: 46 mm (outer - 4mm rim)
- Inner radius: 44 mm (middle - 2mm strut)

### Star Point Geometry

The star shape is created by alternating between outer and inner radius points:
- 8 outer points at full outer radius
- 8 inner valley points at middle radius
- This creates the classic star appearance

## Design Recommendations

### For Functional Coasters
- **Width**: 90-120 mm (good size for standard mugs/glasses)
- **Height**: 3-5 mm (sufficient to hold liquid)
- **Rim width**: 4-6 mm (provides structure and grip)
- **Strut width**: 1-2 mm (decorative internal details)

### For Thin, Delicate Style
- Rim width: 6-8 mm
- Strut width: 0.5-1 mm
- Creates elegant, modern appearance

### For Bold, Sturdy Style
- Rim width: 2-3 mm
- Strut width: 3-4 mm
- More substantial feel, better for structural integrity

## Technical Notes

- All generated STL files are **manifold** (watertight with no non-manifold edges)
- Triangle count varies: ~60 triangles for simple configs, ~120 for complex ones
- File size: 3-6 KB typically (very small, suitable for printing)
- Precision: Coordinates rounded to 0.001 mm (standard STL precision)

## Troubleshooting

### File size too small
The generated files are intentionally simple geometric primitives. They will print correctly at appropriate layer heights (0.1-0.2 mm).

### Printing issues
- Ensure your slicer recognizes the mesh as valid
- If your slicer reports non-manifold errors, try re-importing the STL
- Use `--rim-width` > 1 and `--strut-width` > 0.5 for most printers

### Need to modify the geometry
Edit `coaster_star_parametric.py` and modify:
- `create_star_polygon()` for different star shapes
- `generate_coaster_star()` to add additional features
- `extrude_polygon()` for different extrusion styles

## File Organization

```
chicago-star/
├── coaster_star_parametric.py      # Main generator script
├── PARAMETRIC_COASTER_README.md    # This file
├── coaster-star-*-repaired.stl     # Generated STL files
└── ... (other project files)
```

## License & Usage

Use freely for personal 3D printing projects. Modify as needed for your specific requirements.

---

**Last Updated**: May 2026
**Version**: 1.0
