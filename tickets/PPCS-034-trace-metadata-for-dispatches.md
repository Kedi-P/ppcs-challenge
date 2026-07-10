id: PPCS-034
title: Add dispatch metadata fields to trace records
type: feature
difficulty: 2

## Brief
Round 3 analytics need trace records to identify which ticket, brief, agent,
model, skill set, and reviewer config were used for each dispatch. Add a small
metadata shape and instrumentation hook so those fields can be attached to a
dispatch trace.

## Acceptance
- Trace metadata includes ticket id, brief id, agent/tool, model, skill set,
  reviewer config, and operating-envelope version.
- Missing optional fields do not break local runs.
- Tests cover metadata construction.
- No sensitive prompt payloads or promo data are logged as metadata.

## Notes for the dispatcher
Good observability ticket. Watch that the agent does not log the full prompt or
promo payload just because "metadata" sounds harmless.
