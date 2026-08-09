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
if [ -d data/sidecars ]; then
  rm -rf "$SITE/data/sidecars"
  cp -a data/sidecars "$SITE/data/sidecars"
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
