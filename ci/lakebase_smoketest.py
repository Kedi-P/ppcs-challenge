#!/usr/bin/env python3
"""Lakebase access smoketest — verify a team app SP can actually use its schema.

Runs the full chain the app depends on, stopping at the first failure and
printing a specific diagnosis:

    1. Workspace auth        who am I (current_user)?
    2. Project resolves      does the Lakebase project exist?
    3. Branch + endpoint     is the branch's endpoint host resolvable?
    4. Mint DB credential    POST /api/2.0/postgres/credentials
    5. TCP + TLS to :5432    is the network path open?
    6. Postgres login        does the SP authenticate as a Postgres role?
    7. Schema read/write     can it insert+select in <schema>.app_identity_evidence?

The common failure is step 6 (`password authentication failed`): the credential
mints and the network is open, but the SP has not been registered as a Postgres
role on the branch. That is an owner action — see LAKEBASE.md / pre-workshop
setup: `grant usage on schema <team> to "<app-sp-client-id>"; grant all on all
tables in schema <team> to "<app-sp-client-id>";`.

Usage:
    uv run python ci/lakebase_smoketest.py --branch team01 --schema team01
    uv run python ci/lakebase_smoketest.py            # uses env / defaults

Auth: databricks-sdk WorkspaceClient (env/profile configured). Read-only apart
from a single idempotent upsert into <schema>.app_identity_evidence.
"""
from __future__ import annotations

import argparse
import os
import socket
import ssl
import struct
import sys

PROJECT = os.environ.get("PPCS_PROJECT", "projects/ppcs-coda-challenge")
DB_NAME = "databricks_postgres"


def _ok(msg: str) -> None:
    print(f"OK   {msg}")


def _fail(msg: str, detail: str = "") -> None:
    print(f"FAIL {msg}")
    if detail:
        print(f"     {detail.strip()}")
    sys.exit(1)


def _endpoint_path(branch: str) -> str:
    return f"{PROJECT}/branches/{branch}/endpoints/primary"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--branch", default=os.environ.get("PPCS_LAKEBASE_BRANCH", "team01"))
    ap.add_argument("--schema", default=os.environ.get("PPCS_TEAM_SCHEMA", "team01"))
    ap.add_argument("--host", default=os.environ.get("PPCS_LAKEBASE_HOST"))
    args = ap.parse_args()

    endpoint = _endpoint_path(args.branch)

    # 1. Workspace auth
    try:
        from databricks.sdk import WorkspaceClient

        client = WorkspaceClient()
        me = client.current_user.me().user_name
        _ok(f"workspace auth: {me}")
    except Exception as exc:  # noqa: BLE001
        _fail("workspace auth", str(exc))

    # 2 + 3. Resolve the endpoint host (proves project + branch + endpoint exist).
    host = args.host
    if not host:
        try:
            ep = client.api_client.do("GET", f"/api/2.0/postgres/{endpoint}")
            host = (ep.get("status") or {}).get("hosts", {}).get("host")
            if not host:
                _fail("resolve endpoint host", f"no host in status: {ep.get('status')}")
            _ok(f"endpoint resolves: {host}")
        except Exception as exc:  # noqa: BLE001
            _fail(f"resolve endpoint {endpoint}", str(exc))
    else:
        _ok(f"endpoint host (from env/flag): {host}")

    # 4. Mint DB credential.
    try:
        cred = client.api_client.do(
            "POST", "/api/2.0/postgres/credentials", body={"endpoint": endpoint}
        )
        token = cred["token"]
        _ok(f"minted DB credential ({len(token)} chars)")
    except Exception as exc:  # noqa: BLE001
        _fail("mint DB credential", str(exc))

    # 5. TCP + TLS to :5432. Postgres uses opportunistic TLS: after the TCP
    # connect the client sends an 8-byte SSLRequest (int32 length=8, int32
    # code=80877103) and the server replies 'S' (upgrade) or 'N' (plaintext).
    # We must send SSLRequest BEFORE the TLS handshake — starting TLS
    # immediately makes the server read a stray ClientHello and drop the
    # connection (UNEXPECTED_EOF), which looks like a firewall but isn't.
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 5432), timeout=10) as sock:
            sock.sendall(struct.pack("!ii", 8, 80877103))
            reply = sock.recv(1)
            if reply != b"S":
                _fail("TLS negotiation to :5432", f"server declined SSL (replied {reply!r})")
            with ctx.wrap_socket(sock, server_hostname=host) as tls:
                _ok(f"TCP + TLS to :5432 ({tls.version()})")
    except Exception as exc:  # noqa: BLE001
        _fail("TCP/TLS to :5432", str(exc))

    # 6 + 7. Postgres login + schema read/write.
    try:
        import psycopg
    except ImportError:
        _fail("import psycopg", "pip install 'psycopg[binary]>=3'")

    db_user = me  # SP identity == Postgres role name
    try:
        conn = psycopg.connect(
            host=host,
            dbname=DB_NAME,
            user=db_user,
            password=token,
            sslmode="require",
            connect_timeout=15,
        )
    except psycopg.OperationalError as exc:
        detail = str(exc)
        if "password authentication failed" in detail:
            _fail(
                "Postgres login (SP not registered as a role)",
                f"identity {db_user!r} authenticates to the workspace and mints a "
                f"credential, but the branch rejects login. The project owner must "
                f"register this SP as a Postgres role and grant it on schema "
                f"{args.schema!r}. See LAKEBASE.md.",
            )
        _fail("Postgres login", detail)
    except Exception as exc:  # noqa: BLE001
        _fail("Postgres login", str(exc))

    _ok(f"Postgres login as {db_user}")

    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                f"insert into {args.schema}.app_identity_evidence (id) "
                f"values ('smoketest') "
                f"on conflict (id) do update set checked_at = now()"
            )
            cur.execute(
                f"select current_user, current_database(), id, checked_at "
                f"from {args.schema}.app_identity_evidence where id = 'smoketest'"
            )
            row = cur.fetchone()
        _ok(
            f"schema read/write: user={row[0]} db={row[1]} "
            f"row={row[2]} at={row[3].isoformat()}"
        )
    except Exception as exc:  # noqa: BLE001
        _fail(f"read/write {args.schema}.app_identity_evidence", str(exc))

    print(f"\nPASS  {args.branch}/{args.schema} is fully usable by {db_user}")


if __name__ == "__main__":
    main()
