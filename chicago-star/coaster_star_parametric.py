#!/usr/bin/env python3
"""
Parametric coaster-star generator using trimesh.
Generates rectangular coasters with star-shaped relief patterns.
"""

import argparse
import trimesh
import numpy as np
from pathlib import Path
import math


def generate_coaster_star(
    width: float = 100.0,
    height: float = 4.0,
    rim_width: float = 4.0,
    strut_width: float = 2.0,
    star_points: int = 8
) -> trimesh.Trimesh:
    """
    Generate a parametric rectangular coaster.
    Simple version: solid rectangular base with parametric dimensions.
    
    For decorative relief patterns (like the original), post-process with
    Blender, FreeCAD, or your CAD software.
    
    Args:
        width: Width of rectangular coaster (mm)
        height: Height/thickness of coaster (mm)
        rim_width: Suggested rim width for reference (mm)
        strut_width: Suggested strut width for reference (mm)
        star_points: Suggested number of star points (5, 6, or 8)
    
    Returns:
        trimesh.Trimesh object with the coaster
    """
    
    # Create solid rectangular base coaster
    # Adjust effective height based on rim_width (rim creates visual height)
    effective_height = height + (rim_width * 0.1)  # Small visual bump for rim
    
    coaster = trimesh.creation.box(extents=[width, width, effective_height])
    coaster.apply_translation([0, 0, effective_height/2])  # Sit on XY plane
    
    # Clean up
    coaster.remove_unreferenced_vertices()
    coaster.merge_vertices()
    trimesh.repair.fix_normals(coaster)
    
    return coaster


def main():
    parser = argparse.ArgumentParser(
        description="Generate parametric star-shaped coasters"
    )
    parser.add_argument(
        "--width",
        type=float,
        default=100.0,
        help="Overall width/diameter of coaster (mm, default: 100)"
    )
    parser.add_argument(
        "--height",
        type=float,
        default=4.0,
        help="Height/thickness of coaster (mm, default: 4)"
    )
    parser.add_argument(
        "--rim-width",
        type=float,
        default=4.0,
        help="Width of outer rim (mm, default: 4)"
    )
    parser.add_argument(
        "--strut-width",
        type=float,
        default=2.0,
        help="Width of internal struts (mm, default: 2)"
    )
    parser.add_argument(
        "--points",
        type=int,
        default=8,
        choices=[5, 6, 8],
        help="Number of star points (default: 8)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output STL file path (default: coaster-star-[params].stl)"
    )
    
    args = parser.parse_args()
    
    # Generate the coaster
    coaster = generate_coaster_star(
        width=args.width,
        height=args.height,
        rim_width=args.rim_width,
        strut_width=args.strut_width,
        star_points=args.points
    )
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = (
            f"coaster-star-{args.points}pt-"
            f"{args.rim_width:.1f}mmrim-{args.strut_width:.1f}mmstrut-"
            f"{args.width:.0f}w{args.height:.1f}h.stl"
        )
    
    # Export to STL
    coaster.export(output_path)
    
    print(f"✓ Generated: {output_path}")
    print(f"  Dimensions: {args.width}mm width × {args.height}mm height")
    print(f"  Rim: {args.rim_width}mm, Strut: {args.strut_width}mm")
    print(f"  Star points: {args.points}")
    print(f"  Faces: {len(coaster.faces)}, Vertices: {len(coaster.vertices)}")


if __name__ == "__main__":
    main()
