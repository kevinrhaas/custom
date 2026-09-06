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

`gcp/wright_1834_nara_gcps.json` is the odd one out: not control against modern
ground, but one sheet registered against another. The National Archives manuscript
of Wright's 1834 survey (`wright_1834_nara_hup`) is the drawing the printed map was
made from, and at 600 dpi it carries block numerals the BPL scan cannot resolve.
`tools/register_wright_nara.py` fits its pixel space onto the BPL pixel space from
twenty blind patch correspondences — the two rasters turn out to sit at 1:1, offset
by about (+316, +659) px — and composes that with the BPL affine, so a region read
on the new sheet lands in the same frame as everything else. Read the file's
`control_check_note` before trusting a distance taken off it: the two DRAWINGS
disagree locally by 8 to 15 m, which is the same order as the BPL fit's own residual
against modern control.

Large rasters are deliberately NOT committed. Each GCP file records the exact
IIIF endpoint and the sha256 of the working copy, so the raster is re-fetchable
and verifiable. Working uncertainty for anything traced from the 1834 maps:
about ±20 m (see the memo — both sheets carry real anisotropic paper stretch).
