#!/bin/bash
# Open a psql shell on the local test-DB container. Usage: ./psql-local.sh [dbname]
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[ -f "${SCRIPT_DIR}/db.env" ] && { set -a; source "${SCRIPT_DIR}/db.env"; set +a; }
DB="${1:-${LOCAL_DEFAULT_DB:-postgres}}"
docker exec -it "${LOCAL_CONTAINER_NAME:-test-db-local}" \
    psql -U "${LOCAL_SUPERUSER:-postgres}" -d "$DB"
