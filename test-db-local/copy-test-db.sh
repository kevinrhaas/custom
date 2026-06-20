#!/bin/bash
# ================================================================================================
# Copy the SE test database(s) into a local Postgres for offline dev (no VPN fragility).
# ================================================================================================
# Copies, per the db.env decision:
#   - bidb       (real data)         host 10.80.230.246 / db bidb        -> local db "bidb"
#   - bidb_ext   (RDS, fdw layer)    airlinesample RDS  / db postgres    -> local db "bidb_ext"
#
# Source credentials are read from pdc_analysis.properties (PROPERTIES_FILE in db.env).
# The local Postgres destination is the docker-compose stack in this directory.
#
# Requirements: docker + docker compose, and a Postgres client (pg_dump/psql/pg_restore) that
# matches the source major version (17). On macOS:  brew install libpq  (and add to PATH), or the
# script will fall back to running the client from the postgres:17 Docker image with --network host.
#
# Usage:  ./copy-test-db.sh db.env
# ================================================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${1:-${SCRIPT_DIR}/db.env}"
[ -f "$ENV_FILE" ] || ENV_FILE="${SCRIPT_DIR}/$(basename "${1:-db.env}")"
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Config not found. Copy db.env.template to db.env first."
    exit 1
fi
# shellcheck disable=SC1090
set -a; source "$ENV_FILE"; set +a

LOCAL_PORT="${LOCAL_PORT:-5433}"
LOCAL_SUPERUSER="${LOCAL_SUPERUSER:-postgres}"
LOCAL_PASSWORD="${LOCAL_PASSWORD:-postgres}"
LOCAL_PG_IMAGE="${LOCAL_PG_IMAGE:-postgres:17}"
DUMP_SCOPE="${DUMP_SCOPE:-all}"
TMP_DIR="${SCRIPT_DIR}/work"
mkdir -p "$TMP_DIR"

# ------------------------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------------------------
prop() {  # read KEY=VALUE from the properties file (value may contain '=')
    [ -f "$PROPERTIES_FILE" ] || { echo ""; return; }
    grep -E "^$1=" "$PROPERTIES_FILE" | head -1 | cut -d= -f2-
}

HAVE_HOST_PG=0
if command -v pg_dump >/dev/null 2>&1 && command -v psql >/dev/null 2>&1 && command -v pg_restore >/dev/null 2>&1; then
    HAVE_HOST_PG=1
fi

# pg client wrappers — prefer host binaries; else dockerized client on the host network.
# PGPASSWORD must be exported by the caller.
_pg() {  # _pg <pg_dump|psql|pg_restore> [args...]
    local bin="$1"; shift
    if [ "$HAVE_HOST_PG" = "1" ]; then
        "$bin" "$@"
    else
        docker run --rm -i --network host -e PGPASSWORD="${PGPASSWORD:-}" \
            -v "$TMP_DIR:$TMP_DIR" -w "$TMP_DIR" "$LOCAL_PG_IMAGE" "$bin" "$@"
    fi
}

tcp_ok() {  # host port  -> 0 if reachable
    local h="$1" p="$2"
    timeout 8 bash -c "exec 3<>/dev/tcp/${h}/${p}" 2>/dev/null
}

# ------------------------------------------------------------------------------------------------
# Preflight
# ------------------------------------------------------------------------------------------------
echo "🔎 Preflight"
echo "==========="
fail=0
command -v docker >/dev/null 2>&1 || { echo "❌ docker not found"; fail=1; }
docker compose version >/dev/null 2>&1 || { echo "❌ docker compose v2 not found"; fail=1; }
docker info >/dev/null 2>&1 || { echo "❌ docker daemon not reachable"; fail=1; }
if [ ! -f "$PROPERTIES_FILE" ]; then
    echo "❌ PROPERTIES_FILE not found: $PROPERTIES_FILE"
    echo "   Set it in db.env to your local solution-engineering checkout."
    fail=1
fi
if [ "$HAVE_HOST_PG" = "1" ]; then
    echo "✅ Using host Postgres client ($(pg_dump --version | awk '{print $NF}'))"
else
    echo "ℹ️  No host pg client; will run ${LOCAL_PG_IMAGE} via docker (--network host)."
    echo "   Note: on macOS, --network host can't reach VPN routes — install libpq instead:"
    echo "         brew install libpq && echo 'export PATH=\"\$(brew --prefix libpq)/bin:\$PATH\"' >> ~/.zshrc"
fi
[ "$fail" -ne 0 ] && { echo "🚫 Preflight failed."; exit 1; }
echo ""

# ------------------------------------------------------------------------------------------------
# Bring up local Postgres
# ------------------------------------------------------------------------------------------------
echo "🐘 Starting local Postgres"
echo "=========================="
( cd "$SCRIPT_DIR" && docker compose up -d )
echo -n "⏳ Waiting for local Postgres to be ready"
for _ in $(seq 1 60); do
    if docker exec "${LOCAL_CONTAINER_NAME:-test-db-local}" pg_isready -U "$LOCAL_SUPERUSER" >/dev/null 2>&1; then
        echo " ✅"; break
    fi
    echo -n "."; sleep 2
done
echo ""

# Create a target database if missing
ensure_db() {
    local db="$1"
    PGPASSWORD="$LOCAL_PASSWORD" _pg psql -h localhost -p "$LOCAL_PORT" -U "$LOCAL_SUPERUSER" -d postgres -tAc \
        "SELECT 1 FROM pg_database WHERE datname='${db}'" 2>/dev/null | grep -q 1 || \
    PGPASSWORD="$LOCAL_PASSWORD" _pg psql -h localhost -p "$LOCAL_PORT" -U "$LOCAL_SUPERUSER" -d postgres -c \
        "CREATE DATABASE \"${db}\"" >/dev/null
}

# ------------------------------------------------------------------------------------------------
# Copy one source -> local
# ------------------------------------------------------------------------------------------------
copy_source() {
    local label="$1" src_host="$2" src_port="$3" src_user="$4" src_db="$5" src_pass="$6" target_db="$7"; shift 7
    local schemas=("$@")

    echo ""
    echo "════════════════════════════════════════════════════════"
    echo "📦 ${label}:  ${src_user}@${src_host}:${src_port}/${src_db}  ->  local db '${target_db}'"
    echo "   schemas: ${schemas[*]}"
    echo "════════════════════════════════════════════════════════"

    if [ -z "$src_host" ] || [ -z "$src_pass" ]; then
        echo "⚠️  Missing host/password for ${label} (check PROPERTIES_FILE). Skipping."
        return 1
    fi
    if ! tcp_ok "$src_host" "$src_port"; then
        echo "❌ Cannot reach ${src_host}:${src_port} — is the VPN connected? Skipping ${label}."
        return 1
    fi
    echo "✅ Source reachable"

    ensure_db "$target_db"

    local scope_flag=""
    [ "$DUMP_SCOPE" = "schema-only" ] && scope_flag="--schema-only"

    local n_args=()
    for s in "${schemas[@]}"; do n_args+=("-n" "$s"); done

    local dump="${TMP_DIR}/${label}.dump"
    echo "⬇️  Dumping ${label} ..."
    if ! PGPASSWORD="$src_pass" _pg pg_dump -h "$src_host" -p "$src_port" -U "$src_user" -d "$src_db" \
            "${n_args[@]}" -Fc --no-owner --no-privileges $scope_flag -f "$dump"; then
        echo "❌ pg_dump failed for ${label}"
        return 1
    fi
    echo "   dump size: $(du -h "$dump" 2>/dev/null | cut -f1)"

    echo "⬆️  Restoring into local db '${target_db}' ..."
    # pg_restore returns non-zero on benign errors (e.g. FDW/extension ownership); don't abort.
    PGPASSWORD="$LOCAL_PASSWORD" _pg pg_restore -h localhost -p "$LOCAL_PORT" -U "$LOCAL_SUPERUSER" \
        -d "$target_db" --no-owner --no-privileges --clean --if-exists "$dump" \
        || echo "   ⚠️  pg_restore reported warnings (often FDW/extension related) — continuing."
    echo "✅ ${label} copied"
}

# ------------------------------------------------------------------------------------------------
# Read source creds from properties and run the copies
# ------------------------------------------------------------------------------------------------
RC=0
if [ "${COPY_BIDB:-yes}" = "yes" ]; then
    read -r -a _bidb_schemas <<< "${BIDB_SCHEMAS:-bidb}"
    copy_source "bidb" \
        "$(prop BIDB_HOST)" "$(prop BIDB_PORT)" "$(prop BIDB_USERNAME)" "$(prop BIDB_DB_NAME)" "$(prop BIDB_PASSWORD)" \
        "${BIDB_TARGET_DB:-bidb}" "${_bidb_schemas[@]}" || RC=1
fi

if [ "${COPY_BIDB_EXT:-yes}" = "yes" ]; then
    read -r -a _ext_schemas <<< "${BIDB_EXT_SCHEMAS:-bidb_ext_dev}"
    copy_source "bidb_ext" \
        "$(prop BIDB_EXT_HOST)" "$(prop BIDB_EXT_PORT)" "$(prop BIDB_EXT_USERNAME)" "$(prop BIDB_EXT_DB_NAME)" "$(prop BIDB_EXT_PASSWORD)" \
        "${BIDB_EXT_TARGET_DB:-bidb_ext}" "${_ext_schemas[@]}" || RC=1
fi

# ------------------------------------------------------------------------------------------------
# Optional: repoint bidb_ext's postgres_fdw server at the LOCAL bidb copy
# ------------------------------------------------------------------------------------------------
if [ "${REPOINT_FDW_TO_LOCAL:-no}" = "yes" ] && [ "${COPY_BIDB:-yes}" = "yes" ] && [ "${COPY_BIDB_EXT:-yes}" = "yes" ]; then
    echo ""
    echo "🔁 Repointing bidb_ext postgres_fdw server(s) at the local bidb copy ..."
    # List foreign servers in the bidb_ext db and repoint each to the local container (in-Docker addr).
    PGPASSWORD="$LOCAL_PASSWORD" _pg psql -h localhost -p "$LOCAL_PORT" -U "$LOCAL_SUPERUSER" \
        -d "${BIDB_EXT_TARGET_DB:-bidb_ext}" -v ON_ERROR_STOP=0 <<SQL || echo "   ⚠️  FDW repoint reported warnings."
DO \$\$
DECLARE srv text;
BEGIN
  FOR srv IN SELECT srvname FROM pg_foreign_server LOOP
    EXECUTE format('ALTER SERVER %I OPTIONS (SET host %L, SET port %L, SET dbname %L)',
                   srv, 'host.docker.internal', '${LOCAL_PORT}', '${BIDB_TARGET_DB:-bidb}');
    RAISE NOTICE 'Repointed server % -> host.docker.internal:${LOCAL_PORT}/${BIDB_TARGET_DB:-bidb}', srv;
  END LOOP;
END\$\$;
SQL
    echo "   ℹ️  If foreign-table queries fail on a user mapping, set its password to the local one:"
    echo "      ALTER USER MAPPING FOR <user> SERVER <srv> OPTIONS (SET password '${LOCAL_PASSWORD}');"
fi

# ------------------------------------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------------------------------------
echo ""
echo "════════════════════════════════════════════════════════"
echo "🎉 Done (exit status: $RC)"
echo "Local Postgres:  host=localhost  port=${LOCAL_PORT}  user=${LOCAL_SUPERUSER}  pass=${LOCAL_PASSWORD}"
echo "Connect:         ./psql-local.sh ${BIDB_TARGET_DB:-bidb}"
echo "                 psql -h localhost -p ${LOCAL_PORT} -U ${LOCAL_SUPERUSER} -d ${BIDB_TARGET_DB:-bidb}"
echo "════════════════════════════════════════════════════════"
exit $RC
