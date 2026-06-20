# Pentaho 11 — Local Docker Install

A **local** (no AWS / no Okta / no VPN) install of a **Pentaho 11 Server** on your own machine.

This is adapted from the Solution Engineering repo
[`kevinrhaas/solution-engineering` → `pentaho-11-docker-deploy`](https://github.com/kevinrhaas/solution-engineering/tree/main/pentaho-11-docker-deploy),
which deploys Pentaho onto an AWS EC2 instance. The EC2 / Okta / SSH orchestration has been
stripped out so the same container artifacts run directly on your laptop or workstation.

## What it does

The upstream deploy does the real work *on the EC2 host* in two steps (`download.sh` + `deploy.sh`).
This local version runs those same steps on your machine:

1. Downloads two artifacts from JFrog using your token:
   - `…/<version>/images/pentaho-server-<version>.tar.gz` — the Pentaho Server Docker image
   - `…/<version>/dists/on-prem-<version>.zip` — the on-prem distribution (bundled `docker-compose` + Postgres)
2. `docker load`s the image
3. Unzips the distribution and locates `…/pentaho-server-postgres/docker-compose-postgres.yaml`
4. Patches the bundled `.env` (version, license URL, port, image name, JVM heap)
5. Removes `build:` sections (we use the pre-loaded image) and runs `docker compose up -d`

The repository database (PostgreSQL) is bundled inside the on-prem distribution's compose file —
nothing extra to install.

## Prerequisites

| Requirement | Notes |
|---|---|
| **Docker + Compose v2** | Docker Desktop (macOS/Windows) or Docker Engine (Linux). `docker compose version` must work. |
| **`curl`, `unzip`** | Standard CLI tools. |
| **JFrog token** | From <https://one.hitachivantara.com/> → **Set Me Up**. Needed to download the image + dist. |
| **License URL** | Flexera license server URL for your Pentaho license (from your Pentaho account manager). |
| **Resources** | ~6 GB RAM free for the Pentaho container + ~2 GB for Postgres; ~10 GB disk for artifacts/images. |
| **Internet** | Required at install time to reach JFrog; the server reaches the license server at runtime. |

> Unlike the EC2 version, you do **not** need AWS CLI, an Okta profile, an SSH key, or the VPN.

## Quick start

```bash
cd pentaho-11-local-install

cp local.env.template local.env
# Edit local.env — set JFROG_TOKEN, LICENSE_URL, and PENTAHO_VERSION (REQUIRED)

./local-deploy-pentaho.sh local.env
```

Then open **http://localhost:8080/pentaho** (default port; allow ~5–10 min for first boot).

**Login:** `admin` / `password`

### Install plugins

Once the server is up, install the plugins listed in your env file
(`PLUGINS_TYPICAL` + `PLUGINS_SPECIAL` — PAZ, PIR, PDD, PAS scheduler, webttle, etc.):

```bash
./local-deploy-plugins.sh local.env                 # install all configured plugins
./local-deploy-plugins.sh local.env <url-or-name>   # install a single plugin
```

The script waits for the server to report `Server startup in …`, downloads each plugin from JFrog,
copies it into the running container, extracts it to the right location (system folder, or the
special locations for `webttle` / `app-shell`), clears the Karaf cache, and restarts the container
once at the end. Local `file://` plugins are read from `work/downloads/plugins/<version>/`.

## Configuration

All settings live in `local.env` (copied from `local.env.template`). Key values:

| Variable | Default | Description |
|---|---|---|
| `PENTAHO_VERSION` | `11.1.0.0-120` | Version to install; must exist in JFrog under that path. |
| `JFROG_TOKEN` | _(required)_ | JFrog access token. |
| `JFROG_BASE_URL` | dev repo | Switch to the `pntprv-generic-rc` URL for release candidates. |
| `LICENSE_URL` | _(required)_ | Flexera license server URL. |
| `DB_TYPE` | `postgres` | `postgres` \| `mysql` \| `sqlserver` \| `oracle` (must exist in the dist). |
| `PORT` | `8080` | Host port for the Pentaho User Console. `http://localhost:<PORT>/pentaho`. |
| `PENTAHO_JVM_MAX_HEAP` | `3g` | Max JVM heap; keep ≈60–75% of the container memory limit. |

## Lifecycle

The deploy script prints the exact compose file path at the end. From the compose directory
(`work/onprem/dist/on-prem/pentaho-server/pentaho-server-postgres/`):

```bash
docker compose -f docker-compose-postgres.yaml ps           # status
docker compose -f docker-compose-postgres.yaml logs -f pentaho-server   # follow logs
docker compose -f docker-compose-postgres.yaml down         # stop
docker compose -f docker-compose-postgres.yaml up -d        # start again
```

### Teardown

```bash
./local-teardown.sh local.env            # stop + remove containers and volumes (keeps downloads)
./local-teardown.sh local.env --purge    # also delete work/ (downloaded artifacts + extraction)
```

## Differences vs. the EC2 SE repo

| Aspect | SE repo (`pentaho-11-docker-deploy`) | This local install |
|---|---|---|
| Target | AWS EC2 (Ubuntu) | Your local machine |
| Auth | Okta → AWS, SSH key, VPN | None |
| Image source | JFrog (downloaded onto EC2) | JFrog (downloaded locally) — same artifacts |
| Default port | `80` | `8080` (no root needed) |
| Plugins | `20-deploy-all-plugins.sh` etc. | `local-deploy-plugins.sh` (same logic, local container) |

## Troubleshooting

- **Download returns an HTML page / 401** — bad or expired `JFROG_TOKEN`, or the `PENTAHO_VERSION`
  doesn't exist under `JFROG_BASE_URL`. Verify the version path in Artifactory.
- **Console never comes up** — `docker compose ... logs -f pentaho-server`. First boot initializes the
  Jackrabbit repository and Postgres schema; this can take several minutes.
- **License errors in the log** — confirm `LICENSE_URL` is reachable from your machine and is the
  correct activation URL.
- **Permission denied on `logs/`/`config/`** — the container runs as uid `5000`; the script chowns
  those dirs (and falls back to `sudo`). On Docker Desktop (macOS/Windows) this is usually a no-op.
- **Port already in use** — change `PORT` in `local.env` and re-run.

## Security note

Do **not** commit `local.env` — it contains your JFrog token and license URL. It is gitignored here.
(The upstream SE sample env files contain live tokens; rotate any token that has been committed.)
