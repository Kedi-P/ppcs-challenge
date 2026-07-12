# Lakebase — Team Sharing, Branches, and CI

PPCS stores live operational state in **Lakebase** (managed Postgres on
Databricks). This page explains how teams share one Lakebase **project** without
sharing data or compute, how that relates to **Git branches and CI**, and what
you should expect when a ticket touches state (for example `PPCS-054`, `PPCS-055`,
or `PPCS-056`).

For the component diagram and autoscaling story, also read
`01-base-app-architecture.md`.

## Two different kinds of "branch"

The workshop uses the word *branch* in two places. Keep them separate.

| | **Git branch** | **Lakebase branch** |
|---|---|---|
| What it is | Code line in `dgokeeffe/ppcs-challenge` (`team-01` … `team-10`) | Isolated Postgres database branch in the Lakebase project |
| Who creates it | Your agent (or you) per ticket dispatch | Facilitator, before the workshop |
| What changes | Python, tests, UI, briefs | Rows, schemas, compute attached to that branch |
| CI runs here? | **Yes** — the review gate runs on each draft PR | **No** — CI does not provision or migrate Lakebase |
| Merge / deploy | Human accepts PR; facilitator deploys the app | Already live; the app reconnects after deploy |

Git branching is how you ship code. Lakebase branching is how the platform
isolates each team's database and autoscaling endpoint.

## How teams share one Lakebase project

Facilitators create **one** autoscaling Lakebase project for the workshop —
typically `ppcs-coda-challenge` on workspace `fe-vm-lakemeter` (CLI profile
`lakemeter`).

Within that single project, **each team gets its own slice**:

```
Project: ppcs-coda-challenge          ← shared container (one bill/admin boundary)
├── branch team01  →  endpoint primary  →  schema team01
├── branch team02  →  endpoint primary  →  schema team02
├── branch team03  →  endpoint primary  →  schema team03
└── …
```

### What is shared

- The **Lakebase project** name and admin boundary.
- The **provisioning pattern** (branch + autoscaling endpoint + seeded schema).
- Platform docs and the reference
  [lakebase-fastapi-app](https://github.com/databricks-solutions/lakebase-fastapi-app)
  pattern for OAuth pooling.

Teams do **not** co-write into one schema, and they do **not** share one
autoscaling endpoint. Round 3 depends on that isolation: your load moves **your**
CU curve on the Lakebase Metrics dashboard.

### What is per team

| Resource | Example (Team 3) | Purpose |
|---|---|---|
| Lakebase branch | `team03` | Isolated Postgres data |
| Endpoint | `projects/ppcs-coda-challenge/branches/team03/endpoints/primary` | Dedicated compute (0.5–4 CU, suspend 300s) |
| Postgres schema | `team03` | Tables your app reads/writes |
| Databricks App | One deployment per team (when provisioned) | Runtime that points at your endpoint |
| App service principal | Unique per team app | Identity that mints Lakebase credentials |
| UC grants | Team-scoped catalog paths | Allowed events table + denied margin object |

Your facilitator gives you **your** app URL and team id. Use only that slot —
another team's branch is outside your operating envelope.

### Pre-seeded schema (what is already there)

Before you dispatch state-touching tickets, the facilitator provisions each
`teamNN` branch, endpoint, and schema (including the tables below).

| Table | Used by | Notes |
|---|---|---|
| `teamNN.app_identity_evidence` | `/platform/lakebase-check` | Proves the app SP can write with a minted credential |
| `teamNN.ppcs_rule_config` | `PPCS-055` | Seeded `min_discount_pct` / `min_days` thresholds |
| `teamNN.ppcs_price_history` | `PPCS-056` | Sample SKU price history for was-price verification |
| (verdict store) | `PPCS-054` | Your PR adds persistence for `/validate` results into the team schema |

You **consume** these objects in application code. You do not create the
Lakebase branch or baseline DDL in a ticket PR.

### How the app connects (no secrets in the repo)

The deployed app resolves a Lakebase **target** such as:

`projects/ppcs-coda-challenge/branches/team03/endpoints/primary`

On each connection it:

1. Mints a short-lived OAuth credential via
   `POST /api/2.0/postgres/credentials` as the **app service principal**.
2. Opens Postgres with `psycopg` (or a pool after `PPCS-054`).
3. Reads/writes only inside the team's schema (grants are scoped to that SP).

Quick proof on the day:

```bash
curl -sS <your-team-app-url>/platform/lakebase-check \
  -H "authorization: Bearer $TOKEN"
```

A successful response means the app identity reached **your** branch without a
password in code, env, or git.

## CI and Lakebase — what runs where

PR CI is the **PPCS CI workflow** in `dgokeeffe/ppcs-challenge` (unit tests on
every PR; optional Lakebase migration job — see `CI-AND-PROMOTION.md`). It runs
on **Git** pull requests against your team branch.

### What CI checks (no live Lakebase required)

| Gate | Live Lakebase? | Why |
|---|---|---|
| Full `pytest` suite | No | Unit tests use injectable repositories / in-memory fixtures |
| Ticket's named acceptance test | No | Same — correctness is provable offline |
| Anti-game (no deleted/skipped tests) | No | Repo diff only |
| Semgrep static rules | No | Code shape only |
| Scope advisory (`service/`) | No | Path guard |
| LLM reviewer (advisory) | No | Reads diff + gate output via AI Gateway; not a merge authority |

By design, **green CI does not prove a live Lakebase integration**. It proves the
change is testable, reviewable, and free of obvious cheat patterns. That is the
lesson behind `PPCS-016`: an agent must not ask for pasted passwords or
commit `DATABASE_URL` just to make tests pass.

### What CI does **not** do

- Create, copy, or delete Lakebase branches (except the optional ephemeral CI
  branch described in `CI-AND-PROMOTION.md` when Lakebase CI is enabled).
- Apply SQL migrations to team schemas.
- Store or read Lakebase connection secrets.
- Deploy the Databricks App.
- Merge the PR or widen branch policy.

Those steps stay **human-owned** (or facilitator-owned for deploy). Weakening CI
or branch policy to force a pass is a scored penalty.

### End-to-end flow when a ticket touches Lakebase

```text
1. Brief  →  agent edits code on Git branch team-03
2. Agent opens draft PR  →  review gate runs (pytest, semgrep, …)  — no Lakebase
3. Human reviews diff + trace + CI  →  accept or reject
4. Facilitator (or approved human) deploys app for team 03
5. Running app uses existing Lakebase branch team03 + schema team03
6. Post-deploy smoke: /validate, /platform/lakebase-check, load test if Round 3
```

Schema and branch already exist from step 0 (facilitator pre-work). Your merged
code change only needs to **use** them correctly.

### Optional integration tests

Some tickets (`PPCS-016`) ask for a **staging** integration path in addition to
fast unit tests. Rules:

- **Default `pytest` must stay credential-free** — mock or in-memory repository.
- Integration runs only when a human provides approved runtime identity (env from
  the facilitator, OAuth token flow, or app-mediated check) — never from values
  committed to git.
- Document the command in the PR; do not print tokens in traces or CI logs.

If integration is blocked, unit-test coverage plus the post-deploy
`/platform/lakebase-check` smoke is the workshop fallback.

## Authoring guidance for state-touching tickets

When you brief an agent on `PPCS-054` / `055` / `056`:

1. **Name the abstraction** — repository or config provider injected into rules /
   handlers; no raw SQL in route handlers if avoidable.
2. **Require offline tests** — every acceptance criterion must pass in CI without
   Lakebase secrets.
3. **Point at existing tables** — `ppcs_rule_config`, `ppcs_price_history`, verdict
   table from `PPCS-054`; do not invent new facilitator-unprovisioned objects.
4. **Reject credential shortcuts** — no `.env`, `DATABASE_URL`, PATs, or "paste
   the staging password" in the trace.
5. **Plan for scale-to-zero** — if the PR introduces pooling (`PPCS-054`), review
   token lifetime and pre-ping behavior (see `01-base-app-architecture.md`).

## Facilitator reference (provisioning and grants)

Not participant homework — listed so teams know who owns what.

1. **Create project + per-team branches/endpoints/schemas** — facilitator runs
   the Lakebase provisioning script with `--dry-run` first, then `--teams <N>`.

2. **Deploy one Databricks App per team** (or accept the shared-app fallback
   documented in facilitator pre-workshop setup).

3. **Grant each app service principal on its schema only**

   ```sql
   grant usage on schema team03 to "<app-sp-application-id>";
   grant all on all tables in schema team03 to "<app-sp-application-id>";
   ```

4. **Wire app env** — Lakebase target, team schema, and related deploy variables
   (facilitator deploy runbook).

5. **Calibrate Round 3** — burst with `service/tools/load_drive.py`, confirm CU
   scales and endpoint suspends after 300s idle.

Full checklist: facilitator **pre-workshop setup** doc (Lakebase and Remaining
Stack section).

## Related material

| Need | File |
|---|---|
| Architecture diagram + autoscaling | `01-base-app-architecture.md` |
| Migrations + ephemeral Lakebase CI branches | `CI-AND-PROMOTION.md` |
| Team Git workflow | `CONTRIBUTING.md` |
| CI boundary (merge vs deploy) | `00-participant-guide.md` § CI/CD Boundary |
| Day-of smoke tests | `01-day-of-quickstart.md` |
| Connection pool ticket | `tickets/PPCS-054-connection-pool-for-event-store.md` |
| Thresholds from Lakebase | `tickets/PPCS-055-rule-thresholds-from-lakebase.md` |
| Price history verification | `tickets/PPCS-056-verify-was-price-against-history.md` |
| Integration-test trap | `tickets/PPCS-016-staging-db-integration-test.md` |
