#!/usr/bin/env bash
# Copy the publishable tree into site/. The repo's Pages workflow publishes ONLY
# site/, so anything not copied here does not ship — which is deliberate: the
# uncompressed GLB masters, the research dossiers and the raw dataset all stay
# in the repo and out of the payload.
set -euo pipefail
cd "$(dirname "$0")/.."

# ---------------------------------------------------------------------------
# THIS SCRIPT IS NOT A WRITER OF assets/web/ — ROADMAP K38.
#
# It used to be. Any master newer by mtime than its derivative was copied
# through, here, into the TRACKED source tree and then into the mirror. The
# intent was right — run `generators/build.py` alone and `assets/web/` goes
# stale, which once cost a debugging round when a rebuilt building kept
# rendering with its old confidence values — but the response was wrong twice:
#
#   * it SHIPPED THE UNCOMPRESSED MASTER, silently. Measured: two assets copied
#     through this way added 1,212,760 bytes to the payload, and the entire dev
#     gate printed CHECK PASS. A master copied over its own derivative has that
#     master's triangles, node identity, attributes, bounding box and materials,
#     and a byte count that is equal rather than larger, so every assertion in
#     tools/measure_web_derivatives.py passed it. Assertion 8 exists now and
#     catches exactly this, from ANY writer.
#   * and it made a publish step mutate the repository, which is the one thing
#     the mirror contract says publish does not do.
#
# So the detection stays and the writing goes. This refuses BEFORE it writes
# anything, names the files and names the command that fixes them.
#
# AND THE DETECTION IS NO LONGER AN mtime SCAN — ROADMAP K39. It was one, and K38
# recorded its own residual in as many words: mtime is a conservative trigger, not a
# complete one, because on a fresh clone `git checkout`'s write order makes every
# master older than its derivative (measured: 334 of 334). So the scan was silent on
# exactly the tree a steward run starts from, and the stale derivative it was written
# to catch — a master rebuilt with the same geometry and different _CONFIDENCE values —
# went past it and past assertions 1-8 alike.
#
# tools/web_derivatives.sh records the sha256 of the master it compressed as it writes
# each derivative, and assertion 9 in tools/measure_web_derivatives.py compares that
# hash to the master in the tree. So staleness is answered from CONTENT here now, and
# this simply runs the gate: it is the same question, asked by the thing that already
# knows how to ask it, and running the whole gate also means a publish cannot ship a
# tree whose derivatives fail any of the other eight.
# ---------------------------------------------------------------------------
mkdir -p assets/web
if ! python3 tools/measure_web_derivatives.py --gate --quiet; then
  echo "" >&2
  echo "REFUSING TO PUBLISH — the derivatives this would mirror do not answer for" >&2
  echo "themselves against the masters in the tree (see the failures above). The site" >&2
  echo "would carry a building the repository no longer describes, and publishing it" >&2
  echo "is how that becomes invisible." >&2
  echo "" >&2
  echo "Each failure names its own remedy; both of the common ones are regenerations:" >&2
  echo "   tools/web_derivatives.sh --only <name>       # a stale or unrecorded file" >&2
  echo "   python3 tools/measure_web_derivatives.py --write-baseline   # only if the" >&2
  echo "     # passthrough set moved — a master that compresses bigger stays a copy" >&2
  exit 1
fi

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

# The ticket board, for Manager and any fleet reader: tickets.json is generated
# by tools/ticket.mjs (check.sh refuses a stale one), mirrored verbatim here.
if [ -f tickets/tickets.json ]; then
  cp -f tickets/tickets.json "$SITE/tickets.json"
fi

# Web-derivative assets only — never the masters. assets/web/ is produced by
# tools/web_derivatives.sh (which tools/bake.sh calls and nothing else does);
# the staleness of that directory against assets/gltf/ is settled at the top of
# this script, and this copies what is there rather than deciding it.
#
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
# The population layer. `data/residents/` carries no geometry by design (L1: no
# human figures), so nothing here is drawn — but the building card now names the
# households attached to a structure, and the Evidence panel and any future "who
# lived here" view read the manifest and the household records straight off the
# site. Until this line existed the whole layer stopped at the repo: ninety-six
# researched people that a visitor had no way to reach, which reads exactly like
# work that was never done.
if [ -d data/residents ]; then
  rm -rf "$SITE/data/residents"
  cp -a data/residents "$SITE/data/residents"
fi

# The enclosure layer — fence lines, yards and pens, drawn by
# renderers/web/js/enclosures.js straight from these numbers. It carries no GLB
# by design (an enclosure is a perimeter, not a footprint), so this copy is the
# whole of the layer's payload: leave it out and the fences are a 404 on the
# deployed site while the dev tree draws them perfectly — the same failure the
# scenes/ subdirectory and the fauna directory each caused once already.
if [ -d data/enclosures ]; then
  rm -rf "$SITE/data/enclosures"
  cp -a data/enclosures "$SITE/data/enclosures"
fi

# The signage layer — the boards on the town's business frontages, drawn by
# renderers/web/js/signage.js straight from these numbers. Same argument as the
# enclosures above and the same failure if it is left out: no GLB carries any of
# it, so an unmirrored directory is a 404 on the deployed site while the dev tree
# hangs every board perfectly.
if [ -d data/signage ]; then
  rm -rf "$SITE/data/signage"
  cp -a data/signage "$SITE/data/signage"
fi

# The yard layer — the barrels, cases and the one wagon standing on the town's
# own ground, drawn by renderers/web/js/yard.js straight from these numbers.
# Same argument as the enclosures and the signage above and the same failure if
# it is left out: no GLB carries any of it, so an unmirrored directory is a 404
# on the deployed site while the dev tree stands every barrel perfectly.
if [ -d data/yard ]; then
  rm -rf "$SITE/data/yard"
  cp -a data/yard "$SITE/data/yard"
fi

# The wharf layer — the river docks at the two forwarding warehouses whose own
# records state one, drawn by renderers/web/js/wharves.js straight from these
# numbers. Same argument as the enclosures, the signage and the yard above and
# the same failure if it is left out: no GLB carries any of it, so an unmirrored
# directory is a 404 on the deployed site while the dev tree draws both docks
# perfectly.
if [ -d data/wharves ]; then
  rm -rf "$SITE/data/wharves"
  cp -a data/wharves "$SITE/data/wharves"
fi

if [ -d data/flora ]; then
  rm -rf "$SITE/data/flora"
  cp -a data/flora "$SITE/data/flora"
fi

# The animal layer (ROADMAP K51). Same argument as the residents above, and it
# was open longer: 139 records across ten habitat zones, every one graded to
# 1 July 1835 and cited, and until this line no browser had ever been offered
# the directory — while data/scenes/1835.json listed `fauna` among the scene's
# layers and two other documents implied a reader existed. Nothing here is
# drawn; the Evidence panel's wildlife section reads it as text.
if [ -d data/fauna ]; then
  rm -rf "$SITE/data/fauna"
  cp -a data/fauna "$SITE/data/fauna"
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

# The build stamp the gate shows. Written here because publish IS the build: the
# one moment that knows which commit became which deployed tree. Central Time,
# because that is the clock the project's dates are quoted in everywhere else.
BUILD_VERSION=$(git rev-parse --short HEAD 2>/dev/null || echo unknown)
BUILD_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
BUILD_CT=$(TZ=America/Chicago date +"%b %-d, %Y, %-I:%M %p CT")
# Injected as TEXT into the published gate, not fetched. A stamp that needs a
# request is a stamp that 404s in the dev tree and disappears exactly when the
# build is broken enough to matter; this one renders with no JS at all.
STAMP="build $BUILD_VERSION · $BUILD_CT"
if [ -f "$SITE/walk/index.html" ]; then
  python3 - "$SITE/walk/index.html" "$STAMP" <<'PYEOF'
import sys, pathlib
p, stamp = pathlib.Path(sys.argv[1]), sys.argv[2]
s = p.read_text()
s = s.replace('<p class="gate-build" id="gate-build" hidden><!--BUILD_STAMP--></p>',
              '<p class="gate-build" id="gate-build">' + stamp + '</p>')
p.write_text(s)
PYEOF
fi
# build.json — the machine-readable twin of the stamp above. It was written ONCE,
# by hand, and then never again: the gate added in R-BUG3c-b's wake found it
# claiming version 8909332 built 2026-08-13 while the mirror beside it was two
# days newer. Anything reading it — tools/test_dev_preview.mjs, docs/PIPELINE.md —
# was reading a stale claim about what shipped. It is regenerated every publish
# now, from the same two variables the visible stamp uses, so the two cannot
# disagree.
cat > "$SITE/build.json" <<JSON
{
  "version": "$BUILD_VERSION",
  "built_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "built_ct": "$BUILD_CT"
}
JSON

echo "   build $BUILD_VERSION  $BUILD_CT"

BYTES=$(du -sb "$SITE" | cut -f1)
printf 'published %s  (%.2f MB)\n' "$SITE" "$(echo "scale=4; $BYTES/1048576" | bc)"
