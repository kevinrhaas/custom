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
  compress=(--compress meshopt)
  if command -v ktx >/dev/null 2>&1; then
    compress+=(--texture-compress ktx2)
  else
    echo "   no ktx binary; meshopt only (nothing in this scene is textured)"
  fi
  fellback=0
  for f in assets/gltf/*.glb; do
    [ -e "$f" ] || continue
    out="assets/web/$(basename "$f")"
    npx --yes @gltf-transform/cli optimize "$f" "$out" \
      "${compress[@]}" 2>&1 | tail -2 || {
        echo "   optimize failed for $(basename "$f"); copying the master through"
        cp "$f" "$out"; fellback=$((fellback + 1)); }
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
