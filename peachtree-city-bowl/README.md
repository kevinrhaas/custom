# Peachtree City Bowl

Parametric wavy-rim decorative bowls designed in OpenSCAD — organic, flowing forms with configurable scallops, shimmer textures, and concave interior dishes.

## Overview

A fully parametric bowl generator with control over rim waviness, wall thickness, base radius, scallop patterns, and surface texture. Multiple iterations refine the manifold geometry and visual quality.

### Features

- **Wavy rim** — configurable wave count, amplitude, and height variation
- **Radial scallops** — multiple independent scallop bands (rim, outer, inner)
- **Concave interior dish** — optional curved interior floor
- **Shimmer texture** — subtle outer surface undulations
- **High-resolution mesh** — 220 × 90 default resolution for smooth curves

## Files

### OpenSCAD Source

- `wavy.scad` — First version (degree-correct parametric bowl)
- `wavy-2.scad` — Second iteration
- `wavy-3.scad` — Current version (closed manifold, guaranteed solid base, center cap fix)

### Print-Ready

- `wavy-2.scad.3mf` — Slicer project for wavy v2
- `Meshy_AI_Ruffled Rim Plate_1771629277_generate.3mf` — AI-generated ruffled rim plate variant

### Exports

- `wavy-2.stl` / `wavy-3.stl` — Rendered mesh exports

### Reference

- `ChatGPT Image Feb 20, 2026, 11_30_17 PM.png` — Design concept image

## Key Parameters (wavy-3.scad)

| Parameter | Description | Default |
|-----------|-------------|---------|
| `base_radius` | Outer radius at base (mm) | 35 |
| `height` | Overall bowl height (mm) | 40 |
| `pitch_deg` | Side flare angle (°) | 40 |
| `wall_thickness` | Wall thickness (mm) | 2 |
| `rim_waves` | Number of rim scallops | 3 |
| `rim_z_waves` | Rim height wave count | 3 |
| `rim_z_amp` | Rim height wave amplitude (mm) | 10 |
| `bottom_thickness` | Solid floor thickness (mm) | 0 |

## Tools

- [OpenSCAD](https://openscad.org/)
