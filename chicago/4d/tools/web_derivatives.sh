#!/usr/bin/env bash
# The web-derivative step, on its own: assets/gltf/*.glb -> assets/web/*.glb by
# `gltf-transform` alone. NO BLENDER, which is the whole point of it living here.
#
#   tools/web_derivatives.sh              regenerate every derivative
#   tools/web_derivatives.sh --out DIR    write somewhere else (measuring)
#   tools/web_derivatives.sh --only NAME  one file, by basename
#
# It was lifted out of `tools/bake.sh` by K36(b) unchanged — bake.sh calls this
# and nothing else does the work, so the bytes a nightly ships and the bytes a
# steward run can regenerate on a Blender-free runner are produced by ONE
# implementation. That mattered before it was possible: K36(a) found the
# data -> master -> derivative -> mirror chain gated at links 1 and 3 and not at
# link 2, and a repair to link 2 that could only be exercised inside a nightly
# is a repair nothing can measure.
#
# Verified byte-for-byte at the extraction: running this over the committed
# masters reproduces all 334 committed derivatives exactly, md5 for md5, on
# gltf-transform 4.4.2.
#
# THAT SENTENCE WAS NOT TRUE WHEN IT WAS WRITTEN — K36(b)'s own control measured
# 243 of 334, and the 91 it did not reproduce are the two findings it deferred:
# the 90 placeholder passthroughs (K37, decided below — the passthrough is right
# and the step now produces it) and the terrain derivative (R-W6(b), still open).
# With the size rule below in place, and K37's three repairs applied, it
# reproduces 331 of 334. The three it does not are named, not rounded off:
# `terrain__e1834_harbor_cut.glb` (committed at 14 bits, asked for at 16 —
# R-W6(b) owns it) and the two placeholders that compress SMALLER, which stay
# master copies because `generators/inferred_placeholder.py` rewrites the web
# tree from the master on every run and would undo them. See K37's open end.
set -euo pipefail
cd "$(dirname "$0")/.."

OUT=assets/web
ONLY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --out) OUT="$2"; shift 2 ;;
    --only) ONLY="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

echo "== web derivatives"
if npx --yes @gltf-transform/cli --version >/dev/null 2>&1; then
  mkdir -p "$OUT"
  # `--texture-compress ktx2` shells out to the KTX-Software `ktx` binary, and
  # gltf-transform aborts the WHOLE optimize when it is absent — meshopt included.
  # ubuntu-latest does not ship `ktx` and neither does the dev container, so that
  # flag silently turned every derivative into an uncompressed copy of its master,
  # in every environment, since this step was written. Nothing has a texture yet,
  # so ask for KTX2 only where it can actually run.
  # KTX2 IS OFF, AND THE `ktx` BINARY BEING PRESENT IS NOT ENOUGH TO TURN IT ON.
  #
  # This used to read `if command -v ktx; then --texture-compress ktx2`, which
  # asks the wrong question. Whether the TOOL can write KTX2 says nothing about
  # whether the RENDERER can read it — and it cannot: the vendored GLTFLoader
  # only handles KHR_texture_basisu after `setKTX2Loader()` is called, nothing
  # calls it, and no Basis transcoder is vendored (it would need to be, since
  # renderers/web/ takes no CDN).
  #
  # Observed the moment `ktx` was installed on the runner (bake run
  # 31773216178): three derivatives came back with KTX2 textures, and the smoke
  # got `THREE.GLTFLoader: setKTX2Loader must be called before loading KTX2
  # textures` for each of them. An asset that throws in the loader is an asset
  # that is not in the scene, so it also took out the raycast, inspection and
  # ground-contact checks downstream. The bake never reached its push step, so
  # none of it left the runner.
  #
  # Turning this on is part of W2 (docs/RENDERING.md), and the order is: wire
  # KTX2Loader + a vendored transcoder into the renderer FIRST, prove it loads a
  # textured asset, and only then set BAKE_KTX2=1 here.
  # POSITION PRECISION IS PER-MESH, AND ONE MESH IN THIS TOWN IS 5 KM WIDE.
  #
  # `gltf-transform` quantises POSITION to a bit depth under ONE UNIFORM node
  # scale set by the mesh's own bounding box, so the rung spacing an asset lands
  # on is its own widest axis over 2^bits — nothing to do with how big its
  # details are. Measured on the 244 derivatives that ship quantised
  # (tools/measure_terrain_horizontal.mjs, and the per-asset scan in R-W6):
  #
  #   water__e1834_harbor_cut   330.8 mm  ) the two epoch-scale meshes: a 2,020 m
  #   terrain__e1834_harbor_cut 306.4 mm  ) box plus 1.5 km of skirt on each side
  #   north_pier                 16.8 mm
  #   every other asset          ≤ 4.8 mm, median 0.5 mm
  #
  # At 14 bits the ground therefore ships on a 306 mm lattice, which R-BUG3c
  # found buries the road, and the town's OTHER 242 assets ship at half a
  # millimetre, which is precision nobody asked for and nothing can see. So the
  # bit depth is raised where it is needed and left alone where it is not:
  # 16 bits on the epoch meshes costs 1,116 bytes and takes the ground's lattice
  # to 76.6 mm and its worst drawn-surface error from 46.3 mm to 12.9 mm — under
  # the 22 mm road lift at every one of the field's 259,689 sample points. Asking
  # for 16 bits EVERYWHERE was measured too: +105.7 KB on a 4.47 MB payload
  # (+2.4 %) to buy nothing measurable, so it is not done. See R-W6.
  #
  # `optimize` has no --quantize-position, so compression moves to the `meshopt`
  # command in a second pass. Verified byte-for-byte: `optimize --compress false`
  # followed by a default `meshopt` reproduces the file this step shipped before,
  # exactly — the ONLY thing that changes below is the bit depth.
  EPOCH_QUANT_BITS="${EPOCH_QUANT_BITS:-16}"
  ASSET_QUANT_BITS="${ASSET_QUANT_BITS:-14}"
  compress=(--compress false)
  if [ "${BAKE_KTX2:-0}" = "1" ]; then
    if command -v ktx >/dev/null 2>&1; then
      echo "   BAKE_KTX2=1 — asking for KTX2 textures (the renderer MUST have setKTX2Loader wired)"
      compress+=(--texture-compress ktx2)
    else
      echo "   BAKE_KTX2=1 but no ktx binary on PATH; meshopt only"
    fi
  fi

  # NEVER SIMPLIFY. `optimize` runs mesh simplification BY DEFAULT, and on this
  # dataset that is not an optimisation, it is damage:
  #
  #   • The terrain is already decimated, deliberately, by generators/terrain_gen.py
  #     at a tolerance it MEASURES — it ray-casts the decimated mesh against the
  #     heightfield and refuses to export past 30 mm of drift. That number is the
  #     promise that the ground you stand on is the ground you see. A second,
  #     blind simplification pass with its own error budget breaks the promise
  #     silently and leaves nothing to measure it against.
  #   • Observed, not theorised: the ground went from 56,463 vertices per tile to
  #     about 100, and 33 of one tile's 99 remaining vertices came back with
  #     normals pointing DOWNWARD (normal.y = -1) — a hard-edged black polygon
  #     across the south-east of the town, visible from the air. The terrain had
  #     never been through this step before (it was the one asset gltf-transform
  #     had never run over), so nobody had seen what it does to a large, low-relief
  #     surface.
  #   • The buildings are authored low-poly from archetype parameters. There is no
  #     fat here for a simplifier to find, and the same class of normal damage on a
  #     clapboard wall would be far harder to spot.
  #
  # meshopt still does the compression work; simplification was never what made
  # the payload small.
  compress+=(--simplify false)

  # NEVER PALETTE, EITHER — K36(b), and the reason is the opposite of the one
  # the flag advertises.
  #
  # `optimize`'s palette pass folds a file's named materials into one
  # `PaletteMaterial` plus two generated PNGs whenever the file carries five or
  # more of them. It is sold as a draw-call saving, and inside one glTF file it
  # is. In THIS renderer it is a draw-call COST, measured on the mirror a
  # visitor is served rather than argued from the flag's documentation:
  #
  #   • `materialKey()` in renderers/web/js/buildings.js batches by material,
  #     and a texture is part of the key — a GLTFLoader mints a fresh uuid per
  #     loaded texture, so an asset arriving with its own generated palette map
  #     cannot join ANY batch, not even another palette asset's.
  #   • So the 38 faulted assets shipped as 40 single-building batches on top of
  #     the town's 16, and the published town drew 56 batches where R-W5a's
  #     number — taken against the SOURCE tree — was 16. Turning the pass off
  #     merges all 40 back in: 56 -> 16 batches, measured on the mirror.
  #   • A batch holding one building is culled with that building, so the cost
  #     is paid per POSE and it is worst where the town is densest. Measured at
  #     the eight scene anchors, 1280x800, before -> after:
  #
  #       green_tree 102 -> 70   forks  96 -> 68   from_above 84 -> 63
  #       south_water 82 -> 69   lake_market 71 -> 63   sauganash_wing 68 -> 61
  #       first_post_office 66 -> 60   sauganash 62 -> 59
  #
  #     FOUR OF THE EIGHT WERE OVER THE 80 BUDGET on the site. None is now, and
  #     the worst anchor falls 102 -> 70.
  #   • The payload it "saves" is a cost too: dropping the pass takes the 38
  #     from 318,540 to 505,932 bytes (+187,392, +58.8 % of those files, +4.1 %
  #     of the 4.5 MB tree against a 25 MB budget). The generated PNGs are
  #     cheaper on disk than 197 named materials and dearer in every other
  #     currency the renderer counts.
  #
  # It also silently deleted the names those assets were baked with — `log`,
  # `chinking`, `board`, `roof`, `dark`, `interior` — which is what K36(a) found
  # and what R-W2b needs back before it can wire an atlas onto them.
  #
  # `BAKE_PALETTE=1` restores the old behaviour for anyone who wants to
  # re-measure. Nothing in the pipeline sets it.
  if [ "${BAKE_PALETTE:-0}" = "1" ]; then
    echo "   BAKE_PALETTE=1 — palette pass ON (it costs draw calls here; see K36(b))"
  else
    compress+=(--palette false)
  fi

  # KEEP THE SMALLER FILE — K37, and the rule is a MEASUREMENT, not a class.
  #
  # `meshopt` writes an EXT_meshopt_compression header, a buffer-view table and
  # an index buffer. On a big mesh those are free; on a 30-triangle shed they
  # are most of the file, and the derivative comes out LARGER than the master it
  # was compressed from. Measured 2026-08-16 over the whole tree:
  #
  #   • the 90 flagged placeholders, compressed here for the first time:
  #     520,700 -> 628,028 bytes, +107,328 (+20.6 %). 88 of the 90 grow.
  #   • and it is not a placeholder property, in EITHER direction. THREE assets
  #     that have always been through this step ship bigger than their master
  #     today — fort_dearborn_root_house (+324), lake_house_construction (+240),
  #     fort_dearborn_magazine (+224) — while fort_dearborn_parade, 30 triangles
  #     and 5,504 bytes, compresses to -24.5 %. And two of the ninety
  #     placeholders go the other way (-808 and -816 bytes, both -9.3 %).
  #     Nothing about the asset's KIND predicts the sign; only measuring it does.
  #
  # K36(a) reported the 90 as an anomaly and K36(b)'s control found that this
  # step does not reproduce them. Both readings were right and neither was the
  # rule: the passthrough is CORRECT for those files, it was just arrived at by
  # the accident of `generators/inferred_placeholder.py` writing the same bytes
  # into both trees rather than by anything deciding it. So decide it here,
  # per file, from the bytes — a derivative that is not smaller than its master
  # has no reason to exist, and `tools/measure_web_derivatives.py` asserts the
  # outcome so the 91st cannot appear silently.
  #
  # A passthrough is not a degraded derivative. It is the master, so it carries
  # exact float positions instead of a quantised lattice, and it satisfies every
  # assertion that gate makes about identity, triangles and bounds by construction.
  # 90 assets have shipped this way to visitors since 2026-08-11.
  #
  # THE TWO EPOCH MESHES ARE EXCLUDED, DELIBERATELY AND BY NAME. `water__` is
  # +744 bytes (+55.0 %) under this rule and would be passed through by it — but
  # the epoch derivatives' bit depth is a GEOMETRIC decision (R-W6 set
  # EPOCH_QUANT_BITS against measured drawn-surface error, and the ground and the
  # waterline are what R-BUG3c, R-BUG4 and R-M1a all measure against), and
  # R-W6(b) is holding those two files pending the owner's word on regenerating
  # geometry outside a bake. A payload rule does not get to move the water while
  # that is open. The exclusion is recorded in the gate too, with its number.
  fellback=0
  passthrough=0
  for f in assets/gltf/*.glb; do
    [ -e "$f" ] || continue
    [ -z "$ONLY" ] || [ "$(basename "$f")" = "$ONLY" ] || continue
    out="$OUT/$(basename "$f")"
    case "$(basename "$f")" in
      terrain__*|water__*) bits="$EPOCH_QUANT_BITS"; epoch=1 ;;
      *) bits="$ASSET_QUANT_BITS"; epoch=0 ;;
    esac
    tmp="$(mktemp -t gltfopt.XXXXXX.glb)"
    npx --yes @gltf-transform/cli optimize "$f" "$tmp" "${compress[@]}" 2>&1 | tail -2 \
      && npx --yes @gltf-transform/cli meshopt "$tmp" "$out" \
        --quantize-position "$bits" 2>&1 | tail -2 || {
        echo "   optimize failed for $(basename "$f"); copying the master through"
        cp "$f" "$out"; fellback=$((fellback + 1)); }
    rm -f "$tmp"
    note=""
    if [ "$epoch" = "0" ] && [ "$(stat -c%s "$out")" -ge "$(stat -c%s "$f")" ]; then
      cp -f "$f" "$out"
      passthrough=$((passthrough + 1))
      note="  (compression grew it; master passed through)"
    fi
    printf '   %s  %s -> %s bytes%s\n' "$(basename "$f")" \
      "$(stat -c%s "$f")" "$(stat -c%s "$out")" "$note"
  done
  # Say it once, at the end, where it cannot scroll past unnoticed. A fallback
  # copy is CORRECT but fat, and a fat payload is what fails the 25 MB gate —
  # so the reason has to be visible next to the number.
  if [ "$fellback" -gt 0 ]; then
    echo "   WARNING: $fellback derivative(s) fell back to an uncompressed master copy"
  fi
  if [ "$passthrough" -gt 0 ]; then
    echo "   $passthrough derivative(s) kept as a master passthrough — compressing them"
    echo "   makes them bigger, which is a decision now and not an accident (K37)"
  fi
else
  echo "   gltf-transform unavailable; copying masters to assets/web unoptimised"
  mkdir -p "$OUT" && cp -f assets/gltf/*.glb "$OUT/" 2>/dev/null || true
fi

