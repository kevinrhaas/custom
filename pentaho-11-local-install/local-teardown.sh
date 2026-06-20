#!/bin/bash
# ================================================================================================
# Pentaho 11 LOCAL install — teardown
# ================================================================================================
# Stops and removes the local Pentaho stack (containers + volumes) created by
# local-deploy-pentaho.sh. Downloaded artifacts under work/ are kept unless --purge is given.
#
# Usage:
#   ./local-teardown.sh local.env            # stop + remove containers and volumes
#   ./local-teardown.sh local.env --purge    # also delete the work/ dir (downloads + extraction)
# ================================================================================================

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <env-file> [--purge]"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$1"
[ -f "$ENV_FILE" ] || ENV_FILE="${SCRIPT_DIR}/$(basename "$1")"
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Env file not found: $1"; exit 1
fi
# shellcheck disable=SC1090
source "$ENV_FILE"

DB_TYPE="${DB_TYPE:-postgres}"
WORK_DIR="${WORK_DIR:-${SCRIPT_DIR}/work}"
COMPOSE_FILE="$(find "${WORK_DIR}/onprem/dist/on-prem/pentaho-server" -maxdepth 3 -type f -name "docker-compose-${DB_TYPE}.yaml" 2>/dev/null | head -n1 || true)"
[ -z "$COMPOSE_FILE" ] && COMPOSE_FILE="$(find "${WORK_DIR}" -type f -name 'docker-compose-*.yaml' 2>/dev/null | head -n1 || true)"

if [ -n "$COMPOSE_FILE" ]; then
    echo "🛑 Bringing down stack: $COMPOSE_FILE"
    docker compose -f "$COMPOSE_FILE" down -v --remove-orphans || true
else
    echo "⚠️  No compose file found under ${WORK_DIR}; nothing to bring down."
fi

if [ "${2:-}" = "--purge" ]; then
    echo "🧹 Purging work dir: ${WORK_DIR}"
    rm -rf "$WORK_DIR"
fi

echo "✅ Teardown complete."
