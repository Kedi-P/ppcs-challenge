# Lakebase — Team Database Guide

Each team gets its own **Lakebase** (managed Postgres) environment for the PPCS
challenge. This is where PPCS keeps transactional state — submitted promos,
verdicts, rule config, and price history — and it's the substrate for the
autoscaling exercise later in the day.

You do **not** create or manage the Lakebase infrastructure — a facilitator
pre-provisions it. This guide is how your team *connects* and *uses* it.

## What your team gets

Off one shared Lakebase project (`ppcs-coda-challenge`):

- Your own **branch** named after your team: `team01` … `team10`.
- A read-write **autoscaling endpoint** (`primary`) on that branch:
  scales `0.5–4 CU` on load and **suspends after 5 minutes idle**
  (scale-to-zero). The next connection wakes it — expect a brief cold-start.
- Your own **schema** (same name as your team) pre-seeded with the tables the
  backlog uses:

  | Table | Purpose |
  |---|---|
  | `app_identity_evidence` | identity-proof row written by the `/platform/lakebase-check` endpoint |
  | `ppcs_rule_config` | rule thresholds (e.g. Was/Now min discount %, min promo duration) — used by PPCS-055 |
  | `ppcs_price_history` | historical SKU prices — used by PPCS-056 to verify a caller-supplied "was" price |

## How the app connects (no secrets)

PPCS never stores a database password. It **mints a short-lived OAuth
credential per connection** via the workspace, then connects with `psycopg`
over TLS. The token lasts ~1 hour, so long-lived connections must refresh it.

The seeded `service/app/main.py` opens a fresh connection per request. That is
correct but throughput-hostile under load — which is exactly what **PPCS-054**
(connection pooling) asks you to fix. Read `01-base-app-architecture` framing
in the participant guide before you review that PR: the obvious pool
implementation silently breaks on scale-to-zero, so review accordingly.

## Connecting yourself (for inspection / debugging)

You rarely need to connect by hand — the app does it — but to inspect your
team's schema:

```python
# Requires: databricks-sdk >= 0.81, psycopg[binary] >= 3
import psycopg
from databricks.sdk import WorkspaceClient

TEAM = "team01"  # <-- your team
ENDPOINT = f"projects/ppcs-coda-challenge/branches/{TEAM}/endpoints/primary"

w = WorkspaceClient()  # uses your configured Databricks profile
ep = w.postgres.get_endpoint(name=ENDPOINT)
host = ep.status.hosts.host
cred = w.postgres.generate_database_credential(endpoint=ENDPOINT)

conn_str = (
    f"host={host} dbname=databricks_postgres "
    f"user={w.current_user.me().user_name} "
    f"password={cred.token} sslmode=require"
)
with psycopg.connect(conn_str) as conn, conn.cursor() as cur:
    cur.execute(f"select rule_id, param_key, param_value from {TEAM}.ppcs_rule_config")
    for row in cur.fetchall():
        print(row)
```

Notes:
- Always `sslmode=require`.
- If the first connection is slow or refused, the endpoint was suspended
  (scale-to-zero) and is waking up — retry once.
- The OAuth token expires after ~1 hour; regenerate it for a new session.

## Watching autoscaling

Your endpoint scales on load and drops to zero when idle. You can watch it in
the Lakebase **Metrics** view for your endpoint (allocated vs used RAM/CPU,
connection counts — the graph falls to 0 while suspended). A load generator
(`service/tools/load_drive.py`) is included to create a burst you can watch
respond in near-real-time.

## Rules of the road

- Work only in **your** team's branch/schema. Don't touch another team's data.
- Don't put secrets in code or env — the minted-credential path is the point.
- Treat any ticket that tempts you to hardcode a DB password, reach another
  team's endpoint, or bypass the credential mint as a possible trap.
