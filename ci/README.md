# CI — PPCS

Two layers of CI for the PPCS app, wired in `.github/workflows/ci.yml`.

## 1. `unit` job (always runs)

Runs the pytest suite. The challenge ships ONE intentional failing seed test
(PPCS-001). CI is green when only that test is red, or when all tests pass.
Logic in `evaluate_pytest.py`.

## 2. `lakebase-ci` — where the live cycle actually runs

See **`../LAKEBASE-DEPLOYMENTS.md`** for the mermaid map. The "getting to prod"
cycle — cut an ephemeral Lakebase branch off `production`, migrate an isolated
CI schema on the clone, test, always tear down — is modelled in two places:

- **`.github/workflows/ci.yml` (`lakebase-ci` job): REFERENCE ONLY.** It does
  NOT run in the workshop. GitHub-hosted runners live in GitHub's cloud and have
  no network path to the firewalled Lakebase workspace, and we will not put
  Databricks credentials in a public repo. It stays as the readable reference
  and is gated off by default.
- **`azure-pipelines.yml` (`lakebase_ci` stage): THE LIVE PIPELINE.** Runs on a
  self-hosted Azure DevOps agent pool INSIDE the Coles perimeter, where the agent
  can reach Lakebase and the service-principal secret comes from an ADO variable
  group / Key Vault — never from the public repo.

Both invoke the exact same portable scripts below, so the logic is defined once.

### Enabling the live Azure DevOps pipeline

1. Create a **self-hosted agent pool** inside the perimeter (agents must be able
   to reach `*.database.<region>.azuredatabricks.net`). Set its name in
   `azure-pipelines.yml` (`pool.name`, marked `<<CHANGE>>`).
2. Create an ADO **variable group** `ppcs-lakebase-ci` (Key Vault-backed
   recommended) with:
   - `DATABRICKS_HOST`
   - `DATABRICKS_CLIENT_ID`
   - `DATABRICKS_CLIENT_SECRET` (mark secret)
   - `PPCS_LAKEBASE_CI_ENABLED = true`
3. Create an ADO pipeline of type **GitHub**, point it at
   `dgokeeffe/ppcs-challenge` via a GitHub service connection. ADO manages the
   PR/branch triggers declared in the YAML.

Until `PPCS_LAKEBASE_CI_ENABLED = true`, only the `unit` stage runs.

The GitHub `lakebase-ci` job stays gated off (do NOT set
`PPCS_LAKEBASE_CI_ENABLED` as a GitHub variable / do NOT add Databricks secrets
to this public repo).

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
