#!/usr/bin/env bash
# The per-commit gate. Seconds, no Blender, runs in every agent sandbox.
#
# A gate that takes four minutes gets skipped, so this one deliberately does not
# build geometry. Content builds live in tools/bake.sh and run on demand.
#
#   tools/check.sh            the gate
#   tools/check.sh --strict   warnings are errors (used before a release)
set -uo pipefail
cd "$(dirname "$0")/.."

STRICT=""
[ "${1:-}" = "--strict" ] && STRICT="--strict"

FAILED=0
step() {
  local label="$1"; shift
  printf '\n\033[1m== %s\033[0m\n' "$label"
  if "$@"; then
    return 0
  else
    FAILED=1
    printf '\033[31m   ^ %s failed\033[0m\n' "$label"
    return 1
  fi
}

step "dataset (schema, provenance, date gates, licenses, staleness, publish)" \
  python3 tools/validate.py --all $STRICT

step "validator self-tests" \
  python3 tools/test_validate.py

# Anonymous reconstruction infill is authored as a compact parcel recipe, then
# expanded to ordinary one-file-per-structure records and visibly flagged GLBs.
# Both derivations must stay reproducible without Blender.
step "inferred infill records match the 665-roof programme" \
  python3 tools/generate_inferred_infill.py --check

step "North Division initial parcel matches its reviewed recipe" \
  python3 tools/generate_north_infill.py --check

step "West Division approaches parcel matches its recipe" \
  python3 tools/generate_west_infill.py --check

# The block parcels are the same shape of derivation with one difference worth the
# extra step: they author no coordinates at all. Every metre comes from the committed
# lot polygons, so a hand-nudged building would show up here as drift rather than as a
# plausible-looking number sitting beside a derived grid.
step "platted block parcels match their recipe and the committed lots" \
  python3 tools/generate_block_infill.py --check

# The inferred-household layer (K1 phase two) is the same shape of thing: an
# authored recipe — an occupation census, a roof-adoption table and a placement
# list — expanded into households, occupancy blocks and structure records. It also
# re-runs its own placement gates, so a centre that drifts onto another building,
# onto water or off the modelled ground fails here rather than in a bake.
step "inferred households, adoptions and their buildings match the programme" \
  python3 tools/generate_inferred_households.py --check

step "inferred placeholder GLBs match their records" \
  python3 generators/inferred_placeholder.py --check

# The platted block and lot grid is generated from the Thompson module and the
# committed street lines, never traced off the 1834 sheets. Re-deriving it here is
# what keeps it a derivation: a hand-nudged block face would otherwise sit in the
# repo looking exactly like a surveyed one.
step "the platted block and lot grid re-derives from the module" \
  python3 tools/generate_plat_lots.py --check

# The 665-roof programme's remainder is a function of what has been built, and the town
# grows most nights. Left as an authored number it goes stale silently — the crosswalk
# called 617 roofs remaining while 232 were standing — and the next block parcel schedules
# against a figure that is wrong by a third of the programme.
step "the 665-roof programme reconciles with the town that stands" \
  python3 tools/reconcile_665.py --check

# The datum must remain the output of its committed ground control, never a
# hand-edited number. Skips (exit 0) when pyproj is not installed.
step "datum re-derivation" \
  python3 tools/rederive_datum.py

# The liberties the walkthrough shows must still be the ones the markdown
# states. LIBERTIES.md is append-only and is the source of truth; data/
# liberties.json is derived and committed so the site needs no build step, which
# only holds up if drift is a gate failure rather than a discovery.
step "liberties derived from docs/LIBERTIES.md" \
  python3 tools/compile_liberties.py --check

# The renderer reads the sidecars and never the dataset, which only keeps the
# walkthrough and the archive together if a record edited without a recompile is
# a failure here rather than a discovery on the deployed site.
step "sidecars derived from data/" \
  python3 tools/compile_scene.py --all --check

# Renderer JS must at least parse. The repo's deploy workflow does the same thing
# for site/, and a syntax error there is a blank page for everyone.
check_js() {
  local n=0 bad=0
  while IFS= read -r -d '' f; do
    n=$((n + 1))
    node --input-type=module --check < "$f" 2>/dev/null || {
      echo "   parse error: $f"; bad=1
    }
  done < <(find renderers -name '*.js' -not -path '*/vendor/*' -print0 2>/dev/null)
  echo "   $n module(s) parsed"
  return $bad
}
step "renderer modules parse" check_js

# The ground the town is ANCHORED to and the ground it is DRAWN as, compared on
# the committed bytes. `generators/terrain_gen.py` refuses to export a mesh more
# than 30 mm from the heightfield — inside a Blender run this gate cannot make,
# so nothing re-checked the committed master afterwards, and R-BUG3c was a 306 mm
# disagreement nobody could see. This asserts the master and REPORTS the shipped
# derivative, which is quantised by the publish step and conformed at load; the
# surface actually drawn is asserted by tools/smoke_renderer.mjs.
step "the ground mesh still meets the heightfield the walker samples" \
  node tools/measure_terrain_fit.mjs --gate

# The changelog contract, on every run rather than only when somebody remembers
# it. AGENTS.md has always told an agent to run this by hand before merging, and
# on 2026-08-13 the file was corrupted BY A MERGE — `.gitattributes` merges it
# with `merge=union`, so both parents were green and the union of them was not.
# A hand-run check cannot cover a file that a merge rewrites; this one can.
step "changelog contract" \
  node tools/check-changelog.mjs

# Does the site ship what the repository says it ships? R-BUG3c-b (#145) cost
# three parcels because the ground a browser loads was quantised by a publish
# step AFTER the only gate that measured it, and every gate passed because every
# gate compared a render to another render. #145 fixed that instance and left
# the general case open in as many words: "Nothing else in this project measures
# a published artefact against its own source." This is that gate. publish.sh is
# almost entirely `cp`, so the invariant is total — every published file is
# byte-identical to its source unless it is on a declared list that has to name
# what transforms it and which gate measures the SHIPPED form. It found two
# unchecked files on its first run, one of them a build.json two days stale.
# Skipped rather than failed when the mirror is absent, so a fresh checkout that
# has not published yet still gates cleanly.
if [ -d ../../site/chicago/4d ]; then
  step "published mirror matches its source" \
    node tools/check_published.mjs
fi

# The integration preview's assembler. It lives at the repo root because the
# deploy workflow does, but nothing else tests it, and it is the only thing that
# marks the preview as a preview — the noindex, the banner, the build stamp. A
# preview that quietly stops saying "DEV PREVIEW" is one screenshot away from
# being reported as a production bug. Skipped rather than failed when the script
# is absent, so a checkout of chicago/4d alone still gates cleanly.
if [ -f ../../.github/chicago-4d-dev-preview.mjs ]; then
  step "dev preview assembles, marked and stamped" \
    node tools/test_dev_preview.mjs
fi

# Every JSON in data/ must be loadable — a stray comma here breaks the whole build
# in a place far from the edit that caused it.
check_json() {
  python3 - <<'PY'
import json, sys
from pathlib import Path
bad = 0
n = 0
for p in sorted(Path("data").rglob("*.json")):
    n += 1
    try:
        json.loads(p.read_text())
    except json.JSONDecodeError as e:
        print(f"   invalid JSON: {p}: {e}")
        bad = 1
print(f"   {n} data file(s) parsed")
sys.exit(bad)
PY
}
# Attested must cite a source, an inference must record what it reasoned from,
# and NOTHING on an invented structure may outrank the invention that put it
# there. That last rule is the one that mattered: without it, 158 buildings that
# never existed graded their wall heights as evidence and rendered solid.
# The invented names, re-derived. Deterministic from each person's id, so a name
# that changed without the pools or the generator changing is a real finding.
step "the reconstructed residents' invented names re-derive" \
  python3 tools/generate_inferred_names.py --check

step "the three levels mean what they say" \
  python3 tools/audit_confidence.py --strict

step "data JSON parses" check_json

printf '\n'
if [ "$FAILED" -eq 0 ]; then
  printf '\033[32mCHECK PASS\033[0m\n'
else
  printf '\033[31mCHECK FAIL\033[0m — fix the above before committing\n'
fi
exit $FAILED
