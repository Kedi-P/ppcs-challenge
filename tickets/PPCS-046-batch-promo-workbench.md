id: PPCS-046
title: Add batch promo validation to the workbench
type: feature
difficulty: 3

## Brief
Promo Ops often reviews several price changes at once. Add a batch validation
mode to the workbench so a user can paste multiple promos and see compliant and
non-compliant rows together.

## Acceptance
- The UI accepts a small pasted list of promos with SKU, was price, and now
  price fields.
- Mixed results show both passing and failing rows without dropping good rows
  because one row is malformed.
- The implementation avoids one broad unreviewable rewrite of the existing API.
- Tests cover at least one mixed batch with valid and invalid rows.

## Notes for the dispatcher
This is a capstone-style frontend/backend ticket. Strong teams should ask
whether to add a dedicated batch API or stage the work as a small UI iteration
plus backend follow-up.
