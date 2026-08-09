# Georeferencing traces

The citable record of how this project's spatial frame was derived. Everything in
`docs/RESEARCH/datum_derivation.md` computes from these files, and
`tools/rederive_datum.py` (run by `check.sh`) fails the build if `data/datum.json`
ever stops matching them.

```
allmaps/   Published georeference annotations archived verbatim (provenance for
           what the holding institutions assert; superseded by gcp/ for use)
gcp/       This project's ground control: per-map GCPs with pixel coords,
           modern OSM control (node ids, ODbL), fitted transforms, residuals
vectors/   (S2+) per-map traced vector layers, each tagged with its source_id
```

Large rasters are deliberately NOT committed. Each GCP file records the exact
IIIF endpoint and the sha256 of the working copy, so the raster is re-fetchable
and verifiable. Working uncertainty for anything traced from the 1834 maps:
about ±20 m (see the memo — both sheets carry real anisotropic paper stretch).
