#!/usr/bin/env bash
# Copy the publishable tree into site/. The repo's Pages workflow publishes ONLY
# site/, so anything not copied here does not ship — which is deliberate: the
# uncompressed GLB masters, the research dossiers and the raw dataset all stay
# in the repo and out of the payload.
set -euo pipefail
cd "$(dirname "$0")/.."

SITE="../../site/chicago/4d"
mkdir -p "$SITE/data/gltf" "$SITE/data/sidecars"

# renderer
if [ -d renderers/web ]; then
  rm -rf "$SITE/walk"
  cp -a renderers/web "$SITE/walk"
fi

# The changelog is authored inside the app (the What's-new tab imports it, and
# a page under walk/ cannot import from this publish mirror). Manager and the
# polecat.live launcher fetch it from <site>/js/changelog.js, though, so mirror
# it to that URL — it is a fleet-parsed contract path and must not move.
if [ -f renderers/web/js/changelog.js ]; then
  mkdir -p "$SITE/js"
  cp -f renderers/web/js/changelog.js "$SITE/js/changelog.js"
fi

# Web-derivative assets only — never the masters.
#
# assets/web/ is produced by the gltf-transform step in bake.sh. Running
# generators/build.py directly refreshes assets/gltf/ but NOT assets/web/, and
# publishing then silently ships the previous mesh — which cost a debugging
# round when a rebuilt building kept rendering with its old confidence values.
# So: any master newer than its derivative is copied through here, and says so.
mkdir -p assets/web
for m in assets/gltf/*.glb; do
  [ -e "$m" ] || continue
  w="assets/web/$(basename "$m")"
  if [ ! -e "$w" ] || [ "$m" -nt "$w" ]; then
    echo "   derivative stale, copying master through: $(basename "$m")"
    cp -f "$m" "$w"
  fi
done
# The mirror is a MIRROR, not an accumulator. Copying in without clearing out
# means a retired asset ships forever: the 108 __recommended_1835.glb placeholders
# were deleted from the source tree and kept being published for as long as anyone
# ran this script. Clear the directory so a deletion propagates the way an edit does.
rm -rf "$SITE/data/gltf"
mkdir -p "$SITE/data/gltf"
if compgen -G "assets/web/*.glb" > /dev/null; then
  cp -f assets/web/*.glb "$SITE/data/gltf/"
fi

# scenes, sidecars, datum (the renderer needs the origin for sun position).
# Keep the scenes/ subdirectory — the renderer fetches data/scenes/<year>.json,
# and flattening it here 404s the published build while the source tree works.
mkdir -p "$SITE/data/scenes"
cp -f data/scenes/*.json "$SITE/data/scenes/" 2>/dev/null || true
rm -f "$SITE"/data/[0-9]*.json
cp -f data/datum.json "$SITE/data/"
# The liberties list the Evidence panel reads. Derived from docs/LIBERTIES.md,
# which itself stays out of the payload.
cp -f data/liberties.json "$SITE/data/"

# Terrain: the epoch registry, the traced river vectors, and the heightfield the
# renderer samples. The .bin is a plain binary and must travel with its meta —
# publishing heightfield.json without heightfield.bin gives a flat world and a
# 404 that only appears on the deployed site, never in the dev tree.
mkdir -p "$SITE/data/terrain"
cp -f data/terrain/epochs.json "$SITE/data/terrain/"
if [ -d data/terrain/epochs ]; then
  rm -rf "$SITE/data/terrain/epochs"
  cp -a data/terrain/epochs "$SITE/data/terrain/epochs"
fi

if [ -d data/sidecars ]; then
  rm -rf "$SITE/data/sidecars"
  cp -a data/sidecars "$SITE/data/sidecars"
fi

# Vegetation: the flora manifest plus every zone and palette file it names. The
# renderer fetches exactly what index.json names and never probes, so a zone file
# left behind here is an HTTP 404 on the deployed walkthrough while the dev tree
# renders perfectly — the same failure the scenes/ subdirectory once caused.
# tools/validate.py --site checks the manifest against what actually landed here.
if [ -d data/flora ]; then
  rm -rf "$SITE/data/flora"
  cp -a data/flora "$SITE/data/flora"
fi

# every URL-targeted directory needs an index.html or Pages 404s the bare path
[ -f "$SITE/index.html" ] || cat > "$SITE/index.html" <<'HTML'
<!doctype html>
<meta charset="utf-8">
<title>4D Chicago — opening the walkthrough</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="canonical" href="walk/">
<style>
  body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0d1117;
       color:#e6edf3;font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
       text-align:center;padding:24px}
  a{color:#58a6ff}
</style>
<div>
  <p>Opening the <strong>4D Chicago</strong> walkthrough…</p>
  <p><a id="go" href="walk/?year=1835">Continue to the walkthrough</a></p>
</div>
<script>
  (function () {
    var p = location.pathname; if (p.slice(-1) !== '/') p += '/';
    var t = p + 'walk/' + (location.search || '?year=1835') + location.hash;
    document.getElementById('go').setAttribute('href', t);
    location.replace(t);
  })();
</script>
<noscript><meta http-equiv="refresh" content="0; url=walk/?year=1835"></noscript>
HTML

BYTES=$(du -sb "$SITE" | cut -f1)
printf 'published %s  (%.2f MB)\n' "$SITE" "$(echo "scale=4; $BYTES/1048576" | bc)"
