#!/bin/bash
# ================================================================================================
# Pentaho 11 LOCAL install — plugin installer
# ================================================================================================
# Installs the plugins defined in the env file (PLUGINS_TYPICAL + PLUGINS_SPECIAL) into the
# locally running Pentaho container, then restarts it once. Adapted from the SE repo's
# 20-deploy-all-plugins.sh / 21-deploy-plugin.sh (EC2/SSH layer removed — runs against the
# local Docker container created by local-deploy-pentaho.sh).
#
# Usage:
#   ./local-deploy-plugins.sh local.env                 # install all configured plugins
#   ./local-deploy-plugins.sh local.env <url-or-name>   # install a single plugin
#
# TYPICAL plugins (URLs)  -> extracted to pentaho-solutions/system
# SPECIAL plugins (name|url, with optional file:// for local zips):
#   webttle-plugins-ee-client          -> /opt/pentaho/
#   pentaho-app-shell-core-webclient   -> pentaho-solutions/system/app-shell
#   semantic-model-editor              -> pentaho-solutions/system
# Local file:// plugins are read from:  <WORK_DIR or .>/downloads/plugins/<version>/
# ================================================================================================

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <env-file> [single-plugin-url-or-name]"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$1"
[ -f "$ENV_FILE" ] || ENV_FILE="${SCRIPT_DIR}/$(basename "$1")"
if [ ! -f "$ENV_FILE" ]; then echo "❌ Env file not found: $1"; exit 1; fi
# shellcheck disable=SC1090
source "$ENV_FILE"
SINGLE_PLUGIN="${2:-}"

DB_TYPE="${DB_TYPE:-postgres}"
WORK_DIR="${WORK_DIR:-${SCRIPT_DIR}/work}"
LOCAL_PLUGIN_DIR="${WORK_DIR}/downloads/plugins/${PENTAHO_VERSION}"
DL_DIR="${WORK_DIR}/plugin-downloads"
mkdir -p "$DL_DIR"

if [ -z "${JFROG_TOKEN:-}" ] || [ -z "${PENTAHO_VERSION:-}" ]; then
    echo "❌ JFROG_TOKEN and PENTAHO_VERSION must be set in the env file"; exit 1
fi

# ------------------------------------------------------------------------------------------------
# Locate the running Pentaho container
# ------------------------------------------------------------------------------------------------
find_container() {
    docker ps --format '{{.Names}}' | grep -E "pentaho-server.*pentaho-server" | head -n1
}
CONTAINER="$(find_container)"
if [ -z "$CONTAINER" ]; then
    echo "❌ No running Pentaho container found. Run ./local-deploy-pentaho.sh first."
    docker ps --format '   {{.Names}} ({{.Status}})' || true
    exit 1
fi
echo "🐳 Target container: ${CONTAINER}"

# ------------------------------------------------------------------------------------------------
# Wait for server readiness ("Server startup in ..." in the Tomcat log)
# ------------------------------------------------------------------------------------------------
echo "⏳ Waiting for Pentaho server to be ready (up to 5 min)..."
elapsed=0
until docker logs "$CONTAINER" 2>&1 | grep -q "Server startup in"; do
    if [ "$elapsed" -ge 300 ]; then
        echo "⚠️  Readiness check timed out; proceeding anyway (plugins may need a later restart)."
        break
    fi
    sleep 10; elapsed=$((elapsed + 10))
    echo "   ...still starting (${elapsed}s)"
done
[ "$elapsed" -lt 300 ] && echo "✅ Server is ready"

# ------------------------------------------------------------------------------------------------
# Build the plugin work list
# ------------------------------------------------------------------------------------------------
# Each entry is "kind|ref" where kind is "url" or "name".
declare -a WORK=()
if [ -n "$SINGLE_PLUGIN" ]; then
    if [[ "$SINGLE_PLUGIN" =~ ^https?:// ]]; then WORK+=("url|$SINGLE_PLUGIN"); else WORK+=("name|$SINGLE_PLUGIN"); fi
else
    while IFS= read -r line; do
        url="$(echo "$line" | xargs)"; [ -z "$url" ] && continue
        eval "url=\"$url\""   # expand ${PENTAHO_VERSION}
        WORK+=("url|$url")
    done <<< "${PLUGINS_TYPICAL:-}"
    while IFS='|' read -r name url; do
        name="$(echo "$name" | xargs)"; [ -z "$name" ] && continue
        WORK+=("name|$name")
    done <<< "${PLUGINS_SPECIAL:-}"
fi

if [ "${#WORK[@]}" -eq 0 ]; then
    echo "❌ No plugins to install (PLUGINS_TYPICAL / PLUGINS_SPECIAL empty and no plugin arg given)."
    exit 1
fi
echo "📦 ${#WORK[@]} plugin(s) to install"

# ------------------------------------------------------------------------------------------------
# Resolve a SPECIAL plugin name -> url (or file://) from PLUGINS_SPECIAL
# ------------------------------------------------------------------------------------------------
resolve_special() {
    local want="$1"
    while IFS='|' read -r name url; do
        name="$(echo "$name" | xargs)"; [ -z "$name" ] && continue
        if [ "$name" = "$want" ]; then eval "echo \"$url\""; return 0; fi
    done <<< "${PLUGINS_SPECIAL:-}"
    return 1
}

# ------------------------------------------------------------------------------------------------
# Install a single plugin (no restart). Args: kind ref
# ------------------------------------------------------------------------------------------------
install_one() {
    local kind="$1" ref="$2"
    local url="" name="" zip="" local_src=""

    if [ "$kind" = "url" ]; then
        url="$ref"; zip="$(basename "$url")"; name="${zip%.zip}"
    else
        name="$ref"
        url="$(resolve_special "$name" || true)"
        if [ -z "$url" ]; then echo "❌ Special plugin '$name' not found in PLUGINS_SPECIAL"; return 1; fi
        if [[ "$url" =~ ^file:// ]]; then
            zip="${url#file://}"; local_src="${LOCAL_PLUGIN_DIR}/${zip}"
        else
            zip="$(basename "$url")"
        fi
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📦 ${name}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    local host_zip
    if [ -n "$local_src" ]; then
        [ -f "$local_src" ] || { echo "❌ Local plugin not found: $local_src"; return 1; }
        host_zip="$local_src"
        echo "   Using local file: $host_zip"
    else
        host_zip="${DL_DIR}/${zip}"
        if [ ! -f "$host_zip" ] || [ "$(stat -c%s "$host_zip" 2>/dev/null || stat -f%z "$host_zip" 2>/dev/null || echo 0)" -lt 10240 ]; then
            echo "   Downloading ${zip} ..."
            if ! curl -f -L --progress-bar -H "X-JFrog-Art-Api: ${JFROG_TOKEN}" "$url" -o "$host_zip"; then
                echo "❌ Download failed: $url"; rm -f "$host_zip"; return 1
            fi
            if file "$host_zip" | grep -qi HTML; then echo "❌ Got HTML (bad token/URL)"; rm -f "$host_zip"; return 1; fi
        else
            echo "   Reusing cached download: $host_zip"
        fi
    fi

    echo "   Copying into container..."
    docker cp "$host_zip" "${CONTAINER}:/tmp/${zip}"
    docker exec -u 0 "$CONTAINER" bash -c "command -v unzip >/dev/null 2>&1 || (apt-get update && apt-get install -y unzip)" >/dev/null 2>&1 || true

    # Choose extraction target by plugin identity
    case "$name" in
        *webttle*)
            echo "   [special] extract -> /opt/pentaho/"
            docker exec -u 0 "$CONTAINER" bash -c "unzip -o /tmp/${zip} -d /opt/pentaho/ >/dev/null && chown -R pentaho:pentaho /opt/pentaho/"
            ;;
        *app-shell*)
            echo "   [special] extract -> system/app-shell"
            docker exec -u 0 "$CONTAINER" bash -c "mkdir -p /opt/pentaho/pentaho-server/pentaho-solutions/system/app-shell && unzip -o /tmp/${zip} -d /opt/pentaho/pentaho-server/pentaho-solutions/system/app-shell >/dev/null && chown -R pentaho:pentaho /opt/pentaho/pentaho-server/pentaho-solutions/system/app-shell"
            ;;
        *)
            echo "   extract -> pentaho-solutions/system"
            docker exec -u 0 "$CONTAINER" bash -c "unzip -o /tmp/${zip} -d /opt/pentaho/pentaho-server/pentaho-solutions/system >/dev/null && chown -R pentaho:pentaho /opt/pentaho/pentaho-server/pentaho-solutions/system"
            ;;
    esac

    # Clear Karaf cache so the new plugin is picked up, then clean tmp
    docker exec -u 0 "$CONTAINER" bash -c "rm -rf /opt/pentaho/pentaho-server/pentaho-solutions/system/karaf/caches/* 2>/dev/null || true; rm -f /tmp/${zip}"
    echo "✅ ${name} installed"
}

# ------------------------------------------------------------------------------------------------
# Run
# ------------------------------------------------------------------------------------------------
installed=0; failed=()
for entry in "${WORK[@]}"; do
    kind="${entry%%|*}"; ref="${entry#*|}"
    if install_one "$kind" "$ref"; then installed=$((installed+1)); else failed+=("$ref"); fi
done

echo ""
echo "📊 Installed ${installed}/${#WORK[@]} plugin(s)"
if [ "${#failed[@]}" -gt 0 ]; then
    echo "❌ Failed:"; printf '   - %s\n' "${failed[@]}"
fi

echo ""
echo "🔄 Restarting Pentaho container to load plugins..."
docker restart "$CONTAINER" >/dev/null
echo "✅ Restarted ${CONTAINER}"
echo "🌐 Access: http://localhost:${PORT:-8080}/pentaho  (admin / password; allow a couple minutes)"
