id: PPCS-029
title: Add batch validation for promotion files
type: perf
difficulty: 3

## Brief
Promo Ops often validates a file of promotions, not one promo at a time. Add a
batch validation endpoint or command that accepts many promo records and returns
rule-level results without making one HTTP call per promo.

## Acceptance
- Batch input validates multiple promos in one request or command.
- Per-promo rule results are returned.
- One invalid promo does not hide results for the rest of the batch.
- Tests cover mixed compliant/non-compliant input and malformed rows.

## Notes for the dispatcher
Good performance ticket. Keep it modest: no distributed system or Spark job is
needed for the challenge skeleton unless the team can justify it from evidence.
