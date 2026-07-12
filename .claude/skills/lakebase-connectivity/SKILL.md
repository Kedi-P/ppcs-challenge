---
name: lakebase-connectivity
description: "Use when connecting to, debugging, or authorizing access to the PPCS challenge Lakebase (managed Postgres) — symptoms like 'password authentication failed', 'UNEXPECTED_EOF' / TLS handshake timeout on :5432, 'No API found' on postgres branch/endpoint calls, minting an OAuth DB credential, or granting a coda app service principal access to a team schema. Covers the coda-app→team-schema pairing and the two-step SP authorization (create-role + SQL grant)."
user-invocable: true
---

# PPCS Lakebase Connectivity

How the PPCS challenge app reaches its team Lakebase (managed Postgres on
`lakemeter`, project `projects/ppcs-coda-challenge`), and how to debug the four
failure modes we actually hit. Read this before touching any Lakebase code path
or granting an app access.

## The connection model (no stored passwords)

The app never stores a DB password. Per connection it:

1. Mints a short-lived (~1h) OAuth credential via the workspace REST API:
   `POST /api/2.0/postgres/credentials` with body `{"endpoint": "<endpoint-path>"}`.
   The token's `sub` is the calling identity (user or service principal).
2. Connects with `psycopg` over TLS, using **that identity as the Postgres
   username** and the token as the password. `sslmode=require`.

Endpoint path shape:
`projects/ppcs-coda-challenge/branches/<team>/endpoints/primary`
Endpoints autoscale 0.5–4 CU and **suspend after 300s idle** (scale-to-zero) —
the first connection after idle may be slow/refused; retry once.

## Four failure modes (in the order a connection hits them)

### 1. `No API found` on branch/endpoint REST calls
The Postgres branch/endpoint routes live under `/api/2.0/postgres/…`. Omitting
the `postgres/` prefix (e.g. `/api/2.0/projects/…/branches`) 404s. The
credentials-mint path `/api/2.0/postgres/credentials` already has it. Fixed in
`ci/lakebase_branch.py` via URL-builder helpers.

### 2. `UNEXPECTED_EOF` / TLS handshake timeout on :5432 — NOT a firewall
Postgres uses **opportunistic TLS**, not immediate-TLS like HTTPS. After the
TCP connect the client must send an 8-byte **SSLRequest** packet
(`struct.pack("!ii", 8, 80877103)`) and read a 1-byte reply (`S` = upgrade,
`N` = plaintext) **before** starting the TLS handshake. Calling
`ssl.wrap_socket()` immediately makes the server read a stray ClientHello and
drop the connection → `UNEXPECTED_EOF`, which *looks* like a blocked port but
is a client bug. `psycopg` does this dance correctly; hand-rolled probes must
too. See the reachability step in `ci/lakebase_smoketest.py` for the correct
pattern.

### 3. Wrong Postgres username → `password authentication failed`
The username must be the identity that minted the credential. In the app
runtime `DATABRICKS_CLIENT_ID` is **unset** (SP self-auth via apiKeyHelper), so
derive it from the SDK: `WorkspaceClient().current_user.me().user_name` (for an
SP that's its application-id UUID). Fixed in `service/app/main.py`
(`platform_lakebase_check`), overridable via `PPCS_LAKEBASE_USER`.

### 4. `password authentication failed` even with the right username → SP has no role
The credential mints and the network is open, but the branch rejects login
because the app **service principal was never registered as a Postgres role**.
This is the most common real blocker. Fixing it is a **two-step, owner-only**
action (project owner = `david.okeeffe1@coles.com.au`):

```bash
# Step 1 — create the SP role on the branch (HTTPS, via CLI, as owner)
databricks postgres create-role \
  projects/ppcs-coda-challenge/branches/<team> \
  --role-id <SP_CLIENT_ID> \
  --json '{"spec": {"identity_type": "SERVICE_PRINCIPAL", "postgres_role": "<SP_CLIENT_ID>", "auth_method": "LAKEBASE_OAUTH_V1"}}'

# check first:  databricks postgres list-roles projects/ppcs-coda-challenge/branches/<team> -o json
```

A freshly created role has **default privileges only** — step 1 alone does not
grant schema access. Then:

```sql
-- Step 2 — grant on the team schema (SQL over :5432, as a superuser role)
grant usage on schema <team> to "<SP_CLIENT_ID>";
grant all on all tables in schema <team> to "<SP_CLIENT_ID>";
```

Both steps run from a container with owner credentials — HTTPS for step 1, a
`psycopg` connection for step 2 (:5432 is reachable; see failure mode 2).

## coda-app → team-schema pairing

There is **no central mapping table.** The pairing lives only in each app's
`app.yaml` `env` as `PPCS_TEAM_SCHEMA`, set by hand at deploy time. Code
defaults to `team04` when unset. There are **8 coda apps but 10 team branches**;
the working convention is **positional: `coda-0N` → `team0N`** (teams 09/10 have
no app).

**Do NOT hardcode SP client ids here — they are sensitive infra identifiers and
this repo has a public GitHub remote.** The facilitator script
`omnigent/workshop/assign_codas.py` writes the concrete `coda-0N` → SP-client-id
→ schema table to Databricks Workspace storage, not git:

```bash
databricks workspace export \
  "/Workspace/Users/david.okeeffe1@coles.com.au/.coda/admin/ppcs_lakebase_pairings.json" \
  --format SOURCE -p DEFAULT
```

Or resolve them live (ids change if an app is recreated):

```bash
databricks apps list -o json | \
  jq -r '.[] | select(.name|startswith("coda-")) | "\(.name) \(.service_principal_client_id)"'
```

`apps get` does **not** return the env block, so confirm
`PPCS_TEAM_SCHEMA` from the deployed `app.yaml`, not the API.

## Verify with the smoketest

`ci/lakebase_smoketest.py` runs the full chain (auth → project → endpoint →
mint → SSLRequest+TLS → login → schema read/write), stopping at the first
failure with a specific diagnosis:

```bash
# as owner (should pass all the way):
uv run python ci/lakebase_smoketest.py --branch team01 --schema team01
```

Run it as the **app SP** (profile whose creds are that SP) to prove an app can
actually reach its schema after a grant. A green run as the SP is the
definitive "the app is authorized" evidence.

## Rules of the road

- Work only in your team's branch/schema. Don't touch another team's data.
- Never hardcode a DB password or connection string — the minted-credential
  path is the point, and a ticket that tempts you to bypass it is a trap.
- `create-role`/`grant` on the shared workshop Lakebase is hard to reverse and
  affects other teams — confirm the target branch before running, never guess
  the pairing.
