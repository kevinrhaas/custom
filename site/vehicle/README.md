# Corsair Finder

A curated, verified search for a **2026 Lincoln Corsair** for Pat — priorities in order:

1. **Red Carpet Metallic Tinted Clearcoat** exterior
2. **Light interior** — Light Smoked Truffle ideal; Medium Smoked Truffle / Eternal Red / Ebony as backups; light faux-leather is acceptable
3. **Reserve or Premiere** trim (Grand Touring / PHEV excluded)
4. **AWD** preferred (FWD acceptable as a fallback)
5. Panoramic Vista Roof and higher packages preferred
6. New 2026, or lightly used / essentially new

`index.html` is a self-contained static app (Polecat design tokens inlined — no build step).
`vehicles.json` is the underlying data snapshot; edit it and re-run `build_app.py` to regenerate,
or hand-edit `index.html` directly.

Published via GitHub Pages by `.github/workflows/deploy-pages.yml` →
**https://kevinrhaas.github.io/custom/vehicle/**

Data snapshot: 2026-07-19. Live inventory changes daily — confirm availability, price, exact
interior and options with each dealer before acting. Nothing in the data is invented; fields that
couldn't be verified from a listing read "call to confirm."
