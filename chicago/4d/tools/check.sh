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
step "data JSON parses" check_json

printf '\n'
if [ "$FAILED" -eq 0 ]; then
  printf '\033[32mCHECK PASS\033[0m\n'
else
  printf '\033[31mCHECK FAIL\033[0m — fix the above before committing\n'
fi
exit $FAILED
