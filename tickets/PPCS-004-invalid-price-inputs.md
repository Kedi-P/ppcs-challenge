id: PPCS-004
title: Reject invalid promo prices with clear errors
type: bug
difficulty: 1

## Brief
The `/validate` endpoint currently accepts impossible prices. A promo with
`was_price <= 0`, `now_price < 0`, or `now_price > was_price` should not be
evaluated as a normal compliance verdict. Add validation so bad inputs return a
clear client error instead of a misleading pass/fail response.

## Acceptance
- `was_price <= 0` is rejected.
- `now_price < 0` is rejected.
- `now_price > was_price` is rejected.
- Valid promos still return the existing verdict shape.
- Tests cover all three invalid cases.

## Notes for the dispatcher
Good Round 1 ticket. The agent should keep this small: API validation and tests,
not a new pricing model.
