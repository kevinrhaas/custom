# Custom 3D Print Projects

A collection of original, custom-designed 3D-printable models — spanning decorative art, functional household parts, and organizational tools. All models are designed for FDM printing.

## Live site

A garden-themed landing page and the interactive **Hosta Gangway Guide** are published via GitHub Pages from the [`site/`](site/) folder:

- **Landing:** `https://kevinrhaas.github.io/custom/`
- **Hosta guide:** `https://kevinrhaas.github.io/custom/hosta/`
- **Porchfest Planner:** `https://kevinrhaas.github.io/custom/porchfest/`
- **Wau-Bun:** `https://kevinrhaas.github.io/custom/wau-bun/`

The published site is only the `site/` folder (curated web content) — the CAD source in the project folders stays in the repo but out of the deploy. See [`site/`](site/) and `.github/workflows/deploy.yml`. Not part of the Polecat app fleet, but it follows the platform's static-first / aurora-backdrop / light-dark conventions. The Hosta app is generated from `hosta/hosta_gangway_guide_v3.html` by `hosta/build_app.py`.

## Projects

| Project | Description |
|---------|-------------|
| [alligator-chess](alligator-chess/) | “Tomorrowland Alligators” — six support-free, mid-century modern alligator chess pieces with pure-Python STL source |
| [bamboo-vase](bamboo-vase/) | Parametric "Wave Ring" fluted vase for lucky bamboo — six variants + centering collar, pure-Python STL generator |
| [chicago-star](chicago-star/) | Chicago flag six-pointed star coasters and mesh art pieces, modeled in Blender |
| [garage](garage/) | Custom garage door header trim pieces, modeled in Blender |
| [gridfinity-rationell](gridfinity-rationell/) | Gridfinity adapter for IKEA Rationell drawer organizers |
| [ordovician-sandstone](ordovician-sandstone/) | Parametric sandstone strata lamp shade generator — organic geology-inspired cylindrical forms with a Python/OpenSCAD pipeline |
| [peachtree-city-bowl](peachtree-city-bowl/) | Parametric wavy-rim decorative bowl designed in OpenSCAD |
| [porchfest](porchfest/) | Uptown Porchfest 2026 walking-route planner — 91 bands rated across ten dimensions, an orienteering solver over the real street grid, self-contained map, and shareable plans. Builds `site/porchfest/app/` |
| [pentaho](pentaho/) | Pentaho logo 3D prints, modeled in Blender from SVG source |
| [wau-bun](site/wau-bun/) | Juliette Kinzie's 1856 frontier memoir as an interactive telling — a character-presence chart of every person against every scene, a scene-by-scene reader carrying the summary, the modernized text and the original 1856 text, and the full cast. Part 1 (Journey West, 1830–31) is complete |

## File Formats

- **`.blend` / `.blend1`** — Blender source files
- **`.scad`** — OpenSCAD parametric source files
- **`.stl`** — Mesh files for slicing
- **`.3mf`** — 3MF project files (may include slicer settings)
- **`.svg`** — Vector source artwork
- **`.py`** — Python generator scripts

## Tools Used

- [Blender](https://www.blender.org/) — 3D modeling
- [OpenSCAD](https://openscad.org/) — Parametric/programmatic CAD
- [Python 3](https://www.python.org/) — Code generation pipelines
- [OrcaSlicer](https://github.com/SoftFever/OrcaSlicer) / [Bambu Studio](https://bambulab.com/en/download/studio) — Slicing & print profiles
