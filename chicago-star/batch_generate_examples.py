#!/usr/bin/env python3
"""
Batch generation examples for the parametric coaster star generator.
Run this to generate multiple coaster variations at once.
"""

from coaster_star_parametric import generate_coaster_star
from pathlib import Path


def main():
    # Create output directory if needed
    output_dir = Path("generated_variants")
    output_dir.mkdir(exist_ok=True)
    
    print("🌟 Generating parametric coaster star variations...\n")
    
    # Define variations to generate
    variations = [
        {
            "name": "slim-modern",
            "width": 100,
            "height": 4,
            "rim_width": 8,
            "strut_width": 0.5,
            "star_points": 8,
            "description": "Elegant modern style with wide rim and minimal struts"
        },
        {
            "name": "balanced-classic",
            "width": 100,
            "height": 4,
            "rim_width": 4,
            "strut_width": 2,
            "star_points": 8,
            "description": "Classic balanced design (original parameters)"
        },
        {
            "name": "bold-substantial",
            "width": 100,
            "height": 4,
            "rim_width": 2.5,
            "strut_width": 3,
            "star_points": 8,
            "description": "Bold, sturdy style with thick struts"
        },
        {
            "name": "large-deluxe",
            "width": 120,
            "height": 5,
            "rim_width": 6,
            "strut_width": 1.5,
            "star_points": 8,
            "description": "Larger coaster with deluxe proportions"
        },
        {
            "name": "pentagram",
            "width": 100,
            "height": 4,
            "rim_width": 5,
            "strut_width": 2,
            "star_points": 5,
            "description": "5-pointed star design"
        },
        {
            "name": "hexagon-star",
            "width": 100,
            "height": 4,
            "rim_width": 4,
            "strut_width": 2,
            "star_points": 6,
            "description": "6-pointed star (hexagon-like)"
        },
    ]
    
    # Generate each variation
    for var in variations:
        print(f"📝 Generating: {var['name']}")
        print(f"   {var['description']}")
        print(f"   Params: {var['width']}×{var['height']}mm, "
              f"rim={var['rim_width']}mm, strut={var['strut_width']}mm")
        
        coaster = generate_coaster_star(
            width=var['width'],
            height=var['height'],
            rim_width=var['rim_width'],
            strut_width=var['strut_width'],
            star_points=var['star_points']
        )
        
        output_file = output_dir / f"coaster-{var['name']}.stl"
        coaster.export(str(output_file))
        
        file_size = output_file.stat().st_size
        print(f"   ✓ {output_file.name} ({file_size:,} bytes)\n")
    
    print(f"✅ Generated {len(variations)} coaster variations in '{output_dir}/'")
    print("\n💡 Try custom parameters with the main script:")
    print("   python coaster_star_parametric.py --width 100 --rim-width 6 --strut-width 1")


if __name__ == "__main__":
    main()
