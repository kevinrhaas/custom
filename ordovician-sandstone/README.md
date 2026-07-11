# Ordovician Sandstone Lamp

Parametric, geology-inspired cylindrical lamp shades that mimic the layered strata of Ordovician-era Illinois sandstone. A Python + OpenSCAD pipeline generates organic forms with full control over height, wall thickness, hollow interior, solid base, and center hole dimensions.

## Overview

The original model is a hand-sculpted polyhedron cylinder with 111 rings of 120 vertices each, capturing a naturalistic sandstone strata surface. The parametric generator reads this source geometry and regenerates it at any target size, interpolating between rings to preserve the organic character.

For connected lamps, use **v4** (`main/generate_sandstone_v4.py`). It retains
every original source ring, preserves the gentle rounded inward-return top lip,
and Boolean-unifies the prepared 80 mm connector with the shell. The 120, 150,
and 180 mm v4 releases are single watertight solids with a continuous interior
floor, eliminating the multipart non-manifold and dashed-rim artifacts in v2.
Earlier generators remain available for compatibility with existing files.

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
│   ├── generate_sandstone.py      # Original parametric generator
│   ├── generate_sandstone_v2.py   # Detail-preserving watertight lamp generator
│   ├── test_generate_sandstone_v2.py
│   ├── generate_sandstone_v4.py   # Single-body connected lamp Boolean generator
│   ├── repair_connector_v4.py     # Prepares the legacy 80 mm connector
│   ├── test_generate_sandstone_v4.py
│   ├── generate_coupon.py         # Transparency test-coupon generator
│   └── archive/                   # Previous generator versions (v1–v4)
├── raw/                           # Original hand-sculpted SCAD source files
├── files/
│   ├── lamp/                      # Generated parametric lamp files (.scad, .stl, .3mf)
│   │   └── nonparametric/         # Earlier non-parametric slicer projects
│   ├── coupon/                    # Filament light-transparency test coupons
│   └── base/                      # Lamp attachment base pieces
└── additional/                    # Extra STL exports and experimental variants
```

## Transparency Test Coupons

Before printing a full 180 mm shade, test how a filament transmits light with a
small, support-free coupon that reproduces the real 2 mm lamp wall and strata
texture. See [`files/coupon/`](files/coupon/) and `main/generate_coupon.py`.

## Usage

```bash
cd ordovician-sandstone/main

# Recommended connected v4 releases (automatically 111L, 139L, and 166L)
python3 -m pip install -r requirements-v4.txt
python3 generate_sandstone_v4.py --height 120
python3 generate_sandstone_v4.py --height 150
python3 generate_sandstone_v4.py --height 180

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

V4 uses `--hole` instead of `--base-hole`, supports `--top-lip-segments`, and
writes STL, 3MF, SCAD, and a validation report into
`files/lamp/v4/connected/` by default. The repaired 80 mm threaded connector
is Boolean-unified unless `--no-connector` is specified. See
`files/lamp/v4/connected/README.md` for the complete v4 preset.

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

The v4 connected releases standardize these at 111L, 139L, and 166L,
respectively, all with a manifold 80 mm connector and 115 mm screw-base
compatibility.

## Recommended screw base

Use `files/base/sandstonelayers-base-v4-smooth-drilled.3mf` with the connected
lamp v4 releases. Base v4 preserves the v3 screw and core geometry, replaces only
the outer body with a tangent-continuous curve into the flat top, and retains
the existing drill/cord mesh as an active Bambu Studio negative part. Regenerate
it with `main/generate_base_v4.py`.

## Tools

- Python 3 (v4 dependencies are pinned in `main/requirements-v4.txt`)
- [OpenSCAD](https://openscad.org/) (for viewing/rendering `.scad` files)
