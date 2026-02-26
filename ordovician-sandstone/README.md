# Ordovician Sandstone Lamp

Parametric, geology-inspired cylindrical lamp shades that mimic the layered strata of Ordovician-era Illinois sandstone. A Python + OpenSCAD pipeline generates organic forms with full control over height, wall thickness, hollow interior, solid base, and center hole dimensions.

## Overview

The original model is a hand-sculpted polyhedron cylinder with 111 rings of 120 vertices each, capturing a naturalistic sandstone strata surface. The parametric generator reads this source geometry and regenerates it at any target size, interpolating between rings to preserve the organic character.

### Features

- **Height control** — scale to any height (default 120 mm)
- **Strata layer count** — adjust ring density for finer or coarser layering
- **Hollow mode** — configurable wall thickness for lamp shade use
- **Solid base** — optional floor with precise height control
- **Base hole** — center hole for lamp hardware pass-through
- **Dual output** — generates both `.scad` (parametric source) and `.stl` (print-ready mesh)

## Directory Structure

```
ordovician-sandstone/
├── main/
│   ├── generate_sandstone.py      # Parametric generator (current version)
│   └── archive/                   # Previous generator versions (v1–v4)
├── raw/                           # Original hand-sculpted SCAD source files
├── files/
│   ├── lamp/                      # Generated parametric lamp files (.scad, .stl, .3mf)
│   │   └── nonparametric/         # Earlier non-parametric slicer projects
│   └── base/                      # Lamp attachment base pieces
└── additional/                    # Extra STL exports and experimental variants
```

## Usage

```bash
cd ordovician-sandstone/main

# Default — recreate original (120mm, 111 layers)
python3 generate_sandstone.py

# Taller lamp shade
python3 generate_sandstone.py --height 180

# Hollow with 2mm wall, solid base, and 79mm center hole
python3 generate_sandstone.py --wall 2 --base 9.46 --base-hole 79

# Thin wall (1mm) variant
python3 generate_sandstone.py --height 120 --wall 1 --base 9.46 --base-hole 79

# Custom strata density
python3 generate_sandstone.py --height 150 --layers 200

# Scale by percentage
python3 generate_sandstone.py --height-percent 150
```

### Key Parameters

| Flag | Description | Default |
|------|-------------|---------|
| `--height` | Target height in mm | 120 |
| `--layers` | Number of strata ring layers | 111 |
| `--wall` | Wall thickness in mm (enables hollow) | *(solid)* |
| `--base` | Solid base floor height in mm | *(none)* |
| `--base-hole` | Center hole diameter in mm | *(none)* |
| `--height-percent` | Height as percentage of baseline | 100 |
| `--height-scale` | Height as scale factor | 1.0 |
| `-o` | Output filename | *(auto-generated)* |

## Generated File Naming

Files are auto-named with their parameters:

```
illinois_sandstone_parametric_<height>mm_<layers>L_wall<wall>_base<base>_hole<hole>.scad
illinois_sandstone_parametric_<height>mm_<layers>L_wall<wall>_base<base>_hole<hole>.stl
```

## Pre-Generated Sizes

The `files/lamp/` directory includes ready-to-print files for:

- **120mm** — original size (110L and 111L variants, wall 1–2mm)
- **150mm** — medium tall (138L, wall 2mm)
- **180mm** — tall (165–166L, wall 2mm, with/without base hole)

## Tools

- Python 3 (no external dependencies)
- [OpenSCAD](https://openscad.org/) (for viewing/rendering `.scad` files)
