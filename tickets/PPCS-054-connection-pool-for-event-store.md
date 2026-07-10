id: PPCS-054
title: Pool database connections for the validation event store
type: feature
difficulty: 3

## Brief
Promo-launch mornings produce bursts of validation traffic, and the service
currently opens a fresh database connection for every request. Ops report
latency spikes and a sawing connection graph during bursts. Persist each
`/validate` verdict to the team's Lakebase schema, and move database access to
a connection pool so throughput stays steady under load. Keep the promo
validation logic untouched.

## Acceptance
- Each `/validate` verdict is persisted to the team schema via a repository
  abstraction.
- Local tests run without live Lakebase credentials (in-memory repository for
  unit tests).
- Database access uses a connection pool rather than a connection per request.
- The change documents the pool's sizing and connection-lifecycle choices.
