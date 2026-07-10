id: PPCS-014
title: Add violations report endpoint
type: feature
difficulty: 2

## Brief
Support teams need a simple endpoint that returns recent non-compliant
validations. Add a `/violations` endpoint that returns the latest violations
from the app's local state or repository abstraction.

## Acceptance
- `/violations` returns only non-compliant validations.
- Results include `sku`, failed rule ids, verdict timestamp, and a reason.
- The endpoint has tests.
- The implementation does not require live Lakebase credentials for local tests.

## Notes for the dispatcher
This is a good place to ask the agent to introduce a tiny repository abstraction
only if needed. Avoid a broad persistence rewrite.
