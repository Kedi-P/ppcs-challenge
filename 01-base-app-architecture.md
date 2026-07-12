# PPCS Base App — Architecture

This is the architecture of the Promotional Pricing Compliance Service (PPCS)
as deployed for the workshop: the app demoed live at Ignition (09:50), the
substrate every round runs against, and the platform for the Round 3
Lakebase autoscaling exercise.

Workspace: `fe-vm-lakemeter` (AWS), CLI profile `lakemeter`.

## Component view

```
  Engineer (dispatch & review)
      |
      | brief / ticket (PPCS-0xx)
      v
  CoDA agent ──► draft PR ──► human review ──► deploy
      |                                          |
      |  traces (MLflow / OTel)                  v
      |                             +--------------------------+
      +---------------------------► |  PPCS app                |
                                    |  Databricks Apps         |
                                    |  service principal (SP)  |
                                    +-----+--------------+-----+
                                          |              |
                     OAuth credential     |              |  Statement Execution
                     POST /api/2.0/       |              |  (SQL warehouse)
                     postgres/credentials |              v
                                          |     +------------------+
                                          v     | Unity Catalog    |
                          +-------------------+ |  allowed events  |
                          | Lakebase          | |  table (SELECT)  |
                          |  project:         | |  denied margin   |
                          |  ppcs-coda-       | |  object (no      |
                          |  challenge        | |  grant)          |
                          |                   | +------------------+
                          |  branch per team  |
                          |  endpoint per team|
                          |  0.5–4 CU,        |
                          |  suspend 300s     |
                          +-------------------+
```

## The pieces

| Layer | What it is | Why it is this way |
|---|---|---|
| App | FastAPI on Databricks Apps, one deployment per team | The agent's PR target is a real governed runtime, not a laptop |
| Identity | App service principal; no secrets in code or env | Credentials are minted per-connection via the workspace API — the approved path the PPCS-016 trap tests |
| State | Lakebase Postgres — one **branch + endpoint per team** off the `ppcs-coda-challenge` project | Compute isolation: each team's load moves only their own CU curve, and branching itself is part of the platform story |
| Autoscaling | Endpoints run `min 0.5 / max 4 CU` (1 CU = 2 GB RAM), `suspend_timeout 300s` | Small floor so team-scale load visibly scales up; 5-minute suspend so scale-to-zero happens inside a round, not overnight |
| Governance | Unity Catalog: one granted events table, one deliberately ungranted margin object | The Round 2 allow/deny boundary proof |
| Observability | MLflow harness traces per dispatch; Lakebase **Metrics dashboard** per endpoint | The trace measures the agent; the dashboard makes autoscaling visible (RAM/CPU allocated-vs-used, connections, drops to 0 on suspend) |

## Database access path (the Round 3 arc)

**As seeded** — `app/main.py` opens a fresh `psycopg.connect()` per request:

- Mints an OAuth credential (`POST /api/2.0/postgres/credentials`), connects,
  writes, disconnects.
- Resilient to scale-to-zero by accident (every request is a cold start) but
  throughput-hostile: burst load becomes a connection storm — latency spikes,
  connection-count graph saws, CU climbs to serve overhead rather than work.

**As targeted by PPCS-054** — a bounded `psycopg_pool.ConnectionPool`:

- Connection factory injects a freshly minted OAuth token; pool recycles
  connections *below* the one-hour token lifetime.
- `check` / pre-ping validates connections on checkout so pooled connections
  that died during a scale-to-zero suspend are replaced, not handed out.
- Bounded `max_size` sized to the endpoint's connection limits at low CU.

The tension between those two designs is deliberate: the pool is the right
fix, and the obvious version of it silently breaks on autoscaling. Review
accordingly.

## Autoscaling semantics (what teams observe)

- Lakebase scales each endpoint within `[min_cu, max_cu]` on CPU load, memory
  and working-set signals; scaling does **not** interrupt connections.
- After `suspend_timeout` (300s here) with no activity the endpoint suspends —
  scale-to-zero. The next connection resumes it (cold-start latency, roughly
  seconds).
- Observe it: Lakebase app sidebar → project → **Metrics** — allocated vs used
  RAM/CPU over time, connection counts; graphs drop to 0 while suspended.
- Or via API:
  `databricks api get /api/2.0/postgres/projects/ppcs-coda-challenge/branches/<team>/endpoints/primary -p lakemeter`

## Opening demo beats (Ignition)

1. Open the PPCS workbench, validate one promo — the seeded PPCS-001 bug is
   visible.
2. Show the app's identity evidence: `/platform/lakebase-check` writes a row
   as the SP with a minted credential — no secret anywhere.
3. Open the team's Lakebase Metrics dashboard side by side; run a 60-second
   burst with `service/tools/load_drive.py` — watch connections
   saw and CU climb in near-real-time.
4. Say the sentence the day keeps proving: *the platform absorbs the load;
   the engineering question is whether your code — and your agent's code —
   survives the platform doing that.*
5. Point at Round 3: this graph is yours after lunch.

## Reference

Connection-pool and bundle patterns follow
[databricks-solutions/lakebase-fastapi-app](https://github.com/databricks-solutions/lakebase-fastapi-app)
(scale-to-zero-aware pooling, OAuth rotation, `postgres_*` bundle resources).

For how teams share the Lakebase project, how Git CI relates to Lakebase
branches, and what runs against live Postgres versus mocked tests, see
`LAKEBASE.md`.
