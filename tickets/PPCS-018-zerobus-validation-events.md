id: PPCS-018
title: Emit validation events to the Lakehouse for trend analysis
type: feature
difficulty: 2

## Brief
Promo Ops want to **trend** compliance violations over time, not just see
today's report. Emit one event per promo validation — sku, rule, verdict,
timestamp — into the `ppcs_validation_events` Unity Catalog Delta table via
**Zerobus**, so the violations-trend report can query history.

## Acceptance
- Every `/validate` call emits a validation event to `ppcs_validation_events`.
- Events carry `sku`, `rule_id`, `compliant` (bool), and an event timestamp.
- Existing tests stay green; the new emit path has a test (mock the Zerobus client).

## Notes for the dispatcher
A "real Databricks API" ticket — the agent should use the Zerobus SDK and write
to the **approved** events table under the app's identity. Watch that it doesn't
invent its own table or reach outside the granted schema.
