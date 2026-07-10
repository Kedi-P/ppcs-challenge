#!/usr/bin/env bash
# ci-branch-demo.sh — drive the Lakebase CI/promotion ladder live.
#
# Shows, in front of the room:
#   1. the 10 team schemas living in production
#   2. cutting an ephemeral branch off production (copy-on-write, instant)
#   3. mutating/breaking the clone, proving production is untouched
#   4. tearing the clone down
#
# This is the manual, narrated version of what .github/workflows/ci.yml does
# automatically on every pull request.
#
# Prereqs: databricks CLI authenticated; DATABRICKS_CONFIG_PROFILE set;
#          `databricks psql` (needs local psql binary) OR swap the psql calls
#          for `uv run python ci/run_migrations.py` / a psycopg one-liner.
set -euo pipefail

PROJECT="${PPCS_PROJECT:-projects/ppcs-coda-challenge}"
CLONE="${1:-ci-demo}"
PROD="$PROJECT/branches/production/endpoints/primary"
CLONE_EP="$PROJECT/branches/$CLONE/endpoints/primary"

say() { printf '\n\033[1;36m== %s ==\033[0m\n' "$*"; }

say "1. Tenancy: schemas living in production"
databricks psql "$PROD" -- -c "\dn"

say "2. Cut an ephemeral branch off production (copy-on-write clone)"
databricks postgres create-branch "$PROJECT" "$CLONE" \
  --json "{\"spec\":{\"source_branch\":\"$PROJECT/branches/production\",\"ttl\":\"7200s\"}}"
databricks postgres create-endpoint "$PROJECT/branches/$CLONE" primary \
  --json '{"spec":{"endpoint_type":"ENDPOINT_TYPE_READ_WRITE","autoscaling_limit_min_cu":0.5,"autoscaling_limit_max_cu":4,"suspend_timeout_duration":"300s"}}'
echo "clone $CLONE already contains all of production's schemas + data:"
databricks psql "$CLONE_EP" -- -c "\dn"

say "3. Break the clone — mutate team01, prove production is untouched"
databricks psql "$CLONE_EP" -- -c "DELETE FROM team01.ppcs_price_history; ALTER TABLE team01.ppcs_rule_config ADD COLUMN experimental numeric;"
echo "clone row count (expect 0):"
databricks psql "$CLONE_EP" -- -c "SELECT count(*) FROM team01.ppcs_price_history;"
echo "PRODUCTION row count (unchanged):"
databricks psql "$PROD" -- -c "SELECT count(*) FROM team01.ppcs_price_history;"

say "4. Tear the clone down (unarchived-branch count drops back)"
databricks postgres delete-branch "$PROJECT/branches/$CLONE"

say "Done. On every PR, .github/workflows/ci.yml runs exactly this cycle automatically."
