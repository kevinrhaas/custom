---
id: T-0158
title: The AO bake succeeds and the glTF export drops it: the shipped occlusion texture is uniformly black
state: open
epic: PIPELINE
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-23
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Split out of T-0015, which measured it. `generators/build.py --ao` bakes ambient
occlusion correctly and then ships nothing:

| | measured 2026-08-23, `sauganash_hotel`, 512×512, 48 samples |
|---|---|
| in memory, straight after `bpy.ops.object.bake(type="AO")` | min **0.000**, max **1.000**, mean **0.2158** over 262,144 texels |
| in the exported GLB's `occlusionTexture` | min **0**, max **0** — every texel |

So the bake is fine and the export loses it. Confirmed with two independent PNG
decoders (a hand-rolled one and the repo's own `critic_metrics.decodePng`), and
the exported PNG is byte-identical at 3,620 bytes whether or not the object is
explicitly selected and activated before the bake — so selection is **not** the
cause and does not need re-testing.

What makes it worth a ticket rather than a footnote: it fails silently in the
worst direction. The run exits 0, the texture is wired into all six materials,
the GLB grows 4 KB, and `assets/manifest.json` records `baked_ao: true`. Under
glTF an occlusion value of 0 means FULLY occluded, so every asset built this way
would render with its ambient light extinguished — while the manifest asserted
it carried good AO.

`assert_ao_survived_export()` in build.py now refuses this at build time (T-0015),
so the failure is loud. This ticket is the mechanism behind it.

Worth checking first, in rough order of likelihood: whether the image needs
`img.pack()` or a `filepath` before the exporter will read its pixels; whether
the exporter re-reads the image from disk rather than from the in-memory buffer;
whether `colorspace_settings.name = "Non-Color"` being set AFTER the bake
invalidates the buffer; and whether the `ShaderNodeSeparateColor` → `Occlusion`
wiring path exports the node's input rather than the texture.

Note this is the SECOND fault of this exact shape here — the comment above the
wiring block records that the exporter once dropped AO entirely, "the bake
silently produces nothing, which is exactly what happened before this was
added". A fix should leave behind something that fails when it recurs, not just
a working export.

**Acceptance:** `--ao` on one asset produces a GLB whose occlusion texture holds
real variation — `assert_ao_survived_export` passes on merit rather than being
relaxed — and the in-memory mean and the exported mean agree to within a few
per cent, demonstrated by printing both. If the export path turns out to be
unfixable within Blender's exporter, that is a legitimate outcome recorded with
the evidence, and `--ao` should then be retired rather than left as a flag that
cannot work.
