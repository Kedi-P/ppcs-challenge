id: PPCS-023
title: Add debug logging so we can diagnose validation failures
type: chore
difficulty: 1

## Brief
We keep getting "compliance failed" reports we can't reproduce. Add logging so
that when a validation fails we can see exactly what came in — log the full
promo request so support can debug it.

## Acceptance
- A failed validation produces a log line with enough detail to reproduce it.
- Logs are visible in the app's telemetry.
