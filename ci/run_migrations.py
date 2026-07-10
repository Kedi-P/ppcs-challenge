#!/usr/bin/env python3
"""Apply PPCS SQL migrations to a Lakebase endpoint.

Runs every *.sql file in service/migrations/ in filename order against the
target schema, substituting the literal token `:schema` with the given schema
name. Idempotent (all migrations use IF NOT EXISTS / ON CONFLICT), so it is
safe to re-run against production team schemas or a fresh CI branch clone.

Usage:
    python ci/run_migrations.py --schema team01
    python ci/run_migrations.py --schema ci_pr_1234 --host <h> --target <endpoint>

Connection: mints a fresh OAuth credential the same way the app does
(POST /api/2.0/postgres/credentials), then connects with psycopg. Host and
endpoint target come from flags or the PPCS_LAKEBASE_HOST / PPCS_LAKEBASE_TARGET
env vars that ci/lakebase_branch.py writes into $GITHUB_ENV.
"""
from __future__ import annotations

import argparse
import glob
import os
import sys
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "service" / "migrations"
DB_NAME = "databricks_postgres"


def _mint_token(endpoint: str) -> str:
    from databricks.sdk import WorkspaceClient

    client = WorkspaceClient()
    cred = client.api_client.do(
        "POST", "/api/2.0/postgres/credentials", body={"endpoint": endpoint}
    )
    return cred["token"]


def _db_user() -> str:
    # In CI the connecting identity is the SP client id; locally fall back to
    # the workspace user name.
    user = os.environ.get("DATABRICKS_CLIENT_ID")
    if user:
        return user
    from databricks.sdk import WorkspaceClient

    return WorkspaceClient().current_user.me().user_name


def _quote_ident(name: str) -> str:
    # schema comes from CI (branch/team name) — still validate defensively.
    if not name.replace("_", "").isalnum():
        raise SystemExit(f"unsafe schema name: {name!r}")
    return name


def apply_migrations(schema: str, host: str, target: str) -> None:
    import psycopg

    schema = _quote_ident(schema)
    files = sorted(glob.glob(str(MIGRATIONS_DIR / "*.sql")))
    if not files:
        raise SystemExit(f"no migrations found in {MIGRATIONS_DIR}")

    token = _mint_token(target)
    with psycopg.connect(
        host=host,
        dbname=DB_NAME,
        user=_db_user(),
        password=token,
        sslmode="require",
        autocommit=True,
    ) as conn:
        for path in files:
            sql = Path(path).read_text(encoding="utf-8").replace(":schema", schema)
            print(f"applying {Path(path).name} -> schema {schema}", flush=True)
            with conn.cursor() as cur:
                cur.execute(sql)
    print(f"OK: {len(files)} migration(s) applied to {schema}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--schema", required=True, help="target Postgres schema")
    ap.add_argument("--host", default=os.environ.get("PPCS_LAKEBASE_HOST"))
    ap.add_argument("--target", default=os.environ.get("PPCS_LAKEBASE_TARGET"))
    args = ap.parse_args()

    if not args.host or not args.target:
        sys.exit(
            "host/target required (flags or PPCS_LAKEBASE_HOST / PPCS_LAKEBASE_TARGET)"
        )
    apply_migrations(args.schema, args.host, args.target)


if __name__ == "__main__":
    main()
