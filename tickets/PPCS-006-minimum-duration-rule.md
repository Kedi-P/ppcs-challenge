id: PPCS-006
title: Add minimum promotion duration rule
type: feature
difficulty: 2

## Brief
PPCS needs to flag promotions that run for too short a window. Add a minimum
duration rule: a promotion must run for at least 7 calendar days. The verdict
should include a separate rule result so reviewers can tell whether a promo
failed because of Was/Now discount, duration, or both.

## Acceptance
- Promo input supports `start_date` and `end_date`.
- A 6-day promotion is non-compliant for the duration rule.
- A 7-day promotion is compliant for the duration rule.
- Was/Now compliance still works independently.
- Tests cover pass, fail, and combined failure cases.

## Notes for the dispatcher
This is a feature with a schema change. Watch for date arithmetic shortcuts and
ambiguous inclusive/exclusive handling.
