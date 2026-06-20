# Local Test Database (offline copy)

Stand up a **local Postgres** and copy the Solution Engineering test databases into it, so you can
keep testing and developing **without depending on the VPN**.

Copies (per `db.env`):

| Source | Host | DB | Schemas | → Local DB |
|---|---|---|---|---|
| **bidb** (real data) | `10.80.230.246` | `bidb` | `bidb` | `bidb` |
| **bidb_ext** (RDS / FDW layer) | `airlinesample.…rds.amazonaws.com` | `postgres` | `bidb_ext_dev`, `bidb_ext_demo`, `bidb_ext_jcd` | `bidb_ext` |

Source credentials are read directly from the SE repo's
`pdc-analysis/.../pdc_analysis.properties` (`BIDB_*` / `BIDB_EXT_*`).

## Prerequisites

- Docker + Docker Compose v2 (for the local Postgres container)
- A **Postgres 17 client** (`pg_dump` / `pg_restore` / `psql`) to match the source version.
  - macOS: `brew install libpq` then `export PATH="$(brew --prefix libpq)/bin:$PATH"`
  - If no host client is found, the script falls back to the `postgres:17` Docker image with
    `--network host` (works on Linux; on macOS it can't reach VPN routes, so install `libpq`).
- A local checkout of `kevinrhaas/solution-engineering` (for the properties file)
- **VPN connected** when you run the copy (the sources are private)

## Usage

```bash
cd test-db-local
cp db.env.template db.env
# Edit db.env: set PROPERTIES_FILE to your solution-engineering checkout path

# 1) (VPN connected) copy the data
./copy-test-db.sh db.env

# 2) connect
./psql-local.sh bidb          # or: ./psql-local.sh bidb_ext
# or from any client:
#   psql -h localhost -p 5433 -U postgres -d bidb     (password: postgres)
```

The script: brings up local Postgres → checks each source is reachable (skips with a clear message
if the VPN is down) → `pg_dump -Fc` each schema → `pg_restore` into the local DB → optionally
repoints the `bidb_ext` foreign-data-wrapper server at your local `bidb` copy.

## What gets created

- Container `test-db-local`, data in the `test-db-data` Docker volume (persists across restarts)
- Local Postgres on **`localhost:5433`** (user `postgres` / pass `postgres` — change in `db.env`)
- Databases `bidb` and `bidb_ext`

## Notes

- **postgres_fdw:** `bidb_ext` schemas use a foreign-data wrapper that points at the real `bidb`.
  Regular tables/materialized data copy fine. With `REPOINT_FDW_TO_LOCAL=yes` the script rewrites
  the foreign server(s) to target your local `bidb` so foreign tables resolve offline. If a query
  hits an auth error on a user mapping, set its password to the local one:
  ```sql
  ALTER USER MAPPING FOR <user> SERVER <srv> OPTIONS (SET password 'postgres');
  ```
- **Re-running** is safe: `pg_restore --clean --if-exists` replaces objects. To start fresh,
  `./teardown.sh --purge` then re-copy.
- **Schema-only** copy: set `DUMP_SCOPE=schema-only` in `db.env`.

## Teardown

```bash
./teardown.sh            # stop + remove container (keeps the data volume)
./teardown.sh --purge    # also delete the data volume and work/ dumps
```

## Pentaho repository DB vs. this

This local DB is for **BI content/development data** (the airline sample). It is separate from the
Pentaho Server's own repository database (Jackrabbit/Quartz), which the Pentaho install in
`../pentaho-11-local-install/` provisions via its bundled Postgres.
