#!/bin/bash
# Stop the local test-DB. Usage: ./teardown.sh [--purge]
#   (no args)  stop + remove the container
#   --purge    also delete the data volume (all copied data) and work/ dumps
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[ -f "${SCRIPT_DIR}/db.env" ] && { set -a; source "${SCRIPT_DIR}/db.env"; set +a; }
cd "$SCRIPT_DIR"
if [ "${1:-}" = "--purge" ]; then
    docker compose down -v
    rm -rf "${SCRIPT_DIR}/work"
    echo "✅ Stopped and purged data volume + work/."
else
    docker compose down
    echo "✅ Stopped (data volume kept). Use --purge to delete data."
fi
