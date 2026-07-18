# V2 Liner — original zen-classic bamboo vase (PETG)

A watertight drop-in liner cup for the **original zen-classic** vase, redesigned
from the v1 liner:

- **No flange/lip** — plain straight-walled cup.
- **Flush** — comes up to the rim (0.5 mm below), not proud of it.
- **Thick walls** for a 0.6 mm nozzle so it actually seals.

`liner-zen-classic-v2-petg.stl` — generate/tweak with `python3 generate_liner_v2.py`.

## Fit (to the original zen-classic — measured from the printed 3mf)

| | Value |
|---|---|
| Vase interior bore | 105.0 mm |
| Vase cavity depth (floor→rim) | 126 mm |
| **Liner OD** | **103.5 mm** (~0.75 mm/side slip fit) |
| **Liner height** | **125.5 mm** (rests on floor, top 0.5 mm below rim) |
| Liner ID | 97.5 mm |
| Wall / floor | 3.0 mm / 3.6 mm |
| Capacity | ~0.9 L |

Drop it in, top sits flush with the rim; the bamboo bunch + beads go inside the
liner. Prints upright, open end up, **no supports**.

## Print settings for watertight (from your wave-gentle PETG success)

These are the settings that sealed the wave-gentle snake planter on the 0.6
nozzle — match them:

| Setting | Value |
|---|---|
| Nozzle | **0.6 mm** |
| Filament | **PETG**, nozzle **~250 °C** |
| Layer height | **0.3 mm** (first layer 0.35 mm) |
| Wall loops | **5** (fills the 3 mm wall solid — key for watertight) |
| Outer / inner wall line width | 0.66 / 0.72 mm |
| Bottom shell layers | **8+** (solid, leak-proof floor) |
| Top shell layers | 5 |
| Sparse infill | 10–15% (walls carry it) |
| Wall generator | Classic · Seam | Random or Back |

**Tips:** dry the PETG (damp PETG = stringing + weak layer bonding = leaks). Do a
**sink water-test overnight** before planting. If the outer walls print wide and
it's snug in the bore, scale X/Y down ~0.3 mm or bump `OD` down in the script.
