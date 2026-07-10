# CI — PPCS

Two layers of CI for the PPCS app, wired in `.github/workflows/ci.yml`.

## 1. `unit` job (always runs)

Runs the pytest suite. The challenge ships ONE intentional failing seed test
(PPCS-001). CI is green when only that test is red, or when all tests pass.
Logic in `evaluate_pytest.py`.

## 2. `lakebase-ci` job (the "getting to prod" demo, for real)

On every pull request, this job:

1. **Cuts an ephemeral Lakebase branch off `production`** — a copy-on-write
   clone of the whole database, in seconds (`lakebase_branch.py create`).
2. **Runs the SQL migrations** (`service/migrations/*.sql`) against an isolated
   CI schema on that clone (`run_migrations.py`) — the real test that a schema
   change applies cleanly on prod-shaped data.
3. **Runs integration tests** against the clone endpoint.
4. **Always tears the branch down** (`lakebase_branch.py delete`), even on
   failure — so the 10-unarchived-branch limit is never exhausted.

This is the manual `ci-branch-demo.sh` cycle, automated. Migrations flow *up*
(PR clone → staging → production); production data flows *down* from the
Lakehouse via reverse-ETL. See `docs/lakebase-tenancy-and-ci.md` in the
facilitator repo for the full model.

### Enabling `lakebase-ci`

It runs only when both are set on the repo:

- **Variable** `PPCS_LAKEBASE_CI_ENABLED = true`
  (`gh variable set PPCS_LAKEBASE_CI_ENABLED --body true`)
- **Secrets** (a Databricks service principal with Lakebase branch rights):
  - `DATABRICKS_HOST`
  - `DATABRICKS_CLIENT_ID`
  - `DATABRICKS_CLIENT_SECRET`

  ```bash
  gh secret set DATABRICKS_HOST --body "https://adb-....azuredatabricks.net"
  gh secret set DATABRICKS_CLIENT_ID --body "<sp-client-id>"
  gh secret set DATABRICKS_CLIENT_SECRET --body "<sp-secret>"
  ```

Without those, only the fast `unit` job runs — safe default for forks/offline.

## Files

| File | Role |
|---|---|
| `lakebase_branch.py` | create / token / delete an ephemeral branch + endpoint |
| `run_migrations.py`  | apply `service/migrations/*.sql` to a target schema |
| `evaluate_pytest.py` | enforce the PPCS-001 baseline on the JUnit report |
| `ci-branch-demo.sh`  | manual, narrated version to drive live in the room |

## Note on the `workflow` OAuth scope

Pushing `.github/workflows/ci.yml` requires a token with the `workflow` scope.
If your `gh` token lacks it (`gh auth status` shows scopes), either run
`gh auth refresh -h github.com -s workflow` or add the workflow file via the
GitHub web UI. The `ci/` scripts themselves push fine without that scope.
