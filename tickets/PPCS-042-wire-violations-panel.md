id: PPCS-042
title: Wire the workbench violations panel
type: feature
difficulty: 2

## Brief
Support reviewers need the browser workbench to show recent non-compliant
validations. Wire the violations panel to a `/violations` API path and show the
latest failed validations in the UI.

## Acceptance
- `/violations` returns only non-compliant validations.
- Results include `sku`, failed rule ids, verdict timestamp, and a reason.
- Local tests do not require live Lakebase credentials.
- The UI handles empty, loading, and error states.

## Notes for the dispatcher
This can build on `PPCS-014`, but it should not force a full persistence rewrite.
Prefer a small repository abstraction or in-memory test fixture when needed.
