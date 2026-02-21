# GitHub Actions: Run DB Migrations

This workflow allows you to run the project's PostgreSQL migrations from GitHub Actions using a manual dispatch. It does NOT store credentials in the repository; instead it reads them from repository Secrets.

## What I added
- `.github/workflows/run-migrations.yml` — manual workflow that installs Python deps, runs `python -m src.database.migrations`, and tests the DB connection.

## Required repository Secrets
Set these in your repository: Settings → Secrets and variables → Actions → New repository secret
- `DB_HOST` — database host (e.g. `db.myhost.com` or `127.0.0.1`)
- `DB_PORT` — database port (default `5432`)
- `DB_NAME` — database name (must already exist)
- `DB_USER` — DB user with permissions to create tables
- `DB_PASSWORD` — password for `DB_USER`

Important: the migrations script expects the target database to already exist. If you need the workflow to create the database itself, tell me and I will add a step that uses `psql` with higher-privilege credentials to create it before running migrations.

## How to run
1. Push this branch to GitHub.
2. Go to the repository → Actions → "Run DB Migrations" workflow.
3. Choose the branch and click "Run workflow".

The run log will show dependency installation, migration output, and a final DB connection test.

## Troubleshooting
- `psycopg2` build failures: the workflow uses `psycopg2-binary` which should avoid compilation; if you added `psycopg2` instead, switch to the binary build or add system packages.
- Authentication errors: double-check secrets are correct and that the DB is reachable from GitHub's runner (network/firewall may block access).
- If your DB is not publicly reachable, consider running this workflow in a self-hosted runner inside your network, or use a controlled CI runner that has network access to the database.

If you want, I can update the workflow to create the database automatically (requires a superuser secret) or to run on pushes/PRs instead of manual dispatch.
