#!/bin/bash
# ================================================================================================
# Pentaho 11 — LOCAL Docker install
# ================================================================================================
# Adapted from the Solution Engineering repo (kevinrhaas/solution-engineering/pentaho-11-docker-deploy)
# with the AWS EC2 / Okta / SSH layer removed so it runs entirely on your own machine.
#
# What it does (all locally):
#   1. Downloads the Pentaho Server image tarball + on-prem distribution zip from JFrog
#   2. docker load's the image
#   3. Unzips the on-prem distribution (bundled docker-compose + Postgres)
#   4. Patches the bundled .env (version, license URL, port, image name, JVM heap)
#   5. Strips build: sections (we use the pre-loaded image) and brings the stack up
#
# Usage:
#   cp local.env.template local.env      # then fill in JFROG_TOKEN, LICENSE_URL, PENTAHO_VERSION
#   ./local-deploy-pentaho.sh local.env
#
# Access when done:  http://localhost:${PORT}/pentaho   (admin / password, allow ~5-10 min)
# ================================================================================================

set -euo pipefail

# ------------------------------------------------------------------------------------------------
# Args + env
# ------------------------------------------------------------------------------------------------
if [ $# -lt 1 ]; then
    echo "Usage: $0 <env-file>"
    echo "Example: $0 local.env"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$1"
[ -f "$ENV_FILE" ] || ENV_FILE="${SCRIPT_DIR}/$(basename "$1")"
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Env file not found: $1"
    exit 1
fi

# shellcheck disable=SC1090
source "$ENV_FILE"

# Defaults
DB_TYPE="${DB_TYPE:-postgres}"
PORT="${PORT:-8080}"
WORK_DIR="${WORK_DIR:-${SCRIPT_DIR}/work}"
PENTAHO_CONTAINER_CPU_LIMIT="${PENTAHO_CONTAINER_CPU_LIMIT:-1.8}"
PENTAHO_CONTAINER_MEMORY_LIMIT="${PENTAHO_CONTAINER_MEMORY_LIMIT:-5.5GB}"
DATABASE_CONTAINER_CPU_LIMIT="${DATABASE_CONTAINER_CPU_LIMIT:-0.2}"
DATABASE_CONTAINER_MEMORY_LIMIT="${DATABASE_CONTAINER_MEMORY_LIMIT:-1.5GB}"
PENTAHO_JVM_MIN_HEAP="${PENTAHO_JVM_MIN_HEAP:-1g}"
PENTAHO_JVM_MAX_HEAP="${PENTAHO_JVM_MAX_HEAP:-3g}"

# ------------------------------------------------------------------------------------------------
# Preflight
# ------------------------------------------------------------------------------------------------
echo "🔎 Preflight checks"
echo "==================="
fail=0
for tool in docker curl unzip; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "❌ Missing required tool: $tool"; fail=1
    fi
done
if command -v docker >/dev/null 2>&1; then
    if ! docker compose version >/dev/null 2>&1; then
        echo "❌ 'docker compose' (v2) not available"; fail=1
    fi
    if ! docker info >/dev/null 2>&1; then
        echo "❌ Docker daemon not running / not reachable"; fail=1
    fi
fi
for var in PENTAHO_VERSION JFROG_TOKEN JFROG_BASE_URL LICENSE_URL; do
    if [ -z "${!var:-}" ]; then
        echo "❌ Required variable not set in env file: $var"; fail=1
    fi
done
if [ "$fail" -ne 0 ]; then
    echo ""
    echo "🚫 Preflight failed. Fix the issues above and re-run."
    exit 1
fi
echo "✅ Tools, Docker daemon, and required variables present"
echo ""
echo "📋 Version:     ${PENTAHO_VERSION}"
echo "📋 DB type:     ${DB_TYPE}"
echo "📋 Port:        ${PORT}"
echo "📋 Work dir:    ${WORK_DIR}"
echo ""

mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Cross-platform file size helper
filesize() { stat -c%s "$1" 2>/dev/null || stat -f%z "$1" 2>/dev/null || echo 0; }

# ------------------------------------------------------------------------------------------------
# Step 1: download artifacts from JFrog
# ------------------------------------------------------------------------------------------------
echo "📥 Step 1: Downloading artifacts from JFrog"
echo "==========================================="
download_file() {
    local subdir="$1" filename="$2"
    local url="${JFROG_BASE_URL}/${PENTAHO_VERSION}/${subdir}/${filename}"
    local min_size=1048576  # 1MB

    if [ -f "$filename" ] && [ "$(filesize "$filename")" -gt "$min_size" ]; then
        echo "✅ ${filename} already present ($(numfmt --to=iec "$(filesize "$filename")" 2>/dev/null || filesize "$filename") ), skipping"
        return 0
    fi
    echo "📦 Downloading ${filename} ..."
    if ! curl -f -L --progress-bar -H "X-JFrog-Art-Api: ${JFROG_TOKEN}" "$url" -o "$filename"; then
        echo "❌ Failed to download ${filename} from ${url}"
        rm -f "$filename"
        return 1
    fi
    if file "$filename" | grep -qi "HTML"; then
        echo "❌ ${filename} looks like an HTML error page (bad token / URL / version?)"
        rm -f "$filename"
        return 1
    fi
    echo "✅ Downloaded ${filename} ($(numfmt --to=iec "$(filesize "$filename")" 2>/dev/null || filesize "$filename"))"
}

IMAGE_TARBALL="pentaho-server-${PENTAHO_VERSION}.tar.gz"
DIST_ZIP="on-prem-${PENTAHO_VERSION}.zip"
download_file "images" "$IMAGE_TARBALL"
download_file "dists"  "$DIST_ZIP"
echo ""

# ------------------------------------------------------------------------------------------------
# Step 2: load image
# ------------------------------------------------------------------------------------------------
echo "🐳 Step 2: Loading Docker image"
echo "==============================="
docker load -i "$IMAGE_TARBALL"
# Detect the exact repository:tag that was loaded for this version
LOADED_IMAGE="$(docker images --format '{{.Repository}}:{{.Tag}}' | grep "pentaho-server:${PENTAHO_VERSION}" | head -n1 || true)"
if [ -z "$LOADED_IMAGE" ]; then
    echo "❌ Could not find a loaded image matching pentaho-server:${PENTAHO_VERSION}"
    docker images | grep -i pentaho || true
    exit 1
fi
PENTAHO_IMAGE_NAME="${LOADED_IMAGE%:*}"   # strip the tag, keep the repository
echo "✅ Loaded image: ${LOADED_IMAGE}"
echo "   Image repository (for .env): ${PENTAHO_IMAGE_NAME}"
echo ""

# ------------------------------------------------------------------------------------------------
# Step 3: extract distribution + locate compose file
# ------------------------------------------------------------------------------------------------
echo "📦 Step 3: Extracting on-prem distribution"
echo "=========================================="
rm -rf onprem
unzip -q "$DIST_ZIP" -d onprem

BASE_DIR="onprem/dist/on-prem/pentaho-server"
DB_DIR="${BASE_DIR}/pentaho-server-${DB_TYPE}"
COMPOSE_FILE_NAME="docker-compose-${DB_TYPE}.yaml"

if [ -d "$DB_DIR" ] && [ -f "${DB_DIR}/${COMPOSE_FILE_NAME}" ]; then
    cd "$DB_DIR"
else
    echo "[WARN] ${COMPOSE_FILE_NAME} not found in ${DB_DIR}; scanning..."
    PICK="$(find "$BASE_DIR" -maxdepth 3 -type f -name 'docker-compose-*.yaml' | sort | grep -E "docker-compose-${DB_TYPE}\.yaml" | head -n1 || true)"
    [ -z "$PICK" ] && PICK="$(find "$BASE_DIR" -maxdepth 3 -type f -name 'docker-compose-*.yaml' | sort | head -n1 || true)"
    if [ -z "$PICK" ]; then
        echo "❌ No docker-compose-*.yaml found under ${BASE_DIR}"
        exit 1
    fi
    COMPOSE_FILE_NAME="$(basename "$PICK")"
    cd "$(dirname "$PICK")"
    DB_TYPE="$(echo "$COMPOSE_FILE_NAME" | sed -E 's/docker-compose-([^.]+)\.yaml/\1/')"
fi
echo "✅ Compose dir: $(pwd)"
echo "✅ Compose file: ${COMPOSE_FILE_NAME} (DB_TYPE=${DB_TYPE})"
echo ""

# ------------------------------------------------------------------------------------------------
# Step 4: configure bundled .env
# ------------------------------------------------------------------------------------------------
echo "⚙️  Step 4: Configuring .env"
echo "==========================="
[ -f .env ] && cp .env .env.backup
# Use a portable in-place sed (GNU + BSD)
sedi() { if sed --version >/dev/null 2>&1; then sed -i "$@"; else sed -i '' "$@"; fi; }
sedi "s|PENTAHO_VERSION=.*|PENTAHO_VERSION=${PENTAHO_VERSION}|g" .env
sedi "s|LICENSE_URL=.*|LICENSE_URL=${LICENSE_URL}|g" .env
sedi "s|PORT=.*|PORT=${PORT}|g" .env
sedi "s|PENTAHO_IMAGE_NAME=.*|PENTAHO_IMAGE_NAME=${PENTAHO_IMAGE_NAME}|g" .env
sedi "s|JAVA_XMX=.*|JAVA_XMX=${PENTAHO_JVM_MAX_HEAP}|g" .env
sedi "s|JAVA_XMS=.*|JAVA_XMS=${PENTAHO_JVM_MIN_HEAP}|g" .env
echo "📋 Effective .env:"
sed 's/^/   /' .env
echo ""

# ------------------------------------------------------------------------------------------------
# Step 5: strip build: sections, fix perms, bring up
# ------------------------------------------------------------------------------------------------
echo "🔧 Step 5: Preparing and starting the stack"
echo "==========================================="
if grep -q "^[[:space:]]*build:" "$COMPOSE_FILE_NAME"; then
    cp "$COMPOSE_FILE_NAME" "${COMPOSE_FILE_NAME}.bak"
    sedi '/^[[:space:]]*build:/,/^[[:space:]]*args:/d' "$COMPOSE_FILE_NAME"
    sedi '/^[[:space:]]*PENTAHO_VERSION:/d' "$COMPOSE_FILE_NAME"
    echo "✅ Removed build: sections (using pre-loaded image)"
fi

# Resource limits (best-effort; matches upstream defaults in the bundled compose)
sedi "s|cpus: '3'|cpus: '${PENTAHO_CONTAINER_CPU_LIMIT}'|g" "$COMPOSE_FILE_NAME" 2>/dev/null || true
sedi "s|memory: 5g|memory: ${PENTAHO_CONTAINER_MEMORY_LIMIT}|g" "$COMPOSE_FILE_NAME" 2>/dev/null || true

# Container runs as uid 5000; make bind-mounted dirs writable
for d in logs softwareOverride config; do
    [ -d "$d" ] || continue
    if ! chown -R 5000:5000 "$d" 2>/dev/null; then
        sudo chown -R 5000:5000 "$d" 2>/dev/null || echo "  ⚠️  Could not chown $d (may need sudo); continuing"
    fi
    chmod -R 775 "$d" 2>/dev/null || sudo chmod -R 775 "$d" 2>/dev/null || true
done

docker compose -f "$COMPOSE_FILE_NAME" down 2>/dev/null || true
docker compose -f "$COMPOSE_FILE_NAME" up -d

echo ""
echo "🎉 Pentaho 11 is starting locally!"
echo "=================================="
docker compose -f "$COMPOSE_FILE_NAME" ps || true
echo ""
echo "🌐 Access:  http://localhost:${PORT}/pentaho   (allow ~5-10 min for first boot)"
echo "👤 Login:   admin / password"
echo ""
echo "📜 Follow logs:  docker compose -f \"$(pwd)/${COMPOSE_FILE_NAME}\" logs -f pentaho-server"
echo "🛑 Stop:         docker compose -f \"$(pwd)/${COMPOSE_FILE_NAME}\" down"
echo ""
echo "COMPOSE_DIR=$(pwd)"
echo "COMPOSE_FILE=${COMPOSE_FILE_NAME}"
