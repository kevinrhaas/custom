#!/usr/bin/env bash
# The content build. Minutes, not seconds — runs on demand and nightly, NOT on
# every commit. tools/check.sh is the per-commit gate and needs no Blender.
#
#   tools/bake.sh                 build everything
#   tools/bake.sh --only <id>     build one structure
#   tools/bake.sh --no-bake       skip AO baking (fast iteration)
#
# Blender is pinned by exact version + sha256 in generators/blender.pin. Version
# pinning is what buys back determinism from a stateful tool; determinism itself
# is defined on INPUTS (see assets/manifest.json), because Cycles AO is not
# bit-reproducible across hardware.
set -euo pipefail
cd "$(dirname "$0")/.."

# shellcheck disable=SC1091
source generators/blender.pin

CACHE="${BLENDER_CACHE:-/opt/blender-dl}"
BIN="$CACHE/$BLENDER_DIR/blender"
TARBALL="$CACHE/$(basename "$BLENDER_URL")"

fetch_blender() {
  mkdir -p "$CACHE"
  if [ ! -x "$BIN" ]; then
    if [ ! -f "$TARBALL" ]; then
      echo "fetching Blender $BLENDER_VERSION ..."
      curl -fL --retry 3 -o "$TARBALL" "$BLENDER_URL"
    fi
    echo "$BLENDER_SHA256  $TARBALL" | sha256sum -c - || {
      echo "SHA256 MISMATCH on the Blender tarball — refusing to run."
      echo "Either the download is corrupt or blender.pin is wrong. Do not 'fix'"
      echo "this by updating the hash without knowing why it changed."
      exit 1
    }
    tar -xf "$TARBALL" -C "$CACHE"
  fi
  "$BIN" --version | head -1
}

echo "== Blender"
fetch_blender

echo
echo "== generate + bake"
"$BIN" -b -noaudio --factory-startup --python generators/build.py -- "$@"

echo
echo "== web derivatives"
if npx --yes @gltf-transform/cli --version >/dev/null 2>&1; then
  mkdir -p assets/web
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
  fellback=0
  for f in assets/gltf/*.glb; do
    [ -e "$f" ] || continue
    out="assets/web/$(basename "$f")"
    case "$(basename "$f")" in
      terrain__*|water__*) bits="$EPOCH_QUANT_BITS" ;;
      *) bits="$ASSET_QUANT_BITS" ;;
    esac
    tmp="$(mktemp -t gltfopt.XXXXXX.glb)"
    npx --yes @gltf-transform/cli optimize "$f" "$tmp" "${compress[@]}" 2>&1 | tail -2 \
      && npx --yes @gltf-transform/cli meshopt "$tmp" "$out" \
        --quantize-position "$bits" 2>&1 | tail -2 || {
        echo "   optimize failed for $(basename "$f"); copying the master through"
        cp "$f" "$out"; fellback=$((fellback + 1)); }
    rm -f "$tmp"
    printf '   %s  %s -> %s bytes\n' "$(basename "$f")" \
      "$(stat -c%s "$f")" "$(stat -c%s "$out")"
  done
  # Say it once, at the end, where it cannot scroll past unnoticed. A fallback
  # copy is CORRECT but fat, and a fat payload is what fails the 25 MB gate —
  # so the reason has to be visible next to the number.
  if [ "$fellback" -gt 0 ]; then
    echo "   WARNING: $fellback derivative(s) fell back to an uncompressed master copy"
  fi
else
  echo "   gltf-transform unavailable; copying masters to assets/web unoptimised"
  mkdir -p assets/web && cp -f assets/gltf/*.glb assets/web/ 2>/dev/null || true
fi

echo
echo "== sidecars"
python3 tools/compile_scene.py --all

echo
echo "== publish"
tools/publish.sh

echo
echo "== gate"
tools/check.sh

# The smoke runs against the PUBLISHED mirror, not the source tree, and it runs
# here because this is the step that just produced the compressed derivatives.
#
# The two trees do not load the same geometry: a sidecar's `gltf/<name>.glb`
# resolves to the uncompressed masters in the source tree and to the meshopt +
# quantised derivatives on the site. For as long as the smoke only ran against
# the source tree it never loaded a compressed asset, and a bug that collapsed
# every building to a two-metre box shipped past a fully green gate — twice.
# Whatever else is true, the bytes a visitor downloads have to be the bytes
# something tested.
if [ "${SKIP_SMOKE:-0}" = "1" ]; then
  echo
  echo "== smoke (skipped: SKIP_SMOKE=1)"
else
  echo
  echo "== smoke (published mirror)"
  node tools/smoke_renderer.mjs --published
fi
